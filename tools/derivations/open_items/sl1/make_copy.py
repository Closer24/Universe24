"""sl1's flagged COPY of the engine (engine-5.0-test 88ed48d24): src/event_universe copied bit for bit to src_sl1/event_universe, then close.py and take.py changed by the named replacements below, every one asserted to match the text exactly once. The flag is the environment variable SL1_CLOSE=generic; with the flag absent every act is David's path bit for bit (close.click calls the same functions with the same arguments; take_at's new argument defaults to the gap-0 row).

The generic close (the brief sl, question (2)): every record's whole quanta meeting at a Link are taken by one act, meet_generic, called once per record: both ends at or above the record's own unit at the vacuum's weight; the orientation from the taken row's own current (num x cross of its first line at the two ends); the twist from the taken row's first line; the one-Link read composed modulo the taken row's unit times the count of records; the children from the taken pair's list (list_of): the lifts drawn by the number for the pair at the gap 0 (David's), and for a pair with a gap the Gaussian product (num + i s)(num - i s) = den^2 = (den + 0 i)^2, the two quanta of the pair (den, den), the record found by its pair; the take from the taken row's first line at its own rule (take_at(..., rec)); the lay refused by name as before; the run back restores the taken row's line. A probe (no act) logs, at every close after a birth, the born pair's Link for up to 12 intervals: the two ends' standing share in the child's unit (quotient, remainder), the first and second lines' currents across the Link, the twist, the gap-0 standing at the ends, and the fall the taken row's line could pay at each end against the walls of two light quanta.

Run: python make_copy.py (writes src_sl1/ beside it)."""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src", "event_universe"))
DST_PKG = os.path.join(HERE, "src_sl1")
DST = os.path.join(DST_PKG, "event_universe")

if os.path.isdir(DST_PKG):
    shutil.rmtree(DST_PKG)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, pairs):
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            print("REFUSED: the text matches %d times, not once, in %s:\n%s" % (n, path, old[:200]))
            sys.exit(1)
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)


# ---------------- take.py: the take from a named record's first line (default the gap-0 row: bit for bit)
take_pairs = [
    (
        'def take_at(\n    node: Node, at: tuple[int, ...], walls: int, r_gap0: rule3.Rule, cause: int\n) -> tuple[int, int, int, int] | None:',
        'def take_at(\n    node: Node, at: tuple[int, ...], walls: int, r_gap0: rule3.Rule, cause: int, rec: int | None = None\n) -> tuple[int, int, int, int] | None:',
    ),
    (
        '    gap0 = node.row(PLANE, gap=0)\n    z = gap0.lines[0]\n    levels, fall = fall_of(node, at, walls, r_gap0, z)',
        '    gap0 = node.row(PLANE, gap=0) if rec is None else node.records()[rec]  # sl1: the taken row\'s line (the gap-0 row where no record is named: David\'s path bit for bit)\n    z = gap0.lines[0]\n    levels, fall = fall_of(node, at, walls, r_gap0, z)',
    ),
]
replace_once(os.path.join(DST, "take.py"), take_pairs)

# ---------------- close.py: the generic close behind the flag
close_pairs = []

close_pairs.append(
    (
        'from __future__ import annotations\n\nfrom typing import TYPE_CHECKING, Any\n\nimport numpy as np\n',
        'from __future__ import annotations\n\nimport os\nfrom typing import TYPE_CHECKING, Any\n\nimport numpy as np\n\nSL1_GENERIC = os.environ.get("SL1_CLOSE") == "generic"  # sl1\'s flag: the generic close; absent, David\'s path bit for bit\nSL1_PROBE_SPAN = 12  # the born pair\'s Link probed for this many closes after its birth (a reading, no act)\n',
    )
)

close_pairs.append(
    (
        'from event_universe.core.rule3 import quotient, remainder\n',
        'from event_universe.core.paces import sine_den\nfrom event_universe.core.rule3 import quotient, remainder\n',
    )
)

close_pairs.append(
    (
        'from event_universe.take import (\n    frame_nodes,\n    lay,\n',
        'from event_universe.take import (\n    fall_of,\n    frame_nodes,\n    lay,\n',
    )
)

