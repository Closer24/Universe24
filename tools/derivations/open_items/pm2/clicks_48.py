"""pm2's 48 on the clicks, re-based on the engine from the kit's clicks_48_example.py (pa2's): the world run from its seed and from each of its 48 images (the signed permutations of the axes about the origin, the torus wrapped); the click record (the births: the take's Node, the plane, the two children's Nodes and the signs of their Wronskians; the credits: the Node, the plane, the sense, the beat) compared through the image: equal, equal with every sense exchanged, or apart. Usage: PYTHONPATH=<src> python clicks_48.py <world.json> <intervals> <out.json>; the flag rides in the world file."""
import copy
import itertools
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node


def signed_permutations():
    axes = range(3)
    return [
        np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes])
        for pi in itertools.permutations(axes)
        for s in itertools.product((1, -1), repeat=3)
    ]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def world_image(world, m, cube):
    w = copy.deepcopy(world)
    for lay in w.get("seed", []):
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key]), cube))
    return w


def clicks(node, m, cube, exchange):
    """The click record through the image m (the Nodes mapped) with the senses exchanged where asked, as a sorted list of tuples."""
    found = []
    s = -1 if exchange else 1
    for e in node.log:
        if e["event"] == "birth":
            w0, w1 = e["W_children"]
            found.append(("birth", e["i"], image(m, tuple(e["node"]), cube), e["line_pair"], image(m, tuple(e["minus"]), cube), image(m, tuple(e["plus"]), cube), s * (1 if w0 > 0 else -1 if w0 < 0 else 0), s * (1 if w1 > 0 else -1 if w1 < 0 else 0)))
        elif e["event"] == "credit":
            found.append(("credit", e["i"], image(m, tuple(e["node"]), cube), e["line"], s * e["sense"], e["beat"]))
    return sorted(found)


def run(universe, world, n):
    node = Node(universe, world)
    for _ in range(n):
        node.step()
    return node


def main(argv):
    universe, world = load_world(argv[1])
    n = int(argv[2])
    cube = int(world["shape"][0])
    base = run(universe, world, n)
    eye = np.eye(3, dtype=int)
    base_clicks = clicks(base, eye, cube, False)
    counts = {"equal": 0, "senses exchanged": 0, "apart": 0}
    rows = []
    for k, m in enumerate(signed_permutations()):
        img = run(universe, world_image(world, m, cube), n)
        # the image's clicks mapped back by the inverse (m is orthogonal: the inverse its transpose)
        back = clicks(img, m.T, cube, False)
        back_x = clicks(img, m.T, cube, True)
        det = int(round(np.linalg.det(m)))
        if back == base_clicks:
            verdict = "equal"
        elif back_x == base_clicks:
            verdict = "senses exchanged"
        else:
            verdict = "apart"
        counts[verdict] += 1
        rows.append({"image": k, "det": det, "verdict": verdict, "births": img.counts["births"], "credits": img.counts["body_clicks"]})
        print(json.dumps(rows[-1]), flush=True)
    summary = {"base births": base.counts["births"], "base credits": base.counts["body_clicks"], "counts": counts, "rotations": {v: sum(1 for r in rows if r["det"] == 1 and r["verdict"] == v) for v in counts}, "reflections": {v: sum(1 for r in rows if r["det"] == -1 and r["verdict"] == v) for v in counts}}
    print(json.dumps(summary))
    json.dump({"summary": summary, "rows": rows}, open(argv[3], "w"))


if __name__ == "__main__":
    main(sys.argv)
