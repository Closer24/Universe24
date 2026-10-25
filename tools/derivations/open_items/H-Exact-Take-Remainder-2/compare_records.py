"""Two records compared bit for bit but for the clocks: python compare_records.py a.json b.json -> EQUAL / DIFFER (the keys that differ)."""
import json, sys

def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k != "milliseconds"}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x

a, b = (strip(json.load(open(p, encoding="utf-8"))) for p in sys.argv[1:3])
if a == b:
    print("EQUAL")
else:
    print("DIFFER:", [k for k in a if a.get(k) != b.get(k)])
