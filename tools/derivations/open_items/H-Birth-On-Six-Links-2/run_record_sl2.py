"""One world run N intervals with a run back on a named src (SL2_FORM from the environment); the record written under /dev/shm/tmp/sl2/out; compared with a cached record where named (the log's first apart entry). Usage: run_record_sl2.py <src> <world.json> <intervals> <back> <out.json> [cached.json]"""
import json
import sys
import time

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.run import record  # noqa: E402

t0 = time.time()
u, w = load_world(sys.argv[2])
w = dict(w, intervals=int(sys.argv[3]))
found = record(u, w, int(sys.argv[4]), lambda line: None)
with open(sys.argv[5], "w", encoding="utf-8") as out:
    json.dump(found, out, default=str)
summary = {"world": sys.argv[2], "intervals": sys.argv[3], "counts": {k: str(v) for k, v in found.get("counts", {}).items()}, "run_back": found.get("run_back"), "seconds": int(time.time() - t0)}
if len(sys.argv) > 6:
    cached = json.load(open(sys.argv[6]))
    same = {k: json.dumps(found.get(k), default=str, sort_keys=True) == json.dumps(cached.get(k), default=str, sort_keys=True) for k in sorted(set(found) | set(cached))}
    summary["against_cached"] = {"keys_equal": same, "all_equal": all(same.values())}
    if not all(same.values()):
        lb, lc = found.get("log", []), cached.get("log", [])
        first = next((k for k, (a, b) in enumerate(zip(lb, lc)) if json.dumps(a, default=str, sort_keys=True) != json.dumps(b, default=str, sort_keys=True)), None)
        summary["first_apart_log_entry"] = None if first is None else {"index": first, "found": lb[first], "cached": lc[first]}
        summary["log_lengths"] = [len(lb), len(lc)]
print(json.dumps(summary, default=str))
