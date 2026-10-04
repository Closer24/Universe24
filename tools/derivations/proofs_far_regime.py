"""The far-regime witnesses (the owner's order of 2026-10-04, 08:20 UTC, through the Boss): every claim of main.tex and supplement.tex that says "for every", "for all", "exactly", "at every step", "in the limit", "as the gap closes" or "to O(...)" and names a quantity, computed at the far end of its stated domain beside the claim's value, with whether they agree to the stated order; the claims of the band, the form, the paces, the credit and the bodies stand in their own modules with their far ends; this module holds the rest: the computed pair's limits, the clock's rate in the half sine, the cut region's uniform mode, the folded axis's band, Friedmann's dust equations and the Doppler-times-clock redshift, the content's first order in the clock, the two readings of beta, gamma_K - 1 as half the gap squared, the lattice's half-sine variable, the ports' orthogonality, the gap below 10^-18, the momentum identity at non-uniform paces and the Fourier weight of a smooth body.

Usage: `python tools/derivations/proofs_far_regime.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402
from proofs_ground import (
    PORTS,
    SEED,
    Check,
    Gaussian,
    angles,
    box_arrivals,
    box_index,
    box_nodes,
    has_order,
    pairs,
    read,
    run,
    step_line,
)  # noqa: E402


def check_the_computed_pairs_limits() -> Check:
    """main.tex, Introduction: replacing the computed pair [2, 3] by [999, 1000] moves c_m / c from 0.867 to about 0.9997, and the computed pair's gamma_K and beta_K from 1.5 and 1.25 to about 1.001 and 1.0005, approaching 1 as the gap closes; c_m / c = sqrt(omega_0 / tan omega_0), gamma_K = den / num, beta_K = (den + num) / (2 num); the far end of the gap, num / den = 0.01, beside them."""
    rows = {}
    for num, den in ((2, 3), (999, 1000), (1, 100)):
        omega_0 = math.acos(num / den)
        rows[f"{num} / {den}"] = (
            round(math.sqrt(omega_0 / math.tan(omega_0)), 4),
            round(den / num, 4),
            round((den + num) / (2 * num), 4),
        )
    held = (
        round(rows["2 / 3"][0], 3) == 0.867
        and rows["2 / 3"][1:] == (1.5, 1.25)
        and rows["999 / 1000"] == (0.9997, 1.001, 1.0005)
    )
    return held, {"c_m / c, gamma_K, beta_K": rows}


def check_the_clocks_rate_is_exact_in_the_half_sine() -> Check:
    """main.tex Section 3.4; S.31: the clock's rate is N exactly in the lattice's variable 2 sin(omega / 2): from the band at a pace at k = 0, 1 - cos omega(U) = (1 - nu) N^2, so 2 sin^2(omega(U) / 2) = N^2 2 sin^2(omega_0 / 2) and 2 sin(omega(U) / 2) = N 2 sin(omega_0 / 2) exactly for every N; and in omega up to the finite-rotation correction omega_0^2 / 12, 5.9 percent at the computed pair (6.3 exactly); exact rationals in the half-sines squared, the far end of the content U = 4.7 (the frozen content, N^2 = e^(-9.4)) in floats."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8):
        for _ in range(5):
            n2 = Fraction(draw.randint(1, 99), 100)
            half_sine_squared_0 = (1 - Fraction(num, den)) / 2
            half_sine_squared = (1 - (1 - (1 - Fraction(num, den)) * n2)) / 2
            if half_sine_squared != n2 * half_sine_squared_0:
                return False, {"pair": (num, den), "N^2": n2}
    omega_0 = math.acos(2 / 3)
    n = math.exp(-4.7)
    far = (
        2 * math.asin(n * math.sin(omega_0 / 2)) / (2 * math.asin(math.sin(omega_0 / 2))),
        n,
    )  # omega(U) / omega_0 against N at the frozen content
    return round(omega_0**2 / 12, 3) == 0.059, {
        "omega(U) / omega_0 against N at U = 4.7": far,
        "omega_0^2 / 12 at [2, 3]": omega_0**2 / 12,
    }


def check_the_cut_regions_uniform_mode() -> Check:
    """main.tex Section 5.3 (the NodeReader with its own record): a region with its outer Links cut (the Link's factor 0 at both ends, the Node's own coefficient recomputed from its open Links) and its inner Links open has its uniform mode rotating at cos omega_0 = num / den exactly whatever the region's size: S_i = 12 den Gamma^2 - 12 (den - num) Gamma^2 - SUM over the open Ports of R_ij at the vacuum's clock, so (S_i + SUM over the open Ports of R_ij) / w = 12 num Gamma^2 / (6 den Gamma^2) = 2 num / den; exact rationals on chains of one to five Nodes."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 6):
        gamma = draw.randint(2, 30)
        for size in range(1, 6):
            arrivals = box_arrivals(
                (size + 2, 1, 1)
            )  # the region the Nodes 1 .. size, the Links to 0 and size + 1 cut
            factors = [[gamma] * PORTS for _ in arrivals]
            for i in range(1, size + 1):
                for port, j in enumerate(arrivals[i]):
                    if j in (0, size + 1):
                        factors[i][port] = 0
            wall, reads, selves, paces = read(
                arrivals, [gamma] * len(arrivals), factors, num, den, gamma
            )
            uniform = [Fraction(1) if 1 <= i <= size else Fraction(0) for i in range(len(arrivals))]
            after = step_line(
                arrivals, reads, selves, wall, uniform, [u * Fraction(num, den) for u in uniform]
            )  # before = cos omega_0 now for the rotation e^(-i omega_0 t) on a real line: a_next + a_before = 2 cos omega_0 a_now
            for i in range(1, size + 1):
                if after[i] + uniform[i] * Fraction(num, den) != 2 * Fraction(num, den) * uniform[i]:
                    return False, {
                        "pair": (num, den),
                        "size": size,
                        "Node": i,
                        "a_next + a_before": after[i] + uniform[i] * Fraction(num, den),
                    }
    return True, {"sizes": "1 to 5"}


