"""The ground every proofs_ module of this folder stands on (the owner's order of 2026-10-04, 07:50 UTC, "that all the proofs be checked too, clearly"; the advisor's design lines, #1793 comment 5977935062): Rule3's coefficients as rule3.py holds them, so the checks and the derivations share one Rule3; exact arithmetic in Python's integers and fractions.Fraction; the angles of every trigonometric identity as unit Gaussian rationals from Pythagorean pairs, so that a trigonometric identity in the law's integers is a polynomial identity checked exactly at random rational witnesses with the symmetric cases forced; the residual test of an expansion's order, the residual against the exact function at two step sizes whose ratio is 2^order; and the read of a Node with Link factors (The clock is the Node's, the tension is the Link's). No new dependency, nothing of event_universe, no file of a run, no number of nature.

A check is a function `check_<name>()` of a proofs_ module returning `(True, computed)` where the identity it names holds (exactly, or to the order the law states) and `(False, computed)` where it does not; it raises nothing on a failure, so the gate test prints the computed object beside the statement it quotes. `python tools/derivations/proofs_<module>.py` prints every verdict of the module.
"""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Callable, Sequence
from fractions import Fraction
from pathlib import Path
from types import ModuleType

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402

PORTS, AXES = rule3.PORTS, rule3.AXES
Check = tuple[bool, object]
Number = int | Fraction
SEED = 24  # every witness drawn from one seed, so a failure reproduces


