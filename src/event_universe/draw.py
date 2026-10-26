"""The draw, the one-Link read of a number at a Node (the former take.read_number, moved whole; the take's module holds the take and the lay alone): every line's remainder at the Node on the Node's own lattice and at each neighbour on the Link's lattice, the digits composed modulo the taken row's unit times the planes' count; refused by name at the origin and where every lattice is coarse."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.core import acts, rule3
from event_universe.core.ports import AXES
from event_universe.core.rule3 import half, lattice, quotient, remainder
from event_universe.rows import PLANE, Line
from event_universe.take import at_node, frame_nodes

if TYPE_CHECKING:
    from event_universe.node import Node


def read_number(
    node: Node, at: tuple[int, ...], rules: list[tuple[Line, rule3.Rule]], unit: int
) -> tuple[int, int] | None:
    """The one-Link read: every line's remainder at the Node on the Node's own lattice F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the Link's lattice gcd(w, R_ji), the digit r div F, the base w div F + 1, sorted by value, composed modulo M = the taken row's unit times the planes' count, the shape-2 records the draw names (the carry); refused by name at the origin (every remainder at the half) and where every lattice is coarse (A48-S1's read in the laid frame, a48b's form, built at 05cca50 and reverted: the 48 on the clicks held to the interval 10 and parted at 11 on every reflection at the tie of the sign row's time line's write remainder, and the cycle seed's draws fell on the origin; it returns with its mend)."""
    modulus = unit * sum(1 for r in node.records() if r.shape == PLANE)
    nodes, digits, origin, coarse, w_half = frame_nodes(node, at), [], True, True, half(node.w)
    for line, r in rules:
        for k, n in enumerate(nodes):
            wl, key = at_node(line.wall, n), (id(r), k, n)
            if key not in node.lattices:
                node.lattices[key] = (
                    lattice(wl, at_node(r.mass, n), *[at_node(x, n) for x in r.reaches])
                    if k == 0
                    else lattice(wl, at_node(r.reaches[k - 1], n))
                )
            rem, values = int(line.rem[n]), quotient(wl, f := node.lattices[key])
            origin = origin and rem in (w_half, acts.mirror(w_half, node.w, 1))
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
