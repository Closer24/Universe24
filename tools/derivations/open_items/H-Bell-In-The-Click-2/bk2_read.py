"""The click's cancellation and the twin (hand bk2, on bc2's root_read.py): the board run forward from the seed with the state hash kept at every interval and the two children's record's four levels at every Node kept per interval; the run back exact by the hash; for every born pair clicked at both ends: the first click's end, its interval, whether its take was laid back (EQ-S1) or stands, the twin's Link distance from the first click's Node at that click, the twin's plane levels at the first click's interval and at its own click (what stood at the twin between the clicks), the outcomes under the 3-4-5 settings (a = (1, 0), a' = (0, 1); b = (4, 3), b' = (-3, 4): the exact cosines 4/5, -3/5, 3/5, 4/5) by the frame and by the sense, nature's singlet correlation E = -cos on the same settings and its S as one rational, the law's per-pair identity and S. Integers only; no act touched.

Usage: python bk2_read.py <world.json> <out.json>"""
import json
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 2)[0] + "/H-Bell-Through-The-Cone-2")
from root_read import identity, outcome, pairs_of, root_of, sign, torus_distance  # noqa: E402

from event_universe.node import Node  # noqa: E402
from event_universe.run import load_world  # noqa: E402

SETTINGS_A = ((1, 0), (0, 1))
SETTINGS_B = ((4, 3), (-3, 4))


def cos_rational(u, v):
    """cos of the angle between two integer settings as (num, den): the dot over the product of the lengths, exact where both lengths are integers (the 3-4-5 settings)."""
    dot = u[0] * v[0] + u[1] * v[1]
    la2, lb2 = u[0] ** 2 + u[1] ** 2, v[0] ** 2 + v[1] ** 2
    la = next(k for k in range(la2 + 1) if k * k == la2)
    lb = next(k for k in range(lb2 + 1) if k * k == lb2)
    return dot, la * lb


