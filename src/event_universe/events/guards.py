"""The run-time guards of the walk, out of the loop's module: the arrays of the interval's start the main loop freezes, the arrays an act's card grants, a card's writes, a write applied by name, the generic act's term, its `Start` view and its own record, and the pace guard; each function takes the engine (`DetectorLawSimulation` of `detector_law.py`) and is bound as its method of the same duty, so the main loop and every test call it unchanged."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import numpy as np

from event_universe.core.main_loop import read_only
from event_universe.core.primitive import Own, Start, Term, Write

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def card_writes(loop: DetectorLawSimulation, name: str) -> frozenset[str]:
    """The ledger's words a card names as its writes."""
    return frozenset(loop.register.declarations[name].writes)


def start_arrays(loop: DetectorLawSimulation) -> Iterator[np.ndarray]:
    """Every array of the interval's start the main loop freezes for the walk: the records', the bodies' own records' and masks, the held families', the pair arrays, the detector map, the spans, the paces' carries and the held levels."""
    for live in loop.records.values():
        yield from live.arrays()
    for block in loop.blocks:
        if block.own is not None:
            yield from block.own.arrays()
        yield block.mask
    for record in loop.held_component_records():
        yield from record.arrays()
    for num, den in loop._pairs.values():
        yield num
        yield den
    yield loop.detector_at_node
    yield from loop.span_masks.values()
    yield from loop._pace_carry.values()
    yield from loop.node_level.values()


def grants(loop: DetectorLawSimulation, name: str) -> Iterator[np.ndarray]:
    """The arrays of the start an act may write in place, as its card names them: the count's line a body's position (the pair arrays and the detector map, the hop's writes it carries), the hold a family's level at a Node (the held families' arrays), the recoil the two levels of a body's own record (the turn of its phase), the operation the remainders and the two levels of an open window's record (the giving's write of the body's rotation at both levels)."""
    if name == "the count's line":
        for num, den in loop._pairs.values():
            yield num
            yield den
        yield loop.detector_at_node
    elif name == "the hold":
        for record in loop.held_component_records():
            yield from record.arrays()
    elif name == "the source":
        for family in loop._source_remainders:
            yield from loop._sourced_record(family).arrays()
    elif name == "the recoil":
        for block in loop.blocks:
            if block.own is not None:
                yield block.own.now
                yield block.own.before
    elif name == "the operation":
        for live in loop.records.values():
            yield live.remainder
        for block in (
            loop.blocks
        ):  # an open window's record: the giving writes the body's rotation at both levels
            if block.window is not None and block.window in loop.records:
                yield loop.records[
                    block.window
                ].now  # the record's `before` once its own step rebinds `now`
        for block in loop.blocks:
            if block.own is not None:
                yield block.own.remainder


def apply_write(loop: DetectorLawSimulation, write: Write) -> None:
    """One write of a primitive applied by the main loop: a body's momentum, spin or content by whole integers; another value is refused by name."""
    if write.value == "a body's momentum n":
        block = loop.block_by_number[write.of]
        for axis in range(3):
            block.momentum[axis] += int(write.integers[axis])
    elif write.value == "a body's spin S":
        block = loop.block_by_number[write.of]
        for axis in range(3):
            block.spin[axis] += int(write.integers[axis])
    elif write.value == "a body's content M_k":
        loop.held[write.of][write.at] += int(write.integers)
    else:
        raise ValueError(f"the loop applies no write of {write.value!r}: no such value of a body")


def term_of(loop: DetectorLawSimulation, label: str, name: str) -> Term:
    """The term of the files a generic act is called with: the primitive's name and the line's label, the index parsed from the label."""
    digits = "".join(character for character in label if character.isdigit())
    return Term(name, "", int(digits) if digits else 0, 0, 0, (), label)


def start_view(loop: DetectorLawSimulation) -> Start:
    """The interval's start as a generic act reads it: the held levels as read-only views, the bodies' counts, walls and momenta."""
    held = [family for family in range(len(loop.families)) if family in loop.held_records]
    return Start(
        tuple(read_only(loop.held_records[family].now) for family in held),
        tuple(read_only(loop.held_records[family].before) for family in held),
        (),
        tuple(tuple(row) for row in loop.held),
        tuple(loop.wall_of(block) for block in loop.blocks),
        tuple(tuple(block.momentum) for block in loop.blocks),
    )


def own_of(loop: DetectorLawSimulation, label: str, name: str) -> Own:
    """The own record of a generic act: none until a folder's remainders live on the body."""
    return Own(None)


def guard_paces(loop: DetectorLawSimulation) -> None:
    """The pace guard: every reading family's pace stays positive at every Node, else the run is refused."""
    for family, definition in enumerate(loop.families):
        if not definition.reads:
            continue
        most = int(np.max(np.abs(loop._effective_content(family))))
        axis_contents = loop._axis_contents(family)
        if axis_contents is not None:
            content = loop._effective_content(family)
            most = max(most, *(int(np.max(np.abs(content + t))) for t in axis_contents))
        if most >= loop.node_clock:
            raise RuntimeError(
                f"the effective content {definition.name!r} reads reached {most} "
                f"in size at interval {loop.tick}, at or beyond Gamma = {loop.node_clock}: "
                "the pace Gamma minus the weighted held levels of every read stays positive "
                "under the fixed wall (ALGEBRA.md #the-counts-line, #the-paces); the run is refused"
            )
