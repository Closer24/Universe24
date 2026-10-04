"""Rule3's line and its invariants as docs/ALGEBRA.md states them, in pure Python: the root every derivation script of this folder leans on, and nothing of the engine (no import of event_universe, no file of runs/ or examples/).

Transcribed, each function naming its sentence of the law: the coefficients and the one line at a Node with the remainder kept (The line); the direction's forward and backward acts (The direction); the band of a plane wave at the vacuum's paces and at a Node's paces (The line, "the plain second-order rule of the pair"; The band at a pace); the group velocity (The band at a pace); the conserved form with its weights and the walk the remainders add (The conserved form; The conventions and the units, row 7); the paces' closed formulas, the clock, the Node's pace, the Link's factor and the Link's read coefficient (The paces; The clock is the Node's, the tension is the Link's), the guard's edge (The guard) and the rule's total at an amplitude (The bound).

Not here, because the law states no closed formula for them: the content c of a Node (a sum over the reads of weight times level, a run's quantity), the tension of a Link (read from the record as it stands), the carried remainder of a Node (the integer step's own, exact and in no closed form), the fixed point of a body (the start's iteration), and every number of nature (a click's). Every number in this module is the law's text's (the six Ports, the three axes, the two of the recurrence) or an argument; integers and fractions throughout, floats only where a cosine is asked for.

Usage: `python tools/derivations/rule3.py` prints the vacuum band's values at [1, 1] and [2, 3] and a plane wave's residual against the line.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from fractions import Fraction

PORTS = 6  # the six Ports, the three axes twice (The line)
AXES = 3

Number = int | Fraction


def coefficients(
    num: int,
    den: int,
    gamma: int = 1,
    clock: Number | None = None,
    links: Sequence[Number] | None = None,
) -> tuple[Number, tuple[Number, Number, Number], Number]:
    """(w, (R_x, R_y, R_z), S) of The line: w = 6 den Gamma^2, R_a = 2 num p_a^2, S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num (p_x^2 + p_y^2 + p_z^2); p_0 = p_a = Gamma at the vacuum's paces, the defaults."""
    p_0 = gamma if clock is None else clock
    paces = (gamma, gamma, gamma) if links is None else tuple(links)
    if len(paces) != AXES:
        raise ValueError("one Link pace per axis, three")
    wall = 6 * den * gamma * gamma
    reads = tuple(2 * num * p * p for p in paces)
    self_coefficient = (
        12 * den * gamma * gamma - 12 * (den - num) * p_0 * p_0 - 4 * num * sum(p * p for p in paces)
    )
    return wall, (reads[0], reads[1], reads[2]), self_coefficient


def numerator(
    now: Number,
    neighbours: Sequence[Number],
    reads: tuple[Number, Number, Number],
    self_coefficient: Number,
) -> Number:
    """SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now, the right side's first two terms (The line; Y of The direction); `neighbours` the six arrivals in the order +x, -x, +y, -y, +z, -z."""
    if len(neighbours) != PORTS:
        raise ValueError("six arrivals, one per Port")
    total: Number = self_coefficient * now
    for axis in range(AXES):
        total += reads[axis] * (neighbours[2 * axis] + neighbours[2 * axis + 1])
    return total


def step(
    now: int,
    before: int,
    neighbours: Sequence[int],
    num: int,
    den: int,
    remainder: int = 0,
    gamma: int = 1,
    clock: int | None = None,
    links: Sequence[int] | None = None,
) -> tuple[int, int]:
    """The law in one line (The line): w a_next + r' = SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now - w a_before + r with 0 <= r' < w, the quotient the floor and the remainder r' kept at the Node (The direction, forward, sigma = +1: u = Y + S x - w y + rho, z = u div w, rho' = u mod w); returns (a_next, r')."""
    wall, reads, self_coefficient = coefficients(num, den, gamma, clock, links)
    if not 0 <= remainder < wall:
        raise ValueError("the carried remainder lies in [0, w)")
    total = numerator(now, neighbours, reads, self_coefficient) - wall * before + remainder
    return divmod(int(total), int(wall))


def step_backward(
    now: int,
    next_level: int,
    neighbours: Sequence[int],
    num: int,
    den: int,
    remainder_next: int,
    gamma: int = 1,
    clock: int | None = None,
    links: Sequence[int] | None = None,
) -> tuple[int, int]:
    """The direction, backward, sigma = -1: with (x, y, rho) = (a_now, a_next, r'), u = -(SUM_a R_a arr_a + S x - w y) + rho, z = -(u div w) and rho' = u mod w give (a_before, r) bit for bit, the proof's ceiling identity; returns (a_before, r)."""
    wall, reads, self_coefficient = coefficients(num, den, gamma, clock, links)
    if not 0 <= remainder_next < wall:
        raise ValueError("the carried remainder lies in [0, w)")
    total = -(numerator(now, neighbours, reads, self_coefficient) - wall * next_level) + remainder_next
    quotient, carried = divmod(int(total), int(wall))
    return -quotient, carried


