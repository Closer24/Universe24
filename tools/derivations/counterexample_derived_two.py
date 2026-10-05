"""The breaker's second set of rows for the derived claims of the weak field and the constants (the method of 2026-10-04): the slow limit (S.63), the bending exact in the gap (S.20), the lens (S.28), the gravity of light (S.41 (2)), alpha's form from the write weight (S.26, S.54), the clusters' deceleration (S.29), the binding bound (S.38), Newton's pull and the two G (S.25), the two clocks (S.31, S.41 (1)), the push on a moving record (S.58), the two slits' minima (S.23), the Link's bound (S.24), the electron's gap (S.27), the preferred frame (S.35), the gapped kernel (S.39), the five carrier forms (S.36), the two forces (S.44), the nuclear threshold (S.45), the atom (S.46) and the Zeno curve (S.59). Each row is tried inside its stated condition and outside it; every number of the law is rule3.py's, every chain a derivation module's (weak_field, constants, bands, paces, bodies, greens_function, families, nuclear, atom, zeno, two_slits, frame, cosmology) or a proofs_ module's check; floats stand where the claim itself is a float. The Row is counterexample_rows.py's; the registry is counterexamples.py's."""

from __future__ import annotations

import cmath
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atom  # noqa: E402
import bodies  # noqa: E402
import constants  # noqa: E402
import cosmology  # noqa: E402
import families  # noqa: E402
import frame  # noqa: E402
import greens_function  # noqa: E402
import nuclear  # noqa: E402
import paces  # noqa: E402
import proofs_audit  # noqa: E402
import proofs_band  # noqa: E402
import proofs_bodies  # noqa: E402
import proofs_credit  # noqa: E402
import proofs_far_regime  # noqa: E402
import proofs_paces  # noqa: E402
import rule3  # noqa: E402
import two_slits  # noqa: E402
import weak_field  # noqa: E402
import zeno  # noqa: E402
from counterexample_rows import Row  # noqa: E402
from proofs_ground import SEED, angles, pairs  # noqa: E402

MATTER, SMALL_GAP, LIGHT = (2, 3), (999, 1000), (1, 1)
GAMMA = 6000


def rest_rotation(num: int, den: int) -> float:
    return math.acos(rule3.plane_wave_dispersion(0.0, num, den))


def packet_by_the_band(count: int, width: float, wave_number: float, num: int, den: int, interval: int):
    """A Gaussian packet of amplitude width `width` at k_0 on a periodic chain, laid as the sum of the chain's plane waves each at its own band rotation (rule3.plane_wave_dispersion), at the interval t: the exact two-level state of the line."""
    coefficients = []
    for mode in range(count):
        k = 2 * math.pi * mode / count
        k = k if k <= math.pi else k - 2 * math.pi
        amplitude = (
            sum(
                math.exp(-(((x - count / 4) / width) ** 2)) * cmath.exp(-1j * (k - wave_number) * x)
                for x in range(count)
            )
            / count
        )
        coefficients.append((k, amplitude))
    return [
        sum(
            a * cmath.exp(1j * (k * x - math.acos(rule3.plane_wave_dispersion(k, num, den)) * interval))
            for k, a in coefficients
        ).real
        for x in range(count)
    ]


def three_are_one_as_the_gap_closes() -> Row:
    """Section 3.3 ('Its slow limit at small wave number is Schroedinger's equation with the inertia m* = 3 tan omega_0 and the potential -omega_0 f(omega_0) U, the three conditions named') and S.63: the expansion identity exact and m* the band's (proofs_bodies' check); at k = 0.02 the band departs from Schroedinger's omega_0 + k^2 / (2 m*) by a relative k^2 / 12 of the kinetic term at [2, 3], [9, 10] and [999, 1000]; a Gaussian packet of width 16 Links at k_0 = 0.15 laid by the exact band on a chain of 400 and stepped 300 intervals by the line has its centre at Schroedinger's k_0 T / m* within two percent and its width a sqrt(1 + (T / (2 m* a^2))^2) within three (S.63's check at a smaller size); outside each condition's order: at k = 1 the dropped k^4 term is 1 / 12 of the k^2 (0.083), and the envelope's second difference against 2 sin omega_0 psi' is 1.0 for a packet one interval wide where it is 0.025 at forty."""
    identity = proofs_bodies.check_schroedingers_slow_limit()[0]
    departures, named = {}, True
    for num, den in (MATTER, (9, 10), SMALL_GAP):
        omega_0 = rest_rotation(num, den)
        inertia = 3 * math.tan(omega_0)
        k = 0.02
        band = math.acos(rule3.plane_wave_dispersion(k, num, den)) - omega_0
        kinetic = k * k / (2 * inertia)
        departures[(num, den)] = (band - kinetic) / kinetic
        orders = -(
            k * k / 12 + kinetic / (2 * math.tan(omega_0))
        )  # (ii) and (iii) of S.63 at their orders
        named &= abs(departures[(num, den)] / orders - 1) < 0.1
    count, width, k_0, steps = 400, 16.0, 0.15, 300
    num, den = MATTER
    now, before = (
        packet_by_the_band(count, width, k_0, num, den, 0),
        packet_by_the_band(count, width, k_0, num, den, -1),
    )
    arrivals = rule3.chain_arrivals(count)
    wall, reads, self_coefficient = rule3.coefficients(num, den)
    for _ in range(steps):
        now, before = (
            [
                rule3.numerator(now[i], [now[j] for j in arrivals[i]], reads, self_coefficient) / wall
                - before[i]
                for i in range(count)
            ],
            now,
        )
    nxt = [
        rule3.numerator(now[i], [now[j] for j in arrivals[i]], reads, self_coefficient) / wall
        - before[i]
        for i in range(count)
    ]
    density = [now[i] * now[i] - nxt[i] * before[i] for i in range(count)]
    total = sum(density)
    centre = sum(x * d for x, d in enumerate(density)) / total - count / 4
    spread = math.sqrt(sum((x - count / 4 - centre) ** 2 * d for x, d in enumerate(density)) / total)
    inertia = 3 * math.tan(rest_rotation(num, den))
    a = width / 2  # the density's rms at the lay, S.63's a, for the amplitude e^(-(x / width)^2)
    schroedinger_centre, schroedinger_width = (
        k_0 * steps / inertia,
        a * math.sqrt(1 + (steps / (2 * inertia * a * a)) ** 2),
    )
    packet = abs(centre / schroedinger_centre - 1) < 0.02 and abs(spread / schroedinger_width - 1) < 0.03
    fourth_at_one = ((1 - math.cos(1.0)) - 0.5) / 0.5
    sine = math.sin(rest_rotation(num, den))
    envelope_ratio = {tau: 3 / (4 * tau * sine) for tau in (40.0, 1.0)}
    return Row(
        "The three are one as the gap closes Its slow limit at small",
        identity and named and packet,
        abs(fourth_at_one + 1 / 12) < 5e-3 and envelope_ratio[1.0] > 0.5 and envelope_ratio[40.0] < 0.05,
        f"band less Schroedinger over the kinetic term at k = 0.02, each the sum of the two named orders k^2 / 12 and (omega - omega_0) / (2 tan omega_0) within ten percent: {', '.join(f'[{p[0]}, {p[1]}] {d:.1e}' for p, d in departures.items())}; the packet's centre {centre:.2f} against {schroedinger_centre:.2f}, its rms width {spread:.2f} against {schroedinger_width:.2f}; at k = 1 the k^4 term is {-fourth_at_one:.3f} of the k^2 (1 / 12 = 0.083); psi'' over 2 sin omega_0 psi': {envelope_ratio[40.0]:.3f} at forty intervals, {envelope_ratio[1.0]:.2f} at one",
    )


