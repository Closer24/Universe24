"""The close, the Node's fourth act (ALGEBRA.md, The click writes on the lattice): the readings at the start (every row's rule, the gap-0 plane's share and each record's standing share at the vacuum's weight, the frozen Nodes), the Link close (`meet`: every Link once from its +a end, both ends holding a whole quantum of the record, the + child at the end the record's current flows into where the twist is right-handed, the conjugate pair's selector for a record with a gap, the one-Link read of a number at that end), the lays refused by name (`refuse`), the births taken and laid (`births`: the birth's one take per Node from the gap-0 row, the merger's one take per end from the taken row, SL-S2), the bodies' closing (bodies.py); the lay, the exact take and the momentum they book; the close undone from the log (`unclick`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram, readings
from event_universe.bodies import bodies
from event_universe.core import rule3
from event_universe.core.ports import AXES, across
from event_universe.core.rule3 import quotient, remainder
from event_universe.links import cross, row_current, row_twist
from event_universe.rows import PLANE, Line
from event_universe.take import fall_of, lay, momentum_of, neighbour, read_number, take_at

if TYPE_CHECKING:
    from event_universe.node import Node

Birth = tuple[tuple[int, ...], int, tuple[int, ...], tuple[int, ...], int, int]
Kid = tuple[int, tuple[int, ...], tuple[int, ...], int]


def refused(node: Node, at: tuple[int, ...], cause: str, **numbers: Any) -> None:
    """A refusal by name, counted and logged."""
    node.counts["refused_" + cause] += 1
    node.log.append(
        {"event": "refused", "i": node.interval, "node": list(at), "cause": cause, **numbers}
    )


def list_of(node: Node, rec: int, number: int) -> int:
    """The children's record of a meeting of the record `rec` by the pairs: where the taken row is the emitter the draw's pick among the planes (the number over the unit, modulo their count); where it is another record, the row whose pair is the product (den, den), the emitter (SL-S1: two gapped quanta meeting give light)."""
    records = node.records()
    if records[rec] is not node.emitter():
        return records.index(node.emitter())
    planes = [k for k, r in enumerate(records) if r.shape == PLANE]
    return planes[int(remainder(quotient(number, node.units[rec]), len(planes)))]


def meet(
    node: Node, rec: int, start: list[Line], sh: Any, rules: list[tuple[Line, rule3.Rule]], frozen: Any
) -> list[Birth]:
    """The Link close of one record, the same for every record (SL-S1, the generic close): every Link once from its +a end; a meeting where both ends hold a whole quantum of the record at the interval's start and neither end is frozen (counted as `met`); the + child at the end the record's own current flows into where the twist of its transverse currents is right-handed, at the other end where left-handed (F = 0 and h = 0 refused by name); a record with a gap meets as the conjugate pair alone, the two ends' charges of opposite sign (SL-S2's selector with no name, W_minus W_plus < 0; refused by name `sense` where not); the Link's one number read at the current's end names the children's record (`list_of`). Returns the births as (the take's Node, the children's record, the - child's Node, the + child's Node, the draw's room, the taken record)."""
    born: list[Birth] = []
    row, unit = node.records()[rec], node.units[rec]
    standing = np.vectorize(lambda v: int(v) >= unit, otypes=[bool])(sh) & ~frozen
    currents = [node.den * row_current(start, 2 * axis) for axis in range(AXES)]
    twists = [row_twist(start, axis) for axis in range(AXES)]
    charges = gram.charge(row.shape, start) if row is not node.emitter() else None
    for axis in range(AXES):
        both = standing & across(standing, 2 * axis)
        for where in zip(*np.nonzero(both), strict=True):
            at = tuple(int(x) for x in where)
            j = neighbour(node, at, 2 * axis)
            node.counts["met"] += 1
            flow = int(currents[axis][at])
            if flow == 0:
                refused(node, at, "orientation", link=list(j), row=rec)
                continue
            into, outof = (j, at) if flow > 0 else (at, j)
            h = int(twists[axis][at])
            if h == 0:
                refused(node, at, "twist", link=list(j), row=rec)
                continue
            if charges is not None and int(charges[at]) * int(charges[j]) >= 0:
                w = [int(charges[at]), int(charges[j])]
                refused(node, at, "sense", link=list(j), row=rec, charges=w)
                continue
            plus, minus = (into, outof) if h > 0 else (outof, into)
            drawn = read_number(node, into, rules, unit)
            if drawn is None:
                continue
            number, room = drawn
            born.append((into, list_of(node, rec, number), minus, plus, room, rec))
    return born


def refuse(node: Node, born: list[Birth], owns: list[Any]) -> list[Birth]:
    """The lay refused by name: where any of the child's plane already stands at its Node, and where two children of one plane would land at one Node in one close (the charge made at a crowded lay). Returns the births kept."""
    kept = []
    for at, s, minus, plus, room, rec in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:
            refused(node, at, "lay", standing=int(owns[s][minus]), unit=node.units[s], row=rec)
            continue
        kept.append((at, s, minus, plus, room, rec))
    landing: dict[tuple[int, tuple[int, ...]], int] = {}
    for _at, s, minus, plus, _room, _rec in kept:
        landing[(s, minus)] = landing.get((s, minus), 0) + 1
        landing[(s, plus)] = landing.get((s, plus), 0) + 1
    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
    for at, s, minus, plus, _room, rec in crowded:
        refused(
            node, at, "lay", children_at_one_node=max(landing[(s, minus)], landing[(s, plus)]), row=rec
        )
    return [k for k in kept if k not in crowded]


