"""The breaker's rows for the derived claims of the paper's abstract and tables (the method of 2026-10-04): the band's inertia and kinetic scale, the post-Newtonian parameters, the exponential metric, the shadow, the fall and de Broglie, Bell's 478 / 169 and GHZ's -4, the clock's exponential, Yukawa's reach, light's speed, the moving clock's fourth order, the frozen content, the booking identity and the redshift, each tried inside its condition and outside it where the claim states one. Every number of the law is rule3.py's, every credit bell.py's, every band bands.py's or moving_clock.py's; floats stand only where the claim itself is a float (a series, a root, an arctan). The Row is counterexample_rows.py's; the registry is counterexamples.py's."""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bands  # noqa: E402
import bell  # noqa: E402
import counterexample_forms as forms  # noqa: E402
import counterexample_rows as rows  # noqa: E402
import moving_clock  # noqa: E402
import paces  # noqa: E402
import rule3  # noqa: E402
import weak_field  # noqa: E402
from counterexample_rows import Row  # noqa: E402
from proofs_booking import check_the_booking_identity_of_the_hole, hole_form  # noqa: E402
from proofs_form import weighted_form  # noqa: E402
from proofs_ground import SEED, box_arrivals, pairs, read, step_integer  # noqa: E402

PORTS, AXES = rule3.PORTS, rule3.AXES
COMPUTED_PAIR, SMALL_GAP_PAIR = (2, 3), (999, 1000)
LIGHT = (1, 1)


def rest_rotation(num: int, den: int) -> float:
    return math.acos(rule3.plane_wave_dispersion(0.0, num, den))


def bands_inertia_and_kinetic_scale() -> Row:
    """Table 5 ('The band's inertia and kinetic scale, m* = 3 tan omega_0, c_m^2 = omega_0 / m*') and S.53 (E = m* c_m^2 = omega_0): m* read as 1 / omega''(0) from rule3's band by a finite difference equals 3 tan omega_0 at [2, 3], [9, 10] and [999, 1000]; c_m / c = 0.867 at [2, 3] and 1 as the gap closes; outside: at k = 2.5, near the band's top, no quadratic form fits (the departure above ten percent)."""
    fits, departs, witness = True, False, []
    for num, den in (COMPUTED_PAIR, (9, 10), SMALL_GAP_PAIR):
        omega_0 = rest_rotation(num, den)
        step = 1e-3
        curvature = 2 * (math.acos(rule3.plane_wave_dispersion(step, num, den)) - omega_0) / step**2
        inertia = bands.inertia_from_the_band(num, den)
        # the central difference at the step 1e-3 carries the band's k^4 term, 4 x 10^-5 of m* at the small gap
        fits &= abs(1 / curvature - inertia) < 1e-4 * inertia
        fits &= abs(inertia - 3 * math.tan(omega_0)) < 1e-9
        kinetic = omega_0 / inertia
        fits &= abs(inertia * kinetic - omega_0) < 1e-12
        speed_ratio = math.sqrt(kinetic / bands.light_speed_squared())
        witness.append(f"[{num}, {den}] m* {inertia:.4f} c_m / c {speed_ratio:.4f}")
        high = math.acos(rule3.plane_wave_dispersion(2.5, num, den)) - omega_0
        departs |= abs(high - 2.5**2 / (2 * inertia)) > 0.1 * high
    fits &= (
        round(
            math.sqrt(
                rest_rotation(2, 3) / bands.inertia_from_the_band(2, 3) / bands.light_speed_squared()
            ),
            3,
        )
        == 0.867
    )
    return Row(
        "tab:adds: The bands inertia and kinetic scale m 3tanomega0 cm2 omega0",
        fits,
        departs,
        "; ".join(witness) + "; no quadratic fit at k = 2.5",
    )


