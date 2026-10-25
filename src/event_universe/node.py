"""The generic Node (the owner's word of 2026-10-25: the Node knows nothing, there is no if): its state is the rows the universe file names on the board the world file names, 95 integers at every Node; its readings at an interval's start (the content, the paces, the Link factors, the frames, the Links' counts and phases, the conserved form's share); its acts on a row, each one act on every row alike in either direction (Rule3's rotate with the arrivals turned as the row's shape turns them, the write by one carried division, the exchange at the turned Nodes); the interval's program is interval.run and the close is close.click, each a function of the Node."""

from __future__ import annotations

import hashlib
from typing import Any

import numpy as np

from event_universe import close, interval, readings, seed, take
from event_universe.core import paces, rule3
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import carried_division, half, link_unit_of, mirrored, unit_of, wall_of
from event_universe.features import phase
from event_universe.links import Link, turn_pair
from event_universe.rows import (
    CARRIER,
    HALF_WIDTH,
    PLANE,
    Line,
    Row,
    records_of,
    row_of,
    rows_of,
    walled_of,
    zeros,
)

COUNTS = {  # the run's counts, every one 0 at the start
    "births": 0,
    "taken": 0,
    "booked": 0,
    "body_clicks": 0,
    "refused_stop": 0,
    "refused_origin": 0,
    "refused_lay": 0,
    "refused_orientation": 0,
    "refused_twist": 0,
    "turns": 0,
    "laid": 0,
    "laid_nodes": 0,
}


def bits_of(a: Any) -> int:
    """The largest bit length of an integer array's values."""
    return int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a)))


def scalar(a: Any) -> int:
    """The one integer of a one-element array (a lookup at one level)."""
    return int(np.asarray(a, dtype=object).reshape(-1)[0])


