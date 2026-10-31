"""MIRACLE_A's exact rationals: a rational is a pair of whole numbers (n, d), d >= 1, kept reduced by Euclid's
carries. No fractions module, no true division, no float: Rule3's carry (tensor24.algebra.carry.carry) is the one
division, in the reduction and in the reading of a rational as its count and tooth, n = q d + t.
The reduction is a loop of carries: a reading's tool of the probe, never an act's operation (the act holds no loop), so
the widths it reports are the least an exact form can hold; the act's own unreduced form holds more (MIRACLE_A 3.3)."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("tree", "src")))
sys.path.insert(0, str(HERE.joinpath("tree")))
sys.set_int_max_str_digits(0)

from tensor24.algebra.carry import carry  # noqa: E402


def gcd(a, b):
    """Euclid by Rule3's carries, b >= 1: the greatest common divisor (a reading's loop, not an act's)."""
    while b != 0:
        _, r = carry(a, b, 0)
        a, b = b, r
    return a


class R:
    """An exact rational n / d with d >= 1, reduced; whole numbers with + and * on either side."""

    __slots__ = ("n", "d")

    def __init__(self, n, d=1):
        n, d = int(n), int(d)
        assert d >= 1, d  # a reading: every dial the exact form divides by is positive by the structure
        g = gcd(n, d)
        self.n, self.d = carry(n, g, 0)[0], carry(d, g, 0)[0]

    def __add__(self, o):
        if isinstance(o, R):
            return R(self.n * o.d + o.n * self.d, self.d * o.d)
        return R(self.n + int(o) * self.d, self.d)

    __radd__ = __add__

    def __neg__(self):
        return R(-self.n, self.d)

    def __sub__(self, o):
        return self + (-o if isinstance(o, R) else -int(o))

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if isinstance(o, R):
            return R(self.n * o.n, self.d * o.d)
        return R(self.n * int(o), self.d)

    __rmul__ = __mul__

    def __eq__(self, o):
        if isinstance(o, R):
            return self.n == o.n and self.d == o.d
        return self.d == 1 and self.n == int(o)

    def __hash__(self):
        return hash((self.n, self.d))

    def __repr__(self):
        return f"{self.n}/{self.d}"


def lift(x):
    """A whole number, or an R, as an R."""
    return x if isinstance(x, R) else R(x, 1)


def over(x, y):
    """x / y exactly, y > 0: the product with y's reciprocal, no division but the reduction's carries."""
    x, y = lift(x), lift(y)
    assert y.n >= 1, y  # the dial is positive by the structure (D > 0, kappa a sum of squares at positive factors)
    return R(x.n * y.d, x.d * y.n)


def bits(x):
    """The bits the rational holds: the wider of its numerator and its denominator."""
    x = lift(x)
    return max(int(abs(x.n)).bit_length(), x.d.bit_length())


def count_tooth(x):
    """The rational read as the engine reads a pair: its count q and tooth t at its own dial d, n = q d + t, 0 <= t < d."""
    x = lift(x)
    q, t = carry(x.n, x.d, 0)
    return q, t, x.d
