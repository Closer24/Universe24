"""The close, the Node's fourth act (ALGEBRA.md, The click writes on the lattice): the readings at the start (every row's rule, the gap-0 plane's share and each record's standing share at the vacuum's weight, the frozen Nodes), the Link close (`meet`: every Link once from its +a end, both ends holding a whole quantum of the plane at the gap 0, the + child at the end the light's current flows into where the twist is right-handed, the one-Link read of a number at that end), the lays refused by name (`refuse`), the births taken and laid (`births`), the bodies' closing (`bodies`); the lay, the exact take and the momentum they book; the close undone from the log (`unclick`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram, readings
from event_universe.core import rule3
from event_universe.core.ports import AXES, PORT_SIDES, across
from event_universe.core.rule3 import quotient, remainder
from event_universe.links import cross, row_current, row_twist
from event_universe.rows import PLANE, POTENTIAL, Line
from event_universe.take import frame_nodes, lay, momentum_of, neighbour, read_number, take_at

if TYPE_CHECKING:
    from event_universe.node import Node

Birth = tuple[tuple[int, ...], int, tuple[int, ...], tuple[int, ...], int, int]


def refused(node: Node, at: tuple[int, ...], cause: str, **numbers: Any) -> None:
    """A refusal by name, counted and logged."""
    node.counts["refused_" + cause] += 1
    node.log.append(
        {"event": "refused", "i": node.interval, "node": list(at), "cause": cause, **numbers}
    )


def list_of(node: Node, rec: int, number: int) -> int:
    """The children's record of a meeting of the record `rec` by the pairs: where the taken row is the plane at the gap 0 the draw's pick among the planes (the number over the unit, modulo their count); where it is a row with a gap, the row whose pair is the product (den, den), the plane at the gap 0 (SL-S1: two gapped quanta meeting give light)."""
    records = node.records()
    if records[rec].gap:
        return records.index(node.row(PLANE, gap=0))
    planes = [k for k, r in enumerate(records) if r.shape == PLANE]
    return planes[int(remainder(quotient(number, node.units[rec]), len(planes)))]


def meet(
    node: Node, rec: int, start: list[Line], sh: Any, rules: list[tuple[Line, rule3.Rule]], frozen: Any
) -> list[Birth]:
    """The Link close of one record, the same for every record (SL-S1, the generic close): every Link once from its +a end; a meeting where both ends hold a whole quantum of the record at the interval's start and neither end is frozen (counted as `met`); the + child at the end the record's own current flows into where the twist of its transverse currents is right-handed, at the other end where left-handed (F = 0 and h = 0 refused by name); the Link's one number read at the current's end names the children's record (`list_of`). Returns the births as (the take's Node, the children's record, the - child's Node, the + child's Node, the draw's room, the taken record)."""
    born: list[Birth] = []
    unit = node.units[rec]
    standing = np.vectorize(lambda v: int(v) >= unit, otypes=[bool])(sh) & ~frozen
    currents = [node.den * row_current(start, 2 * axis) for axis in range(AXES)]
    twists = [row_twist(start, axis) for axis in range(AXES)]
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
    """The births kept, every face read before any write: one exact take per Node and taken record of its children's walls summed, the walls the share the two lays add to their plane on the board (`lay_cost`, MS-S1: what is taken is what the lay books and nothing made), the taken record's first line paying at its rule; then each child laid at the charge T div 2 (`children`). Returns every Node a taken birth touched."""
    by_node: dict[
        tuple[tuple[int, ...], int], list[tuple[int, tuple[int, ...], tuple[int, ...], int]]
    ] = {}
    for at, s, minus, plus, room, rec in kept:
        by_node.setdefault((at, rec), []).append((s, minus, plus, room))
    taken = []
    for at, rec in sorted(by_node):
        kids = by_node[(at, rec)]
        walls = sum(lay_cost(node, s, minus, plus, c, factors) for s, minus, plus, _r in kids)
        pair = node.records()[rec].pair
        assert pair is not None
        got = take_at(node, at, walls, node.rule(pair, c, factors), len(kids), rec)
        if got is not None:
            taken.append((at, rec, kids, walls, got, node.last_dp))
    touched: set[tuple[int, ...]] = set()
    for at, rec, kids, walls, (levels, fall, now, before), dp_take in taken:
        node.closes[at] -= 1
        touched |= children(node, at, kids, (walls, levels, fall, now, before, dp_take), rec)
        node.counts["taken"] += fall
        node.counts["booked"] += walls
    return touched


def lay_cost(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> int:
    """The walls a birth books (MS-S1): the share the two children's lays add to their plane on the board in the carrier's unit, read by laying them, reading and taking them back."""
    row = node.records()[s]
    assert row.pair is not None
    rule = node.rule(row.pair, c, factors)
    before = int(sum(int(x) for x in node.share(row.lines, rule).reshape(-1)))
    child_laid(node, s, minus, plus)
    after = int(sum(int(x) for x in node.share(row.lines, rule).reshape(-1)))
    child_laid(node, s, minus, plus, -1)
    return after - before


def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], sign: int = 1
) -> tuple[list[int], list[int], list[list[int]]]:
    """One child laid at the charge T div 2 at the quarter turn (MS-S1: re_now A at the - end, im_before -B; re_now A at the + end, im_before +B; A B = T div 2, the same two integers for every row), each lay's momentum booked; taken back with the sign -1; returns the lay's momentum, each child's Wronskian at its Node (its sense, the owner's word 3; T div 2 where the plane stood at nothing) and the plane's four levels at each Node before the lay (the residue)."""
    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    dp_lay = [0, 0, 0]
    stood = [[int(a[w_]) for a in (re.now, re.before, im.now, im.before)] for w_ in (minus, plus)]
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(
            momentum_of(node, re.now, re.before, where, d_now=sign * node.A, num=row.pair[0])
        ):
            dp_lay[a] += d
        for a, d in enumerate(
            momentum_of(node, im.now, im.before, where, d_before=sign * sense * node.B, num=row.pair[0])
        ):
            dp_lay[a] += d
        lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood


