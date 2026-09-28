"""THE COUNT IS READ ONCE (ALGEBRA.md #the-primitives, THE ALGEBRA OF CLUSTERS (2); Cheshbon's line of 2026-09-28, 14:45 Israel), out of the loop's module: under the divisor 1 the well is the count, so the held level at a Node is the count there, D div T of the record's form laid as the well, written once and never added interval after interval; every family reads it down the graph of the ranks at the weight 1 and its pace at the Node is Gamma - c; under a divisor above 1 (the universe of record) the hold stays the sourced field, the level gaining the source over E_s each interval."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

import numpy as np

from event_universe.core.rule3 import division_forward

if TYPE_CHECKING:
    from event_universe.events.records import Block
    from event_universe.loader.world import FamilyDefinition


def counts_are_the_well(families: Sequence[FamilyDefinition], block: Block) -> bool:
    """THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD (THE ALGEBRA OF CLUSTERS (1); Cheshbon's line of 2026-09-28, 15:41 Israel): whether the count's line lays its counts from the body's well, D div T at every Node of the record, read once per period of the standing record and never from the instantaneous form: the well is laid and the family that holds the content holds it at the divisor 1 (the well is the count); the declared count is then a reading."""
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


def counts_laid(block: Block, node: Sequence[int]) -> np.ndarray:
    """The counts the line steps this interval: the well of the loaded record at the first act, then the standing lay, replaced once per period of the record by the well summed over the period div the period's length ((sum D) div (P T), the well D div T per interval), the period read from the record's own return at the body's Node (two sign changes of its level now); the standing lay between returns (Cheshbon's line of 15:41 and 15:46: the count follows the form over the record's clock, not the instantaneous form)."""
    well = np.asarray(block.well, dtype=np.int64)
    laid, summed = block.period_counts, block.period_sum
    if laid is None or summed is None:
        laid, summed = well.copy(), np.zeros_like(well)
        block.period_length = block.period_flips = block.period_sign = 0
    summed += well
    block.period_length += 1
    level = int(block.own.now[tuple(node)]) if block.own is not None else 0
    sign = 1 if level > 0 else -1 if level < 0 else 0
    if sign and block.period_sign and sign != block.period_sign:
        block.period_flips += 1
    if sign:
        block.period_sign = sign
    if block.period_flips >= 2:  # the average by Rule3's division act, the period's length the wall
        laid = cast(np.ndarray, division_forward(cast(int, summed), block.period_length, 0)[0])
        summed, block.period_length, block.period_flips = np.zeros_like(well), 0, 0
    block.period_counts, block.period_sum = laid, summed
    return laid.copy()
