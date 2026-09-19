"""Domain-neutral integer arithmetic; callers own payload bounds and operation costs."""

from collections.abc import Iterable

MAX_WORK_INT = (1 << 63) - 1


def checked_work(value: int) -> int:
    """Bound intermediate arithmetic to a signed 64-bit working register."""
    if type(value) is not int:
        raise TypeError("integer intermediate required")
    if not -MAX_WORK_INT <= value <= MAX_WORK_INT:
        raise OverflowError("64-bit intermediate range exceeded")
    return value


def signed_divrem(value: int, denominator: int) -> tuple[int, int]:
    """Divide toward zero and retain a remainder with the dividend's sign."""
    checked_work(value)
    checked_work(denominator)
    if denominator < 1:
        raise ValueError("positive denominator required")
    magnitude, residue = divmod(abs(value), denominator)
    sign = -1 if value < 0 else 1
    return sign * magnitude, sign * residue


def ceil_div(numerator: int, denominator: int) -> int:
    """Round a nonnegative ratio up, retaining the bounded adjusted-numerator contract."""
    checked_work(numerator)
    checked_work(denominator)
    if numerator < 0 or denominator < 1:
        raise ValueError("nonnegative numerator and positive denominator required")
    return checked_work(numerator + denominator - 1) // denominator


def checked_sum(values: Iterable[int]) -> int:
    """Sum in order, rejecting intermediate overflow even if later terms cancel it.

    Physical callers supply a fixed, schema-bounded number of components.
    """
    total = 0
    for value in values:
        total = checked_work(total + value)
    return total


def add_components(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Add equally sized decoded components, checking each result before returning."""
    return tuple(checked_work(a + b) for a, b in zip(left, right, strict=True))


def subtract_components(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Subtract equally sized decoded components without scalar broadcasting."""
    return tuple(checked_work(a - b) for a, b in zip(left, right, strict=True))


def dot_product(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    """Multiply and accumulate in order, checking products before any cancellation."""
    return checked_sum(checked_work(a * b) for a, b in zip(left, right, strict=True))


def cross_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return the right-handed 3D cross product with bounded products and differences."""
    if len(left) != 3 or len(right) != 3:
        raise ValueError("cross product requires exactly three components")
    return tuple(
        checked_work(checked_work(left[a] * right[b]) - checked_work(left[b] * right[a]))
        for a, b in ((1, 2), (2, 0), (0, 1))
    )


def bounded_gcd(first: int, second: int) -> int:
    """Euclid on checked magnitudes; 128 divisions is a fixed upper bound."""
    a, b = abs(checked_work(first)), abs(checked_work(second))
    for _ in range(128):
        if b == 0:
            return a
        a, b = b, a % b
    raise ArithmeticError("bounded gcd iteration limit exceeded")


def reduced_ratio(numerator: int, denominator: int) -> tuple[int, int]:
    """The ratio in lowest terms with a positive denominator, checked."""
    checked_work(numerator)
    if checked_work(denominator) <= 0:
        raise ValueError("positive rational denominator required")
    divisor = bounded_gcd(numerator, denominator)
    return numerator // divisor, denominator // divisor


def integer_root(value: int) -> int:
    """The integer square root, the floor, exact: Newton's iteration on
    integers from a power-of-two estimate (no float anywhere)."""
    checked_work(value)
    if value < 0:
        raise ValueError("integer root of a negative value")
    if value < 2:
        return value
    estimate = 1 << ((value.bit_length() + 1) // 2)
    while True:
        better = (estimate + value // estimate) // 2
        if better >= estimate:
            return estimate
        estimate = better


def by_clock(age: int, numerator: int, denominator: int) -> int:
    """What the whole part of age x numerator / denominator gains at the
    self-creation that takes the age from `age` to `age + 1`: a rate read
    off a clock, exact on average, with no remainder kept anywhere."""
    if denominator < 1:
        raise ValueError("positive denominator required")
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


def apportion_whole(total: int, weights: list[int], first: int) -> list[int]:
    """`total` shared over the entries in proportion to `weights`, exact in
    whole numbers: the floors, then the units left to the largest
    remainders, ties broken in index order counted from `first`. Nothing
    without weights."""
    divisor = sum(weights)
    if divisor <= 0 or total <= 0:
        return [0] * len(weights)
    shares = [total * weight // divisor for weight in weights]
    remainders = [
        total * weight - share * divisor for weight, share in zip(weights, shares, strict=True)
    ]
    left = total - sum(shares)
    order = sorted(range(len(weights)), key=lambda k: (-remainders[k], (k - first) % len(weights)))
    for index in order[:left]:
        shares[index] += 1
    return shares