def children(
    node: Node,
    at: tuple[int, ...],
    kids: list[tuple[int, tuple[int, ...], tuple[int, ...], int]],
    take: tuple[int, int, int, int, int, list[int]],
    rec: int,
) -> set[tuple[int, ...]]:
    """One take's children laid (`child_laid`), each birth logged with its numbers, its take's own momentum among them (the Boss's 6399718139: every take's dP on its line, not the close's last). Returns the Nodes touched."""
    walls, levels, fall, now, before, dp_take = take
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
                "taken": fall,
                "booked": walls,
                "levels": levels,
                "taken_now_was": now,
                "taker": [now, before, levels],
                "taken_row": rec,
                "proper": int(node.proper[at]),
                "content": int(node.start_content[at]),
                "amplitude": [node.A, node.B],
                "stood": stood,
                "children_at_node": len(kids),
                "room": room,
                "dP_take": dp_take,
                "dP_lay": dp_lay,
            }
        )
    return touched


def bodies(
    node: Node,
    plane_starts: list[list[Line]],
    owns: list[Any],
    born_nodes: set[tuple[int, ...]],
    frozen: Any,
    r_gap0: rule3.Rule,
) -> None:
    """The bodies' closing: a record standing at a whole quantum of its own unit through one period of its beat clicks (one take of its unit at the Node, the credit logged), a Node of a birth this interval or a frozen Node apart; the beat a plane's by its re line's upward crossings counted, a quartet's from the invariant ratio N.G.B / N.G.N along the law's orbit (gram.period)."""
    for rec, row in enumerate(node.records()):
        standing_now = np.vectorize(
            lambda v, unit=node.units[rec]: 1 if int(v) >= unit else 0, otypes=[object]
        )(owns[rec])
        node.standing[rec] = np.where(standing_now == 1, node.standing[rec] + 1, 0)
        if row.shape == PLANE:
            re = row.lines[0]
            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
                re.before, re.now
            )
            counting = np.vectorize(lambda v: 1 if int(v) > 0 else 0, otypes=[object])(node.crossed[rec])
            node.beats[rec] = np.where(
                (upward == 1) & (counting == 1), node.crossed[rec], node.beats[rec]
            )
            node.crossed[rec] = np.where(
                upward == 1, 1, np.where(counting == 1, node.crossed[rec] + 1, 0)
            )
        else:
            node.beats[rec] = gram.period(node, row.lines, standing_now)
        closing = np.vectorize(
            lambda st, bt: 1 if (int(bt) > 0 and int(st) >= int(bt)) else 0, otypes=[object]
        )(node.standing[rec], node.beats[rec])
        for where in zip(*np.nonzero(closing == 1), strict=True):
            at = tuple(int(x) for x in where)
            if at in born_nodes or frozen[at]:
                continue
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            node.log.append(credit(node, rec, at, plane_starts, fall, levels, now, before))


