"""The swap at the top on a STRUCTURED board (ALGEBRA.md, The swap at the top; swap.py, the interval's fifth act; the structured-board hand's clauses): on the three-clump lay (examples/events/cycle/three_clumps.json, the 5-cube torus at Gamma 1,000, gravity gapped [999, 1000], three matter clumps on z) every Node turns at its own top and its neighbours read its levels as they stand. The clauses over the first 60 intervals: (1) no refusal by name; (2) X at or above Gamma at every Node (the pinned rest of the void Nodes: the seed is the floor over the staggered turns); (3) the fires 122, 108, 76, 36, 8 at intervals 1 to 5, each at a weak maximum of the Node's own time line, every Node's level before after the interval the level it started with; (4) the run back 60 of 60 exact with the inverse firing (5, 8), (4, 36), (3, 76), (2, 108), (1, 122)."""

from pathlib import Path

import numpy as np

from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import state_of

GAMMA, INTERVALS = 1000, 60
WORLD = Path(__file__).resolve().parent.parent / "examples" / "events" / "cycle" / "three_clumps.json"


def same(a, b):  # type: ignore[no-untyped-def]
    return all(
        all(np.array_equal(u, v) for x, y in zip(la, lb, strict=True) for u, v in zip(x, y, strict=True))
        and all(np.array_equal(u, v) for u, v in zip(ra, rb, strict=True))
        for (la, ra), (lb, rb) in zip(a, b, strict=True)
    )


def test_the_swap_on_a_structured_board() -> None:
    board = Lattice(load_world(WORLD))
    board.output = lambda line: None
    g = [i for i in board.held if board.families[i].motion_volume][0]
    objects = lambda a: np.asarray(a, dtype=object)  # noqa: E731
    states = {0: state_of(board)}
    levels = {
        0: (
            objects(board.states[g].lines[0].now).copy(),
            objects(board.states[g].lines[0].before).copy(),
        )
    }
    x_min = []
    for t in range(1, INTERVALS + 1):
        board.step()  # clause (1): no refusal by name
        states[t] = state_of(board)
        now, before = objects(board.states[g].lines[0].now), objects(board.states[g].lines[0].before)
        levels[t] = (now.copy(), before.copy())
        x_min.append(int(now.min()))
    assert min(x_min) >= GAMMA, (
        min(x_min),
        x_min,
    )  # clause (2): the seed is the floor over the staggered turns
    fires = {s[0]: s[2] for s in board.swaps if s[1] == 1}
    assert fires == {1: 122, 2: 108, 3: 76, 4: 36, 5: 8}, (
        fires
    )  # the pinned rest at the void Nodes, staggered over five intervals
    for t in range(
        1, INTERVALS + 1
    ):  # clause (3): a fired Node is at a weak maximum of its own time line, read from the levels kept: (X0, X1) the pre-state, X2 the step's output, which the act replaced by X0; so the post-state's (now, before) is (X0, X1) with X0 <= X1, and an unfired Node's post-state has before == the pre-state's now
        pre_now, pre_before = levels[t - 1]
        post_now, post_before = levels[t]
        assert np.array_equal(post_before, pre_now), (
            t
        )  # every Node's `before` after the interval is the level it started with, fired or not (the swap keeps X1 as before: (before, now) = (X1, X0))
        if (
            t in fires
        ):  # a fired Node ends at (X0, X1) with X0 <= X1: the Nodes standing at their own level before, at or below the level they started with, are at least the fired ones (at the pinned rest, X0 == X1 == X2, exactly them)
            standing = int(np.sum((post_now == pre_before) & (pre_before <= pre_now)))
            assert standing >= fires[t], (t, standing, fires[t])
            if t <= 5:
                assert standing == fires[t], (t, standing, fires[t])
    exact = 0
    for k in range(INTERVALS):
        board.step_inverse()
        exact += same(state_of(board), states[INTERVALS - k - 1])
    assert exact == INTERVALS, exact  # clause (4): the run back exact through every staggered fire
    back = [(s[0], s[2]) for s in board.swaps if s[1] == -1]
    assert back == [(5, 8), (4, 36), (3, 76), (2, 108), (1, 122)], back


def test_the_shipped_course_log_of_the_three_clumps_records_the_cut_at_2376_and_the_returns() -> None:
    """The structured board's long course under the law with both acts, read from the shipped course log (examples/events/cycle/three_clumps.course.jsonl, the structured-cycle branch, 2026-10-23): 2,376 intervals run and the cut at the read of 2,376 by a Link's tension 1,087 above Gamma 1,000; the void's returns at 624, 1,183, 1,738 and 2,374 with X 7,607, 5,430, 22,139 and 7,479, never the crunch; 1,079 fires; the largest Link tension 975 at 2,375."""
    import json

    rows = [
        json.loads(line)
        for line in (WORLD.parent / "three_clumps.course.jsonl").read_text().splitlines()
    ]
    body = [row for row in rows if "t" in row]
    summary = rows[-1]["summary"]
    assert summary["intervals_run"] == 2376 and "tension 1087 exceeds Gamma 1000" in summary["refused"]
    assert summary["fires_total"] == 1079 == sum(row["fires"] for row in body)
    minima = [
        (row["t"], row["X_min"])
        for row in body
        if row["t"] > 10
        and row["X_min"] < 100_000
        and row["X_min"] == min(r["X_min"] for r in body[max(0, row["t"] - 60) : row["t"] + 60])
    ]
    assert minima == [(624, 7607), (1183, 5430), (1738, 22139), (2374, 7479)]
    assert (
        min(row["X_min"] for row in body if row["t"] > 10) == 5430 > 0
    )  # the seed's floor only at the start
    largest = [
        row.get("link_t_max", 0) for row in body
    ]  # the last row carries the refusal in place of the read
    assert max(largest) == 975 and largest[2375] == 975
