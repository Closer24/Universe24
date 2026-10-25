"""bb2: the lay below the drift (the fourth form the file would need), laid by the loader's own act (node.lay, the same act the `at` form uses) with L levels of velocity at the centre on the gap-0 row over the bare sea; the course decomposed as bb2_course.py (its wrappers imported), the exact return read, the run back 10 at the end. Nothing of src changes; the lay is the script's and not the file's: a flagged reading.

Usage: sub_drift.py <world.json> <L> <out.json> [back]
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bb2_course  # noqa: E402  (installs the wrappers)
from bb2_course import LOG, tot  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE  # noqa: E402


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    L = int(argv[2])
    back = int(argv[4]) if len(argv) > 4 else 10
    node = Node(universe, world)
    centre = tuple(c // 2 for c in node.shape)
    rec = node.records().index(node.row(PLANE, gap=0))
    node.lay(rec, centre, (L, 0, 0, 0))
    n = 1
    for x in node.shape:
        n *= x
    seed_x = [int(v) for v in np.asarray(node.row(CARRIER).lines[0].now, dtype=object).reshape(-1)]
    intervals = int(world["intervals"])
    rows, hashes = [], []
    prev_turns = 0
    for t in range(intervals):
        if t >= intervals - back:
            hashes.append(node.state_hash())
        x_line = node.row(CARRIER).lines[0]
        x_before, x_now = x_line.before.copy(), x_line.now.copy()
        node.step()
        x_next = node.row(CARRIER).lines[0].now
        xs = [int(v) for v in np.asarray(x_next, dtype=object).reshape(-1)]
        rows.append({
            "i": node.interval, "X mean": sum(xs) // n, "X min": min(xs), "X max": max(xs),
            "at seed": sum(1 for a, b in zip(xs, seed_x) if a == b),
            "X'' sum": tot(x_next - 2 * x_now + x_before),
            "mass pull sum": LOG["mass"], "links sum": LOG.get("links", 0), "write sum": LOG["write"],
            "e max": LOG.get("e_max", 0), "links above": LOG.get("links_above", 0), "e sq sum": LOG.get("e_sq_sum", 0),
            "forms gap0": LOG["forms"].get("gap0", 0), "forms gapped": LOG["forms"].get("gapped", 0),
            "turns at i": node.counts["turns"] - prev_turns, "births": node.counts["births"],
            "refused_lay": node.counts["refused_lay"], "body_clicks": node.counts["body_clicks"],
            "max bits": node.census()[1],
        })
        prev_turns = node.counts["turns"]
    exact = 0
    for k in range(len(hashes)):
        node.step_back()
        exact += node.state_hash() == hashes[len(hashes) - 1 - k]
    out = {"L": L, "world": world["seed"], "nodes": n, "rows": rows,
           "run back": {"intervals": len(hashes), "exact": exact},
           "counts": {k: str(v) for k, v in node.counts.items()}, "census": list(node.census()),
           "max transient bits": node.max_transient}
    json.dump(out, open(argv[3], "w"))
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))


if __name__ == "__main__":
    main(sys.argv)
