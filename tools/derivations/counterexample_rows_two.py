"""The breaker's second set of rows for the paper's theorems of the line and the bodies (the method of 2026-10-04): the record as the top mode of the symmetric form (S.13), the plane wave exact at the paces (S.1), light's index at the composed paces (S.2), the stress reading of a plane wave (S.7), the adiabatic invariant (S.14), the cross current of two standing records (S.17), Rabi's transfer and the resonance (S.16, S.43), the steady rotation that writes no light (S.42), the guide's lay (S.48 (3)), the stability under the dilation and the proofs of the theorems (S.48). Each row is tried inside its stated condition and outside it on the smallest configuration, exact in rationals and Gaussian rationals where the claim is exact, floats where the claim itself is a float; every step of the line is rule3.py's or proofs_ground.py's, every proof's identity a proofs_ module's check. The Row is counterexample_rows.py's; the registry is counterexamples.py's."""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import body_clicks  # noqa: E402
import counterexample_forms as forms  # noqa: E402
import counterexample_rows as rows  # noqa: E402
import proofs_audit  # noqa: E402
import proofs_band  # noqa: E402
import proofs_bodies  # noqa: E402
import proofs_paces  # noqa: E402
import rule3  # noqa: E402
from counterexample_rows import PORTS, Row  # noqa: E402
from proofs_form import weighted_form  # noqa: E402
from proofs_ground import (  # noqa: E402
    SEED,
    Gaussian,
    angle,
    angles,
    pairs,
    read,
    step_line,
)

TWO_NODE_BODY = [[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1]]  # the x Ports join the two Nodes, the rest fold
MATTER = (2, 3)


def read_matrix(
    arrivals: Sequence[Sequence[int]],
    clocks: Sequence[Fraction | int],
    factors: Sequence[Sequence[int]],
    num: int,
    den: int,
    gamma: int,
) -> tuple[list[list[Fraction]], list[Fraction]]:
    """The read matrix M of the line, a_next + a_before = M a_now (S.13): M_ij = R_ij / w summed over the Ports to j, M_ii carrying S_i / w; and the weights D_i = 1 / p_i^2 that make D M symmetric (Theorem 3)."""
    wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
    count = len(arrivals)
    matrix = [[Fraction(0)] * count for _ in range(count)]
    for i, ports in enumerate(arrivals):
        matrix[i][i] += selves[i] / wall
        for port, j in enumerate(ports):
            matrix[i][j] += reads[i][port] / wall
    return matrix, [1 / p**2 for p in paces]


