"""The giving, the three acts of one window: the open (M_k -= 1 of the given family and the bulk share n_a -= sgn(n_a) x (|n_a| div M), at t + 1), the write (a_given at the shell += g x a_body, before the bookings), the close (at outward x den >= norm the record named, its direction the tally's sign per axis) (ALGEBRA.md 9.117 item 2 the row "the giving" and item 5, 9.107, 9.71 (1), 9.116 item 5); the count's close the click's inverse, the bulk share from the rule, the window's write beyond (H)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.register import Declaration

# the three acts of one window, the words the loop names in `start`
THE_OPEN = "the open"
THE_WRITE = "the write"
THE_CLOSE = "the close"
ACTS = (THE_OPEN, THE_WRITE, THE_CLOSE)

THE_WORD = (
    "the close of the count the click's inverse, the bulk share from the rule 9.57 (1), "
    "the window's write beyond (H)"
)

# THE SCHEMA: the emitter's keys as the loader checks them, each (key, kind,
# low, high, required); the kinds: "name" a family's name, "names" a list of set names,
# "integer" one integer in [low, high], "integers" a list of integers each in [low, high]
# (the branches' pairs, the given clock's pair). The bounds are the loader's of today
# (world.py: `weight`, `period` and `norm_denominator` from 1, `twist` from 0, each to
# 2^62 - 1; `norm` from 1 to 2^126 - 1).
NORM_BOUND = (1 << 126) - 1  # the loader's bound on `norm` (world.py NORM_BOUND)
AMOUNT_BOUND = (1 << 62) - 1  # the loader's bound on every other integer (world.py AMOUNT_BOUND)
SCHEMA: tuple[tuple[str, str, int, int, bool], ...] = (
    ("family", "name", 0, 0, True),
    ("weight", "integer", 1, AMOUNT_BOUND, True),
    ("period", "integer", 1, AMOUNT_BOUND, True),
    ("norm", "integer", 1, NORM_BOUND, True),
    ("norm_denominator", "integer", 1, AMOUNT_BOUND, False),
    ("twist", "integer", 0, AMOUNT_BOUND, True),
    ("receiver", "names", 0, 0, False),
    ("branches", "integers", 0, AMOUNT_BOUND, False),
    ("clock", "integers", 1, AMOUNT_BOUND, False),
)


@dataclass(frozen=True)
class GivingTerm:
    """The emitter's declaration for the window: the weight g, the quantum's norm as norm / norm_denominator, the given family's index."""

    weight: int
    norm: int
    norm_denominator: int
    family: int


@dataclass(frozen=True)
class GivingStart:
    """The interval's reading for one act: the act's word; at the open the body's quanta M and momentum n; at the write the body's levels at its shell; at the close this interval's outward flux and its tally."""

    act: str
    quanta: int = 0
    momentum: tuple[int, int, int] = (0, 0, 0)
    body_levels: np.ndarray | None = None
    outward_flux: int = 0
    outward_tally: tuple[int, int, int] = (0, 0, 0)


@dataclass(frozen=True)
class GivingOwn:
    """The window on the body's record: the intervals written so far (None when closed), the outward norm summed, its tally per axis."""

    window: int | None = None
    outward: int = 0
    tally: tuple[int, int, int] = (0, 0, 0)


@dataclass(frozen=True)
class GivingWrites:
    """The act's writes: the level write at the shell, the deferred count and momentum, the close with its direction, and the window's record after the act."""

    own: GivingOwn
    level: np.ndarray | None = None
    count: int = 0
    momentum: tuple[int, int, int] | None = None
    closed: bool = False
    direction: tuple[int, int, int] | None = None


def sign_of(value: int) -> int:
    return (value > 0) - (value < 0)


def bulk_share(momentum: tuple[int, int, int], quanta: int) -> tuple[int, int, int]:
    """n_a -= sgn(n_a) x (|n_a| div M): the quantum carries its whole share of the momentum and the body keeps the remainder inside n_a, symmetric under reflection (ALGEBRA.md 9.116 item 5)."""
    return (
        momentum[0] - sign_of(momentum[0]) * (abs(momentum[0]) // quanta),
        momentum[1] - sign_of(momentum[1]) * (abs(momentum[1]) // quanta),
        momentum[2] - sign_of(momentum[2]) * (abs(momentum[2]) // quanta),
    )


def check(term: GivingTerm, start: GivingStart, own: GivingOwn) -> None:
    """The refusals by name: the weight, the norm and its denominator from 1; the act one of the three; an open on an open window, a write or a close on none; the quanta from 1 at the open; the write without the body's levels."""
    if term.weight < 1 or term.norm < 1 or term.norm_denominator < 1:
        raise ValueError(
            f"the giving needs a weight, a norm and its denominator from 1, got g = {term.weight}, "
            f"norm = {term.norm} / {term.norm_denominator} (ALGEBRA.md 9.71 (1))"
        )
    if start.act not in ACTS:
        raise ValueError(f"the giving's act is one of {list(ACTS)}, got {start.act!r}")
    if start.act == THE_OPEN and own.window is not None:
        raise ValueError("the giving opens a window while one is open: one window per body")
    if start.act != THE_OPEN and own.window is None:
        raise ValueError(f"the giving's act {start.act!r} on a body with no open window")
    if start.act == THE_OPEN and start.quanta < 1:
        raise ValueError(f"the giving needs quanta from 1 at the open, got M = {start.quanta}")
    if start.act == THE_WRITE and start.body_levels is None:
        raise ValueError("the giving's write needs the body's levels at its shell")


def apply(term: GivingTerm, start: GivingStart, own: GivingOwn) -> GivingWrites:
    """The primitive, one act per call: the open, the write or the close (ALGEBRA.md 9.117 item 2 the row "the giving")."""
    check(term, start, own)
    if start.act == THE_OPEN:
        return GivingWrites(
            GivingOwn(0, 0, (0, 0, 0)), count=-1, momentum=bulk_share(start.momentum, start.quanta)
        )
    assert own.window is not None
    if start.act == THE_WRITE:
        assert start.body_levels is not None
        level = term.weight * np.asarray(start.body_levels, dtype=np.int64)
        return GivingWrites(GivingOwn(own.window + 1, own.outward, own.tally), level=level)
    outward = own.outward + start.outward_flux
    tally = (
        own.tally[0] + start.outward_tally[0],
        own.tally[1] + start.outward_tally[1],
        own.tally[2] + start.outward_tally[2],
    )
    if outward * term.norm_denominator >= term.norm:
        return GivingWrites(
            GivingOwn(None, outward, tally),
            closed=True,
            direction=(sign_of(tally[0]), sign_of(tally[1]), sign_of(tally[2])),
        )
    return GivingWrites(GivingOwn(own.window, outward, tally))


DECLARATION = Declaration(
    "the giving",
    "(ii)",
    (
        "the body's own record's click (the open)",
        "the body's rotation at its shell",
        "the emitter's weight g",
        "the outward flux through the body's outer Ports over the window, and its tally per axis",
        "the quantum's norm T as norm / den",
        "a body's content M_k and its momentum n",
    ),
    ("a family's level at a Node", "a body's content M_k", "a body's momentum n"),
    {"a body's content M_k": 2, "a body's momentum n": 1},
    apply,
    THE_WORD + " (9.117 item 5); 9.117 item 2, the row 'the giving'; 9.107; 9.71 (1); 9.116 item 5; "
    "9.86 (1)",
    word="after the step",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_emit` (the open with the record's birth) until the loop calls `apply` at the three acts."""
    return loop._method("_emit")  # type: ignore[no-any-return]
