"""lc1: two records compared bit for bit but for the clock's milliseconds: the counts, the turns, the rows, the Node lines, the log, the run back. Usage: compare_records.py a.json b.json"""
import json
import sys


def strip(rec):
    rec = dict(rec)
    rec["rows"] = [{k: v for k, v in r.items() if k != "milliseconds"} for r in rec["rows"]]
    return rec


a, b = (strip(json.load(open(p))) for p in sys.argv[1:3])
keys = ["counts", "turns", "rows", "nodes", "log", "run_back"]
same = {k: a[k] == b[k] for k in keys}
print(json.dumps({"equal": all(same.values()), "by key": same}))
