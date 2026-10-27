"""The merger at rest, MG-S1 (H-Merger-At-Rest-1, 2026-10-26, the Boss's order under the owner's delegation; the former CS8-S1 and CS8-S2 as one letter): a child's wall is its own quantum, the share its levels (A, 0 | 0, +-B) hold alone at the Node under its row's rule, the same two integers for every row (`walls_of`; the former board's increment kept by name, equal to it on an empty plane); a record with a gap whose two ends hold a whole quantum each of opposite charge with no current across the Link meets as the conjugate pair (close.meet's rest branch); each child's wall is paid at its own end by the taken record's levels at that Node taken whole by the one lay act at -1, the fall the share the board loses, both ends read before either is written, refused by name `stop` where an end's fall is below the wall (`merger_falls`, `merger_take`; the Link's number read after the stop, so a stopped pair draws nothing); the light is laid at each end as the exact take at -1, on the line the take names, by the least count of levels at which the share rises by the wall (take.fall_of at -1; the former rise_of kept by name), the levels of that lay `light_levels`, the two children's lay one act for the light and the charged child alike (`children_laid`). The close's one take act for every letter (CR-S1 and CR-S2, the owner's word of 2026-10-26, 06:1x UTC): the ends read before any is written (`read_ends`), then written (`write_ends`), the birth's one end, the body's one end and the merger's two alike (`takes`, `summed`)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from event_universe import gram, take
from event_universe.core import rule3
from event_universe.core.ports import AXES
from event_universe.rows import PLANE, Line, zeros
from event_universe.take import frame_nodes, lay, momentum_of, move, recoil

if TYPE_CHECKING:
    from event_universe.node import Node


def child_levels(row: Any, sense: int, a: int, b: int) -> tuple[int, ...]:
    """A child's levels at one end, now and before per line of the row's shape: the one lay of the law laid at the unit (gram.moving, MV-S1's form; the seed's rest lay the same lay at the row's own pair), the now pair (sense A, 0) and the before pair (0, sense B) at the quarter turn along the vector (1, 0, ...), so re_now sense A and im_before B (GP-S1's two integers, A B = T div 2) and 0 on every other level; the former plane-typed four and the child's own spelling kept by name (the Boss's 6414464356: the rest lay and child_at one lay)."""
    lines = gram.moving(1, (sense * a, 0), (0, sense * b), 1, sense)
    return tuple(int(x) for line in lines for x in (line.now, line.before))


def children_laid(
    node: Node,
    s: int,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    levels_of: Callable[[tuple[int, ...], int], tuple[int, ...]],
) -> tuple[list[int], list[int], list[list[int]], list[list[int]]]:
    """The two children laid by the one lay act, the - child at the - end and the + child at the + end, each end's levels by `levels_of` at the end and its sense (the charged child's child_levels at the charge T div 2 with the charge's sign on the re line, GP-S1, the owner's word of 2026-10-26, 04:3x UTC; a merger's light the exact take at -1, `light_levels`, MG-S1), each lay's momentum booked per line of the row at its Node before it is laid (momentum_per_line, the Boss's 6413599502 (b)), the second end read on the board the first lay changed (the sum exact); the former child_at, close.child_laid and light_children one function (NL-S1's stroke 4, 2026-10-26). Returns the lays' momentum summed and per end (dP_lay_ends, the J hands' key, AJ-S2), each child's Wronskian at its Node (its sense, the owner's word 3; -+(T div 2) where the plane stood at nothing) and the record's levels at each Node before the lay (the residue)."""
    row = node.records()[s]
    assert row.pair is not None
    stood, ends = stood_at(row, minus, plus), []
    for where, sense in ((minus, -1), (plus, 1)):
        levels = levels_of(where, sense)
        ends.append(momentum_per_line(node, row.lines, row.pair[0], where, levels))
        lay(node, s, where, levels)
    return [a + b for a, b in zip(*ends, strict=True)], senses_at(row, minus, plus), stood, ends


def light_levels(
    node: Node, s: int, walls: dict[int, int], rule: rule3.Rule, exact: list[list[int] | None]
) -> Callable[[tuple[int, ...], int], tuple[int, ...]]:
    """A merger's light at an end (MG-S1), the levels its lay names: the exact take at -1 (take.fall_of at -1; the former rise_of kept by name) on the line the take names, the count of levels at which the share rises by the child's wall at that end (`walls` by the sense), laid on that line's now alone, at both ends (the light is never the child's lay, which carries the charge; the former `d == 0` branch the bug of H-Children-Charge-Bug-1, struck 2026-10-26), the exact lay [line, count, rise] appended to `exact`; the end's sense enters no level of the light (H-Matter-From-The-Floor's bug (a), open: the merger's orientation reaching the board)."""
    row = node.records()[s]

    def levels_of(where: tuple[int, ...], sense: int) -> tuple[int, ...]:
        count, rise, k = take.fall_of(node, where, walls[sense], rule, row, -1)
        assert count is not None
        z = row.lines[k]
        d = count * (1 if int(z.now[where]) > int(z.before[where]) else -1)
        exact.append([k, d, rise])
        return tuple(d if j == PLANE * k else 0 for j in range(PLANE * len(row.lines)))

    return levels_of