def apply(matrix: Sequence[Sequence], vector: Sequence) -> list:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def record_is_the_top_mode() -> Row:
    """Section 7.2 ('The record is the top mode of Rule3's symmetric form at the paces, and dF / dphi = 2 lambda phi on the sphere is the fixed point's own equation, with 2 cos omega_b = 2 cos omega_0 - lambda'), S.13: on the two-Node body at the vacuum's paces the top mode (1, 1) has the eigenvalue 2 num / den exactly and the iteration of the read act from a random start approaches it as (1 / 3)^n exactly in rationals; on a chain of seven with a well in the clocks the iteration converges to a mode localised at the well with M phi = 2 cos omega_b phi to 10^-9, 2 cos omega_b above 2 cos omega_0 (bound), the gradient identity proofs_bodies' exact check; outside: the non-top mode (1, -1) as the start stays itself for ever (converges to none), a start one part in 10^6 off it converges to the top, named."""
    draw = random.Random(SEED)
    exact_top, approach = True, True
    for num, den in pairs(draw, 4):
        matrix, _ = read_matrix(TWO_NODE_BODY, [5, 5], [[5] * PORTS] * 2, num, den, 5)
        exact_top &= apply(matrix, [Fraction(1), Fraction(1)]) == [Fraction(2 * num, den)] * 2
        exact_top &= apply(matrix, [Fraction(1), Fraction(-1)]) == [
            Fraction(2 * num, 3 * den),
            Fraction(-2 * num, 3 * den),
        ]
        vector = [Fraction(draw.randint(1, 9)), Fraction(draw.randint(10, 19))]
        start = (vector[1] - vector[0]) / (vector[1] + vector[0])
        for n in range(1, 9):
            vector = apply(matrix, vector)
            approach &= (vector[1] - vector[0]) / (vector[1] + vector[0]) == start / 3**n
    gamma, num, den = 6, *MATTER
    clocks = [rule3.clock_pace(gamma, c) for c in (0, 0, 2, 4, 2, 0, 0)]
    matrix, weights = read_matrix(
        rule3.chain_arrivals(7), clocks, [[gamma] * PORTS] * 7, num, den, gamma
    )
    floats = [[float(v) for v in row] for row in matrix]
    phi = [1.0 + 0.1 * draw.random() for _ in range(7)]
    for _ in range(400):
        image = apply(floats, phi)
        norm = math.sqrt(sum(float(w) * v * v for w, v in zip(weights, image, strict=True)))
        phi = [v / norm for v in image]
    image = apply(floats, phi)
    eigenvalue = sum(float(w) * p * m for w, p, m in zip(weights, phi, image, strict=True)) / sum(
        float(w) * p * p for w, p in zip(weights, phi, strict=True)
    )
    residual = max(abs(m - eigenvalue * p) for m, p in zip(image, phi, strict=True))
    bound = eigenvalue > 2 * num / den
    localised = max(range(7), key=lambda i: abs(phi[i])) == 3
    gradient = proofs_bodies.check_the_functionals_gradient_is_the_fixed_points_equation()[0]
    matrix_2, _ = read_matrix(TWO_NODE_BODY, [5, 5], [[5] * PORTS] * 2, num, den, 5)
    stays = [Fraction(1), Fraction(-1)]
    for _ in range(12):
        stays = apply(matrix_2, stays)
    never_top = stays[0] == -stays[1]
    off = [1.0, -1.0 + 1e-6]
    for _ in range(60):
        off = apply([[float(v) for v in row] for row in matrix_2], off)
        off = [v / max(abs(x) for x in off) for v in off]
    reaches_top = abs(off[0] - off[1]) < 1e-9
    return Row(
        "The record is the top mode of Rule3s symmetric form at the p",
        exact_top and approach and residual < 1e-9 and bound and localised and gradient,
        never_top and reaches_top,
        f"two-Node body: (1, 1) at 2 num / den exactly, the iteration's approach (1 / 3)^n exact over 4 pairs; a 7-chain with a well: M phi = {eigenvalue:.6f} phi (2 cos omega_0 = {2 * num / den:.4f}), residual {residual:.1e}, the mode at the well; (1, -1) stays itself for ever, one part in 10^6 off it reaches the top",
    )


