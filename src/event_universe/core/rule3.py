"""RULE3, THE RULE IN ONE PLACE (ALGEBRA.md 9.57 (1), 9.50 (8), (9), (13), 9.91 (2); the model
owner's decisions of 2026-09-26 through the Boss, records 2237 and 2238, and his question of
16:33Z): one function steps every record at every Node, w a_next + r' = SUM_a R_a (arr_a+ +
arr_a-) + S a_now - w a_before + r, 0 <= r' < w; its inverse beside it; the form's Node term
and the integers of the paces from the same place; integers or the loop's arrays, no numpy here.
"""

from __future__ import annotations

from typing import Any

from event_universe.core.integer import bounded_gcd

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
    """The rule's integers at a Node from the paces, ((R_x, R_y, R_z), S, w); the isotropic rule at the axis contents zero, the plain first-order rule with weak_field False (ALGEBRA.md 9.57 (1), 9.91 (2), 9.50 (13))."""
    pace = gamma - content
    if not weak_field:
        read = pace * num
        return (read, read, read), 6 * den * content, 3 * den * gamma
    paces = (pace - axis_contents[0], pace - axis_contents[1], pace - axis_contents[2])
    gamma_squared = gamma * gamma
    reads = (
        2 * paces[0] * paces[0] * num,
        2 * paces[1] * paces[1] * num,
        2 * paces[2] * paces[2] * num,
    )
    squares = paces[0] * paces[0] + paces[1] * paces[1] + paces[2] * paces[2]
    self_coefficient = (
        12 * den * gamma_squared - 6 * (pace * pace + gamma_squared) * (den - num) - 4 * num * squares
    )
    return reads, self_coefficient, 6 * den * gamma_squared


def rule3(
    reads: Reads,
    arrivals: tuple[Any, ...],
    self_coefficient: Any,
    wall: Any,
    now: Any,
    before: Any,
    remainder: Any,
) -> tuple[Any, Any]:
    """One interval forward: w a_next + r' = SUM_a R_a arr_a + S a_now - w a_before + r, the remainder in [0, w); returns (a_next, r') (ALGEBRA.md 9.57 (1); the body's Node record's six reads are (2 a, 2 a, 2 a), 9.60 (2))."""
    total = reads[0] * arrivals[0]
    total += reads[1] * arrivals[1]
    total += reads[2] * arrivals[2]
    total += self_coefficient * now
    total -= wall * before
    total += remainder
    nxt = total // wall
    return nxt, total - wall * nxt


def rule3_inverse(
    reads: Reads,
    arrivals_of_before: tuple[Any, ...],
    self_coefficient: Any,
    wall: Any,
    now: Any,
    before: Any,
    remainder: Any,
) -> tuple[Any, Any]:
    """One interval back with the same integers, a_before the ceiling of (SUM_a R_a arr_a(before) + S a_now - w a_next - r') / w and r the difference, exact; returns (a_before, r) (ALGEBRA.md 9.50 (8), (9))."""
    total = reads[0] * arrivals_of_before[0]
    total += reads[1] * arrivals_of_before[1]
    total += reads[2] * arrivals_of_before[2]
    total += self_coefficient * before
    total -= wall * now + remainder
    a_before = -((-total) // wall)
    return a_before, wall * a_before - total


def form_term(self_coefficient: Any, wall: Any, now: Any, before: Any) -> Any:
    """The conserved form's term at one Node from the rule's integers, w (now^2 + before^2) - S now before (ALGEBRA.md 9.57 (1); BUILD.md section 26 items 36 and 44)."""
    return wall * (now * now + before * before) - self_coefficient * now * before


def rule_total_bound(
    num: int, den: int, gamma: int, content: int, amplitude: int, weak_field: bool
) -> int:
    """The largest total the rule reaches at a Node whose reads and levels stand at the amplitude bound A, 6 A R + A |S| + w (A + 1); below 2^63 or the world is refused (ALGEBRA.md 9.57 (2), 9.61 (3))."""
    reads, self_coefficient, wall = coefficients(num, den, gamma, content, ISOTROPIC, weak_field)
    return int(
        6 * amplitude * abs(reads[0]) + amplitude * abs(self_coefficient) + wall * (amplitude + 1)
    )


def rungs(weights: list[tuple[int, int]], steps: int) -> tuple[list[int], tuple[int, int]]:
    """The ladder's rungs b_k = (2 W C_k + Total) div (2 Total) from the cells' weights as pairs, and the total as the reduced pair (ALGEBRA.md 9.25 (2))."""
    denominator = 1
    for _, m in weights:
        denominator = denominator * m // bounded_gcd(denominator, m)  # the least common multiple
    scaled = [n * (denominator // m) for n, m in weights]
    total = sum(scaled)
    if total == 0:
        return [0] * len(weights), (0, 1)
    found = []
    cumulative = 0
    for value in scaled:
        cumulative += value
        found.append((2 * steps * cumulative + total) // (2 * total))
    common = bounded_gcd(total, denominator) or 1
    return found, (total // common, denominator // common)
