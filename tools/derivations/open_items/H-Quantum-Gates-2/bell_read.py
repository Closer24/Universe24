"""Bell's reading on a record (hand qg2): every birth's two children (the - child at `minus`, the + child at `plus`, the children's record `line_pair`), each child's first credit after the birth at its own Node and line (the click of that end), the outcome at a setting (p, q) the sign of p re_now + q im_now of the credit's frame (the plane's levels at the Node at the click, the frame's axis choice), the correlation E(a, b) = (same - opposite) / pairs per setting pair over the pairs where both ends clicked, and S = E(a, b) - E(a, b') + E(a', b) + E(a', b') as one rational over the pairs' count; the classical bound 2 as 2 N against |numerator|. Beside it the senses' reading (the sign of W at the click) and the senses at the birth (W_children). Integers only.

Usage: python bell_read.py <record.json> [<record.json> ...]"""
import json
import sys
from collections import defaultdict

# the four settings of 4.0's Bell worlds (examples/events/bell/design.json): A (1, 0) and (1, 1), B (12, 5) and (5, 12)
SETTINGS_A = ((1, 0), (1, 1))
SETTINGS_B = ((12, 5), (5, 12))
HUNDRED = 100


def sign(x):
    return (x > 0) - (x < 0)


def outcome(frame, setting):
    p, q = setting
    return sign(p * frame["re_now"] + q * frame["im_now"])


def pairs_of(run):
    """The (minus credit, plus credit) pairs: for every birth the first credit of the children's record at each end after the birth's interval."""
    log = run["log"]
    credits = defaultdict(list)
    for e in log:
        if e["event"] == "credit":
            credits[(tuple(e["node"]), e["line"])].append(e)
    found = []
    births = [e for e in log if e["event"] == "birth"]
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


def chsh(pairs, key):
    """S as one rational: SUM of the four E's with the signs (+, -, +, +), each E = (same - opposite) / n over its own count; the common denominator the product is avoided by reporting each E in hundredths and S in hundredths from the E's rationals (the exact test |S| <= 2 done by cross multiplication on the four rationals)."""
    es = {}
    for ia, a in enumerate(SETTINGS_A):
        for ib, b in enumerate(SETTINGS_B):
            es[(ia, ib)] = correlation(pairs, a, b, key)
    # S = E00 - E01 + E10 + E11; every E over the same pairs' count where every outcome is nonzero; the denominators may differ where an outcome is 0
    terms = [(1, es[(0, 0)]), (-1, es[(0, 1)]), (1, es[(1, 0)]), (1, es[(1, 1)])]
    num, den = 0, 1
    for sgn, (n, d) in terms:
        if d == 0:
            return es, None
        num, den = num * d + sgn * n * den, den * d
    return es, (num, den)


def read(path):
    with open(path, encoding="utf-8") as f:
        run = json.load(f)
    births, pairs = pairs_of(run)
    both = [p for p in pairs if p[1] is not None and p[2] is not None]
    one = sum(1 for p in pairs if (p[1] is None) != (p[2] is None))
    frame_key = lambda c, s: outcome(c["frame"], s) if "re_now" in c["frame"] else 0
    sense_key = lambda c, s: c["sense"]
    es_f, s_f = chsh(both, frame_key)
    es_s, s_s = chsh(both, sense_key)
    born_opposite = sum(1 for b in births if sign(b["W_children"][0]) * sign(b["W_children"][1]) < 0)
    out = {
        "record": path,
        "births": len(births),
        "pairs with both ends clicked": len(both),
        "pairs with one end clicked": one,
        "births with the two children's W of opposite sign (the senses -1 and +1)": born_opposite,
        "E per setting (same - opposite, pairs), the frame's axis (p re + q im)": {f"a{ia} b{ib}": v for (ia, ib), v in es_f.items()},
        "S by the frame's axis (hundredths)": None if s_f is None else (s_f[0] * HUNDRED) // s_f[1] if s_f[1] > 0 else None,
        "S by the frame's axis as a rational": s_f,
        "|S| above 2 by the frame's axis": None if s_f is None else abs(s_f[0]) > 2 * s_f[1],
        "E per setting, the senses (sign of W at the click)": {f"a{ia} b{ib}": v for (ia, ib), v in es_s.items()},
        "S by the senses as a rational": s_s,
        "|S| above 2 by the senses": None if s_s is None else abs(s_s[0]) > 2 * s_s[1],
        "ends one Link apart at the birth (every birth lays its children at the two ends of one Link)": all(sum(min(abs(x - y), int(run["cube"]) - abs(x - y)) for x, y in zip(b["minus"], b["plus"])) == 1 for b in births),
        "children at one Node per birth (a shared take): max": max((b.get("children_at_node", 1) for b in births), default=0),
        "births from a shared take of two or more pairs": sum(1 for b in births if b.get("children_at_node", 1) >= 2),
    }
    print(json.dumps(out))


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    for p in sys.argv[1:]:
        read(p)
