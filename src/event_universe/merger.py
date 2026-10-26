"""The merger at rest, MG-S1 (H-Merger-At-Rest-1, 2026-10-26, the Boss's order under the owner's delegation; the former CS8-S1 and CS8-S2 as one letter): a child's wall is its own quantum, the share its levels (A, 0 | 0, +-B) hold alone at the Node under its row's rule, the same two integers for every row (`walls_of`; the former board's increment kept by name, equal to it on an empty plane); a record with a gap whose two ends hold a whole quantum each of opposite charge with no current across the Link meets as the conjugate pair (close.meet's rest branch); each child's wall is paid at its own end by the taken record's levels at that Node taken whole by the one lay act at -1, the fall the share the board loses, both ends read before either is written, refused by name `stop` where an end's fall is below the wall (`merger_falls`, `merger_take`; the Link's number read after the stop, so a stopped pair draws nothing); the light is laid at each end as the exact take at -1, on the line the take names, by the least count of levels at which the share rises by the wall (`rise_of`), as the child's lay where the line has no direction (`light_children`). The close's one take act for every letter (CR-S1 and CR-S2, the owner's word of 2026-10-26, 06:1x UTC): the ends read before any is written (`read_ends`), then written (`write_ends`), the birth's one end, the body's one end and the merger's two alike (`takes`, `summed`)."""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import TYPE_CHECKING, Any

from event_universe import gram, take
from event_universe.core import rule3
from event_universe.core.ports import AXES
from event_universe.core.rule3 import least_at, quotient, share_weight
from event_universe.links import cross
from event_universe.rows import Line, zeros
from event_universe.take import at_node, frame_nodes, lay, momentum_of, move, neighbour

if TYPE_CHECKING:
    from event_universe.node import Node


def child_at(node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1) -> list[int]:
    """One child laid at one end at the charge T div 2 at the quarter turn, with the charge's sign on the re line (GP-S1, the owner's word of 2026-10-26, 04:3x UTC: re_now sense A, im_before B, A B = T div 2, the same two integers for every row, so the light's re line carries its parity under C P, odd as the emission that sources it; MS-S1's former spelling (A, 0, 0, sense B) kept by name: the - child's two spellings are one record turned by a half turn, the same charge, share and wall), its lay's momentum booked and returned; taken back with the sign -1."""
    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    num = row.pair[0]
    dp = momentum_of(node, re.now, re.before, where, d_now=sign * sense * node.A, num=num)
    dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * node.B, num=num)
    lay(node, s, where, (sense * node.A, 0, 0, node.B), sign)
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


def share_at(node: Node, lines: list[Line], r: rule3.Rule, at: tuple[int, ...]) -> int:
    """A record's share at one Node (gram.share's form, the same integers read at the Node and its six neighbours alone)."""
    g = gram.gram(len(lines))
    weighted = partial(gram.weighted, g)
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


def read_ends(
    node: Node,
    ends: list[tuple[tuple[int, ...], int]],
    rule: rule3.Rule,
    cause: int,
    rec: int,
    cache: dict[tuple[int, tuple[int, ...]], int] | None = None,
) -> list[tuple[tuple[int, ...], int, Any, int, int | None, int, int]] | None:
    """The take act's reads (CR-S2, the owner's word of 2026-10-26, 06:1x UTC: every end read before any is written, refused by name `stop` at the first that cannot pay, the first end's refusal sparing the second's read): at the gap-0 row the end owes the walls booked less the take's remainder standing there (EX-S1) and its line by the fall's sign is read for the least count paying it (take.fall_of); at a record with a gap the end's levels are read whole with the share the board loses by their lay at -1 (`share_fall`, MG-S1, the birth read at -1), owing the wall. Returns per end (the Node, the wall, the levels or the count, the fall, the line or None, the remainder before, the owed), or None; the former merger_falls kept by name."""
    row = node.records()[rec]
    found = []
    for where, wall in ends:
        rem_was = 0 if row is not node.emitter() else int(node.take_rem[where])
        owed = wall - rem_was
        if row is not node.emitter():
            levels: Any = levels_at(row, where)
            fall, k = share_fall(node, rec, rule, where, levels, cache or {}), None
            short = fall < wall
        else:
            levels, fall, k = take.fall_of(node, where, owed, rule, row)
            short = levels is None
        if short:
            node.counts["refused_stop"] += cause
            entry = {"event": "refused", "i": node.interval, "node": list(where), "cause": "stop"}
            node.log.append(entry | {"fall": fall, "walls": wall, "owed": owed, "row": rec})
            return None
        found.append((where, wall, levels, fall, k, rem_was, owed))
    return found


