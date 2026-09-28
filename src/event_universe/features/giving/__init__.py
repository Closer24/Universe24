"""The giving, the three acts of one window: the open (M_k -= 1 of the given family and the bulk share n_a -= sgn(n_a) x (|n_a| div M), at t + 1), the write (a_given at the shell += g x a_body at both levels of the body's rotation, one act of the write's line per Node at the wall 1, features/write; before the bookings), the close (at outward x den >= norm the record named, its direction the tally's sign per axis) (ALGEBRA.md #the-primitives the row "the giving" and item 5, 9.107, ALGEBRA.md); the count's close the click's inverse, the bulk share from the rule, the window's write beyond (H)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.rule3 import THE_ADVANCE, THE_LOAD, Key, carried

# the three acts of one window, the words the loop names in `start`
THE_OPEN = "the open"
THE_WRITE = "the write"
THE_CLOSE = "the close"
ACTS = (THE_OPEN, THE_WRITE, THE_CLOSE)
Counts = tuple[tuple[Key, int], ...]
Levels = tuple[tuple[Key, int, int], ...]
# the write's line (features/write): (act, wall, coefficient, the counts per key, values, carries) ->
# per key (key, now, before), the remainders written back into the two dicts
WriteLine = Callable[[str, int, int, Counts, dict[Key, int], dict[Key, int]], Levels]

THE_WORD = (
    "the close of the count the click's inverse, the bulk share from the rule ALGEBRA.md #the-line, "
    "the window's write beyond (H)"
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
    """The interval's reading for one act, every field named by the loop: the act's word; at the open the body's quanta M and momentum n; at the write the body's levels at its shell now and before (None at the other acts; the before level the now level when not handed) and the write's line the loop hands (features/write; None: the folder's carried division per Node); at the close this interval's outward flux and its tally."""

    act: str
    quanta: int
    momentum: tuple[int, int, int]
    body_levels: np.ndarray | None
    outward_flux: int
    outward_tally: tuple[int, int, int]
    body_levels_before: np.ndarray | None = None
    write: WriteLine | None = None


@dataclass(frozen=True)
class GivingOwn:
    """The window on the body's record: the intervals written so far (None when closed), the outward norm summed, its tally per axis."""

    window: int | None
    outward: int
    tally: tuple[int, int, int]


@dataclass(frozen=True)
class GivingWrites:
    """The act's writes: the level write at the shell at the record's two levels (now, before), the deferred count and momentum, the close with its direction, and the window's record after the act."""

    own: GivingOwn
    level: np.ndarray | None
    count: int
    momentum: tuple[int, int, int] | None
    closed: bool
    direction: tuple[int, int, int] | None
    level_before: np.ndarray | None = None


def sign_of(value: int) -> int:
    return (value > 0) - (value < 0)


def bulk_share(momentum: tuple[int, int, int], quanta: int) -> tuple[int, int, int]:
    """n_a -= sgn(n_a) x (|n_a| div M): the quantum carries its whole share of the momentum and the body keeps the remainder inside n_a, symmetric under reflection (ALGEBRA.md)."""
    return (
        momentum[0] - sign_of(momentum[0]) * (abs(momentum[0]) // quanta),
        momentum[1] - sign_of(momentum[1]) * (abs(momentum[1]) // quanta),
        momentum[2] - sign_of(momentum[2]) * (abs(momentum[2]) // quanta),
    )


def carried_line(
    act: str,
    wall: int,
    coefficient: int,
    counts: Counts,
    values: dict[Key, int],
    carries: dict[Key, int],
) -> Levels:
    """The write's line by Rule3's carried division alone, per key (coefficient x count + r) div wall with the remainder at the key: the folder's own when the loop hands no write, the same arithmetic features/write wraps."""
    return tuple(
        (key, *carried(act, key, coefficient * count, wall, values, carries)) for key, count in counts
    )


def shell_write(term: GivingTerm, start: GivingStart) -> tuple[np.ndarray, np.ndarray]:
    """The write at the body's shell as two intervals of one act of the write's line per Node at the wall 1: the body's level before loaded, then its level now advanced, the line's (now, before) the record's two levels, g the coefficient (ALGEBRA.md #the-primitives the rows "the giving" and "the write")."""
    assert start.body_levels is not None
    now = np.asarray(start.body_levels, dtype=np.int64)
    before = (
        now if start.body_levels_before is None else np.asarray(start.body_levels_before, dtype=np.int64)
    )
    line = start.write if start.write is not None else carried_line
    values: dict[Key, int] = {}
    carries: dict[Key, int] = {}
    line(
        THE_LOAD,
        1,
        term.weight,
        tuple(((i,), int(level)) for i, level in enumerate(before)),
        values,
        carries,
    )
    written = line(
        THE_ADVANCE,
        1,
        term.weight,
        tuple(((i,), int(level)) for i, level in enumerate(now)),
        values,
        carries,
    )
    return (
        np.array([level for _, level, _ in written], dtype=np.int64).reshape(now.shape),
        np.array([level for _, _, level in written], dtype=np.int64).reshape(now.shape),
    )


def check(term: GivingTerm, start: GivingStart, own: GivingOwn) -> None:
    """The refusals by name: the weight, the norm and its denominator from 1; the act one of the three; an open on an open window, a write or a close on none; the quanta from 1 at the open; the write without the body's levels."""
    if term.weight < 1 or term.norm < 1 or term.norm_denominator < 1:
        raise ValueError(
            f"the giving needs a weight, a norm and its denominator from 1, got g = {term.weight}, "
            f"norm = {term.norm} / {term.norm_denominator} (ALGEBRA.md)"
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
    """The primitive, one act per call: the open, the write or the close (ALGEBRA.md #the-primitives the row "the giving")."""
    check(term, start, own)
    if start.act == THE_OPEN:
        return GivingWrites(
            GivingOwn(0, 0, (0, 0, 0)), None, -1, bulk_share(start.momentum, start.quanta), False, None
        )
    assert own.window is not None
    if start.act == THE_WRITE:
        level, level_before = shell_write(term, start)
        return GivingWrites(
            GivingOwn(own.window + 1, own.outward, own.tally), level, 0, None, False, None, level_before
        )
    outward = own.outward + start.outward_flux
    tally = (
        own.tally[0] + start.outward_tally[0],
        own.tally[1] + start.outward_tally[1],
        own.tally[2] + start.outward_tally[2],
    )
    if outward * term.norm_denominator >= term.norm:
        return GivingWrites(
            GivingOwn(None, outward, tally),
            None,
            0,
            None,
            True,
            (sign_of(tally[0]), sign_of(tally[1]), sign_of(tally[2])),
        )
    return GivingWrites(GivingOwn(own.window, outward, tally), None, 0, None, False, None)


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
    apply,
    THE_WORD
    + " (ALGEBRA.md #the-primitives); ALGEBRA.md #the-primitives, the row 'the giving'; 9.107; ALGEBRA.md #the-primitives",
    word="after the step",
)
