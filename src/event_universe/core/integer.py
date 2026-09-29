"""Domain-neutral integer arithmetic: the working bound (the host's integer bound) and the Beam Law's integer primitives; callers own payload bounds and operation costs."""

import sys

MAX_WORK_INT = sys.maxsize


def checked_work(value: int) -> int:
    """Bound intermediate arithmetic to the working bound, the host's signed integer range."""
    if type(value) is not int:
        raise TypeError("integer intermediate required")
    if not -MAX_WORK_INT <= value <= MAX_WORK_INT:
        raise OverflowError("the working bound's intermediate range exceeded")
    return value


def bounded_gcd(first: int, second: int) -> int:
    """Euclid on checked magnitudes; twice the width's bits of divisions is a fixed upper bound."""
    a, b = abs(checked_work(first)), abs(checked_work(second))
    for _ in range(2 * MAX_WORK_INT.bit_length()):
        if b == 0:
            return a
        a, b = b, a % b
    raise ArithmeticError("bounded gcd iteration limit exceeded")


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
