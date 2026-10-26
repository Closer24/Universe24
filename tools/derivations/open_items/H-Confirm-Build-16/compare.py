"""Compare two records key by key, the rows' milliseconds stripped; floats refused."""
import json, sys
def no_float(pairs):
    d = dict(pairs)
    return d
def load(p):
    return json.load(open(p), parse_float=lambda s: (_ for _ in ()).throw(ValueError("float " + s)))
def strip(d):
    for r in d.get("rows", []):
        for k in [k for k in r if "ms" in k.lower() or "milli" in k.lower() or "second" in k.lower()]:
            r.pop(k)
    return d
def first_apart(a, b, path=""):
    if type(a) != type(b): return path, "type"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: return path + "/" + k, "missing"
            r = first_apart(a[k], b[k], path + "/" + k)
            if r: return r
        return None
    if isinstance(a, list):
        if len(a) != len(b): return path, f"len {len(a)} {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            r = first_apart(x, y, path + f"[{i}]")
            if r: return r
        return None
    return None if a == b else (path, f"{str(a)[:40]} != {str(b)[:40]}")
a, b = strip(load(sys.argv[1])), strip(load(sys.argv[2]))
keys = sorted(set(a) | set(b))
apart = [k for k in keys if first_apart(a.get(k), b.get(k), k)]
c = a["counts"]
print(f"{sys.argv[3]}: keys {len(keys)}, equal {len(keys) - len(apart)}, apart {apart}; first apart {first_apart(a, b)}; counts births {c['births']} body_clicks {c['body_clicks']} turns {c['turns']} laid_back {c['laid_back']}; log {len(a['log'])}; run_back {a['run_back']}")
