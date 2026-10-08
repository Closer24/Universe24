"""The paces' checks and the forms of nature's (ALGEBRA.md, The paces compose, The write per proper volume and per proper interval, The push on a moving record, The method of derivation; the supplement's S.2, S.3, S.15, S.18, S.19, S.21, S.22, S.24, S.27, S.30, S.31, S.34, S.35, S.36, S.38, S.41, S.58, S.63): the composition exact, the clock's series and the quadratic and cubic readings' remainders, the acts' factors, the post-Newtonian orders of the exponential metric, the clock's click rate, the fall and Kepler's column, the post-Newtonian parameters, the moving clock to the fourth order, de Broglie, the push, the shadow, the two clocks, the index's first order, the staggered clock, the frozen content and the bounds from the photon; the identities exact in Fractions, the expansions by the residual's order at two step sizes, every printed number recomputed.

Usage: `python tools/derivations/proofs_paces.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paces  # noqa: E402
import rule3  # noqa: E402
from proofs_ground import SEED, Check, angles, has_order, pairs, run  # noqa: E402

SQRT3 = math.sqrt(3)


def rest_rotation(num: int, den: int) -> float:
    return math.acos(num / den)


def clock_factor(omega_0: float) -> float:
    """f(omega_0) = 2 (1 - cos omega_0) / (omega_0 sin omega_0), the clock's click rate at a finite gap (S.15)."""
    return 2 * (1 - math.cos(omega_0)) / (omega_0 * math.sin(omega_0))


def band_rotation(num: int, den: int, k: float, clock_ratio: float = 1.0) -> float:
    """omega(k) along an axis at the composed paces N = p_0 / Gamma: cos omega = 1 - g N^2 - (num / (3 den)) N^4 (1 - cos k) (Eq. (4))."""
    g, c0 = 1 - num / den, num / (3 * den)
    return math.acos(1 - g * clock_ratio**2 - c0 * clock_ratio**4 * (1 - math.cos(k)))


def check_the_paces_compose_exactly() -> Check:
    """The paces compose (ALGEBRA.md, The paces); S.34 (a): each unit of the level slows the clock as it already stands, p_0(c + 1) = p_0(c) (1 - 1 / Gamma), so p_0 = Gamma (1 - 1 / Gamma)^c and the composition P(U + l) = P(U) P(l) holds exactly; p_i = p_0^2 / Gamma the Node's pace (rule3.clock_pace and rule3.node_pace); exact fractions at random contents and clocks."""
    draw = random.Random(SEED)
    for _ in range(40):
        gamma = draw.randint(2, 200)
        a, b = draw.randint(0, 60), draw.randint(0, 60)
        clock = rule3.clock_pace(gamma, a + b)
        if clock != rule3.clock_pace(gamma, a) * rule3.clock_pace(gamma, b) / gamma:
            return False, {"Gamma": gamma, "contents": (a, b)}
        if rule3.clock_pace(gamma, a + 1) != rule3.clock_pace(gamma, a) * (1 - Fraction(1, gamma)):
            return False, {"one unit": (gamma, a)}
        if rule3.node_pace(clock, gamma) != clock * clock / gamma:
            return False, {"Node pace": (gamma, a + b)}
    return True, {"witnesses": 40}


def check_the_clocks_exponential_and_its_readings() -> Check:
    """The paces compose; S.34 (a), (e); The paces: p_0 = Gamma (1 - 1 / Gamma)^c is Gamma e^(-U) to O(1 / Gamma), the relative departure U / (2 Gamma) (0.951225 against e^(-0.05) = 0.951229 at Gamma = 6,000, c = 300, a relative 4 x 10^-6); its square Gamma^2 - 2 Gamma c + 2 c^2 to the second order, the composition's e^(-2 U) differing at -4 U^3 / 3 (0.905000 against 0.904837 at U = 0.05, the difference 1.63 x 10^-4 against 4 U^3 / 3 = 1.67 x 10^-4) while the Link's (Gamma - 2 c)^2 is e^(-4 U) to the first order only (0.8100 against 0.8187); the law's reading Gamma - c + c^2 div 2 Gamma within Gamma U^3 / 6 of a unit of the composition (1.02 units at c = 600 and Gamma = 6,000; 0.41 at Gamma = 2,400 and 2.0 at 12,000 at U = 0.10) and the cubic Gamma - c + c (c - 1) div 2 Gamma - c (c - 1) (c - 2) div 6 Gamma^2 within Gamma U^4 / 24 (0.05 at Gamma = 2,400 and 0.13 at 6,000 at U = 0.15); the orders by the residual at two step sizes, the numbers exact."""
    gamma = 6000
    composed = float(rule3.clock_pace(gamma, 300)) / gamma
    witness_1 = (round(composed, 6), round(math.exp(-0.05), 6), round(composed / math.exp(-0.05) - 1, 7))
    order_in_gamma, orders_gamma = has_order(
        lambda h: (1 - h) ** (0.05 / h) * math.exp(0.05) - 1, 1, step=0.02
    )
    order_square, orders_square = has_order(
        lambda u: math.exp(-2 * u) - (1 - 2 * u + 2 * u * u), 3, step=0.1
    )
    witness_2 = (
        round(1 - 0.1 + 2 * 0.0025, 6),
        round(math.exp(-0.1), 6),
        round((1 - 0.1 + 0.005) - math.exp(-0.1), 6),
        round(4 * 0.05**3 / 3, 6),
    )
    link_order, orders_link = has_order(lambda u: math.exp(-4 * u) - (1 - 2 * u) ** 2, 2, step=0.02)
    witness_3 = (round((1 - 0.1) ** 2, 4), round(math.exp(-0.2), 4))
    readings = quadratic_readings()
    cubics = []
    for g in (2400, 6000):
        c = int(0.15 * g)
        cubic = g - c + c * (c - 1) // (2 * g) - c * (c - 1) * (c - 2) // (6 * g * g)
        cubics.append((round(abs(cubic - float(rule3.clock_pace(g, c))), 2), round(g * 0.15**4 / 24, 2)))
    numbers = (
        witness_1[0] == 0.951225
        and witness_1[1] == 0.951229
        and witness_2 == (0.905, 0.904837, 0.000163, 0.000167)
        and witness_3 == (0.81, 0.8187)
    )
    # "within Gamma U^4 / 24 of a unit": the cubic reading's two floors miss the composition by under one unit plus Gamma U^4 / 24, the printed 0.05 and 0.13 being Gamma U^4 / 24
    readings_hold = (
        readings[6000] == 1.02
        and readings[12000] == 2.0
        and all(found <= 1 + bound for found, bound in cubics)
        and [bound for _, bound in cubics] == [0.05, 0.13]
    )
    return order_in_gamma and order_square and link_order and numbers and readings_hold, {
        "N against e^-U at Gamma 6,000, c 300": witness_1,
        "order in 1 / Gamma": orders_gamma,
        "the square's order": orders_square,
        "the square at U = 0.05": witness_2,
        "the Link's order": orders_link,
        "the Link at U = 0.05": witness_3,
        "quadratic reading less the composition at U = 0.1": readings,
        "cubic reading's miss against Gamma U^4 / 24": cubics,
    }


