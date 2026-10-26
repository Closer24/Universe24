"""The cycle seed's course on a named src (the flag from the environment): tests/worlds/world_ga2.json run N intervals, per interval the births, credits, turns and refusals; at the named intervals X against Gamma at every Node; then `back` intervals run back by the state hash. Usage: ga2_course.py <src> <world.json> <intervals> <back> <out.json> <check intervals comma-separated>"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

u, w = load_world(sys.argv[2])
n, back = int(sys.argv[3]), int(sys.argv[4])
checks = [int(x) for x in sys.argv[6].split(",")]
w = dict(w, intervals=n)
node = Node(u, w)
course, hashes, at_checks = [], [], {}
prev = {k: int(v) for k, v in node.counts.items()}
for t in range(1, n + 1):
    node.step()
    now = {k: int(v) for k, v in node.counts.items()}
    delta = {k: now.get(k, 0) - prev.get(k, 0) for k in now if now.get(k, 0) != prev.get(k, 0)}
    prev = now
    x = node.row(CARRIER).lines[0].now
    row = {"i": t, "delta": delta, "turned": int(np.sum(node.turned)), "x_min": int(np.min(x)), "x_max": int(np.max(x))}
    if delta:
        course.append(row)
    if t in checks:
        at_checks[t] = {"X_equals_Gamma_nodes": int(np.sum(x == node.gamma)), "nodes": int(x.size), "x_min": int(np.min(x)), "x_max": int(np.max(x)), "gamma": int(node.gamma)}
    hashes.append(node.state_hash())
births = [e for e in node.log if e["event"] == "birth"]
by_i = {}
for e in births:
    by_i[e["i"]] = by_i.get(e["i"], 0) + 1
nodes_at_2 = len({tuple(e["node"]) for e in births if e["i"] == 2})
exact = 0
for k in range(back):
    node.run(-1)
    exact += node.state_hash() == hashes[len(hashes) - 2 - k] if len(hashes) - 2 - k >= 0 else 0
summary = {"world": sys.argv[2], "intervals": n, "counts": {k: int(v) for k, v in node.counts.items()}, "births_by_interval": by_i, "birth_nodes_at_2": nodes_at_2,
           "children_records_at_2": sorted({e["line_pair"] for e in births if e["i"] == 2}), "checks": at_checks, "run_back_exact": exact, "run_back_asked": back,
           "intervals_with_change": len(course)}
json.dump({"summary": summary, "course": course}, open(sys.argv[5], "w"), default=str)
print(json.dumps(summary, default=str))
