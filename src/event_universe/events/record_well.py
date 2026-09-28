"""The well of a body with a record, out of the loop's module: its record's one interval with the well's form laid after it, D_i div T at every Node by the source's act at the wall T through the write's line with the remainder carried (features/source, features/write), the numbers the hold reads as the body's sources; each function taking the engine (`DetectorLawSimulation` of `detector_law.py`) and bound as its method of the same duty (ALGEBRA.md #what-a-body-is: the well of a body with a record is its record's form, the count written at its Nodes D_i div T; #the-primitives the rows "the source" and "the write")."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import numpy as np

from event_universe.core.rule3 import THE_INVERSE, Key
from event_universe.events.records import Block
from event_universe.features.source import SourceOwn, SourceStart, SourceTerm, SourceWrites

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def record_form(loop: DetectorLawSimulation, block: Block, direction: int = 1) -> None:
    """One interval of the body's own record in `direction` (the Node record by the one rule, the lattice record by the loop's step or its inverse; the loop's method `_record_form`) and, where the universe declares T, the well's form after it: the record's count D_i = a_now^2 - a_next a_before at every Node from the three levels around the step, divided by T with the remainder carried at the Node by the source's act at the wall T through the write's line, the counts the hold reads at the interval's end; back, the remainder stepped back by the write's inverse act from the same D_i, then the interval's counts laid again from it, the numbers the hold's inverse reads after the record stepped back (`step_inverse`); a universe without T lays no well and the declared counts stand."""
    record: Any = block.node_record if block.node_record is not None else block.own
    if record is None:
        return
    kept = record.before if direction == 1 else record.now
    if block.node_record is not None:
        loop._advance_node_record(block, direction)
    elif direction == 1:
        loop._advance(record)
    else:
        loop._advance_inverse(record)
    wall = loop.world.quantum_action
    if wall < 1:
        return
    if direction == 1:
        count = record.before * record.before - record.now * kept
    else:
        count = record.now * record.now - kept * record.before
    argument = np.zeros(loop.shape, dtype=np.int64)
    if block.node_record is not None:
        argument[block.mask] = count
    else:
        argument = np.asarray(count, dtype=np.int64)
    if block.well_remainder is None:
        block.well_remainder = np.zeros(loop.shape, dtype=np.int64)
    if direction == -1:
        acted = np.argwhere((argument != 0) | (block.well_remainder != 0))
        nodes = [tuple(int(index) for index in node) for node in acted]
        carries: dict[Key, int] = {node: int(block.well_remainder[node]) for node in nodes}
        counts = tuple((node, int(argument[node])) for node in nodes)
        loop._write_line(THE_INVERSE, wall, 1, counts, {}, carries)
        for node in nodes:
            block.well_remainder[node] = carries[node]
    source = loop.main_loop.function_of("the source", "(iv)")
    term = SourceTerm(block.family, block.family, 1, wall)
    start = SourceStart(loop.shape, argument, loop._write_line)
    writes = cast(SourceWrites, source(term, start, SourceOwn(block.well_remainder)))
    block.well = writes.counts
    if direction == 1:
        block.well_remainder = writes.remainders