def plane_wave_exact_at_the_paces() -> Row:
    """S.1 (Eq. (4)): a plane wave at rational angles satisfies the line at uneven static paces exactly iff 2 w cos omega = S + 2 SUM_a R_a cos k_a, the two Links of an axis sharing one R_a (proofs_band's exact checks), and the axial long-wave coefficients 1 / 3 and k^4 / 12 are the series' (the residuals' orders); outside: a Link factor differing on the two Links of one axis, where the plane wave leaves a residual at every Node (the two-Link form fails) while the weighted form with the per-Port reads of S.32 stays conserved over the step, exactly."""
    identity = proofs_band.check_band_identity_of_a_plane_wave()[0]
    lorentz = proofs_band.check_band_at_a_pace_is_the_lorentz_form()[0]
    series = proofs_band.check_lights_speed_and_dispersion_series()[0]
    gamma, num, den = 7, *MATTER
    arrivals = rule3.chain_arrivals(8)
    factors = [[gamma] * PORTS for _ in arrivals]
    for i in range(8):
        factors[i][0] = gamma - 2  # the +x Link's factor, read the same from both ends
        factors[(i + 1) % 8][1] = gamma - 2
    factors[3][0] = factors[4][1] = (
        gamma - 4
    )  # one Link differing: the two Links of Node 4's axis differ
    wall, reads, selves, paces = read(arrivals, [gamma] * 8, factors, num, den, gamma)
    wave, rotation = angle(2, 1), angle(3, 1)
    now = [Fraction(10) * (wave**x).re for x in range(8)]
    before = [Fraction(10) * (wave**x * rotation).re for x in range(8)]
    stepped = step_line(arrivals, reads, selves, wall, now, before)
    residual = max(
        abs(stepped[i] + before[i] - 2 * rotation.re * now[i]) for i in range(8)
    )  # against the one-R_a form's a_next + a_before = 2 cos omega a_now
    uneven_fails = residual > 0 and stepped[4] + before[4] != 2 * rotation.re * now[4]
    form_before = weighted_form(reads, selves, wall, paces, arrivals, now, before, num, gamma)
    form_after = weighted_form(reads, selves, wall, paces, arrivals, stepped, now, num, gamma)
    return Row(
        "S.1",
        identity and lorentz and series,
        uneven_fails and form_before == form_after,
        "the plane wave's identity exact at random paces and angles, Eq. (4) the Lorentz form exactly, the series 1 / 3 and k^4 / 12 by the residuals' orders; two Link factors differing on one axis: the wave leaves a residual, the weighted form with per-Port reads is kept",
    )


def lights_index_at_the_composed_paces() -> Row:
    """S.2 (Section 3.4, 'light's index at a content'): at the composed paces p_0 = Gamma N, p_a = Gamma N^2 the band of [1, 1] has 1 - cos omega = (1 / 3) N^4 SUM_a (1 - cos k_a) exactly in rationals at N = 9 / 10, 1 / 2, 1 / 10 (rule3.coefficients), so light's speed at long wavelength is N^2 / sqrt 3 and its index N^-2 = e^(2U) (floats to 10^-6); outside the composition: the quadratic paces p_0 = Gamma (1 - U), p_a = Gamma (1 - 2U) give the index 1 / (1 - 2U), which agrees with e^(2U) at the first order and parts at the second (2U^2)."""
    draw = random.Random(SEED)
    exact = True
    gamma = 20
    for ratio in (Fraction(9, 10), Fraction(1, 2), Fraction(1, 10)):
        clock, link = gamma * ratio, gamma * ratio * ratio
        wall, reads, self_coefficient = rule3.coefficients(1, 1, gamma, clock, (link,) * 3)
        for _ in range(4):
            cosines = [angles(draw, 8)[7].re for _ in range(3)]
            cosine = (self_coefficient + 2 * sum(r * c for r, c in zip(reads, cosines, strict=True))) / (
                2 * wall
            )
            exact &= 1 - cosine == Fraction(1, 3) * ratio**4 * sum(1 - c for c in cosines)
    k, speeds = 1e-3, {}
    for n in (0.9, 0.5):
        omega = math.acos(rule3.dispersion_at_paces((k, 0.0, 0.0), 1, 1, 60, 60 * n, (60 * n * n,) * 3))
        speeds[n] = omega / k * math.sqrt(3)
    index_holds = all(abs(speeds[n] - n * n) < 1e-6 for n in speeds)
    first, orders_1 = proofs_paces.has_order(lambda u: math.exp(2 * u) - 1 / (1 - 2 * u), 2, step=0.05)
    second_order_coefficient = (1 / (1 - 2 * 0.01) - math.exp(2 * 0.01)) / 0.01**2
    return Row(
        "S.2",
        exact and index_holds,
        first and abs(second_order_coefficient - 2) < 0.1,
        f"1 - cos omega = N^4 (1 - cos k) / 3 exact at N = 9/10, 1/2, 1/10; speeds / (1 / sqrt 3) at N = 0.9, 0.5: {speeds[0.9]:.6f}, {speeds[0.5]:.6f}; the quadratic paces' index parts from e^2U at the second order, coefficient {second_order_coefficient:.3f} (orders {[round(o, 2) for o in orders_1]})",
    )


