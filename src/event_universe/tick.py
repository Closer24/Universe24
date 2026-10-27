"""The tick, the clock's one program forward and backward (ALGEBRA.md, The tick; The going: every act but the strike a bijection, the rewind the same acts in the reverse order, each inverted), in the symmetric form of the driven trains (R5; the owner's approved sentence 1 of 2026-10-25: the held regulator of the teeth and every driven train step as one pair at the mean teeth): five acts of two kinds, the carry (core/acts.carry (the former carried_division kept by name), the rates' odd rounding where the law has it) and the advance; (1) the readings at the start (the load, the rulers, the meshes' count and offsets from the ratchet's act, every driven gear's pull, the hands' lead and the release), (2) the impulse (every driven gear's stride read at the mean teeth and impelled, the hands' sweep at the impulse among them, PL-S1, the regulator's source from every driven train alike, the hands' count flow on each axis from the velocities in and out against the centred gradient, Y-S3), (3) the carry (the regulator's one carry, every driven gear's one carry at the mean teeth of the regulator's two notches at its end, the advances among the carries, the trains set, the stopped clocks' gears restored, BH-S1), (4) the turnover at the top and the bottom, (5) the striking; backward the striking and the turnover are undone first, the advances come off before the impulse and every carry is the same act at -1; one class holds the tick's readings so that each act is one function."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import hands, readings
from event_universe.core import rates
from event_universe.core.acts import carry, mid
from event_universe.core.rule3 import carries, held_numerator
from event_universe.core.spokes import AXES, SPOKES, across, transverse
from event_universe.features import stretch
from event_universe.meshes import (
    centred_count,
    coupling_of,
    cross,
    factors,
    gradient,
    meshes_of,
    offsets,
    pawls,
    skewed,
)
from event_universe.regulation import rest_rate_of, stress_of, tensor_parts
from event_universe.run import rewind_note
from event_universe.trains import OFFSET, REGULATOR, Gear, Train, ratchet_of, zeros
from event_universe.unwind import push_of, recoil

if TYPE_CHECKING:
    from event_universe.clock import Clock


def advanced_on(clock: Clock, gear: Gear, notches: Any) -> None:
    """The release's size, a reading of the run: the notches advanced on the unsprung gear and the clocks they were advanced at."""
    advanced = gear.now - notches
    clock.counts["laid"] += int(sum(abs(int(x)) for x in advanced.reshape(-1)))
    clock.counts["laid_nodes"] += int(sum(1 for x in advanced.reshape(-1) if int(x) != 0))