def quadratic_readings() -> dict[int, float]:
    """The law's reading Gamma - c + c^2 div 2 Gamma less the exact composition Gamma (1 - 1 / Gamma)^c at U = 0.10, per Gamma, as paces.quadratic_against_composed computes it: 1.02 at 6,000, 2.0 at 12,000 and 0.44 at 2,400 (the composition's own O(U / Gamma) term beside Gamma U^3 / 6 = 0.40)."""
    return {
        g: round(
            g - int(0.1 * g) + int(0.1 * g) ** 2 // (2 * g) - float(rule3.clock_pace(g, int(0.1 * g))), 2
        )
        for g in (2400, 6000, 12000)
    }


def check_the_quadratic_reading_at_gamma_2400_as_printed() -> Check:
    """The paces compose (ALGEBRA.md, The paces), as printed: "the law's reading p_0 = Gamma - c + c^2 div 2 Gamma is within one unit of the composition up to U = 0.10 at Gamma = 6,000, within Gamma U^3 / 6 of a unit (1.02 units at c = 600; 0.41 at Gamma = 2,400 and 2.0 at 12,000; R169 (h))": the exact power gives 0.44 at Gamma = 2,400 (0.436), Gamma U^3 / 6 = 0.40 plus the composition's U / (2 Gamma) term, the 1.02 and 2.0 recomputed; a finding on the printed 0.41."""
    readings = quadratic_readings()
    return readings[2400] == 0.41, {
        "readings at U = 0.1 by Gamma": readings,
        "Gamma U^3 / 6 at 2,400": 2400 * 0.001 / 6,
    }


def check_the_acts_factors() -> Check:
    """The write per proper volume and per proper interval (ALGEBRA.md); S.34 (d): with N = p_0 / Gamma, h = p_0 / p_a = 1 / N under p_a = p_0^2 / Gamma, a count source carries N^2 / (h_x h_y h_z) = N^5 = p_x p_y p_z / (p_0 Gamma^2) and the Wronskian N / (h_x h_y h_z) = N^4 = p_x p_y p_z / (p_0^2 Gamma); with a tension the rulers differ, h_a = p_0 / p_a, and the volume is h_x h_y h_z; the isotropic scalar N^2 / h^3 would miss by (h_x h_y h_z)^(1 / 3) / h; exact fractions."""
    draw = random.Random(SEED)
    for _ in range(30):
        gamma = draw.randint(2, 50)
        clock = Fraction(draw.randint(1, gamma))
        pace = clock * clock / gamma
        n = clock / gamma
        if n**5 != pace**3 / (clock * gamma * gamma) or n**4 != pace**3 / (clock * clock * gamma):
            return False, {"Gamma": gamma, "clock": clock}
        links = [pace * Fraction(draw.randint(1, gamma), gamma) for _ in range(3)]
        rulers = [clock / p for p in links]
        volume = rulers[0] * rulers[1] * rulers[2]
        if n * n / volume != links[0] * links[1] * links[2] / (
            clock * gamma * gamma
        ) or n / volume != links[0] * links[1] * links[2] / (clock * clock * gamma):
            return False, {"with tension": (gamma, clock, links)}
    return True, {"witnesses": 30}


def check_the_exponential_metrics_post_newtonian_orders() -> Check:
    """S.34 (c); S.19; Universe24_Paper.tex Section 3.4: the exponential metric g_00 = -e^(-2 U) and g_ij = e^(2 U) delta_ij expand as -(1 - 2 U + 2 U^2) and (1 + 2 U + 2 U^2), so gamma = 1 exactly and beta = 1 in U; the two expansions' remainders are of the third order (-4 U^3 / 3 and 4 U^3 / 3); the far end, U = 0.5: e^(-1) = 0.368 against the truncation's 0.500 and e^1 = 2.718 against 2.500, the orders holding and the values parting."""
    first, orders_1 = has_order(lambda u: math.exp(-2 * u) - (1 - 2 * u + 2 * u * u), 3, step=0.1)
    second, orders_2 = has_order(lambda u: math.exp(2 * u) - (1 + 2 * u + 2 * u * u), 3, step=0.1)
    coefficient_1 = (math.exp(-2 * 0.01) - (1 - 0.02 + 0.0002)) / 0.01**3
    coefficient_2 = (math.exp(2 * 0.01) - (1 + 0.02 + 0.0002)) / 0.01**3
    far = (round(math.exp(-1), 3), 0.5, round(math.exp(1), 3), 2.5)
    return first and second and abs(coefficient_1 + 4 / 3) < 0.02 and abs(
        coefficient_2 - 4 / 3
    ) < 0.02, {
        "orders": (orders_1, orders_2),
        "U^3 coefficients": (coefficient_1, coefficient_2),
        "far end U = 0.5 (exact, truncated)": far,
    }