def bending_exact_in_the_gap() -> Row:
    """Section 8 ('Its bending is exact in the gap, while the orbit's second order at the computed pair carries the band's k^4 term'), Table 1's bending row, the clicks table's bending row and S.20: under the one assumption p_a = p_0^2 / Gamma light's index exponent is 2 (ln n / U from rule3's band at the composed paces), the ray's turn 4 U_b (the transverse integral 2 / b, proofs_paces), Shapiro's gamma = 1 and the perihelion's (2 - beta_K + 2 gamma_K) / 3 = (den + num) / (2 num), which with 4 lambda U_K = 2 (1 + den / num) U_K makes the bending 4 U_b at every pair exactly in rationals; the exponential metric's spatial second order 2 against Schwarzschild's 1.5; the band's k^4 over k^2 at [2, 3] 1 / (12 sin^2 omega_0) = 0.15 (the orbit's share, 13 to 17 percent in S.19, not re-run); outside the assumption: the plain read p_a = p_0 gives the index exponent 1 and the bending 2 U_b."""
    draw = random.Random(SEED)
    exponent = weak_field.light_index_exponent()[0]
    turn = weak_field.bending()[0]
    shapiro = weak_field.shapiro_gamma()[1]
    integrals = proofs_paces.check_the_bending_and_shapiros_integrals()[0]
    exact = True
    for num, den in pairs(draw, 8, with_symmetric=False) + [MATTER, SMALL_GAP]:
        lam = Fraction(den + num, 2 * num)
        gamma_k, beta_k = Fraction(den, num), Fraction(den + num, 2 * num)
        exact &= (2 - beta_k + 2 * gamma_k) / 3 == lam and 4 * lam == 2 * (1 + gamma_k)
    second_order = proofs_paces.check_the_exponential_metrics_post_newtonian_orders()[0]
    fourth_over_second = 1 / (12 * math.sin(rest_rotation(*MATTER)) ** 2)
    gamma, u, k = GAMMA, 0.05, 1e-3
    clock = gamma * math.exp(-u)
    vacuum = math.acos(rule3.dispersion_at_paces((k, 0.0, 0.0), *LIGHT, gamma, gamma, (gamma,) * 3))
    plain = math.acos(rule3.dispersion_at_paces((k, 0.0, 0.0), *LIGHT, gamma, clock, (clock,) * 3))
    plain_exponent = math.log(vacuum / plain) / u
    return Row(
        "Its bending is exact in the gap while the orbits second orde",
        abs(exponent - 2) < 1e-6
        and abs(turn - 4) < 1e-3
        and abs(shapiro - 1) < 1e-3
        and integrals
        and exact
        and second_order,
        abs(plain_exponent - 1) < 1e-6,
        f"index exponent {exponent:.6f}, the turn's coefficient {turn:.4f}, Shapiro's gamma {shapiro:.4f}; 4 lambda U_K = 2 (1 + den / num) U_K exact at 10 pairs; k^4 over k^2 at [2, 3]: {fourth_over_second:.3f}; the plain read's exponent {plain_exponent:.6f}, the bending 2 U_b",
    )


def lens_one_formula_for_light_and_matter() -> Row:
    """Section 8 (p) ('The lens: a content bends light and matter alike by one formula'), Table 5's lens row and S.28: 1 - cos k_in = [1 - cos k + 3 (den - num) (1 - N^2) / num] / N^4 equals rule3's band at the composed paces exactly in rationals at random pairs, N and cos k; for light sin(k_in / 2) = sin(k / 2) / N^2 exactly; light's phase index k_in / k is e^(2U) as k -> 0 and the chromatic term k^2 (e^(6U) - e^(2U)) / 24 (weak_field.lens); slow matter's n_m^2 k^2 is constant at long wavelength (the 1 / k^2 index); outside light's reduction: matter at [2, 3], k = 0.3, N = 0.9 has k_in = 1.0500 by the general equation against 0.3711 by the light reduction, the rest term of matter."""
    draw = random.Random(SEED)
    exact, light_exact = True, True
    for num, den in pairs(draw, 6):
        for _ in range(4):
            n = Fraction(draw.randint(1, 20), 20)
            cos_k = angles(draw, 8)[7].re
            inside = 1 - (1 - cos_k + 3 * (den - num) * (1 - n * n) / num) / n**4
            gamma = 12
            wall, reads, self_coefficient = rule3.coefficients(
                num, den, gamma, gamma * n, (gamma * n * n,) * 3
            )
            band_inside = (self_coefficient + 2 * reads[0] * inside + 2 * reads[1] + 2 * reads[2]) / (
                2 * wall
            )
            exact &= band_inside == Fraction(num, 3 * den) * (2 + cos_k)
            if num == den:
                light_exact &= (1 - inside) / 2 == (1 - cos_k) / 2 / n**4
    residual, index_ratio, divisor = weak_field.lens(1, 1, 0.1, 0.3)
    u, n = 0.1, math.exp(-0.1)
    matter_index = []
    for k in (0.01, 0.005):
        k_in = math.acos(1 - (1 - math.cos(k) + 3 * 1 * (1 - n * n) / 2) / n**4)
        matter_index.append((k_in / k) ** 2 * k * k)
    one_over_k_squared = abs(matter_index[0] / matter_index[1] - 1) < 1e-3
    chromatic = []
    for k in (0.3, 0.6, 0.9):
        exact_index = 2 * math.asin(math.sin(k / 2) / n**2) / k
        chromatic.append(
            (exact_index - math.exp(2 * u), k * k * (math.exp(6 * u) - math.exp(2 * u)) / 24)
        )
    k, n_point_nine = 0.3, 0.9
    general = math.acos(1 - (1 - math.cos(k) + 3 * 1 * (1 - n_point_nine**2) / 2) / n_point_nine**4)
    reduction = 2 * math.asin(math.sin(k / 2) / n_point_nine**2)
    return Row(
        "itemp The lens a content bends light and matter alike by one",
        exact
        and light_exact
        and abs(residual) < 1e-12
        and abs(index_ratio - 1) < 1e-6
        and abs(divisor - 24) < 0.3
        and one_over_k_squared,
        round(general, 4) == 1.05 and abs(reduction - 0.3711) < 1e-3,
        f"the general equation the band at the composed paces, exact over 6 pairs x 4; light's reduction exact; index / e^2U = {index_ratio:.7f}, chromatic divisor {divisor:.2f}; n_m^2 k^2 constant to {abs(matter_index[0] / matter_index[1] - 1):.1e}; chromatic term at k = 0.3, 0.6, 0.9: {', '.join(f'{a:.4f} vs {b:.4f}' for a, b in chromatic)}; matter at k = 0.3, N = 0.9: k_in {general:.4f} against the light reduction's {reduction:.4f}",
    )


