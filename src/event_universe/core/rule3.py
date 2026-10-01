"""Rule3 in one place: one function steps every record at every Node in either direction, w a_next + r' = SUM over the six Ports of R_ij arr_j + S a_now - w a_before + r with the remainder kept in [0, w); the carried division, its division act with the remainder kept between intervals; the fixed point of the division act iterated (the root the loader and the generator read, never the run); the form's Node term and the integers of the paces beside it, one read per Port from the Link's own pace (ALGEBRA.md #the-line, #the-direction, #the-interval, #the-paces)."""

from __future__ import annotations

from typing import Any

# the rule's reads, one per Port in Port order [+X, -X, +Y, -Y, +Z, -Z], R_ij = 2 num p_a(i, j)^2 on
# the Link to that neighbour; the arrivals through the same Ports; integers or the loop's integer arrays
Reads = tuple[Any, ...]

PORTS = 6  # a Node's six Ports, the three axes twice (Rule3's 6)
NO_READ: tuple[int, ...] = (0,) * PORTS


def coefficients(
    num: Any,
    den: Any,
    gamma: Any,
    content: Any,
    links: tuple[Any, ...] | None = None,
    weak_field: bool = True,
) -> tuple[Reads, Any, Any]:
    """The rule's integers at a Node from the paces, (the six reads, S, w): the clock's square p_0^2 = (Gamma - c)^2 + c^2 from the Node's content and each Link's pace p_a(i, j) = Gamma - 2 c_i - t_a(i, j) from the Link's content `links`, the Node's content twice and the Link's own tension in Port order (None: no tension, Gamma - 2 c on every Link), the level entering the clock once with its square over twice the clock and the Link twice (ALGEBRA.md #the-paces), the tension one number per Link read the same from both ends (#the-interval, the dependency radius); R_ij = 2 num p_a(i, j)^2 per Port, S = 12 den Gamma^2 - 12 (den - num) p_0^2 - SUM over the six Ports of R_ij (4 num SUM_a p_a^2 with no tension, so the rotation at wave number zero is the clock's alone), w = 6 den Gamma^2 (#the-line); the plain first-order rule with weak_field False."""
    pace = gamma - content
    if not weak_field:
        read = pace * num
        return (read,) * PORTS, 6 * den * content, 3 * den * gamma
    clock_squared = pace * pace + content * content
    paces = link_paces(gamma, (content + content,) * PORTS if links is None else links)
    reads = tuple(2 * link * link * num for link in paces)
    gamma_squared = gamma * gamma
    self_coefficient = 12 * (den * gamma_squared - (den - num) * clock_squared) - sum(reads)
    return reads, self_coefficient, 6 * den * gamma_squared


def link_paces(gamma: Any, links: tuple[Any, ...]) -> tuple[Any, ...]:
    """The six Links' paces at a Node, p_a(i, j) = Gamma - (2 c_i + t_a(i, j)), one per Port from the Link's content, the Node's level twice and the Link's own tension once (ALGEBRA.md #the-paces; Gamma - 2 c with no tension)."""
    return tuple(gamma - link for link in links)


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
    num: int, den: int, gamma: int, content: int, amplitude: int, weak_field: bool
) -> int:
    """The largest total the rule reaches at a Node whose reads and levels stand at the amplitude bound A, A SUM over the six Ports of |R_ij| + A |S| + w (A + 1), 6 A R in a uniform level; below 2^width - 1 or the world is refused (ALGEBRA.md #the-line, #the-rows-against-nature)."""
    reads, self_coefficient, wall = coefficients(num, den, gamma, content, None, weak_field)
    return int(
        amplitude * sum(abs(read) for read in reads)
        + amplitude * abs(self_coefficient)
        + wall * (amplitude + 1)
    )