def check_the_folded_axis_carries_the_band() -> Check:
    """main.tex Section 9.1: a record uniform along the folded axis has the three-dimensional band at k_z = 0, so the flat lattice carries the file's band exactly: on a chain with y and z folded (rule3.chain_arrivals, four Ports returning the Node itself) a plane wave along x satisfies the line at cos omega = (num / (3 den)) (cos k + 2), the band at k_y = k_z = 0; exact at rational angles by rule3.numerator."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 6):
        gamma = draw.randint(2, 20)
        wall, reads, self_coefficient = rule3.coefficients(num, den, gamma)
        for wave in angles(draw, 7):
            cosine = Fraction(num, 3 * den) * (wave.re + 2)
            for phase in angles(draw, 7)[2:]:
                amplitude = draw.randint(1, 30)
                level = {
                    x: amplitude * (phase * wave**x).re for x in range(-1, 9)
                }  # the wave on the open chain about the Nodes 0 .. 7
                for i in range(8):
                    arrivals = [
                        level[i + 1],
                        level[i - 1],
                        level[i],
                        level[i],
                        level[i],
                        level[i],
                    ]  # the folded y and z Ports return the Node itself
                    right = rule3.numerator(level[i], arrivals, reads, self_coefficient)
                    if right != 2 * wall * cosine * level[i]:
                        return False, {"pair": (num, den), "Node": i}
    return True, {"pairs": 6}


def check_friedmanns_dust_equations_and_the_redshift() -> Check:
    """main.tex Section 7.5; S.29: a shell at a feels the mass inside it, a'' = -(4 pi G_K / 3) rho a with rho a^3 constant, which integrates exactly to a'^2 / a^2 = (8 pi G_K / 3) rho - kappa / a^2, Friedmann's dust equations, the deceleration q_0 = Omega_m / 2 positive for every rho > 0; the invariant a'^2 - 2 mu / a, mu = (4 pi G_K / 3) rho a^3, has the derivative 2 a' (a'' + mu / a^2) = 0 exactly, and a fourth-order integration keeps it to 10^-12; the Doppler period of a receding source times the moving clock's factor, 1 + z = (1 + beta) / sqrt(1 - beta^2) = 1 + beta + beta^2 / 2 + O(beta^3), nature's relativistic form to the second order, the classical 1 / (1 - beta) = 1 + beta + beta^2 differing there; z_t = (2 Omega_Lambda / Omega_m)^(1 / 3) - 1 = 0.67 at Omega_Lambda = 0.7; the far end beta = 0.9."""
    mu = 0.7
    a, v = 1.0, 1.5  # an unbound ball, so the integration meets no collapse
    invariant = v * v - 2 * mu / a
    dt = 1e-3

    def acceleration(x: float) -> float:
        return -mu / (x * x)

    for _ in range(4000):
        k1v, k1a = acceleration(a), v
        k2v, k2a = acceleration(a + dt / 2 * k1a), v + dt / 2 * k1v
        k3v, k3a = acceleration(a + dt / 2 * k2a), v + dt / 2 * k2v
        k4v, k4a = acceleration(a + dt * k3a), v + dt * k3v
        a += dt / 6 * (k1a + 2 * k2a + 2 * k3a + k4a)
        v += dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    drift = abs(v * v - 2 * mu / a - invariant)
    exact_derivative = all(
        abs(2 * vv * (acceleration(aa) + mu / (aa * aa))) == 0.0
        for aa, vv in ((1.0, 0.3), (2.0, -0.5), (0.5, 1.0))
    )
    q_0 = (
        Fraction(4) * Fraction(1, 3) / (Fraction(8) * Fraction(1, 3) / Fraction(1))
    )  # (4 pi G rho / 3) / H^2 over Omega_m = 8 pi G rho / (3 H^2): the ratio 1 / 2 with pi G rho / H^2 = 1
    second_order, orders = has_order(
        lambda b: (1 + b) / math.sqrt(1 - b * b) - (1 + b + b * b / 2), 3, step=0.1
    )
    classical = has_order(lambda b: 1 / (1 - b) - (1 + b + b * b / 2), 2, step=0.1)[0]
    far = ((1 + 0.9) / math.sqrt(1 - 0.81), 1 + 0.9 + 0.405, 1 / 0.1)
    turnaround = round((2 * 0.7 / 0.3) ** (1 / 3) - 1, 2)
    return drift < 1e-12 and exact_derivative and q_0 == Fraction(
        1, 2
    ) and second_order and classical and turnaround == 0.67, {
        "invariant drift": drift,
        "orders of 1 + z": orders,
        "far end beta = 0.9 (exact, second order, classical)": far,
        "z_t": turnaround,
    }


def check_the_contents_first_order_in_the_clock() -> Check:
    """main.tex Section 8 (a); The ledger of exactness: p_0 / Gamma = (1 - 1 / Gamma)^l = e^(-U) exactly with U = -l ln(1 - 1 / Gamma), which is l / Gamma to the first order in 1 / Gamma, U - l / Gamma = l / (2 Gamma^2) + ...; the order by the residual in 1 / Gamma, the far end Gamma = 2 (0.693 l against l / 2)."""
    held, orders = has_order(lambda h: -math.log(1 - h) - h, 2, step=0.1)
    coefficient = (-math.log(1 - 0.01) - 0.01) / 0.01**2
    far = (-math.log(1 - 1 / 2), 1 / 2)
    return held and abs(coefficient - 0.5) < 0.01, {
        "orders": orders,
        "second-order coefficient": coefficient,
        "far end Gamma = 2 (U per level, l / Gamma)": far,
    }


def check_the_two_readings_of_beta() -> Check:
    """main.tex Section 8 (b), the push: the two readings of beta in the box, P / E with p = E v as S.58 writes the push, and v / c_local, agree as the gap closes: on the exact band at the vacuum P / E = c k / omega(k) and v / c = (d omega / dk) / c, equal where the band is Lorentz's (omega^2 = omega_0^2 + c^2 k^2) and parting at a finite gap; at [2, 3] and k = 0.3 they read 0.203 and 0.151, at [999999, 1000000] they agree to 10^-6; the readings recomputed."""
    c = 1 / math.sqrt(3)
    readings = {}
    for num, den in ((2, 3), (999, 1000), (999999, 1000000)):
        c0 = num / (3 * den)
        k = 0.3 if den < 10000 else 0.001

        def omega(q: float, c0: float = c0) -> float:
            return math.acos(c0 * (2 + math.cos(q)))

        h = 1e-6
        velocity = (omega(k + h) - omega(k - h)) / (2 * h)
        readings[f"{num} / {den}"] = (round(c * k / omega(k), 6), round(velocity / c, 6))
    close = readings["999999 / 1000000"]
    return abs(close[0] - close[1]) < 1e-5 and tuple(round(v, 3) for v in readings["2 / 3"]) == (
        0.203,
        0.151,
    ), {"P / E and v / c": readings}


