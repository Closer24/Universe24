"""The interval, the Node's one program in both directions (ALGEBRA.md, The direction: every act but the click a bijection; the run back the same acts in the reverse order, each inverted), in the symmetric ride's form (R5; the owner's approved sentence 1 of 2026-10-25, the held carrier of the wall and every riding row step as one pair at the mean wall): the readings at the start (the frozen mask among them, BH-S1), the walled row's act, every riding line's force and kick, the carrier's one division sourced by the riding momenta, every riding line's one division at the mean wall of the carrier's two levels, the riding rows' writes from numbers known before them, the swap at the top and the close; one class holds the interval's readings so that each act is one short function."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram, readings
from event_universe.core import paces
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import division_forward, half, held_numerator, quotient
from event_universe.features import volume
from event_universe.links import links_of, stress_parts, tensor_parts
from event_universe.rows import CARRIER, PLANE, POTENTIAL, TRACE, Line, Row, zeros

if TYPE_CHECKING:
    from event_universe.node import Node


def laid_on(node: Node, line: Line, levels: Any) -> None:
    """The emission's size, a reading of the run: the levels laid on the gap-0 line and the Nodes they were laid at."""
    laid = line.now - levels
    node.counts["laid"] += int(sum(abs(int(x)) for x in laid.reshape(-1)))
    node.counts["laid_nodes"] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))


