"""The external audit's ten items (#1876, the writer's #1793 comment 5977872784 with the advisor's lines in 5977935062), the first ten rows of the proofs' inventory: Theorem 4's integrated exponent, the time-Link recurrence's Wronskian (in proofs_form), the weighted monopole at the two-Node witness, S.39's band real for every pair, S.43 (e)'s uniform Link phase as a gauge, S.17's beat mean bound, S.24's orientation coefficient, S.57's wall (in proofs_credit), 10.2's "hence" (no machine check) and S.26 (d')'s finite-step remainder; each with the witness the two posts give, recomputed, exact where the statement is exact and by the residual's order where it is an expansion.

Usage: `python tools/derivations/proofs_audit.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402, F401  (the derivations' root; tests/test_derivations_lean_on_rule3_alone.py)
from proofs_ground import SEED, Check, Gaussian, angles, has_order, run  # noqa: E402


def erfcx(z: float) -> float:
    """e^(z^2) erfc(z): math.erfc below z = 6, the asymptotic series (1 / (z sqrt pi)) SUM_n (-1)^n (2 n - 1)!! / (2 z^2)^n above."""
    if z < 6:
        return math.exp(z * z) * math.erfc(z)
    total, term = 0.0, 1.0
    for n in range(0, 14):
        total += term
        term *= -(2 * n + 1) / (2 * z * z)
    return total / (z * math.sqrt(math.pi))


def well_moments(z: float) -> tuple[float, float]:
    """(I, J) = (integral u e^(-u^2 / 4 - z u) du, integral u^2 e^(-u^2 / 4 - z u) du) over u >= 0, in closed form: I = 2 - 2 sqrt pi z erfcx(z), J = -4 z + (2 + 4 z^2) sqrt pi erfcx(z); above z = 6 by the asymptotic series with the cancellations done analytically, I = SUM_(n >= 1) 2 (-1)^(n + 1) (2 n - 1)!! / (2 z^2)^n and J from the same terms."""
    if z < 6:
        return 2 - 2 * math.sqrt(math.pi) * z * erfcx(z), -4 * z + (2 + 4 * z * z) * math.sqrt(
            math.pi
        ) * erfcx(z)
    first, second = 0.0, 0.0
    term = 1.0  # (-1)^n (2 n - 1)!! / (2 z^2)^n at n = 0
    for n in range(0, 14):
        if n >= 1:
            first += -2 * term
            second += 4 * z * term
        second += 2 / z * term
        term *= -(2 * n + 1) / (2 * z * z)
    return first, second


def integrated_exponent(z: float) -> float:
    """s(z) = 1 + z <u^2> / <u> for a Gaussian body's well energy C I(kappa R) / R with I(z) = integral u e^(-u^2 / 4 - z u) du: the running exponent of the integrated well energy, -d ln (I(z) / R) / d ln R."""
    first, second = well_moments(z)
    return 1 + z * second / first