def step_exact(
    now: Number,
    before: Number,
    neighbours: Sequence[Number],
    num: int,
    den: int,
    gamma: int = 1,
    clock: Number | None = None,
    links: Sequence[Number] | None = None,
) -> Fraction:
    """The line without its division's floor, in the rationals: a_next = (SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now) / w - a_before, the line "before the integer remainders" of The conserved form."""
    wall, reads, self_coefficient = coefficients(num, den, gamma, clock, links)
    return Fraction(numerator(now, neighbours, reads, self_coefficient)) / Fraction(wall) - Fraction(
        before
    )


def plane_wave_dispersion(k: float, num: int, den: int) -> float:
    """cos omega of a plane wave along one axis at the vacuum's paces, (num / (3 den)) (2 + cos k) (The line, "the plain second-order rule of the pair"; The conventions and the units, row 3), derived from the line: (1) at p_0 = p_a = Gamma the coefficients are w = 6 den Gamma^2, R_a = 2 num Gamma^2 and S = 12 den Gamma^2 - 12 (den - num) Gamma^2 - 12 num Gamma^2 = 0; (2) in the reals the line is w a_next = SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now - w a_before; (3) for a = A cos(k x - omega t) along x, uniform on y and z, arr_(+x) + arr_(-x) = 2 cos k a_now and each other axis's two arrivals sum to 2 a_now; (4) a_next + a_before = 2 cos omega a_now, the sum of two cosines; (5) so 2 w cos omega = S + 2 R (cos k + 2), that is cos omega = (num / (3 den)) (2 + cos k)."""
    return num / (3 * den) * (2 + math.cos(k))


def dispersion_at_paces(
    wave_numbers: Sequence[float],
    num: int,
    den: int,
    gamma: int,
    clock: Number,
    links: Sequence[Number],
) -> float:
    """cos omega at a Node of the clock's pace p_0 and the Link paces p_a (The band at a pace; The line, "The clock once and the Link twice"): cos omega = 1 - (1 - num / den) (p_0 / Gamma)^2 - (num / (3 den)) SUM_a (p_a / Gamma)^2 (1 - cos k_a), the same substitution as `plane_wave_dispersion` with 2 w cos omega = S + 2 SUM_a R_a cos k_a divided by 2 w = 12 den Gamma^2."""
    if len(wave_numbers) != AXES or len(links) != AXES:
        raise ValueError("one wave number and one Link pace per axis, three")
    mass_term = (1 - num / den) * (float(clock) / gamma) ** 2
    band_term = sum(
        (float(p) / gamma) ** 2 * (1 - math.cos(k)) for p, k in zip(links, wave_numbers, strict=True)
    )
    return 1 - mass_term - num / (3 * den) * band_term


def group_velocity(k: float, num: int, den: int) -> float:
    """d omega / d k along an axis at the vacuum's paces, (num / (3 den)) sin k / sin omega (The band at a pace, the band's group velocity at p_a = Gamma), by differentiating cos omega = (num / (3 den)) (2 + cos k); 1 / sqrt 3 Links per interval for light as k goes to 0 (The lattice constants)."""
    omega = math.acos(plane_wave_dispersion(k, num, den))
    return num / (3 * den) * math.sin(k) / math.sin(omega)


def conserved_form(
    now: Sequence[Number],
    before: Sequence[Number],
    arrivals: Sequence[Sequence[int]],
    num: int,
    den: int,
    gamma: int = 1,
    node_paces: Sequence[Number] | None = None,
    link_factors: Sequence[Sequence[Number]] | None = None,
) -> Fraction:
    """E of The conserved form: E = SUM_i [w (now_i^2 + before_i^2) - S_i now_i before_i] / p_i^2 - 2 num SUM_i SUM_(j ~ i) (q_ij^2 / Gamma^2) now_i before_j, the weight 1 / p_i^2 on the Node terms and the Link's factor squared on each Link's current; `arrivals[i]` the six neighbour indices of the Node i in Port order (a folded axis returns i itself), `node_paces` p_i and `link_factors` q_ij both Gamma at the vacuum's paces, the defaults, where S_i = 0."""
    count = len(now)
    paces = [gamma] * count if node_paces is None else list(node_paces)
    factors = (
        [[gamma] * PORTS for _ in range(count)]
        if link_factors is None
        else [list(f) for f in link_factors]
    )
    total = Fraction(0)
    for i in range(count):
        p_i = paces[i]
        wall, _, self_coefficient = coefficients(
            num, den, gamma, clock=None if node_paces is None else p_i, links=None
        )
        node_term = (
            wall * (now[i] * now[i] + before[i] * before[i]) - self_coefficient * now[i] * before[i]
        )
        total += Fraction(node_term) / Fraction(p_i * p_i)
        for port, j in enumerate(arrivals[i]):
            q = factors[i][port]
            total -= Fraction(2 * num * q * q * now[i] * before[j]) / Fraction(gamma * gamma)
    return total