# the generic functions, inserted before `def bodies(`
generic_code = '''
# ---------------------------------------------------------------- sl1: the generic close (SL1_CLOSE=generic)

GBirth = tuple[tuple[int, ...], int, tuple[int, ...], tuple[int, ...], int, int]  # (the take's Node, the child's record, the - child's Node, the + child's Node, the room, the taken record)


def list_of(node: Node, rec: int, number: int) -> int:
    """The taken pair's list, one child record (a conjugate pair at the senses -1 and 1): for the pair at the gap 0 the lifts' draw by the Link's number modulo the taken unit times the count of records (David's path); for a pair with a gap the Gaussian product (num + i s)(num - i s) = num^2 + s^2 = den^2 = (den + 0 i)^2, two quanta of the pair (den, den), the record found by that pair alone."""
    row = node.records()[rec]
    assert row.pair is not None
    num, den = row.pair
    if row.gap == 0:
        return remainder(quotient(number, node.units[rec]), len(node.records()))
    s = sine_den(num, den)
    product = (num * num + s * s, 0)  # the Gaussian product's (re, im), re = den^2 exactly where the pair is a point of den's circle
    assert product == (den * den, 0), product
    pair = (den, den)  # (den + 0 i) twice: the massless pair
    return next(k for k, r in enumerate(node.records()) if r.pair == pair)


def refused_rec(node: Node, at: tuple[int, ...], cause: str, rec: int, **numbers: Any) -> None:
    """A refusal by name at a meeting of the record rec, counted per cause and per taken record; the log holds the gap-0 row's refusals as David's path does and the first 4,000 of a gapped row's."""
    node.counts["refused_" + cause] += 1
    key = "sl1_refused_%s_rec%d" % (cause, rec)
    node.counts[key] = node.counts.get(key, 0) + 1
    if node.records()[rec].gap == 0 or node.counts[key] <= 4000:
        node.log.append(
            {"event": "refused", "i": node.interval, "node": list(at), "cause": cause, "taken_row": rec, **numbers}
        )


def meet_generic(
    node: Node, rec: int, taken: Line, sh: Any, rules: list[tuple[Line, rule3.Rule]], frozen: Any
) -> list[GBirth]:
    """The Link close of one record, the same act for every record: every Link once from its +a end, a meeting where both ends hold a whole quantum of the record at the vacuum's weight and neither end is frozen; the + child at the end the record's own current flows into where the twist of its first line's transverse currents is right-handed; the one number read at the current's end composed modulo the record's unit times the count of records; the children the pair's list (list_of)."""
    born: list[GBirth] = []
    row = node.records()[rec]
    assert row.pair is not None
    num = row.pair[0]
    unit = node.units[rec]
    currents = [num * link_current(taken, 2 * axis) for axis in range(AXES)]
    twists = [twist(taken, axis) for axis in range(AXES)]
    modulus = unit * len(node.records())
    for at in np.ndindex(*node.shape):
        if frozen[at]:
            continue
        for axis in range(AXES):
            j = neighbour(node, at, 2 * axis)
            if frozen[j] or int(sh[at]) < unit or int(sh[j]) < unit:
                continue
            key = "sl1_met_rec%d" % rec
            node.counts[key] = node.counts.get(key, 0) + 1
            flow = int(currents[axis][at])
            if flow == 0:
                refused_rec(node, at, "orientation", rec, link=list(j))
                continue
            into, outof = (j, at) if flow > 0 else (at, j)
            h = int(twists[axis][at])
            if h == 0:
                refused_rec(node, at, "twist", rec, link=list(j))
                continue
            plus, minus = (into, outof) if h > 0 else (outof, into)
            drawn = read_number_modulo(node, into, rules, modulus)
            if drawn is None:
                key = "sl1_refused_read_rec%d" % rec
                node.counts[key] = node.counts.get(key, 0) + 1
                continue
            number, room = drawn
            born.append((into, list_of(node, rec, number), minus, plus, room, rec))
    return born


def read_number_modulo(
    node: Node, at: tuple[int, ...], rules: list[tuple[Line, rule3.Rule]], modulus: int
) -> tuple[int, int] | None:
    """read_number with the modulus the taken row's unit times the count of records (David's modulus where the taken row is the gap-0 row)."""
    nodes = frame_nodes(node, at)
    digits = []
    origin = coarse = True
    w_half = half(node.w)
    for line, r in rules:
        f0 = lattice(at_node(line.wall, at), at_node(r.mass, at), *[at_node(x, at) for x in r.reaches])
        for k, n in enumerate(nodes):
            wl = at_node(line.wall, n)
            f = f0 if k == 0 else lattice(wl, at_node(r.reaches[k - 1], n))
            rem, values = node.digit_of(int(line.rem[n]), quotient(wl, f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
            coarse = coarse and values <= AXES
            digits.append((quotient(rem, f), values + 1))
    if origin:
        node.counts["refused_origin"] += 1
        return None
    if coarse:
        return None
    digits.sort()
    carry, room = 0, 1
    for d, b in digits:
        carry = remainder(carry * b + d, modulus)
        room = min(room * b, modulus)
    return carry, room


def refuse_generic(node: Node, born: list[GBirth], owns: list[Any]) -> list[GBirth]:
    """refuse, with the taken record carried."""
    kept = []
    for at, s, minus, plus, room, rec in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:
            refused_rec(node, at, "lay", rec, standing=int(owns[s][minus]), unit=node.units[s], child=s)
            continue
        kept.append((at, s, minus, plus, room, rec))
    landing: dict[tuple[int, tuple[int, ...]], int] = {}
    for _at, s, minus, plus, _room, _rec in kept:
        landing[(s, minus)] = landing.get((s, minus), 0) + 1
        landing[(s, plus)] = landing.get((s, plus), 0) + 1
    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
    for at, s, minus, plus, _room, rec in crowded:
        refused_rec(node, at, "lay", rec, children_at_one_node=max(landing[(s, minus)], landing[(s, plus)]))
    return [k for k in kept if k not in crowded]


def births_generic(
    node: Node, kept: list[GBirth], rules_of: dict[int, rule3.Rule], c: Any, factors: tuple[Any, ...], pace: Any
) -> set[tuple[int, ...]]:
    """births, the take from the taken record's first line at its own rule, one take per (Node, taken record)."""
    by_node: dict[tuple[tuple[int, ...], int], list[tuple[int, tuple[int, ...], tuple[int, ...], int]]] = {}
    for at, s, minus, plus, room, rec in kept:
        by_node.setdefault((at, rec), []).append((s, minus, plus, room))
    taken = []
    for at, rec in sorted(by_node):
        kids = by_node[(at, rec)]
        walls = sum(2 * node.units[s] for s, _m, _p, _r in kids)
        got = take_at(node, at, walls, rules_of[rec], len(kids), rec)
        if got is None:
            key = "sl1_refused_stop_rec%d" % rec
            node.counts[key] = node.counts.get(key, 0) + 1
            node.log[-1]["taken_row"] = rec
        else:
            taken.append((at, rec, kids, walls, got))
    touched: set[tuple[int, ...]] = set()
    for at, rec, kids, walls, (levels, fall, now, before) in taken:
        node.closes[at] -= 1
        touched |= children(node, at, kids, (walls, levels, fall, now, before), c, factors, pace)
        for k in range(len(kids)):
            node.log[-1 - k]["taken_row"] = rec
        key = "sl1_taken_rec%d" % rec
        node.counts[key] = node.counts.get(key, 0) + len(kids)
        node.counts["taken"] += fall
        node.counts["booked"] += walls
    return touched


def probe_born_links(
    node: Node, plane_starts: list[list[Line]], owns: list[Any], rules_of: dict[int, rule3.Rule]
) -> None:
    """A reading and no act: for every birth within SL1_PROBE_SPAN closes before this one, the born pair's Link read as the generic close would read it: the two ends' standing share in the child's unit, the currents of its two lines across the Link (num x cross), the twist, the gap-0 row's standing at the ends, the walls of two light quanta and the fall each end's line could pay (fall_of at the full move), and the Link's current of the gap-0 row."""
    gap0 = node.row(PLANE, gap=0)
    rec0 = node.records().index(gap0)
    for entry in [e for e in node.log if e["event"] == "birth" and 0 < node.interval - e["i"] <= SL1_PROBE_SPAN]:
        s = entry["line_pair"]
        minus, plus = tuple(entry["minus"]), tuple(entry["plus"])
        axis = next(a for a in range(AXES) if minus[a] != plus[a])
        at = minus if neighbour(node, minus, 2 * axis) == plus else plus
        j = neighbour(node, at, 2 * axis)
        re0, im0 = plane_starts[s]
        row = node.records()[s]
        assert row.pair is not None
        num = row.pair[0]
        unit = node.units[s]
        f_re = num * int(link_current(re0, 2 * axis)[at])
        f_im = num * int(link_current(im0, 2 * axis)[at])
        h = int(twist(re0, axis)[at])
        walls = 2 * node.units[rec0]
        falls = []
        for end in (at, j):
            levels, full = fall_of(node, end, walls, rules_of[s], row.lines[0])
            falls.append([None if levels is None else int(levels), int(full)])
        node.log.append(
            {
                "event": "sl1_probe",
                "i": node.interval,
                "birth_i": entry["i"],
                "node": list(at),
                "link": list(j),
                "line_pair": s,
                "unit": unit,
                "standing": [[int(owns[s][at]) // unit, int(owns[s][at]) % unit], [int(owns[s][j]) // unit, int(owns[s][j]) % unit]],
                "whole_both_ends": int(int(owns[s][at]) >= unit and int(owns[s][j]) >= unit),
                "F_re": f_re,
                "F_im": f_im,
                "twist": h,
                "gap0_standing": [int(owns[rec0][at]), int(owns[rec0][j])],
                "walls_two_light": walls,
                "falls": falls,
                "F_gap0": node.den * int(link_current(plane_starts[rec0][0], 2 * axis)[at]),
            }
        )


def click_generic(node: Node, plane_starts: list[list[Line]], held: list[list[Line]]) -> None:
    """The close with the generic Link close: every record met by the one act, the births taken from the taken rows' lines, the bodies' closing as before (W-S2's payer kept by name), the probe."""
    c = node.start_content
    pace = readings.paces_of(node, c)[1]
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    gap0 = node.row(PLANE, gap=0)
    r_gap0 = node.rule_of(gap0, c, factors)
    rules = node.read_lines(held, plane_starts, c, factors)
    owns = []
    rules_of: dict[int, rule3.Rule] = {}
    for rec, r in enumerate(node.records()):
        rr = node.rule_of(r, c, factors)
        rules_of[rec] = rr
        re0, im0 = plane_starts[rec]
        owns.append(node.share(re0, rr, pace, vacuum=True) + node.share(im0, rr, pace, vacuum=True))
    born: list[GBirth] = []
    for rec in range(len(node.records())):
        born += meet_generic(node, rec, plane_starts[rec][0], owns[rec], rules, frozen)
    probe_born_links(node, plane_starts, owns, rules_of)
    born_nodes = births_generic(node, refuse_generic(node, born, owns), rules_of, c, factors, pace)
    bodies(node, plane_starts, owns, born_nodes, frozen, r_gap0)


'''

