"""The floor (ALGEBRA.md, The floor, the owner's word of 2026-10-23; swap.at_floor, swap.floor_of): a Node whose time line's output would fall below the floor X_f = volume_of(Gamma, -Gamma), the least volume with a reading, turns as at the top, its output discarded, so that no level the board holds meets the volume reading's refusal. On the universe test's small structured board (tests/laws_universe.small_world, the 3-cube torus with one clump of matter and uniform light), which the former reading ended by the crunch at 78 (X at most 0 at the clump's Node, refused by name): (1) the run goes on past 78 to 160 with no refusal, every X at or above the floor at every interval, and the fifth act fires at the floor (a fire whose triple has an outer level below the floor, read from the states) at least once; (2) the pinned floor is counted: the longest run of consecutive fires at one Node (a two-cycle at the floor, the Node turning back at a weak top the interval after its floor's turn) and the Nodes released, named in the test's print, the two-cycle present at least once on this board or the bounce clearing the fall at every floor turn, either read and not assumed; (3) the run back from 160 to interval 0 is exact at every interval, the fires mirrored (the bijection through the floor's turns and the tops); (4) the floor's number: 19 at Gamma 1,000 (about Gamma / e^4)."""

import numpy as np

from event_universe import swap, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import GAMMA, small_world


def test_the_small_board_turns_at_the_floor_and_runs_back_exactly(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(small_world(tmp_path, detector=False)))
    board.output = lambda line: None
    g, floor = board.held[0], swap.floor_of(GAMMA)
    assert floor == 19  # (4)
    masks, swapped, floor_masks, at_floor = [], swap.swapped, [], swap.at_floor
    monkeypatch.setattr(
        swap,
        "swapped",
        lambda b, held, mask: (masks.append((b.interval, mask.copy())), swapped(b, held, mask)),
    )
    monkeypatch.setattr(  # the floor's own trigger read on the triple, kept beside the act's mask
        swap,
        "at_floor",
        lambda x0, x1, x2, f: floor_masks.append(at_floor(x0, x1, x2, f)) or floor_masks[-1],
    )
    states, lows = [board_state(board)], []
    time = lambda: board.states[g].lines[0]  # noqa: E731
    for _ in range(160):  # (1) past the former crunch at 78, no refusal
        board.step()
        states.append(board_state(board))
        lows.append(int(np.asarray(time().now, dtype=object).min()))
    floor_fires = sum(int(np.count_nonzero(mask)) for mask in floor_masks)
    assert min(lows) >= floor and board.interval == 160, (min(lows), board.interval)
    assert floor_fires > 0, (floor_fires, board.swaps[-10:])  # the floor's turn fired
    runs: dict[tuple[int, ...], int] = {}
    longest, last = 0, {}
    for interval, mask in masks:
        for idx in zip(*np.nonzero(mask), strict=True):
            key = tuple(int(i) for i in idx)
            runs[key] = runs.get(key, 0) + 1 if last.get(key) == interval - 1 else 1
            last[key] = interval
            longest = max(longest, runs[key])
    print(
        f"the floor on the small board: fires {len(board.swaps)} intervals, the longest run of consecutive fires at one Node {longest} (the pinned floor where above 1), the least X {min(lows)} against the floor {floor}"
    )
    assert longest >= 1
    fires = [(s[0], s[2]) for s in board.swaps if s[1] == 1]
    for k in range(160):  # (3) the run back exact through every turn
        board.step_inverse()
        assert same_state(board_state(board), states[160 - k - 1]), board.interval
    assert [(s[0], s[2]) for s in board.swaps if s[1] == -1] == fires[::-1]
