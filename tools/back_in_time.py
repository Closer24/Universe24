"""The back-in-time gate (the owner's word of 2026-09-30: a check that the board can be taken back in time): a world is run N intervals forward after its first interval and N back by the GameBoard's own inverse, and every array of every family (every record's levels now and before and its remainder, every held part's write remainder) and the interval counter are compared bit for bit with the state at the same interval on the way forward: the verdict MATCH, or MISS naming the first interval, the family, the array and the first Node that differ; a GameBoard with a receding face is compared at the shape it had at that interval, the layers a step grew taken off by its inverse, and a run that ends at the largest size before N intervals goes back over the intervals it ran, the end named. A host tool and no state of the law.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/back_in_time.py --intervals 40 <world>.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from event_universe.game_board import GameBoard
from event_universe.growth import SCALARS
from event_universe.node import NodeState
from event_universe.world_files import load_world

Snapshot = list[tuple[str, np.ndarray]]


def arrays_of(name: str, state: NodeState) -> Snapshot:
    """Every array of a family's NodeState with its name, copied."""
    found: list[tuple[str, np.ndarray]] = []
    records = [("levels", state.levels), ("second", state.second)]
    records += [(f"parts[{index}]", part) for index, part in enumerate(state.parts) if index]
    for label, record in records:
        if record is not None:
            found += [(f"{label}.{key}", getattr(record, key)) for key in ("now", "before", "remainder")]
    for key in SCALARS:
        found += [(f"{key}[{part}]", value) for part, value in enumerate(getattr(state, key))]
    return [(f"{name}.{label}", np.asarray(value).copy()) for label, value in found]


def snapshot(board: GameBoard) -> list[Snapshot]:
    """Every array of every family of the GameBoard, copied."""
    return [
        arrays_of(family.name, state) for family, state in zip(board.families, board.states, strict=True)
    ]


def first_difference(before: list[Snapshot], after: list[Snapshot]) -> tuple[str, list[int]] | None:
    """The first array and the first Node at which two snapshots differ, or None where they agree bit for bit."""
    for family_before, family_after in zip(before, after, strict=True):
        for (label, was), (_label, now) in zip(family_before, family_after, strict=True):
            if was.shape != now.shape:
                return f"{label} (the shape {list(now.shape)} against {list(was.shape)})", []
            differing = np.argwhere(was != now)
            if len(differing):
                return label, [int(i) for i in differing[0]]
    return None


def verdict(board: GameBoard, intervals: int) -> dict[str, object]:
    """The gate on a loaded GameBoard: the first interval, then `intervals` forward with a snapshot after each (fewer where the run ends at a receding face's largest size, `ended`), then as many back, each step back compared with the snapshot of its interval; MATCH, or MISS with the first interval, array and Node that differ."""
    board.step()
    snapshots, run = {board.tick: snapshot(board)}, 0
    for _ in range(intervals):
        board.step()
        if board.ended is not None:
            break
        run += 1
        snapshots[board.tick] = snapshot(board)
    ended = board.ended
    for _ in range(run):
        board.step_inverse()
        found = first_difference(snapshots[board.tick], snapshot(board))
        if found is not None:
            label, at = found
            return {"verdict": "MISS", "interval": board.tick, "array": label, "node": at}
    return {"verdict": "MATCH", "intervals": run, "interval": board.tick, "ended": ended}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, with its mode file beside it")
    parser.add_argument("--intervals", type=int, required=True, help="the intervals forward and back")
    args = parser.parse_args(argv)
    print(json.dumps(verdict(GameBoard(load_world(args.world)), args.intervals)))


if __name__ == "__main__":
    main()
