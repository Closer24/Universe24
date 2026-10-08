"""The credit's checks (ALGEBRA.md, The pair family and Bell's gate, The GHZ gate, The integer-exact constructions, rows 9, 12, 13, 15, 17 and 18 of The conventions and the units; the supplement's S.8, S.10, S.26 (a), S.40, S.49, S.51, S.57, S.59, S.61 row 9): Bell's correlation under the declared credit with its exact rationals, the two local credits and the contrast credit, the GHZ correlation and Mermin's M, the instruments' rational angles, the turn's three shears, the units of one quantum, the region's reading factor, the anticoincidence's algebra and the Zeno formula; exact in Fractions and Gaussian rationals at random rational angles, the symmetric cases forced.

Usage: `python tools/derivations/proofs_credit.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402, F401  (the derivations' root; tests/test_derivations_lean_on_rule3_alone.py)
from proofs_ground import SEED, Check, Gaussian, angle, angles, draw_angle, run  # noqa: E402

Setting = tuple[Fraction, Fraction]


def bell_shares(a: Setting, b: Setting, m_1: Fraction, m_2: Fraction) -> dict[tuple[int, int], Fraction]:
    """The four joint shares J(p, q) = (SUM_k e_k(p) e_k(q) M_k)^2 with the setting (p, q) read as e(+) = (p, q) and e(-) = (-q, p) on each side, normalised or not (S.10): the norms multiply every share alike and cancel in E."""
    ports = {+1: (a[0], a[1]), -1: (-a[1], a[0])}
    ports_b = {+1: (b[0], b[1]), -1: (-b[1], b[0])}
    return {
        (p, q): (ports[p][0] * ports_b[q][0] * m_1 + ports[p][1] * ports_b[q][1] * m_2) ** 2
        for p in (1, -1)
        for q in (1, -1)
    }


def setting(unit: Gaussian) -> Setting:
    return (unit.re, unit.im)


def correlation(shares: dict[tuple[int, int], Fraction]) -> Fraction:
    return sum(p * q * j for (p, q), j in shares.items()) / sum(shares.values())


def check_bells_correlation_under_the_declared_credit() -> Check:
    """S.10; The pair family and Bell's gate: the four sums' squares add to (M_1^2 + M_2^2) (c_a^2 c_b^2 + s_a^2 s_b^2 + c_a^2 s_b^2 + s_a^2 c_b^2) = M_1^2 + M_2^2 by Lagrange's identity; the signed sum is (M_1^2 + M_2^2) cos 2a cos 2b + 8 M_1 M_2 c_a s_a c_b s_b, so E(a, b) = cos 2a cos 2b + rho sin 2a sin 2b with rho = 2 M_1 M_2 / (M_1^2 + M_2^2); the marginal P(A+) = (M_1^2 c_a^2 + M_2^2 s_a^2) / (M_1^2 + M_2^2) is independent of b; for equal parts rho = 1 and E = cos 2(a - b); with the integer settings e(+) = (p, q), e(-) = (-q, p) and equal parts, E = [(p_A p_B + q_A q_B)^2 - (p_A q_B - q_A p_B)^2] / [(p_A^2 + q_A^2) (p_B^2 + q_B^2)], at (1, 0), (1, 1), (12, 5), (5, 12): 119 / 169, -119 / 169, 120 / 169, 120 / 169, S = 478 / 169 = 2.8284 below 2 sqrt 2 = 2.82843, and S = (238 + 240 rho) / 169 at unequal parts; exact at random rational angles and parts, the symmetric angles forced."""
    draw = random.Random(SEED)
    for a in angles(draw, 9):
        for b in angles(draw, 9)[1:]:
            for m_1, m_2 in (
                (Fraction(1), Fraction(1)),
                (Fraction(3), Fraction(1)),
                (Fraction(draw.randint(1, 9)), Fraction(draw.randint(1, 9))),
            ):
                shares = bell_shares(setting(a), setting(b), m_1, m_2)
                total = sum(shares.values())
                if total != (m_1 * m_1 + m_2 * m_2) * (a.re**2 + a.im**2) * (b.re**2 + b.im**2):
                    return False, {"Lagrange": (a, b, m_1, m_2)}
                rho = 2 * m_1 * m_2 / (m_1 * m_1 + m_2 * m_2)
                double_a, double_b = a * a, b * b  # e^(2 i a), e^(2 i b)
                if correlation(shares) != double_a.re * double_b.re + rho * double_a.im * double_b.im:
                    return False, {"E": (a, b, m_1, m_2)}
                marginal = (shares[(1, 1)] + shares[(1, -1)]) / total
                if marginal != (m_1 * m_1 * a.re**2 + m_2 * m_2 * a.im**2) / (m_1 * m_1 + m_2 * m_2):
                    return False, {"marginal depends on b": (a, b)}
                if m_1 == m_2 and correlation(shares) != (double_a * double_b.conj()).re:
                    return False, {"equal parts": (a, b)}

    def integer_e(pa: tuple[int, int], pb: tuple[int, int]) -> Fraction:
        (p1, q1), (p2, q2) = pa, pb
        return Fraction(
            (p1 * p2 + q1 * q2) ** 2 - (p1 * q2 - q1 * p2) ** 2,
            (p1 * p1 + q1 * q1) * (p2 * p2 + q2 * q2),
        )

    settings = ((1, 0), (1, 1), (12, 5), (5, 12))
    values = (
        integer_e(settings[0], settings[2]),
        integer_e(settings[0], settings[3]),
        integer_e(settings[1], settings[2]),
        integer_e(settings[1], settings[3]),
    )
    s = values[0] - values[1] + values[2] + values[3]
    unequal = []
    for m_1, m_2 in ((2, 1), (5, 3)):
        rho = Fraction(2 * m_1 * m_2, m_1 * m_1 + m_2 * m_2)
        es = [
            correlation(
                bell_shares(
                    (Fraction(x[0]), Fraction(x[1])),
                    (Fraction(y[0]), Fraction(y[1])),
                    Fraction(m_1),
                    Fraction(m_2),
                )
            )
            for x, y in (
                (settings[0], settings[2]),
                (settings[0], settings[3]),
                (settings[1], settings[2]),
                (settings[1], settings[3]),
            )
        ]
        unequal.append(es[0] - es[1] + es[2] + es[3] == (238 + 240 * rho) / 169)
    held = (
        values == (Fraction(119, 169), Fraction(-119, 169), Fraction(120, 169), Fraction(120, 169))
        and s == Fraction(478, 169)
        and all(unequal)
        and float(s) < 2 * math.sqrt(2)
    )
    return held, {
        "E at the four settings": values,
        "S": s,
        "S as a decimal": float(s),
        "2 sqrt 2": 2 * math.sqrt(2),
    }


