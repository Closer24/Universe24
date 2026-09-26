"""THE SOURCE, the folder source (ALGEBRA.md 9.117 item 2, the row "the source"; 9.117 item 5;
9.108 items 3, 10, 11, 13; 9.116 item 4b; 9.112 row 6; the Boss's records 2217 and 2221; the
run files of examples/events/source/).

9.113 item 2: THE FIELD'S SHAPE IS FROM THE RULE 9.57 (1) (the sourced family steps by its own
pair, and its stationary level is the rule's own response (Delta - kappa^2) a = - sigma / q with
kappa^2 = 6 den / num - 6, 9.108 item 11); THE WRITE IS BEYOND THE RULE (H): a record's count
added into another family's level is a declared term, the window's write of 9.71 (1) (b) with no
close.

THE LINE. A family declared `sourced` by a record family gains, at every Node of the record's
support, the record's local count each interval:

  D_i = now_i^2 - next_i x before_i      (the record's invariant at the step's end, 9.108 item 13)
  s_i = (D_i + r_i) div E_s,  r_i' = (D_i + r_i) mod E_s,  0 <= r_i' < E_s
  level_i += weight x s_i

E_s the scale, an integer of the universe from 1; `weight` a nonzero integer; the remainder r_i
the primitive's own record at the Node (core/primitive.py, Own; 9.91 (2), (3)), carried so that
the sum of the counts over any run of intervals is the exact floor of the sum of D_i / E_s. WITH
A TABLE (9.108 item 3) the count saturates, s_i = s_cap D_i div (s_cap E_s + D_i), the quotient
alone: the modulus moves with D_i, so no remainder is kept (a declaration beyond the rule).
D_i is never negative for a bounded rotation (A^2 sin^2 omega for one rotation); a negative D_i
is a growing level, which the guard ends, and is refused here by name. THE INVERSE subtracts the
same integers and restores the remainder: r_i = s_i E_s + r_i' - D_i (`invert`); the trace's hand
identity per Node is after = before + weight x ((D_i + r_i) div E_s) (`hand_identity`).

The loop forms D_i (before, now and the step's output next of (i)) and hands it in as the
argument; the folder never forms it and reads no level of its own. The place: (iv), the word
the right side, order 2 after the hold (1) on "a family's level at a Node". Writes: the sourced
family's level at the record's Nodes; the record's remainder is the primitive's own. The
declaration is the row of ALGEBRA.md 9.117; no `bind`: the loop has no source today, so a term
naming it is refused until the loop's cut calls `apply` (its red test, tests/test_ledger_items.py
test 3a; the run files, examples/events/source/). Integers only: int64 arrays, no float, no
family's name, no number of the universe.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from event_universe.core.register import Declaration

# the words of ALGEBRA.md 9.113 item 2 and 9.117 item 5 on this folder
THE_WORD = "the field's shape from the rule 9.57 (1), the write beyond (H)"
# the products of the table form stay inside int64 (the loader's overflow bound, 9.116 item 6b)
PRODUCT_BOUND = 1 << 62


@dataclass(frozen=True)
class SourceTerm:
    """The sourced family's declaration from the run's files (`sourced` {of, weight, scale,
    cap}): the sourced family (the target) and the record family (the argument's owner) by
    index, the signed weight, the scale E_s and the table's cap (None for the plain form)."""

    target: int
    of: int
    weight: int
    scale: int
    cap: int | None = None


@dataclass(frozen=True)
class SourceStart:
    """The interval's start as this primitive reads it: the GameBoard's shape and the record
    family's D_i at every Node, formed by the loop from before, now and the step's output."""

    shape: tuple[int, ...]
    argument: np.ndarray


@dataclass
class SourceOwn:
    """The primitive's own record: the remainder r_i at every Node, 0 <= r_i < E_s (the plain
    form; the table form keeps none and its array stays zero)."""

    remainders: np.ndarray


@dataclass(frozen=True)
class SourceWrites:
    """The write into the sourced family's level at the Nodes where the count is nonzero
    (`at`, a mask; `integers` the weight times the count there), the count itself at every
    Node, and the remainder after."""

    at: np.ndarray
    integers: np.ndarray
    counts: np.ndarray
    remainders: np.ndarray
    reads: dict[str, Any] = field(default_factory=dict)


def check(term: SourceTerm, start: SourceStart, own: SourceOwn) -> None:
    """The refusals by name: the scale from 1, the weight nonzero, the cap from 1, the shapes
    the GameBoard's, the argument never negative, the table's products inside the bound."""
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
    if start.argument.size and int(start.argument.min()) < 0:
        node = np.unravel_index(int(np.argmin(start.argument)), start.shape)
        raise ValueError(
            f"the record's D_i is {int(start.argument.min())} at the Node "
            f"{tuple(int(i) for i in node)}: a growing level, which the guard ends (9.108 item 13)"
        )
    if term.cap is not None and start.argument.size:
        largest = int(start.argument.max())
        if term.cap * largest >= PRODUCT_BOUND or term.cap * term.scale + largest >= PRODUCT_BOUND:
            raise ValueError(
                f"the source's table products s_cap x D_i = {term.cap} x {largest} leave the bound "
                f"{PRODUCT_BOUND} (9.116 item 6b)"
            )


def counts_of(
    term: SourceTerm, argument: np.ndarray, remainders: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """The count s_i at every Node and the remainder after: the plain form divides D_i plus the
    carried remainder by E_s and keeps the rest; the table form saturates and keeps none."""
    if term.cap is None:
        total = argument + remainders
        return total // term.scale, total % term.scale
    counts = (term.cap * argument) // (term.cap * term.scale + argument)
    return counts, np.zeros_like(remainders)


def apply(term: SourceTerm, start: SourceStart, own: SourceOwn) -> SourceWrites:
    """The primitive: the count at every Node of the record's support and the write of weight
    times the count into the sourced family's level where the count is nonzero."""
    check(term, start, own)
    counts, remainders = counts_of(term, start.argument, own.remainders)
    at = counts != 0
    return SourceWrites(at, term.weight * counts, counts, remainders)


def invert(
    term: SourceTerm, start: SourceStart, own_after: SourceOwn, writes: SourceWrites
) -> tuple[np.ndarray, SourceOwn]:
    """The inverse (9.91 (8), backward): the same integers subtracted from the level (returned
    as the write's negative) and the remainder before restored, r_i = s_i E_s + r_i' - D_i for
    the plain form, zero for the table form."""
    if term.cap is None:
        before = writes.counts * term.scale + own_after.remainders - start.argument
    else:
        before = np.zeros_like(own_after.remainders)
    return -writes.integers, SourceOwn(before)


def hand_identity(
    term: SourceTerm, argument: int, remainder: int, level_before: int, level_after: int
) -> bool:
    """The trace's hand check at one Node (9.112 item 5): after = before + weight x count with
    the count from the same integers the trace line shows."""
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
)
