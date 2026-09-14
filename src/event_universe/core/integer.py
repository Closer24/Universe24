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
