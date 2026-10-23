"""The horizon (ALGEBRA.md, The horizon, the owner's word of 2026-10-23): a Link whose tension reaches the wall Gamma is read at the wall, its factor Gamma - t at 0, and the run goes on with its two ends decoupled, where the former reading refused the run by name at a tension above Gamma (features/read.link_tensions). On the universe test's small structured board (tests/laws_universe.small_world, the 3-cube torus with one clump of matter and uniform light) no Link reaches the wall within the test's seconds (the largest tension 440 before the crunch), so the Link is forced to the wall by the test's state: gravity's x tension line (the shear's momentum, a held line) at the clump's Node set to the level Gamma + 300 now and before (pulled down by its own massless line toward its neighbours' levels) and its +x neighbour's to the same, matter at the neighbour lifted by 100 so that a plain current stands across the Link, so that the Link (1, 1, 1)-(2, 1, 1) stands past the wall at the first reads and falls below it within the six intervals run. The clauses: (1) the forward run through the wall takes no refusal; (2) while the tension stands at or past Gamma the Link's factor is 0 at both ends and the plain current reading through it is 0, and the neighbouring Links' factors stand above 0 (the Node steps on its other Links); (3) once the tension falls below Gamma the Link re-couples, its factor above 0 again, by the same read with no act and no log; (4) the run back from the end to the forced state at interval 2 is exact at every interval through the horizon and its dissolution, the whole state's digest equal (the forced state is no step's output, so the run back stops at it) (the bijection: nothing is lost behind the wall, the read being a function of the state the inverse reads alike); (5) the former refusal is gone: the read at a tension past Gamma returns the wall and raises nothing."""

import numpy as np

from event_universe import board_readings, meeting_back, readings, records, world_files
from event_universe.features.read import link_tensions
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import CLUMP, GAMMA, small_world

HERE, NEXT = (
    tuple(CLUMP),
    ((CLUMP[0] + 1) % 3, CLUMP[1], CLUMP[2]),
)  # the Link forced to the wall, along x from the clump


def test_a_link_at_the_wall_decouples_recouples_and_the_run_back_is_exact(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(small_world(tmp_path, detector=False)))
    board.output = lambda line: None
    g, dust = (
        board.held[0],
        [f.name for f in board.families].index("matter"),
    )  # the quanta family reading gravity
    kept = {0: meeting_back.snapshot(board)}
    for _ in range(2):
        board.step()
        kept[board.interval] = meeting_back.snapshot(board)
    line = board.states[g].lines[1]  # gravity's x tension line
    now, before = np.asarray(line.now, dtype=object).copy(), np.asarray(line.before, dtype=object).copy()
    for at in (HERE, NEXT):
        now[at], before[at] = GAMMA + 300, GAMMA + 300
    board.states[g].lines[1] = records.Record(now, before, line.remainder)
    dust_line = board.states[dust].lines[
        0
    ]  # matter lifted at the far end, so that a current stands across the Link
    lifted = np.asarray(dust_line.now, dtype=object).copy()
    lifted[NEXT] = lifted[NEXT] + 100
    board.states[dust].lines[0] = records.Record(
        lifted.astype(dust_line.now.dtype), dust_line.before, dust_line.remainder
    )
    kept[board.interval] = meeting_back.snapshot(board)  # the state the run back returns to
    assert (
        link_tensions([(1, [now, now, now])], board.wrap, GAMMA)[0][HERE] == GAMMA
    )  # (5) read at the wall
    factors, far, currents = [], [], []
    for _ in range(6):  # the reads the step takes, then the step: (1) no refusal
        factors.append(tuple(int(np.asarray(f)[HERE]) for f in board.read(dust)[1]))
        far.append(
            int(np.asarray(board.read(dust)[1][1])[NEXT])
        )  # the -x Port of the far end, the same Link
        ports = board_readings.horizon_ports(board, dust)  # the Links at the wall, the current's mask
        currents.append(None if ports is None else (bool(ports[0][HERE]), bool(ports[1][NEXT])))
        board.step()
        kept[board.interval] = meeting_back.snapshot(board)
    at_wall = [f[0] == 0 for f in factors]
    first_open = at_wall.index(False)
    assert at_wall[0] and not any(at_wall[first_open:]), (
        factors
    )  # (2) decoupled, then (3) re-coupled, once
    assert [f == 0 for f in far] == at_wall, far  # the same Link read at the wall from both ends
    assert all(f[1] > 0 and f[2] > 0 for f in factors), factors  # the Node steps on its other Links
    assert currents[0] == (True, True) and all(c is None for c in currents[first_open:]), currents
    lines = board.lines_of(dust, 0)  # (2) the plain current through the Link at the wall reads 0, masked
    free = readings.currents_of(1, lines, board.wrap)
    masked = readings.currents_of(
        1, lines, board.wrap, horizon=tuple(np.zeros(board.shape, dtype=bool) for _ in range(6))
    )
    assert any(int(np.asarray(f)[HERE]) != 0 for f in free) and [
        np.array_equal(a, b) for a, b in zip(free, masked, strict=True)
    ]
    wall_mask = tuple(
        np.ones(board.shape, dtype=bool) if port == 0 else np.zeros(board.shape, dtype=bool)
        for port in range(6)
    )
    assert int(np.asarray(readings.currents_of(1, lines, board.wrap, horizon=wall_mask)[0])[HERE]) == 0
    end = board.interval
    for k in range(
        end - 2
    ):  # (4) the run back through the horizon and its dissolution, to the forced state at 2
        board.step_inverse()
        assert meeting_back.first_difference(kept[end - k - 1], meeting_back.snapshot(board)) is None, (
            board.interval
        )
    assert board.interval == 2


def test_the_structured_boards_run_back_is_exact_through_a_forced_horizon(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The proof that nothing is lost on the universe test's small structured board (tests/laws_universe.small_world, the 3-cube torus with one clump of matter and uniform light): stepped 20 intervals, a Link beside the clump forced to the wall (gravity's x tension line at the clump's Node and its +x neighbour at Gamma + 300), stepped 8 more through the horizon's standing and its dissolution, and run back to the forced state exact at every interval, the fires mirrored."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(small_world(tmp_path, detector=False)))
    board.output = lambda line: None
    g, quanta = board.held[0], [f.name for f in board.families].index("matter")
    for _ in range(20):
        board.step()
    here, there = tuple(CLUMP), tuple(np.add(CLUMP, (1, 0, 0)) % board.shape[0])
    line = board.states[g].lines[1]
    now, before = np.asarray(line.now, dtype=object).copy(), np.asarray(line.before, dtype=object).copy()
    for at in (here, there):
        now[at], before[at] = GAMMA + 300, GAMMA + 300
    board.states[g].lines[1] = records.Record(now, before, line.remainder)
    kept = {board.interval: meeting_back.snapshot(board)}
    fired = len(board.swaps)
    at_wall = []
    for _ in range(8):
        ports = board_readings.horizon_ports(board, quanta)
        at_wall.append(ports is not None and bool(ports[0][here]))
        board.step()
        kept[board.interval] = meeting_back.snapshot(board)
    assert at_wall[0] and not at_wall[-1], at_wall  # the horizon stands, then dissolves
    forward = [s for s in board.swaps[fired:] if s[1] == 1]
    end = board.interval
    for k in range(8):
        board.step_inverse()
        assert meeting_back.first_difference(kept[end - k - 1], meeting_back.snapshot(board)) is None, (
            board.interval
        )
    assert [(s[0], s[2]) for s in board.swaps if s[1] == -1] == [(s[0], s[2]) for s in forward][::-1]
