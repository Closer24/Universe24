"""ma1's driver: the engine's own Node, Interval and writer (src untouched), with a fourth form of the lay laid by the driver after the file's lays: `plasma` lays one rest record of a plane with a gap at every Node of a pattern (uniform / checker / stripes4 / pair), the amplitude fitted so that the largest share over the board at the vacuum's weight is at most `quanta` units of the row (seed.fitted's search on the pattern itself); `flip` names Nodes whose sense is flipped and `remove` Nodes left empty (the group broken by one quantum). Per interval the driver reads the board's mean / least / largest X, the spread e in thousandths (the largest over the Links), the turns, the gap-0 line's share at the vacuum's weight (the largest over the board, in units, and the count of Nodes at or above one unit), the largest |F| of the gap-0 line over the Links, the largest |twist|, the planes' W summed, the births / credits / refusals so far, and the group's invariance (every array constant over the board for the uniform patterns; the translation by one Link composed with the sense's flip for the checker; the translation by two and the stripes' reflection composed with the flip for the stripes). Integers only.
Usage: python ma_run.py <world.json> <out_prefix> [back N]; the record at <out_prefix>_record.json (the engine's), the readings at <out_prefix>_diag.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import readings, run
from event_universe.core.ports import AXES, across
from event_universe.core.rule3 import quotient
from event_universe.links import link_current, twist, wronskian
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, zeros
from event_universe.seed import rest_record

THOUSAND = 1000


def ints(a: Any) -> list[int]:
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def pattern_masks(node: Node, pattern: str, sense: int = 1) -> list[tuple[int, Any]]:
    """The (sense, envelope) pairs of a pattern: uniform (+1 everywhere), pair (+1 and -1 everywhere), checker (+1 at the even Nodes, -1 at the odd, the parity of the index sum), stripes4 (+1 where x mod 4 in {0, 1}, -1 where in {2, 3})."""
    idx = np.indices(node.shape)
    parity = (idx[0] + idx[1] + idx[2]) % 2
    one = zeros(node.shape) + 1
    if pattern == "uniform":
        return [(sense, one)]
    if pattern == "pair":
        return [(1, one), (-1, one)]
    if pattern == "checker":
        return [(1, np.where(parity == 0, 1, 0).astype(object)), (-1, np.where(parity == 1, 1, 0).astype(object))]
    if pattern == "stripes4":
        half_x = (idx[0] % 4) // 2
        return [(1, np.where(half_x == 0, 1, 0).astype(object)), (-1, np.where(half_x == 1, 1, 0).astype(object))]
    raise ValueError(f"no pattern {pattern!r}")


def apply_defects(masks: list[tuple[int, Any]], flips: list[Any], removes: list[Any]) -> list[tuple[int, Any]]:
    """The group broken by name: at a flipped Node the sense's envelope moves to the other sense; at a removed Node both envelopes are 0."""
    by_sense = {s: e.copy() for s, e in masks}
    for s in (1, -1):
        if s not in by_sense:
            by_sense[s] = zeros(next(iter(by_sense.values())).shape)
    for xyz in flips:
        at = tuple(int(x) for x in xyz)
        plus, minus = int(by_sense[1][at]), int(by_sense[-1][at])
        by_sense[1][at], by_sense[-1][at] = minus, plus
    for xyz in removes:
        at = tuple(int(x) for x in xyz)
        by_sense[1][at], by_sense[-1][at] = 0, 0
    return [(s, e) for s, e in by_sense.items() if int(sum(ints(e))) > 0]


def share_of_pattern(node: Node, rec: int, masks: list[tuple[int, Any]], amplitude: int) -> tuple[int, int]:
    """The largest and the summed share over the board at the vacuum's weight of the pattern laid at the amplitude (the lines summed over the senses first, as the lay adds them)."""
    row = node.records()[rec]
    rule = node.rule_of(row, node.content(), node.link_factors())
    re_now, re_before, im_now, im_before = zeros(node.shape), zeros(node.shape), zeros(node.shape), zeros(node.shape)
    for sense, env in masks:
        re, im = rest_record(node, row, env, 1, amplitude, sense)
        re_now, re_before = re_now + re.now, re_before + re.before
        im_now, im_before = im_now + im.now, im_before + im.before
    re_l = type(row.lines[0])(re_now, re_before, None, node.w)
    im_l = type(row.lines[0])(im_now, im_before, None, node.w)
    sh = node.share(re_l, rule, vacuum=True) + node.share(im_l, rule, vacuum=True)
    laid = zeros(node.shape)
    for _sense, env in masks:
        laid = laid + env
    values = [int(v) for v, l in zip(ints(sh), ints(laid), strict=True) if l > 0]
    return min(values), sum(values)