def check_the_clocks_click_rate() -> Check:
    """S.15, the clock's click rate; Universe24_Paper.tex Section 7.4: Eq. (4) at k = 0 with p_0^2 = Gamma^2 (1 - 2 U + 2 U^2) gives cos omega(U) = cos omega_0 + 2 g U - 2 g U^2 exactly; to first order d omega / omega_0 = -f(omega_0) dU with f = 2 (1 - cos omega_0) / (omega_0 sin omega_0), 1.063 at [2, 3]; f -> 1 as omega_0 -> 0, in series f = 1 + omega_0^2 / 12 + ..., 5.9 percent at the computed pair (6.3 exactly); the far end of the gap, num / den = 0.01: f = 1.269 against the series' 1.203; exact fractions for the quadratic clock, the residual's order for the first order (2 in U) and the series (4 in omega_0)."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8):
        g = 1 - Fraction(num, den)
        for _ in range(5):
            u = Fraction(draw.randint(0, 50), 100)
            if 1 - g * (1 - 2 * u + 2 * u * u) != Fraction(num, den) + 2 * g * u - 2 * g * u * u:
                return False, {"pair": (num, den), "U": u}
    omega_0 = rest_rotation(2, 3)
    f = clock_factor(omega_0)
    first_order, orders_u = has_order(
        lambda u: band_rotation(2, 3, 0.0, math.exp(-u)) - omega_0 * (1 - f * u), 2, step=0.02
    )
    series, orders_w = has_order(lambda w: clock_factor(w) - 1 - w * w / 12, 4, step=0.4)
    far_omega = rest_rotation(1, 100)
    witness = (
        round(f, 3),
        round(f - 1, 3),
        round(omega_0**2 / 12, 3),
        round(clock_factor(far_omega), 3),
        round(1 + far_omega**2 / 12, 3),
    )
    return first_order and series and witness[:3] == (1.063, 0.063, 0.059), {
        "f at [2, 3], f - 1, omega_0^2 / 12, f at num / den = 0.01, its series": witness,
        "orders": (orders_u, orders_w),
    }


def check_the_fall_and_keplers_potential() -> Check:
    """S.18, the fall and the Newtonian potential the orbits measure; Eq. (14); The method of derivation: the inertia m* = 3 den sin omega_0 / num = 3 tan omega_0; the acceleration a = [num / (3 den sin omega_0)] [2 g / sin omega_0] |grad U| = 2 cos omega_0 (1 - cos omega_0) / (3 sin^2 omega_0) |grad U| = 2 cos omega_0 / (3 (1 + cos omega_0)) |grad U|, in the gap epsilon = 1 - cos omega_0 [(1 - epsilon) / (3 (1 - epsilon / 2))] |grad U|: 0.2667 at [2, 3] and 1 / 3 as the gap closes; U_K = [2 cos omega_0 / (1 + cos omega_0)] U, 0.800 at [2, 3], 1 as the gap closes; exact rationals in cos omega_0 = num / den (sin^2 = (1 - cos)(1 + cos)), the limits at [999999, 1000000] and the far end num / den = 0.01."""
    draw = random.Random(SEED)
    results = {}
    for num, den in pairs(draw, 8) + [(999999, 1000000), (1, 100)]:
        if num == den:
            continue  # light: no gap, the fall's sines 0
        c = Fraction(num, den)
        g = 1 - c
        sine_squared = 1 - c * c
        acceleration = (
            (c / 3) / sine_squared * 2 * g
        )  # [num / (3 den sin)] [2 g / sin], the two sines as sin^2
        closed = 2 * c / (3 * (1 + c))
        epsilon = 1 - c
        gap_form = (1 - epsilon) / (3 * (1 - epsilon / 2))
        if acceleration != closed or gap_form != closed:
            return False, {"pair": (num, den), "a": acceleration, "closed": closed}
        results[(num, den)] = (closed, 2 * c / (1 + c))
    witness = (
        results[(2, 3)] == (Fraction(4, 15), Fraction(4, 5))
        and round(float(results[(2, 3)][0]), 4) == 0.2667
    )
    far = {
        "[999999, 1000000]": tuple(float(v) for v in results[(999999, 1000000)]),
        "num / den = 0.01": tuple(float(v) for v in results[(1, 100)]),
    }
    inertia = (
        abs(3 * 3 * math.sin(rest_rotation(2, 3)) / 2 - 3 * math.tan(rest_rotation(2, 3))) < 1e-12
    )  # m* = 3 den sin omega_0 / num = 3 tan omega_0 at [2, 3]
    return witness and inertia, {
        "a / |grad U| and U_K / U at [2, 3]": results[(2, 3)],
        "the limit and the far end": far,
    }


def check_the_post_newtonian_parameters() -> Check:
    """S.19: with U = lambda U_K, lambda = (1 + cos omega_0) / (2 cos omega_0) = (den + num) / (2 num), the bending 4 lambda U_K gives 1 + gamma_K = 1 + den / num; the periapsis lambda times Einstein's with (2 - beta + 2 gamma) / 3 gives beta_K = 2 + 2 den / num - 3 (den + num) / (2 num) = (den + num) / (2 num); the redshift f lambda = tan omega_0 / omega_0 = 1 + alpha_K; at [2, 3]: 1.5, 1.25, 1.329; all three tend to 1 as omega_0 -> 0, and gamma_K - 1 < 2 x 10^-5 requires den / num - 1 < 2 x 10^-5; exact rationals for gamma_K and beta_K, f lambda = tan omega_0 / omega_0 exact in (cos, sin) at rational points, the limit at [999999, 1000000] and the far end num / den = 0.01."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8):
        lam = Fraction(den + num, 2 * num)
        gamma_k = Fraction(den, num)
        beta_k = 2 + 2 * gamma_k - 3 * lam
        if beta_k != lam or lam != (1 + Fraction(num, den)) / (2 * Fraction(num, den)):
            return False, {"pair": (num, den), "beta_K": beta_k}
    for unit in angles(draw, 10):
        c, s = unit.re, unit.im
        if c <= 0 or s <= 0:
            continue
        if (
            2 * (1 - c) / s * (1 + c) / (2 * c) != s / c
        ):  # f lambda with omega_0 cancelled: [2 (1 - c) / (omega s)] [(1 + c) / (2 c)] = (s / c) / omega
            return False, {"f lambda": (c, s)}
    omega_0 = rest_rotation(2, 3)
    at_two_three = (1.5, 1.25, round(math.tan(omega_0) / omega_0, 3))
    far = {}
    for num, den in ((999999, 1000000), (1, 100)):
        w = rest_rotation(num, den)
        far[f"{num} / {den}"] = (den / num, (den + num) / (2 * num), math.tan(w) / w)
    return at_two_three == (1.5, 1.25, 1.329), {
        "gamma_K, beta_K, 1 + alpha_K at [2, 3]": at_two_three,
        "the limit and the far end": far,
    }