def check_gamma_k_minus_one_is_half_the_gap_squared() -> Check:
    """main.tex Section 10.1; S.27: gamma_K - 1 = den / num - 1 = 1 / cos omega_0 - 1 = omega_0^2 / 2 + O(omega_0^4) (5 omega_0^4 / 24), below 6.7 x 10^-20 at omega_e < 3.7 x 10^-10; the order by the residual, the far end [1, 2] (omega_0 = pi / 3: 1 against 0.548)."""
    held, orders = has_order(lambda w: 1 / math.cos(w) - 1 - w * w / 2, 4, step=0.4)
    coefficient = (1 / math.cos(0.01) - 1 - 0.01**2 / 2) / 0.01**4
    far = (2 / 1 - 1, (math.pi / 3) ** 2 / 2)
    return held and abs(coefficient - 5 / 24) < 0.01, {
        "orders": orders,
        "fourth-order coefficient": coefficient,
        "far end [1, 2] (exact, omega^2 / 2)": far,
    }


def check_the_lattices_half_sine_variable() -> Check:
    """S.31: with s(x) = 2 sin(x / 2), s(k)^2 = k^2 [1 - k^2 / 12 + ...], every mode scaling by N in s(omega) exactly at long wavelength and to the lattice's k^2 / 12 at finite k; the residual of the sixth order, the far end k = pi (s^2 = 4 against pi^2 (1 - pi^2 / 12) = 1.75)."""
    held, orders = has_order(
        lambda k: (2 * math.sin(k / 2)) ** 2 - k * k * (1 - k * k / 12), 6, step=0.5
    )
    far = ((2 * math.sin(math.pi / 2)) ** 2, math.pi**2 * (1 - math.pi**2 / 12))
    return held, {"orders": orders, "far end k = pi (exact, truncated)": far}


