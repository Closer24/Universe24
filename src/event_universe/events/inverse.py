"""The inverse's returns out of the loop's module: the interval's bookings at the detectors' Ports and the body's clock taken back, each function taking the engine (`DetectorLawSimulation` of `detector_law.py`) and bound as its method of the same duty, so every caller, test and spy works unchanged (ALGEBRA.md #the-interval: the inverse returns every ledger word but the click's)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe.events.records import Block, LiveRecord

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def booking_inverse(loop: DetectorLawSimulation, live: LiveRecord) -> None:
    """The interval's bookings at the detectors' Ports taken back before the record steps back (the loop's method `_booking_inverse`): the same one-way inflow read from the levels as the interval left them, the pointers, the absorbed sum, the momentum tally and the ladder's running total returned to the interval's start; a record that clicked is the click's own loss and a held part, a standing or a silent record books nothing (ALGEBRA.md #the-interval: the inverse returns every ledger word but the click's)."""
    if live.held_part or live.standing or live.silent or live.clicked:
        return
    tallies = {detector: list(tally) for detector, tally in live.momentum_tally.items()}
    increments = [0] * len(live.pointers)
    for detector, value in loop.detector_inflow_tally(live).items():
        increments[detector] = loop._polarised(live, detector, value)
        live.pointers[detector] -= increments[detector]
        live.absorbed -= increments[detector]
    for detector, tally in list(live.momentum_tally.items()):
        was = tallies.get(detector, [0, 0, 0])
        live.momentum_tally[detector] = [2 * a - b for a, b in zip(was, tally, strict=True)]
        if not any(live.momentum_tally[detector]):
            del live.momentum_tally[detector]  # an entry the forward booking made at this interval
    if live.pair_record is None:
        ladder = range(len(increments)) if live.norm <= 0 else loop._ladder_of(live)
        live.total -= sum(increments[detector] for detector in ladder)


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