def ppn_parameters_against_kepler() -> Row:
    """Table 5 and S.19: with lambda = (1 + cos omega_0) / (2 cos omega_0) = (den + num) / (2 num), the bending 4 lambda U_K = (1 + gamma_K) 2 U_K gives gamma_K = den / num, the periapsis (2 - beta_K + 2 gamma_K) / 3 = lambda gives beta_K = (den + num) / (2 num), both exact rationals, and f lambda = tan omega_0 / omega_0 gives 1 + alpha_K: 1.5, 1.25, 1.329 at [2, 3] and 1.001, 1.0005, 1.00067 at [999, 1000] (the breaker text's 1.0000003 is a slip of the breaker's hand; the paper prints no such number). No condition to step outside of."""
    draw = random.Random(SEED)
    exact, printed = True, []
    for num, den in [COMPUTED_PAIR, SMALL_GAP_PAIR, *pairs(draw, 6, with_symmetric=False)]:
        if num == den:
            continue  # light has no rest rotation and no Kepler column
        scale = Fraction(den + num, 2 * num)
        gamma_k = 2 * scale - 1
        beta_k = 2 + 2 * gamma_k - 3 * scale
        exact &= gamma_k == Fraction(den, num) and beta_k == Fraction(den + num, 2 * num)
        omega_0 = rest_rotation(num, den)
        f = 2 * (1 - math.cos(omega_0)) / (omega_0 * math.sin(omega_0))
        one_plus_alpha = math.tan(omega_0) / omega_0
        exact &= abs(f * float(scale) - one_plus_alpha) < 1e-12
        if (num, den) in (COMPUTED_PAIR, SMALL_GAP_PAIR):
            printed.append(
                f"[{num}, {den}]: {float(gamma_k):.4g}, {float(beta_k):.5g}, {one_plus_alpha:.6g}"
            )
    kepler = weak_field.kepler_column(2, 3)
    exact &= [round(v, 3) for v in kepler[:3]] == [1.5, 1.25, 1.329]
    return Row(
        "tab:adds: The postNewtonian parameters with the gap for 0 num le den g",
        exact,
        None,
        "; ".join(printed),
    )


def series(coefficient: Fraction, order: int) -> list[Fraction]:
    """The Taylor coefficients of e^(coefficient U) up to the order, exact."""
    return [coefficient**n / math.factorial(n) for n in range(order + 1)]


def exponential_metric_ppn() -> Row:
    """Table 5 and S.34 (c): N^2 = e^(-2U) and h^2 = e^(2U) expanded exactly, g_00 = -(1 - 2U + 2U^2 - 4U^3 / 3), g_ij = (1 + 2U + 2U^2) delta_ij: gamma = 1 (the U coefficient of h^2 over 2), beta = 1 (the U^2 coefficient of -g_00 over 2), the spatial second order 2 against Schwarzschild's isotropic 1.5; the redshift's factor f(omega_0) = 1.063 at [2, 3]; outside: the clock's quadratic truncation (Gamma - c)^2 + c^2 differs from e^(-2U) at the third order by 4U^3 / 3 and the Link's (Gamma - 2c)^2 at the second by 4U^2 against 8U^2 (S.34 (e))."""
    lapse, ruler = series(Fraction(-2), 3), series(Fraction(2), 3)
    gamma_ppn, beta_ppn = ruler[1] / 2, lapse[2] / 2
    holds = lapse[:3] == [1, -2, 2] and ruler[:3] == [1, 2, 2] and gamma_ppn == 1 and beta_ppn == 1
    schwarzschild_isotropic = Fraction(3, 2)
    holds &= ruler[2] != schwarzschild_isotropic
    f = weak_field.redshift_factors(2, 3)[0]
    holds &= round(f, 3) == 1.063
    truncation_differs = (
        lapse[3] == Fraction(-4, 3) and [Fraction(1), Fraction(-2), Fraction(2), Fraction(0)] != lapse
    )
    link_differs = (
        series(Fraction(-4), 2)[2] == 8 and (1 - 2 * Fraction(1, 1)) ** 2 != 1 - 4 + 8
    )  # (1 - 2U)^2's U^2 coefficient is 4
    return Row(
        "tab:adds: Yilmazs exponential metric N2 e2U h2 e2U gamma beta 1 exactl",
        holds,
        truncation_differs and link_differs,
        f"g_00 coefficients {[str(c) for c in lapse]}, g_ij {[str(c) for c in ruler[:3]]}: gamma = beta = 1, spatial second order 2 vs 1.5; f(omega_0) = {f:.3f}; the truncations differ at U^3 (clock) and U^2 (Link)",
    )


