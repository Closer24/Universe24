"""The generator makes a body (ALGEBRA.md #the-generator, the generator is Rule3; the model owner's word of 2026-09-28, 22:05 Israel: no body is reduced to one Node, the generator generates a whole body): the mode file of a world of bodies and the bodies themselves. A body is its quanta, M, about a centre; the world declares it with one Node carrying M (a new body) or with its Nodes and their counts (a body laid before, laid anew here). The generator finds the body's fixed point in whole integers: the counts at its Nodes source every held row of the universe file at the row's level weight, the rest of each row by the start (features/start: the division act iterated from nothing until the levels repeat) is the level every record reads, the body's record is the standing record Rule3 makes in those paces, the held rows then rest under that record by the engine's own start (`start_content`, one act with `GameBoard.start`: the form of the record as the hold books it over the write's wall, the lay and the rest iterated to the fixed point; the count is the seed of the first pass alone), and the counts are that record's share in quanta at the paces of its read in those rests (ALGEBRA.md #the-count-is-the-records-share) at every Node of the body's region, until the counts return themselves within the rounding, each round taking the half step from the counts toward the share (the deep well overshoots under the whole step); the body's Nodes are then the Nodes carrying a quantum, its region those Nodes and a Link around them (widened a Link a round while the share reaches a quantum there, narrowed where it falls below one; the region names the body's Nodes and where its counts are read, not where its record is iterated), and the record written is the top mode of the read act on the board as declared (`on_the_board`: a mode cut at the region is no mode of the board's and relaxes when laid), the content it stands in the board's. The counts the world declares are the engine's own reading at the start, the record's share in quanta at the paces of its read, the held rows at the rests the engine's start lays under the laid records (`read_at_the_start` calls the same act), so one body's declaration is the gate's reading within the rounding."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from math import lcm
from pathlib import Path
from typing import Any, cast

import numpy as np

from event_universe.bookings import booked_sources
from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import (
    NO_READ,
    coefficients,
    division_fixed_point,
    division_forward,
    rule3,
)
from event_universe.features.start import (
    RestCollapses,
    Sourced,
    held_rests,
    returned,
    settled_rows,
)
from event_universe.loader.derived import FamilyRule, held_write, with_records
from event_universe.loader.faces import faces_of
from event_universe.loader.keys import AXES
from event_universe.loader.lay import FIXED_POINT, Lay, lay_of
from event_universe.loader.universe import universe_of
from event_universe.node import Record, empty_state, ports, record_slice, wronskian
from event_universe.node import read as content_read
from event_universe.share import quanta_of, share
from event_universe.world_files import input_digest, world_files

Axis = tuple[int, int, int]


@dataclass(frozen=True)
class Board:
    """The world's board as Rule3 sees it: its shape, its face rule (which axes wrap, the Nodes beyond it), the universe's Gamma and T, and a record's pair [num, den] as the file writes it."""

    shape: Axis
    wrap: Wrap
    gamma: int
    action: int
    pair: tuple[int, int]
    width: int  # the largest integer of the universe's width, 2^width - 1
    unit: int  # the Link's unit G, the run's declaration like Gamma (ALGEBRA.md #the-paces)


@dataclass(frozen=True)
class Standing:
    """A body's standing record over its window: the share in quanta its record carries over the region at the vacuum's paces, the window's length (the period is [window, 2]), the amplitude b, the clock pair [next + before, now] at the largest level at the centre, and the two levels over the board at that moment with the next level after it."""

    carried: int
    window: int
    amplitude: int
    clock: tuple[int, int]
    now: np.ndarray
    before: np.ndarray
    next: np.ndarray


def step(
    board: Board, content: np.ndarray, now: np.ndarray, before: np.ndarray, remainder: np.ndarray
) -> np.ndarray:
    """One interval of Rule3 on the whole board, the engine's own form: the six arrivals through the Ports (0 beyond a face, the wrap on a periodic one, `node.ports`), the coefficients from the composed paces of the content at every Node with no tension (core.rule3, core.paces, ALGEBRA.md #the-paces), the division by the wall with the remainder kept at the Node."""
    reads, self_coefficient, wall = coefficients(
        board.pair[0],
        board.pair[1],
        board.gamma,
        *paces.node_paces(board.gamma, content),
        None,
        board.unit,
    )
    arrivals = ports(now, board.wrap)
    nxt, remainder[...] = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    return np.asarray(nxt, dtype=np.int64)


def share_of(board: Board, content: np.ndarray | int, now: np.ndarray, before: np.ndarray) -> np.ndarray:
    """The record's weighted share at every Node in the current's units, the engine's own `share.share` at the paces of the content (ALGEBRA.md #the-count-is-the-records-share): the conserved form's Node term over the Link's pace squared less the plain Link term."""
    record = Record(now.astype(np.int64), before.astype(np.int64), np.zeros(board.shape, dtype=np.int64))
    found = share(board.pair, record, board.wrap, board.gamma, content, None, board.unit)
    return np.asarray(found, dtype=np.int64)


def read_quanta(share_now: np.ndarray, den: int, action: int) -> np.ndarray:
    """A share read in quanta at every Node, the engine's own reading (`share.quanta_of`): (share + W_c div 2) div W_c with W_c = 3 den T by Rule3's division act (ALGEBRA.md #the-count-is-the-records-share)."""
    return np.asarray(quanta_of(share_now, 3 * den * action, np.int64))


def period_reading(
    board: Board, content: np.ndarray, node: Axis, state: list[np.ndarray]
) -> tuple[int, int, tuple[int, int], np.ndarray, np.ndarray, np.ndarray] | None:
    """One whole period of the record at the centre, from the interval its level returns upward through 0 to the next such return: the period's length, the largest |now| at the centre and the pair [next + before, now] with the three levels over the board at that moment; None when the whole state repeats before the level returns twice (a cloud, no record). `state` is [now, before, remainder], stepped in place."""
    now, before, remainder = state
    sign = 1 if now[node] > 0 else -1 if now[node] < 0 else 0
    length, largest, best, returned = 0, -1, None, False
    seen: set[bytes] = set()
    while (key := digest(now, before, remainder)) not in seen:
        seen.add(key)
        nxt = step(board, content, now, before, remainder)
        here = int(now[node])
        if here > 0 and sign <= 0:
            if returned and best is not None:
                state[:] = [now, before, remainder]
                return (length, largest, best[0], best[1], best[2], best[3])
            returned = True
        if here:
            sign = 1 if here > 0 else -1
        if returned:
            length += 1
            if abs(here) > largest:
                largest = abs(here)
                best = (
                    (int(nxt[node]) + int(before[node]), here),
                    now.copy(),
                    before.copy(),
                    nxt.copy(),
                )
        now, before = nxt, now
    return None


def digest(*arrays: np.ndarray) -> bytes:
    """A state's digest for the repeat searches, the arrays' bytes hashed so that the memory of a search is bounded on a large board (a repeat is read exactly on the digest, the tool's own bookkeeping and no number of the law)."""
    found = hashlib.sha256()
    for array in arrays:
        found.update(array.tobytes())
    return found.digest()


def agree(first: int, second: int) -> bool:
    """Two readings of a count within the rounding of its amplitude, ((|a - b| - 1) div 2)^2 at most the larger, as integer squares."""
    return bool(within(np.array(first - second), np.array(max(first, second))))


