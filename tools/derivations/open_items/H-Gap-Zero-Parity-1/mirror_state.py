"""gp1's copy of lr2's tool with the sign table amended (the modes law, gp1u, gp1l, the sixth argument). The 48 through the C P mirror STATE (David's root cause, #2187 6406297069): the base world laid from its file; for each image g of the 48 the sign table read from the FILE images at the interval 0 and 1 (a line even where its level is equal at g x, odd where negated; a line at 0 on the whole board read at the interval 1 of the file image, else even by name); the mirror state built from the base's seed state by the table (every level signed, every odd line's remainder W - 1 - r and its write remainder likewise), stepped N intervals beside the base; the click record carried back and compared (EQUAL / CONJUGATE / APART with the first apart interval), and the state compared at every interval (the first interval any integer is off the table's mirror). Usage: mirror_state.py <src> <world.json> <intervals> <out.json> [images comma-separated] [measured|law|gp1u|gp1l]"""
import itertools
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

universe, world = load_world(sys.argv[2])
n = int(sys.argv[3])
world = dict(world, intervals=n)
cube = int(world["shape"][0])
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]
which = list(range(48)) if len(sys.argv) < 6 else [int(x) for x in sys.argv[5].split(",")]


def det_of(m):
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    signs = [int(m[pi[a], a]) for a in range(3)]
    inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
    return (-1) ** inv * signs[0] * signs[1] * signs[2]