def minimum_of(impact: Callable[[float], float], low: float, high: float) -> float:
    """The r in [low, high] where the impact parameter is least, by ternary search."""
    for _ in range(200):
        third = (high - low) / 3
        left, right = low + third, high - third
        low, high = (low, right) if impact(left) < impact(right) else (left, high)
    return (low + high) / 2


def shadow_capture_radius_is_2em() -> Row:
    """Section 8 and S.30: light's index n = e^(2U), U = m / r, keeps n r sin psi = b along a ray, so the circular ray stands where b(r) = r e^(2m / r) is least: at r = 2m, b = 2e m = 5.437 m against Schwarzschild's 3 sqrt 3 m = 5.196 m, 4.6 percent larger; outside the composed index: the quadratic index 1 / (1 - 2U) puts the minimum at r = 4m with b = 8m (+54 percent), which the Event Horizon Telescope excludes."""
    mass = 1.0
    radius = minimum_of(lambda r: r * math.exp(2 * mass / r), 1.01 * mass, 10 * mass)
    capture = radius * math.exp(2 * mass / radius)
    schwarzschild = 3 * math.sqrt(3) * mass
    holds = abs(radius - 2 * mass) < 1e-6 and abs(capture - 2 * math.e * mass) < 1e-9
    holds &= round((capture / schwarzschild - 1) * 100, 1) == 4.6
    grid = weak_field.shadow(mass)
    holds &= abs(grid[1] - capture) < 1e-4
    quadratic_radius = minimum_of(lambda r: r / (1 - 2 * mass / r), 2.5 * mass, 10 * mass)
    quadratic_capture = quadratic_radius / (1 - 2 * mass / quadratic_radius)
    breaks = abs(quadratic_radius - 4 * mass) < 1e-6 and abs(quadratic_capture - 8 * mass) < 1e-6
    return Row(
        "Lights index e2U places the photon sphere at r 2m with U m r",
        holds,
        breaks,
        f"r / m = {radius:.9f}, b / m = {capture:.4f} = 2e, Schwarzschild {schwarzschild:.4f}, +{(capture / schwarzschild - 1) * 100:.1f} percent; the quadratic index: r = {quadratic_radius:.3f} m, b = {quadratic_capture:.3f} m",
    )


def fall_coefficient_and_de_broglie() -> Row:
    """Table 1's row (S.18, S.22) and Section 8 (h): the slow packet's fall a = [2 nu (1 - nu) / (3 sin^2 omega_0)] |grad U| reduces by sin^2 omega_0 = 1 - nu^2 to 2 nu / (3 (1 + nu)) |grad U|, exactly rational, 4 / 15 at [2, 3] and 2 / 7 at [3, 4]; de Broglie's k = m* v holds at small k with a residual of the order k^2 (bands.de_broglie); outside: at k = 0.5 the residual stands at the percent level, and the fall differs between families at finite gaps (4 / 15 against 2 / 7), the equivalence between families reached only as the gaps close. The content's index of the same row is not tried here."""
    draw = random.Random(SEED)
    exact = True
    for num, den in [COMPUTED_PAIR, (3, 4), *pairs(draw, 6, with_symmetric=False)]:
        nu = Fraction(num, den)
        if nu == 1:
            continue
        exact &= 2 * nu * (1 - nu) / (3 * (1 - nu * nu)) == 2 * nu / (3 * (1 + nu))
    exact &= 2 * Fraction(2, 3) / (3 * (1 + Fraction(2, 3))) == Fraction(4, 15)
    exact &= 2 * Fraction(3, 4) / (3 * (1 + Fraction(3, 4))) == Fraction(2, 7)
    small, half = bands.de_broglie(2, 3, 0.02)[1], bands.de_broglie(2, 3, 0.01)[1]
    exact &= abs(small / half - 4) < 0.1  # the residual falls as k^2
    departure = bands.de_broglie(2, 3, 0.5)[1]
    return Row(
        "tab:results: De Broglie the fall Newtons pull the contents index for ever",
        exact,
        abs(departure) > 1e-3 and Fraction(4, 15) != Fraction(2, 7),
        f"fall 2 nu / (3 (1 + nu)) exact at 8 pairs, 4/15 at [2, 3], 2/7 at [3, 4]; de Broglie residual {half:.2e} at k = 0.01, {small:.2e} at 0.02, {departure:.4f} at 0.5; the fall family-dependent at finite gaps",
    )


