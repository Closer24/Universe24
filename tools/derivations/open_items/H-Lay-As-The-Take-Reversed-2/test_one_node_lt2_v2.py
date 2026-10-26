"""The one-Node test of the lay as the take reversed, the mended form (H-Lay-As-The-Take-Reversed-2, v2: one carried division per far Node per close): the hole seed on the 5-cube run to its first births (the interval 9) under the flag from the flagged copy /dev/shm/tmp/lt2b/src_lt2b; at every birth the reads name exactly the take's Node's six neighbours; the close writes once per far Node, the quotient q against the summed record S = SUM -sense R_j holding |A q - S| < A; every remainder written stays within [0, the line's wall at the Node); the interval runs back exactly (the state hash before it restored). Under 15 s. Run: LT2_LAY_REVERSED=1 PYTHONPATH=/dev/shm/tmp/lt2b/src_lt2b pytest -q -c /dev/null --rootdir <this folder> test_one_node_lt2_v2.py"""
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
def test_the_lay_is_the_take_reversed_once_per_far_node() -> None:
    world = json.load(open(WORLDS / "world_hole.json"))
    universe = json.load(open(WORLDS / world["universe"]))
    node = Node(universe, world)
    for _ in range(8):
        node.step()
    before_hash = node.state_hash()
    log_from = len(node.log)
    node.step()
    births = [e for e in node.log[log_from:] if e["event"] == "birth"]
    assert births, "the hole seed's first births at the interval 9"
    a_ = node.A
    sums: dict[tuple[int, tuple[int, ...]], int] = {}
    for e in births:
        at = tuple(e["node"])
        sense = -1 if e["minus"] == e["node"] else 1
        reads = e["far_records"]
        assert len(reads) == 6
        assert {tuple(x[0]) for x in reads} == {neighbour(node, at, port) for port in range(6)}
        for where, r_j, _total in reads:
            key = (int(e["line_pair"]), tuple(where))
            sums[key] = sums.get(key, 0) - sense * int(r_j)
    written = [e for e in births if "lay_far" in e]
    assert len(written) == 1, "one write list per close, on the close's last birth line"
    far = written[0]["lay_far"]
    assert {(int(s), tuple(w)) for s, w, *_ in far} == set(sums)
    for s, where, _total, q, rem_was, rest in far:
        key = (int(s), tuple(where))
        assert abs(a_ * int(q) - sums[key]) < a_
        wall = int(np.asarray(node.records()[int(s)].lines[0].wall)[tuple(where)])
        assert 0 <= int(rest) < wall
        assert 0 <= int(rem_was) < wall
    node.step_back()
    assert node.state_hash() == before_hash
