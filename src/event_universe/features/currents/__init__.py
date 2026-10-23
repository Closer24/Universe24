"""The currents (ALGEBRA.md #the-count-is-the-records-share): the current through each of a Node's six Ports from the record's level pairs, F_ij = num (now_i before_j - before_i now_j) into Node i from its neighbour j, the booking of the family's two levels at the Link's two ends, positive inward, the reading a node_detector makes at its boundary Ports; the share's change over one step of Rule3 is exactly the six currents summed, at the pair the step started from. Beside it the tension's part at the Node on each axis from the levels, h_a(i) = now_(i-a) now_(i+a) - now_i^2 times the weight, the Node's own reading of its two neighbours along the axis, one Link's reach: the stress booking on the Link (i, i + a), G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)), the flux of the a-momentum through the Link at one time, is the sum of its two ends' parts, G_aa(i) = h_a(i) + h_a(i + a), so each Node sources its own part into the held row's axis part and the Link's tension is read from the two ends' parts through the Ports (ALGEBRA.md #the-primitives, The tension; #the-interval, the dependency radius). Beside them the shear's part on each axis pair, weight x D_a now_i x D_b now_i, the product of the Node's own two axis differences (`off_diagonal_part`), the two ends' halves of the Link's off-diagonal booking G_ab in the mean, written into a held row's shear lines where its declaration names the shear. All three are readings of the record's levels at the interval's start and never a write to it."""

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
    """The lattice momentum's term at every Node of one level pair along `axis` before the sum (Part F2; the mathematician's line of 2026-10-09, 6085486079: the piece's p is read from "currents.momentum's per-Node terms before their sum" at a region's Nodes): F_(i,i-a) - F_(i,i+a), the Node's two Link currents along the axis, F_ij = weight (now_i before_j - before_i now_j) into i from j (`current`), the neighbours through the Ports (`core/ports.arrival`, 0 beyond a face); an array over the board in the current's own unit, no division; `momentum` is its sum over the board, a region's P_a its sum over the region's Nodes (`readings.momentum_of`)."""
    here = Levels(now, before)
    behind = Levels(arrival(now, axis, -1, wrap), arrival(before, axis, -1, wrap))
    ahead = Levels(arrival(now, axis, 1, wrap), arrival(before, axis, 1, wrap))
    return np.asarray(current(weight, here, behind) - current(weight, here, ahead))


def momentum(now: Any, before: Any, axis: int, wrap: Wrap, weight: int = 1) -> int:
    """The lattice momentum of one level pair along `axis` (Part F; the advisor's and the mathematician's lines of 2026-10-09, momentum from Rule3, 6083929632 and 6084001231): P_a = SUM_i (F_(i,i-a) - F_(i,i+a)), the antisymmetric sum over every Node of the two Link currents along the axis in the current's own unit (`momentum_terms`), F_ij = weight (now_i before_j - before_i now_j) into i from j (`current`), so that P_a = 2 weight SUM_i (now_(i+a) before_i - now_i before_(i+a)) on a periodic board, the mathematician's normalisation with the current's weight kept: a plane wave cos(k x - omega t) has P_a of the sign of +k (the term's mean weight A^2 sin k sin omega per Link), and a piece of action T carries weight T sin k_a, "sin k" the integer current in T's unit. Conserved exactly by the rational step at uniform static paces on a periodic board (M circulant and symmetric commutes with the shift T_a, [M, T_a] = 0) and to the floors on the integers, Delta P_a = (weight / w) SUM_i (r'_i - r_i)(now_(i-a) - now_(i+a)) per step, below weight SUM_i |now_(i+a) - now_(i-a)|, a walk of mean 0; at non-uniform static paces it changes by minus the gradient of the Node's rest rotation times the density, the fall. A reading of the record as it stands, never a write; no division: the unit is the current's."""
    return int(momentum_terms(now, before, axis, wrap, weight).sum(dtype=object))


