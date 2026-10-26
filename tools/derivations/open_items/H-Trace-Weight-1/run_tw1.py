"""tw1's runner: one world of the law's records run on the copy under PYTHONPATH (src_tw1 or the head's src), to a count of
intervals with N intervals back, the record kept under /dev/shm/tmp/tw1/ and one summary line printed as JSON: the record's
hash (the record with the rows' milliseconds struck, sha256), the seed's X, the returns (the intervals where every Node's X is
the seed's), the tops (every Node turned at once) with the X there, the bottom (the least X over the run and its interval),
the births, the credits (body_clicks), the laid, the turns, the run back, the integers and the bits, the charge (W total)
at the end, and the gates SHOWN by number. Usage: run_tw1.py <world.json> <intervals> <back> <tag>"""

import hashlib
import json
import os
import sys

sys.set_int_max_str_digits(0)

from event_universe.gates import gates  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.run import record  # noqa: E402

path, intervals, back, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
universe, world = load_world(path)
world["intervals"] = intervals
found = json.loads(json.dumps(record(universe, world, back, lambda line: None)))
out_dir = os.path.join(os.environ.get("TMPDIR", "/dev/shm/tmp"), "tw1")
os.makedirs(out_dir, exist_ok=True)
json.dump(found, open(os.path.join(out_dir, tag + ".json"), "w"))
timeless = dict(found)
timeless["rows"] = [{k: v for k, v in row.items() if k != "milliseconds"} for row in found["rows"]]
digest = hashlib.sha256(json.dumps(timeless, sort_keys=True).encode()).hexdigest()
nodes = found["nodes"]
count = len(nodes[0]["X"])
seed_x = nodes[0]["X"]
returns = [n["i"] for n in nodes[1:] if n["X"] == seed_x]
tops = [(n["i"], min(n["X"]), max(n["X"])) for n in nodes if len(n["turned"]) == count]
bottom = min((min(n["X"]), n["i"]) for n in nodes)
last = found["rows"][-1]
read = gates(found)
shown = sorted(int(k.split()[0]) for k, v in read.items() if k.split()[0].isdigit() and str(v.get("verdict", "")).startswith("SHOWN"))
summary = {
    "tag": tag,
    "trace_weight": int(os.environ.get("TW1_TRACE", "54")),
    "hash": digest[:16],
    "seed X": sorted(set(seed_x)),
    "returns": returns[:12],
    "returns count": len(returns),
    "tops": tops[:6],
    "tops count": len(tops),
    "bottom X, interval": bottom,
    "births": found["counts"]["births"],
    "credits": found["counts"]["body_clicks"],
    "laid": found["counts"]["laid"],
    "turns": found["counts"]["turns"],
    "run back": found["run_back"],
    "integers": last["integers"],
    "max bits": last["max bits"],
    "transient bits": last["max transient bits"],
    "W total at the end": last["W total"],
    "gates SHOWN": shown,
}
print(json.dumps(summary))
