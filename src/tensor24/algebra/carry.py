"""Rule3's carry, the one place a division is written, and the fine tooth's flip at the mirror."""

from typing import Any

Z = Any  # a whole number, or a numpy array of Python integers: the same code serves both


def carry(n: Z, d: Z, r: Z) -> tuple[Z, Z]:
    """Rule3: n + r = q d + r' with 0 <= r' < d, d a teeth count of at least 1; q leaves, r' stays."""
    u = n + r
    return u // d, u % d


def flip(r: Z, w: Z) -> Z:
    """The fine tooth reflected in its teeth w, the mirror's: w - 1 - r, within [0, w) where r is."""
    return w - 1 - r


def lit(x: Z) -> Z:
    """1 where x is not 0 and 0 where it is, by one carry: x^4 + 1 <= x^2 + x^4 < 2 (x^4 + 1) wherever x is not 0."""
    square = x * x
    found, _ = carry(square + square * square, square * square + 1, 0)
    return found
