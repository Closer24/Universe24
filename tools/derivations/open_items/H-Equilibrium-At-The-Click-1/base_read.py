"""Read a record of the head's writer (run.py's out.json): the bottoms of the mean X, the tops, the credits per interval with their levels and the per-Node sums of levels taken before each bottom, the shortfall 1000 - X at each bottom; integers only."""
import json, sys
sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
gamma = rec["gamma"]
nodes = rec["nodes"]
means = []
alike = 0
for line in nodes:
    x = line["X"]
    means.append(sum(x) // len(x))
    alike += min(x) == max(x)
n = len(means)
bottoms = [(k + 1, means[k]) for k in range(1, n - 1) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
tops = rec["turns"]
credits = [e for e in rec["log"] if e["event"] == "credit"]
by_i = {}
for c in credits:
    by_i.setdefault(c["i"], []).append(c)
print("alike", alike, "of", n, "tops", tops, "bottoms", bottoms, "births", rec["counts"]["births"], "credits", len(credits), "laid", rec["counts"]["laid"], "run back", rec["run_back"])
print("credit intervals (i: count, levels each, beat, line):")
for i in sorted(by_i):
    cs = by_i[i]
    print(" ", i, len(cs), sorted(set(c["levels"] for c in cs)), sorted(set(c["beat"] for c in cs)), sorted(set(c["line"] for c in cs)), "taken", sorted(set(c["taken"] for c in cs)))
cube = rec["cube"]
for b_i, b_x in bottoms:
    per_node = {}
    for c in credits:
        if c["i"] <= b_i:
            per_node[tuple(c["node"])] = per_node.get(tuple(c["node"]), 0) + c["levels"]
    sums = sorted(set(per_node.values()))
    print("bottom", b_i, "X", b_x, "shortfall", gamma - b_x, "levels taken per Node before it", sums, "nodes", len(per_node), "credits before it", sum(1 for c in credits if c["i"] <= b_i))
