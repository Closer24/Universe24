"""The interval, the Node's one program in both directions (ALGEBRA.md, The interval; The direction: every act but the click a bijection, the run back the same acts in the reverse order, each inverted), in the symmetric ride's form (R5; the owner's approved sentence 1 of 2026-10-25: the held carrier of the wall and every riding row step as one pair at the mean wall): five acts of two kinds, the carried division (core/rule3.acts.divide (the former carried_division kept by name), the paces' odd rounding where the law has it) and the lay; (1) the readings at the start (the content, the rulers, the Links' count and phases from the walled row's act, every riding line's force, the records' current and the emission), (2) the kick (every riding line's momentum read at the mean wall and kicked, the records' charge at the kick among them, PL-S1, the carrier's source from every riding row alike, the records' count flux on each axis from the velocities in and out against the centred gradient, Y-S3), (3) the division (the carrier's one division, every riding line's one division at the mean wall of the carrier's two levels at its end, the lays among the divisions, the rows set, the frozen Nodes' lines restored, BH-S1), (4) the swap at the top and the floor, (5) the close; backward the close and the swap are undone first, the lays come off before the kick and every division is the same act at -1; one class holds the interval's readings so that each act is one function."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram, readings
from event_universe.core import paces
from event_universe.core.acts import divide
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import half, held_numerator, quotient
from event_universe.features import volume
from event_universe.links import centred_count, coupling_of, factors, folded, frames, links_of, phases
from event_universe.metric import net_flux, rotation_of, shear_parts, stress_parts, tensor_parts
from event_universe.rows import CARRIER, POTENTIAL, Line, Row, walled_of, zeros
from event_universe.run import frame
from event_universe.take import momentum_of, recoil

if TYPE_CHECKING:
    from event_universe.node import Node


def laid_on(node: Node, line: Line, levels: Any) -> None:
    """The emission's size, a reading of the run: the levels laid on the emitter's line and the Nodes they were laid at."""
    laid = line.now - levels
    node.counts["laid"] += int(sum(abs(int(x)) for x in laid.reshape(-1)))
    node.counts["laid_nodes"] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))


class Interval:
    """One interval's readings at its start and the rows as the acts leave them, in the direction given: forward from the pre-state, the interval counted up; backward from the post-state with the close undone (5, close.click at -1) and the turned Nodes returned to their pre-state by the swap's own exchange (4), the acts inverted in the reverse order."""

    def __init__(self, node: Node, direction: int) -> None:
        self.node, self.direction = node, direction
        node.interval += direction
        if direction == 1:
            self.top: Any = np.zeros(node.shape, dtype=bool)
            self.kept: list[list[Line]] | None = None
            self.frozen: Any = None
            self.bookings: list[tuple[tuple[int, ...], list[int], int]] = []
        else:
            frame = node.stack.pop()
            node.click([], [], -1, frame)
            self.top = frame["turned"]
            self.frozen = frame["frozen"]
            self.bookings = frame["bookings"]
        self.still: Any = self.top if self.frozen is None else self.top | self.frozen
        self.held = [[line.copy() for line in row] for row in node.rows()]
        if direction == -1:
            node.swap(self.held, -1, self.top)
            self.kept = [[line.copy() for line in row] for row in node.rows()]
        self.rows = node.rows()
        self.where = {id(r): k for k, r in enumerate(node.rows_)}
        self.carrier, self.walled = node.row(CARRIER), walled_of(node.rows_)
        self.potential, self.emitter = node.row(POTENTIAL), node.emitter()
        self.riders = [r for r in node.rows_ if r.wall is None and r is not self.carrier]
        self.records = node.records()
        self.planes = [(r, coupling_of(r)) for r in self.records]
        self.scales = {self.where[id(r)]: gram.scale(r.shape, node.gamma) for r in self.riders}
        self.common = max(self.scales.values())
        self.out: list[list[Line]] = [[] for _ in self.rows]
        self.plane_starts: list[list[Line]] = []
        self.stepped: list[list[Line]] = []
        self.w_half = half(node.w)

    def at(self, line: Line) -> Any:
        """A line's start level: forward the now slot; backward the before slot, and the now slot at a still Node, turned or frozen (BH-S1), which ended the interval at its pre-state."""
        return line.now if self.direction == 1 else np.where(self.still, line.now, line.before)

    def lines(self, row: Row) -> list[Line]:
        """A row's lines as the interval holds them."""
        return self.rows[self.where[id(row)]]

    def ends(self, row: Row) -> tuple[Any, list[Line] | None]:
        """The turned Nodes and the row's kept pre-state for an act backward."""
        return self.top, None if self.kept is None else self.kept[self.where[id(row)]]

    def mean_wall(self, line: Line) -> Any:
        """The mean wall (w div 2)(X_before + X_now) of the carrier's time line as given: the rows' own before the carrier's act for the kick and the lays, the act's at its end for the riding lines' divisions."""
        return self.w_half * (line.before + line.now)

    def readings(self) -> None:
        """(1) The readings at the start (the former `readings`, `walled_act` and `forces`): the content and the clock, the frozen mask (BH-S1), the proper count resting at a frozen Node, the Link factors with a frozen end at the wall, the frames, the clocked potential, the carrier's level and the stress of the planes; the walled row's act, one carried division with the flux 2 c Phi inside it (its start the Links' count K = 2 (Phi_now - Phi_before) + c, backward recovered by the inverse division alone), the six Links' records read once per coupling present among the records (links.coupling_of; the frame sign, the count and the odd part at the coupling, so the turn at the coupling 0 is the identity by arithmetic), the curl of the odd lines; the records' current at this end, each at its coupling; every riding line's force, SUM_j R_j (m_j - a) - D a plus the row's Node term by shape (gram.term), every record turned by the Links at its coupling and by the flux lines' fold at its rest rotation (links.folded, Y-S3; the row at the gap 0 by nothing); and the emission, X_now SUM over the records with a gap of F.GJ.N (the plane's re F_im - im F_re), each over its scale against the common one."""
        node = self.node
        self.c = np.asarray(volume.level_of(node.gamma, self.at(self.carrier.lines[0])), dtype=object)
        node.start_content = self.c
        self.p0, self.pi = readings.paces_of(node, self.c)
        node.start_clock = self.p0
        if self.frozen is None:
            self.frozen = readings.frozen_of(node, self.c)
            self.still = self.top | self.frozen
        node.proper = node.proper + self.direction * np.where(self.frozen, 0, self.p0)
        self.factors = factors(
            node, [self.at(line) for line in self.carrier.lines[1 : 1 + AXES]], self.frozen
        )
        node.start_factors = self.factors
        self.frames = frames(self.walled.lines[0].rem)
        node.start_frames = self.frames
        self.cphi = paces.rounded(self.at(self.potential.lines[0]) * self.p0, node.gamma)
        self.x_now = self.at(self.carrier.lines[0])
        node.start_x = self.x_now
        sources = [
            ([self.at(line) for line in r.lines], r.pair[0], gram.gram(r.shape))
            for r in self.records
            if r.pair
        ]
        self.trace, self.traceless = tensor_parts(stress_parts(sources, node.shape))
        self.shear = shear_parts(sources, node.shape)
        self.flux_lines = [self.at(line) for line in self.carrier.lines[1 + AXES : 1 + AXES + AXES]]
        k, flux = self.where[id(self.walled)], [self.cphi + self.cphi]
        rule, ends = node.rule_of(self.walled, self.c, self.factors), self.ends(self.walled)
        act = node.act(self.rows[k], rule, None, [None], self.direction, flux, *ends)
        (phi_start,), self.out[k] = act
        count = centred_count(self.cphi, phi_start)
        node.count_max = max(
            int(abs(int(x)))
            for port in range(PORTS)
            for x in (count - self.frames[port] * across(count, port)).reshape(-1)
        )
        self.phases = phases(node, self.frames, count)
        self.odd = [self.at(line) for line in self.potential.lines[1 : 1 + AXES]]
        node.start_phases, node.start_odd = self.phases, [o.copy() for o in self.odd]
        self.links_at = {
            c: links_of(
                self.factors,
                [f**c for f in self.frames],
                self.phases if c == 1 else phases(node, self.frames, count * c),
                [o * c for o in self.odd],
            )
            for c in sorted({c for _r, c in self.planes})
        }
        self.curl = gram.curl(self.odd)
        self.current = [zeros(node.shape) for _ in range(AXES)]
        for r, cpl in self.planes:
            nows = [self.at(line) for line in self.lines(r)]
            for a, j_a in enumerate(gram.current(r.shape, nows, self.frames)):
                self.current[a] = self.current[a] + cpl * j_a
        self.starts: dict[int, list[Any]] = {}
        self.force: dict[int, list[Any]] = {}
        self.walls: dict[int, Any] = {}
        for r in self.riders:
            rule = node.rule_of(r, self.c, self.factors)
            turn = None
            if r in self.records:
                assert r.pair is not None
                rotation = coupling_of(r) * rotation_of(node, r.pair)
                turn = folded(self.links_at[coupling_of(r)], rotation, self.flux_lines, node.gamma)
            k = self.where[id(r)]
            self.walls[k] = rule.wall
            self.starts[k] = [self.at(line) for line in self.lines(r)]
            arrivals = node.arrivals(self.starts[k], rule, turn)
            coefficient = quotient(sum(rule.reaches), self.scales[k])
            added = gram.term(r.shape, coefficient, self.curl, self.starts[k])
            self.force[k] = [
                m + t - (rule.wall + rule.wall - rule.self_coefficient) * a
                for a, m, t in zip(self.starts[k], arrivals, added, strict=True)
            ]
        self.emission = zeros(node.shape)
        for r, cpl in self.planes:
            k = self.where[id(r)]
            gj = gram.matmul(gram.gram(r.shape), gram.rotation(r.shape))
            flow = cpl * gram.form(gj, self.force[k], self.starts[k])
            self.emission = self.emission + self.x_now * flow * quotient(self.common, self.scales[k])

    def kick(self) -> None:
        """(2) The kick (the former `kicks`): every riding line's momentum at the start read at the mean wall of the carrier's two levels as the rows hold them times the row's scale, P = W (a_now - a_before) + r - W div 2, and kicked by X_now F in the direction; the shape-4 row's time line kicked besides by the records' charge read at the kick (PL-S1, the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423: SUM over the records with a gap of N.GJ.u_in + N.GJ.u_out, N the levels at the start and u the odd rounding of 2 P + 1 over 2 w X_now at the scale, the plane's -(re u_im - im u_re) in and out, the same integers in either direction and its own mirror under the exchange and the conjugation; one carried division at the line's write wall T with the carry kept in its write remainder, the quotient landing as the kick w X_now q before the line's one division; the charge summed over the records before the shape-4 row is met, which rests on rows.order_of, H-Confirm-Build-11; the former level write of 2 W of the records after the step kept by name: a source pinned to the step's end, whose mirror under the exchange is a start, so the fall wrote 2 W(top - 1 - k) where the inverted recurrence needs 2 W(top - k)); and the carrier's source from every riding row alike with its G, line by line u_in (G u_out) + (-a (G F)) div w, w the row's wall."""
        node = self.node
        self.forms = zeros(node.shape)
        self.kicked: dict[int, list[Any]] = {}
        d = (node.w + node.w) * self.x_now
        w_side = self.mean_wall(self.carrier.lines[0])
        charge = zeros(node.shape)
        self.flux = [zeros(node.shape) for _ in range(AXES)]
        for r in self.riders:
            k = self.where[id(r)]
            ws, ds, g = self.scales[k] * w_side, self.scales[k] * d, gram.gram(r.shape)
            p_side = [ws * (line.now - line.before) + line.rem - half(ws) for line in self.rows[k]]
            p_other = [
                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)
            ]
            if r is self.potential:
                line = self.rows[k][0]
                q, line.wr = divide(charge, line.wwall, line.wr, self.direction)
                p_other[0] = p_other[0] + self.direction * node.w * self.x_now * q
            u_in = [paces.rounded(p + p + 1, ds) for p in p_side]
            u_out = [paces.rounded(p + p + 1, ds) for p in p_other]
            if r in self.records:
                gj = gram.matmul(g, gram.rotation(r.shape))
                forms = gram.form(gj, self.starts[k], u_in) + gram.form(gj, self.starts[k], u_out)
                charge = charge + coupling_of(r) * forms
                assert r.pair is not None
                for u in (u_in, u_out):
                    for a in range(AXES):
                        self.flux[a] = self.flux[a] + r.pair[0] * net_flux(g, self.starts[k], u, a)
            pulls = gram.weighted(g, self.starts[k], self.force[k])
            for product, pull in zip(gram.weighted(g, u_in, u_out), pulls, strict=True):
                self.forms = self.forms + product + quotient(-pull, self.walls[k])
            self.kicked[k] = p_other

    def division(self) -> None:
        """(3) The division (the former `carrier_act`, `divisions`, `writes` and `rest`): the carrier's one division with the write sourced by the riding rows' momenta, 4 X (forms (the file's trace weight) den Gamma^2 - trace p_0^2) p_0 on its time line and, times p_0^2 on its nine axis lines by the position of their reading, the traceless stress, the records' count flux and the shears (Y-S1, Y-S3; the carrier's act node.act, the former `carried` by this name); every riding line's one carried division at the mean wall of the carrier's two levels at its end times the row's scale, its remainder kept in [0, W) there, backward the turned Nodes set to their kept pre-state; the records' lines at the start and after the step kept for the close; the rows set; forward the lays among the divisions after them (`lays`; backward they came off first); then every line at a frozen Node restored to its held line, its levels, its remainders and its wall by the Node's one restore (BH-S1, the former `rest`), so no act but the swap changes any integer of a frozen Node's state in either direction; backward a Node both frozen and turned is restored to the pre-state the exchange returned (FR-S1)."""
        node, carrier = self.node, self.carrier
        k = self.where[id(carrier)]
        p02 = self.p0 * self.p0
        numerators = [
            held_numerator(node.trace, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma)
        ]
        numerators += [part * p02 for part in (*self.traceless, *self.flux, *self.shear)]
        rule = node.rule_of(carrier, self.c, self.factors)
        self.out[k] = node.act(
            self.rows[k], rule, None, numerators, self.direction, None, *self.ends(carrier)
        )[-1]
        w_div = self.mean_wall(self.out[k][0])
        for r in self.riders:
            k = self.where[id(r)]
            ws = self.scales[k] * w_div
            new = []
            for a, p, line in zip(self.starts[k], self.kicked[k], self.rows[k], strict=True):
                v, rem = divide(p, ws, half(ws))
                now, before = (a + self.direction * v, a)[:: self.direction]
                new.append(Line(now, before, rem, ws, line.wr, line.wwall))
            if self.direction == -1 and self.kept is not None:
                node.restore(new, self.kept[k], self.top)
            self.out[k] = new
            if r in self.records:
                start = self.rows[k] if self.direction == 1 else new
                after = new if self.direction == 1 else self.held[k]
                self.plane_starts.append(list(start))
                self.stepped.append([line.copy() for line in after])
        node.stepped = self.stepped
        node.set_rows(self.out)
        if self.direction == 1:
            self.lays()
        if self.direction == -1 and self.kept is not None:
            node.restore(
                node.all_lines(), [line for row in self.kept for line in row], self.frozen & self.top
            )
        node.restore(
            node.all_lines(), [line for row in self.held for line in row], self.frozen & ~self.top
        )

    def lays(self) -> None:
        """The lays among the divisions (the former `writes` and `unwrite`), each one carried division at the line's write wall T with the carry kept in its write remainder (node.write), on the rows as the Node holds them at the end: the emitter's line's W-S1 lay, the emission over the carrier's mean wall at the end at the common scale, its quotient rounded odd (EM-S1's odd rounding, paces.rounded: the lay exactly odd under the sense's flip, the former floor kept by name), its size counted forward (`laid_on`), its booking per Node laid written on the carrier's flux lines by the Node's write act (take.recoil, LT-S1: the emission's lay taken into the clause), its bookings kept in the interval's frame for the run back and undone at -1 by the same act, the last first, after the swap's undoing and before the writes come off, at no still Node (turned or frozen), where the swap or the restore wiped the forward's booking with the lay; the shape-4 row's current at the start on its three odd lines, its time line's numerator None (its charge landed at the kick, PL-S1); forward after every line's division, backward the first act to come off."""
        node = self.node
        line, carrier = node.emitter().lines[0], node.row(CARRIER).lines[0]
        levels = line.now
        wall = self.common * self.mean_wall(carrier)
        node.write(line, paces.rounded(self.emission, wall), self.direction)
        if self.direction == 1:
            laid_on(node, line, levels)
        if self.direction == -1:
            for at, dp, clock in reversed(self.bookings):
                if not self.still[at]:
                    recoil(node, at, dp, clock, -1)
        else:
            laid, pair = line.now - levels, node.emitter().pair
            assert pair is not None
            for at in (at for at in np.ndindex(node.shape) if int(laid[at])):
                dp = momentum_of(node, line.now, line.before, at, d_now=int(laid[at]), num=pair[0])
                self.bookings.append((at, dp, int(node.start_clock[at])))
                recoil(node, at, dp, int(node.start_clock[at]), 1)
        for line, n in zip(node.row(POTENTIAL).lines, [None, *self.current], strict=True):
            if n is not None:
                node.write(line, n, self.direction)

    def swap(self) -> None:
        """(4) The swap at the top and the floor (node.swap; the frozen Node released by its own trigger, FR-S1): the weak maximum of the carrier's three levels, the held before, the held now and the now after the lays, or an outer one below the floor; the turned Node ends the interval at its held pre-state, exchanged and complemented."""
        self.top = self.node.swap(self.held)

    def close(self) -> None:
        """(5) The close (close.click) after the swap, the frame pushed for the run back: the turned Nodes, the counters as they stood before the click (the swap changes none), the log's length and the frozen mask."""
        node = self.node
        log_from = len(node.log)
        kept = frame(node, self.top, log_from, self.frozen, self.bookings)
        node.click(self.plane_starts, self.held)
        node.stack.append(kept)


def run(node: Node, direction: int) -> None:
    """One interval in the direction, five acts: the readings, the kick, the division, the swap at the top, the close; backward the close and the swap are undone at the Interval's making, the lays come off before the kick (the reverse order: the last laid, the first undone), the kick and the division are the same acts at -1 and the interval is counted down."""
    interval = Interval(node, direction)
    acts = {
        1: (interval.kick, interval.division, interval.swap, interval.close),
        -1: (interval.lays, interval.kick, interval.division),
    }
    for act in (interval.readings, *acts[direction]):
        act()
