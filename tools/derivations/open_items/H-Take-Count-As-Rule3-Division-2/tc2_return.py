"""The cycle seed's return read on the board: a world run n intervals on a named src (the flag from the environment); per interval the
count of Nodes whose carrier level X equals Gamma, the least and the largest X, the births so far; one JSON line per interval (every interval written). Usage: tc2_return.py <src> <world.json> <n> <out.txt> <i1,i2,...>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER

src, world_path, n, out, named = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], [int(x) for x in sys.argv[5].split(",")]
u, w = load_world(world_path)
node = Node(u, dict(w, intervals=n))
gamma = int(node.gamma)
rows, last = [], None
for i in range(1, n + 1):
    node.step()
    x = [int(v) for v in np.asarray(node.row(CARRIER).lines[0].now, dtype=object).reshape(-1)]
    at_gamma = sum(1 for v in x if v == gamma)
    if True:
        rows.append(dict(i=i, nodes_at_gamma=at_gamma, of=len(x), x_min=min(x), x_max=max(x), births=int(node.counts["births"])))
        last = at_gamma
open(out, "w").write("\n".join(json.dumps(r) for r in rows) + "\n")
print(json.dumps(dict(flag=os.environ.get("TC2_CHORD_COUNT", ""), world=os.path.basename(world_path), at_named=[r for r in rows if r["i"] in named], changes=len(rows))))
