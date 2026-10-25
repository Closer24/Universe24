"""lc1: chosen columns of a course file at chosen intervals. Usage: cols.py <course.json> <step> [first N intervals]"""
import json, sys
rows = json.load(open(sys.argv[1])); step = int(sys.argv[2]); first = int(sys.argv[3]) if len(sys.argv) > 3 else 0
keys = ["i", "X sum", "X min", "X max", "X'' sum", "mass pull sum", "carrier links quot", "write sum", "forms gap0", "forms gapped", "turns at i", "turned", "births", "body_clicks", "e", "e max"]
print(" | ".join(keys))
for r in rows:
    if r["i"] % step == 0 or r["i"] <= first:
        print(" | ".join(str(r[k]) for k in keys))
