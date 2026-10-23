"""The lay's inverse crosses exactly what the forward wrote, nothing for nothing (ALGEBRA.md, No write from outside Rule3 wakes either double root, the lay's inverse of 2026-10-23; `lay.written`, `meeting_back.logged`, `meeting_back.crossed`): on the gapped 3-cube torus of tests/test_the_swap_at_the_top, (1) a lay act that changes no level and no remainder at an interval above 0 logs no line in the books and writes no output line; (2) a lay that changes one Node is logged once, the output's line the log's own object; (3) the host's crossing from the output lines (tools/back_in_time.py, the tests' BACK.crossed) crosses nothing the books' log holds, so the state stands under it, and the run back with the host's crossing before every inverse is exact at every interval through the lay, as the blind run back is (the former crossing undid a logged lay twice, once from the log in the loop and once from the lines by the host, and the run back with the lays crossed missed at the held write's remainder beside the lay while the blind one held)."""

import copy

import numpy as np

from event_universe import lay, meeting_back, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_gapped import GAMMA, gapped_world


def test_a_lay_that_writes_nothing_is_logged_by_nothing_and_the_run_back_with_the_lines_crossed_is_exact(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(gapped_world(tmp_path, GAMMA - 1, 21, 869)), lines.append)
    dust = [f.name for f in board.families].index("dust")
    kept = {0: meeting_back.snapshot(board)}
    for _ in range(3):
        board.step()
        kept[board.interval] = meeting_back.snapshot(board)
    zeros = np.zeros(board.shape, dtype=object)
    lay.laid(board, dust, 0, (zeros, zeros), None, None)  # (1) a write that writes nothing
    assert board.interval not in board.credit.lays and not [x for x in lines if x["event"] == "lay"]
    assert meeting_back.first_difference(kept[3], meeting_back.snapshot(board)) is None
    change = np.zeros(board.shape, dtype=object)
    change[1, 1, 1] = 5
    lay.laid(board, dust, 0, (change, zeros), None, None)  # (2) one Node written, logged once
    logged = board.credit.lays[board.interval]
    written = [x for x in lines if x["event"] == "lay"]
    assert len(logged) == 1 and len(written) == 1 and logged[0] is written[0]
    kept[3] = meeting_back.snapshot(board)
    for _ in range(2):
        board.step()
        kept[board.interval] = meeting_back.snapshot(board)
    blind = copy.deepcopy(board)
    for _ in range(5):  # (3) the run back with the host's crossing before every inverse
        before = meeting_back.snapshot(board)
        meeting_back.crossed(board, lines)
        assert meeting_back.first_difference(before, meeting_back.snapshot(board)) is None
        board.step_inverse()
        assert meeting_back.first_difference(kept[board.interval], meeting_back.snapshot(board)) is None
    for _ in range(5):  # the blind run back, the loop's own crossing from the books' log
        blind.step_inverse()
        assert meeting_back.first_difference(kept[blind.interval], meeting_back.snapshot(blind)) is None
    assert board.interval == 0 and blind.interval == 0
