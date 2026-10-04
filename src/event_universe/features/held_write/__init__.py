"""The held write: a held family's parts gain at every Node their sources by one write per part, (SUM over the sourcing families of w x q + r) div wall, the write's carried division with the one remainder r kept at the Node in [0, wall) (ALGEBRA.md #the-primitives, the row "the held write"; #the-interval): the time part's q the form D of a source that holds the content and the Wronskian W of one that holds the sign, over the wall E_s T; each axis part's q the tension T_aa, over the wall E_s W_c; the division Rule3's act in either direction; the row's lines its sources' count, one real line per source (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from typing import Any

from event_universe.core.rule3 import division_back, division_forward


def held_write(
    level: Any, numerator: Any, wall: int, remainder: Any, direction: int = 1
) -> tuple[Any, Any]:
    """One part's level after its write and the remainder after it: forward the level gains (numerator + r) div wall, back it loses the increment the forward act wrote and the remainder steps back, exact; the wall from 1, refused by name otherwise."""
    if wall < 1:
        raise ValueError(f"the write's wall E_s T is from 1, got {wall}")
    act = division_forward if direction == 1 else division_back
    increment, carried_out = act(numerator, wall, remainder)
    return level + direction * increment, carried_out
