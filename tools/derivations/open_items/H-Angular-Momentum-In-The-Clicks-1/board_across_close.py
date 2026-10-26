"""The board's L2 (am2's reading of MV-S1's density about the centre, doubled coordinates) before and after every close on the head's interval (interval.run's five acts), so the clicks' J can be set against it. Usage: python board_across_close.py <world.json> <out.json>"""
import json, sys, time
import numpy as np
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.interval import Interval
from event_universe.core.ports import AXES, across

EPS = {0: (1, 2), 1: (2, 0), 2: (0, 1)}

def L2P(recs, X, c):
    L = [0, 0, 0]; P = [0, 0, 0]
    for r in recs:
        num = r.pair[0]; p = []
        for b in range(AXES):
            s = 0
            for line in r.lines:
                s = s + across(line.now, 2 * b) * line.before - line.now * across(line.before, 2 * b)
            p.append(2 * num * s)
        for b in range(AXES):
            P[b] += int(np.sum(p[b]))
        for cc in range(AXES):
            a, b = EPS[cc]
            L[cc] += int(np.sum((2 * X[a] - (c - 1)) * p[b] - (2 * X[b] - (c - 1)) * p[a]))
    return L, P

def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1]); node = Node(universe, world); c = node.cube
    idx = np.indices(node.shape); X = [idx[a].astype(object) for a in range(AXES)]
    recs = node.records(); per = []; t0 = time.monotonic_ns()
    for t in range(int(world["intervals"])):
        L0, P0 = L2P(recs, X, c)
        iv = Interval(node, 1); iv.readings(); iv.kick(); iv.division(); iv.swap()
        L3, P3 = L2P(node.records(), X, c)
        n0 = len(node.log); iv.close()
        L4, P4 = L2P(node.records(), X, c)
        per.append({"i": node.interval, "L2_start": L0, "dL2_before_close": [x - y for x, y in zip(L3, L0)],
                    "dL2_click": [x - y for x, y in zip(L4, L3)], "dP_click": [x - y for x, y in zip(P4, P3)], "L2_end": L4, "P_end": P4,
                    "log lines": len(node.log) - n0})
    out = {"world": argv[1], "cube": c, "log": node.log, "per_interval": per, "counts": {k: int(v) for k, v in node.counts.items()}, "ms": (time.monotonic_ns() - t0) // 10**6}
    json.dump(out, open(argv[2], "w"))
    print(json.dumps({"done": argv[1], "ms": out["ms"], "L2_end": per[-1]["L2_end"], "counts": out["counts"]}))

if __name__ == "__main__":
    main(sys.argv)
