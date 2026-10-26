"""Compare a found record with a cached (or head) record on the content keys after one JSON round trip (the cache holds the integers as strings): log, nodes, counts, run_back, turns, gapped; the rows without the milliseconds. Usage: compare.py found.json other.json"""
import json, sys
sys.set_int_max_str_digits(0)
def rt(x): return json.loads(json.dumps(x, default=str))
a, b = (json.load(open(p)) for p in sys.argv[1:3])
out = {}
for k in ("log", "nodes", "counts", "run_back", "turns", "gapped", "planes", "T", "G", "gamma"):
    out[k] = rt(a.get(k)) == rt(b.get(k))
ra = [{k: v for k, v in r.items() if k != "milliseconds"} for r in a["rows"]]
rb = [{k: v for k, v in r.items() if k != "milliseconds"} for r in b["rows"]]
out["rows_without_milliseconds"] = rt(ra) == rt(rb)
out["log_len"] = [len(a["log"]), len(b["log"])]
out["max_bits"] = max(int(r["max bits"]) for r in a["rows"])
out["all"] = all(v for k, v in out.items() if k not in ("log_len", "max_bits"))
print(sys.argv[1].split("/")[-1], json.dumps(out))
