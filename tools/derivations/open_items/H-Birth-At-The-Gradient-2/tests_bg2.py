"""bg2 (H-Birth-At-The-Gradient-2): the gradient as the orientation at a Link where the record carries no current, on the fed 3-cube under FR-S1 and BG2_FORM for 30 intervals (the copy src_bg2 beside this file): the Link's pace difference read at meetings refused by the orientation on the head (met_gradient above 0), the number drawn at the faster end at every one, the lay refused where the children's plane already stands (the standing sea), births 0 and the record's clicks the head's; the transient within 128 bits; the run back exact 10 of 10. Run: FR2_RELEASE=1 BG2_FORM=1 python tests_bg2.py (under 15 s)."""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["FR2_RELEASE"] = "1"
os.environ["BG2_FORM"] = "1"
sys.path.insert(0, os.path.join(HERE, "src_bg2"))
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402

from event_universe import close  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402


def test_gradient_meets_and_the_lay_refuses() -> None:
    t0 = time.time()
    universe, world = load_world(os.path.join(HERE, "..", "..", "..", "..", "tests", "worlds", "world_node.json"))
    n, back = 30, 10
    node = Node(universe, dict(world, intervals=n))
    centre = tuple(s // 2 for s in node.shape)
    car = node.row(CARRIER).lines[0]
    car.now[centre], car.before[centre] = 4268834097, 2560000000
    node.start_content, node.start_x = node.content(), car.now
    assert close.BG2_FORM
    met_gradient = drawn = twist = sense = 0
    lay_before = int(node.counts["refused_lay"])
    hashes = []
    frozen_twice, releases, frozen_last = 0, 0, set()
    for k in range(n):
        if k >= n - back:
            hashes.append(node.state_bytes())
        close.BG2.update({"met_gradient": 0, "twist_nonzero": 0, "sense_opposite": 0, "drawn": 0, "clock_apart_only": 0, "born": []})
        node.step()
        met_gradient += close.BG2["met_gradient"]
        drawn += close.BG2["drawn"]
        twist += close.BG2["twist_nonzero"]
        sense += close.BG2["sense_opposite"]
        for at, j, rec, g, into in close.BG2["born"]:
            assert g != 0 and (tuple(into) == tuple(j)) == (g > 0), "the + child at the faster end"
        pace = np.asarray(paces.link_pace_of(node.gamma, node.content()), dtype=object)
        frozen_now = {tuple(int(x) for x in w) for w in zip(*np.nonzero(pace == 0))}
        frozen_twice += len(frozen_now & frozen_last)
        releases += len(frozen_last - frozen_now)
        frozen_last = frozen_now
    assert frozen_twice == 0 and releases >= 3, (frozen_twice, releases)
    assert met_gradient > 0 and drawn == met_gradient, (met_gradient, drawn)
    assert twist == 0 and sense == 0, (twist, sense)
    assert int(node.counts["refused_lay"]) - lay_before >= met_gradient, (node.counts["refused_lay"], met_gradient)
    assert int(node.counts["births"]) == 0
    assert int(node.max_transient) <= 128
    ok = 0
    for k in range(back):
        node.step_back()
        ok += node.state_bytes() == hashes[back - 1 - k]
    assert ok == back, (ok, back)
    print({"met_gradient": met_gradient, "drawn": drawn, "refused_lay": int(node.counts["refused_lay"]), "births": int(node.counts["births"]), "releases": releases, "transient": int(node.max_transient), "run back": [ok, back], "seconds": int(time.time() - t0)})


if __name__ == "__main__":
    test_gradient_meets_and_the_lay_refuses()
