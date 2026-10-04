"""Rule3's line and its invariants as docs/ALGEBRA.md states them, in pure Python: the root every derivation script of this folder leans on, and nothing of the engine (no import of event_universe, no file of runs/ or examples/).

Transcribed, each function naming its sentence of the law: the coefficients and the one line at a Node with the remainder kept (The line); the direction's forward and backward acts (The direction); the band of a plane wave at the vacuum's paces and at a Node's paces (The line, "the plain second-order rule of the pair"; The band at a pace); the group velocity (The band at a pace); the conserved form with its weights, its Link's current and the walk the remainders add (The conserved form; The conventions and the units, row 7); the paces' closed formulas, the clock, the Node's pace, the Link's factor and the Link's read coefficient (The paces; The clock is the Node's, the tension is the Link's), the guard's edge (The guard) and the rule's total at an amplitude (The bound).

Not here, because the law states no closed formula for them: the content c of a Node (a sum over the reads of weight times level, a run's quantity), the tension of a Link (read from the record as it stands), the carried remainder of a Node (the integer step's own, exact and in no closed form), the fixed point of a body (the start's iteration), and every number of nature (a click's). Every number in this module is the law's text's (the six Ports, the three axes, the two of the recurrence) or an argument; integers and fractions throughout, floats only where a cosine is asked for.

Usage: `python tools/derivations/rule3.py` prints the vacuum band's values at [1, 1] and [2, 3] and a plane wave's residual against the line.
"""

from __future__ import annotations

import math
import random
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
    clocks: Sequence[Number] | None = None,
    link_factors: Sequence[Sequence[Number]] | None = None,
) -> Fraction:
    """E of The conserved form: E = SUM_i [w (now_i^2 + before_i^2) - S_i now_i before_i] / p_i^2 - 2 num SUM_i SUM_(j ~ i) (q_ij^2 / Gamma^2) now_i before_j, the weight 1 / p_i^2 on the Node terms and the Link's factor squared on each Link's current; `arrivals[i]` the six neighbour indices of the Node i in Port order (a folded axis returns i itself); `clocks[i]` the clock p_0(i) of the Node i, its pace p_i = p_0(i)^2 / Gamma (The paces, the clock twice), and `link_factors[i][port]` the factor q_ij = Gamma - t_a(i, j) of the Link through that Port, both Gamma at the vacuum's paces, the defaults. S_i is the line's own self coefficient at the Node's paces (The line): 12 den Gamma^2 - 12 (den - num) p_0(i)^2 less the six reads R(i -> j) = 2 num p_i^2 q_ij^2 / Gamma^2 (`link_coefficient`; `coefficients`' 4 num SUM_a p_a^2 where the two Ports of an axis share a pace), 0 at the vacuum's paces; so E is the form of the line `step_exact` steps at those paces and holds at any paces, D M symmetric (the proof), where a self coefficient built from any other pace drifts."""
    count = len(now)
    p_0s = [Fraction(gamma)] * count if clocks is None else [Fraction(c) for c in clocks]
    factors = (
        [[gamma] * PORTS for _ in range(count)]
        if link_factors is None
        else [list(f) for f in link_factors]
    )
    wall, _, _ = coefficients(num, den, gamma)
    total = Fraction(0)
    for i in range(count):
        p_0 = p_0s[i]
        p_i = node_pace(p_0, gamma)
        reads = [link_coefficient(num, p_i, q, gamma) for q in factors[i]]
        self_coefficient = 12 * den * gamma * gamma - 12 * (den - num) * p_0 * p_0 - sum(reads)
        node_term = (
            wall * (now[i] * now[i] + before[i] * before[i]) - self_coefficient * now[i] * before[i]
        )
        total += Fraction(node_term) / (p_i * p_i)
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


def link_current(
    num: int,
    now_i: Number,
    before_i: Number,
    now_j: Number,
    before_j: Number,
    factor: Number = 1,
    gamma: int = 1,
) -> Fraction:
    """F_ij = num (q_ij / Gamma)^2 (now_i before_j - before_i now_j), the conserved form's current through the Link ij into the Node i (The conserved form, "Its Link term is the current"; The count is the record's share, "The share's change is the currents"), the Link's factor squared the one weight, 1 where no tension stands (the defaults)."""
    plain = Fraction(now_i) * Fraction(before_j) - Fraction(before_i) * Fraction(now_j)
    return Fraction(num) * Fraction(factor) ** 2 / Fraction(gamma * gamma) * plain


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


def band_at_a_pace(
    num: int = 2, den: int = 3, gamma: int = 6000, content: int = 300, k: float = 0.3
) -> list[float]:
    """The band at a pace from the line's coefficients (The band at a pace; the paper's Eq. (4) and its line 189, S.1): at the clock p_0 = Gamma (1 - 1 / Gamma)^c and the Node's pace p_a = p_0^2 / Gamma a plane wave along x has 2 w cos omega = S + 2 SUM_a R_a cos k_a, the arrivals of an axis summing to 2 cos k_a a_now and a_next + a_before to 2 cos omega a_now; [cos omega so computed from `coefficients`, its difference from the closed formula of `dispersion_at_paces`], the difference 0."""
    clock = clock_pace(gamma, content)
    pace = node_pace(clock, gamma)
    wall, reads, self_coefficient = coefficients(num, den, gamma, clock, (pace, pace, pace))
    cosines = (math.cos(k), 1.0, 1.0)
    from_the_line = (
        float(self_coefficient) + 2 * sum(float(r) * c for r, c in zip(reads, cosines, strict=True))
    ) / (2 * float(wall))
    closed = dispersion_at_paces((k, 0.0, 0.0), num, den, gamma, clock, (pace, pace, pace))
    return [from_the_line, abs(from_the_line - closed)]


