"""The write: a body's one act onto the GameBoard (ALGEBRA.md #the-primitives, A BODY'S WRITE IS ONE ACT): every write of a body is (kappa x q(Node) + r) div E at a Node of the body each interval, at both levels of the body's rotation (the second the read act once more, halved), Rule3's carried division act with the remainder r at that Node; q(Node) the body's own quantity there (the hold: the count declared there times the body's tensor (1, n_a / W, n_a n_b / W^2); the giving: the body's record's two levels at the shell; the recoil: the click's tally), kappa the row's factor, E the row's divisor (E_s at the hold, k at the giving, the wall L at the recoil, the rest of the hold's line at THE START); the four instances one act, and no number is the act's own."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from event_universe.core.register import Declaration
from event_universe.core.rule3 import ACTS, Key, carried

THE_WORD = "the right side, the step or after the step as the caller's card says: the act is the caller's, the write one"


@dataclass(frozen=True)
class WriteTerm:
    """The row's numbers for one write: the wall the division act divides by (E_s, E_s W^k, the norm's denominator, L) and the coefficient the count is booked with (a held factor, the emitter's weight g, a sense times a sign), 1 where the row names none."""

    wall: int
    coefficient: int = 1


@dataclass(frozen=True)
class WriteStart:
    """The interval's reading for one body: the act (the load, the advance, the rewrite, the inverse or the unhold) and, per key (a Node of the body, a momentum part or an axis), the body's count there, the numerator's other factor."""

    act: str
    counts: tuple[tuple[Key, int], ...]


@dataclass(frozen=True)
class WriteOwn:
    """The body's remainders of its writes: the value and the carry of every carried division by its key, the remainder's one home."""

    values: Mapping[Key, int]
    carries: Mapping[Key, int]


@dataclass(frozen=True)
class WriteWrites:
    """The act's writes: per key the two levels (now, before) as the carried division gives them, and the body's remainders after."""

    levels: tuple[tuple[Key, int, int], ...]
    own: WriteOwn


def check(term: WriteTerm, start: WriteStart) -> None:
    """The refusals by name: the wall from 1, the act one of the five."""
    if term.wall < 1:
        raise ValueError(f"the write's wall is from 1, got {term.wall}")
    if start.act not in ACTS:
        raise ValueError(f"the write's act is one of {list(ACTS)}, got {start.act!r}")


def apply(term: WriteTerm, start: WriteStart, own: WriteOwn) -> WriteWrites:
    """The primitive: per key (coefficient x count + r) div wall by the carried division act, the two levels returned and the remainder kept at the key (ALGEBRA.md #the-primitives, the row "the write")."""
    check(term, start)
    values, carries = dict(own.values), dict(own.carries)
    levels = tuple(
        (key, *carried(start.act, key, term.coefficient * count, term.wall, values, carries))
        for key, count in start.counts
    )
    return WriteWrites(levels, WriteOwn(values, carries))


DECLARATION = Declaration(
    name="the write",
    place="any",
    reads=("a body's content M_k", "the row's wall", "the row's coefficient"),
    writes=("a body's remainders",),
    function=apply,
    section="ALGEBRA.md #the-primitives, the row 'the write'; #the-interval; #the-four-acts",
    word="any",
)
