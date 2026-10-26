"""The generic Node (the owner's word of 2026-10-25: the Node knows nothing, there is no if): its state is the rows the universe file names on the board the world file names, 98 integers at every Node with the toy universe's seven rows, 116 with a shape-8 row beside them; its readings at an interval's start (the content, the paces, the Link factors, the frames, the Links' counts and phases, the conserved form's share); its acts on a row, each one act on every row alike in either direction (Rule3's rotate with the arrivals turned as the row's shape turns them, the write by one carried division, the exchange at the turned Nodes); the interval's program is interval.run and the close is close.click, each a function of the Node."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe import close, gram, interval, readings, seed
from event_universe.core import acts, paces, rule3
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import half, link_unit_of, unit_of, wall_of
from event_universe.features import phase
from event_universe.links import Link, turned
from event_universe.record import bits_of
from event_universe.rows import (
    CARRIER,
    HALF_WIDTH,
    PLANE,
    POTENTIAL,
    Line,
    Row,
    records_of,
    row_of,
    rows_of,
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


class Node:
    """The Node from the universe's integers and rows and the world's shape and seed, nothing else (the owner's rule: no number in the code)."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any]) -> None:
        ints = universe["integers"]
        self.den, self.gamma = int(ints["den"]), int(ints["node_clock"])
        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)
        self.trace = int(ints["trace"])
        shape = tuple(int(x) for x in world["shape"])
        if len(shape) != AXES or len(set(shape)) != 1:
            raise ValueError("the board is a cube: the shape is [c, c, c]")
        self.cube, self.shape = shape[0], shape
        self.w = wall_of(self.den, self.gamma, self.G)
        paces.certified(self.gamma)
        self.rows_, self.by_index = rows_of(universe, shape, self.w)
        for r in self.records():
            num, den = (r.pair[0] if r.pair else 0), self.den
            if r.pair and num * num + sine_den(num, den) * sine_den(num, den) != den * den:
                raise ValueError("a gapped pair off den's circle: num^2 + s^2 is not den^2 (MS-S2)")
        self.units = [
            unit_of(sine_den(num, self.den) + self.den * rule3.quotient(num, self.den), self.T)
            for num in (r.pair[0] for r in self.records() if r.pair)
        ]
        self.gapped = [r for r in self.records() if r is not self.emitter()]
        self.unit_emitter = self.units[self.records().index(self.emitter())]
        self.start_state()
        self.ride_walls()
        seed.lay_world(self, world.get("seed", []))

    def start_state(self) -> None:
        """The Node's state before the seed: the records' standing, crossings and beats, the proper count, the closes, the take's remainder (EX-S1, born at 0), the interval, the log, the turns, the frames' stack, the run's counts; the carrier's time line at Gamma, the drift the largest integer whose square is at most T, the lay's two levels (A, B) with A B = T div 2 (MS-S1), the phase pair's amplitude from half the width less one and the orbit's seed."""
        shape, nr = self.shape, len(self.records())
        self.standing = [zeros(shape) for _ in range(nr)]
        self.crossed = [zeros(shape) for _ in range(nr)]
        self.beats = [zeros(shape) for _ in range(nr)]
        self.proper, self.closes, self.interval = zeros(shape), zeros(shape), 0
        self.take_rem = zeros(shape)
        self.log: list[dict[str, Any]] = []
        self.turns: list[tuple[int, int]] = []
        self.stack: list[dict[str, Any]] = []
        self.turned = np.zeros(shape, dtype=bool)
        self.counts: dict[str, int] = dict(COUNTS)
        self.max_transient = self.count_max = 0
        self.last_dp = [0, 0, 0]
        self.last_recoil: dict[str, Any] = {}
        self.start_factors: tuple[Any, ...] = ()
        self.start_frames: list[Any] = []
        self.start_phases: list[tuple[Any, Any]] = []
        self.start_odd: list[Any] = []
        self.stepped: list[list[Line]] = []
        self.lattices: dict[tuple[int, int, tuple[int, ...]], int] = {}
        self.drawn: dict[tuple[tuple[int, ...], int], tuple[int, int] | None] = {}
        self.rotations: dict[tuple[int, int], int] = {}

        for line in self.row(CARRIER).lines[:1]:
            line.now[:], line.before[:] = self.gamma, self.gamma
        self.drift = rule3.largest_below(self.T)
        self.A, self.B = rule3.balanced_pair(half(self.T))
        self.X = phase.amplitude(phase.unit(self.gamma), HALF_WIDTH - 1)
        seed_pair = phase.seed(self.X, self.gamma)
        self.orbit_lines, self.orbit = [seed_pair], [(int(seed_pair[0][0]), int(seed_pair[1][0]))]
        self.start_content, self.start_x = self.content(), self.row(CARRIER).lines[0].now
        self.start_clock = readings.paces_of(self, self.start_content)[0]

    def ride_walls(self) -> None:
        """The riding lines' remainders at the start: a riding line's remainder lives at the mean wall (w div 2)(X_before + X_now) of the carrier's two levels at its Node, half of it at the seed."""
        carrier = self.row(CARRIER).lines[0]
        wall = half(self.w) * (carrier.before + carrier.now)
        for r in self.rows_:
            if r.wall is None and r.shape != CARRIER:
                scaled = wall * gram.scale(r.shape, self.gamma)
                for line in r.lines:
                    line.wall, line.rem = scaled, half(scaled)

    def node_of(self, xyz: Any) -> tuple[int, ...]:
        """A Node named by the world file: three integers on the board; a Node off the board is refused by name."""
        at = tuple(int(x) for x in xyz)
        if len(at) != AXES or any(not 0 <= x < self.cube for x in at):
            raise ValueError(f"a Node off the board: {at!r}")
        return at

    def row(self, shape: int) -> Row:
        """The one row of the shape with a pair, chosen by the numbers alone (rows.row_of)."""
        return row_of(self.rows_, shape)

    def emitter(self) -> Row:
        """The plane of the potential's pair (rows.row_of, a lookup by the shape and the pair's values): the row the Wronskian's change is laid on and whose quanta the close takes."""
        return row_of(self.rows_, PLANE, self.row(POTENTIAL).pair)

    def records(self) -> list[Row]:
        """The record rows in the acts' order, the planes and the quartets (rows.records_of)."""
        return records_of(self.rows_)

    def rule(self, pair: tuple[int, int], c: Any, factors: tuple[Any, ...]) -> rule3.Rule:
        """Rule3's integers of a pair at the Node's paces from the content."""
        clock, pace = readings.paces_of(self, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)

    def rule_of(self, r: Row, c: Any, factors: tuple[Any, ...]) -> rule3.Rule:
        """A row's rule: Rule3's integers at its pair and the Node's paces scaled by the row's scale (gram.scale: 1 but for the quartet), or, for the row with its own wall, no Links and the own weight 2 w (next = 2 now - before + the write inside the division)."""
        if r.wall is not None:
            return rule3.Rule(tuple(0 for _ in range(PORTS)), r.wall + r.wall, r.wall, 0)
        assert r.pair is not None
        return rule3.scaled(self.rule(r.pair, c, factors), gram.scale(r.shape, self.gamma))

    def content(self) -> Any:
        """The content at every Node (readings.content)."""
        return readings.content(self)

    def link_factors(self, axis_levels: list[Any] | None = None, frozen: Any = None) -> tuple[Any, ...]:
        """The Link factor at each Port (readings.link_factors), 0 where either end is frozen."""
        return readings.link_factors(self, axis_levels, frozen)

    def turned_arrival(self, arrivals: list[Any], port: int, turn: list[Link] | None) -> list[Any]:
        """The arrivals of a row's lines at one Port, read in the Node's frame (the row's conjugation where the frame sign is -1, gram.conjugated) and turned plane by plane by the Link's record (links.turned); a row of one line is turned by the identity; `turn` None is the identity for every shape."""
        if turn is None or len(arrivals) == 1:
            return arrivals
        at = turn[port]
        return turned(gram.conjugated(len(arrivals), arrivals, at.frame), at, self.X, self.gamma)

    def arrivals(self, at: list[Any], r: rule3.Rule, turn: list[Link] | None) -> list[Any]:
        """The Links' part of Rule3's total for a row's lines at every Node, SUM_j R_j m_j, the arrivals at each Port turned as the row's shape turns them."""
        totals: list[Any] = [0] * len(at)
        for port, reach in enumerate(r.reaches):
            found = self.turned_arrival([across(a, port) for a in at], port, turn)
            totals = [t + reach * m for t, m in zip(totals, found, strict=True)]
        return totals

    def rotate(
        self,
        lines: list[Line],
        r: rule3.Rule,
        turn: list[Link] | None,
        direction: int,
        flux: list[Any] | None,
        starts: list[Any] | None,
    ) -> list[Line]:
        """Rule3's step of one row at every Node, the one function of a line in either direction (RW-S1: the line's two slots one pair read reversed by the direction, (a, y) = (now, before) forward and (before, now) backward, the total S a - w y + SUM_j R_j m_j, the new level the quotient on the slot the direction names): for each line the total S now - w before + SUM_j R_j m_j (+ the line's flux where the row carries its write inside the division), one carried division at the wall w per line. Backward the same act on the before slots with the division's direction -1."""
        pairs = [(line.now, line.before)[::direction] for line in lines]
        at = starts or [a for a, _y in pairs]
        fluxes: list[Any] = flux or [0] * len(lines)
        totals = [
            r.self_coefficient * a - r.wall * y + f + m
            for (_a, y), a, f, m in zip(pairs, at, fluxes, self.arrivals(at, r, turn), strict=True)
        ]
        found = []
        for line, a, t in zip(lines, at, totals, strict=True):
            self.max_transient = max(self.max_transient, bits_of(t))
            quotient, rem = acts.divide(t, r.wall, line.rem, direction)
            now, before = (quotient, a)[::direction]
            found.append(Line(now, before, rem, line.wall, line.wr, line.wwall))
        return found

    def write(self, line: Line, numerator: Any, direction: int) -> None:
        """The one write act on a line: the numerator's carried division at the line's write wall, the quotient added to the level now (forward) or taken back (backward), the remainder carried in the line."""
        q, line.wr = acts.divide(numerator, line.wwall, line.wr, direction)
        line.now = acts.lay(line.now, q, direction)

    def act(
        self,
        lines: list[Line],
        r: rule3.Rule,
        turn: list[Link] | None,
        numerators: list[Any],
        direction: int,
        flux: list[Any] | None = None,
        top: Any = None,
        kept: list[Line] | None = None,
    ) -> tuple[list[Line], list[Line]]:
        """The Node's act on one row in the direction, one path (RW-S1): Rule3's rotate and the lines' writes taken in the direction's order, the rotate first forward and the write first backward, each at the direction (the former two branches kept by name). Returns the row at the start and the row as the act leaves it (the stepped levels before the write, read by no engine code, struck 2026-10-26: the lean toy spells its own act for its former interval); backward at the turned Nodes `top` the row is set to `kept`, the pre-state the exchange returned."""
        starts = None if kept is None else [np.where(top, line.now, line.before) for line in lines]

        def rotate(found: list[Line]) -> list[Line]:
            return self.rotate(found, r, turn, direction, flux, starts)

        def write(found: list[Line]) -> list[Line]:
            for line, n in zip(found, numerators, strict=True):
                if n is not None:
                    self.write(line, n, direction)
            return found

        first, second = (rotate, write)[::direction]
        found = second(first(lines))
        if kept is not None:
            self.restore(found, kept, top)
        return (lines if direction == 1 else found), found

    def restore(self, lines: list[Line], kept: list[Line], top: Any) -> None:
        """Backward at the turned Nodes `top`: the row set to `kept`, the pre-state the exchange returned (the inverse at a turned Node is no act)."""
        for line, k in zip(lines, kept, strict=True):
            line.now, line.before = np.where(top, k.now, line.now), np.where(top, k.before, line.before)
            line.rem = np.where(top, k.rem, line.rem)
            if np.ndim(k.wall):
                line.wall = np.where(top, k.wall, line.wall)
            if line.wr is not None:
                line.wr = np.where(top, k.wr, line.wr)

    def rows(self) -> list[list[Line]]:
        """The Node's rows' lines in the acts' order."""
        return [r.lines for r in self.rows_]

    def set_rows(self, rows: list[list[Line]]) -> None:
        """Every row's lines replaced, in the acts' order."""
        for r, lines in zip(self.rows_, rows, strict=True):
            r.lines = list(lines)

    def all_lines(self) -> list[Line]:
        """Every line of every row, in the acts' order."""
        return [line for row in self.rows() for line in row]

    def exchange(self, top: Any, held: list[list[Line]]) -> None:
        """The swap's act at the Nodes `top`: every row set to its held row exchanged and conjugated by the row's K (gram.conjugation: a plane's im line negated, the quartet's K0, the identity on another row), every remainder mirrored once per reversal of its line by the one rule: once for time's exchange, twice where the conjugation negates the line (its own entry of K), so an im line's rotation remainder is left; the write remainders and the frame bit once; an involution with the state it leaves."""
        for r, row, hrow in zip(self.rows_, self.rows(), held, strict=True):
            nows, befores, rems = acts.exchange(
                [h.now for h in hrow],
                [h.before for h in hrow],
                [h.rem for h in hrow],
                [h.wall for h in hrow],
                gram.conjugation(r.shape),
            )
            for i, (line, h) in enumerate(zip(row, hrow, strict=True)):
                line.now = np.where(top, nows[i], line.now)
                line.before = np.where(top, befores[i], line.before)
                line.rem = np.where(top, rems[i], line.rem)
                if np.ndim(h.wall):
                    line.wall = np.where(top, h.wall, line.wall)
                if line.wr is not None:
                    line.wr = np.where(top, acts.mirror(h.wr, line.wwall, 1), line.wr)

    def swap(self, held: list[list[Line]], direction: int = 1, top: Any = None) -> Any:
        """The swap at the top, in the direction (RW-S1; backward the exchange of the turned Nodes `top` from the frame, the former Interval's own exchange kept by name): the weak maximum X0 <= X1 >= X2 with one strict (the held before, the held now, the now after the writes), or the floor (X0 or X2 below X_f), at a frozen Node by this trigger alone on its restored line (FR-S1, the owner's words of 2026-10-26, 03:41 UTC, approved, and 07:3x UTC, entered as the fix of a forbidden state: no Node frozen for ever; BH-S1's mask on the trigger struck and kept by name); the turned Node ends the interval at the state it started from, exchanged and complemented."""
        if direction == -1:
            if top.any():
                self.exchange(top, held)
            return top
        k = self.rows_.index(self.row(CARRIER))
        x0, x1, x2 = held[k][0].before, held[k][0].now, self.row(CARRIER).lines[0].now
        peak = np.vectorize(
            lambda a, b, c: (
                int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))
            ),
            otypes=[bool],
        )
        xf = readings.floor(self)
        below = np.vectorize(lambda a, c: int(a) < xf or int(c) < xf, otypes=[bool])
        top = peak(x0, x1, x2) | below(x0, x2)
        self.turned = top
        if top.any():
            self.counts["turns"] += int(top.sum())
            self.turns.append((self.interval, int(top.sum())))
            self.exchange(top, held)
        return top

    def read_lines(
        self, held: list[list[Line]], c: Any, factors: tuple[Any, ...]
    ) -> list[tuple[Line, rule3.Rule]]:
        """The lines the one-Link read takes with their rules: every line of every row at the interval's start, alike."""
        rules = [self.rule_of(r, c, factors) for r in self.rows_]
        return [(line, rule) for rule, lines in zip(rules, held, strict=True) for line in lines]

    def run(self, direction: int = 1) -> None:
        """One interval of the Node's program in the direction (interval.run)."""
        interval.run(self, direction)

    def click(
        self,
        plane_starts: list[list[Line]],
        held: list[list[Line]],
        direction: int = 1,
        frame: dict[str, Any] | None = None,
    ) -> None:
        """The close (close.click), the Node's fourth act, in the direction: backward the close undone from the log's frame."""
        close.click(self, plane_starts, held, direction, frame)

    def step(self, direction: int = 1) -> None:
        """One interval forward, or back at -1 (the former step_back kept by name)."""
        self.run(direction)
