"""The generator makes a body (ALGEBRA.md #the-generator, the generator is Rule3; the model owner's word of 2026-09-28, 22:05 Israel: no body is reduced to one Node, the generator generates a whole body): the mode file of a world of bodies and the bodies themselves. A body is its quanta, M, about a centre; the world declares it with one Node carrying M (a new body) or with its Nodes and their counts (a body laid before, laid anew here). The generator finds the body's fixed point in whole integers: the counts at its Nodes source every held row of the universe file at the row's divisor, the rest of each row by the start (features/start: the division act iterated from nothing until the levels repeat) is the level every record reads, the body's record is the standing record Rule3 makes in those paces, and the counts are that record's form, D_i = now^2 - next x before div T at every Node of the body's region, until the counts return themselves within the rounding; the counts are laid with the remainder carried from Node to Node (no quantum lost to a Node's rounding) and each round takes the half step from the counts toward the form (the deep well overshoots under the whole step); the body's Nodes are then the Nodes carrying a quantum, its region those Nodes and a Link around them (widened a Link a round while the form reaches a quantum there, narrowed where it falls below one), and the record written is the standing record inside that region and a Link around it, the waste of the reflecting board dropped. Refused by name: a universe without T; a body whose standing rotation is not above its band's top (a cloud, below the window of mass); a body whose iteration drives a pace to zero (a collapse, above the window); two bodies whose regions share a Node. The record is seeded with the shape of the body's own well (the others' wells aside), scaled so that its form over the region carries M quanta, the scale bracketed from the centre's count and bisected as the count's line reads it; every arithmetic on the record is Rule3's (`core/rule3`, `core/ports`), the rests the start's. The generator also lays every message of the world (ALGEBRA.md #the-generator, the message lay): a packet of a family of quanta and no body, its `now` the wave along its axis under its envelope and its `before` the same wave one interval earlier, every cosine by Rule3's rotation act and every root by the fixed point of the division act, its numbers the world's keys. Usage: `python tools/pixel_mode.py --input <world.json> [--out <world.mode.json>]`: the world is rewritten with every body's Nodes and counts (its digest changes) and the mode file is written beside it."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import (
    ISOTROPIC,
    NO_READ,
    coefficients,
    division_fixed_point,
    division_forward,
    rule3,
)
from event_universe.features.start import rest
from event_universe.lay import share
from event_universe.loader.derived import BY_PLAIN, family_rules
from event_universe.loader.faces import faces_of
from event_universe.loader.keys import AXES
from event_universe.node import Record
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


@dataclass(frozen=True)
class Standing:
    """A body's standing record over its window: the count its form carries over the region (SUM D div T), the window's length (the period is [window, 2]), the amplitude b, the clock pair [next + before, now] at the largest level at the centre, and the two levels over the board at that moment with the next level after it."""

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
    """One interval of Rule3 on the whole board, the loop's own isotropic form: the arrivals per axis the two neighbours' levels (0 beyond a face, the wrap on a periodic one), the coefficients from the paces at every Node (core.rule3, ALGEBRA.md #the-paces), the division by the wall with the remainder kept at the Node."""
    arrivals = tuple(
        arrival(now, axis, 1, board.wrap, 0) + arrival(now, axis, -1, board.wrap, 0) for axis in range(3)
    )
    reads, self_coefficient, wall = coefficients(
        board.pair[0], board.pair[1], board.gamma, content, ISOTROPIC, True
    )
    nxt, remainder[...] = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    return np.asarray(nxt, dtype=np.int64)


def share_of(board: Board, content: np.ndarray | int, now: np.ndarray, before: np.ndarray) -> np.ndarray:
    """The record's weighted share at every Node in the current's units, the engine's own `node.share` at the paces of the content (ALGEBRA.md #the-counts-line, the lay and the wall): the conserved form's Node term over the Link's pace squared less the plain Link term."""
    record = Record(now.astype(np.int64), before.astype(np.int64), np.zeros(board.shape, dtype=np.int64))
    return np.asarray(share(board.pair, record, board.wrap, board.gamma, content), dtype=np.int64)


def share_counts(share: np.ndarray, den: int, action: int) -> np.ndarray:
    """The counts the share lays, the engine's lay: W_c c + r = share + W_c div 2 at every Node with W_c = 3 den T by Rule3's division act (no quantum carried from Node to Node: a hole at the record's edge the line conserves, ALGEBRA.md #the-counts-line)."""
    wall = 3 * den * action
    return np.asarray(rule3(NO_READ, NO_READ, 1, wall, 0, 0, share + wall // 2)[0], dtype=np.int64)


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


def dilated(mask: np.ndarray, wrap: Wrap) -> np.ndarray:
    """The mask and its six-neighbour surroundings (the wrap on a periodic axis, nothing beyond a face)."""
    grown = mask.copy()
    for axis in range(3):
        for sense in (1, -1):
            grown |= np.asarray(arrival(mask.astype(np.int64), axis, sense, wrap, 0)) > 0
    return grown


def purged(keep: np.ndarray, now: np.ndarray, before: np.ndarray) -> list[np.ndarray]:
    """The purge: the record re-seeded from itself at the peak phase within `keep`, 0 elsewhere, the remainders 0: the waste of a reflecting board left behind (Cheshbon's line of 2026-09-28, 18:05 Israel)."""
    return [np.where(keep, now, 0), np.where(keep, before, 0), np.zeros(now.shape, dtype=np.int64)]


def top_mode(
    board: Board, content: np.ndarray, keep: np.ndarray, seed: np.ndarray, unit: int
) -> np.ndarray:
    """The iteration of the generator (ALGEBRA.md #the-generator (b)): Rule3's read act with the before-coefficient 0, a <- (SUM_a R_a arr_a + S a) div w within the body's region and 0 outside it, then the division act to the amplitude unit (the level times the unit over its largest size): the power iteration of the symmetric form's top mode, the body's bound mode; the stop is the first repeat of the integer vector, exact, no tolerance."""
    a = np.where(keep, seed, 0).astype(np.int64)
    seen: set[bytes] = set()
    while True:
        arrivals = tuple(
            arrival(a, axis, 1, board.wrap, 0) + arrival(a, axis, -1, board.wrap, 0) for axis in range(3)
        )
        reads, self_coefficient, wall = coefficients(
            board.pair[0], board.pair[1], board.gamma, content, ISOTROPIC, True
        )
        total = (
            reads[0] * arrivals[0]
            + reads[1] * arrivals[1]
            + reads[2] * arrivals[2]
            + self_coefficient * a
        )
        total = np.where(keep, np.asarray(division_forward(total, wall, 0)[0]), 0).astype(np.int64)
        largest = int(np.abs(total).max())
        if largest == 0:
            return a
        a = np.asarray(division_forward(total * unit, largest, 0)[0], dtype=np.int64)
        key = digest(a)
        if key in seen:
            return a
        seen.add(key)


def standing(
    board: Board, content: np.ndarray, node: Axis, shape_seed: np.ndarray, scale: int, region: np.ndarray
) -> Standing | None:
    """Rule3 from the seed until the reading at the centre stands: the record seeded at both levels with the body's shape scaled to `scale` at the centre, read whole period by whole period at the centre until two consecutive periods agree (the same length within one interval, the amplitude within its rounding, the form over the region within its rounding); the purge keeps the record within the region and a Link around it after a span of periods, the span doubled at every purge; None when a purged record repeats, the fixed point's own stop."""
    keep = dilated(region, board.wrap)
    now = top_mode(board, content, keep, shape_seed, scale)
    if not now[node]:
        return None
    state = [now.copy(), now.copy(), np.zeros(board.shape, dtype=np.int64)]
    previous: tuple[int, int, int, tuple[int, int], np.ndarray, np.ndarray, np.ndarray] | None = None
    purges: set[bytes] = set()
    read, span = 0, 1
    while True:
        reading = period_reading(board, content, node, state)
        if reading is None:
            return None
        length, largest, pair, now_at, before_at, next_at = reading
        carried = int(
            np.where(
                region,
                share_counts(share_of(board, content, now_at, before_at), board.pair[1], board.action),
                0,
            ).sum()
        )
        if previous is not None:
            length_before, carried_before, largest_before, pair_before, now_b, before_b, next_b = (
                previous
            )
            if (
                abs(length - length_before) <= 1
                and agree(carried, carried_before)
                and abs(largest - largest_before)
                <= division_fixed_point(max(largest, largest_before)) + 1
            ):
                a, level = pair if largest >= largest_before else pair_before
                now_at, before_at, next_at = (
                    (now_at, before_at, next_at)
                    if largest >= largest_before
                    else (now_b, before_b, next_b)
                )
                if level < 0:
                    a, level, now_at, before_at, next_at = -a, -level, -now_at, -before_at, -next_at
                return Standing(
                    max(carried, carried_before),
                    length + length_before,
                    max(largest, largest_before),
                    (a, level),
                    now_at,
                    before_at,
                    next_at,
                )
        previous = (length, carried, largest, pair, now_at, before_at, next_at)
        read += 1
        if read == span:  # the purge after a span of periods, the span doubled at each purge
            state[:] = purged(keep, now_at, before_at)
            key = digest(state[0], state[1])
            if key in purges:
                return None
            purges.add(key)
            previous, read, span = None, 0, 2 * span


def held_rows(universe: dict[str, Any], family: str) -> list[tuple[str, tuple[int, int], int]]:
    """The held rows a body's family reads by plain, (name, pair, divisor), as the loader derives the reads (ALGEBRA.md #the-paces: every holder of the content): the rows whose levels are the content its record reads; a read by sign is 0 here (a body of the generator is laid real unless a sense is asked, and its sense stands at 0 before the engine's first act)."""
    rows = []
    for row in universe["families"]:
        held = row.get("held")
        word = str(held["count"]) if isinstance(held, dict) else None
        divisor = int(held["divisor"]) if isinstance(held, dict) else None
        rows.append((str(row["name"]), (int(row["pair"][0]), int(row["pair"][1])), word, divisor))
    names = [row[0] for row in rows]
    reads = family_rules(rows)[names.index(family)].reads
    found = [
        (rows[read.family][0], rows[read.family][1], int(rows[read.family][3] or 1))
        for read in reads
        if read.by == BY_PLAIN
    ]
    if not found:
        raise ValueError(
            f"the family {family!r} reads no held row of the content by plain: a body needs a row to bind in "
            "(ALGEBRA.md #the-generator)"
        )
    return found


def rests(
    rows: list[tuple[str, tuple[int, int], int]],
    counts: np.ndarray,
    wrap: Wrap,
    width: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Every held row's level at these sources as the engine's start holds it, summed into the content every record reads: a row without a gap at its rest by the start (features/start: the division act iterated from nothing until it repeats), a row with a gap laid, the sources through its divisor; and the first (the binding) row's level alone, the body's own well."""
    total = np.zeros(counts.shape, dtype=np.int64)
    binding: np.ndarray | None = None
    for _name, pair, divisor in rows:
        if pair[0] != pair[1]:
            field = np.asarray(division_forward(counts, divisor, 0)[0], dtype=np.int64)
        else:
            wall = 3 * pair[1]  # the plain rule's wall, the one the row steps by
            field = np.asarray(rest(counts, pair, wrap, divisor, width, wall).levels, dtype=np.int64)
        total += field
        binding = field if binding is None else binding
    return total, cast(np.ndarray, binding)


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
    rows: list[tuple[str, tuple[int, int], int]],
    others: np.ndarray,
) -> np.ndarray:
    """The first lay: a body declared on one Node is laid over the cube about its centre, its quanta shared alike, the cube widened one Link at a time until every pace is positive (no value of the law: the iteration moves it to the fixed point); a body declared on its Nodes is laid as declared."""
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
        content, _well = rests(
            rows, counts, board.wrap, board.width
        )  # the body alone: the others are spread in their turn
        if (
            2 * int(content.max()) < board.gamma
        ):  # the Link's pace Gamma - 2 c above 0 (ALGEBRA.md #the-paces)
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
) -> Standing:
    """The standing record scaled so its form over the region carries the body's quanta: the scale bracketed from the centre's own count (the form there is its count times T) by halving and doubling, a scale too large to stand halved back toward the last that stood, then bisected; the reading closest to the quanta; refused by name when no reading stands."""
    readings: dict[int, Standing] = {}

    def read(scale: int) -> Standing | None:
        if scale not in readings:
            record = standing(board, content, centre, own, scale, region)
            if record is None:
                return None
            readings[scale] = record
        return readings[scale]

    def stands(scale: int) -> Standing:
        record = read(scale)
        if record is None:
            raise ValueError(
                f"the record of the body of {quanta} quanta about the Node {list(centre)} scaled at {scale} "
                "does not stand: a purged record repeats before two consecutive whole periods of its reading "
                "at its centre agree (the generator is Rule3)"
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
    rows: list[tuple[str, tuple[int, int], int]],
    others: np.ndarray,
    centre: Axis,
    quanta: int,
    first: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, Standing, np.ndarray, np.ndarray]:
    """The body is the fixed point of its binding row: from a first lay of its quanta, the rests of every held row at all sources (the other bodies' standing), the body's region from its own well, its standing record seeded with the well's shape and scaled until its weighted share over the region carries its quanta, the sources the record's plain form (the vacuum's share, the form that sources the fields); repeated until the sources return within the rounding at every Node; returns the sources, the counts the engine lays (the weighted share at the paces), the record, the region and the content; refused by name as a cloud (the rotation not above the band's top) or a collapse (a pace not positive)."""
    counts = first.copy()
    num, den = board.pair
    rounds: set[bytes] = set()
    while (key := counts.tobytes()) not in rounds:
        rounds.add(key)
        content, _well = rests(rows, others + counts, board.wrap, board.width)
        _content, well = rests(
            rows, counts, board.wrap, board.width
        )  # the region from the body's own well, the others' wells aside
        if 2 * int(content.max()) >= board.gamma:
            raise ValueError(
                f"the body of {quanta} quanta about the Node {list(centre)} collapses: its wells reach the pace 0 "
                f"(the content {int(content.max())} at or beyond Gamma div 2 = {board.gamma // 2}, the Link's pace "
                f"Gamma - 2 c; ALGEBRA.md #the-paces); its quanta are above its "
                "binding row's window of mass (ALGEBRA.md #the-generator)"
            )
        region = region_of(counts, well, centre, board.wrap)
        own = np.where(region, well, 0)  # the shape of the seed: the body's own well over its region
        record = scaled_record(board, content, centre, own, region, quanta, int(counts[centre]))
        a, level = record.clock
        if not (2 * num * level < a * den < 2 * level * den):
            raise ValueError(
                f"the body of {quanta} quanta about the Node {list(centre)} is a cloud: its standing reading rotates at "
                f"[{a}, {level}], not above the band's top 2 x {num} / {den} and below 2; its quanta are below its "
                "binding row's window of mass (ALGEBRA.md #the-generator)"
            )
        # the form that sources the fields (the vacuum's share at the written moment, as the engine's
        # start reads it) and the count the engine lays at its first act (the weighted share at the
        # paces, from the levels one step on)
        laid = np.where(
            region, share_counts(share_of(board, 0, record.now, record.before), den, board.action), 0
        )
        if bool(np.all(within(laid - counts, np.maximum(laid, counts)))):
            # the content the engine's start holds under these sources, and the count it lays there
            content, _well = rests(rows, others + laid, board.wrap, board.width)
            remainder = np.zeros(board.shape, dtype=np.int64)
            nxt = step(board, content, record.now.copy(), record.before.copy(), remainder)
            weighted = np.where(
                region, share_counts(share_of(board, content, nxt, record.now), den, board.action), 0
            )
            return laid, weighted, record, region, content
        counts = (counts + laid) // 2  # the half step: the deep well overshoots under the whole step
    raise ValueError(
        f"the body of {quanta} quanta about the Node {list(centre)} finds no fixed point: its counts repeat before they and its form return each other within the rounding (the generator is Rule3)"
    )


def declared(body: dict[str, Any], shape: Axis) -> tuple[np.ndarray, Axis, int]:
    """A body's first lay from the world: its counts at its declared Nodes, its centre (the Node of its largest count) and its quanta (the sum)."""
    counts = np.zeros(shape, dtype=np.int64)
    for entry in cast(list[dict[str, Any]], body["nodes"]):
        node = (int(entry["node"][0]), int(entry["node"][1]), int(entry["node"][2]))
        counts[node] += int(entry["count"])
    centre = tuple(int(index) for index in np.unravel_index(int(counts.argmax()), shape))
    return counts, (centre[0], centre[1], centre[2]), int(counts.sum())


def body_entry(
    record: Standing,
    board: Board,
    region: np.ndarray,
    body: dict[str, Any],
    quanta: int,
    scale: int,
) -> dict[str, Any]:
    """One body's mode entry: its standing record within its region and a Link around it, its clock pair, amplitude and period."""
    keep = dilated(region, board.wrap)
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
) -> tuple[list[np.ndarray], np.ndarray, np.ndarray]:
    """A body laid with a sense (ALGEBRA.md #the-paces, the sign is the rotation sense): its record and its second level pair, sense x the standing record a quarter period on by Rule3 (the mode's own rotation, the period [window, 2]), both within the kept region and scaled by one factor so the two pairs' plain form at the written moment is the record's own (the start's sources, and so the well, unchanged); returns [re_now, re_before, im_now, im_before], the counts the engine lays from both at its first act and the form that sources the fields (the vacuum's share)."""
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
    total, plain = np.zeros(board.shape, dtype=np.int64), np.zeros(board.shape, dtype=np.int64)
    for first in (0, 2):
        level_now, level_before = found[first].copy(), found[first + 1].copy()
        rest_remainder = np.zeros(board.shape, dtype=np.int64)
        nxt = step(board, content, level_now, level_before, rest_remainder)
        total = total + share_of(board, content, nxt, level_now)
        plain = plain + share_of(board, 0, level_now, level_before)
    den, action = board.pair[1], board.action
    return found, share_counts(total, den, action), share_counts(plain, den, action)


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
    """The message's two levels (ALGEBRA.md #the-generator, the message lay): now_i = b e_i cos(k x_i) and before_i = b e_i cos(k x_i + omega), the wave one interval earlier, k = pi p / q per Link along its axis (`wave`), x_i the Node's coordinate on that axis, b the amplitude, e_i the envelope (the product of the three axes' raised cosines, `top` and `edge`), cos omega the vacuum's band, the mean over the three axes of cos k_a (k = 0 across), sin omega the fixed point of the division act; every cosine by the rotation act at a unit derived from the width; 0 beyond the board."""
    along, (turns, halves) = AXES.index(str(message["along"])), message["wave"]
    amplitude = int(message["amplitude"])
    unit = division_fixed_point(int(division_forward(board.width, amplitude, 0)[0]))
    cosines = half_turn(int(halves), unit)
    axes = [
        envelope(
            board.shape[axis],
            (int(message["top"][name][0]), int(message["top"][name][1])),
            int(message["edge"][name]),
            unit,
        )
        for axis, name in enumerate(AXES)
    ]
    coordinates = np.indices(board.shape)[along]
    wave = np.vectorize(lambda x: cosine_at(cosines, 2 * int(turns) * int(x)), otypes=[object])
    quadrature = np.vectorize(
        lambda x: cosine_at(cosines, int(halves) - 2 * int(turns) * int(x)), otypes=[object]
    )
    cosine = sum(cosines[2 * int(turns)] if axis == along else unit for axis in range(3))
    cosine = int(division_forward(cosine, 3, 0)[0])
    sine = division_fixed_point(unit * unit - cosine * cosine)
    shaped = [
        np.array(levels, dtype=object).reshape([-1 if a == axis else 1 for a in range(3)])
        for axis, levels in enumerate(axes)
    ]
    envelope_here = amplitude * shaped[0] * shaped[1] * shaped[2]
    now = envelope_here * wave(coordinates) * unit
    before = envelope_here * (wave(coordinates) * cosine - quadrature(coordinates) * sine)
    scale = unit * unit * unit * unit * unit
    half = int(division_forward(scale, 2, 0)[0])
    found = []
    for numerator in (now, before):
        levels = np.asarray(rule3(NO_READ, NO_READ, 1, scale, 0, 0, numerator + half)[0])
        found.append(np.where(beyond, 0, levels.astype(np.int64)))
    return found[0], found[1]


def message_entry(board: Board, message: dict[str, Any], beyond: np.ndarray) -> dict[str, Any]:
    """One message's mode entry: its family and pair, its amplitude, the count its record lays over the board at the vacuum's paces (a reading) and its two levels."""
    now, before = message_levels(board, message, beyond)
    laid = share_counts(share_of(board, 0, now, before), board.pair[1], board.action)
    return {
        "family": message["family"],
        "pair": list(board.pair),
        "amplitude": int(np.abs(now).max()),
        "count": int(laid.sum()),
        "moving": {"now": now.ravel().tolist(), "before": before.ravel().tolist()},
    }


def pixel_mode(document: dict[str, Any], senses: list[int] | None = None) -> dict[str, Any]:
    """The mode document of a world of bodies and messages: `world_digest`, `bodies`, one entry per measured event in the world's order, each the standing record of the whole body, rotating in the sense `senses` names for it (+1 or -1; 0 or none a real record), and `messages`, one entry per message, its packet laid; the document's bodies are rewritten in place to the fixed point's Nodes and counts (the digest is the rewritten world's)."""
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
    lays = []
    for number, body in enumerate(bodies):
        counts, centre, quanta = declared(body, shape)
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
        )
        rows = held_rows(universe, str(body["family"]))
        lays.append(
            (spread(counts, centre, board, rows, np.zeros(shape, dtype=np.int64)), centre, quanta)
        )
    all_counts = sum((counts for counts, _centre, _quanta in lays), np.zeros(shape, dtype=np.int64))
    entries: list[dict[str, Any]] = []
    # two passes where there are two bodies or more: the second lays each body in the others' sources
    # as the first laid them (a body not yet laid stands at its first lay, its quanta, not its form)
    for _round in range(2 if len(bodies) > 1 else 1):
        entries = []
        regions: list[np.ndarray] = []
        for number, body in enumerate(bodies):
            counts, centre, quanta = lays[number]
            board = Board(
                shape,
                wrap,
                gamma,
                int(integers["quantum_action"]),
                pairs[body["family"]],
                int(2 ** int(integers["width"]) - 1),
            )
            rows = held_rows(universe, str(body["family"]))
            laid, weighted, record, region, content = body_fixed_point(
                board, rows, all_counts - counts, centre, quanta, counts
            )
            sense = (senses or [])[number] if number < len(senses or []) else 0
            if sense not in (-1, 0, 1):
                raise ValueError(f"measured[{number}]: a sense is +1 or -1 (0: none), got {sense}")
            levels: list[np.ndarray] = []
            if sense:
                levels, turned, plain = rotating(
                    board, content, record, dilated(region, board.wrap), sense
                )
                weighted, laid = np.where(region, turned, 0), np.where(region, plain, 0)
            for other, taken in enumerate(regions):
                if bool(np.any(taken & region)):
                    raise ValueError(
                        f"measured[{number}] and measured[{other}] share a Node in their regions: two bodies stand apart or are one body"
                    )
            regions.append(region)
            all_counts = all_counts - counts + laid
            lays[number] = (laid, centre, quanta)
            entry = body_entry(record, board, region, body, quanta, int(record.clock[1]))
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
            ),
            message,
            beyond,
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
    mode = pixel_mode(document, list(args.sense))
    args.input.write_text(json.dumps(document) + "\n", encoding="utf-8")
    out = args.out if args.out is not None else args.input.with_suffix(".mode.json")
    out.write_text(json.dumps(mode) + "\n", encoding="utf-8")
    for body in mode["bodies"]:
        reading = {key: value for key, value in body.items() if key not in ("profile", "moving")}
        reading["nodes"] = sum(1 for level in body["profile"] if level)
        print(json.dumps(reading))
    for message in mode["messages"]:
        reading = {key: value for key, value in message.items() if key != "moving"}
        reading["nodes"] = sum(1 for level in message["moving"]["now"] if level)
        print(json.dumps(reading))


if __name__ == "__main__":
    main()
