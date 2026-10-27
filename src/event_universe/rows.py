"""The rows of the Node as the universe file names them, no name and no role (the owner's word of 2026-10-25, there is no if): a row is a shape (its count of lines) with a pair (num, den) for Rule3's rule or a wall of its own for a row with no Links; its lines are built here with their walls by shape, the rows ordered for the acts (a shape the law does not name refused by name at the loader, loader/world); the lookups choose a row by its numbers alone. The phase line's amplitude is the universe file's `amplitude`, declared from outside and read at the load (loader/world, node.X), carried above the floor derived from Gamma (phase.floor); no width and no room of the machine stands in the engine (the owner's words of 2026-10-27, 04:0x and 04:4x UTC; the former width constant and the room cut from it struck, the value kept in the file so that every record stands bit for bit)."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.acts import born
from event_universe.core.rule3 import held_wall, quotient

CARRIER = 10  # the shape of the row that carries the wall (the metric's row): its time line and three axis lines
POTENTIAL = 4  # the shape of the row at (den, den) with a time line and three odd lines
PLANE = 2  # the shape of a conjugate pair of records
POWER_TIME = 4  # the held wall's power of Gamma on the carrier's time line, POWER_AXIS the nine axis lines' (K-S1 to K-S3, Y-S1)
POWER_AXIS = 2


def zeros(shape: tuple[int, ...]) -> Any:
    """An integer array of the board's shape at 0 (Python integers, no width)."""
    return np.zeros(shape, dtype=object)


class Row:
    """One row of the Node as the universe file names it: a shape (its count of lines), a pair (num, den) for Rule3's rule, or a wall of its own for a row with no Links (the phase row); its lines."""

    __slots__ = ("shape", "pair", "wall", "lines")

    def __init__(
        self, shape: int, pair: tuple[int, int] | None, wall: int | None, lines: list[Line]
    ) -> None:
        self.shape, self.pair, self.wall, self.lines = shape, pair, wall, lines

    @property
    def gap(self) -> int | None:
        """The pair's gap den - num, None for the row with its own wall."""
        return None if self.pair is None else self.pair[1] - self.pair[0]


class Line:
    """One line of a row: its two levels, its rotation remainder at the rule's wall `wall`, and where the row writes it, its write remainder `wr` at the write wall `wwall`. A lay names a line's two levels, now and before, in that order (two per line, the plane's count PLANE at the slices)."""

    __slots__ = ("now", "before", "rem", "wall", "wr", "wwall")

    def __init__(
        self, now: Any, before: Any, rem: Any, wall: Any, wr: Any = None, wwall: Any = None
    ) -> None:
        self.now, self.before, self.rem, self.wall, self.wr, self.wwall = (
            now,
            before,
            rem,
            wall,
            wr,
            wwall,
        )

    def copy(self) -> Line:
        """The line's arrays copied, its walls shared."""
        wr = None if self.wr is None else self.wr.copy()
        return Line(self.now.copy(), self.before.copy(), self.rem.copy(), self.wall, wr, self.wwall)


def write_walls(
    shape: int, pair: tuple[int, int] | None, den: int, gamma: int, action: int, trace: int
) -> list[Any]:
    """The write walls of a row's lines by its shape: the carrier's time line and its other lines the held walls at the file's trace weight (TW-S1, the owner's word of 2026-10-26, 07:5x UTC: the trace's weight is the universe file's integer, dimensionless, 6 in nature's files, the one value with a sentence in nature, light having no trace; 54 the records' value of 2026-10-25 kept by name, ga2's file at it until its re-lay; rule3.held_wall at the powers POWER_TIME 4 of the time line and POWER_AXIS 2 of the nine axis lines, K-S1 to K-S3, Y-S1), the shape-4 row's four lines T, the plane at the universe's own pair (den, den), the emitter, its first line T (the lay of W-S1), another plane none."""
    if shape == CARRIER:
        powers = (POWER_TIME, *[POWER_AXIS] * (shape - 1))
        return [held_wall(trace, den, gamma, action, p) for p in powers]
    if shape == POTENTIAL:
        return [action] * shape
    if shape == PLANE and pair == (den, den):
        return [action, None]
    return [None] * shape


