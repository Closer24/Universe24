"""The source: a record's local count D_i, divided by the scale E_s with its remainder carried at the Node by one act of the write (features/write, the line the loop hands in the start; Rule3's carried division per Node when none is handed), added at the weight into another family's level (ALGEBRA.md #the-primitives rows "the source" and "the write"; ALGEBRA.md #the-paces, #the-primitives: the field's shape from the rule ALGEBRA.md #the-line, the write beyond (H))."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.rule3 import THE_ADVANCE, Key, carried
from event_universe.core.schema import Integer, Name, ObjectOf, Schema

THE_WORD = "the field's shape from the rule ALGEBRA.md #the-line, the write beyond (H)"
PRODUCT_BOUND = (int(np.iinfo(np.int64).max) + 1) // 2  # half the integer width, no number of its own
Counts = tuple[tuple[Key, int], ...]
Levels = tuple[tuple[Key, int, int], ...]
# the write's line (features/write): (act, wall, coefficient, the counts per key, values, carries) ->
# per key (key, now, before), the remainders written back into the two dicts
WriteLine = Callable[[str, int, int, Counts, dict[Key, int], dict[Key, int]], Levels]


@dataclass(frozen=True)
class SourceTerm:
    """The declaration `sourced` {of, weight, scale, cap}: the target and the record family by index, the signed weight, the scale E_s, the table's cap or None (ALGEBRA.md #the-paces)."""

    target: int
    of: int
    weight: int
    scale: int
    cap: int | None = None


@dataclass(frozen=True)
class SourceStart:
    """The interval's start: the GameBoard's shape and the record family's D_i at every Node, formed by the loop (ALGEBRA.md #the-paces); the write's line the loop hands (features/write; None: the folder's carried division per Node)."""

    shape: tuple[int, ...]
    argument: np.ndarray
    write: WriteLine | None = None


@dataclass
class SourceOwn:
    """The primitive's own record: the remainder r_i at every Node, 0 <= r_i < E_s, zero under a table (ALGEBRA.md #the-interval)."""

    remainders: np.ndarray


@dataclass(frozen=True)
class SourceWrites:
    """The write into the sourced family's level: the mask of nonzero counts, the weight times the count, the count, the remainder after (ALGEBRA.md #the-primitives row "the source")."""

    at: np.ndarray
    integers: np.ndarray
    counts: np.ndarray
    remainders: np.ndarray


def check(term: SourceTerm, start: SourceStart, own: SourceOwn) -> None:
    """The refusals by name: the scale from 1, the weight nonzero, the cap from 1, the shapes the GameBoard's, int64 alone, the table's products inside the bound (ALGEBRA.md)."""
    if term.scale < 1:
        raise ValueError(
            f"the source's scale E_s is {term.scale}: an integer from 1 (ALGEBRA.md #the-paces)"
        )
    if term.weight == 0:
        raise ValueError("the source's weight is 0: a nonzero integer (the ledger's source row)")
    if term.cap is not None and term.cap < 1:
        raise ValueError(
            f"the source's table cap s_cap is {term.cap}: an integer from 1 (ALGEBRA.md #the-paces)"
        )
    if start.argument.shape != start.shape or own.remainders.shape != start.shape:
        raise ValueError(
            f"the source's argument {start.argument.shape} and remainder {own.remainders.shape} "
            f"are shaped by the GameBoard {start.shape}"
        )
    if start.argument.dtype != np.int64 or own.remainders.dtype != np.int64:
        raise ValueError("the source's argument and remainder are int64 arrays (integers only)")
    if term.cap is not None and start.argument.size:
        largest = int(np.abs(start.argument).max())
        if term.cap * largest >= PRODUCT_BOUND or term.cap * term.scale + largest >= PRODUCT_BOUND:
            raise ValueError(
                f"the source's table products s_cap x D_i = {term.cap} x {largest} leave the bound "
                f"{PRODUCT_BOUND} (ALGEBRA.md)"
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


def counts_of(
    term: SourceTerm, argument: np.ndarray, remainders: np.ndarray, line: WriteLine = carried_line
) -> tuple[np.ndarray, np.ndarray]:
    """The count s_i and the remainder after: plain, (D_i + r_i) div E_s and mod E_s by one act of the write's line at every Node with a count or a remainder (the Node its key, the advance; a Node with neither writes 0 and keeps 0); with a table, s_cap D_i div (s_cap E_s + D_i) and no remainder (ALGEBRA.md #the-paces)."""
    if term.cap is None:
        nodes = [
            tuple(int(index) for index in node)
            for node in np.argwhere((argument != 0) | (remainders != 0))
        ]
        counts, after = np.zeros_like(argument), remainders.copy()
        carries: dict[Key, int] = {node: int(remainders[node]) for node in nodes}
        written = line(
            THE_ADVANCE, term.scale, 1, tuple((node, int(argument[node])) for node in nodes), {}, carries
        )
        for node, (_, now, _) in zip(nodes, written, strict=True):
            counts[node], after[node] = now, carries[node]
        return counts, after
    counts = (term.cap * argument) // (term.cap * term.scale + argument)
    return counts, np.zeros_like(remainders)


def apply(term: SourceTerm, start: SourceStart, own: SourceOwn) -> SourceWrites:
    """The primitive at (iv): the count at every Node and the write of weight x count where the count is nonzero, the product inside the bound (ALGEBRA.md #the-primitives row "the source")."""
    check(term, start, own)
    line = start.write if start.write is not None else carried_line
    counts, remainders = counts_of(term, start.argument, own.remainders, line)
    if counts.size and abs(term.weight) * int(np.abs(counts).max()) >= PRODUCT_BOUND:
        raise ValueError(
            f"the source's write weight x count = {term.weight} x {int(np.abs(counts).max())} leaves "
            f"the bound {PRODUCT_BOUND} (ALGEBRA.md)"
        )
    return SourceWrites(counts != 0, term.weight * counts, counts, remainders)


def invert(
    term: SourceTerm, start: SourceStart, own_after: SourceOwn, writes: SourceWrites
) -> tuple[np.ndarray, SourceOwn]:
    """The step back: the same integers subtracted (the write's negative) and the remainder before restored, r_i = s_i E_s + r_i' - D_i, zero under a table (ALGEBRA.md #the-interval)."""
    if term.cap is None:
        before = writes.counts * term.scale + own_after.remainders - start.argument
    else:
        before = np.zeros_like(own_after.remainders)
    return -writes.integers, SourceOwn(before)


def hand_identity(
    term: SourceTerm, argument: int, remainder: int, level_before: int, level_after: int
) -> bool:
    """The trace's hand check at one Node: after = before + weight x count from the same integers (ALGEBRA.md #the-interval)."""
    if term.cap is None:
        count = (argument + remainder) // term.scale
    else:
        count = (term.cap * argument) // (term.cap * term.scale + argument)
    return level_after == level_before + term.weight * count


DECLARATION = Declaration(
    "the source",
    "(iv)",
    (
        "the record's D_i at its Nodes from the step's end (before, now, next of (i))",
        "E_s",
        "with a table s_cap",
        "the record's remainder, kept in Own",
    ),
    ("a family's level at a Node", "the record's remainder"),
    apply,
    THE_WORD + " (ALGEBRA.md #the-primitives); ALGEBRA.md #the-primitives, #the-paces",
    word="the right side",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {
                    "sourced": ObjectOf(
                        {
                            "of": Name(),
                            "weight": Integer(),
                            "scale": Integer(least=1),
                            "cap": Integer(least=1),
                        },
                        frozenset({"cap"}),
                    )
                },
                frozenset({"sourced"}),
            )
        }
    ),
)