def bells_478_over_169() -> Row:
    """Section 5.7 and S.10: at the declared integer settings (1, 0), (1, 1), (12, 5), (5, 12) on equal parts the four correlations are 119 / 169, -119 / 169, 120 / 169, 120 / 169 and S = 478 / 169 exactly, below 2 sqrt 2 because the angles are rational; the marginal P(A+) = (p^2 M_1^2 + q^2 M_2^2) / ((p^2 + q^2)(M_1^2 + M_2^2)) is 1 / 2 at equal parts for every setting; outside: unequal parts (1, 1) against (3, 1) give S = sqrt 2 (1 + rho), rho = 0.6, and the ideal irrational angles give 2 sqrt 2."""
    declared = bell.declared_pairs()
    holds = declared == [
        Fraction(119, 169),
        Fraction(-119, 169),
        Fraction(120, 169),
        Fraction(120, 169),
        Fraction(478, 169),
    ]
    holds &= float(declared[-1]) < 2 * math.sqrt(2)
    for p, q in (bell.SETTING_A, bell.SETTING_A_PRIME, bell.SETTING_B, bell.SETTING_B_PRIME):
        m_1, m_2 = Fraction(1, 2), Fraction(1, 2)
        holds &= (
            Fraction(p * p) * m_1**2 + Fraction(q * q) * m_2**2
            == Fraction(p * p + q * q) * (m_1**2 + m_2**2) / 2
        )
    settings = bell.angle_settings(bell.IDEAL_ANGLES)
    ideal = bell.chsh(settings, (1.0, 1.0))
    unequal = bell.chsh(settings, (1.0, 3.0))
    breaks = abs(ideal - 2 * math.sqrt(2)) < 1e-9 and abs(unequal - math.sqrt(2) * 1.6) < 1e-9
    return Row(
        "The declared pairs 478 169 sits below 2sqrt 2 because the an",
        holds,
        breaks,
        f"E = {', '.join(str(e) for e in declared[:4])}, S = {declared[-1]} = {float(declared[-1]):.5f} < {2 * math.sqrt(2):.5f}; marginals 1/2; ideal angles {ideal:.5f}; parts (1, 3): {unequal:.4f}",
    )


def ghz_mermin_minus_four() -> Row:
    """Section 9.4 and S.40: the credit on four lines at the GHZ settings gives E_3 = -1 on the three files with one x and +1 on (x, x, x), no pairwise correlation, Mermin's M = -4 exactly and a local assignment at most 2 (bell.ghz); outside the Mermin angles: a settings' triple off them gives |M| below 4."""
    found = bell.ghz()
    holds = found == [
        Fraction(-1),
        Fraction(-1),
        Fraction(-1),
        Fraction(1),
        Fraction(0),
        Fraction(-4),
        Fraction(2),
    ]
    y, off = (1, 1), (2, 1)
    mermin_off = (
        bell.ghz_correlations((off, y, y))[0]
        + bell.ghz_correlations((y, off, y))[0]
        + bell.ghz_correlations((y, y, off))[0]
        - bell.ghz_correlations((off, off, off))[0]
    )
    return Row(
        "The same credit on four lines gives the threequantum GHZ cor",
        holds,
        abs(mermin_off) < 4,
        f"E_3 on the four files {[str(e) for e in found[:4]]}, pairwise {found[4]}, M = {found[5]}, local at most {found[6]}; with a = (2, 1) in place of x: M = {mermin_off} = {float(mermin_off):.3f}",
    )


