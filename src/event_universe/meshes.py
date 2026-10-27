"""The one reader of the Link (R2 of the readings' map, H-Readings-One-Reader-1, 2026-10-26, under the owner's word of 12:2x UTC; the owner's word of 2026-10-25: the Link's act in one place): every reading of a Link at a Port is a reading of the Link's one record, each a function of arrays at every Node alike and every read across a Link through core/ports.across, the same from both ends up to the side's sign: the two ends' even sum (`even`), the two ends' odd sum signed by the Port's side (`odd_sum`), the frame sign, the parity of the frame bits' even sum (`frame`), and the one bilinear, the cross x_i y_j - y_i x_j (`cross`); the Link's factor from the two ends' axis parts, the six frame signs, the centred count and the Links' phase pairs, the six records of an interval at a coupling and their fold by the flux lines (the former readings.link_factors, frames, centred_count, link_phases, links.link, links_of and metric.fold_links kept by name), the centred gradient, a line's current on a Link, its net transverse current and the twist are named readings of these four (the stress's parts and the metric's sources in metric.py, Y-S1 to Y-S3)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.rates import rounded
from event_universe.core.rule3 import carries, mesh_factor
from event_universe.core.rule3 import odd as parity_of
from event_universe.core.spokes import AXES, SIDES, SPOKE_SIDES, SPOKES, across, spoke_of, transverse
from event_universe.readings import standard_angle
from event_universe.trains import HAND, REGULATOR, Gear, Train

if TYPE_CHECKING:
    from event_universe.clock import Clock


def coupling_of(row: Train) -> int:
    """A record's coupling to the Links' phase as one value of its pair, min(den - num, 1): 0 at the pair with no gap (the emitter: its turn the identity, its sources weighted 0), 1 at every other pair; the law's general form K / Gamma (Y-S1) is the owner's word (UN-S2)."""
    assert row.spring is not None
    return min(row.spring, 1)


def cross(x_i: Any, y_i: Any, x_j: Any, y_j: Any) -> Any:
    """The one bilinear of the law (fd2, U1): x_i y_j - y_i x_j, the 2 x 2 determinant of two readings (x, y) at two places (i, j), odd under the exchange of the places and of the readings; the Wronskian, the current across a Link, the plane's sign current, the twist, the lattice momentum's change, the children's and the credit's senses, the decoder's order of rationals."""
    return x_i * y_j - y_i * x_j


def even(a: Any, port: int) -> Any:
    """The Link's even sum at the Port, a_i + a_j, read the same from both ends (fd2, U5)."""
    return a + across(a, port)


def odd_sum(a: Any, port: int) -> Any:
    """The Link's odd sum at the Port, the two ends' sum signed by the Port's side: the other end reads the negative (the one Link read of an odd part)."""
    return SPOKE_SIDES[port][1] * even(a, port)


def pawl(bits: Any, port: int) -> Any:
    """The frame sign f_ij at the Port, 1 where the two ends' frame bits agree and -1 where they differ, the parity of the Link's even part (fd2, U5)."""
    parity = parity_of(even(bits, port))
    return 1 - parity - parity


def offset_pair(re: Any, im: Any, c: Any, s: Any, scale: Any) -> tuple[Any, Any]:
    """The pair (re, im) turned by the pair (c, s) over the scale, one odd rounding per part (fd2, U2; fd1: the turn's rounding is odd by the one rule of the remainder, a fold with no tie): the phase pair over the amplitude X, the odd tangent triple over its wall, the decoder's solve."""
    return rounded(c * re - s * im, scale), rounded(s * re + c * im, scale)


