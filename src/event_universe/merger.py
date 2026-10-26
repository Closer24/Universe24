"""The merger at rest, MG-S1 (H-Merger-At-Rest-1, 2026-10-26, the Boss's order under the owner's delegation; the former CS8-S1 and CS8-S2 as one letter): a child's wall is its own quantum, the share its levels (A, 0 | 0, +-B) hold alone at the Node under its row's rule, the same two integers for every row (`walls_of`; the former board's increment kept by name, equal to it on an empty plane); a record with a gap whose two ends hold a whole quantum each of opposite charge with no current across the Link meets as the conjugate pair (close.meet's rest branch); each child's wall is paid at its own end by the taken record's levels at that Node taken whole by the one lay act at -1, the fall the share the board loses, both ends read before either is written, refused by name `stop` where an end's fall is below the wall (`merger_falls`, `merger_take`; the Link's number read after the stop, so a stopped pair draws nothing); the light is laid at each end as the exact take at -1, on the line the take names, by the least count of levels at which the share rises by the wall (`rise_of`), as the child's lay where the line has no direction (`light_children`)."""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import TYPE_CHECKING, Any

from event_universe import gram
from event_universe.core import rule3
from event_universe.core.ports import AXES
from event_universe.core.rule3 import half, quotient, share_weight
from event_universe.links import cross
from event_universe.rows import Line, zeros
from event_universe.take import at_node, fall_of, frame_nodes, lay, momentum_of, neighbour

if TYPE_CHECKING:
    from event_universe.node import Node


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


def walls_of(
    node: Node,
    s: int,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    rule: rule3.Rule,
    cache: dict[tuple[int, int, tuple[int, ...]], int],
) -> tuple[int, int]:
    """Each child's wall, its own quantum (MG-S1, CS8-S2): the child laid by the one lay act at its end on zero lines of the row's shape (the row's lines held and put back), the share summed under the row's rule at the board's content over the end and its six neighbours (`share_at`: the zero lines' share is 0 everywhere else), the lines discarded; the same two integers for every row and every Node of one content, read once per end and row in a close (`cache`: no line of the board enters it); the former reading, the board's increment where the plane already stands, kept by name."""
    row = node.records()[s]
    held, found = row.lines, []
    for where, sense in ((minus, -1), (plus, 1)):
        if (s, sense, where) not in cache:
            row.lines = [
                Line(zeros(node.shape), zeros(node.shape), line.rem, line.wall) for line in held
            ]
            child_at(node, s, where, sense)
            cache[(s, sense, where)] = sum(
                share_at(node, row.lines, rule, at) for at in set(frame_nodes(node, where))
            )
        found.append(cache[(s, sense, where)])
    row.lines = held
    return found[0], found[1]


def products(xs: list[int], ys: list[int]) -> list[int]:
    """The bilinear x.G.y line by line at the identity G (gram.weighted's form for every shape but the quartet's), x_k y_k."""
    return [x * y for x, y in zip(xs, ys, strict=True)]


def share_at(node: Node, lines: list[Line], r: rule3.Rule, at: tuple[int, ...]) -> int:
    """A record's share at one Node (gram.share's form, the same integers read at the Node and its six neighbours alone)."""
    g = gram.gram(len(lines))
    weighted = products if g == gram.identity(len(lines)) else partial(gram.weighted, g)
    nows, befores = [int(line.now[at]) for line in lines], [int(line.before[at]) for line in lines]
    reached, shared = [0] * len(lines), [0] * len(lines)
    for port, reach in enumerate(r.reaches):
        q, reach_at = neighbour(node, at, port), at_node(reach, at)
        b_j, n_j = [int(line.before[q]) for line in lines], [int(line.now[q]) for line in lines]
        reached = [x + reach_at * bj for x, bj in zip(reached, b_j, strict=True)]
        parts = weighted(
            [b - bj for b, bj in zip(befores, b_j, strict=True)],
            [n + nj for n, nj in zip(nows, n_j, strict=True)],
        )
        shared = [x + reach_at * part for x, part in zip(shared, parts, strict=True)]
    own = [
        at_node(r.wall, at) * (nn + bb) - at_node(r.self_coefficient, at) * nb - nr
        for nn, bb, nb, nr in zip(
            weighted(nows, nows),
            weighted(befores, befores),
            weighted(nows, befores),
            weighted(nows, reached),
            strict=True,
        )
    ]
    wall, x = share_weight(node.gamma, node.G) + share_weight(node.gamma, node.G), int(node.start_x[at])
    return sum(
        int(rule3.division_forward((o + o - s) * x, wall, 0)[0])
        for o, s in zip(own, shared, strict=True)
    )


def share_fall(
    node: Node,
    rec: int,
    rule: rule3.Rule,
    where: tuple[int, ...],
    levels: tuple[int, ...],
    cache: dict[tuple[int, tuple[int, ...]], int],
) -> int:
    """The share the board loses by a lay at -1 of the levels at the Node (laid and laid back): the lay changes the share at the Node and its six neighbours alone, so the fall is their shares' difference, bit for bit the board's (the former read of the whole board's share, kept by name); the shares as they stand kept in `cache` per record and Node for the close until a take writes."""
    row, window, before = node.records()[rec], set(frame_nodes(node, where)), 0
    for at in window:
        if (rec, at) not in cache:
            cache[(rec, at)] = share_at(node, row.lines, rule, at)
        before += cache[(rec, at)]
    lay(node, rec, where, levels, -1)
    after = sum(share_at(node, row.lines, rule, at) for at in window)
    lay(node, rec, where, levels, 1)
    return before - after