def gravity_of_light_factor_one() -> Row:
    """Table 5's row ('The gravity of light: a light packet's integrated write at 1 x E / c^2, against general relativity's 2'), S.41 (2): on a chain of 16 a travelling light wave at k = pi / 4 at rule3's rotation has D = now^2 - next x before = A^2 sin^2 omega at every Node and interval to 10^-9 (the line's next), as a resting matter record has A^2 sin^2 omega_0, so the write per quantum (D over 2 A^2 sin omega) is the same for the travelling and the resting record, the factor 1 against 2 (weak_field.gravity_of_light); outside the conserved form: the plain read now^2 writes A^2 / 2 per Node for the travelling wave and A^2 cos^2(omega_0 t) for the resting one, their ratio 1 / 2 at t = 0 and unbounded at a quarter period, another factor. The travelling wave of light at a Pythagorean k has no Pythagorean omega on light's band (x^2 + 24 y^2 = 3 z^2 has no rational point), so this row stands in floats."""
    count, k = 16, math.pi / 4
    num, den = LIGHT
    omega = math.acos(rule3.plane_wave_dispersion(k, num, den))
    arrivals = rule3.chain_arrivals(count)
    wall, reads, self_coefficient = rule3.coefficients(num, den)
    amplitude = 3.0
    worst = 0.0
    plain_travelling = 0.0
    for t in range(12):
        now = [amplitude * math.cos(k * x - omega * t) for x in range(count)]
        before = [amplitude * math.cos(k * x - omega * (t - 1)) for x in range(count)]
        nxt = [
            rule3.numerator(now[i], [now[j] for j in arrivals[i]], reads, self_coefficient) / wall
            - before[i]
            for i in range(count)
        ]
        worst = max(
            worst,
            max(
                abs(now[i] ** 2 - nxt[i] * before[i] - amplitude**2 * math.sin(omega) ** 2)
                for i in range(count)
            ),
        )
        plain_travelling = sum(v * v for v in now) / count
    omega_0 = rest_rotation(*MATTER)
    resting = [amplitude * math.cos(omega_0 * t) for t in (-1, 0, 1)]
    resting_form = resting[1] ** 2 - resting[2] * resting[0]
    # the write per quantum: D over the family's own quantum form T sin omega, with one quantum laid at 2 A^2 sin omega = T (rows 13 and 17)
    travelling_write = (
        amplitude**2 * math.sin(omega) ** 2 / ((2 * amplitude**2 * math.sin(omega)) * math.sin(omega))
    )
    resting_write = resting_form / ((2 * amplitude**2 * math.sin(omega_0)) * math.sin(omega_0))
    factor = travelling_write / resting_write
    chain = weak_field.gravity_of_light()
    plain_ratio = plain_travelling / resting[1] ** 2
    return Row(
        "tab:adds: The gravity of light a light packets integrated write at 1 t",
        worst < 1e-9 and abs(factor - 1) < 1e-12 and abs(chain[0] - 1) < 1e-9 and chain[1] == 2,
        abs(plain_ratio - 0.5) < 1e-12,
        f"D = A^2 sin^2 omega at every Node over 12 intervals to {worst:.1e}; the write per quantum travelling over resting {factor:.12f} (weak_field's {chain[0]:.9f}), general relativity's {chain[1]}; the plain read now^2: travelling over resting {plain_ratio:.3f} at t = 0",
    )


def alpha_laws_form_from_the_write_weight() -> Row:
    """Table 5's row ('The fine-structure constant's form alpha = (3 sqrt 3 / 8 pi) k / (Gamma E_s), k the declared write weight; k / (Gamma E_s) = 1 / 28.33 at nature's alpha'), Table 1's alpha row, S.26 and S.54: the prefactor from rule3's rest line (w / R = 3 at [1, 1]), the far kernel 1 / (4 pi), one quantum's Wronskian T / 2 for every family (units.lay_squared at [999, 1000], [1, 2], [2, 3] to the root's rounding) and light's c = 1 / sqrt 3 is 0.20675 (constants.alpha_law); 137.036 x 0.20675 = 28.33, no integer Gamma E_s at k = 1 (28 and 29 give 135.43 and 140.27); the calibration series 28.33, 1, 0; the energy line's ratio 1 at the charged universe's integers; outside the count's lay: a record laid by share writes 1 / (2 sin omega_0) = 0.6708 at [2, 3], the gap in alpha; and the energy read as T omega instead of T sin omega moves the energy line's ratio to 1 / cos omega_s = 1.5 at [2, 3]."""
    prefactor, cancels = constants.alpha_law()
    wronskians = [constants.wronskian_per_quantum(*pair) for pair in (SMALL_GAP, (1, 2), MATTER)]
    numbers = proofs_far_regime.check_newtons_constant_and_alpha_laws_numbers()[0]
    series = [round(v, 2) for v in constants.calibration_series()]
    line = constants.energy_line()
    omega_0 = rest_rotation(*MATTER)
    by_share = 1 / (2 * math.sin(omega_0))
    as_frequency = line[0] / math.cos(
        omega_0
    )  # T omega's derivative T against T cos omega: the ratio 1 / cos omega_s
    return Row(
        "tab:adds: The finestructure constants form alpha 3sqrt 3 8pik Gamma Es",
        abs(prefactor - 3 * math.sqrt(3) / (8 * math.pi)) < 1e-12
        and all(abs(w - 0.5) < 1e-4 for w in wronskians)
        and abs(cancels - 1) < 1e-4
        and numbers
        and series == [28.33, 1.0, 0.0]
        and abs(line[0] - 1) < 1e-5,
        round(by_share, 4) == 0.6708 and abs(as_frequency - 1.5) < 1e-5,
        f"prefactor {prefactor:.5f}; W / T = {', '.join(f'{w:.5f}' for w in wronskians)} at [999, 1000], [1, 2], [2, 3]; 137.036 x 0.20675 = {series[0]}; the energy line's ratio {line[0]:.6f}; laid by share {by_share:.4f}; the energy read as T omega: {as_frequency:.4f}",
    )


