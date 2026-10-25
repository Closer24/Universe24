"""eq2's reading of a record (the writer's JSON): the mean X per interval from the Node lines, the tops with every Node turning at once, the bottoms (board.bottoms_of's predicate), the retrace X(top + k) against X(top - k) with the first k that parts, the credits per interval with their levels and the laid-back count, the stop refusals, the counts, the run back, the bits, and gates 1 / 46 / 8 through the engine's table. Usage: read_record.py <record.json> [--gates]. Integers only."""
import json
import sys
from collections import Counter

sys.set_int_max_str_digits(0)


def read(path, with_gates):
    run = json.load(open(path, encoding="utf-8"))
    gamma = int(run["gamma"])
    lines = run["nodes"]
    count = len(lines[0]["X"])
    means = {int(l["i"]): sum(int(x) for x in l["X"]) // count for l in lines}
    spread = {int(l["i"]): max(int(x) for x in l["X"]) - min(int(x) for x in l["X"]) for l in lines}
    tops = [int(l["i"]) for l in lines if len(l["turned"]) == count]
    turned_some = [(int(l["i"]), len(l["turned"])) for l in lines if 0 < len(l["turned"]) < count]
    ks = sorted(means)
    bottoms = [
        (k, means[k], all(int(x) == gamma for x in lines[k - 1]["X"]))
        for k in ks[1:-1]
        if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]
    log = run["log"]
    credits = [e for e in log if e["event"] == "credit"]
    per_interval = Counter(int(c["i"]) for c in credits)
    levels_at = {}
    for c in credits:
        levels_at.setdefault(int(c["i"]), Counter())[int(c["levels"])] += 1
    laid_back = sum(1 for c in credits if "laid_back" in c)
    stops = Counter(int(e["i"]) for e in log if e["event"] == "refused" and e["cause"] == "stop")
    arrivals = Counter(int(e["i"]) for e in log if e["event"] == "refused" and e.get("cause") == "arrival")
    out = {
        "record": path,
        "cube": run["cube"],
        "intervals": run["intervals"],
        "counts": run["counts"],
        "run_back": run["run_back"],
        "max bits": max(int(r["max bits"]) for r in run["rows"]),
        "integers": run["rows"][-1]["integers"],
        "alike (spread 0) of intervals": [sum(1 for k in ks if spread[k] == 0), len(ks)],
        "tops (every Node turning at once)": tops,
        "partial turns (interval, count)": turned_some[:10],
        "bottoms (interval, mean X, at Gamma at every Node)": bottoms,
        "credits": len(credits),
        "credits laid back": laid_back,
        "credit intervals (first 12: interval, count, levels->count)": [
            (i, per_interval[i], dict(levels_at[i])) for i in sorted(per_interval)[:12]
        ],
        "credit intervals in all": len(per_interval),
        "stop refusals (intervals, count)": [len(stops), sum(stops.values())],
        "arrival refusals (intervals, count)": [len(arrivals), sum(arrivals.values())],
        "laid": run["counts"].get("laid"),
    }
    # the retrace about every whole-board top: X(top + k) against X(top - k)
    retrace = []
    for top in tops:
        first = None
        same = 0
        for k in range(1, min(top - 1, ks[-1] - top) + 1):
            if means[top + k] == means[top - k]:
                same += 1
            elif first is None:
                first = (k, top - k, means[top - k], top + k, means[top + k])
        retrace.append({"top": top, "equal k": same, "first parting (k, i_rise, X_rise, i_fall, X_fall)": first})
    out["retrace"] = retrace
    # the credits by cycle (between the bottoms)
    edges = [0] + [b[0] for b in bottoms] + [ks[-1] + 1]
    out["credits per cycle (lo, hi, credits, levels summed)"] = [
        (lo, hi, sum(1 for c in credits if lo < int(c["i"]) <= hi), sum(int(c["levels"]) for c in credits if lo < int(c["i"]) <= hi))
        for lo, hi in zip(edges, edges[1:])
    ]
    out["X at the bottoms and the intervals around (i, mean)"] = [
        [(k, means[k]) for k in range(max(b[0] - 3, 1), min(b[0] + 3, ks[-1]) + 1)] for b in bottoms
    ]
    if with_gates:
        from event_universe import gates as table

        g = table.gates(run)
        out["gates"] = {k: v for k, v in g.items() if k.startswith(("1 ", "46 ", "8 ", "7 ", "18 ", "47 ", "40 "))}
    return out


if __name__ == "__main__":
    found = read(sys.argv[1], "--gates" in sys.argv)
    print(json.dumps(found, indent=1, default=str))