def clock_pace_is_the_exponential() -> Row:
    """Section 3.4, Eq. (3), S.34 (a): the clock composes, p_0(c + 1) = p_0(c)(1 - 1 / Gamma) exactly, so p_0 / Gamma = (1 - 1 / Gamma)^c = e^(-U)(1 + O(U / Gamma)) with U = c / Gamma, falling with the level (Newton's sign): at Gamma = 6,000 and c = 300 the relative departure from e^(-0.05) is 4 x 10^-6, U / (2 Gamma); outside the composition: the clock's quadratic truncation (Gamma - c)^2 + c^2 is another clock, differing from Gamma^2 e^(-2U) at the third order, 4U^3 / 3 (S.34 (e)); the breaker's 'plain read without hN = 1' is the Link's and not the clock's, not tried here."""
    gamma, content = 6000, 300
    composes = all(
        rule3.clock_pace(gamma, c + 1) == rule3.clock_pace(gamma, c) * (1 - Fraction(1, gamma))
        for c in range(0, 40, 7)
    )
    falls = all(rule3.clock_pace(gamma, c + 1) < rule3.clock_pace(gamma, c) for c in range(0, 40, 7))
    u = content / gamma
    departure = abs(float(rule3.clock_pace(gamma, content)) / gamma - math.exp(-u)) / math.exp(-u)
    holds = composes and falls and abs(departure / (u / (2 * gamma)) - 1) < 0.2
    quadratic = ((gamma - content) ** 2 + content**2) / gamma**2
    exponential = math.exp(-2 * u)
    third_order = abs((quadratic - exponential) / (4 * u**3 / 3) - 1) < 0.05
    return Row(
        "The level slows the clock by the potential Phi ell Gamma U w",
        holds,
        third_order,
        f"(1 - 1 / Gamma)^c against e^-U: relative {departure:.2e} (U / 2 Gamma = {u / (2 * gamma):.2e}); the quadratic clock differs by {quadratic - exponential:.2e} against 4U^3 / 3 = {4 * u**3 / 3:.2e}",
    )


def yukawa_reach_from_the_gap() -> Row:
    """Section 6.4 and S.11: a holder's rest outside its source, the line with next = before = now = a along one axis as lambda^x (lambda = e^(-kappa)) and uniform across, is exact iff num (lambda + 1 / lambda + 4) = 6 den, that is cosh kappa = 3 den / num - 2, checked on rule3's line at random rational lambda; R = 1 / kappa = 20.00 Links at [2400, 2401] and e^(-kappa) = 4 - sqrt 15 = 0.127 at [1, 2]; outside 0 < num <= den: at [-1, 2] the root lambda of lambda + 1 / lambda = -16 is negative, an alternating tail, and at [0, 1] the rest line forces a = 0 outside the source, no tail."""
    draw = random.Random(SEED)
    exact = True
    for _ in range(40):
        decay = Fraction(draw.randint(1, 20), draw.randint(21, 60))
        ratio = 6 / (decay + 1 / decay + 4)
        num, den = ratio.numerator, ratio.denominator
        amplitude = Fraction(draw.randint(1, 30))
        rest = rule3.step_exact(
            amplitude,
            amplitude,
            [amplitude * decay, amplitude / decay, amplitude, amplitude, amplitude, amplitude],
            num,
            den,
        )
        exact &= rest == amplitude and 0 < num <= den
        off = rule3.step_exact(
            amplitude,
            amplitude,
            [amplitude * decay, amplitude / decay, amplitude, amplitude, amplitude, amplitude],
            num + 1,
            den + 1,
        )
        exact &= off != amplitude
    reach = 1 / math.acosh(3 * 2401 / 2400 - 2)
    tail = 4 - math.sqrt(15)
    exact &= (
        round(reach, 2) == 20.00
        and round(tail, 3) == 0.127
        and abs(math.exp(-math.acosh(4)) - tail) < 1e-12
    )
    alternating = -8 + math.sqrt(63)
    negative_root = alternating < 0 and abs(alternating + 1 / alternating - (6 * 2 / -1 - 4)) < 1e-9
    no_tail = rule3.step_exact(5, 5, [5] * PORTS, 0, 1) == -5
    return Row(
        "tab:results: A holders reach from its gap Yukawas form",
        exact,
        negative_root and no_tail,
        f"the rest line exact at 40 rational lambda; R = {reach:.4f} at [2400, 2401]; e^-kappa = {tail:.4f} at [1, 2]; [-1, 2]: lambda = {alternating:.4f} < 0; [0, 1]: rest forces a = 0",
    )


