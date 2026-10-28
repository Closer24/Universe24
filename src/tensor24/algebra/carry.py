"""Rule3's carry, the one place a division is written, and the whethers made of its quotient."""

from typing import Any

Z = Any  # a whole number, or a numpy array of Python integers: the same code serves both


def carry(n: Z, d: Z, r: Z) -> tuple[Z, Z]:
    """Rule3: n + r = q d + r' with 0 <= r' < d, d a teeth count of at least 1; q leaves, r' stays."""
    u = n + r
    return u // d, u % d


def nonneg(n: Z) -> Z:
    """The one whether: 1 where n is at least 0 and 0 below, the quotient of n by n n + 1."""
    q, _ = carry(n, n * n + 1, 0)
    return q + 1


def choose(k: Z, x: Z, y: Z) -> Z:
    """The choice by the bit k: x where k is 1, y where k is 0."""
    return k * x + (1 - k) * y


def home(w: Z, go: Z) -> Z:
    """The fine tooth's home at the going go: (w - go) div 2, the 2 the order of the negation that flips the tooth."""
    q, _ = carry(w - go, 1 + 1, 0)
    return q


def flip(r: Z, w: Z) -> Z:
    """The fine tooth reflected at a negation and at the turnover, the going advanced with it: w - 1 - r."""
    return w - 1 - r
