"""The chiral 2,400 under the flag against the Boss's head record: the frozen count per interval, each frozen Node's intervals (the freeze, the release), the content after, the clicks at the frozen Nodes after their first freeze, the bits, the run back, the counts. Usage: chiral_compare.py <flagged.json> <head.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
a = json.load(open(sys.argv[1]))
b = json.load(open(sys.argv[2]))
print("counts flagged", a["counts"])
print("counts head   ", b["counts"])
print("run back flagged", a.get("run_back"), "head", b.get("run_back"))
fa = {e["i"]: e.get("frozen", []) for e in a["nodes"]}
fb = {e["i"]: e.get("frozen", []) for e in b["nodes"]}
ca = {e["i"]: e["content"] for e in a["nodes"]}
cb = {e["i"]: e["content"] for e in b["nodes"]}
first_a = next((i for i in sorted(fa) if fa[i]), None)
first_b = next((i for i in sorted(fb) if fb[i]), None)
print("first frozen interval flagged", first_a, fa.get(first_a), "head", first_b, fb.get(first_b))
print("frozen count per interval, flagged, from the first freeze (i: count):", [(i, len(fa[i])) for i in sorted(fa) if fa[i]][:60])
print("frozen count per interval, head, the last 6:", [(i, len(fb[i])) for i in sorted(fb)][-6:])
print("max frozen count flagged", max(len(v) for v in fa.values()), "head", max(len(v) for v in fb.values()))
print("intervals with a frozen Node flagged", sum(1 for v in fa.values() if v), "head", sum(1 for v in fb.values() if v))
# two in a row at one Node
nodes_a = set(n for v in fa.values() for n in v)
runs = []
for n in sorted(nodes_a):
    ints = [i for i in sorted(fa) if n in fa[i]]
    pairs = sum(1 for x, y in zip(ints, ints[1:]) if y == x + 1)
    runs.append((n, len(ints), pairs, ints[:5]))
print("frozen Nodes flagged (node, frozen intervals, consecutive pairs, first five):", runs)
print("distinct frozen Nodes flagged", len(nodes_a), "head", len(set(n for v in fb.values() for n in v)))
print("content max per interval flagged, last 8:", [(i, max(ca[i])) for i in sorted(ca)][-8:])
print("content max head at 2400", max(cb[2400]), "flagged at 2400", max(ca[2400]), "mean flagged", sum(ca[2400]) // len(ca[2400]), "head", sum(cb[2400]) // len(cb[2400]))
print("content at the head's 24 frozen Nodes at 2400, flagged:", [ca[2400][n] for n in fb[2400]])
# the clicks at frozen Nodes after their first freeze
first_freeze = {}
for i in sorted(fa):
    for n in fa[i]:
        first_freeze.setdefault(n, i)
cube = a["cube"]
def flat(xyz):
    return (xyz[0] * cube + xyz[1]) * cube + xyz[2]
clicks = [e for e in a["log"] if e.get("event") in ("birth", "credit") and flat(e["node"]) in first_freeze and e["i"] >= first_freeze[flat(e["node"])]]
print("clicks at a frozen Node after its first freeze, flagged:", len(clicks), "births among them", sum(1 for e in clicks if e["event"] == "birth"))
rows_a = {r["i"]: r for r in a["rows"]}
rows_b = {r["i"]: r for r in b["rows"]}
print("max bits flagged", max(r["max bits"] for r in a["rows"]), "transient", max(r["max transient bits"] for r in a["rows"]), "head", max(r["max bits"] for r in b["rows"]), max(r["max transient bits"] for r in b["rows"]))
print("integers per Node flagged", set(r["integers"] for r in a["rows"]), "links at the wall max flagged", max(r["links at the wall"] for r in a["rows"]))
print("first interval the two records part (by rows):", next((i for i in sorted(rows_a) if rows_a[i] != rows_b.get(i)), None))
print("turns flagged", a["counts"]["turns"], "head", b["counts"]["turns"], "; births", a["counts"]["births"], b["counts"]["births"], "; body_clicks", a["counts"]["body_clicks"], b["counts"]["body_clicks"])
