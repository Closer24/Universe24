"""The one reader of the mesh (R2 of the readings' map, H-Readings-One-Reader-1, 2026-10-26, under the owner's word of 12:2x UTC; the owner's word of 2026-10-25: the mesh's act in one place): every reading of a mesh at a spoke is a reading of its one `Mesh`, each a function of arrays at every clock alike and every read across a mesh through core/spokes.across, the same from both ends up to the side's sign: the two ends' even sum (`even`), the two ends' odd sum signed by the spoke's side (`odd_sum`), the pawl sign, the parity of the pawls' even sum (`pawl`), and the one bilinear, the cross x_i y_j - y_i x_j (`cross`); the mesh's factor from the two ends' axis parts, the six pawl signs, the centred count and the meshes' offset pairs, the six `Mesh`es of a tick at a coupling and their skew by the flow gears (the former readings.link_factors, frames, centred_count, link_phases, links.link, links_of and metric.fold_links kept by name), the centred gradient, a gear's lead on a mesh, its net transverse lead and the twist are named readings of these four (the stress's parts and the regulation's sources in regulation.py, Y-S1 to Y-S3)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.rates import rounded
from event_universe.core.rule3 import carries, mesh_factor
from event_universe.core.rule3 import odd as parity_of
from event_universe.core.spokes import AXES, SIDES, SPOKE_SIDES, SPOKES, across, spoke_of, transverse
from event_universe.readings import standard_angle
from event_universe.trains import REGULATOR, Gear, Train

if TYPE_CHECKING:
    from event_universe.clock import Clock


def coupling_of(train: Train) -> int:
    """A hand's coupling to the meshes' offset as one value of its ratio, min(rim - pinion, 1): 0 at the ratio with no spring (the unsprung hand: its turn the identity, its sources weighted 0), 1 at every other ratio; the law's general form K / Gamma (Y-S1) is the owner's word (UN-S2)."""
    assert train.spring is not None
    return min(train.spring, 1)


def cross(x_i: Any, y_i: Any, x_j: Any, y_j: Any) -> Any:
    """The one bilinear of the law (fd2, U1): x_i y_j - y_i x_j, the 2 x 2 determinant of two readings (x, y) at two places (i, j), odd under the exchange of the places and of the readings; the Wronskian, the lead across a mesh, the hand's sign lead, the twist, the push's change, the fitted hands' and the chime's senses, the reckoner's order of rationals."""
    return x_i * y_j - y_i * x_j


def even(a: Any, spoke: int) -> Any:
    """The mesh's even sum at the spoke, a_i + a_j, read the same from both ends (fd2, U5)."""
    return a + across(a, spoke)


def odd_sum(a: Any, spoke: int) -> Any:
    """The mesh's odd sum at the spoke, the two ends' sum signed by the spoke's side: the other end reads the negative (the one mesh read of an odd part)."""
    return SPOKE_SIDES[spoke][1] * even(a, spoke)


def pawl(bits: Any, spoke: int) -> Any:
    """The pawl sign f_ij at the spoke, 1 where the two ends' pawls agree and -1 where they differ, the parity of the mesh's even part (fd2, U5)."""
    parity = parity_of(even(bits, spoke))
    return 1 - parity - parity


def offset_pair(three: Any, twelve: Any, c: Any, s: Any, scale: Any) -> tuple[Any, Any]:
    """The pair (three, twelve) turned by the pair (c, s) over the scale, one odd rounding per part (fd2, U2; fd1: the turn's rounding is odd by the one rule of the remainder, a fold with no tie): the offset pair over the standard length X, the odd tangent triple over its teeth, the reckoner's reckoning."""
    return rounded(c * three - s * twelve, scale), rounded(s * three + c * twelve, scale)


