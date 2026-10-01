"""The currents (ALGEBRA.md #the-count-is-the-records-share): the current through each of a Node's six Ports from the record's level pairs, F_ij = num (now_i before_j - before_i now_j) into Node i from its neighbour j, the booking of the family's two levels at the Link's two ends, positive inward, the reading a detector makes at its boundary Ports; the share's change over one step of Rule3 is exactly the six currents summed, at the pair the step started from. Beside it the tension on each axis from the levels, T_aa(i) = num (G_aa(i) + G_aa(i - a)) div 2 with G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)) the flux of the a-momentum through the a-Link at one time, Rule3's own conservation of the current per axis, read into the paces of the held rows (ALGEBRA.md #the-primitives, the row "the hold"). Both are readings of the record and never a write to it."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from event_universe.core.rule3 import NO_READ, rule3

Vector = tuple[Any, Any, Any]
PORTS = 6  # a Node's six Ports, the lattice's own integer (Rule3's 6)
PRODUCTS = 2  # the current's two products, now_i before_j and before_i now_j
DIFFERENCE = (
    2  # a difference of two levels, at most twice the amplitude: the tension's reach per product
)


@dataclass(frozen=True)
class Levels:
    """A family's two levels at one Node or across one Port: now and before."""

    now: Any
    before: Any


@dataclass(frozen=True)
class Differences:
    """The level now at the Node and its difference across one axis's two Ports, D_a = the +a arrival minus the -a arrival: at the Node (`here`) and the neighbours' own differences brought through the +a Port (`plus`) and the -a Port (`minus`)."""

    now: Any
    here: Any
    plus: Any
    minus: Any


def current(weight: int, here: Levels, there: Levels) -> Any:
    """The current into the Node here from the Node there through their Link, weight (now_i before_j - before_i now_j), positive inward (ALGEBRA.md #the-booking)."""
    return weight * (here.now * there.before - here.before * there.now)


def tension(weight: int, d: Differences) -> Any:
    """The tension on one axis at the Node, T_aa(i) = weight x (G_aa(i) + G_aa(i - a)) div 2, the mean of the a-momentum's flux through the Node's two a-Links at one time, G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)): with the differences D it is weight x (now_i (D_(i+a) - D_(i-a)) - D_i^2) div 2, a plane wave's -2 b^2 sin^2 k_a and a uniform record's 0 (ALGEBRA.md #the-primitives, the row "the hold", the tension)."""
    return rule3(NO_READ, NO_READ, weight, 2, d.now * (d.plus - d.minus) - d.here * d.here, 0, 0)[0]


def stress(weight: int, differences: tuple[Differences, Differences, Differences]) -> Vector:
    """The tension on each axis at every Node from one level pair's differences."""
    x, y, z = (tension(weight, d) for d in differences)
    return x, y, z
