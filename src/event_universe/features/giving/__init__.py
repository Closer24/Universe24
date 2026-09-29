"""The giving, two acts at the body's click (ALGEBRA.md #the-primitives the row "the giving" and "A BODY'S WRITE IS ONE ACT"; #the-counts-line, the free record): the write (a_given at the body's Nodes += (a_body x num + r) div den at both levels of the body's rotation, one act of the write per Node and level (features/write, the line the loop hands in the start; Rule3's division act on the row when none is handed), [num, den] the giving's coupling: the file's weight g as [g, 1]) and the birth (the born record carries the one quantum its count's lay laid from its form; the given family's content at the body falls by one). THE GIVING FIRES AT THE BODY'S CLICK (the model owner's word of 2026-09-29 on #1495, finding 10): every bound body gives at its click, once, and the record it gives is written once; no window stays open after it, and no count-down waits for it."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.rule3 import THE_ADVANCE, Key, division_forward

# the two acts of a giving, the words the loop names in `start`
THE_WRITE = "the write"
THE_BIRTH = "the birth"
ACTS = (THE_WRITE, THE_BIRTH)

THE_WORD = "the giving at the body's click: the write once, the birth of one quantum"
Counts = tuple[tuple[Key, int], ...]
Levels = tuple[tuple[Key, int, int], ...]
# the write's line (features/write): (act, wall, coefficient, the counts per key, values, carries) ->
# per key (key, now, before), the remainders written back into the two dicts
WriteLine = Callable[[str, int, int, Counts, dict[Key, int], dict[Key, int]], Levels]


@dataclass(frozen=True)
class GivingTerm:
    """The numbers of a giving: its coupling as a pair (numerator, denominator), the write (a_body x numerator + r) div denominator at every Node of the body, the numerator one integer or one per Node, the file's weight g as (g, 1); the given family's index."""

    coupling: tuple[int | np.ndarray, int]
    family: int


@dataclass(frozen=True)
class GivingStart:
    """The reading for one act, every field named by the loop: the act's word; at the birth the quanta the born record's count laid (one); at the write the body's two levels (now, before) at its Nodes (None at the birth); the write's line the loop hands (features/write; None: the folder's division act on the row)."""

    act: str
    quanta: int
    body_levels: tuple[np.ndarray, np.ndarray] | None
    write: WriteLine | None = None


@dataclass(frozen=True)
class GivingOwn:
    """The remainders of the write's division at the body's Nodes, one per level (None before the write)."""

    remainders: tuple[np.ndarray, np.ndarray] | None = None


@dataclass(frozen=True)
class GivingWrites:
    """The act's writes: the level write at the body's Nodes at both levels (None at the birth), the change of the given family's content at the body (-1 at the birth), and the remainders after the act."""

    own: GivingOwn
    level: tuple[np.ndarray, np.ndarray] | None
    count: int


def check(term: GivingTerm, start: GivingStart) -> None:
    """The refusals by name: the coupling from 1; the act one of the two; the write without the body's levels; a birth whose record carries other than one quantum."""
    if np.min(term.coupling[0]) < 1 or term.coupling[1] < 1:
        raise ValueError(
            f"the giving needs the coupling's pair from 1, got "
            f"{[np.asarray(term.coupling[0]).tolist(), term.coupling[1]]} (ALGEBRA.md #the-primitives)"
        )
    if start.act not in ACTS:
        raise ValueError(f"the giving's act is one of {list(ACTS)}, got {start.act!r}")
    if start.act == THE_WRITE and start.body_levels is None:
        raise ValueError("the giving's write needs the body's two levels at its Nodes")
    if start.act == THE_BIRTH and start.quanta != 1:
        raise ValueError(
            "the birth bears one quantum: the born record's count laid from its form carries "
            f"{start.quanta} (ALGEBRA.md #the-counts-line, the free record)"
        )


def apply(term: GivingTerm, start: GivingStart, own: GivingOwn) -> GivingWrites:
    """The primitive, one act per call: the write or the birth (ALGEBRA.md #the-primitives the row "the giving")."""
    check(term, start)
    if start.act == THE_BIRTH:
        return GivingWrites(own, None, -1)
    assert start.body_levels is not None
    carries: tuple[np.ndarray | int, ...] = own.remainders if own.remainders is not None else (0, 0)
    written, remainders = zip(
        *(
            divided(term.coupling, np.asarray(level, dtype=np.int64), carry, start.write)
            for level, carry in zip(start.body_levels, carries, strict=True)
        ),
        strict=True,
    )
    return GivingWrites(GivingOwn(remainders), written, 0)


def divided(
    coupling: tuple[int | np.ndarray, int],
    levels: np.ndarray,
    carry: np.ndarray | int,
    line: WriteLine | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """The write at every Node of the body: (level x numerator + r) div denominator written and the remainder r' in [0, denominator) kept at the Node, the numerator one integer or one per Node, one act of the write's line per Node at the advance (the Node its key) when the loop hands it, else Rule3's division act on the row (ALGEBRA.md #the-interval, #the-primitives the row "the write")."""
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


DECLARATION = Declaration(
    "the giving",
    "(ii)",
    (
        "the body's own record's click (its clock's crossing)",
        "the body's rotation at its Nodes",
        "the giving's coupling, the file's weight g",
        "the born record's count as its lay laid it",
    ),
    ("a family's level at a Node", "a body's content M_k", "the count at a Node"),
    apply,
    THE_WORD + " (ALGEBRA.md #the-primitives, the row 'the giving'; ALGEBRA.md #the-counts-line)",
    word="after the step",
)
