"""THE POLARISER (ALGEBRA.md #the-primitives, the row "the polariser"): at a polariser body's Nodes the record's pair is turned back by the body's angle through the transport's rotation and its second level is taken by the body's second set, the first level passing to its first set, so the shares of the click are cos^2 and sin^2 of the angle between the record's pair and the axis, the ladder then as written; the angle an exact pair (m, j) with the triple (m^2 - j^2, 2 m j, m^2 + j^2), no float; a body with no polariser key polarises nothing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3
from event_universe.core.schema import Integer, ListOf, ObjectOf, Schema, Word

Pair = tuple[int, int]
Triple = tuple[int, int, int]

# the word of ALGEBRA.md #the-primitives for this primitive
THE_WORD = "a hypothesis under its own name: the transport's rotation turned back by the body's angle, the two levels to the two sets"


@dataclass(frozen=True)
class PolariserTerm:
    """The body's declaration: the angle as the exact pair (m, j), j from 0 (no turn) to m (a quarter turn), and the two sets' names, the first for the level along the axis and the second for the level across it."""

    angle: Pair
    sets: tuple[str, str]


@dataclass(frozen=True)
class PolariserStart:
    """The record's pair at the body's Nodes as the step left it: the two levels, one integer per Node."""

    re: np.ndarray
    im: np.ndarray


@dataclass(frozen=True)
class PolariserOwn:
    """The polariser keeps nothing between intervals: the transport's rounding carries no remainder (ALGEBRA.md #the-transport)."""


@dataclass(frozen=True)
class PolariserWrites:
    """The record's pair turned back by the angle at the body's Nodes, and the two sets' offers this interval: the first set's the squared level along the axis, the second's the squared level across it (their shares cos^2 and sin^2 of the pair's angle to the axis)."""

    re: np.ndarray
    im: np.ndarray
    first: np.ndarray
    second: np.ndarray


def triple_of(angle: Pair) -> Triple:
    """The Pythagorean triple of the pair (m, j): (m^2 - j^2, 2 m j, m^2 + j^2), cos of the angle (m^2 - j^2) / (m^2 + j^2) exact."""
    m, j = angle
    return (m * m - j * j, 2 * m * j, m * m + j * j)


def check(term: PolariserTerm, start: PolariserStart) -> None:
    """The refusals by name: m from 1 and j from 0 to m; two sets with distinct names; the levels integer arrays of one shape within the width."""
    m, j = term.angle
    if m < 1 or j < 0 or j > m:
        raise ValueError(
            f"the polariser's angle is a pair (m, j) with m from 1 and j from 0 to m, got {term.angle}"
        )
    first, second = term.sets
    if not first or not second or first == second:
        raise ValueError(f"the polariser names two distinct sets, got {term.sets!r}")
    if start.re.shape != start.im.shape or start.re.dtype != np.int64 or start.im.dtype != np.int64:
        raise ValueError("the record's pair at the polariser is two int64 arrays of one shape")
    if start.re.size and int(np.max(np.abs(start.re))) + int(np.max(np.abs(start.im))) > MAX_WORK_INT:
        raise ValueError("the record's levels at the polariser reach the width")


def turned_back(re: np.ndarray, im: np.ndarray, triple: Triple) -> tuple[np.ndarray, np.ndarray]:
    """The transport's rotation by minus the angle (ALGEBRA.md #the-transport): R_re = (2 c re + 2 s im + d) div 2 d and R_im = (2 c im - 2 s re + d) div 2 d, two read acts of Rule3 with the coefficients (2 c, 2 s) and (2 c, -2 s) on the two levels, the load d, the wall 2 d, the remainder not kept."""
    c, s, d = triple
    load, wall = d, 2 * d
    levels = (re.astype(object), im.astype(object), 0)
    new_re = rule3((2 * c, 2 * s, 0), levels, 0, wall, 0, 0, load)[0]
    new_im = rule3((-2 * s, 2 * c, 0), levels, 0, wall, 0, 0, load)[0]
    return np.asarray(new_re).astype(np.int64), np.asarray(new_im).astype(np.int64)


def apply(term: PolariserTerm, start: PolariserStart, own: PolariserOwn) -> PolariserWrites:
    """The primitive at (ii) for one record at one polariser body: the pair turned back by the body's angle, the first set offered the squared level along the axis and the second the squared level across it (bookings, no division), whatever the pair's own angle: at j = 0 the pair passes to the first set whole, at j = m it swaps."""
    check(term, start)
    re, im = turned_back(start.re, start.im, triple_of(term.angle))
    first = re.astype(object) * re.astype(object)
    second = im.astype(object) * im.astype(object)
    return PolariserWrites(re, im, first, second)


def read_term(body: dict[str, Any]) -> PolariserTerm | None:
    """The term of a body's `polariser` key as the file writes it, None for a body with no key (it polarises nothing)."""
    entry = body.get("polariser")
    if entry is None:
        return None
    m, j = entry["angle"]
    first, second = entry["sets"]
    return PolariserTerm((int(m), int(j)), (str(first), str(second)))


DECLARATION = Declaration(
    name="the polariser",
    place="(ii)",
    reads=(
        "the record's pair at a polariser body's Nodes",
        "the polariser's angle",
        "the body's two sets",
    ),
    writes=("the level next, the remainder", "the second level"),
    function=apply,
    section="ALGEBRA.md #the-primitives, #the-transport",
    word="after the step",
    schema=Schema(
        {
            "a body": ObjectOf(
                {
                    "polariser": ObjectOf(
                        {"angle": ListOf(Integer(least=0), 2), "sets": ListOf(Word(), 2)}
                    )
                },
                frozenset({"polariser"}),
            )
        }
    ),
)