def check_theorem_4s_integrated_exponent() -> Check:
    """The audit's item 1 (the writer's 5977872784 and the advisor's 5977935062 on Theorem 4, main 7.2, S.13): for a Gaussian body the integrated well energy of a Yukawa kernel is C I(kappa R) / R with I(z) = integral_0^inf u e^(-u^2 / 4 - z u) du, so its exponent is s = 1 + z <u^2> / <u>: 1.0176, 2.130, 2.971, 2.9997 at kappa R = 0.01, 1, 10, 100, tending to the contact kernel's 3 and not to 1 + kappa R, the pair kernel's log-derivative at one separation (101 at kappa R = 100); s = 1 + sqrt pi kappa R + O((kappa R)^2) at kappa R << 1 and s = 3 - 3 / (kappa R)^2 + O((kappa R)^-4) at kappa R >> 1; s crosses 2 at kappa R = 0.821; the paper's sentence at 2836519e, "s(R) = 1 + kappa R ... holds in the two asymptotic regimes", holds at kappa R << 1 and fails at kappa R >> 1 (3 against infinity), and main 7.2 and S.13 since 9775922e print the integrated exponent, 2.130 at kappa R = 1, 2.971 at 10 and the crossing of 2 at 0.82; the moments in closed form through erfc, the values recomputed, the two asymptotes by the residual's order, the crossing by bisection."""
    values = {z: round(integrated_exponent(z), 4) for z in (0.01, 1.0, 10.0, 100.0)}
    small, orders_small = has_order(
        lambda z: integrated_exponent(z) - (1 + math.sqrt(math.pi) * z), 2, step=0.02
    )
    large, orders_large = has_order(lambda h: integrated_exponent(1 / h) - (3 - 3 * h * h), 4, step=0.1)
    low, high = 0.5, 1.2
    for _ in range(60):
        middle = (low + high) / 2
        if integrated_exponent(middle) < 2:
            low = middle
        else:
            high = middle
    crossing = round((low + high) / 2, 3)
    quadrature = 0.0
    steps, span = 200000, 40.0
    for i in range(steps):  # a check of the closed form at z = 1 by Simpson's rule
        u = span * (i + 0.5) / steps
        quadrature += u * math.exp(-u * u / 4 - u)
    quadrature *= span / steps
    witness = {0.01: 1.0176, 1.0: 2.13, 10.0: 2.971, 100.0: 2.9997}
    kernel_log_derivative = 1 + 100.0
    held = (
        values == witness
        and small
        and large
        and crossing == 0.821
        and abs(quadrature - well_moments(1.0)[0]) < 1e-6
    )
    return held, {
        "s at kappa R = 0.01, 1, 10, 100": values,
        "1 + kappa R at 100": kernel_log_derivative,
        "crossing of 2": crossing,
        "asymptote orders (small, large)": (orders_small, orders_large),
    }


def monopole_at_the_two_node_witness(
    paces_squared: tuple[Fraction, Fraction] = (Fraction(1), Fraction(2)),
) -> tuple[bool, int]:
    """(the weighted monopole SUM W_i / p_i^2 is conserved at every witness, the count of witnesses where the plain sum SUM W_i moved) at the audit's two-Node witness, the paces squared given and the couplings (a p_1^2, a p_2^2), (a, 2 a) at the audit's (1, 2), so that D M is symmetric."""
    draw = random.Random(SEED)
    moved = 0
    for _ in range(20):
        a = Fraction(draw.randint(1, 9), 4)
        reads = ((Fraction(0), a * paces_squared[0]), (a * paces_squared[1], Fraction(0)))
        selves = (Fraction(draw.randint(-9, 9), 3), Fraction(draw.randint(-9, 9), 3))
        z_now = [Gaussian(draw.randint(-9, 9), draw.randint(-9, 9)) for _ in range(2)]
        z_before = [Gaussian(draw.randint(-9, 9), draw.randint(-9, 9)) for _ in range(2)]
        z_next = [z_now[i] * selves[i] + z_now[1 - i] * reads[i][1 - i] - z_before[i] for i in range(2)]
        plain_before = sum((z_now[i].conj() * z_before[i]).im for i in range(2))
        plain_after = sum((z_next[i].conj() * z_now[i]).im for i in range(2))
        weighted_before = sum((z_now[i].conj() * z_before[i]).im / paces_squared[i] for i in range(2))
        weighted_after = sum((z_next[i].conj() * z_now[i]).im / paces_squared[i] for i in range(2))
        if weighted_before != weighted_after:
            return False, moved
        moved += plain_before != plain_after
    return True, moved


def check_the_weighted_monopole_at_the_two_node_witness() -> Check:
    """The audit's item 3 (the advisor's line on S.42's monopole): at static non-uniform paces the conserved monopole is the weighted sum SUM_i W_i / p_i^2 (S.33 (a), S.9's D M symmetric), the plain sum its uniform-pace case; at the audit's two-Node witness, paces squared (1, 2) and couplings (a, 2 a) (the Link coefficient carrying the reading Node's own pace squared, R_12 / p_1^2 = R_21 / p_2^2), the weighted sum is exactly conserved; exact Gaussian rationals at random levels and self coefficients."""
    weighted_holds, moved = monopole_at_the_two_node_witness()
    return weighted_holds and moved > 0, {"plain sums that moved, of 20": moved}


