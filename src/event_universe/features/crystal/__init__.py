"""THE CRYSTAL (ALGEBRA.md #the-primitives, the row "the crystal"; #the-ladder, THE PAIR RECORD and THE HALF QUANTUM): an ordinary body of matter with the key `crystal`, which declares nothing else; the record arriving at its one Node clicks there by the ladder as at any set, its quantum into the crystal's count, and in the same interval the crystal gives one record of rank 2 from that count at the arriving norm over twice its denominator, its two labels identical on its two sides (the identity, nothing declared), each a half quantum, its clock the arriving one's at half the rotation (the symmetric division of the conserved rotation, derived, no key); Rule3 spreads it from the crystal's Node through the Ports as any record's. A body with no key gives nothing at a click."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import ObjectOf, Schema

# the word of ALGEBRA.md #the-primitives for this primitive
THE_WORD = "a hypothesis under its own name: the arriving record clicks at the crystal's Node and in the same interval the crystal gives one record of rank 2 at the arriving norm over twice its denominator, its two labels identical, each a half quantum"

Label = tuple[int, int]
Pair = tuple[int, int]


@dataclass(frozen=True)
class CrystalTerm:
    """The body's declaration: the key `crystal` alone, which declares nothing (the pair's norm, labels and clock are the arriving record's)."""


@dataclass(frozen=True)
class CrystalStart:
    """The click's reading: the arriving record's norm T with its denominator D (the one quantum the crystal took), its label and its clock [p, q]."""

    norm: int
    denominator: int
    label: Label
    clock: Pair


@dataclass(frozen=True)
class CrystalOwn:
    """The crystal keeps nothing between intervals."""


@dataclass(frozen=True)
class CrystalWrites:
    """The pair's declaration for the giving: its two labels, identical (the identity channel), its norm T over 2 D (each label a half quantum, the two together the taken quantum), and its clock at half the arriving rotation."""

    labels: tuple[Label, Label]
    norm: int
    denominator: int
    clock: Pair


def check(term: CrystalTerm, start: CrystalStart) -> None:
    """The refusals by name: a norm from 1 with its denominator from 1, a clock pair from 1."""
    if start.norm < 1 or start.denominator < 1:
        raise ValueError(
            f"the taken quantum's norm is from 1 with its denominator from 1, got {start.norm} / {start.denominator}"
        )
    if start.clock[0] < 1 or start.clock[1] < 1:
        raise ValueError(f"the arriving record's clock is a pair of integers from 1, got {start.clock}")


def apply(term: CrystalTerm, start: CrystalStart, own: CrystalOwn) -> CrystalWrites:
    """The primitive at (ii) for one click at the crystal: the pair's two labels the arriving record's one, identical on its two sides; its norm the taken quantum's over twice the denominator (a half and a half, the count conserved over the click and the giving); its clock [p, 2 q], half the arriving rotation."""
    check(term, start)
    numerator, denominator = start.clock
    return CrystalWrites(
        (start.label, start.label), start.norm, 2 * start.denominator, (numerator, 2 * denominator)
    )


def read_term(body: dict[str, Any]) -> CrystalTerm | None:
    """The term of a body with the key `crystal` (which declares nothing), None for a body with no key."""
    return CrystalTerm() if "crystal" in body else None


DECLARATION = Declaration(
    name="the crystal",
    place="(ii)",
    reads=(
        "the click at the crystal's set",
        "the taken quantum's norm and clock",
        "the arriving record's label",
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
