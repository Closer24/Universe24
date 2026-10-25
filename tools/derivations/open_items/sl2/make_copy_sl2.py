"""sl2's flagged COPY of src/event_universe (engine-5.0-test 88ed48d24), written by this script and never by hand, under
tools/derivations/sl2/src_sl2/event_universe. The flag is the WORLD file's key "sl2_close" (refused by the engine's loader, so no
file of David's can carry it); the key absent, every path is David's bit for bit (the state hash compared by compare_sl2.py).

  "sl2_close": "generic_sense"  the generic close WITH the list's selector (d): a row with a gap lays its list (the two gap-0
      quanta) only where the two ends' own Wronskians are of opposite sign (the conjugate pair, (num + i s)(num - i s) = den^2;
      the same sense or a neutral real line has no list), refused by name "sense" otherwise.
  "sl2_close": "generic"  the GENERIC CLOSE (the brief sl, question 2): EVERY record s is met at its own unit u_s on every Link where
      both ends' standing share of that record is at or above u_s (the gap-0 record among them, David's meeting its case); the
      taken row is the row whose quanta met; the orientation is the taken row's own current across the Link, the sum over the row's
      lines of each line's F_ij = now_i before_j - before_i now_j at the interval's start (a row of one real line the case: the
      default's light current bit for bit); the twist is the cross of the row's summed transverse currents at the two ends (PA2's
      form on the summed u); the draw is read_number at the current's end as David's; the children: for the gap-0 row David's pick
      (the lifts' pairs by the Link's number modulo u x the count of records); for a row with a gap the pair's exact list, the two
      quanta of the gap-0 row (num + i s)(num - i s) = den^2 = (den, 0)^2, one at each end; the walls per child 2 x the child's unit
      (David's booking); the take from the TAKEN row's first line at the current's end at the taken row's rule (David's take_at
      with the row as an argument); a child of the gap-0 row is laid as (A, 0, 0, 0) with A = lay_amplitude(gap0) (the double root:
      im_before = sense A sin omega_0 = 0, the case by number); every meeting of a row with a gap is logged with its numbers
      (the flow, the twist, the shares, the cause) so that the born pair's Link can be read one interval after its birth.

Every replacement must match the engine's text exactly once, else the script refuses. Run: python make_copy_sl2.py"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src", "event_universe"))
DST_ROOT = os.path.join(HERE, "src_sl2")
DST = os.path.join(DST_ROOT, "event_universe")

if os.path.isdir(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

R = {}

R["loader/world.py"] = [
    (
        'WORLD_KEYS = frozenset({"universe", "shape", "intervals", "seed"})',
        'WORLD_KEYS = frozenset({"universe", "shape", "intervals", "seed", "sl2_close"})  # sl2: the hand\'s flag key, absent in every file of David\'s',
    ),
]

R["node.py"] = [
    (
        "        self.cube, self.shape = shape[0], shape\n",
        "        self.cube, self.shape = shape[0], shape\n        self.sl2_close = world.get(\"sl2_close\")  # sl2: None is David's path bit for bit; \"generic\" the generic close\n",
    ),
]

R["take.py"] = [
    (
        "def take_at(\n    node: Node, at: tuple[int, ...], walls: int, r_gap0: rule3.Rule, cause: int\n) -> tuple[int, int, int, int] | None:",
        "def take_at(\n    node: Node, at: tuple[int, ...], walls: int, r_gap0: rule3.Rule, cause: int, rec: int | None = None\n) -> tuple[int, int, int, int] | None:",
    ),
    (
        "    gap0 = node.row(PLANE, gap=0)\n    z = gap0.lines[0]\n    levels, fall = fall_of(node, at, walls, r_gap0, z)",
        "    gap0 = node.row(PLANE, gap=0) if rec is None else node.records()[rec]  # sl2: the taken row, the gap-0 row on David's path\n    z = gap0.lines[0]\n    levels, fall = fall_of(node, at, walls, r_gap0, z)",
    ),
]

R["close.py"] = [
    (
        '    node.counts["refused_" + cause] += 1\n',
        '    node.counts["refused_" + cause] = node.counts.get("refused_" + cause, 0) + 1  # sl2: a cause the counts did not start with (sense, draw) counted alike; David\'s keys unchanged\n',
    ),
    (
        '    if direction == -1:\n        assert frame is not None\n        unclick(node, frame)\n        return\n    c = node.start_content\n',
        '    if direction == -1:\n        assert frame is not None\n        unclick(node, frame)\n        return\n    if getattr(node, "sl2_close", None) in ("generic", "generic_sense"):  # sl2: the generic close under the flag\n        click_generic(node, plane_starts, held)\n        return\n    c = node.start_content\n',
    ),
    (
        '        if entry["event"] == "birth":\n            s, amplitude = entry["line_pair"], entry["amplitude"]\n            lay(node, s, tuple(entry["minus"]), (amplitude, 0, 0, -amplitude), -1)\n            lay(node, s, tuple(entry["plus"]), (amplitude, 0, 0, amplitude), -1)\n        if entry["event"] in ("birth", "credit"):\n            lay(node, rec0, at, (entry["taken_now_was"] - int(gap0.lines[0].now[at]), 0, 0, 0))\n',
        '        if entry["event"] == "birth":\n            s, amplitude = entry["line_pair"], entry["amplitude"]\n            if "child_levels" in entry:  # sl2: a child of the gap-0 row laid as (A, 0, 0, 0) under the flag\n                lay(node, s, tuple(entry["minus"]), tuple(entry["child_levels"][0]), -1)\n                lay(node, s, tuple(entry["plus"]), tuple(entry["child_levels"][1]), -1)\n            else:\n                lay(node, s, tuple(entry["minus"]), (amplitude, 0, 0, -amplitude), -1)\n                lay(node, s, tuple(entry["plus"]), (amplitude, 0, 0, amplitude), -1)\n        if entry["event"] in ("birth", "credit"):\n            rec_t = entry.get("taken_row", rec0)  # sl2: the taken row under the flag, rec0 on David\'s path\n            z_t = node.records()[rec_t].lines[0]\n            lay(node, rec_t, at, (entry["taken_now_was"] - int(z_t.now[at]), 0, 0, 0))\n',
    ),
]

GENERIC = '''

# ---- sl2: the generic close (the brief sl, 2026-10-25), under the world file's flag "sl2_close": "generic" alone ----

BirthG = tuple[tuple[int, ...], int, tuple[int, ...], tuple[int, ...], int, int]  # ..., the taken row
from event_universe.links import wronskian  # sl2: the row's own Wronskian at the two ends, the sense (d)


def row_current(lines: list[Line], port: int) -> Any:
    """sl2: a row's own current across the Link at the Port, the sum over its lines of each line's F_ij (one act on every line alike; a row of one real line the default's current bit for bit)."""
    found = 0
    for line in lines:
        found = found + link_current(line, port)
    return found


def row_twist(lines: list[Line], axis: int) -> Any:
    """sl2: the twist of a row's transverse currents along the +axis Link (PA2's form on the row's summed u_b), u_b(k) = SUM over the row's lines of F(k, k - b) - F(k, k + b)."""
    from event_universe.core.ports import across, wrap
    from event_universe.links import net_current

    a, b, c = axis, wrap(axis + 1, AXES), wrap(axis + 2, AXES)
    ub = 0
    uc = 0
    for line in lines:
        ub = ub + net_current(line, b)
        uc = uc + net_current(line, c)
    return cross(ub, uc, across(ub, 2 * a), across(uc, 2 * a))


def meet_row(
    node: Node,
    s: int,
    lines_start: list[Line],
    sh: Any,
    unit: int,
    rules: list[tuple[Line, rule3.Rule]],
    frozen: Any,
    gap0_index: int,
    owns: list[Any],
) -> list[BirthG]:
    """sl2: David's `meet` for the record s at its own unit: both ends at or above u_s, the orientation by the row's own current, the twist by the row's summed transverse currents, the draw at the current's end, the children by the taken pair's list (David's pick for the gap-0 row; the two gap-0 quanta for a row with a gap); every meeting of a row with a gap logged with its numbers."""
    born: list[BirthG] = []
    currents = [node.den * row_current(lines_start, 2 * axis) for axis in range(AXES)]
    twists = [row_twist(lines_start, axis) for axis in range(AXES)]
    gapped = s != gap0_index
    sense_rule = getattr(node, "sl2_close", None) == "generic_sense"  # sl2: (d) the list's selector, the two ends' senses opposite
    wr = wronskian(lines_start[0], lines_start[1]) if len(lines_start) == 2 else np.zeros(node.shape, dtype=object)
    for at in np.ndindex(*node.shape):
        if frozen[at]:
            continue
        for axis in range(AXES):
            j = neighbour(node, at, 2 * axis)
            if frozen[j] or int(sh[at]) < unit or int(sh[j]) < unit:
                continue
            flow = int(currents[axis][at])
            h = int(twists[axis][at])
            w_ends = [int(wr[at]), int(wr[j])]
            if gapped:
                node.counts["met_gapped"] = node.counts.get("met_gapped", 0) + 1
                node.log.append(
                    {
                        "event": "meeting",
                        "i": node.interval,
                        "node": list(at),
                        "link": list(j),
                        "row": s,
                        "flow": flow,
                        "twist": h,
                        "shares": [int(sh[at]), int(sh[j])],
                        "unit": unit,
                        "light_shares": [int(owns[gap0_index][at]), int(owns[gap0_index][j])],
                        "W_ends": w_ends,
                    }
                )
            if gapped and sense_rule and w_ends[0] * w_ends[1] >= 0:
                refused(node, at, "sense", link=list(j), row=s, W_ends=w_ends)
                continue
            if flow == 0:
                refused(node, at, "orientation", link=list(j), row=s)
                continue
            into, outof = (j, at) if flow > 0 else (at, j)
            if h == 0:
                refused(node, at, "twist", link=list(j), row=s)
                continue
            plus, minus = (into, outof) if h > 0 else (outof, into)
            drawn = read_number(node, into, rules)
            if drawn is None:
                if gapped:
                    refused(node, at, "draw", link=list(j), row=s)
                continue
            number, room = drawn
            child = gap0_index if gapped else remainder(quotient(number, unit), len(node.records()))
            born.append((into, child, minus, plus, room, s))
    return born


def refuse_g(node: Node, born: list[BirthG], owns: list[Any]) -> list[BirthG]:
    """sl2: David's `refuse` with the taken row carried."""
    kept = []
    for at, s, minus, plus, room, taken in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:
            refused(node, at, "lay", standing=int(owns[s][minus]), unit=node.units[s], row=taken)
            continue
        kept.append((at, s, minus, plus, room, taken))
    landing: dict[tuple[int, tuple[int, ...]], int] = {}
    for _at, s, minus, plus, _room, _t in kept:
        landing[(s, minus)] = landing.get((s, minus), 0) + 1
        landing[(s, plus)] = landing.get((s, plus), 0) + 1
    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
    for at, s, minus, plus, _room, taken in crowded:
        refused(node, at, "lay", children_at_one_node=max(landing[(s, minus)], landing[(s, plus)]), row=taken)
    return [k for k in kept if k not in crowded]


def child_levels_of(node: Node, s: int, amplitude: int, sense: int) -> tuple[int, int, int, int]:
    """sl2: a child's four levels: the quarter turn (A, 0, 0, sense A) for a row with a gap (David's), (A, 0, 0, 0) for the gap-0 row (the double root's sine 0: sense A sin omega_0 = 0, the case by number)."""
    row = node.records()[s]
    if row.gap == 0:
        return (amplitude, 0, 0, 0)
    return (amplitude, 0, 0, sense * amplitude)


def births_g(
    node: Node,
    kept: list[BirthG],
    rules_of: list[rule3.Rule],
    c: Any,
    factors: tuple[Any, ...],
    pace: Any,
) -> set[tuple[int, ...]]:
    """sl2: David's `births` with the take from the taken row's first line at its rule, grouped by (Node, taken row); the children laid by `child_levels_of`; a birth whose taken row has a gap is a merger (two gap-0 quanta from a pair), logged as a birth line with taken_row and merger."""
    by_key: dict[tuple[tuple[int, ...], int], list[tuple[int, tuple[int, ...], tuple[int, ...], int]]] = {}
    for at, s, minus, plus, room, taken in kept:
        by_key.setdefault((at, taken), []).append((s, minus, plus, room))
    touched: set[tuple[int, ...]] = set()
    for at, taken in sorted(by_key):
        kids = by_key[(at, taken)]
        walls = sum(2 * node.units[s] for s, _m, _p, _r in kids)
        got = take_at(node, at, walls, rules_of[taken], len(kids), rec=taken)
        if got is None:
            if taken != node.records().index(node.row(PLANE, gap=0)):
                node.counts["merger_stop"] = node.counts.get("merger_stop", 0) + len(kids)
            continue
        levels, fall, now, before = got
        node.closes[at] -= 1
        dp_take = node.last_dp
        touched.add(at)
        for s, minus, plus, room in kids:
            amplitude = lay_amplitude(node, s, at, c, factors, pace)
            row = node.records()[s]
            re, im = row.lines
            assert row.pair is not None
            dp_lay = [0, 0, 0]
            lv = []
            for where, sense in ((minus, -1), (plus, 1)):
                four = child_levels_of(node, s, amplitude, sense)
                lv.append(list(four))
                for a, d in enumerate(momentum_of(node, re.now, re.before, where, d_now=four[0], num=row.pair[0])):
                    dp_lay[a] += d
                for a, d in enumerate(momentum_of(node, im.now, im.before, where, d_before=four[3], num=row.pair[0])):
                    dp_lay[a] += d
                lay(node, s, where, four)
            w_children = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
            touched |= {minus, plus}
            merger = taken != node.records().index(node.row(PLANE, gap=0))
            node.counts["births"] += 1
            if merger:
                node.counts["mergers"] = node.counts.get("mergers", 0) + 1
            node.closes[at] += 1
            node.log.append(
                {
                    "event": "birth",
                    "i": node.interval,
                    "node": list(at),
                    "line_pair": s,
                    "senses": [-1, 1],
                    "W_children": w_children,
                    "minus": list(minus),
                    "plus": list(plus),
                    "taken": fall,
                    "booked": walls,
                    "levels": levels,
                    "taken_now_was": now,
                    "taker": [now, before, levels],
                    "proper": int(node.proper[at]),
                    "content": int(c[at]),
                    "amplitude": amplitude,
                    "children_at_node": len(kids),
                    "room": room,
                    "dP_take": dp_take,
                    "dP_lay": dp_lay,
                    "taken_row": taken,
                    "merger": merger,
                    "child_levels": lv,
                }
            )
        node.counts["taken"] += fall
        node.counts["booked"] += walls
    return touched


def click_generic(node: Node, plane_starts: list[list[Line]], held: list[list[Line]]) -> None:
    """sl2: the generic close: the readings at the start as David's; every record met at its own unit (`meet_row`), the lays refused by name (`refuse_g`), the births and mergers taken and laid (`births_g`), the bodies' closing David's."""
    c = node.start_content
    pace = readings.paces_of(node, c)[1]
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    gap0 = node.row(PLANE, gap=0)
    gap0_index = node.records().index(gap0)
    r_gap0 = node.rule_of(gap0, c, factors)
    rules = node.read_lines(held, plane_starts, c, factors)
    owns = []
    rules_of = []
    for rec, r in enumerate(node.records()):
        rr = node.rule_of(r, c, factors)
        rules_of.append(rr)
        re0, im0 = plane_starts[rec]
        owns.append(node.share(re0, rr, pace, vacuum=True) + node.share(im0, rr, pace, vacuum=True))
    born: list[BirthG] = []
    for rec in range(len(node.records())):
        born += meet_row(node, rec, plane_starts[rec], owns[rec], node.units[rec], rules, frozen, gap0_index, owns)
    born_nodes = births_g(node, refuse_g(node, born, owns), rules_of, c, factors, pace)
    bodies(node, plane_starts, owns, born_nodes, frozen, r_gap0)
'''

for name, pairs in R.items():
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            sys.exit(f"REFUSED: {name}: the text matches {n} times, not once:\n{old[:200]}")
        text = text.replace(old, new)
    if name == "close.py":
        text = text + GENERIC
    open(path, "w", encoding="utf-8").write(text)
    print(f"{name}: {len(pairs)} replacements" + (" + the generic close appended" if name == "close.py" else ""))
print("the copy stands under", DST)
