"""The click's cancellation and the twin (hand bk1, NatureFirst A2 reopened): the world run forward with the state's hash kept at every interval; every birth's two children and each child's first credit at its own Node and line (the end's click); for every pair: the Link distance between the two children at the birth (the twin's distance), the intervals of the two first clicks and their gap, whether the two clicks fall in one interval (nothing crosses a Link within an interval: the read at the start, the write at the close), the Link distance between the two click Nodes, the levels the earlier click's take moved on the taken row's line and whether that take stood or was laid back (EQ-S1), so whether anything of the first click reaches the twin's Node by Rule3 (one Link per interval) before the twin's own click; the run back from the last interval to the earliest birth, every kept hash compared bit for bit. The reading of E and S: nature's singlet at the exact-cosine settings a = (1, 0), a' = (0, 1), b = (3, 4), b' = (-4, 3) (the cosines 3/5, -4/5, 4/5, 3/5; E = -cos, S = -14/5, S^2 = 196/25 in the band 4 < S^2 <= 8) against the law's by the frame at the same settings (the outcome the sign of p re_now + q im_now of the click's frame, a function of its own Node), by bc1's four settings of row 56 and by the senses; the per-pair identity. Integers only; no act of the engine touched.

Usage: python bk1_click_read.py <world.json> <out.json>"""
import json
import sys
from collections import Counter, defaultdict

from event_universe.loader.world import load_world
from event_universe.node import Node

EXACT_A = ((1, 0), (0, 1))
EXACT_B = ((3, 4), (-4, 3))
ROW56_A = ((1, 0), (1, 1))
ROW56_B = ((12, 5), (5, 12))
THOUSAND = 1000


def sign(x):
    return (x > 0) - (x < 0)


def outcome(credit, setting):
    p, q = setting
    f = credit["frame"]
    return sign(p * f["re_now"] + q * f["im_now"])


def torus_distance(a, b, cube):
    return sum(min(abs(x - y), cube - abs(x - y)) for x, y in zip(a, b))


def pairs_of(log):
    credits = defaultdict(list)
    for e in log:
        if e["event"] == "credit":
            credits[(tuple(e["node"]), e["line"])].append(e)
    births = [e for e in log if e["event"] == "birth"]
    found = []
    for b in births:
        s = b["line_pair"]
        ends = []
        for where in (b["minus"], b["plus"]):
            later = [c for c in credits[(tuple(where), s)] if c["i"] > b["i"]]
            ends.append(min(later, key=lambda c: c["i"]) if later else None)
        found.append((b, ends[0], ends[1]))
    return births, found


def correlation(pairs, a, b, key):
    same = opposite = 0
    for _birth, minus, plus in pairs:
        x, y = key(minus, a), key(plus, b)
        if x == 0 or y == 0:
            continue
        if x == y:
            same += 1
        else:
            opposite += 1
    return same - opposite, same + opposite


def chsh(pairs, key, setting_a, setting_b):
    es = {}
    for ia, a in enumerate(setting_a):
        for ib, b in enumerate(setting_b):
            es[(ia, ib)] = correlation(pairs, a, b, key)
    terms = [(1, es[(0, 0)]), (-1, es[(0, 1)]), (1, es[(1, 0)]), (1, es[(1, 1)])]
    num, den = 0, 1
    for sgn, (n, d) in terms:
        if d == 0:
            return es, None
        num, den = num * d + sgn * n * den, den * d
    return es, (num, den)