def three_level_form_walk(
    nodes: int = 24, num: int = 2, den: int = 3, intervals: int = 50, seed: int = 258
) -> list[float]:
    """What the remainders add to the two forms in one interval (The conserved form, the proof's last sentence; The conventions and the units, row 7; the paper's line 258 and S.5): with epsilon_i = (r_i - r_i') / w the two-level form Q = E / w of now and before walks by SUM_i epsilon_i (next_i - before_i) / p_i^2 (`form_walk` over w) and the three-level form E_3 = SUM_i (now_i^2 - next_i before_i) / p_i^2 walks by SUM_i [epsilon_i(t) next_i - epsilon_i(t + 1) now_i] / p_i^2, since E_3(t) = Q(t) - SUM_i epsilon_i(t) before_i / p_i^2 by the line; on a periodic chain of integer levels at the vacuum's paces, exact in the rationals: [the largest departure of Q's walk from its term, of E_3's walk from its term], both 0."""
    draw = random.Random(seed)
    arrivals = chain_arrivals(nodes)
    wall, _, _ = coefficients(num, den)
    levels = [
        [draw.randint(-1000, 1000) for _ in range(nodes)],
        [draw.randint(-1000, 1000) for _ in range(nodes)],
    ]
    remainders = [0] * nodes
    epsilons: list[list[Fraction]] = []
    for _ in range(intervals + 1):
        before, now = levels[-2], levels[-1]
        stepped = [
            step(now[i], before[i], [now[j] for j in arrivals[i]], num, den, remainders[i])
            for i in range(nodes)
        ]
        carried = [s[1] for s in stepped]
        epsilons.append(
            [Fraction(r - r_next, wall) for r, r_next in zip(remainders, carried, strict=True)]
        )
        levels.append([s[0] for s in stepped])
        remainders = carried

    def two_level(t: int) -> Fraction:
        return conserved_form(levels[t], levels[t - 1], arrivals, num, den) / wall

    def three_level(t: int) -> Fraction:
        return Fraction(
            sum(levels[t][i] ** 2 - levels[t + 1][i] * levels[t - 1][i] for i in range(nodes))
        )

    worst_two, worst_three = Fraction(0), Fraction(0)
    for t in range(1, intervals):
        # epsilons[t - 1] belongs to the step from (levels[t - 1], levels[t]) to levels[t + 1]
        term_two = sum(
            e * (nxt - prev)
            for e, nxt, prev in zip(epsilons[t - 1], levels[t + 1], levels[t - 1], strict=True)
        )
        term_three = sum(
            e_now * nxt - e_next * now
            for e_now, e_next, nxt, now in zip(
                epsilons[t - 1], epsilons[t], levels[t + 1], levels[t], strict=True
            )
        )
        worst_two = max(worst_two, abs(two_level(t + 1) - two_level(t) - term_two))
        worst_three = max(worst_three, abs(three_level(t + 1) - three_level(t) - term_three))
    return [float(worst_two), float(worst_three)]


def backward_reading_to_the_bit(
    nodes: int = 24,
    num: int = 2,
    den: int = 3,
    gamma: int = 6000,
    content: int = 300,
    intervals: int = 50,
    seed: int = 308,
) -> list[float]:
    """The backward reading exists to the bit at fixed paces (The direction; the paper's line 308): on a periodic chain at the integer paces p_0 = Gamma (1 - 1 / Gamma)^c to the unit and p_a = p_0^2 / Gamma to the unit, `step` over the intervals and `step_backward` over the same intervals in reverse return the start's levels and remainders; [the Nodes whose level or remainder differs after the round trip], 0."""
    draw = random.Random(seed)
    arrivals = chain_arrivals(nodes)
    clock = round(clock_pace(gamma, content))
    links = (round(node_pace(clock, gamma)),) * AXES
    before = [draw.randint(-1000, 1000) for _ in range(nodes)]
    now = [draw.randint(-1000, 1000) for _ in range(nodes)]
    remainders = [draw.randint(0, 6 * den * gamma * gamma - 1) for _ in range(nodes)]
    start = (list(before), list(now), list(remainders))
    for _ in range(intervals):
        stepped = [
            step(
                now[i],
                before[i],
                [now[j] for j in arrivals[i]],
                num,
                den,
                remainders[i],
                gamma,
                clock,
                links,
            )
            for i in range(nodes)
        ]
        before, now, remainders = now, [s[0] for s in stepped], [s[1] for s in stepped]
    for _ in range(intervals):
        back = [
            step_backward(
                before[i],
                now[i],
                [before[j] for j in arrivals[i]],
                num,
                den,
                remainders[i],
                gamma,
                clock,
                links,
            )
            for i in range(nodes)
        ]
        now, before, remainders = before, [b[0] for b in back], [b[1] for b in back]
    differing = sum(
        int(a != b)
        for a, b in zip(start[0] + start[1] + start[2], before + now + remainders, strict=True)
    )
    return [float(differing)]


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
    print(
        "the band at a pace, from the coefficients and its difference from the closed formula:",
        band_at_a_pace(),
    )
    print(
        "the forms' walks less the remainders' terms, two-level and three-level:",
        three_level_form_walk(),
    )
    print(
        "Nodes differing after the forward and backward intervals at fixed paces:",
        backward_reading_to_the_bit(),
    )
