"""The interval, the Node's one program in both directions (ALGEBRA.md, The interval; The direction: every act but the click a bijection, the run back the same acts in the reverse order, each inverted), in the symmetric ride's form (R5; the owner's approved sentence 1 of 2026-10-25: the held carrier of the wall and every riding row step as one pair at the mean wall): five acts of two kinds, the carried division (core/rule3.acts.divide (the former carried_division kept by name), the paces' odd rounding where the law has it) and the lay; (1) the readings at the start (the content, the rulers, the Links' count and phases from the walled row's act, every riding line's force, the records' current and the emission), (2) the kick (every riding line's momentum read at the mean wall and kicked, the records' charge at the kick among them, PL-S1, the carrier's source from every riding row alike, the records' count flux on each axis from the velocities in and out against the centred gradient, Y-S3), (3) the division (the carrier's one division, every riding line's one division at the mean wall of the carrier's two levels at its end, the lays among the divisions, the rows set, the frozen Nodes' lines restored, BH-S1), (4) the swap at the top and the floor, (5) the close; backward the close and the swap are undone first, the lays come off before the kick and every division is the same act at -1; one class holds the interval's readings so that each act is one function."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import hands, readings
from event_universe.core import rates
from event_universe.core.acts import carry, mid
from event_universe.core.rule3 import carries, held_numerator
from event_universe.core.spokes import AXES, SPOKES, across, spoke_of, transverse
from event_universe.features import stretch
from event_universe.meshes import centred_count, coupling_of, factors, meshes_of, offsets, pawls, skewed
from event_universe.regulation import net_flow, rest_rate_of, shear_parts, stress_parts, tensor_parts
from event_universe.run import rewind_note
from event_universe.trains import OFFSET, REGULATOR, Gear, Train, ratchet_of, zeros
from event_universe.unwind import push_of, recoil

if TYPE_CHECKING:
    from event_universe.clock import Clock


def advanced_on(node: Clock, line: Gear, levels: Any) -> None:
    """The emission's size, a reading of the run: the levels laid on the emitter's line and the Nodes they were laid at."""
    laid = line.now - levels
    node.counts["laid"] += int(sum(abs(int(x)) for x in laid.reshape(-1)))
    node.counts["laid_nodes"] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))


class Tick:
    """One interval's readings at its start and the rows as the acts leave them, in the direction given: forward from the pre-state, the interval counted up; backward from the post-state with the close undone (5, close.click at -1) and the turned Nodes returned to their pre-state by the swap's own exchange (4), the acts inverted in the reverse order."""

    def __init__(self, node: Clock, direction: int) -> None:
        self.clock, self.going = node, direction
        node.ticks += direction
        if direction == 1:
            self.top: Any = np.zeros(node.size, dtype=bool)
            self.kept: list[list[Gear]] | None = None
            self.stopped: Any = None
            self.tallies: list[tuple[tuple[int, ...], list[int], int]] = []
        else:
            frame = node.stack.pop()
            node.strike([], [], -1, frame)
            self.top = frame["turned"]
            self.stopped = frame["frozen"]
            self.tallies = frame["bookings"]
        self.still: Any = self.top if self.stopped is None else self.top | self.stopped
        self.held = [[line.copy() for line in row] for row in node.trains()]
        if direction == -1:
            node.turnover(self.held, -1, self.top)
            self.kept = [[line.copy() for line in row] for row in node.trains()]
        self.trains = node.trains()
        self.where = {id(r): k for k, r in enumerate(node.trains_)}
        self.regulator, self.ratchet = node.train(REGULATOR), ratchet_of(node.trains_)
        self.offset, self.unsprung = node.train(OFFSET), node.unsprung()
        self.driven = [r for r in node.trains_ if r.teeth is None and r is not self.regulator]
        self.hands = node.hands()
        self.hand_couplings = [(r, coupling_of(r)) for r in self.hands]
        self.out: list[list[Gear]] = [[] for _ in self.trains]
        self.hand_starts: list[list[Gear]] = []
        self.before_turnover: list[list[Gear]] = []

    def at(self, line: Gear) -> Any:
        """A line's start level: forward the now slot; backward the before slot, and the now slot at a still Node, turned or frozen (BH-S1), which ended the interval at its pre-state."""
        return line.now if self.going == 1 else np.where(self.still, line.now, line.before)

    def gears(self, row: Train) -> list[Gear]:
        """A row's lines as the interval holds them."""
        return self.trains[self.where[id(row)]]

    def ends(self, row: Train) -> tuple[Any, list[Gear] | None]:
        """The turned Nodes and the row's kept pre-state for an act backward."""
        return self.top, None if self.kept is None else self.kept[self.where[id(row)]]

    def readings(self) -> None:
        """(1) The readings at the start (the former `readings`, `walled_act` and `forces`): the content and the clock, the frozen mask (BH-S1), the proper count resting at a frozen Node, the Link factors with a frozen end at the wall, the frames, the clocked potential, the carrier's level and the stress of the planes; the walled row's act, one carried division with the flux 2 c Phi inside it (its start the Links' count K = 2 (Phi_now - Phi_before) + c, backward recovered by the inverse division alone), the six Links' records read once per coupling present among the records (links.coupling_of; the frame sign, the count and the odd part at the coupling, so the turn at the coupling 0 is the identity by arithmetic); the records' current at this end, each at its coupling; every riding line's force, SUM_j R_j (m_j - a) - D a, every record turned by the Links at its coupling and by the flux lines' fold at its rest rotation (links.folded, Y-S3; the row at the gap 0 by nothing); and the emission, X_now SUM over the records with a gap of F.J.N (the plane's re F_im - im F_re)."""
        self.rate_readings()
        self.standard_rate()
        self.pulls()

    def rate_readings(self) -> None:
        """The Node's clock at the start: its content and paces, the frozen mask, the proper count, the Link factors, the frames, the clocked potential, the carrier's level and the planes' stress."""
        node = self.clock
        self.load = np.asarray(
            stretch.load_of(node.full_rate, self.at(self.regulator.gears[0])), dtype=object
        )
        node.start_load = self.load
        self.rate, self.mesh_rate = readings.rates_of(node, self.load)
        node.start_rate = self.rate
        if self.stopped is None:
            self.stopped = readings.stopped_of(node, self.load)
            self.still = self.top | self.stopped
        node.dial = node.dial + self.going * np.where(self.stopped, 0, self.rate)
        self.factors = factors(
            node, [self.at(line) for line in self.regulator.gears[1 : 1 + AXES]], self.stopped
        )
        node.start_factors = self.factors
        self.pawls = pawls(self.ratchet.gears[0].fine)
        node.start_pawls = self.pawls
        self.clocked_offset = rates.rounded(self.at(self.offset.gears[0]) * self.rate, node.full_rate)
        self.stretch_now = self.at(self.regulator.gears[0])
        node.start_stretch = self.stretch_now
        sources = [([self.at(line) for line in r.gears], r.ratio[0]) for r in self.hands if r.ratio]
        self.trace, self.traceless = tensor_parts(stress_parts(sources, node.size))
        self.shear = shear_parts(sources, node.size)
        self.flow_gears = [self.at(line) for line in self.regulator.gears[1 + AXES : 1 + AXES + AXES]]

    def standard_rate(self) -> None:
        """The walled row's act, the Node's phase clock (one carried division with the flux 2 c Phi inside it), and the six Links read once per coupling present among the records."""
        node = self.clock
        k, flux = self.where[id(self.ratchet)], [self.clocked_offset + self.clocked_offset]
        rule, ends = (
            readings.gearing_of(node, self.ratchet, self.load, self.factors),
            self.ends(self.ratchet),
        )
        act = node.act(self.trains[k], rule, None, [None], self.going, flux, *ends)
        (phi_start,), self.out[k] = act
        count = centred_count(self.clocked_offset, phi_start)
        node.count_max = max(
            int(abs(int(x)))
            for port in range(SPOKES)
            for x in (count - self.pawls[port] * across(count, port)).reshape(-1)
        )
        self.offsets = offsets(node, self.pawls, count)
        self.odd = [self.at(line) for line in self.offset.gears[1 : 1 + AXES]]
        node.start_offsets, node.start_odd = self.offsets, [o.copy() for o in self.odd]
        self.meshes_at = {
            c: meshes_of(
                self.factors,
                [f**c for f in self.pawls],
                self.offsets if c == 1 else offsets(node, self.pawls, count * c),
                [o * c for o in self.odd],
            )
            for c in sorted({c for _r, c in self.hand_couplings})
        }

    def pulls(self) -> None:
        """The records' current at this end, every riding line's force SUM_j R_j (m_j - a) - D a with each record turned by its Links and the flux lines' fold, and the emission."""
        node = self.clock
        self.lead = [zeros(node.size) for _ in range(AXES)]
        for r, cpl in self.hand_couplings:
            nows = [self.at(line) for line in self.gears(r)]
            for a, j_a in enumerate(hands.lead(r.size, nows, self.pawls)):
                self.lead[a] = self.lead[a] + cpl * j_a
        self.starts: dict[int, list[Any]] = {}
        self.pull: dict[int, list[Any]] = {}
        self.train_teeth: dict[int, Any] = {}
        for r in self.driven:
            rule = readings.gearing_of(node, r, self.load, self.factors)
            turn = None
            if r in self.hands:
                assert r.ratio is not None
                rotation = coupling_of(r) * rest_rate_of(node, r.ratio)
                turn = skewed(self.meshes_at[coupling_of(r)], rotation, self.flow_gears, node.full_rate)
            k = self.where[id(r)]
            self.train_teeth[k] = rule.teeth
            self.starts[k] = [self.at(line) for line in self.gears(r)]
            arrivals = node.pulls(self.starts[k], rule, turn)
            self.pull[k] = [
                m - (rule.teeth + rule.teeth - rule.hold) * a
                for a, m in zip(self.starts[k], arrivals, strict=True)
            ]
        self.spin_gear()
        self.release = zeros(node.size)
        for r, cpl in self.hand_couplings:
            k = self.where[id(r)]
            flow = cpl * hands.form(hands.quarter(r.size), self.pull[k], self.starts[k])
            self.release = self.release + self.stretch_now * flow

    def spin_gear(self) -> None:
        """The doublet's coupling (SR-S3 on two planes): the one-Link curl Phi of the potential's odd lines at the start turns a row of two planes by the Pauli matrices on its four lines (re_up, im_up, re_dn, im_dn): sigma_x swaps the planes, sigma_y = i sigma_x sigma_z, sigma_z negates the down plane; per line the numerator SUM_j R_j SUM_a Phi_a (sigma_a x), one carried division at the line's write wall 2 PORTS Gamma, the quotient added to the line's force (the coefficient R / (2 Gamma) per Port, g = 2), the remainder carried in the line."""
        node = self.clock

        def gradient(a: Any, axis: int) -> Any:
            return across(a, spoke_of(axis, 0)) - across(a, spoke_of(axis, 1))

        curl = []
        for a in range(AXES):
            b, c = transverse(a)
            curl.append(gradient(self.odd[c], b) - gradient(self.odd[b], c))
        cx, cy, cz = curl
        for r in self.hands:
            if r.partner is None or self.hands.index(r) > self.hands.index(r.partner):
                continue
            ku, kd = self.where[id(r)], self.where[id(r.partner)]
            (u3, u12), (d3, d12) = self.starts[ku], self.starts[kd]
            sx, sy, sz = (d3, d12, u3, u12), (d12, -d3, -u12, u3), (u3, u12, -d3, -d12)
            reach = sum(readings.gearing_of(node, r, self.load, self.factors).grips)
            gears = [*self.gears(r), *self.gears(r.partner)]
            slots = ((ku, 0), (ku, 1), (kd, 0), (kd, 1))
            for (k, i), gear, x, y, z in zip(slots, gears, sx, sy, sz, strict=True):
                q, gear.dfine = carry(
                    reach * (cx * x + cy * y + cz * z), gear.dteeth, gear.dfine, self.going
                )
                self.pull[k][i] = self.pull[k][i] + q

    def impulse(self) -> None:
        """(2) The kick (the former `kicks`): every riding line's momentum at the start read at the mean wall of the carrier's two levels as the rows hold them, P = W (a_now - a_before) + r - W div 2, and kicked by X_now F in the direction; the shape-4 row's time line kicked besides by the records' charge read at the kick (PL-S1, the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423: SUM over the records with a gap of N.J.u_in + N.J.u_out, N the levels at the start and u the odd rounding of 2 P + 1 over 2 w X_now, the plane's -(re u_im - im u_re) in and out, the same integers in either direction and its own mirror under the exchange and the conjugation; one carried division at the line's write wall T with the carry kept in its write remainder, the quotient landing as the kick w X_now q before the line's one division; the charge summed over the records before the shape-4 row is met, which rests on rows.order_of, H-Confirm-Build-11; the former level write of 2 W of the records after the step kept by name: a source pinned to the step's end, whose mirror under the exchange is a start, so the fall wrote 2 W(top - 1 - k) where the inverted recurrence needs 2 W(top - k)); and the carrier's source from every riding row alike, line by line u_in u_out + (-a F) div w, w the row's wall."""
        node = self.clock
        self.forms = zeros(node.size)
        self.impelled: dict[int, list[Any]] = {}
        d = (node.teeth + node.teeth) * self.stretch_now
        w_side = readings.mean_teeth(self.clock, self.regulator.gears[0])
        charge = zeros(node.size)
        self.flow = [zeros(node.size) for _ in range(AXES)]
        for r in self.driven:
            k = self.where[id(r)]
            p_side = [
                w_side * (line.now - line.before) + line.fine - mid(w_side) for line in self.trains[k]
            ]
            p_other = [
                p + self.going * self.stretch_now * f for p, f in zip(p_side, self.pull[k], strict=True)
            ]
            if r is self.offset:
                line = self.trains[k][0]
                q, line.dfine = carry(charge, line.dteeth, line.dfine, self.going)
                p_other[0] = p_other[0] + self.going * node.teeth * self.stretch_now * q
            u_in = [rates.rounded(p + p + 1, d) for p in p_side]
            u_out = [rates.rounded(p + p + 1, d) for p in p_other]
            if r in self.hands:
                gj = hands.quarter(r.size)
                forms = hands.form(gj, self.starts[k], u_in) + hands.form(gj, self.starts[k], u_out)
                charge = charge + coupling_of(r) * forms
                assert r.ratio is not None
                for u in (u_in, u_out):
                    for a in range(AXES):
                        self.flow[a] = self.flow[a] + r.ratio[0] * net_flow(self.starts[k], u, a)
            pulls = hands.products(self.starts[k], self.pull[k])
            for product, pull in zip(hands.products(u_in, u_out), pulls, strict=True):
                self.forms = self.forms + product + carries(-pull, self.train_teeth[k])
            self.impelled[k] = p_other

    def carry(self) -> None:
        """(3) The division (the former `carrier_act`, `divisions`, `writes` and `rest`): the carrier's one division with the write sourced by the riding rows' momenta, 4 X (forms (the file's trace weight) den Gamma^2 - trace p_0^2) p_0 on its time line and, times p_0^2 on its nine axis lines by the position of their reading, the traceless stress, the records' count flux and the shears (Y-S1, Y-S3; the carrier's act node.act, the former `carried` by this name); every riding line's one carried division at the mean wall of the carrier's two levels at its end, its remainder kept in [0, W) there, backward the turned Nodes set to their kept pre-state; the records' lines at the start and before the swap kept for the close (the latter the state the swap replaces at the turned Nodes, the levels now elsewhere, CL-S2; the former `stepped` kept by name); the rows set; forward the lays among the divisions after them (`lays`; backward they came off first); then every line at a frozen Node restored to its held line, its levels, its remainders and its wall by the Node's one restore (BH-S1, the former `rest`), so no act but the swap changes any integer of a frozen Node's state in either direction; backward a Node both frozen and turned is restored to the pre-state the exchange returned (FR-S1)."""
        node, carrier = self.clock, self.regulator
        k = self.where[id(carrier)]
        p02 = self.rate * self.rate
        numerators = [
            held_numerator(
                node.trace, self.stretch_now, self.forms, self.trace, self.rate, node.rim, node.full_rate
            )
        ]
        numerators += [part * p02 for part in (*self.traceless, *self.flow, *self.shear)]
        rule = readings.gearing_of(node, carrier, self.load, self.factors)
        self.out[k] = node.act(
            self.trains[k], rule, None, numerators, self.going, None, *self.ends(carrier)
        )[-1]
        w_div = readings.mean_teeth(self.clock, self.out[k][0])
        for r in self.driven:
            k = self.where[id(r)]
            new = []
            for a, p, line in zip(self.starts[k], self.impelled[k], self.trains[k], strict=True):
                v, rem = carry(p, w_div, mid(w_div))
                now, before = (a + self.going * v, a)[:: self.going]
                new.append(Gear(now, before, rem, w_div, line.dfine, line.dteeth))
            if self.going == -1 and self.kept is not None:
                node.restore(new, self.kept[k], self.top)
            self.out[k] = new
            if r in self.hands:
                start = self.trains[k] if self.going == 1 else new
                after = new if self.going == 1 else self.held[k]
                self.hand_starts.append(list(start))
                self.before_turnover.append([line.copy() for line in after])
        node.before_turnover = self.before_turnover
        node.set_trains(self.out)
        if self.going == 1:
            self.advances()
        if self.going == -1 and self.kept is not None:
            node.restore(
                node.all_gears(), [line for row in self.kept for line in row], self.stopped & self.top
            )
        node.restore(
            node.all_gears(), [line for row in self.held for line in row], self.stopped & ~self.top
        )

    def advances(self) -> None:
        """The lays among the divisions (the former `writes` and `unwrite`), each one carried division at the line's write wall T with the carry kept in its write remainder (node.write), on the rows as the Node holds them at the end: the emitter's line's W-S1 lay, the emission over the carrier's mean wall at the end, its quotient rounded odd (EM-S1's odd rounding, paces.rounded: the lay exactly odd under the sense's flip, the former floor kept by name), its size counted forward (`laid_on`), its booking per Node laid written on the carrier's flux lines by the Node's write act (take.recoil, LT-S1: the emission's lay taken into the clause), its bookings kept in the interval's frame for the run back and undone at -1 by the same act, the last first, after the swap's undoing and before the writes come off, at no still Node (turned or frozen), where the swap or the restore wiped the forward's booking with the lay; the shape-4 row's current at the start on its three odd lines, its time line's numerator None (its charge landed at the kick, PL-S1); forward after every line's division, backward the first act to come off."""
        node = self.clock
        line, carrier = node.unsprung().gears[0], node.train(REGULATOR).gears[0]
        levels = line.now
        wall = readings.mean_teeth(self.clock, carrier)
        node.drive(line, rates.rounded(self.release, wall), self.going)
        if self.going == 1:
            advanced_on(node, line, levels)
        if self.going == -1:
            for at, dp, clock in reversed(self.tallies):
                if not self.still[at]:
                    recoil(node, at, dp, clock, -1)
        else:
            laid, pair = line.now - levels, node.unsprung().ratio
            assert pair is not None
            for at in (at for at in np.ndindex(node.size) if int(laid[at])):
                dp = push_of(node, line.now, line.before, at, d_now=int(laid[at]), num=pair[0])
                self.tallies.append((at, dp, int(node.start_rate[at])))
                recoil(node, at, dp, int(node.start_rate[at]), 1)
        for line, n in zip(node.train(OFFSET).gears, [None, *self.lead], strict=True):
            if n is not None:
                node.drive(line, n, self.going)

    def turnover(self) -> None:
        """(4) The swap at the top and the floor (node.swap; the frozen Node released by its own trigger, FR-S1): the weak maximum of the carrier's three levels, the held before, the held now and the now after the lays, or an outer one below the floor; the turned Node ends the interval at its held pre-state, exchanged and complemented."""
        self.top = self.clock.turnover(self.held)

    def strike(self) -> None:
        """(5) The close (close.click) after the swap, the frame pushed for the run back: the turned Nodes, the counters as they stood before the click (the swap changes none), the log's length and the frozen mask."""
        node = self.clock
        log_from = len(node.log)
        kept = rewind_note(node, self.top, log_from, self.stopped, self.tallies)
        node.strike(self.hand_starts, self.held)
        node.stack.append(kept)


def run(node: Clock, direction: int) -> None:
    """One interval in the direction, five acts: the readings, the kick, the division, the swap at the top, the close; backward the close and the swap are undone at the Interval's making, the lays come off before the kick (the reverse order: the last laid, the first undone), the kick and the division are the same acts at -1 and the interval is counted down."""
    interval = Tick(node, direction)
    acts = {
        1: (interval.impulse, interval.carry, interval.turnover, interval.strike),
        -1: (interval.advances, interval.impulse, interval.carry),
    }
    for act in (interval.readings, *acts[direction]):
        act()
