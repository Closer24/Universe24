"""a48: the parting birth diagnosed, interval by interval. The seed is run beside its image under one element m of the 48
(default the reflection diag(-1, 1, 1)); after every interval every line of every row is compared through the image: the
levels at the image Node against the base's with the sign the law predicts (C P for a reflection: the planes' re lines even,
the im lines odd; the carrier's lines even, its axis lines permuted; the shape-4 row's time line odd, its three odd lines
a vector times the conjugation; the walled row odd), the remainders equal or mirrored to 2 half(W) - r, read as which of the
two holds. The one-Link read is wrapped so that every draw's digits are logged (the Node, every line's digit with its base,
the number and the room); the first draw whose digit set differs through the image is printed with the line whose digit
differs first, the two remainders, the two digits, and both runs' births at that interval.
Usage: python a48_parting.py <world.json> <cube> <intervals> <out.json> [mx my mz] (the diagonal of m; default -1 1 1);
integers only."""
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import close, take  # noqa: E402
from event_universe.core.rule3 import half  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE, POTENTIAL  # noqa: E402

from a48_48 import determinant, image, world_image  # noqa: E402

DRAWS = {}


def wrapped_read(tag):
    original = take.read_number

    def read(node, at, rules):
        digits = []
        nodes = take.frame_nodes(node, at)
        for li, (line, r) in enumerate(rules):
            f0 = take.lattice(
                take.at_node(line.wall, at), take.at_node(r.mass, at), *[take.at_node(x, at) for x in r.reaches]
            )
            for k, n in enumerate(nodes):
                wl = take.at_node(line.wall, n)
                f = f0 if k == 0 else take.lattice(wl, take.at_node(r.reaches[k - 1], n))
                raw = int(line.rem[n])
                rem, values = node.digit_of(raw, wl, f) if node.digit_of.__code__.co_argcount == 4 else node.digit_of(raw, take.quotient(wl, f))
                digits.append((li, k, n, raw, wl, int(take.quotient(rem, f)), int(values) + 1))
        found = original(node, at, rules)
        DRAWS.setdefault(tag, []).append((node.interval, at, digits, found))
        return found

    return read


def line_kinds(node):
    """Every line in the acts' order with its kind: ('re', rec), ('im', rec), ('carrier', k), ('potential', k), ('walled', 0)."""
    kinds = []
    for r in node.rows_:
        if r.wall is not None:
            kinds += [("walled", 0)]
        elif r.shape == PLANE:
            rec = node.records().index(r)
            kinds += [("re", rec), ("im", rec)]
        elif r.shape == CARRIER:
            kinds += [("carrier", k) for k in range(r.shape)]
        elif r.shape == POTENTIAL:
            kinds += [("potential", k) for k in range(r.shape)]
        else:
            kinds += [("other", k) for k in range(r.shape)]
    return kinds


def axis_map(m):
    """Under m, the axis a maps to the axis b with the sign m[b, a]."""
    found = {}
    for a in range(3):
        b = int(np.nonzero(m[:, a])[0][0])
        found[a] = (b, int(m[b, a]))
    return found


def partner(kinds, kind, m):
    """The line of the image run that the base line maps to, with the sign the law predicts for a reflection (C P) or a
    rotation (P alone)."""
    reflection = determinant(m) == -1
    conj = -1 if reflection else 1
    what, k = kind
    if what == "re":
        return kinds.index(kind), 1
    if what == "im":
        return kinds.index(kind), conj
    if what == "walled":
        return kinds.index(kind), conj
    if what == "carrier":
        if 1 <= k <= 3:
            b, _s = axis_map(m)[k - 1]
            return kinds.index(("carrier", b + 1)), 1
        return kinds.index(kind), 1
    if what == "potential":
        if k == 0:
            return kinds.index(kind), conj
        b, s = axis_map(m)[k - 1]
        return kinds.index(("potential", b + 1)), s * conj
    return kinds.index(kind), 1


def compare(base, img, m, cube, kinds):
    """Every line compared through the image: the levels (now, before) against the predicted sign, the remainders equal or
    mirrored; returns per line (levels: 'held' / 'apart' with the count, remainders: 'equal' / 'mirrored' / 'mixed' / 'apart')."""
    b_lines, i_lines = base.all_lines(), img.all_lines()
    out = []
    for li, kind in enumerate(kinds):
        lj, sign = partner(kinds, kind, m)
        lb, lim = b_lines[li], i_lines[lj]
        apart = 0
        eq = mir = rem_apart = 0
        for at in np.ndindex(*base.shape):
            there = image(m, at, cube)
            if int(lim.now[there]) != sign * int(lb.now[at]) or int(lim.before[there]) != sign * int(lb.before[at]):
                apart += 1
            rb, ri = int(lb.rem[at]), int(lim.rem[there])
            wb = int(np.asarray(lb.wall)[at]) if np.ndim(lb.wall) else int(lb.wall)
            if ri == rb:
                eq += 1
            elif ri == 2 * int(half(wb)) - rb:
                mir += 1
            else:
                rem_apart += 1
        out.append(
            {
                "line": list(kind),
                "sign": sign,
                "levels apart": apart,
                "rem equal": eq,
                "rem mirrored": mir,
                "rem apart": rem_apart,
            }
        )
    return out


