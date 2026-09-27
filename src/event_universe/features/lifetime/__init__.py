"""The lifetime (ALGEBRA.md #the-primitives, the row "the lifetime"): the age is the count on the record, one per interval; at age L the record ends on its tally, the ladder's click first and the end second at (ii); a comparison of two integers, no division."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.register import Declaration
from event_universe.core.schema import Integer, ObjectOf, Schema

# the word of ALGEBRA.md #the-primitives for this primitive
THE_WORD = "the age is the count (b) on the record; at age L on the face the record ends"


@dataclass(frozen=True)
class LifetimeTerm:
    """The family's row: L, the age at which its records end, from 1."""

    lifetime: int


@dataclass(frozen=True)
class LifetimeStart:
    """What the interval left on the record: its age after its step, and whether the ladder clicked it this interval (the click first, the end second)."""

    age: int
    clicked: bool


@dataclass(frozen=True)
class LifetimeWrites:
    """Whether the record ends this interval."""

    ends: bool


def check(term: LifetimeTerm, start: LifetimeStart) -> None:
    """The refusals by name: L from 1, the age from 0."""
    if term.lifetime < 1:
        raise ValueError(
            f"the lifetime L = {term.lifetime} is refused: L is an age from 1 (ALGEBRA.md #the-primitives)"
        )
    if start.age < 0:
        raise ValueError(
            f"the record's age {start.age} is refused: the age counts intervals from 0 (ALGEBRA.md #the-primitives)"
        )


def apply(term: LifetimeTerm, start: LifetimeStart, own: None = None) -> LifetimeWrites:
    """The primitive at (ii): the record ends where its age has reached L and the ladder did not click it this interval (ALGEBRA.md #the-primitives, the row "the lifetime")."""
    check(term, start)
    return LifetimeWrites(not start.clicked and start.age >= term.lifetime)


DECLARATION = Declaration(
    "the lifetime",
    "(ii)",
    ("the record's age", "L"),
    ("the record's tally",),
    apply,
    THE_WORD + ' (ALGEBRA.md #the-primitives, the row "the lifetime")',
    word="after the step",
    schema=Schema(
        {"a family's entry": ObjectOf({"lifetime": Integer(least=1)}, frozenset({"lifetime"}))}
    ),
)
