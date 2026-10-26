"""bg1 (H-Birth-At-The-Gradient-1): the fed 3-cube under FR-S1's two lines with the orientation re-read by the Link's gradient (BG1_FORM): the gradient meets where the current is 0 and the paces differ, every one with the twist 0, every one reaching the lay and refused there (the children's plane standing), 0 births, the run back exact. Run: BG1_FORM=1 FR2_RELEASE=1 PYTHONPATH=src_bg1 python -m pytest tests_bg1.py (under 15 s)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src_bg1"))
os.environ["FR2_RELEASE"] = "1"
os.environ["BG1_FORM"] = "1"
sys.set_int_max_str_digits(0)

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

WORLD = os.path.join(HERE, "..", "..", "..", "..", "tests", "worlds", "world_node.json")


def test_gradient_meets_and_the_lay_refuses():
    universe, world = load_world(WORLD)
    node = Node(universe, dict(world, intervals=40))
    car = node.row(CARRIER).lines[0]
    centre = (1, 1, 1)
    car.now[centre], car.before[centre] = 4268834097, 2560000000
    node.start_content, node.start_x = node.content(), car.now
    hashes = []
    for k in range(40):
        if k >= 30:
            hashes.append(node.state_bytes())
        node.step()
    met = node.counts.get("gradient", 0)
    assert met > 0
    assert node.counts.get("gradient_twist_0", 0) == met
    assert node.counts.get("gradient_born", 0) == met
    assert int(node.counts["births"]) == 0
    assert int(node.counts["refused_lay"]) >= met
    assert node.max_transient <= 128
    ok = 0
    for k in range(10):
        node.step_back()
        ok += node.state_bytes() == hashes[9 - k]
    assert ok == 10
