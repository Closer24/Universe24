"""The lean core (H-Node-Beneath-Rule3-1): the one act beneath Rule3 and its three readings, integers only, no name, no number, no branch on a row's kind. The one act is the carried division at a slot in a direction (`divide`): u = total + carry, the quotient u div wall, the remainder u mod wall kept in [0, wall), the carry read as the remainder itself at +1 and as its mirror wall - 1 - r at -1, the remainder written back the same way. Its three readings: Rule3's step of a line (`step`: the total from the line's two slots read in the direction's order and the six Links' arrivals, the quotient laid on the slot the direction names, the other slot the level read), the write and the take's move (`write`, `move`: the quotient of a numerator at a write wall laid on the level now, CR-S1's numerator count times wall leaving the remainder unmoved), and the slot exchange with the mirror (`exchange`: the direction read on the line, P2, which the engine writes into the arrays). A lay on a slot (`lay`) is the quotient written; it is the division's own last line and no act of its own."""

from __future__ import annotations

from typing import Any

SLOTS = 2  # a line's two slots, now and before


def divide(total: Any, wall: Any, remainder: Any, direction: int = 1) -> tuple[Any, Any]:
    """The one act: the carried division at a slot in a direction; the carry is the remainder read by the direction (its mirror at -1) and written back by it."""
    carry = remainder if direction == 1 else wall - 1 - remainder
    carried = total + carry
    quotient = carried // wall
    rest = carried - wall * quotient
    return quotient, rest if direction == 1 else wall - 1 - rest


def mirror(remainder: Any, wall: Any) -> Any:
    """The remainder read at -1: wall - 1 - r, the reflection of [0, wall) (CA-S1's one asymmetric letter, the floor, reflected)."""
    return wall - 1 - remainder


def lay(level: Any, count: Any, sign: int = 1) -> Any:
    """The quotient laid on a slot: the level plus the count with the sign; the division's last line, written once."""
    return level + sign * count


def exchange(now: Any, before: Any, remainder: Any, wall: Any) -> tuple[Any, Any, Any]:
    """The slot exchange with the mirror (P2): the line read at -1, (before, now, wall - 1 - r); an involution; the engine's swap at the top writes it into the arrays conjugated by the row's K."""
    return before, now, mirror(remainder, wall)


def total_of(own: Any, wall: Any, level: Any, other: Any, flux: Any, reaches: Any, arrivals: Any) -> Any:
    """Rule3's total at a line: S a - w y + flux + SUM over the six Links of R_j m_j, a the level read on the slot the direction names, y the other."""
    found = own * level - wall * other + flux
    for reach, arrival in zip(reaches, arrivals, strict=True):
        found = found + reach * arrival
    return found


def step(
    now: Any, before: Any, remainder: Any, own: Any, wall: Any, flux: Any, reaches: Any, arrivals: Any, direction: int = 1
) -> tuple[Any, Any, Any]:
    """Rule3 on one line in the direction: the two slots read in the direction's order, the one division, the quotient laid on the slot the direction names and the level read becoming the other; the same function at -1 is the inverse (CA-S1, RW-S1)."""
    level, other = (now, before)[::direction]
    quotient, rest = divide(total_of(own, wall, level, other, flux, reaches, arrivals), wall, remainder, direction)
    now, before = (quotient, level)[::direction]
    return now, before, rest


def write(now: Any, numerator: Any, wwall: Any, wrem: Any, direction: int = 1) -> tuple[Any, Any]:
    """The write act: the numerator's division at the write wall, the quotient laid on the level now with the direction's sign, the write remainder carried."""
    quotient, wrem = divide(numerator, wwall, wrem, direction)
    return lay(now, quotient, direction), wrem


def move(now: Any, count: Any, wall: Any, remainder: Any) -> tuple[Any, Any]:
    """The take's move (CR-S1): the write of count times the wall at the line's own wall, the quotient the count and the remainder unmoved; forward, the lay-back and the undoing are this act with the count's sign."""
    quotient, rest = divide(count * wall, wall, remainder, 1)
    return lay(now, quotient), rest


def peak(x0: Any, x1: Any, x2: Any) -> bool:
    """The reading that names the turned Node: the weak maximum of three levels with one strict (the swap's trigger, FR-S1); a reading, not an act."""
    return x0 <= x1 >= x2 and (x0 < x1 or x2 < x1)
