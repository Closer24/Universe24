"""The close's reads and writes at one Node: the one-Link read of a number on the frame's digit lattices (`read_number`), the exact take of the taken row's levels by the share's fall on the line the fall's sign chooses (`fall_of`; the take act at a list of ends is merger.takes, CR-S2), the one lay act (`lay`) and the take's move as the write's form (`move`, CR-S1), the lattice momentum a move books (`momentum_of`) and the refusal by name (`refused`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import rule3
from event_universe.core.ports import AXES, PORT_SIDES, PORTS, port_of, wrap
from event_universe.core.rule3 import quotient
from event_universe.links import cross
from event_universe.rows import PLANE, Row

if TYPE_CHECKING:
    from event_universe.node import Node


def neighbour(node: Node, at: tuple[int, ...], port: int) -> tuple[int, ...]:
    """The Node beyond the Port of the Node `at`, on the torus (fd2, U3): the one spelling of a neighbour's place, as `across` is the one read of a neighbour's array."""
    axis, side = PORT_SIDES[port]
    return tuple(wrap(at[a] + (side if a == axis else 0), node.cube) for a in range(AXES))


def frame_nodes(node: Node, at: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The Node and its six neighbours in Port order."""
    return [at] + [neighbour(node, at, port) for port in range(PORTS)]


def at_node(x: Any, at: tuple[int, ...]) -> int:
    """A rule's integer at a Node (a walled row's reaches are the one integer 0)."""
    return int(np.asarray(x)[at]) if np.ndim(x) else int(x)


def fall_of(
    node: Node, at: tuple[int, ...], walls: int, r: rule3.Rule, row: Row
) -> tuple[int | None, int, int]:
    """The exact take at the Node in the carrier's unit (PM-S1) on the line the fall's sign chooses (CS4-S2, the owner's word of 2026-10-25 through the Boss: the taken record's line whose level now stands farthest from its before, the largest now^2 - before^2, the first line where equal, so the take is covariant under the record's quarter turn; the former first line kept by name): the taken line's now moved toward its before by the least count of levels at which the Node's share falls by the walls (0 where nothing is owed, EX-S1); the fall f(s) an exact quadratic in s scaled by X over 2 Gamma^3 G^2, its least root by largest_below checked at the neighbours, the exact guard where the root misses; (None, the full fall) where the full move cannot pay."""
    gaps = [n * n - b * b for n, b in ((int(z.now[at]), int(z.before[at])) for z in row.lines)]
    k = gaps.index(max(gaps))
    line = row.lines[k]
    now, before = int(line.now[at]), int(line.before[at])
    if walls <= 0:
        return 0, 0, k
    if now == before:
        return None, 0, k
    t = 1 if before > now else -1
    own, w, reached = int(np.asarray(r.self_coefficient)[at]), int(r.wall), 0
    for port, reach in enumerate(r.reaches):
        reached += int(np.asarray(reach)[at]) * int(line.before[neighbour(node, at, port)])
    pull = own * before + reached
    x, weight = int(node.start_x[at]), rule3.share_weight(node.gamma, node.G)

    def fall(s: int) -> int:
        moved = now + t * s
        return int(quotient(x * (w * (now * now - moved * moved) - t * s * pull), weight))

    full = fall(dist := abs(now - before))
    if full < walls:
        return None, full, k
    for s in rule3.least_root(-w * x, -((w + w) * now + pull) * t * x, walls * weight, dist):
        if s <= dist and fall(s) >= walls:
            return s, fall(s), k
    return (*next(((s, fall(s)) for s in range(1, dist + 1) if fall(s) >= walls), (dist, full)), k)


def lay(node: Node, rec: int, where: Any, levels: Any, sign: int = 1) -> None:
    """The one lay act: a record's levels (now, before per line: re_now, re_before, im_now, im_before for a plane) added at the Node `where` (or over the board), taken back with sign -1 (the seed's forms, the children, a merger's ends taken whole and their undoing); the take's move on one line is `move` (CR-S1)."""
    lines = node.records()[rec].lines
    for line_, now, before in zip(lines, levels[0::PLANE], levels[1::PLANE], strict=True):
        line_.now[where] = line_.now[where] + sign * now
        line_.before[where] = line_.before[where] + sign * before


def momentum_of(
    node: Node,
    line_now: Any,
    line_before: Any,
    at: tuple[int, ...],
    d_now: int = 0,
    d_before: int = 0,
    num: int = 1,
) -> list[int]:
    """The change of the lattice momentum P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) when a line's level now at the Node moves by d_now and its level before by d_before: 2 num [d_now (before_(i-a) - before_(i+a)) + d_before (now_(i+a) - now_(i-a))] per axis."""
    found = []
    for a in range(AXES):
        up, down = neighbour(node, at, port_of(a, 0)), neighbour(node, at, port_of(a, 1))
        dn, db = int(line_now[down]) - int(line_now[up]), int(line_before[down]) - int(line_before[up])
        found.append((num + num) * cross(d_now, d_before, dn, db))
    return found


def move(node: Node, rec: int, k: int, at: tuple[int, ...], count: int) -> None:
    """The take's move, the Node's write act at one Node (CR-S1, the owner's word of 2026-10-26, 06:1x UTC): one carried division at the line's own wall of the exact numerator, the count times the wall, the quotient count laid on the line's level now by the one lay act and the remainder unmoved; the take forward, its lay-back and its undoing are this one act with the count's sign; not the interval's write act, whose wall is the line's write wall, which the taken line does not hold. The former take_at (one Node's take, EX-S1's remainder owed at it) is kept by name: its act is merger.takes."""
    lines = node.records()[rec].lines
    wall = at_node(lines[k].wall, at)
    q, _unmoved = rule3.carried_division(count * wall, wall, int(lines[k].rem[at]), 1)
    lay(node, rec, at, tuple(q if j == PLANE * k else 0 for j in range(PLANE * len(lines))))
