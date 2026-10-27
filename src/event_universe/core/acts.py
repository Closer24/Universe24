"""The one act beneath Rule3 and its three names (NL-S1, 2026-10-26, the Boss's approval under the owner's delegation of 08:3x UTC; H-Node-Beneath-Rule3-1 and -2, both hands one core): the Node adds; each line holds one number w a + r, and every act of the Node on a line is the carried division of a sum it reads, at a slot, in a direction (`divide`, the former rule3.carried_division kept by name), the slot exchange with the remainder's mirror (`exchange`, the swap at the top) or the lay of a count on a slot (`lay`); the mirror w - 1 - r once per reversal of the line (`mirror`, the former rule3.mirrored) is the one asymmetric letter (CA-S1: the direction is the slot). Rule3's step, the write, the take's move and lay, the riders' divisions and the swap are their compositions; integers or whole-board integer arrays alike, no name, no number, no branch on a row's kind."""

from __future__ import annotations

from typing import Any


def mirror(remainder: Any, wall: Any, reversals: int) -> Any:
    """The one rule of the remainder's mirror (fd1's form, the owner's word of 2026-10-25): a remainder born at the half wall of its division (`born`) is mirrored to wall - 1 - r once for every reversal of its line (time's exchange, the sign's negation), two reversals leaving it; the identity for an even count. A remainder has two mirrors and this is the direction's (The-48-Holds_COMPARISON.md, 2026-10-26, F48-S1 derived and not built): the mirror of a negated line, a reflection or a charge's negation, is the two's complement (wall - r) mod wall, one apart at every nonzero remainder, whose fixed point at an even wall is the birth; the acts spell the direction's alone until F48-S1 is built."""
    return wall - 1 - remainder if reversals & 1 else remainder


def born(wall: Any) -> Any:
    """The remainder every line is born with, the half wall by the division act on 2 (the engine's one birth, spelt once; the former half(wall) at the rows' lines, the riding lines' walls, the riders' division, the phase line and the draw's origin kept by name): the fixed point of the negated line's mirror, (wall - r) mod wall = r, at an even wall, which the direction's mirror wall - 1 - r sends to the half wall less one; so the birth fits the negation's mirror and not the direction's, the third spelling the 48's pair named (The-48-Holds_COMPARISON.md section 5, 2026-10-26)."""
    return divide(wall, 2, 0)[0]


def divide(total: Any, wall: Any, remainder: Any, direction: int = 1) -> tuple[Any, Any]:
    """The one carried division of the law (ALGEBRA.md #the-four-acts, #the-direction): u = total + r, the quotient u div w and the remainder u mod w kept in [0, w) for a total of either sign; the act at -1 is the act at +1 conjugated by the remainder's mirror, written once (CA-S1, the owner's word of 2026-10-26, 07:04 UTC: the direction is the slot; RW-S1)."""
    carried = total + mirror(remainder, wall, direction == -1)
    quotient = carried // wall
    return quotient, mirror(carried - wall * quotient, wall, direction == -1)


def exchange(
    nows: list[Any], befores: list[Any], remainders: list[Any], walls: list[Any], k: Any
) -> tuple[list[Any], list[Any], list[Any]]:
    """The slot exchange of a row at the top with the mirror (X2, the swap; node.exchange): the two slots exchanged through the row's conjugation K (the plane's im line negated), the remainder mirrored once for time's exchange and once more where its own K entry negates the line; an involution."""
    lines = range(len(nows))
    new_nows = [sum((k[r][c] * befores[c] for c in lines if k[r][c]), start=0) for r in lines]
    new_befores = [sum((k[r][c] * nows[c] for c in lines if k[r][c]), start=0) for r in lines]
    return new_nows, new_befores, [mirror(remainders[r], walls[r], 1 + (k[r][r] < 0)) for r in lines]


def lay(slot: Any, count: Any, direction: int = 1) -> Any:
    """The lay: a count of levels laid on one slot in the direction (the write's quotient, the take's move, the seed's, the children's and the emission's lays, each taken back at -1)."""
    return slot + direction * count
