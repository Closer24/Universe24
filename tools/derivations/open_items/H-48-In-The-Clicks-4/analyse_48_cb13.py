"""Count the 48 images of a dump_48 run: rotations EQUAL, reflections CONJUGATE, APART; the first apart interval. Usage: analyse_48.py <dump.json> [intervals]"""
import json
import sys

import numpy as np

d = json.load(open(sys.argv[1]))
CUBE = int(d.get("cube", 3))
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
NEG = len(sys.argv) > 3 and sys.argv[3] == "neg"


def image(m, node):
    return tuple(int(x) % CUBE for x in np.array(m) @ np.array(node, dtype=int))


def births(log):
    return sorted((e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"]), tuple(e["senses"])) for e in log if e["event"] == "birth" and e["i"] <= n)


def credits(log):
    return sorted((e["i"], tuple(e["node"]), e["line"], e["sense"], e["beat"]) for e in log if e["event"] == "credit" and e["i"] <= n)


def carried(bs, cs, m, conj):
    fb = [(i, image(m, at), s, image(m, mi), image(m, pl), tuple(se)) for i, at, s, mi, pl, se in bs]
    if conj:
        fb = [(i, at, s, pl, mi, se) for i, at, s, mi, pl, se in fb]
    fc = [(i, image(m, at), ln, -sn if (conj and NEG) else sn, bt) for i, at, ln, sn, bt in cs]
    return sorted(fb), sorted(fc)


base_b, base_c = births(d["base"]["log"]), credits(d["base"]["log"])
print("base births", len(base_b), "credits", len(base_c), "turns", d["base"]["counts"]["turns"])
counts = {"rot_equal": 0, "refl_conjugate": 0, "apart": 0}
firsts = []
for im in d["images"]:
    conj = im["det"] == -1
    b, c = births(im["log"]), credits(im["log"])
    eb, ec = carried(base_b, base_c, im["m"], conj)
    if b == eb and c == ec:
        counts["refl_conjugate" if conj else "rot_equal"] += 1
    else:
        counts["apart"] += 1
        apart = sorted(set(b) ^ set(eb) | set(c) ^ set(ec), key=lambda x: x[0])
        firsts.append((apart[0][0] if apart else None, im["m"], "births" if b != eb else "credits", len(b), len(eb), len(c), len(ec)))
print(counts)
for f in firsts[:6]:
    print("apart first at interval", f[0], "image", f[1], f[2], "births got/expected", f[3], f[4], "credits got/expected", f[5], f[6])
