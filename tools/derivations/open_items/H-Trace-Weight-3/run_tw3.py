"""tw3's runner (tw1's form): one world run on the copy under PYTHONPATH to a count of intervals with N back, the record written
to the cache $S/records/d9d7914ff/<tag>.json, the gates' table (event_universe.gates, as tests use it) written whole to
out/<tag>.gates.json beside this script, and one summary line printed as JSON: the record's hash (the rows' milliseconds struck,
sha256, 16 hex digits), births, credits, laid, laid back, turns, the run back, integers, bits, W total, the returns (every Node's X
the seed's), the gates SHOWN by number and every gate's verdict kind. Usage: run_tw3.py <world.json> <intervals> <back> <tag>"""

import hashlib
import json
import os
import sys
import time

sys.set_int_max_str_digits(0)

from event_universe.gates import gates, kind_of  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.run import record  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/d9d7914ff"
path, intervals, back, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
t0 = time.monotonic()
universe, world = load_world(path)
world["intervals"] = intervals
found = json.loads(json.dumps(record(universe, world, back, lambda line: None)))
os.makedirs(CACHE, exist_ok=True)
json.dump(found, open(os.path.join(CACHE, tag + ".json"), "w"))
timeless = dict(found)
timeless["rows"] = [{k: v for k, v in row.items() if k != "milliseconds"} for row in found["rows"]]
digest = hashlib.sha256(json.dumps(timeless, sort_keys=True).encode()).hexdigest()
nodes = found["nodes"]
seed_x = nodes[0]["X"]
returns = [n["i"] for n in nodes[1:] if n["X"] == seed_x]
last = found["rows"][-1]
read = gates(found)
json.dump(read, open(os.path.join(HERE, "out", tag + ".gates.json"), "w"), indent=1, default=str)
numbered = {int(k.split()[0]): v for k, v in read.items() if k.split()[0].isdigit()}
shown = sorted(n for n, v in numbered.items() if kind_of(str(v.get("verdict", ""))) == "SHOWN")
summary = {
    "tag": tag,
    "trace_weight": int(os.environ.get("TW3_TRACE", "54")),
    "src": os.environ.get("PYTHONPATH", ""),
    "hash": digest[:16],
    "intervals": intervals,
    "returns": returns[:12],
    "returns count": len(returns),
    "births": found["counts"]["births"],
    "credits": found["counts"]["body_clicks"],
    "laid": found["counts"]["laid"],
    "laid back": found["counts"]["laid_back"],
    "turns": found["counts"]["turns"],
    "run back": found["run_back"],
    "integers": last["integers"],
    "max bits": last["max bits"],
    "transient bits": last["max transient bits"],
    "W total at the end": last["W total"],
    "gates SHOWN": shown,
    "SHOWN count": len(shown),
    "kinds": {n: kind_of(str(v.get("verdict", ""))) for n, v in sorted(numbered.items())},
    "seconds": int(time.monotonic() - t0),
}
print(json.dumps(summary))
