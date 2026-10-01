"""The read: the content c = SUM over the reads of (weight x the read family's time line) at the Node, p_0^2 = (Gamma - c)^2 + c^2, and the content of each of its six Links, 2 c_i + t_a(i, j), the Node's content twice (the pace's form as main holds it) and the Link's own tension from the held row's axis parts at its two ends, (weight x (aa_i + aa_j) + 1) div 2, the mean of the two ends' parts, one number per Link read the same from both ends and never per Node per axis, no floor and no clamp; and the guard 0 < p and p^2 (den + |num|) <= 2 den Gamma^2 at every Node as squares, on the clock and on the six Links, read once on the whole initial state at load and never in the interval (the band's lowest mode at or above -2, at wave number pi for a numerator at or above 0 and at wave number 0 for one below it: no exponential growth, the edge itself a repeated root admitted) (ALGEBRA.md #the-paces, the root leaves the run; #the-interval, the dependency radius; #the-primitives, The tension)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import division_forward, link_paces


def content_of(reads: Sequence[tuple[int, Any]]) -> Any:
    """c = SUM over the reads of (weight x the read family's time line) at every Node; 0 where a family reads nothing (the plain rule at Gamma)."""
    content: Any = 0
    for weight, level in reads:
        content = content + weight * level
    return content


def link_tension(reads: Sequence[tuple[int, Any, Any]]) -> Any:
    """t_a(i, j) = SUM over the reads of (weight x (aa_i + aa_j) + 1) div 2 on one Link: the mean of the Link's two ends' parts of the tension, each Node's own part h_a sourced into the read family's axis line aa, in one division per read per Link rounded at the read, no remainder kept, one number per Link read the same from both ends; weight x aa in a uniform level (ALGEBRA.md #the-primitives, The tension; #the-interval, the dependency radius)."""
    tension: Any = 0
    for weight, here, there in reads:
        tension = tension + division_forward(weight * (here + there), 2, 1)[0]
    return tension


def link_contents(
    content: Any, axes: Sequence[tuple[int, Sequence[Any]]], wrap: Wrap
) -> tuple[Any, ...]:
    """The content of each of a Node's six Links in Port order, 2 c_i + t_a(i, j) (ALGEBRA.md #the-paces; #the-interval, the dependency radius): the Node's own content twice, the pace's form as main holds it, and the Link's tension from the read rows' axis lines at its two ends, the neighbour's read through the Port the arrival is read through (`link_tension`, `arrival`; 0 beyond a face, a Node with no level), `axes` per read its weight and its three axis lines."""
    found = []
    for axis in range(3):
        for side in (1, -1):
            ends = [
                (weight, lines[axis], arrival(lines[axis], axis, side, wrap)) for weight, lines in axes
            ]
            found.append(content + content + link_tension(ends))
    return tuple(found)


def stability_bound(pair: tuple[int, int], gamma: int) -> tuple[int, int]:
    """The guard's upper side as one integer comparison, p^2 x left <= right with left = den + |num| and right = 2 den Gamma^2: the band's lowest mode stays at or above -2, at wave number pi for a numerator at or above 0, (S - 6 R) / w = 2 - 2 (1 + num / den) (p / Gamma)^2, and at wave number 0 for one below it, (S + 6 R) / w = 2 - 2 (1 - num / den) (p_0 / Gamma)^2 (the pair [-1, 2] at Gamma = 4 with the content -1 reads -23 / 8 there under the edge of den + num, the audit's witness); so the guard excludes exponential growth, and at the edge itself, 2 cos omega = -2, a repeated root, the unrounded line grows linearly (light's vacuum checkerboard at wave number pi), admitted (ALGEBRA.md #the-paces, the guard)."""
    num, den = pair
    return den + abs(num), 2 * den * gamma * gamma


def edge_squared(pair: tuple[int, int], gamma: int) -> int:
    """The edge's square P^2 = right div left, so that p^2 x left <= right exactly when p^2 <= P^2; no root is taken."""
    left, right = stability_bound(pair, gamma)
    return int(division_forward(right, left, 0)[0])


def guard(pair: tuple[int, int], gamma: int, content: Any, links: tuple[Any, ...], name: str) -> None:
    """The guard at load, two-sided and on squares: every Link's pace Gamma - 2 c_i - t_a(i, j) above 0 and every pace's square at or below the edge's square (the clock's square (Gamma - c)^2 + c^2 is never 0); a state outside refuses the run naming the Node, the Port and the family (ALGEBRA.md #the-paces, the guard)."""
    left, right = stability_bound(pair, gamma)
    edge = edge_squared(pair, gamma)
    paces = link_paces(gamma, links)
    for port, pace in enumerate(paces):
        low = int(np.min(pace))
        if low <= 0:
            node = np.unravel_index(int(np.argmin(pace)), np.shape(pace))
            raise ValueError(
                f"the pace of {name!r} (the Port {port}) is {low} at the Node {tuple(int(i) for i in node)} at load: "
                f"the pace stays above 0 (the Link's content {int(np.asarray(links[port])[node]) if np.ndim(links[port]) else links[port]} "
                f"at the Node: the Link's pace Gamma - 2 c_i - t_a(i, j) at or below 0 at Gamma = {gamma}; ALGEBRA.md "
                "#the-paces, the guard's lower side); the run is refused"
            )
    clock = (gamma - content) * (gamma - content) + content * content
    squares = [clock, *(pace * pace for pace in paces)]
    for number, square in enumerate(squares):
        high = int(np.max(square))
        if high > edge:
            node = np.unravel_index(int(np.argmax(square)), np.shape(square))
            raise ValueError(
                f"the pace of {name!r} ({f'the Port {number - 1}' if number else 'the clock'}) squared is {high} "
                f"at the Node {tuple(int(i) for i in node)} at "
                f"load, above the stability edge's square {edge} of its pair {list(pair)} at Gamma = {gamma} "
                f"(p^2 x {left} <= {right}; ALGEBRA.md #the-paces, the guard's upper side: a hill beyond the edge); "
                "the run is refused"
            )