def nature_singlet(setting_a, setting_b):
    """E(a, b) = -(a . b) / (|a| |b|) as a rational where |a| |b| is a whole number (the exact cosines); S the sum of the four."""
    def dot(u, v):
        return u[0] * v[0] + u[1] * v[1]

    def norm2(u):
        return u[0] * u[0] + u[1] * u[1]

    def isqrt_exact(n):
        r = int(n ** 0.5)
        while r * r > n:
            r -= 1
        while (r + 1) * (r + 1) <= n:
            r += 1
        return r if r * r == n else None

    es = {}
    num, den = 0, 1
    terms = []
    for ia, a in enumerate(setting_a):
        for ib, b in enumerate(setting_b):
            m = isqrt_exact(norm2(a) * norm2(b))
            if m is None:
                es[(ia, ib)] = None
                continue
            es[(ia, ib)] = (-dot(a, b), m)
    if any(v is None for v in es.values()):
        return es, None
    terms = [(1, es[(0, 0)]), (-1, es[(0, 1)]), (1, es[(1, 0)]), (1, es[(1, 1)])]
    for sgn, (n, d) in terms:
        num, den = num * d + sgn * n * den, den * d
    from math import gcd
    g = gcd(num, den)
    return es, (num // g, den // g)


def rational_text(r):
    return None if r is None else f"{r[0]} / {r[1]}"


def thousandths(r):
    return None if r is None or r[1] == 0 else (r[0] * THOUSAND) // r[1]


def identity(minus, plus, setting_a, setting_b):
    a0, a1 = outcome(minus, setting_a[0]), outcome(minus, setting_a[1])
    b0, b1 = outcome(plus, setting_b[0]), outcome(plus, setting_b[1])
    return a0 * b0 - a0 * b1 + a1 * b0 + a1 * b1


def main(world_path, out_path):
    universe, world = load_world(world_path)
    node = Node(universe, world)
    intervals = int(world["intervals"])
    hashes = {node.interval: node.state_hash()}
    for _t in range(intervals):
        node.step()
        hashes[node.interval] = node.state_hash()
    log = list(node.log)
    births, pairs = pairs_of(log)
    both = [p for p in pairs if p[1] is not None and p[2] is not None]
    cube = int(node.cube)

    # the twin and the first click: per pair
    rows = []
    for b, m, p in both:
        twin_links = torus_distance(b["minus"], b["plus"], cube)
        first, second = (m, p) if m["i"] <= p["i"] else (p, m)
        gap = second["i"] - first["i"]
        stood = "laid_back" not in first
        rows.append(
            {
                "birth_i": b["i"],
                "twin_links_at_birth": twin_links,
                "first_click_i": first["i"],
                "second_click_i": second["i"],
                "gap": gap,
                "one_interval": gap == 0,
                "links_between_click_nodes": torus_distance(m["node"], p["node"], cube),
                "first_click_levels_moved": int(first["levels"]),
                "first_click_taken_line": first["taken_line"],
                "first_click_stood": stood,
                "first_click_laid_back": int(first.get("laid_back", 0)),
                "reaches_twin_before_its_click": stood and gap >= twin_links and first["levels"] != 0,
                "minus_frame": [m["frame"]["re_now"], m["frame"]["im_now"]],
                "plus_frame": [p["frame"]["re_now"], p["frame"]["im_now"]],
                "senses": [m["sense"], p["sense"]],
            }
        )
    gaps = Counter(r["gap"] for r in rows)
    reach = sum(1 for r in rows if r["reaches_twin_before_its_click"])
    same_interval = sum(1 for r in rows if r["one_interval"])

    # what one click writes (from the log's letter): per credit one line's now at one Node, levels moved; per birth one take line at the take's Node and two lines at each child
    credits = [e for e in log if e["event"] == "credit"]
    credit_levels = Counter(int(e["levels"]) for e in credits)
    laid_back = sum(1 for e in credits if "laid_back" in e)
    birth_lines = Counter((int(e["levels"]), tuple(e["amplitude"])) for e in births)

    # the run back from the last interval to the earliest birth
    earliest = min((b["i"] for b in births), default=node.interval)
    steps_back = exact = 0
    while node.interval > earliest:
        node.step_back()
        steps_back += 1
        exact += node.state_hash() == hashes.get(node.interval)

    frame_key = lambda c, s: outcome(c, s)
    sense_key = lambda c, s: c["sense"]
    es_nat, s_nat = nature_singlet(EXACT_A, EXACT_B)
    es_x, s_x = chsh(both, frame_key, EXACT_A, EXACT_B)
    es_56, s_56 = chsh(both, frame_key, ROW56_A, ROW56_B)
    es_s, s_s = chsh(both, sense_key, EXACT_A, EXACT_B)
    idents_x = Counter(identity(m, p, EXACT_A, EXACT_B) for _b, m, p in both)
    idents_56 = Counter(identity(m, p, ROW56_A, ROW56_B) for _b, m, p in both)

    def band(r):
        if r is None:
            return None
        n, d = r
        return {"4 den^2 < num^2": 4 * d * d < n * n, "num^2 <= 8 den^2": n * n <= 8 * d * d}

    def es_text(es):
        return {f"a{ia} b{ib}": list(v) if v is not None else None for (ia, ib), v in es.items()}

    out = {
        "world": world_path,
        "cube": cube,
        "intervals": intervals,
        "births": len(births),
        "pairs_both_clicked": len(both),
        "twin_links_at_birth": dict(Counter(r["twin_links_at_birth"] for r in rows)),
        "first_click_at_laid_node (links between click nodes)": dict(Counter(r["links_between_click_nodes"] for r in rows)),
        "gap_between_the_two_first_clicks (intervals: pairs)": {str(k): v for k, v in sorted(gaps.items())},
        "pairs_clicking_in_one_interval": same_interval,
        "pairs_where_the_first_click_stood": sum(1 for r in rows if r["first_click_stood"]),
        "pairs_where_the_first_click_reaches_the_twin_before_its_click": reach,
        "first_click_levels_moved (levels: pairs)": {str(k): v for k, v in sorted(Counter(r["first_click_levels_moved"] for r in rows).items())},
        "credits": len(credits),
        "credits_laid_back (EQ-S1)": laid_back,
        "credit_levels_moved (levels: credits)": {str(k): v for k, v in sorted(credit_levels.items())},
        "birth take levels and children amplitude (levels, [A, B]): births": {f"{k[0]} {list(k[1])}": v for k, v in sorted(birth_lines.items())},
        "run_back": {"from": intervals, "to": earliest, "steps": steps_back, "exact": exact},
        "nature singlet at the exact cosines: E (num, den)": es_text(es_nat),
        "nature singlet: S": rational_text(s_nat),
        "nature singlet: S^2 in the band 4 < S^2 <= 8": band(s_nat),
        "law by the frame at the exact cosines: E (same - opposite, pairs)": es_text(es_x),
        "law by the frame at the exact cosines: S": rational_text(s_x),
        "law by the frame at the exact cosines: S (thousandths)": thousandths(s_x),
        "law by the frame at the exact cosines: S^2 in the band": band(s_x),
        "law by the frame at the exact cosines: per-pair identity": {str(k): v for k, v in sorted(idents_x.items())},
        "law by the frame at row 56's settings: E": es_text(es_56),
        "law by the frame at row 56's settings: S": rational_text(s_56),
        "law by the frame at row 56's settings: per-pair identity": {str(k): v for k, v in sorted(idents_56.items())},
        "law by the senses: E": es_text(es_s),
        "law by the senses: S": rational_text(s_s),
        "pairs": rows,
        "counts": {k: str(v) for k, v in node.counts.items()},
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=str)
    short = {k: v for k, v in out.items() if k not in ("pairs", "counts")}
    print(json.dumps(short, default=str))


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    main(sys.argv[1], sys.argv[2])
