"""The inverse's returns out of the loop's module: the body's clock taken back, each function taking the engine (`DetectorLawSimulation` of `detector_law.py`) and bound as its method of the same duty, so every caller, test and spy works unchanged (ALGEBRA.md #the-interval: the inverse returns every ledger word but the click's)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe.events.records import Block

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def block_clock_inverse(loop: DetectorLawSimulation, block: Block) -> None:
    """The body's clock stepped back after its own record stepped back (the loop's method `_block_clock_inverse`): the sum of its record as the interval before left it, and a cycle that began this interval unbegun (its start moved back by the length the count took; the length of the cycle before it is no state of the body and reads 0)."""
    total = 0
    if block.node_record is not None:
        total = int(block.node_record.now)
    elif block.own is not None:
        total = int(np.sum(block.own.now[block.mask]))
    if block.cycle_start == loop.tick and block.new_cycle:
        block.cycle_start -= block.cycle_length
        block.new_cycle, block.cycle_length = block.cycle_start > 0, 0
    block.previous_sum = total