def within(off: np.ndarray, largest: np.ndarray) -> np.ndarray:
    """The law's gate at every Node, ((|a - b| - 1) div 2)^2 <= c by Rule3's division act, the root's inequality written as a square."""
    half = np.asarray(division_forward(np.abs(off) - 1, 2, 0)[0])
    return (np.abs(off) <= 1) | (half * half <= largest)


def on_the_board(board: Board) -> np.ndarray:
    """The Nodes of the board as declared, every Node but those beyond an inner face (nothing stands there): the region the top mode is iterated on and the record is written over. The standing state the engine steps is the top mode of the read act on the board as declared, its faces read as the engine reads them (0 beyond an open or a closed face, the wrap on a periodic one), and not on the body's region with 0 beyond: a mode of the cut operator is no mode of the board's (the Boss's word of 2026-10-02 on the fourth finding, the region's cut compressing the mode: in the pixel's start the mode cut a Link beyond the body's Nodes rotated at 1.3774 against the board's 1.3810 and carried 21 percent less share at the same amplitude, and released on the board it relaxed by a third at the centre)."""
    return np.ones(board.shape, dtype=bool) if board.wrap.beyond is None else ~board.wrap.beyond


def own_board(board: Board, others: np.ndarray) -> np.ndarray:
    """The board as declared less the other bodies' regions (their Nodes carrying a quantum and a Link around them, `others` their counts): the region a body's top mode is iterated on and its record written over. The power iteration finds the top mode of the read in the whole content, which sits in the deepest well; a second body laid in the first's sources needs its own mode, the top mode outside the first's region (laid on the whole board the second body's scale ran away to carry its quanta within its own region, its form collapsing the rest; the look's chain of two bodies, 2026-10-02); the bodies' regions never share a Node, and a body's mode is small at the other's region, so the cut costs it little."""
    return np.asarray(on_the_board(board) & ~dilated(others > 0, board.wrap), dtype=bool)


def dilated(mask: np.ndarray, wrap: Wrap) -> np.ndarray:
    """The mask and its six-neighbour surroundings (the wrap on a periodic axis, nothing beyond a face)."""
    grown = mask.copy()
    for axis in range(3):
        for sense in (1, -1):
            grown |= np.asarray(arrival(mask.astype(np.int64), axis, sense, wrap, 0)) > 0
    return grown


ACTS_OF_A_HELD_ROW = 1 + 1  # the acts `held_rests` composes per held row: its rest's and its booking's
ROUNDINGS_OF_A_STEP = (
    1 + 1 + 1 + 1
)  # the acts composed in next + before - clock x now: now, before, next, the clock's level


