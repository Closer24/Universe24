"""THE GENERATOR IS RULE3 (ALGEBRA.md #the-primitives, THE GENERATOR IS RULE3, THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD, THE WELL IS THE COUNT AND NO FIELD; the owner's word of 2026-09-28, 15:28 Israel; Cheshbon's algorithm of 15:35, 15:41 and 15:43 and his line of 18:05): the mode file of a world of one-Node bodies, each body's bound record what Rule3 makes of its count at its Node in the engine's own integers and nothing else. For every measured body of one declared Node with a count c: the record is seeded at the Node with a level b_0 at both levels and stepped by Rule3 with the count held (the matter pair as the universe file writes it over Gamma, the content c at the Node and 0 elsewhere, the isotropic rule, the world's own board with its faces walls as in the engine: nothing leaves, Rule3 is reversible) and read whole period by whole period at the Node (a period from one upward return of the level through 0 to the next) until two consecutive periods agree within the rounding with the record's peak at its Node: the reading stands; between passes the purge re-seeds the record from itself within three Links of the Node at the peak phase, 0 elsewhere, integers only, the waste of the reflecting board dropped. The readings over the two periods are the count it carries, D-bar = (SUM D) div (P T) with D = now^2 - next x before at the Node, its period as the pair [window, 2], its amplitude b = max |now|, its clock pair [next + before, now] at the moment of the largest level and its tail, the levels one, two and three Links from the Node along the first axis at that moment; the seed b_0 is bracketed from isqrt(c T) and bisected to the seed whose D-bar is nearest c; the pair must read a bound rotation of the kind (above the band's top, below 2), else the reading is a mode of the board's walls and refused by name; the mode entry is the standing record itself at the peak, `moving` its two levels over the whole board, `profile` the level now, `clock` the pair read, `twist` 0 (a pixel does not twist), on a giver its `wavelength` from the pair in integers (cos k = 3 cos omega_b - 2, the Links per return of that rotation over the world's intervals); the remainders of the standing record are not carried by the file (no key of the loader's) and the record restarts at 0 there. Every arithmetic is Rule3's (`core/rule3`, `core/ports`): no clock pair, no tail and no float enters. Usage: `python tools/pixel_mode.py --input <world.json> [--out <world.mode.json>]`."""

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
    """One interval of Rule3 on the whole board, the loop's own isotropic form: the arrivals per axis the two neighbours' levels (0 beyond an open or closed face, a wall as in the engine, the wrap on a periodic one), the coefficients from the pace Gamma - content at every Node, the division by the wall with the remainder kept at the Node; nothing leaves the board (Rule3 is reversible), a quantum leaves only at a click."""
    arrivals = tuple(
        arrival(now, axis, 1, board.wrap[axis], 0) + arrival(now, axis, -1, board.wrap[axis], 0)
        for axis in range(3)
    )
    reads, self_coefficient, wall = coefficients(
        board.pair[0], board.pair[1], board.gamma, content, ISOTROPIC, True
    )
    nxt, remainder[...] = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    return np.asarray(nxt, dtype=np.int64)


PURGE_LINKS = 3  # the purge keeps the record within three Links of the Node (Cheshbon's line of 18:05)
PERIODS_PER_PASS = 8  # the periods read at the Node before a purge
PASSES = 8  # the purges tried before the record is refused as never standing


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
            if returned and best is not None:
                state[:] = [now, before, remainder]
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


def purged(board: Board, node: Axis, now: np.ndarray, before: np.ndarray) -> list[np.ndarray]:
    """THE PURGE: the record re-seeded from itself at the peak phase, its two levels kept within PURGE_LINKS of the Node (the wrap on a periodic axis) and 0 elsewhere, the remainders 0, integers only: the waste of a reflecting board left behind (Cheshbon's line of 18:05, THE GENERATOR IS RULE3)."""
    keep = np.ones(board.shape, dtype=bool)
    for axis in range(3):
        along = np.arange(board.shape[axis]) - node[axis]
        if board.wrap[axis]:
            along = np.minimum(np.abs(along), board.shape[axis] - np.abs(along))
        shape = [1, 1, 1]
        shape[axis] = board.shape[axis]
        keep &= np.abs(along).reshape(shape) <= PURGE_LINKS
    return [np.where(keep, now, 0), np.where(keep, before, 0), np.zeros(board.shape, dtype=np.int64)]


def standing(board: Board, node: Axis, count: int, seed: int) -> Standing | None:
    """Rule3 from the seed until the reading at the Node stands: the content c held at the Node (0 elsewhere), the levels seeded at b_0, the record read whole period by whole period at the Node until two consecutive periods agree (the same length within one interval, the count carried within the rounding, the amplitude within one level) with the record's peak at its Node; between passes of PERIODS_PER_PASS periods the purge re-seeds the record from itself within PURGE_LINKS of the Node, the waste of the reflecting board dropped; None when no reading stands within PASSES purges (no bound record at this count on this board, or a seed too coarse for the integers)."""
    content = np.zeros(board.shape, dtype=np.int64)
    content[node] = count
    now, before = np.zeros(board.shape, dtype=np.int64), np.zeros(board.shape, dtype=np.int64)
    now[node] = before[node] = seed
    state = [now, before, np.zeros(board.shape, dtype=np.int64)]
    previous = None
    for turn in range(PASSES * PERIODS_PER_PASS):
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
                if (
                    level < 0
                ):  # the pair [next + before, now] with now positive: the sign is not the record's
                    a, level, now_at, before_at = -a, -level, -now_at, -before_at
                tail = tuple(
                    int(now_at[(node[0] + d) % board.shape[0], node[1], node[2]]) for d in (1, 2, 3)
                )
                return Standing(
                    both, window, max(largest, largest_before), (a, level), tail, now_at, before_at
                )
        previous = (length, carried, largest, pair, now_at, before_at)
        if (turn + 1) % PERIODS_PER_PASS == 0:
            state[:] = purged(board, node, now_at, before_at)
            previous = None
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
            f"stand on this board {list(board.shape)}: no two consecutive whole periods of its reading at the Node "
            "agree with the peak at the Node within the purges (no bound record at this count on this board, or "
            "a seed too coarse for the integers; THE GENERATOR IS RULE3)"
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
    a, den = record.clock
    if not (2 * board.pair[0] * den < a * board.pair[1] < 2 * den * board.pair[1]):
        raise ValueError(
            f"measured[{number}]: the standing reading at the Node {list(node)} rotates at [{a}, {den}], not "
            f"above the band's top 2 x {board.pair[0]} / {board.pair[1]} and below 2: a mode of the board's walls, "
            "no bound pixel at this count on this board"
        )
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
