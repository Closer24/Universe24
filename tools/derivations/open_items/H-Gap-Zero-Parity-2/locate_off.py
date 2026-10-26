"""gp2: the mirror state (the table by law, as mirror_state_gp2.py) stepped beside the base to the named interval, every integer off the table's mirror printed with its row, line, Node, base carried and mirror value. Usage: locate_off.py <src> <world.json> <interval> <image> <K|mK|mI>"""
import itertools
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

universe, world = load_world(sys.argv[2])
n, k, kind = int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
cube = int(world["shape"][0])
IMAGES = [np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)]) for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
m = IMAGES[k]
d = int(round(np.linalg.det(m)))
sg3 = [int(m[a, a]) for a in range(3)]


def image(x):
    return tuple(int(v) % cube for v in m @ np.array(x, dtype=int))


def carried(a):
    f = a.copy()
    for x in np.ndindex(*a.shape):
        f[image(x)] = a[x]
    return f


bb, mir = Node(universe, world), Node(universe, world)
table, names = [], []
for r in bb.rows_:
    for j in range(len(r.lines)):
        if r.shape == 2:
            s = (1 if j == 0 else d) if kind == "K" else (d if j == 0 else 1) if kind in ("mK", "mKA", "mKAW") else d
        else:
            s = (d if j == 0 else (d * sg3[j - 1] if kind.startswith('mKA') else sg3[j - 1])) if r.shape == 4 else (d if (r.wall is not None and 'W' in kind) else 1)  # 'W': the walled row by det (its flux 2 c Phi odd)
        table.append(s)
        names.append(f"shape{r.shape}{'(light)' if r is bb.emitter() else ''} line{j}")
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
    off = []
    for s, name, lb, lm in zip(table, names, bb.all_lines(), mir.all_lines(), strict=True):
        for field in ("now", "before"):
            a, b = s * carried(getattr(lb, field)), getattr(lm, field)
            for x in zip(*np.nonzero(a != b), strict=True):
                off.append((name, field, tuple(int(v) for v in x), int(a[x]), int(b[x])))
        r = carried(lb.rem)
        w = carried(lb.wall) if isinstance(lb.wall, np.ndarray) else lb.wall
        a = r if s == 1 else w - 1 - r
        for x in zip(*np.nonzero(a != lm.rem), strict=True):
            off.append((name, "rem", tuple(int(v) for v in x), int(a[x]), int(lm.rem[x])))
        if lb.wr is not None:
            r = carried(lb.wr)
            w = carried(lb.wwall) if isinstance(lb.wwall, np.ndarray) else lb.wwall
            a = r if s == 1 else w - 1 - r
            for x in zip(*np.nonzero(a != lm.wr), strict=True):
                off.append((name, "wr", tuple(int(v) for v in x), int(a[x]), int(lm.wr[x])))
    births = [(e["i"], e["node"], e["line_pair"], e["minus"], e["plus"]) for e in bb.log if e["event"] == "birth" and e["i"] == bb.interval]
    print("interval", bb.interval, "off", len(off), "births", births, flush=True)
    for o in off[:12]:
        print("  ", o)
    if off:
        break
