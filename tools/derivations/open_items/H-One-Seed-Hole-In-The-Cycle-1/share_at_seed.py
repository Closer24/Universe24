"""The light's share at every Node at the seed (interval 0) for each candidate world, by the pattern's phase class and by hole / no hole, and X over the first intervals: whether the board parts at the lay. Integers only. Usage: share_at_seed.py <src> <intervals> <world.json>..."""
import json
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402
from event_universe.wave import cycle_phases  # noqa: E402

P1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2, 1]
steps = int(sys.argv[2])
for path in sys.argv[3:]:
    u, w = load_world(path)
    node = Node(u, w)
    holes = {tuple(l["at"]) for l in w["seed"] if l["lay"] == "hole"}
    row = node.emitter()
    rec = node.records().index(row)
    rule = node.rule(row.pair, node.content(), node.link_factors())
    share = node.share(row.lines, rule)
    p = cycle_phases(node, P1)
    by = {}
    for at in np.ndindex(*node.shape):
        key = (int(p[at]), at in holes)
        by.setdefault(key, set()).add(int(share[at]))
    unit = node.units[rec]
    print(path.split("/")[-1], "| holes", len(holes), "| drift", node.drift, "| unit", unit)
    print("  share at i 0 by (class, hole): " + "; ".join(f"{k}: {sorted(v)} = {[s * 100 // unit for s in sorted(v)]} hundredths" for k, v in sorted(by.items())))
    print("  distinct shares over the board:", len({int(s) for s in share.reshape(-1)}))
    course = []
    for t in range(1, steps + 1):
        node.step()
        x = node.row(CARRIER).lines[0].now
        course.append((t, int(x.min()), int(x.max()), len({int(v) for v in x.reshape(-1)}), int(node.turned.sum())))
    print("  X (i, min, max, distinct, turned):", course)
    births = sum(1 for e in node.log if e["event"] == "birth")
    print("  births to", steps, ":", births, "| counts:", {k: int(v) for k, v in node.counts.items() if int(v)})
