"""Probe B1's table: reads the JSON lines b1_counts.py prints (one per chart) and prints the counts as a table,
then every line in full. Usage: python -I b1_counts.py --all > COUNTS; python -I b1_table.py COUNTS"""
import json
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
from bcommon import CHARTS  # noqa: E402

rows = [json.loads(line) for line in open(sys.argv[1]) if line.startswith("{")]
order = [w for w, _t in CHARTS]
rows.sort(key=lambda r: order.index(r["world"]))
hdr = ("chart", "ticks", "F1 >+hold", "F1 <-hold", "F1 max |N| div hold", "F2 t<0", "F2 t>Gamma", "F2 read",
       "F5 load<0", "F5 end", "clock-ticks", "ET fallback", "ET at turned", "ET at stopped", "ET neither", "R10 stopped", "turned")
print(" | ".join(hdr))
tot = {k: 0 for k in hdr[2:]}
for r in rows:
    vals = [r["F1 drive above the hold"], r["F1 drive below minus the hold"], r["F1 largest |drive| div hold"],
            r["F2 tension below 0"], r["F2 tension above Gamma"], r["F2 tensions read"],
            r["F5 load below 0 at the tick's start"], r["F5 load below 0 in the end state"], r["clock-ticks"],
            r["ET end teeth at or below 0 (the fallback)"], r["ET fallback at a turned clock"],
            r["ET fallback at a stopped clock"], r["ET fallback at a clock neither turned nor stopped"],
            r["R10 stopped clock-ticks"], r["turned clock-ticks"]]
    for k, v in zip(hdr[2:], vals):
        tot[k] = max(tot[k], v) if k.startswith("F1 max") else tot[k] + v
    f2 = f"{r['F2 tension below 0']} ({100 * r['F2 tension below 0'] // max(r['F2 tensions read'], 1)}%)"
    f2u = f"{r['F2 tension above Gamma']} ({100 * r['F2 tension above Gamma'] // max(r['F2 tensions read'], 1)}%)"
    print(" | ".join(str(x) for x in [r["world"].replace("world_", "").replace(".json", ""), r["ticks"], vals[0], vals[1], vals[2], f2, f2u, *vals[5:]]))
print(" | ".join(str(x) for x in ["all", "", *tot.values()]))
print()
print("Every chart's counts in full:")
for r in rows:
    print("- " + "; ".join(f"{k}: {v}" for k, v in r.items()))
