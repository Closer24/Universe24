"""H-Quartet-Children-1's reader of the measurement world (the brief's addition, question 8): the standing quartet bodies the world file laid (the log's lay events: centre, vector, sense), their own axial vector at their first credit before any quartet birth, the quartet births (the children's Nodes and axes), and at each body's Node every quartet credit after a quartet birth with the axial's change against the body's own, projected on the body's axis (the outcome's sign) and on the other axes; the cells by the body's axis; integers only.
Usage: python measure_reader.py <record.json> <src of the flagged copy> <out.json>"""
import json
import sys

sys.path.insert(0, sys.argv[2])
from event_universe import gram  # noqa: E402

AXES = 3


def sign(x):
    return (x > 0) - (x < 0)


def main():
    rec = json.load(open(sys.argv[1]))
    log = rec["log"]
    lays = [x for x in log if x["event"] == "lay" and "vector" in x]
    births = [x for x in log if x["event"] == "birth"]
    credits = [x for x in log if x["event"] == "credit" and "axial" in x["frame"]]
    qb = [b for b in births if len(b["stood"][0]) == 16]
    out = {"record": sys.argv[1], "births": len(births), "quartet births": [(int(b["i"]), b["minus"], b["plus"]) for b in qb], "bodies": []}
    first_birth = min((int(b["i"]) for b in qb), default=None)
    for lay in lays:
        v = lay["vector"]
        ax = [int(x) for x in gram.density(8, [sign_ * 0 + x for sign_, x in zip(v, v)])]
        body_axis = max(range(AXES), key=lambda k: abs(ax[k]))
        here = [c for c in credits if c["node"] == lay["node"]]
        own = next((c for c in here if first_birth is None or int(c["i"]) < first_birth), None)
        rows = []
        for c in here:
            if first_birth is None or int(c["i"]) <= first_birth or own is None:
                continue
            delta = [int(a) - int(b) for a, b in zip(c["frame"]["axial"], own["frame"]["axial"])]
            rows.append({"i": int(c["i"]), "axial": c["frame"]["axial"], "delta": delta, "outcome on the body's axis": sign(delta[body_axis]), "sense": c["sense"], "W": c["frame"]["W"]})
        out["bodies"].append({"node": lay["node"], "vector": v, "axial of the vector": ax, "body axis": body_axis, "own axial at the first credit": None if own is None else own["frame"]["axial"], "credits before the first quartet birth": sum(1 for c in here if first_birth is not None and int(c["i"]) < first_birth), "credits after": len(rows), "outcomes (-1, 0, +1)": [sum(1 for r in rows if r["outcome on the body's axis"] == s) for s in (-1, 0, 1)], "first rows": rows[:6]})
    json.dump(out, open(sys.argv[3], "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "bodies"}))
    for b in out["bodies"]:
        print(json.dumps({k: v for k, v in b.items() if k != "first rows"}))
        for r in b["first rows"]:
            print("  ", json.dumps(r))


if __name__ == "__main__":
    main()
