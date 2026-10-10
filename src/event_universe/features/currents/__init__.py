"""The currents (ALGEBRA.md #the-count-is-the-records-share): the current through each of a Node's six Ports from the record's level pairs, F_ij = num (now_i before_j - before_i now_j) into Node i from its neighbour j, the booking of the family's two levels at the Link's two ends, positive inward, the reading a node_detector makes at its boundary Ports; the share's change over one step of Rule3 is exactly the six currents summed, at the pair the step started from. Beside it the tension's part at the Node on each axis from the levels, h_a(i) = now_(i-a) now_(i+a) - now_i^2 times the weight, the Node's own reading of its two neighbours along the axis, one Link's reach: the stress booking on the Link (i, i + a), G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)), the flux of the a-momentum through the Link at one time, is the sum of its two ends' parts, G_aa(i) = h_a(i) + h_a(i + a), so each Node sources its own part into the held row's axis part and the Link's tension is read from the two ends' parts through the Ports (ALGEBRA.md #the-primitives, The tension; #the-interval, the dependency radius). Both are readings of the record as it stands at the interval's start and never a write to it."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival

Vector = tuple[Any, Any, Any]
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


def momentum_terms(now: Any, before: Any, axis: int, wrap: Wrap, weight: int = 1) -> Any:
    """The lattice momentum's term at every Node of one level pair along `axis` before the sum (Part F2; the mathematician's line of 2026-10-09, 6085486079: the piece's p is read from "currents.momentum's per-Node terms before their sum" at a region's Nodes): F_(i,i-a) - F_(i,i+a), the Node's two Link currents along the axis, F_ij = weight (now_i before_j - before_i now_j) into i from j (`current`), the neighbours through the Ports (`core/ports.arrival`, 0 beyond a face); an array over the board in the current's own unit, no division; `momentum` is its sum over the board, a region's P_a its sum over the region's Nodes (`node.momentum_of`)."""
    here = Levels(now, before)
    behind = Levels(arrival(now, axis, -1, wrap), arrival(before, axis, -1, wrap))
    ahead = Levels(arrival(now, axis, 1, wrap), arrival(before, axis, 1, wrap))
    return np.asarray(current(weight, here, behind) - current(weight, here, ahead))


def momentum(now: Any, before: Any, axis: int, wrap: Wrap, weight: int = 1) -> int:
    """The lattice momentum of one level pair along `axis` (Part F; the advisor's and the mathematician's lines of 2026-10-09, momentum from Rule3, 6083929632 and 6084001231): P_a = SUM_i (F_(i,i-a) - F_(i,i+a)), the antisymmetric sum over every Node of the two Link currents along the axis in the current's own unit (`momentum_terms`), F_ij = weight (now_i before_j - before_i now_j) into i from j (`current`), so that P_a = 2 weight SUM_i (now_(i+a) before_i - now_i before_(i+a)) on a periodic board, the mathematician's normalisation with the current's weight kept: a plane wave cos(k x - omega t) has P_a of the sign of +k (the term's mean weight A^2 sin k sin omega per Link), and a piece of action T carries weight T sin k_a, "sin k" the integer current in T's unit. Conserved exactly by the rational step at uniform static paces on a periodic board (M circulant and symmetric commutes with the shift T_a, [M, T_a] = 0) and to the floors on the integers, Delta P_a = (weight / w) SUM_i (r'_i - r_i)(now_(i-a) - now_(i+a)) per step, below weight SUM_i |now_(i+a) - now_(i-a)|, a walk of mean 0; at non-uniform static paces it changes by minus the gradient of the Node's rest rotation times the density, the fall. A reading of the record as it stands, never a write; no division: the unit is the current's."""
    return int(momentum_terms(now, before, axis, wrap, weight).sum(dtype=object))


def tension(weight: int, n: Neighbours) -> Any:
    """The Node's own part of the tension on one axis, -weight x h_a(i) with h_a(i) = now_(i-a) now_(i+a) - now_i^2, one Link's reach, the law's sign (ALGEBRA.md #the-primitives, The tension: the tension is minus the stress booking, T_aa = -num (G_aa(i) + G_aa(i - a)) div 2, the advisor's correction, so a record's stress deepens the content around it and light gravitates by its pressure, no hill): the Link's stress booking G_aa(i) = h_a(i) + h_a(i + a) is the sum of its two ends' parts, a plane wave's part +b^2 sin^2 k_a (the Link's +2 b^2 sin^2 k_a, the pattern [2, 0, -2, 0] along an axis +4 at every Node at the weight 1, +8 on the Link) and a uniform record's 0; no division."""
    return -weight * (n.behind * n.ahead - n.now * n.now)


def stress(weight: int, neighbours: tuple[Neighbours, Neighbours, Neighbours]) -> Vector:
    """The tension's part on each axis at every Node from one level pair's neighbours."""
    x, y, z = (tension(weight, n) for n in neighbours)
    return x, y, z