class Node:
    """The Node from the universe's integers and rows and the world's shape and seed, nothing else (the owner's rule: no number in the code)."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any]) -> None:
        ints = universe["integers"]
        self.den, self.gamma = int(ints["den"]), int(ints["node_clock"])
        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)
        shape = tuple(int(x) for x in world["shape"])
        if len(shape) != AXES or len(set(shape)) != 1:
            raise ValueError("the board is a cube: the shape is [c, c, c]")
        self.cube, self.shape = shape[0], shape
        self.w = wall_of(self.den, self.gamma, self.G)
        paces.certified(self.gamma)
        self.rows_, self.by_index = rows_of(universe, shape, self.w)
        self.gapped = [r for r in self.records() if r.gap is not None and r.gap > 0]
        self.units = [
            unit_of(sine_den(r.pair[0], self.den) if r.gap else self.den, self.T)
            for r in self.records()
            if r.pair
        ]
        self.unit_gap0 = self.units[self.records().index(self.row(PLANE, gap=0))]
        self.start_state()
        seed.lay_world(self, world.get("seed", []))
        self.ride_walls()

    def start_state(self) -> None:
        """The Node's state before the seed: the records' standing, crossings and beats, the proper count, the closes, the interval, the log, the turns, the frames' stack, the run's counts; the carrier's time line at Gamma, the drift the largest integer whose square is at most T, the lay's amplitude where the rule has no positive term, the phase pair's amplitude from half the width less one and the orbit's seed."""
        shape, nr = self.shape, len(self.records())
        self.standing = [zeros(shape) for _ in range(nr)]
        self.crossed = [zeros(shape) for _ in range(nr)]
        self.beats = [zeros(shape) for _ in range(nr)]
        self.proper, self.closes = zeros(shape), zeros(shape)
        self.interval = 0
        self.log: list[dict[str, Any]] = []
        self.turns: list[tuple[int, int]] = []
        self.stack: list[dict[str, Any]] = []
        self.turned = np.zeros(shape, dtype=bool)
        self.counts: dict[str, int] = dict(COUNTS)
        self.max_transient = 0
        self.count_max = 0
        self.last_dp = [0, 0, 0]
        self.start_factors: tuple[Any, ...] = ()
        self.start_frames: list[Any] = []
        self.start_phases: list[tuple[Any, Any]] = []
        self.start_odd: list[Any] = []
        self.stepped: list[list[Line]] = []

        gamma, action = self.gamma, self.T
        for line in self.row(CARRIER).lines[:1]:
            line.now[:] = gamma
            line.before[:] = gamma
        self.drift = rule3.largest_below(action)
        self.A = rule3.largest_below(half(action))
        self.X = phase.amplitude(phase.unit(gamma), HALF_WIDTH - 1)
        seed_pair = phase.seed(self.X, gamma)
        self.orbit_lines = [seed_pair]
        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]
        self.start_content = self.content()

    def ride_walls(self) -> None:
        """The riding lines' remainders at the start: a riding line's remainder lives at the mean wall (w div 2)(X_before + X_now) of the carrier's two levels at its Node, half of it at the seed."""
        carrier = self.row(CARRIER).lines[0]
        wall = half(self.w) * (carrier.before + carrier.now)
        for r in self.rows_:
            if r.wall is None and r.shape != CARRIER:
                for line in r.lines:
                    line.wall, line.rem = wall, half(wall)

    def node_of(self, xyz: Any) -> tuple[int, ...]:
        """A Node named by the world file: three integers on the board; a Node off the board is refused by name."""
        at = tuple(int(x) for x in xyz)
        if len(at) != AXES or any(not 0 <= x < self.cube for x in at):
            raise ValueError(f"a Node off the board: {at!r}")
        return at

    def row(self, shape: int, gap: int | None = None) -> Row:
        """The one row of the shape (and of the gap den - num where given), chosen by the numbers alone."""
        return row_of(self.rows_, shape, gap)

    def walled(self) -> Row:
        """The one row with a wall of its own and no Links."""
        return walled_of(self.rows_)

    def records(self) -> list[Row]:
        """The shape-2 rows in the acts' order."""
        return records_of(self.rows_)

    def rule(self, pair: tuple[int, int], c: Any, factors: tuple[Any, ...]) -> rule3.Rule:
        """Rule3's integers of a pair at the Node's paces from the content."""
        clock, pace = readings.paces_of(self, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)

    def rule_of(self, r: Row, c: Any, factors: tuple[Any, ...]) -> rule3.Rule:
        """A row's rule: Rule3's integers at its pair and the Node's paces, or, for the row with its own wall, no Links and the own weight 2 w (next = 2 now - before + the write inside the division)."""
        if r.wall is not None:
            return rule3.Rule(tuple(0 for _ in range(PORTS)), 2 * r.wall, r.wall, 0)
        assert r.pair is not None
        return self.rule(r.pair, c, factors)

    def content(self) -> Any:
        """The content at every Node (readings.content)."""
        return readings.content(self)

    def link_factors(self, axis_levels: list[Any] | None = None) -> tuple[Any, ...]:
        """The Link factor at each Port (readings.link_factors)."""
        return readings.link_factors(self, axis_levels)

    def share(self, line: Line, r: rule3.Rule, pace: Any = None, vacuum: bool = False) -> Any:
        """The conserved form's share at every Node (readings.share)."""
        return readings.share(self, line, r, pace, vacuum)

    def turned_arrival(self, arrivals: list[Any], port: int, turn: list[Link] | None) -> list[Any]:
        """The arrivals of a row's lines at one Port, read in the Node's frame and turned by the Link's pair over X and by the odd line's tangent triple (W^2 - n^2, 2 W n, W^2 + n^2), W = 4 Gamma, one rounding per Link per part, every number the Link's record; a row of one line is turned by the identity; `turn` None is the identity for every shape."""
        if turn is None or len(arrivals) == 1:
            return arrivals
        at = turn[port]
        re_j, im_j = arrivals[0], at.frame * arrivals[1]
        wl = 4 * self.gamma
        a_re, a_im = turn_pair(re_j, im_j, at.cosine, at.sine, self.X)
        return list(
            turn_pair(a_re, a_im, wl * wl - at.odd * at.odd, 2 * wl * at.odd, wl * wl + at.odd * at.odd)
        )

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
        """Rule3's step of one row at every Node, the one function of a line: for each line the total S now - w before + SUM_j R_j m_j (+ the line's flux where the row carries its write inside the division), one carried division at the wall w per line. Backward the same act on the before slots with the division's direction -1."""
        at = (
            [line.now if direction == 1 else line.before for line in lines] if starts is None else starts
        )
        fluxes: list[Any] = flux or [0] * len(lines)
        totals = [
            r.self_coefficient * a - (r.wall * line.before if direction == 1 else 0) + f + m
            for line, a, f, m in zip(lines, at, fluxes, self.arrivals(at, r, turn), strict=True)
        ]
        found = []
        for line, a, t in zip(lines, at, totals, strict=True):
            if direction == 1:
                self.max_transient = max(self.max_transient, bits_of(t))
            quotient, rem = carried_division(t, r.wall, line.rem, direction)
            if direction == 1:
                found.append(Line(quotient, line.now, rem, line.wall, line.wr, line.wwall))
            else:
                found.append(Line(a, quotient - line.now, rem, line.wall, line.wr, line.wwall))
        return found

    def write(self, line: Line, numerator: Any, direction: int) -> None:
        """The one write act on a line: the numerator's carried division at the line's write wall, the quotient added to the level now (forward) or taken back (backward), the remainder carried in the line."""
        q, line.wr = carried_division(numerator, line.wwall, line.wr, direction)
        line.now = line.now + direction * q

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
    ) -> tuple[list[Line], list[Any], list[Line]]:
        """The Node's act on one row in the direction: Rule3's rotate of the row then its lines' writes (forward); the writes undone then the rotate inverted (backward). Returns the row at the start, the stepped levels before the write, and the row as the act leaves it; backward at the turned Nodes `top` the row is set to `kept`, the pre-state the exchange returned."""
        if direction == 1:
            stepped = self.rotate(lines, r, turn, 1, flux, None)
            levels = [line.now for line in stepped]
            for line, n in zip(stepped, numerators, strict=True):
                if n is not None:
                    self.write(line, n, 1)
            return lines, levels, stepped
        starts = None if kept is None else [np.where(top, line.now, line.before) for line in lines]
        for line, n in zip(lines, numerators, strict=True):
            if n is not None:
                self.write(line, n, -1)
        levels = [line.now for line in lines]
        start = self.rotate(lines, r, turn, -1, flux, starts)
        if kept is not None:
            self.restore(start, kept, top)
        return start, levels, start

    def carried(
        self,
        lines: list[Line],
        r: rule3.Rule,
        numerators: list[Any],
        direction: int,
        top: Any,
        kept: list[Line] | None,
    ) -> list[Line]:
        """The carrier's act: its one division with the write sourced by the riding rows (the act of every row, the carrier's by this name so that a hand may hold it)."""
        return self.act(lines, r, None, numerators, direction, None, top, kept)[2]

    def restore(self, lines: list[Line], kept: list[Line], top: Any) -> None:
        """Backward at the turned Nodes `top`: the row set to `kept`, the pre-state the exchange returned (the inverse at a turned Node is no act)."""
        for line, k in zip(lines, kept, strict=True):
            line.now, line.before, line.rem = (
                np.where(top, k.now, line.now),
                np.where(top, k.before, line.before),
                np.where(top, k.rem, line.rem),
            )
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

    def is_im(self) -> list[bool]:
        """Which lines are a plane's im line (the second line of a shape-2 row), conjugated at a turned Node."""
        return [len(row) == PLANE and k == 1 for row in self.rows() for k in range(len(row))]

    def exchange(self, top: Any, held: list[list[Line]]) -> None:
        """The swap's act at the Nodes `top`: every line set to the held line exchanged and mirrored (the two levels exchanged, an im line conjugated, every remainder mirrored once per reversal of its line by the one rule: once for time's exchange, twice where the conjugation negates the line, so an im line's rotation remainder is left; the write remainders and the frame bit once); an involution with the state it leaves."""
        for line, h, im in zip(
            self.all_lines(), [line for row in held for line in row], self.is_im(), strict=True
        ):
            sgn = -1 if im else 1
            line.now = np.where(top, sgn * h.before, line.now)
            line.before = np.where(top, sgn * h.now, line.before)
            line.rem = np.where(top, mirrored(h.rem, h.wall, 1 + (sgn < 0)), line.rem)
            if np.ndim(h.wall):
                line.wall = np.where(top, h.wall, line.wall)
            if line.wr is not None:
                line.wr = np.where(top, mirrored(h.wr, line.wwall, 1), line.wr)

    def swap(self, held: list[list[Line]]) -> Any:
        """The swap at the top: the weak maximum X0 <= X1 >= X2 with one strict (the held before, the held now, the now after the writes), or the floor (X0 or X2 below X_f); the turned Node ends the interval at the state it started from, exchanged and complemented."""
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
        self, held: list[list[Line]], plane_starts: list[list[Line]], c: Any, factors: tuple[Any, ...]
    ) -> list[tuple[Line, rule3.Rule]]:
        """The lines the one-Link read takes with their rules: every line of every row at the interval's start, alike."""
        return [
            (line, self.rule_of(r, c, factors))
            for r, lines in zip(self.rows_, held, strict=True)
            for line in lines
        ]

    def digit_of(self, rem: int, values: int) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds."""
        return rem, values

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

    def lay(self, rec: int, where: Any, levels: tuple[Any, Any, Any, Any], sign: int = 1) -> None:
        """The one lay act (take.lay)."""
        take.lay(self, rec, where, levels, sign)

    def step(self) -> None:
        self.run(1)

    def step_back(self) -> None:
        self.run(-1)

    def census(self) -> tuple[int, int]:
        """The count of integer arrays the Node holds and the largest bit length among their values."""
        lines = self.all_lines()
        arrays = [a for line in lines for a in (line.now, line.before, line.rem)]
        arrays += [line.wr for line in lines if line.wr is not None]
        arrays += self.standing + self.crossed + self.beats + [self.proper, self.closes]
        return len(arrays), max(bits_of(a) for a in arrays)

    def state_bytes(self) -> bytes:
        """Every level and remainder of the state as text bytes, the run back's comparison bit for bit."""
        lines = self.all_lines()
        arrays = [a for line in lines for a in (line.now, line.before, line.rem)]
        arrays += [line.wr for line in lines if line.wr is not None]
        return " ".join(str(int(v)) for a in arrays for v in a.reshape(-1)).encode()

    def state_hash(self) -> str:
        """The state's hash with the interval."""
        return hashlib.sha256(self.state_bytes() + str(self.interval).encode()).hexdigest()