def check_the_moving_clock_to_the_fourth_order() -> Check:
    """S.21, the moving clock to the second order: from cos omega = c_0 (2 + cos k), omega(k) = omega_0 + alpha k^2 - beta k^4 + O(k^6) with alpha = c_0 / (2 s), beta = c_0 / (24 s) + c c_0^2 / (8 s^3); the rotation at the moving centre Omega = omega - k omega' and v = omega' give Omega / omega_0 = 1 - v^2 / (2 c_m^2) - (2 omega_0 / sin 2 omega_0) v^4 / (8 c_m^4) + O(v^6) with c_m^2 = omega_0 / (3 tan omega_0): Lorentz's factor at c_m to the second order exactly, the fourth order's factor 2 omega_0 / sin 2 omega_0, 1.69 at [2, 3] and 1 as the gap closes; along n the factor omega_0 [(SUM n_a^4) tan omega_0 + cot omega_0], 1.2224 on a face diagonal and 1.0657 on the body diagonal; the check (f - 1 + v^2 / (2 c_m^2)) / v^4 = -3.37 at v = 0.02 along an axis against 1.6926 x (-1.988) = -3.365, -2.12 along the body diagonal against -2.119; the band's series by the residual's order 6, the interval's by its order 6 in k, the numbers recomputed; the far end num / den = 0.01 for the factor."""
    num, den = 2, 3
    omega_0 = rest_rotation(num, den)
    c, s, c0 = math.cos(omega_0), math.sin(omega_0), num / (3 * den)
    alpha, beta = c0 / (2 * s), c0 / (24 * s) + c * c0**2 / (8 * s**3)
    band_order, band_orders = has_order(
        lambda k: band_rotation(num, den, k) - (omega_0 + alpha * k * k - beta * k**4), 6, step=0.3
    )
    c_m2 = omega_0 / (3 * math.tan(omega_0))
    factor = 2 * omega_0 / math.sin(2 * omega_0)

    def interval(k: float, direction=(1.0, 0.0, 0.0)) -> tuple[float, float]:
        """(v, Omega / omega_0) at the wave number k along the unit vector n, from the exact band by a centred difference."""
        h = 1e-4

        def omega(q: float) -> float:
            return math.acos(
                c0 * sum(math.cos(q * n) for n in direction) + c0 * (3 - sum(1 for _ in direction)) * 0
            )

        def full(q: float) -> float:
            return math.acos(1 - (1 - num / den) - c0 * sum(1 - math.cos(q * n) for n in direction))

        v = (full(k + h) - full(k - h)) / (2 * h)
        return v, (full(k) - k * v) / omega_0

    def residual(k: float) -> float:
        v, f = interval(k)
        return f - (1 - v * v / (2 * c_m2) - factor * v**4 / (8 * c_m2**2))

    interval_order, interval_orders = has_order(residual, 6, step=0.4)
    checks = []
    for direction, n4 in (((1.0, 0.0, 0.0), 1.0), ((1 / SQRT3,) * 3, 1 / 3)):
        k = 0.02 * 3 * math.tan(omega_0) * 1.0  # k with v near 0.02: v = k / m* at first order
        v, f = interval(k, direction)
        directional = omega_0 * (n4 * math.tan(omega_0) + 1 / math.tan(omega_0))
        checks.append(
            (
                round(v, 3),
                round((f - 1 + v * v / (2 * c_m2)) / v**4, 2),
                round(directional, 4),
                round(directional * (-1 / (8 * c_m2**2)), 3),
            )
        )
    face = omega_0 * (0.5 * math.tan(omega_0) + 1 / math.tan(omega_0))
    far_factor = rest_rotation(1, 100) * (
        math.tan(rest_rotation(1, 100)) + 1 / math.tan(rest_rotation(1, 100))
    )
    tiny = rest_rotation(999999, 1000000)
    limit_factor = tiny * (math.tan(tiny) + 1 / math.tan(tiny))
    numbers = (
        round(factor, 4),
        round(face, 4),
        round(checks[1][2], 4),
        round(c_m2, 4),
        round(-1 / (8 * c_m2**2), 3),
    )
    hold = (
        band_order
        and interval_order
        and numbers == (1.6926, 1.2224, 1.0657, 0.2508, -1.988)
        and checks[0][1:] == (-3.37, 1.6926, -3.365)
        and abs(checks[1][1] + 2.12) < 0.02
    )
    return hold, {
        "band series orders": band_orders,
        "interval series orders": interval_orders,
        "factor, face, body, c_m^2, Lorentz's v^4": numbers,
        "S.21's check (v, residual / v^4, factor, factor x Lorentz)": checks,
        "the factor at num / den = 0.01 and at 999999 / 1000000": (far_factor, limit_factor),
    }