def births(node: Node, kept: list[Birth], c: Any, factors: tuple[Any, ...]) -> set[tuple[int, ...]]:
    """The births kept, every face read before any write: every child's wall first (`walls_of`, MS-S1: what is taken is what the lay books and nothing made), then the takes by the taken pair's case, the taken row's line by the fall's sign paying at its rule (take.fall_of's choice, CS4-S2; the former first line kept by name): at the gap 0 one exact take per Node and taken record of its children's walls summed (the birth's case, kept by name); with a gap each child's wall paid by one exact take at its own end (`merger_take`, SL-S2: the birth read at -1); then each child laid at the charge T div 2 (`children`). Returns every Node a taken birth touched."""
    by_node: dict[tuple[tuple[int, ...], int], list[Kid]] = {}
    for at, s, minus, plus, room, rec in kept:
        by_node.setdefault((at, rec), []).append((s, minus, plus, room))
    walls = {k: walls_of(node, k[1], k[2], k[3], c, factors) for k in kept}
    taken: list[tuple[tuple[int, ...], int, list[Kid], dict[str, Any]]] = []
    for at, rec in sorted(by_node):
        kids = by_node[(at, rec)]
        row = node.records()[rec]
        assert row.pair is not None
        rule = node.rule(row.pair, c, factors)
        if row is not node.emitter():
            for kid in kids:
                got = merger_take(node, kid[1], kid[2], walls[(at, *kid, rec)], rule, rec)
                if got is not None:
                    taken.append((at, rec, [kid], got))
            continue
        booked = sum(sum(walls[(at, *kid, rec)]) for kid in kids)
        one = take_at(node, at, booked, rule, len(kids), rec)
        if one is None:
            continue
        levels, fall, now, before, k = one
        node.closes[at] -= 1
        take = take_line(fall, booked, levels, now, before, node.last_dp, k)
        taken.append((at, rec, kids, take))
    touched: set[tuple[int, ...]] = set()
    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec)
        node.counts["taken"] += take["taken"]
        node.counts["booked"] += take["booked"]
    return touched


def take_line(
    fall: int, booked: int, levels: int, now: int, before: int, dp: list[int], line: int
) -> dict[str, Any]:
    """One take's numbers as the log carries them: the fall taken, the walls booked, the levels moved, the line's now before the take, the taker's three levels, the take's momentum and the line taken (`taken_line`, logged per take: CS4-S2, unclick restoring that line)."""
    return {
        "taken": fall,
        "booked": booked,
        "levels": levels,
        "taken_now_was": now,
        "taker": [now, before, levels],
        "dP_take": dp,
        "taken_line": line,
    }


def merger_take(
    node: Node,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    walls: tuple[int, int],
    rule: rule3.Rule,
    rec: int,
) -> dict[str, Any] | None:
    """The merger's take (SL-S2, the birth's lay read at -1): each child's wall paid by one exact take at its own end from the taken row's line by the fall's sign at that end (take.fall_of's choice, CS4-S2) at its rule, both ends read (`fall_of`) before either is written; refused by name `stop` where an end cannot pay. Returns the log's take fields, the two ends' takes summed and each end's own under `takes`, or None."""
    row = node.records()[rec]
    for where, wall in zip((minus, plus), walls, strict=True):
        levels, fall, _line = fall_of(node, where, wall, rule, row)
        if levels is None:
            refused(node, where, "stop", fall=fall, walls=wall, row=rec)
            return None
    takes: list[dict[str, Any]] = []
    for where, wall in zip((minus, plus), walls, strict=True):
        got = take_at(node, where, wall, rule, 1, rec)
        assert got is not None
        levels, fall, now, before, k = got
        node.closes[where] -= 1
        takes.append(
            {"node": list(where), **take_line(fall, wall, levels, now, before, node.last_dp, k)}
        )
    return {
        "taken": takes[0]["taken"] + takes[1]["taken"],
        "booked": takes[0]["booked"] + takes[1]["booked"],
        "levels": takes[0]["levels"] + takes[1]["levels"],
        "taken_now_was": [t["taken_now_was"] for t in takes],
        "taker": [t["taker"] for t in takes],
        "dP_take": [a + b for a, b in zip(takes[0]["dP_take"], takes[1]["dP_take"], strict=True)],
        "taken_line": [t["taken_line"] for t in takes],
        "takes": takes,
    }


