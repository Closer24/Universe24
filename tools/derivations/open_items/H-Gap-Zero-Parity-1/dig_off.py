"""gp1: the first integers of the mirror STATE off the table's mirror, by line and Node (image, table mode, intervals as mirror_state.py). Usage: dig_off.py <src> <world.json> <intervals> <image> <mode>"""
import sys, itertools, json
import numpy as np
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
exec(open("mirror_state.py").read().split("base = Node(universe, world)")[0].replace("sys.argv[1]", "sys.argv[1]").replace("which = list(range(48)) if len(sys.argv) < 6 else [int(x) for x in sys.argv[5].split(\",\")]", "which = [int(sys.argv[4])]"))
m = IMAGES[int(sys.argv[4])]; mode = sys.argv[5]
b0, i0 = Node(universe, world), Node(universe, world_image(world, m))
t0 = parity_of(b0, i0, m); b0.step(); i0.step(); t1 = parity_of(b0, i0, m)
table = [a if a in (1, -1) else (b if b in (1, -1) else 0) for a, b in zip(t0, t1, strict=True)]
d, kk, emitter, sg3 = det_of(m), 0, b0.emitter(), [int(m[a, a]) for a in range(3)]
if mode in ("law", "gp1u", "gp1l", "gp1v", "gp1w"):
    table = []
    for r in b0.rows_:
        for j in range(len(r.lines)):
            if r.shape == 2:
                flipped = mode in ("gp1u", "gp1v", "gp1w") or (mode == "gp1l" and r is emitter)
                table.append((d if j == 0 else 1) if flipped else (1 if j == 0 else d))
            elif r.shape == 4:
                table.append(d if j == 0 else (d * sg3[j - 1] if mode in ("gp1v", "gp1w") else sg3[j - 1]))  # gp1v: the sign holder C-odd as a whole, its odd lines det times the axis's sign
            else:
                table.append(d if (mode == "gp1w" and r.shape == 1) else 1)  # gp1w: the walled row (one line, the flux 2 c Phi of the time line) odd as the time line is, lr1's reading
for r in b0.rows_:
    for j in range(len(r.lines)):
        if r.shape == 2 and (mode == "mu" or (mode == "ml" and r is emitter)):
            table[kk] = d if j == 0 else 1
        kk += 1
names = [f"shape{r.shape}:{'emitter' if r is emitter else 'row'}:{j}" for r in b0.rows_ for j in range(len(r.lines))]
print("table", list(zip(names, table)))
bb, mir = Node(universe, world), Node(universe, world)
for s, lb, lm in zip(table, bb.all_lines(), mir.all_lines(), strict=True):
    sg = 1 if s in (0, 2) else s
    lm.now[...] = sg * carried(lb.now, m); lm.before[...] = sg * carried(lb.before, m)
    r = carried(lb.rem, m); w = carried(lb.wall, m) if isinstance(lb.wall, np.ndarray) else lb.wall
    lm.rem[...] = r if sg == 1 else w - 1 - r
    if lb.wr is not None:
        r = carried(lb.wr, m); w = carried(lb.wwall, m) if isinstance(lb.wwall, np.ndarray) else lb.wwall
        lm.wr[...] = r if sg == 1 else w - 1 - r
for t in range(n):
    bb.step(); mir.step()
    off = []
    for s, nm, lb, lm in zip(table, names, bb.all_lines(), mir.all_lines(), strict=True):
        sg = 1 if s in (0, 2) else s
        for name in ("now", "before"):
            a, b = sg * carried(getattr(lb, name), m), getattr(lm, name)
            for x in zip(*np.nonzero(a != b)):
                off.append((nm, name, tuple(int(v) for v in x), int(a[x]), int(b[x])))
        r = carried(lb.rem, m); w = carried(lb.wall, m) if isinstance(lb.wall, np.ndarray) else lb.wall
        a = r if sg == 1 else w - 1 - r
        for x in zip(*np.nonzero(a != lm.rem)):
            off.append((nm, "rem", tuple(int(v) for v in x), int(a[x]), int(lm.rem[x])))
        if lb.wr is not None:
            r = carried(lb.wr, m); w = carried(lb.wwall, m) if isinstance(lb.wwall, np.ndarray) else lb.wwall
            a = r if sg == 1 else w - 1 - r
            for x in zip(*np.nonzero(a != lm.wr)):
                off.append((nm, "wr", tuple(int(v) for v in x), int(a[x]), int(lm.wr[x])))
    print("interval", bb.interval, "off", len(off), off[:12], "births", bb.counts["births"], mir.counts["births"], flush=True)
    if off and bb.interval > 5: break
