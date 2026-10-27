"""The generic clock (the owner's word of 2026-10-25: the clock knows nothing, there is no if): its state is the trains the calibre names on the great clock the piece names, 98 integers at every clock with the toy calibre's seven trains; its readings at a tick's start (the load, the rates, the mesh factors, the pawls, the meshes' counts and offsets, the conserved form's wind); its acts on a train, each one act on every train alike forward and backward (Rule3's turn with the pulls turned as the train's size turns them, the drive by one carry, the reverse at the turned-over clocks); the tick's program is tick.run and the striking is striking.strike, each a function of the clock."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe import hands, readings, striking, tick
from event_universe.assembly import setting
from event_universe.core import acts, rates, rule3
from event_universe.core.rates import sine_rim
from event_universe.core.rule3 import half, mesh_unit_of, teeth_of, winding_of
from event_universe.core.spokes import AXES, across
from event_universe.features import standard
from event_universe.meshes import Mesh, through_mesh
from event_universe.run import bits_of
from event_universe.trains import (
    REGULATOR,
    Gear,
    Train,
    hands_of,
    train_of,
    trains_of,
    zeros,
)

COUNTS = {  # the run's counts, every one 0 at the start
    "births": 0,
    "taken": 0,
    "booked": 0,
    "body_clicks": 0,
    "laid_back": 0,
    "refused_stop": 0,
    "refused_origin": 0,
    "refused_lay": 0,
    "refused_orientation": 0,
    "refused_twist": 0,
    "refused_sense": 0,
    "turns": 0,
    "met": 0,
    "laid": 0,
    "laid_nodes": 0,
}


class Clock:
    """The clock from the calibre's integers and trains and the piece's size and setting, nothing else (the owner's rule: no number in the code)."""

    def __init__(self, calibre: dict[str, Any], piece: dict[str, Any]) -> None:
        ints = calibre["integers"]
        self.rim, self.full_rate = int(ints["den"]), int(ints["node_clock"])
        self.key, self.G = int(ints["quantum_action"]), mesh_unit_of(self.full_rate)
        self.trace = int(ints["trace"])
        self.standard_length = standard.carried(self.full_rate * self.rim, self.full_rate)
        size = tuple(int(x) for x in piece["shape"])
        if len(size) != AXES or len(set(size)) != 1:
            raise ValueError("the board is a cube: the shape is [c, c, c]")
        self.cube, self.size = size[0], size
        self.teeth = teeth_of(self.rim, self.full_rate, self.G)
        rates.certified(self.full_rate)
        self.trains_, self.by_index = trains_of(calibre, size, self.teeth)
        pinions, rim = [r.ratio[0] for r in self.hands() if r.ratio], self.rim
        if any(p * p + sine_rim(p, rim) * sine_rim(p, rim) != rim * rim for p in pinions):
            raise ValueError("a gapped pair off den's circle: num^2 + s^2 is not den^2 (MS-S2)")
        self.windings = [
            winding_of(sine_rim(p, rim) + rim * rule3.carries(p, rim), self.key) for p in pinions
        ]
        self.sprung = [r for r in self.hands() if r is not self.unsprung()]
        self.winding_unsprung = self.windings[self.hands().index(self.unsprung())]
        self.start_state()
        self.driven_teeth()
        setting.set_piece(self, piece.get("seed", []))

    def start_state(self) -> None:
        """The clock's state before the setting: the hands' wound ticks, crossings and beats, the dial, the strikes, the slack (EX-S1, set at 0), the ticks, the log, the turnovers, the rewind notes' stack, the run's counts; the regulator's time gear at the full rate, the drift the largest integer whose square is at most the key, the advance's two notches (A, B) with A B = key div 2 (MS-S1), the standard's first pair at the standard length derived from the rim, X = Gamma rim (clock.standard_length, carried above the shortest hand derived from the full rate, standard.carried; DAVID-AMPLITUDES.md section 4, the former length declared from outside by the owner's words of 2026-10-27, 04:0x and 04:4x UTC, the declaration struck by his rule of 11:3x UTC)."""
        size, nr = self.size, len(self.hands())
        self.wound = [zeros(size) for _ in range(nr)]
        self.crossed = [zeros(size) for _ in range(nr)]
        self.beats = [zeros(size) for _ in range(nr)]
        self.dial, self.strikes, self.ticks, self.slack = zeros(size), zeros(size), 0, zeros(size)
        self.log: list[dict[str, Any]] = []
        self.turnovers: list[tuple[int, int]] = []
        self.stack: list[dict[str, Any]] = []
        self.turned_over = np.zeros(size, dtype=bool)
        self.counts: dict[str, int] = dict(COUNTS)
        self.max_transient, self.count_max, self.last_push = 0, 0, [0, 0, 0]
        self.last_recoil: dict[str, Any] = {}
        self.start_factors: tuple[Any, ...] = ()
        self.start_pawls: list[Any] = []
        self.start_offsets: list[tuple[Any, Any]] = []
        self.start_odd: list[Any] = []
        self.before_turnover: list[list[Gear]] = []
        self.start_gears: list[list[Gear]] = []
        self.pitches: dict[tuple[int, int, tuple[int, ...]], int] = {}
        self.vernier_read: dict[tuple[tuple[int, ...], int], tuple[int, int] | None] = {}
        self.twin_ends: dict[tuple[int, tuple[int, ...], tuple[int, ...]], tuple[int, int]] = {}
        self.rest_rates: dict[tuple[int, int], int] = {}

        for gear in self.train(REGULATOR).gears[:1]:
            gear.now[:], gear.before[:] = self.full_rate, self.full_rate
        self.drift = rule3.largest_below(self.key)
        self.A, self.B = rule3.balanced_notches(half(self.key))
        first_pair = standard.first_pair(self.standard_length, self.full_rate)
        self.circuit_gears, self.circuit = [first_pair], [(int(first_pair[0][0]), int(first_pair[1][0]))]
        self.circuit_half: int | None = None
        self.start_load, self.start_stretch = readings.load(self), self.train(REGULATOR).gears[0].now
        self.start_rate = readings.rates_of(self, self.start_load)[0]

    def driven_teeth(self) -> None:
        """The driven gears' fine teeth at the start: a driven gear's fine tooth lives at the mean teeth (teeth div 2)(stretch_before + stretch_now) of the regulator's two notches at its clock, half of it at the setting."""
        teeth = readings.mean_teeth(self, self.train(REGULATOR).gears[0])
        for r in self.trains_:
            if r.teeth is None and r.size != REGULATOR:
                for gear in r.gears:
                    gear.teeth, gear.fine = teeth, acts.mid(teeth)

    def clock_of(self, xyz: Any) -> tuple[int, ...]:
        """A clock named by the piece: three integers on the great clock; a clock off the great clock is refused by name."""
        at = tuple(int(x) for x in xyz)
        if len(at) != AXES or any(not 0 <= x < self.cube for x in at):
            raise ValueError(f"a Node off the board: {at!r}")
        return at

    def train(self, size: int) -> Train:
        """The one train of the size with a ratio, chosen by the numbers alone (trains.train_of)."""
        return train_of(self.trains_, size)

    def unsprung(self) -> Train:
        """The hand with no spring of its own, the light: the hand whose gearing's spring D = 2 SPOKES (rim - pinion) rate^2 G^2 is 0 at every rate, its ratio's pinion equal to its rim (a property of the train's own numbers, no role; the assembly admits exactly one): the train the sweep's change is advanced on and whose windings the striking unwinds."""
        return next(r for r in self.hands() if r.ratio is not None and r.ratio[0] == r.ratio[1])

    def hands(self) -> list[Train]:
        """The hand trains in the acts' order, the hands (trains.hands_of)."""
        return hands_of(self.trains_)

    def offset_pull(self, pulls: list[Any], spoke: int, meshes: list[Mesh] | None) -> list[Any]:
        """The pulls of a train's gears at one spoke, read by the clock's pawl (the train's reflection where the pawl is -1, hands.seen) and turned hand by hand by the mesh (meshes.through_mesh); a train of one gear is turned by the identity; `meshes` None is the identity for every size."""
        if meshes is None or len(pulls) == 1:
            return pulls
        at = meshes[spoke]
        reflected = hands.seen(pulls, at.pawl)
        return through_mesh(reflected, at, self.standard_length, self.full_rate)

    def pulls(self, at: list[Any], r: rule3.Gearing, meshes: list[Mesh] | None) -> list[Any]:
        """The meshes' part of Rule3's total for a train's gears at every clock, SUM_j grip_j m_j, the pulls at each spoke turned as the train's size turns them."""
        totals: list[Any] = [0] * len(at)
        for spoke, grip in enumerate(r.grips):
            found = self.offset_pull([across(a, spoke) for a in at], spoke, meshes)
            totals = [t + grip * m for t, m in zip(totals, found, strict=True)]
        return totals

    def turn(
        self,
        gears: list[Gear],
        r: rule3.Gearing,
        meshes: list[Mesh] | None,
        going: int,
        flow: list[Any] | None,
        starts: list[Any] | None,
    ) -> list[Gear]:
        """Rule3's step of one train at every clock, the one function of a gear forward and backward (RW-S1: the gear's two slots one pair read reversed by the going, (a, y) = (now, before) forward and (before, now) backward, the total hold a - teeth y + SUM_j grip_j m_j, the new notch the total's carries on the slot the going names): for each gear the total hold now - teeth before + SUM_j grip_j m_j (+ the gear's flow where the train carries its drive inside the carry), one carry at the teeth per gear. Backward the same act on the before slots with the carry's going -1."""
        notches = [(gear.now, gear.before)[::going] for gear in gears]
        at = starts or [a for a, _y in notches]
        flows: list[Any] = flow or [0] * len(gears)
        totals = [
            r.hold * a - r.teeth * y + f + m
            for (_a, y), a, f, m in zip(notches, at, flows, self.pulls(at, r, meshes), strict=True)
        ]
        found = []
        for gear, a, t in zip(gears, at, totals, strict=True):
            self.max_transient = max(self.max_transient, bits_of(t))
            notch, fine = acts.carry(t, r.teeth, gear.fine, going)
            now, before = (notch, a)[::going]
            found.append(Gear(now, before, fine, gear.teeth, gear.dfine, gear.dteeth))
        return found

    def drive(self, gear: Gear, numerator: Any, going: int) -> None:
        """The one drive act on a gear: the numerator's carry at the gear's drive teeth, the carries added to the notch now (forward) or turned back (backward), the drive fine tooth carried in the gear."""
        q, gear.dfine = acts.carry(numerator, gear.dteeth, gear.dfine, going)
        gear.now = acts.advance(gear.now, q, going)

    def act(
        self,
        gears: list[Gear],
        r: rule3.Gearing,
        meshes: list[Mesh] | None,
        numerators: list[Any],
        going: int,
        flow: list[Any] | None = None,
        top: Any = None,
        kept: list[Gear] | None = None,
    ) -> tuple[list[Gear], list[Gear]]:
        """The clock's act on one train in the going, one path (RW-S1): Rule3's turn and the gears' drives run in the going's order, the turn first forward and the drive first backward, each at the going (the former two branches kept by name). Returns the train at the start and the train as the act leaves it (the stepped notches before the drive, read by no engine code, struck 2026-10-26: the lean toy spells its own act for its former interval); backward at the turned-over clocks `top` the train is set to `kept`, the pre-state the reverse returned."""
        starts = None if kept is None else [np.where(top, gear.now, gear.before) for gear in gears]

        def turn(found: list[Gear]) -> list[Gear]:
            return self.turn(found, r, meshes, going, flow, starts)

        def drive(found: list[Gear]) -> list[Gear]:
            for gear, n in zip(found, numerators, strict=True):
                if n is not None:
                    self.drive(gear, n, going)
            return found

        first, second = (turn, drive)[::going]
        found = second(first(gears))
        if kept is not None:
            self.restore(found, kept, top)
        return (gears if going == 1 else found), found

    def restore(self, gears: list[Gear], kept: list[Gear], top: Any) -> None:
        """Backward at the turned-over clocks `top`: the train set to `kept`, the pre-state the reverse returned (the inverse at a turned-over clock is no act)."""
        for gear, k in zip(gears, kept, strict=True):
            gear.now, gear.before = np.where(top, k.now, gear.now), np.where(top, k.before, gear.before)
            gear.fine = np.where(top, k.fine, gear.fine)
            if np.ndim(k.teeth):
                gear.teeth = np.where(top, k.teeth, gear.teeth)
            if gear.dfine is not None:
                gear.dfine = np.where(top, k.dfine, gear.dfine)

    def trains(self) -> list[list[Gear]]:
        """The clock's trains' gears in the acts' order."""
        return [r.gears for r in self.trains_]

    def set_trains(self, trains: list[list[Gear]]) -> None:
        """Every train's gears replaced, in the acts' order."""
        for r, gears in zip(self.trains_, trains, strict=True):
            r.gears = list(gears)

    def all_gears(self) -> list[Gear]:
        """Every gear of every train, in the acts' order."""
        return [gear for train in self.trains() for gear in train]

    def reverse(self, top: Any, held: list[list[Gear]]) -> None:
        """The turnover's act at the clocks `top`: every train set to its held train exchanged and reflected by the train's K (hands.signs: a hand's twelve gear negated, the identity on another train), every fine tooth flipped once per reversal of its gear by the one rule: once for time's exchange, twice where the reflection negates the gear (its own entry of K), so a twelve gear's fine tooth is left; the drive fine teeth and the pawl once; an involution with the state it leaves; the trains set at the top by the clock's one restore."""
        for r, train, held_train in zip(self.trains_, self.trains(), held, strict=True):
            nows, befores, fines = acts.reverse(
                [h.now for h in held_train],
                [h.before for h in held_train],
                [h.fine for h in held_train],
                [h.teeth for h in held_train],
                hands.signs(r.size),
            )
            drives = [None if h.dfine is None else acts.flip(h.dfine, h.dteeth, 1) for h in held_train]
            reversed_gears = [
                Gear(n, b, fine, h.teeth, d, h.dteeth)
                for n, b, fine, h, d in zip(nows, befores, fines, held_train, drives, strict=True)
            ]
            self.restore(train, reversed_gears, top)

    def turnover(self, held: list[list[Gear]], going: int = 1, top: Any = None) -> Any:
        """The turnover at the top, in the going (RW-S1; backward the reverse of the turned-over clocks `top` from the rewind note, the former Interval's own exchange kept by name): the weak maximum X0 <= X1 >= X2 with one strict (the held before, the held now, the now after the drives), or the bottom (X0 or X2 below X_f), at a stopped clock by this trigger alone on its restored gear (FR-S1, the owner's words of 2026-10-26, 03:41 UTC, approved, and 07:3x UTC, entered as the fix of a forbidden state: no clock stopped for ever; BH-S1's mask on the trigger struck and kept by name); the turned-over clock ends the tick at the state it started from, exchanged and complemented."""
        if going == -1:
            if top.any():
                self.reverse(top, held)
            return top
        k = self.trains_.index(self.train(REGULATOR))
        x0, x1, x2 = held[k][0].before, held[k][0].now, self.train(REGULATOR).gears[0].now
        xf = readings.bottom(self)
        top = (x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1)) | (x0 < xf) | (x2 < xf)
        self.turned_over = top
        if top.any():
            self.counts["turns"] += int(top.sum())
            self.turnovers.append((self.ticks, int(top.sum())))
            self.reverse(top, held)
        return top

    def read_gears(
        self, held: list[list[Gear]], c: Any, factors: tuple[Any, ...]
    ) -> list[tuple[Gear, rule3.Gearing]]:
        """The gears the one-mesh read uses, with their gearings: every gear of every train at the tick's start, alike."""
        gearings = [readings.gearing_of(self, r, c, factors) for r in self.trains_]
        return [(gear, gearing) for gearing, gears in zip(gearings, held, strict=True) for gear in gears]

    def strike(
        self,
        hand_starts: list[list[Gear]],
        held: list[list[Gear]],
        going: int = 1,
        rewind_note: dict[str, Any] | None = None,
    ) -> None:
        """The striking (striking.strike), the clock's fourth act, in the going: backward the striking undone from the log's rewind note."""
        striking.strike(self, hand_starts, held, going, rewind_note)

    def tick(self, going: int = 1) -> None:
        """One tick of the clock's program forward, or back at -1 (tick.run; the former step_back and run kept by name)."""
        tick.run(self, going)
