"""The composed paces' cost and width, a GameBoard diagnostic and no measurement (core/paces.py; ALGEBRA.md #the-paces, the principle C, the owner's word of 2026-10-01, 17:02): for the worlds given, at their universe's Gamma, T and width, the time of one lookup of the clock and of the Link's pace over a board of the world's declared shape (and of every shape given with --nodes) holding a well of the depth given, the memo cold and warm, beside the time of the whole first interval of the world itself; the contents at which the Link's pace and the clock round to 0 at Gamma, with the exact integers' size there, the time of one value by its own power and the memo's running fill through the well's depth, 3 Gamma and the Link's zero; and the write's width: the form D of one quantum (T) and at the amplitude bound (A^2) times the three Links' paces at the vacuum and at the guard's edge, as one product and one axis at a time (`paces.write_factor`, on a count and on a Wronskian), each against the width's largest integer, with the identity of the write's and the turn's factors at the vacuum. Every number comes from the files and the command line; the tool holds none of the law's and writes nothing to the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/composed_paces.py --depth 300 --repeat 20 [--nodes X Y Z ...] <world>.json ...
"""

from __future__ import annotations

import argparse
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.rule3 import division_fixed_point
from event_universe.features.read import edge_squared
from event_universe.game_board import GameBoard
from event_universe.world_files import load_world

LABEL = "GAMEBOARD"


def clocks_zero(gamma: int) -> int:
    """The least content at which the clock itself rounds to 0 at Gamma, by doubling and halving on the clock's own power (`paces.clock_alone`), the memo untouched; the Link's pace's zero is `paces.frozen_content`."""
    low, high = 0, 1
    while paces.clock_alone(gamma, high) > 0:
        high += high
    while high - low > 1:
        middle = (low + high) // 2
        if paces.clock_alone(gamma, middle) > 0:
            low = middle
        else:
            high = middle
    return high


def fill_seconds(gamma: int, size: int) -> float:
    """The seconds of the memo's running fill from the vacuum through the content `size`, cold."""
    paces.clear_memo()
    start = time.perf_counter()
    paces.clock(gamma, size)
    return time.perf_counter() - start


