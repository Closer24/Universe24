"""a48b: the 48 on the clicks of the engine, three criteria and the state through the image.

The world is run from its seed and from each of its 48 images (the signed permutations of the axes
about the origin, the torus wrapped).  Three criteria compare the click record through the image:
  A  pm2's tuple (the birth as (take Node, plane, minus Node, plus Node, sign W at minus, sign W at plus));
     "exchanged" there negates the two signs and keeps the two Nodes in place;
  B  the births as a map child Node -> sense (the kit's, pa2's: the conjugate record swaps the two
     children's Nodes, which is the senses negated at fixed Nodes), with the take Node and the plane;
  C  B with the credits (Node, line, sense, beat), the whole click record.
A reflection's lawful image is "senses exchanged" (the ends exchanged, the senses negated); a rotation's
"equal".  Beside the clicks, the state is compared through the image at every interval: every scalar
line equal at the image Node; the shape-4 row's three odd lines carried as a vector, the level signed
with the axis, the remainder under three carries where the axis is reversed: the ones' complement
w - 1 - r (the theorem's), the two's complement (w - r) mod w (the lay's gauge), and the turn-parity
carry (w - r after an even count of the Node's turns, w - 2 - r after an odd count).  The first
interval and Node where each carry fails is written.  The digits of the one-Link read are logged at
every draw (read_number wrapped) so that the first parting draw can be read digit by digit.

Usage: PYTHONPATH=<src> python a48b_48.py <world.json> <intervals> <out.json> [images N]
"""
import copy
import itertools
import json
import os
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import close, take
from event_universe.core.rule3 import half, lattice, mirrored, quotient, remainder
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, POTENTIAL


def signed_permutations():
    axes = range(3)
    return [
        np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes])
        for pi in itertools.permutations(axes)
        for s in itertools.product((1, -1), repeat=3)
    ]


def det_of(m):
    """The determinant of a signed permutation matrix in integers: the permutation's sign times the product of the signs."""
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    signs = [int(m[pi[a], a]) for a in range(3)]
    inversions = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
    return (-1) ** inversions * signs[0] * signs[1] * signs[2]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def world_image(world, m, cube):
    w = copy.deepcopy(world)
    for lay in w.get("seed", []):
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key]), cube))
    return w


def sgn(x):
    return 1 if x > 0 else -1 if x < 0 else 0


def record_a(node, m, cube, exchange):
    """Criterion A: pm2's tuple with the senses' signs negated where `exchange`."""
    found = []
    s = -1 if exchange else 1
    for e in node.log:
        if e["event"] == "birth":
            w0, w1 = e["W_children"]
            found.append(("birth", e["i"], image(m, tuple(e["node"]), cube), e["line_pair"],
                          image(m, tuple(e["minus"]), cube), image(m, tuple(e["plus"]), cube), s * sgn(w0), s * sgn(w1)))
        elif e["event"] == "credit":
            found.append(("credit", e["i"], image(m, tuple(e["node"]), cube), e["line"], s * e["sense"], e["beat"]))
    return sorted(found)


def record_b(node, m, cube, exchange, credits):
    """Criterion B (and C with the credits): the birth as (interval, take Node, plane, the children as a sorted map Node -> sense); the conjugate negates every sense."""
    found = []
    s = -1 if exchange else 1
    for e in node.log:
        if e["event"] == "birth":
            kids = tuple(sorted([(image(m, tuple(e["minus"]), cube), -s), (image(m, tuple(e["plus"]), cube), s)]))
            found.append(("birth", e["i"], image(m, tuple(e["node"]), cube), e["line_pair"], kids))
        elif credits and e["event"] == "credit":
            found.append(("credit", e["i"], image(m, tuple(e["node"]), cube), e["line"], s * e["sense"], e["beat"]))
    return sorted(found)


def verdict(base, img, m, cube, criterion):
    if criterion == "A":
        back, back_x = record_a(img, m.T, cube, False), record_a(img, m.T, cube, True)
        b = record_a(base, np.eye(3, dtype=int), cube, False)
    else:
        credits = criterion == "C"
        back, back_x = record_b(img, m.T, cube, False, credits), record_b(img, m.T, cube, True, credits)
        b = record_b(base, np.eye(3, dtype=int), cube, False, credits)
    if back == b:
        return "equal"
    if back_x == b:
        return "senses exchanged"
    return "apart"


