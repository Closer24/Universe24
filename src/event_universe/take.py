"""The close's reads and writes at one Node: the one-Link read of a number on the frame's digit lattices (`read_number`), the exact take of the taken row's levels by the share's fall on the line the fall's sign chooses (`fall_of`, `take_at`), the one lay act (`lay`, on one line for the take), the lattice momentum a move books (`momentum_of`) and the refusal by name (`refused`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import rule3
from event_universe.core.ports import AXES, PORT_SIDES, PORTS, port_of, wrap
from event_universe.core.rule3 import half, lattice, mirrored, quotient, remainder
from event_universe.links import cross
from event_universe.rows import LEVELS, PLANE, Line, Row

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


def read_number(
    node: Node, at: tuple[int, ...], rules: list[tuple[Line, rule3.Rule]], unit: int
) -> tuple[int, int] | None:
    """The one-Link read: every line's remainder at the Node on the Node's own lattice F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the Link's lattice gcd(w, R_ji), the digit r div F, the base w div F + 1, sorted by value, composed modulo M = the taken row's unit times the planes' count, the shape-2 records the draw names (the carry); refused by name at the origin (every remainder at the half) and where every lattice is coarse (A48-S1's read in the laid frame, a48b's form, built at 05cca50 and reverted: the 48 on the clicks held to the interval 10 and parted at 11 on every reflection at the tie of the sign row's time line's write remainder, and the cycle seed's draws fell on the origin; it returns with its mend)."""
    modulus = unit * sum(1 for r in node.records() if r.shape == PLANE)
    nodes, digits = frame_nodes(node, at), []
    origin, coarse, w_half = True, True, half(node.w)
    for line, r in rules:
        for k, n in enumerate(nodes):
            key = (id(r), k, n)
            if key not in node.lattices:
                wl = at_node(line.wall, n)
                node.lattices[key] = (
                    lattice(wl, at_node(r.mass, n), *[at_node(x, n) for x in r.reaches])
                    if k == 0
                    else lattice(wl, at_node(r.reaches[k - 1], n))
                )
            f = node.lattices[key]
            rem, values = node.digit_of(int(line.rem[n]), quotient(at_node(line.wall, n), f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
            coarse = coarse and values <= AXES
            digits.append((quotient(rem, f), values + 1))
    if origin or coarse:
        node.counts["refused_origin"] += origin
        return None
    carry, room = 0, 1
    for d, b in sorted(digits):
        carry = remainder(carry * b + d, modulus)
        room = min(room * b, modulus)
    return carry, room


def fall_of(
    node: Node, at: tuple[int, ...], walls: int, r: rule3.Rule, row: Row
) -> tuple[int | None, int, int]:
    """The exact take at the Node in the carrier's unit (PM-S1) on the line the fall's sign chooses (CS4-S2, the owner's word of 2026-10-25 through the Boss: the taken record's line whose level now stands farthest from its before, the largest now^2 - before^2, the first line where equal, so the take is covariant under the record's quarter turn; the former first line kept by name): the taken line's now moved toward its before by the least count of levels at which the Node's share falls by the walls; the fall f(s) an exact quadratic in s scaled by X over 2 Gamma^3 G^2, its least root by largest_below checked at the neighbours, the exact guard where the root misses; (None, the full fall) where the full move cannot pay."""
    pairs = [(int(line.now[at]), int(line.before[at])) for line in row.lines]
    gaps = [n * n - b * b for n, b in pairs]
    k = gaps.index(max(gaps))
    line = row.lines[k]
    now, before = int(line.now[at]), int(line.before[at])
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

    dist = abs(now - before)
    full = fall(dist)
    if full < walls:
        return None, full, k
    for s in rule3.least_root(-w * x, -((w + w) * now + pull) * t * x, walls * weight, dist):
        if s <= dist and fall(s) >= walls:
            return s, fall(s), k
    return (*next(((s, fall(s)) for s in range(1, dist + 1) if fall(s) >= walls), (dist, full)), k)


def lay(node: Node, rec: int, where: Any, levels: Any, sign: int = 1, line: int | None = None) -> None:
    """The one lay act: a record's levels (now, before per line: re_now, re_before, im_now, im_before for a plane) added at the Node `where` (or over the board), taken back with sign -1; with `line` named, `levels` is one count added to that line's now alone (the take's move and its undoing, CS4-S2)."""
    lines = node.records()[rec].lines
    if line is not None:
        levels = tuple(levels if j == LEVELS * line else 0 for j in range(LEVELS * len(lines)))
    for line_, now, before in zip(lines, levels[0::LEVELS], levels[1::LEVELS], strict=True):
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


def take_at(
    node: Node, at: tuple[int, ...], walls: int, rule: rule3.Rule, cause: int, rec: int | None = None
) -> tuple[int, int, int, int, int] | None:
    """One exact take at a Node of the walls booked from the taken row (the gap-0 row's where none is named: a body's take) at its rule, on the line the fall's sign chooses (`fall_of`, CS4-S2): its level now moved toward its before by the least count of levels at which the Node's share falls by the walls; refused by name where the fall cannot reach the walls (the stop). Returns (levels, fall, the line's now before the take, its before, the line taken) or None."""
    taken = node.records().index(node.emitter()) if rec is None else rec
    row = node.records()[taken]
    levels, fall, k = fall_of(node, at, walls, rule, row)
    z = row.lines[k]
    if levels is None:
        node.counts["refused_stop"] += cause
        entry = {"event": "refused", "i": node.interval, "node": list(at), "cause": "stop"}
        node.log.append(entry | {"fall": fall, "walls": walls, "row": taken})
        return None
    now, before = int(z.now[at]), int(z.before[at])
    toward = 1 if before > now else -1
    lay(node, taken, at, toward * levels, line=k)
    node.closes[at] += 1
    assert row.pair is not None
    node.last_dp = momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=row.pair[0])
    return levels, fall, now, before, k