def clusters_deceleration() -> Row:
    """Table 5's row ('The clusters' deceleration q_0 = Omega_m / 2 > 0 at z << 1, bound or free') and S.29: for a shell with a'' = -mu / a^2 the deceleration q = -a a'' / a'^2 = mu / (a a'^2) and Omega_m = 2 mu / (a a'^2), so q = Omega_m / 2 exactly in rationals, positive for a bound ball (a'^2 < 2 mu / a) and a free one alike; Hubble's law for a homologous ball, v = (a' / a) r at every shell exactly; Friedmann's invariant and the Doppler form proofs_far_regime's check; outside the law's forms: a vacuum write Lambda, q_0 = Omega_m / 2 - Omega_Lambda = -0.55 at (0.3, 0.7), the sign turned by a declaration (cosmology.deceleration)."""
    draw = random.Random(SEED)
    exact, both_signs = True, {"bound": False, "free": False}
    for _ in range(40):
        mu, a = (
            Fraction(draw.randint(1, 20), draw.randint(1, 5)),
            Fraction(draw.randint(1, 20), draw.randint(1, 5)),
        )
        speed = Fraction(draw.randint(1, 30), draw.randint(1, 5))
        deceleration = (mu / (a * a)) * a / (speed * speed)
        omega_m = 2 * mu / (a * speed * speed)
        exact &= deceleration == omega_m / 2 and deceleration > 0
        both_signs["bound" if speed * speed < 2 * mu / a else "free"] = True
        shells = [
            Fraction(draw.randint(1, 9), 3) for _ in range(3)
        ]  # the shells' comoving radii x_i, r_i = x_i a
        exact &= all((x * speed) == (speed / a) * (x * a) for x in shells)
    friedmann = proofs_far_regime.check_friedmanns_dust_equations_and_the_redshift()[0]
    with_vacuum = cosmology.deceleration(0.3, 0.7)
    return Row(
        "tab:adds: The clusters deceleration q0 Omegam 2 0 at z ll 1 bound or f",
        exact and all(both_signs.values()) and friedmann,
        with_vacuum[1] < 0 and round(with_vacuum[0], 2) == 0.15,
        f"q = Omega_m / 2 exact at 40 rational (mu, a, a') with bound and free balls, Hubble's law exact; q_0 = {with_vacuum[0]:.2f} at Omega_m = 0.3 and {with_vacuum[1]:.2f} with Omega_Lambda = 0.7",
    )


def binding_bound_by_watsons_integral() -> Row:
    """Table 5's row ('A body's binding per quantum is bounded by 0.76 C W / (Gamma E) at one Node and is about 0.29 C W / (Gamma E r) for a uniform ball of r Links, 0.36 at its centre') and S.38: 3 G(0) = 0.7582 by Watson's closed form (bodies) and by the lattice's Fourier sum (greens_function) alike; G(r) <= G(0) at r = 0 to 5, so a body's self-level at any Node is at most 3 G(0) C W / (Gamma E), attained by one quantum on one Node; the uniform ball's factors 1.5 and 1.2 give 0.36 and 0.29 per r; the deuteron's 1.2 x 10^-3 and iron's 9 x 10^-3 need C W / (Gamma E r) of 4 x 10^-3 and 3 x 10^-2, the miss named; a bound states no condition to step outside of."""
    closed, lattice = 3 * bodies.watson_green_at_the_source(), greens_function.three_g()[0]
    green = greens_function.green()
    monotone = all(green[0] >= g > 0 for g in green)
    bound = bodies.binding_bound()
    one_node = 3 * bodies.watson_green_at_the_source() * 1  # C = 1 on one Node: the bound attained
    ball = bound[1] * 1000 / 5  # 1,000 quanta over a ball of 5 Links, per C W / (Gamma E): 0.29 C / r
    needs = (1.2e-3 / bound[1], 9e-3 / bound[1])
    return Row(
        "tab:adds: A bodys binding per quantum bounded by 076CW Gamma E at one",
        abs(closed - lattice) < 1e-6
        and round(closed, 4) == 0.7582
        and monotone
        and [round(v, 2) for v in bound] == [0.76, 0.29, 0.36]
        and ball < one_node * 1000,
        None,
        f"3 G(0) = {closed:.4f} (closed) and {lattice:.4f} (lattice); G(r) falls from G(0) over r = 0 to 5; the ball's 1.2 and 1.5 give {bound[1]:.2f} and {bound[2]:.2f} per r; a body of 1,000 quanta over 5 Links at {ball:.0f} against the bound {one_node * 1000:.0f}; the deuteron and iron need C W / (Gamma E r) of {needs[0]:.1e} and {needs[1]:.1e}",
    )


