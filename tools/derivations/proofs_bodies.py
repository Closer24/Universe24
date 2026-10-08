"""The bodies' and the clicks' checks (ALGEBRA.md, The functional and the dilation, The surplus leaves, The integer budget of a derived row, The count is the record's share; the paper's Theorem 4, Eqs. (12), (13); the supplement's S.6, S.13, S.14, S.16, S.17, S.42, S.43, S.44, S.45, S.46, S.47, S.48, S.63): the stable body's virial and second variation, the barrier's roots, the functional's gradient as the fixed point's equation, the adiabatic invariant and the count's drift, the body's click share, Schroedinger's slow limit with its three conditions, the resonance's exponents and its stepped growth, the cross current, the budget's walk, the guide's lay, what a body writes, the two-mode line under the rotation, the two forces, the nuclear threshold, the atom's self-term, the equivalence between families, the cloud's settling and the non-negative total share; exact in Fractions and Gaussian rationals, the expansions by the residual's order, the hand proofs' witnesses recomputed.

Usage: `python tools/derivations/proofs_bodies.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402, F401  (the derivations' root; tests/test_derivations_lean_on_rule3_alone.py)
from proofs_ground import (
    SEED,
    Check,
    Gaussian,
    angles,
    box_arrivals,
    draw_angle,
    has_order,
    pairs,
    run,
)  # noqa: E402


def check_the_stable_body_theorem() -> Check:
    """Theorem 4 (the paper's Section 7.2; ALGEBRA.md, The functional and the dilation; S.48): F(R) = K / R^2 - SUM_r sigma_r W_r R^(-s_r); F'(1) = 0 is -2 K + SUM_r sigma_r s_r W_r = 0, the virial 2 K = SUM_r sigma_r s_r W_r, and F''(1) = 6 K - SUM_r sigma_r s_r (s_r + 1) W_r = SUM_r sigma_r s_r (2 - s_r) W_r under it; s (2 - s) is +1 at s = 1, 0 at s = 2 and -3 at s = 3; Pekar's body, F = a / R^2 - c / R, has the one critical point R = 2 a / c, a minimum (F'' = c^4 / (8 a^3)) for every mass; the Taylor remainder F(1 + h) - F(1) - (1 / 2) F''(1) h^2 of the third order at random power-law kernels with K set by the virial, F'' exact, Pekar's exact."""
    draw = random.Random(SEED)
    for _ in range(12):
        rows = [
            (draw.choice((1, -1)), draw.choice((1, 2, 3)), Fraction(draw.randint(1, 20)))
            for _ in range(draw.randint(1, 4))
        ]
        kinetic = sum(Fraction(sigma * s) * w for sigma, s, w in rows) / 2
        if kinetic <= 0:
            continue
        second = sum(Fraction(sigma * s * (2 - s)) * w for sigma, s, w in rows)
        if second != 6 * kinetic - sum(Fraction(sigma * s * (s + 1)) * w for sigma, s, w in rows):
            return False, {"F''": rows}

        def functional(r: Fraction, kinetic: Fraction = kinetic, rows: list = rows) -> Fraction:
            return kinetic / r**2 - sum(sigma * w / r**s for sigma, s, w in rows)

        held, orders = has_order(
            lambda h, second=second: float(
                functional(1 + Fraction(h)) - functional(Fraction(1)) - second * Fraction(h) ** 2 / 2
            ),
            3,
            step=0.05,
        )
        if not held:
            return False, {"rows": rows, "orders": orders}
    signs = {s: s * (2 - s) for s in (1, 2, 3)}
    a, c = Fraction(7), Fraction(3)
    pekar_root = 2 * a / c
    derivative = -2 * a / pekar_root**3 + c / pekar_root**2
    second_pekar = 6 * a / pekar_root**4 - 2 * c / pekar_root**3
    return signs == {1: 1, 2: 0, 3: -3} and derivative == 0 and second_pekar == c**4 / (
        8 * a**3
    ) and second_pekar > 0, {"s (2 - s)": signs, "Pekar's F'' at 2 a / c": second_pekar}


def check_the_hollows_barrier() -> Check:
    """7.2 (b); S.13's hollow's barrier: F(R) = a / R^2 - b / R^3 - c / R has F'(R) = (c R^2 - 2 a R + 3 b) / R^4, vanishing at R_+- = (a +- sqrt(a^2 - 3 b c)) / c, two critical points where a^2 > 3 b c and none where 3 b c > a^2 (the collapse); at a root F'' = 2 (a R - 3 b) / R^5, positive at R_+ >= a / c > 3 b / a and negative at R_- = 3 b / (a + sqrt(a^2 - 3 b c)) < 3 b / a, so the wide point is the minimum and the narrow the saddle; exact rationals at (a, b, c) = (5, 1, 3), the roots 3 and 1 / 3, and the derivative identity at random points."""
    draw = random.Random(SEED)
    for _ in range(20):
        a, b, c = (Fraction(draw.randint(1, 30)) for _ in range(3))
        r = Fraction(draw.randint(1, 50), draw.randint(1, 9))
        if -2 * a / r**3 + 3 * b / r**4 + c / r**2 != (c * r * r - 2 * a * r + 3 * b) / r**4:
            return False, {"F' identity": (a, b, c, r)}
    a, b, c = Fraction(5), Fraction(1), Fraction(3)
    roots = ((a + 4) / c, (a - 4) / c)
    if roots != (Fraction(3), Fraction(1, 3)) or any(c * r * r - 2 * a * r + 3 * b != 0 for r in roots):
        return False, {"roots": roots}
    curvatures = [6 * a / r**4 - 12 * b / r**5 - 2 * c / r**3 for r in roots]
    if any(
        curvature != 2 * (a * r - 3 * b) / r**5 for curvature, r in zip(curvatures, roots, strict=True)
    ):
        return False, {"F'' at the roots": curvatures}
    wide_minimum = curvatures[0] > 0 and roots[0] >= a / c > 3 * b / a
    narrow_saddle = curvatures[1] < 0 and roots[1] == 3 * b / (a + 4) < 3 * b / a
    a2, b2, c2 = Fraction(2), Fraction(1), Fraction(3)  # 3 b c = 9 > a^2 = 4: no critical point
    no_root = all(c2 * r * r - 2 * a2 * r + 3 * b2 > 0 for r in (Fraction(k, 10) for k in range(1, 200)))
    return wide_minimum and narrow_saddle and no_root, {"roots": roots, "F'' at the roots": curvatures}


def polynomial_derivative(function, point: list[Fraction], index: int, degree: int = 4) -> Fraction:
    """The exact partial derivative of a polynomial of degree at most `degree` at a rational point, by interpolation in the step h: F(point + h e_index) at h = 0 .. degree determines the polynomial in h, whose linear coefficient is the derivative."""
    samples = []
    for h in range(degree + 1):
        shifted = list(point)
        shifted[index] += h
        samples.append(function(shifted))
    # Newton's forward differences at h = 0: the derivative is SUM_(j >= 1) (-1)^(j + 1) Delta^j f(0) / j
    differences = list(samples)
    derivative = Fraction(0)
    for j in range(1, degree + 1):
        differences = [differences[i + 1] - differences[i] for i in range(len(differences) - 1)]
        derivative += Fraction((-1) ** (j + 1), j) * differences[0]
    return derivative


def check_the_functionals_gradient_is_the_fixed_points_equation() -> Check:
    """S.13; ALGEBRA.md, The functional: F[phi] = (num / (3 den)) SUM over Links (phi_i - phi_j)^2 - (2 g / Gamma) SUM_r sigma_r (M / E_r) SUM_ij phi_i^2 G_r,ij phi_j^2, each well counted once (Hartree's form); its gradient is dF / dphi_i = (2 num / (3 den)) (-Delta^2 phi)_i - (8 g / Gamma) Phi_i phi_i with Phi_i = SUM_r sigma_r (M / E_r) SUM_j G_r,ij phi_j^2, the symmetric kernel emission the factor 2 g in F the 4 g in the gradient; so dF / dphi = -2 (M(Phi) phi - 2 cos omega_0 phi) with (M(Phi) phi)_i = 2 cos omega_0 phi_i + (4 g / Gamma) Phi_i phi_i - (num / (3 den)) (-Delta^2 phi)_i, and dF / dphi = 2 lambda phi on the sphere is the fixed point's equation with lambda = 2 cos omega_0 - 2 cos omega_b; exact rationals on a periodic chain of five with two symmetric kernels, the derivative by exact interpolation of the quartic."""
    draw = random.Random(SEED)
    count = 5
    for num, den in pairs(draw, 4):
        gamma = Fraction(draw.randint(10, 100))
        g = 1 - Fraction(num, den)
        rows = []
        for _ in range(2):
            kernel = [[Fraction(0)] * count for _ in range(count)]
            for i in range(count):
                for j in range(i, count):
                    kernel[i][j] = kernel[j][i] = Fraction(draw.randint(-5, 9), 7)
            rows.append(
                (
                    draw.choice((1, -1)),
                    Fraction(draw.randint(1, 50)),
                    Fraction(draw.randint(1, 9)),
                    kernel,
                )
            )

        def well(phi: list[Fraction], rows: list = rows) -> list[Fraction]:
            return [
                sum(
                    sigma * mass / weight * sum(kernel[i][j] * phi[j] ** 2 for j in range(count))
                    for sigma, mass, weight, kernel in rows
                )
                for i in range(count)
            ]

        def functional(
            phi: list[Fraction],
            rows: list = rows,
            num: int = num,
            den: int = den,
            g: Fraction = g,
            gamma: Fraction = gamma,
        ) -> Fraction:
            pressure = Fraction(num, 3 * den) * sum(
                (phi[i] - phi[(i + 1) % count]) ** 2 for i in range(count)
            )
            wells = sum(
                sigma
                * mass
                / weight
                * sum(
                    phi[i] ** 2 * kernel[i][j] * phi[j] ** 2 for i in range(count) for j in range(count)
                )
                for sigma, mass, weight, kernel in rows
            )
            return pressure - 2 * g / gamma * wells

        phi = [Fraction(draw.randint(-9, 9), 4) for _ in range(count)]
        potential = well(phi)
        for i in range(count):
            laplacian = (
                2 * phi[i] - phi[(i + 1) % count] - phi[(i - 1) % count]
            )  # -Delta^2 phi on the chain with the four folded Ports
            gradient = polynomial_derivative(functional, phi, i)
            claimed = Fraction(2 * num, 3 * den) * laplacian - 8 * g / gamma * potential[i] * phi[i]
            read_act = (
                2 * Fraction(num, den) * phi[i]
                + 4 * g / gamma * potential[i] * phi[i]
                - Fraction(num, 3 * den) * laplacian
            )
            if gradient != claimed or gradient != -2 * (read_act - 2 * Fraction(num, den) * phi[i]):
                return False, {"pair": (num, den), "Node": i, "gradient": gradient, "claimed": claimed}
    return True, {"pairs": 4, "Nodes": count}


def ansatz_residual(ramp: float, midpoint: bool) -> float:
    """The line's residual a_(t+1) + a_(t-1) - 2 cos omega_t a_t at t = 10 for the slowly varying ansatz a_t = C cos(Phi_t) / sqrt(sin omega_t) under the ramp omega_t = 0.841 - ramp t, with the phase's increment Phi_(t+1) - Phi_t the midpoint (omega_t + omega_(t+1)) / 2 or, as S.14 prints it, the sum SUM_(s <= t) omega_s (the increment omega_(t+1))."""

    def omega_at(t: int) -> float:
        return 0.841 - ramp * t

    def phase(t: int) -> float:
        if midpoint:
            return sum((omega_at(s) + omega_at(s + 1)) / 2 for s in range(0, t))
        return sum(omega_at(s) for s in range(1, t + 1))

    def level(t: int) -> float:
        return math.cos(phase(t)) / math.sqrt(math.sin(omega_at(t)))

    return level(11) + level(9) - 2 * math.cos(omega_at(10)) * level(10)


def check_s14s_plain_phase_fails_at_the_first_order() -> Check:
    """S.14 since d7e97674: "the ansatz a_t = C cos(theta_t + phi) / sqrt(sin omega_t) with the midpoint phase theta_t = SUM_(s <= t) (omega_s + omega_(s+1)) / 2 satisfies the line to the second order in omega_(t+1) - omega_t (the phase SUM_(s <= t) omega_s fails at the first order)"; at 2836519e the plain phase was printed with the first order, a finding of this inventory then: the line's residual with the plain phase, the increment omega_(t+1), is of the first order in the ramp (-Delta cos Phi sin omega) and with the midpoint increment of the second, by the residual's order at halving."""
    plain_first, orders_plain = has_order(
        lambda ramp: ansatz_residual(ramp, midpoint=False), 1, step=0.001
    )
    midpoint_second, orders_midpoint = has_order(
        lambda ramp: ansatz_residual(ramp, midpoint=True), 2, step=0.001
    )
    return plain_first and midpoint_second, {
        "orders of the residual with the plain phase": orders_plain,
        "with the midpoint phase": orders_midpoint,
    }


def check_the_adiabatic_invariant_and_the_drift() -> Check:
    """S.14; Eq. (13); the paper's invariant_check.py: at fixed omega the form D_t = a_t^2 - a_(t+1) a_(t-1) = a_t^2 + a_(t-1)^2 - 2 cos omega a_t a_(t-1) is conserved and equals A^2 sin^2 omega for a_t = A cos(omega t + phi); the step is a map of determinant 1 whose orbits are the ellipses D = const, of area pi D / sin omega (the form's determinant 1 - cos^2 omega = sin^2 omega); a slow change of omega keeps the area, so D / sin omega = A^2 sin omega is the adiabatic invariant, and the ansatz a_t = C cos(SUM_(s <= t) omega_s + phi) / sqrt(sin omega_t) satisfies the line to the first order in omega_(t+1) - omega_t (the residual of the second order in the ramp); the recurrence stepped 20,000 intervals with omega lowered from 0.841 to 0.600 keeps D / sin omega within 4 x 10^-5 while D falls by a quarter (a witness, the paper's own check); with A^2 sin omega_b fixed the share (Gamma^2 / p_i^2) A^2 sin^2 omega_b / T gives N(t_2) / N(t_1) = [sin omega_b(t_2) / sin omega_b(t_1)] [p_i^2(t_1) / p_i^2(t_2)]; exact rationals, the orders and the witness recomputed."""
    draw = random.Random(SEED)
    for rotation in angles(draw, 10):
        c = rotation.re
        a_before, a_now = Fraction(draw.randint(-50, 50)), Fraction(draw.randint(-50, 50))
        form = a_now**2 + a_before**2 - 2 * c * a_now * a_before
        for _ in range(8):
            a_next = 2 * c * a_now - a_before
            if a_now**2 - a_next * a_before != form:
                return False, {"D moved": rotation}
            a_before, a_now = a_now, a_next
        amplitude, phase = draw.randint(1, 30), draw_angle(draw)
        a_t, a_prev = amplitude * phase.re, amplitude * (phase * rotation.conj()).re
        if a_t**2 + a_prev**2 - 2 * c * a_t * a_prev != amplitude**2 * rotation.im**2:
            return False, {"A^2 sin^2": rotation}
        if 1 - c * c != rotation.im**2:
            return False, {"determinant": rotation}
    held, orders = has_order(lambda ramp: ansatz_residual(ramp, midpoint=True), 2, step=0.001)
    omega_0 = 0.841
    a_before, a_now = math.cos(0.3 - omega_0), math.cos(0.3)
    start, worst, ratio = None, 0.0, 1.0
    for t in range(20000):
        omega = omega_0 + (0.600 - omega_0) * t / 19999
        a_next = 2 * math.cos(omega) * a_now - a_before
        d = a_now * a_now - a_next * a_before
        invariant = d / math.sin(omega)
        start = (invariant, d) if start is None else start
        worst, ratio = max(worst, abs(invariant / start[0] - 1)), d / start[1]
        a_before, a_now = a_now, a_next
    s1, s2, p1, p2 = Fraction(3, 5), Fraction(4, 5), Fraction(7), Fraction(5)
    a1_squared = Fraction(13)
    a2_squared = a1_squared * s1 / s2  # A^2 sin omega fixed
    drift = (a2_squared * s2 * s2 / p2**2) / (a1_squared * s1 * s1 / p1**2)
    return held and worst < 4e-5 and 0.7 < ratio < 0.8 and drift == (s2 / s1) * (p1**2 / p2**2), {
        "ansatz residual orders": orders,
        "D / sin omega drift and D's fall": (worst, ratio),
        "drift ratio": drift,
    }


def check_the_bodys_click_share() -> Check:
    """S.14, the body's click: the share a transition takes, T (sin omega_j - sin omega_i), is T sin(omega_j - omega_i) [1 - omega_i omega_j / 2 + O(omega^4)] by sin omega_j - sin omega_i = 2 cos((omega_i + omega_j) / 2) sin((omega_j - omega_i) / 2): one photon's share T sin omega_L at the line omega_L = omega_j - omega_i, to a relative omega_0^2 / 2 at nature's gap; the identity exact at rational half-angles, the expansion's order (the absolute residual of the fifth order along omega_i = t, omega_j = 2 t), the far end omega_i = 1, omega_j = 2."""
    draw = random.Random(SEED)
    for half_i in angles(draw, 8):
        for half_j in angles(draw, 8)[1:]:
            full_i, full_j = half_i * half_i, half_j * half_j
            left = full_j.im - full_i.im
            right = 2 * (half_i * half_j).re * (half_j * half_i.conj()).im
            if left != right:
                return False, {"identity": (half_i, half_j)}
    held, orders = has_order(
        lambda t: (math.sin(2 * t) - math.sin(t)) - math.sin(t) * (1 - 2 * t * t / 2), 5, step=0.2
    )
    far = (math.sin(2.0) - math.sin(1.0), math.sin(1.0) * (1 - 1.0 * 2.0 / 2))
    return held, {"orders": orders, "far end omega = 1, 2 (exact, first order)": far}


def check_schroedingers_slow_limit() -> Check:
    """S.63: with a_t = Re[psi_t e^(-i omega_0 t)], psi_(t +- 1) = psi +- psi' + psi'' / 2, a_next + a_before = Re[e^(-i omega_0 t) (2 cos omega_0 psi - 2 i sin omega_0 psi' + cos omega_0 psi'')] exactly, the right side Re[e^(-i omega_0 t) (2 cos omega_0 psi + (num / (3 den)) Delta psi)] since (num / (3 den)) 6 = 2 cos omega_0; dropping psi'', i psi' = -Delta psi / (2 m*) with m* = 3 den sin omega_0 / num = 3 tan omega_0; the three conditions: (ii) the band's k^4 term of relative size k^2 / 12 along an axis, (iii) psi'' against 2 sin omega_0 psi' of relative size (omega - omega_0) / (2 tan omega_0), below (omega - omega_0) / omega_0 = k^2 / (2 m* omega_0); the slow limit's dispersion omega_0 + k^2 / (2 m*) against the exact band to the fourth order; the expansion exact in Gaussian rationals, the rest by the residual's order."""
    draw = random.Random(SEED)
    for rotation in angles(draw, 10):
        psi = Gaussian(draw.randint(-9, 9), draw.randint(-9, 9))
        first = Gaussian(draw.randint(-9, 9), draw.randint(-9, 9))
        second = Gaussian(draw.randint(-9, 9), draw.randint(-9, 9))
        for phase in angles(draw, 7):  # e^(-i omega_0 t)
            left = ((psi + first + second / 2) * phase * rotation.conj()).re + (
                (psi - first + second / 2) * phase * rotation
            ).re
            right = (
                phase
                * (
                    psi * (2 * rotation.re)
                    - Gaussian(0, 1) * first * (2 * rotation.im)
                    + second * rotation.re
                )
            ).re
            if left != right:
                return False, {"expansion identity": (rotation, phase)}
    for num, den in pairs(draw, 6):
        c = Fraction(num, den)
        omega_0 = math.acos(num / den)
        if abs(3 * den * math.sin(omega_0) / num - 3 * math.tan(omega_0)) > 1e-9:
            return False, {"inertia": (num, den)}
        if Fraction(num, 3 * den) * 6 != 2 * c:
            return False, {"band at k = 0": (num, den)}
    num, den = 2, 3
    omega_0 = math.acos(num / den)
    inertia = 3 * math.tan(omega_0)
    held, orders = has_order(
        lambda k: math.acos(num / (3 * den) * (2 + math.cos(k))) - omega_0 - k * k / (2 * inertia),
        4,
        step=0.3,
    )
    held_band, orders_band = has_order(
        lambda k: ((1 - math.cos(k)) - k * k / 2) / (k * k / 2) + k * k / 12, 4, step=0.4
    )
    delta = 0.05
    ratio_iii = math.cos(omega_0) * delta**2 / (2 * math.sin(omega_0) * delta)
    condition_iii = (
        abs(ratio_iii - delta / (2 * math.tan(omega_0))) < 1e-15 and ratio_iii < delta / omega_0
    )
    return held and held_band and condition_iii, {
        "dispersion orders": orders,
        "k^2 / 12 orders": orders_band,
        "m* at [2, 3]": inertia,
    }


def check_the_resonances_exponents() -> Check:
    """S.16: the antilinear map z' = -i epsilon e^(i theta) conj(z) / (4 sin omega_b) has the real eigenvalues +- mu, mu = epsilon / (4 sin omega_b), on two lines of the plane, and detuned by Delta the system zeta' = -i (Delta / 2) zeta - i mu e^(i theta) conj(zeta) has the exponents +- sqrt(mu^2 - Delta^2 / 4): growth for |Delta| < 2 mu, a full width epsilon / sin omega_b; the real 2 x 2 generator squares to (mu^2 - Delta^2 / 4) times the identity, exactly at rational mu, Delta and theta."""
    draw = random.Random(SEED)
    for unit in angles(draw, 10):
        c, s = unit.re, unit.im
        mu, delta = Fraction(draw.randint(1, 20), 7), Fraction(draw.randint(-20, 20), 5)
        matrix = (
            (mu * s, delta / 2 - mu * c),
            (-delta / 2 - mu * c, -mu * s),
        )  # (x, y)' for zeta = x + i y
        square = tuple(
            tuple(sum(matrix[i][k] * matrix[k][j] for k in range(2)) for j in range(2)) for i in range(2)
        )
        if square != ((mu * mu - delta * delta / 4, 0), (0, mu * mu - delta * delta / 4)):
            return False, {"generator squared": square}
    epsilon, sine = Fraction(13, 1000), Fraction(7, 10)
    mu = epsilon / (4 * sine)
    return 4 * mu == epsilon / sine, {
        "full width 4 mu against epsilon / sin omega_b": (4 * mu, epsilon / sine)
    }


def check_the_resonant_growth_witness() -> Check:
    """S.16's check (witness only): the recurrence a_(t+1) + a_(t-1) = [2 cos omega_b + epsilon cos(omega_L t + theta)] a_t stepped 20,000 intervals at 2 cos omega_b = 1.4317 and epsilon = 0.013 grows at 0.004653 to 0.004656 per interval over seven modulation phases, the formula's first-order mu = epsilon / (4 sin omega_b) = 0.004654 to four digits; the growth read from the form D_t = a_t^2 + a_(t-1)^2 - 2 cos omega_b a_t a_(t-1), which grows as e^(2 mu t)."""
    two_cosine, epsilon = 1.4317, 0.013
    omega_b = math.acos(two_cosine / 2)
    mu = epsilon / (4 * math.sin(omega_b))
    rates = []
    for phase in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        a_before, a_now = 1.0, math.cos(omega_b)
        forms = {}
        for t in range(20001):
            if t in (10000, 20000):
                forms[t] = a_now * a_now + a_before * a_before - two_cosine * a_now * a_before
            a_before, a_now = (
                a_now,
                (two_cosine + epsilon * math.cos(2 * omega_b * t + phase)) * a_now - a_before,
            )
        rates.append(math.log(forms[20000] / forms[10000]) / (2 * 10000))
    return all(abs(rate - mu) < 3e-6 for rate in rates) and round(mu, 6) == 0.004654, {
        "stepped growth rates": [round(r, 6) for r in rates],
        "mu": mu,
    }


def check_the_cross_current_of_two_standing_records() -> Check:
    """S.17: the current num (a_t b_(t-1) - a_(t-1) b_t) of two standing records A cos(omega_1 t + alpha), B cos(omega_2 t + beta) at a Link's ends is (num A B / 2) [cos((omega_1 - omega_2) t + alpha - beta + omega_2) - cos((omega_1 - omega_2) t + alpha - beta - omega_1) + cos((omega_1 + omega_2) t + alpha + beta - omega_2) - cos((omega_1 + omega_2) t + alpha + beta - omega_1)], a sum of cosines of (omega_1 - omega_2) t and (omega_1 + omega_2) t with a constant part only when omega_1 = omega_2; exact at rational angles."""
    draw = random.Random(SEED)
    for w1 in angles(draw, 7):
        for w2 in angles(draw, 7)[1:]:
            alpha, beta = draw_angle(draw), draw_angle(draw)
            amplitude_a, amplitude_b, num = draw.randint(1, 9), draw.randint(1, 9), draw.randint(1, 5)
            for t in range(0, 4):
                a_t, a_prev = amplitude_a * (alpha * w1**t).re, amplitude_a * (alpha * w1 ** (t - 1)).re
                b_t, b_prev = amplitude_b * (beta * w2**t).re, amplitude_b * (beta * w2 ** (t - 1)).re
                current = num * (a_t * b_prev - a_prev * b_t)
                difference = (w1 * w2.conj()) ** t * alpha * beta.conj()
                total = (w1 * w2) ** t * alpha * beta
                closed = Fraction(num * amplitude_a * amplitude_b, 2) * (
                    (difference * w2).re
                    - (difference * w1.conj()).re
                    + (total * w2.conj()).re
                    - (total * w1.conj()).re
                )
                if current != closed:
                    return False, {"t": t, "current": current, "closed": closed}
    return True, {"witnesses": 7 * 6 * 4}


def check_the_budgets_walk() -> Check:
    """The integer budget of a derived row (ALGEBRA.md, The method of derivation): per band mode the deviation obeys D_(t+1) - 2 cos omega_k D_t + D_(t-1) = rho_t - rho_(t+1), whose response is SUM_m (G_m - G_(m-1)) rho_(t-m) with G_m = sin(omega_k (m + 1)) / sin omega_k, the kernel cos(omega_k (m + 1 / 2)) / cos(omega_k / 2) of mean square 1 / (1 + cos omega_k), so the walk is sqrt(n / (12 (1 + cos omega_k))) levels: 0.224 sqrt n at [2, 3]'s rest, 0.209 sqrt n at light's k = pi / 4 and 0.289 sqrt n at a band's centre; at the two roots the first remainder's coefficient G_(t-1) is t at the uniform mode and (-1)^t t at the checkerboard; the kernel identity exact at rational half-angles, 2 cos^2(omega / 2) = 1 + cos omega exact, the double roots exact in integers, the numbers recomputed; the zone means (0.354, 0.259, 0.226 sqrt n for the massless row over a cube, a plane and a chain, 0.302 for [2, 3] over a cube) by quadrature, a witness."""
    draw = random.Random(SEED)
    for half in angles(draw, 10):
        if half.re == 0 or (half * half).im == 0:
            continue
        full = half * half
        for m in range(0, 6):
            response = ((full ** (m + 1)).im - (full**m).im) / full.im  # G_m - G_(m-1)
            kernel = (half ** (2 * m + 1)).re / half.re
            if response != kernel:
                return False, {"kernel": (half, m)}
        if 2 * half.re**2 != 1 + full.re:
            return False, {"half angle": half}
    for cosine, expected in ((1, lambda m: m + 1), (-1, lambda m: (-1) ** m * (m + 1))):
        g_prev, g = 0, 1
        for m in range(1, 30):
            g_prev, g = g, 2 * cosine * g - g_prev
            if g != expected(m):
                return False, {"double root": cosine}
    light = (2 + math.cos(math.pi / 4)) / 3
    numbers = tuple(round(math.sqrt(1 / (12 * (1 + c))), 3) for c in (2 / 3, light, 0.0))

    def zone_mean(dimension: int, c0: float, steps: int = 60) -> float:
        total, count = 0.0, 0
        grid = [math.pi * (i + 0.5) / steps for i in range(steps)]
        axes = [grid] * dimension
        import itertools

        for ks in itertools.product(*axes):
            cosine = c0 * (sum(math.cos(k) for k in ks) + (3 - dimension))
            total += 1 / (1 + cosine)
            count += 1
        return total / count

    means = (
        zone_mean(3, 1 / 3, 40),
        zone_mean(2, 1 / 3, 200),
        zone_mean(1, 1 / 3, 20000),
        zone_mean(3, 2 / 9, 40),
    )
    walks = tuple(round(math.sqrt(m / 12), 3) for m in means)
    return numbers == (0.224, 0.209, 0.289) and walks == (0.354, 0.259, 0.226, 0.302), {
        "walk per mode at [2, 3], light pi / 4, the centre": numbers,
        "zone means": means,
        "walks per Node": walks,
    }


def check_the_guides_lay() -> Check:
    """S.48, the guide's lay (row 18 of The conventions and the units): a source s e^(-i Omega t) at one Node of a width-one guide, whose band is cos Omega = (num / 3 den) cos k, drives two outgoing waves C e^(i k |x|) with C (2 cos Omega - (2 num / 3 den) e^(i k)) = s, so |C| = 3 den s / (2 num sin k); the two outgoing waves of an increment A have B = 3 A / (2 sin k) at num = den, the form of a travelling wave is D = B^2 sin^2 Omega at every Node, each interval's emission occupies v_g = sin k / (3 sin Omega) Links on each side, so the two trains' form is 2 (9 / (4 sin^2 k)) (SUM_t A_t^2) sin^2 Omega sin k / (3 sin Omega) = (3 / 2) (SUM_t A_t^2) sin Omega / sin k; one quantum on a real line is SUM D = T sin Omega, so one quantum is laid at SUM_t A_t^2 = (2 / 3) T sin k, and the increments' own squares sum to half of it; exact at rational angles, the half by the discrete sum over a period."""
    draw = random.Random(SEED)
    for wave in angles(draw, 10):
        if wave.im == 0:
            continue
        for num, den in pairs(draw, 4):
            c0 = Fraction(num, 3 * den)
            cos_omega = c0 * wave.re
            s = Fraction(draw.randint(1, 50))
            factor = Gaussian(2 * cos_omega, 0) - wave * (
                2 * c0
            )  # 2 cos Omega - (2 num / 3 den) e^(i k)
            if (
                factor.abs2() * (2 * num * wave.im) ** 2
                != (2 * c0 * wave.im) ** 2 * (2 * num * wave.im) ** 2
                or s * s / factor.abs2() != (Fraction(3 * den) * s / (2 * num * wave.im)) ** 2
            ):
                return False, {"|C|": (wave, num, den)}
        a = Fraction(draw.randint(1, 30))
        sine_k, sine_omega = wave.im, Fraction(draw.randint(1, 9), 10)
        b = 3 * a / (2 * sine_k)
        trains = 2 * b * b * sine_omega**2 * sine_k / (3 * sine_omega)
        if trains != Fraction(3, 2) * a * a * sine_omega / sine_k:
            return False, {"trains' form": wave}
        t_action = Fraction(65536)
        laid = Fraction(2, 3) * t_action * sine_k
        if Fraction(3, 2) * laid * sine_omega / sine_k != t_action * sine_omega:
            return False, {"one quantum": wave}
    period = 20
    half = sum(math.cos(2 * math.pi * t / period) ** 2 for t in range(period)) / period
    return abs(half - 0.5) < 1e-12, {"mean of cos^2 over a period": half}


def check_what_a_body_writes_into_the_holder_of_the_sign() -> Check:
    """S.42: at one isolated Node z_(t+1) + z_(t-1) = 2 cos omega_t z_t with any real omega_t keeps W = Im(conj(z_t) z_(t-1)) exactly (W_(t+1) = Im(2 cos omega_t |z_t|^2 - conj(z_(t-1)) z_t) = W_t); a body at rest with the standing plane record z_i = phi_i e^(-i omega_b t), phi real, has W_i = phi_i^2 sin omega_b constant at every Node and the Link quantity g_ij = Im(conj(z_i) z_j) = 0, so a steady rotation writes nothing travelling; the quanta radiated per interval through a far sphere, 4 pi r^2 (3 s / (4 pi r))^2 sin^2 Omega / (sqrt 3 T) = (3 sqrt 3 / 4 pi) s^2 sin^2 Omega / T, the coefficient 0.4135; exact Gaussian rationals and the number recomputed."""
    draw = random.Random(SEED)
    for _ in range(30):
        z_prev, z_now = (
            Gaussian(draw.randint(-9, 9), draw.randint(-9, 9)),
            Gaussian(draw.randint(-9, 9), draw.randint(-9, 9)),
        )
        wronskian = (z_now.conj() * z_prev).im
        for _ in range(6):
            two_cosine = Fraction(draw.randint(-20, 20), 10)
            z_prev, z_now = z_now, z_now * two_cosine - z_prev
            if (z_now.conj() * z_prev).im != wronskian:
                return False, {"W moved": two_cosine}
    for rotation in angles(draw, 8):
        phi = [Fraction(draw.randint(-9, 9)) for _ in range(4)]
        for t in range(3):
            z = [Gaussian(p, 0) * rotation ** (-t) for p in phi]
            z_before = [Gaussian(p, 0) * rotation ** (-(t - 1)) for p in phi]
            if any((z[i].conj() * z_before[i]).im != phi[i] ** 2 * rotation.im for i in range(4)) or any(
                (z[i].conj() * z[j]).im != 0 for i in range(4) for j in range(4)
            ):
                return False, {"steady rotation": rotation}
    coefficient = 9 / (4 * math.pi * math.sqrt(3))
    return round(coefficient, 4) == 0.4135 and abs(
        coefficient - 3 * math.sqrt(3) / (4 * math.pi)
    ) < 1e-15, {"3 sqrt 3 / (4 pi)": coefficient}


def check_the_two_mode_line_under_the_rotation() -> Check:
    """S.43: (a) with z_t = e^(-i Phi_t) u_t and Phi_(t+1) = Phi_t + theta_t, the turned step z_(t+1) = U_t (M z_t / w - U_(t-1) z_(t-1)), U_t = e^(-i theta_t), is the plain line u_(t+1) = M u_t / w - u_(t-1) exactly for any theta_t, a uniform time turn a gauge; (b) at a constant turn the plane solutions rotate at theta +- omega_b, 2 cos(Omega - theta) = 2 cos omega_b; (c) K_jm = SUM over Links R epsilon [phi_j(i) phi_m(i+a) - phi_m(i) phi_j(i+a)] is antisymmetric with K_mm = 0; (d) the transfer generator [[-i Delta / 2, -g], [g, i Delta / 2]] squares to -(g^2 + Delta^2 / 4), so its exponents are +- i sqrt(g^2 + Delta^2 / 4) and P(t) = [g^2 / (g^2 + Delta^2 / 4)] sin^2(sqrt(g^2 + Delta^2 / 4) t), half height at |Delta| = 2 g, the full width 4 Omega_R; (e) the dipole identity on an open chain, SUM_i x_i [phi_j (M phi_m) - (M phi_j) phi_m]_i = -K_jm for any two vectors, so for two modes K_jm = 2 w (cos omega_j - cos omega_m) d_jm = -4 w sin((omega_j + omega_m) / 2) sin((omega_j - omega_m) / 2) d_jm, and Omega_R = theta_L omega_L |d_jm| / 2 for a small line; exact Gaussian rationals and Fractions, the small line by the residual's order."""
    draw = random.Random(SEED)
    for _ in range(20):  # (a) at one Node, M / w = 2 cos omega rational
        two_cosine = Fraction(draw.randint(-19, 19), 10)
        u_prev, u_now = (
            Gaussian(draw.randint(-9, 9), draw.randint(-9, 9)),
            Gaussian(draw.randint(-9, 9), draw.randint(-9, 9)),
        )
        phi_prev, phi_now = draw_angle(draw), draw_angle(draw)  # e^(i Phi_(t-1)), e^(i Phi_t)
        z_prev, z_now = u_prev * phi_prev.conj(), u_now * phi_now.conj()
        turn_before = phi_now * phi_prev.conj()  # e^(i theta_(t-1)) = e^(i (Phi_t - Phi_(t-1)))
        for _ in range(5):
            turn_now = draw_angle(draw)
            phi_next = phi_now * turn_now
            u_next = u_now * two_cosine - u_prev
            z_next = (
                z_now * two_cosine - turn_before.conj() * z_prev
            ) * turn_now.conj()  # U_t (M z / w - U_(t-1) z_before)
            if z_next != u_next * phi_next.conj():
                return False, {"gauge": two_cosine}
            u_prev, u_now, z_prev, z_now, phi_now, turn_before = (
                u_now,
                u_next,
                z_now,
                z_next,
                phi_next,
                turn_now,
            )
    for omega_b in angles(draw, 8):  # (b)
        for turn in angles(draw, 8):
            for sense in (omega_b, omega_b.conj()):
                rate = turn * sense  # e^(i (theta +- omega_b)); z_t = rate^(-t)
                z_prev, z_now = rate**1, Gaussian(1, 0)
                z_next = (z_now * (2 * omega_b.re) - turn.conj() * z_prev) * turn.conj()
                if z_next != rate ** (-1):
                    return False, {"constant turn": (omega_b, turn)}
    for _ in range(10):  # (d)
        g, delta = Fraction(draw.randint(1, 9), 4), Fraction(draw.randint(-9, 9), 3)
        generator = (
            (Gaussian(0, -delta / 2), Gaussian(-g, 0)),
            (Gaussian(g, 0), Gaussian(0, delta / 2)),
        )
        square = tuple(
            tuple(
                sum((generator[i][k] * generator[k][j] for k in range(2)), Gaussian(0, 0))
                for j in range(2)
            )
            for i in range(2)
        )
        if square != (
            (Gaussian(-(g * g + delta * delta / 4), 0), Gaussian(0, 0)),
            (Gaussian(0, 0), Gaussian(-(g * g + delta * delta / 4), 0)),
        ):
            return False, {"generator squared": square}
        if g * g / (g * g + (2 * g) ** 2 / 4) != Fraction(1, 2):
            return False, {"half height": g}
    count, hop = 6, Fraction(draw.randint(1, 9))  # (e) on an open chain
    for _ in range(10):
        phi_j = [Fraction(draw.randint(-9, 9)) for _ in range(count)]
        phi_m = [Fraction(draw.randint(-9, 9)) for _ in range(count)]
        self_coefficient = Fraction(draw.randint(-9, 9))

        def hopping(
            phi: list[Fraction], self_coefficient: Fraction = self_coefficient
        ) -> list[Fraction]:
            return [
                self_coefficient * phi[i]
                + hop * ((phi[i + 1] if i + 1 < count else 0) + (phi[i - 1] if i > 0 else 0))
                for i in range(count)
            ]

        m_j, m_m = hopping(phi_j), hopping(phi_m)
        left = sum(i * (phi_j[i] * m_m[i] - m_j[i] * phi_m[i]) for i in range(count))
        k_jm = sum(hop * (phi_j[i] * phi_m[i + 1] - phi_m[i] * phi_j[i + 1]) for i in range(count - 1))
        if left != -k_jm or k_jm != -sum(
            hop * (phi_m[i] * phi_j[i + 1] - phi_j[i] * phi_m[i + 1]) for i in range(count - 1)
        ):
            return False, {"dipole identity": left}
    for half_j in angles(draw, 6):
        for half_m in angles(draw, 6)[1:]:
            if (
                2 * ((half_j * half_j).re - (half_m * half_m).re)
                != -4 * (half_j * half_m).im * (half_j * half_m.conj()).im
            ):
                return False, {"double angle": (half_j, half_m)}
    omega_m = 0.8
    held, orders = has_order(
        lambda line: (
            abs(math.cos(omega_m + line) - math.cos(omega_m))
            / (2 * math.sqrt(math.sin(omega_m + line) * math.sin(omega_m)))
            / (line / 2)
            - 1
        ),
        2,
        step=0.1,
    )
    return held, {"small line orders": orders}


def check_the_two_forces_between_quanta() -> Check:
    """S.44: the sign holder is written by a quantum's Wronskian, 1 / (2 E_s) per interval for every family, and the content holder by its form, sin omega_s / E_g; a quantum writes U(r) = 3 sin omega_s / (4 pi r Gamma E_g); the pull F_g = 3 T sin omega_s sin omega_s' / (4 pi Gamma E_g r^2) against the electric F_e = 3 k T cos omega / (8 pi Gamma E_s r^2); gravity's coupling alpha_g(s) = (3 sqrt 3 / 4 pi) sin^2 omega_s / (Gamma E_g); the ratio at one family F_e / F_g = k E_g / (2 E_s sin^2 omega_s) at cos omega -> 1, and between two families (F_e / F_g)_e / (F_e / F_g)_p = sin^2 omega_p / sin^2 omega_e = (m_p / m_e)^2 with no number; nature's e^2 / (4 pi epsilon_0 G m_e^2) = 4.17 x 10^42 and 1.24 x 10^36 for the proton, the ratio 3.37 x 10^6 = 1836.15^2; exact rationals and the numbers recomputed."""
    draw = random.Random(SEED)
    for _ in range(20):
        k, e_g, e_s, gamma, t_action, r = (Fraction(draw.randint(1, 50)) for _ in range(6))
        pi_symbol = Fraction(
            355, 113
        )  # pi cancels in every ratio below; a rational stand-in keeps the arithmetic exact
        sine_s, sine_p = Fraction(draw.randint(1, 99), 100), Fraction(draw.randint(1, 99), 100)
        f_g = 3 * t_action * sine_s * sine_s / (4 * pi_symbol * gamma * e_g * r * r)
        f_e = 3 * k * t_action / (8 * pi_symbol * gamma * e_s * r * r)
        if f_e / f_g != k * e_g / (2 * e_s * sine_s**2):
            return False, {"ratio at one family": (k, e_g, e_s)}
        ratio_e = k * e_g / (2 * e_s * sine_s**2)
        ratio_p = k * e_g / (2 * e_s * sine_p**2)
        if ratio_e / ratio_p != sine_p**2 / sine_s**2:
            return False, {"between families": (sine_s, sine_p)}
    e_charge, epsilon_0, g_newton = 1.602176634e-19, 8.8541878128e-12, 6.6743e-11
    m_e, m_p = 9.1093837e-31, 1.67262192e-27
    electron = e_charge**2 / (4 * math.pi * epsilon_0 * g_newton * m_e**2)
    proton = e_charge**2 / (4 * math.pi * epsilon_0 * g_newton * m_p**2)
    numbers = (f"{electron:.2e}", f"{proton:.2e}", f"{electron / proton:.2e}", f"{1836.15**2:.2e}")
    return numbers == ("4.17e+42", "1.24e+36", "3.37e+06", "3.37e+06"), {"numbers": numbers}


def check_the_nuclear_holders_threshold() -> Check:
    """S.45: the pair's potential V(r) = -g^2 e^(-kappa r) / r with g^2 = 3 W omega_p sin omega_p / (4 pi Gamma) and the inertia mu = m* = 3 tan omega_p binds iff 2 mu g^2 / kappa >= 1.6798, that is W >= 1.17 Gamma kappa / omega_p^3 at a small gap (1.6798 x 4 pi / 18 = 1.173): 591 in the rule's own universe ([2, 3], kappa = 1 / 20, Gamma = 6,000), 502 at the exact inertia; under the pair hypothesis mu = m* / 2 and the threshold doubles, 2.35 Gamma kappa / omega_p^3 (1.6798 x 4 pi / 9 = 2.345), 1,183 and 1,004; the Compton length lambda_p = 0.210 fm and the binding fractions (lambda_s / R)^2 / 2: 3.1 x 10^-2 at 0.84 fm, 4.9 x 10^-3 at 2.13 fm, 1.6 x 10^-3 at 3.75 fm; every number recomputed."""
    omega_p = math.acos(2 / 3)
    gamma, kappa = 6000, 1 / 20
    coefficient = 1.6798 * 4 * math.pi / 18
    small_gap = coefficient * gamma * kappa / omega_p**3
    exact_inertia = (
        1.6798 * 4 * math.pi * gamma * kappa / (18 * math.tan(omega_p) * omega_p * math.sin(omega_p))
    )
    hbar_c, m_p_mev = 197.327, 938.272
    compton = hbar_c / m_p_mev
    fractions = tuple(f"{(compton / r) ** 2 / 2:.1e}" for r in (0.84, 2.13, 3.75))
    numbers = (
        round(coefficient, 3),
        round(1.6798 * 4 * math.pi / 9, 3),
        round(small_gap),
        round(exact_inertia),
        round(2 * small_gap),
        round(2 * exact_inertia),
        round(compton, 3),
        fractions,
    )
    expected = (1.173, 2.345, 591, 502, 1183, 1004, 0.21, ("3.1e-02", "4.9e-03", "1.6e-03"))
    return numbers == expected, {"computed": numbers, "printed": expected}


def check_the_atoms_self_term() -> Check:
    """S.46 (c): for a hydrogen-like trial record with x = a_0 / a the mode's frequency over Z^2 Rydberg is epsilon = x^2 - 2 x + (1.25 / Z) x; Hartree's fixed point is the minimum of E_tot = x^2 - 2 x + (0.625 / Z) x, at x = 1 - 0.3125 / Z, with E_tot / (Z^2 R) = -(1 - 0.3125 / Z)^2 and epsilon / (Z^2 R) = E_tot + 0.625 (1 - 0.3125 / Z) / Z, the radius 1 / (1 - 0.3125 / Z); at Z = 1: -0.473, -0.043, 1.45; Z = 2: -0.712, -0.448, 1.19; Z = 10: -0.938, -0.878, 1.03; Z = 30: -0.979, -0.959, 1.01; the Rydberg ratios 1 - 1.25 / Z, 95.9 percent at Z = 30; exact rationals."""
    rows = {}
    for z in (1, 2, 10, 30):
        x = 1 - Fraction(5, 16) / z
        total = x * x - 2 * x + Fraction(5, 8) / z * x
        if total != -((1 - Fraction(5, 16) / z) ** 2):
            return False, {"E_tot": z}
        slope = 2 * x - 2 + Fraction(5, 8) / z  # dE_tot / dx at the minimum
        if slope != 0:
            return False, {"minimum": z}
        epsilon = total + Fraction(5, 8) * x / z
        rows[z] = (
            round(float(total), 3),
            round(float(epsilon), 3),
            round(float(1 / x), 2),
            round(float(-epsilon), 3),
        )
    expected = {
        1: (-0.473, -0.043, 1.45),
        2: (-0.712, -0.448, 1.19),
        10: (-0.938, -0.878, 1.03),
        30: (-0.979, -0.959, 1.01),
    }
    held = (
        all(rows[z][:3] == expected[z] for z in expected)
        and round(rows[30][3], 3) == 0.959
        and round(1 - 1.25 / 30, 3) == 0.958
    )
    return held, {"E_tot, epsilon, radius, -epsilon": rows}


def check_the_equivalence_principle_between_families() -> Check:
    """S.47; Universe24_Paper.tex Section 8 (i): 2 nu / (1 + nu) = 1 - tan^2(omega_s / 2) exactly with nu = cos omega_s, so two families fall apart by tan^2(omega_n / 2) - tan^2(omega_p / 2), (omega_n^2 - omega_p^2) / 4 at small gaps; beryllium (5 / 9) against titanium (26 / 48) differ in their neutron fractions by 0.0139, omega_n^2 - omega_p^2 = (1838.68^2 - 1836.15^2) omega_e^2 = 9,297 omega_e^2, and eta = 0.0139 x 2,324 omega_e^2 = 32.3 omega_e^2, below 4.4 x 10^-18 at omega_e < 3.7 x 10^-10; the identity exact at rational points, the small-gap difference by the residual's order, the numbers recomputed."""
    draw = random.Random(SEED)
    for unit in angles(draw, 12):
        c = unit.re
        if c == -1:
            continue
        if 2 * c / (1 + c) != 1 - (1 - c) / (1 + c):  # tan^2(omega / 2) = (1 - cos) / (1 + cos)
            return False, {"identity": unit}
    held, orders = has_order(
        lambda t: (math.tan(1.5 * t / 2) ** 2 - math.tan(t / 2) ** 2) - ((1.5 * t) ** 2 - t * t) / 4,
        4,
        step=0.4,
    )
    fractions = 5 / 9 - 26 / 48
    gaps = 1838.68**2 - 1836.15**2
    eta = fractions * gaps / 4
    numbers = (round(fractions, 4), round(gaps), round(eta, 1), f"{eta * (3.7e-10) ** 2:.1e}")
    return held and numbers == (0.0139, 9297, 32.3, "4.4e-18"), {"orders": orders, "numbers": numbers}


def check_the_quanta_a_cloud_gives_to_settle() -> Check:
    """The number of quanta a cloud gives to settle (ALGEBRA.md, The surplus leaves): the fraction f that stays solves f = (4 f / (1 + 4 f^2))^3 in a box (23 percent leaving), f = 4 f^(1 / 3) / (4 f^(2 / 3) + 1) on a chain (17.1 percent) and f = 16 f / (4 f + 1)^2 on a plane, the root f = 3 / 4 exactly (25.0 percent); the brackets at most 1 - (4 / 5)^d for a fixed well (20, 36 and 49 percent); the plane's root exact, the two others by bisection."""
    plane = Fraction(3, 4)
    if 16 * plane / (4 * plane + 1) ** 2 != plane:
        return False, {"plane root": plane}

    def bisect(residual, low: float, high: float) -> float:
        for _ in range(100):
            middle = (low + high) / 2
            if residual(low) * residual(middle) <= 0:
                high = middle
            else:
                low = middle
        return (low + high) / 2

    box = bisect(lambda f: (4 * f / (1 + 4 * f * f)) ** 3 - f, 0.5, 0.99)
    chain = bisect(lambda f: 4 * f ** (1 / 3) / (4 * f ** (2 / 3) + 1) - f, 0.5, 0.99)
    leaving = (round(100 * (1 - box)), round(100 * (1 - chain), 1), 100 * (1 - float(plane)))
    brackets = tuple(round(100 * (1 - (4 / 5) ** d)) for d in (1, 2, 3))
    return leaving == (23, 17.1, 25.0) and brackets == (20, 36, 49), {
        "percent leaving (box, chain, plane)": leaving,
        "brackets": brackets,
    }


def check_the_total_share_is_non_negative() -> Check:
    """S.6; ALGEBRA.md, The share's sign and the credit's floor (a) (at the vacuum's coefficients since 3a334eeb, the bound in a well the hands' to state): SUM_i e_i = 3 den (|n|^2 + |b|^2) - num n . S_6 b >= 3 (den - |num|) (|n|^2 + |b|^2) >= 0 on a closed or periodic board for |num| <= den, with equality at the static uniform level of light and, on an even periodic board, its checkerboard with before = -now, whose shares are 0; the total is the quadratic form of the symmetric integer matrix [[3 den I, -(num / 2) S_6], [-(num / 2) S_6^T, 3 den I]], every row of which carries six neighbours counted with multiplicity, so its Gershgorin discs lie in [3 den - 3 |num|, 3 den + 3 |num|] and the bound is Gershgorin's theorem on the integer rows, the machine's (S.6's hand proof by the norm of S_6 restated), the random boards its witnesses; a Node's share at fixed before_i and s = S_6(before)_i is a quadratic in now_i with the minimum 3 den before_i^2 - num^2 s^2 / (12 den), negative iff |s| > 6 (den / num) |before_i|, exact."""
    draw = random.Random(SEED)
    for shape in ((4, 1, 1), (4, 4, 1), (2, 2, 2), (4, 2, 2)):
        arrivals = box_arrivals(shape)
        count = len(arrivals)
        neighbours = [[0] * count for _ in range(count)]  # S_6 with multiplicity
        for i, ports in enumerate(arrivals):
            for j in ports:
                neighbours[i][j] += 1
        for num, den in pairs(draw, 6):
            now = [draw.randint(-30, 30) for _ in arrivals]
            before = [draw.randint(-30, 30) for _ in arrivals]
            total = sum(
                3 * den * (now[i] ** 2 + before[i] ** 2) - num * now[i] * sum(before[j] for j in ports)
                for i, ports in enumerate(arrivals)
            )
            bound = 3 * (den - abs(num)) * (sum(x * x for x in now) + sum(x * x for x in before))
            if total < bound or total < 0:
                return False, {"pair": (num, den), "board": shape, "total": total, "bound": bound}
            levels = now + before
            matrix = [[Fraction(0)] * (2 * count) for _ in range(2 * count)]
            for i in range(count):
                matrix[i][i] = matrix[count + i][count + i] = Fraction(3 * den)
                for j in range(count):
                    matrix[i][count + j] -= Fraction(num * neighbours[i][j], 2)
                    matrix[count + j][i] -= Fraction(num * neighbours[i][j], 2)
            quadratic = sum(
                levels[r] * matrix[r][c] * levels[c] for r in range(2 * count) for c in range(2 * count)
            )
            gershgorin = min(
                matrix[r][r] - sum(abs(matrix[r][c]) for c in range(2 * count) if c != r)
                for r in range(2 * count)
            )
            if quadratic != total or gershgorin != 3 * (den - abs(num)) or gershgorin < 0:
                return False, {"pair": (num, den), "board": shape, "Gershgorin": gershgorin}
        uniform = sum(
            3 * (a * a + a * a) - a * sum(a for _ in ports)
            for a, ports in zip([7] * len(arrivals), arrivals, strict=True)
        )
        if uniform != 0:
            return False, {"uniform light": shape}
        if all(n % 2 == 0 for n in shape):
            nodes = [
                (x, y, z) for x in range(shape[0]) for y in range(shape[1]) for z in range(shape[2])
            ]
            checker = [(-1) ** (x + y + z) * 5 for x, y, z in nodes]
            before_c = [-v for v in checker]
            if any(
                3 * (checker[i] ** 2 + before_c[i] ** 2) - checker[i] * sum(before_c[j] for j in ports)
                != 0
                for i, ports in enumerate(arrivals)
            ):
                return False, {"checkerboard": shape}
    for _ in range(20):
        num, den = draw.randint(1, 9), draw.randint(9, 20)
        b, s = Fraction(draw.randint(-20, 20)), Fraction(draw.randint(-200, 200))
        minimum = 3 * den * b * b - num * num * s * s / (12 * den)
        at_vertex = (
            3 * den * (Fraction(num * s, 6 * den) ** 2 + b * b) - num * Fraction(num * s, 6 * den) * s
        )
        if at_vertex != minimum or (minimum < 0) != (abs(s) > 6 * Fraction(den, num) * abs(b)):
            return False, {"Node minimum": (num, den, b, s)}
    return True, {"boards": 4}


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
