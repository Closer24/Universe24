"""THE COUNT IS READ ONCE (ALGEBRA.md #the-primitives, THE ALGEBRA OF CLUSTERS (2); Cheshbon's line of 2026-09-28, 14:45 Israel), out of the loop's module: under the divisor 1 the well is the count, so the held level at a Node is the count there, D div T of the record's form laid as the well, written once and never added interval after interval; every family reads it down the graph of the ranks at the weight 1 and its pace at the Node is Gamma - c; under a divisor above 1 (the universe of record) the hold stays the sourced field, the level gaining the source over E_s each interval."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from event_universe.events.records import Block
    from event_universe.loader.world import FamilyDefinition


def counts_are_the_well(families: Sequence[FamilyDefinition], block: Block) -> bool:
    """THE COUNT IS THE RECORD'S FORM (THE ALGEBRA OF CLUSTERS (1); the Closer's ruling of 2026-09-28, 15:19 Israel): whether the count's line lays its counts from the body's well, D div T at every Node of the record, at every interval, the line's move a reading of it: the well is laid and the family that holds the content holds it at the divisor 1 (the well is the count); the declared count is then a reading."""
    holds = any(row.held == "content" and row.held_divisor == 1 for row in families)
    return block.well is not None and holds


def read_once(block: Block | None, definition: FamilyDefinition) -> bool:
    """Whether the held level at the body's Nodes is the count itself: the body's well is laid (the universe declares T) and the family holds at the divisor 1."""
    return block is not None and block.well is not None and definition.held_divisor == 1


def written(
    block: Block | None, definition: FamilyDefinition, standing: np.integer | int, level: int, sign: int
) -> int:
    """The held level at a Node after the hold's act: the level itself (the count there, once; the same at the inverse, where the well laid back is that interval's count) where the count is read once, else the standing level plus the signed increment (the sourced field)."""
    return level if read_once(block, definition) else int(standing) + sign * level