def check_the_ports_are_exactly_orthogonal() -> Check:
    """main.tex Section 9.3; S.51: the port coefficients e(+) = (p, q) and e(-) = (-q, p) are exactly orthogonal with equal norms, so each side's marginal is one half for any setting; and in nature cos omega differs from 1 by under 10^-18 for every family (6.8 x 10^-20 at omega_e = 3.7 x 10^-10); exact integers and the number recomputed."""
    draw = random.Random(SEED)
    for _ in range(30):
        p, q = draw.randint(-99, 99), draw.randint(-99, 99)
        if p * (-q) + q * p != 0 or p * p + q * q != q * q + p * p:
            return False, {"setting": (p, q)}
    gap = 1 - math.cos(3.7e-10)
    gap_series = (3.7e-10) ** 2 / 2
    return gap_series < 1e-18, {"1 - cos omega_e (float, omega^2 / 2)": (gap, gap_series)}


def check_the_fringes_near_field_minima() -> Check:
    """S.23: the gaps centred at the rows 18 and 30, d = 12, the screen L = 24 Links from the wall, lambda = 8: the far-field spacing is lambda L / d = 16 Links, and the near-field minima, where the two paths differ by half a wavelength, sqrt(L^2 + (y - 18)^2) - sqrt(L^2 + (y - 30)^2) = +- 4, are at y = 15.28 and 32.72, the rows 15 and 33; the roots by bisection."""

    def difference(y: float) -> float:
        return math.sqrt(24**2 + (y - 18) ** 2) - math.sqrt(24**2 + (y - 30) ** 2)

    roots = []
    for target, low, high in ((-4.0, 0.0, 24.0), (4.0, 24.0, 48.0)):
        for _ in range(60):
            middle = (low + high) / 2
            low, high = (
                (middle, high)
                if (difference(middle) - target) * (difference(low) - target) > 0
                else (low, middle)
            )
        roots.append(round((low + high) / 2, 2))
    return roots == [15.28, 32.72] and 8 * 24 / 12 == 16, {
        "minima": roots,
        "far-field spacing": 8 * 24 / 12,
    }


def check_newtons_constant_and_alpha_laws_numbers() -> Check:
    """S.25, Eq. (20): the massless holder's rest far from a static source of s quanta per interval is 3 s / (4 pi r) over E_g, so U = 3 s / (4 pi r Gamma E_g), and nature's U = G M / (c^2 r) with M = s and c^2 = 1 / 3 gives G_clock = 1 / (4 pi Gamma E_g); S.26 (b): alpha_law = (3 sqrt 3 / 8 pi) k / (Gamma E_s) = 0.20675 k / (Gamma E_s), and nature's 1 / 137.036 fixes k / (Gamma E_s) = 1 / 28.33, no integer Gamma E_s emission it at k = 1 (28 gives 1 / 135.43 and 29 gives 1 / 140.27); the algebra exact with pi as a symbol cancelled, the numbers recomputed."""
    for s, r, gamma, e_g in ((3, 7, 11, 5), (1, 2, 6000, 10)):
        level = Fraction(3 * s, 4 * r * gamma * e_g)  # U times pi
        g_over_c2 = level * r / s  # G / c^2 times pi
        if g_over_c2 / 3 != Fraction(1, 4 * gamma * e_g):  # G = (G / c^2) / 3 = 1 / (4 pi Gamma E_g)
            return False, {"G_clock": (s, r, gamma, e_g)}
    coefficient = 3 * math.sqrt(3) / (8 * math.pi)
    product = 137.036 * coefficient
    numbers = (
        round(coefficient, 5),
        round(product, 2),
        round(1 / (coefficient / 28), 2),
        round(1 / (coefficient / 29), 2),
    )
    return numbers == (0.20675, 28.33, 135.43, 140.27), {
        "3 sqrt 3 / 8 pi, 137.036 x it, 1 / alpha at Gamma E_s = 28 and 29": numbers
    }


