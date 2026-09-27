"""The signed read with the two-sided guard: p_0 = Gamma - SUM over the reads of (weight x by x argument), the axes' paces with the tensor's parts, and 0 < p <= P with P = isqrt(Gamma^2 (18 den + 6 num) div (18 num + 6 den)) at every Node (ALGEBRA.md 9.117 item 2 row 1 and item 5, 9.78 (4), 9.108 item 12); from the rule. `content_of` is this read's one place: the loop's `_effective_content` calls it."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from math import isqrt
from typing import Any

import numpy as np

from event_universe.core.register import Declaration
from event_universe.core.schema import (
    Either,
    Integer,
    IntegerName,
    ListOf,
    Name,
    ObjectOf,
    OneOf,
    Schema,
)

# by "plain" reads the level as it is; by "sign" reads it with the reading family's own sign q
BY_PLAIN = "plain"
BY_SIGN = "sign"

# the sum of the reads stays within int64: the reach of the products is bounded before any is formed
TOTAL_BOUND = (1 << 63) - 1

# the two words of ALGEBRA.md 9.113 item 1 and 9.117 item 5: this primitive is the rule's own
THE_WORD = "from the rule 9.57 (1) and the click"


@dataclass(frozen=True)
class SignedReadTerm:
    """The reading family's declaration: its reads (family, signed weight, by), its sign q, its pair and the Node clock Gamma."""

    reads: tuple[tuple[int, int, str], ...]
    q: int
    pair: tuple[int, int]
    gamma: int


@dataclass(frozen=True)
class SignedReadStart:
    """The interval's start: the GameBoard's shape, each read family's argument at every Node (a level, or D_i for a pair), the axis contents or None."""

    shape: tuple[int, ...]
    arguments: Mapping[int, np.ndarray]
    axis_contents: tuple[np.ndarray, ...] | None


@dataclass(frozen=True)
class SignedReadOwn:
    """The reading family's identity for the guard's line: its index, its name, the interval."""

    family: int
    name: str
    interval: int


@dataclass(frozen=True)
class SignedReadWrites:
    """The paces in the loop's form: the content c with p_0 = Gamma - c, and the axis contents or None."""

    content: np.ndarray
    axis_contents: tuple[np.ndarray, ...] | None


def stability_bound(pair: tuple[int, int], gamma: int) -> tuple[int, int]:
    """The guard's upper side as one integer comparison, p^2 x left <= right with left = 18 num + 6 den and right = Gamma^2 (18 den + 6 num) (ALGEBRA.md 9.108 item 12)."""
    num, den = pair
    return 18 * num + 6 * den, gamma * gamma * (18 * den + 6 * num)


def pace_bound(pair: tuple[int, int], gamma: int) -> int:
    """The largest admitted pace P = isqrt(right div left), so that p^2 x left <= right exactly when p <= P."""
    left, right = stability_bound(pair, gamma)
    return isqrt(right // left)


def content_of(term: SignedReadTerm, start: SignedReadStart) -> np.ndarray:
    """c = SUM over the reads of (weight x by x argument) at every Node, a single plain read at weight 1 the argument itself; a read by another word, or a sum whose reach leaves int64, is refused by name before any product is formed."""
    if len(term.reads) == 1 and term.reads[0][1] == 1 and term.reads[0][2] == BY_PLAIN:
        return start.arguments[term.reads[0][0]]
    content = np.zeros(start.shape, dtype=np.int64)
    reach = 0
    for other, weight, by in term.reads:
        if by not in (BY_PLAIN, BY_SIGN):
            raise ValueError(
                f"the read of family {other} is by {by!r}: by {BY_PLAIN!r} or by {BY_SIGN!r} "
                "(ALGEBRA.md 9.48 (3))"
            )
        factor = weight if by == BY_PLAIN else -term.q * weight
        if factor:
            argument = start.arguments[other]
            reach += abs(factor) * int(np.max(np.abs(argument)))
            if reach > TOTAL_BOUND:
                raise ValueError(
                    f"the read of family {other} at the weight {weight} reaches {reach} with the "
                    f"argument's size {int(np.max(np.abs(argument)))}, beyond int64 {TOTAL_BOUND} "
                    "(ALGEBRA.md 9.61 (3))"
                )
            content = content + factor * argument
    return content


def guard(term: SignedReadTerm, writes: SignedReadWrites, own: SignedReadOwn) -> None:
    """The two-sided guard 0 < p <= P on p_0 and every axis pace; a pace outside ends the run naming the Node, the family and the interval (ALGEBRA.md 9.108 item 12)."""
    gamma = term.gamma
    left, right = stability_bound(term.pair, gamma)
    bound = pace_bound(term.pair, gamma)
    paces = [gamma - writes.content]
    if writes.axis_contents is not None:
        paces.extend(gamma - writes.content - t for t in writes.axis_contents)
    for axis, pace in enumerate(paces):
        low = int(np.min(pace))
        if low <= 0:
            node = np.unravel_index(int(np.argmin(pace)), pace.shape)
            raise RuntimeError(
                f"the pace of {own.name!r} (family {own.family}, axis {axis}) is {low} at the Node "
                f"{tuple(int(i) for i in node)} at interval {own.interval}: the pace stays above 0 "
                f"(the content {int(writes.content[node])} at or beyond Gamma = {gamma}; ALGEBRA.md "
                "9.108 item 12, the guard's lower side); the run ends"
            )
        high = int(np.max(pace))
        if high > bound:
            node = np.unravel_index(int(np.argmax(pace)), pace.shape)
            raise RuntimeError(
                f"the pace of {own.name!r} (family {own.family}, axis {axis}) is {high} at the Node "
                f"{tuple(int(i) for i in node)} at interval {own.interval}, above the stability "
                f"edge {bound} of its pair {list(term.pair)} at Gamma = {gamma} (p^2 x {left} <= "
                f"{right}; ALGEBRA.md 9.108 item 12, the guard's upper side: a hill beyond the edge); "
                "the run ends"
            )


def apply(term: SignedReadTerm, start: SignedReadStart, own: SignedReadOwn) -> SignedReadWrites:
    """The primitive: the paces from the reads, then the guard (ALGEBRA.md 9.117 item 2 row 1)."""
    content = content_of(term, start) if term.reads else np.zeros(start.shape, dtype=np.int64)
    writes = SignedReadWrites(content, start.axis_contents)
    guard(term, writes, own)
    return writes


DECLARATION = Declaration(
    "the signed read",
    "(i)",
    (
        "the read families' arguments at the interval's start (a level, or D_i for a pair)",
        "the signed weights",
        "by (plain, or q)",
        "the axis contents with their remainders",
    ),
    ("the paces",),
    apply,
    THE_WORD
    + " (9.117 item 5); 9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c",
    word="the right side",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {
                    "reads": ListOf(
                        ObjectOf(
                            {
                                "family": Name(),
                                "weight": Either((Integer(least=1), IntegerName())),
                                "twist": Either((Integer(least=0), OneOf(("own",)))),
                                "by": OneOf((1, "q")),
                            }
                        )
                    )
                }
            )
        }
    ),
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_effective_content`, which reads through `content_of`, until the loop calls `apply`."""
    return loop._method("_effective_content")  # type: ignore[no-any-return]
