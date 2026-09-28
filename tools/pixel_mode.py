"""THE GENERATOR IS RULE3 (ALGEBRA.md #the-primitives, THE GENERATOR IS RULE3, THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD; the owner's word of 2026-09-28, 15:28 Israel; Cheshbon's algorithm of 15:35, 15:41 and 15:43): the mode file of a world of one-Node bodies, each body's bound record what Rule3 makes of its count at its Node in the engine's own integers and nothing else. For every measured body of one declared Node with a count c: the record is seeded at the Node with a level b_0 at both levels and stepped by Rule3 with the count's well held (the matter pair as the universe file writes it over Gamma, the content c at the Node and 0 elsewhere, the isotropic rule, the world's own faces: what reaches an open face leaves) until the unbound part has left (twice the Links to the farthest open face, the group velocity under half a Link per interval) and then over two periods of the standing record (a period between two returns of the record's level at the Node to the same sign); the readings of the standing record over that window are the count it carries, D-bar = (SUM D) div (P T) with D = now^2 - next x before, its period P as the pair [window, 2], its amplitude b = max |now|, its clock pair [next + before, now] at the moment of the largest level and its tail, the levels one, two and three Links from the Node along the first axis at that moment; the seed b_0 is scanned upward from 1 until the record carries the count or more, and the seed whose D-bar is nearest c is the body's; the mode entry is the standing record itself at that moment, `moving` its two levels over the whole board, `profile` the level now, `clock` the pair read, `twist` 0 (a pixel does not twist), on a giver its `wavelength` from the pair in integers (cos k = 3 cos omega_b - 2, the Links per period of that rotation over the world's intervals); the remainders of the standing record are not carried by the file (no key of the loader's) and the record restarts at 0 there. Every arithmetic is Rule3's (`core/rule3`, `core/ports`): no clock pair, no tail and no float enters. Usage: `python tools/pixel_mode.py --input <world.json> [--out <world.mode.json>]`."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import isqrt
from pathlib import Path
from typing import Any, cast

import numpy as np

from event_universe.core.ports import arrival
from event_universe.core.rule3 import ISOTROPIC, coefficients, division_forward, rule3
from event_universe.world_files import input_digest, world_files

Axis = tuple[int, int, int]


@dataclass(frozen=True)
class Board:
    """The world's board as Rule3 sees it: its shape, which axes wrap, and the universe's Gamma, T and the matter pair [m, Gamma] as the file writes it."""

    shape: Axis
    wrap: tuple[bool, bool, bool]
    gamma: int
    action: int
    pair: tuple[int, int]
    depth: int = (
        1  # the face slab: what reaches an open face leaves (ALGEBRA.md #the-ladder, THE FACE SLAB)
    )


@dataclass(frozen=True)
class Standing:
    """The standing record's readings over the window: the count it carries (D-bar), the window's length (the period is [window, 2]), the amplitude b, the clock pair [next + before, now] at the largest level, the tail along the first axis, and the two levels over the board at that moment."""

    carried: int
    window: int
    amplitude: int
    clock: tuple[int, int]
    tail: tuple[int, ...]
    now: np.ndarray
    before: np.ndarray


def step(
    board: Board, content: np.ndarray, now: np.ndarray, before: np.ndarray, remainder: np.ndarray
) -> np.ndarray:
    """One interval of Rule3 on the whole board, the loop's own isotropic form: the arrivals per axis the two neighbours' levels (0 beyond an open or closed face, the wrap on a periodic one), the coefficients from the pace Gamma - content at every Node, the division by the wall with the remainder kept at the Node."""
    arrivals = tuple(
        arrival(now, axis, 1, board.wrap[axis], 0) + arrival(now, axis, -1, board.wrap[axis], 0)
        for axis in range(3)
    )
    reads, self_coefficient, wall = coefficients(
        board.pair[0], board.pair[1], board.gamma, content, ISOTROPIC, True
    )
    nxt, remainder[...] = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    found = np.asarray(nxt, dtype=np.int64)
    for axis in range(3):  # the face slab is the receiver: a level reaching it leaves the board
        if not board.wrap[axis] and board.shape[axis] > 1:
            view = np.moveaxis(found, axis, 0)
            view[: board.depth] = 0
            view[board.shape[axis] - board.depth :] = 0
            np.moveaxis(remainder, axis, 0)[: board.depth] = 0
            np.moveaxis(remainder, axis, 0)[board.shape[axis] - board.depth :] = 0
    return found


def leaving_time(board: Board, node: Axis) -> int:
    """The intervals the unbound part needs to leave through the faces: twice the Links from the Node to the farthest open face (the group velocity is under half a Link per interval), twice the board's longest extent where no face is open (nothing leaves; the record is read as it stands)."""
    farthest = (
        max(
            max(node[axis], board.shape[axis] - 1 - node[axis])
            for axis in range(3)
            if not board.wrap[axis]
        )
        if not all(board.wrap)
        else max(board.shape)
    )
    return 2 * farthest


