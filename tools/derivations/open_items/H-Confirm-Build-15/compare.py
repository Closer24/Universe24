"""Two records compared in every key, the rows' milliseconds alone stripped; the first apart interval and field named."""
import json, sys
def strip(d):
    d = dict(d)
    d["rows"] = [{k: v for k, v in r.items() if k != "milliseconds"} for r in d["rows"]]
    return d
def load(p):
    text = open(p, encoding="utf-8").read()
    assert "." not in json.dumps(json.loads(text, parse_float=lambda s: (_ for _ in ()).throw(ValueError("float " + s)))) or True
    return strip(json.loads(text, parse_float=lambda s: (_ for _ in ()).throw(ValueError("float " + s))))
a, b = load(sys.argv[1]), load(sys.argv[2])
keys = sorted(set(a) | set(b))
apart = []
for k in keys:
    if a.get(k) != b.get(k):
        apart.append(k)
if not apart:
    print(f"EQUAL in every key ({len(keys)} keys: {', '.join(keys)}); rows {len(a['rows'])}, nodes {len(a['nodes'])}, log {len(a['log'])}, counts {a['counts']}, run_back {a['run_back']}, turns {len(a['turns'])}")
    sys.exit(0)
print("APART in keys:", apart)
for k in apart:
    x, y = a.get(k), b.get(k)
    if isinstance(x, list) and isinstance(y, list):
        for i, (p, q) in enumerate(zip(x, y)):
            if p != q:
                if isinstance(p, dict):
                    f = [kk for kk in set(p) | set(q) if p.get(kk) != q.get(kk)]
                    print(f"  {k}[{i}] (i={p.get('i')}) first apart field(s): {f}: {[(p.get(kk), q.get(kk)) for kk in f][:3]}")
                else:
                    print(f"  {k}[{i}] apart: {str(p)[:200]} | {str(q)[:200]}")
                break
        else:
            print(f"  {k}: lengths {len(x)} vs {len(y)}")
    else:
        print(f"  {k}: {str(x)[:300]} | {str(y)[:300]}")
sys.exit(1)
