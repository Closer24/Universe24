"""fr2: the frozen Node's release by the turn of its own time (FR-S1), run against the flagged src with FR2_RELEASE set: the 3-cube's centre fed to the frozen content with its before slot one step below (a Node that rose into the horizon), 12 intervals: frozen at the start of interval 1 and turned at its end (the swap's own trigger, the hold making the weak maximum X0 < X1 = X2), its content below the frozen content from interval 1 and its clock running again at interval 2, every integer within 128 bits, the run back exact 12 of 12; and the standing Node (before = now) frozen at every interval as BH-S1's test has it (no drift to turn). Usage: PYTHONPATH=src_fr2 FR2_RELEASE=1 python -m pytest -c /dev/null -p no:cacheprovider tests_fr2.py -q (the -c /dev/null keeps the worktree pyproject from putting the head src first)"""
import copy
import os
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.core import paces  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "..", "..", "..", "..", "tests", "worlds", "world_node.json")
CENTRE = (1, 1, 1)


def level_at(node, c):
    return int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])


def fed(before_content):
    universe, world = load_world(WORLD)
    node = Node(universe, world)
    frozen = paces.frozen_content(node.gamma)
    carrier = node.row(CARRIER).lines[0]
    carrier.now[CENTRE] = level_at(node, frozen)
    carrier.before[CENTRE] = level_at(node, before_content)
    node.ride_walls()
    light = node.emitter().lines[0]
    light.now[CENTRE] = 4 * int(light.now[CENTRE])
    return node, frozen


def run_back(node, n):
    states = []
    for _ in range(n):
        states.append(node.state_bytes())
        node.step()
    return sum(node.state_bytes() == states[n - 1 - k] for k in range(n) if not node.step_back())


def test_the_frozen_node_that_rose_in_is_turned_at_its_freeze_and_released_fr_s1():
    assert os.environ.get("FR2_RELEASE"), "the flag FR2_RELEASE must be set for the release"
    node, frozen = fed(3700)
    kept = copy.deepcopy(node)
    proper0 = int(node.proper[CENTRE])
    frozen_at_start = []
    for _ in range(12):
        c = node.content()
        frozen_at_start.append(bool(np.asarray(paces.link_pace_of(node.gamma, c), dtype=object)[CENTRE] == 0))
        node.step()
        if node.interval == 1:
            assert frozen_at_start[-1] and bool(node.turned[CENTRE])  # frozen at the start, turned at the end: the release at the freeze interval
            assert int(node.proper[CENTRE]) == proper0  # the clock stood through the frozen interval
            assert int(node.content()[CENTRE]) < frozen  # the content below the horizon after the exchange
        if node.interval == 2:
            assert not frozen_at_start[-1] and int(node.proper[CENTRE]) > proper0  # the clock runs again
    assert node.max_transient <= 128 and node.census()[1] <= 128
    assert run_back(kept, 12) == 12


def test_the_standing_frozen_node_has_no_drift_to_turn_and_stays_as_bh_s1_has_it():
    node, frozen = fed(3793)
    kept = copy.deepcopy(node)
    fed_lines = [[int(a[CENTRE]) for a in (line.now, line.before, line.rem)] for line in node.all_lines()]
    for _ in range(12):
        node.step()
        assert [[int(a[CENTRE]) for a in (line.now, line.before, line.rem)] for line in node.all_lines()] == fed_lines
        assert not node.turned[CENTRE]
    assert run_back(kept, 12) == 12
