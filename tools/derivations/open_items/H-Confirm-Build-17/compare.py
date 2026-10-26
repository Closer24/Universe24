"""Compare two records key by key, the rows' milliseconds alone stripped; floats refused at the parse. Usage: python compare.py a.json b.json"""
import json, sys
def no_float(x):
    raise ValueError("float met: " + x)
def strip(d):
    if isinstance(d, dict):
        return {k: strip(v) for k, v in d.items() if k != "milliseconds"}
    if isinstance(d, list):
        return [strip(v) for v in d]
    return d
a, b = (strip(json.load(open(p), parse_float=no_float)) for p in sys.argv[1:3])
keys = sorted(set(a) | set(b)); apart = []
for k in keys:
    if a.get(k) != b.get(k):
        apart.append(k)
if not apart:
    print("EQUAL", len(keys), "keys:", " ".join(keys))
else:
    print("APART in", apart)
    for k in apart:
        if isinstance(a.get(k), list) and isinstance(b.get(k), list):
            for i, (x, y) in enumerate(zip(a[k], b[k])):
                if x != y:
                    print(f"  {k}[{i}] first apart:", str(x)[:300], "|", str(y)[:300]); break
            if len(a[k]) != len(b[k]): print(f"  {k} lengths {len(a[k])} {len(b[k])}")
        else:
            print(f"  {k}:", str(a.get(k))[:300], "|", str(b.get(k))[:300])