def check_the_plain_monopole_is_the_uniform_pace_case() -> Check:
    """S.42's inputs since 9775922e, "the weighted sum SUM_i W_i / p_i^2 over a body is exactly conserved for a static self-level, the plain sum its uniform-pace case" (at 2836519e the plain sum was printed as the conserved one, the audit's item 3, a finding of this inventory then): at the two-Node witness the plain sum moves at the paces squared (1, 2) and stands with the weighted one at the paces squared (1, 1); exact Gaussian rationals."""
    weighted_at_two, moved_at_two = monopole_at_the_two_node_witness((Fraction(1), Fraction(2)))
    weighted_at_one, moved_at_one = monopole_at_the_two_node_witness((Fraction(1), Fraction(1)))
    return weighted_at_two and weighted_at_one and moved_at_two > 0 and moved_at_one == 0, {
        "plain sums that moved, of 20, at the paces squared (1, 2) and (1, 1)": (
            moved_at_two,
            moved_at_one,
        )
    }


def check_s39s_band_is_real_for_every_pair() -> Check:
    """The audit's item 4 (S.39 (b)): kappa is the static kernel's fall per Link, cosh kappa = 3 den / num - 2, and the band is real throughout for every pair: with S = 0 at the vacuum's paces 2 cos omega = (2 num / 3 den) SUM_a cos k_a runs from 2 num / den at k = 0 to -2 num / den at k = pi on every axis, within [-2, 2] for num <= den, so no quantum stands "above the band's top" and the clause does not follow from kappa > 1; [1, 2] has cosh kappa = 4 and the band from 60 to 120 degrees; exact rationals at the zone's corners (the sum of cosines is extremal there) and random cosines."""
    draw = random.Random(SEED)
    for den in range(1, 40):
        for num in range(1, den + 1):
            c0 = Fraction(num, 3 * den)
            extremes = (2 * c0 * 3, -2 * c0 * 3)
            if (
                extremes != (2 * Fraction(num, den), -2 * Fraction(num, den))
                or extremes[0] > 2
                or extremes[1] < -2
            ):
                return False, {"pair": (num, den), "extremes": extremes}
            for _ in range(3):
                cosines = [angles(draw, 7)[6].re for _ in range(3)]
                value = 2 * c0 * sum(cosines)
                if not extremes[1] <= value <= extremes[0]:
                    return False, {"pair": (num, den), "value outside": value}
    one_two = (
        Fraction(3 * 2, 1) - 2,
        round(math.degrees(math.acos(1 / 2)), 9),
        round(math.degrees(math.acos(-1 / 2)), 9),
    )
    return one_two == (4, 60.0, 120.0), {"[1, 2]: cosh kappa and the band's edges in degrees": one_two}