def newtons_pull_and_the_two_g() -> Row:
    """Table 1's row ('Newton's pull, the clock's G and Kepler's G') and S.25: G_clock Gamma E_g = 1 / (4 pi) from the rest line's w / R = 3 at [1, 1] (rule3.coefficients, exact), the far kernel 3 / (4 pi r) and c^2 = R / w = 1 / 3; 4 pi r G(r) = 1.012 at r = 5 on the lattice toward the continuum's 1; the far kernel's powers 2 and 1 (Newton's pull and Kepler's v^2); Kepler's G is [2 cos omega_0 / (1 + cos omega_0)] G_clock, 4 / 5 at [2, 3] exactly and 1998 / 1999 at [999, 1000], 1 as the gap closes; a circular orbit's r^3 / T^2 = G M / (4 pi^2) at every radius, Kepler's third law, exact with pi as a symbol. No condition to step outside of (the breaker text's 'f(omega_0) apart' is U_K / U = 0.8 in the paper, not f = 1.063)."""
    wall, reads, _ = rule3.coefficients(*LIGHT)
    three, light_squared = Fraction(wall, reads[0]), Fraction(reads[0], wall)
    g_clock = (
        light_squared * three / 4
    )  # G_clock Gamma E_g times pi, from G / c^2 = 3 / (4 pi Gamma E_g) (S.25): 1 / 4
    newton = constants.newton_constant()
    far = greens_function.four_pi_r_g()[-1]
    powers = [round(v, 3) for v in weak_field.newton_powers()]
    ratios = {pair: Fraction(2 * pair[0], pair[0] + pair[1]) for pair in (MATTER, SMALL_GAP)}
    kepler = constants.kepler_factor()
    mass_product = Fraction(7)  # G M, a symbol; pi^2 another, cancelling in the ratio below
    third_law = all(
        Fraction(r**3) / (4 * Fraction(r) ** 3 / mass_product) == mass_product / 4 for r in (1, 2, 3)
    )  # v^2 = G M / r gives T^2 = 4 pi^2 r^3 / (G M), so r^3 / T^2 = G M / (4 pi^2) at every radius
    return Row(
        "tab:results: Newtons pull the clocks G and Keplers G",
        three == 3
        and light_squared == Fraction(1, 3)
        and g_clock == Fraction(1, 4)
        and abs(newton[3] - 1 / (4 * math.pi)) < 1e-12
        and abs(far - 1.012) < 1e-3
        and powers == [2.0, 1.0]
        and ratios[MATTER] == Fraction(4, 5)
        and round(kepler[1], 3) == 0.8
        and third_law,
        None,
        f"w / R = {three}, c^2 = {light_squared}, G_clock Gamma E_g = 1 / (4 pi); 4 pi r G(r) = {far:.3f} at r = 5; powers {powers}; G_K / G_clock = {ratios[MATTER]} at [2, 3], {ratios[SMALL_GAP]} at [999, 1000]; Kepler's third law exact",
    )


def two_clocks_shift_alike() -> Row:
    """Table 1's row ('The two clocks shift alike'), the clicks table's clock rate row, S.31 and S.41 (1): every family's rest at the composed paces has 1 - cos omega_b = N^2 (1 - cos omega_0) exactly in rationals (rule3.coefficients at p_0 = Gamma N, p_a = Gamma N^2), so the Node's clock and a body's beat shift alike in 2 sin(omega / 2); in omega the rest line's rate is -2 tan(omega_0 / 2) / omega_0 = -f(omega_0), 1.0634 at [2, 3], the clock's click rate 1 - f(omega_0) U; the beat Delta' = N Delta [1 - (1 - N^2)(omega_1^2 + omega_1 omega_2 + omega_2^2) / 24] at N = 0.8: 0.3916 exact against 0.4 and the series 0.3920 (paces.two_clocks), the correction's order 5 (proofs_paces); outside the bodies: a cavity of declared faces, a NodeDetector's region and no body, intervals at N^2 against the bodies' N (0.64 against 0.8); the plain read p_a = p_0 moves nothing of the rest's factor N here, so it is no breaker of this row (a note for the hands)."""
    draw = random.Random(SEED)
    exact = True
    for num, den in pairs(draw, 8):
        for _ in range(3):
            n = Fraction(draw.randint(1, 30), 30)
            gamma = 30
            wall, reads, self_coefficient = rule3.coefficients(
                num, den, gamma, gamma * n, (gamma * n * n,) * 3
            )
            rest = (self_coefficient + 2 * sum(reads)) / (2 * wall)
            exact &= 1 - rest == n * n * (1 - Fraction(num, den))
            wall_p, reads_p, self_p = rule3.coefficients(num, den, gamma, gamma * n, (gamma * n,) * 3)
            exact &= 1 - (self_p + 2 * sum(reads_p)) / (2 * wall_p) == n * n * (
                1 - Fraction(num, den)
            )  # the plain read: the rest's factor the same
    omega_0 = rest_rotation(*MATTER)
    rate = 2 * math.tan(omega_0 / 2) / omega_0
    f = weak_field.redshift_factors(*MATTER)[0]
    beat = [round(v, 4) for v in paces.two_clocks()]
    series = proofs_paces.check_the_two_clocks_under_the_principle()[0]
    return Row(
        "tab:results: The two clocks shift alike the findings against nature of Se",
        exact
        and abs(rate - f) < 1e-12
        and round(f, 4) == 1.0634
        and beat[:3] == [0.3916, 0.4, 0.392]
        and series,
        beat[3] != beat[4],
        f"1 - cos omega_b = N^2 (1 - cos omega_0) exact at 8 pairs x 3 N (under the plain read too); -2 tan(omega_0 / 2) / omega_0 = f = {f:.4f}; the beat {beat[0]} against N Delta {beat[1]} and the series {beat[2]}; a cavity of bodies at {beat[3]}, of declared faces at {beat[4]}",
    )


def push_on_a_moving_record() -> Row:
    """S.58 (Eq. (16)): on the exact band at [2, 3] the rest push over E is f(omega_0) = 1.0634 and the coefficient of beta^2 is 1.3354 = gamma_K - alpha_K / 2, at [999, 1000] 1.00017 and 1.00067 (proofs_paces' check, weak_field.push_on_a_moving_record); the covariant form E (1 + beta^2) at beta = 1 is twice the rest push, the bending 4 U_b; outside the small gap: at [2, 3] the beta^2 coefficient parts from the covariant form's 1 by 0.335, the quadratic band's own term, closing as the gap does."""
    held = proofs_paces.check_the_push_on_a_moving_record()[0]
    push = weak_field.push_on_a_moving_record()
    at_beta_one = 1 + 1**2
    return Row(
        "S.58",
        held
        and round(push[0], 4) == 1.0634
        and round(push[1], 4) == 1.3354
        and round(push[2], 5) == 1.00017
        and round(push[3], 5) == 1.00067
        and at_beta_one == 2,
        abs(push[1] - 1) > 0.3 and abs(push[3] - 1) < 1e-3,
        f"rest push {push[0]:.4f}, beta^2 coefficient {push[1]:.4f} at [2, 3]; {push[2]:.5f}, {push[3]:.5f} at [999, 1000]; the covariant form's 1 missed by {push[1] - 1:.3f} at the computed pair",
    )


