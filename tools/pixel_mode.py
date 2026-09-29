"""THE GENERATOR MAKES A BODY (ALGEBRA.md #the-generator, THE GENERATOR IS RULE3; the model owner's word of 2026-09-28, 22:05 Israel: no body is reduced to one Node, the generator generates a whole body): the mode file of a world of bodies and the bodies themselves. A body is its quanta, M, about a centre; the world declares it with one Node carrying M (a new body) or with its Nodes and their counts (a body laid before, laid anew here). The generator finds the body's fixed point in whole integers: the counts at its Nodes source every held row of the universe file at the row's divisor, the rest of each row by the start's own solver (features/start) is the level every record reads, the body's record is the standing record Rule3 makes in those paces, and the counts are that record's form, D_i = now^2 - next x before div T at every Node of the body's region, until the counts return themselves within the rounding; the counts are laid with the remainder carried from Node to Node (no quantum lost to a Node's rounding) and each round takes the half step from the counts toward the form (the deep well overshoots under the whole step); the body's Nodes are then the Nodes carrying a quantum, its region those Nodes and a Link around them (widened a Link a round while the form reaches a quantum there, narrowed where it falls below one), and the record written is the standing record inside that region and a Link around it, the waste of the reflecting board dropped. Refused by name: a universe without T; a body whose standing rotation is not above its band's top (a cloud, below the window of mass); a body whose iteration drives a pace to zero (a collapse, above the window); two bodies whose regions share a Node. The record is seeded with the shape of the body's own well (the others' wells aside), scaled so that its form over the region carries M quanta, the scale bracketed from the centre's count and bisected as the count's line reads it; every arithmetic on the record is Rule3's (`core/rule3`, `core/ports`), the rests the start's. Usage: `python tools/pixel_mode.py --input <world.json> [--out <world.mode.json>]`: the world is rewritten with every body's Nodes and counts (its digest changes) and the mode file is written beside it."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import isqrt
from pathlib import Path
from typing import Any, cast

import numpy as np

from event_universe.core.ports import arrival
from event_universe.core.rule3 import (
    ISOTROPIC,
    NO_READ,
    coefficients,
    division_forward,
    form_term,
    rule3,
)
from event_universe.features.start import rest
from event_universe.world_files import input_digest, world_files

Axis = tuple[int, int, int]


@dataclass(frozen=True)
class Board:
    """The world's board as Rule3 sees it: its shape, which axes wrap, the universe's Gamma and T, and a record's pair [num, den] as the file writes it."""

    shape: Axis
    wrap: tuple[bool, bool, bool]
    gamma: int
    action: int
    pair: tuple[int, int]


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
        arrival(now, axis, 1, board.wrap[axis], 0) + arrival(now, axis, -1, board.wrap[axis], 0)
        for axis in range(3)
    )
    reads, self_coefficient, wall = coefficients(
        board.pair[0], board.pair[1], board.gamma, content, ISOTROPIC, True
    )
    nxt, remainder[...] = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    return np.asarray(nxt, dtype=np.int64)


PERIODS_PER_PASS = 8  # the periods read at the centre before a purge
PASSES = 8  # the purges tried before the record is refused as never standing
ROUNDS = 4 * 8  # the rounds of the fixed point (counts, rests, record, half step) before a refusal


def share_of(board: Board, content: np.ndarray, now: np.ndarray, before: np.ndarray) -> np.ndarray:
    """The record's form's share at every Node in the current's units, the engine's `count_share` (ALGEBRA.md #the-counts-line; issue #1495 finding 6): 3 den (now^2 + before^2) - num now S_6(before), the form's Node term at the plain wall less the Link term by the read act."""
    num, den = board.pair
    arrivals = tuple(
        arrival(before, axis, 1, board.wrap[axis], 0) + arrival(before, axis, -1, board.wrap[axis], 0)
        for axis in range(3)
    )
    node_term = np.asarray(
        form_term(0, 3 * den, now.astype(np.int64), before.astype(np.int64)), dtype=np.int64
    )
    return node_term - np.asarray(rule3((num * now,) * 3, arrivals, 0, 1, 0, 0, 0)[0], dtype=np.int64)