class Interval:
    """One interval's readings at its start and the rows as the acts leave them, in the direction given: forward from the pre-state; backward from the post-state with the close undone and the turned Nodes returned to their pre-state by the same exchange."""

    def __init__(self, node: Node, direction: int) -> None:
        self.node, self.direction = node, direction
        if direction == 1:
            node.interval += 1
            self.top: Any = np.zeros(node.shape, dtype=bool)
            self.kept: list[list[Line]] | None = None
            self.frozen: Any = None
        else:
            frame = node.stack.pop()
            node.click([], [], -1, frame)
            self.top = frame["turned"]
            self.frozen = frame["frozen"]
        self.still: Any = self.top if self.frozen is None else self.top | self.frozen
        self.held = [[line.copy() for line in row] for row in node.rows()]
        if direction == -1:
            if self.top.any():
                node.exchange(self.top, self.held)
            self.kept = [[line.copy() for line in row] for row in node.rows()]
        self.rows = node.rows()
        self.where = {id(r): k for k, r in enumerate(node.rows_)}
        self.carrier, self.walled = node.row(CARRIER), node.walled()
        self.potential, self.gap0 = node.row(POTENTIAL), node.row(PLANE, gap=0)
        self.riders = [r for r in node.rows_ if r.wall is None and r is not self.carrier]
        self.records = node.records()
        self.gapped = [r for r in self.riders if r.gap]
        self.scales = {self.where[id(r)]: gram.scale(r.shape, node.gamma) for r in self.riders}
        self.common = max(self.scales.values())
        self.out: list[list[Line]] = [[] for _ in self.rows]
        self.plane_starts: list[list[Line]] = []
        self.stepped: list[list[Line]] = []
        self.w_half = half(node.w)
        self.readings()

    def at(self, line: Line) -> Any:
        """A line's start level: forward the now slot; backward the before slot, and the now slot at a still Node, turned or frozen (BH-S1), which ended the interval at its pre-state."""
        return line.now if self.direction == 1 else np.where(self.still, line.now, line.before)

    def lines(self, row: Row) -> list[Line]:
        """A row's lines as the interval holds them."""
        return self.rows[self.where[id(row)]]

    def ends(self, row: Row) -> tuple[Any, list[Line] | None]:
        """The turned Nodes and the row's kept pre-state for an act backward."""
        return self.top, None if self.kept is None else self.kept[self.where[id(row)]]

    def readings(self) -> None:
        """The readings at the start: the content and the clock, the Link factors, the frames, the clocked potential, the carrier's level and the stress of the planes."""
        node = self.node
        self.c = np.asarray(volume.level_of(node.gamma, self.at(self.carrier.lines[0])), dtype=object)
        node.start_content = self.c
        self.p0, self.pi = readings.paces_of(node, self.c)
        if self.frozen is None:
            self.frozen = readings.frozen_of(node, self.c)
            self.still = self.top | self.frozen
        node.proper = node.proper + self.direction * np.where(self.frozen, 0, self.p0)
        self.factors = node.link_factors(
            [self.at(line) for line in self.carrier.lines[1 : 1 + AXES]], self.frozen
        )
        node.start_factors = self.factors
        self.frames = readings.frames(node, self.walled.lines[0].rem)
        node.start_frames = self.frames
        self.cphi = paces.odd_rounded(self.at(self.potential.lines[0]) * self.p0, node.gamma)
        self.x_now = self.at(self.carrier.lines[0])
        node.start_x = self.x_now
        stress = stress_parts(
            [
                ([self.at(line) for line in r.lines], r.pair[0], gram.gram(r.shape))
                for r in self.records
                if r.pair
            ],
            node.shape,
        )
        self.trace, self.traceless = tensor_parts(stress)

    def walled_act(self) -> None:
        """The walled row first: its act carries its own write; the Links' count and phases come from it, and the six Links' records (the factor, the frame, the pair, the odd part) are read once for the planes' turn."""
        node, walled = self.node, self.walled
        k = self.where[id(walled)]
        rule = node.rule_of(walled, self.c, self.factors)
        (phi_start,), _levels, self.out[k] = node.act(
            self.rows[k], rule, None, [None], self.direction, [2 * self.cphi], *self.ends(walled)
        )
        count = readings.centred_count(node, self.cphi, phi_start)
        node.count_max = max(
            int(abs(int(x)))
            for port in range(PORTS)
            for x in (count - self.frames[port] * across(count, port)).reshape(-1)
        )
        self.phases = readings.link_phases(node, self.frames, count)
        self.odd = [self.at(line) for line in self.potential.lines[1 : 1 + AXES]]
        node.start_phases, node.start_odd = self.phases, [o.copy() for o in self.odd]
        self.links = links_of(self.factors, self.frames, self.phases, self.odd)
        self.curl = gram.curl(self.odd)

    def forces(self) -> None:
        """Every riding line's force at the start, SUM_j R_j (m_j - a) - D a plus the row's Node term by shape (gram.term, the coefficient the unscaled reaches' sum), a riding row with a gap turned by the Links; the records' charge and current at this end; and the emission read from the kick, X_now SUM over the records with a gap of F.GJ.N (the plane's re F_im - im F_re), each over its scale against the common one."""
        node = self.node
        self.w_end = zeros(node.shape)
        self.current = [zeros(node.shape) for _ in range(AXES)]
        for r in self.gapped:
            self.w_end = self.w_end + gram.charge(r.shape, self.lines(r))
            nows = [self.at(line) for line in self.lines(r)]
            for a, j_a in enumerate(gram.current(r.shape, nows, self.frames)):
                self.current[a] = self.current[a] + j_a
        self.starts: dict[int, list[Any]] = {}
        self.force: dict[int, list[Any]] = {}
        self.walls: dict[int, Any] = {}
        for r in self.riders:
            rule = node.rule_of(r, self.c, self.factors)
            turn = self.links if r.gap else None
            k = self.where[id(r)]
            self.walls[k] = rule.wall
            self.starts[k] = [self.at(line) for line in self.lines(r)]
            arrivals = node.arrivals(self.starts[k], rule, turn)
            coefficient = quotient(sum(rule.reaches), self.scales[k])
            added = gram.term(r.shape, coefficient, self.curl, self.starts[k])
            self.force[k] = [
                m + t - (2 * rule.wall - rule.self_coefficient) * a
                for a, m, t in zip(self.starts[k], arrivals, added, strict=True)
            ]
        self.emission = zeros(node.shape)
        for r in self.gapped:
            k = self.where[id(r)]
            gj = gram.matmul(gram.gram(r.shape), gram.rotation(r.shape))
            flow = gram.form(gj, self.force[k], self.starts[k])
            self.emission = self.emission + self.x_now * flow * quotient(self.common, self.scales[k])

    def mean_wall(self) -> Any:
        """The mean wall (w div 2)(X_before + X_now) of the carrier's two levels as the rows hold them: forward W_in from the pre carrier, backward W_out from the post carrier."""
        return self.w_half * (self.carrier.lines[0].before + self.carrier.lines[0].now)

    def unwrite(self) -> None:
        """Backward: the riding rows' writes come off first, from the post state (the gap-0 line's W-S1 lay at the post mean wall at the common scale, the emission's quotient rounded odd as the forward write rounds it, the shape-4 row's 2 W and the current)."""
        node = self.node
        node.write(
            self.lines(self.gap0)[0],
            paces.odd_rounded(self.emission, self.common * self.mean_wall()),
            -1,
        )
        for line, n in zip(self.lines(self.potential), [2 * self.w_end, *self.current], strict=True):
            node.write(line, n, -1)

    def kicks(self) -> None:
        """Every riding line's momentum in and out at the mean wall times the row's scale, P_in = W (a_now - a_before) + r - W div 2 and P_out = P_in + X_now F, and the carrier's source from every riding row alike with its G, line by line u_in (G u_out) + (-a (G F)) div w with u the odd rounding of 2 P + 1 over 2 w X_now at the scale, w the row's wall."""
        node = self.node
        self.forms = zeros(node.shape)
        self.kicked: dict[int, list[Any]] = {}
        d = 2 * node.w * self.x_now
        w_side = self.mean_wall()
        for r in self.riders:
            k = self.where[id(r)]
            ws, ds, g = self.scales[k] * w_side, self.scales[k] * d, gram.gram(r.shape)
            p_side = [ws * (line.now - line.before) + line.rem - half(ws) for line in self.rows[k]]
            p_other = [
                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)
            ]
            u_in = [paces.odd_rounded(2 * p + 1, ds) for p in p_side]
            u_out = [paces.odd_rounded(2 * p + 1, ds) for p in p_other]
            pulls = gram.weighted(g, self.starts[k], self.force[k])
            for product, pull in zip(gram.weighted(g, u_in, u_out), pulls, strict=True):
                self.forms = self.forms + product + quotient(-pull, self.walls[k])
            self.kicked[k] = p_other

    def carrier_act(self) -> None:
        """The carrier: its one division with the write sourced by the riding rows' momenta, 4 X (forms 54 den Gamma^2 - trace p_0^2) p_0 on its time line and the traceless stress times p_0^2 on its axis lines; the mean wall of its two levels at the end for the riding lines' divisions."""
        node, carrier = self.node, self.carrier
        k = self.where[id(carrier)]
        p02 = self.p0 * self.p0
        numerators = [
            held_numerator(TRACE, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma)
        ]
        numerators += [self.traceless[a] * p02 for a in range(AXES)] + [None] * (
            carrier.shape - 1 - AXES
        )
        self.out[k] = node.carried(
            self.rows[k],
            node.rule_of(carrier, self.c, self.factors),
            numerators,
            self.direction,
            *self.ends(carrier),
        )
        xc = self.out[k][0]
        self.w_div = self.w_half * (xc.before + xc.now)

    def divisions(self) -> None:
        """Every riding line divides once at the mean wall of the carrier's two levels at its end times its row's scale, its remainder kept in [0, W) there; the records' lines at the start and after the step kept for the close, the charge after summed for the shape-4 row's write."""
        node = self.node
        self.w_after = zeros(node.shape)
        for r in self.riders:
            k = self.where[id(r)]
            ws = self.scales[k] * self.w_div
            new = []
            for a, p, line in zip(self.starts[k], self.kicked[k], self.rows[k], strict=True):
                v, rem = division_forward(p, ws, half(ws))
                new.append(
                    Line(a + v, a, rem, ws, line.wr, line.wwall)
                    if self.direction == 1
                    else Line(a, a - v, rem, ws, line.wr, line.wwall)
                )
            if self.direction == -1 and self.kept is not None:
                node.restore(new, self.kept[k], self.top)
            self.out[k] = new
            if r in self.records:
                start = self.rows[k] if self.direction == 1 else new
                after = new if self.direction == 1 else self.held[k]
                self.plane_starts.append(list(start))
                self.stepped.append([line.copy() for line in after])
                if r.gap:
                    self.w_after = self.w_after + gram.charge(r.shape, after)
        node.stepped = self.stepped

    def writes(self) -> None:
        """Forward: the riding rows' writes after the divisions, from numbers known before them: the gap-0 line's W-S1 lay, the emission over the mean wall after at the common scale, its quotient rounded odd (EM-S1's odd rounding, paces.odd_rounded: the write exactly odd under the sense's flip, the former floor kept by name); the shape-4 row's 2 W of the records after the step and the current at the start."""
        node = self.node
        laid_line = self.out[self.where[id(self.gap0)]][0]
        before_write = laid_line.now
        node.write(laid_line, paces.odd_rounded(self.emission, self.common * self.w_div), 1)
        laid_on(node, laid_line, before_write)
        for line, n in zip(
            self.out[self.where[id(self.potential)]], [2 * self.w_after, *self.current], strict=True
        ):
            node.write(line, n, 1)

    def rest(self) -> None:
        """BH-S1: every line at a frozen Node restored to the held line after the acts (its levels, its remainders and its wall, by the Node's one restore), so no act changes any integer of a frozen Node's state in either direction."""
        self.node.restore(
            self.node.all_lines(), [line for row in self.held for line in row], self.frozen
        )

    def close(self) -> None:
        """Forward after the acts: the swap at the top, the close, the frame pushed for the run back."""
        node = self.node
        counters = (
            [a.copy() for a in node.standing],
            [a.copy() for a in node.crossed],
            [a.copy() for a in node.beats],
        )
        top = node.swap(self.held, self.frozen)
        log_from = len(node.log)
        node.click(self.plane_starts, self.held)
        node.stack.append(
            {"turned": top, "counters": counters, "log_from": log_from, "frozen": self.frozen}
        )


def run(node: Node, direction: int) -> None:
    """One interval in the direction: the readings, the walled row's act, the forces, (backward the writes undone), the kicks, the carrier's act, the riding lines' divisions, (forward the writes), the rows set; forward then the swap and the close, backward the interval counted down."""
    interval = Interval(node, direction)
    interval.walled_act()
    interval.forces()
    if direction == -1:
        interval.unwrite()
    interval.kicks()
    interval.carrier_act()
    interval.divisions()
    if direction == 1:
        interval.writes()
    node.set_rows(interval.out)
    interval.rest()
    if direction == -1:
        node.interval -= 1
        return
    interval.close()
