"""The identity per close: the board's L2 change across the close (am2's reader, dL2_click) against the clicks' J from the record alone."""
import json, sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from moment_of_clicks import moment_of_clicks
rec = json.load(open(sys.argv[1])); board = json.load(open(sys.argv[2]))
J = moment_of_clicks(rec)["per close"]
exact = miss = 0; worst = 0; misses = []
births_by_i = {}
for e in rec["log"]:
    if e["event"] == "birth" and any(any(s) for s in e.get("stood", [])):
        births_by_i[int(e["i"])] = births_by_i.get(int(e["i"]), 0) + 1
for p in board["per_interval"]:
    i = p["i"]; d = p["dL2_click"]; j = J.get(i, {"J": [0, 0, 0]})["J"]
    if d == j:
        exact += 1
    else:
        miss += 1; gap = [x - y for x, y in zip(d, j)]; worst = max(worst, max(abs(g) for g in gap))
        misses.append({"i": i, "dL2_click": d, "J_clicks": j, "gap": gap, "births with a child on standing light": births_by_i.get(i, 0)})
print(json.dumps({"record": sys.argv[1], "closes": len(board["per_interval"]), "exact": exact, "not exact": miss, "worst gap abs": worst,
                  "closes with a click": len(J), "misses": misses, "counts board": board["counts"], "L2 end board": board["per_interval"][-1]["L2_end"],
                  "dL2 summed over the run, the interval's acts before the close": [sum(p.get("dL2_before_close", [x + y + z for x, y, z in zip(p.get("dL2_step", [0]*3), p.get("dL2_write", [0]*3), p.get("dL2_swap", [0]*3))])[a] for p in board["per_interval"]) for a in range(3)],
                  "closes where the board's L2 moved and no click": sum(1 for p in board["per_interval"] if any(p["dL2_click"]) and p["i"] not in J),
                  "click": [sum(p["dL2_click"][a] for p in board["per_interval"]) for a in range(3)]}))