def tension(weight: int, n: Neighbours) -> Any:
    """The Node's own part of the tension on one axis, weight x (now_(i+a) - now_(i-a))^2, the square of the Node's centred difference along the axis, one Link's reach, at the doubled wall 2 E_s W_c (ALGEBRA.md, The stress is the Links', a proposal under its own name, 2026-10-23; the former reading -weight x h_a(i) with h_a(i) = now_(i-a) now_(i+a) - now_i^2 at E_s W_c kept by name under The tension): by the identity h_a = a_i Delta_a a_i - (a_(i+a) - a_i)(a_i - a_(i-a)) and the wrapped board's sum of a Delta a being minus the sum of the Link differences squared, the board sum of this reading over the doubled wall equals the former's over its wall to the bit for every record on every wrapped board, so the trace into the time line keeps its board mean and a plane wave's part keeps its mean +b^2 sin^2 k_a (the pattern [2, 0, -2, 0] along an axis 0, 16, 0, 16 at the weight 1 over the doubled wall, the Link's two ends' sum 16 on every Link, the former +4 at every Node and +8 on the Link), while the reading is invariant under the shift of a massless family's level by one uniform number (a -> a + m gave the former h_a the cross term m Delta_a a, a traceless source at a laid wave's k growing with the wave's coasting mean on a wrapped board, which rang the tension lines' k > 0 modes to Gamma; Rule3's line with D = 0 moves a uniform level by nothing, and the reading now knows it); the law's sign (The tension: the tension is minus the stress booking, so a record's stress deepens the content around it and light gravitates by its pressure, no hill); a one-Node record's part 0 at its Node and its level squared at each of its two neighbours on the axis (the former -a^2 at the Node, 0 beside it, the same sum); a uniform record's 0; no division."""
    difference = n.ahead - n.behind
    return weight * difference * difference


def stress(weight: int, neighbours: tuple[Neighbours, Neighbours, Neighbours]) -> Vector:
    """The tension's part on each axis at every Node from one level pair's neighbours."""
    x, y, z = (tension(weight, n) for n in neighbours)
    return x, y, z


def difference(n: Neighbours) -> Any:
    """The Node's own axis difference of the level now, D_a now_i = now_(i+a) - now_(i-a), the two a-Ports' differences summed, one Link's reach: the axis booking the shear's product takes (ALGEBRA.md, The tension: D_a the centred difference along the axis a)."""
    return n.ahead - n.behind


def off_diagonal_part(weight: int, first: Neighbours, second: Neighbours) -> Any:
    """The Node's own part of the shear on one axis pair, weight x D_a now_i x D_b now_i, the product of its two axis differences at the same Node and the same interval, one Link's reach and no read at the reach sqrt 2 (the owner's word of 2026-10-20): over the doubled wall 2 E_s W_c it is the Node's half of the Link's off-diagonal booking, the flux of the a-momentum across a b-Link, -num G_ab(i) = -num [now_i D_a now_(i+b) - now_(i+b) D_a now_i], in the mean (ALGEBRA.md, The tension: a plane record of the amplitude b has G_ab = -2 b^2 sin k_a sin k_b, and D_a now D_b now = 4 b^2 sin^2(theta) sin k_a sin k_b, whose mean over the record's phase theta is 2 b^2 sin k_a sin k_b, the Link's -G_ab, so the two ends' halves meet the Link's booking as -num h_a(i) - num h_a(i + a) meets -num G_aa(i) exactly; a uniform record's part 0; a narrow-band packet of count c and velocity v the dust's c v_a v_b beside the tension's c v_a^2, within the rounding); the sign the tension's, a record's stress deepening the content; no division."""
    return weight * difference(first) * difference(second)


def off_diagonal(weight: int, neighbours: tuple[Neighbours, Neighbours, Neighbours]) -> Vector:
    """The shear's part on each axis pair at every Node from one level pair's neighbours, in the order xy, yz, zx (`off_diagonal_part`)."""
    x, y, z = neighbours
    return (
        off_diagonal_part(weight, x, y),
        off_diagonal_part(weight, y, z),
        off_diagonal_part(weight, z, x),
    )
