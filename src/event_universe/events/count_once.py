"""THE COUNT IS READ ONCE (ALGEBRA.md #the-primitives, THE ALGEBRA OF CLUSTERS (2); Cheshbon's line of 2026-09-28, 14:45 Israel), out of the loop's module: under the divisor 1 the well is the count, so the held level at a Node is the count there, D div T of the record's form laid as the well, written once and never added interval after interval; every family reads it down the graph of the ranks at the weight 1 and its pace at the Node is Gamma - c; under a divisor above 1 (the universe of record) the hold stays the sourced field, the level gaining the source over E_s each interval."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

import numpy as np

from event_universe.core.rule3 import division_forward

if TYPE_CHECKING:
    from event_universe.events.records import Block
    from event_universe.loader.world import FamilyDefinition


def no_field(families: Sequence[FamilyDefinition], action: int) -> bool:
    """THE WELL IS THE COUNT AND NO FIELD (ALGEBRA.md; Cheshbon's line of 2026-09-28, 18:05 Israel): in the rule's own universe (the file declares T and a family holds content at the divisor 1: the well is the count) a held family has no record that Rule3 steps and no rest that THE START solves; its level at a Node is the count laid there div its divisor at every interval, and the well at a distance is the matter record's own count there. The universe of record (no T) keeps its sourced fields."""
    return action > 0 and any(row.held == "content" and row.held_divisor == 1 for row in families)


def counts_are_the_well(families: Sequence[FamilyDefinition], block: Block) -> bool:
    """THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD (THE ALGEBRA OF CLUSTERS (1); Cheshbon's line of 2026-09-28, 15:41 Israel): whether the count's line lays its counts from the body's well, D div T at every Node of the record, read once per period of the standing record and never from the instantaneous form: the well is laid and the family that holds the content holds it at the divisor 1 (the well is the count); the declared count is then a reading."""
    holds = any(row.held == "content" and row.held_divisor == 1 for row in families)
    return block.well is not None and holds


def read_once(block: Block | None, definition: FamilyDefinition) -> bool:
    """Whether the held level at the body's Nodes is the count itself, written once and never added: the body's well is laid (the universe declares T) and the family holds at the divisor 1 (THE WELL IS THE COUNT AND NO FIELD); a family holding at a divisor above 1 keeps the sourced field's carried division."""
    return block is not None and block.well is not None and definition.held_divisor == 1


def written(
    block: Block | None, definition: FamilyDefinition, standing: np.integer | int, level: int, sign: int
) -> int:
    """The held level at a Node after the hold's act: the level itself (the count there, once; the same at the inverse, where the well laid back is that interval's count) where the count is read once, else the standing level plus the signed increment (the sourced field)."""
    return level if read_once(block, definition) else int(standing) + sign * level


def counts_laid(block: Block, node: Sequence[int]) -> np.ndarray:
    """The counts the line steps this interval: at the first act the declared count at each declared Node, the reading the gate approved, and nothing elsewhere (never the form of one interval, which is twice the mode's form at rest on a profile that does not stand: Cheshbon's line of 2026-09-28, 16:53 Israel); then the standing lay, replaced once per whole period of the record by the well summed over that period div its length ((sum D) div (P T), the well D div T per interval), a whole period read at the body's Node from one sign change of its level now to the second after it, the sum starting at the first sign change since the load (the load's own phase is no whole period); the standing lay between (THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD; Cheshbon's lines of 15:41 and 15:46)."""
    well = np.asarray(block.well, dtype=np.int64)
    laid, summed = block.period_counts, block.period_sum
    if laid is None or summed is None:
        declared_within_gate(block)
        laid, summed = np.zeros_like(well), np.zeros_like(well)
        for declared, count in zip(
            block.definition.nodes or (), block.definition.counts or (), strict=True
        ):
            laid[tuple(declared)] = int(count)  # the first lay: the declared count at its Node
        block.period_length, block.period_flips, block.period_sign = 0, -1, 0  # no sign change yet
    summed += well
    block.period_length += 1
    level = int(block.own.now[tuple(node)]) if block.own is not None else 0
    sign = 1 if level > 0 else -1 if level < 0 else 0
    if sign and block.period_sign and sign != block.period_sign:
        if block.period_flips < 0:  # the first sign change since the load: the whole period starts
            summed, block.period_length = well.copy(), 1
        block.period_flips += 1
    if sign:
        block.period_sign = sign
    if block.period_flips >= 2:  # the average by Rule3's division act, the period's length the wall
        laid = cast(np.ndarray, division_forward(cast(int, summed), block.period_length, 0)[0])
        summed, block.period_length, block.period_flips = np.zeros_like(well), 0, 0
    block.period_counts, block.period_sum = laid, summed
    return laid.copy()


def declared_within_gate(block: Block) -> None:
    """THE GATE READS THE FORM AT ANY PHASE (Cheshbon's line of 2026-09-28, 18:05 Israel; #1464): a count declared at a Node that is not the loaded record's form there after one interval of Rule3 (D div T, the well `record_form` lays at the first act, D = B^2 sin^2 omega_b at every phase, no phase formula) within the rounding of the record's amplitude, |c - D div T| <= 2 isqrt(c) + 1, is refused by name at the first lay; within it the declared count is a reading and the record's form is the count."""
    definition, well = block.definition, block.well
    if well is None or definition.profile is None:
        return
    for node, count in zip(definition.nodes or (), definition.counts or (), strict=True):
        form = int(well[tuple(node)])
        off = abs(
            int(count) - form
        )  # off <= 2 isqrt(c) + 1 as integer squares: (off - off mod 2)^2 <= 4 c
        if (off - (off & 1)) ** 2 > 4 * int(count):
            raise ValueError(
                f"measured[{block.number}] declares the count {count} at the Node {list(node)} and its "
                f"record's form there after one interval is {form}: a declared count is D div T of its "
                "record within 2 isqrt(c) + 1"
            )
