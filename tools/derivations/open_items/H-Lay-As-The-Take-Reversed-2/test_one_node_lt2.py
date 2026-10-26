"""The one-Node test of the lay as the take reversed (H-Lay-As-The-Take-Reversed-2): the hole seed on the 5-cube run to its first births (the interval 9) under the flag from the flagged copy; at every birth the far lay writes at exactly the take's Node's six neighbours, each write's quotient q_j against the taken row's record R_j = d before_j holds the Link identity R_j + sense A q_j to a magnitude below A, the remainder written stays within [0, the line's wall at j), and the interval runs back exactly (the state hash before the interval restored). Under 15 s. Run: LT2_LAY_REVERSED=1 PYTHONPATH=/dev/shm/tmp/lt2/src_lt2 pytest -q test_one_node_lt2.py"""
import json
import os
from pathlib import Path

import numpy as np
import pytest

from event_universe.node import Node
from event_universe.take import neighbour

HERE = Path(__file__).resolve()
WORLDS = HERE.parents[4] / "tests" / "worlds"


@pytest.mark.skipif(not os.environ.get("LT2_LAY_REVERSED"), reason="the flag LT2_LAY_REVERSED is empty")
def test_the_lay_is_the_take_reversed_on_one_node() -> None:
    world = json.load(open(WORLDS / "world_hole.json"))
    universe = json.load(open(WORLDS / world["universe"]))
    node = Node(universe, world)
    births = []
    for _ in range(8):
        node.step()
    before_hash = node.state_hash()
    log_from = len(node.log)
    node.step()
    births = [e for e in node.log[log_from:] if e["event"] == "birth"]
    assert births, "the hole seed's first births at the interval 9"
    a_ = node.A
    for e in births:
        at = tuple(e["node"])
        sense = -1 if e["minus"] == e["node"] else 1
        far = e["lay_far"]
        assert len(far) == 6
        wrote = {tuple(x[0]) for x in far}
        assert wrote == {neighbour(node, at, port) for port in range(6)}
        re = node.records()[e["line_pair"]].lines[0]
        for where, r_j, q, rem_was, rest in far:
            assert abs(int(r_j) + sense * a_ * int(q)) < a_
            wall = int(np.asarray(re.wall)[tuple(where)])
            assert 0 <= int(rest) < wall
            assert 0 <= int(rem_was) < wall
    node.step_back()
    assert node.state_hash() == before_hash
