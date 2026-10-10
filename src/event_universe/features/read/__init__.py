"""The read: the content c = SUM over the reads of (weight x the read family's time line) at the Node, the reading row's own level among it where it holds the content (ALGEBRA.md #the-paces, Every row reads the content), the clock p_0 = Gamma (1 - 1 / Gamma)^c and the Node's pace p_i = p_0^2 / Gamma on its six Links the composed paces' two functions of the content (core/paces.py, The paces compose); and each Link's factor Q_ij from the Link's tension, the held rows' axis parts at its two ends, t_a(i, j) = (weight x (aa_i + aa_j) + 1) div 2, one number per Link read the same from both ends and never per Node per axis, booked squared as one integer per Link in the unit G^2 of the run's Link unit (`core.rule3.link_factor`), no floor and no clamp; the Node's pace along each axis from its two a-Links' factors by their mean, the write's rulers (`axis_paces`); and the guard, two-sided, at every Node as squares, the lower side a content at or beyond the Link's zero (`paces.frozen_content`, where the Node's pace rounds to 0: a pace never below 0 under the composed paces, so the branch below 0 is met by no content) and every Link's factor above 0, the upper side p^2 (den + |num|) <= 2 den Gamma^2 on the clock, on the Node's pace and on each Link's pace p_i^2 Q_ij / G^2 (the band's lowest mode at or above -2, at wave number pi for a numerator at or above 0 and at wave number 0 for one below it: no exponential growth, the edge itself a repeated root admitted), read once on the whole initial state at load and never in the interval (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's; The guard; the root leaves the run; #the-interval, the dependency radius; #the-primitives, The tension)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import division_forward, largest_below, link_factor


def plain(level: Any, sign: bool) -> Any:
    """A holder's level as the plain read takes it into a pace: a holder of the content's as it is, of either sign (a level below 0 a hill, the clock above the vacuum's), and a holder of the sign's as its size |L|, a hollow whatever the reader's sense, so that charge conjugation, the sense flipped and the level with it, leaves the physics (ALGEBRA.md row (f), The sign holder rotates the two-part record: a plane reads the holder of the sign plainly into its pace, a hollow whatever its sense, under the act pace; the advisor's hand); under the rotation the turn takes the signed level and this read is not made."""
    return np.abs(level) if sign else level


def content_of(reads: Sequence[tuple[int, Any]]) -> Any:
    """c = SUM over the reads of (weight x the read family's time line) at every Node, the reading row's own among them where it holds the content; 0 where a family reads nothing (the plain rule at Gamma)."""
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


def link_tensions(axes: Sequence[tuple[int, Sequence[Any]]], wrap: Wrap) -> tuple[Any, ...]:
    """The tension of each of a Node's six Links in Port order (ALGEBRA.md #the-primitives, The tension; #the-interval, the dependency radius): from the read rows' axis lines at the Link's two ends, the neighbour's read through the Port the arrival is read through (`link_tension`, `arrival`; 0 beyond a face, a Node with no level), `axes` per read its weight and its three axis lines; the integer 0 on every Link where no row carries axis lines."""
    found = []
    for axis in range(3):
        for side in (1, -1):
            ends = [
                (weight, lines[axis], arrival(lines[axis], axis, side, wrap)) for weight, lines in axes
            ]
            found.append(link_tension(ends))
    return tuple(found)


def link_factors(gamma: int, unit: int, tensions: Sequence[Any]) -> tuple[Any, ...]:
    """The factor of each of a Node's six Links in Port order, Q_ij from the Link's tension (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's), booked once per Link as the integer Q_ij in the unit G^2 (`link_factor`)."""
    return tuple(link_factor(gamma, unit, tension) for tension in tensions)


def axis_paces(gamma: int, pace: Any, tensions: Sequence[Any]) -> tuple[Any, Any, Any]:
    """The Node's pace along each axis, (p_x, p_y, p_z), from its pace p_i and its six Links' tensions in Port order: p_a = p_i (q_(+a) + q_(-a)) / (2 Gamma) rounded once, the mean of the two a-Links' factors q = Gamma - t (`paces.axis_pace`), the rulers h_a = p_0 / p_a of the write per proper volume (ALGEBRA.md, The write per proper volume and per proper interval)."""
    found = [
        paces.axis_pace(pace, gamma, tensions[2 * axis], tensions[2 * axis + 1]) for axis in range(3)
    ]
    return found[0], found[1], found[2]


def stability_bound(pair: tuple[int, int], gamma: int) -> tuple[int, int]:
    """The guard's upper side as one integer comparison, p^2 x left <= right with left = den + |num| and right = 2 den Gamma^2: the band's lowest mode stays at or above -2, at wave number pi for a numerator at or above 0, (S - 6 R) / w = 2 - 2 (1 + num / den) (p / Gamma)^2, and at wave number 0 for one below it, (S + 6 R) / w = 2 - 2 (1 - num / den) (p_0 / Gamma)^2 (the pair [-1, 2] at Gamma = 4 with the content -1 reads -23 / 8 there under the edge of den + num, the audit's witness); so the guard excludes exponential growth, and at the edge itself, 2 cos omega = -2, a repeated root, the unrounded line grows linearly (light's vacuum checkerboard at wave number pi), admitted (ALGEBRA.md #the-paces, the guard)."""
    num, den = pair
    return den + abs(num), 2 * den * gamma * gamma


def edge_squared(pair: tuple[int, int], gamma: int) -> int:
    """The edge's square P^2 = right div left, so that p^2 x left <= right exactly when p^2 <= P^2; no root is taken."""
    left, right = stability_bound(pair, gamma)
    return int(division_forward(right, left, 0)[0])


def edge_of(pair: tuple[int, int], gamma: int) -> int:
    """The edge's pace P, the largest integer whose square is at or below the edge's square, by the search on the share reading, `rule3.largest_below` (the loader's own act, never a root in the run): the largest clock and the largest pace the guard admits, a hill's, Gamma where num = den; the loader reads the amplitude bound at it (ALGEBRA.md #the-bound)."""
    return largest_below(edge_squared(pair, gamma))


def at_the_node(value: Any, node: tuple[Any, ...]) -> int:
    """A read integer at one Node, for the guard's refusal by name."""
    return int(np.asarray(value)[node]) if np.ndim(value) else int(value)


def paces_guard(
    pair: tuple[int, int], gamma: int, unit: int, content: Any, factors: tuple[Any, ...], name: str
) -> None:
    """The guard at load, two-sided and on squares (ALGEBRA.md #the-paces, The guard): the content below the Link's zero at every Node (the lower side: at `paces.frozen_content` the Node's pace p_0^2 / Gamma rounds to 0, a frozen clock, where under the composed paces no pace is ever below 0) and every Link's factor above 0 (a Link's factor 0 the Link closed, its tension at Gamma); the clock's square, the Node's pace squared and each Link's pace squared, p_i^2 Q_ij over G^2, at or below the edge's square (the upper side, p^2 (den + num) <= 2 den Gamma^2 read as p_i^2 Q_ij (den + num) <= 2 den Gamma^2 G^2 on a Link, no division; a hill's clock above Gamma); a state outside refuses the run naming the Node, the Port and the family."""
    left, right = stability_bound(pair, gamma)
    edge = edge_squared(pair, gamma)
    clock, pace = paces.node_paces(gamma, content)
    deepest, frozen = int(np.max(content)), paces.frozen_content(gamma)
    if deepest >= frozen:
        node = np.unravel_index(int(np.argmax(content)), np.shape(content))
        raise ValueError(
            f"the content of {name!r} is {deepest} at the Node {tuple(int(i) for i in node)} at load, at or "
            f"beyond {frozen}, where the Node's pace p_0^2 / Gamma rounds to 0 at Gamma = {gamma}, a frozen "
            "clock (ALGEBRA.md #the-paces, the guard's lower side); the run is refused"
        )
    for port, factor in enumerate(factors):
        least = int(np.min(factor))
        if least <= 0:
            node = np.unravel_index(int(np.argmin(factor)), np.shape(factor))
            raise ValueError(
                f"the Link's factor of {name!r} (the Port {port}) is {least} at the Node "
                f"{tuple(int(i) for i in node)} at load: the Link's factor stays above 0, its tension below "
                f"Gamma = {gamma} (ALGEBRA.md #the-paces, the guard's lower side); the run is refused"
            )
    squares = [clock * clock, pace * pace]
    for number, square in enumerate(squares):
        high = int(np.max(square))
        if high > edge:
            node = np.unravel_index(int(np.argmax(square)), np.shape(square))
            raise ValueError(
                f"the pace of {name!r} ({'the Node' if number else 'the clock'}) squared is {high} "
                f"at the Node {tuple(int(i) for i in node)} at "
                f"load, above the stability edge's square {edge} of its pair {list(pair)} at Gamma = {gamma} "
                f"(p^2 x {left} <= {right}; ALGEBRA.md #the-paces, the guard's upper side: a hill beyond the edge); "
                "the run is refused"
            )
    room = right * unit * unit
    for port, factor in enumerate(factors):
        weighed = pace * pace * factor * left
        high = int(np.max(weighed))
        if high > room:
            node = np.unravel_index(int(np.argmax(weighed)), np.shape(weighed))
            raise ValueError(
                f"the pace of {name!r} (the Port {port}) squared is {at_the_node(pace * pace * factor, node)} "
                f"in the unit G^2 = {unit * unit} at the Node {tuple(int(i) for i in node)} at load, above the "
                f"stability edge's square {edge} of its pair {list(pair)} at Gamma = {gamma} (p_i^2 Q_ij x {left} "
                f"<= {room}; ALGEBRA.md #the-paces, the guard's upper side: a hill beyond the edge); the run is refused"
            )