def fitted_pattern(node: Node, rec: int, masks: list[tuple[int, Any]], target: int) -> int:
    """The least amplitude at which the least share over the laid Nodes is at least the target (take.lay_amplitude's rule for a child, one whole quantum, by seed.fitted's search on the pattern)."""
    high = 1
    while share_of_pattern(node, rec, masks, high)[0] < target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if share_of_pattern(node, rec, masks, middle)[0] < target:
            low = middle
        else:
            high = middle
    return high


def lay_plasma(node: Node, lay: dict[str, Any]) -> dict[str, Any]:
    rec = int(lay["row"])
    row = node.by_index[rec]
    rec = node.records().index(row)
    masks = apply_defects(pattern_masks(node, lay["pattern"], int(lay.get("sense", 1))), lay.get("flip", []), lay.get("remove", []))
    n = int(lay["quanta"])
    amplitude = fitted_pattern(node, rec, masks, n * node.units[rec])
    for sense, env in masks:
        re, im = rest_record(node, row, env, 1, amplitude, sense)
        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))
    largest, summed = share_of_pattern(node, rec, masks, amplitude)
    found = {
        "event": "plasma",
        "pattern": lay["pattern"],
        "row": int(lay["row"]),
        "quanta": n,
        "sense": int(lay.get("sense", 1)),
        "amplitude": amplitude,
        "unit": node.units[rec],
        "least share at a laid Node": largest,
        "summed share": summed,
        "nodes laid": int(sum(1 for s, e in masks for x in ints(e) if x > 0)),
        "flip": lay.get("flip", []),
        "remove": lay.get("remove", []),
    }
    node.log.append(found)
    return found


def invariance(node: Node, pattern: str) -> dict[str, int]:
    """The group's invariance of the state: the count of arrays (every line's now, before, rem, wr) equal to their image under the group's generator, over the count of arrays. uniform / pair: every array constant (the translation by one on every axis); checker: the translation by one on each axis with an im line negated; stripes4: the translation by two on x, by one on y and z, and the reflection x -> 3 - x with an im line negated."""
    lines = node.all_lines()
    im = node.is_im()
    arrays = []
    for line, is_im in zip(lines, im, strict=True):
        for a in (line.now, line.before, line.rem, line.wr):
            if a is not None:
                arrays.append((a, is_im))
    held, total = 0, 0
    held_levels, total_levels = 0, 0

    def same(a: Any, b: Any) -> bool:
        return bool(np.all(np.asarray(a, dtype=object) == np.asarray(b, dtype=object)))

    levels = [id(a) for line in lines for a in (line.now, line.before)]
    for a, is_im in arrays:
        ok = True
        if pattern in ("uniform", "pair", "sea"):
            for axis in range(AXES):
                ok = ok and same(a, np.roll(a, 1, axis=axis))
        elif pattern == "checker":
            s = -1 if is_im else 1
            for axis in range(AXES):
                ok = ok and same(np.roll(a, 1, axis=axis), s * a)
        elif pattern == "stripes4":
            s = -1 if is_im else 1
            ok = ok and same(np.roll(a, 2, axis=0), a)
            ok = ok and same(np.roll(a, 1, axis=1), a) and same(np.roll(a, 1, axis=2), a)
            ok = ok and same(np.flip(a, axis=0), s * a)
        held += 1 if ok else 0
        total += 1
        if id(a) in levels:
            held_levels += 1 if ok else 0
            total_levels += 1
    return {"held": held, "of": total, "levels held": held_levels, "of levels": total_levels}


