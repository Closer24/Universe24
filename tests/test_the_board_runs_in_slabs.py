"""The board stepped in slabs by several processes with one-Link halos (slabs.py; the owner's word of 2026-10-24, everything local, fast and asynchronous, the Node stepping simply with Rule3): whatever the slabs' count, the board's every array after every interval, every output line in its order and the swaps' count equal the single process's bit for bit, through the births; the run back from the board the slabs stepped exact; the count the machine's cores and the board's layers, no key of any file."""

import json
import os
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.meeting_back import first_difference, snapshot
from event_universe.slabs import Slabs, arrays_of, axis_of, slabs_of
from event_universe.world_files import load_world
from tests.laws_universe import small_universe

Run = tuple[list[list[Any]], list[dict[str, Any]], list[tuple[int, int, int]]]
CUBE, TUBE = (
    [5, 5, 5],
    [3, 3, 9],
)  # the hole seed's boards: the 5-cube, and a tube whose longest axis is z


def board_of(folder: Path, shape: list[int], intervals: int, lines: list[dict[str, Any]]) -> Lattice:
    """The tests' small universe on the bare torus `shape` (the law's seed, the sea with its origin empty), every output line kept; the world file's three keys and no other."""
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    small_universe(folder)
    world = {"universe": "u.json", "shape": shape, "intervals": intervals}
    (path := folder / "w.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(path), output=lines.append)


def run(folder: Path, shape: list[int], intervals: int, processes: int) -> Run:
    """The board stepped `intervals` times by `processes` slabs (one slab the single process): every array of the state after every interval, the output lines in their order and the swaps."""
    lines: list[dict[str, Any]] = []
    board = board_of(folder, shape, intervals, lines)
    slabs = Slabs(board, processes)
    assert slabs.count == processes
    states = []
    for _ in range(intervals):
        slabs.advanced()
        states.append([np.asarray(a, dtype=object).copy() for a in arrays_of(board)])
    slabs.close()
    return states, lines, list(board.swaps)


def parting(single: Run, slabs: Run) -> str | None:
    """Where a slabs' run departs from the single process's, or None where they agree bit for bit: the first interval and the arrays differing there (every line's three arrays, the write remainders, the phase lines, the time count, the closes), else the first output line differing with its index, else the swaps."""
    for interval, (a, b) in enumerate(zip(single[0], slabs[0], strict=True), start=1):
        differ = [k for k, (x, y) in enumerate(zip(a, b, strict=True)) if not np.array_equal(x, y)]
        if differ:
            return f"the interval {interval}: the arrays {differ}"
    for k, (a, b) in enumerate(zip(single[1], slabs[1], strict=False)):
        if a != b:
            return f"the line {k}: {json.dumps(a)} against {json.dumps(b)}"
    if len(single[1]) != len(slabs[1]):
        return f"{len(slabs[1])} lines against the single process's {len(single[1])}"
    return None if single[2] == slabs[2] else f"the swaps {slabs[2]} against {single[2]}"


@pytest.mark.parametrize("processes", [2, 5])
def test_the_5_cube_hole_seed_runs_the_same_by_two_and_by_five_slabs(
    tmp_path: Path, processes: int
) -> None:
    """The 5-cube hole seed stepped 12 intervals through its births (from the second interval, at the hole's sides) by two slabs (3 and 2 layers along x) and by five (one layer each, every Node a face Node): the board's every array after every interval, the clicks log's every line in its order (the holes' lays, the children's lays, the credit and birth lines) and the swaps' counts equal the single process's bit for bit."""
    single, found = run(tmp_path / "one", CUBE, 12, 1), run(tmp_path / "slabs", CUBE, 12, processes)
    assert parting(single, found) is None
    assert any(line["event"] == "birth" for line in single[1])  # the run reaches the births


def test_a_tube_cut_across_z_runs_the_same_by_three_slabs(tmp_path: Path) -> None:
    """A [3, 3, 9] tube, its longest axis z, stepped 16 intervals through its births by three slabs of three layers across z: equal to the single process bit for bit, the lines of the three slabs interleaved into the board's x-major order."""
    single, found = run(tmp_path / "one", TUBE, 16, 1), run(tmp_path / "slabs", TUBE, 16, 3)
    assert parting(single, found) is None
    assert any(line["event"] == "birth" for line in single[1])


def test_the_run_back_from_the_board_the_slabs_stepped_is_exact(tmp_path: Path) -> None:
    """The 3-cube hole seed 12 intervals forward through three slabs, through its births, then 12 back by the board's own inverse (the lays the slabs returned logged in the books as the lay act logs them, the points born at a close unborn before its step back): every snapshot met again bit for bit."""
    lines: list[dict[str, Any]] = []
    board = board_of(tmp_path, [3, 3, 3], 30, lines)
    slabs, snapshots = Slabs(board, 3), {0: snapshot(board)}
    for interval in range(1, 13):
        slabs.advanced()
        snapshots[interval] = snapshot(board)
    slabs.close()
    assert any(line["event"] == "birth" for line in lines)
    for _ in range(12):
        board.step_inverse()
        assert first_difference(snapshots[board.interval], snapshot(board)) is None, board.interval


def test_the_slabs_count_is_the_machines_and_the_boards_and_no_files(tmp_path: Path) -> None:
    """The count the fewer of the longest axis's layers and the machine's cores, the first slabs one layer longer where the division leaves a remainder (`slabs_of`); a world file holds its three keys and names no count, and the runner made from it takes the machine's."""
    assert slabs_of(5, 4) == [range(0, 2), range(2, 3), range(3, 4), range(4, 5)]
    assert slabs_of(9, 3) == [range(0, 3), range(3, 6), range(6, 9)] and slabs_of(5, 8) == slabs_of(5, 5)
    assert slabs_of(1, 4) == [range(0, 1)] and axis_of((3, 3, 9)) == 2 and axis_of((5, 5, 5)) == 0
    board = board_of(tmp_path, TUBE, 40, [])
    keys = json.loads((tmp_path / "w.json").read_text(encoding="utf-8"))
    assert sorted(keys) == ["intervals", "shape", "universe"]  # no key names a count of anything
    slabs = Slabs(board)
    try:
        assert slabs.count == min(9, os.process_cpu_count() or 1) and slabs.axis == 2
    finally:
        slabs.close()