def group_speed_along(
    direction: tuple[float, float, float],
    num: int,
    den: int,
    gamma: int,
    clock: float,
    links: tuple[float, float, float],
    k: float = 1e-3,
) -> float:
    """d omega / d|k| along the unit direction by a central difference on rule3.dispersion_at_paces."""

    def omega(size: float) -> float:
        return math.acos(
            rule3.dispersion_at_paces(tuple(size * n for n in direction), num, den, gamma, clock, links)
        )

    return (omega(1.5 * k) - omega(0.5 * k)) / k


def light_speed_and_dispersion() -> Row:
    """Table 1's row (S.1, S.12): light's group speed at long wavelength is 1 / sqrt 3 Links per interval along an axis, a face diagonal and the body diagonal alike; its dispersion along an axis is omega^2 = k^2 / 3 - k^4 / 54 + ..., and the phase speed falls to 0.392 at the zone's edge, omega(pi) / pi; outside the vacuum's pace: at a clock p_0 = N Gamma with p_a = p_0^2 / Gamma the speed is N^2 / sqrt 3."""
    light = 1 / math.sqrt(3)
    directions = {
        "axis": (1.0, 0.0, 0.0),
        "face diagonal": (1 / math.sqrt(2), 1 / math.sqrt(2), 0.0),
        "body diagonal": (1 / math.sqrt(3),) * 3,
    }
    speeds = {
        name: group_speed_along(n, *LIGHT, 1, 1, (1.0, 1.0, 1.0)) for name, n in directions.items()
    }
    holds = (
        all(abs(v - light) < 1e-5 for v in speeds.values())
        and abs(rule3.group_velocity(1e-3, *LIGHT) - light) < 1e-5
    )
    fourth = [
        (math.acos(rule3.plane_wave_dispersion(k, *LIGHT)) ** 2 - k * k / 3) / k**4
        for k in (0.05, 0.025)
    ]
    holds &= all(abs(c + 1 / 54) < 1e-3 for c in fourth)
    edge = math.acos(rule3.plane_wave_dispersion(math.pi, *LIGHT)) / math.pi
    holds &= round(edge, 3) == 0.392
    gamma, n = 100, 0.8
    slowed = group_speed_along(directions["axis"], *LIGHT, gamma, n * gamma, (n * n * gamma,) * 3)
    breaks = abs(slowed - n * n * light) < 1e-4 and abs(slowed - light) > 0.1
    return Row(
        "tab:results: Lights speed 1 sqrt 3 Links per interval its dispersion and",
        holds,
        breaks,
        f"speeds {', '.join(f'{k} {v:.6f}' for k, v in speeds.items())} vs 1 / sqrt 3 = {light:.6f}; k^4 coefficient {fourth[1]:.5f} (-1/54 = {-1 / 54:.5f}); edge {edge:.3f}; at N = 0.8: {slowed:.4f} = N^2 / sqrt 3",
    )


def moving_clock_fourth_order() -> Row:
    """Table 5's row, Section 8 (e), S.21: the interval of a free quantum is Lorentz's factor at c_m to the second order and at the fourth order carries omega_0 [(SUM_a n_a^4) tan omega_0 + cot omega_0]: 1.6926 along an axis, 1.2224 along a face diagonal, 1.0657 along the body diagonal at [2, 3], the axis's read on the exact band's inversion at v = 0.02 (moving_clock), c_m / c = 0.867, and 1 in every direction as the gap closes; outside: above the band's largest group speed (0.2501 Links per interval along an axis at [2, 3]) the inversion v(k) has no root."""
    factors = moving_clock.fourth_order_over_lorentz(2, 3)
    holds = [round(f, 4) for f in factors[:3]] == [1.6926, 1.2224, 1.0657] and abs(
        factors[3] - factors[0]
    ) < 0.01
    holds &= round(moving_clock.kinetic_scale(2, 3)[1], 3) == 0.867
    closing = moving_clock.fourth_order_over_lorentz(*SMALL_GAP_PAIR)[:3]
    holds &= all(abs(f - 1) < 2e-3 for f in closing)  # omega_0^2 = 0.002 there
    top = moving_clock.largest_group_speed(2, 3)[0]
    return Row(
        "tab:adds: The moving clocks fourth order omega0suma na4tanomega0 cotom",
        holds,
        top < 0.3,
        f"fourth order {[round(f, 4) for f in factors[:3]]}, the band's own {factors[3]:.4f}; at [999, 1000] {[round(f, 5) for f in closing]}; largest group speed {top:.4f}, no root above it",
    )