def first_difference(b, back):
    """The first click line (by interval) where two sorted records differ, or None."""
    for x, y in zip(b, back):
        if x != y:
            return [str(x), str(y)]
    if len(b) != len(back):
        return ["lengths", len(b), len(back)]
    return None


def wrap_read_number(node):
    """read_number wrapped: every draw's digits logged on the node (interval, Node, the tagged digits, the carry, the room)."""
    node.draws = []
    original = take.read_number

    def wrapped(nd, at, rules):
        modulus = nd.unit_gap0 * len(nd.records())
        nodes = take.frame_nodes(nd, at)
        digits = []
        origin = coarse = True
        w_half = half(nd.w)
        for li, (line, r) in enumerate(rules):
            f0 = lattice(take.at_node(line.wall, at), take.at_node(r.mass, at), *[take.at_node(x, at) for x in r.reaches])
            for k, n in enumerate(nodes):
                wl = take.at_node(line.wall, n)
                f = f0 if k == 0 else lattice(wl, take.at_node(r.reaches[k - 1], n))
                rem, values = nd.digit_of(int(line.rem[n]), quotient(wl, f))
                origin = origin and rem in (w_half, mirrored(w_half, nd.w, 1))
                coarse = coarse and values <= 3
                digits.append((quotient(rem, f), values + 1, li, k, int(line.rem[n]), wl, f))
        got = original(nd, at, rules)
        nd.draws.append({"i": nd.interval, "node": list(at), "digits": digits, "origin": origin, "coarse": coarse, "drawn": None if got is None else list(got)})
        return got

    close.read_number = wrapped


def line_tags(node):
    """Every line of the Node's rows in the acts' order with its kind: ('scalar', row shape, line index) or ('odd', axis)."""
    tags = []
    for r in node.rows_:
        for k, _line in enumerate(r.lines):
            if r.shape == POTENTIAL and 1 <= k <= 3:
                tags.append(("odd", k - 1))
            elif r.shape == CARRIER and 1 <= k <= 3:
                tags.append(("axis_even", k - 1))
            else:
                tags.append(("scalar", r.shape, k))
    return tags


def map_array(a, m, cube, shape):
    """The array carried to the image: out[g x] = a[x]."""
    out = np.empty(shape, dtype=object)
    for x in np.ndindex(*shape):
        out[image(m, x, cube)] = a[x]
    return out


def compare_state(base, img, m, cube, turns_base, carries):
    """The image run's state against the base's through the image; per carry the count of mismatching (line, Node) entries, split into scalars, odd levels, odd remainders."""
    shape = base.shape
    tags = line_tags(base)
    lines_b, lines_i = base.all_lines(), img.all_lines()
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    signs = [int(m[pi[a], a]) for a in range(3)]
    bad = {c: {"scalar": 0, "odd_level": 0, "odd_rem": 0, "odd_wr": 0, "first": None} for c in carries}
    det = det_of(m)
    # every line: its sign under the image (1 for an even line; det for a plane's im line and the shape-4 row's time line, the conjugation of the reflected world; det s_a for the odd line of the axis a, an axial vector) and its image line (the odd lines and the carrier's axis lines permuted with the axes)
    for li, tag in enumerate(tags):
        if tag[0] in ("odd", "axis_even"):
            a = tag[1]
            li_img = li - a + pi[a]
            s = det * signs[a] if tag[0] == "odd" else 1
        else:
            li_img = li
            s = det if (tag[1] == PLANE and tag[2] == 1) or (tag[1] == POTENTIAL and tag[2] == 0) else 1
        lb, lim = lines_b[li], lines_i[li_img]
        kind = "odd" if s == -1 else "scalar"
        if s == 1:
            for name, arr_b, arr_i in (("now", lb.now, lim.now), ("before", lb.before, lim.before), ("rem", lb.rem, lim.rem)):
                mapped = map_array(arr_b, m, cube, shape)
                n_bad = int(sum(1 for x in np.ndindex(*shape) if int(mapped[x]) != int(arr_i[x])))
                for c in carries:
                    bad[c]["scalar"] += n_bad
                    if n_bad and bad[c]["first"] is None:
                        bad[c]["first"] = ["scalar", tag, name]
            continue
        a = tag
        for name, arr_b, arr_i in (("now", lb.now, lim.now), ("before", lb.before, lim.before)):
            mapped = map_array(arr_b, m, cube, shape)
            n_bad = int(sum(1 for x in np.ndindex(*shape) if s * int(mapped[x]) != int(arr_i[x])))
            for c in carries:
                bad[c]["odd_level"] += n_bad
                if n_bad and bad[c]["first"] is None:
                    bad[c]["first"] = [tag[0], a, name]
        for name, arr_b, arr_i, wall_b, wall_i in (("rem", lb.rem, lim.rem, lb.wall, lim.wall), ("wr", lb.wr, lim.wr, lb.wwall, lim.wwall)):
            if arr_b is None:
                continue
            for x in np.ndindex(*shape):
                gx = image(m, x, cube)
                r, ri = int(arr_b[x]), int(arr_i[gx])
                w = int(np.asarray(wall_b)[x]) if np.ndim(wall_b) else int(wall_b)
                parity = turns_base[x] % 2
                for c in carries:
                    if s == 1:
                        want = r
                    elif c == "ones":
                        want = w - 1 - r
                    elif c == "twos":
                        want = (w - r) % w
                    else:
                        want = (w - r) % w if parity == 0 else (w - 2 - r) % w
                    if want != ri:
                        bad[c]["odd_" + name] += 1
                        if bad[c]["first"] is None:
                            bad[c]["first"] = [tag[0], a, name, list(x), r, ri, w, parity]
    return bad