def frame_of(
    node: Node, rec: int, at: tuple[int, ...], plane_starts: list[list[Line]]
) -> dict[str, Any]:
    """A credit's frame: the record's levels at the Node now, stepped and at the start, its neighbours' at the start, the Link phases, frames, odd lines and factors the Node read at the start."""
    re, im = node.records()[rec].lines
    re0, im0 = plane_starts[rec]
    nodes = frame_nodes(node, at)[1:]
    sre, sim = node.stepped[rec]
    return {
        "re_now": int(re.now[at]),
        "im_now": int(im.now[at]),
        "re_before": int(re.before[at]),
        "im_before": int(im.before[at]),
        "re_stepped": int(sre.now[at]),
        "im_stepped": int(sim.now[at]),
        "re_start_now": int(re0.now[at]),
        "re_start_before": int(re0.before[at]),
        "im_start_now": int(im0.now[at]),
        "im_start_before": int(im0.before[at]),
        "re_neighbours_start": [int(re0.now[n]) for n in nodes],
        "im_neighbours_start": [int(im0.now[n]) for n in nodes],
        "phases": [[int(c[at]), int(sn[at])] for c, sn in node.start_phases],
        "frames": [int(f[at]) for f in node.start_frames],
        "odd": [
            int(side * (node.start_odd[axis][at] + node.start_odd[axis][n]))
            for (axis, side), n in zip(PORT_SIDES, nodes, strict=True)
        ],
        "X": node.X,
        "factors": [int(f[at]) for f in node.start_factors],
    }


def bilinears_of(node: Node, rec: int, at: tuple[int, ...]) -> dict[str, Any]:
    """A quartet's credit frame: its levels at the Node, its charge W, its spin density (the record's axial vector, signed per axis) and its axial Wronskians B.GJ Gamma_a.N (SR-S2; the decoder's species solve is a plane's, owed for the quartet by name)."""
    row = node.records()[rec]
    nows, befores = [line.now for line in row.lines], [line.before for line in row.lines]
    gj = gram.matmul(gram.gram(row.shape), gram.rotation(row.shape))
    axial = [int(s[at]) for s in gram.density(row.shape, nows)]
    return {
        "levels_now": [int(n[at]) for n in nows],
        "levels_before": [int(b[at]) for b in befores],
        "W": int(gram.charge(row.shape, row.lines)[at]),
        "axial": axial,
        "axial_sign": [(s > 0) - (s < 0) for s in axial],
        "axial_wronskian": [
            int(gram.form(gj, befores, gram.matvec(ga, nows))[at]) for ga in gram.axes(row.shape)
        ],
    }


def credit(
    node: Node,
    rec: int,
    at: tuple[int, ...],
    plane_starts: list[list[Line]],
    fall: int,
    levels: int,
    taken_was: int,
    taken_before: int,
) -> dict[str, Any]:
    """A body's credit with its frame (a plane's `frame_of`, a quartet's `bilinears_of`), its sense the sign of its charge at the Node, its beat, the take's numbers and momentum, the taker's three levels (the gap-0 line's now before the take, its before, the levels taken: PC-S2), the sign level and whether the Node turned."""
    row = node.records()[rec]
    w = int(gram.charge(row.shape, row.lines)[at])
    return {
        "event": "credit",
        "i": node.interval,
        "node": list(at),
        "proper": int(node.proper[at]),
        "closes": int(node.closes[at]),
        "content": int(node.start_content[at]),
        "line": rec,
        "sense": 1 if w > 0 else -1 if w < 0 else 0,
        "beat": int(node.beats[rec][at]),
        "frame": frame_of(node, rec, at, plane_starts)
        if row.shape == PLANE
        else bilinears_of(node, rec, at),
        "taken": fall,
        "levels": levels,
        "taken_now_was": taken_was,
        "taker": [taken_was, taken_before, levels],
        "dP_take": node.last_dp,
        "sign_level": int(node.row(POTENTIAL).lines[0].now[at]),
        "turned": bool(node.turned[at]),
    }


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
    gap0 = node.row(PLANE, gap=0)
    r_gap0 = node.rule_of(gap0, c, factors)
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
    bodies(node, plane_starts, owns, born_nodes, frozen, r_gap0)


def unclick(node: Node, frame: dict[str, Any]) -> None:
    """The close undone from the log, in the reverse order of its lines: the lays removed, the taken row's line restored, the readings' counters restored."""
    gap0 = node.row(PLANE, gap=0)
    rec0 = node.records().index(gap0)
    for entry in reversed(node.log[frame["log_from"] :]):
        at = tuple(entry["node"])
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
            lay(node, s, tuple(entry["minus"]), (a, 0, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, 0, 0, b), -1)
        if entry["event"] in ("birth", "credit"):
            row = entry.get("taken_row", rec0)
            line = node.records()[row].lines[0]
            lay(
                node,
                row,
                at,
                (entry["taken_now_was"] - int(line.now[at]),)
                + (0,) * (2 * node.records()[row].shape - 1),
            )
            node.closes[at] -= 1
    del node.log[frame["log_from"] :]
    node.standing, node.crossed, node.beats = frame["counters"]