def half_up(value: Fraction) -> int:
    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def frozen_content_level() -> Row:
    """Table 5's row ('The frozen content U_f = (1 / 2) ln(2 Gamma), (Gamma / 2) ln 2 Gamma levels, 28,178 at Gamma = 6,000'): the Node's pace Gamma e^(-2U) falls under 1 / 2, the integer's rounding to 0, exactly at U_f = (1 / 2) ln(2 Gamma), 4.70 at Gamma = 6,000; the composed paces' own integers freeze at 28,206 levels (paces.frozen_content), 0.1 percent above the formula's 28,178, the formula being e^-U's to the unit; outside: one level under the frozen content the pace still rounds to one or more, the loader's admission (its refusal the engine's act, not tried here)."""
    gamma = 6000
    frozen_u = 0.5 * math.log(2 * gamma)
    formula_holds = abs(gamma * math.exp(-2 * frozen_u) - 0.5) < 1e-12
    exact_level, formula_level = paces.frozen_content(gamma)
    close = abs(exact_level - formula_level) / formula_level < 0.002 and round(formula_level) == 28178
    pace_under = half_up(rule3.clock_pace(gamma, int(exact_level) - 1)) ** 2 / gamma
    pace_at = half_up(rule3.clock_pace(gamma, int(exact_level))) ** 2 / gamma
    return Row(
        "tab:adds: The frozen content Uf tfrac12ln2Gamma Gamma 2ln 2Gamma level",
        formula_holds and close and pace_at < 0.5,
        pace_under >= 0.5,
        f"U_f = {frozen_u:.4f}; (Gamma / 2) ln 2 Gamma = {formula_level:.1f}; the composed integers freeze at {int(exact_level)} (the pace {pace_at:.3f} there, {pace_under:.3f} one level under)",
    )


