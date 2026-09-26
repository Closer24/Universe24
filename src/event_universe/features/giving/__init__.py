"""THE GIVING, the folder giving (ALGEBRA.md 9.117 item 2, the row "the giving"; 9.117
item 5; 9.107; 9.71 (1); 9.116 item 5's note; 9.86 (1); the Boss's records 2223 and
2230; issue #1156).

THE WORDS OF 9.117 ITEM 5: the close of the count is THE CLICK'S INVERSE (M_k -= 1 of
the given family, 9.107); THE BULK SHARE IS FROM THE RULE (the rule's conserved momentum
shared by the quantum that leaves, 9.84 (1), 9.86 (1)); THE WINDOW'S WRITE IS BEYOND THE
RULE (H): a count written into a level is a load, as the hold's.

THE LINE, three acts of one window (9.71 (1)):
  the open, at the body's own record's click (the excitation's rung): the window opens;
    the given family's quantum leaves the body's count, M_k -= 1, and the momentum's
    bulk share leaves with it, per axis
      n_a -= sgn(n_a) x (|n_a| div M),
    M the body's live quanta before the giving: the quantum carries the whole share and
    the body keeps the remainder |n_a| mod M inside n_a (momentum conserved exactly in
    integers; the velocity n / W on the live wall W = 3 Q M kept within one unit of n on
    the new wall, exactly where M divides n_a, as on the moving rows); the two writes
    enter at t + 1 with the click's (9.111 item 6), where the engine moves the quantum
    (9.107 item 2, commit 7);
  the write, at every interval of the window, after the given record's own step and
    before the bookings read the rows (9.71 (1) (b), the interval's last act on them):
      a_given(shell) += g x a_body(shell),
    g the emitter's declared weight, the shell the body's Nodes with a Port to the
    outside (a one-Node body its one Node);
  the close, after the interval's bookings (9.71 (1) (c), (d)): the outward flux through
    the body's outer Ports, booked by the loop, is summed on the window; at the first
    interval with outward x den >= norm (T, the quantum's norm, as the exact rational
    norm / den) the writing ends, the record is named, and its four-vector's space part
    is the sign per axis of the summed outward tally (9.111 item 1; the recoil at (iv)
    reads it with the giver's sign).

The place: (ii), the word after the step; the orders per value (9.117 item 3): on a
body's content M_k 2 after the clicks (1), on a body's momentum n 1 before the recoil
(2), both ordered at (iv) as a click's deferred writes; the record's four-vector's
space part is the giving line's, the loop's output. The loop calls `apply` with the act
named in `start` (THE_OPEN, THE_WRITE, THE_CLOSE) and enters each act's writes at its
moment; the record's birth (its seed, its residue u and wheel W, its ladder) is the
loop's, not this primitive's. `bind` is cut 2's binding to the loop's `_emit`, bit for
bit, until the loop's cut calls `apply`. The schema is the emitter's keys, their kinds
and integer bounds as the loader checks them today (record 2226); no default: a key the
engine reads is declared.
"""

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

# THE SCHEMA (record 2226): the emitter's keys as the loader checks them, each (key, kind,
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
    """The emitter's declaration for the window: the weight g, the quantum's norm T as
    the exact rational norm / norm_denominator, and the given family's index."""

    weight: int
    norm: int
    norm_denominator: int
    family: int


@dataclass(frozen=True)
class GivingStart:
    """The interval's reading for one act: the act's word; at the open the body's live
    quanta M and its momentum n; at the write the body's rotation at its shell Nodes
    (after its own step this interval); at the close this interval's outward flux
    through the outer Ports and its tally per axis, as the loop booked them."""

    act: str
    quanta: int = 0
    momentum: tuple[int, int, int] = (0, 0, 0)
    body_levels: np.ndarray | None = None
    outward_flux: int = 0
    outward_tally: tuple[int, int, int] = (0, 0, 0)


@dataclass(frozen=True)
class GivingOwn:
    """The window on the body's record: the intervals written so far (None when no
    window is open), the outward norm summed and its tally per axis."""

    window: int | None = None
    outward: int = 0
    tally: tuple[int, int, int] = (0, 0, 0)


@dataclass(frozen=True)
class GivingWrites:
    """The act's writes: the level write at the shell (the write act); the deferred count
    (-1 of the given family) and momentum (the open act, entered at t + 1); the close
    (the record named) with its direction, the sign per axis of the tally; and the
    window's own record after the act."""

    own: GivingOwn
    level: np.ndarray | None = None
    count: int = 0
    momentum: tuple[int, int, int] | None = None
    closed: bool = False
    direction: tuple[int, int, int] | None = None


def sign_of(value: int) -> int:
    return (value > 0) - (value < 0)


def bulk_share(momentum: tuple[int, int, int], quanta: int) -> tuple[int, int, int]:
    """n_a -= sgn(n_a) x (|n_a| div M): the quantum that leaves carries its whole share of
    the body's momentum and the body keeps the remainder inside n_a; symmetric under
    reflection (the share rounded toward zero on both signs)."""
    return (
        momentum[0] - sign_of(momentum[0]) * (abs(momentum[0]) // quanta),
        momentum[1] - sign_of(momentum[1]) * (abs(momentum[1]) // quanta),
        momentum[2] - sign_of(momentum[2]) * (abs(momentum[2]) // quanta),
    )


def check(term: GivingTerm, start: GivingStart, own: GivingOwn) -> None:
    """The refusals by name: the weight, the norm and its denominator from 1; the act one
    of the three; the open on an open window, the write or the close on none, refused; at
    the open the quanta from 1 (a body with no quantum gives none)."""
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
    """The primitive, one act per call: the open (the deferred count and bulk share, the
    window opened), the write (g x the body's levels at the shell, the window's count),
    the close (the outward flux summed; at outward x den >= norm the record named with
    its direction)."""
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
    """Cut 2's binding: the loop's method `_emit`, resolved at each call (the open with the
    record's birth); the loop's next cut calls `apply` at the three acts."""
    return loop._method("_emit")  # type: ignore[no-any-return]
