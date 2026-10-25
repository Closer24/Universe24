"""The close, the Node's fourth act (ALGEBRA.md, The click writes on the lattice): the readings at the start (every row's rule, the gap-0 plane's share and each record's standing share at the vacuum's weight, the frozen Nodes), the Link close (`meet`: every Link once from its +a end, both ends holding a whole quantum of the plane at the gap 0, the + child at the end the light's current flows into where the twist is right-handed, the one-Link read of a number at that end), the lays refused by name (`refuse`), the births taken and laid (`births`), the bodies' closing (`bodies`); the lay, the exact take and the momentum they book; the close undone from the log (`unclick`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import readings
from event_universe.core import rule3
from event_universe.core.ports import AXES, PORT_SIDES
from event_universe.core.rule3 import quotient, remainder
from event_universe.links import cross, link_current, twist
from event_universe.rows import PLANE, POTENTIAL, Line
from event_universe.take import (
    frame_nodes,
    lay,
    lay_amplitude,
    momentum_of,
    neighbour,
    read_number,
    take_at,
)

if TYPE_CHECKING:
    from event_universe.node import Node

Birth = tuple[tuple[int, ...], int, tuple[int, ...], tuple[int, ...], int]


def refused(node: Node, at: tuple[int, ...], cause: str, **numbers: Any) -> None:
    """A refusal by name, counted and logged."""
    node.counts["refused_" + cause] += 1
    node.log.append(
        {"event": "refused", "i": node.interval, "node": list(at), "cause": cause, **numbers}
    )


def meet(
    node: Node, taken: Line, sh: Any, rules: list[tuple[Line, rule3.Rule]], frozen: Any
) -> list[Birth]:
    """The Link close: every Link once from its +a end; a meeting where both ends hold a whole quantum of the plane at the gap 0 at the vacuum's weight and neither end is frozen; the + child at the end the gap-0 line's own current flows into where the twist of the taken line's transverse currents is right-handed, at the other end where left-handed (F = 0 and h = 0 refused by name); the Link's one number read at the current's end gives the plane. Returns the births as (the take's Node, the plane, the - child's Node, the + child's Node, the draw's room)."""
    born: list[Birth] = []
    currents = [node.den * link_current(taken, 2 * axis) for axis in range(AXES)]
    twists = [twist(taken, axis) for axis in range(AXES)]
    for at in np.ndindex(*node.shape):
        if frozen[at]:
            continue
        for axis in range(AXES):
            j = neighbour(node, at, 2 * axis)
            if frozen[j] or int(sh[at]) < node.unit_gap0 or int(sh[j]) < node.unit_gap0:
                continue
            flow = int(currents[axis][at])
            if flow == 0:
                refused(node, at, "orientation", link=list(j))
                continue
            into, outof = (j, at) if flow > 0 else (at, j)
            h = int(twists[axis][at])
            if h == 0:
                refused(node, at, "twist", link=list(j))
                continue
            plus, minus = (into, outof) if h > 0 else (outof, into)
            drawn = read_number(node, into, rules)
            if drawn is None:
                continue
            number, room = drawn
            born.append(
                (
                    into,
                    remainder(quotient(number, node.unit_gap0), len(node.records())),
                    minus,
                    plus,
                    room,
                )
            )
    return born


def refuse(node: Node, born: list[Birth], owns: list[Any]) -> list[Birth]:
    """The lay refused by name: where any of the child's plane already stands at its Node, and where two children of one plane would land at one Node in one close (the charge made at a crowded lay). Returns the births kept."""
    kept = []
    for at, s, minus, plus, room in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:
            refused(node, at, "lay", standing=int(owns[s][minus]), unit=node.units[s])
            continue
        kept.append((at, s, minus, plus, room))
    landing: dict[tuple[int, tuple[int, ...]], int] = {}
    for _at, s, minus, plus, _room in kept:
        landing[(s, minus)] = landing.get((s, minus), 0) + 1
        landing[(s, plus)] = landing.get((s, plus), 0) + 1
    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
    for at, s, minus, plus, _room in crowded:
        refused(node, at, "lay", children_at_one_node=max(landing[(s, minus)], landing[(s, plus)]))
    return [k for k in kept if k not in crowded]


def births(
    node: Node, kept: list[Birth], r_gap0: rule3.Rule, c: Any, factors: tuple[Any, ...], pace: Any
) -> set[tuple[int, ...]]:
    """The births kept, every face read before any write: one exact take per Node of its children's walls summed, the start's gap-0 line paying; then each child laid as one quantum of its record at the quarter turn (`children`). Returns every Node a taken birth touched."""
    by_node: dict[tuple[int, ...], list[tuple[int, tuple[int, ...], tuple[int, ...], int]]] = {}
    for at, s, minus, plus, room in kept:
        by_node.setdefault(at, []).append((s, minus, plus, room))
    taken = []
    for at in sorted(by_node):
        walls = sum(2 * node.units[s] for s, _m, _p, _r in by_node[at])
        got = take_at(node, at, walls, r_gap0, len(by_node[at]))
        if got is not None:
            taken.append((at, by_node[at], walls, got))
    touched: set[tuple[int, ...]] = set()
    for at, kids, walls, (levels, fall, now, before) in taken:
        node.closes[at] -= 1
        touched |= children(node, at, kids, (walls, levels, fall, now, before), c, factors, pace)
        node.counts["taken"] += fall
        node.counts["booked"] += walls
    return touched


