"""The one lay act (ALGEBRA.md, No write from outside Rule3 wakes either double root of the massless row; The uniform seed is a lay; `src/event_universe/lay.py`): every write from outside Rule3 is one call of `laid`, the division act absorption the uniform part out of each level's change where weights are given, the guard refusing by name a lay that moves one of the two sums, the write at the lay's Nodes with the remainder at the division's origin; the seed of the bare torus is one such call with no weights, the levels laid as built."""

from pathlib import Path

import numpy as np
import pytest

from event_universe import lay, records, seed, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import refused
from tests.laws_universe import CUBE, bare_torus, flat


def test_the_division_act_keeps_the_two_sums_and_the_guard_refuses_a_lay_that_moves_one():
    """The principle's one division act (ALGEBRA.md, The packet lay (h); `lay.division_act`, `lay.shares_of`, `lay.corrected`, `lay.guarded`): a level summing to 7 over four Nodes weighted 1, 3, 3, 1 has -7 divided back floor by floor, (-1, -3, -3, -1) short by one unit, the leftover to the heaviest Node first, so the level [1, 4, 3, -1] is laid as [0, 2, 0, -2] and sums to 0; a level summing to 0 as laid, or weighted nowhere, is returned as it is; the guard: a massless lay whose weights carry nothing refuses by name with the family and the two changes, a gapped family's lay and a lay handed no weights are laid as given, and in time the span's increments are kept at the sum 0 and the first moment 0 (`lay.laid_in_time`, the branch's division act in time bit for bit, `lay.division_act_in_time`). The shipped two slits' mode file is the generator's through the act, bit for bit."""
    level, weights = np.array([1, 4, 3, -1], dtype=object), np.array([1, 3, 3, 1], dtype=object)
    assert lay.shares_of(-7, [1, 3, 3, 1]) == [-1, -2, -3, -1]
    assert list(lay.division_act(level, weights)) == [0, 2, 0, -2]
    assert lay.division_act(level - level, weights) is not None and list(
        lay.division_act(level, weights * 0)
    ) == [1, 4, 3, -1]
    now, before = lay.corrected("light", True, (level, level * 2), weights)
    assert (int(now.sum()), int(before.sum())) == (0, 0) and list(before) == [0, 3, 1, -4]
    refused("wakes the zero mode", lay.corrected, "light", True, (level, level), weights * 0)
    refused("'light'", lay.guarded, "light", True, 7, 0, False)
    assert (
        lay.corrected("matter", False, (level, level), weights)[0] is level
    )  # a gapped family: as given
    assert (
        lay.corrected("light", True, (level, level), None)[1] is level
    )  # no weights: laid as built, named


def test_the_seeds_lay_is_one_call_of_the_act_with_no_weights(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The uniform seed is a lay (ALGEBRA.md; seed.uniform_seed): on the bare 3-cube torus of the one universe file the light family's one line stands at the drift v now (v^2 <= T, the largest such) and 0 before on every Node with the remainder at the lay's origin, the half wall; the same call of `lay.laid` with no weights on the line emptied returns the changes as built bit for bit and leaves the board at the seed's state, no uniform part taken out."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path, CUBE)))
    light = board.world.seed
    assert light is not None
    drift, half = seed.drift_of(board.world.quantum_action), board.half_wall(light)
    assert drift * drift <= board.world.quantum_action < (drift + 1) * (drift + 1)
    line = board.states[light].lines[0]
    assert flat(line.now) == [drift] * CUBE**3 and flat(line.before) == [0] * CUBE**3
    assert flat(line.remainder) == [half] * CUBE**3
    zeros = records.zeros(board.shape, board.kind)
    board.states[light].lines[0] = records.Record(zeros, zeros.copy(), line.remainder)
    now = records.full(board.shape, drift, board.kind)
    written = lay.laid(board, light, 0, (now, zeros), None, None)
    assert np.array_equal(written[0], now) and np.array_equal(written[1], zeros)
    laid = board.states[light].lines[0]
    assert flat(laid.now) == flat(line.now) and flat(laid.before) == flat(line.before)
    assert flat(laid.remainder) == flat(line.remainder)