def write_ends(
    node: Node, reads: list[tuple[tuple[int, ...], int, Any, int, int | None, int, int]], rec: int
) -> list[dict[str, Any]]:
    """The take act's writes after its reads (CR-S2): at the gap-0 row the end's line moved toward its before by the count (take.move, CR-S1), the fall above what was owed its new remainder (EX-S1), the momentum booked; at a record with a gap the end's levels taken whole by the lay act at -1, the momentum booked on both lines (MG-S1). Returns each end's take as the log carries it; the former take_line and merger_take kept by name."""
    row = node.records()[rec]
    assert row.pair is not None
    found: list[dict[str, Any]] = []
    for where, wall, levels, fall, k, rem_was, owed in reads:
        if row is not node.emitter():
            (re, im), (re_now, re_before, im_now, im_before) = row.lines, levels
            dp = momentum_of(node, re.now, re.before, where, -re_now, -re_before, row.pair[0])
            dp_im = momentum_of(node, im.now, im.before, where, -im_now, -im_before, row.pair[0])
            lay(node, rec, where, levels, -1)
            node.closes[where] -= 1
            size, moment = sum(abs(x) for x in levels), [a + b for a, b in zip(dp, dp_im, strict=True)]
            found.append(
                dict(
                    node=list(where),
                    taken=fall,
                    booked=wall,
                    levels=size,
                    taken_levels=list(levels),
                    dP_take=moment,
                )
            )
            continue
        assert k is not None
        z = row.lines[k]
        now, before = int(z.now[where]), int(z.before[where])
        toward = 1 if before > now else -1
        move(node, rec, k, where, toward * levels)
        node.closes[where] += 1
        node.take_rem[where] = fall - owed
        node.last_dp = momentum_of(node, z.now, z.before, where, d_now=toward * levels, num=row.pair[0])
        found.append(
            {
                "node": list(where),
                "taken": fall,
                "booked": wall,
                "levels": levels,
                "taken_now_was": now,
                "taker": [now, before, levels],
                "dP_take": node.last_dp,
                "taken_line": k,
                "remainder_was": rem_was,
                "remainder": fall - owed,
                "owed": owed,
            }
        )
    return found


def takes(
    node: Node,
    ends: list[tuple[tuple[int, ...], int]],
    rule: rule3.Rule,
    cause: int,
    rec: int | None = None,
    draw: Callable[[], Any] | None = None,
    cache: dict[tuple[int, tuple[int, ...]], int] | None = None,
) -> list[dict[str, Any]] | None:
    """The close's one take act for every letter alike (CR-S2): the walls booked at each end paid by one exact take at that end from the taken row (the gap-0 row's where none is named: a body's take), every end read before any is written (`read_ends`) and refused by name at the first that cannot pay, the Link's number drawn between the reads and the writes where the letter draws one (`draw`, the merger's; None drawn refuses the take), then every end written (`write_ends`); the birth's list one end of its children's walls summed, the body's one end of its unit, the merger's its two ends. Returns each end's take, or None."""
    taken = node.records().index(node.emitter()) if rec is None else rec
    reads = read_ends(node, ends, rule, cause, taken, cache)
    if reads is None or (draw is not None and draw() is None):
        return None
    return write_ends(node, reads, taken)


