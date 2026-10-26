"""H-Quartet-Carriage-1's reader of the quartet row's credits on a record (a reader of the log; no engine import): every credit whose frame carries the axial vector, grouped by Node; for each world-laid quartet body (the log's lay events with a vector) the credits at its centre and at the centre's six neighbours: the lay axis's sign kept at N of M credits, the lay axis dominant at N of M; the turn per interval between consecutive credits at one Node as integers: the off-axis part's change (the sum of the absolute changes on the two other axes) over the axial's absolute value on the lay axis, and the count of intervals between them, each as [off change, axial, intervals]; the odd lines' size at the credits (the frame's odd entries, the curl's bound) as the largest absolute entry. Integers only.
Usage: python axis_track_reader.py <record.json> <out.json>"""
import json
import sys
from collections import defaultdict

AXES = 3
PORT_SIDES = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]


def sign(x):
    return (x > 0) - (x < 0)


def main():
    rec = json.load(open(sys.argv[1]))
    cube = int(rec["world"]["shape"][0]) if "world" in rec else int(rec["cube"])
    log = rec["log"]
    credits = [x for x in log if x["event"] == "credit" and "axial" in x.get("frame", {})]
    by_node = defaultdict(list)
    for c in credits:
        by_node[tuple(int(v) for v in c["node"])].append(c)
    lays = [x for x in log if x["event"] == "lay" and x.get("vector")]
    odd_max = max((max(abs(int(o)) for o in c["frame"].get("odd", [0])) for c in credits), default=0)
    out = {"record": sys.argv[1], "quartet credits": len(credits), "nodes credited": len(by_node), "odd max abs at the credits": odd_max, "bodies": []}
    for lay in lays:
        centre = tuple(int(v) for v in (lay.get("node") or lay.get("centre")))
        ax = lay.get("axial") or lay.get("axis")
        window = [centre] + [tuple((centre[a] + (side if a == axis else 0)) % cube for a in range(AXES)) for axis, side in PORT_SIDES]
        body = {"node": list(centre), "vector": lay["vector"], "lay event keys": sorted(lay.keys())}
        kept = dom = total = 0
        turns = []
        first = None
        for at in window:
            here = sorted(by_node.get(at, []), key=lambda c: int(c["i"]))
            prev = None
            for c in here:
                axial = [int(v) for v in c["frame"]["axial"]]
                if first is None:
                    first = axial
                    body_axis = max(range(AXES), key=lambda a: abs(first[a]))
                    body_sign = sign(first[body_axis])
                total += 1
                kept += sign(axial[body_axis]) == body_sign
                dom += max(range(AXES), key=lambda a: abs(axial[a])) == body_axis
                if prev is not None:
                    off = sum(abs(axial[a] - prev[1][a]) for a in range(AXES) if a != body_axis)
                    turns.append([off, abs(prev[1][body_axis]), int(c["i"]) - prev[0]])
                prev = (int(c["i"]), axial)
        body.update({"first axial read": first, "sign kept": [kept, total], "dominant kept": [dom, total], "turns [off change, axial, intervals] (first 12)": turns[:12], "turns count": len(turns), "turn sum [off, axial, intervals]": [sum(t[0] for t in turns), sum(t[1] for t in turns), sum(t[2] for t in turns)]})
        out["bodies"].append(body)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "bodies"}))
    for b in out["bodies"]:
        print(json.dumps(b))


main()