def check_the_rules_total_at_the_width() -> Check:
    """The bound (ALGEBRA.md): the rule's total at a Node at the amplitude A is at most 6 A |R| + A |S| + w (A + 1); with Gamma = 10^4 and A = 2^20 the total is 4.4 x 10^15 at [2, 3] and 8.8 x 10^18 at [4000, 6000], 0.96 of 2^63; exact integers by rule3.rule_total."""
    small, large = rule3.rule_total(1 << 20, 2, 3, 10**4), rule3.rule_total(1 << 20, 4000, 6000, 10**4)
    numbers = (f"{small:.1e}", f"{large:.1e}", round(large / 2**63, 3))
    return numbers[:2] == ("4.4e+15", "8.8e+18") and abs(numbers[2] - 0.96) < 0.01, {
        "totals (the room 0.955 of 2^63, the law's 0.96)": numbers
    }


def check_a_body_stands_in_integers() -> Check:
    """The integer budget of a derived row, A body stands, in integers: the share's deviation over n intervals lies within 2 sqrt 8 sigma sqrt n / A at the confidence 2, sqrt 8 the exponential profile's factor, sigma the mode's walk per interval, against the amplitude A = sqrt(T c_i / (2 sin omega_s)) of c_i quanta per Node: 852 at T = 2^15 and 3,407 at 2^19 for c_i = 33 at [2, 3], and 4.7 percent per mode at rest at n = 10^3 (0.224 sqrt 1000 x 5.66 / 852); at the two slits over 130 intervals the walk is 2.4 levels per mode at the carrier (0.209 sqrt 130), 3.0 per Node over the plane's zone (0.259 sqrt n) and 4.0 over a cube's (0.354 sqrt n); the numbers recomputed."""
    omega_s = math.acos(2 / 3)
    amplitudes = tuple(round(math.sqrt(t * 33 / (2 * math.sin(omega_s)))) for t in (1 << 15, 1 << 19))
    deviation = round(100 * 0.224 * math.sqrt(1000) * 2 * math.sqrt(8) / amplitudes[0], 1)
    slits = tuple(round(w * math.sqrt(130), 1) for w in (0.209, 0.259, 0.354))
    return amplitudes == (852, 3407) and deviation == 4.7 and slits == (2.4, 3.0, 4.0), {
        "A at T = 2^15 and 2^19": amplitudes,
        "deviation percent": deviation,
        "the two slits' walks": slits,
    }


def check_the_one_sided_mixed_terms_dispersion() -> Check:
    """S.36 (i): the one-sided real mixed term C_a [(a_(+a) - a_(-a))_now - (a_(+a) - a_(-a))_before] added to the line gives w (e^(-i omega) + e^(i omega)) = S + 2 SUM_a R_a cos k_a + C_a (2 i sin k_a) (1 - e^(i omega)), and 1 - e^(i omega) = -2 i sin(omega / 2) e^(i omega / 2), so the term is 2 C_a sin k_a sin omega + 4 i C_a sin k_a sin^2(omega / 2): a g_0a part beside an imaginary part that breaks the form and the exact inverse; the identity exact in Gaussian rationals at rational half-angles."""
    draw = random.Random(SEED)
    for half in angles(draw, 10):
        omega = half * half
        for wave in angles(draw, 8):
            c = Fraction(draw.randint(1, 9), 7)
            left = (
                Gaussian(0, 2 * wave.im) * c * (Gaussian(1, 0) - omega)
            )  # C (2 i sin k) (1 - e^(i omega))
            right = Gaussian(2 * c * wave.im * omega.im, 4 * c * wave.im * half.im**2)
            if left != right or Gaussian(1, 0) - omega != Gaussian(0, -2 * half.im) * half:
                return False, {"half angle": half, "left": left, "right": right}
    return True, {"witnesses": 80}


