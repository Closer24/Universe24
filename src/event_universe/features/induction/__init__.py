"""THE INDUCTION (ALGEBRA.md #the-primitives, the row "the induction"): minus the change of the momentum part of the contraction at the body's Nodes, P_a = -SUM over the reads of f x V_a (the coefficient of n_a div W in the contraction, V the read's vector part summed over the body's N Nodes): n_a += W x SUM f x (V_a now - V_a before) div (2 Gamma N) over the interval, a push on both of the body's integers of momentum (n and n_before, the feed's leapfrog pair), the division Rule3's division act with its remainder carried on the body; a row of the ledger the loop does not call yet (function None: bodies move by the hop until the owner's word on motion)."""

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
STEP_ACTS = (THE_ADVANCE, THE_INVERSE)


@dataclass(frozen=True)
class InductionRead:
    """One read of the body's family: the read's factor f and the read family's vector part summed over the body's Nodes as the interval leaves it and at its start (0 where the family has no vector part)."""

    factor: int
    vector_now: Vector
    vector_before: Vector


@dataclass(frozen=True)
class InductionStart:
    """The interval's reading for one body: the act, its two integers of momentum (n and n before), its wall W, the Node clock Gamma, its count of Nodes N and its reads."""

    act: str
    momentum: Vector
    momentum_before: Vector
    wall: int
    gamma: int
    nodes: int
    reads: tuple[InductionRead, ...]


@dataclass(frozen=True)
class InductionOwn:
    """The body's remainders of the induction: the carry of the carried division per axis."""

    carries: Mapping[Key, int]


@dataclass(frozen=True)
class InductionWrites:
    """The writes of one act: the body's two integers of momentum after, minus the change of the momentum part per axis, SUM f x (V_a now - V_a before) (a reading), the body's remainders after."""

    momentum: Vector
    momentum_before: Vector
    changes: Vector
    own: InductionOwn


def check(start: InductionStart) -> None:
    """The refusals by name: the act one of the two steps, the wall, the clock and the count of Nodes from 1."""
    if start.act not in STEP_ACTS:
        raise ValueError(f"the induction's act is one of {list(STEP_ACTS)}, got {start.act!r}")
    if start.wall < 1 or start.gamma < 1 or start.nodes < 1:
        raise ValueError(
            f"the induction's wall W = {start.wall}, clock Gamma = {start.gamma} and count of "
            f"Nodes N = {start.nodes} are from 1"
        )


def apply(start: InductionStart, own: InductionOwn) -> InductionWrites:
    """The primitive at (v) for one body: per axis minus the change of the momentum part, SUM f x (V_a now - V_a before), and both integers of momentum += W x that div (2 Gamma N) by the carried division (forward (numerator + carry) div wall; backward the carry before recovered by Rule3's direction -1 and the same value recomputed and taken off)."""
    check(start)
    carries = dict(own.carries)
    inverse = start.act == THE_INVERSE
    momentum, before = list(start.momentum), list(start.momentum_before)
    changes = [0, 0, 0]
    wall = SPAN * start.gamma * start.nodes
    for axis in range(len(momentum)):
        for read in start.reads:
            changes[axis] += read.factor * (read.vector_now[axis] - read.vector_before[axis])
        key: Key = ("induction", axis)
        carry = carries.get(key, 0)
        if inverse:
            _, carry = division_back(start.wall * changes[axis], wall, 0, carry)
        value, carry_after = division_forward(start.wall * changes[axis], wall, carry)
        carries[key] = carry if inverse else carry_after
        momentum[axis] += -value if inverse else value
        before[axis] += -value if inverse else value
    return InductionWrites(
        (momentum[0], momentum[1], momentum[2]),
        (before[0], before[1], before[2]),
        (changes[0], changes[1], changes[2]),
        InductionOwn(carries),
    )


DECLARATION = Declaration(
    name="the induction",
    place="(v)",
    reads=(
        "the momentum part of the contraction at the body's Node this interval and the last",
        "n now and n before",
        "W",
        "Gamma",
    ),
    writes=("a body's momentum n", "a body's remainders"),
    function=None,
    section="ALGEBRA.md #the-primitives, #a-familys-declaration, #the-interval",
    word="after the step",
)