def stress_reading_of_a_plane_wave() -> Row:
    """S.7 (Section 4.3): on the plane wave b cos(k x + phi) the stress reading G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)) is -2 b^2 sin^2 k at every Node, exactly at rational angles and in floats at k = pi / 4 and pi / 3, the Node's h_a = G / 2 being -b^2 sin^2 k (the breaker text's '-A^2 sin^2 k' is h_a's value, G's is twice it); the cross reading on a wave with two components is -2 b^2 sin k_a sin k_b; outside: a packet's envelope, where G_aa varies along the chain."""
    draw = random.Random(SEED)
    exact = True
    for wave in angles(draw, 9):
        for phase in angles(draw, 5)[2:]:
            b = draw.randint(1, 20)
            level = {x: b * (phase * wave**x).re for x in range(-1, 4)}
            for i in (0, 1):
                g = level[i] * (level[i + 2] - level[i]) - level[i + 1] * (level[i + 1] - level[i - 1])
                exact &= g == -2 * b * b * wave.im**2
    in_floats = True
    for k in (math.pi / 4, math.pi / 3):
        for i in range(6):
            level = [math.cos(k * x + 0.3) for x in range(i - 1, i + 3)]
            g = level[1] * (level[3] - level[1]) - level[2] * (level[2] - level[0])
            in_floats &= abs(g + 2 * math.sin(k) ** 2) < 1e-12
    k_a, k_b = angle(3, 1), angle(4, 1)
    cross = True
    for phase in angles(draw, 4):
        # the wave b cos(k_a x + k_b y + phi) at (x, y) and its two-axis cross reading
        def level(x: int, y: int, phase=phase) -> Fraction:
            return 7 * (phase * k_a**x * k_b**y).re

        g_ab = level(0, 0) * (level(1, 1) - level(-1, 1)) - level(0, 1) * (level(1, 0) - level(-1, 0))
        cross &= g_ab == -2 * 49 * k_a.im * k_b.im
    envelope = [math.exp(-(((x - 10) / 4) ** 2)) * math.cos(math.pi / 4 * x) for x in range(24)]
    readings = [
        envelope[i] * (envelope[i + 2] - envelope[i])
        - envelope[i + 1] * (envelope[i + 1] - envelope[i - 1])
        for i in range(1, 21)
    ]
    return Row(
        "S.7",
        exact and in_floats and cross,
        max(readings) - min(readings) > 0.1,
        f"G_aa = -2 b^2 sin^2 k at every Node, exact at 9 rational angles and to 10^-12 at pi / 4, pi / 3; the cross reading -2 b^2 sin k_a sin k_b exact; an envelope's G varies from {min(readings):.3f} to {max(readings):.3f}",
    )


def adiabatic_invariant_and_the_drift() -> Row:
    """S.14 (Eq. (13)): the one-Node line a_next + a_before = 2 cos omega_t a_now with omega lowered from 0.841 to 0.600 over 10,000 intervals keeps A^2 sin omega = D / sin omega within 2 x 10^-4 while D falls by a quarter, and the midpoint-phase ansatz satisfies the line to the second order (proofs_bodies' check with the drift ratio of Eq. (13) exact); outside: omega jumping by 0.5 in one step, where D / sin omega moves by a named amount above ten percent."""
    held = proofs_bodies.check_the_adiabatic_invariant_and_the_drift()[0]
    start, end, intervals = 0.841, 0.600, 10_000
    cosines = [math.cos(start + (end - start) * t / intervals) for t in range(intervals + 1)]
    levels = body_clicks.one_node_line(1000.0, 1000.0 * math.cos(-start), cosines)
    invariants = [
        (levels[t] ** 2 - levels[t + 1] * levels[t - 1]) / math.sin(math.acos(c))
        for t, c in zip(range(1, len(levels) - 1), cosines, strict=True)
    ]
    slow = (max(invariants) - min(invariants)) / invariants[0]
    jumped = body_clicks.one_node_line(
        1000.0, 1000.0 * math.cos(-start), [math.cos(start)] * 50 + [math.cos(start - 0.5)] * 50
    )
    before_jump = (jumped[25] ** 2 - jumped[26] * jumped[24]) / math.sin(start)
    after_jump = (jumped[80] ** 2 - jumped[81] * jumped[79]) / math.sin(start - 0.5)
    fast = abs(after_jump / before_jump - 1)
    return Row(
        "S.14",
        held and slow < 2e-4,
        fast > 0.1,
        f"D / sin omega within {slow:.1e} over 10,000 slow intervals; a jump of 0.5 in one step moves it by {fast * 100:.1f} percent",
    )