def near_field_minima_of_the_two_slits() -> Row:
    """S.23 (Section 9.2): the near-field minima of the declared file solve sqrt(L^2 + (y - 18)^2) - sqrt(L^2 + (y - 30)^2) = +-4 at y = 24 +- 2 sqrt 19 (with u = y - 24 and u^2 = 76 the two roots are 2 + 3u and 3u - 2 exactly), the rows 15.28 and 32.72 in the regions 3 and 8, the far-field spacing lambda L / d = 16 (two_slits.near_field_minima); the Huygens per-Node sum against expectation.json is a run's file and is not re-run. No condition to step outside of."""
    found = two_slits.near_field_minima()
    roots = (24 - 2 * math.sqrt(19), 24 + 2 * math.sqrt(19))
    u_squared = Fraction(
        76
    )  # (u + 6)^2 + 576 = 688 + 12 u = (2 + 3 u)^2 and (u - 6)^2 + 576 = 688 - 12 u = (3 u - 2)^2 with u^2 = 76
    exact = 4 + 9 * u_squared == 688 and 2 * 2 * 3 == 12 and (2 + 3 * 1) - (3 * 1 - 2) == 4
    in_floats = all(
        abs(two_slits.path_difference(r) - s) < 1e-12 for r, s in zip(roots, (-4.0, 4.0), strict=True)
    )
    return Row(
        "S.23",
        [round(v, 2) for v in found] == [16.0, 15.28, 32.72, 3.0, 8.0, 24.0, 23.5]
        and exact
        and in_floats
        and all(abs(a - b) < 1e-9 for a, b in zip(found[1:3], roots, strict=True)),
        None,
        f"the minima at {found[1]:.4f} and {found[2]:.4f} = 24 -+ 2 sqrt 19, the regions {int(found[3])} and {int(found[4])}, the spacing {found[0]:.0f}; the roots exact in rationals through (2 + 3u)^2 = 688 + 12u at u^2 = 76",
    )


def links_bound_from_the_dispersion() -> Row:
    """S.24 (Section 10.2): the Link's bound from MAGIC's quadratic limit, k < 6.7 x 10^-8 per Link at 1 TeV, the Link below 1.3 x 10^-26 m along an axis and 2.1 x 10^-26 averaged, omega_e < 2.0 x 10^-14 and gamma_K - 1 < 2.0 x 10^-28 (proofs_paces' check, constants.link_bound), the band's k^4 coefficient -1 / 54 on an axis, -1 / 135 averaged, 0 on the body diagonal (proofs_band); outside the quadratic form: the band is even in k exactly (rule3's coefficients share one R_a per axis), so a linear or cubic dispersion bound has no coefficient to bind, the stated 'weaker by a factor' being no term of the band (a note for the hands)."""
    numbers = proofs_paces.check_the_bounds_from_the_photon_and_the_dispersion()[0]
    fourth = proofs_band.check_the_fourth_order_of_lights_band()[0]
    bound = [round(v, 1) for v in constants.link_bound()]
    even = all(
        rule3.dispersion_at_paces((k, 0.0, 0.0), *LIGHT, 1, 1, (1, 1, 1))
        == rule3.dispersion_at_paces((-k, 0.0, 0.0), *LIGHT, 1, 1, (1, 1, 1))
        for k in (0.1, 0.7, 2.0)
    )
    odd_coefficient = (
        math.acos(rule3.plane_wave_dispersion(0.1, *LIGHT))
        - math.acos(rule3.plane_wave_dispersion(-0.1, *LIGHT))
    ) / 0.1**3
    return Row(
        "S.24",
        numbers and fourth and bound == [2.0, 3.1, 2.0, 4.9, 4.0],
        even and abs(odd_coefficient) < 1e-12,
        f"omega_e bound {bound[0]} and {bound[1]} x 10^-14 (axis, averaged), gamma_K - 1 {bound[2]} and {bound[3]} x 10^-28; the band even in k, its odd coefficient {odd_coefficient:.1e}: no cubic bound",
    )


def electron_as_the_free_matter_quantum() -> Row:
    """S.27 (Section 10.1): den = d / (1 - cos omega_0) with d = den - num exactly, about 2 d / omega_0^2; at [999, 1001] d = 2 and 2 d / omega_0^2 = 1000.7 against den = 1001, the bound at d = 1 half of it, 500.3; a 1.4 PeV photon read as a share T sin omega gives sin omega_0 <= 3.65 x 10^-10, den > 1.5 x 10^19 and gamma_K - 1 < 6.7 x 10^-20 (proofs_paces' check); outside the share's reading: the frequency read as the energy T omega gives the other bound, pi times slacker on the diagonal (1.1 x 10^-9) and 1.231 times on an axis (4.5 x 10^-10)."""
    exact = all(
        Fraction(den - num) / (1 - Fraction(num, den)) == den
        for num, den in ((999, 1001), (2, 3), (4000, 6000))
    )
    omega = rest_rotation(999, 1001)
    two_d, one_d = 4 / omega**2, 2 / omega**2
    numbers = proofs_paces.check_the_bounds_from_the_photon_and_the_dispersion()[0]
    sine_bound = 0.511e6 / 1.4e15
    diagonal_top, axis_top = math.pi, math.acos(rule3.plane_wave_dispersion(math.pi, *LIGHT))
    as_frequency = (sine_bound * diagonal_top, sine_bound * axis_top)
    return Row(
        "S.27",
        exact and round(two_d, 1) == 1000.7 and round(one_d, 1) == 500.3 and numbers,
        f"{as_frequency[0]:.1e}" == "1.1e-09" and f"{as_frequency[1]:.1e}" == "4.5e-10",
        f"den = d / (1 - cos omega_0) exact; 2 d / omega_0^2 = {two_d:.1f} against 1001 at d = 2, {one_d:.1f} at d = 1; sin omega_0 <= {sine_bound:.2e}; read as T omega: {as_frequency[0]:.1e} (diagonal), {as_frequency[1]:.1e} (axis)",
    )


def preferred_frame_parameter() -> Row:
    """S.35 (Section 10.3): a metric diagonal in the lattice's frame has 4 gamma + 4 + alpha_1 = 0, alpha_1 = -8 at gamma = 1, alpha_2 = -1 in the standard gauge and the frame dragging 0 (frame.preferred_frame_parameters, proofs_paces' check); the band is even in every k_a at the composed paces, no g_0a (frame.no_cross_terms); the miss against nature is named and has no breaker beyond the arithmetic."""
    held = proofs_paces.check_the_preferred_frame_parameter()[0]
    parameters = frame.preferred_frame_parameters()
    cross = frame.no_cross_terms()
    return Row(
        "S.35",
        held and parameters == [-8.0, -1.0, 0.0] and all(abs(v) < 1e-12 for v in cross[:2]),
        None,
        f"alpha_1, alpha_2, the drag: {parameters}; the band's odd part {cross[0]:.1e}",
    )


