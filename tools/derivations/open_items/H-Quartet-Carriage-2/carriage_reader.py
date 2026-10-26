"""H-Quartet-Carriage-2's reader of a record under HQ_S1 (a reader of the log, no run): the quartet births and each pair's fate at the next closes (taken back by the merger: a later birth whose taken row is the quartet's at the pair's two ends, with its delay); the quartet record's credits along the track (every credit of the quartet row, grouped by Node): the axis sign on the lay's axis kept at N of M, the dominant axis at N of M, at the lay's own Node and over the board; the precession: between consecutive credits at one Node the axial vector's turn (the across part over the along part, thousandths per interval, and the cross product's sign) ; the seeded lays (amplitude, share, unit). Integers only.
Usage: python carriage_reader.py <record.json> <quartet record index> <axis 0..2 of the seeded lay or -1> <sign of the seeded lay> <out.json>"""
import json, sys
from collections import defaultdict

rec = json.load(open(sys.argv[1]))
q, axis, sgn = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
log = rec["log"]
births = [x for x in log if x["event"] == "birth"]
credits = [x for x in log if x["event"] == "credit" and int(x["line"]) == q]
lays = [x for x in log if x["event"] == "lay"]
out = {"record": sys.argv[1], "run_back": rec["run_back"], "births": len(births), "quartet credits": len(credits),
       "lays": [{k: x[k] for k in ("node", "line_pair", "width", "quanta", "amplitude", "share", "unit") if k in x} for x in lays]}
qb = [b for b in births if len(b["stood"][0]) == 16]
pairs = []
for b in qb:
    ends = {tuple(b["minus"]), tuple(b["plus"])}
    later = [x for x in births if int(x["i"]) > int(b["i"]) and x.get("taken_row") == q and "takes" in x and {tuple(t["node"]) for t in x["takes"]} == ends]
    pairs.append({"birth i": int(b["i"]), "minus": b["minus"], "plus": b["plus"], "W_children": b["W_children"],
                  "taken back by the merger": bool(later), "delay": None if not later else int(later[0]["i"]) - int(b["i"]),
                  "credits at the ends after the birth": sum(1 for c in credits if tuple(c["node"]) in ends and int(c["i"]) > int(b["i"]))})
out["quartet pairs born"] = pairs
out["pairs taken back at the next close"] = [sum(1 for p in pairs if p["taken back by the merger"] and p["delay"] == 1), len(pairs)]
# the merger's births on the seeded pair (no quartet birth): any birth taking the quartet row
out["mergers taking the quartet row"] = [{"i": int(x["i"]), "ends": [t["node"] for t in x["takes"]]} for x in births if x.get("taken_row") == q and "takes" in x]
def sign(x):
    return (x > 0) - (x < 0)
if axis >= 0:
    at_home = [c for c in credits if tuple(c["node"]) == tuple(lays[0]["node"])] if lays else []
    def kept(cs):
        return [sum(1 for c in cs if c["frame"]["axial_sign"][axis] == sgn), len(cs)]
    def dominant(cs):
        return [sum(1 for c in cs if max(range(3), key=lambda k, c=c: abs(int(c["frame"]["axial"][k]))) == axis and c["frame"]["axial_sign"][axis] == sgn), len(cs)]
    out["axis sign kept, all quartet credits"] = kept(credits)
    out["dominant axis kept, all quartet credits"] = dominant(credits)
    out["axis sign kept, at the lay's Node"] = kept(at_home)
    out["dominant axis kept, at the lay's Node"] = dominant(at_home)
    out["credits at the lay's Node, intervals"] = [int(c["i"]) for c in at_home][:40]
    out["first credits"] = [{"i": int(c["i"]), "node": c["node"], "levels_now": c["frame"]["levels_now"], "axial": c["frame"]["axial"], "W": c["frame"]["W"]} for c in credits[:6]]
    out["last credits"] = [{"i": int(c["i"]), "node": c["node"], "levels_now": c["frame"]["levels_now"], "axial": c["frame"]["axial"], "W": c["frame"]["W"]} for c in credits[-3:]]
    nodes_credited = len({tuple(c["node"]) for c in credits})
    out["Nodes credited"] = nodes_credited
    # the precession: consecutive credits at one Node, the axial's turn per interval
    by_node = defaultdict(list)
    for c in credits:
        by_node[tuple(c["node"])].append(c)
    turns = []
    for node, cs in by_node.items():
        for c1, c2 in zip(cs, cs[1:]):
            a1, a2 = [int(x) for x in c1["frame"]["axial"]], [int(x) for x in c2["frame"]["axial"]]
            di = int(c2["i"]) - int(c1["i"])
            cross = [a1[1] * a2[2] - a1[2] * a2[1], a1[2] * a2[0] - a1[0] * a2[2], a1[0] * a2[1] - a1[1] * a2[0]]
            dot = sum(x * y for x, y in zip(a1, a2))
            along = [a1[axis], a2[axis]]
            across1 = sum(a1[k] * a1[k] for k in range(3) if k != axis)
            across2 = sum(a2[k] * a2[k] for k in range(3) if k != axis)
            turns.append({"node": list(node), "i": [int(c1["i"]), int(c2["i"])], "intervals": di, "along": along,
                          "across squared": [across1, across2], "cross sign": [sign(x) for x in cross], "dot sign": sign(dot),
                          "across over along, thousandths": [None if a1[axis] == 0 else (1000 * across1) // (a1[axis] * a1[axis]), None if a2[axis] == 0 else (1000 * across2) // (a2[axis] * a2[axis])]})
    out["turns between consecutive credits at one Node"] = turns[:30]
    out["turns: dot sign counts"] = {str(s): sum(1 for t in turns if t["dot sign"] == s) for s in (-1, 0, 1)}
    out["turns: cross sign on the lay's axis counts"] = {str(s): sum(1 for t in turns if t["cross sign"][axis] == s) for s in (-1, 0, 1)}
json.dump(out, open(sys.argv[5], "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("turns between consecutive credits at one Node", "first credits", "last credits", "lays", "credits at the lay's Node, intervals")}))
if lays:
    print("lays", out["lays"])
