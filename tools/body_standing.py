"""The standing world's three reads, GameBoard readings labelled so and no measurement (docs/ENGINE.md #6-how-to-run-a-world; HIGHLIGHTS.md, the mathematician's 167 with the advisor's second hand 5955658812, the body round's standing world): a world of one body is loaded as tools/run_inputs.py loads it and stepped by the engine's own step over the window, and at the body's declared Nodes (where the lay's share stands) three readings are taken from the record and the share, every number an exact fraction of the engine's integers. (1) The drift: the centroid of the body's share along each axis at the window's ends and its change, the centroid tools/body_drift.py reads along a chain, taken here along each axis in turn with the density summed over the other two. (2) The share's deviation over the body, rho_s^2 = SUM over the body's Nodes of (s_n - s_0)^2 / SUM of s_0^2, s the share per Node in the current's units at the paces of the read (`GameBoard.share_of`), s_0 the lay's and s_n the share at the interval n, read at the quarters of the window so that the sqrt(n) law, rho_s(n) / rho_s(n / 4), is read within the run; rho_s itself is the fixed point of the division act on rho_s^2 at the scale of the universe's T, [rho_s T, T], no root. (3) The rotation read in the summed form, cos omega_read = SUM over the body of z_t (z_(t + 1) + z_(t - 1)) / (2 SUM of z_t^2) (167's line; twice it is the clock pair's 2 cos omega), never per Node, at every interval, its least and largest over the intervals where the record's weight 2 SUM z_t^2 is at least half its largest (a real standing record passes through 0 at every Node at once twice a period, where the ratio is the rounding's alone) and the window's accumulated ratio. The tool compares nothing, holds no number of the law and writes nothing to the engine; with an expectation file its blind is printed beside the readings.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/body_standing.py [--intervals N] [--expectation <expectation>.json] <world>.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core.rule3 import division_fixed_point
from event_universe.game_board import GameBoard
from event_universe.loader.keys import AXES
from event_universe.world_files import load_world

LABEL = "GAMEBOARD"


def pair(value: Fraction | None) -> list[int] | None:
    """A fraction as [numerator, denominator] for the output, None where there is none."""
    return None if value is None else [value.numerator, value.denominator]


def rooted(square: Fraction, scale: int) -> list[int]:
    """A fraction's root at a scale as [root x scale, scale] by the fixed point of the division act on the square's numerator times the scale squared over its denominator, the largest integer whose square fits (no root act)."""
    found = division_fixed_point(square.numerator * scale * scale // square.denominator)
    return [found, scale]


def centroids(density: np.ndarray, nodes: np.ndarray) -> list[Fraction | None]:
    """The centroid of a density over the Nodes `nodes` along each axis, the density summed over the other two axes at each coordinate, exact fractions; None where the density sums to 0."""
    weights = np.where(nodes, density, 0).astype(object)
    total = int(weights.sum())
    if total == 0:
        return [None] * len(AXES)
    grids = np.indices(density.shape)
    return [Fraction(int((weights * grids[axis]).sum()), total) for axis in range(len(AXES))]


def deviation(share: np.ndarray, laid: np.ndarray, nodes: np.ndarray) -> Fraction:
    """The share's deviation squared over the body's Nodes, SUM (s_n - s_0)^2 over SUM s_0^2, exact."""
    moved = np.where(nodes, share.astype(object) - laid.astype(object), 0)
    return Fraction(
        int((moved * moved).sum()), int((np.where(nodes, laid, 0).astype(object) ** 2).sum())
    )


def rotation(
    before: np.ndarray, now: np.ndarray, after: np.ndarray, nodes: np.ndarray
) -> tuple[int, int]:
    """The rotation of the body's record read in the summed form over its Nodes, as the pair (SUM z_t (z_(t + 1) + z_(t - 1)), 2 SUM z_t^2), whose ratio is cos omega_read (167's line as written; twice it is the rotation 2 cos omega the mode file's clock pair reads, z_(t + 1) + z_(t - 1) = 2 cos omega z_t on a standing record), exact integers; a real standing record passes through 0 at every Node at once twice a period, where the pair's second number is small and the ratio is the rounding's, so the reader reads the ratio where the record's weight 2 SUM z_t^2 is at least half its largest over the window, and the window's accumulated ratio, both sums over the intervals too."""
    z = np.where(nodes, now, 0).astype(object)
    return int((z * (after.astype(object) + before.astype(object))).sum()), 2 * int((z * z).sum())


