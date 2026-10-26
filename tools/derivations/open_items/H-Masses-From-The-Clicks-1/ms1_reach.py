"""ms1: the one-Link reach on the engine or ms1's flagged copy (by PYTHONPATH): two boards run alike to an interval, one light level changed at a Node on one, both stepped once; the distances at which the states differ (tests/test_the_node.differences) must lie within {0, 1}; backward within {0}.
Usage: python ms1_reach.py <world.json> <intervals before the change>"""
import copy
import json
import sys

sys.set_int_max_str_digits(0)

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import PLANE  # noqa: E402
from tests.test_the_node import differences  # noqa: E402


def main():
    universe, world = load_world(sys.argv[1])
    before = int(sys.argv[2])
    a = Node(universe, world)
    for _ in range(before):
        a.step()
    at = tuple(int(x) // 2 for x in world["shape"])
    b = copy.deepcopy(a)
    light = b.row(PLANE, gap=0).lines[0]
    light.now[at] = light.now[at] + 1
    d0 = sorted(differences(a, b, at))
    a.step()
    b.step()
    d1 = sorted(differences(a, b, at))
    a2, b2 = copy.deepcopy(a), copy.deepcopy(a)
    light = b2.row(PLANE, gap=0).lines[0]
    light.now[at] = light.now[at] + 1
    a2.step_back()
    b2.step_back()
    d2 = sorted(differences(a2, b2, at))
    print(
        json.dumps(
            {
                "world": sys.argv[1],
                "changed at": list(at),
                "interval": before,
                "distances differing before the step": d0,
                "after one step forward": d1,
                "after one step back": d2,
                "births a / b": [a.counts["births"], b.counts["births"]],
                "reach forward within one Link": d1 == [0] or d1 == [0, 1] or d1 == [1],
                "reach backward within the Node": d2 in ([], [0]),
            }
        )
    )


if __name__ == "__main__":
    main()
