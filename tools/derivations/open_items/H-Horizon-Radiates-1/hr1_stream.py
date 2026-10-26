"""hr1 (H-Horizon-Radiates-1): one world run N intervals on a named src (the flag FR2_RELEASE from the environment), the record streamed one JSON line per interval as it comes: the interval, the frozen Nodes, the turned Nodes, every Node's content and X, and the clicks (births, credits) of that interval without their frame; then the run back of `back` intervals compared by the state's hash and the counts as a last line. Integers only. Usage: hr1_stream.py <src> <world.json> <intervals> <back> <out.jsonl>"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.core import paces  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

world_path, n, back = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
universe, world = load_world(world_path)
world = dict(world, intervals=n)
node = Node(universe, world)
out = open(sys.argv[5], "w", encoding="utf-8")
out.write(json.dumps({"head": True, "src": sys.argv[1], "world": world_path, "intervals": n, "shape": [int(s) for s in node.shape], "gamma": int(node.gamma), "frozen content": int(paces.frozen_content(node.gamma))}) + "\n")
hashes = []
seen = 0
for k in range(n):
    if k >= n - back:
        hashes.append(node.state_bytes())
    node.step()
    carrier = node.row(CARRIER).lines[0]
    c = node.content()
    pace = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object).reshape(-1)
    clicks = [{kk: v for kk, v in e.items() if kk != "frame"} for e in node.log[seen:] if e.get("event") in ("birth", "credit")]
    seen = len(node.log)
    line = {
        "i": int(node.interval),
        "frozen": [i for i, p in enumerate(pace.tolist()) if int(p) == 0],
        "turned": [i for i, t in enumerate(node.turned.reshape(-1).tolist()) if t],
        "content": [int(x) for x in c.reshape(-1).tolist()],
        "X": [int(x) for x in np.asarray(carrier.now, dtype=object).reshape(-1).tolist()],
        "Xb": [int(x) for x in np.asarray(carrier.before, dtype=object).reshape(-1).tolist()],
        "clicks": clicks,
        "max transient": int(node.max_transient),
        "state bits": int(node.census()[1]),
    }
    out.write(json.dumps(line, default=str) + "\n")
    out.flush()
ok = 0
for k in range(back):
    node.step_back()
    ok += node.state_bytes() == hashes[back - 1 - k]
out.write(json.dumps({"tail": True, "run back": [ok, back], "counts": {k: str(v) for k, v in node.counts.items()}, "max transient": int(node.max_transient)}) + "\n")
out.close()
print(json.dumps({"run back": [ok, back], "counts": {k: str(v) for k, v in node.counts.items()}}))
