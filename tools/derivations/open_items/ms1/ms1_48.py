"""ms1: the cube's 48 on the clicks of the engine (or of ms1's flagged copy, by PYTHONPATH): the world run from its seed and from each of its 48 images (the signed permutations about the origin, tests/test_the_board.py's IMAGES), the birth lines compared through the image (interval, the take's Node, the plane, the two children's Nodes, the two children's W, the amplitude), a reflection with the children's ends exchanged and the senses exchanged (W negated per end).
Usage: python ms1_48.py <world.json> <intervals> ; integers only."""
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from tests.test_the_board import IMAGES, image, world_image  # noqa: E402


def births_of(node, m, cube, reflection):
    found = []
    for e in node.log:
        if e["event"] != "birth":
            continue
        at = image(m, tuple(e["node"]), cube)
        mi, pl = image(m, tuple(e["minus"]), cube), image(m, tuple(e["plus"]), cube)
        wm, wp = e["W_children"]
        if reflection:
            mi, pl, wm, wp = pl, mi, -wp, -wm
        found.append((e["i"], at, e["line_pair"], mi, pl, wm, wp, e["amplitude"]))
    return sorted(found)


def main():
    universe, world = load_world(sys.argv[1])
    intervals = int(sys.argv[2])
    cube = int(world["shape"][0])
    world = dict(world, intervals=intervals)

    def run(w):
        node = Node(json.loads(json.dumps(universe)), w)
        for _ in range(intervals):
            node.step()
        return node

    base = run(world_image(world, np.eye(3, dtype=int), cube))
    births = births_of(base, np.eye(3, dtype=int), cube, False)
    equal = apart = 0
    apart_list = []
    for m in IMAGES:
        other = run(world_image(world, m, cube))
        reflection = int(round(np.linalg.det(m))) == -1
        mapped = births_of(base, m, cube, reflection)
        if births_of(other, np.eye(3, dtype=int), cube, False) == mapped:
            equal += 1
        else:
            apart += 1
            apart_list.append(m.tolist())
    print(
        json.dumps(
            {
                "world": sys.argv[1],
                "intervals": intervals,
                "births": len(births),
                "W per child (distinct |W|)": sorted({abs(w) for b in births for w in (b[5], b[6])}),
                "images equal through the image (reflections with the ends and the senses exchanged)": equal,
                "apart": apart,
                "apart images": apart_list[:6],
            }
        )
    )


if __name__ == "__main__":
    main()
