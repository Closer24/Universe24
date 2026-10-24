"""The run back is exact (ALGEBRA.md, Clicks go only forward; the backward run is exact; The lay's inverse): the bare 3-cube torus of the tests' small universe under the law's hole seed, 32 intervals forward through its births and their clicks and 32 back, every family's lines and write remainders bit for bit at every interval and the interval back at 0; the one run back of the suite since the tests' audit of 2026-10-24 (the file held the level reading's memo test to that day as test_the_level_reading_is_read_once_per_volume.py)."""

from pathlib import Path

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import bare_torus

INTERVALS, CUBE = 32, 3


def test_the_bare_torus_runs_back_exact_over_32_intervals(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    clicks: list[dict[str, object]] = []
    board = Lattice(load_world(bare_torus(tmp_path, CUBE)), output=clicks.append)
    states = [board_state(board)]
    for _ in range(INTERVALS):
        board.step()
        states.append(board_state(board))
    during: list[dict[str, object]] = []
    board.output = during.append
    back = 0
    for k in range(INTERVALS):
        board.step_inverse()
        back += same_state(board_state(board), states[INTERVALS - 1 - k])
    assert (back, during, board.interval) == (INTERVALS, [], 0)
    assert any(line["event"] == "credit" for line in clicks)  # the births at 29, the board's own clicks
