"""The hold: a held family's parts gain at every Node their source over the row's divisor by the write's carried division with the remainder carried at the Node (ALGEBRA.md #the-primitives, the row "the hold"; #the-interval): the time part (w x n_i + r) div E_s with n_i the well of the families that source it, the tension on each axis (w x T_aa + r_aa) div (E_s W_c) with T_aa the wave's own stress along it; the division Rule3's act in either direction; the parts of the row's rank, 1 or 1 + 3 components, the ones Rule3 reads (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from typing import Any

from event_universe.core.rule3 import division_back, division_forward

COUNT_WORDS = ("content", "sign")


def components(parts: tuple[int, ...]) -> int:
    """The number of a held family's components: the time part and the three tensions as its rank has them."""
    return sum(parts)


def diagonal(parts: tuple[int, ...]) -> tuple[int, int, int] | None:
    """The indices of the tensions xx, yy, zz among the components, after the time part; None where the rank holds none."""
    if len(parts) < 2:
        return None
    first = parts[0]
    return first, first + 1, first + 2


def hold(level: Any, source: Any, divisor: int, carry: Any, direction: int = 1) -> tuple[Any, Any]:
    """The part's level after the hold and the carry after it: forward the level gains (source + r) div E, back it loses the increment the forward act wrote and the carry steps back, exact; the divisor E from 1, refused by name otherwise."""
    if divisor < 1:
        raise ValueError(f"the hold's divisor E_s is from 1, got {divisor}")
    act = division_forward if direction == 1 else division_back
    increment, carried_out = act(source, divisor, carry)
    return level + direction * increment, carried_out
