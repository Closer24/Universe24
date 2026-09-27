"""The feed and the induction at (v), out of the loop's module (the split's pattern, #1275): the body's reads' factors, a held family's parts summed over Nodes, the body's two faces on an axis read through the Ports, and the two acts that gather the interval's reads for the folders' lines (features/feed, features/induction) and write the two levels of momentum and the remainders back (ALGEBRA.md #the-primitives, the rows of the feed and the induction; #the-well)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, cast

import numpy as np

from event_universe.core.ports import port_of
from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE
from event_universe.events.records import Block, LiveRecord
from event_universe.features.feed import (
    PAIR_INDEX,
    FeedFace,
    FeedOwn,
    FeedRead,
    FeedStart,
    FeedWrites,
    Tensor,
    Vector,
)
from event_universe.features.induction import (
    InductionOwn,
    InductionRead,
    InductionStart,
    InductionWrites,
)

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def read_factors(loop: DetectorLawSimulation, block: Block) -> list[tuple[int, int]]:
    """The body's family's reads of held families with their factors f: the weight plainly, minus the body's charge times the weight by q (ALGEBRA.md #the-primitives, the rows of the feed and the induction)."""
    found: list[tuple[int, int]] = []
    for other, weight, by, _ in loop.families[block.family].reads:
        if other in loop.held_records:
            factor = weight if by == "plain" else -loop._body_charge(block.number) * weight
            found.append((other, factor))
    return found


def parts_summed(
    loop: DetectorLawSimulation, family: int, where: np.ndarray, before: bool = False
) -> tuple[int, Vector, Tensor]:
    """A held family's levels summed over the Nodes of `where` (HOST, the feed's and the induction's read): the time part, the vector part (0 where the family has none) and the symmetric tensor part in the feed's order (0 where none), as the interval leaves them or at its start."""

    def total(record: LiveRecord) -> int:
        return int((record.before if before else record.now)[where].sum())

    vector = [0, 0, 0]
    tensor = [0] * len(set(PAIR_INDEX.values()))
    for index, record in enumerate(loop.held_parts[family]):
        group, axes = loop.main_loop.function_of("the degree", "(i)")(
            loop.families[family].parts, index + 1
        )
        if group == 1:
            vector[axes[0]] = total(record)
        elif group == 2:
            tensor[PAIR_INDEX[axes]] = total(record)
    return (
        total(loop.held_records[family]),
        (vector[0], vector[1], vector[2]),
        cast(Tensor, tuple(tensor)),
    )


def faces_of(
    loop: DetectorLawSimulation, block: Block, axis: int
) -> tuple[np.ndarray, np.ndarray] | None:
    """The body's two faces on an axis (minus, plus): the Nodes outside the body whose Link through the Port toward it leads inside, read through the Ports (the wrap on a periodic axis, nothing beyond an open face); None where the axis has one layer or the two faces differ in size (a face beyond an open face, a body not a box)."""
    if loop.shape[axis] == 1:
        return None
    inside = loop.ports.arrivals(block.mask, loop.kind_wrap[block.family], False)
    minus = inside[port_of(axis, 1)] & ~block.mask
    plus = inside[port_of(axis, -1)] & ~block.mask
    if not minus.any() or int(minus.sum()) != int(plus.sum()):
        return None
    return minus, plus


def feed_act(
    loop: DetectorLawSimulation, line: Callable[..., object], block: Block, inverse: bool
) -> None:
    """THE FEED AT (v): the feed's line (features/feed) on the body, from the fields as the interval leaves them: per axis the two faces' reads (the time, vector and tensor parts summed over the face's Nodes, with the read's factor), the faces' distance in Links (the body's layers plus one) and a face's Node count, the body's two levels of momentum, its wall and the Node clock; the writes the two levels and the remainders back; a body held in place (the word `fixed`) is not fed."""
    factors = [] if block.fixed else read_factors(loop, block)
    if not factors:
        return
    faces_per_axis: list[tuple[FeedFace, FeedFace] | None] = []
    distance = [0, 0, 0]
    for axis in range(3):
        faces = faces_of(loop, block, axis)
        if faces is None:
            faces_per_axis.append(None)
            continue
        pair = tuple(
            FeedFace(
                tuple(FeedRead(f, *parts_summed(loop, other, face)) for other, f in factors),
                int(face.sum()),
            )
            for face in faces
        )
        faces_per_axis.append((pair[0], pair[1]))
        layers = np.any(block.mask, axis=tuple(other for other in range(3) if other != axis))
        distance[axis] = int(layers.sum()) + 1
    start = FeedStart(
        THE_INVERSE if inverse else THE_ADVANCE,
        (int(block.momentum[0]), int(block.momentum[1]), int(block.momentum[2])),
        (
            int(block.momentum_before[0]),
            int(block.momentum_before[1]),
            int(block.momentum_before[2]),
        ),
        loop.wall_of(block),
        loop.node_clock,
        (faces_per_axis[0], faces_per_axis[1], faces_per_axis[2]),
        (distance[0], distance[1], distance[2]),
    )
    own = FeedOwn({key: value for key, value in block.hold_carry.items() if key[0] == "feed"})
    writes = cast(FeedWrites, line(start, own))
    block.momentum, block.momentum_before = list(writes.momentum), list(writes.momentum_before)
    block.hold_carry.update(writes.own.carries)


def induction_act(
    loop: DetectorLawSimulation, line: Callable[..., object], block: Block, inverse: bool
) -> None:
    """THE INDUCTION AT (v): the induction's line (features/induction) on the body: per read the vector part summed over the body's Nodes as the interval leaves it and at its start, with the read's factor; the body's two levels of momentum, its wall, the Node clock and its Node count; the writes the two levels and the remainders back; a body held in place (the word `fixed`) is not fed."""
    factors = [] if block.fixed else read_factors(loop, block)
    factors = [(other, f) for other, f in factors if loop.held_parts[other]]
    if not factors:
        return
    reads = tuple(
        InductionRead(
            f,
            parts_summed(loop, other, block.mask)[1],
            parts_summed(loop, other, block.mask, True)[1],
        )
        for other, f in factors
    )
    start = InductionStart(
        THE_INVERSE if inverse else THE_ADVANCE,
        (int(block.momentum[0]), int(block.momentum[1]), int(block.momentum[2])),
        (
            int(block.momentum_before[0]),
            int(block.momentum_before[1]),
            int(block.momentum_before[2]),
        ),
        loop.wall_of(block),
        loop.node_clock,
        int(np.count_nonzero(block.mask)),
        reads,
    )
    own = InductionOwn({key: value for key, value in block.hold_carry.items() if key[0] == "induction"})
    writes = cast(InductionWrites, line(start, own))
    block.momentum, block.momentum_before = list(writes.momentum), list(writes.momentum_before)
    block.hold_carry.update(writes.own.carries)
