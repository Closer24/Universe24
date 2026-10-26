"""The merger at rest, MG-S1 (H-Merger-At-Rest-1, 2026-10-26, the Boss's order under the owner's delegation; the former CS8-S1 and CS8-S2 as one letter): a child's wall is its own quantum, the share its levels (A, 0 | 0, +-B) hold alone at the Node under its row's rule, the same two integers for every row (`walls_of`; the former board's increment kept by name, equal to it on an empty plane); a record with a gap whose two ends hold a whole quantum each of opposite charge with no current across the Link meets as the conjugate pair (close.meet's rest branch); each child's wall is paid at its own end by the taken record's levels at that Node taken whole by the one lay act at -1, the fall the share the board loses, both ends read before either is written, refused by name `stop` where an end's fall is below the wall (`merger_take`); the light is laid at each end as the exact take at -1, on the line the take names, by the least count of levels at which the share rises by the wall (`rise_of`), as the child's lay where the line has no direction (`light_children`)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from event_universe import gram
from event_universe.core import rule3
from event_universe.core.ports import AXES
from event_universe.core.rule3 import half, quotient, share_weight
from event_universe.links import cross
from event_universe.rows import Line, zeros
from event_universe.take import at_node, fall_of, lay, momentum_of, neighbour

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
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> tuple[int, int]:
    """Each child's wall, its own quantum (MG-S1, CS8-S2): the child laid by the one lay act at its end on zero lines of the row's shape (the row's lines held and put back), the share summed over the board under the row's rule at the board's content, the lines discarded; the same two integers for every row and every Node of one content; the former reading, the board's increment where the plane already stands, kept by name."""
    row = node.records()[s]
    assert row.pair is not None
    rule = node.rule(row.pair, c, factors)
    held, found = row.lines, []
    for where, sense in ((minus, -1), (plus, 1)):
        row.lines = [Line(zeros(node.shape), zeros(node.shape), line.rem, line.wall) for line in held]
        child_at(node, s, where, sense)
        found.append(int(sum(int(x) for x in gram.share(node, row.lines, rule).reshape(-1))))
    row.lines = held
    return found[0], found[1]


def levels_at(row: Any, where: tuple[int, ...]) -> tuple[int, ...]:
    """A record's levels at the Node as one lay names them (now, before per line)."""
    return tuple(int(a[where]) for line in row.lines for a in (line.now, line.before))


def merger_take(
    node: Node,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    walls: tuple[int, int],
    rule: rule3.Rule,
    rec: int,
    refused: Callable[..., None],
) -> dict[str, Any] | None:
    """The merger's take (MG-S1, the birth's lay read at -1): at each end the taken record's levels at the Node read and the share the board loses by their lay at -1 read (laid and laid back), both ends read before either is written; refused by name `stop` where an end's fall is below its child's wall; then each end's levels taken whole by the one lay act at -1, its momentum booked on both lines. Returns the log's take fields, the two ends' takes summed and each end's own under `takes` (its `taken_levels` the levels taken, unclick laying them back), or None."""
    row = node.records()[rec]
    assert row.pair is not None

    def total() -> int:
        return int(sum(int(x) for x in node.share(row.lines, rule).reshape(-1)))

    ends = []
    for where, wall in zip((minus, plus), walls, strict=True):
        levels = levels_at(row, where)
        before = total()
        lay(node, rec, where, levels, -1)
        fall = before - total()
        lay(node, rec, where, levels, 1)
        ends.append((where, wall, levels, fall))
    for where, wall, _levels, fall in ends:
        if fall < wall:
            refused(node, where, "stop", fall=fall, walls=wall, row=rec)
            return None
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
