"""The read: the content c = SUM over the reads of (weight x the read family's time line), p_0^2 = (Gamma - c)^2 + c^2, the axes' contents from the held row's axis lines, (weight x the aa line + 1) div 2, no floor and no clamp, and the guard 0 < p and p^2 (den + num) <= 2 den Gamma^2 at every Node as squares, read once on the whole initial state at load and never in the interval (ALGEBRA.md #the-paces, the root leaves the run)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np

from event_universe.core.rule3 import division_forward, link_paces


def content_of(reads: Sequence[tuple[int, Any]]) -> Any:
    """c = SUM over the reads of (weight x the read family's time line) at every Node; 0 where a family reads nothing (the plain rule at Gamma)."""
    content: Any = 0
    for weight, level in reads:
        content = content + weight * level
    return content


def axis_content(reads: Sequence[tuple[int, Any]]) -> Any:
    """t_a = SUM over the reads of (weight x the read family's aa line + 1) div 2 at every Node, one division per read rounded at the read, no remainder kept (ALGEBRA.md #the-paces)."""
    content: Any = 0
    for weight, level in reads:
        content = content + division_forward(weight * level, 2, 1)[0]
    return content


def stability_bound(pair: tuple[int, int], gamma: int) -> tuple[int, int]:
    """The guard's upper side as one integer comparison, p^2 x left <= right with left = den + num and right = 2 den Gamma^2: the mode at wave number pi, (S - 6 R) / w = 2 - 2 (1 + num / den) (p / Gamma)^2, stays at or above -2 (ALGEBRA.md #the-paces)."""
    num, den = pair
    return den + num, 2 * den * gamma * gamma


def edge_squared(pair: tuple[int, int], gamma: int) -> int:
    """The edge's square P^2 = right div left, so that p^2 x left <= right exactly when p^2 <= P^2; no root is taken."""
    left, right = stability_bound(pair, gamma)
    return int(division_forward(right, left, 0)[0])


def squared_paces(gamma: int, content: Any, axis_contents: tuple[Any, Any, Any]) -> list[Any]:
    """The clock's square p_0^2 = (Gamma - c)^2 + c^2 and each Link's pace p_a = Gamma - 2 c - t_a at every Node, the Link's paces as they are (integers) and the clock's as its square, in the order clock, x, y, z."""
    return [
        (gamma - content) * (gamma - content) + content * content,
        *link_paces(gamma, content, axis_contents),
    ]


def guard(
    pair: tuple[int, int], gamma: int, content: Any, axis_contents: tuple[Any, Any, Any], name: str
) -> None:
    """The guard at load, two-sided and on squares: every Link's pace above 0 and every pace's square at or below the edge's square (the clock's square is never 0); a state outside refuses the run naming the Node and the family (ALGEBRA.md #the-paces, the guard)."""
    left, right = stability_bound(pair, gamma)
    edge = edge_squared(pair, gamma)
    clock, *links = squared_paces(gamma, content, axis_contents)
    for axis, pace in enumerate(links):
        low = int(np.min(pace))
        if low <= 0:
            node = np.unravel_index(int(np.argmin(pace)), np.shape(pace))
            raise ValueError(
                f"the pace of {name!r} (axis {axis}) is {low} at the Node {tuple(int(i) for i in node)} at load: "
                f"the pace stays above 0 (the content {int(np.asarray(content)[node]) if np.ndim(content) else content} "
                f"at the Node: the Link's pace Gamma - 2 c - t_a at or below 0 at Gamma = {gamma}; ALGEBRA.md "
                "#the-paces, the guard's lower side); the run is refused"
            )
    squares = [clock, *(pace * pace for pace in links)]
    for number, square in enumerate(squares):
        high = int(np.max(square))
        if high > edge:
            node = np.unravel_index(int(np.argmax(square)), np.shape(square))
            raise ValueError(
                f"the pace of {name!r} ({f'axis {number - 1}' if number else 'the clock'}) squared is {high} "
                f"at the Node {tuple(int(i) for i in node)} at "
                f"load, above the stability edge's square {edge} of its pair {list(pair)} at Gamma = {gamma} "
                f"(p^2 x {left} <= {right}; ALGEBRA.md #the-paces, the guard's upper side: a hill beyond the edge); "
                "the run is refused"
            )