def momentum_per_line(
    node: Node,
    lines: list[Line],
    num: int,
    where: tuple[int, ...],
    levels: tuple[int, ...],
    sign: int = 1,
) -> list[int]:
    """The momentum a lay of `levels` (now, before per line) at the Node books, summed over the record's lines as given, `lines` the board the reading is at (the live board for a lay, the interval's start for a take's end, CL-S2) and `num` the record's pair (take.momentum_of per line; the form generic in the lines)."""
    found = [0] * AXES
    for j, line in enumerate(lines):
        dj = momentum_of(
            node,
            line.now,
            line.before,
            where,
            sign * levels[PLANE * j],
            sign * levels[PLANE * j + 1],
            num,
        )
        found = [a + b for a, b in zip(found, dj, strict=True)]
    return found


def walls_of(
    node: Node,
    s: int,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    rule: rule3.Rule,
    cache: dict[tuple[int, int, tuple[int, ...]], int],
) -> tuple[int, int]:
    """Each child's wall, its own quantum (MG-S1, CS8-S2): the child laid by the one lay act at its end on zero lines of the row's shape (the row's lines held and put back), the share summed under the row's rule at the board's content over the end and its six neighbours (gram.share at that window: the zero lines' share is 0 everywhere else), the lines discarded; the same two integers for every row and every Node of one content, read once per end and row in a close (`cache`: no line of the board enters it); the former reading, the board's increment where the plane already stands, kept by name."""
    row = node.records()[s]
    held, found = row.lines, []
    for where, sense in ((minus, -1), (plus, 1)):
        if (s, sense, where) not in cache:
            row.lines = [
                Line(zeros(node.shape), zeros(node.shape), line.rem, line.wall) for line in held
            ]
            lay(node, s, where, child_levels(row, sense, node.A, node.B))
            window = sorted(set(frame_nodes(node, where)))
            cache[(s, sense, where)] = sum(int(v) for v in gram.share(node, row.lines, rule, window))
        found.append(cache[(s, sense, where)])
    row.lines = held
    return found[0], found[1]


def share_fall(
    node: Node,
    rec: int,
    rule: rule3.Rule,
    where: tuple[int, ...],
    levels: tuple[int, ...],
    cache: dict[tuple[int, tuple[int, ...]], int],
) -> int:
    """The share the board loses by a lay at -1 of the levels at the Node (laid and laid back): the lay changes the share at the Node and its six neighbours alone, so the fall is their shares' difference, bit for bit the board's (the former read of the whole board's share, kept by name); the shares as they stand kept in `cache` per record and Node for the close until a take writes."""
    row, window = node.records()[rec], sorted(set(frame_nodes(node, where)))
    unread = [at for at in window if (rec, at) not in cache]
    for at, v in zip(unread, gram.share(node, row.lines, rule, unread) if unread else [], strict=True):
        cache[(rec, at)] = int(v)
    before = sum(cache[(rec, at)] for at in window)
    lay(node, rec, where, levels, -1)
    after = sum(int(v) for v in gram.share(node, row.lines, rule, window))
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


Read = tuple[tuple[int, ...], int, Any, int, int | None, int, int]


def merger_end(node: Node, rec: int, read: Read) -> tuple[dict[str, Any], list[int]]:
    """One end of a merger's take written: its whole levels laid at -1, the end's entry with the momentum the start books and its recoil, and the live board's momentum less the start's (the cross term's share)."""
    where, wall, levels, fall, _k, _rem_was, _owed = read
    row = node.records()[rec]
    assert row.pair is not None
    live = momentum_per_line(node, row.lines, row.pair[0], where, tuple(levels), -1)
    moment = momentum_per_line(node, node.start_lines[rec], row.pair[0], where, tuple(levels), -1)
    lay(node, rec, where, levels, -1)
    node.closes[where] -= 1
    size = sum(abs(x) for x in levels)
    entry = dict(
        node=list(where),
        taken=fall,
        booked=wall,
        levels=size,
        taken_levels=list(levels),
        dP_take=moment,
        **recoil(node, where, moment, int(node.start_clock[where]), 1),
    )
    return entry, [a - b for a, b in zip(live, moment, strict=True)]


