"""The back-in-time gate (the owner's word of 2026-09-30: a check that the board can be taken back in time): a world is run N intervals forward after its first interval and N back by the lattice's own inverse, and every array of every family (every line's levels now and before and its remainder, every held line's write remainder) and the interval counter are compared bit for bit with the state at the same interval on the way forward: the verdict MATCH, or MISS naming the first interval, the family, the array and the first Node that differ; a lattice with a receding face is compared at the shape it had at that interval, the layers a step grew taken off by its inverse, and a run that ends at the largest size before N intervals goes back over the intervals it ran, the end named. The NodeReaders' acts from outside the Node are crossed from the LATTICE-labelled lines the forward run wrote (ENGINE.md, section 3, act 6; the mathematician's 193 and 195 with the advisor's second, two hands): the faces presented at the clicks' Nodes and on the fronts' shells are rebuilt from the `face` lines into the books' log, emptied first, so the inverse presents the lines' values and nothing the books kept (`faces_from`), and before each step back every line a lay changed at that interval (the taking's and the giving's lays, the given quantum's, the null window's re-lay) is set back to its levels before the lay from the `lay` lines (`crossed`), the lay's line the crossing, so that Rule3's inverse runs through the click; the start is the loaded state, which one step back from the first interval returns. A host tool and no state of the law.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/back_in_time.py --intervals 40 <world>.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from event_universe.features.click import Face
from event_universe.lattice import Lattice
from event_universe.node import NodeState, Record
from event_universe.world_files import load_world

Snapshot = list[tuple[str, np.ndarray]]
Lines = list[dict[str, object]]  # the output lines of a run, as the lattice's output receives them


def arrays_of(name: str, state: NodeState) -> Snapshot:
    """Every array of a family's NodeState with its name, copied."""
    found: list[tuple[str, np.ndarray]] = []
    for index, record in enumerate(state.lines):
        found += [
            (f"lines[{index}].{key}", getattr(record, key)) for key in ("now", "before", "remainder")
        ]
    found += [
        (f"write_remainders[{index}]", value) for index, value in enumerate(state.write_remainders)
    ]
    return [(f"{name}.{label}", np.asarray(value).copy()) for label, value in found]


def snapshot(board: Lattice) -> list[Snapshot]:
    """Every array of every family of the lattice, copied."""
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


def node_of(board: Lattice, line: dict[str, object]) -> tuple[int, tuple[int, int, int]]:
    """A LATTICE line's family by its position and its Node at the file's coordinates."""
    names = [family.name for family in board.families]
    at = [int(a) for a in line["node"]["at"]]  # type: ignore[index]
    return names.index(str(line["family"])), (at[0], at[1], at[2])


def faces_from(board: Lattice, lines: Lines) -> None:
    """The faces of a run rebuilt from its `face` lines into the books' log, the log emptied first: per line the family, the line, the Node, the Port, the interval and the value, so the inverse presents what the lines carry."""
    board.credit.faces = {}
    for line in [line for line in lines if line["event"] == "face"]:
        index, at = node_of(board, line)
        interval, port, value = (int(str(line[key])) for key in ("interval", "port", "value"))
        found = Face(index, int(str(line["line"])), at, port, interval, value)
        board.credit.faces.setdefault(interval, []).append(found)


def crossed(board: Lattice, lines: Lines) -> None:
    """The lays of the lattice's interval undone from their `lay` lines before the step back: every line a lay changed at a Node set back to its levels [now, before, remainder] before the lay, the interval's lines in reverse order (two lays on one Node in one interval are two lines, the second's `before` the first's `after`), every other Node as it stands."""
    for line in reversed(
        [line for line in lines if line["event"] == "lay" and line["interval"] == board.interval]
    ):
        index, at = node_of(board, line)
        here = (at[0] + board.offset[0], at[1] + board.offset[1], at[2] + board.offset[2])
        record, number = board.states[index].lines[int(str(line["line"]))], int(str(line["line"]))
        arrays = [np.array(a, copy=True) for a in (record.now, record.before, record.remainder)]
        for array, value in zip(arrays, line["before"], strict=True):  # type: ignore[call-overload]
            array[here] = value
        board.states[index].lines[number] = Record(arrays[0], arrays[1], arrays[2])


def verdict(board: Lattice, intervals: int) -> dict[str, object]:
    """The gate on a loaded lattice: the first interval, then `intervals` forward with a snapshot after each (fewer where the run ends at a receding face's largest size, `ended`) and the output lines kept, then as many back, the faces presented from the `face` lines and each interval's lays undone from its `lay` lines (`faces_from`, `crossed`), each step back compared with the snapshot of its interval; MATCH, or MISS with the first interval, array and Node that differ."""
    kept, lines = board.output, []

    def observed(line: dict[str, object]) -> None:
        lines.append(line)
        if kept is not None:
            kept(line)

    board.output = observed
    board.step()
    snapshots, run = {board.interval: snapshot(board)}, 0
    for _ in range(intervals):
        board.step()
        if board.ended is not None:
            break
        run += 1
        snapshots[board.interval] = snapshot(board)
    ended = board.ended
    faces_from(board, lines)
    for _ in range(run):
        crossed(board, lines)
        board.step_inverse()
        found = first_difference(snapshots[board.interval], snapshot(board))
        if found is not None:
            label, at = found
            return {"verdict": "MISS", "interval": board.interval, "array": label, "node": at}
    board.output = kept
    return {"verdict": "MATCH", "intervals": run, "interval": board.interval, "ended": ended}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, with its mode file beside it")
    parser.add_argument("--intervals", type=int, required=True, help="the intervals forward and back")
    args = parser.parse_args(argv)
    print(json.dumps(verdict(Lattice(load_world(args.world)), args.intervals)))


if __name__ == "__main__":
    main()
