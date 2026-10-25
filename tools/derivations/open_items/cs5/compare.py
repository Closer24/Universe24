"""cs5: two records compared line by line: every diag line (X, counts, e, turned, bits), the counts and the rows; prints the first differing interval or EQUAL.
Usage: python compare.py <a.json> <b.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
first = None
for da, db in zip(a["diag"], b["diag"]):
    if da != db:
        first = da["i"]
        break
same = a["counts"] == b["counts"] and len(a["diag"]) == len(b["diag"]) and first is None and a["rows"] == b["rows"]
print("counts equal", a["counts"] == b["counts"], "diag lines", len(a["diag"]), len(b["diag"]), "first differing interval", first, "rows equal", a["rows"] == b["rows"], "EQUAL" if same else "DIFFER")