class Mesh:
    """The Link's record at one Port for the interval, read once from its two ends and the same from both (X2's link(i, j)): the factor Q_ij from the two ends' tensions, the frame sign f_ij, the Link's phase pair (cos, sin) over X from the two ends' centred counts, and the odd part n_ij of the shape-4 row's odd line on the Link's axis for the tangent triple, and the flux lines' fold for one record (`folded`, Y-S3: a tangent triple, the identity (1, 0, 1) where the record has no gap or the flux is 0); every act reads these and recomputes none."""

    __slots__ = ("factor", "pawl", "cosine", "sine", "odd", "skew")

    def __init__(
        self, factor: Any, frame: Any, cosine: Any, sine: Any, odd: Any, fold: Any = (1, 0, 1)
    ) -> None:
        self.factor, self.pawl, self.cosine, self.sine, self.odd = factor, frame, cosine, sine, odd
        self.skew = fold


def factors(node: Clock, axis_levels: list[Any] | None = None, frozen: Any = None) -> tuple[Any, ...]:
    """The Link factor at each Port from the two ends' axis parts of the carrier (the former readings.link_factors and node.link_factors kept by name): the tension the mean of the two ends' levels rounded half up, the division act's quotient of their even sum plus one at the two sides (the one rounding not reached by the remainder's rule, so not paces.rounded: fd1 measured the odd rounding here parts the 48's reflections), a tension at or past Gamma read at the wall, the factor 0 (the horizon); and 0 where either end is frozen, the Link pace 0 at the interval's start (BH-S1: every Link with a frozen end is at the wall, from both ends)."""
    levels = (
        [line.now for line in node.train(REGULATOR).gears[1 : 1 + AXES]]
        if axis_levels is None
        else axis_levels
    )
    found = []
    for port, (axis, _side) in enumerate(SPOKE_SIDES):
        t = carries(even(levels[axis], port) + 1, SIDES)
        factor = np.vectorize(
            lambda tt: int(mesh_factor(node.full_rate, node.G, min(int(tt), node.full_rate))),
            otypes=[object],
        )
        at_wall = None if frozen is None else frozen | across(frozen, port)
        found.append(factor(t) if at_wall is None else np.where(at_wall, 0, factor(t)))
    return tuple(found)


def pawls(phi_rem: Any) -> list[Any]:
    """The frame signs per Port (the former readings.frames kept by name): +1 where the two ends' frame bits (the phase row's remainder at the wall 2, complemented at every swap) agree, -1 where they differ; there the neighbour's plane is read conjugated and its count negated."""
    return [pawl(phi_rem, port) for port in range(SPOKES)]


def centred_count(cphi: Any, phi: Gear) -> Any:
    """The Node's centred count K = 2 (Phi_now - Phi_before) + c from the phase row at the start, twice the trapezoid sum of the clocked potential to the triple's centre (the former readings.centred_count kept by name)."""
    moved = phi.now - phi.before
    return moved + moved + cphi


def offsets(node: Clock, frames: list[Any], count: Any) -> list[tuple[Any, Any]]:
    """The Link's count n_ij = K_i - f_ij K_j (the two ends' centred counts; f_ij the frame sign, the neighbour's count negated where the frames differ) and its (cos, sin) pair over X (readings.pair_angle; the former readings.link_phases kept by name)."""
    found = []
    for port in range(SPOKES):
        n = count - frames[port] * across(count, port)
        pairs = np.vectorize(lambda m: standard_angle(node, m), otypes=[object, object])(n)
        found.append((pairs[0], pairs[1]))
    return found


def meshes_of(
    factors: tuple[Any, ...], frames: list[Any], phases: list[tuple[Any, Any]], odd_lines: list[Any]
) -> list[Mesh]:
    """The six Links' records from the interval's readings: the factors, the frame signs, the phase pairs and, per Port, the odd line of its axis summed over the two ends with the Port's sign (`odd_sum`)."""
    return [
        Mesh(factors[port], frames[port], *phases[port], odd_sum(odd_lines[axis], port))
        for port, (axis, _side) in enumerate(SPOKE_SIDES)
    ]