def share_counts(share: np.ndarray, den: int, action: int) -> np.ndarray:
    """The counts the share lays, the engine's lay: W_c c + r = share + W_c div 2 at every Node with W_c = 3 den T by Rule3's division act (no quantum carried from Node to Node: a hole at the record's edge the line conserves, ALGEBRA.md #the-counts-line)."""
    wall = 3 * den * action
    return np.asarray(rule3(NO_READ, NO_READ, 1, wall, 0, 0, share + wall // 2)[0], dtype=np.int64)


def period_reading(
    board: Board, content: np.ndarray, node: Axis, state: list[np.ndarray]
) -> tuple[int, int, tuple[int, int], np.ndarray, np.ndarray, np.ndarray] | None:
    """One whole period of the record at the centre, from the interval its level returns upward through 0 to the next such return: the period's length, the largest |now| at the centre and the pair [next + before, now] with the three levels over the board at that moment; None when the level never returns within 4 Gamma intervals (a cloud, no record). `state` is [now, before, remainder], stepped in place."""
    now, before, remainder = state
    sign = 1 if now[node] > 0 else -1 if now[node] < 0 else 0
    length, largest, best, returned = 0, -1, None, False
    for _ in range(4 * board.gamma + 8):
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


def agree(first: int, second: int) -> bool:
    """Two readings of a count within the rounding of its amplitude, |a - b| <= 2 isqrt(a) + 1, as integer squares."""
    off = abs(first - second)
    return (off - (off & 1)) ** 2 <= 4 * max(first, second)


def dilated(mask: np.ndarray, wrap: tuple[bool, bool, bool]) -> np.ndarray:
    """The mask and its six-neighbour surroundings (the wrap on a periodic axis, nothing beyond a face)."""
    grown = mask.copy()
    for axis in range(3):
        for sense in (1, -1):
            grown |= np.asarray(arrival(mask.astype(np.int64), axis, sense, wrap[axis], 0)) > 0
    return grown


def purged(keep: np.ndarray, now: np.ndarray, before: np.ndarray) -> list[np.ndarray]:
    """THE PURGE: the record re-seeded from itself at the peak phase within `keep`, 0 elsewhere, the remainders 0: the waste of a reflecting board left behind (Cheshbon's line of 2026-09-28, 18:05 Israel)."""
    return [np.where(keep, now, 0), np.where(keep, before, 0), np.zeros(now.shape, dtype=np.int64)]


def top_mode(
    board: Board, content: np.ndarray, keep: np.ndarray, seed: np.ndarray, unit: int
) -> np.ndarray:
    """THE ITERATION of the generator (ALGEBRA.md #the-generator (b)): Rule3's read act with the before-coefficient 0, a <- (SUM_a R_a arr_a + S a) div w within the body's region and 0 outside it, then the division act to the amplitude unit (the level times the unit over its largest size): the power iteration of the symmetric form's top mode, the body's bound mode; the stop is the first repeat of the integer vector, exact, no tolerance."""
    a = np.where(keep, seed, 0).astype(np.int64)
    seen: set[bytes] = set()
    for _ in range(PASSES * PERIODS_PER_PASS * board.gamma):
        arrivals = tuple(
            arrival(a, axis, 1, board.wrap[axis], 0) + arrival(a, axis, -1, board.wrap[axis], 0)
            for axis in range(3)
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
        key = a.tobytes()
        if key in seen:
            return a
        seen.add(key)
    return a


def standing(
    board: Board, content: np.ndarray, node: Axis, shape_seed: np.ndarray, scale: int, region: np.ndarray
) -> Standing | None:
    """Rule3 from the seed until the reading at the centre stands: the record seeded at both levels with the body's shape scaled to `scale` at the centre, read whole period by whole period at the centre until two consecutive periods agree (the same length within one interval, the amplitude within its rounding, the form over the region within its rounding); between passes the purge keeps the record within the region and a Link around it; None when no reading stands within PASSES purges."""
    keep = dilated(region, board.wrap)
    now = top_mode(board, content, keep, shape_seed, scale)
    if not now[node]:
        return None
    state = [now.copy(), now.copy(), np.zeros(board.shape, dtype=np.int64)]
    previous: tuple[int, int, int, tuple[int, int], np.ndarray, np.ndarray, np.ndarray] | None = None
    for turn in range(PASSES * PERIODS_PER_PASS):
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
                and abs(largest - largest_before) <= isqrt(max(largest, largest_before)) + 1
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
        if (turn + 1) % PERIODS_PER_PASS == 0:
            state[:] = purged(keep, now_at, before_at)
            previous = None
    return None


def held_rows(universe: dict[str, Any]) -> list[tuple[str, tuple[int, int], int]]:
    """The universe's held content rows, (name, pair, divisor): the rows every record of the world reads at the weight 1 (THE FAMILIES FROM THE RULE); a sign row is read as 0 here, a body of the generator carries no charge."""
    rows = []
    for family in universe["families"]:
        held = family.get("held")
        if isinstance(held, dict) and held.get("count") == "content":
            rows.append(
                (
                    str(family["name"]),
                    (int(family["pair"][0]), int(family["pair"][1])),
                    int(held["divisor"]),
                )
            )
    if not rows:
        raise ValueError(
            "the universe file holds no content row: a body needs a held row to bind in (ALGEBRA.md #the-generator)"
        )
    return rows


def rests(
    rows: list[tuple[str, tuple[int, int], int]], counts: np.ndarray, wrap: tuple[bool, bool, bool]
) -> tuple[np.ndarray, np.ndarray]:
    """Every held row's rest at these counts by the start's own solver, summed into the content every record reads, and the first (the binding) row's rest alone, the body's own well."""
    total = np.zeros(counts.shape, dtype=np.int64)
    binding: np.ndarray | None = None
    for _name, pair, divisor in rows:
        field = np.asarray(rest(counts, pair, wrap, divisor).levels, dtype=np.int64)
        total += field
        binding = field if binding is None else binding
    return total, cast(np.ndarray, binding)


def region_of(
    counts: np.ndarray, well: np.ndarray, centre: Axis, wrap: tuple[bool, bool, bool]
) -> np.ndarray:
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
    """THE FIRST LAY: a body declared on one Node is laid over the cube about its centre, its quanta shared alike, the cube widened one Link at a time until every pace is positive (no value of the law: the iteration moves it to the fixed point); a body declared on its Nodes is laid as declared."""
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
            rows, counts, board.wrap
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
        for attempt in range(scale, scale + 8):
            if attempt not in readings:
                record = standing(board, content, centre, own, attempt, region)
                if record is not None:
                    readings[attempt] = record
            if attempt in readings:
                return readings[attempt]
        return None

    def stands(scale: int) -> Standing:
        record = read(scale)
        if record is None:
            raise ValueError(
                f"the record of the body of {quanta} quanta about the Node {list(centre)} scaled at {scale} to "
                f"{scale + 7} does not stand: no two consecutive whole periods of its reading at its centre agree "
                "within the purges (THE GENERATOR IS RULE3)"
            )
        return record

    low = max(1, isqrt(max(1, centre_count) * board.action))
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
) -> tuple[np.ndarray, Standing, np.ndarray]:
    """THE BODY IS THE FIXED POINT OF ITS BINDING ROW: from a first lay of its quanta, the rests of every held row at all counts (the other bodies' counts standing), the body's region from its own well, its standing record seeded with the well's shape and scaled until the form over the region carries its quanta, the counts the form; repeated until the counts return within the rounding at every Node; refused by name as a cloud (the rotation not above the band's top) or a collapse (a pace not positive)."""
    counts = first.copy()
    num, den = board.pair
    for _round in range(ROUNDS):
        content, _well = rests(rows, others + counts, board.wrap)
        _content, well = rests(
            rows, counts, board.wrap
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
        laid = np.where(
            region,
            share_counts(
                share_of(board, content, record.now, record.before), board.pair[1], board.action
            ),
            0,
        )
        off = np.abs(laid - counts)
        if bool(np.all((off - (off & 1)) ** 2 <= 4 * np.maximum(laid, counts))):
            return laid, record, region
        counts = (counts + laid) // 2  # the half step: the deep well overshoots under the whole step
    raise ValueError(
        f"the body of {quanta} quanta about the Node {list(centre)} finds no fixed point in {ROUNDS} rounds: its counts and its form do not return each other within the rounding (THE GENERATOR IS RULE3)"
    )


def wavelength(clock: tuple[int, int], links: int) -> int:
    """The given light's wavelength from the giver's clock pair in integers: cos k = 3 cos omega_b - 2, so 2 cos k = (3 a - 4 den) div den for the pair [a, den]; the rotation x_(n+1) = 2 cos k x_n - x_(n-1) run over `links` Links by Rule3's division with the remainder carried, its Links per period the Links per upward return of x through 0, rounded to the whole Link; the Links themselves when it never returns."""
    a, den = clock
    numerator = 3 * a - 4 * den
    x_before, x_now, carry, returns = 0, den, 0, 0
    for _ in range(links):
        x_next, carry = division_forward(numerator * x_now - den * x_before, den, carry)
        if x_next > 0 and x_now <= 0:
            returns += 1
        x_before, x_now = x_now, x_next
    return int(division_forward(2 * links + returns, 2 * returns, 0)[0]) if returns else links


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
    world: dict[str, Any],
    quanta: int,
    scale: int,
) -> dict[str, Any]:
    """One body's mode entry: its standing record within its region and a Link around it, its clock pair, amplitude and period, its twist 0 (a body of the generator does not twist), and on a giver its `wavelength` from the pair."""
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
        "twist": 0,
        "profile": now.ravel().tolist(),
        "moving": {"now": now.ravel().tolist(), "before": before.ravel().tolist()},
    }
    if "emitter" in body or body.get("q"):
        entry["wavelength"] = wavelength(record.clock, int(world.get("ticks", 1)))
    return entry


def pixel_mode(document: dict[str, Any]) -> dict[str, Any]:
    """The mode document of a world of bodies: `world_digest` and `bodies`, one entry per measured event in the world's order, each the standing record of the whole body; the document's bodies are rewritten in place to the fixed point's Nodes and counts (the digest is the rewritten world's)."""
    universe = cast(dict[str, Any], world_files(document)[document["universe"]])
    integers = universe["integers"]
    if "quantum_action" not in integers:
        raise ValueError(
            "the universe file declares no quantum_action T: the count c = D div T needs it"
        )
    rows = held_rows(universe)
    pairs = {
        family["name"]: (int(family["pair"][0]), int(family["pair"][1]))
        for family in universe["families"]
    }
    shape = (int(document["shape"][0]), int(document["shape"][1]), int(document["shape"][2]))
    wrap = tuple(document["boundary"][axis] == "periodic" for axis in "xyz")
    gamma = int(document.get("node_clock", integers["node_clock"]))
    bodies = cast(list[dict[str, Any]], document.get("measured", []))
    lays = []
    for body in bodies:
        counts, centre, quanta = declared(body, shape)
        board = Board(
            shape,
            (wrap[0], wrap[1], wrap[2]),
            gamma,
            int(integers["quantum_action"]),
            pairs[body["family"]],
        )
        lays.append(
            (spread(counts, centre, board, rows, np.zeros(shape, dtype=np.int64)), centre, quanta)
        )
    all_counts = sum((counts for counts, _centre, _quanta in lays), np.zeros(shape, dtype=np.int64))
    entries, regions = [], []
    for number, body in enumerate(bodies):
        counts, centre, quanta = lays[number]
        board = Board(
            shape,
            (wrap[0], wrap[1], wrap[2]),
            gamma,
            int(integers["quantum_action"]),
            pairs[body["family"]],
        )
        laid, record, region = body_fixed_point(board, rows, all_counts - counts, centre, quanta, counts)
        for other, taken in enumerate(regions):
            if bool(np.any(taken & region)):
                raise ValueError(
                    f"measured[{number}] and measured[{other}] share a Node in their regions: two bodies stand apart or are one body"
                )
        regions.append(region)
        all_counts = all_counts - counts + laid
        body["nodes"] = [
            {"node": [int(x), int(y), int(z)], "count": int(laid[x, y, z])}
            for x, y, z in zip(*np.nonzero(laid), strict=True)
        ]
        entries.append(body_entry(record, board, region, body, document, quanta, int(record.clock[1])))
    return {"world_digest": input_digest(document), "bodies": entries}


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
    args = parser.parse_args(argv)
    document = json.loads(args.input.read_text(encoding="utf-8"))
    mode = pixel_mode(document)
    args.input.write_text(json.dumps(document) + "\n", encoding="utf-8")
    out = args.out if args.out is not None else args.input.with_suffix(".mode.json")
    out.write_text(json.dumps(mode) + "\n", encoding="utf-8")
    for body in mode["bodies"]:
        reading = {key: value for key, value in body.items() if key not in ("profile", "moving")}
        reading["nodes"] = sum(1 for level in body["profile"] if level)
        print(json.dumps(reading))


if __name__ == "__main__":
    main()
