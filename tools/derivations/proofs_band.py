"""The band's checks (ALGEBRA.md, The line, The band at a pace, The guard, The exact bands, The well; the supplement's S.1, S.3, S.11, S.21, S.24, S.27, S.28): every statement quoted in its function's docstring with its place, the identities exact in Fractions at random rational witnesses with the symmetric cases forced, the expansions by the residual's order at two step sizes (proofs_ground).

Usage: `python tools/derivations/proofs_band.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402
from proofs_ground import (  # noqa: E402
    SEED,
    Check,
    angle,
    angles,
    cos_sin,
    has_order,
    pairs,
    run,
)


def band_cosine(
    num: int,
    den: int,
    gamma: int,
    clock: int,
    links: tuple[int, int, int],
    cosines: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    """(S + 2 SUM_a R_a cos k_a) / (2 w) from rule3's coefficients: the line's dispersion (row 3 of The conventions and the units)."""
    wall, reads, self_coefficient = rule3.coefficients(num, den, gamma, clock, links)
    return (
        Fraction(self_coefficient)
        + 2 * sum(Fraction(r) * c for r, c in zip(reads, cosines, strict=True))
    ) / (2 * wall)


def lorentz_form(
    num: int,
    den: int,
    gamma: int,
    clock: int,
    links: tuple[int, int, int],
    cosines: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    """cos omega = 1 - (1 - num / den) (p_0 / Gamma)^2 - (num / (3 den)) SUM_a (p_a / Gamma)^2 (1 - cos k_a) (The line, The clock once and the Link twice; Eq. (4) of the paper)."""
    mass = (1 - Fraction(num, den)) * Fraction(clock, gamma) ** 2
    band = sum(Fraction(p, gamma) ** 2 * (1 - c) for p, c in zip(links, cosines, strict=True))
    return 1 - mass - Fraction(num, 3 * den) * band


def light_rotation(k: float, direction: tuple[float, float, float] = (1.0, 0.0, 0.0)) -> float:
    """omega of light's band along the unit vector n at the wave number k, 1 - cos omega = (1 / 3) SUM_a (1 - cos(k n_a)) evaluated as 2 sin^2 of half angles, so no cancellation at small k."""
    half = sum(2 * math.sin(k * n / 2) ** 2 for n in direction) / 3  # 1 - cos omega
    return 2 * math.asin(math.sqrt(half / 2))


def check_band_identity_of_a_plane_wave() -> Check:
    """The line (ALGEBRA.md, The line; row 3 of The conventions and the units; S.1): a plane wave A cos(k . x - omega t) put into the line without its remainder leaves the residual w (a_next + a_before) - [SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now] = a_now [2 w cos omega - S - 2 SUM_a R_a cos k_a], so the wave solves the line exactly iff 2 w cos omega = S + 2 SUM_a R_a cos k_a; checked exactly at every Node for random rational angles k_a, omega and theta = k . x - omega t (the arrivals read through rule3.numerator), the symmetric angles 0, pi and the quarter turns forced."""
    draw = random.Random(SEED)
    witnesses = 0
    for num, den in pairs(draw, 8):
        gamma = draw.randint(2, 30)
        clock = draw.randint(1, gamma)
        links = (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma))
        wall, reads, self_coefficient = rule3.coefficients(num, den, gamma, clock, links)
        wave_triples = [(angle(1, 0),) * 3, (angle(0, 1),) * 3] + [
            tuple(angles(draw, 9)[6:9]) for _ in range(3)
        ]
        for rotation in angles(draw, 7):
            for phase in angles(draw, 7):
                waves = wave_triples[(len(wave_triples) + witnesses) % len(wave_triples)]
                amplitude = draw.randint(1, 1000)
                now = amplitude * phase.re
                before = amplitude * (phase * rotation).re  # theta + omega one interval earlier
                after = amplitude * (phase * rotation.conj()).re  # theta - omega
                arrivals = []
                for wave_unit in waves:
                    arrivals += [
                        amplitude * (phase * wave_unit).re,
                        amplitude * (phase * wave_unit.conj()).re,
                    ]
                right = rule3.numerator(now, arrivals, reads, self_coefficient)
                residual = wall * (after + before) - right
                claimed = now * (
                    2 * wall * rotation.re
                    - self_coefficient
                    - 2 * sum(r * w.re for r, w in zip(reads, waves, strict=True))
                )
                if residual != claimed:
                    return False, {"pair": (num, den), "residual": residual, "claimed": claimed}
                witnesses += 1
    return True, {"witnesses": witnesses}