def image(m, node):
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(w, m):
    found = dict(w, seed=[dict(lay) for lay in w["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, lay[key]))
    return found


def carried(a, m):
    """An array carried to the image Nodes: found[g x] = a[x]."""
    found = a.copy()
    for x in np.ndindex(*a.shape):
        found[image(m, x)] = a[x]
    return found


def parity_of(base, img, m):
    """Per line: +1 even, -1 odd, 0 undetermined (the line 0 on the whole board of both)."""
    table = []
    for lb, li in zip(base.all_lines(), img.all_lines(), strict=True):
        s = 0
        for name in ("now", "before"):
            a, b = carried(getattr(lb, name), m), getattr(li, name)
            if np.any(a != 0):
                if np.array_equal(a, b):
                    s = s if s else 1
                elif np.array_equal(-a, b):
                    s = s if s else -1
                else:
                    s = s if s else 2
        table.append(s)
    return table


def record(node, m, s):
    found = []
    for e in node.log:
        if e["event"] == "birth":
            kids = tuple(sorted([(image(m, e["minus"]), -s), (image(m, e["plus"]), s)]))
            found.append(("birth", e["i"], image(m, e["node"]), e["line_pair"], kids))
        elif e["event"] == "credit":
            found.append(("credit", e["i"], image(m, e["node"]), e["line"], s * e["sense"], e["beat"]))
    return sorted(found)


def first_apart(a, b):
    sa, sb = set(a), set(b)
    odd = sorted(sa ^ sb, key=lambda x: x[1])
    return None if not odd else odd[0][1]


def mirror_off(base, mir, m, table):
    """The count of integers of the mirror state off the table's mirror of the base."""
    off = 0
    for s, lb, lm in zip(table, base.all_lines(), mir.all_lines(), strict=True):
        s = 1 if s in (0, 2) else s
        for name in ("now", "before"):
            off += int(np.sum(s * carried(getattr(lb, name), m) != getattr(lm, name)))
        r = carried(lb.rem, m)
        w = carried(lb.wall, m) if isinstance(lb.wall, np.ndarray) else lb.wall
        off += int(np.sum((r if s == 1 else w - 1 - r) != lm.rem))
        if lb.wr is not None:
            r = carried(lb.wr, m)
            w = carried(lb.wwall, m) if isinstance(lb.wwall, np.ndarray) else lb.wwall
            off += int(np.sum((r if s == 1 else w - 1 - r) != lm.wr))
    return off


base = Node(universe, world)
rows = []
for k in which:
    m = IMAGES[k]
    # the sign table from the file images at the intervals 0 and 1
    b0, i0 = Node(universe, world), Node(universe, world_image(world, m))
    t0 = parity_of(b0, i0, m)
    b0.step(); i0.step()
    t1 = parity_of(b0, i0, m)
    table = [a if a in (1, -1) else (b if b in (1, -1) else 0) for a, b in zip(t0, t1, strict=True)]
    mode = sys.argv[6] if len(sys.argv) > 6 else "measured"
    if mode in ("mu", "ml"):  # gp1: lr2's measured table (the file images at 0 and 1) with the planes' entries amended: "mu" every plane (det, even), "ml" the gap-0 plane alone (det, even), the rest as measured (David's one sign changed, 6407559475, is "ml" on the measured table)
        d, kk, emitter = det_of(m), 0, b0.emitter()
        for r in b0.rows_:
            for j in range(len(r.lines)):
                if r.shape == 2 and (mode == "mu" or r is emitter):
                    table[kk] = d if j == 0 else 1
                kk += 1
    if mode in ("law", "gp1u", "gp1l", "gp1v", "gp1w"):  # the table by the law for a diagonal image; "law" lr2's (every plane re even, im by det); "gp1u" gp1's uniform table (every plane re by det, im even: the conjugation composed with the half turn, the plane's Wronskian odd under it); "gp1l" the gap-0 plane alone at (det, even), the planes with a gap at lr2's (even, det); the potential's time line by det, its odd line a by s_a, the carrier and the walled row even
        d, sg3 = det_of(m), [int(m[a, a]) for a in range(3)]
        table = []
        emitter = b0.emitter()
        for r in b0.rows_:
            for j in range(len(r.lines)):
                if r.shape == 2:
                    flipped = mode in ("gp1u", "gp1v", "gp1w") or (mode == "gp1l" and r is emitter)
                    table.append((d if j == 0 else 1) if flipped else (1 if j == 0 else d))
                elif r.shape == 4:
                    table.append(d if j == 0 else (d * sg3[j - 1] if mode in ("gp1v", "gp1w") else sg3[j - 1]))  # gp1v: the sign holder C-odd as a whole, its odd lines det times the axis's sign
                else:
                    table.append(d if (mode == "gp1w" and r.shape == 1) else 1)  # gp1w: the walled row (one line, the flux 2 c Phi of the time line) odd as the time line is, lr1's reading
    # the mirror state from the base's seed state
    bb, mir = Node(universe, world), Node(universe, world)
    for s, lb, lm in zip(table, bb.all_lines(), mir.all_lines(), strict=True):
        sg = 1 if s in (0, 2) else s
        lm.now[...] = sg * carried(lb.now, m)
        lm.before[...] = sg * carried(lb.before, m)
        r = carried(lb.rem, m)
        w = carried(lb.wall, m) if isinstance(lb.wall, np.ndarray) else lb.wall
        lm.rem[...] = r if sg == 1 else w - 1 - r
        if lb.wr is not None:
            r = carried(lb.wr, m)
            w = carried(lb.wwall, m) if isinstance(lb.wwall, np.ndarray) else lb.wwall
            lm.wr[...] = r if sg == 1 else w - 1 - r
    first_state_off = None
    for t in range(n):
        bb.step(); mir.step()
        if first_state_off is None and mirror_off(bb, mir, m, table):
            first_state_off = bb.interval
    base_rec = record(bb, np.eye(3, dtype=int), 1)
    back, back_x = record(mir, m.T, 1), record(mir, m.T, -1)
    v = "EQUAL" if back == base_rec else "CONJUGATE" if back_x == base_rec else "APART"
    row = {"image": k, "det": det_of(m), "verdict": v, "births_base": bb.counts["births"], "births_mirror": mir.counts["births"],
           "credits_base": bb.counts["body_clicks"], "credits_mirror": mir.counts["body_clicks"],
           "first_apart_equal": first_apart(base_rec, back), "first_apart_conjugate": first_apart(base_rec, back_x),
           "first_state_off_mirror": first_state_off, "table": table}
    rows.append(row)
    print(json.dumps(row), flush=True)
json.dump(rows, open(sys.argv[4], "w"))
