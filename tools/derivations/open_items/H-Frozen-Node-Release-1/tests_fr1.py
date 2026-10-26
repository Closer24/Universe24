"""fr1's test on the flagged COPY (src_fr1, the flag FR1_RELEASE set here): the frozen Node released by the turn of its own time (FR-S1). The 3-cube's centre fed to the frozen content 3,793 at Gamma 1,000 (X 4,268,834,097) with a velocity (its before slot at the content 3,700, X 2,560,000,000), 20 intervals: at the first interval the centre is frozen (the Link pace 0, its six factors 0, its clock standing) and turned by the swap's own trigger (the restored line a weak maximum, before < now = after); at the second its levels are the exchanged pair (now the former before, below the frozen content), the Link pace above 0, the clock running; no Node is frozen at two intervals in a row; 0 clicks at the centre; every integer within 128 bits; the run back exact 20 of 20. Under 15 s. Run: FR1_RELEASE=1 python -m pytest tests_fr1.py (or python tests_fr1.py)."""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src_fr1"))
os.environ["FR1_RELEASE"] = "1"
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402

from event_universe.core import paces  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

CENTRE = (1, 1, 1)


def level_at(node: Node, content: int) -> int:
    return int(np.asarray(volume.volume_of(node.gamma, np.array([content], dtype=object)), dtype=object).reshape(-1)[0])


def fed_node() -> Node:
    universe, world = load_world(os.path.join(HERE, "worlds", "world_node.json"))
    node = Node(universe, world)
    carrier = node.row(CARRIER).lines[0]
    carrier.now[CENTRE] = level_at(node, paces.frozen_content(node.gamma))
    carrier.before[CENTRE] = level_at(node, 3700)
    node.ride_walls()
    light = node.emitter().lines[0]
    light.now[CENTRE] = 4 * int(light.now[CENTRE])
    return node


def test_the_frozen_node_is_released_by_the_turn_of_its_time_fr_s1() -> None:
    node = fed_node()
    carrier = node.row(CARRIER).lines[0]
    x_now, x_before = int(carrier.now[CENTRE]), int(carrier.before[CENTRE])
    assert (x_now, x_before) == (4_268_834_097, 2_560_000_000)
    kept = copy.deepcopy(node)
    hashes = []
    frozen_before = False
    for i in range(20):
        content = node.content()
        pace = int(paces.link_pace(node.gamma, int(content[CENTRE])))
        frozen_now = np.asarray(paces.link_pace_of(node.gamma, content), dtype=object) == 0
        assert not (frozen_before and frozen_now[CENTRE]), "frozen at two intervals in a row"
        frozen_before = bool(frozen_now[CENTRE])
        proper = int(node.proper[CENTRE])
        hashes.append(node.state_hash())
        node.step()
        carrier = node.row(CARRIER).lines[0]
        if i == 0:
            assert pace == 0 and node.turned[CENTRE] and int(node.proper[CENTRE]) == proper
            assert all(int(f[CENTRE]) == 0 for f in node.link_factors(None, frozen_now))
            assert (int(carrier.now[CENTRE]), int(carrier.before[CENTRE])) == (x_before, x_now)
        if i == 1:
            assert pace > 0 and int(node.proper[CENTRE]) > proper
            assert int(carrier.now[CENTRE]) - int(carrier.before[CENTRE]) < 0
    assert [e for e in node.log if tuple(e["node"]) == CENTRE and e["event"] in ("birth", "credit")] == []
    assert node.max_transient <= 128 and node.census()[1] <= 128
    exact = 0
    for k in range(20):
        node.step_back()
        exact += node.state_hash() == hashes[19 - k]
    assert exact == 20
    del kept


if __name__ == "__main__":
    import time

    t = time.time()
    test_the_frozen_node_is_released_by_the_turn_of_its_time_fr_s1()
    print("ok", round(time.time() - t, 1), "s")