def run_pair(universe, world, m, cube, n, carries, track):
    """The base and the image run side by side, interval by interval; the state compared through the image at every interval where `track`."""
    base, img = Node(universe, world), Node(universe, world_image(world, m, cube))
    wrap_read_number(base)
    wrap_read_number(img)
    turns = {x: 0 for x in np.ndindex(*base.shape)}
    firsts = {c: None for c in carries}
    per_interval = []
    for t in range(n):
        base.step()
        img.step()
        for x in np.ndindex(*base.shape):
            if base.turned[x]:
                turns[x] += 1
        if track:
            bad = compare_state(base, img, m, cube, turns, carries)
            per_interval.append({c: [bad[c]["scalar"], bad[c]["odd_level"], bad[c]["odd_rem"], bad[c]["odd_wr"]] for c in carries})
            for c in carries:
                if firsts[c] is None and bad[c]["first"] is not None:
                    firsts[c] = {"i": base.interval, **bad[c]}
    return base, img, firsts, per_interval


def main(argv):
    universe, world = load_world(argv[1])
    n = int(argv[2])
    cube = int(world["shape"][0])
    limit = int(argv[argv.index("images") + 1]) if "images" in argv else 48
    track = "notrack" not in argv
    carries = ["ones", "twos", "parity"]
    mats = signed_permutations()
    # the seed's stabilizer in the 48 (a seed with a mirror plane births nothing under the twist)
    seed_nodes = sorted(tuple(lay.get("at", lay.get("centre"))) for lay in world.get("seed", []) if "at" in lay or "centre" in lay)
    stabilizer = [k for k, m in enumerate(mats) if sorted(image(m, s, cube) for s in seed_nodes) == [tuple(s) for s in seed_nodes]]
    counts = {c: {"equal": 0, "senses exchanged": 0, "apart": 0} for c in "ABC"}
    rows = []
    base_ref = None
    for k, m in enumerate(mats[:limit]):
        base, img, firsts, per_interval = run_pair(universe, world, m, cube, n, carries, track)
        base_ref = base
        d = det_of(m)
        row = {"image": k, "det": d, "matrix": m.tolist(), "births": img.counts["births"], "credits": img.counts["body_clicks"], "turns": img.counts["turns"]}
        for c in "ABC":
            v = verdict(base, img, m, cube, c)
            counts[c][v] += 1
            row["verdict_" + c] = v
        b_rec = record_b(base, np.eye(3, dtype=int), cube, False, True)
        back = record_b(img, m.T, cube, False, True)
        back_x = record_b(img, m.T, cube, True, True)
        row["first_difference_C_equal"] = first_difference(b_rec, back)
        row["first_difference_C_exchanged"] = first_difference(b_rec, back_x)
        row["state_first_mismatch"] = firsts
        # the first draw whose digit multiset differs through the image
        draws_i = {(e["i"], tuple(e["node"])): e for e in img.draws}
        parting = None
        for e in base.draws:
            key = (e["i"], image(m, tuple(e["node"]), cube))
            f = draws_i.get(key)
            db = sorted((x[0], x[1]) for x in e["digits"])
            di = None if f is None else sorted((x[0], x[1]) for x in f["digits"])
            if f is None or db != di or e["drawn"] != f["drawn"]:
                differing = []
                if f is not None:
                    for x in e["digits"]:
                        tag = (x[2],)
                        same = [y for y in f["digits"] if y[2] == x[2] and y[0] == x[0] and y[1] == x[1]]
                        if not same:
                            differing.append({"line": x[2], "slot": x[3], "digit": x[0], "base": x[1], "rem": x[4], "wall": x[5], "lattice": x[6]})
                parting = {"i": e["i"], "node": e["node"], "image_node": list(key[1]), "image_draw_found": f is not None, "drawn_base": e["drawn"], "drawn_image": None if f is None else f["drawn"], "digits_differing_base_side": differing[:12], "count_differing": len(differing), "count_digits": len(e["digits"])}
                break
        row["first_parting_draw"] = parting
        row["draws_base"] = len(base.draws)
        # the residues of every logged digit's remainder on its lattice, over the base's draws: 0, F - 1, or other
        hist = {"zero": 0, "F-1": 0, "other": 0}
        for e in base.draws:
            for x in e["digits"]:
                s_res = x[4] % x[6]
                hist["zero" if s_res == 0 else "F-1" if s_res == x[6] - 1 else "other"] += 1
        row["residues"] = hist
        # the folds read offline at the first parting draw: would the folded digit multisets agree there
        if parting is not None and parting["image_draw_found"]:
            e = next(d for d in base.draws if d["i"] == parting["i"] and d["node"] == parting["node"])
            f = draws_i[(e["i"], tuple(parting["image_node"]))]
            def fold_ones(x):
                d, b, rem, wl, F = x[0], x[1], x[4], x[5], x[6]
                return (min(rem, wl - 1 - rem) // F, b)
            def fold_lattice(x):
                rem, wl, F = x[4], x[5], x[6]
                values = wl // F
                delta = (rem + F - 1) // F
                return (min(delta, values - delta), values // 2 + 1)
            row["fold_at_parting"] = {
                "ones": sorted(fold_ones(x) for x in e["digits"]) == sorted(fold_ones(x) for x in f["digits"]),
                "lattice": sorted(fold_lattice(x) for x in e["digits"]) == sorted(fold_lattice(x) for x in f["digits"]),
            }
        rows.append(row)
        print(json.dumps({k2: row.get(k2) for k2 in ("image", "det", "verdict_A", "verdict_B", "verdict_C", "births", "credits", "state_first_mismatch", "first_parting_draw", "residues", "fold_at_parting")}, default=str), flush=True)
    summary = {
        "world": argv[1], "intervals": n, "cube": cube, "images": limit,
        "seed_stabilizer_size": len(stabilizer), "seed_stabilizer": stabilizer,
        "base births": base_ref.counts["births"], "base credits": base_ref.counts["body_clicks"], "base turns": base_ref.counts["turns"], "base counts": base_ref.counts,
        "counts": counts,
        "by_det": {c: {d: {v: sum(1 for r in rows if r["det"] == d and r["verdict_" + c] == v) for v in counts[c]} for d in (1, -1)} for c in "ABC"},
        "odd_lines_moved_in_base": int(max(abs(int(v)) for line in base_ref.row(POTENTIAL).lines[1:4] for v in line.now.reshape(-1))),
        "gapped_levels_in_base": int(max(abs(int(v)) for r in base_ref.gapped for line in r.lines for v in line.now.reshape(-1))),
    }
    print(json.dumps(summary, default=str))
    json.dump({"summary": summary, "rows": rows}, open(argv[3], "w"), default=str)


if __name__ == "__main__":
    main(sys.argv)
