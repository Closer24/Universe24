"""The write: a family's one act onto the GameBoard, (w x q(Node) + r) div E at every Node by Rule3's carried division with the remainder r kept at that Node, forward and back (ALGEBRA.md #the-primitives, a family's write is one act): the hold, the well and the giving are its instances, and no number is the act's own."""

from __future__ import annotations

from typing import Any

from event_universe.core.rule3 import division_back, division_forward


def carried(numerator: Any, wall: int, carry: Any, direction: int = 1) -> tuple[Any, Any]:
    """One act of the write at every Node: forward (numerator + r) div wall and the remainder r' in [0, wall); back, from the remainder after, the quantity the forward act wrote and the remainder before it, exact (ALGEBRA.md #the-direction); the wall from 1, refused by name otherwise."""
    if direction not in (1, -1):
        raise ValueError(f"the write runs in the direction +1 or -1, got {direction}")
    if wall < 1:
        raise ValueError(f"the write's wall is from 1, got {wall}")
    if direction == 1:
        return division_forward(numerator, wall, carry)
    return division_back(numerator, wall, carry)
