"""The cycle seed's return read from a record: the Nodes whose X stands at the seed's (the X of the record's first Node line, the same at every Node) at the intervals named, and every interval at which X is the seed's at every Node, the births per interval, the count. Usage: ga2_return.py <record.json> <i1,i2,...>"""
import json
import sys

sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
nodes0 = rec["nodes"][0]
seed = int(nodes0["X"][0])
marks = [int(x) for x in sys.argv[2].split(",")]
nodes = rec["nodes"]
found = {}
for m in marks:
    line = next((n for n in nodes if int(n["i"]) == m), None)
    if line is None:
        found[m] = None
        continue
    xs = [int(x) for x in line["X"]]
    found[m] = {"nodes at the seed's X": sum(1 for x in xs if x == seed), "of": len(xs), "X min max": [min(xs), max(xs)]}
births = [e for e in rec["log"] if e["event"] == "birth"]
by_i = {}
for b in births:
    by_i[b["i"]] = by_i.get(b["i"], 0) + 1
uniform = [int(n["i"]) for n in nodes if len(set(int(x) for x in n["X"])) == 1]
returns = [int(n["i"]) for n in nodes if all(int(x) == seed for x in n["X"])]
print(json.dumps({"record": sys.argv[1], "seed X": seed, "intervals with X the seed's at every Node": returns, "intervals with X uniform at any value": uniform, "returns": found, "births": len(births), "births by interval": by_i, "counts": rec.get("counts"), "run_back": rec.get("run_back")}))