def light_end(node: Node, rec: int, read: Read) -> dict[str, Any]:
    """One end of the light's take written: the taken line moved toward its before by the count (take.move, CR-S1), the fall above what was owed its new remainder (EX-S1), the momentum booked and its recoil."""
    where, wall, levels, fall, k, rem_was, owed = read
    row = node.records()[rec]
    assert row.pair is not None and k is not None
    z = row.lines[k]
    now, before = int(z.now[where]), int(z.before[where])
    toward = 1 if before > now else -1
    move(node, rec, k, where, toward * levels)
    node.closes[where] += 1
    node.take_rem[where] = fall - owed
    node.last_dp = momentum_of(node, z.now, z.before, where, d_now=toward * levels, num=row.pair[0])
    node.last_recoil = recoil(node, where, node.last_dp, int(node.start_clock[where]), 1)
    return {
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
        **node.last_recoil,
    }


def write_ends(
    node: Node,
    reads: list[Read],
    rec: int,
    at: tuple[int, ...] | None = None,
) -> list[dict[str, Any]]:
    """The take act's writes after its reads (CR-S2): at the gap-0 row the end's line moved toward its before by the count (take.move, CR-S1), the fall above what was owed its new remainder (EX-S1), the momentum booked; at a record with a gap the end's levels taken whole by the lay act at -1, the momentum each end books read at the record's levels at the interval's start (node.start_lines, CL-S2: so the two ends of one Link commute and the per-Node attribution does not depend on the order the meeting named them) and the cross term of the two moves, the live board's sum less the start's, nonzero on the Link's own axis alone, booked once at the meeting's own Node `at` after both ends (the levels taken whole keep their moment, the board the take writes, MG-S1). Returns each end's take as the log carries it, the cross under the last end's `cross` for `summed` to lift; the former take_line and merger_take kept by name."""
    row = node.records()[rec]
    found: list[dict[str, Any]] = []
    cross = [0] * AXES
    for read in reads:
        if row is not node.emitter():
            entry, moved = merger_end(node, rec, read)
            cross = [c + m for c, m in zip(cross, moved, strict=True)]
            found.append(entry)
            continue
        found.append(light_end(node, rec, read))
    if at is not None and len(found) > 1 and row is not node.emitter():
        booked = recoil(node, at, cross, int(node.start_clock[at]), 1)
        found[-1]["cross"] = {"node": list(at), "dP": cross, **booked}
    return found


def takes(
    node: Node,
    ends: list[tuple[tuple[int, ...], int]],
    rule: rule3.Rule,
    cause: int,
    rec: int | None = None,
    draw: Callable[[], Any] | None = None,
    cache: dict[tuple[int, tuple[int, ...]], int] | None = None,
    at: tuple[int, ...] | None = None,
) -> list[dict[str, Any]] | None:
    """The close's one take act for every letter alike (CR-S2): the walls booked at each end paid by one exact take at that end from the taken row (the gap-0 row's where none is named: a body's take), every end read before any is written (`read_ends`) and refused by name at the first that cannot pay, the Link's number drawn between the reads and the writes where the letter draws one (`draw`, the merger's; None drawn refuses the take), then every end written (`write_ends`); the birth's list one end of its children's walls summed, the body's one end of its unit, the merger's its two ends. Returns each end's take, or None."""
    taken = node.records().index(node.emitter()) if rec is None else rec
    reads = read_ends(node, ends, rule, cause, taken, cache)
    if reads is None or (draw is not None and draw() is None):
        return None
    return write_ends(node, reads, taken, at)


def summed(found: list[dict[str, Any]]) -> dict[str, Any]:
    """One take's numbers as the log carries them: one end's own fields; two ends' summed, each end's own under `takes` (a merger's whole levels as the taken and the taker, no line), the cross term's booking lifted from the last end under `cross` (CL-S2)."""
    if len(found) == 1:
        return {k: v for k, v in found[0].items() if k != "node"}
    whole = "taken_levels" in found[0]
    cross = found[-1].get("cross")
    if cross is not None:
        del found[-1]["cross"]
    return {
        **({} if cross is None else {"cross": cross}),
        "taken": sum(t["taken"] for t in found),
        "booked": sum(t["booked"] for t in found),
        "levels": sum(t["levels"] for t in found),
        "taken_now_was": [t["taken_levels" if whole else "taken_now_was"] for t in found],
        "taker": [t["taken_levels" if whole else "taker"] for t in found],
        "dP_take": [sum(x) for x in zip(*(t["dP_take"] for t in found), strict=True)],
        "taken_line": [None if whole else t["taken_line"] for t in found],
        "takes": found,
    }


def stood_at(row: Any, minus: tuple[int, ...], plus: tuple[int, ...]) -> list[list[int]]:
    """The record's levels standing at the two ends, now and before per line in the row's order (the log's `stood`; generic in the lines)."""
    return [[int(x[w_]) for line in row.lines for x in (line.now, line.before)] for w_ in (minus, plus)]


def senses_at(row: Any, minus: tuple[int, ...], plus: tuple[int, ...]) -> list[int]:
    """The record's charge at the two ends after the lay (gram.charge, the plane's Wronskian re_now im_before - im_now re_before; generic in the lines), the children's W as the log names it."""
    charge = gram.charge(row.shape, row.lines)
    return [int(charge[w_]) for w_ in (minus, plus)]