def check_de_broglie_and_the_three_speeds() -> Check:
    """S.22; Universe24_Paper.tex Section 3.3 and S.53: v = k / m* with m* = 3 tan omega_0, so k = m* v = omega_b v / c_m^2 with c_m^2 = omega_0 / m* = omega_0 / (3 tan omega_0), 0.2508 at [2, 3], and m* c_m^2 = omega_0 exactly for every pair; the family's own speed c_s^2 = num / (3 den), c_m^2 and light's 1 / 3 are one as the gap closes (c_m / c = 0.867 at [2, 3], 0.9997 at [999, 1000]); the identity exact, the limit at [999999, 1000000], the far end num / den = 0.01."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8) + [(1, 100), (999999, 1000000)]:
        if num == den:
            continue  # light has no gap and no inertia
        omega_0 = rest_rotation(num, den)
        inertia = 3 * math.tan(omega_0)
        if abs(inertia * (omega_0 / inertia) - omega_0) > 1e-12 * omega_0:
            return False, {"pair": (num, den)}
    speeds = {}
    for num, den in ((2, 3), (999, 1000), (999999, 1000000), (1, 100)):
        omega_0 = rest_rotation(num, den)
        c_m2 = omega_0 / (3 * math.tan(omega_0))
        speeds[f"{num} / {den}"] = (num / (3 * den), c_m2, 1 / 3, math.sqrt(3 * c_m2))
    witness = (
        round(speeds["2 / 3"][1], 4),
        round(speeds["2 / 3"][3], 3),
        round(speeds["999 / 1000"][3], 4),
    )
    return witness == (0.2508, 0.867, 0.9997), {"c_s^2, c_m^2, c^2, c_m / c": speeds}


def check_the_push_on_a_moving_record() -> Check:
    """S.58; The push on a moving record (ALGEBRA.md, The paces): with E^2 = m^2 + P^2, m = N omega_0, P = c N^2 k and N = e^(-U), d(E^2) / dU = -2 m^2 - 4 P^2, so -(d omega / dU)_k = (E^2 + P^2) / E = E (1 + beta^2) with beta = P / E; the exact line from the band at a pace, F_perp = grad U [2 (1 - nu) e^(-2 U) + (4 nu / 3) e^(-4 U) SUM_a (1 - cos k_a)] / sin omega; at [2, 3] the rest push over E is f(omega_0) = 1.0634 and the coefficient of beta^2 is 1.3354 = gamma_K - alpha_K / 2; at [999, 1000] 1.00017 and 1.00067 (1 + omega_0^2 / 12 and 1 + omega_0^2 / 3); the derivative identities by the centred difference's order 2, the numbers recomputed."""
    omega_0 = rest_rotation(2, 3)
    c = 1 / SQRT3

    def energy(u: float, k: float) -> float:
        n = math.exp(-u)
        return math.sqrt((n * omega_0) ** 2 + (c * n * n * k) ** 2)

    k = 0.4
    e, p = energy(0.0, k), c * k
    held_1, orders_1 = has_order(
        lambda h: -(energy(h, k) - energy(-h, k)) / (2 * h) - (e * e + p * p) / e, 2, step=0.02
    )

    def exact_rotation(u: float, k: float, num: int = 2, den: int = 3) -> float:
        nu = num / den
        return math.acos(
            1 - (1 - nu) * math.exp(-2 * u) - (nu / 3) * math.exp(-4 * u) * (1 - math.cos(k))
        )

    def exact_push(u: float, k: float, num: int = 2, den: int = 3) -> float:
        nu = num / den
        return (
            2 * (1 - nu) * math.exp(-2 * u) + (4 * nu / 3) * math.exp(-4 * u) * (1 - math.cos(k))
        ) / math.sin(exact_rotation(u, k, num, den))

    held_2, orders_2 = has_order(
        lambda h: -(exact_rotation(h, k) - exact_rotation(-h, k)) / (2 * h) - exact_push(0.0, k),
        2,
        step=0.02,
    )
    rest = exact_push(0.0, 0.0) / omega_0
    coefficients = {}
    for num, den in ((2, 3), (999, 1000)):
        w0 = rest_rotation(num, den)
        rest_push = exact_push(0.0, 0.0, num, den) / w0

        def coefficient_at(
            small: float, w0: float = w0, num: int = num, den: int = den, rest_push: float = rest_push
        ) -> float:  # of beta^2 over the rest push, at the wave number small
            h = 1e-6 * w0
            v = (exact_rotation(0.0, small + h, num, den) - exact_rotation(0.0, small - h, num, den)) / (
                2 * h
            )
            beta = v / c
            return (
                exact_push(0.0, small, num, den) / exact_rotation(0.0, small, num, den) - rest_push
            ) / (rest_push * beta**2)

        at_k, at_half_k = coefficient_at(0.01 * w0), coefficient_at(0.005 * w0)
        coefficient = at_half_k + (at_half_k - at_k) / 3  # the limit k -> 0, the k^2 correction removed
        coefficients[f"{num} / {den}"] = (round(rest_push, 5), round(coefficient, 5))
    gamma_k, alpha_k = 1.5, math.tan(omega_0) / omega_0 - 1
    witness = (
        coefficients["2 / 3"] == (round(clock_factor(omega_0), 5), round(gamma_k - alpha_k / 2, 5))
        and round(rest, 4) == 1.0634
    )
    return held_1 and held_2 and witness and coefficients["999 / 1000"] == (1.00017, 1.00067), {
        "orders": (orders_1, orders_2),
        "rest push over E and the beta^2 coefficient over it": coefficients,
        "gamma_K - alpha_K / 2": gamma_k - alpha_k / 2,
    }


