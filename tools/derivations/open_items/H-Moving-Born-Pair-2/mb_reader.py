"""H-Moving-Born-Pair-2's reader of a record under MB_S1 against the head's record of the same world: per birth the wave (axis, side, h, den sin k) and the levels laid; the born pair's survival (a merger, a birth entry with takes, at the pair's two ends at a later close: taken back at the delay d; the pairs never taken back); the first parting interval against the head's log (the first interval whose events, births and credits by Node and row, differ) and the counts; the children's row credited at the pair's ends after the birth. Integers only. Usage: python mb_reader.py <flagged record> <head record or none> <out.json>"""

import json
import sys
from collections import Counter


def events_by_interval(log):
    found = {}
    for e in log:
        key = (e["event"], tuple(e["node"]), e.get("line_pair"), e.get("taken_row"), e.get("row"))
        found.setdefault(int(e["i"]), []).append(key)
    return found


r = json.load(open(sys.argv[1]))
log = r["log"]
births = [e for e in log if e["event"] == "birth" and "takes" not in e]
mergers = [e for e in log if e["event"] == "birth" and "takes" in e]
credits = [e for e in log if e["event"] == "credit"]
out = {"record": sys.argv[1], "counts": r["counts"], "run_back": r.get("run_back"), "births": len(births), "mergers": len(mergers), "credits": len(credits)}
waves, taken_back, delays, survived = [], 0, Counter(), []
for e in births:
    ends = {tuple(e["minus"]), tuple(e["plus"])}
    back = [m for m in mergers if m["i"] > e["i"] and {tuple(t["node"]) for t in m["takes"]} == ends and m.get("taken_row") == e["line_pair"]]
    if back:
        taken_back += 1
        delays[back[0]["i"] - e["i"]] += 1
    else:
        survived.append([e["i"], e["node"], e["line_pair"]])
    later = [c for c in credits if c["i"] > e["i"] and tuple(c["node"]) in ends and c.get("row") == e["line_pair"]]
    waves.append({"i": e["i"], "row": e["line_pair"], "minus": e["minus"], "plus": e["plus"], "wave": e.get("mb_wave"), "phase": e.get("mb_phase"), "levels": e.get("mb_levels"), "W": e["W_children"], "dP_take": e["dP_take"], "credits of the row at the ends after": len(later), "taken back": bool(back)})
out["waves"] = waves
out["pairs taken back by a merger"] = f"{taken_back} of {len(births)}"
out["delays"] = dict(delays)
out["pairs surviving (i, node, row)"] = survived
out["h zero"] = sum(1 for w in waves if w["wave"] and w["wave"][2] == 0)
out["h above zero"] = sum(1 for w in waves if w["wave"] and w["wave"][2] > 0)
out["at the band's edge"] = sum(1 for w in waves if w["wave"] and w["wave"][3] == int(r["den"]))
out["W summed per pair 0"] = f"{sum(1 for w in waves if sum(w['W']) == 0)} of {len(waves)}"
if sys.argv[2] != "none":
    h = json.load(open(sys.argv[2]))
    a, b = events_by_interval(log), events_by_interval(h["log"])
    first = None
    for i in sorted(set(a) | set(b)):
        if Counter(a.get(i, [])) != Counter(b.get(i, [])):
            first = i
            break
    out["head counts"] = h["counts"]
    out["first parting interval (events)"] = first
    out["head births"] = sum(1 for e in h["log"] if e["event"] == "birth" and "takes" not in e)
    out["head credits"] = sum(1 for e in h["log"] if e["event"] == "credit")
    out["rows equal at the marks"] = r.get("rows") == h.get("rows")
json.dump(out, open(sys.argv[3], "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "waves"}))
