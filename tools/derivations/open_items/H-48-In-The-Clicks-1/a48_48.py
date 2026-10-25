"""a48: the cube's 48 on the clicks of the engine (or of a48's flagged copy, by PYTHONPATH and A48_READ): the world run from
its seed and from each of its 48 images (the signed permutations of the axes about the origin, the torus wrapped); the click
record compared through the image in two criteria at once:
  births: (interval, the take's Node, the plane, the - child's Node, the + child's Node, W at the - end, W at the + end, the
          amplitude); a reflection's image is read with the ends AND the senses exchanged (the + child at the other end, W
          negated per end: CP), as ms1 read it; the senses alone (pm2's read) cannot match a birth by construction and is
          counted beside as a control;
  clicks: the births as above AND the credits (interval, Node, plane, sense, beat), the sense negated under the exchange.
Verdicts per image: equal / senses exchanged / apart; for an apart image the first apart line by interval is printed.
Usage: python a48_48.py <world.json> <cube> <intervals> <out.json>; integers only (the determinant of a signed permutation is
the product of its three nonzero entries, read in integers)."""
import copy
import itertools
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402


def signed_permutations():
    axes = range(3)
    return [
        np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes], dtype=int)
        for pi in itertools.permutations(axes)
        for s in itertools.product((1, -1), repeat=3)
    ]


def determinant(m):
    """The determinant of a signed permutation in integers: the sign of the permutation times the product of the signs."""
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    sign = 1
    for a in range(3):
        for b in range(a + 1, 3):
            if pi[a] > pi[b]:
                sign = -sign
    return sign * int(np.prod([m[pi[a], a] for a in range(3)]))


def image(m, node, cube):
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(world, m, cube, intervals):
    w = copy.deepcopy(world)
    w["shape"], w["intervals"] = [cube] * 3, intervals
    for lay in w.get("seed", []):
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(int(x) % cube for x in lay[key]), cube))
    return w


def births_of(node, m, cube, exchange):
    found = []
    for e in node.log:
        if e["event"] != "birth":
            continue
        at = image(m, tuple(e["node"]), cube)
        mi, pl = image(m, tuple(e["minus"]), cube), image(m, tuple(e["plus"]), cube)
        wm, wp = e["W_children"]
        if exchange:
            mi, pl, wm, wp = pl, mi, -wp, -wm
        found.append(("birth", e["i"], at, e["line_pair"], mi, pl, wm, wp, e["amplitude"]))
    return sorted(found)


def senses_only(node, m, cube, exchange):
    """pm2's read: the ends kept, the senses' signs negated (the control)."""
    found = []
    s = -1 if exchange else 1
    for e in node.log:
        if e["event"] != "birth":
            continue
        wm, wp = e["W_children"]
        found.append(
            (
                "birth",
                e["i"],
                image(m, tuple(e["node"]), cube),
                e["line_pair"],
                image(m, tuple(e["minus"]), cube),
                image(m, tuple(e["plus"]), cube),
                s * ((wm > 0) - (wm < 0)),
                s * ((wp > 0) - (wp < 0)),
            )
        )
    return sorted(found)


def credits_of(node, m, cube, exchange):
    s = -1 if exchange else 1
    return sorted(
        ("credit", e["i"], image(m, tuple(e["node"]), cube), e["line"], s * e["sense"], e["beat"])
        for e in node.log
        if e["event"] == "credit"
    )


def run(universe, world):
    node = Node(json.loads(json.dumps(universe)), world)
    for _ in range(int(world["intervals"])):
        node.step()
    return node


def first_apart(a, b):
    """The first line (by interval) in a and not in b, or in b and not in a."""
    sa, sb = set(a), set(b)
    only_a = sorted(sa - sb, key=lambda t: t[1])
    only_b = sorted(sb - sa, key=lambda t: t[1])
    first = None
    if only_a:
        first = ("base has, image lacks", only_a[0])
    if only_b and (first is None or only_b[0][1] < first[1][1]):
        first = ("image has, base lacks", only_b[0])
    return first


def verdict(base_lines, image_lines_plain, image_lines_exchanged):
    if image_lines_plain == base_lines:
        return "equal"
    if image_lines_exchanged == base_lines:
        return "senses exchanged"
    return "apart"


def main(argv):
    universe, world = load_world(argv[1])
    cube, intervals = int(argv[2]), int(argv[3])
    eye = np.eye(3, dtype=int)
    base = run(universe, world_image(world, eye, cube, intervals))
    b_births = births_of(base, eye, cube, False)
    b_senses = senses_only(base, eye, cube, False)
    b_clicks = b_births + credits_of(base, eye, cube, False)
    counts = {
        k: {"equal": 0, "senses exchanged": 0, "apart": 0}
        for k in ("births", "births (senses alone, pm2)", "clicks")
    }
    by_det = {d: {k: dict(v) for k, v in counts.items()} for d in (1, -1)}
    rows = []
    for k, m in enumerate(signed_permutations()):
        img = run(universe, world_image(world, m, cube, intervals))
        mt = m.T
        det = determinant(m)
        i_births, i_births_x = births_of(img, mt, cube, False), births_of(img, mt, cube, True)
        i_senses, i_senses_x = senses_only(img, mt, cube, False), senses_only(img, mt, cube, True)
        i_clicks = i_births + credits_of(img, mt, cube, False)
        i_clicks_x = i_births_x + credits_of(img, mt, cube, True)
        v = {
            "births": verdict(b_births, i_births, i_births_x),
            "births (senses alone, pm2)": verdict(b_senses, i_senses, i_senses_x),
            "clicks": verdict(b_clicks, i_clicks, i_clicks_x),
        }
        for key, value in v.items():
            counts[key][value] += 1
            by_det[det][key][value] += 1
        row = {
            "image": k,
            "m": m.tolist(),
            "det": det,
            "verdicts": v,
            "births": img.counts["births"],
            "credits": img.counts["body_clicks"],
            "turns": img.counts["turns"],
        }
        if v["clicks"] == "apart":
            other = i_clicks_x if det == -1 else i_clicks
            fa = first_apart(b_clicks, other)
            row["first apart (through the image, the senses exchanged for a reflection)"] = [
                fa[0],
                [str(x) for x in fa[1]],
            ]
        rows.append(row)
        print(json.dumps(row), flush=True)
    summary = {
        "world": argv[1],
        "cube": cube,
        "intervals": intervals,
        "base births": base.counts["births"],
        "base credits": base.counts["body_clicks"],
        "base turns": base.counts["turns"],
        "planes of the births": sorted({e["line_pair"] for e in base.log if e["event"] == "birth"}),
        "birth intervals": sorted({e["i"] for e in base.log if e["event"] == "birth"}),
        "counts": counts,
        "rotations (det +1)": by_det[1],
        "reflections (det -1)": by_det[-1],
    }
    print(json.dumps(summary))
    with open(argv[4], "w", encoding="utf-8") as out:
        json.dump({"summary": summary, "rows": rows}, out)


if __name__ == "__main__":
    main(sys.argv)
