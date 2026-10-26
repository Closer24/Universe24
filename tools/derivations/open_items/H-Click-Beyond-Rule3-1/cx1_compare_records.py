"""Two records compared bit for bit with the rows' milliseconds struck: prints EQUAL or APART with the first key apart."""
import json
import sys

sys.set_int_max_str_digits(0)


def struck(rec):
    for row in rec.get("rows", []):
        row.pop("milliseconds", None)
    return rec


a, b = (struck(json.load(open(p, encoding="utf-8"))) for p in sys.argv[1:3])
apart = [k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
print(json.dumps({"a": sys.argv[1], "b": sys.argv[2], "verdict": "EQUAL" if not apart else "APART", "keys_apart": apart}))
