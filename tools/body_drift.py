"""The drift of the bodies' share centroids, a GameBoard reading labelled so and no measurement (docs/ENGINE.md #6-how-to-run-a-world; ALGEBRA.md #the-rows-against-nature (f), the like-or-unlike look of the rotation round): a world of one or two bodies on a chain is loaded as tools/run_inputs.py loads it and stepped by the engine's own step over the window; at the window's ends the share of the bodies' family at every Node in the current's units at the paces of its read (`GameBoard.share_of`) is read over each body's half of the chain (a single body's over the whole chain), the halves split midway between the two bodies' declared Nodes, and its centroid along the chain is formed as an exact fraction at the file's coordinates; the output per world carries each body's centroid at the window's ends and its drift, and for two bodies the separation (the second body's centroid less the first's) at the ends with its change. With an expectation file (the like-or-unlike look's, examples/events/like_or_unlike/expectation.json) the worlds named like and unlike are read against the background it names, the uncharged pair's change plus the image force of the faces read on the single bodies (the charged singles' separation change less the uncharged singles'): a = like's change less the background, b = unlike's change less the background, and the blind's three lines (a above 0, b below 0, |a + b| within a third of (a - b) / 2) are each answered yes or no, with the mutual effect's own sign beside them, like further apart than unlike, (a - b) / 2 above 0, which no background enters. The tool holds no number of the law and writes nothing to the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/body_drift.py [--intervals N] [--expectation <expectation>.json] <world>.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.game_board import GameBoard
from event_universe.world_files import load_world

LABEL = "GAMEBOARD"


def pair(value: Fraction | None) -> list[int] | None:
    """A fraction as [numerator, denominator] for the output, None where there is none."""
    return None if value is None else [value.numerator, value.denominator]


def centroid(density: np.ndarray, first: int, last: int, offset: int) -> Fraction | None:
    """The centroid along the chain of a density over the Nodes from `first` through `last` (the file's coordinates, `offset` the layers grown before the origin), an exact fraction, the density summed over the cross-section at each x (a chain's one Node; a box's plane, the body round's standing world), None where the density sums to 0."""
    total = Fraction(0)
    weighted = Fraction(0)
    for x in range(first, last + 1):
        value = int(density[x + offset].sum(dtype=object))
        total += value
        weighted += x * value
    return None if total == 0 else weighted / total


def split_of(board: GameBoard) -> int:
    """The chain's split midway between two bodies' declared Nodes, the first Node of the second body's half; the chain's length for a single body, whose half is the whole chain."""
    if len(board.world.bodies) == 1:
        return board.world.shape[0]
    first = max(node[0] for node in board.world.bodies[0].nodes)
    second = min(node[0] for node in board.world.bodies[1].nodes)
    return (first + second + 1) // 2


def centroids(board: GameBoard) -> list[Fraction | None]:
    """The bodies' centroids now: each body's family's share over its half of the chain, the first half from the chain's first Node to the split, the second from the split to the last."""
    split, found = split_of(board), []
    halves = ((0, split - 1), (split, board.world.shape[0] - 1))
    for number, (first, last) in enumerate(halves[: len(board.world.bodies)]):
        density = board.share_of(board.world.bodies[number].family)[0]
        found.append(centroid(density, first, last, board.offset[0]))
    return found


def drift(source: Path | GameBoard, intervals: int | None) -> dict[str, Any]:
    """One world's reading, from its path (loaded here) or from a GameBoard standing at its start: the bodies' centroids at the start and after `intervals` intervals (the world's ticks without it), each body's drift and, for two bodies, the separation's change, exact fractions, labelled GAMEBOARD."""
    name = getattr(source, "name", "GameBoard")  # the file's name, or a board's
    board = source if isinstance(source, GameBoard) else GameBoard(load_world(source))
    if len(board.world.bodies) not in (1, 2):
        raise ValueError(f"{name} declares {len(board.world.bodies)} bodies: the drift reads one or two")
    steps = board.world.ticks if intervals is None else intervals
    start = centroids(board)
    for _ in range(steps):
        board.step()
        if board.ended is not None:
            break
    end = centroids(board)
    bodies = []
    for number, (before, after) in enumerate(zip(start, end, strict=True)):
        row = board.world.bodies[number]
        moved = None if before is None or after is None else after - before
        bodies.append(
            {
                "family": board.families[row.family].name,
                "declared": sorted(node[0] for node in row.nodes),
                "start": pair(before),
                "end": pair(after),
                "drift": pair(moved),
            }
        )
    found = {
        "label": LABEL,
        "input": name,
        "intervals": board.tick,
        "split": split_of(board),
        "bodies": bodies,
    }
    if len(bodies) == 2:
        apart = [None if a is None or b is None else b - a for a, b in (start, end)]
        change = None if apart[0] is None or apart[1] is None else apart[1] - apart[0]
        found["separation"] = {"start": pair(apart[0]), "end": pair(apart[1]), "change": pair(change)}
    return found


def change_of(reading: dict[str, Any]) -> Fraction:
    """A world's separation change as a fraction, a single body's its drift, refused by name where a half read no share."""
    value = reading["separation"]["change"] if "separation" in reading else reading["bodies"][0]["drift"]
    if value is None:
        raise ValueError(f"{reading['input']}: a half of the chain read no share, no centroid stands")
    return Fraction(int(value[0]), int(value[1]))


def compared(expected: dict[str, Any], readings: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """The like and the unlike worlds against the background the blind names: the uncharged pair's separation change plus the image force of the faces read on the single bodies (the charged singles' separation change, the second's drift less the first's, less the uncharged singles'); a and b, their sum (the asymmetry) and their half-difference (the effect's size), and the blind's three lines answered."""
    worlds, named = expected["worlds"], expected["background"]
    pair = change_of(readings[str(named["pair"])])
    charged, uncharged = (
        change_of(readings[str(names[1])]) - change_of(readings[str(names[0])])
        for names in (named["charged_alone"], named["uncharged_alone"])
    )
    like, unlike = (change_of(readings[str(worlds[name])]) for name in ("like", "unlike"))
    a, b = like - (pair + charged - uncharged), unlike - (pair + charged - uncharged)
    half = (a - b) / 2
    return {
        "label": LABEL,
        "uncharged_pair": [pair.numerator, pair.denominator],
        "image_force_of_the_singles": [
            (charged - uncharged).numerator,
            (charged - uncharged).denominator,
        ],
        "a_like_less_background": [a.numerator, a.denominator],
        "b_unlike_less_background": [b.numerator, b.denominator],
        "asymmetry": [(a + b).numerator, (a + b).denominator],
        "half_difference": [half.numerator, half.denominator],
        "like_apart": a > 0,
        "unlike_together": b < 0,
        "same_size": 3 * abs(a + b) <= abs(half),
        "like_further_than_unlike": half > 0,
        "blind": expected["blind"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "worlds", type=Path, nargs="+", help="the world files, each with its mode file beside it"
    )
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals read (the world's ticks)"
    )
    parser.add_argument("--expectation", type=Path, default=None, help="the blind expectation file")
    args = parser.parse_args(argv)
    readings = {path.stem: drift(path, args.intervals) for path in args.worlds}
    found: dict[str, Any] = {"label": LABEL, "worlds": readings}
    if args.expectation is not None:
        expected = json.loads(args.expectation.read_text(encoding="utf-8"))
        found["against_the_blind"] = compared(expected, readings)
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
