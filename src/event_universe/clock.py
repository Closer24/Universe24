"""The generic Node (the owner's word of 2026-10-25: the Node knows nothing, there is no if): its state is the rows the universe file names on the board the world file names, 98 integers at every Node with the toy universe's seven rows; its readings at an interval's start (the content, the paces, the Link factors, the frames, the Links' counts and phases, the conserved form's share); its acts on a row, each one act on every row alike in either direction (Rule3's rotate with the arrivals turned as the row's shape turns them, the write by one carried division, the exchange at the turned Nodes); the interval's program is interval.run and the close is close.click, each a function of the Node."""

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
    """The Node from the universe's integers and rows and the world's shape and seed, nothing else (the owner's rule: no number in the code)."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any]) -> None:
        ints = universe["integers"]
        self.rim, self.full_rate = int(ints["den"]), int(ints["node_clock"])
        self.key, self.G = int(ints["quantum_action"]), mesh_unit_of(self.full_rate)
        self.trace = int(ints["trace"])
        self.standard_length = standard.carried(int(ints["amplitude"]), self.full_rate)
        shape = tuple(int(x) for x in world["shape"])
        if len(shape) != AXES or len(set(shape)) != 1:
            raise ValueError("the board is a cube: the shape is [c, c, c]")
        self.cube, self.size = shape[0], shape
        self.teeth = teeth_of(self.rim, self.full_rate, self.G)
        rates.certified(self.full_rate)
        self.trains_, self.by_index = trains_of(universe, shape, self.teeth)
        pinions, den = [r.ratio[0] for r in self.hands() if r.ratio], self.rim
        if any(num * num + sine_rim(num, den) * sine_rim(num, den) != den * den for num in pinions):
            raise ValueError("a gapped pair off den's circle: num^2 + s^2 is not den^2 (MS-S2)")
        self.windings = [
            winding_of(sine_rim(num, den) + den * rule3.carries(num, den), self.key) for num in pinions
        ]
        self.sprung = [r for r in self.hands() if r is not self.unsprung()]
        self.winding_unsprung = self.windings[self.hands().index(self.unsprung())]
        self.start_state()
        self.driven_teeth()
        setting.set_piece(self, world.get("seed", []))

    def start_state(self) -> None:
        """The Node's state before the seed: the records' standing, crossings and beats, the proper count, the closes, the take's remainder (EX-S1, born at 0), the interval, the log, the turns, the frames' stack, the run's counts; the carrier's time line at Gamma, the drift the largest integer whose square is at most T, the lay's two levels (A, B) with A B = T div 2 (MS-S1), the phase pair's seed at the amplitude the universe file declares (node.X, read at the load and carried above the floor derived from Gamma, phase.carried; the owner's words of 2026-10-27, 04:0x and 04:4x UTC: the amplitude separated from the former width and declared from outside)."""
        shape, nr = self.size, len(self.hands())
        self.wound = [zeros(shape) for _ in range(nr)]
        self.crossed = [zeros(shape) for _ in range(nr)]
        self.beats = [zeros(shape) for _ in range(nr)]
        self.dial, self.strikes, self.ticks = zeros(shape), zeros(shape), 0
        self.slack = zeros(shape)
        self.log: list[dict[str, Any]] = []
        self.turnovers: list[tuple[int, int]] = []
        self.stack: list[dict[str, Any]] = []
        self.turned_over = np.zeros(shape, dtype=bool)
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
        self.rest_rates: dict[tuple[int, int], int] = {}

        for line in self.train(REGULATOR).gears[:1]:
            line.now[:], line.before[:] = self.full_rate, self.full_rate
        self.drift = rule3.largest_below(self.key)
        self.A, self.B = rule3.balanced_notches(half(self.key))
        seed_pair = standard.first_pair(self.standard_length, self.full_rate)
        self.circuit_gears, self.circuit = [seed_pair], [(int(seed_pair[0][0]), int(seed_pair[1][0]))]
        self.circuit_half: int | None = None
        self.start_load, self.start_stretch = readings.load(self), self.train(REGULATOR).gears[0].now
        self.start_rate = readings.rates_of(self, self.start_load)[0]

    def driven_teeth(self) -> None:
        """The riding lines' remainders at the start: a riding line's remainder lives at the mean wall (w div 2)(X_before + X_now) of the carrier's two levels at its Node, half of it at the seed."""
        wall = readings.mean_teeth(self, self.train(REGULATOR).gears[0])
        for r in self.trains_:
            if r.teeth is None and r.size != REGULATOR:
                for line in r.gears:
                    line.teeth, line.fine = wall, acts.mid(wall)

    def clock_of(self, xyz: Any) -> tuple[int, ...]:
        """A Node named by the world file: three integers on the board; a Node off the board is refused by name."""
        at = tuple(int(x) for x in xyz)
        if len(at) != AXES or any(not 0 <= x < self.cube for x in at):
            raise ValueError(f"a Node off the board: {at!r}")
        return at

    def train(self, shape: int) -> Train:
        """The one row of the shape with a pair, chosen by the numbers alone (rows.row_of)."""
        return train_of(self.trains_, shape)

    def unsprung(self) -> Train:
        """The plane with no pendulum of its own, the light: the record whose rule's mass D = 2 PORTS (den - num) p_0^2 G^2 is 0 at every clock, its pair's num equal to its den (a property of the row's own numbers, no role; the loader admits exactly one): the row the Wronskian's change is laid on and whose quanta the close takes."""
        return next(r for r in self.hands() if r.ratio is not None and r.ratio[0] == r.ratio[1])

    def hands(self) -> list[Train]:
        """The record rows in the acts' order, the planes (rows.records_of)."""
        return hands_of(self.trains_)

    def offset_pull(self, arrivals: list[Any], port: int, turn: list[Mesh] | None) -> list[Any]:
        """The arrivals of a row's lines at one Port, read in the Node's frame (the row's conjugation where the frame sign is -1, gram.conjugated) and turned plane by plane by the Link's record (links.turned); a row of one line is turned by the identity; `turn` None is the identity for every shape."""
        if turn is None or len(arrivals) == 1:
            return arrivals
        at = turn[port]
        reflected = hands.reflected(len(arrivals), arrivals, at.pawl)
        return through_mesh(reflected, at, self.standard_length, self.full_rate)

    def pulls(self, at: list[Any], r: rule3.Gearing, turn: list[Mesh] | None) -> list[Any]:
        """The Links' part of Rule3's total for a row's lines at every Node, SUM_j R_j m_j, the arrivals at each Port turned as the row's shape turns them."""
        totals: list[Any] = [0] * len(at)
        for port, reach in enumerate(r.grips):
            found = self.offset_pull([across(a, port) for a in at], port, turn)
            totals = [t + reach * m for t, m in zip(totals, found, strict=True)]
        return totals

    def turn(
        self,
        lines: list[Gear],
        r: rule3.Gearing,
        turn: list[Mesh] | None,
        direction: int,
        flux: list[Any] | None,
        starts: list[Any] | None,
    ) -> list[Gear]:
        """Rule3's step of one row at every Node, the one function of a line in either direction (RW-S1: the line's two slots one pair read reversed by the direction, (a, y) = (now, before) forward and (before, now) backward, the total S a - w y + SUM_j R_j m_j, the new level the quotient on the slot the direction names): for each line the total S now - w before + SUM_j R_j m_j (+ the line's flux where the row carries its write inside the division), one carried division at the wall w per line. Backward the same act on the before slots with the division's direction -1."""
        pairs = [(line.now, line.before)[::direction] for line in lines]
        at = starts or [a for a, _y in pairs]
        fluxes: list[Any] = flux or [0] * len(lines)
        totals = [
            r.hold * a - r.teeth * y + f + m
            for (_a, y), a, f, m in zip(pairs, at, fluxes, self.pulls(at, r, turn), strict=True)
        ]
        found = []
        for line, a, t in zip(lines, at, totals, strict=True):
            self.max_transient = max(self.max_transient, bits_of(t))
            quotient, rem = acts.carry(t, r.teeth, line.fine, direction)
            now, before = (quotient, a)[::direction]
            found.append(Gear(now, before, rem, line.teeth, line.dfine, line.dteeth))
        return found

    def drive(self, line: Gear, numerator: Any, direction: int) -> None:
        """The one write act on a line: the numerator's carried division at the line's write wall, the quotient added to the level now (forward) or taken back (backward), the remainder carried in the line."""
        q, line.dfine = acts.carry(numerator, line.dteeth, line.dfine, direction)
        line.now = acts.advance(line.now, q, direction)

    def act(
        self,
        lines: list[Gear],
        r: rule3.Gearing,
        turn: list[Mesh] | None,
        numerators: list[Any],
        direction: int,
        flux: list[Any] | None = None,
        top: Any = None,
        kept: list[Gear] | None = None,
    ) -> tuple[list[Gear], list[Gear]]:
        """The Node's act on one row in the direction, one path (RW-S1): Rule3's rotate and the lines' writes taken in the direction's order, the rotate first forward and the write first backward, each at the direction (the former two branches kept by name). Returns the row at the start and the row as the act leaves it (the stepped levels before the write, read by no engine code, struck 2026-10-26: the lean toy spells its own act for its former interval); backward at the turned Nodes `top` the row is set to `kept`, the pre-state the exchange returned."""
        starts = None if kept is None else [np.where(top, line.now, line.before) for line in lines]

        def rotate(found: list[Gear]) -> list[Gear]:
            return self.turn(found, r, turn, direction, flux, starts)

        def write(found: list[Gear]) -> list[Gear]:
            for line, n in zip(found, numerators, strict=True):
                if n is not None:
                    self.drive(line, n, direction)
            return found

        first, second = (rotate, write)[::direction]
        found = second(first(lines))
        if kept is not None:
            self.restore(found, kept, top)
        return (lines if direction == 1 else found), found

    def restore(self, lines: list[Gear], kept: list[Gear], top: Any) -> None:
        """Backward at the turned Nodes `top`: the row set to `kept`, the pre-state the exchange returned (the inverse at a turned Node is no act)."""
        for line, k in zip(lines, kept, strict=True):
            line.now, line.before = np.where(top, k.now, line.now), np.where(top, k.before, line.before)
            line.fine = np.where(top, k.fine, line.fine)
            if np.ndim(k.teeth):
                line.teeth = np.where(top, k.teeth, line.teeth)
            if line.dfine is not None:
                line.dfine = np.where(top, k.dfine, line.dfine)

    def trains(self) -> list[list[Gear]]:
        """The Node's rows' lines in the acts' order."""
        return [r.gears for r in self.trains_]

    def set_trains(self, rows: list[list[Gear]]) -> None:
        """Every row's lines replaced, in the acts' order."""
        for r, lines in zip(self.trains_, rows, strict=True):
            r.gears = list(lines)

    def all_gears(self) -> list[Gear]:
        """Every line of every row, in the acts' order."""
        return [line for row in self.trains() for line in row]

    def reverse(self, top: Any, held: list[list[Gear]]) -> None:
        """The swap's act at the Nodes `top`: every row set to its held row exchanged and conjugated by the row's K (gram.conjugation: a plane's im line negated, the identity on another row), every remainder mirrored once per reversal of its line by the one rule: once for time's exchange, twice where the conjugation negates the line (its own entry of K), so an im line's rotation remainder is left; the write remainders and the frame bit once; an involution with the state it leaves; the rows set at the top by the Node's one restore."""
        for r, row, hrow in zip(self.trains_, self.trains(), held, strict=True):
            nows, befores, rems = acts.reverse(
                [h.now for h in hrow],
                [h.before for h in hrow],
                [h.fine for h in hrow],
                [h.teeth for h in hrow],
                hands.reflection(r.size),
            )
            drives = [None if h.dfine is None else acts.flip(h.dfine, h.dteeth, 1) for h in hrow]
            exchanged = [
                Gear(n, b, rem, h.teeth, d, h.dteeth)
                for n, b, rem, h, d in zip(nows, befores, rems, hrow, drives, strict=True)
            ]
            self.restore(row, exchanged, top)

    def turnover(self, held: list[list[Gear]], direction: int = 1, top: Any = None) -> Any:
        """The swap at the top, in the direction (RW-S1; backward the exchange of the turned Nodes `top` from the frame, the former Interval's own exchange kept by name): the weak maximum X0 <= X1 >= X2 with one strict (the held before, the held now, the now after the writes), or the floor (X0 or X2 below X_f), at a frozen Node by this trigger alone on its restored line (FR-S1, the owner's words of 2026-10-26, 03:41 UTC, approved, and 07:3x UTC, entered as the fix of a forbidden state: no Node frozen for ever; BH-S1's mask on the trigger struck and kept by name); the turned Node ends the interval at the state it started from, exchanged and complemented."""
        if direction == -1:
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
        """The lines the one-Link read takes with their rules: every line of every row at the interval's start, alike."""
        rules = [readings.gearing_of(self, r, c, factors) for r in self.trains_]
        return [(line, rule) for rule, lines in zip(rules, held, strict=True) for line in lines]

    def strike(
        self,
        plane_starts: list[list[Gear]],
        held: list[list[Gear]],
        direction: int = 1,
        frame: dict[str, Any] | None = None,
    ) -> None:
        """The close (close.click), the Node's fourth act, in the direction: backward the close undone from the log's frame."""
        striking.strike(self, plane_starts, held, direction, frame)

    def tick(self, direction: int = 1) -> None:
        """One interval of the Node's program forward, or back at -1 (interval.run; the former step_back and run kept by name)."""
        tick.run(self, direction)