def check_the_momentum_identity_at_non_uniform_paces_as_printed() -> Check:
    """main.tex Section 4.3 as printed: "at non-uniform static paces Eq. (7) gains the Link-wise differences of the coefficients, [R_b(i) - R_b(i - b)] times the stress readings, while the share's identity (S.5) gains nothing at static paces": computed on a periodic 5-box with per-Node coefficients from differing clocks and the line without its division, w [P_a(t + 1) - P_a(t)] - SUM_b [R_b(i) G_ab(i) - R_b(i - b) G_ab(i - b)] does not vanish; the exact identity at non-uniform static paces is w [P_a(t + 1) - P_a(t)] = -Y_i Delta_a now_i + now_i Delta_a Y_i with Y the read, whose extra terms against Eq. (7) are the differences of the reading Node's coefficients along the momentum's axis a, [R_b(i + a) - R_b(i)] and [S_(i + a) - S_i], times the levels, not the b-Link-wise differences of R alone; the share's identity does gain nothing (proofs_booking); a finding on the sentence."""
    draw = random.Random(SEED)
    shape = (5, 5, 5)
    nodes, arrivals = box_nodes(shape), box_arrivals(shape)
    num, den, gamma = 2, 3, 12
    clocks = [draw.randint(6, 12) for _ in nodes]
    wall, reads, selves, paces = read(
        arrivals, clocks, [[gamma] * PORTS for _ in nodes], num, den, gamma
    )
    now = [Fraction(draw.randint(-30, 30)) for _ in nodes]
    before = [Fraction(draw.randint(-30, 30)) for _ in nodes]
    after = step_line(arrivals, reads, selves, wall, now, before)
    unit = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

    def at(levels, x, y, z):
        return levels[box_index(shape, x, y, z)]

    def coefficient(b, x, y, z):
        return reads[box_index(shape, x, y, z)][2 * b]

    def self_at(x, y, z):
        return selves[box_index(shape, x, y, z)]

    printed_residual, exact_residual = Fraction(0), Fraction(0)
    for x, y, z in nodes:
        for a in range(3):
            ea = unit[a]
            plus, minus = (x + ea[0], y + ea[1], z + ea[2]), (x - ea[0], y - ea[1], z - ea[2])
            p_now = (at(now, x, y, z) * at(before, *minus) - at(before, x, y, z) * at(now, *minus)) - (
                at(now, x, y, z) * at(before, *plus) - at(before, x, y, z) * at(now, *plus)
            )
            p_next = (at(after, x, y, z) * at(now, *minus) - at(now, x, y, z) * at(after, *minus)) - (
                at(after, x, y, z) * at(now, *plus) - at(now, x, y, z) * at(after, *plus)
            )
            left = wall * (p_next - p_now)
            flux = Fraction(0)
            for b in range(3):
                eb = unit[b]

                def stress(cx, cy, cz, now=now, ea=ea, eb=eb):
                    return at(now, cx, cy, cz) * (
                        at(now, cx + ea[0] + eb[0], cy + ea[1] + eb[1], cz + ea[2] + eb[2])
                        - at(now, cx - ea[0] + eb[0], cy - ea[1] + eb[1], cz - ea[2] + eb[2])
                    ) - at(now, cx + eb[0], cy + eb[1], cz + eb[2]) * (
                        at(now, cx + ea[0], cy + ea[1], cz + ea[2])
                        - at(now, cx - ea[0], cy - ea[1], cz - ea[2])
                    )

                flux += coefficient(b, x, y, z) * stress(x, y, z) - coefficient(
                    b, x - eb[0], y - eb[1], z - eb[2]
                ) * stress(x - eb[0], y - eb[1], z - eb[2])

            def read_at(cx, cy, cz):
                total = self_at(cx, cy, cz) * at(now, cx, cy, cz)
                for b in range(3):
                    eb = unit[b]
                    total += coefficient(b, cx, cy, cz) * (
                        at(now, cx + eb[0], cy + eb[1], cz + eb[2])
                        + at(now, cx - eb[0], cy - eb[1], cz - eb[2])
                    )
                return total

            exact = -read_at(x, y, z) * (at(now, *plus) - at(now, *minus)) + at(now, x, y, z) * (
                read_at(*plus) - read_at(*minus)
            )
            printed_residual = max(printed_residual, abs(left - flux))
            exact_residual = max(exact_residual, abs(left - exact))
    return printed_residual == 0 and exact_residual == 0, {
        "largest residual of the printed clause": printed_residual,
        "largest residual of the exact identity -Y_i Delta_a now_i + now_i Delta_a Y_i": exact_residual,
    }


def check_the_fourier_weight_of_a_smooth_body() -> Check:
    """S.42 (b) as printed: a source faster than light's zone-edge phase speed is matched to zone-edge light, "which a body smooth over many Links sources only by its Fourier weight at that wave number, below e^-100 for every body of the paper": a Gaussian body of rms width R Links has the weight e^(-k^2 R^2 / 2) at k = pi, below e^-100 only for R above 4.5 Links; the paper's bodies on the chain are 2.1 to 3.4 Links wide about the mode's 2.4 (the surplus's breathing cloud), where the weight is e^-22 to e^-57, and a body with an exponential tail has a Fourier weight falling as a power of k; a finding on "for every body of the paper"."""
    weights = {width: -(math.pi**2) * width**2 / 2 for width in (2.1, 2.4, 3.4, 4.5)}
    width_for_100 = math.sqrt(200) / math.pi
    return all(exponent <= -100 for exponent in weights.values()), {
        "ln of the Fourier weight at k = pi by the rms width": weights,
        "the width for e^-100": width_for_100,
    }


