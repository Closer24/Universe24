"""The hand (ALGEBRA.md #the-primitives, the row "the hand"): S . n, a booking of the spin's and the momentum's levels over the three axes; its sign against the declared hand admits or refuses the click, the opposite sign alone refusing; no division."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.register import Declaration
from event_universe.core.schema import ObjectOf, OneOf, Schema

# the word of ALGEBRA.md #the-primitives for this primitive
THE_WORD = "S . n is a booking of the spin's and the momentum's levels; its sign against the declared hand admits or refuses the click"


@dataclass(frozen=True)
class HandTerm:
    """The declared hand: -1 or +1."""

    hand: int


@dataclass(frozen=True)
class HandStart:
    """The body's spin S and momentum n per axis as the interval left them."""

    spin: tuple[int, int, int]
    momentum: tuple[int, int, int]


@dataclass(frozen=True)
class HandWrites:
    """The booking S . n and whether the click is admitted."""

    booking: int
    admitted: bool


def sign_of(value: int) -> int:
    """The sign, -1, 0 or 1."""
    return (value > 0) - (value < 0)


def booking(spin: tuple[int, int, int], momentum: tuple[int, int, int]) -> int:
    """S . n over the three axes, a sum of products of integers."""
    return sum(s * n for s, n in zip(spin, momentum, strict=True))


def check(term: HandTerm) -> None:
    """The refusal by name: the declared hand is -1 or +1."""
    if term.hand not in (-1, 1):
        raise ValueError(
            f"the declared hand {term.hand} is refused: a hand is -1 or +1 (ALGEBRA.md #the-primitives)"
        )


def apply(term: HandTerm, start: HandStart, own: None = None) -> HandWrites:
    """The primitive at (ii): the booking's sign against the declared hand; the click is refused where the two are opposite and admitted otherwise, a body with no spin or no momentum admitting every click (ALGEBRA.md #the-primitives, the row "the hand")."""
    check(term)
    value = booking(start.spin, start.momentum)
    return HandWrites(value, sign_of(value) * term.hand != -1)


DECLARATION = Declaration(
    "the hand",
    "(ii)",
    ("a body's spin S", "a body's momentum n", "the declared hand"),
    (),
    apply,
    THE_WORD + ' (ALGEBRA.md #the-primitives, the row "the hand")',
    word="after the step",
    schema=Schema({"a family's entry": ObjectOf({"hand": OneOf((-1, 1))}, frozenset({"hand"}))}),
)
