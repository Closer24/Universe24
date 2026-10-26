"""The course of a world on the head's src: per interval the births, the credits (laid back), the turns, the Nodes at X = Gamma, the frozen Nodes (content at or above paces.frozen_content(Gamma), the horizon's content); the exact returns (X = Gamma at every Node) listed; then `back` intervals run back by the state hash; the census (arrays, bits). Usage: course.py <src> <world.json> <intervals> <back> <out.json>"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.core import paces  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

u, w = load_world(sys.argv[2])
n, back = int(sys.argv[3]), int(sys.argv[4])
w = dict(w, intervals=n)
node = Node(u, w)
frozen_at = paces.frozen_content(node.gamma)
course, hashes, returns, frozen_by_i, top_by_i = [], [], [], {}, {}
prev = {k: int(v) for k, v in node.counts.items()}
x_course = []
for t in range(1, n + 1):
    node.step()
    now = {k: int(v) for k, v in node.counts.items()}
    delta = {k: now.get(k, 0) - prev.get(k, 0) for k in now if now.get(k, 0) != prev.get(k, 0)}
    prev = now
    x = node.row(CARRIER).lines[0].now
    content = node.content()
    frozen = int(np.sum(np.vectorize(lambda c: int(c) >= frozen_at, otypes=[bool])(content)))
    at_gamma = int(np.sum(x == node.gamma))
    row = {"i": t, "delta": delta, "turned": int(np.sum(node.turned)), "x_min": int(np.min(x)), "x_max": int(np.max(x)), "at_gamma": at_gamma, "frozen": frozen}
    x_course.append([t, int(np.min(x)), int(np.max(x)), at_gamma])
    if frozen:
        frozen_by_i[t] = frozen
    if row["turned"]:
        top_by_i[t] = row["turned"]
    if at_gamma == x.size and t > 1:
        returns.append(t)
    if delta or at_gamma == x.size:
        course.append(row)
    hashes.append(node.state_hash())
births = [e for e in node.log if e["event"] == "birth"]
by_i = {}
for e in births:
    by_i[e["i"]] = by_i.get(e["i"], 0) + 1
credits = {}
for r in course:
    if "laid_back" in r["delta"]:
        credits[r["i"]] = r["delta"]["laid_back"]
exact = 0
for k in range(back):
    node.run(-1)
    exact += node.state_hash() == hashes[len(hashes) - 2 - k] if len(hashes) - 2 - k >= 0 else 0
arrays, bits = node.census()
xs = [r[1] for r in x_course]
summary = {"world": sys.argv[2], "nodes": int(x.size), "intervals": n, "counts": {k: int(v) for k, v in node.counts.items()},
           "births_by_interval": by_i, "birth_nodes": len({tuple(e["node"]) for e in births}),
           "credits_by_interval": credits, "turns_by_interval": top_by_i,
           "returns_X_equals_Gamma_every_node": returns, "gamma": int(node.gamma),
           "x_min_lowest": min(xs), "x_max_highest": max(r[2] for r in x_course), "x_at_end": [x_course[-1][1], x_course[-1][2]],
           "frozen_content": int(frozen_at), "frozen_nodes_by_interval": frozen_by_i, "frozen_nodes_max": max([0] + list(frozen_by_i.values())),
           "run_back_exact": exact, "run_back_asked": back, "arrays": arrays, "bits": bits,
           "lays": [e for e in node.log if e["event"] == "lay"]}
json.dump({"summary": summary, "course": course, "x_course": x_course}, open(sys.argv[5], "w"), default=str)
print(json.dumps({k: v for k, v in summary.items() if k != "lays"}, default=str))