class Mesh:
    """The mesh's readings at one spoke for the tick, read once from its two ends and the same from both (X2's link(i, j)): the factor Q_ij from the two ends' tensions, the pawl sign f_ij, the mesh's offset pair (cos, sin) over X from the two ends' centred counts, and the odd part n_ij of the offset train's odd gear on the mesh's axis for the tangent triple, and the flow gears' skew for one hand (`skewed`, Y-S3: a tangent triple, the identity (1, 0, 1) where the hand has no spring or the flow is 0); every act reads these and recomputes none."""

    __slots__ = ("factor", "pawl", "cosine", "sine", "odd", "skew")

    def __init__(
        self, factor: Any, pawl_sign: Any, cosine: Any, sine: Any, odd: Any, skew: Any = (1, 0)
    ) -> None:
        self.factor, self.pawl, self.cosine, self.sine, self.odd = factor, pawl_sign, cosine, sine, odd
        self.skew = skew


def factors(clock: Clock, axis_notches: list[Any] | None = None, stopped: Any = None) -> tuple[Any, ...]:
    """The mesh factor at each spoke from the two ends' axis parts of the regulator (the former readings.link_factors and node.link_factors kept by name): the tension the mean of the two ends' notches rounded half up, the carry's carries of their even sum plus one at the two sides (the one rounding not reached by the fine tooth's rule, so not rates.rounded: fd1 measured the odd rounding here parts the 48's reflections), a tension at or past Gamma read at the teeth, the factor 0 (the standstill), and a tension below 0 read at 0 (no mesh turns faster than the full rate, the great clock's); and 0 where either end is stopped, the mesh rate 0 at the tick's start (BH-S1: every mesh with a stopped end is at the teeth, from both ends)."""
    notches = (
        [gear.now for gear in clock.train(REGULATOR).gears[1 : 1 + AXES]]
        if axis_notches is None
        else axis_notches
    )
    found = []
    for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
        t = carries(even(notches[axis], spoke) + 1, SIDES)
        factor = mesh_factor(clock.full_rate, clock.G, np.minimum(np.maximum(t, 0), clock.full_rate))
        at_teeth = None if stopped is None else stopped | across(stopped, spoke)
        found.append(factor if at_teeth is None else np.where(at_teeth, 0, factor))
    return tuple(found)


def pawls(ratchet_fine: Any) -> list[Any]:
    """The pawl signs per spoke (the former readings.frames kept by name): +1 where the two ends' pawls (the ratchet's fine tooth at two teeth, complemented at every turnover) agree, -1 where they differ; there the neighbour's hand is read reflected and its count negated."""
    return [pawl(ratchet_fine, spoke) for spoke in range(SPOKES)]


def centred_count(clocked_offset: Any, ratchet: Gear) -> Any:
    """The clock's centred count K = 2 (Phi_now - Phi_before) + c from the ratchet at the start, twice the trapezoid sum of the clocked offset to the triple's centre (the former readings.centred_count kept by name)."""
    moved = ratchet.now - ratchet.before
    return moved + moved + clocked_offset


def offsets(clock: Clock, pawl_signs: list[Any], count: Any) -> list[tuple[Any, Any]]:
    """The mesh's count n_ij = K_i - f_ij K_j (the two ends' centred counts; f_ij the pawl sign, the neighbour's count negated where the pawls differ) and its (cos, sin) pair over X (readings.standard_angle; the former readings.link_phases kept by name)."""
    found = []
    for spoke in range(SPOKES):
        n = count - pawl_signs[spoke] * across(count, spoke)
        pairs = np.vectorize(lambda m: standard_angle(clock, m), otypes=[object, object])(n)
        found.append((pairs[0], pairs[1]))
    return found


def meshes_of(
    factors: tuple[Any, ...], pawl_signs: list[Any], offset_pairs: list[tuple[Any, Any]], odd: list[Any]
) -> list[Mesh]:
    """The six `Mesh`es from the tick's readings: the factors, the pawl signs, the offset pairs and, per spoke, the odd gear of its axis summed over the two ends with the spoke's sign (`odd_sum`)."""
    return [
        Mesh(factors[spoke], pawl_signs[spoke], *offset_pairs[spoke], odd_sum(odd[axis], spoke))
        for spoke, (axis, _side) in enumerate(SPOKE_SIDES)
    ]


