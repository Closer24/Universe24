"""Domain-neutral integer arithmetic: the working-register bound and the Beam
Law's integer primitives; callers own payload bounds and operation costs."""

from collections.abc import Sequence

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
    off a clock, the first difference of a floor, with no remainder kept
    anywhere. Since the fraction-free law (2026-09-20, BEAM_LAW note 41)
    every count of a body is `by_drive` on an accumulator of the body's
    record, and this is its constant-rate identity: from an empty
    accumulator at age 0, `by_drive` gains `by_clock(k - 1, n, d)` at the
    k-th self-creation and holds `(k n) mod d` after it while the rate is
    constant (`tests/test_fraction_free.py` (a)); a row's phase per
    interval of age (a count on a row, not on a body: `by_clock_rows`)
    and the turn by momentum (a count against the record's own count of
    Links) keep this form, and the readings tools derive the constant-rate
    counts by it."""
    if denominator < 1:
        raise ValueError("positive denominator required")
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


def by_drive(drive: int, rate: int, denominator: int, at_most: int = 0) -> tuple[int, int]:
    """The one count primitive of the Beam Law (the model owner's record
    108 of 2026-09-20, "a generic solution if he can"; the step drive of
    the same day, and since the fraction-free law of that day, BEAM_LAW
    note 41, every count of a body): an accumulator on the reader's own
    record gains `rate` at this self-creation, the count is the whole part
    the accumulator then holds in units of `denominator`, that much is
    subtracted, and the remainder stays in the accumulator, bounded below
    the denominator, its one owner. Returns (the count gained, the
    accumulator after). A signed rate (the step drive: `rate` the momentum
    component, signed since record 126) counts with its sign, -1 when the
    accumulator reaches -denominator: the accumulator is then the signed
    sum of the rates since the last count, so a rate that reverses first
    cancels what it had accumulated the other way and counts nothing until
    the sum reaches the denominator on the new side; an unsigned rate
    (every other count: the owed count, the release, the lamp, the turn,
    the push per column) keeps the accumulator in
    [0, denominator). `at_most`, when positive, caps the count gained at
    one self-creation and keeps the rest in the accumulator, the step's
    rule (one Link per interval: a drive earned at a larger momentum fires
    one at each following self-creation until it is spent); 0, the
    default, takes the whole part. With a constant rate of one sign from
    an empty accumulator the count fires exactly where `by_clock(n - 1,
    |rate|, denominator)` does over the self-creations n, with the rate's
    sign, and the accumulator is `sign x (n x |rate| mod denominator)`,
    the remainder `by_clock` keeps nowhere; where the rate changes the
    count is the whole part of the sum of the rates, exact over any
    period, which `by_clock` at the current rate is not."""
    if denominator < 1:
        raise ValueError("positive denominator required")
    drive += rate
    count = abs(drive) // denominator
    if at_most and count > at_most:
        count = at_most
    if drive < 0:
        count = -count
    return count, drive - count * denominator


def signed_inner(
    left: Sequence[int], right: Sequence[int], signs: Sequence[int], bound: int | None = None
) -> int:
    """The signed inner product of two integer vectors, the sum over k of
    signs[k] x left[k] x right[k]: a vector, a declared diagonal matrix of
    +1 and -1, a vector (the bilinear operation of the law; the model
    owner's order of 2026-09-21, "not a square in the code but a vector
    operation", record 173 of the log of 2026-09-20). The click's weight
    is the pointer's inner product with itself, `signed_inner((X, Y), (X,
    Y), (1, 1))`, and nothing is squared as a step of its own. Python
    integers, exact; a boolean, a float, vectors of different lengths and
    a sign other than +1 or -1 are refused. With a `bound` (the caller's
    register; the coupling's bound is MOMENTUM_BOUND) every component is
    within +-bound, every product is tested by division before it is
    formed and every partial sum is within the bound after every
    component, refused beyond it as the law's other bounds are; without a
    bound the sum is exact and unbounded (the apparatus's layer, whose
    weights are the host's reports: a pair's pass 2^116 and a GHZ
    triple's 2^174)."""
    if not len(left) == len(right) == len(signs):
        raise ValueError("signed inner product of vectors of different lengths")
    if bound is not None and (type(bound) is not int or bound < 1):
        raise ValueError("positive integer bound required")
    total = 0
    for index, (a, b, sign) in enumerate(zip(left, right, signs, strict=True)):
        if type(a) is not int or type(b) is not int or type(sign) is not int:
            raise TypeError(f"integer components and signs required at component {index}")
        if sign != 1 and sign != -1:
            raise ValueError(f"a declared sign is +1 or -1, not {sign} at component {index}")
        if bound is not None:
            if abs(a) > bound or abs(b) > bound:
                raise OverflowError(f"component {index} exceeds the integer bound {bound}")
            # The product tested by division before it is formed.
            if b and abs(a) > bound // abs(b):
                raise OverflowError(
                    f"the product at component {index} exceeds the integer bound {bound}"
                )
        total += sign * a * b
        if bound is not None and abs(total) > bound:
            raise OverflowError(f"the sum through component {index} exceeds the integer bound {bound}")
    return total


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
