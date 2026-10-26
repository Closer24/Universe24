"""hr2 (H-Horizon-Radiates-2): the test of the row "the horizon radiates" under FR-S1's form (the flag FR2_RELEASE on the flagged copy; on the head the two lines in place): the 3-cube of tests/worlds/world_node.json with its centre fed to the frozen content and its before below it, 40 intervals. What the law does, asserted: (a) no Node is frozen at two intervals in a row (FR-S1); (b) the released centre's content stays between the floor's reflection and the horizon and returns to the horizon (the hover: frozen lines at the centre at least 5 of 40); (c) the content reaches the six neighbours by their own read within two intervals and the neighbours stand at the horizon within ten: the horizon's neighbourhood grows and does not empty; (d) no credit is written at the centre, at its neighbours, or anywhere on the board over the 40 intervals (the law's clicks carry nothing of the horizon); (e) the run back 40 of 40 by the state's hash; (f) every transient within 128 bits. Usage: FR2_RELEASE=1 PYTHONPATH=<src copy> python test_horizon_radiates_hr2.py [world.json]; also collected by pytest."""
import os
import sys
import time

import numpy as np

os.environ.setdefault("FR2_RELEASE", "1")
sys.set_int_max_str_digits(0)
from event_universe.core import paces  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "..", "..", "..", "..", "tests", "worlds", "world_node.json")


def fed_node(world_path, content, before):
    universe, world = load_world(world_path)
    node = Node(universe, world)
    centre = tuple(int(s) // 2 for s in node.shape)

    def level_at(c):
        return int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])

    carrier = node.row(CARRIER).lines[0]
    carrier.now[centre] = level_at(content)
    carrier.before[centre] = level_at(before)
    node.ride_walls()
    light = node.emitter().lines[0]
    light.now[centre] = 4 * int(light.now[centre])
    return node, centre


def neighbours_of(centre, shape):
    out = []
    for ax in range(3):
        for d in (-1, 1):
            q = list(centre)
            q[ax] = (q[ax] + d) % shape[ax]
            out.append(tuple(q))
    return out


def test_the_horizon_radiates_nothing_and_its_neighbourhood_grows(world_path=WORLD, n=40):
    frozen_content = paces.frozen_content(1000)
    node, centre = fed_node(world_path, frozen_content, frozen_content - 93)
    shape = tuple(int(s) for s in node.shape)
    nbs = neighbours_of(centre, shape)
    hashes, prev_frozen, two_in_row = [], set(), 0
    centre_frozen, centre_contents, first_nb_content, nb_at_horizon = 0, [], None, None
    max_transient = 0
    for t in range(n):
        hashes.append(node.state_hash())
        node.step()
        c = node.content()
        pace = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object)
        frozen = {tuple(int(v) for v in idx) for idx in zip(*np.nonzero(pace == 0))}
        two_in_row += len(frozen & prev_frozen)
        prev_frozen = frozen
        centre_frozen += centre in frozen
        centre_contents.append(int(c[centre]))
        if first_nb_content is None and all(int(c[p]) > 0 for p in nbs):
            first_nb_content = node.interval
        if nb_at_horizon is None and all(int(pace[p]) == 0 for p in nbs):
            nb_at_horizon = node.interval
        max_transient = max(max_transient, int(node.max_transient))
    credits = [e for e in node.log if e.get("event") == "credit"]
    exact = 0
    for k in range(n):
        node.step_back()
        exact += node.state_hash() == hashes[n - 1 - k]
    found = {"two in a row": two_in_row, "centre frozen lines": centre_frozen, "centre content min/max": [min(centre_contents), max(centre_contents)], "neighbours read the content at": first_nb_content, "neighbours at the horizon at": nb_at_horizon, "credits": len(credits), "run back": [exact, n], "max transient bits": max_transient}
    assert two_in_row == 0, found  # (a)
    assert centre_frozen >= 5 and min(centre_contents) > 0 and max(centre_contents) >= frozen_content, found  # (b)
    assert first_nb_content is not None and first_nb_content <= 2, found  # (c) the content reaches the neighbours by their own read
    assert nb_at_horizon is not None and nb_at_horizon <= 10, found  # (c) the neighbourhood grows to the horizon
    assert len(credits) == 0, found  # (d)
    assert exact == n, found  # (e)
    assert max_transient <= 128, found  # (f)
    return found


if __name__ == "__main__":
    t0 = time.monotonic_ns()
    found = test_the_horizon_radiates_nothing_and_its_neighbourhood_grows(sys.argv[1] if len(sys.argv) > 1 else WORLD)
    print(found, "ms", (time.monotonic_ns() - t0) // 1000000)
