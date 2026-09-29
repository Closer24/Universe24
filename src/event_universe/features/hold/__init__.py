"""The hold: a held family's time part gains at every Node the source there over the row's divisor, (w x n_i + r) div E_s by the write's carried division with the remainder r carried at the Node, n_i the well of the families whose bodies source it (ALGEBRA.md #the-primitives, the row "the hold"; #the-interval), the division Rule3's act in either direction; the parts of the row's rank, 1, 1 + 3 or 1 + 3 + 6 components (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from typing import Any

from event_universe.core.rule3 import division_back, division_forward

COUNT_WORDS = ("content", "sign")
# the tensor's six parts in the order xx, yy, zz, xy, xz, yz
TENSOR_AXES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def components(parts: tuple[int, ...]) -> int:
    """The number of a held family's components: the time part, the vector's three and the tensor's six as its rank has them."""
    return sum(parts)


def diagonal(parts: tuple[int, ...]) -> tuple[int, int, int] | None:
    """The indices of the tensor's parts xx, yy, zz among the components, None where the rank holds no tensor."""
    if len(parts) < 3:
        return None
    first = parts[0] + parts[1]
    return first, first + 1, first + 2


def hold(level: Any, source: Any, divisor: int, carry: Any, direction: int = 1) -> tuple[Any, Any]:
    """The time part's level after the hold and the carry after it: forward the level gains (source + r) div E_s, back it loses the increment the forward act wrote and the carry steps back, exact; the divisor E_s from 1, refused by name otherwise."""
    if divisor < 1:
        raise ValueError(f"the hold's divisor E_s is from 1, got {divisor}")
    act = division_forward if direction == 1 else division_back
    increment, carried_out = act(source, divisor, carry)
    return level + direction * increment, carried_out
