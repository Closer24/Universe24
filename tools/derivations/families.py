"""The families from the two keys of a row, its pair and its shape (ALGEBRA.md, The lattice and the families; the paper's universe table, Sections 6.1 to 6.5 and 10.3): what Rule3 reads of a Node, one clock and three Link paces, so a holder carries 1 + 3 parts at most; the holder's rest line from Rule3 at rest, num Delta a - 6 (den - num) a = -3 den sigma, Poisson's for [1, 1] with the kernel 3 G(r) s and 3 s / (4 pi r) far away; the gap as the inverse reach, cosh kappa = 3 den / num - 2, the range R = 1 / kappa, 20 Links at [2400, 2401] and the contact well of [1, 2]; the two speeds under Every row reads the content, light and the massless holder's events at one pace, their Shapiro difference 0 against GW170817's bound; and the gapped holder's kernel, Yukawa's with the massless constant, coupling at alpha at the Link. Roots in rule3.py; the lattice Green's function is greens_function.py's (Watson's anchor) and the gapped one its own integral.

Usage: `python tools/derivations/families.py` prints them.
"""

from __future__ import annotations

import math

import numpy as np

try:
    import greens_function
    import rule3
except ModuleNotFoundError:  # the gates load a module by its path, the folder not on sys.path
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import greens_function
    import rule3

GAMMA = 6000  # the universe table's Node clock, Gamma = 6,000 (the paper's line 395)
GRAVITY = (6000, 6000)  # the gravity holder's pair [1, 1] over Gamma (the universe table)
BINDING = (2400, 2401)  # the binding holder's pair, its range R = 20 Links (the universe table; S.11)
MATTER = (4000, 6000)  # matter's pair [2, 3] over Gamma (the universe table)
CONTACT = (1, 2)  # the pair of the paper's contact well, cosh kappa = 4 (line 416)
GW170817_BOUNDS = (
    -2.6e-7,
    1.2e-6,
)  # nature's bounds on gamma_GW - gamma_EM (Abbott and others 2017; line 430, S.12)
QUADRATURE = (
    256  # points per axis of the midpoint rule for the gapped Green's function, the error e^(-kappa M)
)


def rest_line_coefficients(num: int, den: int) -> tuple[float, float]:
    """The holder's rest from Rule3's line (S.11, S.39): with a_next = a_before = a_now = a at the vacuum's paces, 2 w a = R S_6(a) + S a + w sigma, so (2 w - S) / R = 6 den / num is the six-neighbour sum of a unit rest and w / R = 3 den / num the source's coefficient, num Delta a - 6 (den - num) a = -3 den sigma; returns [(2 w - S) / R, w / R]."""
    wall, reads, self_coefficient = rule3.coefficients(num, den)
    return (2 * wall - self_coefficient) / reads[0], wall / reads[0]


def inverse_reach(num: int, den: int) -> float:
    """kappa with cosh kappa = 3 den / num - 2, the rest's fall per Link along an axis (S.11): S_6 of a rest e^(-kappa r) uniform across is 2 cosh kappa + 4, equal to 6 den / num by the rest line."""
    six_sum, _ = rest_line_coefficients(num, den)
    return math.acosh((six_sum - 4) / 2)


def gapped_green(kappa: float, reach: int = 1, points: int = QUADRATURE) -> float:
    """G_kappa(r) = INT d^3k / (2 pi)^3 e^(i k . r) / (6 - 2 SUM_a cos k_a + kappa^2) on an axis, the lattice Yukawa integral (S.39), by the midpoint rule on `points` per axis, exponentially accurate as e^(-kappa points)."""
    k = -math.pi + (np.arange(points) + 0.5) * 2 * math.pi / points
    cosine = np.cos(k)
    plane = cosine[:, None] + cosine[None, :]
    total = 0.0
    for c_x, k_x in zip(cosine, k, strict=True):
        total += float(np.sum(np.cos(k_x * reach) / (6 - 2 * (c_x + plane) + kappa * kappa)))
    return total / points**3


def universe_table() -> list[float]:
    """The universe table's derived columns from each row's pair and shape (line 395; ALGEBRA.md, A family's declaration, the pair [num, den] and the shape; The line, cos omega_0 = num / den at wave number zero; The well, the rest's fall e^(-kappa) per Link with cosh kappa = 3 den / num - 2): [gravity's inverse reach kappa at [1, 1], 0, no gap; the binding holder's range R = 1 / kappa at [2400, 2401], 20 Links; matter's rest cos omega_0 = num / den at [4000, 6000], 2 / 3; the parts a holder read into the paces carries at most, 1 + 3]."""
    return [
        inverse_reach(*GRAVITY),
        1 / inverse_reach(*BINDING),
        rule3.plane_wave_dispersion(0.0, *MATTER),
        float(1 + rule3.AXES),
    ]


