"""Compare two records bit for bit with the clock reading `milliseconds` struck: the log, the Node lines, the counts, the turns, the rows. Usage: compare.py <a.json> <b.json>"""
import json
import sys

sys.set_int_max_str_digits(0)


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k != "milliseconds"}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


a, b = (strip(json.load(open(p))) for p in sys.argv[1:3])
out = {}
for k in sorted(set(a) | set(b)):
    out[k] = a.get(k) == b.get(k)
print(json.dumps({"all_equal": all(out.values()), "keys": out, "log_lengths": [len(a.get("log", [])), len(b.get("log", []))], "run_back": [a.get("run_back"), b.get("run_back")], "counts_equal": a.get("counts") == b.get("counts"), "turns_equal": a.get("turns") == b.get("turns"), "nodes_equal": a.get("nodes") == b.get("nodes")}))
