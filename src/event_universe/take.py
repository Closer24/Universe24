"""The close's reads and writes at one Node: the one-Link read of a number on the frame's digit lattices (`read_number`), the exact take of the gap-0 line's levels by the share's fall (`fall_of`, `take_at`), the one lay act (`lay`), the lay of one quantum's amplitude (`lay_amplitude`) and the lattice momentum a move books (`momentum_of`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import paces, rule3
from event_universe.core.ports import AXES, PORT_SIDES, wrap
from event_universe.core.rule3 import half, lattice, quotient, remainder
from event_universe.rows import PLANE, Line

if TYPE_CHECKING:
    from event_universe.node import Node


def neighbour(node: Node, at: tuple[int, ...], axis: int, side: int) -> tuple[int, ...]:
    """The Node one Link along the axis toward the side, on the torus."""
    return tuple(wrap(at[a] + (side if a == axis else 0), node.cube) for a in range(AXES))


def frame_nodes(node: Node, at: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The Node and its six neighbours in Port order."""
    return [at] + [neighbour(node, at, axis, side) for axis, side in PORT_SIDES]


def at_node(x: Any, at: tuple[int, ...]) -> int:
    """A rule's integer at a Node (a walled row's reaches are the one integer 0)."""
    return int(np.asarray(x)[at]) if np.ndim(x) else int(x)


def read_number(
    node: Node, at: tuple[int, ...], rules: list[tuple[Line, rule3.Rule]]
) -> tuple[int, int] | None:
    """The one-Link read: every line's remainder at the Node on the Node's own lattice F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the Link's lattice gcd(w, R_ji), the digit r div F, the base w div F + 1, sorted by value, composed modulo M = the gap-0 unit times the planes' count (the carry); refused by name at the origin (every remainder at the half) and where every lattice is coarse."""
    modulus = node.unit_gap0 * len(node.records())
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
            origin = origin and rem in (w_half - 1, w_half)
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


def fall_of(
    node: Node, at: tuple[int, ...], walls: int, r: rule3.Rule, line: Line
) -> tuple[int | None, int]:
    """The exact take at the Node: the gap-0 line's now moved toward its before by the least count of levels at which the Node's share falls by the walls; the fall f(s) an exact quadratic in s, its least root by largest_below checked at the neighbours, the exact guard where the root misses; (None, the full fall) where the full move cannot pay."""
    now, before = int(line.now[at]), int(line.before[at])
    if now == before:
        return None, 0
    t = 1 if before > now else -1
    own, w = int(np.asarray(r.self_coefficient)[at]), int(r.wall)
    reached = 0
    for (axis, side), reach in zip(PORT_SIDES, r.reaches, strict=True):
        reached += int(np.asarray(reach)[at]) * int(line.before[neighbour(node, at, axis, side)])
    pace = int(np.asarray(paces.link_pace_of(node.gamma, node.start_content), dtype=object)[at])
    weight = 2 * pace * pace * node.G * node.G + (1 if pace == 0 else 0)

    def fall(s: int) -> int:
        return int(
            quotient(w * (now * now - (now + t * s) ** 2) - t * s * (own * before + reached), weight)
        )

    dist = abs(now - before)
    full = fall(dist)
    if full < walls:
        return None, full
    for s in rule3.least_root(-w, -(2 * w * now + own * before + reached) * t, walls * weight, dist):
        if s <= dist and fall(s) >= walls:
            return s, fall(s)
    for s in range(1, dist + 1):
        if fall(s) >= walls:
            return s, fall(s)
    return dist, full


def lay(node: Node, rec: int, where: Any, levels: tuple[Any, Any, Any, Any], sign: int = 1) -> None:
    """The one lay act: a record's four levels (re_now, re_before, im_now, im_before) added at the Node `where` (or over the board), taken back with sign -1."""
    re, im = node.records()[rec].lines
    for line, now, before in ((re, levels[0], levels[1]), (im, levels[2], levels[3])):
        line.now[where] = line.now[where] + sign * now
        line.before[where] = line.before[where] + sign * before


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
        up, down = neighbour(node, at, a, 1), neighbour(node, at, a, -1)
        found.append(
            2
            * num
            * (
                d_now * (int(line_before[down]) - int(line_before[up]))
                + d_before * (int(line_now[up]) - int(line_now[down]))
            )
        )
    return found


def take_at(
    node: Node, at: tuple[int, ...], walls: int, r_gap0: rule3.Rule, cause: int
) -> tuple[int, int, int, int] | None:
    """One exact take at a Node of the walls booked: the gap-0 line's level now moved toward its before by the least count of levels at which the Node's share falls by the walls; refused by name where the fall cannot reach the walls (the stop). Returns (levels, fall, the gap-0 line's now before the take, its before) or None."""
    gap0 = node.row(PLANE, gap=0)
    z = gap0.lines[0]
    levels, fall = fall_of(node, at, walls, r_gap0, z)
    if levels is None:
        node.counts["refused_stop"] += cause
        node.log.append(
            {
                "event": "refused",
                "i": node.interval,
                "node": list(at),
                "cause": "stop",
                "fall": fall,
                "walls": walls,
            }
        )
        return None
    now, before = int(z.now[at]), int(z.before[at])
    toward = 1 if before > now else -1
    lay(node, node.records().index(gap0), at, (toward * levels, 0, 0, 0))
    node.closes[at] += 1
    assert gap0.pair is not None
    node.last_dp = momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=gap0.pair[0])
    return levels, fall, now, before


def lay_amplitude(
    node: Node, s: int, at: tuple[int, ...], c: Any, factors: tuple[Any, ...], pace: Any
) -> int:
    """The lay of one quantum: the child's record laid at the Node with the least amplitude A at which its own share reads one quantum of its unit at the Node's paces, (2 D + SUM_j R_j) A^2 >= unit x 4 p^2 G^2 (the frame share's term of a lone record with now = before = A)."""
    r = node.rule_of(node.records()[s], c, factors)
    reaches = sum(int(np.asarray(x)[at]) for x in r.reaches)
    mass = 2 * int(np.asarray(r.wall)) - int(np.asarray(r.self_coefficient)[at]) - reaches
    weight = 2 * mass + reaches
    pc = int(np.asarray(pace, dtype=object)[at])
    target = node.units[s] * 4 * pc * pc * node.G * node.G
    if weight <= 0:
        return node.A
    amplitude = rule3.largest_below(quotient(target, weight))
    while weight * amplitude * amplitude < target:
        amplitude += 1
    return amplitude
