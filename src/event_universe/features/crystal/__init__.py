"""THE CRYSTAL (docs/HIGHLIGHTS.md "Where a tensor enters"; the law's row to come): a body of one Node with the key `crystal`; the click of an arriving record at its set is followed by the giving of one record of rank 2, its two labels identical (the entangled channel's one term), its norm the taken quantum's by conservation and its clock the crystal's own; Rule3 spreads it from the crystal's Node through the Ports, no arms; the joint click at the two ends is the row's to write. A body with no key gives nothing at a click."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.schema import Integer, ListOf, ObjectOf, Schema

# the word of the law's row for this primitive (the row is the mathematician's; the draft names the highlight)
THE_WORD = "a hypothesis under its own name: one record of rank 2 with two identical labels given at the crystal's click, the joint click at the two ends"

Label = tuple[int, int]


@dataclass(frozen=True)
class CrystalTerm:
    """The body's declaration: the label its pair carries on both indices (a label as the emitter's branches write one, two integers), and the crystal's own clock [p, q] the pair rotates with."""

    label: Label
    clock: tuple[int, int]


@dataclass(frozen=True)
class CrystalStart:
    """The click's reading: the taken record's norm and its denominator (the quantum's content the crystal took)."""

    norm: int
    denominator: int


@dataclass(frozen=True)
class CrystalOwn:
    """The crystal keeps nothing between intervals."""


@dataclass(frozen=True)
class CrystalWrites:
    """The pair's declaration for the giving: its labels, the two identical, and its norm with its denominator, the taken quantum's by conservation, and the crystal's clock the pair rotates with."""

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
    """The primitive at (ii) for one click at the crystal: the pair's two labels the crystal's one, its norm the taken quantum's whole (one in, one out: the crystal's content is unchanged over the click and the giving)."""
    check(term, start)
    return CrystalWrites((term.label, term.label), start.norm, start.denominator, term.clock)


def read_term(body: dict[str, Any], clock: tuple[int, int] | None) -> CrystalTerm | None:
    """The term of a body's `crystal` key as the file writes it with the body's clock, None for a body with no key; a crystal with no clock is refused by name."""
    entry = body.get("crystal")
    if entry is None:
        return None
    if clock is None:
        raise ValueError("a crystal body declares its clock: the pair rotates with it")
    first, second = entry["label"]
    return CrystalTerm((int(first), int(second)), (int(clock[0]), int(clock[1])))


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
    section='docs/HIGHLIGHTS.md "Where a tensor enters"; the law\'s row to come',
    word="after the step",
    schema=Schema(
        {
            "a body": ObjectOf(
                {"crystal": ObjectOf({"label": ListOf(Integer(), 2)})},
                frozenset({"crystal"}),
            )
        }
    ),
)
