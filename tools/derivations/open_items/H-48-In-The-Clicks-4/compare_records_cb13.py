"""Compare a world's record under the build with the parent's; the laws on each. Usage: compare_records.py <src> <new.json> <parent.json or ->"""
import json
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.gates import gates  # noqa: E402


def floats(x):
    bad = []
    json.loads(x, parse_float=lambda s: bad.append(s))
    return len(bad)


def laws(path):
    text = open(path, encoding="utf-8").read()
    r = json.loads(text)
    rows = r["rows"]
    print(" ", path.split("/")[-2], path.split("/")[-1], "run_back", r["run_back"], "integers per Node", sorted({row["integers"] for row in rows}), "max bits", max(max(row["max bits"], row["max transient bits"]) for row in rows), "floats in file", floats(text), "counts", {k: r["counts"][k] for k in ("births", "body_clicks", "laid_back", "turns", "refused_origin")}, "turns len", len(r["turns"]))
    g = gates(r)
    for k, v in g.items():
        if k.startswith("1 ") or k.startswith("46 "):
            print("   ", k, json.dumps(v)[:400])
    return r


a = laws(sys.argv[2])
if sys.argv[3] != "-":
    b = laws(sys.argv[3])
    timeless = lambda rs: [{k: v for k, v in row.items() if k != "milliseconds"} for row in rs]
    same = {k: (a[k] == b[k]) for k in ("log", "counts", "turns", "nodes", "run_back")}
    same["rows"] = timeless(a["rows"]) == timeless(b["rows"])
    print("  build against parent:", same)
    if not same["log"]:
        for i, (x, y) in enumerate(zip(a["log"], b["log"])):
            if x != y:
                print("  first log difference at index", i, "interval", x.get("i"), json.dumps(x)[:200], "||", json.dumps(y)[:200]); break
