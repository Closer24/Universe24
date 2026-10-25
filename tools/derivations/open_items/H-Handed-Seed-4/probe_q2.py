"""cs4: the light's own closing on cs3's cyc_c14_q2 record: the credits' attempts (the stop refusals whose walls are the light's unit) and the credits by interval, with the fall values; the diag's light share per interval."""
import json, sys
sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
log = rec["log"]
unit = int(rec["log"][0]["unit"])
print("unit", unit)
stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop" and int(e["walls"]) == unit]
by_i = {}
for e in stops:
    by_i.setdefault(e["i"], []).append(int(e["fall"]))
for i in sorted(by_i)[:40]:
    f = by_i[i]
    print("credit attempts refused at", i, "count", len(f), "fall min/max", min(f), max(f))
credits = [e for e in log if e["event"] == "credit"]
ci = {}
for e in credits:
    ci[e["i"]] = ci.get(e["i"], 0) + 1
print("credits per interval", sorted(ci.items())[:40])
d = rec["diag"]
print("share hundredths / whole nodes / X_mean at 1..12 and 165..175:", [(x["i"], x["light_share_min_max_hundredths"], x["light_share_whole_nodes"], x["X_mean"]) for x in d if x["i"] <= 12 or 165 <= x["i"] <= 175])
print("whole nodes count per interval (first 200):", [x["light_share_whole_nodes"] for x in d[:200]])
