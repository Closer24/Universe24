"""Rule3 in one place: one function steps every record at every Node in either direction, w a_next + r' = SUM_a R_a (arr_a+ + arr_a-) + S a_now - w a_before + r with the remainder kept in [0, w); the carried division, its division act with the remainder kept between intervals; the form's Node term and the integers of the paces beside it (ALGEBRA.md #the-line, #the-direction, #the-interval)."""

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
    """The rule's integers at a Node from the paces, ((R_x, R_y, R_z), S, w); the isotropic rule at the axis contents zero, the plain first-order rule with weak_field False (ALGEBRA.md #the-line, #the-interval, #the-direction)."""
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


THE_LOAD = "the load"
THE_ADVANCE = "the advance"
THE_REWRITE = "the rewrite"
THE_INVERSE = "the inverse"
THE_UNHOLD = "the unhold"
ACTS = (THE_LOAD, THE_ADVANCE, THE_REWRITE, THE_INVERSE, THE_UNHOLD)
NO_READ = (0, 0, 0)
Key = tuple[object, ...]
# the span of a step on two levels (the leapfrog of a body's spin or momentum): two intervals; the
# same 2 is the form's second order, the potential's 2 Gamma (ALGEBRA.md #the-well)
SPAN = 2


def division_forward(numerator: int, wall: int, carry: int) -> tuple[int, int]:
    """Rule3's division act forward: (numerator + carry) div wall and the remainder, the line with no read and the numerator as the self coefficient on the level 1 (ALGEBRA.md #the-interval)."""
    return rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry, 1)


def division_back(numerator: int, wall: int, value: int, carry: int) -> tuple[int, int]:
    """The carried division one interval back by Rule3's direction -1: the carry before from (value, carry), then the value before from that carry as the ceiling form, exact while the carry stays below the wall (ALGEBRA.md #the-direction, #the-interval)."""
    _, carry_before = rule3(NO_READ, NO_READ, numerator, wall, 1, value, carry, -1)
    value_before, _ = rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry_before, -1)
    return value_before, carry_before


def carried(
    act: str, key: Key, numerator: int, wall: int, values: dict[Key, int], carries: dict[Key, int]
) -> tuple[int, int]:
    """One carried division by its act on the body's remainders: forward the value of this interval and the last one's (the first value twice at the load), back the state stepped back with the value before it, a rewrite the standing value twice (ALGEBRA.md #the-interval)."""
    if act == THE_INVERSE:
        value, carry = division_back(numerator, wall, values.get(key, 0), carries.get(key, 0))
        values[key], carries[key] = value, carry
        before, _ = division_back(numerator, wall, value, carry)
        return value, before
    if act in (THE_ADVANCE, THE_LOAD):
        previous = values.get(key)
        value, carry = division_forward(numerator, wall, carries.get(key, 0))
        values[key], carries[key] = value, carry
        return value, value if previous is None else previous
    value = values.get(key, 0)
    return value, value


def form_term(self_coefficient: Any, wall: Any, now: Any, before: Any) -> Any:
    """The conserved form's term at one Node from the rule's integers, w (now^2 + before^2) - S now before (ALGEBRA.md #the-line; BUILD.md section 26 items 36 and 44)."""
    return wall * (now * now + before * before) - self_coefficient * now * before


def rule_total_bound(
    num: int, den: int, gamma: int, content: int, amplitude: int, weak_field: bool
) -> int:
    """The largest total the rule reaches at a Node whose reads and levels stand at the amplitude bound A, 6 A R + A |S| + w (A + 1); below 2^63 or the world is refused (ALGEBRA.md #the-line, #the-rows-against-nature)."""
    reads, self_coefficient, wall = coefficients(num, den, gamma, content, ISOTROPIC, weak_field)
    return int(
        6 * amplitude * abs(reads[0]) + amplitude * abs(self_coefficient) + wall * (amplitude + 1)
    )


def rungs(weights: list[tuple[int, int]], steps: int) -> tuple[list[int], tuple[int, int]]:
    """The ladder's rungs b_k = (2 W C_k + Total) div (2 Total) from the cells' weights as pairs, and the total as the reduced pair (ALGEBRA.md #the-ladder)."""
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