def gapped_holders_kernel() -> Row:
    """S.39 (Section 10.3): the gapped holder's lattice kernel at kappa = 1 / 20 has G_kappa(1) / G_0(1) = 0.9546 by the lattice Yukawa integral and the slope 1 - 0.92 kappa (families.gapped_holder_kernel), 0.9977 at kappa = 1 / 400 by the first order; the domain 0 < num <= den as S.11's; outside: num = 0, where the static line forces a = 0 outside the source (local support), and num < 0, the alternating tail (lambda = -8 + sqrt 63 at [-1, 2])."""
    kernel = families.gapped_holder_kernel()
    first_order = 1 - kernel[2] / 400
    no_tail = rule3.step_exact(5, 5, [5] * 6, 0, 1) == -5
    alternating = -8 + math.sqrt(63)
    return Row(
        "S.39",
        round(kernel[0], 2) == 20.0
        and round(kernel[1], 4) == 0.9546
        and round(kernel[2], 2) == 0.92
        and round(first_order, 4) == 0.9977,
        no_tail and alternating < 0,
        f"R = {kernel[0]:.2f}; G_kappa(1) / G_0(1) = {kernel[1]:.4f} at 1 / 20, slope {kernel[2]:.4f}, {first_order:.4f} at 1 / 400; [0, 1] forces a = 0 outside the source; [-1, 2]: lambda = {alternating:.4f}",
    )


def five_carrier_forms() -> Row:
    """S.36 (Section 10.3): the five forms tried for g_0a are refused: the one-sided mixed term gives a complex omega (0.16984 - 2.47 x 10^-4 i against the band's 0.17277 at k = 0.3, C / w = 10^-2), a growth that breaks the form and the inverse (frame.five_forms, proofs_far_regime's exact identity), and the staggered clock's redshift is 5 / 3 of general relativity's (sqrt(3 / (4 - 0.9^4)) = 0.9472, proofs_paces' check); Rule3's own line is real and even in k (the admitted form, the band's eigenvalues on the unit circle); outside the line: with the first-difference term a carrier appears, the real part of omega shifted below the band's with the imaginary part beside it."""
    forms = frame.five_forms()
    identity = proofs_far_regime.check_the_one_sided_mixed_terms_dispersion()[0]
    staggered = proofs_paces.check_the_staggered_clocks_redshift()[0]
    even = rule3.dispersion_at_paces(
        (0.3, 0.0, 0.0), *LIGHT, 1, 1, (1, 1, 1)
    ) == rule3.dispersion_at_paces((-0.3, 0.0, 0.0), *LIGHT, 1, 1, (1, 1, 1))
    return Row(
        "S.36",
        identity
        and staggered
        and round(forms[3], 4) == 0.9472
        and abs(forms[4] - 5 / 3) < 1e-12
        and even,
        round(forms[0], 5) == 0.16984 and abs(forms[1] + 2.47e-4) < 1e-6 and forms[0] < forms[2],
        f"the mixed term's omega {forms[0]:.5f} {forms[1]:.2e} i against the band's {forms[2]:.5f}; the staggered clock's {forms[3]:.4f}, the redshift {forms[4]:.4f} of general relativity's",
    )


def two_forces_between_quanta() -> Row:
    """S.44 (Section 10.1): F_e / F_g = k E_g / (2 E_s sin^2 omega_s) at one family and (F_e / F_g)_e / (F_e / F_g)_p = sin^2 omega_p / sin^2 omega_e = (m_p / m_e)^2 between two, exact in rationals (proofs_bodies' check; constants.two_forces_ratio at [999, 1000] against [1, 2]), nature's 4.17 x 10^42 and 1.24 x 10^36 with the ratio 3.37 x 10^6 = 1836.15^2; an identity with no condition to step outside of."""
    held = proofs_bodies.check_the_two_forces_between_quanta()[0]
    ratio = constants.two_forces_ratio()
    return Row(
        "S.44",
        held and ratio[0] == 0 and abs(ratio[1] - ratio[2]) < 1e-3,
        None,
        f"the identity's residual {ratio[0]}; (m_p / m_e)^2 = {ratio[1]:.4f} x 10^6 against nature's force ratios' {ratio[2]:.4f} x 10^6",
    )


def nuclear_holders_threshold() -> Row:
    """S.45 (Section 10.3): the nuclear holder's well binds iff W >= 1.6798 x 4 pi Gamma kappa / (6 mu omega_p sin omega_p), 1.17 Gamma kappa / omega_p^3 at the law's mu = m*, 591 and 502 at [2, 3], kappa = 1 / 20, Gamma = 6,000, doubling under the pair hypothesis to 1,183 and 1,004 (nuclear.nuclear_well_threshold, proofs_bodies' check); the binding at a size (lambda_s / R)^2 / 2: 3.1 x 10^-2, 4.9 x 10^-3, 1.6 x 10^-3, the size law 28 and 784, the miss against nature's 1.19 x 10^-3 and 9.4 x 10^-3 named; outside: a reach below one Link, where the kernel is the contact one, the running exponent s(kappa R) at 3 (2.971 at kappa R = 10, 2.993 at 20) against the Yukawa well's 1 at a long reach."""
    held = proofs_bodies.check_the_nuclear_holders_threshold()[0]
    threshold = [round(v) for v in nuclear.nuclear_well_threshold()]
    sizes = nuclear.binding_at_a_size()
    exponents = {z: proofs_audit.integrated_exponent(z) for z in (0.01, 10.0, 20.0)}
    return Row(
        "S.45",
        held
        and threshold[1:3] == [591, 502]
        and threshold[4:] == [1183, 1004]
        and [f"{v:.1e}" for v in sizes[:3]] == ["3.1e-02", "4.9e-03", "1.6e-03"]
        and sizes[3:] == [28.0, 784.0],
        exponents[10.0] > 2.9 and exponents[20.0] > 2.99 and exponents[0.01] < 1.1,
        f"W thresholds {threshold[1:3]} (the law's mu) and {threshold[4:]} (the pair hypothesis); binding fractions {[f'{v:.1e}' for v in sizes[:3]]} against nature's 1.2e-03 (deuteron) and 9.4e-03 (iron); s(kappa R) = {exponents[10.0]:.3f}, {exponents[20.0]:.3f} at 10, 20 (the contact kernel's 3), {exponents[0.01]:.3f} at 0.01",
    )