def skewed(meshes: list[Mesh], rest_rate: int, flow_gears: list[Any], full_rate: int) -> list[Mesh]:
    """The six `Mesh`es with the flow gears' skew for one hand (Y-S2, Y-S3; the former metric.fold_links kept by name): the flow gear of the mesh's axis summed over the two ends with the spoke's sign, n_ij = V_a(i) + V_a(j) = -n_ji, read as the odd gear is, turned at the hand's rest rate K as the tangent triple (W^2 - m^2, 2 W m, W^2 + m^2), W = Gamma^2 and m = 3 K n (the skew form's sine 6 K n / Gamma^2 to first order), the identity where K is 0 (the train at the spring 0) or the flow 0."""
    w2 = full_rate * full_rate
    found = []
    for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
        skew = (w2, AXES * rest_rate * odd_sum(flow_gears[axis], spoke))
        at = meshes[spoke]
        found.append(Mesh(at.factor, at.pawl, at.cosine, at.sine, at.odd, skew))
    return found


def mesh_teeth(full_rate: Any) -> Any:
    """The mesh's teeth 4 Gamma, the turn's unit of the pull (twice the standard rate 2 Gamma; the law's, typed once here)."""
    return 4 * full_rate


def through_mesh(xs: list[Any], at: Mesh, scale: Any, full_rate: Any) -> list[Any]:
    """A train's gears at a spoke, read in the clock's frame, turned hand by hand ((0, 1), (2, 3), ...) by the mesh's offset pair over X and by the odd gear's tangent triple (W^2 - n^2, 2 W n, W^2 + n^2), W = 4 Gamma, multiplied exactly by the flow gears' skew triple (Y-S3, the mesh's `skew`), one rounding per mesh per part, every number the `Mesh`'s."""
    wl, (w2, m), (three, twelve) = mesh_teeth(full_rate), at.skew, xs
    g3, g12 = wl * w2 - at.odd * m, wl * m + at.odd * w2
    three, twelve = offset_pair(three, twelve, at.cosine, at.sine, scale)
    return list(offset_pair(three, twelve, g3 * g3 - g12 * g12, (g3 + g3) * g12, g3 * g3 + g12 * g12))


def gradient(a: Any, axis: int) -> Any:
    """The centred difference of a train's gear along an axis, a(i + a) - a(i - a), read through the mesh's one read at the two spokes of the axis."""
    return across(a, spoke_of(axis, 0)) - across(a, spoke_of(axis, 1))


def mesh_lead(gear: Gear, spoke: int) -> Any:
    """The gear's own lead on the mesh at the spoke, F_ij = now_i before_j - before_i now_j: odd under the exchange of the ends (the other end reads -F), read at the tick's start; the + fitted hand of a mesh fitting goes to the end the lead flows into."""
    return cross(gear.now, gear.before, across(gear.now, spoke), across(gear.before, spoke))


def train_lead(gears: list[Gear], spoke: int) -> Any:
    """A hand's own lead on the mesh at the spoke, the sum of its gears' (a hand's three and twelve; the spring-0 train's twelve at 0 leaves its three gear's)."""
    return sum((mesh_lead(gear, spoke) for gear in gears), start=0)


def train_twists(gears: list[Gear]) -> list[Any]:
    """A hand's twist on every axis from its six spokes' leads read once (`train_lead`): the net transverse lead u_b = F(-b) - F(+b) on each axis (the lead into the clock from the -b mesh less the lead out along the +b mesh), then per axis a the cross of the two ends' (u_b, u_c) along the +a mesh, (b, c) the transverse pair."""
    leads = [train_lead(gears, spoke) for spoke in range(SPOKES)]
    net = [leads[spoke_of(b, 1)] - leads[spoke_of(b, 0)] for b in range(AXES)]
    found = []
    for a, (b, c) in enumerate(map(transverse, range(AXES))):
        far = [across(n, spoke_of(a, 0)) for n in (net[b], net[c])]
        found.append(cross(net[b], net[c], *far))
    return found