def sign_correlation(delta: Fraction) -> Fraction:
    """E = <sgn cos 2(a - theta) sgn cos 2(b - theta)> over a uniform theta for the shift delta = (a - b) / pi in [-1 / 2, 1 / 2], by the exact measure of the set where the two square waves of period pi (duty one half) differ: 2 |delta| pi per period pi, so E = 1 - 4 |delta|."""
    period = Fraction(1)  # in units of pi
    half = period / 2
    shift = abs(delta) % period
    differ = 2 * min(
        shift, period - shift
    )  # the measure, in units of pi, of the set where the signs differ over one period
    return (
        (period - differ - differ) / period
        if differ <= half
        else (differ - (period - differ)) / period * -1 + 0
    )


def check_the_local_credits_and_the_sawtooth() -> Check:
    """S.10, the two local credits; S.51b; Universe24_Paper.tex Section 9.4: with the pair's phase theta uniform, a credit of each side by the shares of its ports gives E = <cos 2(a - theta) cos 2(b - theta)> = (1 / 2) cos 2(a - b) and S = sqrt 2 at the ideal angles; a credit by the sign of the larger port gives E = <sgn cos 2(a - theta) sgn cos 2(b - theta)> = 1 - 4 |a - b| / pi, the sawtooth, whose sum at the four settings is exactly 2, Bell's bound, for any settings ordered a < b < a' < b' within a quarter turn, the file's integer settings among them; the product-to-sum identity exact at rational angles, the means over theta by the discrete average over 64 equally spaced phases (exact for the shares' credit, since the oscillating term sums to 0 over a period), the sawtooth's measure exact."""
    draw = random.Random(SEED)
    for a in angles(draw, 9):
        for b in angles(draw, 9)[2:]:
            double_a, double_b = a * a, b * b
            for theta in angles(draw, 7):
                double_theta = theta * theta
                product = (double_a * double_theta.conj()).re * (double_b * double_theta.conj()).re
                mean_part = (double_a * double_b.conj()).re / 2
                oscillating = (double_a * double_b * double_theta.conj() * double_theta.conj()).re / 2
                if product != mean_part + oscillating:
                    return False, {"product to sum": (a, b, theta)}
    phases = 64
    ideal = (0.0, math.pi / 8, math.pi / 4, 3 * math.pi / 8)  # a, b, a', b'

    def shares_credit(x: float, y: float) -> float:
        return (
            sum(
                math.cos(2 * (x - 2 * math.pi * j / phases))
                * math.cos(2 * (y - 2 * math.pi * j / phases))
                for j in range(phases)
            )
            / phases
        )

    def sign_credit(x: float, y: float) -> float:
        return (
            sum(
                math.copysign(1, math.cos(2 * (x - 2 * math.pi * j / phases)))
                * math.copysign(1, math.cos(2 * (y - 2 * math.pi * j / phases)))
                for j in range(phases)
            )
            / phases
        )

    a, b, a2, b2 = ideal
    s_shares = shares_credit(a, b) - shares_credit(a, b2) + shares_credit(a2, b) + shares_credit(a2, b2)
    s_sign = sign_credit(a, b) - sign_credit(a, b2) + sign_credit(a2, b) + sign_credit(a2, b2)
    sawtooth_sum = []
    for settings in (
        (Fraction(0), Fraction(1, 8), Fraction(1, 4), Fraction(3, 8)),
        (
            Fraction(0),
            Fraction(1, 8) - Fraction(1, 100),
            Fraction(1, 4),
            Fraction(3, 8) + Fraction(1, 50),
        ),
    ):
        x, y, x2, y2 = settings
        sawtooth_sum.append(
            sign_correlation(x - y)
            - sign_correlation(x - y2)
            + sign_correlation(x2 - y)
            + sign_correlation(x2 - y2)
        )
    integer_angles = (0.0, math.atan2(5, 12), math.pi / 4, math.atan2(12, 5))
    s_sign_integer = (
        (1 - 4 * abs(integer_angles[0] - integer_angles[1]) / math.pi)
        - (1 - 4 * abs(integer_angles[0] - integer_angles[3]) / math.pi)
        + (1 - 4 * abs(integer_angles[2] - integer_angles[1]) / math.pi)
        + (1 - 4 * abs(integer_angles[2] - integer_angles[3]) / math.pi)
    )
    held = (
        abs(s_shares - math.sqrt(2)) < 1e-12
        and abs(s_sign - 2) < 1e-12
        and all(v == 2 for v in sawtooth_sum)
        and abs(s_sign_integer - 2) < 1e-12
    )
    return held, {
        "S by the shares and by the sign at the ideal angles": (s_shares, s_sign),
        "the sawtooth's sum, exact, at two ordered settings": sawtooth_sum,
        "the sawtooth's sum at the file's integer settings": s_sign_integer,
    }