def form_walk(
    remainders_in: Sequence[int],
    remainders_out: Sequence[int],
    next_levels: Sequence[Number],
    before: Sequence[Number],
    node_paces: Sequence[Number] | None = None,
    gamma: int = 1,
) -> Fraction:
    """What the remainders add to E in one interval (The conserved form, the proof's last sentence; The conventions and the units, row 7: Q walks by SUM_i epsilon_i (next_i - before_i) with epsilon_i = (r_i - r_i') / w and E = w Q): SUM_i (r_i - r_i') (next_i - before_i) / p_i^2, each term below one unit of the level's change."""
    paces = [gamma] * len(before) if node_paces is None else list(node_paces)
    total = Fraction(0)
    for r_in, r_out, nxt, prev, p in zip(
        remainders_in, remainders_out, next_levels, before, paces, strict=True
    ):
        total += Fraction((r_in - r_out) * (nxt - prev)) / Fraction(p * p)
    return total


def chain_arrivals(count: int) -> list[list[int]]:
    """The six neighbour indices of every Node of a periodic chain of `count` Nodes along x with y and z folded: i + 1, i - 1 through the x Ports and the Node itself through the four others (The line, the arrival on a folded axis)."""
    return [[(i + 1) % count, (i - 1) % count, i, i, i, i] for i in range(count)]


def clock_pace(gamma: int, content: int) -> Fraction:
    """p_0 = Gamma (1 - 1 / Gamma)^c, the clock, exact in the rationals (The paces; The paces compose); the law says "to the unit", the rounding the read's and not written here."""
    return Fraction(gamma) * (Fraction(gamma - 1, gamma) ** content)


def node_pace(clock: Number, gamma: int) -> Fraction:
    """p_i = p_0(i)^2 / Gamma, the Node's pace, the clock twice (The paces, "The clock is the Node's, the tension is the Link's")."""
    return Fraction(clock) * Fraction(clock) / Fraction(gamma)


def link_factor(gamma: int, tension: int) -> int:
    """q_ij = Gamma - t_a(i, j), the Link's factor from the Link's tension (The paces)."""
    return gamma - tension


def link_coefficient(num: int, pace: Number, factor: Number, gamma: int) -> Fraction:
    """R_a(i -> j) = 2 num p_i^2 q_ij^2 / Gamma^2, the Node's pace squared times the Link's factor squared, the product and not the sum (The paces, "The clock is the Node's, the tension is the Link's")."""
    return Fraction(2 * num) * Fraction(pace) ** 2 * Fraction(factor) ** 2 / Fraction(gamma * gamma)


def guard_edge_squared(num: int, den: int, gamma: int) -> int:
    """P^2 = 2 den Gamma^2 div (den + |num|), the edge's square of the two-sided guard on squares (The guard): Gamma^2 for light and above it where |num| < den."""
    return 2 * den * gamma * gamma // (den + abs(num))


def rule_total(amplitude: int, num: int, den: int, gamma: int) -> int:
    """6 A |R| + A |S| + w (A + 1), the rule's total at a Node whose levels and arrivals stand at the amplitude A (The bound), at the vacuum's paces."""
    wall, reads, self_coefficient = coefficients(num, den, gamma)
    return 6 * amplitude * abs(reads[0]) + amplitude * abs(self_coefficient) + wall * (amplitude + 1)


def plane_wave_residual(
    k: float, num: int, den: int, nodes: int = 24, amplitude: float = 1000.0
) -> float:
    """The largest |a_next - (the line's right side) / w| over a periodic chain for a = A cos(k x - omega t) at the derived omega, in the reals: 0 to rounding, the check of `plane_wave_dispersion`."""
    omega = math.acos(plane_wave_dispersion(k, num, den))
    wall, reads, self_coefficient = coefficients(num, den)
    levels = [[amplitude * math.cos(k * x - omega * t) for x in range(nodes)] for t in (-1, 0, 1)]
    before, now, nxt = levels
    worst = 0.0
    for i, ports in enumerate(chain_arrivals(nodes)):
        arrivals = [now[j] for j in ports]
        right = numerator(now[i], arrivals, reads, self_coefficient) / wall - before[i]
        worst = max(worst, abs(nxt[i] - right))
    return worst


if __name__ == "__main__":
    for pair in ((1, 1), (2, 3)):
        values = [
            round(plane_wave_dispersion(k, *pair), 4) for k in (0.0, math.pi / 4, math.pi / 2, math.pi)
        ]
        print(f"cos omega at {list(pair)} for k = 0, pi / 4, pi / 2, pi:", values)
    print(
        "light's speed as k -> 0:",
        round(group_velocity(1e-3, 1, 1), 6),
        "against 1 / sqrt 3 =",
        round(1 / math.sqrt(3), 6),
    )
    print(
        "a plane wave's residual against the line at [2, 3], k = pi / 4:",
        plane_wave_residual(math.pi / 4, 2, 3),
    )
