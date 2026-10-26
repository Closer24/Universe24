"""The chiral seed of the 3-cube (the A48-S1 test's world) run N intervals from the seed and its 48 images on a named src; the logs dumped. Usage: dump_48.py <src> <worktree> <intervals> <out.json>"""
import itertools
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

root, n = sys.argv[2], int(sys.argv[3])
universe, world = load_world(root + "/tests/worlds/world_node.json")
centres = ([1, 0, 0], [0, 2, 1], [2, 1, 0])
lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in centres]
world = dict(world, shape=[3, 3, 3], intervals=n, seed=lays)
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]


def image(m, node, cube):
    return [int(x) % cube for x in m @ np.array(node, dtype=int)]


def world_image(w, m):
    found = dict(w, seed=[dict(lay) for lay in w["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = image(m, lay[key], 3)
    return found


def run(w):
    node = Node(universe, w)
    for _ in range(n):
        node.step()
    return {"log": node.log, "counts": dict(node.counts), "turns": node.turns}


out = {"base": run(world), "images": []}
for m in IMAGES:
    out["images"].append({"m": m.tolist(), "det": int(round(np.linalg.det(m))), **run(world_image(world, m))})
    print(len(out["images"]), flush=True)
with open(sys.argv[4], "w", encoding="utf-8") as f:
    json.dump(out, f)
