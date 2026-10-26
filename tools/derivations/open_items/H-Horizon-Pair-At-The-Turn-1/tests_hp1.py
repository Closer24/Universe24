"""hp1 (H-Horizon-Pair-At-The-Turn-1): two readings of the letter on the copy with FR-S1's two lines (FR2_RELEASE=1): (1) the carrier's rule (node.rule_of on the shape-10 row at its pair (den - den div Gamma, den)) carries Rule3's six reaches 2 num p_i^2 Q_ij, 2 num Gamma^2 G^2 at the vacuum, 2 num G^2 one below the horizon (the Link pace 1), 0 at the horizon (the Link pace 0): the Link term is in the letter and closed by the Node's own pace; (2) on the fed 3-cube (the centre at the frozen content, its before at 3,700) the released centre and its neighbours stand on the gap-0 row with a current on the Link and the twist 0, so the close refuses the birth by name `twist` and births 0; the run back exact; 128 bits. Run from the hand's folder: python tests_hp1.py (or pytest -o pythonpath= tests_hp1.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["FR2_RELEASE"] = "1"
sys.path.insert(0, os.path.join(HERE, "src_hp1"))
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER
from event_universe.features import volume
from event_universe.core import paces
from event_universe import readings

WORLD = os.path.join(HERE, "..", "H-Frozen-Node-Release-1", "worlds", "world_node.json")


def test_carrier_link_term_in_the_letter():
    u, w = load_world(WORLD); node = Node(u, w); car = node.row(CARRIER)
    assert car.wall is None and car.pair == (node.den - node.den // node.gamma, node.den)
    num = car.pair[0]; G2 = node.G * node.G
    for c, pace, expect in ((0, node.gamma, 2 * num * node.gamma * node.gamma * G2), (3792, 1, 2 * num * G2), (3793, 0, 0), (3837, 0, 0)):
        cc = np.full(node.shape, c, dtype=object)
        r = node.rule_of(car, cc, node.link_factors(None, None))
        assert int(np.asarray(readings.paces_of(node, cc)[1]).reshape(-1)[0]) == pace
        assert all(int(np.asarray(x).reshape(-1)[0]) == expect for x in r.reaches), (c, expect)
        assert int(r.wall) == node.w and int(np.asarray(r.mass).reshape(-1)[0]) > 0


def test_no_birth_at_the_turn_the_twist_refuses():
    u, w = load_world(WORLD); node = Node(u, w); centre = (1, 1, 1); car = node.row(CARRIER).lines[0]
    lv = lambda c: int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])
    car.now[centre] = lv(3793); car.before[centre] = lv(3700); node.ride_walls()
    light = node.emitter().lines[0]; light.now[centre] = 4 * int(light.now[centre])
    rec = node.records().index(node.emitter()); unit = node.units[rec]
    hashes = []; released_standing = 0; frozen_twice = 0; prev_frozen = np.zeros(node.shape, dtype=bool); prev_turned = prev_frozen
    for t in range(24):
        c = readings.content(node); frozen = readings.frozen_of(node, c)
        assert not (frozen & prev_frozen).any()
        sh = node.share(node.emitter().lines, node.rule(node.emitter().pair, c, node.link_factors(None, frozen)))
        if prev_turned[centre] and not frozen[centre] and int(sh[centre]) >= unit:
            released_standing += 1
        hashes.append(node.state_hash() if hasattr(node, "state_hash") else repr([(l.now.tolist(), l.before.tolist(), l.rem.tolist()) for l in node.all_lines()]))
        node.step(); prev_turned = np.asarray(node.turned, dtype=bool) & frozen; prev_frozen = frozen
    assert released_standing >= 3
    assert int(node.counts["refused_twist"]) > 0 and int(node.counts["births"]) == 0 and int(node.counts["body_clicks"]) == 0
    assert int(node.counts["refused_orientation"]) > 0
    assert node.max_transient <= 128
    for t in range(24):
        node.step_back()
        h = node.state_hash() if hasattr(node, "state_hash") else repr([(l.now.tolist(), l.before.tolist(), l.rem.tolist()) for l in node.all_lines()])
        assert h == hashes[23 - t], t


if __name__ == "__main__":
    import time
    t0 = time.time(); test_carrier_link_term_in_the_letter(); test_no_birth_at_the_turn_the_twist_refuses(); print("hp1 tests passed in", int((time.time() - t0) * 1000), "ms")
