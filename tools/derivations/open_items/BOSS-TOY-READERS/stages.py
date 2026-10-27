"""The bang in stages, read from a record's Node lines: per interval the content's max and mean, the frozen count,
the X width, births and credits at that interval; the peaks of contraction (a local maximum of the content's max),
the exact returns (every Node at content 0 and X at the resolution) and the eras between. Integers only."""
import json, sys
sys.set_int_max_str_digits(2000000)
r = json.load(open(sys.argv[1]))
gamma = int(r["gamma"])
births = {}; credits = {}
for e in r["log"]:
    if e.get("event") == "birth": births[e["i"]] = births.get(e["i"], 0) + 1
    if e.get("event") == "credit": credits[e["i"]] = credits.get(e["i"], 0) + 1
rows = []
for f in r["nodes"]:
    c = [int(x) for x in f["content"]]; X = [abs(int(x)) for x in f["X"]]
    rows.append(dict(i=f["i"], cmax=max(c), cmean=sum(c) // len(c), frozen=len(f["frozen"]), turned=len(f["turned"]),
                     xbits=max(X).bit_length(), ret=(max(c) == 0 and max(X) == gamma and min(X) == gamma),
                     births=births.get(f["i"], 0), credits=credits.get(f["i"], 0)))
peaks = [rows[k]["i"] for k in range(1, len(rows) - 1) if rows[k]["cmax"] > rows[k-1]["cmax"] and rows[k]["cmax"] >= rows[k+1]["cmax"] and rows[k]["cmax"] > 0]
rets = [x["i"] for x in rows if x["ret"]]
print(f"{sys.argv[1]}: {len(rows)} intervals, births {r['counts']['births']}, credits {r['counts']['body_clicks']}, widest X {max(x['xbits'] for x in rows)} bits")
print(f"  exact returns to the seed: {rets}")
print(f"  contraction peaks (content max): {[(p, rows[p-1]['cmax']) for p in peaks][:16]}")
print(f"  births at: {sorted(births)[:20]}")
print(f"  credits at: {sorted(credits)[:20]}")
if len(sys.argv) > 2:
    print("  i    cmax   cmean  frozen turned xbits births credits ret")
    for x in rows:
        print(f"  {x['i']:<4} {x['cmax']:<6} {x['cmean']:<6} {x['frozen']:<6} {x['turned']:<6} {x['xbits']:<5} {x['births']:<6} {x['credits']:<7} {'R' if x['ret'] else ''}")