def well(shape: tuple[int, ...], depth: int) -> np.ndarray:
    """A well of the given depth over a board: the content depth div (1 + the distance from the centre along the axes), the hardware's integers."""
    centre = [extent // 2 for extent in shape]
    distance: Any = 0
    for axis, index in enumerate(np.indices(shape)):
        distance = distance + np.abs(index - centre[axis])
    return np.asarray(depth // (1 + distance), dtype=np.int64)


def timed(function: Callable[[], Any], repeat: int) -> float:
    """The seconds of one call, the mean over `repeat` calls."""
    start = time.perf_counter()
    for _ in range(repeat):
        function()
    return (time.perf_counter() - start) / repeat


def lookup_cost(gamma: int, shape: tuple[int, ...], depth: int, repeat: int) -> dict[str, Any]:
    """The lookups' cost on one board: the memo cold (the first lookup fills it over the well's values) and warm, the clock and the Link's pace, and the distinct contents on the board."""
    contents = well(shape, depth)
    paces.clear_memo()
    cold = timed(lambda: paces.clock_of(gamma, contents), 1)
    return {
        "shape": list(shape),
        "nodes": int(contents.size),
        "distinct_contents": int(np.unique(contents).size),
        "first_lookup_seconds": cold,
        "clock_lookup_seconds": timed(lambda: paces.clock_of(gamma, contents), repeat),
        "link_pace_lookup_seconds": timed(lambda: paces.link_pace_of(gamma, contents), repeat),
    }


def fits(value: int, largest: int) -> str:
    return "fits" if value <= largest else "overflows"


def width_of(
    gamma: int, action: int, bound: int, largest: int, pairs: list[tuple[int, int]]
) -> dict[str, Any]:
    """The write's width at the vacuum's paces and at the guard's edge: D p_x p_y p_z as one product and p_0 D p_x p_y p_z with the clock, each against the width's largest integer, and the per-axis booking's largest intermediate, D times one pace; D the form of one quantum, T, and the form at the amplitude bound, A^2; the identities at the vacuum."""
    edge = max(division_fixed_point(edge_squared(pair, gamma)) for pair in pairs)
    found: dict[str, Any] = {"vacuum_pace": gamma, "edge_pace": edge, "largest": largest}
    for name, form in (("one_quantum_T", action), ("amplitude_bound_A_squared", bound * bound)):
        for label, pace in (("vacuum", gamma), ("edge", edge)):
            product = form * pace * pace * pace
            found[f"{name}_{label}"] = {
                "D_px_py_pz": [product, fits(product, largest)],
                "p0_D_px_py_pz": [product * pace, fits(product * pace, largest)],
                "per_axis_intermediate_D_p": [form * pace, fits(form * pace, largest)],
                "write_factor_count": int(paces.write_factor(form, pace, pace, pace, pace, gamma, 2)),
                "write_factor_wronskian": int(
                    paces.write_factor(form, pace, pace, pace, pace, gamma, 1)
                ),
            }
    vacuum = np.full((2, 1, 1), gamma, dtype=np.int64)
    counts = np.array([[[action]], [[bound]]], dtype=np.int64)
    found["identity_at_the_vacuum"] = {
        "write_count": paces.write_factor(counts, vacuum, vacuum, vacuum, vacuum, gamma, 2)
        .ravel()
        .tolist(),
        "write_wronskian": paces.write_factor(counts, vacuum, vacuum, vacuum, vacuum, gamma, 1)
        .ravel()
        .tolist(),
        "turn": paces.turn_factor(counts, vacuum, gamma).ravel().tolist(),
        "counts": counts.ravel().tolist(),
    }
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worlds", nargs="+", type=Path)
    parser.add_argument("--depth", type=int, required=True, help="the well's depth in levels")
    parser.add_argument("--repeat", type=int, required=True, help="the calls per timing")
    parser.add_argument("--nodes", type=int, nargs=3, action="append", default=[], help="a shape X Y Z")
    args = parser.parse_args(argv)
    for path in args.worlds:
        world = load_world(path)
        gamma, action = world.node_clock, world.quantum_action
        board = GameBoard(world, lambda line: None)
        interval = timed(board.step, 1)
        link_zero, clock_zero = paces.frozen_content(gamma), clocks_zero(gamma)
        start = time.perf_counter()
        at_zero = paces.clock_alone(gamma, clock_zero)
        one_value = time.perf_counter() - start
        fills = {size: fill_seconds(gamma, size) for size in (args.depth, 3 * gamma, link_zero)}
        reading: dict[str, Any] = {
            "label": LABEL,
            "world": str(path),
            "node_clock": gamma,
            "quantum_action": action,
            "amplitude_bound": world.amplitude_bound,
            "first_interval_seconds": interval,
            "link_pace_rounds_to_zero_at": [link_zero, paces.clock(gamma, link_zero)],
            "clock_rounds_to_zero_at": [clock_zero, at_zero, paces.clock_alone(gamma, clock_zero - 1)],
            "exact_numerator_bits_at_the_zeros": [
                (gamma * (gamma - 1) ** link_zero).bit_length(),
                (gamma * (gamma - 1) ** clock_zero).bit_length(),
            ],
            "one_value_alone_seconds_at_the_clocks_zero": one_value,
            "running_fill_seconds_through": fills,
            "lookups": [
                lookup_cost(gamma, shape, args.depth, args.repeat)
                for shape in [tuple(world.shape), *(tuple(nodes) for nodes in args.nodes)]
            ],
            "width": width_of(
                gamma, action, world.amplitude_bound, world.width, [f.pair for f in world.families]
            ),
        }
        print(reading)


if __name__ == "__main__":
    main()