def cross_current_of_two_standing_records() -> Row:
    """S.17 (Section 7.5): the current num (a_t b_(t-1) - a_(t-1) b_t) of two standing records at a Link's ends is the closed sum of cosines of (omega_1 -+ omega_2) t (proofs_bodies' exact check), and its mean over a common period is 0 for distinct non-aliased rotations (omega = 2 pi 3 / 60 and 2 pi 7 / 60, the exact period 60) to rounding; outside: omega_1 = omega_2, where the constant part -num A B sin(alpha - beta) sin omega stands, and the aliased omega_1 + omega_2 = 2 pi, where cos((omega_1 + omega_2) t) is 1 at every interval."""
    exact = proofs_bodies.check_the_cross_current_of_two_standing_records()[0]

    def mean_current(omega_1: float, omega_2: float, alpha: float, beta: float, period: int) -> float:
        total = 0.0
        for t in range(period):
            a_t, a_prev = math.cos(omega_1 * t + alpha), math.cos(omega_1 * (t - 1) + alpha)
            b_t, b_prev = math.cos(omega_2 * t + beta), math.cos(omega_2 * (t - 1) + beta)
            total += a_t * b_prev - a_prev * b_t
        return total / period

    distinct = abs(mean_current(2 * math.pi * 3 / 60, 2 * math.pi * 7 / 60, 0.4, 1.1, 60)) < 1e-12
    equal = mean_current(2 * math.pi * 7 / 60, 2 * math.pi * 7 / 60, 0.4, 1.1, 60)
    closed = -math.sin(0.4 - 1.1) * math.sin(2 * math.pi * 7 / 60)
    aliased = mean_current(2 * math.pi * 7 / 60, 2 * math.pi * 53 / 60, 0.4, 1.1, 60)
    return Row(
        "S.17",
        exact and distinct,
        abs(equal - closed) < 1e-12 and abs(equal) > 0.1 and abs(aliased) > 0.1,
        f"the closed form exact at rational angles; mean over a period 0 for distinct rotations; equal rotations {equal:.4f} (closed {closed:.4f}); aliased omega_1 + omega_2 = 2 pi: {aliased:.4f}",
    )


def two_node_transfer(epsilon: float, line: float, steps: int) -> float:
    """The largest invariant A^2 sin omega_a of the antisymmetric mode over the start's A^2 sin omega_s, on the two-Node body of [2, 3] driven at Node 0 by epsilon cos(line t) over `steps` intervals (body_clicks.rabi_transfer's recurrence, the line's right side by rule3's coefficients): 1 at a full transfer."""
    num, den = MATTER
    wall, reads, self_coefficient = rule3.coefficients(num, den)
    omega_s, omega_a = body_clicks.two_node_modes()
    before, now = [math.cos(-omega_s)] * 2, [1.0, 1.0]
    start = (
        (now[0] + now[1]) ** 2 / 2 * math.sin(omega_s)
    )  # the invariant A^2 sin omega of the start (S.14)
    best = 0.0
    for t in range(steps):
        drive = epsilon * math.cos(line * t)
        nxt = [
            rule3.numerator(
                now[0], [now[1], now[1], now[0], now[0], now[0], now[0]], reads, self_coefficient
            )
            / wall
            + drive * now[0]
            - before[0],
            rule3.numerator(
                now[1], [now[0], now[0], now[1], now[1], now[1], now[1]], reads, self_coefficient
            )
            / wall
            - before[1],
        ]
        c_before, c_now, c_next = (
            (before[0] - before[1]) / math.sqrt(2),
            (now[0] - now[1]) / math.sqrt(2),
            (nxt[0] - nxt[1]) / math.sqrt(2),
        )
        best = max(best, (c_now * c_now - c_next * c_before) / math.sin(omega_a) / start)
        before, now = now, nxt
    return best


