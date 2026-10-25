"""cs5: the second slimming (the first removed every 400-interval record: the log's refusal entries alone are above the bound): the run's rows, the Node rows and the log's refusal entries dropped, a count of the refusals per interval and cause kept in their place under `refused_counts`; the births, the credits, the landing census, the lay and the diag kept whole.
Usage: python shrink2.py <record.json> ..."""
import json
import os
import sys

sys.set_int_max_str_digits(0)
for p in sys.argv[1:]:
    rec = json.load(open(p))
    for k in ("rows", "nodes"):
        rec.pop(k, None)
    counts = {}
    kept = []
    for e in rec["log"]:
        if e["event"] == "refused":
            key = f"{e['i']}:{e['cause']}" + ("_crowd" if "children_at_one_node" in e else "_standing" if "standing" in e else "_control" if "control" in e else "")
            counts[key] = counts.get(key, 0) + 1
        else:
            kept.append(e)
    rec["log"] = kept
    rec["refused_counts"] = counts
    json.dump(rec, open(p, "w"))
    print(p, "slimmed to", os.path.getsize(p))
