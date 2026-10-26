"""Run a world N intervals and print the state hash, L2 end and counts (the flag-off check bit for bit; the uniform boards). Usage: python run_hash.py <world.json> <intervals> [back]"""
import json, sys
import numpy as np
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.core.ports import AXES, across
EPS = {0: (1, 2), 1: (2, 0), 2: (0, 1)}
def L2(node):
    c = node.cube; idx = np.indices(node.shape); X = [idx[a].astype(object) for a in range(AXES)]
    L = [0, 0, 0]
    for r in node.records():
        num = r.pair[0]; p = []
        for b in range(AXES):
            s = 0
            for line in r.lines:
                s = s + across(line.now, 2 * b) * line.before - line.now * across(line.before, 2 * b)
            p.append(2 * num * s)
        for cc in range(AXES):
            a, b = EPS[cc]
            L[cc] += int(np.sum((2 * X[a] - (c - 1)) * p[b] - (2 * X[b] - (c - 1)) * p[a]))
    return L
sys.set_int_max_str_digits(0)
u, w = load_world(sys.argv[1]); node = Node(u, w); n = int(sys.argv[2])
h0 = node.state_hash()
for _ in range(n):
    node.step()
out = {"world": sys.argv[1], "intervals": n, "hash": node.state_hash(), "L2": L2(node), "counts": {k: int(v) for k, v in node.counts.items()}, "bits": node.census()[1]}
if len(sys.argv) > 3:
    back = int(sys.argv[3])
    for _ in range(back):
        node.step_back()
    for _ in range(back):
        node.step()
    out["run_back"] = {"back": back, "same": node.state_hash() == out["hash"]}
    for _ in range(n):
        node.step_back()
    out["run_back"]["to_start_same"] = node.state_hash() == h0
print(json.dumps(out))