class Gaussian:
    """A Gaussian rational x + i y with exact parts: the arithmetic of the plane record (re, im) and of the unit angles."""

    __slots__ = ("re", "im")

    def __init__(self, re: Number = 0, im: Number = 0) -> None:
        self.re, self.im = Fraction(re), Fraction(im)

    def __add__(self, other: Gaussian) -> Gaussian:
        return Gaussian(self.re + other.re, self.im + other.im)

    def __sub__(self, other: Gaussian) -> Gaussian:
        return Gaussian(self.re - other.re, self.im - other.im)

    def __neg__(self) -> Gaussian:
        return Gaussian(-self.re, -self.im)

    def __mul__(self, other: Gaussian | Number) -> Gaussian:
        if isinstance(other, Gaussian):
            return Gaussian(
                self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re
            )
        return Gaussian(self.re * other, self.im * other)

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Gaussian) and self.re == other.re and self.im == other.im

    def __hash__(self) -> int:
        return hash((self.re, self.im))

    def __repr__(self) -> str:
        return f"({self.re} + {self.im} i)"

    def conj(self) -> Gaussian:
        return Gaussian(self.re, -self.im)

    def abs2(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def inverse(self) -> Gaussian:
        norm = self.abs2()
        return Gaussian(self.re / norm, -self.im / norm)

    def __pow__(self, power: int) -> Gaussian:
        base, result = (self if power >= 0 else self.inverse()), Gaussian(1, 0)
        for _ in range(abs(power)):
            result = result * base
        return result

    def __truediv__(self, other: Gaussian | Number) -> Gaussian:
        if isinstance(other, Gaussian):
            return self * other.inverse()
        return Gaussian(self.re / other, self.im / other)

    def to_complex(self) -> complex:
        return complex(float(self.re), float(self.im))


ONE, IMAGINARY_UNIT = Gaussian(1, 0), Gaussian(0, 1)


def angle(m: int, n: int) -> Gaussian:
    """The unit Gaussian rational e^(i phi) of the Pythagorean pair (m, n): cos phi = (m^2 - n^2) / (m^2 + n^2), sin phi = 2 m n / (m^2 + n^2), exactly on the circle (the instruments' rational angles, The integer-exact constructions (3))."""
    norm = m * m + n * n
    return Gaussian(Fraction(m * m - n * n, norm), Fraction(2 * m * n, norm))


def cos_sin(unit: Gaussian) -> tuple[Fraction, Fraction]:
    return unit.re, unit.im


def draw_angle(draw: random.Random, size: int = 12) -> Gaussian:
    """A random rational angle, no quadrant excluded."""
    while True:
        m, n = draw.randint(-size, size), draw.randint(-size, size)
        if m * m + n * n:
            return angle(m, n)


SYMMETRIC_ANGLES = (angle(1, 0), angle(0, 1), angle(1, 1), angle(1, -1), angle(2, 1), angle(3, 1))
# e^(i phi) at phi = 0, pi, pi / 2, -pi / 2 and the two Pythagorean angles of (3, 4, 5) and (5, 12, 13)


def angles(draw: random.Random, count: int) -> list[Gaussian]:
    """`count` angles: the symmetric cases first (0, pi, the quarter turns, the Pythagorean pair), then random ones."""
    found = list(SYMMETRIC_ANGLES)
    while len(found) < count:
        found.append(draw_angle(draw))
    return found[:count]


def rational(draw: random.Random, size: int = 50, denominators: int = 7) -> Fraction:
    return Fraction(draw.randint(-size, size), draw.randint(1, denominators))


def pairs(draw: random.Random, count: int, with_symmetric: bool = True) -> list[tuple[int, int]]:
    """Family pairs [num, den] with 0 < num <= den: light [1, 1], the toy's [2, 3], the shipped matter pair's shape [4000, 6000] and the exact bands [1, 2] first, then random ones."""
    found = [(1, 1), (2, 3), (4000, 6000), (1, 2), (5760, 6000)] if with_symmetric else []
    while len(found) < count:
        den = draw.randint(1, 60)
        found.append((draw.randint(1, den), den))
    return found[:count]


def order_of(residual: Callable[[float], float], step: float) -> float:
    """log2 of the residuals' ratio at the steps h and h / 2: the order of the remainder's leading term."""
    coarse, fine = abs(residual(step)), abs(residual(step / 2))
    if fine == 0.0:
        return math.inf
    return math.log2(coarse / fine)


def has_order(
    residual: Callable[[float], float],
    order: int,
    step: float = 0.1,
    tolerance: float = 0.2,
    floor: float = 1e-13,
) -> tuple[bool, list[float]]:
    """Whether the residual's leading term is of the stated order: the ratio at (h, h / 2) and at (h / 2, h / 4) both 2^order within the tolerance in log2; a residual at the rounding's floor at every step is an expansion exact to every order and holds; returns the verdict and the two measured orders."""
    if all(abs(residual(step / 2**i)) <= floor for i in range(3)):
        return True, [math.inf, math.inf]
    measured = [order_of(residual, step), order_of(residual, step / 2)]
    return all(abs(found - order) <= tolerance for found in measured), measured


def wave(amplitude: Number, exponent: Gaussian) -> Fraction:
    """Re(A e^(i phi)) for the unit e^(i phi): a plane wave's level, exact."""
    return Fraction(amplitude) * exponent.re


def plane_wave_levels(
    amplitude: Number,
    waves: Sequence[Gaussian],
    rotation: Gaussian,
    nodes: Sequence[tuple[int, int, int]],
    interval: int,
) -> list[Fraction]:
    """A cos(k . x - omega t) at every Node x listed, at the interval t, with e^(i k_a) the units `waves` and e^(i omega) the unit `rotation`."""
    found = []
    for x, y, z in nodes:
        phase = (waves[0] ** x) * (waves[1] ** y) * (waves[2] ** z) * (rotation ** (-interval))
        found.append(wave(amplitude, phase))
    return found


def read(
    arrivals: Sequence[Sequence[int]],
    clocks: Sequence[Number],
    factors: Sequence[Sequence[Number]],
    num: int,
    den: int,
    gamma: int,
) -> tuple[Fraction, list[list[Fraction]], list[Fraction], list[Fraction]]:
    """The law's read at every Node (The clock is the Node's, the tension is the Link's): the Node's pace p_i = p_0(i)^2 / Gamma, the Link's read coefficient R_ij = 2 num p_i^2 q_ij^2 / Gamma^2 through each Port and the self coefficient S_i = 12 den Gamma^2 - 12 (den - num) p_0(i)^2 - SUM over the six Ports of R_ij; returns (w, R, S, p). At every q_ij = Gamma and p_a = p_i it is rule3.coefficients' own (checked in proofs_form)."""
    wall = Fraction(6 * den * gamma * gamma)
    node_paces = [Fraction(clock) ** 2 / gamma for clock in clocks]
    reads, selves = [], []
    for i in range(len(arrivals)):
        row = [2 * num * node_paces[i] ** 2 * Fraction(q) ** 2 / (gamma * gamma) for q in factors[i]]
        reads.append(row)
        selves.append(12 * den * gamma * gamma - 12 * (den - num) * Fraction(clocks[i]) ** 2 - sum(row))
    return wall, reads, selves, node_paces


def apply_read(
    arrivals: Sequence[Sequence[int]],
    reads: Sequence[Sequence[Fraction]],
    selves: Sequence[Fraction],
    levels: Sequence[Number],
) -> list[Fraction]:
    """(S_i a_i + SUM over the six Ports of R_ij a_j) at every Node: w times the line's right side before the level before."""
    return [
        selves[i] * Fraction(levels[i])
        + sum(reads[i][port] * Fraction(levels[j]) for port, j in enumerate(ports))
        for i, ports in enumerate(arrivals)
    ]


def step_line(
    arrivals: Sequence[Sequence[int]],
    reads: Sequence[Sequence[Fraction]],
    selves: Sequence[Fraction],
    wall: Fraction,
    now: Sequence[Number],
    before: Sequence[Number],
) -> list[Fraction]:
    """The line without its division: a_next = (S a_now + SUM R a_j) / w - a_before, in the rationals."""
    return [
        total / wall - Fraction(b)
        for total, b in zip(apply_read(arrivals, reads, selves, now), before, strict=True)
    ]


def step_integer(
    arrivals: Sequence[Sequence[int]],
    reads: Sequence[Sequence[Fraction]],
    selves: Sequence[Fraction],
    wall: Fraction,
    now: Sequence[int],
    before: Sequence[int],
    remainders: Sequence[int],
) -> tuple[list[int], list[int]]:
    """The law in one line with the remainder kept: w a_next + r' = S a_now + SUM R a_j - w a_before + r, 0 <= r' < w, the quotient the floor (the coefficients integers here)."""
    levels, carried = [], []
    for total, b, r in zip(apply_read(arrivals, reads, selves, now), before, remainders, strict=True):
        numerator = total - wall * b + r
        assert numerator.denominator == 1 and wall.denominator == 1
        quotient, remainder = divmod(numerator.numerator, wall.numerator)
        levels.append(quotient)
        carried.append(remainder)
    return levels, carried


def chain_nodes(count: int) -> list[tuple[int, int, int]]:
    return [(x, 0, 0) for x in range(count)]


def box_index(shape: tuple[int, int, int], x: int, y: int, z: int) -> int:
    """The index of the Node (x, y, z) on a periodic box, the coordinates taken modulo the shape."""
    n_x, n_y, n_z = shape
    return ((x % n_x) * n_y + (y % n_y)) * n_z + (z % n_z)


def box_nodes(shape: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    n_x, n_y, n_z = shape
    return [(x, y, z) for x in range(n_x) for y in range(n_y) for z in range(n_z)]


def box_arrivals(shape: tuple[int, int, int]) -> list[list[int]]:
    """The six neighbour indices of every Node of a periodic box in Port order +x, -x, +y, -y, +z, -z; an axis of one layer folds onto the Node itself."""
    return [
        [
            box_index(shape, x + 1, y, z),
            box_index(shape, x - 1, y, z),
            box_index(shape, x, y + 1, z),
            box_index(shape, x, y - 1, z),
            box_index(shape, x, y, z + 1),
            box_index(shape, x, y, z - 1),
        ]
        for x, y, z in box_nodes(shape)
    ]


def link_factors(
    arrivals: Sequence[Sequence[int]], draw: random.Random | None, gamma: int, spread: int = 0
) -> list[list[int]]:
    """One factor q_ij = Gamma - t per Link, read the same from both ends; a self-Link of a folded axis one number of its own per axis; `draw` None or `spread` 0 gives Gamma on every Link (no tension)."""
    table: dict[tuple[int, int, int], int] = {}
    found = []
    for i, ports in enumerate(arrivals):
        row = []
        for port, j in enumerate(ports):
            key = (min(i, j), max(i, j), port // 2 if i == j else -1)
            if key not in table:
                table[key] = gamma - (draw.randint(-spread, spread) if draw and spread else 0)
            row.append(table[key])
        found.append(row)
    return found


def integer_witness(
    draw: random.Random, arrivals: Sequence[Sequence[int]], gamma: int, tension: bool
) -> tuple[int, list[int], list[list[int]]]:
    """A read whose coefficients are integers, for the checks of the integer step: the clocks Gamma x j_i with j_i in 1..3, so that p_i = p_0^2 / Gamma = Gamma j_i^2 and R_ij = 2 num j_i^4 q_ij^2 are integers for any integer Link factor q_ij (a clock above Gamma is a hill's; the identities checked are algebraic in the paces and hold on either side); returns (Gamma, clocks, factors)."""
    clocks = [gamma * draw.randint(1, 3) for _ in arrivals]
    factors = link_factors(
        arrivals, draw if tension else None, gamma, spread=gamma // 2 if tension else 0
    )
    return gamma, clocks, factors


def checks_of(module: ModuleType) -> list[Callable[[], Check]]:
    """Every `check_*` function of a module, in the order of its names."""
    return [getattr(module, name) for name in sorted(dir(module)) if name.startswith("check_")]


def run(module: ModuleType) -> int:
    """Run every check of a module and print each verdict; the count of failures."""
    failures = 0
    for check in checks_of(module):
        held, computed = check()
        failures += not held
        print(f"{'holds' if held else 'FAILS'}  {check.__name__}: {computed}")
    return failures