def rotation_spread(
    now: np.ndarray, before: np.ndarray, nxt: np.ndarray, where: np.ndarray
) -> tuple[Fraction, int, Fraction]:
    """The one-step reading of a record in a content: the rotation (next + before) / now at every Node of `where` carrying a level, its median (the mode's clock as the body reads it), the number of Nodes read and the largest departure from the median in units of the Node's rounding 1 / |now|: next + before - clock x now is made of integers each rounded once, the two laid levels by the generator's scale act, next by the step's own act and the clock's level at the median's Node, so a record standing in the content departs at most one unit per act composed, `ROUNDINGS_OF_A_STEP`, at every Node (the power iteration's own integer fixed point at the pixel's amplitude departs up to 4.6 units in the rule's seed well, a GameBoard reading of 2026-10-02), and a record departing further is no mode of the step in that content."""
    read = where & (now != 0)
    sums, levels = (nxt + before)[read].tolist(), now[read].tolist()
    ratios = sorted(Fraction(int(s), int(level)) for s, level in zip(sums, levels, strict=True))
    if not ratios:
        return Fraction(0), 0, Fraction(0)
    median = ratios[len(ratios) // 2]
    worst = max(
        abs(Fraction(int(s), int(level)) - median) * abs(int(level))
        for s, level in zip(sums, levels, strict=True)
    )
    return median, len(ratios), worst


def top_mode(
    board: Board, content: np.ndarray, keep: np.ndarray, seed: np.ndarray, unit: int
) -> tuple[np.ndarray, np.ndarray]:
    """The iteration of the generator (ALGEBRA.md #the-generator (b)): Rule3's read act with the before-coefficient 0, a <- (SUM over the Ports of R_ij arr_j + S a) div w within `keep` (the board as declared, `on_the_board`) and 0 outside it, then the division act to a fine unit (the level times the unit over its largest size): the power iteration of the symmetric form's top mode, the body's bound mode; the stop is the first repeat of the integer vector, exact, no tolerance. The fine unit is derived from the width and never written, the largest at which the read of a level stays inside the host's width (`MAX_WORK_INT` over twice the sum of the coefficients at a Node, as the start derives its own, `features.start.unit_of`), so that the rounding trap of the iteration is far below the amplitude's rounding; the mode is then rounded once to the amplitude `unit` by the division act and read once more: returns the mode at the amplitude and its read, (SUM over the Ports of R_ij arr_j + S a) div w, the mode times its rotation 2 cos omega within the step's one act."""
    reads, self_coefficient, wall = coefficients(
        board.pair[0],
        board.pair[1],
        board.gamma,
        *paces.node_paces(board.gamma, content),
        None,
        board.unit,
    )
    reach = int((np.abs(np.asarray(self_coefficient)) + sum(np.asarray(read) for read in reads)).max())
    fine = max(unit, int(division_forward(MAX_WORK_INT, 2 * reach, 0)[0]))

    def read_of(a: np.ndarray) -> np.ndarray:
        total = np.asarray(rule3(reads, ports(a, board.wrap), self_coefficient, wall, a, 0, 0)[0])
        return np.where(keep, total, 0).astype(np.int64)

    def scaled(total: np.ndarray, to: int) -> np.ndarray:
        largest = int(np.abs(total).max())
        if largest == 0:
            return total
        return np.asarray(division_forward(total * to, largest, 0)[0], dtype=np.int64)

    a = scaled(np.where(keep, seed, 0).astype(np.int64), fine)
    seen: set[bytes] = set()
    while True:
        total = read_of(a)
        if not total.any():
            break
        a = scaled(total, fine)
        key = digest(a)
        if key in seen:
            break
        seen.add(key)
    a = scaled(a, unit)
    return a, read_of(a)


def standing(
    board: Board,
    content: np.ndarray,
    node: Axis,
    shape_seed: np.ndarray,
    scale: int,
    region: np.ndarray,
    keep: np.ndarray,
) -> Standing | None:
    """The standing record of the body in a content: the top mode of Rule3's read act over `keep`, the board as declared outside the other bodies' regions (`own_board`; the power iteration from the body's shape, scaled to `scale` at its largest level; a bound mode's eigenvalue stands above the band's top, so the iteration on the board finds it, and the other bodies' regions are left out so that it is this body's mode and not the deeper well's), laid at its peak, the level before and the level next alike at half the mode's read (next + before = 2 cos omega x now at every Node of a standing record, so before = next = the read div 2 at the peak), the clock pair [the read, now] at the centre, the period read by Rule3 from that record (`period_reading`, the length from the centre's return upward through 0 to the next, the window twice it) and the share in quanta the record carries over the region at the paces of the content; None, no record, where the mode departs from one rotation across the region by more than the roundings of a step at a Node (`rotation_spread`, `ROUNDINGS_OF_A_STEP`: the mode is no eigenvector of the read in this content within the integers' rounding, a cloud's or a trapped iteration's), where the mode is 0 at the centre or where the centre's level never returns (a cloud, no period). The read act with the before-coefficient 0 is Rule3's own and the step a <- read - before keeps the record: a record stepped from this lay rotates at the mode's clock within the rounding."""
    now, total = top_mode(board, content, keep, shape_seed, scale)
    if not now[node]:
        return None
    if now[node] < 0:
        now, total = -now, -total
    if rotation_spread(now, np.zeros_like(now), total, region)[2] > ROUNDINGS_OF_A_STEP:
        return None
    before = np.asarray(division_forward(total, 2, 0)[0], dtype=np.int64)
    nxt = total - before
    carried = int(
        np.where(
            region, read_quanta(share_of(board, content, now, before), board.pair[1], board.action), 0
        ).sum()
    )
    reading = period_reading(
        board, content, node, [now.copy(), before.copy(), np.zeros(board.shape, dtype=np.int64)]
    )
    if reading is None:
        return None
    return Standing(
        carried,
        2 * reading[0],
        int(np.abs(now).max()),
        (int(total[node]), int(now[node])),
        now,
        before,
        nxt,
    )


def rows_read(universe: dict[str, Any], family: str, sign: bool) -> list[tuple[int, FamilyRule]]:
    """The held rows a body's family reads into its paces that hold the sign (`sign`, sourced by the Wronskian) or the content (sourced by the form), each by its position among the universe's families with its rule, as the loader reads the family's declaration (ALGEBRA.md #the-paces); a holder of the sign that declares the rotation is read by the turn of the record and not into the pace, so it is none of these (its turn leaves the record's share as it is)."""
    families = universe_of(universe)[1]
    reader = families[[row.name for row in families].index(family)]
    found = []
    for read in reader.reads:
        row = families[read.family]
        if row.wronskian == sign and not row.rotation:
            found.append((read.family, row))
    return found


Rows = list[tuple[int, FamilyRule]]  # the held rows of the content a body's family reads, by position


def held_rows(universe: dict[str, Any], family: str) -> Rows:
    """The held rows holding the content a body's family reads: the rows whose levels are the content its record reads, sourced by the plain share of its record; refused by name where there is none, a body needing a row to bind in."""
    found = rows_read(universe, family, False)
    if not found:
        raise ValueError(
            f"the family {family!r} reads no held row of the content: a body needs a row to bind in "
            "(ALGEBRA.md #the-generator)"
        )
    return found


def family_of(universe: dict[str, Any], name: str) -> FamilyRule:
    """A family of the universe file as the loader derives it, by its name."""
    families = universe_of(universe)[1]
    return families[[row.name for row in families].index(name)]


def rests(rows: Rows, counts: np.ndarray, board: Board) -> np.ndarray:
    """Every held row's level under counts in quanta at the row's level weight times its write weight, the seed of a lay and no result (the engine's start sources the form, `start_content`): every holder of the content at the rest of its own line, reading the holders among these rows its declaration names at their weights, its own level among them where it names itself (features/start, `settled_rows`: the division act iterated from nothing until it repeats, at the row's pair and level weight, with or without a gap), with its vacuum content added (the massless row's `rest`), summed into the content every record reads: the first lay's well, the shape a body's first record is seeded with."""
    positions = [position for position, _row in rows]
    sourced = [
        (
            row.write * counts,
            row.pair,
            int(row.level_weight or 0),
            row.rest,
            tuple((positions.index(r.family), r.weight) for r in row.reads if r.family in positions),
        )
        for _position, row in rows
    ]
    fields = settled_rows(sourced, board.wrap, board.width, board.gamma, board.unit)
    return sum(
        (
            np.asarray(field.levels, dtype=np.int64) + row[3]
            for field, row in zip(fields, sourced, strict=True)
        ),
        np.zeros(counts.shape, dtype=np.int64),
    )


Pairs = list[tuple[np.ndarray, np.ndarray]]  # a body's level pairs as laid, (now, before) per line pair
Laid = list[
    tuple[int, int, Pairs]
]  # laid records: each its family, its record number and its level pairs
Others = tuple[np.ndarray, Laid]  # the other bodies' counts (the seed's) and the other records as laid


def start_content(
    board: Board, families: tuple[FamilyRule, ...], index: int, slot: int, pairs: Pairs, others: Laid
) -> np.ndarray:
    """The content a body's record reads at the engine's own start, by the engine's own act and no copy of it (`GameBoard.start`; `booked_sources` and `held_rests` are the one act, so the generator and the engine compute one fixed point and agree by construction): the body's level pairs laid on its record's lines and the other bodies' and the messages' on theirs (`others`, each its family and its record, `node.record_slice`; the symmetric lay over a record's parts, the plane's second pair on its second line), every held row at the rest the lay and the rest return together from nothing, the holders of the content and every row of the holders of the sign a laid plane sources (the form of every record and its Wronskian as the hold books them, the Wronskian into the record's own row, over the write's wall E_s T, the fine form and no whole quanta), and the record's read of those rests (every holder of the content, and for a plane every row of the holders of the sign but its own, plainly), the content the engine steps its record in (ALGEBRA.md, No record reads its own write of the sign)."""
    walls = {
        number: held_write(families, number, board.action).walls
        for number, f in enumerate(families)
        if f.held
    }
    states = [
        empty_state(f, board.shape, walls.get(number, ()), np.int64) for number, f in enumerate(families)
    ]
    for number, own, laid in [(index, slot, pairs), *others]:
        family, lines = families[number], states[number].lines
        span = record_slice(family, own)
        for first in range(span.start, span.stop, family.width):
            for part, (now, before) in enumerate(laid):
                line = lines[first + part]
                lines[first + part] = Record(line.now + now, line.before + before, line.remainder)
    holders = [(number, 0) for number, f in enumerate(families) if f.held and not f.wronskian]
    signs = [
        (number, row)
        for number, f in enumerate(families)
        if f.held
        and f.wronskian
        and any(
            bool(np.asarray(wronskian(states[reader].lines, families[reader].plane)).any())
            for reader, family in enumerate(families)
            if family.quanta and any(taken.family == number for taken in family.reads)
        )
        for row in range(f.records)
    ]
    rows = holders + signs
    time_walls = {row: walls[row[0]][0] for row in rows}
    messages = {row: states[row[0]].lines[record_slice(families[row[0]], row[1]).start] for row in rows}

    def booked(levels: Sequence[np.ndarray]) -> tuple[list[Sourced], list[Sourced]]:
        return booked_sources(
            families,
            states,
            rows,
            holders,
            time_walls,
            messages,
            levels,
            board.wrap,
            board.gamma,
            board.unit,
        )

    fields = held_rests(
        booked,
        [np.zeros(board.shape, dtype=np.int64) for _ in rows],
        board.wrap,
        board.width,
        board.gamma,
        board.unit,
    )
    booked([field.levels for field in fields])  # the rests as found laid into the rows for the read
    return np.asarray(
        content_read(index, families, states, 1, board.wrap, board.gamma, board.unit, slot)[0],
        dtype=np.int64,
    )


def region_of(counts: np.ndarray, well: np.ndarray, centre: Axis, wrap: Wrap) -> np.ndarray:
    """A body's region: the Nodes carrying a quantum of it and one Link around them, where its form may reach next round (the body's width is its own: the iteration widens it a Link a round while its form reaches a quantum there, and narrows it where the form falls below one)."""
    if int(well[centre]) <= 0:
        raise ValueError(
            f"the body about the Node {list(centre)} has no well: its binding level there is {int(well[centre])}"
        )
    return dilated(counts > 0, wrap)


def spread(
    first: np.ndarray,
    centre: Axis,
    board: Board,
    rows: Rows,
    others: np.ndarray,
) -> np.ndarray:
    """The first lay: a body declared on one Node is laid over the cube about its centre, its quanta shared alike, the cube widened one Link at a time until every pace is positive, the content below the Link's zero (no value of the law: the iteration moves it to the fixed point); a body declared on its Nodes is laid as declared."""
    if int(np.count_nonzero(first)) > 1:
        return first.copy()
    quanta = int(first.sum())
    for half in range(1, max(board.shape)):
        idx = np.indices(board.shape).reshape(3, -1).T
        cube = (np.abs(idx - np.array(centre)).max(axis=1) <= half).reshape(board.shape)
        for axis in range(3):  # a cube beyond a face stays on the board
            if not board.wrap[axis]:
                cube &= np.abs(idx[:, axis] - centre[axis]).reshape(board.shape) <= half
        nodes = int(cube.sum())
        counts = np.where(cube, int(division_forward(quanta, nodes, 0)[0]), 0).astype(np.int64)
        counts[centre] += quanta - int(counts.sum())
        try:  # the body alone: the others are spread in their turn
            content = rests(rows, counts, board)
        except RestCollapses:
            continue  # the rows' own rests reach the pace 0 under this cube: the next
        if int(content.max()) < paces.frozen_content(
            board.gamma
        ):  # the Node's pace above 0 (#the-paces)
            return counts
    raise ValueError(
        f"the body of {quanta} quanta about the Node {list(centre)} fits no cube on this board with a positive pace"
    )


def scaled_record(
    board: Board,
    content: np.ndarray,
    centre: Axis,
    own: np.ndarray,
    region: np.ndarray,
    quanta: int,
    centre_count: int,
    keep: np.ndarray,
) -> Standing:
    """The standing record scaled so its form over the region carries the body's quanta: the scale bracketed from the centre's own count (the form there is its count times T) by halving and doubling, a scale too large to stand halved back toward the last that stood, then bisected; the reading closest to the quanta; refused by name when no reading stands."""
    readings: dict[int, Standing] = {}

    def read(scale: int) -> Standing | None:
        if scale not in readings:
            record = standing(board, content, centre, own, scale, region, keep)
            if record is None:
                return None
            readings[scale] = record
        return readings[scale]

    def stands(scale: int) -> Standing:
        record = read(scale)
        if record is None:
            raise ValueError(
                f"the record of the body of {quanta} quanta about the Node {list(centre)} scaled at {scale} "
                "does not stand: the top mode of the read in this content is no one rotation across the region "
                "within the roundings of a step, or its centre's level never returns (the generator is Rule3)"
            )
        return record

    low = max(1, division_fixed_point(max(1, centre_count) * board.action))
    while low > 1 and ((found := read(low)) is None or found.carried > quanta):
        low = max(1, low // 2)
    high = low
    while (found := read(high)) is not None and found.carried < quanta:
        low, high = high, 2 * high
        while read(high) is None and high > low + 1:
            high = (low + high) // 2
    stands(low), stands(high)
    while high - low > 1:
        middle = (low + high) // 2
        if stands(middle).carried < quanta:
            low = middle
        else:
            high = middle
    return readings[min(readings, key=lambda found: (abs(readings[found].carried - quanta), found))]


def body_fixed_point(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    rows: Rows,
    others: Others,
    centre: Axis,
    quanta: int,
    first: np.ndarray,
    sense: int = 0,
) -> tuple[np.ndarray, Standing, np.ndarray, np.ndarray, Pairs]:
    """The body is the joint fixed point of its record and its content: from a first lay of its quanta the count's rest, the seed of the first pass alone (the other bodies' counts among it), the body's region from its well, its standing record seeded with the well's shape and scaled until its weighted share over the region carries its quanta, the record laid as the engine lays it (its level pair over the board as declared outside the other bodies' regions, `own_board`; with a sense its second pair the record a quarter period on, `rotating`, so that the holder of the sign rests inside the iteration and not after it), then the engine's own start on that lay (`start_content`: every held row at the rest its form and Wronskian return, the fine form over the write's wall as the hold books it, the other bodies' laid records among the sources), the content the record stands in next, and the counts the record's share in quanta at that content over the region; repeated until the content returns itself by the start's own rule (`returned`: the fixed point, or an earlier content one unit per division act composed at most, a rounding tie; the acts composed in the content are the record's scale, one, and per held row the family's declaration reads into its content, the content holders and the holders of the sign where a sense is laid, the acts the engine's own `held_rests` composes for that row, its rest's and its booking's, `ACTS_OF_A_HELD_ROW`, so 1 + 2 x 2 = 5 for matter reading the binding and gravity and 1 + 2 x 3 = 7 for a charged plane reading the charge too, counted from the family's reads at the call; a return further off a cycle, refused by name, the law's own answer at this count and sense and no defect) and the counts return within the rounding at every Node, each round taking the half step from the counts toward the share (the deep well overshoots under the whole step); returns the counts over the region, the record standing in the content returned, the region, the content and the laid level pairs, all of one round; refused by name as a cloud (the rotation not above the band's top) or a collapse (a pace not positive). The seed is the count and the fixed point is the form's and the content's together."""
    counts = first.copy()
    seen: dict[bytes, int] = {}
    name = f"the lay and the rest of the body of {quanta} quanta about the Node {list(centre)}"
    read_rows = [  # the held rows the family's declaration reads into its content at this lay
        r
        for r in families[index].reads
        if not families[r.family].rotation and (sense or not families[r.family].wronskian)
    ]
    acts = 1 + ACTS_OF_A_HELD_ROW * len(
        read_rows
    )  # the record's scale, then every row's rest and booking
    content = rests(rows, others[0] + counts, board)  # the seed, the first pass alone
    keep = own_board(board, others[0])
    round_number = 0
    while True:
        round_number += 1
        record, pairs, found = one_pass(
            board, families, index, slot, others, centre, quanta, counts, content, keep, sense
        )
        region = region_of(counts, content, centre, board.wrap)
        a, level = record.clock
        zero = np.zeros(board.shape, dtype=np.int64)
        total = sum((share_of(board, found, now, before) for now, before in pairs), zero)
        laid = np.where(region, read_quanta(total, board.pair[1], board.action), 0)
        agreed = bool(np.all(within(laid - counts, np.maximum(laid, counts))))
        print(
            f"GAMEBOARD the body about {list(centre)}, round {round_number}: the content at the centre "
            f"{int(content[centre])} -> {int(found[centre])}, the count {int(counts[centre])} -> {int(laid[centre])} "
            f"of {int(laid.sum())}, the clock [{a}, {level}] = {a / level:.4f}",
            file=sys.stderr,
            flush=True,
        )
        if returned([found], [content], seen, name, acts) and agreed:
            return laid, record, region, found, pairs
        counts = (counts + laid) // 2  # the half step: the deep well overshoots under the whole step
        content = found


def one_pass(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    others: Others,
    centre: Axis,
    quanta: int,
    counts: np.ndarray,
    content: np.ndarray,
    keep: np.ndarray,
    sense: int,
) -> tuple[Standing, Pairs, np.ndarray]:
    """One pass of the lay-and-rest map, the act both lays share: refused by name where the content reaches the Link's zero (a collapse, a frozen clock); the body's region from its counts, its standing record in the content scaled to carry its quanta (`scaled_record`), refused by name as a cloud where its rotation is not above the band's top and below 2; the record's level pairs over the board as declared outside the other bodies' regions (with a sense its second pair, `rotating`); and the content the engine's own start returns under that lay (`start_content`), the paces the record stands in next."""
    num, den = board.pair
    if int(content.max()) >= paces.frozen_content(board.gamma):
        raise ValueError(
            f"the body of {quanta} quanta about the Node {list(centre)} collapses: its wells reach the pace 0 "
            f"(the content {int(content.max())} at or beyond the Link's zero {paces.frozen_content(board.gamma)}, "
            "where the Node's pace p_0^2 / Gamma rounds to 0, a frozen clock; ALGEBRA.md #the-paces, "
            "The paces compose)"
        )
    region = region_of(counts, content, centre, board.wrap)
    own = np.where(region, content, 0)  # the shape of the seed: the well over the body's region
    record = scaled_record(board, content, centre, own, region, quanta, int(counts[centre]), keep)
    a, level = record.clock
    if not (2 * num * level < a * den < 2 * level * den):
        raise ValueError(
            f"the body of {quanta} quanta about the Node {list(centre)} is a cloud: its standing reading rotates at "
            f"[{a}, {level}], not above the band's top 2 x {num} / {den} and below 2; its quanta are below its "
            "binding row's window of mass (ALGEBRA.md #the-generator)"
        )
    pairs: Pairs = [(np.where(keep, record.now, 0), np.where(keep, record.before, 0))]
    if sense:
        levels = rotating(board, content, record, keep, sense)
        pairs = [(levels[0], levels[1]), (levels[2], levels[3])]
    return record, pairs, start_content(board, families, index, slot, pairs, others[1])


Trajectory = list[
    list[int | None]
]  # per pass: its number, the content's largest change, the record's, the count laid


def unit_fixed_point(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    rows: list[tuple[str, tuple[int, int], int, int]],
    others: Others,
    centre: Axis,
    quanta: int,
    first: np.ndarray,
    sense: int,
    lay: Lay,
) -> tuple[np.ndarray, Standing, np.ndarray, np.ndarray, Pairs, Trajectory]:
    """The lay at the integer fixed point under the body's own paces (the world's `lay` of the kind `fixed_point`, loader/lay.py; HIGHLIGHTS.md, the mathematician's 162 (3) and 168 item 2 (1), the owner's word of 2026-10-02, 17:40): the same map as `body_fixed_point`, one pass the standing record in the content and the engine's own start under that record (`one_pass`), iterated with the design's count the input of every pass and no half step on the counts, until the record's two levels and the content repeat the pass before within the declared `stop` units at every Node (0 the exact repeat), inside the declared `passes`; the record of the last pass is laid in the content it returned to within the stop, so the start the engine lays under the mode file's record gives the paces the record was laid in to the unit declared, the body standing exact by construction and the reads' walk alone remaining; the trajectory, per pass the content's largest change, the record's and the count laid, printed as a GameBoard reading and written to the mode file; where the passes run out the body is refused by name with its trajectory, the law's own answer at this count and no defect. Returns the counts, the record, the region, the content and the laid level pairs of the last pass, and the trajectory."""
    counts = first.copy()
    content = rests(rows, others[0] + counts, board)  # the seed, the first pass alone
    keep = own_board(board, others[0])
    previous: Standing | None = None
    trajectory: Trajectory = []
    for number in range(1, lay.passes + 1):
        record, pairs, found = one_pass(
            board, families, index, slot, others, centre, quanta, counts, content, keep, sense
        )
        region = region_of(counts, content, centre, board.wrap)
        zero = np.zeros(board.shape, dtype=np.int64)
        total = sum((share_of(board, found, now, before) for now, before in pairs), zero)
        laid = np.where(region, read_quanta(total, board.pair[1], board.action), 0)
        moved = int(np.abs(found - content).max())
        turned = None
        if previous is not None:
            turned = max(
                int(np.abs(record.now - previous.now).max()),
                int(np.abs(record.before - previous.before).max()),
            )
        trajectory.append([number, moved, turned, int(laid.sum())])
        a, level = record.clock
        print(
            f"GAMEBOARD the fixed-point lay about {list(centre)}, pass {number}: the content's largest change "
            f"{moved} ({int(content[centre])} -> {int(found[centre])} at the centre), the record's {turned}, the "
            f"count {int(laid.sum())} ({int(laid[centre])} at the centre), the clock [{a}, {level}] = {a / level:.4f}",
            file=sys.stderr,
            flush=True,
        )
        if turned is not None and max(moved, turned) <= lay.stop:
            return laid, record, region, found, pairs, trajectory
        counts, content, previous = laid, found, record
    raise ValueError(
        f"the body of {quanta} quanta about the Node {list(centre)} finds no fixed point to {lay.stop} unit(s) in "
        f"{lay.passes} passes: the trajectory, per pass [the pass, the content's largest change, the record's, the "
        f"count laid], {trajectory} (the world's declared stop and passes, loader/lay.py)"
    )


def declared(
    body: dict[str, Any], shape: Axis, quanta: int | None = None
) -> tuple[np.ndarray, Axis, int]:
    """A body's first lay from the world: its counts at its declared Nodes, its centre (the Node of its largest count) and its quanta: the sum of the declared counts for a new body, one Node carrying its quanta, and for a body laid before (declared on its Nodes) the design's count where it is given (`quanta`, the input of every re-lay: the declared Nodes' counts are the engine's reading of the lay before, the output, and never the input)."""
    counts = np.zeros(shape, dtype=np.int64)
    for entry in cast(list[dict[str, Any]], body["nodes"]):
        node = (int(entry["node"][0]), int(entry["node"][1]), int(entry["node"][2]))
        counts[node] += int(entry["count"])
    centre = tuple(int(index) for index in np.unravel_index(int(counts.argmax()), shape))
    return (
        counts,
        (centre[0], centre[1], centre[2]),
        int(counts.sum()) if quanta is None or int(np.count_nonzero(counts)) <= 1 else int(quanta),
    )


def designed_quanta(world: Path, bodies: int) -> list[int | None]:
    """The design's count of every body of a world file, the input of a re-lay: the folder's design file (`design.json` beside the world, its world's entry `quanta` or the design's own `quanta`, one count for every body of the world), else the mode file beside the world (`<world>.mode.json`, each body's `count`, the first lay's design), else none (the world's declared counts sum to a new body's quanta)."""
    design = world.with_name("design.json")
    if design.exists():
        document = json.loads(design.read_text(encoding="utf-8"))
        worlds = cast(dict[str, Any], document.get("worlds", {}))
        entry = cast(dict[str, Any], worlds.get(world.stem, {}))
        quanta = entry.get("quanta", document.get("quanta"))
        if quanta is not None:
            return [int(quanta)] * bodies
    mode = world.with_suffix(".mode.json")
    if mode.exists():
        laid = cast(list[dict[str, Any]], json.loads(mode.read_text(encoding="utf-8")).get("bodies", []))
        if len(laid) == bodies:
            return [int(body["count"]) for body in laid]
    return [None] * bodies


def body_entry(
    record: Standing,
    board: Board,
    region: np.ndarray,
    body: dict[str, Any],
    quanta: int,
    scale: int,
) -> dict[str, Any]:
    """One body's mode entry: its standing record over the board as declared, its clock pair, amplitude and period."""
    keep = on_the_board(board)
    now, before = np.where(keep, record.now, 0), np.where(keep, record.before, 0)
    entry: dict[str, Any] = {
        "family": body["family"],
        "pair": list(board.pair),
        "count": quanta,
        "seed": scale,
        "carried": record.carried,
        "period": [record.window, 2],
        "amplitude": int(np.abs(now).max()),
        "clock": list(record.clock),
        "profile": now.ravel().tolist(),
        "moving": {"now": now.ravel().tolist(), "before": before.ravel().tolist()},
    }
    return entry


def rotating(
    board: Board, content: np.ndarray, record: Standing, keep: np.ndarray, sense: int
) -> list[np.ndarray]:
    """A body laid with a sense (ALGEBRA.md #the-paces, the sign is the rotation sense): its record and its second level pair, sense x the standing record a quarter period on by Rule3 (the mode's own rotation, the period [window, 2]), both within the kept region and scaled by one factor so the two pairs' plain form at the written moment is the record's own (the start's sources, and so the well, unchanged); returns [re_now, re_before, im_now, im_before]."""
    now, before = record.now.copy(), record.before.copy()
    remainder = np.zeros(board.shape, dtype=np.int64)
    quarter = (
        record.window
    )  # the period is [window, 2]: a quarter period is window div 8, three halvings
    for _ in range(3):
        quarter = int(division_forward(quarter, 2, 0)[0])
    for _ in range(quarter):
        now, before = step(board, content, now, before, remainder), now
    pairs = [np.where(keep, level, 0) for level in (record.now, record.before, now, before)]
    own = int(share_of(board, 0, pairs[0], pairs[1]).sum())
    both = own + int(share_of(board, 0, pairs[2], pairs[3]).sum())
    amplitude = max(int(np.abs(level).max()) for level in pairs)
    scale = division_fixed_point(int(division_forward(amplitude * amplitude * own, both, 0)[0]))
    found = [
        np.asarray(division_forward(level * scale, amplitude, 0)[0], dtype=np.int64) for level in pairs
    ]
    found[2], found[3] = sense * found[2], sense * found[3]
    return found


def read_at_the_start(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    others: Laid,
    region: np.ndarray,
    pairs: Pairs,
) -> tuple[np.ndarray, np.ndarray]:
    """The count the engine's gate reads at the start (ALGEBRA.md #the-count-is-the-records-share; `GameBoard.gate`): the record's share in quanta at the paces of its read at the engine's own start (`start_content`, the one act with `GameBoard.start`: every held row at the rest the laid records' forms and Wronskians return, the other bodies' laid records among them), over the body's region, with the content of that start (the one-step standing check reads it); the body's Nodes are where that share stands in quanta."""
    content = start_content(board, families, index, slot, pairs, others)
    zero = np.zeros(board.shape, dtype=np.int64)
    total = sum((share_of(board, content, now, before) for now, before in pairs), zero)
    return np.where(region, read_quanta(total, board.pair[1], board.action), 0), content


def standing_check(
    board: Board,
    content: np.ndarray,
    pairs: Pairs,
    nodes: np.ndarray,
    centre: Axis,
    clock: tuple[int, int],
) -> None:
    """The generator's one-step standing check of a lay (the advisor's hand, 5944220853 and 5944611538 section 3): the laid world stepped once by Rule3 in its own start's content (`read_at_the_start` builds it as `GameBoard.start` does), the rotation (next + before) / now read over the body's Nodes (`nodes`, the Nodes where its share stands in quanta) on every level pair of the lay alike, a real record's one and a plane's re and im; a lay standing in its content reads one rotation within the rounding 1 / |now| per act composed at every Node (`rotation_spread`, `ROUNDINGS_OF_A_STEP`), and a lay reading a spread beyond it is no mode of the step in the well the engine lays and is refused by name, printing the centre's rotation, the median read and the mode file's clock."""
    for part, (now, before) in enumerate(pairs):
        nxt = step(board, content, now, before, np.zeros(board.shape, dtype=np.int64))
        median, read, worst = rotation_spread(now, before, nxt, nodes)
        at_centre = (
            Fraction(int(nxt[centre]) + int(before[centre]), int(now[centre])) if now[centre] else None
        )
        print(
            f"GAMEBOARD the lay about {list(centre)}, level pair {part}: stepped once in its start's content the "
            f"rotation (next + before) / now reads {float(median):.4f} (the median over {read} Nodes), at the centre "
            f"{None if at_centre is None else float(at_centre):.4f}, the largest departure {float(worst):.2f} of the "
            f"rounding 1 / |now|; the mode file's clock [{clock[0]}, {clock[1]}] = {clock[0] / clock[1]:.4f}",
            file=sys.stderr,
            flush=True,
        )
        if worst > ROUNDINGS_OF_A_STEP:
            raise ValueError(
                f"the lay of the body about the Node {list(centre)} does not stand in its own start: stepped once, "
                f"its level pair {part} rotates at {float(median):.4f} in the median over {read} Nodes and at the "
                f"centre at {None if at_centre is None else float(at_centre):.4f}, a Node departing {float(worst):.2f} "
                f"roundings 1 / |now| where at most {ROUNDINGS_OF_A_STEP}, one per act composed, is a standing record's (the mode file's "
                f"clock [{clock[0]}, {clock[1]}]; ALGEBRA.md #the-generator)"
            )


def turned(doubled: int, unit: int, steps: int) -> list[int]:
    """Rule3's rotation act (ALGEBRA.md #the-four-acts (b)) from the level `unit` and the level `doubled` div 2 after it: a_next = (doubled x a_now + r) div unit - a_before with the remainder kept, `steps` turns; the levels unit x cos(n theta) at 2 unit cos theta = doubled."""
    levels, carry = [unit, int(division_forward(doubled, 2, 0)[0])], 0
    for _ in range(steps - 1):
        nxt, carry = rule3(NO_READ, NO_READ, doubled, unit, levels[-1], levels[-2], carry)
        levels.append(int(nxt))
    return levels


def half_turn(halves: int, unit: int) -> list[int]:
    """The cosines of a half turn in `halves` x 2 steps at the unit, unit x cos(n pi / (2 halves)) for n from 0 through 2 halves, by the rotation act: its doubled cosine is the largest integer at which the rotation from the unit reaches 0 or below within `halves` turns (bisection on the integers, the first zero of the cosine at the quarter turn), no root and no table."""
    lower, upper = 0, 2 * unit
    while upper - lower > 1:
        middle = int(division_forward(lower + upper, 2, 0)[0])
        if min(turned(middle, unit, halves)) <= 0:
            lower = middle
        else:
            upper = middle
    return turned(lower, unit, 2 * halves)


def cosine_at(turns: list[int], index: int) -> int:
    """The cosine at a step of the full turn from a half turn's cosines, cos(2 pi - a) = cos a."""
    whole = 2 * (len(turns) - 1)
    index %= whole
    return turns[whole - index] if index > len(turns) - 1 else turns[index]


def envelope(extent: int, top: tuple[int, int], edge: int, unit: int) -> list[int]:
    """A raised cosine along one axis at the unit: the unit over the flat top [first, last], (unit + unit cos(pi j / edge)) div 2 at j Nodes beyond either end up to the half-width `edge`, 0 further; the unit at every Node where the edge is 0 within the top and 0 beyond it."""
    taper = half_turn(edge, unit) if edge else []
    found = []
    for at in range(extent):
        away = max(top[0] - at, at - top[1], 0)
        if away == 0:
            found.append(unit)
        elif away <= edge:
            found.append(int(division_forward(unit + taper[2 * away], 2, 0)[0]))
        else:
            found.append(0)
    return found


def message_levels(
    board: Board, message: dict[str, Any], beyond: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """The message's two levels (ALGEBRA.md #the-generator, the message lay): now_i = b e_i cos(k x_i + phi) and before_i = b e_i cos(k x_i + phi + omega), the wave one interval earlier, k = pi p / q per Link along its axis (`wave`, p below 0 the packet toward the axis's lower side) with a wave number per axis across the beam (`transverse`, 0 without the key; k x_i then stands for the wave vector's product with the Node's coordinates), phi = 2 pi r / s its phase (`phase`, 0 without the key), b the amplitude, e_i the envelope (the product of the three axes' raised cosines, `top` and `edge`), cos omega the vacuum's band, the mean over the three axes of cos k_a, sin omega the fixed point of the division act; every cosine by the rotation act at a unit derived from the width, the turn cut into the least steps that hold every fraction (a multiple of 2 x 2 q on each axis and of s); 0 beyond the board."""
    along, (turns, halves) = AXES.index(str(message["along"])), message["wave"]
    turned, whole_turn = message.get("phase", [0, 1])
    sideways = {
        AXES.index(str(name)): (int(r), int(s)) for name, (r, s) in message.get("transverse", {}).items()
    }
    numbers = [
        (int(turns), int(halves)) if axis == along else sideways.get(axis, (0, 1)) for axis in range(3)
    ]
    amplitude = int(message["amplitude"])
    unit = division_fixed_point(int(division_forward(board.width, amplitude, 0)[0]))
    steps = lcm(*(2 * 2 * q for _p, q in numbers), int(whole_turn))
    quarter = int(division_forward(steps, 2 * 2, 0)[0])
    cosines = half_turn(quarter, unit)  # cos(2 pi j / steps) for j from 0 through the half turn
    per_link = [
        int(division_forward(p * steps, 2 * q, 0)[0]) for p, q in numbers
    ]  # k's steps per Link per axis
    shift = int(division_forward(int(turned) * steps, int(whole_turn), 0)[0])  # the phase's steps
    axes = [
        envelope(
            board.shape[axis],
            (int(message["top"][name][0]), int(message["top"][name][1])),
            int(message["edge"][name]),
            unit,
        )
        for axis, name in enumerate(AXES)
    ]
    coordinates = np.indices(board.shape)
    index = sum(per_link[axis] * coordinates[axis] for axis in range(3)) + shift
    wave = np.vectorize(lambda i: cosine_at(cosines, int(i)), otypes=[object])(index)
    quadrature = np.vectorize(lambda i: cosine_at(cosines, int(i) - quarter), otypes=[object])(index)
    cosine = int(division_forward(sum(cosine_at(cosines, per_link[axis]) for axis in range(3)), 3, 0)[0])
    sine = division_fixed_point(unit * unit - cosine * cosine)
    shaped = [
        np.array(levels, dtype=object).reshape([-1 if a == axis else 1 for a in range(3)])
        for axis, levels in enumerate(axes)
    ]
    envelope_here = amplitude * shaped[0] * shaped[1] * shaped[2]
    now = envelope_here * wave * unit
    before = envelope_here * (wave * cosine - quadrature * sine)
    scale = unit * unit * unit * unit * unit
    half = int(division_forward(scale, 2, 0)[0])
    found = []
    for numerator in (now, before):
        levels = np.asarray(rule3(NO_READ, NO_READ, 1, scale, 0, 0, numerator + half)[0])
        found.append(np.where(beyond, 0, levels.astype(np.int64)))
    return found[0], found[1]


def message_entry(
    board: Board, message: dict[str, Any], beyond: np.ndarray, parts: int
) -> dict[str, Any]:
    """One message's mode entry: its family and pair, its amplitude, the count its record reads over the board at the vacuum's paces (its share in quanta, a reading, over every part of the family, the one event laid on each part alike) and its two levels as their nonzero Nodes."""
    now, before = message_levels(board, message, beyond)
    laid = read_quanta(share_of(board, 0, now, before), board.pair[1], board.action)
    return {
        "family": message["family"],
        "pair": list(board.pair),
        "amplitude": int(np.abs(now).max()),
        "count": int(laid.sum()) * parts,
        "moving": {"now": nonzero(now), "before": nonzero(before)},
    }


def nonzero(levels: np.ndarray) -> dict[str, list[int]]:
    """A level over the board as its nonzero Nodes alone, the mode file's sparse form: their flat x-major indexes and their levels (a packet stands on few Nodes of a long board)."""
    flat = levels.ravel()
    at = np.flatnonzero(flat)
    return {"at": at.tolist(), "values": flat[at].tolist()}


def pixel_mode(
    document: dict[str, Any], senses: list[int] | None = None, designed: list[int | None] | None = None
) -> dict[str, Any]:
    """The mode document of a world of bodies and messages: `world_digest`, `bodies`, one entry per measured event in the world's order, each the standing record of the whole body, rotating in the sense `senses` names for it (+1 or -1; 0 or none a real record), laid at the design's count `designed` where given (the input of every re-lay, `designed_quanta`; the declared counts' sum otherwise), and `messages`, one entry per message, its packet laid; the document's bodies are rewritten in place to the fixed point's Nodes and counts (the digest is the rewritten world's)."""
    universe = cast(dict[str, Any], world_files(document)[document["universe"]])
    integers = universe["integers"]
    if "quantum_action" not in integers:
        raise ValueError(
            "the universe file declares no quantum_action T: the count c = D div T needs it"
        )
    pairs = {
        family["name"]: (int(family["pair"][0]), int(family["pair"][1]))
        for family in universe["families"]
    }
    shape = (int(document["shape"][0]), int(document["shape"][1]), int(document["shape"][2]))
    beyond = np.zeros(shape, dtype=bool)
    outside = faces_of(document["faces"], shape) if "faces" in document else ()
    for node in outside:
        beyond[node] = True
    wrap = Wrap(
        *(document["boundary"][axis] == "periodic" for axis in AXES), beyond if outside else None
    )
    gamma = int(document.get("node_clock", integers["node_clock"]))
    bodies = cast(list[dict[str, Any]], document.get("measured", []))
    lay = lay_of(document["lay"], "lay") if "lay" in document else None  # the lay by name
    lays: list[tuple[np.ndarray, Pairs, Axis, int]] = []
    zero = np.zeros(shape, dtype=np.int64)
    for number, body in enumerate(bodies):
        counts, centre, quanta = declared(body, shape, (designed or [None] * len(bodies))[number])
        if bool(counts[beyond].any()):
            raise ValueError(
                f"measured[{number}] declares a Node beyond the board's inner face: nothing stands there"
            )
        board = Board(
            shape,
            wrap,
            gamma,
            int(integers["quantum_action"]),
            pairs[body["family"]],
            int(2 ** int(integers["width"]) - 1),
            int(integers["link_unit"]),
        )
        rows = held_rows(universe, str(body["family"]))
        lays.append((spread(counts, centre, board, rows, zero), [], centre, quanta))
    all_counts = sum((counts for counts, _pairs, _centre, _quanta in lays), zero)
    names = [family.name for family in universe_of(universe)[1]]
    document_messages = cast(list[dict[str, Any]], document.get("messages", []))
    events = [names.index(str(row["family"])) for row in bodies]
    families = with_records(universe_of(universe)[1], [events.count(i) for i in range(len(names))])
    records = []  # each body's record number within its family; a message lays on the first record, 0
    for number, family_index in enumerate(events):
        records.append(min(events[:number].count(family_index), families[family_index].records - 1))
    records += [0] * len(document_messages)
    laid_messages: Laid = []  # every message's record on its family, as the engine lays it
    for number, message in enumerate(document_messages):
        family = str(message["family"])
        board = Board(
            shape,
            wrap,
            gamma,
            int(integers["quantum_action"]),
            pairs[family],
            int(2 ** int(integers["width"]) - 1),
            int(integers["link_unit"]),
        )
        slot = records[len(bodies) + number]
        laid_messages.append((names.index(family), slot, [message_levels(board, message, beyond)]))
    entries: list[dict[str, Any]] = []
    # two passes where there are two bodies or more: the second lays each body in the others' sources
    # as the first laid them (a body not yet laid stands at its first lay, its quanta, not its share);
    # one body's declaration is the engine's reading exactly, several bodies' within the gate's rounding
    for _round in range(2 if len(bodies) > 1 else 1):
        entries = []
        regions: list[np.ndarray] = []
        for number, body in enumerate(bodies):
            counts, _pairs, centre, quanta = lays[number]
            index = names.index(str(body["family"]))
            others = list(laid_messages)  # the messages, then the other bodies as laid
            for other, (_counts, laid_pairs, _centre, _quanta) in enumerate(lays):
                if other != number and laid_pairs:
                    others.append(
                        (names.index(str(bodies[other]["family"])), records[other], laid_pairs)
                    )
            board = Board(
                shape,
                wrap,
                gamma,
                int(integers["quantum_action"]),
                pairs[body["family"]],
                int(2 ** int(integers["width"]) - 1),
                int(integers["link_unit"]),
            )
            rows = held_rows(universe, str(body["family"]))
            sense = (senses or [])[number] if number < len(senses or []) else 0
            if sense not in (-1, 0, 1):
                raise ValueError(f"measured[{number}]: a sense is +1 or -1 (0: none), got {sense}")
            if sense and not family_of(universe, str(body["family"])).plane:
                raise ValueError(
                    f"measured[{number}]: a body of {body['family']!r}, a family of dimension one, is laid with "
                    "no sense: a rotating record is a plane, dimension two (ALGEBRA.md #a-familys-declaration)"
                )
            arguments = (board, families, index, records[number], rows, (all_counts - counts, others))
            trajectory: Trajectory = []
            try:
                if lay is not None and lay.kind == FIXED_POINT:
                    laid, record, region, _content, pairs_kept, trajectory = unit_fixed_point(
                        *arguments, centre, quanta, counts, sense, lay
                    )
                else:
                    laid, record, region, _content, pairs_kept = body_fixed_point(
                        *arguments, centre, quanta, counts, sense
                    )
            except RestCollapses as refusal:
                raise ValueError(
                    f"the body of {quanta} quanta about the Node {list(centre)} collapses: its wells reach the "
                    f"pace 0 ({refusal}; the rows reading their own levels, ALGEBRA.md #the-paces, Every row "
                    "reads the content; a frozen clock, The paces compose)"
                ) from refusal
            levels = [level for pair in pairs_kept for level in pair] if sense else []
            try:
                weighted, content = read_at_the_start(
                    board, families, index, records[number], others, region, pairs_kept
                )
            except RestCollapses as refusal:
                raise ValueError(
                    f"the body of {quanta} quanta about the Node {list(centre)} collapses at the start's read: "
                    f"{refusal} (a frozen clock; ALGEBRA.md #the-paces, The paces compose)"
                ) from refusal
            standing_check(board, content, pairs_kept, weighted > 0, centre, record.clock)
            for other, taken in enumerate(regions):
                if bool(np.any(taken & region)):
                    raise ValueError(
                        f"measured[{number}] and measured[{other}] share a Node in their regions: two bodies stand apart or are one body"
                    )
            regions.append(region)
            all_counts = all_counts - counts + laid
            lays[number] = (laid, pairs_kept, centre, quanta)
            entry = body_entry(record, board, region, body, quanta, int(record.clock[1]))
            if trajectory and lay is not None:
                entry["lay"] = {"kind": lay.kind, "stop": lay.stop, "trajectory": trajectory}
            entry["nodes"] = [
                {"node": [int(x), int(y), int(z)], "count": int(weighted[x, y, z])}
                for x, y, z in zip(*np.nonzero(weighted), strict=True)
            ]
            if levels:
                words = ("now", "before", "im_now", "im_before")
                entry["moving"] = {
                    word: level.ravel().tolist() for word, level in zip(words, levels, strict=True)
                }
            entries.append(entry)
    for body, entry in zip(bodies, entries, strict=True):
        body["nodes"] = entry.pop("nodes")
    messages = [
        message_entry(
            Board(
                shape,
                wrap,
                gamma,
                int(integers["quantum_action"]),
                pairs[str(message["family"])],
                int(2 ** int(integers["width"]) - 1),
                int(integers["link_unit"]),
            ),
            message,
            beyond,
            family_of(universe, str(message["family"])).parts,
        )
        for message in cast(list[dict[str, Any]], document.get("messages", []))
    ]
    return {"world_digest": input_digest(document), "bodies": entries, "messages": messages}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="the world file of bodies, rewritten with their Nodes and counts",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="the mode file to write; beside the world as <world>.mode.json when omitted",
    )
    parser.add_argument(
        "--sense",
        type=int,
        nargs="*",
        default=[],
        help="the rotation sense of each body in the world's order, +1 or -1 (0: a real record, neutral)",
    )
    args = parser.parse_args(argv)
    document = json.loads(args.input.read_text(encoding="utf-8"))
    designed = designed_quanta(args.input, len(cast(list[Any], document.get("measured", []))))
    mode = pixel_mode(document, list(args.sense), designed)
    args.input.write_text(json.dumps(document) + "\n", encoding="utf-8")
    out = args.out if args.out is not None else args.input.with_suffix(".mode.json")
    out.write_text(json.dumps(mode, separators=(",", ":")) + "\n", encoding="utf-8")
    for body in mode["bodies"]:
        reading = {key: value for key, value in body.items() if key not in ("profile", "moving")}
        reading["nodes"] = sum(1 for level in body["profile"] if level)
        print(json.dumps(reading))
    for message in mode["messages"]:
        reading = {key: value for key, value in message.items() if key != "moving"}
        reading["nodes"] = sum(1 for level in message["moving"]["now"]["values"] if level)
        print(json.dumps(reading))


if __name__ == "__main__":
    main()