def nature_s():
    """Nature's singlet: E(a, b) = -cos(a, b); S = E(a,b) - E(a,b') + E(a',b) + E(a',b') as one rational over the common denominator."""
    a, a1 = SETTINGS_A
    b, b1 = SETTINGS_B
    terms = [cos_rational(a, b), cos_rational(a, b1), cos_rational(a1, b), cos_rational(a1, b1)]
    den = 1
    for _n, d in terms:
        den = den * d // __import__("math").gcd(den, d)
    e = [(-n * (den // d)) for n, d in terms]
    s = e[0] - e[1] + e[2] + e[3]
    return {"E(a,b), E(a,b'), E(a',b), E(a',b') over den": e, "den": den, "S as a rational": [s, den], "4 den^2 < S^2 <= 8 den^2": 4 * den * den < s * s <= 8 * den * den}


def levels_at(node, rec, at):
    lines = node.records()[rec].lines
    return [[int(z.now[at]), int(z.before[at])] for z in lines]


def main(argv):
    sys.set_int_max_str_digits(0)
    world_path, out_path = argv[1], argv[2]
    universe, world = load_world(world_path)
    node = Node(universe, world)
    intervals = int(world["intervals"])
    rec0 = node.records().index(node.emitter())
    nrec = len(node.records())
    t0 = time.monotonic_ns()
    hashes = [node.state_hash()]
    snaps = [{}]  # per interval: per record the lines' (now, before) at every Node as nested lists
    def snap():
        return {rec: [[z.now.tolist(), z.before.tolist()] for z in node.records()[rec].lines] for rec in range(nrec)}
    snaps = [snap()]
    for _ in range(intervals):
        node.step()
        hashes.append(node.state_hash())
        snaps.append(snap())
    forward_ms = (time.monotonic_ns() - t0) // 1000000
    log = list(node.log)
    cube = node.cube
    pairs = pairs_of(log)
    both = [p for p in pairs if p[1] is not None and p[2] is not None]
    t1 = time.monotonic_ns()
    exact = 0
    for k in range(intervals, 0, -1):
        node.step_back()
        exact += node.state_hash() == hashes[k - 1]
    back_ms = (time.monotonic_ns() - t1) // 1000000

    def at_snap(k, rec, where):
        s = snaps[k][rec]
        out = []
        for now, before in s:
            a, b = now, before
            for x in where:
                a, b = a[x], b[x]
            out.append([int(a), int(b)])
        return out

    rows, ids_frame, ids_sense = [], [], []
    first_laid_back = first_standing = 0
    twin_dist = []
    twin_changed_between = 0
    light_changed_at_twin_next = 0
    for b, m, p in both:
        root = root_of(b)
        s = b["line_pair"]
        first, second = (m, p) if m["i"] <= p["i"] else (p, m)
        first_end = "minus" if first is m else "plus"
        twin_node = tuple(p["node"]) if first is m else tuple(m["node"])
        laid = "laid_back" in first
        first_laid_back += laid
        first_standing += not laid
        d = torus_distance(tuple(first["node"]), twin_node, cube)
        twin_dist.append(d)
        k1 = first["i"]  # the first click's interval; snaps[k1] the state after that interval's step (the click inside it)
        k2 = second["i"]
        twin_at_first = at_snap(min(k1, intervals), s, twin_node)
        twin_before_first = at_snap(max(k1 - 1, 0), s, twin_node)
        twin_at_own = at_snap(min(k2, intervals), s, twin_node)
        twin_changed_between += twin_at_first != twin_at_own
        light_twin_before = at_snap(max(k1 - 1, 0), rec0, twin_node)
        light_twin_after = at_snap(min(k1, intervals), rec0, twin_node)
        light_twin_next = at_snap(min(k1 + 1, intervals), rec0, twin_node)
        light_changed_at_twin_next += light_twin_after != light_twin_next
        a_out = [outcome(m["frame"], st) for st in SETTINGS_A]
        b_out = [outcome(p["frame"], st) for st in SETTINGS_B]
        idf = identity(a_out, b_out)
        ids_ = identity([m["sense"]] * 2, [p["sense"]] * 2)
        ids_frame.append(idf)
        ids_sense.append(ids_)
        rows.append({
            "birth i": b["i"], "children record": s, "clicks i (minus, plus)": [m["i"], p["i"]],
            "first click end": first_end, "first click node": first["node"], "twin node": list(twin_node),
            "twin Link distance at the first click": d,
            "first click laid back (EQ-S1)": laid,
            "first click take: taker [now, before, levels], line": [first["taker"], first["taken_line"]],
            "twin's plane levels [re, im] x [now, before] at the first click's interval start": twin_before_first,
            "twin's plane levels after the first click's interval": twin_at_first,
            "twin's plane levels at its own click's interval": twin_at_own,
            "light (gap-0) line levels at the twin: before, after the first click's interval, one later": [light_twin_before, light_twin_after, light_twin_next],
            "outcomes by the frame (A at a, a'; B at b, b')": [a_out, b_out],
            "outcomes by the sense": [m["sense"], p["sense"]],
            "identity by the frame": idf, "identity by the sense": ids_,
            "root": root,
        })

    def summary(ids):
        num, den = sum(ids), len(ids)
        return {"S as a rational": [num, den], "S in hundredths": (num * 100) // den if den else None,
                "4 den^2 < S^2 <= 8 den^2 (nature's band)": (4 * den * den < num * num <= 8 * den * den) if den else None,
                "|S| <= 2": abs(num) <= 2 * den if den else None,
                "identity per pair": {str(k): ids.count(k) for k in sorted(set(ids))}}

    out = {
        "world": world_path, "cube": cube, "intervals": intervals, "forward ms": forward_ms, "run back ms": back_ms,
        "run back exact, intervals": exact, "births": sum(1 for e in log if e["event"] == "birth"),
        "credits": sum(1 for e in log if e["event"] == "credit"),
        "credits laid back": sum(1 for e in log if e["event"] == "credit" and "laid_back" in e),
        "pairs clicked at both ends": len(both),
        "first clicks laid back (EQ-S1)": first_laid_back, "first clicks whose take stands": first_standing,
        "twin Link distance at the first click: per pair": twin_dist,
        "pairs whose twin's plane levels moved between the first click and its own": twin_changed_between,
        "pairs whose light line at the twin moved in the interval after the first click": light_changed_at_twin_next,
        "settings": {"a, a'": SETTINGS_A, "b, b'": SETTINGS_B},
        "nature's singlet on these settings": nature_s(),
        "the law's S at the clicks by the frame": summary(ids_frame),
        "the law's S at the clicks by the sense": summary(ids_sense),
        "pairs": rows,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(json.dumps({k: v for k, v in out.items() if k != "pairs"}))


if __name__ == "__main__":
    main(sys.argv)