def check_band_at_a_pace_is_the_lorentz_form() -> Check:
    """The line, The clock once and the Link twice; The band at a pace; S.1, Eq. (4): (S + 2 SUM_a R_a cos k_a) / (2 w) equals 1 - (1 - num / den) (p_0 / Gamma)^2 - (num / (3 den)) SUM_a (p_a / Gamma)^2 (1 - cos k_a) exactly, a polynomial identity in the paces and the cosines, at random integer paces and rational cosines, the vacuum's paces and k = 0, pi forced."""
    draw = random.Random(SEED)
    witnesses = 0
    for num, den in pairs(draw, 10):
        gamma = draw.randint(2, 40)
        for clock, links in [(gamma, (gamma, gamma, gamma))] + [
            (
                draw.randint(1, gamma),
                (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma)),
            )
            for _ in range(6)
        ]:
            for cosines in [
                (Fraction(1), Fraction(1), Fraction(1)),
                (Fraction(-1), Fraction(-1), Fraction(-1)),
            ] + [tuple(cos_sin(u)[0] for u in angles(draw, 9)[6:9]) for _ in range(5)]:
                left = band_cosine(num, den, gamma, clock, links, cosines)
                right = lorentz_form(num, den, gamma, clock, links, cosines)
                if left != right:
                    return False, {
                        "pair": (num, den),
                        "paces": (clock, links),
                        "left": left,
                        "right": right,
                    }
                witnesses += 1
    return True, {"witnesses": witnesses}


def check_vacuum_band_and_lights_dispersion() -> Check:
    """Row 3 of The conventions and the units; S.1: at the vacuum's paces w = 6 den Gamma^2, R = 2 num Gamma^2, S = 12 num Gamma^2 - 6 R = 0, so cos omega = (num / (3 den)) SUM_a cos k_a, the gap cos omega_0 = num / den at k = 0, light [1, 1] has cos omega = (2 + cos k) / 3 along an axis; exact at rational cosines, and rule3.plane_wave_dispersion is the same number in floats."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8):
        gamma = draw.randint(2, 40)
        wall, reads, self_coefficient = rule3.coefficients(num, den, gamma)
        if self_coefficient != 0 or self_coefficient != 12 * num * gamma**2 - 6 * reads[0]:
            return False, {"pair": (num, den), "S": self_coefficient}
        for units in [angles(draw, 9)[6:9] for _ in range(5)]:
            cosines = tuple(u.re for u in units)
            if band_cosine(num, den, gamma, gamma, (gamma,) * 3, cosines) != Fraction(
                num, 3 * den
            ) * sum(cosines):
                return False, {"pair": (num, den), "cosines": cosines}
        if band_cosine(num, den, gamma, gamma, (gamma,) * 3, (Fraction(1),) * 3) != Fraction(num, den):
            return False, {"pair": (num, den), "gap": "not num / den"}
    light = band_cosine(1, 1, 7, 7, (7, 7, 7), (angle(2, 1).re, Fraction(1), Fraction(1)))
    if light != (2 + angle(2, 1).re) / 3:
        return False, {"light": light}
    k = math.acos(float(angle(2, 1).re))
    agreement = abs(rule3.plane_wave_dispersion(k, 1, 1) - float(light)) < 1e-12
    return agreement, {
        "light cos omega at cos k = 3 / 5": light,
        "rule3": rule3.plane_wave_dispersion(k, 1, 1),
    }


def check_the_clocks_shift_alike() -> Check:
    """The line (i), The clocks shift alike: at k = 0 every massive band's rest rotation obeys 1 - cos omega_b = (p_0 / Gamma)^2 (1 - cos omega_0), one factor for every family; from the band at a pace, exact."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 10):
        gamma = draw.randint(2, 40)
        clock = draw.randint(1, gamma)
        links = (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma))
        rest = band_cosine(num, den, gamma, clock, links, (Fraction(1),) * 3)
        if 1 - rest != Fraction(clock, gamma) ** 2 * (1 - Fraction(num, den)):
            return False, {"pair": (num, den), "1 - cos omega_b": 1 - rest}
    return True, {"pairs": 10}


