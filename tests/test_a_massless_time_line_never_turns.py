"""The swap at the top reads the gapped time line alone (ALGEBRA.md, The swap at the top, the clause of 2026-10-23 on the massless row; swap.acted): the gap on gravity's pair is the one form within the law that turns a board, and a massless row's weak maximum is the rounding's dip at a static well or a rest, X0 = X1 > X2 by one level, and no top. On the universe test's small structured board (tests/test_universe24_runs_its_cycle.small_world, the 3-cube torus with one clump of matter and uniform light): (1) with gravity massless, [Gamma, Gamma], the fifth act fires nowhere over 60 intervals, and on the shipped massless matter world (examples/events/big_bang/big_bang_matter.json) the weak maximum holds at the body's six neighbours at interval 2 by the letter (the rounding's dip at the rest they stand at) and the act fires nowhere, where the former reading fired there (a closed 9-cube's 38 Nodes at interval 1 alike); (2) with the gap [990, 1000] the same board tops and fires within 40 intervals as before, the structured top standing; (3) the massless board's run back is exact to interval 0 (no act fired, Rule3's own inverse)."""

import numpy as np

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests import laws_universe
from tests import test_universe24_runs_its_cycle as universe


def digest(board):  # type: ignore[no-untyped-def]
    return [
        np.asarray(a, dtype=object).tolist()
        for s in board.states
        for line in s.lines
        for a in (line.now, line.before, line.remainder)
    ] + [np.asarray(r, dtype=object).tolist() for s in board.states for r in s.write_remainders]


def test_a_massless_time_line_never_turns_at_a_well_and_the_gapped_one_still_tops(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(laws_universe, "GAP", universe.GAMMA)  # (1) gravity massless
    monkeypatch.setattr(
        Lattice, "gate", lambda board: None
    )  # the clump's declared count is the gapped board's reading
    board = Lattice(load_world(universe.small_world(tmp_path, detector=False)))
    board.output = lambda line: None
    g = board.held[0]
    assert list(board.families[g].pair) == [universe.GAMMA, universe.GAMMA]
    kept = {0: digest(board)}
    for _ in range(40):  # 60 before the suite's bound of 2026-10-24
        board.step()
        kept[board.interval] = digest(board)
    assert board.swaps == [], (
        board.swaps
    )  # no fire on the massless row (the shipped big_bang_matter world's weak maximum at the body's six neighbours at the interval 2 with no fire read the same sentence on 16 s of load, left on 2026-10-24)
    for k in range(40):  # (3) the run back exact
        board.step_inverse()
        assert digest(board) == kept[40 - k - 1], board.interval
    (tmp_path / "gapped").mkdir()
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path / "gapped")
    monkeypatch.setattr(laws_universe, "GAP", universe.GAMMA - 10)  # (2) the gapped board tops and fires
    gapped = Lattice(load_world(universe.small_world(tmp_path / "gapped", detector=False)))
    gapped.output = lambda line: None
    for _ in range(40):
        gapped.step()
    assert any(s[1] == 1 for s in gapped.swaps), gapped.swaps
