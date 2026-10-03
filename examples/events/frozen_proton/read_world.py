"""The frozen proton's reader (the two hands' blind, #1572 comments 5963954612 (b) and 5964082980 (b)): the world is loaded as the runner loads it and stepped by the engine's own step over its `ticks` with an observer, and the blind's rows are read from the GameBoard and the lines, every number a GameBoard reading labelled so unless it is a detector's line: per interval the six lines' levels now and before and Rule3's remainders at the body's Node (the cycle), the Wronskian sum there, the count in the books, the Nodes carrying a level of the record (the spread); at the start the sign holder's rows and the binding holder's level at the Node and at its six neighbours (the rest); the click and credit lines of the run. The tool holds no number of the law and compares nothing.

PYTHONPATH=src python examples/events/frozen_proton/read_world.py --expectation examples/events/frozen_proton/expectation.json examples/events/frozen_proton/frozen_proton.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import node
from event_universe.core.ports import arrival
from event_universe.game_board import GameBoard
from event_universe.world_files import load_world


def at_and_around(array: np.ndarray, at: tuple[int, int, int], board: GameBoard) -> dict[str, Any]:
    """An array's value at a Node and at its six neighbours through the Ports, in Port order."""
    return {
        "at": int(array[at]),
        "neighbours": [
            int(np.asarray(arrival(array, axis, side, board.wrap, 0))[at])
            for axis in range(3)
            for side in (1, -1)
        ],
    }


def reading(path: Path) -> dict[str, Any]:
    """One world's reading over its run."""
    board = GameBoard(load_world(path), (lines := []).append)
    index = board.world.bodies[0].family
    family, state = board.families[index], board.states[index]
    at = tuple(int(a) + b for a, b in zip(board.world.bodies[0].nodes[0], board.offset, strict=True))
    node_at = (at[0], at[1], at[2])
    holders = {
        board.families[i].name: [
            at_and_around(line.now, node_at, board)
            for line in board.states[i].lines[: board.families[i].records]
        ]
        for i in board.held
    }
    cycle = []
    for _ in range(board.world.ticks):
        levels = [
            [int(r.now[node_at]), int(r.before[node_at]), int(r.remainder[node_at])] for r in state.lines
        ]
        wronskian = int(np.asarray(node.wronskian(state.lines, family.plane))[node_at])
        standing = int(sum((r.now != 0) | (r.before != 0) for r in state.lines).astype(bool).sum())
        cycle.append(
            {
                "interval": board.tick,
                "lines": levels,
                "wronskian": wronskian,
                "quanta": board.books()[family.name]["quanta"],
                "nodes_carrying_a_level": standing,
            }
        )
        if board.ended is not None:
            break
        board.step()
    return {
        "world": path.name,
        "label": "GAMEBOARD",
        "lines": family.lines,
        "amplitude_laid": int(np.abs(state.lines[0].now).max()) if cycle and cycle[0]["lines"] else None,
        "holders_at_the_start": holders,
        "cycle": cycle,
        "period_4_exact": all(c["lines"] == cycle[k % 4]["lines"] for k, c in enumerate(cycle))
        if len(cycle) >= 4
        else None,
        "remainders_0": all(r == 0 for c in cycle for *_levels, r in c["lines"]),
        "wronskian_sums": sorted({c["wronskian"] for c in cycle}),
        "quanta_over_the_run": sorted({c["quanta"] for c in cycle}),
        "nodes_carrying_a_level": sorted({c["nodes_carrying_a_level"] for c in cycle}),
        "click_lines": [line for line in lines if line["event"] == "click"],
        "credit_lines": [line for line in lines if line["event"] == "credit"],
        "books": board.books(),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "worlds", type=Path, nargs="+", help="the world files, with their mode files beside them"
    )
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    args = parser.parse_args(argv)
    blind = json.loads(args.expectation.read_text(encoding="utf-8"))
    found = {
        "label": "GAMEBOARD",
        "blind": blind["blind"],
        "readings": {path.stem: reading(path) for path in args.worlds},
    }
    print(json.dumps(found, indent=1, default=str))


if __name__ == "__main__":
    main()