def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], amplitude: int
) -> tuple[list[int], list[int]]:
    """One child laid as one quantum of its record at the quarter turn (re_now A at the - end, im_before -A; re_now A at the + end, im_before +A), each lay's momentum booked; returns the lay's momentum and each child's Wronskian at its Node (its sense, the owner's word 3)."""
    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    dp_lay = [0, 0, 0]
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(
            momentum_of(node, re.now, re.before, where, d_now=amplitude, num=row.pair[0])
        ):
            dp_lay[a] += d
        for a, d in enumerate(
            momentum_of(node, im.now, im.before, where, d_before=sense * amplitude, num=row.pair[0])
        ):
            dp_lay[a] += d
        lay(node, s, where, (amplitude, 0, 0, sense * amplitude))
    return dp_lay, [
        int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)
    ]


def children(
    node: Node,
    at: tuple[int, ...],
    kids: list[tuple[int, tuple[int, ...], tuple[int, ...], int]],
    take: tuple[int, int, int, int, int],
    c: Any,
    factors: tuple[Any, ...],
    pace: Any,
) -> set[tuple[int, ...]]:
    """One take's children laid (`child_laid`), each birth logged with its numbers. Returns the Nodes touched."""
    walls, levels, fall, now, before = take
    dp_take = node.last_dp
    touched = {at}
    for s, minus, plus, room in kids:
        amplitude = lay_amplitude(node, s, at, c, factors, pace)
        dp_lay, w_children = child_laid(node, s, minus, plus, amplitude)
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
                "proper": int(node.proper[at]),
                "content": int(c[at]),
                "amplitude": amplitude,
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
    """The bodies' closing: a record standing at a whole quantum of its own unit through one period of its re line's upward crossings clicks (one take of its unit at the Node, the credit logged), a Node of a birth this interval or a frozen Node apart."""
    for rec in range(len(node.records())):
        standing_now = np.vectorize(
            lambda v, unit=node.units[rec]: 1 if int(v) >= unit else 0, otypes=[object]
        )(owns[rec])
        node.standing[rec] = np.where(standing_now == 1, node.standing[rec] + 1, 0)
        re = node.records()[rec].lines[0]
        upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
            re.before, re.now
        )
        counting = np.vectorize(lambda v: 1 if int(v) > 0 else 0, otypes=[object])(node.crossed[rec])
        node.beats[rec] = np.where((upward == 1) & (counting == 1), node.crossed[rec], node.beats[rec])
        node.crossed[rec] = np.where(upward == 1, 1, np.where(counting == 1, node.crossed[rec] + 1, 0))
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
    """A body's credit with its frame (`frame_of`), its sense the sign of its Wronskian at the Node, its beat, the take's numbers and momentum, the taker's three levels (the gap-0 line's now before the take, its before, the levels taken: PC-S2), the sign level and whether the Node turned."""
    re, im = node.records()[rec].lines
    w = int(cross(re.now[at], im.now[at], re.before[at], im.before[at]))
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
        "frame": frame_of(node, rec, at, plane_starts),
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
    """The click in the direction (X2: the undo is the click at -1): forward the readings at the start, the Link close, the lays refused by name, the births taken and laid, the bodies' closing; backward the close undone from the log's frame (`unclick`). `plane_starts` the planes' lines at the interval's start, `held` every row's."""
    if direction == -1:
        assert frame is not None
        unclick(node, frame)
        return
    c = node.start_content
    factors = node.link_factors()
    gap0 = node.row(PLANE, gap=0)
    r_gap0 = node.rule_of(gap0, c, factors)
    gap0_start = plane_starts[node.records().index(gap0)]
    rules = node.read_lines(held, plane_starts, c, factors)
    pace = readings.paces_of(node, c)[1]
    owns = []
    for rec, r in enumerate(node.records()):
        rr = node.rule_of(r, c, factors)
        re0, im0 = plane_starts[rec]
        owns.append(node.share(re0, rr, pace, vacuum=True) + node.share(im0, rr, pace, vacuum=True))
    sh = owns[node.records().index(gap0)]
    frozen = np.asarray(pace, dtype=object) == 0 if np.ndim(pace) else np.zeros(node.shape, dtype=bool)
    born_nodes = births(
        node, refuse(node, meet(node, gap0_start[0], sh, rules, frozen), owns), r_gap0, c, factors, pace
    )
    bodies(node, plane_starts, owns, born_nodes, frozen, r_gap0)


def unclick(node: Node, frame: dict[str, Any]) -> None:
    """The close undone from the log, in the reverse order of its lines: the lays removed, the gap-0 line restored, the readings' counters restored."""
    gap0 = node.row(PLANE, gap=0)
    rec0 = node.records().index(gap0)
    for entry in reversed(node.log[frame["log_from"] :]):
        at = tuple(entry["node"])
        if entry["event"] == "birth":
            s, amplitude = entry["line_pair"], entry["amplitude"]
            lay(node, s, tuple(entry["minus"]), (amplitude, 0, 0, -amplitude), -1)
            lay(node, s, tuple(entry["plus"]), (amplitude, 0, 0, amplitude), -1)
        if entry["event"] in ("birth", "credit"):
            lay(node, rec0, at, (entry["taken_now_was"] - int(gap0.lines[0].now[at]), 0, 0, 0))
            node.closes[at] -= 1
    del node.log[frame["log_from"] :]
    node.standing, node.crossed, node.beats = frame["counters"]
