"""a484: the base and one reflection to N; the log events of both by interval (births, refusals) and at the interval named the scalar mismatches by line, name and Node. Usage: locate_state.py <src> <worktree> <N> <image index> <interval>"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2] + "/tools/derivations/open_items/H-48-In-The-Clicks-2")
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import PLANE, POTENTIAL  # noqa: E402
import a48b_48 as A  # noqa: E402

root, n, k_img, at_i = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
universe, world = load_world(root + "/tests/worlds/world_node.json")
centres = ([1, 0, 0], [0, 2, 1], [2, 1, 0])
lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in centres]
world = dict(world, shape=[3, 3, 3], intervals=n, seed=lays)
cube = 3
m = A.signed_permutations()[k_img]
base, img = Node(universe, world), Node(universe, A.world_image(world, m, cube))
for t in range(n):
    base.step(); img.step()
    if base.interval == at_i:
        tags = A.line_tags(base)
        lb, li_ = base.all_lines(), img.all_lines()
        for li, tag in enumerate(tags):
            if tag[0] != "scalar" or (tag[1] == PLANE and tag[2] == 1) or (tag[1] == POTENTIAL and tag[2] == 0):
                continue
            for name in ("now", "before", "rem"):
                a, b = getattr(lb[li], name), getattr(li_[li], name)
                for x in np.ndindex(*base.shape):
                    gx = A.image(m, x, cube)
                    if int(a[x]) != int(b[gx]):
                        print("scalar mismatch at", at_i, tag, name, "node", x, "->", gx, "base", int(a[x]), "image", int(b[gx]))
print("base turns", base.turns[:12])
print("img  turns", img.turns[:12])
for name, nd in (("base", base), ("img", img)):
    for e in nd.log:
        if e["i"] <= at_i + 1 and e["event"] != "credit":
            print(name, json.dumps(e, default=str)[:400])
print("counts base", dict(base.counts)); print("counts img", dict(img.counts))
