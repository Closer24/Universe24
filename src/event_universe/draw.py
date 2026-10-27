"""The draw, the one-Link read of a number at a Node (the former take.read_number, moved whole; the take's module holds the take and the lay alone): every line's remainder at the Node on the Node's own lattice and at each neighbour on the Link's lattice, the digits composed modulo the taken row's unit times the planes' count; refused by name at the origin and where every lattice is coarse."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.core import acts, rule3
from event_universe.core.rule3 import carries, pitch, remainder
from event_universe.core.spokes import AXES
from event_universe.trains import HAND, Gear
from event_universe.unwind import at_clock, window_clocks

if TYPE_CHECKING:
    from event_universe.clock import Clock


def vernier(
    node: Clock, at: tuple[int, ...], rules: list[tuple[Gear, rule3.Gearing]], unit: int
) -> tuple[int, int] | None:
    """The one-Link read: every line's remainder at the Node on the Node's own lattice F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the Link's lattice gcd(w, R_ji), the digit r div F, the base w div F + 1, sorted by value, composed modulo M = the taken row's unit times the planes' count, the shape-2 records the draw names (the carry); refused by name at the origin (every remainder at the half) and where every lattice is coarse (A48-S1's read in the laid frame, a48b's form, built at 05cca50 and reverted: the 48 on the clicks held to the interval 10 and parted at 11 on every reflection at the tie of the sign row's time line's write remainder, and the cycle seed's draws fell on the origin; it returns with its mend)."""
    modulus = unit * sum(1 for r in node.hands() if r.size == HAND)
    nodes, digits, origin, coarse, w_half = window_clocks(node, at), [], True, True, acts.mid(node.teeth)
    for line, r in rules:
        for k, n in enumerate(nodes):
            wl, key = at_clock(line.teeth, n), (id(r), k, n)
            if key not in node.pitches:
                node.pitches[key] = (
                    pitch(wl, at_clock(r.spring, n), *[at_clock(x, n) for x in r.grips])
                    if k == 0
                    else pitch(wl, at_clock(r.grips[k - 1], n))
                )
            rem, values = int(line.fine[n]), carries(wl, f := node.pitches[key])
            origin = origin and rem in (w_half, acts.flip(w_half, node.teeth, 1))
            coarse = coarse and values <= AXES
            digits.append((carries(rem, f), values + 1))
    if origin or coarse:
        node.counts["refused_origin"] += origin
        return None
    carry, room = 0, 1
    for d, b in sorted(digits):
        carry = remainder(carry * b + d, modulus)
        room = min(room * b, modulus)
    return carry, room
