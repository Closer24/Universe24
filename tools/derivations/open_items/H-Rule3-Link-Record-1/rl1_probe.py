"""rl1: the chiral under FR-S1's two lines run N intervals on a named src (RL1_FORM and FR2_RELEASE from the environment); per interval the frozen count (the Link pace 0 at the start), and every `every` intervals the content sum of the board, the X spread among the Nodes ever frozen (least, largest, distinct) and the board's distinct X count; the frozen histogram at the end. Integers only. Usage: rl1_probe.py <src> <world.json> <intervals> <every> <out.json>"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe import readings  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

u, w = load_world(sys.argv[2])
n, every = int(sys.argv[3]), int(sys.argv[4])
node = Node(u, dict(w, intervals=n))
ever = np.zeros(node.shape, dtype=bool)
hist: dict[int, int] = {}
rows = []
first_freeze = None
for i in range(n):
    c = node.content()
    frozen = readings.frozen_of(node, c)
    k = int(frozen.sum())
    hist[k] = hist.get(k, 0) + 1
    if k and first_freeze is None:
        first_freeze = i
    ever |= frozen
    if (i + 1) % every == 0 or i == n - 1:
        X = np.asarray(node.row(CARRIER).lines[0].now, dtype=object).ravel()
        xs = [int(x) for x in X]
        hov = [int(x) for x, e in zip(xs, ever.ravel()) if e]
        row = {"i": i + 1, "frozen": k, "ever_frozen": int(ever.sum()), "content_sum": str(sum(int(x) for x in np.asarray(c, dtype=object).ravel())),
               "X_distinct": len(set(xs)), "hover_X_least": str(min(hov)) if hov else None, "hover_X_largest": str(max(hov)) if hov else None,
               "hover_X_distinct": len(set(hov)), "births": str(node.counts["births"]), "credits": str(node.counts["body_clicks"]), "bits": int(node.max_transient)}
        rows.append(row)
        print(json.dumps(row), flush=True)
    node.step()
out = {"src": sys.argv[1], "form": __import__("os").environ.get("RL1_FORM", ""), "intervals": n, "first_freeze": first_freeze, "frozen_histogram": {str(k): v for k, v in sorted(hist.items())}, "rows": rows}
json.dump(out, open(sys.argv[5], "w"))
print(json.dumps({"first_freeze": first_freeze, "frozen_histogram": out["frozen_histogram"]}))
