"""The signed read: the content c = SUM over the reads of (weight x by x the read family's time part), p_0^2 = (Gamma - c)^2 + c^2, the axes' paces with the tensor's parts, no floor and no clamp, and the guard 0 < p and p^2 (den + num) <= 2 den Gamma^2 at every Node as squares, read once on the whole initial state at load and never in the interval (ALGEBRA.md #the-paces, the root leaves the run)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_forward, link_paces

# by "plain" reads the level as it is; by "sign" reads it with the reader's own sign q at the Node
BY_PLAIN = "plain"
BY_SIGN = "sign"

# the sum of the reads stays within int64: the reach of the products is bounded before any is formed
TOTAL_BOUND = MAX_WORK_INT  # the reads' sum within the work integer's width, the one place of the width


@dataclass(frozen=True)
class SignedReadTerm:
    """The reading family's declaration: its reads (family, weight, by), its sign q (an integer or one per Node, the sign of its own sense there), its pair and the Node clock Gamma."""

    reads: tuple[tuple[int, int, str], ...]
    q: Any
    pair: tuple[int, int]
    gamma: int


@dataclass(frozen=True)
class SignedReadStart:
    """The interval's start: the GameBoard's shape, each read family's time part at every Node, the axis contents or None."""

    shape: tuple[int, ...]
    arguments: Mapping[int, np.ndarray]
    axis_contents: tuple[np.ndarray, ...] | None


@dataclass(frozen=True)
class SignedReadOwn:
    """The reading family's identity for the guard's line: its index and its name."""

    family: int
    name: str


@dataclass(frozen=True)
class SignedReadWrites:
    """The paces as the rule reads them: the content c with p_0^2 = (Gamma - c)^2 + c^2 and p_a = Gamma - 2 c - t_a, and the axis contents t_a or None."""

    content: np.ndarray
    axis_contents: tuple[np.ndarray, ...] | None


def stability_bound(pair: tuple[int, int], gamma: int) -> tuple[int, int]:
    """The guard's upper side as one integer comparison, p^2 x left <= right with left = den + num and right = 2 den Gamma^2: the mode at wave number pi, (S - 6 R) / w = 2 - 2 (1 + num / den) (p / Gamma)^2, stays at or above -2 (ALGEBRA.md #the-paces)."""
    num, den = pair
    return den + num, 2 * den * gamma * gamma


def edge_squared(pair: tuple[int, int], gamma: int) -> int:
    """The edge's square P^2 = right div left, so that p^2 x left <= right exactly when p^2 <= P^2; no root is taken."""
    left, right = stability_bound(pair, gamma)
    return int(division_forward(right, left, 0)[0])


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
                "(ALGEBRA.md #the-paces)"
            )
        factor = weight if by == BY_PLAIN else -np.asarray(term.q) * weight
        size = int(np.max(np.abs(factor)))
        if size:
            argument = start.arguments[other]
            reach += size * int(np.max(np.abs(argument)))
            if reach > TOTAL_BOUND:
                raise ValueError(
                    f"the read of family {other} at the weight {weight} reaches {reach} with the "
                    f"argument's size {int(np.max(np.abs(argument)))}, beyond int64 {TOTAL_BOUND} "
                    "(ALGEBRA.md #the-rows-against-nature)"
                )
            content = content + factor * argument
    return content


def squared_paces(writes: SignedReadWrites, gamma: int) -> list[np.ndarray]:
    """The clock's square p_0^2 = (Gamma - c)^2 + c^2 and each Link's pace p_a = Gamma - 2 c - t_a at every Node, the Link's paces as they are (integers) and the clock's as its square, in the order clock, x, y, z."""
    content = writes.content
    axes = writes.axis_contents if writes.axis_contents is not None else (0, 0, 0)
    return [(gamma - content) * (gamma - content) + content * content, *link_paces(gamma, content, axes)]


def guard(term: SignedReadTerm, writes: SignedReadWrites, own: SignedReadOwn) -> None:
    """The guard at load, two-sided and on squares: every Link's pace above 0 and every pace's square at or below the edge's square (the clock's square is never 0); a state outside refuses the run naming the Node and the family (ALGEBRA.md #the-paces, the guard)."""
    gamma = term.gamma
    left, right = stability_bound(term.pair, gamma)
    edge = edge_squared(term.pair, gamma)
    clock, *links = squared_paces(writes, gamma)
    for axis, pace in enumerate(links):
        low = int(np.min(pace))
        if low <= 0:
            node = np.unravel_index(int(np.argmin(pace)), pace.shape)
            raise ValueError(
                f"the pace of {own.name!r} (family {own.family}, axis {axis}) is {low} at the Node "
                f"{tuple(int(i) for i in node)} at load: the pace stays above 0 "
                f"(the content {int(writes.content[node])} at the Node: the Link's pace Gamma - 2 c - t_a "
                f"at or below 0 at Gamma = {gamma}; ALGEBRA.md #the-paces, the guard's lower side); the run is refused"
            )
    squares = [clock, *(pace * pace for pace in links)]
    for label, square in zip(("the clock", "axis 0", "axis 1", "axis 2"), squares, strict=True):
        high = int(np.max(square))
        if high > edge:
            node = np.unravel_index(int(np.argmax(square)), square.shape)
            raise ValueError(
                f"the pace of {own.name!r} (family {own.family}, {label}) squared is {high} at the Node "
                f"{tuple(int(i) for i in node)} at load, above the stability edge's square {edge} of its "
                f"pair {list(term.pair)} at Gamma = {gamma} (p^2 x {left} <= {right}; ALGEBRA.md #the-paces, "
                "the guard's upper side: a hill beyond the edge); the run is refused"
            )


def apply(term: SignedReadTerm, start: SignedReadStart) -> SignedReadWrites:
    """The read: the content as it is, no floor, no clamp and no guard in the interval (ALGEBRA.md #the-paces)."""
    content = content_of(term, start) if term.reads else np.zeros(start.shape, dtype=np.int64)
    return SignedReadWrites(content, start.axis_contents)