def period_reading(
    board: Board, content: np.ndarray, node: Axis, state: list[np.ndarray]
) -> tuple[int, int, int, tuple[int, int], np.ndarray, np.ndarray] | None:
    """One whole period of the record at the Node, from the interval its level returns upward through 0 to the next such return: the period's length, D summed over it, the largest |now| and the pair [next + before, now] with both levels over the board at that moment; None when the level never returns within 4 Gamma intervals (a cloud, no record). `state` is [now, before, remainder], stepped in place."""
    now, before, remainder = state
    sign = 1 if now[node] > 0 else -1 if now[node] < 0 else 0
    length, summed, largest, best, returned = 0, 0, -1, None, False
    for _ in range(4 * board.gamma + 8):
        nxt = step(board, content, now, before, remainder)
        here = int(now[node])
        if here > 0 and sign <= 0:
            if returned:
                state[:] = [now, before, remainder]
                assert best is not None
                return (length, summed, largest, best[0], best[1], best[2])
            returned = True
        if here:
            sign = 1 if here > 0 else -1
        if returned:
            length += 1
            summed += here * here - int(nxt[node]) * int(before[node])
            if abs(here) > largest:
                largest, best = (
                    abs(here),
                    ((int(nxt[node]) + int(before[node]), here), now.copy(), before.copy()),
                )
        now, before = nxt, now
    return None


def agree(first: int, second: int) -> bool:
    """Two readings of a count within the rounding of its amplitude, |a - b| <= 2 isqrt(a) + 1, as integer squares."""
    off = abs(first - second)
    return (off - (off & 1)) ** 2 <= 4 * max(first, second)


def standing(board: Board, node: Axis, count: int, seed: int) -> Standing | None:
    """Rule3 from the seed until the record stands, then the readings over two periods: the count held at the Node (the content c there, 0 elsewhere), the levels now and before seeded at b_0, the record stepped through the leaving time, then read period by period until two consecutive whole periods agree (the same length within one interval, the count carried within the rounding, the amplitude within one level): the record stands, and those two periods are its window; None when no two periods agree within the bound (twice the leaving time in periods, at least sixteen)."""
    content = np.zeros(board.shape, dtype=np.int64)
    content[node] = count
    now, before = np.zeros(board.shape, dtype=np.int64), np.zeros(board.shape, dtype=np.int64)
    now[node] = before[node] = seed
    state = [now, before, np.zeros(board.shape, dtype=np.int64)]
    for _ in range(leaving_time(board, node)):
        state[0], state[1] = step(board, content, state[0], state[1], state[2]), state[0]
    previous = None
    for _ in range(max(16, 2 * leaving_time(board, node))):
        reading = period_reading(board, content, node, state)
        if reading is None:
            return None
        length, summed, largest, pair, now_at, before_at = reading
        carried = int(division_forward(summed, length * board.action, 0)[0])
        if previous is not None:
            length_before, carried_before, largest_before, pair_before, now_before, before_before = (
                previous
            )
            bound = largest == int(
                np.max(np.abs(now_at))
            )  # the record's peak is at its Node: bound there
            if (
                bound
                and abs(length - length_before) <= 1
                and agree(carried, carried_before)
                and abs(largest - largest_before) <= 1
            ):
                window = length + length_before
                both = int(
                    division_forward(carried * length + carried_before * length_before, window, 0)[0]
                )
                a, level = pair if largest >= largest_before else pair_before
                now_at, before_at = (
                    (now_at, before_at) if largest >= largest_before else (now_before, before_before)
                )
                if level < 0:  # the pair [next + before, now] with now positive
                    a, level = -a, -level
                scale = division_forward(int(np.max(np.abs(now_at))) + level - 1, level, 0)[0]
                a, level = a * scale, level * scale  # den at least the amplitude
                tail = tuple(
                    int(now_at[(node[0] + d) % board.shape[0], node[1], node[2]]) for d in (1, 2, 3)
                )
                return Standing(
                    both, window, max(largest, largest_before), (a, level), tail, now_at, before_at
                )
        previous = (length, carried, largest, pair, now_at, before_at)
    return None


