"""THE FEED (ALGEBRA.md #the-primitives, the row "the feed"; #the-paces; #the-well): the contraction C at each face of a body on an axis, C = SUM over the reads of f x [the time level - (n_b V_b) div W + (n_b n_c h_bc) div W^2] over the face's Nodes, read with the coefficients +1 and -1 at the two faces; n_a += W x (C_+ - C_-) div (2 Gamma D_a F_a), D_a the faces' distance in Links and F_a a face's Nodes, stepped as the spin is, by the body's two integers n and n_before with the doubled term (n_next = n_before + 2 W (C_+ - C_-)(n) div (2 Gamma D_a F_a)), exactly invertible since the contraction is read at the middle; every division Rule3's division act with its remainder carried on the body; bound at (v) through the register (the owner's word of 09:37Z)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from event_universe.core.register import Declaration
from event_universe.core.rule3 import (
    SPAN,
    THE_ADVANCE,
    THE_INVERSE,
    Key,
    division_back,
    division_forward,
)

Vector = tuple[int, int, int]
Tensor = tuple[int, int, int, int, int, int]
Faces = tuple["FeedFace", "FeedFace"] | None
TENSOR_AXES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
# the symmetric tensor's component for an ordered pair of axes (h_bc = h_cb)
PAIR_INDEX = {pair: k for k, (b, c) in enumerate(TENSOR_AXES) for pair in ((b, c), (c, b))}
STEP_ACTS = (THE_ADVANCE, THE_INVERSE)


@dataclass(frozen=True)
class FeedRead:
    """One read of the body's family at one face: the read's factor f (the weight plainly, minus the body's charge times the weight by q) and the read family's levels summed over the face's Nodes: the time part, the vector part (three, 0 where the family has none) and the symmetric tensor part (six in TENSOR_AXES' order, 0 where none)."""

    factor: int
    time: int
    vector: Vector
    tensor: Tensor


@dataclass(frozen=True)
class FeedFace:
    """One face of the body on an axis: the reads' levels summed over the F Nodes read across the body's Ports on that side, and F."""

    reads: tuple[FeedRead, ...]
    nodes: int


@dataclass(frozen=True)
class FeedStart:
    """The interval's reading for one body: the act, its two integers of momentum (n now, the middle the contraction reads, and n before), its wall W, the Node clock Gamma, per axis the two faces (minus, plus) or None where the body has no two faces (one layer, an open face), and per axis the distance D_a in Links between the two faces' reads (the body's extent plus one)."""

    act: str
    momentum: Vector
    momentum_before: Vector
    wall: int
    gamma: int
    faces: tuple[Faces, Faces, Faces]
    distance: Vector


@dataclass(frozen=True)
class FeedOwn:
    """The body's remainders of the feed: the carry of every carried division by its key."""

    carries: Mapping[Key, int]


@dataclass(frozen=True)
class FeedWrites:
    """The writes of one act: the body's two integers of momentum after (forward n_next and n; backward n and n_before), the contraction read at each face ((minus, plus) per axis or None: a reading), the body's remainders after."""

    momentum: Vector
    momentum_before: Vector
    contractions: tuple[tuple[int, int] | None, ...]
    own: FeedOwn


def check(start: FeedStart) -> None:
    """The refusals by name: the act one of the two steps, the wall and the clock from 1, on every axis with faces the same reads on both, a Node on each face and a distance from 2."""
    if start.act not in STEP_ACTS:
        raise ValueError(f"the feed's act is one of {list(STEP_ACTS)}, got {start.act!r}")
    if start.wall < 1 or start.gamma < 1:
        raise ValueError(f"the feed's wall W = {start.wall} and clock Gamma = {start.gamma} are from 1")
    for axis, faces in enumerate(start.faces):
        if faces is None:
            continue
        minus, plus = faces
        if len(minus.reads) != len(plus.reads) or minus.nodes != plus.nodes or plus.nodes < 1:
            raise ValueError(
                f"the feed's two faces on axis {axis} read the same reads over the same count of "
                f"Nodes, from 1: {len(minus.reads)} reads on {minus.nodes} Nodes against "
                f"{len(plus.reads)} on {plus.nodes}"
            )
        if start.distance[axis] <= 1:  # the two faces' reads at least two Links apart
            raise ValueError(
                f"the feed's faces on axis {axis} stand {start.distance[axis]} Links apart: from 2"
            )


def division(act: str, key: Key, numerator: int, wall: int, carries: dict[Key, int]) -> int:
    """This interval's value of a carried division on the body, Rule3's division act: forward (numerator + carry) div wall with the remainder kept; backward the carry before recovered ((carry - numerator) mod wall, Rule3's direction -1) and the value the forward wrote recomputed from it, so that the same numerator gives the same value bit for bit."""
    carry = carries.get(key, 0)
    if act == THE_INVERSE:
        _, carry = division_back(numerator, wall, 0, carry)
    value, carry_after = division_forward(numerator, wall, carry)
    carries[key] = carry if act == THE_INVERSE else carry_after
    return value


def contraction(face: FeedFace, n: Vector, start: FeedStart, key: Key, carries: dict[Key, int]) -> int:
    """The contraction at one face (ALGEBRA.md #the-primitives, the row "the feed") with the momentum n the interval reads: per read f x [the time level - (n_b V_b) div W + (n_b n_c h_bc) div W^2], the vector and the tensor parts bookings of the momentum with the read's levels (the symmetric tensor over every ordered pair of axes), their divisions carried by the face's key."""
    total = 0
    for position, read in enumerate(face.reads):
        current = sum(n[b] * read.vector[b] for b in range(len(n)))
        stress = 0
        for (b, c), k in PAIR_INDEX.items():
            stress += n[b] * n[c] * read.tensor[k]
        vector_part = division(
            start.act, (*key, position, "v"), read.factor * current, start.wall, carries
        )
        tensor_part = division(
            start.act, (*key, position, "h"), read.factor * stress, start.wall * start.wall, carries
        )
        total += read.factor * read.time - vector_part + tensor_part
    return total


def apply(start: FeedStart, own: FeedOwn) -> FeedWrites:
    """The primitive at (v) for one body: on each axis with two faces the contraction at both with the momentum in the middle (n now forward, n before backward), and n_next = n_before + 2 W (C_+ - C_-) div (2 Gamma D_a F_a) by the carried division, the two integers then (n_next, n); backward the same term recomputed and taken off, the two integers (n_before, n_before_before) and every division stepped back."""
    check(start)
    carries = dict(own.carries)
    inverse = start.act == THE_INVERSE
    middle = start.momentum_before if inverse else start.momentum
    other = list(start.momentum if inverse else start.momentum_before)
    contractions: list[tuple[int, int] | None] = []
    for axis, faces in enumerate(start.faces):
        if faces is None:
            contractions.append(None)
            continue
        minus = contraction(faces[0], middle, start, ("feed", axis, "-"), carries)
        plus = contraction(faces[1], middle, start, ("feed", axis, "+"), carries)
        contractions.append((minus, plus))
        wall = SPAN * start.gamma * start.distance[axis] * faces[1].nodes
        step = division(start.act, ("feed", axis), SPAN * start.wall * (plus - minus), wall, carries)
        other[axis] += -step if inverse else step
    moved = (other[0], other[1], other[2])
    return FeedWrites(
        middle if inverse else moved, moved if inverse else middle, tuple(contractions), FeedOwn(carries)
    )


DECLARATION = Declaration(
    name="the feed",
    place="(v)",
    reads=(
        "the paces at the two faces of each axis of the body's Node (the contraction)",
        "n now and n before",
        "W",
        "Gamma",
    ),
    writes=("a body's momentum n", "a body's remainders"),
    function=apply,
    section="ALGEBRA.md #the-primitives, #a-familys-declaration, #the-interval",
    word="after the step",
)
