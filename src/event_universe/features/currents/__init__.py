"""The currents (ALGEBRA.md #the-count-is-the-records-share): the current through each of a Node's six Ports from the record's level pairs, F_ij = num (now_i before_j - before_i now_j) into Node i from its neighbour j, the booking of the family's two levels at the Link's two ends, positive inward, the reading a detector makes at its boundary Ports; the share's change over one step of Rule3 is exactly the six currents summed, at the pair the step started from. Beside it the tension's part at the Node on each axis from the levels, h_a(i) = now_(i-a) now_(i+a) - now_i^2 times the weight, the Node's own reading of its two neighbours along the axis, one Link's reach: the stress booking on the Link (i, i + a), G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)), the flux of the a-momentum through the Link at one time, is the sum of its two ends' parts, G_aa(i) = h_a(i) + h_a(i + a), so each Node sources its own part into the held row's axis part and the Link's tension is read from the two ends' parts through the Ports (ALGEBRA.md #the-primitives, The tension; #the-interval, the dependency radius). Both are readings of the record as it stands at the interval's start and never a write to it."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

Vector = tuple[Any, Any, Any]
PORTS = 6  # a Node's six Ports, the lattice's own integer (Rule3's 6)
AXIS_PORTS = 2  # the two Ports of one axis, +a and -a: the sign's current is the mean of their Links'
PRODUCTS = 2  # the current's two products, now_i before_j and before_i now_j


@dataclass(frozen=True)
class Levels:
    """A family's two levels at one Node or across one Port: now and before."""

    now: Any
    before: Any


@dataclass(frozen=True)
class Neighbours:
    """The level now at the Node and at its two neighbours along one axis, through the +a Port (`ahead`) and the -a Port (`behind`), one Link's reach."""

    now: Any
    ahead: Any
    behind: Any


def current(weight: int, here: Levels, there: Levels) -> Any:
    """The current into the Node here from the Node there through their Link, weight (now_i before_j - before_i now_j), positive inward (ALGEBRA.md #the-booking)."""
    return weight * (here.now * there.before - here.before * there.now)


def tension(weight: int, n: Neighbours) -> Any:
    """The Node's own part of the tension on one axis, -weight x h_a(i) with h_a(i) = now_(i-a) now_(i+a) - now_i^2, one Link's reach, the law's sign (ALGEBRA.md #the-primitives, The tension: the tension is minus the stress booking, T_aa = -num (G_aa(i) + G_aa(i - a)) div 2, the advisor's correction of #1519 comment 5906225516, so a record's stress deepens the content around it and light gravitates by its pressure, no hill): the Link's stress booking G_aa(i) = h_a(i) + h_a(i + a) is the sum of its two ends' parts, a plane wave's part +b^2 sin^2 k_a (the Link's +2 b^2 sin^2 k_a, the pattern [2, 0, -2, 0] along an axis +4 at every Node at the weight 1, +8 on the Link) and a uniform record's 0; no division."""
    return -weight * (n.behind * n.ahead - n.now * n.now)


def stress(weight: int, neighbours: tuple[Neighbours, Neighbours, Neighbours]) -> Vector:
    """The tension's part on each axis at every Node from one level pair's neighbours."""
    x, y, z = (tension(weight, n) for n in neighbours)
    return x, y, z
