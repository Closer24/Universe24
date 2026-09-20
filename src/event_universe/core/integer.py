"""Domain-neutral integer arithmetic: the working-register bound and the Beam
Law's integer primitives; callers own payload bounds and operation costs."""

MAX_WORK_INT = (1 << 63) - 1


def checked_work(value: int) -> int:
    """Bound intermediate arithmetic to a signed 64-bit working register."""
    if type(value) is not int:
        raise TypeError("integer intermediate required")
    if not -MAX_WORK_INT <= value <= MAX_WORK_INT:
        raise OverflowError("64-bit intermediate range exceeded")
    return value


def bounded_gcd(first: int, second: int) -> int:
    """Euclid on checked magnitudes; 128 divisions is a fixed upper bound."""
    a, b = abs(checked_work(first)), abs(checked_work(second))
    for _ in range(128):
        if b == 0:
            return a
        a, b = b, a % b
    raise ArithmeticError("bounded gcd iteration limit exceeded")


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


def reduced(numerator: int, denominator: int) -> tuple[int, int]:
    """A rational as the pair (n, d) in lowest terms with d positive."""
    common = bounded_gcd(abs(numerator), denominator) or 1
    return numerator // common, denominator // common


def rational_sum(terms: list[tuple[int, int]]) -> tuple[int, int]:
    """The exact sum of rationals (n, d), reduced: a report of the books
    and, since the columns of 2026-09-20, a measured event's charge in a
    column over the families it holds."""
    numerator, denominator = 0, 1
    for n, d in terms:
        numerator, denominator = reduced(numerator * d + n * denominator, denominator * d)
    return numerator, denominator


def by_clock(age: int, numerator: int, denominator: int) -> int:
    """What the whole part of age x numerator / denominator gains at the
    self-creation that takes the age from `age` to `age + 1`: a rate read
    off a clock, exact on average, with no remainder kept anywhere. Where
    the rate is constant this is `by_drive` (below) with the remainder on
    the reader's record; the clock's turn, the release, the lamp and the
    owed count read a rate no push changes and keep this form."""
    if denominator < 1:
        raise ValueError("positive denominator required")
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


def by_drive(drive: int, rate: int, denominator: int) -> tuple[int, int]:
    """The whole part of an accumulated SIGNED rate on the reader's own
    record (the model owner's decision of 2026-09-20, record 108: one count
    primitive for a rate that may change; signed since record 126, the
    same day: a rate that reverses discharges what it had accumulated
    before it counts the other way): `drive` gains `rate` at this
    self-creation, and the count gains +1 when the drive reaches
    `denominator` and -1 when it reaches `-denominator`, that much
    subtracted with the count's sign. Returns (the count gained, -1, 0 or
    +1, and the drive after). With a constant rate of one sign the count
    fires exactly where `by_clock(n - 1, |rate|, denominator)` is 1 over
    the self-creations n, with the rate's sign, and the drive is `sign x
    (n x |rate| mod denominator)`, the remainder `by_clock` keeps nowhere;
    the count gained is one at most whenever `|rate| < denominator`, and
    |drive| stays below `denominator` from then on (a drive earned at a
    larger rate fires one at each following self-creation until it
    does). With a rate that changes sign the drive is the signed sum of
    the rates since the last count, so a reversal first cancels the
    distance driven the other way and counts nothing until the sum
    reaches the denominator on the new side."""
    if denominator < 1:
        raise ValueError("positive denominator required")
    drive += rate
    if drive >= denominator:
        return 1, drive - denominator
    if drive <= -denominator:
        return -1, drive + denominator
    return 0, drive


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
