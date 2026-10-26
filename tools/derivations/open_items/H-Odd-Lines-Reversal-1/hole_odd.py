"""ol1: the hole 60's odd lines read on the head's path: at every interval the largest |level| of the three odd lines over the board, the count of Nodes with a nonzero odd line, and at the turned Nodes the odd lines' levels (the first 12 intervals printed). Usage: PYTHONPATH=<src> hole_odd.py <world>"""
import json, sys
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import POTENTIAL
universe, world = load_world(sys.argv[1])
node = Node(universe, world)
row = node.row(POTENTIAL)
for t in range(12):
    node.step()
    odd = [np.asarray(line.now, dtype=object) for line in row.lines[1:]]
    big = max(int(abs(int(v))) for a in odd for v in a.reshape(-1))
    nonzero = int(sum(1 for at in np.ndindex(*node.shape) if any(int(a[at]) != 0 for a in odd)))
    turned = [tuple(int(v) for v in at) for at in np.argwhere(node.turned)]
    at_turned = [[int(a[at]) for a in odd] for at in turned[:6]]
    print(json.dumps({"i": node.interval, "odd max abs": big, "nodes with an odd line nonzero": nonzero, "turned": len(turned), "odd lines at the first turned Nodes": at_turned, "time line max abs": max(int(abs(int(v))) for v in row.lines[0].now.reshape(-1))}))