def check_the_massless_rows_two_double_roots() -> Check:
    """ALGEBRA.md at 3a334eeb (No write from outside Rule3 wakes either double root of the massless row): the massless row's band cos omega_k = (1 / 3) SUM_a cos k_a has two double roots, the uniform mode at k = 0, omega = 0, and the staggered mode (-1)^(x + y + z + t) at k = (pi, pi, pi), omega = pi; each carries neither form nor share, 3 den (a^2 + b^2) - den a SUM_j b_j = 0 for a = b uniform and for the staggered pair b = -a; each is an exact mode of a board periodic on three axes of even extent, and in either a level stands and a velocity impulse is a slope that grows as tau + 1 for ever; a gapped row has no double root. The band's line 2 cos omega - (2 / 3) SUM_a cos k_a and its omega-derivative -2 sin omega are both 0 at the two roots, exact in rationals; the two modes are stepped by the vacuum's massless line a_next = (1 / 3) SUM_j a_j - a_before on the periodic boxes (2, 2, 2) and (4, 2, 2) exactly, the share and the form 0 at every Node, the slope of a uniform impulse growing by one level per interval over ten intervals, the staggered pattern no mode of the odd box (3, 2, 2); a gapped pair's sin omega_0 is not 0."""
    one, minus_one = Fraction(1), Fraction(-1)
    roots = (
        2 * one - Fraction(2, 3) * 3 * one == 0  # k = 0: cos omega = 1, the line 0
        and 2 * minus_one - Fraction(2, 3) * 3 * minus_one == 0  # k = (pi, pi, pi): cos omega = -1
        and all(1 - c * c == 0 for c in (one, minus_one))  # sin omega = 0 at both, the double roots
    )
    gapped = all(1 - Fraction(num * num, den * den) != 0 for num, den in ((2, 3), (999, 1000), (1, 2)))
    gamma = 7
    stepped = True
    for shape in ((2, 2, 2), (4, 2, 2)):
        arrivals, nodes = box_arrivals(shape), box_nodes(shape)
        sigma = [Fraction((-1) ** (x + y + z)) for x, y, z in nodes]
        uniform = [Fraction(5)] * len(nodes)
        for now, before, expected in (
            (sigma, [-s for s in sigma], [-s for s in sigma]),
            (uniform, uniform, uniform),
        ):
            nxt = [sum(now[j] for j in ports) / 3 - before[i] for i, ports in enumerate(arrivals)]
            share = [
                3 * (now[i] ** 2 + before[i] ** 2) - now[i] * sum(before[j] for j in ports)
                for i, ports in enumerate(arrivals)
            ]
            form = [
                6 * gamma**2 * (now[i] ** 2 + before[i] ** 2)
                - 2 * gamma**2 * now[i] * sum(before[j] for j in ports)
                for i, ports in enumerate(arrivals)
            ]
            stepped = stepped and nxt == expected and not any(share) and not any(form)
        before, now = uniform, [u + 1 for u in uniform]
        for tau in range(10):
            before, now = (
                now,
                [sum(now[j] for j in ports) / 3 - before[i] for i, ports in enumerate(arrivals)],
            )
            stepped = stepped and now == [u + tau + 2 for u in uniform]
    odd_arrivals, odd_nodes = box_arrivals((3, 2, 2)), box_nodes((3, 2, 2))
    odd_sigma = [Fraction((-1) ** (x + y + z)) for x, y, z in odd_nodes]
    odd_next = [
        sum(odd_sigma[j] for j in ports) / 3 + odd_sigma[i] for i, ports in enumerate(odd_arrivals)
    ]
    return roots and gapped and stepped and odd_next != [-s for s in odd_sigma], {
        "double roots at k = 0 and (pi, pi, pi)": roots,
        "the two modes stepped exactly with 0 share and 0 form, the impulse's slope": stepped,
        "the staggered pattern a mode of the odd box": odd_next == [-s for s in odd_sigma],
    }


def lights_stress_over_energy(k: float) -> float:
    """(num / 3 den) sin^2 k / sin^2 omega at light's pair along an axis, cos omega = (2 + cos k) / 3."""
    cosine = (2 + math.cos(k)) / 3
    return math.sin(k) ** 2 / (3 * (1 - cosine * cosine))


