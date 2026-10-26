"""lr1: the cycle seed ga2 (tests/worlds/world_ga2.json) run to N on a named src with the flags from the environment: the births by interval, the refusals at 2 by name, the returns (the intervals at which the mean X over the board is Gamma again), the run back 10. Usage: run_ga2_lr1.py <src> <worktree> <N> <out.json>"""
import collections
import json
import os
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.run import record  # noqa: E402

os.nice(19)
root, n = sys.argv[2], int(sys.argv[3])
u, w = load_world(root + "/tests/worlds/world_ga2.json")
found = record(u, dict(w, intervals=n), 10, lambda line: None)
births = collections.Counter(e["i"] for e in found["log"] if e["event"] == "birth")
at2 = {tuple(e["node"]) for e in found["log"] if e["event"] == "birth" and e["i"] == 2}
refused2 = collections.Counter(e["cause"] for e in found["log"] if e["event"] == "refused" and e["i"] == 2)
gamma = found["gamma"]
returns = [e["i"] for e in found["nodes"] if sum(e["X"]) // len(e["X"]) == gamma]
summary = {"N": n, "flags": {k: os.environ.get(k) for k in ("LR1_PICK", "LR1_LAY")}, "births by interval": sorted(births.items()), "nodes birthing at 2": len(at2), "refused at 2": dict(refused2), "returns (mean X = Gamma)": returns, "counts": found["counts"], "run_back": found["run_back"], "max_bits": max(found.get("bits", [0])) if "bits" in found else None}
print(json.dumps(summary, default=str))
json.dump(summary, open(sys.argv[4], "w"), default=str)
