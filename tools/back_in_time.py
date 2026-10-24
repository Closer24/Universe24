"""The back-in-time gate (the owner's word of 2026-09-30: a check that the board can be taken back in time): a world is run N intervals forward after its first interval and N back by the lattice's own inverse, and every array of every family (every line's levels now and before and its remainder, every held line's write remainder) and the interval counter are compared bit for bit with the state at the same interval on the way forward: the verdict MATCH, or MISS naming the first interval, the family, the array and the first Node that differ, or REFUSED with the lattice's reason where the run back is refused by name; a lattice with a receding face is compared at the shape it had at that interval, the layers a step grew taken off by its inverse, and a run that ends at the largest size before N intervals goes back over the intervals it ran, the end named. The NodeDetectors' acts from outside the Node are crossed from the LATTICE-labelled lines the forward run wrote (ENGINE.md, section 3, act 6; the mathematician's 193 and 195 with the advisor's second, two hands): the faces presented at the clicks' Nodes and on the fronts' shells are rebuilt from the `face` lines into the books' log, emptied first, so the inverse presents the lines' values and nothing the books kept (`faces_from`), and before each step back every line a lay changed at that interval (the absorption's and the emission's lays, the emitted quantum's, the null window's re-lay) is set back to its levels before the lay from the `lay` lines (`crossed`), the lay's line the crossing, so that Rule3's inverse runs through the click; the start is the loaded state, which one step back from the first interval returns. The crossing and the comparison are the engine's own functions (src/event_universe/meeting_back.py, where the meeting that runs back runs the board back and forward inside the act), imported here; a host tool and no state of the law.

The window (2026-10-24, the record's second check, the run back across a return): `--from K` runs the board forward to the interval K keeping no snapshot and no output line, then `--intervals` N forward with a snapshot after each and N back compared to K, so a run of thousands of intervals is checked across a return where every interval's snapshot does not fit; the report as without it, with the window's first interval under `from`.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/back_in_time.py --intervals 40 <world>.json
    PYTHONPATH=src python tools/back_in_time.py --from 380 --intervals 20 <world>.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from event_universe.lattice import Lattice
from event_universe.meeting_back import arrays_of, crossed, first_difference, snapshot
from event_universe.world_files import load_world

__all__ = [
    "arrays_of",
    "crossed",
    "first_difference",
    "main",
    "snapshot",
    "verdict",
]  # the readings the tests read by this tool's name


def verdict(board: Lattice, intervals: int, start: int | None = None) -> dict[str, object]:
    """The gate on a loaded lattice: the first interval, then `intervals` forward with a snapshot after each (fewer where the run ends at a receding face's largest size, `ended`) and the output lines kept, then as many back, the faces presented from the `face` lines and each interval's lays undone from its `lay` lines (`faces_from`, `crossed`), each step back compared with the snapshot of its interval; MATCH, or MISS with the first interval, array and Node that differ, or REFUSED with the reason where the lattice refuses the run back by name. With `start` K the window: the board runs forward to the interval K first, keeping no snapshot and no output line (nothing before K is crossed), the snapshots and the run back from K on, and the report carries K under `from`."""
    kept, lines = board.output, []

    def observed(line: dict[str, object]) -> None:
        lines.append(line)
        if kept is not None:
            kept(line)

    board.output = observed
    board.step()
    while start is not None and board.interval < start:
        board.step()
        lines.clear()
    snapshots, run = {board.interval: snapshot(board)}, 0
    for _ in range(intervals):
        board.step()
        run += 1
        snapshots[board.interval] = snapshot(board)
    for _ in range(run):
        crossed(board, lines)
        try:
            board.step_inverse()
        except RuntimeError as refusal:  # the run back refused by name by the lattice itself
            board.output = kept
            return {
                "verdict": "REFUSED",
                "interval": board.interval,
                "reason": str(refusal),
            }
        found = first_difference(snapshots[board.interval], snapshot(board))
        if found is not None:
            label, at = found
            return {"verdict": "MISS", "interval": board.interval, "array": label, "node": at}
    board.output = kept
    found: dict[str, object] = {"verdict": "MATCH", "intervals": run, "interval": board.interval}
    if start is not None:
        found["from"] = start
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, with its mode file beside it")
    parser.add_argument("--intervals", type=int, required=True, help="the intervals forward and back")
    parser.add_argument(
        "--from",
        dest="start",
        type=int,
        default=None,
        metavar="K",
        help="the window: forward to the interval K with no snapshot, then --intervals forward and back",
    )
    args = parser.parse_args(argv)
    print(json.dumps(verdict(Lattice(load_world(args.world)), args.intervals, args.start)))


if __name__ == "__main__":
    main()