def check_a_uniform_link_phase_is_a_gauge() -> Check:
    """The audit's item 5 (S.43 (e)): a uniform static Link phase theta is a gauge on an open domain, the step matrix with the phases conjugate to the plain one by the diagonal e^(i theta x) and the modes unchanged, and a holonomy on the periodic board (the conjugation fails at the wrap unless N theta is a multiple of 2 pi: it shifts the allowed k and mixes no mode of a body); Stark's shift needs a potential's gradient across the body; exact Gaussian rationals on a chain of six."""
    draw = random.Random(SEED)
    count = 6
    for theta in angles(draw, 8):
        if theta.re == 1:
            continue
        hop, self_coefficient = Fraction(draw.randint(1, 9)), Fraction(draw.randint(-9, 9))
        gauge = [theta**x for x in range(count)]  # e^(i theta x)

        def phased(
            open_chain: bool,
            theta: Gaussian = theta,
            hop: Fraction = hop,
            self_coefficient: Fraction = self_coefficient,
        ) -> list[list[Gaussian]]:
            matrix = [[Gaussian(0, 0) for _ in range(count)] for _ in range(count)]
            for i in range(count):
                matrix[i][i] = Gaussian(self_coefficient, 0)
                for j, unit in ((i + 1, theta), (i - 1, theta.conj())):
                    if 0 <= j < count:
                        matrix[i][j] = matrix[i][j] + unit * hop
                    elif not open_chain:
                        matrix[i][j % count] = matrix[i][j % count] + unit * hop
            return matrix

        def plain(
            open_chain: bool, hop: Fraction = hop, self_coefficient: Fraction = self_coefficient
        ) -> list[list[Gaussian]]:
            matrix = [[Gaussian(0, 0) for _ in range(count)] for _ in range(count)]
            for i in range(count):
                matrix[i][i] = Gaussian(self_coefficient, 0)
                for j in (i + 1, i - 1):
                    if 0 <= j < count:
                        matrix[i][j] = matrix[i][j] + Gaussian(hop, 0)
                    elif not open_chain:
                        matrix[i][j % count] = matrix[i][j % count] + Gaussian(hop, 0)
            return matrix

        for open_chain in (True, False):
            conjugated = [
                [gauge[i].conj() * plain(open_chain)[i][j] * gauge[j] for j in range(count)]
                for i in range(count)
            ]  # (U^-1 M U)_ij = e^(-i theta i) M_ij e^(i theta j), the phase +theta through the +a Port
            equal = all(
                conjugated[i][j] == phased(open_chain)[i][j] for i in range(count) for j in range(count)
            )
            if open_chain and not equal:
                return False, {"open chain not gauged": theta}
            if not open_chain and equal and theta**count != Gaussian(1, 0):
                return False, {"periodic chain gauged without the holonomy": theta}
    return True, {"chain": count}


def check_s17s_beat_mean_bound() -> Check:
    """The audit's item 6 (S.17's beat, printed since 9775922e as "its mean over n beats is 0 to the order of the fast term over the window, 1 / ((omega_1 + omega_2) n T_b)"; witness only): the finite window's mean of the current of two standing records is the sum-frequency term's, bounded by 2 / ((omega_1 + omega_2) n T_b) for n beats of length T_b, falling as 1 / n and never 0 at a finite window: 0.0083 over one beat at A = B = num = 1, omega_1 = 0.4, omega_2 = 0.4 + 2 pi / 20 (T_b = 20) and 1.1 x 10^-4 over 100 beats, the bounds 0.09 and 0.0009; the means and the bounds recomputed, the inequality checked at random phases."""
    omega_1, omega_2 = 0.4, 0.4 + 2 * math.pi / 20
    beat = 20

    def mean(n: int, alpha: float = 0.0, beta: float = 0.0) -> float:
        total = 0.0
        for t in range(n * beat):
            total += math.cos(omega_1 * t + alpha) * math.cos(omega_2 * (t - 1) + beta) - math.cos(
                omega_1 * (t - 1) + alpha
            ) * math.cos(omega_2 * t + beta)
        return total / (n * beat)

    witnesses = (round(abs(mean(1)), 4), abs(mean(100)))
    bounds = (
        round(2 / ((omega_1 + omega_2) * beat), 2),
        round(2 / ((omega_1 + omega_2) * 100 * beat), 4),
    )
    draw = random.Random(SEED)
    within = all(
        abs(mean(n, draw.uniform(0, 6.3), draw.uniform(0, 6.3))) <= 2 / ((omega_1 + omega_2) * n * beat)
        for n in (1, 2, 5, 10, 100)
        for _ in range(4)
    )
    return witnesses[0] == 0.0083 and abs(witnesses[1] - 1.1e-4) < 1e-5 and bounds == (
        0.09,
        0.0009,
    ) and within, {"means over 1 and 100 beats": witnesses, "bounds": bounds}


