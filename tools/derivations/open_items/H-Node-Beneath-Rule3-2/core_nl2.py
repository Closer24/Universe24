"""The lean core of the Node (H-Node-Beneath-Rule3-2): three primitives and every state-moving act of the Node and its six Links as their composition; integers or whole-board integer arrays alike, no name, no number of a universe, no branch on a row's kind. The reads (the paces, the Link factors, the frames, the turn, the arrivals, the stress) are readings and enter as integers; the record (the log, the frame, the census) is kept nowhere here."""

from __future__ import annotations

from typing import Any


def divide(total: Any, wall: Any, rem: Any, direction: int = 1) -> tuple[Any, Any]:
    """P1, the carried division with the direction: u = sigma total + rem, the quotient sigma (u div wall), the remainder u mod wall in [0, wall) (ALGEBRA.md, The direction); at -1 bit for bit rule3.carried_division's mirror form, since floor((wall - 1 - u) / wall) = -floor(u / wall)."""
    u = direction * total + rem
    q = u // wall
    return direction * q, u - wall * q


def mirror(rem: Any, wall: Any, reversals: Any) -> Any:
    """The remainder's mirror wall - 1 - rem once per odd count of reversals: the complement of the floor's interval, the one asymmetric piece of the letter (CA-S1), itself a reading of P1 on the complement, divide(-1 - rem, wall, 0)[1]."""
    odd = reversals - 2 * (reversals // 2)
    return rem + odd * (wall - 1 - rem - rem)


def exchange(now: Any, before: Any, rem: Any, wall: Any, sign: Any = 1) -> tuple[Any, Any, Any]:
    """P2, the slot exchange with the mirror: the two slots exchanged and both signed by the row's K entry (the plane's im line -1), the remainder mirrored once for time's exchange and once more where the sign negates the line (node.exchange's rule); an involution."""
    return sign * before, sign * now, mirror(rem, wall, 1 + (sign < 0))


def lay(slot: Any, count: Any, direction: int = 1) -> Any:
    """P3, the lay: a count of levels laid on one slot in the direction (take.lay with the sign)."""
    return slot + direction * count


def rotate(a: Any, y: Any, rem: Any, own: Any, wall: Any, flux: Any, direction: int) -> tuple[Any, Any, Any]:
    """Rule3's step of one line (node.rotate's one line): the slots (a, y) in the direction's order, the total S a - w y + the Links' part, P1 on it, the new level on the slot the direction names and a on the other: P1 then the slot shift (P2 with the new level laid)."""
    q, rem2 = divide(own * a - wall * y + flux, wall, rem, direction)
    return q, a, rem2


def placed(lead: Any, start: Any, direction: int) -> tuple[Any, Any]:
    """The slot shift of the step: the quotient on the slot the direction names and the start level on the other, (lead, start) forward and (start, lead) backward: P2's exchange of the two slots followed by the lay of the new level on the slot it names (read before written, CR-S2)."""
    return (lead, start) if direction == 1 else (start, lead)


def write(now: Any, wr: Any, numerator: Any, wwall: Any, direction: int) -> tuple[Any, Any]:
    """The write (node.write): P1 at the line's write wall with the write remainder carried, the quotient laid on the level by P3 in the direction."""
    q, wr2 = divide(numerator, wwall, wr, direction)
    return lay(now, q, direction), wr2


def ride(a: Any, momentum: Any, wall: Any, direction: int) -> tuple[Any, Any, Any]:
    """The riding line's division (interval.division): P1 of the kicked momentum at the mean wall from the half wall, the quotient laid on the start level by P3, the slots in the direction's order."""
    v, rem = divide(momentum, wall, wall // 2, 1)
    now, before = placed(lay(a, v, direction), a, direction)
    return now, before, rem


def move(now: Any, rem: Any, count: Any, wall: Any) -> Any:
    """The take's move (take.move, CR-S1): P1 of the exact numerator count x wall at the line's own wall, the remainder unmoved, the quotient laid by P3."""
    q, _unmoved = divide(count * wall, wall, rem, 1)
    return lay(now, q)


def exchange_row(nows: list[Any], befores: list[Any], rems: list[Any], walls: list[Any], k: list[list[int]]) -> tuple[list[Any], list[Any], list[Any]]:
    """The swap's act on one row (node.exchange): every line P2 with the row's K, a matrix on the lines (the plane's im line negated, the quartet's K0), the remainder mirrored by the line's own K entry at the line's own wall."""
    n = len(nows)
    new_n = [sum((k[r][c] * befores[c] for c in range(n) if k[r][c]), start=0) for r in range(n)]
    new_b = [sum((k[r][c] * nows[c] for c in range(n) if k[r][c]), start=0) for r in range(n)]
    new_r = [mirror(rems[r], walls[r], 1 + (k[r][r] < 0)) for r in range(n)]
    return new_n, new_b, new_r