def rabi_transfer_and_the_resonance() -> Row:
    """Section 7.4 ('A body with two bound modes omega_i, omega_j transfers between them at the line omega_j - omega_i at Rabi's rate'), S.16, S.43 and the clicks table's absorption line: on the two-Node body of [2, 3] driven at the difference line the first full transfer comes at T_pi = pi / (2 Omega_R) within two percent (body_clicks), the transferred share at the detuning 2 Omega_R is half the resonant one within 15 percent (the envelope g^2 / (g^2 + Delta^2 / 4) of S.43 (d), its generator exact in proofs_bodies), and the one-mode line at 2 omega_b grows at mu = epsilon / (4 sin omega_b) to four digits (S.16's witness); outside: the alias omega_b = pi / 2, where the drive cos(pi t) = (-1)^t grows the record at asinh(epsilon / 2) per interval against the averaging's epsilon / 4 (the two-step transfer matrix's trace -2 - epsilon^2, exact), and a drive epsilon = 1 beyond the rotating-wave condition, where T_pi misses by over ten percent."""
    ratio = body_clicks.rabi_transfer()[0]
    generator = proofs_bodies.check_the_two_mode_line_under_the_rotation()[0]
    parametric = proofs_bodies.check_the_resonant_growth_witness()[0]
    omega_s, omega_a = body_clicks.two_node_modes()
    rate = body_clicks.rabi_rate(body_clicks.RABI_EPSILON / 2, omega_s, omega_a)
    steps = int(3 * math.pi / (2 * rate))
    resonant = two_node_transfer(body_clicks.RABI_EPSILON, omega_a - omega_s, steps)
    detuned = two_node_transfer(body_clicks.RABI_EPSILON, omega_a - omega_s + 2 * rate, steps)
    half = abs(detuned / resonant - 0.5) < 0.15 and abs(resonant - 1) < 0.1
    epsilon = Fraction(1, 10)
    trace = (
        -(epsilon * epsilon) - 2
    )  # of [[-eps, -1], [1, 0]] [[eps, -1], [1, 0]], the two steps at cos omega_b = 0
    alias_growth = math.acosh(-float(trace) / 2) / 2  # per interval, asinh(eps / 2)
    alias = (
        abs(alias_growth - math.asinh(float(epsilon) / 2)) < 1e-12
        and alias_growth > 1.9 * float(epsilon) / 4
    )
    strong_rate = body_clicks.rabi_rate(1.0 / 2, omega_s, omega_a)
    strong = two_node_transfer(1.0, omega_a - omega_s, int(3 * math.pi / (2 * strong_rate)))
    return Row(
        "A body with two bound modes omegai omegaj transfers between",
        abs(ratio - 1) < 0.02 and generator and parametric and half,
        alias and abs(strong - 1) > 0.1,
        f"T_pi over the first full transfer {ratio:.4f}; transfer at resonance {resonant:.3f}, at Delta = 2 Omega_R {detuned:.3f}; mu = epsilon / (4 sin omega_b) to four digits; the alias grows at {alias_growth:.5f} = asinh(eps / 2) against eps / 4 = {float(epsilon) / 4}; epsilon = 1: transfer {strong:.2f}",
    )