def rotations_read(found: list[tuple[int, int, int]]) -> dict[str, Any]:
    """The rotation readings over the window, (numerator, weight, tick) per interval: cos omega_read's least and largest over the intervals whose weight is at least half the largest weight (the record away from its zero crossings) with their ticks and the spread, the count of those intervals, the window's accumulated ratio SUM numerators / SUM weights, and the first interval's 2 cos omega."""
    heaviest = max(weight for _n, weight, _t in found)
    strong = [(Fraction(n, w), t) for n, w, t in found if 2 * w >= heaviest]
    least, largest = min(strong), max(strong)
    return {
        "cos_omega_least": {"reading": pair(least[0]), "tick": least[1]},
        "cos_omega_largest": {"reading": pair(largest[0]), "tick": largest[1]},
        "spread": pair(largest[0] - least[0]),
        "intervals_read": len(strong),
        "accumulated_cos_omega": pair(
            Fraction(sum(n for n, _w, _t in found), sum(w for _n, w, _t in found))
        ),
        "two_cos_omega_first": pair(2 * Fraction(found[0][0], found[0][1])) if found[0][1] else None,
    }


def standing(path: Path, intervals: int | None) -> dict[str, Any]:
    """One world's three reads over the window (the world's ticks, or `intervals`): the body's declared Nodes read, the lay's share kept, the board stepped interval by interval with the record's level before each step kept as z_(t - 1); the rotation at every interval, the share's deviation at the quarters of the window and the centroids at its ends, labelled GAMEBOARD."""
    board = GameBoard(load_world(path))
    if len(board.world.bodies) != 1:
        raise ValueError(
            f"{path.name} declares {len(board.world.bodies)} bodies: the standing world has one"
        )
    row = board.world.bodies[0]
    index, nodes, action = row.family, board.mask(row.nodes), board.world.quantum_action
    steps = board.world.ticks if intervals is None else intervals
    quarters = sorted({steps * part // (2 * 2) for part in (1, 2, 3, 2 * 2)} - {0})
    laid = board.share_of(index)[0]
    start = centroids(laid, nodes)
    deviations: dict[str, Any] = {}
    rotations: list[tuple[int, int, int]] = []
    for _ in range(steps):
        record = board.record(index)[0]
        previous, current = record.before.copy(), record.now.copy()  # z_(t - 1) and z_t at the tick t
        board.step()
        if board.ended is not None:
            break
        turned = rotation(previous, current, board.record(index)[0].now, nodes)  # z_(t + 1) stepped
        if turned[1]:
            rotations.append((*turned, board.tick))
        if board.tick in quarters:
            square = deviation(board.share_of(index)[0], laid, nodes)
            deviations[str(board.tick)] = {"squared": pair(square), "rho": rooted(square, action)}
    end = centroids(board.share_of(index)[0], nodes)
    return {
        "label": LABEL,
        "input": path.name,
        "intervals": board.tick,
        "ended": board.ended,
        "quantum_action": action,
        "amplitude_bound": board.world.amplitude_bound,
        "nodes": int(nodes.sum()),
        "family": board.families[index].name,
        "centroid": {
            "start": [pair(c) for c in start],
            "end": [pair(c) for c in end],
            "drift": [
                None if a is None or b is None else pair(b - a) for a, b in zip(start, end, strict=True)
            ],
        },
        "share_deviation": deviations,
        "rotation": rotations_read(rotations),
        "books": board.books(),
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
    found: dict[str, Any] = {"label": LABEL}
    found["worlds"] = {path.stem: standing(path, args.intervals) for path in args.worlds}
    if args.expectation is not None:
        expected = json.loads(args.expectation.read_text(encoding="utf-8"))
        found["blind"] = {key: expected.get(key) for key in ("reading", "blind", "fence", "status")}
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
