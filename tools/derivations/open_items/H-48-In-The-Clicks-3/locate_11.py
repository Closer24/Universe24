"""The first apart line between the base and one reflection's conjugate on a named src: the chiral 3-cube run N intervals beside its x-reflected image; at every interval the state carried through the image (scalars equal; a negated line's levels negated: a plane's im line and the shape-4 row's time line by det, the odd line of the axis a by det s_a; the negated line's remainder under the ones' complement wl - 1 - r and the two's complement (wl - r) mod wl), the first mismatch per carry with the remainder, the wall, the Node's turn parity and the frame bit; the draws of the read logged at both and the first parting draw. Usage: locate_11.py <src> <world.json> <intervals> <out.json> [sx sy sz]"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe import close, take  # noqa: E402
from event_universe.core.rule3 import half, mirrored  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE, POTENTIAL  # noqa: E402

universe, world = load_world(sys.argv[2])
n = int(sys.argv[3])
cube = int(world["shape"][0])
signs = [int(x) for x in sys.argv[5:8]] if len(sys.argv) > 5 else [-1, 1, 1]
m = np.diag(signs)
det = signs[0] * signs[1] * signs[2]


def image(node):
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(w):
    found = dict(w, seed=[dict(lay) for lay in w["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(lay[key]))
    return found


def wrap(node):
    node.draws = []
    original = take.read_number

    def wrapped(nd, at, rules, unit):
        got = original(nd, at, rules, unit)
        digits = []
        is_im = nd.is_im()
        for li, (line, r) in enumerate(rules):
            for k, nn in enumerate(take.frame_nodes(nd, at)):
                wl = take.at_node(line.wall, nn)
                bit = int(rules[0][0].rem[nn])
                rem = int(line.rem[nn])
                rho = mirrored(rem, wl, (1 - bit) * (1 + is_im[li]))
                digits.append([li, k, list(nn), rem, rho, wl, bit, (1 - bit) * (1 + is_im[li]), int(nd.lattices[(id(r), k, nn)])])
        nd.draws.append({"i": nd.interval, "node": list(at), "drawn": None if got is None else list(got), "digits": digits})
        return got

    close.read_number = wrapped


def tags(node):
    found = []
    for r in node.rows_:
        for k in range(r.shape):
            if r.shape == POTENTIAL and 1 <= k <= 3:
                found.append(("odd", k - 1))
            else:
                found.append(("scalar" if not ((r.shape == PLANE and k == 1) or (r.shape == POTENTIAL and k == 0)) else "conj", r.shape, k))
    return found


def compare(base, img, turns):
    bad = {c: None for c in ("ones", "twos")}
    counts = {c: 0 for c in bad}
    bad["parity"] = None
    levels_bad = 0
    lines_b, lines_i = base.all_lines(), img.all_lines()
    for li, tag in enumerate(tags(base)):
        s = 1 if tag[0] == "scalar" else det if tag[0] == "conj" else det * signs[tag[1]]
        lb, lim = lines_b[li], lines_i[li]
        for x in np.ndindex(*base.shape):
            gx = image(x)
            if s * int(lb.now[x]) != int(lim.now[gx]) or s * int(lb.before[x]) != int(lim.before[gx]):
                levels_bad += 1
                counts.setdefault("levels_by_line", {}).setdefault(str(li) + ":" + str(tag), 0)
                counts["levels_by_line"][str(li) + ":" + str(tag)] += 1
                if tag[0] == "scalar" and tag[1] == 1 and -int(lb.now[x]) == int(lim.now[gx]) and -int(lb.before[x]) == int(lim.before[gx]):
                    counts["walled_negated"] = counts.get("walled_negated", 0) + 1
                if "level" not in bad:
                    bad["level"] = {"line": li, "tag": list(tag), "node": list(x), "sign": s, "now": [int(lb.now[x]), int(lim.now[gx])], "before": [int(lb.before[x]), int(lim.before[gx])], "rem": [int(lb.rem[x]), int(lim.rem[gx])], "wall": int(np.asarray(lb.wall)[x]) if np.ndim(lb.wall) else int(lb.wall), "turns": turns[x], "frame_bit": int(base.rows_[0].lines[0].rem[x]), "wr": None if lb.wr is None else [int(lb.wr[x]), int(lim.wr[gx])], "wwall": None if lb.wr is None else int(np.asarray(lb.wwall)[x]) if np.ndim(lb.wwall) else (None if lb.wr is None else int(lb.wwall))}
            r, ri = int(lb.rem[x]), int(lim.rem[gx])
            w = int(np.asarray(lb.wall)[x]) if np.ndim(lb.wall) else int(lb.wall)
            for c in ("ones", "twos", "parity"):
                want = r if s == 1 else (w - 1 - r if c == "ones" else (w - r) % w if c == "twos" else ((w - r) % w if turns[x] % 2 == 0 else (w - 2 - r) % w))
                if c == "parity":
                    counts.setdefault(c, 0)
                if want != ri:
                    counts[c] += 1
                    if bad[c] is None:
                        bad[c] = {"line": li, "tag": list(tag), "node": list(x), "r": r, "r_image": ri, "wall": w, "half": int(half(w)), "turns": turns[x], "frame_bit": int(base.rows_[0].lines[0].rem[x])}
    return levels_bad, counts, bad


base, img = Node(universe, world), Node(universe, world_image(world))
wrap(base)
wrap(img)
turns = {x: 0 for x in np.ndindex(*base.shape)}
per, firsts = [], {}
for t in range(n):
    base.step()
    img.step()
    for x in np.ndindex(*base.shape):
        if base.turned[x]:
            turns[x] += 1
    levels_bad, counts, bad = compare(base, img, turns)
    per.append({"i": base.interval, "levels_bad": levels_bad, "rem_bad": counts, "births": [base.counts["births"], img.counts["births"]]})
    for c in bad:
        if c not in firsts and bad.get(c) is not None:
            firsts[c] = {"i": base.interval, **bad[c]}
    if "levels" not in firsts and levels_bad:
        firsts["levels"] = {"i": base.interval, "count": levels_bad}
draws_i = {(e["i"], tuple(e["node"])): e for e in img.draws}
parting = None
for e in base.draws:
    f = draws_i.get((e["i"], image(e["node"])))
    if f is None or e["drawn"] != f["drawn"]:
        parting = {"base": e, "image": f}
        break
out = {"signs": signs, "det": det, "per_interval": per, "firsts": firsts, "first_parting_draw": parting, "draws": [len(base.draws), len(img.draws)]}
json.dump(out, open(sys.argv[4], "w"), default=str)
print(json.dumps({"firsts": firsts, "per_interval": per[:14], "parting_i": None if parting is None else parting["base"]["i"], "parting_drawn": None if parting is None else [parting["base"]["drawn"], parting["image"] and parting["image"]["drawn"]]}, default=str))
