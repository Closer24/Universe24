import json, sys
from collections import Counter
d = json.load(open(sys.argv[1]))
log, nodes, rows = d["log"], d["nodes"], d["rows"]
G = d["G"]; gamma = d["gamma"]
births = [e for e in log if e["event"] == "birth"]
print("births", len(births), "at intervals", Counter(e["i"] for e in births), "distinct nodes", len({tuple(e["node"]) for e in births}))
print("birth keys", sorted(births[0].keys()))
print("taken lines at births", Counter(str(e.get("taken_line")) for e in births))
credits = [e for e in log if e["event"] == "credit"]
print("credits", len(credits), "laid_back count", d["counts"]["laid_back"], "credit keys", sorted(credits[0].keys()))
stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop"]
print("stop refusals", len(stops), "fall values", Counter(e["fall"] for e in stops).most_common(5), "intervals", min(e["i"] for e in stops) if stops else None, max(e["i"] for e in stops) if stops else None)
print("refused causes", Counter(e["cause"] for e in log if e["event"] == "refused"))
Xmax = [(n["i"], max(n["X"])) for n in nodes]
tops = [i for i, x in Xmax if x == max(x for _, x in Xmax)]
# local maxima of mean X
import statistics
mx = [(n["i"], max(n["X"]), min(n["X"])) for n in nodes]
peaks = [mx[k][0] for k in range(1, len(mx) - 1) if mx[k][1] > mx[k-1][1] and mx[k][1] >= mx[k+1][1]]
print("X peaks (local maxima of max X) at", peaks[:10], "values", [(i, x, mn) for i, x, mn in mx if i in peaks][:6])
print("nodes keys", sorted(nodes[0].keys()))
turned = [(n["i"], sum(1 for t in n["turned"] if t)) for n in nodes if any(n["turned"])] if "turned" in nodes[0] else None
print("intervals with turns (i, count)", turned[:10] if turned else None, "total turns", d["counts"]["turns"])
gam = [(n["i"], Counter(n["X"])) for n in nodes if all(x == gamma for x in n["X"])]
print("X == Gamma at every Node at", [i for i, _ in gam])
print("X at 218", Counter(nodes[217]["X"]), "at 442", Counter(nodes[441]["X"]), "at 109", Counter(nodes[108]["X"]).most_common(3), "at 330", Counter(nodes[329]["X"]).most_common(3))
print("integers", Counter(r["integers"] for r in rows), "max bits", max(r["max bits"] for r in rows), "max transient bits", max(r["max transient bits"] for r in rows))
print("run_back", d["run_back"], "intervals", d["intervals"], "turns", d["turns"])
print("lay", {k: (v if k != "p1" else v) for k, v in log[0].items()})
