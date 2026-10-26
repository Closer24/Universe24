"""One Node (the 3-cube, tests/worlds/world_node.json), under 15 s: a merger's light at an end whose named line has no direction
(fall_of names the im line, its gap 0 being the largest where re_now^2 < re_before^2) is laid by merger.light_children as the charged
child's lay (merger.py, rise_of's `if now == before: return k, 0, 0` and light_children's `if d == 0: child_at`), so the merger's two
children carry the Wronskian -T div 2 + 0, not 0. The law's letter: the merger's children are light, laid as the exact take at -1
on one line (their own W 0) at both ends; the born pair's charges sum to 0 (ALGEBRA.md, The charge at the click). Fails on the head
(toys-5 3dc12e307); passes on the flagged copy with CC1_LIGHT_EXACT set (the tie now == before resolved by rise_of's own u).
The levels are the chiral 60's birth at the interval 10 (the engine's log: stood [939, 1175, 0, 0] and [1329, 1112, 0, 0]).
Run: PYTHONPATH=<src> pytest -q test_children_charge_cc1.py (the src the worktree's, or /dev/shm/tmp/cc1/src_cc1 with the flag)."""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
WORKTREE = HERE.parents[4]
sys.path.insert(0, str(WORKTREE / "tests"))

from event_universe import readings  # noqa: E402
from event_universe.core import rule3  # noqa: E402
from event_universe.merger import light_children, walls_of  # noqa: E402
from laws import node_of  # noqa: E402


def test_the_merger_lays_light_of_no_charge_at_both_ends() -> None:
    node = node_of("world_node.json")
    node.step()
    s = 0
    row = node.records()[s]
    assert row.pair is not None
    minus, plus = (1, 1, 1), (1, 1, 2)
    node.lay(s, minus, (939, 1175, 0, 0))
    node.lay(s, plus, (1329, 1112, 0, 0))
    c = node.start_content
    factors = node.link_factors(None, readings.frozen_of(node, c))
    rule = node.rule(row.pair, c, factors)
    walls = list(walls_of(node, s, minus, plus, rule, {}))
    A, B = (int(x) for x in rule3.balanced_pair(rule3.half(node.T)))
    _dp, w_after, stood, exact, _ends = light_children(node, s, minus, plus, walls, rule)
    own = [0 if exact[end] is not None else sense * A * B for end, sense in ((0, -1), (1, 1))]
    import event_universe.merger as m_
    print(json.dumps(dict(flag=os.environ.get("CC1_LIGHT_EXACT", ""), src=m_.__file__, walls=walls, exact=exact, stood=stood, W_after=w_after, W_own=own)))
    assert all(x is not None for x in exact), f"a merger end laid as the charged child's lay: exact {exact}, W own {own}"
    assert sum(own) == 0
