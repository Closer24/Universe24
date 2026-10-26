"""The 48 on the clicks: a world run N intervals from its seed and from each of its 48 images on a named src (the flag from the environment); the click record (births as (i, Node, pair, the children as a map Node -> sense) and credits as (i, Node, line, sense, beat)) carried back through the image and compared with the base's: EQUAL, CONJUGATE (every sense negated, the children's Nodes kept) or APART with the first apart interval. Usage: run_48.py <src> <world.json> <intervals> <out.json>"""
import itertools
import json
import os
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
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]


def det_of(m):
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    signs = [int(m[pi[a], a]) for a in range(3)]
    inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
    return (-1) ** inv * signs[0] * signs[1] * signs[2]


def image(m, node):
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(w, m):
    found = dict(w, seed=[dict(lay) for lay in w["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, lay[key]))
    return found


def run(w):
    node = Node(universe, w)
    for _ in range(n):
        node.step()
    return node


def record(node, m, s):
    found = []
    for e in node.log:
        if e["event"] == "birth":
            kids = tuple(sorted([(image(m, e["minus"]), -s), (image(m, e["plus"]), s)]))
            found.append(("birth", e["i"], image(m, e["node"]), e["line_pair"], kids))
        elif e["event"] == "credit":
            found.append(("credit", e["i"], image(m, e["node"]), e["line"], s * e["sense"], e["beat"]))
    return sorted(found)


def first_apart(a, b):
    sa, sb = set(a), set(b)
    odd = sorted(sa ^ sb, key=lambda x: x[1])
    return None if not odd else odd[0][1]


base = run(world)
base_rec = record(base, np.eye(3, dtype=int), 1)
rows, counts = [], {"EQUAL": 0, "CONJUGATE": 0, "APART": 0}
for k, m in enumerate(IMAGES):
    img = run(world_image(world, m))
    back, back_x = record(img, m.T, 1), record(img, m.T, -1)
    v = "EQUAL" if back == base_rec else "CONJUGATE" if back_x == base_rec else "APART"
    counts[v] += 1
    row = {"image": k, "det": det_of(m), "verdict": v, "births": img.counts["births"], "credits": img.counts["body_clicks"],
           "first_apart_equal": first_apart(base_rec, back), "first_apart_conjugate": first_apart(base_rec, back_x)}
    rows.append(row)
    print(json.dumps(row), flush=True)
summary = {"world": sys.argv[2], "src": sys.argv[1], "flag": os.environ.get("CM1_FORM", ""), "intervals": n, "cube": cube, "counts": counts,
           "by_det": {d: {v: sum(1 for r in rows if r["det"] == d and r["verdict"] == v) for v in counts} for d in (1, -1)},
           "base": {"births": base.counts["births"], "credits": base.counts["body_clicks"], "turns": base.counts["turns"], "counts": {k: int(v) for k, v in base.counts.items()}},
           "first_apart_intervals": sorted(set(r["first_apart_conjugate" if r["det"] == -1 else "first_apart_equal"] for r in rows if r["verdict"] == "APART"), key=lambda x: (x is None, x))}
print(json.dumps(summary))
json.dump({"summary": summary, "rows": rows}, open(sys.argv[4], "w"), default=str)
