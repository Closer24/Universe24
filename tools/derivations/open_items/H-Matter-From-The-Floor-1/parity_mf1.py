"""The C, P and C P mirror of the STATE after the seed (GP-S1's one rule of the sign with the complemented remainders; P the reflection diag(-1, 1, 1) with the polar lines signed), stepped forward beside the base: per interval the integers off between the base's image and the mirror (the state the exact image until the first birth), the births compared under the image (EQUAL: the same plane at the same ends; CONJUGATE: the ends exchanged; APART), and the mirror's matter count (the + child at the take's Node against the other end, the children's W summed). Imports through run.py. Usage: python parity_mf1.py <world.json> <intervals> <image: C|P|CP> <out.json> [walled 0|1]"""
import json
import sys

import numpy as np

from event_universe.run import Node, load_world

sys.set_int_max_str_digits(0)
PLANE, POTENTIAL, CARRIER = 2, 4, 10


def carry(a):
    """a'[x] = a[g x], g the negation of the first axis on the torus."""
    return np.roll(np.flip(a, axis=0), 1, axis=0) if np.ndim(a) else a


def signs_of(node, image, walled):
    """Per row (acts' order) per line: (c_odd, p_sign)."""
    found = []
    for r in node.rows_:
        for k in range(r.shape):
            c_odd = (r.shape == PLANE and k == 0) or r.shape == POTENTIAL or (r.shape == 1 and walled)
            p_sign = 1
            if r.shape == POTENTIAL and k == 1:
                p_sign = -1
            if r.shape == CARRIER and k in (4, 7, 9):
                p_sign = -1
            sign = (-1 if (c_odd and "C" in image) else 1) * (p_sign if "P" in image else 1)
            found.append(sign)
    return found


def mirror_line(line, sign, spatial):
    f = carry if spatial else (lambda a: a)
    now, before = f(line.now) * sign, f(line.before) * sign
    wall = f(line.wall) if np.ndim(line.wall) else line.wall
    rem = f(line.rem)
    rem = wall - 1 - rem if sign < 0 else rem
    wr = None if line.wr is None else f(line.wr)
    if wr is not None and sign < 0:
        wr = line.wwall - 1 - wr
    return now, before, rem, wr


def apply_image(node, image, walled):
    spatial = "P" in image
    signs = signs_of(node, image, walled)
    k = 0
    for r in node.rows_:
        for line in r.lines:
            now, before, rem, wr = mirror_line(line, signs[k], spatial)
            line.now, line.before, line.rem = now, before, rem
            if wr is not None:
                line.wr = wr
            k += 1
    if spatial:
        for name in ("proper", "closes", "take_rem", "start_content", "turned"):
            setattr(node, name, carry(getattr(node, name)))
        node.start_x = node.row(CARRIER).lines[0].now
        node.standing = [carry(a) for a in node.standing]
        node.crossed = [carry(a) for a in node.crossed]
        node.beats = [carry(a) for a in node.beats]
    node.lattices, node.drawn = {}, {}


def off_count(base, mirror, image, walled):
    spatial = "P" in image
    signs = signs_of(base, image, walled)
    k, off = 0, 0
    for rb, rm in zip(base.rows_, mirror.rows_):
        for lb, lm in zip(rb.lines, rm.lines):
            now, before, rem, wr = mirror_line(lb, signs[k], spatial)
            off += int(np.sum(now != lm.now)) + int(np.sum(before != lm.before)) + int(np.sum(rem != lm.rem))
            if wr is not None:
                off += int(np.sum(wr != lm.wr))
            if "lines" in sys.argv:
                parts = {"now": int(np.sum(now != lm.now)), "before": int(np.sum(before != lm.before)), "rem": int(np.sum(rem != lm.rem)), "wr": 0 if wr is None else int(np.sum(wr != lm.wr))}
                if any(parts.values()):
                    print(json.dumps({"i": int(base.interval), "shape": rb.shape, "line": rb.lines.index(lb), **parts}))
            k += 1
    f = carry if spatial else (lambda a: a)
    for name in ("proper", "closes", "take_rem"):
        off += int(np.sum(f(getattr(base, name)) != getattr(mirror, name)))
    return off


def g_node(at, spatial, cube):
    return ((-at[0]) % cube, at[1], at[2]) if spatial else tuple(at)


def births_at(node, t, spatial):
    pairs = [r.pair for r in node.records()]
    found = []
    for e in node.log:
        if e["event"] == "birth" and int(e["i"]) == t:
            found.append((pairs[e["line_pair"]], g_node(e["minus"], spatial, node.cube), g_node(e["plus"], spatial, node.cube)))
    return found


def main(argv):
    world_path, intervals, image, out_path = argv[1], int(argv[2]), argv[3], argv[4]
    walled = int(argv[argv.index("walled") + 1]) if "walled" in argv else 1
    universe, world = load_world(world_path)
    base, mirror = Node(universe, world), Node(universe, world)
    apply_image(mirror, image, walled)
    spatial = "P" in image
    per = []
    first_off = first_apart = None
    verdicts = {"EQUAL": 0, "CONJUGATE": 0, "APART": 0}
    for t in range(1, intervals + 1):
        base.step()
        mirror.step()
        off = off_count(base, mirror, image, walled)
        bb = births_at(base, t, False)
        bm = births_at(mirror, t, False)
        bb_img = sorted((s, g_node(m, spatial, base.cube), g_node(p, spatial, base.cube)) for s, m, p in bb)
        bb_conj = sorted((s, p, m) for s, m, p in bb_img)
        bm_s = sorted(bm)
        verdict = "none" if not bb and not bm else "EQUAL" if bb_img == bm_s else "CONJUGATE" if bb_conj == bm_s else "APART"
        if verdict != "none":
            verdicts[verdict] += 1
            if verdict == "APART" and first_apart is None:
                first_apart = t
        if off and first_off is None:
            first_off = t
        if off or bb or bm:
            per.append({"i": t, "off": off, "base_births": len(bb), "mirror_births": len(bm), "verdict": verdict})
    def matter(node):
        births = [e for e in node.log if e["event"] == "birth"]
        r = sum(1 for b in births if b["plus"] == b["node"])
        return {"births": len(births), "plus_at_take": r, "plus_other": len(births) - r, "excess": 2 * r - len(births),
                "W_children_sum": sum(int(x) for b in births for x in b["W_children"]),
                "credits": sum(1 for e in node.log if e["event"] == "credit")}
    found = {"world": world_path, "intervals": intervals, "image": image, "walled": walled,
             "first_off": first_off, "first_apart": first_apart, "verdicts": verdicts,
             "base": matter(base), "mirror": matter(mirror), "per_interval": per[:400]}
    json.dump(found, open(out_path, "w"), indent=0)
    print(json.dumps({k: v for k, v in found.items() if k != "per_interval"}))
    print(json.dumps(per[:12]))


if __name__ == "__main__":
    main(sys.argv)
