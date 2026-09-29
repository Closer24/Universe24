"""The momentum as a reading (ALGEBRA.md #the-generator (e), the recoil's row): a body's momentum n is read from its record's current after the count's line and is no level of any click's; the loop's method `_read_momentum`, out of the loop's module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe.core.ports import port_of
from event_universe.core.rule3 import NO_READ, SPAN, rule3
from event_universe.events.records import Block

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def read_momentum(
    loop: DetectorLawSimulation, block: Block, arrived: list[tuple[np.ndarray, ...] | None], wall: int
) -> None:
    """THE MOMENTUM AS A READING (the loop's method `_read_momentum`; ALGEBRA.md #the-generator (e), the recoil's row): n = W x the record's velocity, W = 3 Q M the body's wall and the velocity the record's current over its form: per axis the count's line's booking weight x (now_j before_i - before_j now_i) from Node i to its neighbour j through the +a Port, summed over the Links from the arrivals the count's line read (the second level's term added on a pair), over the count's wall T (the form per quantum) times M, to the nearest unit by the division act; no level, no remainder: both levels of the body's momentum are the reading, forward and back alike (the feed's pair one number); the products in the width, the sum in whole integers; a GAMEBOARD reading."""
    live, quanta = block.own, loop._body_count(block)
    if live is None or loop.world.quantum_action < 1 or quanta < 1 or block.definition.nodes is None:
        return  # a body of the older form (by its position) keeps its declared momentum, the pushing agent's
    levels = [(live.now, live.before, arrived[0], arrived[1])]
    if live.im_now is not None and live.im_before is not None:
        levels.append((live.im_now, live.im_before, arrived[2], arrived[3]))
    denominator, reading = (
        loop.world.quantum_action * quanta,
        [],
    )  # the record's form c T (THE COUNT IS THE RECORD'S FORM)
    for axis in range(3):
        total = 0
        for now, before, now_arrived, before_arrived in levels:
            if now_arrived is None or before_arrived is None:
                continue
            port = port_of(axis, 1)
            total += int((now_arrived[port] * before - before_arrived[port] * now).sum(dtype=object))
        numerator = loop.wall_of(block) * wall * total
        reading.append(
            int(rule3(NO_READ, NO_READ, SPAN, SPAN * denominator, numerator, 0, denominator)[0])
        )
    block.momentum, block.momentum_before = list(reading), list(reading)
