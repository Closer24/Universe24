"""The two-level body's reader (examples/events/body_node_detector; line 1 of the generic emitter/detector): the world run once per seed given from its lay, the detector's credit lines counted by the level realised (the clicks, DETECTOR) beside the blind, the detector's proper time against the board's tick and the window index, and as a GameBoard reading labelled so the exact solve's p_e on every window's level sequence at the detector's Node, read from the arrays and no click.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/body_node_detector/read_world.py [--folder .] [--seeds 24 ...] [--windows N]
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe.body_node import references_over, scale_of_the_width, shares, solved
from event_universe.game_board import GameBoard
from event_universe.world_files import load_world

HERE = Path(__file__).resolve().parent


def one_seed(path: Path, seed: int, windows: int | None) -> dict[str, Any]:
    """One run at the seed: the clicks per level realised, the clocks' check and the solve's p_e per window, a GameBoard reading."""
    lines: list[dict[str, Any]] = []
    board = GameBoard(load_world(path), lines.append)
    board.credit.state = seed
    detector = next(d for d in board.detectors if d.levels)
    pairs, weights = tuple(v.pair for v in detector.levels), tuple(v.weight for v in detector.levels)
    window, scale = board.world.instrument.window, scale_of_the_width(board.world.width)  # type: ignore[union-attr]
    count = windows if windows is not None else board.world.ticks // window
    at, index, read = detector.nodes, board.order[0], []
    for _ in range(count):
        sequence = []
        for _ in range(window):
            board.step()
            sequence.append(int(board.record(index)[0].now[at][0]))  # type: ignore[index]
        found = shares(solved(references_over(scale, pairs, window), sequence)[1], pairs, weights)
        read.append(Fraction(found[1], sum(found)))
    credits = [c for c in lines if c["event"] == "credit" and c["detector"] == detector.name]
    return {
        "seed": seed,
        "clicks": dict(Counter(c["realised"] for c in credits)),
        "windows": len(credits),
        "proper_is_tick": all(c["proper"] == c["tick"] for c in credits),
        "window_index": [c["windows"] for c in credits[:3]],
        "count_moved": sorted({c["count"] for c in credits}),
        "solve_p_e": {
            "least": round(float(min(read)), 4),
            "largest": round(float(max(read)), 4),
            "mean": round(float(sum(read) / len(read)), 4),
            "label": "GAMEBOARD",
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--seeds", type=int, nargs="*", default=None)
    parser.add_argument("--windows", type=int, default=None)
    args = parser.parse_args(argv)
    design = json.loads((args.folder / "design.json").read_text(encoding="utf-8"))
    blind = json.loads((args.folder / "expectation.json").read_text(encoding="utf-8"))
    seeds = args.seeds if args.seeds else [int(design["seed"])]
    path = args.folder / f"{design['world']}.json"
    found = {
        "seeds": [one_seed(path, seed, args.windows) for seed in seeds],
        "blind": {"clicks": blind["clicks"], "reference": blind["reference"]},
        "label": "DETECTOR for the clicks; GAMEBOARD for the solve's p_e",
    }
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
