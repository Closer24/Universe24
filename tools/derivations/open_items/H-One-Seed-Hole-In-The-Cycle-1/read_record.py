"""os1's reader of a record of event_universe.run: per interval X min / max / distinct over the Nodes, turned and frozen counts; the exact returns to Gamma at every Node; the first parted interval; the births by interval with their Nodes; the credits; the run back; the integers and bits; the lay lines. Integers only. Usage: read_record.py <record.json> [first N intervals shown, default 12]"""
import json
import sys

sys.set_int_max_str_digits(0)


def main(path, first):
    r = json.load(open(path))
    gamma = int(r["gamma"])
    nodes = r["nodes"]
    n = len(nodes)
    cube = int(r["cube"])
    count = cube**3
    log = r["log"]
    lays = [e for e in log if e["event"] == "lay"]
    print("record", path.split("/")[-1], "| intervals", n, "| cube", cube, "| Gamma", gamma, "| run back", r["run_back"], "| counts", r["counts"])
    print("lays:", len(lays), "| the wave lay:", [{k: e[k] for k in ("quanta", "amplitude", "share", "sense") if k in e} for e in lays if "p1" in e])
    rows = r["rows"]
    print("integers", rows[-1].get("integers"), "| max bits", max(int(x.get("max bits", 0)) for x in rows), "| max transient bits", max(int(x.get("max transient bits", 0)) for x in rows))
    per = []
    for d in nodes:
        x = [int(v) for v in d["X"]]
        per.append((int(d["i"]), min(x), max(x), len(set(x)), len(d["turned"]), len(d["frozen"]), len(d["held"])))
    print("the first intervals (i, X min, X max, X distinct, turned, frozen, held Links):")
    for p in per[:first]:
        print("  ", p)
    exact = [p[0] for p in per if p[1] == p[2] == gamma]
    print("exact returns to Gamma at every Node:", exact)
    parted = next((p[0] for p in per if p[3] > 1), None)
    print("the first parted interval (X distinct above 1):", parted, "| uniform intervals:", sum(1 for p in per if p[3] == 1), "of", n)
    whole = [p[0] for p in per if p[4] == count]
    parts = [(p[0], p[4]) for p in per if 0 < p[4] < count]
    print("intervals with every Node turning:", whole[:12], "| turns in parts (first 12):", parts[:12], "| count", len(parts))
    frozen = [(p[0], p[5]) for p in per if p[5] > 0]
    print("frozen Nodes (i, count), first 12:", frozen[:12], "| intervals with a frozen Node:", len(frozen), "| the most frozen at once:", max((p[5] for p in per), default=0))
    held = [(p[0], p[6]) for p in per if p[6] > 0]
    print("held Links (i, count), first 8:", held[:8], "| intervals with a held Link:", len(held))
    bottom = min(per, key=lambda p: p[1])
    top = max(per, key=lambda p: p[2])
    print("the lowest X (i, min, max):", bottom[:3], "| the highest X:", top[:3], "| X at the end (min, max, distinct):", per[-1][1:4])
    births = [e for e in log if e["event"] == "birth"]
    by_i = {}
    for e in births:
        by_i.setdefault(int(e["i"]), []).append(e)
    print("births:", len(births), "| by interval (i, count, Nodes):", [(i, len(v), len({tuple(e["node"]) for e in v})) for i, v in sorted(by_i.items())][:24])
    credits = [e for e in log if e["event"] == "credit"]
    ci = {}
    for e in credits:
        ci.setdefault(int(e["i"]), []).append(e)
    print("credits:", len(credits), "| laid back", sum(1 for e in credits if "laid_back" in e), "| by interval (i, count), first 16:", [(i, len(v)) for i, v in sorted(ci.items())][:16])
    refused = {}
    for e in log:
        if e["event"] == "refused":
            refused[e.get("cause")] = refused.get(e.get("cause"), 0) + 1
    print("refusals by cause:", refused)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 12)
