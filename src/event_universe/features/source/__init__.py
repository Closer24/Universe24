"""The source: a record's local count D_i, divided by the scale E_s with its remainder carried at the Node, added at the weight into another family's level (ALGEBRA.md 9.117 row "the source"; 9.108 items 3, 11, 13; 9.113 item 2: the field's shape from the rule 9.57 (1), the write beyond (H))."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.schema import Integer, Name, ObjectOf, Schema

THE_WORD = "the field's shape from the rule 9.57 (1), the write beyond (H)"
PRODUCT_BOUND = 1 << 62


@dataclass(frozen=True)
class SourceTerm:
    """The declaration `sourced` {of, weight, scale, cap}: the target and the record family by index, the signed weight, the scale E_s, the table's cap or None (ALGEBRA.md 9.108 items 3, 11)."""

    target: int
    of: int
    weight: int
    scale: int
    cap: int | None = None


@dataclass(frozen=True)
class SourceStart:
    """The interval's start: the GameBoard's shape and the record family's D_i at every Node, formed by the loop (ALGEBRA.md 9.108 item 13)."""

    shape: tuple[int, ...]
    argument: np.ndarray


@dataclass
class SourceOwn:
    """The primitive's own record: the remainder r_i at every Node, 0 <= r_i < E_s, zero under a table (ALGEBRA.md 9.91 (2), (3))."""

    remainders: np.ndarray


@dataclass(frozen=True)
class SourceWrites:
    """The write into the sourced family's level: the mask of nonzero counts, the weight times the count, the count, the remainder after (ALGEBRA.md 9.117 row "the source")."""

    at: np.ndarray
    integers: np.ndarray
    counts: np.ndarray
    remainders: np.ndarray


def check(term: SourceTerm, start: SourceStart, own: SourceOwn) -> None:
    """The refusals by name: the scale from 1, the weight nonzero, the cap from 1, the shapes the GameBoard's, int64 alone, the table's products inside the bound (ALGEBRA.md 9.116 item 6b)."""
    if term.scale < 1:
        raise ValueError(f"the source's scale E_s is {term.scale}: an integer from 1 (9.108 item 11)")
    if term.weight == 0:
        raise ValueError("the source's weight is 0: a nonzero integer (the ledger's source row)")
    if term.cap is not None and term.cap < 1:
        raise ValueError(f"the source's table cap s_cap is {term.cap}: an integer from 1 (9.108 item 3)")
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
                f"{PRODUCT_BOUND} (9.116 item 6b)"
            )


def counts_of(
    term: SourceTerm, argument: np.ndarray, remainders: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """The count s_i and the remainder after: plain, (D_i + r_i) div E_s and mod E_s; with a table, s_cap D_i div (s_cap E_s + D_i) and no remainder (ALGEBRA.md 9.108 items 3, 11)."""
    if term.cap is None:
        total = argument + remainders
        return total // term.scale, total % term.scale
    counts = (term.cap * argument) // (term.cap * term.scale + argument)
    return counts, np.zeros_like(remainders)


def apply(term: SourceTerm, start: SourceStart, own: SourceOwn) -> SourceWrites:
    """The primitive at (iv): the count at every Node and the write of weight x count where the count is nonzero, the product inside the bound (ALGEBRA.md 9.117 row "the source")."""
    check(term, start, own)
    counts, remainders = counts_of(term, start.argument, own.remainders)
    if counts.size and abs(term.weight) * int(np.abs(counts).max()) >= PRODUCT_BOUND:
        raise ValueError(
            f"the source's write weight x count = {term.weight} x {int(np.abs(counts).max())} leaves "
            f"the bound {PRODUCT_BOUND} (9.116 item 6b)"
        )
    return SourceWrites(counts != 0, term.weight * counts, counts, remainders)


def invert(
    term: SourceTerm, start: SourceStart, own_after: SourceOwn, writes: SourceWrites
) -> tuple[np.ndarray, SourceOwn]:
    """The step back: the same integers subtracted (the write's negative) and the remainder before restored, r_i = s_i E_s + r_i' - D_i, zero under a table (ALGEBRA.md 9.91 (8))."""
    if term.cap is None:
        before = writes.counts * term.scale + own_after.remainders - start.argument
    else:
        before = np.zeros_like(own_after.remainders)
    return -writes.integers, SourceOwn(before)


def hand_identity(
    term: SourceTerm, argument: int, remainder: int, level_before: int, level_after: int
) -> bool:
    """The trace's hand check at one Node: after = before + weight x count from the same integers (ALGEBRA.md 9.112 item 5)."""
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
    2,
    None,
    THE_WORD + " (9.113 item 2; 9.117 item 5); 9.117 item 2; 9.108 items 3, 10, 11, 13; 9.116 item 4b",
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