def lines_of(
    board: tuple[int, ...],
    shape: int,
    pair: tuple[int, int] | None,
    wall: int | None,
    w: int,
    walls: list[Any],
) -> list[Line]:
    """A row's lines at the start: every level 0, every remainder at half its wall (the rule's w, or the row's own wall), a write remainder at half the write wall where the line writes."""
    if wall is not None:
        return [Line(zeros(board), zeros(board), zeros(board) + born(wall), wall)]
    found = []
    for ww in walls:
        wr = None if ww is None else zeros(board) + born(ww)
        found.append(Line(zeros(board), zeros(board), zeros(board) + born(w), w, wr, ww))
    return found


def order_key(row: Row) -> tuple[bool, int]:
    """The acts' order as a key compared and never tested: the row with its own wall first, then every row by the count of lines it writes, a row whose write reads other rows after them (the records writing nothing, the emitter its one line, the shape-4 row its four, the carrier its ten), the ties in the file's order."""
    return row.wall is None, sum(1 for line in row.lines if line.wwall is not None)


def rows_of(universe: dict[str, Any], board: tuple[int, ...], w: int) -> tuple[list[Row], list[Row]]:
    """The rows from the universe file's list, each a shape with a pair or a wall of its own, in the acts' order, and the same rows in the file's order (a lay names a row by its index); the file's shapes refused by name: a shape-1 row with a pair (the emitter is the plane whose pair is (den, den)), a count of the carrier, the shape-4 row, the emitter or the walled row other than one, the carrier off (den - den div Gamma, den), the shape-4 row off (den, den), no plane at another pair; a pair named in several rows is admitted as written, each row a record of its own with the same numbers (CS5-S2, the owner's word of 2026-10-25, 22:50 UTC, through the Boss: no row refused for its pair's repetition)."""
    ints = universe["integers"]
    den, gamma, action = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])
    trace = int(ints["trace"])
    by_index: list[Row] = []
    for r in universe["rows"]:
        shape = int(r["shape"])
        pair = None if r.get("pair") is None else (int(r["pair"][0]), int(r["pair"][1]))
        wall = None if r.get("wall") is None else int(r["wall"])
        if shape == 1 and wall is None:
            raise ValueError("a shape-1 row with a pair: the gap-0 row is the plane at (den, den)")
        walls = write_walls(shape, pair, den, gamma, action, trace)
        lines = lines_of(board, shape, pair, wall, w, walls)
        by_index.append(Row(shape, pair, wall, lines))
    rows = sorted(by_index, key=order_key)
    walled = [r for r in rows if r.wall is not None]
    planes = [r for r in rows if r.shape == PLANE]
    emitters = [r for r in planes if r.pair == (den, den)]
    carriers = [r for r in rows if r.shape == CARRIER]
    potentials = [r for r in rows if r.shape == POTENTIAL]
    if len(walled) != 1 or len(emitters) != 1 or len(carriers) != 1 or len(potentials) != 1:
        raise ValueError(
            "the universe names one row with its own wall, one plane at the gap 0, one shape-10 row and one shape-4 row"
        )
    if carriers[0].pair != (den - quotient(den, gamma), den):
        raise ValueError(
            "the shape-10 row is the clock's one level: its pair (den - den div Gamma, den)"
        )
    if potentials[0].pair != (den, den):
        raise ValueError("the shape-4 row stands at (den, den)")
    if len(planes) == len(emitters):
        raise ValueError("the universe names no plane row with a gap")
    return rows, by_index


def row_of(rows: list[Row], shape: int, pair: tuple[int, int] | None = None) -> Row:
    """The one row of the shape with a pair, and of the pair where given, chosen by the numbers alone (the emitter: the plane of the potential's pair)."""
    return next(
        r for r in rows if r.shape == shape and r.wall is None and (pair is None or r.pair == pair)
    )


def walled_of(rows: list[Row]) -> Row:
    """The one row with a wall of its own and no Links."""
    return next(r for r in rows if r.wall is not None)


def records_of(rows: list[Row]) -> list[Row]:
    """The record rows in the acts' order, the planes (the emitter among them)."""
    return [r for r in rows if r.shape == PLANE]
