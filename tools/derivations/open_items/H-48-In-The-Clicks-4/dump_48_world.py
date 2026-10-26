"""a484: dump_48 (CB13's) widened to a world file and an image limit. Usage: dump_48_world.py <src> <world.json> <intervals> <out.json> [images N]"""
import itertools
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

universe, world = load_world(sys.argv[2])
n = int(sys.argv[3])
world = dict(world, intervals=n)
cube = int(world["shape"][0])
limit = int(sys.argv[sys.argv.index("images") + 1]) if "images" in sys.argv else 48
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
][:limit]


def image(m, node):
    return [int(x) % cube for x in m @ np.array(node, dtype=int)]


def world_image(w, m):
    found = dict(w, seed=[dict(lay) for lay in w["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = image(m, lay[key])
    return found


def run(w):
    node = Node(universe, w)
    for _ in range(n):
        node.step()
    return {"log": node.log, "counts": dict(node.counts), "turns": node.turns}


out = {"base": run(world), "images": [], "cube": cube}
for m in IMAGES:
    out["images"].append({"m": m.tolist(), "det": int(round(np.linalg.det(m))), **run(world_image(world, m))})
    print(len(out["images"]), flush=True)
with open(sys.argv[4], "w", encoding="utf-8") as f:
    json.dump(out, f)