def check_the_shadows_capture_radius() -> Check:
    """S.30: in a static isotropic index n(r) = e^(2 m / r) a circular ray stands where d(n r) / dr = 0, e^(2 m / r) (1 - 2 m / r) = 0 at r = 2 m, and the capture radius is b = n(2 m) 2 m = 2 e m = 5.437 m against Schwarzschild's 3 sqrt 3 m = 5.196 m, larger by 0.046; the quadratic index 1 / (1 - 2 U) gives r = 4 m and b = 8 m; the derivative by the centred difference (order 2), the roots and numbers recomputed."""
    m = 1.0

    def composed(r: float) -> float:
        return r * math.exp(2 * m / r)

    def quadratic(r: float) -> float:
        return r / (1 - 2 * m / r)

    held, orders = has_order(
        lambda h: (composed(2 * m + h) - composed(2 * m - h)) / (2 * h) - math.exp(1.0) * (1 - 1),
        2,
        step=0.1,
    )
    derivative_formula = all(
        abs((composed(r + 1e-6) - composed(r - 1e-6)) / 2e-6 - math.exp(2 * m / r) * (1 - 2 * m / r))
        < 1e-6
        for r in (2.5, 3.0, 5.0)
    )
    quadratic_root = abs((quadratic(4 * m + 1e-6) - quadratic(4 * m - 1e-6)) / 2e-6) < 1e-6
    numbers = (
        round(2 * math.e, 3),
        round(3 * SQRT3, 3),
        round(2 * math.e / (3 * SQRT3) - 1, 3),
        quadratic(4 * m),
    )
    return held and derivative_formula and quadratic_root and numbers == (5.437, 5.196, 0.046, 8.0), {
        "orders": orders,
        "2 e, 3 sqrt 3, excess, quadratic b": numbers,
    }


def check_the_two_clocks_under_the_principle() -> Check:
    """S.31; Universe24_Paper.tex Table 4 and Section 3.4: every mode scales by N in 2 sin(omega / 2), so omega' = 2 arcsin(N sin(omega / 2)) = N omega [1 - (1 - N^2) omega^2 / 24 + O(omega^4)] and the beat Delta' = N Delta [1 - (1 - N^2) (omega_1^2 + omega_1 omega_2 + omega_2^2) / 24 + O(omega^4)], (1 - N^2) omega^2 / 8 at omega_1 = omega_2: at N = 0.8, omega_1 = 0.4, omega_2 = 0.9 the exact beat 0.3916 against N Delta = 0.4 and the series 0.3920; the correction 2.5 x 10^-38 at omega = 10^-14 and U = 10^-9; in omega the rest line's rate -2 tan(omega_0 / 2) / omega_0 = -f(omega_0) (the half-angle identity tan(omega / 2) = (1 - cos omega) / sin omega, exact at rational points); a cavity of bodies L / h = L N Links apart has the round trip 2 L N sqrt 3 / N^2 = 2 L sqrt 3 / N, the rate N exactly; the series by the residual's order 5, the numbers recomputed, the far end omega_1 = 2, omega_2 = 3 at N = 0.8."""
    draw = random.Random(SEED)

    def turned(n: float, omega: float) -> float:
        return 2 * math.asin(n * math.sin(omega / 2))

    n = 0.8
    held, orders = has_order(
        lambda w: turned(n, w) - n * w * (1 - (1 - n * n) * w * w / 24), 5, step=0.4
    )
    w1, w2 = 0.4, 0.9
    exact = turned(n, w2) - turned(n, w1)
    series = n * (w2 - w1) * (1 - (1 - n * n) * (w1 * w1 + w1 * w2 + w2 * w2) / 24)
    witness = (round(exact, 4), round(n * (w2 - w1), 4), round(series, 4))
    correction = (1 - math.exp(-2e-9)) * (1e-14) ** 2 / 8
    for unit in angles(draw, 10):
        c, s = unit.re, unit.im
        if s == 0:
            continue
        # tan(omega / 2) = (1 - cos omega) / sin omega: the Pythagorean (m, n) gives tan(omega / 2) = n / m exactly
        if (1 - c) / s != (1 - c) / s or (1 - c) * (1 + c) != s * s:
            return False, {"half angle": (c, s)}
    far_exact = turned(n, 3.0) - turned(n, 2.0)
    far_series = n * 1.0 * (1 - (1 - n * n) * (4 + 6 + 9) / 24)
    cavity = abs(2 * 10 * n * SQRT3 / (n * n) - 2 * 10 * SQRT3 / n) < 1e-12
    return held and witness == (0.3916, 0.4, 0.392) and abs(
        correction / 2.5e-38 - 1
    ) < 0.02 and cavity, {
        "orders": orders,
        "exact beat, N Delta, series": witness,
        "correction at nature's gap": correction,
        "far end omega = 2, 3 (exact, N Delta, series)": (far_exact, n * 1.0, far_series),
    }


def check_lights_index_to_first_order() -> Check:
    """S.2; S.12: light's speed at the content x is N^2 = e^(-2 x) of its vacuum speed, so its index is n = e^(2 x) = 1 / (1 - 2 x) + O(x^2) and n - 1 = 2 x + O(x^2); two events over L Links at the two speeds arrive L sqrt 3 [1 / (1 - 2 x) - 1] = 2 x L sqrt 3 + O(x^2) intervals apart; the orders by the residual, the far end x = 0.4 and the quadratic form's horizon x = 0.5, where 1 / (1 - 2 x) diverges and e^(2 x) = 2.718 (S.3: a horizon of the truncation)."""
    first, orders_1 = has_order(lambda x: math.exp(2 * x) - 1 / (1 - 2 * x), 2, step=0.05)
    second, orders_2 = has_order(lambda x: math.exp(2 * x) - 1 - 2 * x, 2, step=0.05)
    third, orders_3 = has_order(
        lambda x: 10 * SQRT3 * (1 / (1 - 2 * x) - 1) - 2 * x * 10 * SQRT3, 2, step=0.05
    )
    far = {
        "x = 0.4": (math.exp(0.8), 1 / 0.2, 1.8),
        "x = 0.5": (math.exp(1.0), "1 / (1 - 2 x) diverges", 2.0),
    }
    return first and second and third, {
        "orders": (orders_1, orders_2, orders_3),
        "far end (e^2x, 1 / (1 - 2x), 1 + 2x)": far,
    }


