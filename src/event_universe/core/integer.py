"""Shared domain-neutral working-register bound."""

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