def steady_rotation_writes_no_light() -> Row:
    """Table 1's row ('A body's clicks: no light from a steady rotation, light at a breathing body's beat') and S.42: a body at rest with the standing plane record z_i = phi_i e^(-i omega_b t) has W_i = phi_i^2 sin omega_b constant and every Link quantity g_ij = 0 at every interval, exactly in Gaussian rationals (proofs_bodies' check and a chain of five here); a breathing body z_i = phi_i (1 + epsilon cos Omega t) e^(-i omega_b t) writes W_i(t) = phi_i^2 sin omega_b [1 + epsilon (c_t + c_(t-1)) + epsilon^2 c_t c_(t-1)], the first-order part 2 epsilon cos(Omega / 2) cos(Omega (t - 1 / 2)) at the breathing's frequency, exactly; the monopole SUM W_i / p_i^2 is kept at static paces and the plain SUM W_i at uniform paces (proofs_audit's two-Node witness); outside uniform paces: the plain monopole moves, its change linear in the pace's variation (exactly twice as large at twice the variation)."""
    draw = random.Random(SEED)
    steady = proofs_bodies.check_what_a_body_writes_into_the_holder_of_the_sign()[0]
    rotation, breathing = angle(3, 1), angle(2, 1)
    phi = [Fraction(draw.randint(-9, 9)) for _ in range(5)]
    epsilon = Fraction(1, 7)
    constant, breathes = True, True
    for t in range(1, 6):
        z_now = [Gaussian(p, 0) * rotation ** (-t) for p in phi]
        z_before = [Gaussian(p, 0) * rotation ** (-(t - 1)) for p in phi]
        constant &= all(
            (z_now[i].conj() * z_before[i]).im == phi[i] ** 2 * rotation.im for i in range(5)
        )
        constant &= all((z_now[i].conj() * z_now[j]).im == 0 for i in range(5) for j in range(5))
        c_now, c_before = (breathing**t).re, (breathing ** (t - 1)).re
        scaled_now = [z * (1 + epsilon * c_now) for z in z_now]
        scaled_before = [z * (1 + epsilon * c_before) for z in z_before]
        for i in range(5):
            wronskian = (scaled_now[i].conj() * scaled_before[i]).im
            rest = phi[i] ** 2 * rotation.im
            breathes &= wronskian == rest * (
                1 + epsilon * (c_now + c_before) + epsilon**2 * c_now * c_before
            )
            breathes &= wronskian - rest * (1 + epsilon**2 * c_now * c_before) == rest * epsilon * (
                c_now + c_before
            )
    weighted_two, moved_two = proofs_audit.monopole_at_the_two_node_witness((Fraction(1), Fraction(2)))
    weighted_one, moved_one = proofs_audit.monopole_at_the_two_node_witness((Fraction(1), Fraction(1)))

    def plain_change(variation: Fraction) -> Fraction:
        """The plain monopole's change over one step at the paces squared (1, 1 + variation), one witness."""
        a = Fraction(3, 4)
        reads = ((Fraction(0), a), (a * (1 + variation), Fraction(0)))
        selves = (Fraction(1, 3), Fraction(-2, 3))
        z_now = [Gaussian(2, -3), Gaussian(1, 4)]
        z_before = [Gaussian(-1, 2), Gaussian(3, 1)]
        z_next = [z_now[i] * selves[i] + z_now[1 - i] * reads[i][1 - i] - z_before[i] for i in range(2)]
        return sum((z_next[i].conj() * z_now[i]).im for i in range(2)) - sum(
            (z_now[i].conj() * z_before[i]).im for i in range(2)
        )

    linear = plain_change(Fraction(1, 50)) == 2 * plain_change(Fraction(1, 100)) != 0
    return Row(
        "tab:results: A bodys clicks no light from a steady rotation light at a br",
        steady and constant and breathes and weighted_two and weighted_one and moved_one == 0,
        moved_two > 0 and linear,
        f"W_i constant and g_ij = 0 over 5 intervals of a 5-Node standing record; the breathing body's W carries epsilon (c_t + c_(t-1)) at Omega exactly; the weighted monopole kept at paces (1, 2), the plain moved in {moved_two} of 20 witnesses, 0 at uniform paces, its change linear in the variation",
    )