def main(argv):
    universe, world = load_world(argv[1])
    cube, intervals = int(argv[2]), int(argv[3])
    diag = [int(x) for x in argv[5:8]] if len(argv) >= 8 else [-1, 1, 1]
    m = np.diag(diag).astype(int)
    eye = np.eye(3, dtype=int)
    base = Node(json.loads(json.dumps(universe)), world_image(world, eye, cube, intervals))
    img = Node(json.loads(json.dumps(universe)), world_image(world, m, cube, intervals))
    kinds = line_kinds(base)
    report = {"m": m.tolist(), "cube": cube, "intervals": intervals, "per interval": []}
    first_level_part = None
    first_draw_part = None
    for t in range(intervals):
        close.read_number = wrapped_read("base")
        base.step()
        close.read_number = wrapped_read("image")
        img.step()
        cmp = compare(base, img, m, cube, kinds)
        parted = [c for c in cmp if c["levels apart"] or c["rem apart"]]
        births_b = [(e["node"], e["line_pair"], e["minus"], e["plus"]) for e in base.log if e["event"] == "birth" and e["i"] == base.interval]
        births_i = [(e["node"], e["line_pair"], e["minus"], e["plus"]) for e in img.log if e["event"] == "birth" and e["i"] == img.interval]
        row = {
            "i": base.interval,
            "births base": len(births_b),
            "births image": len(births_i),
            "lines with levels apart": [c["line"] for c in cmp if c["levels apart"]],
            "lines with rem apart": [c["line"] for c in cmp if c["rem apart"]],
            "lines with rem mirrored (count of Nodes)": {str(c["line"]): c["rem mirrored"] for c in cmp if c["rem mirrored"]},
        }
        report["per interval"].append(row)
        if parted and first_level_part is None:
            first_level_part = {"i": base.interval, "lines": parted, "births base": births_b, "births image": births_i}
            report["first interval with a level apart"] = first_level_part
        # the draws of this interval compared through the image
        db = [d for d in DRAWS.get("base", []) if d[0] == base.interval]
        di = [d for d in DRAWS.get("image", []) if d[0] == img.interval]
        if first_draw_part is None:
            di_by_node = {d[1]: d for d in di}
            for d in db:
                there = image(m, d[1], cube)
                if there not in di_by_node:
                    first_draw_part = {"i": d[0], "node": list(d[1]), "cause": "the image draws at no such Node", "base result": d[3]}
                    break
                e = di_by_node[there]
                sb = sorted((x[5], x[6]) for x in d[2])
                si = sorted((x[5], x[6]) for x in e[2])
                if sb != si or d[3] != e[3]:
                    # the line whose digit differs first: the same (line, neighbour k) through the image
                    diffs = []
                    e_by = {(x[0], x[1]): x for x in e[2]}
                    for x in d[2]:
                        li, k, n, raw, wl, dg, bs = x
                        lj, _sign = partner(kinds, kinds[li], m)
                        # the neighbour k through the image: the Port k-1 maps to the Port of the image axis
                        y = None
                        for cand in e[2]:
                            if cand[0] == lj and cand[2] == image(m, n, cube):
                                y = cand
                                break
                        if y is None or (dg, bs) != (y[5], y[6]):
                            diffs.append(
                                {
                                    "line": list(kinds[li]),
                                    "neighbour": list(n),
                                    "base rem": raw,
                                    "image rem": None if y is None else y[3],
                                    "wall W": wl,
                                    "2 half(W) - base rem": 2 * int(half(wl)) - raw,
                                    "base digit, base": [dg, bs],
                                    "image digit, base": None if y is None else [y[5], y[6]],
                                }
                            )
                    first_draw_part = {
                        "i": d[0],
                        "node": list(d[1]),
                        "image node": list(there),
                        "base (number, room)": d[3],
                        "image (number, room)": e[3],
                        "base digit set equals image digit set": sb == si,
                        "digits that differ (first 8)": diffs[:8],
                        "count of digits that differ": len(diffs),
                        "births base at i": births_b,
                        "births image at i": births_i,
                    }
                    break
            if first_draw_part is not None:
                report["first draw apart"] = first_draw_part
        print(json.dumps(row), flush=True)
    report["base counts"] = {k: str(v) for k, v in base.counts.items()}
    report["image counts"] = {k: str(v) for k, v in img.counts.items()}
    print(json.dumps({"first interval with a level apart": first_level_part}))
    print(json.dumps({"first draw apart": first_draw_part}))
    with open(argv[4], "w", encoding="utf-8") as out:
        json.dump(report, out)


if __name__ == "__main__":
    main(sys.argv)