def check_the_mass_defects_first_order() -> Check:
    """S.38 (b): a body in its own content x rotates at N omega_0 with N = e^(-x), so its click mass is M sin(N omega_0) = M sin omega_0 - M omega_0 x cos omega_0 + O(x^2); the order by the residual, the far end x = 1 at [2, 3]."""
    omega_0 = rest_rotation(2, 3)
    held, orders = has_order(
        lambda x: (
            math.sin(math.exp(-x) * omega_0) - (math.sin(omega_0) - omega_0 * x * math.cos(omega_0))
        ),
        2,
        step=0.01,
    )
    far = (math.sin(math.exp(-1) * omega_0), math.sin(omega_0) - omega_0 * math.cos(omega_0))
    return held, {"orders": orders, "far end x = 1 (exact, first order)": far}


def check_the_preferred_frame_parameter() -> Check:
    """S.35: a metric whose g_0j vanishes in its preferred frame has 4 gamma + 4 + alpha_1 = 0, alpha_1 = -4 (1 + gamma) = -8 at gamma = 1; the frame-dragging precession (4 gamma + 4 + alpha_1) / 8 of Lense-Thirring's is 0; a covariant boost of the static metric would give g_0i = gamma_L^2 v (N^2 - h^2) = -4 U v to first order (-4.000); exact arithmetic and the residual's order (3, since e^(-2 U) - e^(2 U) = -4 U - 8 U^3 / 3 - ...)."""
    gamma_ppn = Fraction(1)
    alpha_1 = -4 * (1 + gamma_ppn)
    drag = (4 * gamma_ppn + 4 + alpha_1) / 8
    held, orders = has_order(lambda u: (math.exp(-2 * u) - math.exp(2 * u)) + 4 * u, 3, step=0.1)
    coefficient = (math.exp(-2 * 0.001) - math.exp(2 * 0.001)) / 0.001
    return alpha_1 == -8 and drag == 0 and held and round(coefficient, 3) == -4.0, {
        "alpha_1": alpha_1,
        "drag": drag,
        "orders": orders,
        "first-order coefficient": coefficient,
    }


def check_the_staggered_clocks_redshift() -> Check:
    """S.36, the fifth way: the staggered clock's rest rotation 1 - cos omega = (1 - nu) N^2 + nu N^4 (1 - cos(omega / 2)) gives at small omega omega^2 = 8 (1 - nu) N^2 / (4 - nu N^4) and for nu -> 1 omega / omega_0 = N sqrt(3 / (4 - N^4)) = N (1 - 2 U / 3 + ...), a redshift 5 / 3 of general relativity's; sqrt(3 / (4 - 0.9^4)) = 0.9472; demanding the exact redshift for every small-gap family, P_0 (4 - nu) = N^2 (4 - nu P_a) for all nu, forces P_0 = N^2 and P_a = 1 (the coefficients of nu^0 and nu^1); the series by the residual's order 2, the forcing exact."""
    held, orders = has_order(
        lambda u: math.exp(-u) * math.sqrt(3 / (4 - math.exp(-4 * u))) - math.exp(-u) * (1 - 2 * u / 3),
        2,
        step=0.05,
    )
    witness = round(math.sqrt(3 / (4 - 0.9**4)), 4)
    draw = random.Random(SEED)
    forcing = True
    for _ in range(20):
        n2 = Fraction(draw.randint(1, 99), 100)
        # P_0 (4 - nu) = N^2 (4 - nu P_a) at two values of nu determines (P_0, P_a): nu = 0 gives P_0 = N^2, then nu = 1 gives P_a = 1
        p_0 = n2 * 4 / 4
        p_a = (4 - p_0 * (4 - 1) / n2) / 1
        forcing = forcing and p_0 == n2 and p_a == 1
    return held and witness == 0.9472 and forcing, {"orders": orders, "sqrt(3 / (4 - 0.9^4))": witness}


def check_the_frozen_content() -> Check:
    """S.41 (3); The paces compose; row 4 of The conventions and the units: p_i = p_0^2 / Gamma rounds to 0 where Gamma e^(-2 U) < 1 / 2, that is U > (1 / 2) ln(2 Gamma), the frozen content c_f = (Gamma / 2) ln(2 Gamma), 4.70 Gamma levels, 28,206 at Gamma = 6,000 with p_0 rounded to the unit before squaring (paces.frozen_content, the derivation script's), the formula's 28,178; the inequality exact, the numbers recomputed."""
    gamma = 6000
    exact, formula = paces.frozen_content(gamma)
    threshold = 0.5 * math.log(2 * gamma)
    inequality = all(
        (gamma * math.exp(-2 * u) < 0.5) == (u > threshold) for u in (4.0, 4.5, 4.69, 4.70, 4.8, 6.0)
    )
    return inequality and exact == 28206 and round(formula) == 28178 and round(threshold, 2) == 4.7, {
        "frozen content exact and formula": (exact, formula),
        "(1 / 2) ln(2 Gamma)": threshold,
    }


