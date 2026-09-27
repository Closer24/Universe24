"""THE CRYSTAL (ALGEBRA.md #the-primitives, the row "the crystal"; docs/HIGHLIGHTS.md "Where a tensor enters"): an ordinary body of matter with the key `crystal`, which declares nothing else; the record arriving at its one Node ends there by the ladder as at any set, and in the same interval the crystal gives one record of rank 2 with the same one quantum (the norm T, the count conserved), its two labels identical on its two sides (the identity channel, nothing declared) and its rotation the crystal's own from its count in the file; Rule3 spreads it from the crystal's Node through the Ports as any record's. The joint click is the row's hypothesis for the owner's word; the record clicks by its own ladder until then. A body with no key gives nothing at a click."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import ObjectOf, Schema

# the word of ALGEBRA.md #the-primitives for this primitive
THE_WORD = "a hypothesis under its own name: the arriving record ends at the crystal's Node and in the same interval the crystal gives one record of rank 2 with the same one quantum, its two labels identical, its rotation the crystal's own"

Label = tuple[int, int]


@dataclass(frozen=True)
class CrystalTerm:
    """The body's declaration: the crystal's own clock [p, q] from its count in the file, the pair's rotation; the key `crystal` itself declares nothing."""

    clock: tuple[int, int]


@dataclass(frozen=True)
class CrystalStart:
    """The click's reading: the arriving record's norm T with its denominator (the one quantum the crystal took) and its label."""

    norm: int
    denominator: int
    label: Label


@dataclass(frozen=True)
class CrystalOwn:
    """The crystal keeps nothing between intervals."""


@dataclass(frozen=True)
class CrystalWrites:
    """The pair's declaration for the giving: its two labels, identical (the identity channel), its norm with its denominator, the taken quantum's by conservation, and the crystal's clock the pair rotates with."""

    labels: tuple[Label, Label]
    norm: int
    denominator: int
    clock: tuple[int, int]


def check(term: CrystalTerm, start: CrystalStart) -> None:
    """The refusals by name: a clock pair from 1, a norm from 1 with its denominator from 1."""
    if term.clock[0] < 1 or term.clock[1] < 1:
        raise ValueError(f"the crystal's clock is a pair of integers from 1, got {term.clock}")
    if start.norm < 1 or start.denominator < 1:
        raise ValueError(
            f"the taken quantum's norm is from 1 with its denominator from 1, got {start.norm} / {start.denominator}"
        )


def apply(term: CrystalTerm, start: CrystalStart, own: CrystalOwn) -> CrystalWrites:
    """The primitive at (ii) for one click at the crystal: the pair's two labels the arriving record's one, identical on its two sides; its norm the taken quantum's whole (one in, one out: the count conserved over the click and the giving); its clock the crystal's."""
    check(term, start)
    return CrystalWrites((start.label, start.label), start.norm, start.denominator, term.clock)


def read_term(body: dict[str, Any], clock: tuple[int, int] | None) -> CrystalTerm | None:
    """The term of a body with the key `crystal` (which declares nothing) with the body's own clock, None for a body with no key; a crystal with no clock is refused by name."""
    if "crystal" not in body:
        return None
    if clock is None:
        raise ValueError("a crystal body declares its clock: the pair rotates with it")
    return CrystalTerm((int(clock[0]), int(clock[1])))


DECLARATION = Declaration(
    name="the crystal",
    place="(ii)",
    reads=(
        "the click at the crystal's set",
        "the taken quantum's norm",
        "the crystal's clock and label",
    ),
    writes=(),
    function=apply,
    section=THE_WORD + ' (ALGEBRA.md #the-primitives, the row "the crystal")',
    word="after the step",
    schema=Schema(
        {
            "a body": ObjectOf(
                {"crystal": ObjectOf({})},
                frozenset({"crystal"}),
            )
        }
    ),
)
