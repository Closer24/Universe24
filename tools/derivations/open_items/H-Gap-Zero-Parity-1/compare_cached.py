"""Compare a record written by run_record.py (json, default=str) with the cached record, both read back from json so that the types agree. Usage: compare_cached.py <out.json> <cached.json>"""
import json
import sys

a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
for d in (a, b):  # the readings' milliseconds are the run's clock, not the record's
    for row in d.get("rows", []):
        if isinstance(row, dict):
            row.pop("milliseconds", None)
same = {k: a.get(k) == b.get(k) for k in sorted(set(a) | set(b))}
off = [k for k, v in same.items() if not v]
out = {"all_equal": not off, "keys_apart": off, "counts": a.get("counts"), "run back": a.get("run back")}
if "log" in off:
    la, lb = a["log"], b["log"]
    first = next((k for k, (x, y) in enumerate(zip(la, lb)) if x != y), None)
    out["log_lengths"] = [len(la), len(lb)]
    out["first_apart_log_entry"] = None if first is None else {"index": first, "found": la[first], "cached": lb[first]}
print(json.dumps(out, default=str)[:3000])