def atom_with_the_nucleus_angle() -> Row:
    """S.46 (Section 7.3): with the nucleus's angle alone the levels are Bohr's, E_n proportional to 1 / n^2 and a_0 = sqrt 3 / (m* Z alpha) (atom.bohr_levels); the trial record's E_tot = x^2 - 2x + (5 / 8) x / Z is least at x = 1 - 5 / (16 Z) exactly, at Z = 1 x = 11 / 16 with E_tot = -121 / 256 Rydberg = -121 / 512 hartree, the mode's epsilon = -0.043 the miss named, the Rydberg ratios 1 - 1.25 / Z at large Z (proofs_bodies' check); outside the one-parameter family: H psi / psi for the trial psi = e^(-x r) with its own Hartree level is not constant in r (-0.37, -0.13, -0.08 hartree at r = 0.5, 1, 2 a_0), so the trial is no fixed point."""
    bohr = atom.bohr_levels()
    self_term = proofs_bodies.check_the_atoms_self_term()[0]
    x = Fraction(11, 16)
    slope = 2 * x - 2 + Fraction(5, 8)
    energy_rydberg = x * x - 2 * x + Fraction(5, 8) * x
    hartree = energy_rydberg / 2
    exact = slope == 0 and energy_rydberg == Fraction(-121, 256) and hartree == Fraction(-121, 512)
    xf = float(x)

    def local_energy(r: float) -> float:
        """H psi / psi in hartree for psi = e^(-x r), the nucleus's -1 / r and the Hartree level of the record's own cloud (1 - (1 + x r) e^(-2 x r)) / r, at the self-read's weight 5 / 8 of the full 1 / r term's coefficient."""
        kinetic = -(xf * xf) / 2 + xf / r
        hartree_level = (1 - (1 + xf * r) * math.exp(-2 * xf * r)) / r
        return kinetic - 1 / r + hartree_level

    locals_ = [local_energy(r) for r in (0.5, 1.0, 2.0)]
    return Row(
        "S.46",
        [round(v, 4) for v in bohr] == [1.0, 0.25, 0.1111, 1.7321] and self_term and exact,
        max(locals_) - min(locals_) > 0.1,
        f"Bohr's 1, 1/4, 1/9 and a_0 m* Z alpha = sqrt 3; the trial's minimum at x = {x}, E_tot = {energy_rydberg} Ry = {hartree} Ha; H psi / psi at r = 0.5, 1, 2: {', '.join(f'{v:.3f}' for v in locals_)} hartree, not constant",
    )


def zeno_curve() -> Row:
    """S.59 (Section 5.4): with the window's outcome written the share in e after n windows during a pi pulse is (1 - cos^n(pi / n)) / 2, 1, 0.500, 0.375, 0.235, 0.133 at n = 1, 2, 4, 8, 16 (zeno.formula_column, proofs_credit's recurrence); outside: a reading with no write, where the n rotations by pi / (2 n) compose to pi / 2 and P(e) = 1 at every n, and a body reading itself at its own period 7.47 intervals, whose P(e) over the 768-interval pulse would be 0.023 against nature's full transfer at n = 1 (zeno.own_period_as_window)."""
    column = [round(v, 3) for v in zeno.formula_column()]
    recurrence = proofs_credit.check_the_zeno_formula()[0]
    no_write = all(abs(math.sin(n * (math.pi / (2 * n))) ** 2 - 1) < 1e-12 for n in zeno.PULSES)
    own = zeno.own_period_as_window()
    return Row(
        "S.59",
        column == [1.0, 0.5, 0.375, 0.235, 0.133] and recurrence,
        no_write and own[2] < 0.05 and own[0] == 1,
        f"column A {column}; no write: P(e) = 1 at every n; the body's own period {own[1]:.2f} intervals as the window: P(e) = {own[2]:.3f}",
    )


def lattice_scale_quartic_coefficient() -> Row:
    """S.65 (Table 5's scale row): the massless band's quartic coefficient per direction, omega^2 = k^2 / 3 - (k^4 / 108)(3 S_4 - 1) with S_4 = SUM_a n_a^4, -1 / 54 on an axis, -1 / 216 on a face diagonal and 0 on a body diagonal, by the series and by the exact arccosine at k = 0.01 (the mathematician's #1836 comment 5984624212 (1)); outside: an isotropic band, cos omega = cos(|k| / sqrt 3), has the coefficient 0 in every direction, and the band has no cubic term, being even in k."""

    def exact(direction: tuple[int, int, int], k: float = 0.01) -> float:
        norm = math.sqrt(sum(d * d for d in direction))
        cos_omega = sum(math.cos(k * d / norm) for d in direction) / 3
        omega = math.acos(cos_omega)
        return (omega * omega - k * k / 3) / k**4

    def series(direction: tuple[int, int, int]) -> Fraction:
        n2 = sum(d * d for d in direction)
        s4 = sum(Fraction(d * d, n2) ** 2 for d in direction)
        return -(3 * s4 - 1) / 108

    directions = ((1, 0, 0), (1, 1, 0), (1, 1, 1))
    expected = [Fraction(-1, 54), Fraction(-1, 216), Fraction(0)]
    by_series = [series(d) for d in directions]
    by_arccos = [exact(d) for d in directions]
    inside = by_series == expected and all(
        abs(a - float(b)) < 1e-3 for a, b in zip(by_arccos, by_series, strict=True)
    )
    k = 0.01
    isotropic = (math.acos(math.cos(k / math.sqrt(3))) ** 2 - k * k / 3) / k**4
    even = all(
        abs(
            math.acos(sum(math.cos(s * k * d / math.sqrt(sum(x * x for x in d_))) for d in d_) / 3)
            - math.acos(sum(math.cos(-s * k * d / math.sqrt(sum(x * x for x in d_))) for d in d_) / 3)
        )
        < 1e-15
        for d_ in directions
        for s in (1.0, 7.0)
    )
    return Row(
        "S.65",
        inside,
        abs(isotropic) < 1e-6 and even,
        f"quartic coefficient by the series {[str(v) for v in by_series]}, by the arccosine {[round(v, 5) for v in by_arccos]}; the isotropic band's {isotropic:.1e}; the band even in k",
    )
