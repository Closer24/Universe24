"""H-Moving-Born-Pair-2: the born pairs per row. For every birth (the log): the row, the wave (axis, side, h, den sin k), the Link's current across the born Link from the levels laid, F = now_m . G . before_p - before_m . G . now_p (0 exactly for the conjugate pair in the rational algebra; the residue the rounding's), the charges W, the refusal at the pair's Link at the next close (the log's refused events naming the pair's ends), the merger's take-back (delay), and the row's credits at the pair's ends and anywhere after the birth. Integers only. Usage: python pair_reader.py <record> <src of the flagged copy> <out.json>"""

import json
import sys
from collections import Counter

sys.path.insert(0, sys.argv[2])
from event_universe import gram  # noqa: E402

r = json.load(open(sys.argv[1]))
rows = r["universe"]["rows"]
log = r["log"]
A, B = None, None
births = [e for e in log if e["event"] == "birth" and "takes" not in e]
mergers = [e for e in log if e["event"] == "birth" and "takes" in e]
credits = [e for e in log if e["event"] == "credit"]
refused = [e for e in log if e["event"] == "refused"]
per_row = {}
found = []
for e in births:
    s = e["line_pair"]
    shape = len(e["stood"][0]) // 2
    g = gram.gram(shape)
    ends = {tuple(e["minus"]), tuple(e["plus"])}
    lev = e.get("mb_levels")
    F = None
    if lev is not None:
        nm, bm = lev[0][0::2], lev[0][1::2]
        np_, bp = lev[1][0::2], lev[1][1::2]
        form = lambda x, y: sum(x[i] * g[i][j] * y[j] for i in range(len(x)) for j in range(len(x)))
        F = form(nm, bp) - form(bm, np_)
    back = [m for m in mergers if m["i"] > e["i"] and {tuple(t["node"]) for t in m["takes"]} == ends and m.get("taken_row") == s]
    delay = back[0]["i"] - e["i"] if back else None
    nxt = [(x.get("cause"), x["i"]) for x in refused if x["i"] == e["i"] + 1 and x.get("row") == s and (tuple(x["node"]) in ends) and ("link" in x and tuple(x["link"]) in ends)]
    at_ends = [c for c in credits if c["i"] > e["i"] and c.get("row") == s and tuple(c["node"]) in ends]
    anywhere = [c for c in credits if c["i"] > e["i"] and c.get("row") == s]
    d = per_row.setdefault(s, {"shape": shape, "births": 0, "taken back": 0, "delays": Counter(), "F zero": 0, "F nonzero": 0, "W sum zero": 0, "refused at the next close": Counter(), "credits at the ends after": 0, "h zero": 0})
    d["births"] += 1
    d["taken back"] += bool(back)
    if delay:
        d["delays"][delay] += 1
    if F is not None:
        d["F zero" if F == 0 else "F nonzero"] += 1
    d["W sum zero"] += sum(e["W_children"]) == 0
    for cause, _i in nxt:
        d["refused at the next close"][cause] += 1
    d["credits at the ends after"] += len(at_ends)
    if e.get("mb_wave") and e["mb_wave"][2] == 0:
        d["h zero"] += 1
    found.append({"i": e["i"], "row": s, "shape": shape, "wave": e.get("mb_wave"), "F": F, "W": e["W_children"], "delay": delay, "refused next": nxt, "credits at ends after": len(at_ends), "credits of the row after": len(anywhere)})
for d in per_row.values():
    d["delays"] = dict(d["delays"])
    d["refused at the next close"] = dict(d["refused at the next close"])
out = {"record": sys.argv[1], "per row": per_row, "births": found}
json.dump(out, open(sys.argv[3], "w"), indent=1)
print(json.dumps({"record": sys.argv[1].split("/")[-1], "per row": per_row}))