def orientation_coefficient(direction: tuple[float, float, float]) -> float:
    """C(n) = (3 SUM_a n_a^4 - 1) / 24, the relative k^2 deficit of light's radial group speed along the unit vector n."""
    return (3 * sum(n**4 for n in direction) - 1) / 24


def check_the_orientation_coefficient() -> Check:
    """The audit's item 7 (S.24's orientation): C(n) = (3 SUM_a n_a^4 - 1) / 24 is 1 / 12 on an axis, 1 / 48 on a face diagonal, 0 on the body diagonal and continuous toward it (C / C_axis = 4.4 x 10^-11, C = 3.7 x 10^-12, at n proportional to (1.00001, 1, 1), the Link bound weakening by sqrt(C_axis / C) = 1.5 x 10^5 there); the mean over directions, <SUM n_a^4> = 3 / 5, gives C_mean / C_axis = 2 / 5; the bound weakens tenfold only within about 4 degrees of a body diagonal (C / C_axis = 1 / 100, 2 sin^2 psi to the leading order), about one percent of the sky, and a hundredfold within 0.4 degrees; the coefficient as the band's own from proofs_band (the fourth order), the numbers recomputed, the cap's angle by bisection and the sky's fraction by the eight caps."""
    axis = orientation_coefficient((1.0, 0.0, 0.0))
    face = orientation_coefficient((1 / math.sqrt(2), 1 / math.sqrt(2), 0.0))
    body = orientation_coefficient((1 / math.sqrt(3),) * 3)
    near = (1.00001, 1.0, 1.0)
    norm = math.sqrt(sum(n * n for n in near))
    near_c = orientation_coefficient(tuple(n / norm for n in near))
    mean = (3 * 3 / 5 - 1) / 24

    def ratio_at(psi: float, azimuth: float) -> float:
        d = (1 / math.sqrt(3),) * 3
        e1 = (1 / math.sqrt(2), -1 / math.sqrt(2), 0.0)
        e2 = (1 / math.sqrt(6), 1 / math.sqrt(6), -2 / math.sqrt(6))
        n = tuple(
            math.cos(psi) * d[a]
            + math.sin(psi) * (math.cos(azimuth) * e1[a] + math.sin(azimuth) * e2[a])
            for a in range(3)
        )
        return orientation_coefficient(n) / axis

    caps = {}
    for target in (0.01, 0.0001):
        angles_found = []
        for azimuth in (j * math.pi / 12 for j in range(24)):
            low, high = 0.0, 0.3
            for _ in range(50):
                middle = (low + high) / 2
                low, high = (middle, high) if ratio_at(middle, azimuth) < target else (low, middle)
            angles_found.append(math.degrees((low + high) / 2))
        mean_angle = sum(angles_found) / len(angles_found)
        caps[target] = (
            round(mean_angle, 2),
            round(100 * 4 * (1 - math.cos(math.radians(mean_angle))), 2),
        )
    held = (
        abs(axis - 1 / 12) < 1e-15
        and abs(face - 1 / 48) < 1e-15
        and abs(body) < 1e-15
        and f"{near_c:.1e}" == "3.7e-12"
        and f"{near_c / axis:.1e}" == "4.4e-11"
        and f"{math.sqrt(axis / near_c):.1e}" == "1.5e+05"
        and abs(mean / axis - 2 / 5) < 1e-15
        and abs(caps[0.01][0] - 4.0) < 0.1
        and abs(caps[0.0001][0] - 0.4) < 0.01
    )
    return held, {
        "C on an axis, a face diagonal, the body diagonal": (axis, face, body),
        "near the diagonal (C, C / C_axis, the weakening)": (
            near_c,
            near_c / axis,
            math.sqrt(axis / near_c),
        ),
        "C_mean / C_axis": mean / axis,
        "caps (degrees, percent of the sky) at tenfold and hundredfold": caps,
    }