def cube48(node: Node, pattern: str) -> dict[str, int]:
    """The 48 about the cube's centre (the Node at the centre on an odd cube, the point between Nodes on an even one): the count of the 48 under which every array of the state maps to itself (equal), to its sense-flipped image (an im line negated: the senses exchanged), or neither (apart)."""
    import itertools

    lines = node.all_lines()
    im = node.is_im()
    arrays = [(a, i) for line, i in zip(lines, im, strict=True) for a in (line.now, line.before, line.rem, line.wr) if a is not None]
    levels = [(a, i) for line, i in zip(lines, im, strict=True) for a in (line.now, line.before)]
    equal = exchanged = apart = 0
    l_equal = l_exchanged = l_apart = 0
    for perm in itertools.permutations(range(AXES)):
        for flips in itertools.product((False, True), repeat=AXES):
            all_equal = all_exchanged = True
            for a, is_im in levels:
                b = np.transpose(np.asarray(a, dtype=object), perm)
                for axis in range(AXES):
                    if flips[axis]:
                        b = np.flip(b, axis=axis)
                all_equal = all_equal and bool(np.all(b == a))
                all_exchanged = all_exchanged and bool(np.all(b == (-a if is_im else a)))
            if all_equal:
                l_equal += 1
            elif all_exchanged:
                l_exchanged += 1
            else:
                l_apart += 1
            all_equal = all_exchanged = True
            for a, is_im in arrays:
                b = np.transpose(np.asarray(a, dtype=object), perm)
                for axis in range(AXES):
                    if flips[axis]:
                        b = np.flip(b, axis=axis)
                e = bool(np.all(b == a))
                x = bool(np.all(b == (-a if is_im else a)))
                all_equal = all_equal and e
                all_exchanged = all_exchanged and x
            if all_equal:
                equal += 1
            elif all_exchanged:
                exchanged += 1
            else:
                apart += 1
    return {"equal": equal, "senses exchanged": exchanged, "apart": apart, "levels equal": l_equal, "levels exchanged": l_exchanged, "levels apart": l_apart}


def merger_premise(node: Node, c: Any, factors: tuple[Any, ...], pace: Any) -> dict[str, int]:
    """Gate 24's premise counted on every Link of every plane with a gap, from its +a end, in SL_COMPARISON's order: `whole` the Links with both ends at or above one unit of the row at the vacuum's weight; `opposite` of them with the two ends' Wronskians of opposite sign (SL-S2's selector); then the refusal the letter would give, in order: `orientation` the row's current (the two lines' link currents summed) 0; `twist` the row's twist 0 (the sum of the lines' twists); `lay` the light's plane above 0 at either end (the sea stands); `stop` the exact take short at the paying end: `stop_letter` one take of 2 u_0 from the row's re line at the current's end (the letter's one take per Node), `stop_s2` each end paying u_0 from its own re line (SL-S2); `payable` the rest. Counts over the board at the interval's end."""
    from event_universe.take import fall_of

    found = {"whole": 0, "opposite": 0, "orientation": 0, "twist": 0, "lay": 0, "stop_letter": 0, "stop_s2": 0, "payable": 0}
    gap0 = node.row(PLANE, gap=0)
    r0 = node.rule_of(gap0, c, factors)
    light = node.share(gap0.lines[0], r0, pace, vacuum=True) + node.share(gap0.lines[1], r0, pace, vacuum=True)
    u0 = node.unit_gap0
    for rec, row in enumerate(node.records()):
        if not row.gap:
            continue
        rr = node.rule_of(row, c, factors)
        re, im = row.lines
        own = node.share(re, rr, pace, vacuum=True) + node.share(im, rr, pace, vacuum=True)
        unit = node.units[rec]
        wv = wronskian(re, im)
        for axis in range(AXES):
            flow = link_current(re, 2 * axis) + link_current(im, 2 * axis)
            h = twist(re, axis) + twist(im, axis)
            own_j, w_j, light_j = across(own, 2 * axis), across(wv, 2 * axis), across(light, 2 * axis)
            for at in np.ndindex(*node.shape):
                if int(own[at]) < unit or int(own_j[at]) < unit:
                    continue
                found["whole"] += 1
                if int(wv[at]) * int(w_j[at]) >= 0:
                    continue
                found["opposite"] += 1
                if int(flow[at]) == 0:
                    found["orientation"] += 1
                    continue
                if int(h[at]) == 0:
                    found["twist"] += 1
                    continue
                j = tuple(int(x) for x in np.unravel_index(np.ravel_multi_index(at, node.shape), node.shape))
                j = list(at)
                j[axis] = (j[axis] + 1) % node.cube
                j = tuple(j)
                if int(light[at]) > 0 or int(light_j[at]) > 0:
                    found["lay"] += 1
                    continue
                into = j if int(flow[at]) > 0 else at
                levels, _fall = fall_of(node, into, 2 * u0, rr, re)
                if levels is None:
                    found["stop_letter"] += 1
                    continue
                l1, _f1 = fall_of(node, at, u0, rr, re)
                l2, _f2 = fall_of(node, j, u0, rr, re)
                if l1 is None or l2 is None:
                    found["stop_s2"] += 1
                    continue
                found["payable"] += 1
    return found


