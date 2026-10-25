"""EQ-S1's test (eq1, 2026-10-25; under 15 s): run with PYTHONPATH=<this folder>/src_eq1 and EQ1_LAW=b0 (the flagged copy; David's build needs no flag).

(1) The uniform pair on the 3-cube (tests/worlds/world_pair_3.json) to 20 intervals: at every Node the gap-0 line's current is 0 on every Link at every interval's start (nothing arrives), every credit carries `laid_back` equal to its `levels`, and the gap-0 line's level now at the credited Node after the close equals the credit's `taken_now_was` (the board as if untaken: the light whole at every Node), the credits 27 at each of the intervals 4, 6 and 8 (81 in all; the head's board, its light taken, credits at 10 and 13 too), no closing at 10 or 13 on the untaken board (the head's board, its light taken, credits there too), the run back exact 10 of 10.
(2) The hole seed on the 5-cube (world_hole.json) to 20 intervals: every credit stands at a Node where the gap-0 line's current on some Link is not 0 (something arrives), no credit carries `laid_back`, the credits and births the head's (pinned below from the head's run of this script's date), the run back exact 10 of 10."""
import os
import sys
from pathlib import Path

os.environ.setdefault("EQ1_LAW", "b0")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src_eq1"))
sys.path.insert(0, str(HERE.parents[2]))
from event_universe.bodies import EQ1_LAW, eq1_arrival  # noqa: E402
from event_universe.rows import PLANE  # noqa: E402
from tests.laws import node_of, run_back_exact  # noqa: E402

import numpy as np  # noqa: E402

HEAD_HOLE_20 = (40, 16)  # the head's credits and births on the hole seed at 20 (pinned from the head's run, eq1_REPORT.md section 3)


def arrivals(node):
    rec0 = node.records().index(node.row(PLANE, gap=0))
    lines = node.records()[rec0].lines
    return {at: eq1_arrival(node, at, [lines] * (rec0 + 1)) for at in np.ndindex(*node.shape)}


def credits_of(node, seen):
    return [e for e in node.log[seen:] if e["event"] == "credit"]


def test_the_uniform_pair_takes_what_it_lays_back_and_the_light_stays_whole():
    assert EQ1_LAW == "b0"
    node = node_of("world_pair_3.json")
    kept = node_of("world_pair_3.json")
    by_interval = {}
    for _ in range(20):
        assert set(arrivals(node).values()) == {0}
        seen = len(node.log)
        node.step()
        gap0 = node.row(PLANE, gap=0).lines[0]
        for c in credits_of(node, seen):
            assert c["laid_back"] == c["levels"] > 0
            assert int(gap0.now[tuple(c["node"])]) == c["taken_now_was"]
            assert [a + b for a, b in zip(c["dP_take"], c["dP_back"], strict=True)] == [0, 0, 0]
        by_interval[node.interval] = len(credits_of(node, seen))
    assert {i: n for i, n in by_interval.items() if n} == {4: 27, 6: 27, 8: 27}
    assert node.counts["refused_stop"] == 0 and node.counts["births"] == 0
    assert run_back_exact(kept, 10) == 10


def test_the_hole_seed_takes_where_light_arrives_as_the_head_does():
    node = node_of("world_hole.json")
    kept = node_of("world_hole.json")
    credits = 0
    for _ in range(20):
        arriving = arrivals(node)
        seen = len(node.log)
        node.step()
        for c in credits_of(node, seen):
            assert arriving[tuple(c["node"])] > 0 and "laid_back" not in c
            credits += 1
    assert (credits, node.counts["births"]) == HEAD_HOLE_20
    assert run_back_exact(kept, 10) == 10