def what_rule3_reads() -> list[float]:
    """What a family carries is set by what Rule3 reads and what a record can write (line 410; ALGEBRA.md, The line, the coefficients w = 6 den Gamma^2, R_a = 2 num p_a^2 and S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num (p_x^2 + p_y^2 + p_z^2)): the line's coefficients read one clock pace p_0, in S alone, and three Link paces p_a, one read coefficient per axis; [the clock's count, the Link paces' count, 1 + 3 the most parts of a holder]."""
    wall, reads, self_coefficient = rule3.coefficients(2, 3, 10, clock=7, links=(5, 6, 7))
    clocks = 1  # p_0 enters S once: 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM_a p_a^2
    assert (
        self_coefficient == 12 * 3 * 100 - 12 * 1 * 49 - 4 * 2 * (25 + 36 + 49) and wall == 6 * 3 * 100
    )
    return [float(clocks), float(len(reads)), float(clocks + len(reads))]


def poisson_rest() -> list[float]:
    """Around a static source the holder [1, 1] rests at Poisson's solution 3 G(r) s, 3 s / (4 pi r) far away (line 412; S.38): the rest line at [1, 1] is Delta a = -3 sigma, the 3 the line's w / R; [w / R at [1, 1], the far kernel's 3 / (4 pi), 3 G(0) at the Node from the lattice Green's function, 4 pi r G(r) at r = 5 toward 1]."""
    _, source = rest_line_coefficients(1, 1)
    return [
        source,
        source / (4 * math.pi),
        greens_function.three_g()[0],
        greens_function.four_pi_r_g()[-1],
    ]


def gap_is_the_inverse_reach() -> list[float]:
    """The gap is one number that is both the mass of the holder's quanta and the inverse reach of the row (line 416; S.11): [kappa at [1, 1], no gap; cosh kappa at [1, 2], 4; its fall e^(-kappa) per Link, 0.127; its reach 1 / kappa, 0.48 Links]."""
    kappa = inverse_reach(*CONTACT)
    return [inverse_reach(1, 1), math.cosh(kappa), math.exp(-kappa), 1 / kappa]


def two_speeds(gamma: int = GAMMA, content: int = 300, links: int = 1000) -> list[float]:
    """Under Every row reads the content the massless holder's travelling events have light's paces identically, so gamma_GW = gamma_EM and the two Shapiro delays differ by 0, inside GW170817's bounds (line 430; S.12): light and the holder's events both run on rule3's band at the paces p_0 = Gamma N, p_a = Gamma N^2, N^2 / sqrt 3 at long wavelength; [their speeds' difference, their arrivals' difference over the Links in intervals, the superseded version's separation L sqrt 3 (1 / N^2 - 1) with the holder at 1 / sqrt 3, exact in x (182.2 over 1,000 Links at x = 0.05), where S.12's written formula L sqrt 3 [1 / (1 - 2 x) - 1] is its first order in x (192.5); whether 0 lies within GW170817's bounds]."""
    clock = rule3.clock_pace(gamma, content)
    pace = rule3.node_pace(clock, gamma)
    k = 1e-3

    def speed(num: int, den: int) -> float:
        return (
            math.acos(rule3.dispersion_at_paces((k, 0.0, 0.0), num, den, gamma, clock, (pace,) * 3)) / k
        )

    light, events = speed(1, 1), speed(*GRAVITY)
    vacuum = rule3.group_velocity(k, 1, 1)
    low, high = GW170817_BOUNDS
    return [
        light - events,
        links / events - links / light,
        links / light - links / vacuum,
        float(low <= light - events <= high),
    ]


def gapped_holder_kernel() -> list[float]:
    """Every rotation holder, massive or not, couples at alpha at the Link; its gap is its range and never its strength (line 612; S.39): the rest line divided by num is Delta L - kappa^2 L = -(3 / nu) sigma with Yukawa's lattice kernel G_kappa, far away e^(-kappa r) / (4 pi r), and at one Link G_kappa(1) = G_0(1) (1 - 0.92 kappa + O(kappa^2)) by the continuum's first order G_0(1) - kappa / (4 pi); [the range R = 1 / kappa at [2400, 2401], 20 Links; G_kappa(1) / G_0(1) at kappa = 1 / R by the lattice integral against Watson's G_0(1) = G(0) - 1 / 6, 0.9546; the slope 1 / (4 pi G_0(1)), 0.92; the coupling's factor at one Link, 1 - 1 / R]."""
    kappa = inverse_reach(*BINDING)
    massless_at_one = greens_function.WATSON - 1 / 6
    return [
        1 / kappa,
        gapped_green(kappa) / massless_at_one,
        1 / (4 * math.pi * massless_at_one),
        1 - kappa,
    ]


if __name__ == "__main__":
    print("the universe table's derived columns:", [round(v, 4) for v in universe_table()])
    print("what Rule3 reads, the clock, the Links, the parts:", what_rule3_reads())
    print(
        "Poisson's rest, w / R, 3 / (4 pi), 3 G(0), 4 pi r G(r) at 5:",
        [round(v, 4) for v in poisson_rest()],
    )
    print("the gap as the inverse reach:", [round(v, 4) for v in gap_is_the_inverse_reach()])
    print("the two speeds:", [round(v, 6) for v in two_speeds()])
    print("the gapped holder's kernel:", [round(v, 4) for v in gapped_holder_kernel()])