def diag(node: Node, pattern: str, every: int) -> dict[str, Any]:
    """The readings at the end of an interval."""
    x = node.row(CARRIER).lines[0].now
    xs = ints(x)
    e_max = 0
    links_sum = 0
    for axis in range(AXES):
        xj = across(x, 2 * axis)
        for a, b in zip(ints(x), ints(xj), strict=True):
            d = abs(a - b)
            e_max = max(e_max, quotient(THOUSAND * d, min(a, b)) if min(a, b) > 0 else THOUSAND * THOUSAND)
            if a > 0 and b > 0:
                links_sum += quotient(node.gamma * d * d, 3 * a * b)
    c = node.content()
    pace = readings.paces_of(node, c)[1]
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    gap0 = node.row(PLANE, gap=0)
    rule = node.rule_of(gap0, c, factors)
    sh = node.share(gap0.lines[0], rule, pace, vacuum=True) + node.share(gap0.lines[1], rule, pace, vacuum=True)
    shs = ints(sh)
    unit = node.unit_gap0
    z = gap0.lines[0]
    f_max = max(abs(v) for axis in range(AXES) for v in ints(link_current(z, 2 * axis)))
    h_max = max(abs(v) for axis in range(AXES) for v in ints(twist(z, axis)))
    mergers = merger_premise(node, c, factors, pace)
    w_tot = 0
    w_abs = 0
    w_rows = []
    for r in node.records():
        wv = ints(wronskian(*r.lines))
        w_tot += sum(wv)
        w_abs += sum(abs(v) for v in wv)
        w_rows.append(sum(wv))
    found = {
        "i": node.interval,
        "X mean/min/max": [sum(xs) // len(xs), min(xs), max(xs)],
        "e max (thousandths)": e_max,
        "links sum": links_sum,
        "turned": int(node.turned.sum()),
        "gap0 share max (units, rem)": [max(shs) // unit, max(shs) % unit],
        "nodes at one unit": sum(1 for v in shs if v >= unit),
        "F max": f_max,
        "twist max": h_max,
        "W total": w_tot,
        "W abs": w_abs,
        "W per row": w_rows,
        "mergers": mergers,
        "counts": dict(node.counts),
    }
    if every and node.interval % every == 0:
        found["invariance"] = invariance(node, pattern)
    return found


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    where = Path(argv[1])
    world = json.loads(where.read_text(encoding="utf-8"))
    universe = json.loads(where.parent.joinpath(world["universe"]).read_text(encoding="utf-8"))
    plasma = [lay for lay in world.get("seed", []) if lay.get("lay") == "plasma"]
    stripped = dict(world, seed=[lay for lay in world.get("seed", []) if lay.get("lay") != "plasma"])
    universe, stripped = read_world(stripped, universe)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    every = int(argv[argv.index("every") + 1]) if "every" in argv else 50
    node = Node(universe, stripped)
    pattern = "sea"
    laid = []
    for lay in plasma:
        laid.append(lay_plasma(node, lay))
        pattern = lay["pattern"]
        if lay.get("flip") or lay.get("remove"):
            pattern = "broken"
    print(json.dumps({"laid": laid, "pattern": pattern}), flush=True)
    intervals = int(stripped["intervals"])
    diags = [diag(node, pattern, every)]
    print(json.dumps(diags[-1]), flush=True)
    rows: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = []
    hashes: list[str] = []
    maxbits = 0
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        node.step()
        maxbits = max(maxbits, node.census()[1])
        nodes.append(run.node_lines(node))
        diags.append(diag(node, pattern, every))
        if node.interval % 10 == 0 or node.turned.any():
            print(json.dumps(diags[-1]), flush=True)
    rows.append(run.reading(node, maxbits))
    end48 = cube48(node, pattern)
    end_inv = invariance(node, pattern)
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    counts = {k: str(v) for k, v in node.counts.items()}
    n, _bits = node.census()
    merger_sums = {k: sum(d["mergers"][k] for d in diags) for k in diags[0]["mergers"]}
    summary = {
        "run back": returned,
        "mergers summed over the intervals": merger_sums,
        "counts": counts,
        "integers": n,
        "max bits": maxbits,
        "max transient bits": node.max_transient,
        "48": end48,
        "invariance at the end": end_inv,
        "turns": node.turns,
    }
    print(json.dumps(summary), flush=True)
    from event_universe.core.paces import sine_den

    record = {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": counts,
        "turns": node.turns,
        "rows": rows,
        "nodes": nodes,
        "run_back": returned,
        "log": kept_log,
    }
    with open(argv[2] + "_record.json", "w", encoding="utf-8") as out:
        json.dump(record, out)
    with open(argv[2] + "_diag.json", "w", encoding="utf-8") as out:
        json.dump({"laid": laid, "summary": summary, "diag": diags}, out)


if __name__ == "__main__":
    main(sys.argv)
