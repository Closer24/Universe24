"""gp2: the base and the mirror state (the table mKAW, image 4) stepped to the named interval on the 5-cube; the log's events at that interval printed side by side, the mirror's carried back through the image. Usage: dump_12.py <src> <world.json> <interval>"""
import itertools
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

universe, world = load_world(sys.argv[2])
n = int(sys.argv[3])
cube = int(world["shape"][0])
m = np.diag([-1, 1, 1])
d = -1
sg3 = [-1, 1, 1]


def image(x):
    return tuple(int(v) % cube for v in m @ np.array(x, dtype=int))


def carried(a):
    f = a.copy()
    for x in np.ndindex(*a.shape):
        f[image(x)] = a[x]
    return f


bb, mir = Node(universe, world), Node(universe, world)
table = []
for r in bb.rows_:
    for j in range(len(r.lines)):
        if r.shape == 2:
            table.append(d if j == 0 else 1)
        elif r.shape == 4:
            table.append(d if j == 0 else d * sg3[j - 1])
        else:
            table.append(d if r.wall is not None else 1)
for s, lb, lm in zip(table, bb.all_lines(), mir.all_lines(), strict=True):
    lm.now[...] = s * carried(lb.now)
    lm.before[...] = s * carried(lb.before)
    r = carried(lb.rem)
    w = carried(lb.wall) if isinstance(lb.wall, np.ndarray) else lb.wall
    lm.rem[...] = r if s == 1 else w - 1 - r
    if lb.wr is not None:
        r = carried(lb.wr)
        w = carried(lb.wwall) if isinstance(lb.wwall, np.ndarray) else lb.wwall
        lm.wr[...] = r if s == 1 else w - 1 - r
for t in range(n):
    bb.step(); mir.step()
keys = ("event", "i", "node", "line_pair", "line", "sense", "beat", "minus", "plus", "W_children", "taken_row", "taken_line", "room", "cause")
for e in bb.log:
    if e["i"] == n and e["event"] in ("birth", "credit"):
        print("base  ", {k: e[k] for k in keys if k in e})
for e in mir.log:
    if e["i"] == n and e["event"] in ("birth", "credit"):
        f = dict(e)
        for k in ("node", "minus", "plus"):
            if k in f and f[k] is not None:
                f[k] = list(image(f[k]))
        print("mirror", {k: f[k] for k in keys if k in f})
