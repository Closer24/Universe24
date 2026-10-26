"""tw1's algebra in integers (no float): (1) the products of the lattice's constants that give 54; (2) the forms' term of the
carrier's time line is exact under every weight W (the carried division at the wall W den Gamma^4 T on a numerator that is a
multiple of W den Gamma^2 is the carried division at the wall Gamma^2 T, quotient for quotient: Euclid), checked on a random
integer course at two weights; (3) the identity of The stress is the Links' on a ring, SUM d^2 = -2 SUM h to the bit; (4) the
massless wave's write on the lattice at the vacuum paces: the bracket W den Gamma^2 forms - trace p_0^2 on an exact integer wave
of period 2, 3, 4 and 6 along one axis (cos k = -1, -1/2, 0, 1/2) with the engine's own stress_parts and the rule's integers,
the weight W_0(k) at which it vanishes, as a pair of integers (no single integer at every k; 6 at the long wave); (5) the
light wave's write at the weights 6, 18, 36, 54 as a fraction of its forms. Run with PYTHONPATH=<src>."""

import random
import sys

sys.set_int_max_str_digits(0)

from event_universe.core.ports import AXES, PORTS, SIDES  # noqa: E402
from event_universe.core.rule3 import carried_division, rule_integers, wall_of  # noqa: E402

print("(1) the lattice's constants whose product is 54 (SIDES 2, AXES 3, PORTS 6, the wall's 6, the mass's 12, d + 1 = 4):")
names = {"SIDES": SIDES, "AXES": AXES, "PORTS": PORTS, "d+1": AXES + 1, "mass 12": 2 * PORTS}
found = []
for a in range(0, 4):
    for b in range(0, 4):
        for c in range(0, 3):
            if SIDES**a * AXES**b * PORTS**c == 54:
                found.append(f"SIDES^{a} AXES^{b} PORTS^{c}")
print("   ", found, "(every one is 2 x 3^3: one SIDES and three AXES in some grouping; no clause names three AXES on the time line)")

print("(2) the forms' term under the weight: Euclid")
den, gamma, T = 348893, 1000, 36000
random.seed(7)
course = [random.randrange(-10**9, 10**9) for _ in range(5000)]  # 4 X p_0 forms, any integers
for w1, w2 in ((54, 18), (54, 36), (6, 108)):
    wall1, wall2 = w1 * den * gamma**4 * T, w2 * den * gamma**4 * T
    r1, r2 = wall1 // 2, wall2 // 2
    same = 0
    for a in course:
        q1, r1 = carried_division(a * w1 * den * gamma**2, wall1, r1)
        q2, r2 = carried_division(a * w2 * den * gamma**2, wall2, r2)
        same += q1 == q2
    print(f"    W {w1} against {w2}: the quotients equal at {same} of {len(course)} intervals (the trace 0)")

print("(3) The stress is the Links': SUM over a ring of (a_+ - a_-)^2 = -2 SUM (a_- a_+ - a^2), to the bit")
for n in (3, 4, 5, 6, 12):
    ring = [random.randrange(-1000, 1000) for _ in range(n)]
    d2 = sum((ring[(i + 1) % n] - ring[i - 1]) ** 2 for i in range(n))
    h = sum(ring[i - 1] * ring[(i + 1) % n] - ring[i] ** 2 for i in range(n))
    print(f"    ring of {n}: SUM d^2 {d2}, -2 SUM h {-2 * h}, equal {d2 == -2 * h}")

print("(4) the massless wave on the lattice at the vacuum paces: the bracket W den Gamma^2 forms - trace p_0^2 per Node, board mean")
# an x-wave of period n along one axis with integer levels; the time part from Rule3's own dispersion at the vacuum for light:
# w (a_next - 2 a + a_before) = SUM_j R (m_j - a), R / w = num / (3 den) = 1 / 3 for light; forms' time part the two-level
# product (a_now - a_before)(a_next - a_now) and its gradient part (1 / 3) a (6 a - SUM_j m_j) (-pull / w), the trace
# den SUM_a (a_+ - a_-)^2 (links.stress_parts at num = den). On a standing integer wave with the levels a(i, t) = b(i) c(t),
# c(t) the same integer cosine sequence in time at the lattice's own omega: for the board mean the exact pairs of integers
# (numerator, denominator) are computed from the cosines' pairs (cos k = ck_n / ck_d) by the identities of the means:
#   <(a_+ - a)^2> = b^2 (1 - cos k), <(a_now - a_before)(a_next - a_now)> = b^2 cos w (1 - cos w), 1 - cos w = (1 - cos k) / 3,
#   <d^2> = 2 b^2 (1 - cos k)(1 + cos k); every mean in the unit b^2 / 1.
rule = rule_integers(den, den, gamma, gamma, gamma)
print(f"    the rule at the vacuum for light: R {rule.reaches[0]}, w {rule.wall}, 3 R == w: {3 * rule.reaches[0] == rule.wall}, D {rule.mass}")
for period, (ck_n, ck_d) in ((2, (-1, 1)), (3, (-1, 2)), (4, (0, 1)), (6, (1, 2)), ("long wave", (1, 1))):
    # all over the denominator 9 ck_d^2: forms = (1 - c)(5 + c) / 9 (the product form), trace / den = 2 (1 - c)(1 + c)
    one_minus = ck_d - ck_n
    forms_n, forms_d = one_minus * (5 * ck_d + ck_n), 9 * ck_d * ck_d
    trace_n, trace_d = 2 * one_minus * (ck_d + ck_n), ck_d * ck_d
    # W forms - trace = 0  ->  W = trace / forms as a pair
    w0_n, w0_d = trace_n * forms_d, forms_n * trace_d
    from math import gcd  # integers

    # W_0 = trace / forms = 18 (1 + c) / (5 + c) after the common factor (1 - c) is struck: finite at the long wave
    w0_n, w0_d = 18 * (ck_d + ck_n), 5 * ck_d + ck_n
    g = gcd(w0_n, w0_d)
    w0 = f"{w0_n // g}/{w0_d // g}"
    light = {W: f"{W * forms_n * trace_d - trace_n * forms_d}/{W * forms_n * trace_d}" for W in (6, 18, 36, 54)}
    print(f"    period {period} (cos k = {ck_n}/{ck_d}): forms {forms_n}/{forms_d} b^2, trace {trace_n}/{trace_d} den b^2, W_0(k) = {w0}; the light's write over its forms at W 6, 18, 36, 54: {light}")
print("    (with the squared velocity in place of the two-level product the forms are 2 (1 - c) / 3 and W_0(k) = 3 (1 + c): 6 at the long wave, 3 at the period 4, 0 at the band's top)")
