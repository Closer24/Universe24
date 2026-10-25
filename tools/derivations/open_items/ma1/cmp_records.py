"""Two engine records compared with the timing dropped (the rows' milliseconds): equal or the first differing key."""
import json, sys
sys.set_int_max_str_digits(0)
a, b = (json.load(open(f)) for f in sys.argv[1:3])
for r in a["rows"] + b["rows"]:
    r.pop("milliseconds", None)
a["world"], b["world"] = None, None
print("EQUAL (timing dropped)" if a == b else "DIFFER: " + ", ".join(k for k in a if a[k] != b.get(k)))