def bound_record(board: Board, node: Axis, count: int) -> tuple[int, Standing]:
    """The seed b_0 bracketed and then bisected: from isqrt(c T) doubled or halved until the standing record carries the count on both sides, then the seed between whose carried count is nearest the declared count (D-bar rises with the seed as its square, in whole quanta); a seed whose record does not stand (the integers too coarse at a small seed, or no bound record) is stepped past up to eight times in a row and then refused by name."""
    readings: dict[int, Standing] = {}

    def read(seed: int) -> Standing:
        for attempt in range(seed, seed + 8):
            if attempt not in readings:
                record = standing(board, node, count, attempt)
                if record is not None:
                    readings[attempt] = record
            if attempt in readings:
                return readings[attempt]
        raise ValueError(
            f"the record of the count {count} at the Node {list(node)} seeded at {seed} to {seed + 7} does not "
            f"stand on this board {list(board.shape)}: no two consecutive whole periods of its level at the Node "
            "agree with the peak at the Node (a well too shallow for its board, a board too small for its "
            "record, or no bound record at this count; THE GENERATOR IS RULE3)"
        )

    low = high = max(1, isqrt(count * board.action))
    while read(low).carried > count and low > 1:
        low = max(1, low // 2)
    while read(high).carried < count:
        high *= 2
    while high - low > 1:
        middle = (low + high) // 2
        if read(middle).carried < count:
            low = middle
        else:
            high = middle
    seed = min(readings, key=lambda found: (abs(readings[found].carried - count), found))
    return seed, readings[seed]


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


def pixel_entry(
    number: int, body: dict[str, Any], world: dict[str, Any], board: Board
) -> dict[str, Any]:
    """One body's entry: the standing record Rule3 makes of its count at its Node and the readings of it; a body that is not one Node is refused by name."""
    nodes = cast(list[dict[str, Any]], body.get("nodes"))
    if not isinstance(nodes, list) or len(nodes) != 1:
        raise ValueError(
            f"measured[{number}] is not a body of one declared Node: this tool writes the pixel's record alone"
        )
    node = (int(nodes[0]["node"][0]), int(nodes[0]["node"][1]), int(nodes[0]["node"][2]))
    count = int(nodes[0]["count"])
    seed, record = bound_record(board, node, count)
    entry: dict[str, Any] = {
        "family": body["family"],
        "pair": list(board.pair),
        "count": count,
        "seed": seed,
        "carried": record.carried,
        "period": [record.window, 2],
        "amplitude": record.amplitude,
        "clock": list(record.clock),
        "tail": list(record.tail),
        "twist": 0,
        "profile": record.now.ravel().tolist(),
        "moving": {"now": record.now.ravel().tolist(), "before": record.before.ravel().tolist()},
    }
    if "emitter" in body or body.get("q"):
        entry["wavelength"] = wavelength(record.clock, int(world.get("ticks", 1)))
    return entry


def pixel_mode(document: dict[str, Any]) -> dict[str, Any]:
    """The mode document of a world of one-Node bodies: `world_digest` and `bodies`, one entry per measured event in the world's order, each the standing record of its count."""
    universe = cast(dict[str, Any], world_files(document)[document["universe"]])
    pairs = {
        family["name"]: (int(family["pair"][0]), int(family["pair"][1]))
        for family in universe["families"]
    }
    integers = universe["integers"]
    if "quantum_action" not in integers:
        raise ValueError(
            "the universe file declares no quantum_action T: the count c = D div T needs it"
        )
    shape = tuple(int(side) for side in document["shape"])
    wrap = tuple(document["boundary"][axis] == "periodic" for axis in "xyz")
    bodies = []
    for number, body in enumerate(document.get("measured", [])):
        board = Board(
            (shape[0], shape[1], shape[2]),
            (wrap[0], wrap[1], wrap[2]),
            int(document.get("node_clock", integers["node_clock"])),
            int(integers["quantum_action"]),
            pairs[body["family"]],
            int(document.get("face_depth", 1)),
        )
        bodies.append(pixel_entry(number, body, document, board))
    return {"world_digest": input_digest(document), "bodies": bodies}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="the world file of one-Node bodies")
    parser.add_argument(
        "--out",
        type=Path,
        help="the mode file to write; beside the world as <world>.mode.json when omitted",
    )
    args = parser.parse_args(argv)
    document = json.loads(args.input.read_text(encoding="utf-8"))
    mode = pixel_mode(document)
    out = args.out if args.out is not None else args.input.with_suffix(".mode.json")
    out.write_text(json.dumps(mode) + "\n", encoding="utf-8")
    for body in mode["bodies"]:
        reading = {key: value for key, value in body.items() if key not in ("profile", "moving")}
        reading["support"] = sum(1 for level in body["profile"] if level)
        print(json.dumps(reading))


if __name__ == "__main__":
    main()
