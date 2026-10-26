"""a484: the base and one reflection run to N; at the intervals named every line's (now, before, rem) at one Node in both worlds, with the row's shape and the line's index. Usage: locate_node.py <src> <worktree> <image index> <node x,y,z> <i1,i2,...>"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2] + "/tools/derivations/open_items/H-48-In-The-Clicks-2")
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
import a48b_48 as A  # noqa: E402

root, k_img = sys.argv[2], int(sys.argv[3])
at = tuple(int(v) for v in sys.argv[4].split(","))
when = [int(v) for v in sys.argv[5].split(",")]
universe, world = load_world(root + "/tests/worlds/world_node.json")
centres = ([1, 0, 0], [0, 2, 1], [2, 1, 0])
lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in centres]
world = dict(world, shape=[3, 3, 3], intervals=max(when), seed=lays)
m = A.signed_permutations()[k_img]
base, img = Node(universe, world), Node(universe, A.world_image(world, m, 3))
gx = A.image(m, at, 3)
for t in range(max(when)):
    base.step(); img.step()
    if base.interval in when:
        tags = A.line_tags(base)
        for li, (lb, lim) in enumerate(zip(base.all_lines(), img.all_lines())):
            vb = [int(lb.now[at]), int(lb.before[at]), int(lb.rem[at])]
            vi = [int(lim.now[gx]), int(lim.before[gx]), int(lim.rem[gx])]
            flag = "" if vb == vi else ("  NEG" if vb[:2] == [-vi[0], -vi[1]] else "  <<<")
            print("i", base.interval, "line", li, tags[li], "base", vb, "image", vi, flag)
        print("turned base", bool(base.turned[at]), "image", bool(img.turned[gx]), "turns so far", base.counts["turns"], img.counts["turns"])
