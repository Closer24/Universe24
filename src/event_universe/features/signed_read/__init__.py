"""THE SIGNED READ WITH THE TWO-SIDED GUARD (ALGEBRA.md 9.117 item 2, the first row;
9.117 item 5; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c; the Boss's
record 2224).

FROM THE RULE 9.57 (1): the line is the rule's own pace p = Gamma - c + q Lambda d
(9.78 (4)), and the guard is the rule's own stability (9.108 item 12); the folder
builds this sum and this edge and no formula of its own. It is the engine's read
(`_effective_content`) moved into its own folder with the guard added; when the
loop binds the folder, the engine's copy goes.

THE LINE. A family that declares `reads` lowers its pace at every Node by the
weighted sum of the read families' arguments at the interval's start:

  c = SUM over the reads of (weight x by x argument),   p_0 = Gamma - c,

`weight` a signed integer (a hollow positive, a hill negative), `by` 1 for "plain"
or -q for "sign" with q the reading family's own sign, the argument a phase-1
family's level at the Node (a phase-2 family's invariant D_i = now^2 - next x
before of the last step, when such a read is declared: 9.108 item 13; the loop
hands the argument in, the folder never forms it). The axes' paces p_a = p_0 - t_a
carry the tensor's parts (9.91 (2)); the loop hands t_a in.

THE GUARD, the same primitive's check after its write (9.108 item 12): the step is
stable where the rule's factor (S - 6 R) / w at the band's edge (the checkerboard
mode) stays at or above -2, that is

  0 < p   and   p^2 (18 num + 6 den) <= Gamma^2 (18 den + 6 num),

the pair [num, den] the reading family's; the upper side is compared as p <= P
with P = isqrt(Gamma^2 (18 den + 6 num) div (18 num + 6 den)), one integer per
family, exactly the same test and no product of paces (a product of two paces of
10^8 wraps a 64-bit integer). P = Gamma exactly for a massless family, 1.0152
Gamma for [800, 850], 1.0028 Gamma for [800, 809]. A pace outside ends the run
with the guard's line naming the Node, the family and the interval; nothing wraps
and nothing is clipped. With no negative weight declared (hollows alone) the upper
side never fires and the lower side is today's refusal at Gamma, so every such
world is bit for bit; a hill (a like charge read by sign, a negative weight) is
admitted up to P and refused beyond it, where today's guard admits up to 2 Gamma
and the rule's checkerboard mode grows.

The place: (i), the word the right side (the paces are read by the step of this
interval). Writes: the paces (as the content c and the axis contents, the loop's
form). Order: none, the only writer of the paces. `bind` is cut 2's binding to the
loop's method of today; `apply` is the primitive the loop's next cut calls.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from math import isqrt
from typing import Any

import numpy as np

from event_universe.core.register import Declaration

# by "plain" reads the level as it is; by "sign" reads it with the reading family's own sign q
BY_PLAIN = "plain"
BY_SIGN = "sign"

# the two words of ALGEBRA.md 9.113 item 1 and 9.117 item 5: this primitive is the rule's own
THE_WORD = "from the rule 9.57 (1) and the click"


@dataclass(frozen=True)
class SignedReadTerm:
    """The reading family's declaration, from the run's files: its reads as (the read
    family, the signed weight, by), its own sign q, its pair [num, den] and the Node
    clock Gamma of the universe."""

    reads: tuple[tuple[int, int, str], ...]
    q: int
    pair: tuple[int, int]
    gamma: int


@dataclass(frozen=True)
class SignedReadStart:
    """The interval's start: the GameBoard's shape, the argument of every read family
    at every Node (a phase-1 family its level, a phase-2 family its D_i, formed by the
    loop), and the axis contents t_a the loop already divided with their remainders
    (None where no read's tensor part was ever sourced: the rule isotropic)."""

    shape: tuple[int, ...]
    arguments: Mapping[int, np.ndarray]
    axis_contents: tuple[np.ndarray, ...] | None = None


@dataclass(frozen=True)
class SignedReadOwn:
    """The reading family's own identity, for the guard's line: its index, its
    name and the interval."""

    family: int
    name: str
    interval: int


@dataclass(frozen=True)
class SignedReadWrites:
    """The paces, in the loop's form: the content c (p_0 = Gamma - c) at every Node
    and the axis contents t_a (p_a = p_0 - t_a), None where isotropic."""

    content: np.ndarray
    axis_contents: tuple[np.ndarray, ...] | None


def stability_bound(pair: tuple[int, int], gamma: int) -> tuple[int, int]:
    """The upper side of the guard as one comparison in integers: p is admitted
    where p^2 x left <= right, left = 18 num + 6 den and right = Gamma^2 (18 den + 6
    num) (ALGEBRA.md 9.108 item 12: the factor (S - 6 R) / w = -2 there)."""
    num, den = pair
    return 18 * num + 6 * den, gamma * gamma * (18 * den + 6 * num)


def pace_bound(pair: tuple[int, int], gamma: int) -> int:
    """The largest admitted pace P = isqrt(right div left): for integers p^2 x left <=
    right exactly when p <= P, so the guard compares paces and never their squares."""
    left, right = stability_bound(pair, gamma)
    return isqrt(right // left)


def content_of(term: SignedReadTerm, start: SignedReadStart) -> np.ndarray:
    """c = SUM over the reads of (weight x by x argument) at every Node; zeros for a
    family that reads nothing; a single plain read at weight 1 is the argument
    itself (the loop's form, no copy)."""
    if len(term.reads) == 1 and term.reads[0][1] == 1 and term.reads[0][2] == BY_PLAIN:
        return start.arguments[term.reads[0][0]]
    content = np.zeros(start.shape, dtype=np.int64)
    for other, weight, by in term.reads:
        factor = weight if by == BY_PLAIN else -term.q * weight
        if factor:
            content = content + factor * start.arguments[other]
    return content


def guard(term: SignedReadTerm, writes: SignedReadWrites, own: SignedReadOwn) -> None:
    """The two-sided guard on p_0 and on every axis pace: 0 < p <= P at every Node,
    P the pace bound of the family's pair (p^2 (18 num + 6 den) <= Gamma^2 (18 den +
    6 num)); the run ends with the line naming the Node, the family and the interval
    where a pace falls outside."""
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
    """The primitive: the paces from the reads, then the guard on both sides."""
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
    None,
    apply,
    THE_WORD + " (9.117 item 5); 9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; "
    "9.116 items 4a and 4c",
    word="the right side",
)


def bind(loop: Any) -> Callable[..., object]:
    """Cut 2's binding: the loop's method `_effective_content`, resolved at each call,
    which `apply` equals bit for bit (its test); the loop's next cut calls `apply` in its
    place and the engine's copy goes."""
    return loop._method("_effective_content")  # type: ignore[no-any-return]
