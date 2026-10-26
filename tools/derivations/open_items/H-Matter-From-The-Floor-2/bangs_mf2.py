"""mf2, question (8): the tops (every Node turned at one interval), the bottoms (every Node's content at Gamma), the excess (+ child at the take's Node less the other end) running over the record and read at each top and bottom, the charge (W total, W abs sum at the reader's marks) around the tops, the children's W by sign per bang, the run back's span."""
import json
import sys

rec = json.load(open(sys.argv[1]))
gamma = int(rec["gamma"])
nodes = rec["nodes"]
tops = [int(e["i"]) for e in nodes if sum(1 for t in e["turned"] if t) == len(e["turned"])]
bottoms = [int(e["i"]) for e in nodes if all(int(c) == gamma for c in e["content"])]
births = [e for e in rec["log"] if e["event"] == "birth"]
def excess_to(i):
    return sum((tuple(e["plus"]) == tuple(e["node"])) - (tuple(e["minus"]) == tuple(e["node"])) for e in births if e["i"] <= i)
marks = sorted(((int(r["i"]), int(r["W total"]), int(r["W abs sum"]), int(r["turns"]), int(r["births"])) for r in rec["rows"]))
out = {"record": sys.argv[1], "gamma": gamma, "tops": tops, "bottoms": bottoms,
       "excess at tops": [[t, excess_to(t)] for t in tops], "excess at bottoms": [[b, excess_to(b)] for b in bottoms],
       "excess at the end": excess_to(10 ** 9), "births": len(births),
       "marks (i, W total, W abs sum, turns, births)": marks, "run_back": rec["run_back"]}
edges = [0] + tops + [10 ** 9]
per = []
for k in range(len(edges) - 1):
    bb = [e for e in births if edges[k] < e["i"] <= edges[k + 1]]
    per.append({"from top": edges[k], "to top": edges[k + 1], "births": len(bb), "excess": sum((tuple(e["plus"]) == tuple(e["node"])) - (tuple(e["minus"]) == tuple(e["node"])) for e in bb), "W_children > 0": sum(1 for e in bb for w in e["W_children"] if w > 0), "W_children < 0": sum(1 for e in bb for w in e["W_children"] if w < 0)})
out["per span between tops"] = per
print(json.dumps(out))
