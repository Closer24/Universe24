"""The giving, the three acts of one window and their inverse: the open (M_k -= 1 of the given family and the bulk share n_a -= sgn(n_a) x (|n_a| div M), at t + 1), the write (a_given at the shell += (a_body x num + r) div den at both levels of the body's rotation, one act of the write per Node and level (features/write, the line the loop hands in the start; Rule3's division act on the row when none is handed) with the remainder r carried at the Node, [num, den] the giving's coupling: the universe's pair [1, k], or the file's weight g as [g, 1] until the loader reads the universe's, before the bookings), the close (at outward >= T, the universe's quantum action, the record named, its direction the tally's sign per axis), and the inverse of a write (the levels written that interval and the remainders before them, from the same body levels and the remainders after) (ALGEBRA.md #the-primitives the row "the giving" and "A BODY'S WRITE IS ONE ACT"; 9.107); the count's close the click's inverse, the bulk share from the rule, the window's write beyond (H)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE, Key, division_forward

# the three acts of one window, the words the loop names in `start`
THE_OPEN = "the open"
THE_WRITE = "the write"
THE_CLOSE = "the close"
ACTS = (
    THE_OPEN,
    THE_WRITE,
    THE_CLOSE,
    THE_INVERSE,
)  # the inverse: a write stepped back, Rule3's own word

THE_WORD = (
    "the close of the count the click's inverse, the bulk share from the rule ALGEBRA.md #the-line, "
    "the window's write beyond (H)"
)
Counts = tuple[tuple[Key, int], ...]
Levels = tuple[tuple[Key, int, int], ...]
# the write's line (features/write): (act, wall, coefficient, the counts per key, values, carries) ->
# per key (key, now, before), the remainders written back into the two dicts
WriteLine = Callable[[str, int, int, Counts, dict[Key, int], dict[Key, int]], Levels]


@dataclass(frozen=True)
class GivingTerm:
    """The numbers of the window: the giving's coupling as a pair (numerator, denominator), the write (a_body x numerator + r) div denominator at every Node of the shell: the law's (M_pol(Node), E_s of the charge), the body's polarisation content at the Node over the charge's divisor, the numerator then one integer per Node of the shell (Cheshbon's 05:33Z), or the file's weight g as (g, 1) while the file declares it; the quantum's action T (the close at outward >= T); the given family's index."""

    coupling: tuple[int | np.ndarray, int]
    action: int
    family: int


@dataclass(frozen=True)
class GivingStart:
    """The interval's reading for one act, every field named by the loop: the act's word; at the open the body's quanta M and momentum n; at the write and at the inverse the body's two levels (now, before) at its shell (None at the other acts); at the close this interval's outward flux and its tally; the write's line the loop hands (features/write; None: the folder's division act on the row)."""

    act: str
    quanta: int
    momentum: tuple[int, int, int]
    body_levels: tuple[np.ndarray, np.ndarray] | None
    outward_flux: int
    outward_tally: tuple[int, int, int]
    write: WriteLine | None = None


@dataclass(frozen=True)
class GivingOwn:
    """The window on the body's record: the intervals written so far (None when closed), the outward norm summed, its tally per axis, and the remainders of the write's division at the shell's Nodes, one per level (None before the first write and after the close)."""

    window: int | None
    outward: int
    tally: tuple[int, int, int]
    remainders: tuple[np.ndarray, np.ndarray] | None = None


@dataclass(frozen=True)
class GivingWrites:
    """The act's writes: the level write at the shell at both levels (added at the write, subtracted at the inverse), the deferred count and momentum, the close with its direction, and the window's record after the act."""

    own: GivingOwn
    level: tuple[np.ndarray, np.ndarray] | None
    count: int
    momentum: tuple[int, int, int] | None
    closed: bool
    direction: tuple[int, int, int] | None


def sign_of(value: int) -> int:
    return (value > 0) - (value < 0)


def bulk_share(momentum: tuple[int, int, int], quanta: int) -> tuple[int, int, int]:
    """n_a -= sgn(n_a) x (|n_a| div M): the quantum carries its whole share of the momentum and the body keeps the remainder inside n_a, symmetric under reflection (ALGEBRA.md)."""
    return (
        momentum[0] - sign_of(momentum[0]) * (abs(momentum[0]) // quanta),
        momentum[1] - sign_of(momentum[1]) * (abs(momentum[1]) // quanta),
        momentum[2] - sign_of(momentum[2]) * (abs(momentum[2]) // quanta),
    )


def check(term: GivingTerm, start: GivingStart, own: GivingOwn) -> None:
    """The refusals by name: the coupling and the action from 1; the act one of the four; an open on an open window, a write, a close or an inverse on none; the quanta from 1 at the open; the write or the inverse without the body's levels; the inverse without a write to step back."""
    if np.min(term.coupling[0]) < 1 or term.coupling[1] < 1 or term.action < 1:
        raise ValueError(
            f"the giving needs the coupling's pair and the quantum action T from 1, got the coupling "
            f"{[np.asarray(term.coupling[0]).tolist(), term.coupling[1]]}, T = {term.action} (ALGEBRA.md)"
        )
    if start.act not in ACTS:
        raise ValueError(f"the giving's act is one of {list(ACTS)}, got {start.act!r}")
    if start.act == THE_OPEN and own.window is not None:
        raise ValueError("the giving opens a window while one is open: one window per body")
    if start.act != THE_OPEN and own.window is None:
        raise ValueError(f"the giving's act {start.act!r} on a body with no open window")
    if start.act == THE_OPEN and start.quanta < 1:
        raise ValueError(f"the giving needs quanta from 1 at the open, got M = {start.quanta}")
    if start.act in (THE_WRITE, THE_INVERSE) and start.body_levels is None:
        raise ValueError(f"the giving's {start.act} needs the body's two levels at its shell")
    if start.act == THE_INVERSE and (own.remainders is None or not own.window):
        raise ValueError("the giving's inverse steps back a write, and none is written on this window")


def apply(term: GivingTerm, start: GivingStart, own: GivingOwn) -> GivingWrites:
    """The primitive, one act per call: the open, the write or the close (ALGEBRA.md #the-primitives the row "the giving")."""
    check(term, start, own)
    if start.act == THE_OPEN:
        return GivingWrites(
            GivingOwn(0, 0, (0, 0, 0)), None, -1, bulk_share(start.momentum, start.quanta), False, None
        )
    assert own.window is not None
    if start.act == THE_WRITE:
        assert start.body_levels is not None
        carries: tuple[np.ndarray | int, ...] = own.remainders if own.remainders is not None else (0, 0)
        written, remainders = zip(
            *(
                divided(term.coupling, np.asarray(level, dtype=np.int64), carry, start.write)
                for level, carry in zip(start.body_levels, carries, strict=True)
            ),
            strict=True,
        )
        return GivingWrites(
            GivingOwn(own.window + 1, own.outward, own.tally, remainders), written, 0, None, False, None
        )
    if start.act == THE_INVERSE:
        levels = cast(tuple[np.ndarray, np.ndarray], start.body_levels)
        after = cast(tuple[np.ndarray, np.ndarray], own.remainders)
        undone, remainders = zip(
            *(
                divided_back(term.coupling, np.asarray(level, dtype=np.int64), carry)
                for level, carry in zip(levels, after, strict=True)
            ),
            strict=True,
        )
        return GivingWrites(
            GivingOwn(own.window - 1, own.outward, own.tally, remainders), undone, 0, None, False, None
        )
    outward = own.outward + start.outward_flux
    tally = (
        own.tally[0] + start.outward_tally[0],
        own.tally[1] + start.outward_tally[1],
        own.tally[2] + start.outward_tally[2],
    )
    if outward >= term.action:
        return GivingWrites(
            GivingOwn(None, outward, tally),
            None,
            0,
            None,
            True,
            (sign_of(tally[0]), sign_of(tally[1]), sign_of(tally[2])),
        )
    return GivingWrites(
        GivingOwn(own.window, outward, tally, own.remainders), None, 0, None, False, None
    )


def divided(
    coupling: tuple[int | np.ndarray, int],
    levels: np.ndarray,
    carry: np.ndarray | int,
    line: WriteLine | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """The write at every Node of the shell: (level x numerator + r) div denominator written and the remainder r' in [0, denominator) kept at the Node, the numerator one integer or one per Node, one act of the write's line per Node at the advance (the Node its key) when the loop hands it, else Rule3's division act on the row (ALGEBRA.md #the-interval, #the-primitives the row "the write")."""
    scaled = levels * coupling[0]
    if line is None:
        return cast(
            tuple[np.ndarray, np.ndarray],
            division_forward(scaled, coupling[1], carry),  # type: ignore[arg-type]
        )
    keys: list[Key] = [(index,) for index in range(levels.shape[0])]
    carried_in = np.broadcast_to(np.asarray(carry, dtype=np.int64), levels.shape)
    carries: dict[Key, int] = {key: int(rest) for key, rest in zip(keys, carried_in, strict=True)}
    counts = tuple((key, int(numerator)) for key, numerator in zip(keys, scaled, strict=True))
    written = line(THE_ADVANCE, coupling[1], 1, counts, {}, carries)
    return (
        np.array([now for _, now, _ in written], dtype=np.int64),
        np.array([carries[key] for key in keys], dtype=np.int64),
    )


def divided_back(
    coupling: tuple[int | np.ndarray, int], levels: np.ndarray, carry: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """The division act stepped back at every Node: from the same level and the remainder after, the remainder before is the remainder of (r' - level x num) div den and the written value (level x num + r - r') div den exactly, so the write and its inverse are a bijection on (level written, remainder)."""
    scaled: np.ndarray = levels * coupling[0]
    before = cast(np.ndarray, division_forward(carry - scaled, coupling[1], 0)[1])
    return cast(np.ndarray, division_forward(scaled + before - carry, coupling[1], 0)[0]), before


DECLARATION = Declaration(
    "the giving",
    "(ii)",
    (
        "the body's own record's click (the open)",
        "the body's rotation at its shell",
        "the giving's coupling at the shell's Nodes: the body's polarisation content there over the charge's divisor E_s",
        "the outward flux through the body's outer Ports over the window, and its tally per axis",
        "the universe's quantum action T",
        "a body's content M_k and its momentum n",
    ),
    ("a family's level at a Node", "a body's content M_k", "a body's momentum n"),
    apply,
    THE_WORD
    + " (ALGEBRA.md #the-primitives); ALGEBRA.md #the-primitives, the row 'the giving'; 9.107; ALGEBRA.md #the-primitives",
    word="after the step",
)
