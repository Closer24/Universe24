"""Bell's and the GHZ's gates from the declared credit (ALGEBRA.md, The pair family and Bell's gate; The GHZ gate; the paper's Sections 9.3 and 9.4, S.10 and S.40): the root's sum cos(a - b), the four lines of Eq. (bell) by the average over the pair's phase, unequal parts with rho = 2 r / (1 + r^2), the declared pairs' S = 478 / 169 exactly by Lagrange's identity, the two local credits on the same file, the GHZ's E_3 = cos 2(a + b + c) with M = -4 exactly, and the bound 2 of every local credit.

The one fact of the board the gates use is the determinism of equal parts: two records of one family laid equal and stepped by Rule3's one integer map stay identical bit for bit, so the parts' products M_1 = M_2, r = 1 and rho = 1 with no bug; `equal_parts_stay_equal` steps two equal integer lays with `rule3.step` and reads r. Everything after it is the credit's algebra on the declared ports, in exact rationals where the settings are integer pairs.

Usage: `python tools/derivations/bell.py` prints every number.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the folder's root, rule3.py, by its file
import rule3  # noqa: E402

# the parts' laid weights for the symmetric lay (the paper's Eq. (joint), c = (1, 1))
LAID_WEIGHTS = (1, 1)
# the CHSH settings of the declared pairs: A's (p, q) = (1, 0) and (1, 1), B's (12, 5) and (5, 12)
# (the paper's Section 9.3; examples/events/bell/, the settings in the world files)
SETTING_A, SETTING_A_PRIME = (1, 0), (1, 1)
SETTING_B, SETTING_B_PRIME = (12, 5), (5, 12)
# the ideal angles of the CHSH test, a = 0, a' = pi / 4, b = pi / 8, b' = 3 pi / 8 (S.10, "the ideal angles")
IDEAL_ANGLES = (0.0, math.pi / 4, math.pi / 8, 3 * math.pi / 8)
# the GHZ patterns, one integer pair (alpha_k, beta_k) per part for A, B and C (S.40; The GHZ gate)
PATTERN_A = ((1, 0), (1, 0), (0, 1), (0, 1))
PATTERN_B = ((1, 0), (0, 1), (1, 0), (0, 1))
PATTERN_C = ((1, 0), (0, -1), (0, -1), (-1, 0))
# the GHZ's two bases, x = (1, 0) and y = (1, 1), nature's theta = 0 and pi / 2 at theta = 2 a (S.40)
BASIS_X, BASIS_Y = (1, 0), (1, 1)
# the four GHZ files: (x, y, y), (y, x, y), (y, y, x) and (x, x, x) (The GHZ gate)
GHZ_FILES = (
    (BASIS_X, BASIS_Y, BASIS_Y),
    (BASIS_Y, BASIS_X, BASIS_Y),
    (BASIS_Y, BASIS_Y, BASIS_X),
    (BASIS_X, BASIS_X, BASIS_X),
)
# the parts' ratio of the law's example, r = 0.95 (The pair family and Bell's gate)
EXAMPLE_RATIO = 0.95
# the grid of the pair's phase theta for the averages of S.10, 2 x 10^5 points
PHASE_GRID = 200_000
# light's pair, the pair family's (The pair family and Bell's gate), for the determinism check
LIGHT_PAIR = (1, 1)


def ports(p: int | float, q: int | float) -> tuple[tuple[int | float, int | float], ...]:
    """The + port e(+) = (p, q) and the - port e(-) = (-q, p) of a setting (the paper's Section 9.3)."""
    return ((p, q), (-q, p))


def equal_parts_stay_equal(intervals: int = 40, nodes: int = 24) -> Fraction:
    """r = M_2 / M_1, the ratio of the two parts' products at the ports, after two equal integer lays are stepped by Rule3's one line on a periodic chain (the determinism of equal parts, the paper's (1) of Section 9.4): 1 exactly, since one integer map on equal integers gives equal integers."""
    draw = random.Random(24)
    arrivals = rule3.chain_arrivals(nodes)
    now = [draw.randint(-1000, 1000) for _ in range(nodes)]
    before = [draw.randint(-1000, 1000) for _ in range(nodes)]
    parts = [(list(now), list(before), [0] * nodes) for _ in LAID_WEIGHTS]
    for _ in range(intervals):
        for index, (p_now, p_before, carried) in enumerate(parts):
            stepped = [
                rule3.step(
                    p_now[i], p_before[i], [p_now[j] for j in arrivals[i]], *LIGHT_PAIR, carried[i]
                )
                for i in range(nodes)
            ]
            parts[index] = ([s[0] for s in stepped], p_now, [s[1] for s in stepped])
    # the product of a part's level sums at the two sides, the region's sum over its Nodes
    products = [sum(p_now[: nodes // 2]) * sum(p_now[nodes // 2 :]) for p_now, _, _ in parts]
    return Fraction(products[1], products[0])


def root_sum(a: float, b: float) -> float:
    """SUM_k c_k e_k(a) e_k(b) with c = (1, 1) and e(a) = (cos a, sin a), the root's sum of the two branches (the paper's (2) of Section 9.4): cos a cos b + sin a sin b = cos(a - b)."""
    e_a, e_b = (math.cos(a), math.sin(a)), (math.cos(b), math.sin(b))
    return sum(c * x * y for c, x, y in zip(LAID_WEIGHTS, e_a, e_b, strict=True))


def root_sum_is_cos_difference(points: int = 60) -> list[float]:
    """[the largest |root_sum(a, b) - cos(a - b)| over a grid of angles]: 0 to rounding."""
    worst = 0.0
    for i in range(points):
        for j in range(points):
            a, b = 2 * math.pi * i / points, 2 * math.pi * j / points
            worst = max(worst, abs(root_sum(a, b) - math.cos(a - b)))
    return [worst]


def joint_shares(
    setting_a: tuple[float, float], setting_b: tuple[float, float], products: tuple[float, float]
) -> dict[tuple[int, int], float]:
    """J(p, q) = (SUM_k e_k(p) e_k(q) M_k)^2 on the four port pairs, the declared credit (the paper's Eq. (joint); S.10), with M_k the part k's product of its amplitudes at the two sides; the keys the ports' signs (+1, -1)."""
    shares = {}
    for sign_a, e_a in zip((1, -1), ports(*setting_a), strict=True):
        for sign_b, e_b in zip((1, -1), ports(*setting_b), strict=True):
            amplitude = sum(x * y * m for x, y, m in zip(e_a, e_b, products, strict=True))
            shares[(sign_a, sign_b)] = amplitude * amplitude
    return shares


def correlation(shares: dict[tuple[int, int], float]) -> float:
    """E = SUM s(p) s(q) J(p, q) / SUM J(p, q) (S.10)."""
    return sum(s_a * s_b * j for (s_a, s_b), j in shares.items()) / sum(shares.values())


def chsh(settings: tuple[tuple[float, float], ...], products: tuple[float, float]) -> float:
    """S = E(a, b) - E(a, b') + E(a', b) + E(a', b') at the settings (a, a', b, b')."""
    a, a_prime, b, b_prime = settings
    return (
        correlation(joint_shares(a, b, products))
        - correlation(joint_shares(a, b_prime, products))
        + correlation(joint_shares(a_prime, b, products))
        + correlation(joint_shares(a_prime, b_prime, products))
    )


def angle_settings(angles: tuple[float, ...]) -> tuple[tuple[float, float], ...]:
    """The settings (cos a, sin a) of the angles."""
    return tuple((math.cos(angle), math.sin(angle)) for angle in angles)


def phase_average(credit, settings: tuple[float, float, float, float]) -> float:
    """S of a credit E(a, b) = <credit(a - theta, b - theta)> over the pair's phase theta uniform on a grid (S.10, "the two local credits")."""
    a, a_prime, b, b_prime = settings

    def averaged(x: float, y: float) -> float:
        total = 0.0
        for i in range(PHASE_GRID):
            theta = math.pi * (i + 0.5) / PHASE_GRID
            total += credit(x - theta, y - theta)
        return total / PHASE_GRID

    return averaged(a, b) - averaged(a, b_prime) + averaged(a_prime, b) + averaged(a_prime, b_prime)


def four_lines_of_bell() -> list[float]:
    """The four lines of the paper's Eq. (bell) at the ideal angles: [S of the meeting, S of the local credit by the shares, S of the local credit by the sign, S of the contrast credit, the contrast credit's one-side efficiency]: the meeting E = cos 2(a - b) from the declared credit on equal parts, S = 2 sqrt 2; the shares' credit <cos 2(a - theta) cos 2(b - theta)> = cos 2(a - b) / 2, S = sqrt 2; the sign's credit <sgn cos 2(a - theta) sgn cos 2(b - theta)> = 1 - 4 |a - b| / pi, S = 2; the contrast credit <|cos 2(a - theta)| sgn ... > with the other side's sign always counted, E = cos 2(a - b) at the efficiency <|cos x|> = 2 / pi, S = 2 sqrt 2 (S.10)."""
    ideal = angle_settings(IDEAL_ANGLES)
    meeting = chsh(ideal, (1.0, 1.0))
    shares = phase_average(lambda x, y: math.cos(2 * x) * math.cos(2 * y), IDEAL_ANGLES)
    sign = phase_average(
        lambda x, y: math.copysign(1.0, math.cos(2 * x)) * math.copysign(1.0, math.cos(2 * y)),
        IDEAL_ANGLES,
    )
    efficiency = sum(abs(math.cos(math.pi * (i + 0.5) / PHASE_GRID)) for i in range(PHASE_GRID))
    efficiency /= PHASE_GRID
    contrast = (
        phase_average(lambda x, y: math.cos(2 * x) * math.copysign(1.0, math.cos(2 * y)), IDEAL_ANGLES)
        / efficiency
    )
    return [meeting, shares, sign, contrast, efficiency]


def unequal_parts() -> list[float]:
    """Unequal parts, r the ratio of the parts' products (S.10): [the largest |E - (cos 2a cos 2b + rho sin 2a sin 2b)| over r and the angles, the largest |S - sqrt 2 (1 + rho)| at the ideal angles over r, rho at r = 0.95, S at r = 0.95], rho = 2 r / (1 + r^2)."""
    worst_e, worst_s = 0.0, 0.0
    for tenth in range(1, 21):
        r = tenth / 10
        rho = 2 * r / (1 + r * r)
        for i in range(12):
            for j in range(12):
                a, b = math.pi * i / 12, math.pi * j / 12
                e = correlation(
                    joint_shares((math.cos(a), math.sin(a)), (math.cos(b), math.sin(b)), (1.0, r))
                )
                closed = math.cos(2 * a) * math.cos(2 * b) + rho * math.sin(2 * a) * math.sin(2 * b)
                worst_e = max(worst_e, abs(e - closed))
        worst_s = max(
            worst_s, abs(chsh(angle_settings(IDEAL_ANGLES), (1.0, r)) - math.sqrt(2) * (1 + rho))
        )
    rho_example = 2 * EXAMPLE_RATIO / (1 + EXAMPLE_RATIO**2)
    return [worst_e, worst_s, rho_example, math.sqrt(2) * (1 + rho_example)]


def exact_correlation(setting_a: tuple[int, int], setting_b: tuple[int, int]) -> Fraction:
    """E at integer settings on equal parts, [(p_A p_B + q_A q_B)^2 - (p_A q_B - q_A p_B)^2] / [(p_A^2 + q_A^2) (p_B^2 + q_B^2)], the four shares closed by Lagrange's identity (S.10, "the integer settings")."""
    (p_a, q_a), (p_b, q_b) = setting_a, setting_b
    same = (p_a * p_b + q_a * q_b) ** 2
    cross = (p_a * q_b - q_a * p_b) ** 2
    norm = (p_a * p_a + q_a * q_a) * (p_b * p_b + q_b * q_b)
    assert 2 * same + 2 * cross == 2 * norm  # Lagrange's identity on the four shares
    return Fraction(same - cross, norm)


def declared_pairs() -> list[Fraction]:
    """[E(a, b), E(a, b'), E(a', b), E(a', b'), S] at the declared pairs (1, 0), (1, 1), (12, 5), (5, 12) on equal parts: 119 / 169, -119 / 169, 120 / 169, 120 / 169 and S = 478 / 169 exactly."""
    e = [
        exact_correlation(SETTING_A, SETTING_B),
        exact_correlation(SETTING_A, SETTING_B_PRIME),
        exact_correlation(SETTING_A_PRIME, SETTING_B),
        exact_correlation(SETTING_A_PRIME, SETTING_B_PRIME),
    ]
    return [*e, e[0] - e[1] + e[2] + e[3]]


def below_tsirelson() -> list[float]:
    """[S = 478 / 169 as a decimal, 2 sqrt 2, their difference]: the declared pairs' S sits below 2 sqrt 2 by 2.5 x 10^-5 because the angles are rational, the Pythagorean 22.62 and 67.38 degrees and not 22.5 and 67.5."""
    s = float(declared_pairs()[-1])
    return [s, 2 * math.sqrt(2), 2 * math.sqrt(2) - s]


def local_credits_on_the_same_file() -> list[float]:
    """Without the declaration, the second and third lines of Eq. (bell) under the uniform phase: [S by the shares of each side's ports, S by the sign of its larger port], sqrt 2 and 2 (the sawtooth's sum, Bell's bound) (S.10)."""
    lines = four_lines_of_bell()
    return [lines[1], lines[2]]


def ghz_amplitude(
    settings: tuple[tuple[int, int], tuple[int, int], tuple[int, int]], signs: tuple[int, int, int]
) -> int:
    """SUM_k e_k(A) e_k(B) e_k(C) on equal parts at the three sides' settings and ports, e_k(+) = alpha_k p + beta_k q and e_k(-) = alpha_k (-q) + beta_k p (S.40)."""
    total = 0
    for k in range(4):
        term = 1
        for (p, q), sign, pattern in zip(
            settings, signs, (PATTERN_A, PATTERN_B, PATTERN_C), strict=True
        ):
            alpha, beta = pattern[k]
            term *= alpha * p + beta * q if sign > 0 else alpha * (-q) + beta * p
        total += term
    return total


def ghz_correlations(
    settings: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
) -> tuple[Fraction, Fraction]:
    """(E_3, the largest |pairwise E|) of the eight joint shares J = (SUM_k e_k(A) e_k(B) e_k(C))^2 at the settings, E_3 the shares signed by the product of the three signs over their sum, a pairwise E signed by two sides' signs (S.40)."""
    shares = {signs: ghz_amplitude(settings, signs) ** 2 for signs in product((1, -1), repeat=3)}
    total = sum(shares.values())
    e_3 = Fraction(sum(a * b * c * j for (a, b, c), j in shares.items()), total)
    pairwise = [
        abs(Fraction(sum(signs[i] * signs[j] * share for signs, share in shares.items()), total))
        for i, j in ((0, 1), (0, 2), (1, 2))
    ]
    return e_3, max(pairwise)


def ghz() -> list[Fraction]:
    """[E_3 on (x, y, y), (y, x, y), (y, y, x), (x, x, x), the largest pairwise |E| over the four files, Mermin's M = E(x, y, y) + E(y, x, y) + E(y, y, x) - E(x, x, x), the largest |M| of a local assignment of signs]: -1, -1, -1, 1, 0, -4 and 2, the GHZ correlation E_3 = cos 2(a + b + c) at the law's bases x = (1, 0), y = (1, 1) (S.40)."""
    results = [ghz_correlations(settings) for settings in GHZ_FILES]
    e_3 = [r[0] for r in results]
    pairwise = max(r[1] for r in results)
    mermin = e_3[0] + e_3[1] + e_3[2] - e_3[3]
    # every local assignment gives each side a sign at x and a sign at y; its M over the four files
    local = 0
    for signs in product((1, -1), repeat=6):
        a_x, a_y, b_x, b_y, c_x, c_y = signs
        local = max(
            local,
            abs(a_x * b_y * c_y + a_y * b_x * c_y + a_y * b_y * c_x - a_x * b_x * c_x),
        )
    return [*e_3, pairwise, mermin, Fraction(local)]


def bounds_of_the_credits() -> list[float]:
    """[the largest S of every local assignment of signs to the four settings, the declared credit's largest S over the four settings, 2 sqrt(1 + rho^2) at rho = 1]: 2 (Bell's bound, every product form and every mixture of them) and 2 sqrt 2 (Tsirelson's), the bound the law's credits give between separately prepared bodies joined by a coupling or a transferred quantum being the local 2 (S.56 (14))."""
    local = 0
    for a, a_prime, b, b_prime in product((1, -1), repeat=4):
        local = max(local, abs(a * b - a * b_prime + a_prime * b + a_prime * b_prime))
    best = 0.0
    for i in range(1, 64):
        delta = math.pi * i / 128
        settings = angle_settings((0.0, 2 * delta, delta, 3 * delta))
        best = max(best, chsh(settings, (1.0, 1.0)))
    return [float(local), best, 2 * math.sqrt(1 + 1.0)]


if __name__ == "__main__":
    print("r of two equal parts stepped by Rule3:", equal_parts_stay_equal())
    print("root sum against cos(a - b):", root_sum_is_cos_difference())
    print(
        "the four lines' S and the contrast's efficiency:", [round(v, 4) for v in four_lines_of_bell()]
    )
    print("unequal parts:", [round(v, 4) for v in unequal_parts()])
    print("the declared pairs:", [str(v) for v in declared_pairs()])
    print("below Tsirelson:", [round(v, 6) for v in below_tsirelson()])
    print("the GHZ:", [str(v) for v in ghz()])
    print("the credits' bounds:", [round(v, 4) for v in bounds_of_the_credits()])
