"""rg1: the stops (refused by name `stop`) and the lay refusals of a cs6_run record by interval and by phase class for the first intervals: the count, the fall over the walls in thousandths (min, max), the taken row; the births' Nodes by class. Integers only. Usage: python read_stops.py <record.json> [intervals shown, default 8]"""
import json
import sys

sys.set_int_max_str_digits(0)
r = json.load(open(sys.argv[1]))
upto = int(sys.argv[2]) if len(sys.argv) > 2 else 8
cube = int(r["cube"])
log = r["log"]
lay = next(e for e in log if e["event"] == "lay_pattern")
phases = lay["phases"]
cls = lambda node: phases[(node[0] * cube + node[1]) * cube + node[2]]
for i in range(1, upto + 1):
    stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop" and e["i"] == i]
    lays = [e for e in log if e["event"] == "refused" and e["cause"] == "lay" and e["i"] == i]
    births = [e for e in log if e["event"] == "birth" and e["i"] == i]
    by = {}
    for e in stops:
        by.setdefault((cls(e["node"]), e.get("row")), []).append(1000 * int(e["fall"]) // int(e["walls"]) if int(e["walls"]) else None)
    print(f"i {i}: births {len(births)} at classes {sorted({cls(e['node']) for e in births})}; lay refusals {len(lays)} at classes {sorted({cls(e['node']) for e in lays})}; stops {len(stops)}:")
    for k in sorted(by, key=str):
        v = by[k]
        print(f"    class {k[0]} taken row {k[1]}: {len(v)} stops at {len({tuple(e['node']) for e in stops if (cls(e['node']), e.get('row')) == k})} Nodes, fall over walls (thousandths) min {min(v)} max {max(v)}")
