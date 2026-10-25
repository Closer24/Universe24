"""ex1: the 48 on the clicks over the engine's Node (the toy's class): the world is run from its seed and from each of its
48 images (the signed permutations about the origin, the seed's Nodes carried); the click records (the births with the two
children's Nodes and the take's numbers, the credits with their line, sense, beat and take) are compared through the image:
equal, equal with the senses exchanged (the children's ends swapped, every credit's sense negated), or apart; the counts.
Usage: cube48_ex1.py <engine dir> <world.json> <out.json>"""
import copy
import itertools
import json
import sys

import numpy as np


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


def clicks(log, m, cube, exchanged):
    found = []
    for e in log:
        if e["event"] == "birth":
            minus, plus = image(m, tuple(e["minus"]), cube), image(m, tuple(e["plus"]), cube)
            if exchanged:
                minus, plus = plus, minus
            found.append(
                ("birth", e["i"], image(m, tuple(e["node"]), cube), e["line_pair"], minus, plus, e["taken"], e["booked"], e["levels"], e.get("remainder_was"), e.get("remainder"))
            )
        elif e["event"] == "credit":
            found.append(
                ("credit", e["i"], image(m, tuple(e["node"]), cube), e["line"], (-1 if exchanged else 1) * e["sense"], e["beat"], e["taken"], e["levels"], e.get("remainder_was"), e.get("remainder"))
            )
    return sorted(found, key=str)


def main(argv):
    sys.set_int_max_str_digits(0)
    sys.path.insert(0, argv[1])
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    import toy_ex1

    universe, world = toy_ex1.load_toy_world(argv[2])
    cube = int(world["shape"][0])
    intervals = int(world["intervals"])

    def run(w):
        node = toy_ex1.Toy(universe, w)
        for _ in range(intervals):
            node.step()
        return node

    base = run(world)
    base_clicks = clicks(base.log, np.eye(3, dtype=int), cube, False)
    counts = {"equal": 0, "senses exchanged": 0, "apart": 0}
    rows = []
    for k, m in enumerate(signed_permutations()):
        node = run(world_image(world, m, cube))
        inv = np.linalg.inv(m).astype(int)
        straight = clicks(node.log, inv, cube, False)
        swapped = clicks(node.log, inv, cube, True)
        verdict = "equal" if straight == base_clicks else "senses exchanged" if swapped == base_clicks else "apart"
        counts[verdict] += 1
        rows.append({"image": k, "det": int(round(np.linalg.det(m))), "verdict": verdict, "births": node.counts["births"], "credits": node.counts["body_clicks"], "taken": str(node.counts["taken"]), "booked": str(node.counts["booked"])})
    out = {"world": argv[2], "base_births": base.counts["births"], "base_credits": base.counts["body_clicks"], "base_clicks": len(base_clicks), "counts": counts, "rotations_equal": sum(1 for r in rows if r["det"] == 1 and r["verdict"] == "equal"), "reflections_exchanged": sum(1 for r in rows if r["det"] == -1 and r["verdict"] == "senses exchanged"), "rows": rows}
    json.dump(out, open(argv[3], "w"))
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))


if __name__ == "__main__":
    main(sys.argv)
