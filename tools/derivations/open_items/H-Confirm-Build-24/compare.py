"""Two records compared on every top-level key but the rows' milliseconds and the universe's integers (the key trace allowed); floats refused at the parse; the first apart interval and field named."""
import json, sys
def parse(p):
    def no_float(s):
        raise ValueError("float in the record: " + s)
    return json.load(open(p), parse_float=no_float)
a, b = parse(sys.argv[1]), parse(sys.argv[2])
def strip(d):
    d = dict(d)
    rows = d.get("rows")
    if isinstance(rows, list):
        d["rows"] = [{k: v for k, v in r.items() if "ms" not in k and "millis" not in k} if isinstance(r, dict) else r for r in rows]
    u = d.get("universe")
    if isinstance(u, dict):
        u = dict(u); u["integers"] = {k: v for k, v in u.get("integers", {}).items() if k != "trace"}; d["universe"] = u
    return d
a, b = strip(a), strip(b)
keys = sorted(set(a) | set(b))
apart = []
for k in keys:
    if a.get(k) != b.get(k):
        where = ""
        va, vb = a.get(k), b.get(k)
        if isinstance(va, list) and isinstance(vb, list):
            for i, (x, y) in enumerate(zip(va, vb)):
                if x != y:
                    f = ""
                    if isinstance(x, dict) and isinstance(y, dict):
                        f = ",".join(sorted(kk for kk in set(x) | set(y) if x.get(kk) != y.get(kk)))
                        where = f" first apart at index {i} (interval {x.get('i', '?')}) fields {f}"
                    else:
                        where = f" first apart at index {i}"
                    break
            else:
                where = f" lengths {len(va)} and {len(vb)}"
        apart.append(k + where)
print(("EQUAL" if not apart else "APART " + "; ".join(apart)) + f", {len(keys)} keys: " + " ".join(keys))
