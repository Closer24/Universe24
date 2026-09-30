"""Rule3 in one place: one function steps every record at every Node in either direction, w a_next + r' = SUM_a R_a (arr_a+ + arr_a-) + S a_now - w a_before + r with the remainder kept in [0, w); the carried division, its division act with the remainder kept between intervals; the form's Node term and the integers of the paces beside it (ALGEBRA.md #the-line, #the-direction, #the-interval)."""

from __future__ import annotations

from math import isqrt
from typing import Any

import numpy as np

# the rule's three reads, one per axis of the Node (R_x, R_y, R_z); the three arrival
# sums (arr_a+ + arr_a-) of the same axes; integers or the loop's integer arrays
Reads = tuple[Any, Any, Any]

ISOTROPIC: tuple[int, int, int] = (0, 0, 0)


def coefficients(
    num: Any,
    den: Any,
    gamma: Any,
    content: Any,
    axis_contents: tuple[Any, ...] = ISOTROPIC,
    weak_field: bool = True,
) -> tuple[Reads, Any, Any]:
    """The rule's integers at a Node from the paces, ((R_x, R_y, R_z), S, w): the clock's square p_0^2 = (Gamma - c)^2 + c^2 and the Link's pace p_a = Gamma - 2 c - t_a (the level entering the clock once with its square over twice the clock and the Link twice, ALGEBRA.md #the-paces), R_a = 2 num p_a^2, S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM p_a^2, w = 6 den Gamma^2 (#the-line); the plain first-order rule with weak_field False."""
    pace = gamma - content
    if not weak_field:
        read = pace * num
        return (read, read, read), 6 * den * content, 3 * den * gamma
    clock_squared = pace * pace + content * content
    paces = link_paces(gamma, content, axis_contents)
    gamma_squared = gamma * gamma
    reads = (
        2 * paces[0] * paces[0] * num,
        2 * paces[1] * paces[1] * num,
        2 * paces[2] * paces[2] * num,
    )
    squares = paces[0] * paces[0] + paces[1] * paces[1] + paces[2] * paces[2]
    self_coefficient = 12 * (den * gamma_squared - (den - num) * clock_squared) - 4 * num * squares
    return reads, self_coefficient, 6 * den * gamma_squared


def link_paces(
    gamma: Any, content: Any, axis_contents: tuple[Any, ...] = ISOTROPIC
) -> tuple[Any, Any, Any]:
    """The Link's paces at a Node, p_a = Gamma - 2 c - t_a, the level on the Link twice and the axis content once (ALGEBRA.md #the-paces)."""
    pace = gamma - content - content
    return (pace - axis_contents[0], pace - axis_contents[1], pace - axis_contents[2])


def clock_pace(gamma: Any, content: Any) -> Any:
    """The clock's pace as an integer where a guard or a clock pair reads it: the integer square root of p_0^2 = (Gamma - c)^2 + c^2 (ALGEBRA.md #the-paces), Gamma - c + c^2 div 2 Gamma to the unit; on an array by Newton's integer iteration from above (Gamma + |c| is at or above the root), the descent stopping where it turns."""
    squared = (gamma - content) * (gamma - content) + content * content
    if not isinstance(squared, np.ndarray):
        return isqrt(int(squared))
    root = gamma + np.abs(content) + 1
    while True:
        lower = np.minimum(root, (root + squared // root) // 2)
        if np.array_equal(lower, root):
            return root
        root = lower


def rule3(
    reads: Reads,
    arrivals: tuple[Any, ...],
    self_coefficient: Any,
    wall: Any,
    now: Any,
    other: Any,
    carry: Any,
    direction: int = 1,
) -> tuple[Any, Any]:
    """One interval of Rule3 in `direction` sigma: u = sigma (SUM_a R_a arr_a + S a_now - w other) + carry, z = sigma (u div w), carry' = u mod w; +1 from (a_now, a_before, r) to (a_next, r'), -1 from (a_now, a_next, r') back to (a_before, r) (ALGEBRA.md #the-line, #the-direction)."""
    total = reads[0] * arrivals[0]
    total += reads[1] * arrivals[1]
    total += reads[2] * arrivals[2]
    total += self_coefficient * now
    total -= wall * other
    total = direction * total + carry
    quotient = total // wall
    return direction * quotient, total - wall * quotient


NO_READ = (0, 0, 0)


def division_forward(numerator: Any, wall: Any, carry: Any) -> tuple[Any, Any]:
    """Rule3's division act forward: (numerator + carry) div wall and the remainder, the line with no read and the numerator as the self coefficient on the level 1 (ALGEBRA.md #the-four-acts)."""
    return rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry, 1)


def division_back(numerator: Any, wall: Any, carry: Any) -> tuple[Any, Any]:
    """The division act one interval back by Rule3's direction -1: from the remainder after, the quotient the forward act wrote and the remainder before it, exact (ALGEBRA.md #the-direction)."""
    return rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry, -1)


def form_term(self_coefficient: Any, wall: Any, now: Any, before: Any) -> Any:
    """The conserved form's term at one Node from the rule's integers, w (now^2 + before^2) - S now before (ALGEBRA.md #the-conserved-form)."""
    return wall * (now * now + before * before) - self_coefficient * now * before


def rule_total_bound(
    num: int, den: int, gamma: int, content: int, amplitude: int, weak_field: bool
) -> int:
    """The largest total the rule reaches at a Node whose reads and levels stand at the amplitude bound A, 6 A R + A |S| + w (A + 1); below 2^63 or the world is refused (ALGEBRA.md #the-line, #the-rows-against-nature)."""
    reads, self_coefficient, wall = coefficients(num, den, gamma, content, ISOTROPIC, weak_field)
    return int(
        6 * amplitude * abs(reads[0]) + amplitude * abs(self_coefficient) + wall * (amplitude + 1)
    )
