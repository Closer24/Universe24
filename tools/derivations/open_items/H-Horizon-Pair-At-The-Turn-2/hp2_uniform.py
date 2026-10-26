"""hp2: run a cached record's world on a named src (the flags from the environment) and compare with the cache bit for bit (log, nodes, counts, run back). Usage: hp2_uniform.py <src> <cached.json> <back> <out.json>"""
import json
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import read_world  # noqa: E402
from event_universe.run import record  # noqa: E402

cached = json.load(open(sys.argv[2]))
u, w = read_world(cached["world"], cached["universe"])
found = record(u, w, int(sys.argv[3]), lambda line: None)
json.dump(found, open(sys.argv[4], "w"), default=str)
same = {k: json.dumps(found.get(k), default=str) == json.dumps(cached.get(k), default=str) for k in sorted(set(found) | set(cached)) if k not in ("world", "universe")}
summary = {"cached": sys.argv[2].split("/")[-1], "counts": {k: str(v) for k, v in found.get("counts", {}).items()}, "run back": found.get("run back"), "keys_equal": same, "all_equal": all(same.values())}
if not all(same.values()):
    lb, lc = found.get("log", []), cached.get("log", [])
    first = next((k for k, (a, b) in enumerate(zip(lb, lc)) if a != b), None)
    summary["first_apart_log_entry"] = None if first is None else {"index": first, "found": lb[first], "cached": lc[first]}
    summary["log_lengths"] = [len(lb), len(lc)]
print(json.dumps(summary, default=str)[:3000])