def booking_identity_delta_q() -> Row:
    """Table 5's row and S.50: a face writing x in place of the level v the step would write at one Node, the leaving level b standing, changes the form by w (x - v)(x - b) at the line's v (proofs_booking's check), and at the integer step's v by w (x - v)(x - b) + (x - v)(r - r'), the remainders' term, exactly in integers at uniform paces and, over p_i^2, in the weighted form at uneven paces and tensions; the most one write removes is w (v - b)^2 / 4 at the midpoint. No condition to step outside of."""
    draw = random.Random(SEED)
    line_holds = check_the_booking_identity_of_the_hole()[0]
    integer_holds, weighted_holds = True, True
    for num, den in pairs(draw, 4):
        gamma = draw.randint(2, 9)
        pace = draw.randint(1, gamma)
        wall, reads, self_coefficient = rule3.coefficients(num, den, gamma, pace, (pace,) * AXES)
        arrivals = box_arrivals((2, 2, 2))
        now, before = rows.levels(draw, 8), rows.levels(draw, 8)
        remainders = [draw.randint(0, wall - 1) for _ in arrivals]
        stepped = [
            rule3.step(
                now[i],
                before[i],
                [now[j] for j in arrivals[i]],
                num,
                den,
                remainders[i],
                gamma,
                pace,
                (pace,) * AXES,
            )
            for i in range(8)
        ]
        integer, carried = [s[0] for s in stepped], [s[1] for s in stepped]
        node, x = draw.randrange(8), draw.randint(-60, 60)
        written = list(integer)
        written[node] = x
        change = hole_form(wall, reads[0], self_coefficient, arrivals, written, now) - hole_form(
            wall, reads[0], self_coefficient, arrivals, integer, now
        )
        integer_holds &= change == wall * (x - integer[node]) * (x - before[node]) + (
            x - integer[node]
        ) * (remainders[node] - carried[node])
        arrivals, clocks, factors = rows.uneven_board(draw, (3, 2, 2), gamma)
        wall_f, reads_f, selves, paces_f = read(arrivals, clocks, factors, num, den, gamma)
        now, before = rows.levels(draw, len(arrivals)), rows.levels(draw, len(arrivals))
        remainders = [draw.randint(0, int(wall_f) - 1) for _ in arrivals]
        integer, carried = step_integer(arrivals, reads_f, selves, wall_f, now, before, remainders)
        node = draw.randrange(len(arrivals))
        written = list(integer)
        written[node] = x
        change = weighted_form(
            reads_f, selves, wall_f, paces_f, arrivals, written, now, num, gamma
        ) - weighted_form(reads_f, selves, wall_f, paces_f, arrivals, integer, now, num, gamma)
        expected = (
            wall_f * (x - integer[node]) * (x - before[node])
            + (x - integer[node]) * (remainders[node] - carried[node])
        ) / paces_f[node] ** 2
        weighted_holds &= change == expected
    return Row(
        "tab:adds: The clicks booking identity Delta Q wx vx b with the records",
        line_holds and integer_holds and weighted_holds,
        None,
        "Delta Q = w (x - v)(x - b) at the line's v on three boards; + (x - v)(r - r') at the integer step's v, exact in integers at uniform paces and over p_i^2 at uneven paces, 4 pairs",
    )


def redshift_f_omega0() -> Row:
    """Table 1's row, S.15: a bound record's rest rotation at a clock p_0 = Gamma e^(-U) obeys 1 - cos omega_b = e^(-2U)(1 - cos omega_0) (rule3.dispersion_at_paces at k = 0), so its redshift z = (omega_0 - omega_b) / omega_0 is f(omega_0) U to the first order with f = 2 (1 - cos omega_0) / (omega_0 sin omega_0), 1.063 at [2, 3] and 1 as the gap closes, read on the rotation and not on the clock. No condition to step outside of."""
    holds, witness = True, []
    for num, den in (COMPUTED_PAIR, SMALL_GAP_PAIR):
        omega_0 = rest_rotation(num, den)
        f = weak_field.redshift_factors(num, den)[0]
        gamma = 6000.0
        slopes = []
        for u in (2e-3, 1e-3):
            clock = gamma * math.exp(-u)
            omega_b = math.acos(
                rule3.dispersion_at_paces(
                    (0.0, 0.0, 0.0), num, den, int(gamma), clock, (clock * clock / gamma,) * 3
                )
            )
            slopes.append((omega_0 - omega_b) / omega_0 / u)
        holds &= abs(slopes[1] - f) < 2e-3 * f and abs(slopes[1] - f) < abs(slopes[0] - f)
        witness.append(f"[{num}, {den}] f = {f:.4f}, z / U at U = 10^-3: {slopes[1]:.4f}")
    holds &= round(weak_field.redshift_factors(2, 3)[0], 3) == 1.063
    return Row("tab:results: The gravitational redshift z fomega0U", holds, None, "; ".join(witness))


def count_is_the_share() -> Row:
    """Table 1's row ('The count is the record's share; the rational total share is non-negative'): S.5's and S.6's breakers together, the share's change the six weighted currents plus the remainder term and the total share non-negative on closed and periodic boards at |num| <= den, each tested outside its fence in its own row."""
    change, total = (
        forms.shares_change_is_the_six_weighted_currents(),
        forms.total_share_nonnegative_inside_the_guard(),
    )
    return Row(
        "tab:results: The count is the records share the rational total share is n",
        change.holds_inside and total.holds_inside,
        bool(change.breaks_outside) and bool(total.breaks_outside),
        f"S.5: {change.witness}; S.6: {total.witness}",
    )