close_pairs.append(("\ndef bodies(\n", generic_code + "\ndef bodies(\n"))

# the click under the flag
close_pairs.append(
    (
        '    if direction == -1:\n        assert frame is not None\n        unclick(node, frame)\n        return\n    c = node.start_content\n',
        '    if direction == -1:\n        assert frame is not None\n        unclick(node, frame)\n        return\n    if SL1_GENERIC:\n        click_generic(node, plane_starts, held)\n        return\n    c = node.start_content\n',
    )
)

# unclick restores the taken row's line
close_pairs.append(
    (
        '        if entry["event"] in ("birth", "credit"):\n            lay(node, rec0, at, (entry["taken_now_was"] - int(gap0.lines[0].now[at]), 0, 0, 0))\n',
        '        if entry["event"] in ("birth", "credit"):\n            taken_row = entry.get("taken_row", rec0)  # sl1: the taken row\'s line restored (the gap-0 row where none is named)\n            lay(node, taken_row, at, (entry["taken_now_was"] - int(node.records()[taken_row].lines[0].now[at]), 0, 0, 0))\n',
    )
)

# the imports the generic code needs (lattice, mirrored, half, at_node)
close_pairs.append(
    (
        'from event_universe.take import (\n    fall_of,\n    frame_nodes,\n    lay,\n    lay_amplitude,\n    momentum_of,\n    neighbour,\n    read_number,\n    take_at,\n)\n',
        'from event_universe.core.rule3 import half, lattice, mirrored\nfrom event_universe.take import (\n    at_node,\n    fall_of,\n    frame_nodes,\n    lay,\n    lay_amplitude,\n    momentum_of,\n    neighbour,\n    read_number,\n    take_at,\n)\n',
    )
)

replace_once(os.path.join(DST, "close.py"), close_pairs)
print("the copy written under", DST)
print("replacements: take.py %d, close.py %d" % (len(take_pairs), len(close_pairs)))