def walls_of(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> tuple[int, int]:
    """Each child's wall (MS-S1): the share its lay adds to its plane on the board in the carrier's unit, read by laying the - child, then the + child, reading after each and taking both back; the birth's walls their sum."""
    row = node.records()[s]
    assert row.pair is not None
    rule = node.rule(row.pair, c, factors)

    def total() -> int:
        return int(sum(int(x) for x in node.share(row.lines, rule).reshape(-1)))

    before = total()
    child_at(node, s, minus, -1)
    middle = total()
    child_at(node, s, plus, 1)
    after = total()
    child_at(node, s, plus, 1, -1)
    child_at(node, s, minus, -1, -1)
    return middle - before, after - middle


def child_at(node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1) -> list[int]:
    """One child laid at one end at the charge T div 2 at the quarter turn (MS-S1: re_now A, im_before sense B, A B = T div 2, the same two integers for every row), its lay's momentum booked and returned; taken back with the sign -1."""
    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    num = row.pair[0]
    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, num=num)
    dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * sense * node.B, num=num)
    lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)
    return [a + b for a, b in zip(dp, dp_im, strict=True)]


def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]
) -> tuple[list[int], list[int], list[list[int]]]:
    """The two children laid by the one lay act (`child_at`: the - child at the - end, the + child at the + end); returns the lays' momentum, each child's Wronskian at its Node (its sense, the owner's word 3; -+(T div 2) where the plane stood at nothing) and the plane's four levels at each Node before the lay (the residue)."""
    re, im = node.records()[s].lines
    stood = [[int(a[w_]) for a in (re.now, re.before, im.now, im.before)] for w_ in (minus, plus)]
    dp_lay = [0, 0, 0]
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(child_at(node, s, where, sense)):
            dp_lay[a] += d
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood


def children(
    node: Node, at: tuple[int, ...], kids: list[Kid], take: dict[str, Any], rec: int
) -> set[tuple[int, ...]]:
    """One take's children laid (`child_laid`), each birth logged with its numbers, its take's own momentum among them (the Boss's 6399718139: every take's dP on its line, not the close's last), a merger's two ends' takes under `takes`. Returns the Nodes touched."""
    touched = {at}
    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
        node.counts["births"] += 1
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
                "taken": take["taken"],
                "booked": take["booked"],
                "levels": take["levels"],
                "taken_now_was": take["taken_now_was"],
                "taker": take["taker"],
                "taken_row": rec,
                "taken_line": take["taken_line"],
                "proper": int(node.proper[at]),
                "content": int(node.start_content[at]),
                "amplitude": [node.A, node.B],
                "stood": stood,
                "children_at_node": len(kids),
                "room": room,
                "dP_take": take["dP_take"],
                "dP_lay": dp_lay,
                **({"takes": take["takes"]} if "takes" in take else {}),
            }
        )
    return touched


def click(
    node: Node,
    plane_starts: list[list[Line]],
    held: list[list[Line]],
    direction: int = 1,
    frame: dict[str, Any] | None = None,
) -> None:
    """The click in the direction (X2: the undo is the click at -1): forward the readings at the start (each record's standing share at its unscaled rule in the carrier's unit, PM-S1), the Link close of every record alike (SL-S1), the lays refused by name, the births taken and laid, the bodies' closing; backward the close undone from the log's frame (`unclick`). `plane_starts` the records' lines at the interval's start, `held` every row's."""
    if direction == -1:
        assert frame is not None
        unclick(node, frame)
        return
    c = node.start_content
    node.lattices = {}
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    r_emitter = node.rule_of(node.emitter(), c, factors)
    rules = node.read_lines(held, plane_starts, c, factors)
    owns = []
    for rec, r in enumerate(node.records()):
        assert r.pair is not None
        owns.append(node.share(plane_starts[rec], node.rule(r.pair, c, factors)))
    born = [
        b
        for rec in range(len(node.records()))
        for b in meet(node, rec, plane_starts[rec], owns[rec], rules, frozen)
    ]
    born_nodes = births(node, refuse(node, born, owns), c, factors)
    bodies(node, plane_starts, owns, born_nodes, frozen, r_emitter)


def unclick(node: Node, frame: dict[str, Any]) -> None:
    """The close undone from the log, in the reverse order of its lines: the lays removed, the taken line restored at every take's Node (the line each take logged, `taken_line`, CS4-S2; a merger's two ends under `takes`), the readings' counters restored."""
    rec0 = node.records().index(node.emitter())
    for entry in reversed(node.log[frame["log_from"] :]):
        at = tuple(entry["node"])
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
            lay(node, s, tuple(entry["minus"]), (a, 0, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, 0, 0, b), -1)
        if entry["event"] in ("birth", "credit"):
            row = entry.get("taken_row", rec0)
            for take in entry.get("takes", [entry]):
                where, k = tuple(take["node"]), take["taken_line"]
                line = node.records()[row].lines[k]
                lay(node, row, where, take["taken_now_was"] - int(line.now[where]), line=k)
            node.closes[at] -= 1
    del node.log[frame["log_from"] :]
    node.standing, node.crossed, node.beats = frame["counters"]
