"""An echo off matter (Big Pic, the owner's ask of 07:0x UTC): two records of the mesh world compared, the plain lay and
the same lay with the held hand laid at 2 instead of 1 on a patch of Node-clocks partway round the ring. The light's
leading front reaches distance d at round 2 d (fronts.py). Read here, from the click lines alone: at each Node-clock,
the first round where any click line of the two records differs: where the patch first answers the light, and how the
answer travels back to the bump. Einstein's rule on it: the patch's distance from the bump is a quarter of the round
the answer reaches the bump, at the front's half a Mesh a round. Rounds as order and as a stand-in for a clock's own
count (FACE2 not in the record); whole numbers alone.

Usage: python3 -I mirror.py <src> <plain.jsonl> <variant.jsonl> <ring> <centre> <rounds>
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

plain, variant, ring, centre, rounds = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
half, _ = carry(ring, 2, 0)


def dist(s):
    _, r = carry(s - centre + half, ring, 0)
    return r - half


def lines(path):
    out = {}
    for line in open(path):
        d = json.loads(line)
        if d["kind"] == "click" and d["round"] <= rounds:
            out[(d["round"], d["site"], d["train"])] = (d["q"], json.dumps(d.get("sides")), json.dumps(d.get("across")))
    return out


a, b = lines(plain), lines(variant)
first = {}
for k in set(a) | set(b):
    if a.get(k) != b.get(k):
        t, s, _ = k
        if s not in first or t < first[s]:
            first[s] = t
print(f"{plain} against {variant}, rounds 1 to {rounds}: {len(first)} Node-clocks where a click line differs")
for s in sorted(first, key=lambda s: (first[s], s))[:3]:
    print(f"   the first: Node-clock {s} (distance {dist(s)}) at round {first[s]}")
for dd in (52, 50, 45, 40, 38, 35, 30, 25, 20, 15, 10, 5, 3, 0):
    sites = [s for s in first if dist(s) == dd]
    print(f"   distance {dd:3d}: the first difference at round {first[sites[0]] if sites else '-'}")
bump = [first[s] for s in first if abs(dist(s)) <= 0]
if bump:
    t2 = min(bump)
    quarter, _ = carry(t2, 4, 0)
    print(f"Einstein's rule from the bump: the answer reaches it at round {t2}, so the answer came from distance {t2} / 4,"
          f" about {quarter}; the patch lies at distances 40 to 50")