def skewed(links: list[Mesh], rotation: int, flux_lines: list[Any], gamma: int) -> list[Mesh]:
    """The six Links' records with the flux lines' fold for one record (Y-S2, Y-S3; the former metric.fold_links kept by name): the flux line of the Link's axis summed over the two ends with the Port's sign, n_ij = V_a(i) + V_a(j) = -n_ji, read as the odd line is, turned at the record's rest rotation K as the tangent triple (W^2 - m^2, 2 W m, W^2 + m^2), W = Gamma^2 and m = 3 K n (the fold form's sine 6 K n / Gamma^2 to first order), the identity where K is 0 (the row at the gap 0) or the flux 0."""
    w2 = gamma * gamma
    found = []
    for port, (axis, _side) in enumerate(SPOKE_SIDES):
        m = AXES * rotation * odd_sum(flux_lines[axis], port)
        fold = (w2 * w2 - m * m, (w2 + w2) * m, w2 * w2 + m * m)
        at = links[port]
        found.append(Mesh(at.factor, at.pawl, at.cosine, at.sine, at.odd, fold))
    return found


def mesh_teeth(gamma: Any) -> Any:
    """The Link's wall 4 Gamma, the turn's unit of the arrival (twice the phase unit 2 Gamma; the law's, typed once here)."""
    return 4 * gamma


def through_mesh(xs: list[Any], at: Mesh, scale: Any, gamma: Any) -> list[Any]:
    """A row's lines at a Port, read in the Node's frame, turned plane by plane ((0, 1), (2, 3), ...) by the Link's pair over X and by the odd line's tangent triple (W^2 - n^2, 2 W n, W^2 + n^2), W = 4 Gamma, multiplied exactly by the flux lines' fold triple (Y-S3, the Link's `fold`), one rounding per Link per part, every number the Link's record."""
    wl = mesh_teeth(gamma)
    tc, ts, tw = wl * wl - at.odd * at.odd, (wl + wl) * at.odd, wl * wl + at.odd * at.odd
    fc, fs, fw = at.skew
    tc, ts, tw = tc * fc - ts * fs, ts * fc + tc * fs, tw * fw
    found: list[Any] = []
    for re_j, im_j in zip(xs[0::HAND], xs[1::HAND], strict=True):
        a_re, a_im = offset_pair(re_j, im_j, at.cosine, at.sine, scale)
        found += offset_pair(a_re, a_im, tc, ts, tw)
    return found


def gradient(a: Any, axis: int) -> Any:
    """The centred difference of a row's line along an axis, a(i + a) - a(i - a), read through the Link's one read at the two Ports of the axis."""
    return across(a, spoke_of(axis, 0)) - across(a, spoke_of(axis, 1))


def mesh_lead(line: Gear, port: int) -> Any:
    """The line's own current on the Link at the Port, F_ij = now_i before_j - before_i now_j: odd under the exchange of the ends (the other end reads -F), read at the interval's start; the + child of a Link birth goes to the end the current flows into."""
    return cross(line.now, line.before, across(line.now, port), across(line.before, port))


def train_lead(lines: list[Gear], port: int) -> Any:
    """A record's own current on the Link at the Port, the sum of its lines' (a plane's re and im; the gap-0 row's im at 0 leaves its re line's)."""
    return sum((mesh_lead(line, port) for line in lines), start=0)


def train_twist(lines: list[Gear], axis: int) -> Any:
    """The twist of a record's transverse currents along the +axis Link (the lines' net currents summed per axis, then the cross of the two ends')."""
    a, (b, c) = axis, transverse(axis)
    ub = sum((net_lead(line, b) for line in lines), start=0)
    uc = sum((net_lead(line, c) for line in lines), start=0)
    return cross(ub, uc, across(ub, spoke_of(a, 0)), across(uc, spoke_of(a, 0)))


def net_lead(line: Gear, axis: int) -> Any:
    """A line's net transverse current at every Node along an axis, u_b(k) = F(k, k - b) - F(k, k + b): the current into the Node from the -b Link less the current out along the +b Link, read from the Node's own two Links of that axis."""
    return mesh_lead(line, spoke_of(axis, 1)) - mesh_lead(line, spoke_of(axis, 0))