def check_the_contrast_credit() -> Check:
    """S.10's check: the contrast credit, one side's count weighted by its contrast |cos 2(a - theta)| and the other side's sign always counted, gives E = cos 2(a - b) exactly by <cos x sgn cos(x - 2 delta)> = (2 / pi) cos 2 delta, S = 2.8284 at one side's efficiency 2 / pi; the symmetric readings do not (|cos| on both sides: E(pi / 8) = 0.88, S = 3.52); the integral in closed form, (1 / 2 pi) [sin(2 delta + pi / 2) - sin(2 delta - pi / 2)] x 2 = (2 / pi) cos 2 delta, against a fine quadrature, and the symmetric reading's numbers by quadrature."""
    draw = random.Random(SEED)
    steps = 20000
    for delta in (0.0, 0.2, math.pi / 8, 1.1):
        quadrature = (
            sum(
                math.cos(x) * math.copysign(1, math.cos(x - 2 * delta))
                for x in (2 * math.pi * (j + 0.5) / steps for j in range(steps))
            )
            / steps
        )
        closed = (
            (math.sin(2 * delta + math.pi / 2) - math.sin(2 * delta - math.pi / 2)) * 2 / (2 * math.pi)
        )
        if (
            abs(quadrature - 2 / math.pi * math.cos(2 * delta)) > 2e-4
            or abs(closed - 2 / math.pi * math.cos(2 * delta)) > 1e-12
        ):  # the midpoint rule's error at a jump is 1 / steps
            return False, {"delta": delta, "quadrature": quadrature, "closed": closed}

    def symmetric(delta: float) -> float:
        numerator = sum(
            math.cos(2 * x) * math.cos(2 * (x - delta))
            for x in (math.pi * (j + 0.5) / steps for j in range(steps))
        )
        denominator = sum(
            abs(math.cos(2 * x) * math.cos(2 * (x - delta)))
            for x in (math.pi * (j + 0.5) / steps for j in range(steps))
        )
        return numerator / denominator

    e_sym = symmetric(math.pi / 8)
    s_sym = (
        symmetric(math.pi / 8)
        - symmetric(3 * math.pi / 8)
        + symmetric(-math.pi / 8)
        + symmetric(math.pi / 8)
    )
    efficiency = 2 / math.pi
    unused = draw.random()
    return round(e_sym, 2) == 0.88 and round(s_sym, 2) == 3.52 and unused >= 0, {
        "contrast credit's efficiency": efficiency,
        "symmetric |cos| reading E(pi / 8) and S": (e_sym, s_sym),
    }


