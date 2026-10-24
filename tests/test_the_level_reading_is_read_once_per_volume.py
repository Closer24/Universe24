"""The volume's level reading read once per distinct volume (features/volume `level_of`, the memo `LEVELS`; the architect's round of 2026-10-24): the bare 3-cube torus with the one universe file over 32 intervals holds the state the search at every Node holds, and 32 intervals of it run back exact with the clicks' history kept (the births at 29, the board's own click lines). To 2026-10-24 the test ran a 9-cube of the small universe, a world laid with bodies, cancelled with every world but Universe24; the sentence the same."""

from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import world_files
from event_universe.features import volume
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import bare_torus

INTERVALS, CUBE, COMPARED = 32, 3, 32  # 30, 9, 15 on the small universe to 2026-10-24


def searched_at_every_node(gamma: int, volumes: Any) -> Any:
    """The level reading as the search at every Node gives it, no memo (`volume.searched_levels` on the whole array)."""
    flat = np.asarray(volumes, dtype=object).reshape(-1)
    return volume.searched_levels(gamma, flat).reshape(np.asarray(volumes).shape)


def test_the_bare_torus_holds_the_state_of_the_search_at_every_node(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = bare_torus(tmp_path, CUBE)
    searched: list[dict[str, object]] = []
    monkeypatch.setattr(volume, "level_of", searched_at_every_node)
    board = Lattice(load_world(path), output=searched.append)
    states = []
    for _ in range(COMPARED):
        board.step()
        states.append(board_state(board))
    monkeypatch.undo()
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    read_once: list[dict[str, object]] = []
    board = Lattice(load_world(path), output=read_once.append)
    for interval in range(COMPARED):
        board.step()
        assert same_state(board_state(board), states[interval]), interval
    assert read_once == searched and any(line["event"] == "credit" for line in read_once)


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