def guides_lay_of_one_quantum() -> Row:
    """The clicks table's emission row and S.48 (3): on a width-one guide one quantum is laid at SUM_t A_t^2 = (2 / 3) T sin k (proofs_bodies' exact identities), and the increments' own squares SUM_t A_t^2 cos^2(Omega t) sum to half of it for an envelope narrow in band against Omega (a Gaussian of width 40 intervals at Omega = 0.8411: within 10^-3 of one half); outside: the short envelope A = (1, 0, 2, 0, 1) at Omega = pi / 2, whose increments' squares sum to all of SUM A_t^2 and not half."""
    identities = proofs_bodies.check_the_guides_lay()[0]
    omega = math.acos(2 / 3)
    envelope = [math.exp(-(((t - 200) / 40) ** 2)) for t in range(400)]
    narrow = sum(a * a * math.cos(omega * t) ** 2 for t, a in enumerate(envelope)) / sum(
        a * a for a in envelope
    )
    short = (1, 0, 2, 0, 1)
    short_ratio = Fraction(
        sum(a * a * (round(math.cos(math.pi / 2 * t)) ** 2) for t, a in enumerate(short)),
        sum(a * a for a in short),
    )
    return Row(
        "tab:clicks: Emission",
        identities and abs(narrow - 0.5) < 1e-3,
        short_ratio != Fraction(1, 2),
        f"one quantum at SUM A_t^2 = (2 / 3) T sin k exact; the narrow envelope's increments' squares {narrow:.5f} of the sum; A = (1, 0, 2, 0, 1) at pi / 2: {short_ratio}",
    )


def stability_under_the_dilation() -> Row:
    """Table 1's row ('The stability of a body under the dilation, to first order in the well') and the proposition of Section 7.2: the virial 2 K = SUM sigma_r s_r W_r and the second variation F''(1) = SUM sigma_r s_r (2 - s_r) W_r along the dilation at power-law kernels, Pekar's minimum, the hollow's barrier (proofs_bodies' exact checks); outside the dilation: the Hessian's mixed block H = [[1, 2], [2, 1]] has the eigenvalues 3 and -1, indefinite, so no full minimum is claimed."""
    virial = proofs_bodies.check_the_stable_body_theorem()[0]
    barrier = proofs_bodies.check_the_hollows_barrier()[0]
    block = ((Fraction(1), Fraction(2)), (Fraction(2), Fraction(1)))
    trace = block[0][0] + block[1][1]
    determinant = block[0][0] * block[1][1] - block[0][1] * block[1][0]
    root = Fraction(math.isqrt(int(trace * trace - 4 * determinant)))
    eigenvalues = sorted(((trace - root) / 2, (trace + root) / 2))
    return Row(
        "tab:results: The stability of a body under the dilation to first order in",
        virial and barrier,
        determinant < 0 and eigenvalues == [Fraction(-1), Fraction(3)],
        f"the virial and F''(1) = SUM sigma s (2 - s) W exact, Pekar's minimum, the barrier's roots; the mixed block [[1, 2], [2, 1]] has the eigenvalues {[str(e) for e in eigenvalues]}: indefinite",
    )


def proofs_of_the_theorems() -> Row:
    """S.48, the proofs of Theorems 1 to 3 and the proposition: Theorem 1's bijection on random states, Theorem 2's linear acts, Theorem 3's weighted form by the one-step algebra, the proposition's virial and dilation with the mixed block, and (3) the guide's lay with the increments' half, each its own row here, composed."""
    parts = [
        rows.the_step_is_a_bijection(),
        forms.acts_form_no_product_of_levels(),
        forms.weighted_form_is_exact_at_static_paces(),
        stability_under_the_dilation(),
        guides_lay_of_one_quantum(),
    ]
    return Row(
        "S.48",
        all(p.holds_inside for p in parts),
        all(p.breaks_outside is not False for p in parts),
        "Theorem 1's bijection, Theorem 2's linear acts, Theorem 3's weighted form, the proposition's virial with the mixed block and the guide's lay: each row green",
    )
