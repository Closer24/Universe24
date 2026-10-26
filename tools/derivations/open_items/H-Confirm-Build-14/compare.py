"""Two records compared bit for bit in every field but the reader's milliseconds. Usage: compare.py <a.json> <b.json>"""
import json, sys
sys.set_int_max_str_digits(0)
def load(p):
    bad = []
    r = json.loads(open(p, encoding="utf-8").read(), parse_float=lambda s: bad.append(s))
    return r, len(bad)
a, fa = load(sys.argv[1]); b, fb = load(sys.argv[2])
strip = lambda rows: [{k: v for k, v in row.items() if k != "milliseconds"} for row in rows]
keys = sorted(set(a) | set(b))
apart = []
for k in keys:
    x, y = a.get(k), b.get(k)
    if k == "rows": x, y = strip(x), strip(y)
    if x != y:
        apart.append(k)
print("keys", keys, "floats", fa, fb, "run_back", a.get("run_back"), b.get("run_back"), "counts", a["counts"])
print("APART" if apart else "EQUAL", apart)
for k in apart:
    x, y = a[k], b[k]
    if isinstance(x, list) and isinstance(y, list):
        for i, (p, q) in enumerate(zip(x, y)):
            if p != q:
                fields = sorted(f for f in set(p) | set(q) if p.get(f) != q.get(f)) if isinstance(p, dict) else "-"
                print(" ", k, "first apart at index", i, "interval", p.get("i") if isinstance(p, dict) else "-", "fields", fields); break
        else:
            print(" ", k, "lengths", len(x), len(y))
    else:
        print(" ", k, "differs")