def summed(found: list[dict[str, Any]]) -> dict[str, Any]:
    """One take's numbers as the log carries them: one end's own fields; two ends' summed, each end's own under `takes` (a merger's whole levels as the taken and the taker, no line)."""
    if len(found) == 1:
        return {k: v for k, v in found[0].items() if k != "node"}
    whole = "taken_levels" in found[0]
    return {
        "taken": sum(t["taken"] for t in found),
        "booked": sum(t["booked"] for t in found),
        "levels": sum(t["levels"] for t in found),
        "taken_now_was": [t["taken_levels" if whole else "taken_now_was"] for t in found],
        "taker": [t["taken_levels" if whole else "taker"] for t in found],
        "dP_take": [sum(x) for x in zip(*(t["dP_take"] for t in found), strict=True)],
        "taken_line": [None if whole else t["taken_line"] for t in found],
        "takes": found,
    }


def rise_of(
    node: Node, where: tuple[int, ...], wall: int, rule: rule3.Rule, row: Any
) -> tuple[int, int, int]:
    """The exact take at -1 (MG-S1): on the line the fall's sign names (take.fall_of, CS4-S2) the least count d of levels moved away from the before at which the Node's share rises by the wall (a line with no direction, now equal to before, moved away as the fall\'s own sense names it, -1: the bug of H-Children-Charge-Bug-1, the tie end laid as the charged child, struck 2026-10-26), the rise fall_of's form with the sign mirrored, x (w ((now + u d)^2 - now^2) + u d pull) over the weight, the least count by doubling and bisection in comparisons; (k, 0, 0) where the line has no direction (now = before). Returns (the line, the signed count, the rise)."""
    _levels, _fall, k = take.fall_of(node, where, wall, rule, row)
    line = row.lines[k]
    now, before = int(line.now[where]), int(line.before[where])
    u = 1 if now > before else -1
    own, w, reached = at_node(rule.self_coefficient, where), int(rule.wall), 0
    for port, reach in enumerate(rule.reaches):
        reached += at_node(reach, where) * int(line.before[neighbour(node, where, port)])
    pull = own * before + reached
    x, weight = int(node.start_x[where]), share_weight(node.gamma, node.G)

    def rise(d: int) -> int:
        moved = now + u * d
        return int(quotient(x * (w * (moved * moved - now * now) + u * d * pull), weight))

    high = least_at(lambda d: rise(d) >= wall)
    return k, u * high, rise(high)


def light_children(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], walls: list[int], rule: rule3.Rule
) -> tuple[list[int], list[int], list[list[int]], list[list[int] | None], list[list[int]]]:
    """A merger's two light children (MG-S1): at each end the light laid as the exact take at -1 (`rise_of`) on the line the take names, at both ends (the light is never the child's lay, which carries the charge; the former `d == 0` branch the bug of H-Children-Charge-Bug-1, struck 2026-10-26); returns the lays' momentum, each child's Wronskian at its Node, the plane's four levels at each Node before the lay and the exact lays [line, count, rise] (None where the child's lay)."""
    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    stood = [[int(a[w_]) for a in (re.now, re.before, im.now, im.before)] for w_ in (minus, plus)]
    dp_lay, exact, ends = [0] * AXES, [], []  # type: list[int], list[list[int] | None], list[list[int]]
    for where, wall in zip((minus, plus), walls, strict=True):
        k, d, rise = rise_of(node, where, wall, rule, row)
        z = row.lines[k]
        dp = momentum_of(node, z.now, z.before, where, d_now=d, num=row.pair[0])
        move(node, s, k, where, d)
        exact.append([k, d, rise])
        dp_lay, ends = [a + b for a, b in zip(dp_lay, dp, strict=True)], [*ends, list(dp)]
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood, exact, ends