def check_lights_written_stress_over_energy_at_finite_k() -> Check:
    """main.tex 4.3 since 5f5df82b: on light's wave the written stress over the written energy is (num / 3 den) sin^2 k / sin^2 omega, 1 at long wavelength (nature's T_xx = T_00), 0.90 at k = pi / 4, and 3 / 5 where sin k = 1, at k = pi / 2 (printed as "the band's top along an axis", row F08); at light's pair cos omega = (2 + cos k) / 3: the long-wavelength limit 1 by the residual's order 2, 0.897 at pi / 4, 3 / 5 exactly at k = pi / 2 (sin^2 omega = 5 / 9) and 0 at the band's top k = pi, where sin k = 0."""
    held, orders = has_order(lambda h: lights_stress_over_energy(h) - 1, 2, step=0.2)
    at_quarter = round(lights_stress_over_energy(math.pi / 4), 2)
    at_half = Fraction(1, 3) * 1 / (1 - Fraction(2, 3) ** 2)  # sin^2 k = 1, cos omega = 2 / 3
    at_top = Fraction(1, 3) * 0 / (1 - Fraction(1, 3) ** 2)  # sin^2 pi = 0, cos omega = 1 / 3
    return held and at_quarter == 0.9 and at_half == Fraction(3, 5) and at_top == 0, {
        "orders of the limit": orders,
        "at pi / 4": at_quarter,
        "at pi / 2": at_half,
        "at the band's top, k = pi": at_top,
    }


def check_lights_stress_at_the_band_top_as_printed() -> Check:
    """main.tex 4.3 as printed since 5f5df82b, "3 / 5 at the band's top along an axis": at the band's top along an axis, k = pi with cos omega = 1 / 3 for light, sin k = 0 and the written stress over the written energy is 0; 3 / 5 is its value at k = pi / 2, where sin k = 1 and the group speed along the axis is largest; a finding on the number's place."""
    at_top = Fraction(1, 3) * 0 / (1 - Fraction(1, 3) ** 2)
    at_half = Fraction(1, 3) * 1 / (1 - Fraction(2, 3) ** 2)
    return at_top == Fraction(3, 5), {"at the band's top k = pi": at_top, "at k = pi / 2": at_half}


def check_the_division_acts_stop() -> Check:
    """main.tex since 5f5df82b (the one root, Section 5): the integer square root at a lay is the stop of the division act x <- (x + n div x) div 2, the law's fixed point, where the iterate stops falling (at n = 3 the iterates 2, 1, 2 alternate and the stop is 1); from x_0 = n the stop is isqrt(n) for every n to 5,000, exact integers."""

    def stop(n: int) -> int:
        x = n
        while True:
            y = (x + n // x) // 2
            if y >= x:
                return x
            x = y

    def iterates(n: int, count: int) -> list[int]:
        xs = [n]
        for _ in range(count):
            xs.append((xs[-1] + n // xs[-1]) // 2)
        return xs

    every = all(stop(n) == math.isqrt(n) for n in range(1, 5001))
    return every and iterates(3, 3) == [3, 2, 1, 2] and stop(3) == 1, {
        "n = 3": iterates(3, 3),
        "the stop isqrt(n) for n to 5,000": every,
    }


def check_the_shears_exact_angle_at_small_angles() -> Check:
    """main.tex 5.5 since d7e97674: the exact angle of the three shears is 2 arctan(L p_0 / (2 Gamma^2)), which is (L / Gamma)(p_0 / Gamma) at small angles; with x = L p_0 / Gamma^2 the remainder 2 arctan(x / 2) - x is of the third order, -x^3 / 12, and the exact angle's sine is x / (1 + x^2 / 4) at every rational x (the Pythagorean point of tan(theta / 2) = x / 2, sin^2 + cos^2 = 1 exactly)."""
    held, orders = has_order(lambda x: 2 * math.atan(x / 2) - x, 3, step=0.2)
    coefficient = (2 * math.atan(0.05) - 0.1) / 0.1**3
    draw = random.Random(SEED)
    exact = True
    for _ in range(20):
        x = Fraction(draw.randint(-40, 40), draw.randint(1, 40))
        t = x / 2
        sine, cosine = 2 * t / (1 + t * t), (1 - t * t) / (1 + t * t)
        exact = exact and sine == x / (1 + x * x / 4) and sine * sine + cosine * cosine == 1
    return held and exact and abs(coefficient + 1 / 12) < 1e-3, {
        "orders of the remainder": orders,
        "its coefficient": round(coefficient, 4),
        "at the largest turn x = 2 (exact angle, small-angle)": (round(2 * math.atan(1), 3), 2),
    }


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