def check_the_bounds_from_the_photon_and_the_dispersion() -> Check:
    """S.27 and S.24: one interval is omega_0 x 1.288 x 10^-21 s and one Link omega_0 x 6.69 x 10^-13 m (sqrt 3 x 3.862 x 10^-13); a photon of 1.4 PeV read as a share gives sin omega_0 <= 0.511 MeV / 1.4 PeV = 3.65 x 10^-10 on the diagonal and 3.44 x 10^-10 on an axis (the axis's share tops at T sin 1.231 = 0.943 T), den = 2 / omega_0^2 > 1.5 x 10^19 and gamma_K - 1 = omega_0^2 / 2 < 6.7 x 10^-20; MAGIC's |delta v / v| = (3 / 2) (1 TeV / 6.3 x 10^10 GeV)^2 = 3.8 x 10^-16 gives k^2 / 12 < 3.8 x 10^-16, k < 6.7 x 10^-8 per Link, the Link below k lambda / (2 pi) = 1.3 x 10^-26 m along an axis with lambda = 1.24 x 10^-18 m, 2.1 x 10^-26 m on the directional mean (the k^4 coefficient -1 / 135 against -1 / 54), omega_e < 2.0 x 10^-14 over the unit 6.69 x 10^-13 m (3.1 x 10^-14 on the mean) and gamma_K - 1 < 2.0 x 10^-28; every number recomputed."""
    hbar, m_e, c_light = 1.054572e-34, 9.109384e-31, 2.99792458e8
    interval = hbar / (m_e * c_light**2)
    link = SQRT3 * hbar / (m_e * c_light)
    sine_bound = 0.511e6 / 1.4e15
    axis_bound = sine_bound * math.sin(math.acos(1 / 3))
    den_bound = 2 / sine_bound**2
    gamma_bound = sine_bound**2 / 2
    magic = 1.5 * (1e3 / 6.3e10) ** 2
    k_bound = math.sqrt(12 * magic)
    link_bound = k_bound * 1.24e-18 / (2 * math.pi)
    mean_link_bound = link_bound * math.sqrt((1 / 54) / (1 / 135))
    omega_e = link_bound / 6.69e-13
    numbers = (
        f"{interval:.3e}",
        f"{link:.2e}",
        f"{sine_bound:.2e}",
        f"{axis_bound:.2e}",
        f"{den_bound:.1e}",
        f"{gamma_bound:.1e}",
        f"{magic:.1e}",
        f"{k_bound:.1e}",
        f"{link_bound:.1e}",
        f"{mean_link_bound:.1e}",
        f"{omega_e:.1e}",
        f"{omega_e**2 / 2:.1e}",
        f"{mean_link_bound / 6.69e-13:.1e}",
    )
    expected = (
        "1.288e-21",
        "6.69e-13",
        "3.65e-10",
        "3.44e-10",
        "1.5e+19",
        "6.7e-20",
        "3.8e-16",
        "6.7e-08",
        "1.3e-26",
        "2.1e-26",
        "2.0e-14",
        "2.0e-28",
        "3.1e-14",
    )
    return numbers == expected, {"computed": numbers, "printed": expected}


def check_the_bending_and_shapiros_integrals() -> Check:
    """S.20: along a straight path at the impact parameter b from -x_1 to x_2 the delay is 2 sqrt 3 mu [arsinh(x_2 / b) + arsinh(x_1 / b)], for x_1, x_2 >> b 2 sqrt 3 mu ln(4 x_1 x_2 / b^2), Shapiro's delay; the bending's transverse integral is integral b dl / (b^2 + l^2)^(3 / 2) = 2 / b, so with n - 1 = 2 U the turn is 4 U_b, twice the Newtonian 2 U_b; the antiderivative l / (b sqrt(b^2 + l^2)) exact at its limits, the arsinh integral by quadrature against the closed form, the logarithm's remainder of the order 1 / x^2."""
    b = 1.7
    exact = 2 / b

    def antiderivative(x: float) -> float:
        return x / (b * math.sqrt(b * b + x * x))

    limit = antiderivative(1e9) - antiderivative(-1e9)
    steps = 200000
    quadrature = (
        sum(b / (b * b + x * x) ** 1.5 for x in (-60 + 120 * (j + 0.5) / steps for j in range(steps)))
        * 120
        / steps
    )
    tail = 2 * (1 / b - antiderivative(60))
    delay_quadrature = (
        sum(1 / math.sqrt(x * x + b * b) for x in (-30 + 80 * (j + 0.5) / steps for j in range(steps)))
        * 80
        / steps
    )
    delay_closed = math.asinh(50 / b) + math.asinh(30 / b)
    held, orders = has_order(
        lambda h: (math.asinh(1 / (h * b)) + math.asinh(1 / (h * b))) - math.log(4 / (h * h * b * b)),
        2,
        step=0.02,
    )
    return abs(limit - exact) < 1e-9 and abs(quadrature + tail - exact) < 1e-7 and abs(
        delay_quadrature - delay_closed
    ) < 1e-6 and held, {
        "2 / b": exact,
        "antiderivative's limit": limit,
        "quadrature with its tail": quadrature + tail,
        "logarithm's orders": orders,
    }


def check_the_slow_limits_rest_rotation() -> Check:
    """S.63's input: the rest rotation at a content, omega_0(U) = omega_0 - omega_0 f(omega_0) U + O(U^2) (S.15); the order by the residual at [2, 3] with the composed clock, the far end U = 0.5."""
    omega_0 = rest_rotation(2, 3)
    f = clock_factor(omega_0)
    held, orders = has_order(
        lambda u: band_rotation(2, 3, 0.0, math.exp(-u)) - omega_0 * (1 - f * u), 2, step=0.05
    )
    far = (band_rotation(2, 3, 0.0, math.exp(-0.5)), omega_0 * (1 - f * 0.5))
    return held, {"orders": orders, "far end U = 0.5 (exact, first order)": far}


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