def check_s26_d_primes_finite_step_remainder() -> Check:
    """The audit's item 10 (S.26 (d')): the gain side is exact, the discrete form H_t = (1 / 2) |l_(t+1) - l_t|^2 - (1 / 2) l_(t+1) . L l_t of the holder's line l_(t+1) - 2 l_t + l_(t-1) = L l_t + s_t with L symmetric changing per step by exactly (1 / 2) s_t . (l_(t+1) - l_(t-1)); the loss side is the finite sine difference T [sin omega - sin(omega - Delta theta)] = 2 T cos(omega - Delta theta / 2) sin(Delta theta / 2); their ratio is kappa times cos(omega_s - Delta theta / 2) sin(Delta theta / 2) / (cos omega_s Delta theta / 2) = kappa (1 + (Delta theta / 2) tan omega_s + O(Delta theta^2)), so the balance closes to first order in the turn with the remainder (Delta theta / 2) tan omega_s, below 10^-18 at nature's turn and not 0; at the largest turn the law allows (the tangent half-angle at most 1, Delta theta = pi / 2) the exact ratio at [2, 3] is 1.348 against the first order's 1.878; the gain identity exact in Fractions with a random symmetric L, the sine difference exact at rational half-angles, the remainder by the residual's order."""
    draw = random.Random(SEED)
    count = 4
    for _ in range(12):
        matrix = [[Fraction(0)] * count for _ in range(count)]
        for i in range(count):
            for j in range(i, count):
                matrix[i][j] = matrix[j][i] = Fraction(draw.randint(-9, 9), 5)
        l_prev = [Fraction(draw.randint(-9, 9)) for _ in range(count)]
        l_now = [Fraction(draw.randint(-9, 9)) for _ in range(count)]
        source = [Fraction(draw.randint(-9, 9), 3) for _ in range(count)]
        read_now = [sum(matrix[i][j] * l_now[j] for j in range(count)) for i in range(count)]
        read_prev = [sum(matrix[i][j] * l_prev[j] for j in range(count)) for i in range(count)]
        l_next = [2 * l_now[i] - l_prev[i] + read_now[i] + source[i] for i in range(count)]
        h_now = (
            sum((l_next[i] - l_now[i]) ** 2 for i in range(count)) / 2
            - sum(l_next[i] * read_now[i] for i in range(count)) / 2
        )
        h_prev = (
            sum((l_now[i] - l_prev[i]) ** 2 for i in range(count)) / 2
            - sum(l_now[i] * read_prev[i] for i in range(count)) / 2
        )
        if h_now - h_prev != sum(source[i] * (l_next[i] - l_prev[i]) for i in range(count)) / 2:
            return False, {"gain identity": h_now - h_prev}
    for half_omega in angles(draw, 8):
        for half_turn in angles(draw, 8):
            omega, turn = half_omega * half_omega, half_turn * half_turn
            left = omega.im - (omega * turn.conj()).im  # sin omega - sin(omega - Delta theta)
            right = (
                2 * (half_omega * half_omega * half_turn.conj()).re * half_turn.im
            )  # 2 cos(omega - Delta theta / 2) sin(Delta theta / 2)
            if left != right:
                return False, {"sine difference": (half_omega, half_turn)}
    omega_s = math.acos(2 / 3)

    def ratio(turn: float) -> float:
        return math.cos(omega_s - turn / 2) * math.sin(turn / 2) / (math.cos(omega_s) * turn / 2)

    held, orders = has_order(lambda turn: ratio(turn) - (1 + turn / 2 * math.tan(omega_s)), 2, step=0.1)
    far = (round(ratio(math.pi / 2), 3), round(1 + math.pi / 4 * math.tan(omega_s), 3))
    nature = (1e-13 / 2) * math.tan(omega_s)
    return held and far == (1.348, 1.878) and nature < 1e-13, {
        "remainder orders": orders,
        "at the largest turn pi / 2 (exact ratio, first order)": far,
        "remainder at a turn of 10^-13": nature,
    }


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