def levels_at(row: Any, where: tuple[int, ...]) -> tuple[int, ...]:
    """A record's levels at the Node as one lay names them (now, before per line)."""
    return tuple(int(a[where]) for line in row.lines for a in (line.now, line.before))


def merger_falls(
    node: Node,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    walls: tuple[int, int],
    rule: rule3.Rule,
    rec: int,
    refused: Callable[..., None],
    cache: dict[tuple[int, tuple[int, ...]], int],
) -> list[tuple[tuple[int, ...], int, tuple[int, ...], int]] | None:
    """The merger's reads (MG-S1, the birth's lay read at -1): at each end the taken record's levels at the Node and the share the board loses by their lay at -1 (`share_fall`, laid and laid back), both ends read before either is written, the first end's refusal sparing the second's read; refused by name `stop` where an end's fall is below its child's wall. Returns per end (the Node, the wall, the levels, the fall), or None."""
    row = node.records()[rec]
    ends = []
    for where, wall in zip((minus, plus), walls, strict=True):
        levels = levels_at(row, where)
        fall = share_fall(node, rec, rule, where, levels, cache)
        if fall < wall:
            refused(node, where, "stop", fall=fall, walls=wall, row=rec)
            return None
        ends.append((where, wall, levels, fall))
    return ends


def merger_take(
    node: Node, ends: list[tuple[tuple[int, ...], int, tuple[int, ...], int]], rule: rule3.Rule, rec: int
) -> dict[str, Any]:
    """The merger's take after its reads (`merger_falls`): each end's levels taken whole by the one lay act at -1, its momentum booked on both lines. Returns the log's take fields, the two ends' takes summed and each end's own under `takes` (its `taken_levels` the levels taken, unclick laying them back)."""
    row = node.records()[rec]
    assert row.pair is not None
    takes: list[dict[str, Any]] = []
    for where, wall, levels, fall in ends:
        (re, im), (re_now, re_before, im_now, im_before) = row.lines, levels
        dp = momentum_of(node, re.now, re.before, where, -re_now, -re_before, row.pair[0])
        dp_im = momentum_of(node, im.now, im.before, where, -im_now, -im_before, row.pair[0])
        lay(node, rec, where, levels, -1)
        node.closes[where] -= 1
        takes.append(
            {
                "node": list(where),
                "taken": fall,
                "booked": wall,
                "levels": sum(abs(x) for x in levels),
                "taken_levels": list(levels),
                "dP_take": [a + b for a, b in zip(dp, dp_im, strict=True)],
            }
        )
    return {
        "taken": takes[0]["taken"] + takes[1]["taken"],
        "booked": takes[0]["booked"] + takes[1]["booked"],
        "levels": takes[0]["levels"] + takes[1]["levels"],
        "taken_now_was": [t["taken_levels"] for t in takes],
        "taker": [t["taken_levels"] for t in takes],
        "dP_take": [a + b for a, b in zip(takes[0]["dP_take"], takes[1]["dP_take"], strict=True)],
        "taken_line": [None, None],
        "takes": takes,
    }


def rise_of(
    node: Node, where: tuple[int, ...], wall: int, rule: rule3.Rule, row: Any
) -> tuple[int, int, int]:
    """The exact take at -1 (MG-S1): on the line the fall's sign names (take.fall_of, CS4-S2) the least count d of levels moved away from the before at which the Node's share rises by the wall, the rise fall_of's form with the sign mirrored, x (w ((now + u d)^2 - now^2) + u d pull) over the weight, the least count by doubling and bisection in comparisons; (k, 0, 0) where the line has no direction (now = before). Returns (the line, the signed count, the rise)."""
    _levels, _fall, k = fall_of(node, where, wall, rule, row)
    line = row.lines[k]
    now, before = int(line.now[where]), int(line.before[where])
    if now == before:
        return k, 0, 0
    u = 1 if now > before else -1
    own, w, reached = at_node(rule.self_coefficient, where), int(rule.wall), 0
    for port, reach in enumerate(rule.reaches):
        reached += at_node(reach, where) * int(line.before[neighbour(node, where, port)])
    pull = own * before + reached
    x, weight = int(node.start_x[where]), share_weight(node.gamma, node.G)

    def rise(d: int) -> int:
        moved = now + u * d
        return int(quotient(x * (w * (moved * moved - now * now) + u * d * pull), weight))

    high = 1
    while rise(high) < wall:
        high += high
    low = 0
    while high - low > 1:
        middle = int(half(low + high))
        low, high = (middle, high) if rise(middle) < wall else (low, middle)
    return k, u * high, rise(high)


def light_children(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], walls: list[int], rule: rule3.Rule
) -> tuple[list[int], list[int], list[list[int]], list[list[int] | None]]:
    """A merger's two light children (MG-S1): at each end the light laid as the exact take at -1 (`rise_of`) on the line the take names, or as the child's lay where the line has no direction; returns the lays' momentum, each child's Wronskian at its Node, the plane's four levels at each Node before the lay and the exact lays [line, count, rise] (None where the child's lay)."""
    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    stood = [[int(a[w_]) for a in (re.now, re.before, im.now, im.before)] for w_ in (minus, plus)]
    dp_lay, exact = [0] * AXES, []
    for where, sense, wall in zip((minus, plus), (-1, 1), walls, strict=True):
        k, d, rise = rise_of(node, where, wall, rule, row)
        if d == 0:
            dp, exact_lay = child_at(node, s, where, sense), None
        else:
            z = row.lines[k]
            dp = momentum_of(node, z.now, z.before, where, d_now=d, num=row.pair[0])
            lay(node, s, where, d, line=k)
            exact_lay = [k, d, rise]
        exact.append(exact_lay)
        dp_lay = [a + b for a, b in zip(dp_lay, dp, strict=True)]
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood, exact