def check_the_guards_edge() -> Check:
    """The guard; S.3: the mode at wave number pi on every axis has the factor (S - 2 SUM_a R_a) / w = 2 - 2 (1 - num / den) (p_0 / Gamma)^2 - 4 (num / den) (p_a / Gamma)^2, -2 num / den in the vacuum, and with p_0 = p_a = p it stays at or above -2 exactly when p^2 (den + num) <= 2 den Gamma^2, the edge P^2 = 2 den Gamma^2 div (den + |num|), Gamma^2 for light; for a numerator below 0 the lowest mode is at k = 0, 2 - 2 (1 - num / den) (p_0 / Gamma)^2, at or above -2 exactly when p_0^2 (den - num) <= 2 den Gamma^2, the same edge with |num|; exact, rule3.guard_edge_squared the edge."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8) + [(-1, 2), (-3, 7), (-5, 5)]:
        gamma = draw.randint(2, 40)
        for pace in range(1, 2 * gamma + 1):
            links = (pace, pace, pace)
            wall, reads, self_coefficient = rule3.coefficients(num, den, gamma, pace, links)
            at_pi = Fraction(self_coefficient - 2 * sum(reads), wall)
            closed = (
                2
                - 2 * (1 - Fraction(num, den)) * Fraction(pace, gamma) ** 2
                - 4 * Fraction(num, den) * Fraction(pace, gamma) ** 2
            )
            if at_pi != closed:
                return False, {"pair": (num, den), "at pi": at_pi, "closed form": closed}
            at_zero = Fraction(self_coefficient + 2 * sum(reads), wall)
            lowest = min(at_pi, at_zero)
            edge = rule3.guard_edge_squared(num, den, gamma)
            if (lowest >= -2) != (pace * pace <= edge):
                return False, {"pair": (num, den), "pace": pace, "lowest": lowest, "edge": edge}
            if (lowest >= -2) != (pace * pace * (den + abs(num)) <= 2 * den * gamma * gamma):
                return False, {"pair": (num, den), "pace": pace, "inequality": lowest}
        if band_cosine(num, den, gamma, gamma, (gamma,) * 3, (Fraction(-1),) * 3) * 2 != -2 * Fraction(
            num, den
        ):
            return False, {"pair": (num, den), "vacuum at pi": "not -2 num / den"}
    return rule3.guard_edge_squared(1, 1, 6000) == 6000**2, {
        "P^2 for light at Gamma 6,000": rule3.guard_edge_squared(1, 1, 6000)
    }


def check_the_total_mirror_of_light() -> Check:
    """The band at a pace: for [1, 1] a record of the vacuum's rotation at the wave number k is evanescent inside a pace region, cosh kappa = (Gamma / p_a)^2 (1 - cos k) - 1 per Node, and light meets a total mirror exactly where p_a < Gamma sin(k / 2), that is where e^(-2 U) falls below sin(k / 2) under the composed paces, c above 1,733 at lambda = 4 Links and 2,464 at 4.78 at Gamma = 10^4 (the derivation script paces.py's thresholds in U); the evanescence condition cosh kappa > 1 is (p_a / Gamma)^2 < (1 - cos k) / 2 = sin^2(k / 2) exactly (the half-angle identity at the Pythagorean angle), and the thresholds by the exact power (1 - 1 / Gamma)^(2 c)."""
    gamma = 10
    for m in range(1, 9):
        for n in range(0, m):
            unit = angle(m, n)
            half_sine_squared = Fraction(n * n, m * m + n * n)  # sin^2(k / 2) at the Pythagorean angle
            if (1 - unit.re) / 2 != half_sine_squared:
                return False, {"half angle": (m, n)}
            for pace in range(1, gamma + 1):
                cosh_kappa = Fraction(gamma, pace) ** 2 * (1 - unit.re) - 1
                if (cosh_kappa > 1) != (Fraction(pace, gamma) ** 2 < half_sine_squared):
                    return False, {"mirror condition": (m, n, pace)}
    gamma = 10_000
    thresholds = []
    for wavelength in (4.0, 4.78):
        sine = math.sin(math.pi / wavelength)
        content = 0
        while (1 - 1 / gamma) ** (2 * content) >= sine:
            content += 1
        thresholds.append(content)
    return thresholds == [1733, 2464], {"c at lambda = 4 and 4.78": thresholds}


def check_the_three_exact_bands() -> Check:
    """The exact bands (a family's declaration): the one-Node line at rest, a_next = 2 cos omega_0 a_now - a_before, is exact in integers only where 2 cos omega_0 is an integer, so the rule carries exactly three exact rotations, 2 cos omega_0 = 1, 0 and -1, the periods 6, 4 and 3, the pairs [1, 2], [0, 1] and [-1, 2]: the integer matrix [[m, -1], [1, 0]] has the order 6, 4, 3 at m = 1, 0, -1 exactly, and no finite order at m = 2 and -2 (the uniform mode and the checkerboard, the double roots), the integers in [-2, 2] being all the values 2 cos omega_0 can take."""
    periods = {}
    for m in (-2, -1, 0, 1, 2):
        matrix = ((m, -1), (1, 0))
        power = ((1, 0), (0, 1))
        found = None
        for n in range(1, 13):
            power = (
                (
                    power[0][0] * matrix[0][0] + power[0][1] * matrix[1][0],
                    power[0][0] * matrix[0][1] + power[0][1] * matrix[1][1],
                ),
                (
                    power[1][0] * matrix[0][0] + power[1][1] * matrix[1][0],
                    power[1][0] * matrix[0][1] + power[1][1] * matrix[1][1],
                ),
            )
            if power == ((1, 0), (0, 1)):
                found = n
                break
        periods[m] = found
    rotations = {1: (1, 2), 0: (0, 1), -1: (-1, 2)}
    pairs_hold = all(Fraction(2 * num, den) == m for m, (num, den) in rotations.items())
    return periods == {-2: None, -1: 3, 0: 4, 1: 6, 2: None} and pairs_hold, {"periods": periods}


def check_the_band_top_along_the_diagonal_and_the_axis() -> Check:
    """S.27: along the body diagonal, k_a = q on every axis, light's band is omega = q exactly, so its speed stays 1 / sqrt 3 up to the corner; along an axis the top at k = pi has cos omega = 1 / 3, omega = 1.231, sin omega = 0.943; exact at rational cos q for the diagonal, the axis's numbers in floats."""
    draw = random.Random(SEED)
    for unit in angles(draw, 12):
        if band_cosine(1, 1, 5, 5, (5, 5, 5), (unit.re, unit.re, unit.re)) != unit.re:
            return False, {"diagonal cos q": unit.re}
    top = band_cosine(1, 1, 5, 5, (5, 5, 5), (Fraction(-1), Fraction(1), Fraction(1)))
    omega = math.acos(float(top))
    return top == Fraction(1, 3) and round(omega, 3) == 1.231 and round(math.sin(omega), 3) == 0.943, {
        "cos omega at k = pi on an axis": top,
        "omega": omega,
    }


def check_the_largest_group_speed() -> Check:
    """S.21: on the full band v_g is largest at k = (pi / 2, pi / 2, pi / 2), (num / den) / sqrt 3 = c cos omega_0, 0.3849 at [2, 3]: there cos omega = 0 and each component of grad omega is (num / (3 den)) sin k_a / sin omega = num / (3 den), so |v_g|^2 = num^2 / (3 den^2) exactly; the maximum over a grid of the zone is at the centre within the grid's step (a witness beside the exact value)."""
    num, den = 2, 3
    exact = Fraction(num * num, 3 * den * den)
    centre = 3 * Fraction(num, 3 * den) ** 2
    if centre != exact:
        return False, {"centre": centre}
    c0, best = num / (3 * den), 0.0
    steps = 24
    for i in range(1, steps):
        for j in range(1, steps):
            for m in range(1, steps):
                ks = (math.pi * i / steps, math.pi * j / steps, math.pi * m / steps)
                cosine = c0 * sum(math.cos(x) for x in ks)
                sine = math.sqrt(1 - cosine * cosine)
                speed = math.sqrt(sum((c0 * math.sin(x) / sine) ** 2 for x in ks))
                best = max(best, speed)
    return abs(best - math.sqrt(float(exact))) < 2e-3 and round(math.sqrt(float(exact)), 4) == 0.3849, {
        "largest on the grid": best,
        "(num / den) / sqrt 3": math.sqrt(float(exact)),
    }


def check_the_contents_index() -> Check:
    """S.28, the content's index for every family: a stationary boundary conserves omega, so equating the band outside, cos omega = 1 - g - (num / (3 den)) (1 - cos k), with the band inside, 1 - g N^2 - (num / (3 den)) N^4 (1 - cos k_in), gives 1 - cos k_in = [1 - cos k + 3 (den - num) (1 - N^2) / num] / N^4 exactly; for light (g = 0) sin(k_in / 2) = sin(k / 2) / s with s = N^2; the phase index k_in / k = (2 / k) arcsin(sin(k / 2) / s) = 1 / s + k^2 (1 / s^3 - 1 / s) / 24 + O(k^4), and to first order in U it is 1 + [4 tan(k / 2) / k] U; at k = pi / 2 and s = 0.8 the exact ratio is 1.380; the exact lines in Fractions, the two expansions by the residual's order (4 in k, 2 in U)."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8):
        for _ in range(5):
            clock_ratio = Fraction(draw.randint(1, 20), 20)
            cos_k = angles(draw, 7)[6].re
            inside = (
                1 - (1 - cos_k + 3 * (den - num) * (1 - clock_ratio**2) / num) / clock_ratio**4
            )  # cos k_in
            outside_band = 1 - (1 - Fraction(num, den)) - Fraction(num, 3 * den) * (1 - cos_k)
            inside_band = (
                1
                - (1 - Fraction(num, den)) * clock_ratio**2
                - Fraction(num, 3 * den) * clock_ratio**4 * (1 - inside)
            )
            if outside_band != inside_band:
                return False, {"pair": (num, den), "N": clock_ratio}
            if num == den and (1 - inside) / 2 != (1 - cos_k) / 2 / clock_ratio**4:
                return False, {"light": "sin^2(k_in / 2) is not sin^2(k / 2) / s^2"}
    s = 0.8

    def phase_index(k: float) -> float:
        return 2 / k * math.asin(math.sin(k / 2) / s)

    in_k, orders_k = has_order(
        lambda k: phase_index(k) - (1 / s + k * k * (1 / s**3 - 1 / s) / 24), 4, step=0.4
    )
    k = 0.7

    def index_at_content(u: float) -> float:
        return 2 / k * math.asin(math.sin(k / 2) * math.exp(2 * u))

    in_u, orders_u = has_order(
        lambda u: index_at_content(u) - (1 + 4 * math.tan(k / 2) / k * u), 2, step=0.02
    )
    witness = round(phase_index(math.pi / 2), 3)
    return in_k and in_u and witness == 1.380, {
        "orders in k": orders_k,
        "orders in U": orders_u,
        "ratio at k = pi / 2, s = 0.8": witness,
    }


def check_the_slow_matters_index_limit() -> Check:
    """S.28's check: with k^2 = m*^2 v^2 and m* = 3 tan omega_0 the 1 / k^2 term of the slow index is [4 (1 - cos omega_0) / (3 cos omega_0 tan^2 omega_0)] U / v^2, which as omega_0 -> 0 is (2 / 3) U / v^2 = 2 Phi / v^2 with Phi = c^2 U, c^2 = 1 / 3, nature's index for a slow body: the coefficient 12 (den - num) / (num m*^2) equals 4 (1 - cos omega_0) / (3 cos omega_0 tan^2 omega_0) exactly (cos omega_0 = num / den), and its residual against 2 / 3 is of the second order in omega_0."""

    def coefficient(omega_0: float) -> float:
        return 4 * (1 - math.cos(omega_0)) / (3 * math.cos(omega_0) * math.tan(omega_0) ** 2)

    for num, den in ((2, 3), (4, 5), (9, 10), (999, 1000)):
        omega_0 = math.acos(num / den)
        inertia = 3 * math.tan(omega_0)
        if abs(12 * (den - num) / (num * inertia**2) - coefficient(omega_0)) > 1e-9:
            return False, {"pair": (num, den)}
    held, orders = has_order(lambda w: coefficient(w) - 2 / 3, 2, step=0.2)
    return held, {"orders": orders, "coefficient at [2, 3]": coefficient(math.acos(2 / 3))}


def check_the_reach_of_a_holder() -> Check:
    """The well; S.11: a holder's rest outside its source, 6 den a = num S_6(a), falling as e^(-kappa r) along one axis has S_6(a) = (2 cosh kappa + 4) a, so cosh kappa = 3 den / num - 2; kappa^2 = 6 den / num - 6 to the second order in the gap; [1, 2] has cosh kappa = 4, e^(-kappa) = 0.127; R = 1 / kappa = sqrt(num / (6 (den - num))) = 20.00 at [2400, 2401]; inside a thick body the rest stands at 3 den sigma / (num kappa^2) = 3 den sigma / (6 (den - num)); Yukawa's identity, c / omega_g = R sqrt(den / num) to the gap's first order: the algebra exact, the two expansions by the residual's order."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8):
        if num == den:
            continue
        cosh_kappa = Fraction(3 * den, num) - 2
        if 6 * den != num * (2 * cosh_kappa + 4):
            return False, {"pair": (num, den), "cosh kappa": cosh_kappa}
        kappa_squared = Fraction(6 * (den - num), num)
        sigma = draw.randint(1, 9)
        if Fraction(3 * den * sigma, num) / kappa_squared != Fraction(3 * den * sigma, 6 * (den - num)):
            return False, {"pair": (num, den), "inside rest": "differs"}
    one_two = 4 - math.sqrt(15)
    reach = math.sqrt(2400 / (6 * (2401 - 2400)))

    def gap_residual(g: float) -> float:  # g = (den - num) / num, cosh kappa = 1 + 3 g
        return math.acosh(1 + 3 * g) ** 2 - 6 * g

    second_order, orders = has_order(gap_residual, 2, step=0.02)

    def yukawa_residual(g: float) -> float:  # g = (den - num) / den, cos omega_g = 1 - g
        return (1 / math.sqrt(3)) / math.acos(1 - g) / math.sqrt(1 / (6 * g)) - 1

    first_order, yukawa_orders = has_order(yukawa_residual, 1, step=0.02)
    witness = round(one_two, 3) == 0.127 and reach == 20.0
    return second_order and first_order and witness, {
        "e^-kappa at [1, 2]": one_two,
        "R at [2400, 2401]": reach,
        "kappa^2 orders": orders,
        "Yukawa orders": yukawa_orders,
    }


def check_the_group_velocity() -> Check:
    """The band at a pace; S.1: the group velocity along an axis is d omega / dk = (R_a / w) sin k / sin omega = (num / (3 den)) (p_a / Gamma)^2 sin k / sin omega, the vacuum's (num / (3 den)) sin k / sin omega, rule3.group_velocity; the centred difference quotient of omega(k) at the band's pace agrees with it to the second order in the step (the ratio 4 at halving)."""
    results = []
    for num, den, ratio in ((1, 1, 1.0), (2, 3, 1.0), (2, 3, 0.7), (9, 10, 0.5)):
        g, c0 = 1 - num / den, num / (3 * den)

        def omega(k: float, g: float = g, ratio: float = ratio, c0: float = c0) -> float:
            return math.acos(1 - g * ratio**2 - c0 * ratio**4 * (1 - math.cos(k)))

        k = 0.9
        formula = c0 * ratio**4 * math.sin(k) / math.sin(omega(k))
        held, orders = has_order(
            lambda h, k=k, formula=formula: (omega(k + h) - omega(k - h)) / (2 * h) - formula,
            2,
            step=0.05,
        )
        if ratio == 1.0 and abs(formula - rule3.group_velocity(k, num, den)) > 1e-12:
            return False, {
                "pair": (num, den),
                "rule3": rule3.group_velocity(k, num, den),
                "formula": formula,
            }
        results.append((num, den, ratio, orders))
        if not held:
            return False, {"pair": (num, den), "ratio": ratio, "orders": orders}
    return True, {"orders": results}


def check_lights_speed_and_dispersion_series() -> Check:
    """S.1, Light's speed and dispersion: for [1, 1] along an axis cos omega = (2 + cos k) / 3, so 1 - omega^2 / 2 + omega^4 / 24 = 1 - k^2 / 6 + k^4 / 72, omega = (k / sqrt 3) (1 - k^2 / 36 + ...) and the group velocity d omega / dk = sin k / (3 sin omega) = (1 / sqrt 3) (1 - k^2 / 12 + ...): the speed 1 / sqrt 3 at long wavelength (The lattice constants) and the group speed falling as 1 - 0.083 k^2; S.1's check, (sqrt 3 d omega / dk - 1) / k^2 = -0.0833, -0.0834, -0.0835 at k = 0.05, 0.1, 0.2; the residuals of the two expansions are of the orders 5 and 4."""
    omega_order, omega_orders = has_order(
        lambda k: light_rotation(k) - k / math.sqrt(3) * (1 - k * k / 36), 5, step=0.2
    )
    group_order, group_orders = has_order(
        lambda k: math.sin(k) / (3 * math.sin(light_rotation(k))) - (1 - k * k / 12) / math.sqrt(3),
        4,
        step=0.2,
    )
    cosine_order, cosine_orders = has_order(
        lambda k: (2 + math.cos(k)) / 3 - (1 - k * k / 6 + k**4 / 72), 6, step=0.4
    )
    witnesses = [
        round((math.sqrt(3) * math.sin(k) / (3 * math.sin(light_rotation(k))) - 1) / k**2, 4)
        for k in (0.05, 0.1, 0.2)
    ]
    speed = abs(rule3.group_velocity(1e-3, 1, 1) - 1 / math.sqrt(3)) < 1e-5
    return omega_order and group_order and cosine_order and speed and witnesses == [
        -0.0833,
        -0.0834,
        -0.0835,
    ], {
        "omega orders": omega_orders,
        "group orders": group_orders,
        "cosine orders": cosine_orders,
        "S.1's check": witnesses,
    }


def check_the_fourth_order_of_lights_band() -> Check:
    """S.24: along an axis the band's k^4 coefficient (of omega^2) is -1 / 54, -1 / 135 averaged over directions and 0 along a diagonal; from 1 - cos omega = (1 / 3) SUM_a (1 - cos(k n_a)) the coefficient is 1 / 108 - SUM_a n_a^4 / 36, an exact rational for a direction with rational squares, the sphere's mean of n_a^4 the exact 1 / 5 (the mean of x^4 on [-1, 1]), so the mean coefficient is -1 / 135; each coefficient confirmed by the residual's order 6 along its direction; and the anisotropies of The law's own formulas (11), an axis against the face diagonal k^2 / 48 in phase and k^2 / 16 in group, against the body diagonal k^2 / 36 and k^2 / 12, follow from the same coefficients exactly."""
    directions = {
        "axis": ((Fraction(1), Fraction(0), Fraction(0)), (1.0, 0.0, 0.0)),
        "face diagonal": (
            (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
            (1 / math.sqrt(2), 1 / math.sqrt(2), 0.0),
        ),
        "body diagonal": ((Fraction(1, 3),) * 3, (1 / math.sqrt(3),) * 3),
    }
    coefficients = {}
    for name, (squares, unit) in directions.items():
        fourth = sum(s * s for s in squares)
        coefficient = Fraction(1, 108) - fourth / 36
        coefficients[name] = coefficient
        held, orders = has_order(
            lambda k, u=unit, c=coefficient: light_rotation(k, u) ** 2 - k * k / 3 - float(c) * k**4,
            6,
            step=0.4,
        )
        if not held:
            return False, {"direction": name, "orders": orders}
    mean_fourth_power = Fraction(1, 2) * (
        Fraction(1, 5) - Fraction(-1, 5)
    )  # the mean of x^4 over [-1, 1]
    mean = Fraction(1, 108) - 3 * mean_fourth_power / 36
    phase = {
        name: Fraction(3, 2) * c for name, c in coefficients.items()
    }  # omega / k = (1 / sqrt 3)(1 + (3 c / 2) k^2)
    group = {
        name: -Fraction(9, 2) * c for name, c in coefficients.items()
    }  # d omega / dk = (1 / sqrt 3)(1 - C k^2)
    anisotropy = (
        phase["axis"] - phase["face diagonal"],
        group["face diagonal"] - group["axis"],
        phase["axis"] - phase["body diagonal"],
        group["body diagonal"] - group["axis"],
    )
    expected = (Fraction(-1, 48), Fraction(-1, 16), Fraction(-1, 36), Fraction(-1, 12))
    held = (
        coefficients["axis"] == Fraction(-1, 54)
        and coefficients["body diagonal"] == 0
        and mean == Fraction(-1, 135)
        and anisotropy == expected
    )
    return held, {
        "coefficients": coefficients,
        "mean": mean,
        "anisotropies (phase face, group face, phase body, group body)": anisotropy,
    }


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