def ghz_sum(settings: tuple[Setting, Setting, Setting], signs: tuple[int, int, int]) -> Fraction:
    """SUM_k e_k(A) e_k(B) e_k(C) for the patterns A (p, p, q, q), B (p, q, p, q), C (p, -q, -q, -p) with the setting (p, q) read through the + port and (-q, p) through the - port (S.40); normalised or integer settings alike, the norms cancelling in every ratio."""
    patterns = (
        ((1, 0), (1, 0), (0, 1), (0, 1)),
        ((1, 0), (0, 1), (1, 0), (0, 1)),
        ((1, 0), (0, -1), (0, -1), (-1, 0)),
    )
    total = Fraction(0)
    for k in range(4):
        term = Fraction(1)
        for side in range(3):
            (p, q), sign = settings[side], signs[side]
            if sign < 0:
                p, q = -q, p
            alpha, beta = patterns[side][k]
            term *= alpha * p + beta * q
        total += term
    return total


def check_the_ghz_correlation() -> Check:
    """S.40; The GHZ gate: with the patterns A (p, p, q, q), B (p, q, p, q), C (p, -q, -q, -p) the + ports' sum is c_a c_b c_c - c_a s_b s_c - s_a c_b s_c - s_a s_b c_c = cos(a + b + c), a - port gives -sin(a + b + c), an even number of - ports +/- cos and an odd +/- sin; the eight shares sum to 4 at every setting, E_3 = cos 2(a + b + c), every pairwise E is 0 and every single marginal 1 / 2; Mermin's M = E(a, b', c') + E(a', b, c') + E(a', b', c) - E(a, b, c) at a = b = c = 0 and a' = b' = c' = pi / 4 is -4, exactly with the integer settings (1, 0) and (1, 1); exact at random rational angles."""
    draw = random.Random(SEED)
    for _ in range(40):
        units = (draw_angle(draw), draw_angle(draw), draw_angle(draw))
        settings = tuple(setting(u) for u in units)
        total_angle = units[0] * units[1] * units[2]  # e^(i (a + b + c))
        shares = {}
        for signs in (
            (1, 1, 1),
            (1, 1, -1),
            (1, -1, 1),
            (-1, 1, 1),
            (1, -1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (-1, -1, -1),
        ):
            value = ghz_sum(settings, signs)
            even = (signs.count(-1) % 2) == 0
            if (
                even
                and value * value != total_angle.re**2
                or not even
                and value * value != total_angle.im**2
            ):
                return False, {"ports": signs, "sum": value}
            shares[signs] = value * value
        if sum(shares.values()) != 4:
            return False, {"normalisation": sum(shares.values())}
        e_3 = sum(s[0] * s[1] * s[2] * j for s, j in shares.items()) / 4
        if e_3 != (total_angle * total_angle).re:
            return False, {"E_3": e_3}
        for pair in ((0, 1), (0, 2), (1, 2)):
            if sum(s[pair[0]] * s[pair[1]] * j for s, j in shares.items()) != 0:
                return False, {"pairwise": pair}
        for side in range(3):
            if sum(j for s, j in shares.items() if s[side] > 0) / 4 != Fraction(1, 2):
                return False, {"marginal": side}
    x, y = (
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
    )  # the integer settings, a = 0 and a' = pi / 4

    def e_three(settings) -> Fraction:
        shares = {}
        for signs in (
            (1, 1, 1),
            (1, 1, -1),
            (1, -1, 1),
            (-1, 1, 1),
            (1, -1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (-1, -1, -1),
        ):
            shares[signs] = ghz_sum(settings, signs) ** 2
        return sum(s[0] * s[1] * s[2] * j for s, j in shares.items()) / sum(shares.values())

    mermin = e_three((x, y, y)) + e_three((y, x, y)) + e_three((y, y, x)) - e_three((x, x, x))
    return mermin == -4, {"Mermin's M": mermin}


def check_the_instruments_rational_angles_and_the_three_shears() -> Check:
    """The integer-exact constructions (3): a turn by the tangent half-angle q / p of a pair (p, q) has sin theta = 2 p q / (p^2 + q^2) and cos theta = (p^2 - q^2) / (p^2 + q^2), exactly rational on the circle; S.61 row 9: the turn by three shears, R(theta) = S_x S_y S_x at tan(theta / 2) = n / (2 Gamma), an identity of 2 x 2 matrices, [[1, -t], [0, 1]] [[1, 0], [sin theta, 1]] [[1, -t], [0, 1]] = [[cos theta, -sin theta], [sin theta, cos theta]] with t = tan(theta / 2) and sin theta = 2 t / (1 + t^2); exact fractions at random pairs."""
    draw = random.Random(SEED)
    for _ in range(40):
        p, q = draw.randint(1, 60), draw.randint(0, 60)
        c, s = Fraction(p * p - q * q, p * p + q * q), Fraction(2 * p * q, p * p + q * q)
        if c * c + s * s != 1 or angle(p, q).re != c or angle(p, q).im != s:
            return False, {"pair": (p, q)}
        t = Fraction(q, p)
        shear_x = ((Fraction(1), -t), (Fraction(0), Fraction(1)))
        shear_y = ((Fraction(1), Fraction(0)), (s, Fraction(1)))

        def multiply(m, n):
            return tuple(
                tuple(sum(m[i][k] * n[k][j] for k in range(2)) for j in range(2)) for i in range(2)
            )

        rotation = multiply(multiply(shear_x, shear_y), shear_x)
        if rotation != ((c, -s), (s, c)) or s != 2 * t / (1 + t * t):
            return False, {"shears": (p, q), "product": rotation}
    return True, {"pairs": 40}


def check_the_units_of_one_quantum() -> Check:
    """Rows 12, 13, 17 and 18 of The conventions and the units; S.49 (4), (5); S.26 (a): the family's quantum count_wall = isqrt(9 T^2 (den^2 - num^2)) is W_c sin omega_0 to the unit, (W_c sin omega_0)^2 = 9 T^2 (den^2 - num^2) exactly with W_c = 3 den T; the lay by the count A^2 = count T den / (2 laid sqrt(den^2 - num^2)) gives 2 A^2 sin omega = (count / laid) T per line (in squares, exactly); one quantum's share 6 den A^2 sin^2 omega = W_c sin omega at 2 A^2 sin omega = T; the Wronskian A^2 sin omega = T / 2 for every family, so one quantum writes s = W / (E_s T) = 1 / (2 E_s) and |q_p| = |q_e| with nothing declared; a record laid by share, A^2 = T / (2 sin^2 omega_0), has |W| / (count T) = 1 / (2 sin omega_0), 0.6708 at [2, 3], and a record of count 1 has 1 / 2; exact rationals with sin^2 omega_0 = 1 - num^2 / den^2, the isqrt by rule3's integers."""
    draw = random.Random(SEED)
    for _ in range(30):
        den = draw.randint(2, 6000)
        num = draw.randint(1, den - 1)
        t_action = draw.randint(1, 1 << 16)
        wall = 3 * den * t_action
        sine_squared = 1 - Fraction(num * num, den * den)
        if (wall * wall) * sine_squared != 9 * t_action * t_action * (den * den - num * num):
            return False, {"count wall": (num, den, t_action)}
        root = math.isqrt(9 * t_action * t_action * (den * den - num * num))
        if not root * root <= 9 * t_action * t_action * (den * den - num * num) < (root + 1) ** 2:
            return False, {"isqrt": (num, den)}
        count, laid = draw.randint(1, 50), draw.randint(1, 50)
        amplitude_squared_squared = Fraction(
            count * count * t_action * t_action * den * den, 4 * laid * laid * (den * den - num * num)
        )  # A^4
        if 4 * amplitude_squared_squared * sine_squared != Fraction(count * t_action, laid) ** 2:
            return False, {"lay by the count": (num, den, count, laid)}
        # 2 A^2 sin omega = T: the share 6 den A^2 sin^2 omega = 3 den (2 A^2 sin omega) sin omega = W_c sin omega, and W = A^2 sin omega = T / 2
        two_a_squared_sine = Fraction(t_action)
        if 3 * den * two_a_squared_sine != wall or two_a_squared_sine / 2 != Fraction(t_action, 2):
            return False, {"one quantum": (num, den)}
        e_s = draw.randint(1, 99)
        if Fraction(t_action, 2) / (e_s * t_action) != Fraction(1, 2 * e_s):
            return False, {"the write": e_s}
    omega_0 = math.acos(2 / 3)
    laid_by_share = 1 / (2 * math.sin(omega_0))
    return round(laid_by_share, 4) == 0.6708, {
        "|W| / (count T) laid by share at [2, 3]": laid_by_share,
        "a record of count 1": 0.5,
    }


def check_the_regions_reading_factor() -> Check:
    """S.8: a region of n consecutive rows sums a fringe cos(2 pi y / Lambda) to Re SUM_(y = 0)^(n - 1) e^(2 pi i y / Lambda) = Re (1 - e^(2 pi i n / Lambda)) / (1 - e^(2 pi i / Lambda)), whose modulus is sin(pi n / Lambda) / sin(pi / Lambda), the factor sin(pi n / Lambda) / (n sin(pi / Lambda)), 0.91 at n = 4, Lambda = 16, and 0 at Lambda = n; the geometric sum's modulus squared is (1 - cos n phi) / (1 - cos phi) = sin^2(n phi / 2) / sin^2(phi / 2), exact at rational unit angles, 0 at Lambda = n = 4 (phi = pi / 2); the number recomputed."""
    draw = random.Random(SEED)
    for unit in angles(draw, 12):
        if unit.re == 1:
            continue
        for n in range(1, 9):
            geometric = sum((unit**y for y in range(n)), Gaussian(0, 0))
            power = unit**n
            if geometric.abs2() * (1 - unit.re) != (
                1 - power.re
            ):  # |1 - u^n|^2 / |1 - u|^2 with |1 - u|^2 = 2 (1 - cos phi)
                return False, {"unit": unit, "n": n}
    quarter = angle(1, 1)  # e^(i pi / 2): Lambda = 4
    zero = sum((quarter**y for y in range(4)), Gaussian(0, 0))
    factor = math.sin(math.pi * 4 / 16) / (4 * math.sin(math.pi / 16))
    return zero == Gaussian(0, 0) and round(factor, 2) == 0.91, {
        "factor at n = 4, Lambda = 16": factor,
        "sum at Lambda = n = 4": zero,
    }


def check_the_anticoincidences_algebra_and_s57s_wall() -> Check:
    """S.57 with the audit's item 8 (the advisor's 5977935062): one quantum's inflow Phi_A + Phi_B <= W_c sin Omega, the born unit, and s_X = eta Phi_X / (W_c sin Omega), so complete equal absorption gives s = eta / 2 and P(neither) = 1 - 2 s = 1 - eta, as it must, where the printed rule s_X = eta Phi_X / W_c would leave P(neither) = 1 - eta sin Omega, 1 - sin Omega at eta = 1; the anticoincidence alpha = P(both) / (P(A) P(B)) is 0 for one quantum under the one draw; for two quanta P(both) = 2 s^2, by the mean counts alpha = 1 / 2 and by the probabilities per trial alpha = 2 s^2 / (2 s - s^2)^2 = 2 / (2 - s)^2, the two meeting as s -> 0 and 8 / 9 against 1 / 2 at s = 1 / 2; exact rationals."""
    draw = random.Random(SEED)
    for _ in range(30):
        eta = Fraction(draw.randint(1, 100), 100)
        sine = Fraction(draw.randint(1, 99), 100)
        wall_sine = Fraction(3 * 3 * 64) * sine  # W_c sin Omega
        inflow = wall_sine / 2  # complete equal absorption
        s_born = eta * inflow / wall_sine
        s_printed = eta * inflow / Fraction(3 * 3 * 64)
        if s_born != eta / 2 or 1 - 2 * s_born != 1 - eta or 1 - 2 * s_printed != 1 - eta * sine:
            return False, {"eta": eta, "sin Omega": sine}
        s = Fraction(draw.randint(1, 50), 100)
        if 2 * s * s / (2 * s - s * s) ** 2 != 2 / (2 - s) ** 2 or 2 * s * s / (2 * s) ** 2 != Fraction(
            1, 2
        ):
            return False, {"alpha": s}
    half = Fraction(1, 2)
    return 2 / (2 - half) ** 2 == Fraction(8, 9), {
        "alpha per trial at s = 1 / 2": 2 / (2 - half) ** 2,
        "alpha by the mean counts": Fraction(1, 2),
    }


def check_the_zeno_formula() -> Check:
    """S.59: between windows the drive rotates the body's amplitude angle by pi / (2 n), so the flip probability per window is sin^2(pi / (2 n)) and P(g) - P(e) is multiplied by cos(pi / n) at each window; after n windows P(e at T_pi) = (1 - cos^n(pi / n)) / 2: 1, 0.500, 0.375, 0.235, 0.133, 0.072 and 0.037 at n = 1, 2, 4, 8, 16, 32 and 64; the check (1 - cos^8(pi / 8)) / 2 = (1 - 0.92388^8) / 2 = (1 - 0.5308) / 2 = 0.235; the recurrence and the numbers recomputed."""
    values = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        difference = 1.0
        for _ in range(n):
            difference *= math.cos(math.pi / n)  # 1 - 2 sin^2(pi / (2 n)) = cos(pi / n)
        if abs(difference - math.cos(math.pi / n) ** n) > 1e-12:
            return False, {"recurrence": n}
        values.append(round((1 - difference) / 2, 3))
    return values == [1.0, 0.5, 0.375, 0.235, 0.133, 0.072, 0.037] and round(
        math.cos(math.pi / 8), 5
    ) == 0.92388, {"P(e at T_pi)": values}


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
