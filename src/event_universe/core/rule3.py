"""Rule3 in one place: one function steps every record at every Node in either direction, w a_next + r' = SUM over the six Ports of R_ij arr_j + S a_now - w a_before + r with the remainder kept in [0, w); the carried division, its division act with the remainder kept between intervals; the fixed point of the division act iterated (the root the loader and the generator read, never the run); the form's Node term and the rule's integers from the paces beside it, one read per Port as the product of the Node's pace squared and the Link's factor, the clock the Node's and the tension the Link's, the paces themselves the composed clock's two functions of the content (core/paces.py; ALGEBRA.md #the-line, #the-direction, #the-interval, #the-paces)."""

from __future__ import annotations

from typing import Any

# the rule's reads, one per Port in Port order [+X, -X, +Y, -Y, +Z, -Z], R_ij = 2 num p_i^2 Q_ij on
# the Link to that neighbour; the arrivals through the same Ports; integers or the loop's integer arrays
Reads = tuple[Any, ...]

PORTS = 6  # a Node's six Ports, the three axes twice (Rule3's 6)
NO_READ: tuple[int, ...] = (0,) * PORTS


def coefficients(
    num: Any,
    den: Any,
    gamma: Any,
    clock: Any,
    pace: Any,
    factors: tuple[Any, ...] | None = None,
    unit: Any = 1,
) -> tuple[Reads, Any, Any]:
    """The rule's integers at a Node from its paces, (the six reads, S, w), the clock the Node's and the tension the Link's (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's; The paces compose): the clock p_0 = Gamma (1 - 1 / Gamma)^c to the unit from the Node's content c, the reading row's own level among it, the primary number whose square enters S (`paces.clock_of`); the Node's pace p_i = p_0^2 / Gamma, the clock twice, on every one of its six Links (`paces.link_pace_of`); each Link's factor Q_ij, one integer per Link in the unit G^2 of the run's Link unit G (`link_factor`, read the same from both ends; None: no tension, G^2 on every Link); R_ij = 2 num p_i^2 Q_ij per Port, the product and not the sum; S = 12 (den Gamma^2 - (den - num) p_0^2) G^2 - SUM over the six Ports of R_ij (12 num p_i^2 G^2 with no tension, so the rotation at wave number zero is the clock's alone), w = 6 den Gamma^2 G^2 (#the-line); at the vacuum's paces p_0 = p_i = Gamma the plain rule of the pair."""
    square = unit * unit
    clock_squared = clock * clock
    node_squared = pace * pace
    links = (square,) * PORTS if factors is None else factors
    reads = tuple(2 * node_squared * factor * num for factor in links)
    gamma_squared = gamma * gamma
    self_coefficient = 12 * (den * gamma_squared - (den - num) * clock_squared) * square - sum(reads)
    return reads, self_coefficient, 6 * den * gamma_squared * square


def link_factor(gamma: Any, unit: Any, tension: Any) -> Any:
    """The Link's factor Q_ij, the one place of its form (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's; the Boss's booking): q_ij^2 / Gamma^2 = (Gamma - t_a(i, j))^2 / Gamma^2 booked squared as one integer per Link in the unit G^2 of the run's Link unit G, Q_ij = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 by the division act, rounded once to the nearest from the Link's tension t and read the same from both ends, so the step's operator is exactly symmetric in integers; G^2 with no tension, 0 where the tension reaches Gamma (the Link's coefficient 0), the tension resolved to Gamma / (2 G^2)."""
    pace = gamma - tension
    wall = gamma * gamma
    half = division_forward(wall, 2, 0)[0]
    return division_forward(unit * unit * pace * pace, wall, half)[0]


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
    """One interval of Rule3 in `direction` sigma: u = sigma (SUM over the Ports of R_ij arr_j + S a_now - w other) + carry, z = sigma (u div w), carry' = u mod w; +1 from (a_now, a_before, r) to (a_next, r'), -1 from (a_now, a_next, r') back to (a_before, r) (ALGEBRA.md #the-line, #the-direction); the reads and the arrivals in Port order, one per Port, none for the division act (NO_READ)."""
    total = self_coefficient * now
    total -= wall * other
    for read, arrived in zip(reads, arrivals, strict=True):
        total += read * arrived
    total = direction * total + carry
    quotient = total // wall
    return direction * quotient, total - wall * quotient


def division_forward(numerator: Any, wall: Any, carry: Any) -> tuple[Any, Any]:
    """Rule3's division act forward: (numerator + carry) div wall and the remainder, the line with no read and the numerator as the self coefficient on the level 1 (ALGEBRA.md #the-four-acts)."""
    return rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry, 1)


def division_back(numerator: Any, wall: Any, carry: Any) -> tuple[Any, Any]:
    """The division act one interval back by Rule3's direction -1: from the remainder after, the quotient the forward act wrote and the remainder before it, exact (ALGEBRA.md #the-direction)."""
    return rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry, -1)


def division_fixed_point(square: int) -> int:
    """The fixed point of the division act iterated from above, x <- (x + n div x) div 2 while it falls (Newton's integer iteration, the start's own act), the largest x with x^2 <= n; at n = 0 the descent ends at 0 (ALGEBRA.md #the-guard, the root leaves everywhere)."""
    root = square + 1
    while True:
        lower = division_forward(root + division_forward(square, root, 0)[0], 2, 0)[0]
        if lower >= root:
            return int(root)
        root = lower
        if root == 0:
            return 0


def form_term(self_coefficient: Any, wall: Any, now: Any, before: Any) -> Any:
    """The conserved form's term at one Node from the rule's integers, w (now^2 + before^2) - S now before (ALGEBRA.md #the-conserved-form)."""
    return wall * (now * now + before * before) - self_coefficient * now * before


def rule_total_bound(
    num: int, den: int, gamma: int, clock: int, pace: int, amplitude: int, unit: int = 1
) -> int:
    """The largest total the rule reaches at a Node of the paces (p_0, p_i) whose reads and levels stand at the amplitude bound A, A SUM over the six Ports of |R_ij| + A |S| + w (A + 1), 6 A R in a uniform level, the Link's unit G^2 among the integers; below 2^width - 1 or the world is refused (ALGEBRA.md #the-line, #the-bound, #the-rows-against-nature)."""
    reads, self_coefficient, wall = coefficients(num, den, gamma, clock, pace, None, unit)
    return int(
        amplitude * sum(abs(read) for read in reads)
        + amplitude * abs(self_coefficient)
        + wall * (amplitude + 1)
    )