class Tick:
    """One tick's readings at its start and the trains as the acts leave them, in the going given: forward from the pre-state, the tick counted up; backward from the post-state with the striking undone (5, striking.strike at -1) and the turned-over clocks returned to their pre-state by the turnover's own reverse (4), the acts inverted in the reverse order."""

    def __init__(self, clock: Clock, going: int) -> None:
        self.clock, self.going = clock, going
        clock.ticks += going
        if going == 1:
            self.top: Any = np.zeros(clock.size, dtype=bool)
            self.kept: list[list[Gear]] | None = None
            self.stopped: Any = None
            self.tallies: list[tuple[tuple[int, ...], list[int], int]] = []
        else:
            note = clock.stack.pop()
            clock.strike([], [], -1, note)
            self.top = note["turned"]
            self.stopped = note["frozen"]
            self.tallies = note["bookings"]
        self.still: Any = self.top if self.stopped is None else self.top | self.stopped
        self.held = [[gear.copy() for gear in train] for train in clock.trains()]
        if going == -1:
            clock.turnover(self.held, -1, self.top)
            self.kept = [[gear.copy() for gear in train] for train in clock.trains()]
        self.trains = clock.trains()
        self.where = {id(r): k for k, r in enumerate(clock.trains_)}
        self.regulator, self.ratchet = clock.train(REGULATOR), ratchet_of(clock.trains_)
        self.offset, self.unsprung = clock.train(OFFSET), clock.unsprung()
        self.driven = [r for r in clock.trains_ if r.teeth is None and r is not self.regulator]
        self.hands = clock.hands()
        self.hand_couplings = [(r, coupling_of(r)) for r in self.hands]
        self.out: list[list[Gear]] = [[] for _ in self.trains]
        self.hand_starts: list[list[Gear]] = []
        self.before_turnover: list[list[Gear]] = []

    def at(self, gear: Gear) -> Any:
        """A gear's start notch: forward the now slot; backward the before slot, and the now slot at a still clock, turned over or stopped (BH-S1), which ended the tick at its pre-state."""
        return gear.now if self.going == 1 else np.where(self.still, gear.now, gear.before)

    def gears(self, train: Train) -> list[Gear]:
        """A train's gears as the tick holds them."""
        return self.trains[self.where[id(train)]]

    def ends(self, train: Train) -> tuple[Any, list[Gear] | None]:
        """The turned-over clocks and the train's kept pre-state for an act backward."""
        return self.top, None if self.kept is None else self.kept[self.where[id(train)]]

    def readings(self) -> None:
        """(1) The readings at the start (the former `readings`, `walled_act` and `forces`): the load and the rate, the stopped mask (BH-S1), the dial resting at a stopped clock, the mesh factors with a stopped end at the teeth, the pawls, the clocked offset and the regulator's notch; the ratchet's act, one carry with the flow 2 c Phi inside it (its start the meshes' count K = 2 (Phi_now - Phi_before) + c, backward recovered by the inverse carry alone), the six meshes read once per coupling present among the hands (meshes.coupling_of; the pawl, the count and the odd part at the coupling, so the turn at the coupling 0 is the identity by arithmetic); the hands' lead at this end, each at its coupling; every driven gear's pull, SUM_j grip_j (m_j - a) - D a, every hand turned by the meshes at its coupling and by the flow gears' skew at its rest rate (meshes.skewed, Y-S3; the unsprung train by nothing); and the release, stretch_now SUM over the sprung hands of F.J.N (the hand's three F_twelve - twelve F_three)."""
        self.rate_readings()
        self.standard_rate()
        self.pulls()

    def rate_readings(self) -> None:
        """The clock's rate at the start: its load and rates, the stopped mask, the dial, the mesh factors, the pawls, the clocked offset and the regulator's notch."""
        clock = self.clock
        self.load = np.asarray(
            stretch.load_of(clock.full_rate, self.at(self.regulator.gears[0])), dtype=object
        )
        clock.start_load = self.load
        self.rate, self.mesh_rate = readings.rates_of(clock, self.load)
        clock.start_rate = self.rate
        if self.stopped is None:
            self.stopped = readings.stopped_of(clock, self.load)
            self.still = self.top | self.stopped
        clock.dial = clock.dial + self.going * np.where(self.stopped, 0, self.rate)
        self.factors = factors(
            clock, [self.at(gear) for gear in self.regulator.gears[1 : 1 + AXES]], self.stopped
        )
        clock.start_factors = self.factors
        self.pawls = pawls(self.ratchet.gears[0].fine)
        clock.start_pawls = self.pawls
        self.clocked_offset = rates.rounded(self.at(self.offset.gears[0]) * self.rate, clock.full_rate)
        self.stretch_now = self.at(self.regulator.gears[0])
        clock.start_stretch = self.stretch_now
        self.flow_gears = [self.at(gear) for gear in self.regulator.gears[1 + AXES : 1 + AXES + AXES]]

    def standard_rate(self) -> None:
        """The ratchet's act, the clock's standard rate (one carry with the flow 2 c Phi inside it), and the six meshes read once per coupling present among the hands."""
        clock = self.clock
        k, flow = self.where[id(self.ratchet)], [self.clocked_offset + self.clocked_offset]
        gearing, ends = (
            readings.gearing_of(clock, self.ratchet, self.load, self.factors),
            self.ends(self.ratchet),
        )
        act = clock.act(self.trains[k], gearing, None, [None], self.going, flow, *ends)
        (phi_start,), self.out[k] = act
        count = centred_count(self.clocked_offset, phi_start)
        clock.count_max = max(
            int(abs(int(x)))
            for spoke in range(SPOKES)
            for x in (count - self.pawls[spoke] * across(count, spoke)).reshape(-1)
        )
        self.offsets = offsets(clock, self.pawls, count)
        self.odd = [self.at(gear) for gear in self.offset.gears[1 : 1 + AXES]]
        clock.start_offsets, clock.start_odd = self.offsets, [o.copy() for o in self.odd]
        self.meshes_at = {
            c: meshes_of(
                self.factors,
                [f**c for f in self.pawls],
                self.offsets if c == 1 else offsets(clock, self.pawls, count * c),
                [o * c for o in self.odd],
            )
            for c in sorted({c for _r, c in self.hand_couplings})
        }

    def pulls(self) -> None:
        """The hands' lead at this end, every driven gear's pull SUM_j grip_j (m_j - a) - D a with each hand turned by its meshes and the flow gears' skew, and the release."""
        clock = self.clock
        self.lead = [zeros(clock.size) for _ in range(AXES)]
        for r, cpl in self.hand_couplings:
            nows = [self.at(gear) for gear in self.gears(r)]
            for a, j_a in enumerate(hands.lead(nows, self.pawls)):
                self.lead[a] = self.lead[a] + cpl * j_a
        self.starts: dict[int, list[Any]] = {}
        self.pull: dict[int, list[Any]] = {}
        self.train_teeth: dict[int, Any] = {}
        for r in self.driven:
            gearing = readings.gearing_of(clock, r, self.load, self.factors)
            turn = None
            if r in self.hands:
                assert r.ratio is not None
                rotation = coupling_of(r) * rest_rate_of(clock, r.ratio)
                turn = skewed(self.meshes_at[coupling_of(r)], rotation, self.flow_gears, clock.full_rate)
            k = self.where[id(r)]
            self.train_teeth[k] = gearing.teeth
            self.starts[k] = [self.at(gear) for gear in self.gears(r)]
            pulls = clock.pulls(self.starts[k], gearing, turn)
            self.pull[k] = [
                m - (gearing.teeth + gearing.teeth - gearing.hold) * a
                for a, m in zip(self.starts[k], pulls, strict=True)
            ]
        self.twin_pulls()
        self.release = zeros(clock.size)
        for r, cpl in self.hand_couplings:
            k = self.where[id(r)]
            flow = cpl * cross(*self.starts[k], *self.pull[k])
            self.release = self.release + self.stretch_now * flow

    def twin_pulls(self) -> None:
        """The twins' gearing to the offset (SR-S3 on twin hands): the offset's one-mesh curl Phi at the tick's start turns a train of twin hands through the Pauli gearing on its four gears (three_up, twelve_up, three_down, twelve_down): sigma_x swaps the twins, sigma_y = i sigma_x sigma_z, sigma_z reverses the down twin; per gear the numerator SUM_j grip_j SUM_a Phi_a (sigma_a x), one carry at the gear's drive teeth SPOKES (full rate + full rate), the carries added to the gear's pull (the coefficient grip / (2 full rate) per spoke, g = 2), the fine tooth kept on the gear's drive wheel."""
        clock = self.clock
        cx, cy, cz = offset_curl(self.odd)
        for r in self.hands:
            if r.twin is None or self.hands.index(r) > self.hands.index(r.twin):
                continue
            ku, kd = self.where[id(r)], self.where[id(r.twin)]
            up, dn = self.starts[ku], self.starts[kd]
            grip = sum(readings.gearing_of(clock, r, self.load, self.factors).grips)
            pauli = (
                (r, ku, dn, (dn[1], -dn[0]), up),
                (r.twin, kd, up, (-up[1], up[0]), [-g for g in dn]),
            )
            for hand, k, sx, sy, sz in pauli:
                for i, gear in enumerate(self.gears(hand)):
                    numerator = grip * (cx * sx[i] + cy * sy[i] + cz * sz[i])
                    q, gear.dfine = carry(numerator, gear.dteeth, gear.dfine, self.going)
                    self.pull[k][i] = self.pull[k][i] + q

    def impulse(self) -> None:
        """(2) The impulse (the former `kicks`): every driven gear's stride at the start read at the mean teeth of the regulator's two notches as the trains hold them, P = W (a_now - a_before) + r - W div 2, and impelled by stretch_now F in the going; the offset train's time gear impelled besides by the hands' sweep read at the impulse (PL-S1, the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423: SUM over the sprung hands of N.J.u_in + N.J.u_out, N the notches at the start and u the odd rounding of 2 P + 1 over 2 w stretch_now, the hand's -(three u_twelve - twelve u_three) in and out, the same integers forward and backward and its own image under the exchange and the reflection; one carry at the gear's drive teeth T with the carry kept in its drive fine tooth, the carries landing as the impulse w stretch_now q before the gear's one carry; the sweep summed over the hands before the offset train is met, which rests on trains.order_key, H-Confirm-Build-11; the former notch drive of 2 W of the hands after the step kept by name: a source pinned to the step's end, whose image under the exchange is a start, so the fall drove 2 W(top - 1 - k) where the inverted recurrence needs 2 W(top - k)); and the regulator's source from every driven train alike, gear by gear u_in u_out + (-a F) div w, w the train's teeth; and every hand's stress, one outer product of its start notches' gradients and its velocity u_in + u_out (regulation.stress_of)."""
        clock = self.clock
        self.forms = zeros(clock.size)
        self.impelled: dict[int, list[Any]] = {}
        d = (clock.teeth + clock.teeth) * self.stretch_now
        w_side = readings.mean_teeth(self.clock, self.regulator.gears[0])
        sweep = zeros(clock.size)
        self.stress = [zeros(clock.size) for _ in range(REGULATOR - 1)]
        for r in self.driven:
            k = self.where[id(r)]
            p_side = [
                w_side * (gear.now - gear.before) + gear.fine - mid(w_side) for gear in self.trains[k]
            ]
            p_other = [
                p + self.going * self.stretch_now * f for p, f in zip(p_side, self.pull[k], strict=True)
            ]
            if r is self.offset:
                gear = self.trains[k][0]
                q, gear.dfine = carry(sweep, gear.dteeth, gear.dfine, self.going)
                p_other[0] = p_other[0] + self.going * clock.teeth * self.stretch_now * q
            u_in = [rates.rounded(p + p + 1, d) for p in p_side]
            u_out = [rates.rounded(p + p + 1, d) for p in p_other]
            if r in self.hands:
                velocity = [x + y for x, y in zip(u_in, u_out, strict=True)]
                sweep = sweep + coupling_of(r) * cross(*velocity, *self.starts[k])
                assert r.ratio is not None
                found = stress_of(self.starts[k], velocity)
                self.stress = [s + r.ratio[0] * t for s, t in zip(self.stress, found, strict=True)]
            pulls = hands.products(self.starts[k], self.pull[k])
            for product, pull in zip(hands.products(u_in, u_out), pulls, strict=True):
                self.forms = self.forms + product + carries(-pull, self.train_teeth[k])
            self.impelled[k] = p_other

    def carry(self) -> None:
        """(3) The carry (the former `carrier_act`, `divisions`, `writes` and `rest`): the regulator's one carry with the drive sourced by the driven trains' strides, 4 stretch_now (forms (the file's trace weight) rim full_rate^2 - trace rate^2) rate on its time gear and, times rate^2 on its nine axis gears by the position of their reading, the traceless stress, the hands' count flow and the shears (Y-S1, Y-S3; the regulator's act clock.act, the former `carried` by this name); every driven gear's one carry at the mean teeth of the regulator's two notches at its end, its fine tooth kept in [0, W) there, backward the turned-over clocks set to their kept pre-state; the hands' gears at the start and before the turnover kept for the striking (the latter the state the turnover replaces at the turned-over clocks, the notches now elsewhere, CL-S2; the former `stepped` kept by name); the trains set; forward the advances among the carries after them (`advances`; backward they came off first); then every gear at a stopped clock restored to its held gear, its notches, its fine teeth and its teeth by the clock's one restore (BH-S1, the former `rest`), so no act but the turnover changes any integer of a stopped clock's state forward or backward; backward a clock both stopped and turned over is restored to the pre-state the reverse returned (FR-S1)."""
        clk, regulator = self.clock, self.regulator
        k = self.where[id(regulator)]
        p02, (trace, traceless) = self.rate * self.rate, tensor_parts(self.stress[:AXES])
        numerators = [
            held_numerator(
                clk.trace, self.stretch_now, self.forms, trace, self.rate, clk.rim, clk.full_rate
            )
        ]
        numerators += [part * p02 for part in (*traceless, *self.stress[AXES:])]
        gearing = readings.gearing_of(clk, regulator, self.load, self.factors)
        self.out[k] = clk.act(
            self.trains[k], gearing, None, numerators, self.going, None, *self.ends(regulator)
        )[-1]
        w_div = readings.mean_teeth(self.clock, self.out[k][0])
        for r in self.driven:
            k = self.where[id(r)]
            new = []
            for a, p, gear in zip(self.starts[k], self.impelled[k], self.trains[k], strict=True):
                v, fine = carry(p, w_div, mid(w_div))
                now, before = (a + self.going * v, a)[:: self.going]
                new.append(Gear(now, before, fine, w_div, gear.dfine, gear.dteeth))
            if self.going == -1 and self.kept is not None:
                clk.restore(new, self.kept[k], self.top)
            self.out[k] = new
            if r in self.hands:
                start = self.trains[k] if self.going == 1 else new
                after = new if self.going == 1 else self.held[k]
                self.hand_starts.append(list(start))
                self.before_turnover.append([gear.copy() for gear in after])
        clk.before_turnover = self.before_turnover
        clk.set_trains(self.out)
        if self.going == 1:
            self.advances()
        if self.going == -1 and self.kept is not None:
            clk.restore(
                clk.all_gears(), [gear for train in self.kept for gear in train], self.stopped & self.top
            )
        clk.restore(
            clk.all_gears(), [gear for train in self.held for gear in train], self.stopped & ~self.top
        )

    def advances(self) -> None:
        """The advances among the carries (the former `writes` and `unwrite`), each one carry at the gear's drive teeth T with the carry kept in its drive fine tooth (clock.drive), on the trains as the clock holds them at the end: the unsprung gear's W-S1 advance, the release over the regulator's mean teeth at the end, its carries rounded odd (EM-S1's odd rounding, rates.rounded: the advance exactly odd under the sense's flip, the former floor kept by name), its size counted forward (`advanced_on`), its tally per advanced clock driven on the regulator's flow gears by the clock's drive act (unwind.recoil, LT-S1: the release's advance taken into the clause), its tallies kept in the tick's rewind note for the rewind and undone at -1 by the same act, the last first, after the turnover's undoing and before the drives come off, at no still clock (turned over or stopped), where the turnover or the restore wiped the forward's tally with the advance; the offset train's lead at the start on its three odd gears, its time gear's numerator None (its sweep landed at the impulse, PL-S1); forward after every gear's carry, backward the first act to come off."""
        clock = self.clock
        gear, time_gear = clock.unsprung().gears[0], clock.train(REGULATOR).gears[0]
        notches = gear.now
        teeth = readings.mean_teeth(self.clock, time_gear)
        clock.drive(gear, rates.rounded(self.release, teeth), self.going)
        if self.going == 1:
            advanced_on(clock, gear, notches)
        if self.going == -1:
            for at, push, rate in reversed(self.tallies):
                if not self.still[at]:
                    recoil(clock, at, push, rate, -1)
        else:
            advanced, ratio = gear.now - notches, clock.unsprung().ratio
            assert ratio is not None
            for at in (at for at in np.ndindex(clock.size) if int(advanced[at])):
                push = push_of(clock, [gear], at, (int(advanced[at]), 0), ratio[0])
                self.tallies.append((at, push, int(clock.start_rate[at])))
                recoil(clock, at, push, int(clock.start_rate[at]), 1)
        for gear, n in zip(clock.train(OFFSET).gears, [None, *self.lead], strict=True):
            if n is not None:
                clock.drive(gear, n, self.going)

    def turnover(self) -> None:
        """(4) The turnover at the top and the bottom (clock.turnover; the stopped clock released by its own trigger, FR-S1): the weak maximum of the regulator's three notches, the held before, the held now and the now after the advances, or an outer one below the bottom; the turned-over clock ends the tick at its held pre-state, exchanged and complemented."""
        self.top = self.clock.turnover(self.held)

    def strike(self) -> None:
        """(5) The striking (striking.strike) after the turnover, the rewind note pushed for the rewind: the turned-over clocks, the counters as they stood before the strike (the turnover changes none), the log's length and the stopped mask."""
        clock = self.clock
        log_from = len(clock.log)
        note = rewind_note(clock, self.top, log_from, self.stopped, self.tallies)
        clock.strike(self.hand_starts, self.held)
        clock.stack.append(note)


def offset_curl(odd: list[Any]) -> list[Any]:
    """The offset's one-mesh curl at every clock, Phi_a = d_b A_c - d_c A_b from its odd gears, d_b the centred difference through the axis b's two spokes (the struck hands.curl, 6501cd679)."""
    found = []
    for a in range(AXES):
        b, c = transverse(a)
        found.append(gradient(odd[c], b) - gradient(odd[b], c))
    return found


def run(clock: Clock, going: int) -> None:
    """One tick in the going, five acts: the readings, the impulse, the carry, the turnover at the top, the striking; backward the striking and the turnover are undone at the Tick's making, the advances come off before the impulse (the reverse order: the last advanced, the first undone), the impulse and the carry are the same acts at -1 and the tick is counted down."""
    tick = Tick(clock, going)
    acts = {
        1: (tick.impulse, tick.carry, tick.turnover, tick.strike),
        -1: (tick.advances, tick.impulse, tick.carry),
    }
    for act in (tick.readings, *acts[going]):
        act()
