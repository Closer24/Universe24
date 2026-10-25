"""ma1's reader of the engine's own record (run.py's): the mean X course from the Node lines, the tops with every Node turned, the returns to Gamma, the counts, the run back, the births and credits (interval, node, line, sense). Integers only."""
import json, sys
sys.set_int_max_str_digits(0)
r = json.load(open(sys.argv[1]))
gamma = r["gamma"]
nodes = r["nodes"]
n = len(nodes[0]["X"])
means = [(x["i"], sum(x["X"]) // n) for x in nodes]
tops = [(x["i"], sum(x["X"]) // n) for x in nodes if len(x["turned"]) == n]
partial = [(x["i"], len(x["turned"])) for x in nodes if 0 < len(x["turned"]) < n]
returns = [i for i, m in means if m == gamma]
e_marks = []
for x in nodes:
    if x["i"] % 40 == 0:
        xs = x["X"]
        e_marks.append((x["i"], (1000 * (max(xs) - min(xs))) // min(xs)))
births = [(e["i"], e["node"], e["line_pair"], e["W_children"]) for e in r["log"] if e["event"] == "birth"]
credits = [(e["i"], e["node"], e["line"], e["sense"], e["beat"]) for e in r["log"] if e["event"] == "credit"]
print(json.dumps({
    "file": sys.argv[1], "nodes": n, "intervals": r["intervals"],
    "mean at the marks": [m for m in means if m[0] % 50 == 0 or m[0] in (58, 115, 116, 173, 230, 231, 288, 345, 346)],
    "mean's peak": max(means, key=lambda t: t[1]),
    "tops with every Node turning": tops[:8], "partial turns (first 6)": partial[:6],
    "returns to Gamma": returns[:8], "e (max-min over the board) at every 40th": e_marks,
    "counts": {k: v for k, v in r["counts"].items() if v != "0"}, "run back": r["run_back"],
    "births (i, node, line, W children)": births[:12], "births total": len(births),
    "credits (i, node, line, sense, beat)": credits[:40], "credits total": len(credits),
    "credit senses summed": sum(c[3] for c in credits),
    "lay log": [e for e in r["log"] if e["event"] == "lay"][:2],
}))
