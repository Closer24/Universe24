"""fd2's one-Node test: the algebra of section 1 and 3 of fd2_REPORT.md checked on integers (no board, no float).
 1. U1: the one bilinear equals the eight spellings on random integers (the Wronskian, the current, the sign current, the twist,
    the form, the momentum's change) and the decoder's two (the rationals' order, the distance to a pair).
 2. U4: the toy's odd_round(q, d) equals paces.rounded(q, d) at every (q, d) drawn (odd and even alike).
 3. NOT unified: paces.rounded against paces.odd_rounded: the count of inputs where they differ (the negative ties alone) and the
    numbers at the tie x = -wall div 2.
 4. U5: the frame sign 1 - 2 (b_i xor b_j) equals 1 - 2 ((b_i + b_j) mod 2) on the bits 0, 1 (the wall 2), and the count of
    mismatches on remainders of a wider wall (where the fold would NOT hold).
 5. The swap is C T_0 on a plane: the exchange (re_now, re_before, im_now, im_before) -> (re_before, re_now, -im_before, -im_now)
    keeps W = cross(re_now, im_now, re_before, im_before) exactly, and T_0 alone or C alone negates it.
 6. NOT unified: the complement at the wall of the half-wall origin is w div 2 - 1 and not w div 2 (w even): the pair the origin
    refusal names; the mean wall (w div 2)(X_0 + X_1) against w X: equal at X_0 = X_1 alone.
 7. The clock as a carried division: (a) K-S4's first-order carried division from the half wall against paces.clock_alone over the
    contents 0 .. frozen_content(Gamma): the count equal, the count off by one, the largest deviation; (b) Rule3's own three-term
    line (the hyperbolic Chebyshev recurrence of the geometric sequence) with a carried remainder, the same readings: the
    second root 1 / q grows, so the three-term form is NOT the clock (the number).
 8. The beat and the band are one dispersion law: at the vacuum's paces S = 0 exactly and 6 R = 2 w num / den, so
    2 w cos omega = SUM_j R_j cos k_j gives the kinetic clause; at k = 0 and the content c, 1 - cos omega_c = D(c) / (2 w) with
    D(c) Gamma^2 = D(0) p_0(c)^2 exactly, PC's beat law sin(omega_c / 2) = (p_0 / Gamma) sin(omega_0 / 2).
 9. NOT unified: the unit 3 T sine_den(num, den) is 0 at num = den where the massless unit is 3 den T.
10. The exclusion's dot: the plane's lay refusal (standing > 0) is the dot rule with a one-component density (the dot standing x child
    > 0 iff standing > 0, the child's share positive): counted on random shares.
Run: python fd2_one_node.py   (prints one JSON line per check; exit 0 iff every check that must hold holds)."""
import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toy_fd2'))
from fractions import Fraction
from event_universe.core import rule3, paces
from event_universe.core.paces import rounded, odd_rounded, sine_den, clock_alone, frozen_content
from lean_full import cross, turn_pair

sys.set_int_max_str_digits(0)
rng = random.Random(24)
out = {}; failed = []


def check(name, ok, numbers):
    out[name] = numbers | {'holds': bool(ok)}
    if not ok: failed.append(name)
    print(json.dumps({name: out[name]}))


R = lambda: rng.randint(-10 ** 12, 10 ** 12)
N = 20000
# 1. the one bilinear
agree = 0
for _ in range(N):
    re_n, re_b, im_n, im_b, n_i, b_i, n_j, b_j = (R() for _ in range(8))
    ok = cross(re_n, im_n, re_b, im_b) == re_n * im_b - im_n * re_b  # the Wronskian
    ok &= cross(n_i, b_i, n_j, b_j) == n_i * b_j - b_i * n_j  # the current
    dz_re, dz_im = R(), R()
    ok &= cross(re_n, im_n, dz_re, dz_im) == re_n * dz_im - im_n * dz_re  # the sign current's term
    ub, uc, ubj, ucj = R(), R(), R(), R()
    ok &= cross(ub, uc, ubj, ucj) == ub * ucj - uc * ubj  # the twist
    now, before, nxt = R(), R(), R()
    ok &= cross(now, before, nxt, now) == now * now - nxt * before  # the form
    d_n, d_b, n_up, n_dn, b_up, b_dn = (R() for _ in range(6))
    ok &= 2 * cross(d_n, d_b, n_dn - n_up, b_dn - b_up) == 2 * (d_n * (b_dn - b_up) + d_b * (n_up - n_dn))  # the momentum's change
    p0, p1, q0, q1 = R(), R(), R(), R()
    ok &= cross(p0, p1, q0, q1) == p0 * q1 - q0 * p1  # the rationals' order
    ok &= cross(n_i, b_i, q0, q1) == n_i * q1 - b_i * q0  # the distance of (N, D) to (num, den)
    agree += ok
check('1 U1 one bilinear equals the eight spellings', agree == N, {'drawn': N, 'equal': agree})

# 2. odd_round is rounded
agree = 0
for _ in range(N):
    q = R(); d = rng.randint(1, 10 ** 9) * rng.choice((1, 2))
    agree += ((2 * q + d) // (2 * d)) == int(rounded(q, d))
check('2 U4 odd_round(q, d) equals paces.rounded(q, d)', agree == N, {'drawn': N, 'equal': agree})

# 3. rounded against odd_rounded: the ties
differ = 0; neg_ties = 0; drawn = 0
for _ in range(N):
    wall = rng.randint(1, 1000) * 2; x = rng.randint(-5 * wall, 5 * wall); drawn += 1
    r, o = int(rounded(x, wall)), int(odd_rounded(x, wall))
    differ += (r != o); neg_ties += (x < 0 and (2 * x) % (2 * wall) == wall)
w_ = 1000
check('3 NOT unified: rounded against odd_rounded differ at the negative ties alone', differ == neg_ties, {'drawn': drawn, 'differ': differ, 'negative ties': neg_ties, 'at x = -wall div 2, wall 1000: rounded, odd_rounded': [int(rounded(-w_ // 2, w_)), int(odd_rounded(-w_ // 2, w_))], 'at x = +wall div 2': [int(rounded(w_ // 2, w_)), int(odd_rounded(w_ // 2, w_))]})

# 4. the frame sign's parity
bits_ok = all((1 - 2 * (a ^ b)) == (1 - 2 * ((a + b) % 2)) for a in (0, 1) for b in (0, 1))
wider = sum(1 for a in range(4) for b in range(4) if (1 - 2 * (a ^ b)) != (1 - 2 * ((a + b) % 2)))
check('4 U5 frame sign: xor equals the sum mod 2 on the bits of the wall 2', bits_ok, {'pairs on {0,1}': 4, 'mismatches on {0..3} (a wider wall would break the fold)': wider})

# 5. the swap is C T_0 on a plane: W kept
kept = 0; t0_neg = 0; c_neg = 0
for _ in range(N):
    re_n, re_b, im_n, im_b = R(), R(), R(), R()
    W = cross(re_n, im_n, re_b, im_b)
    sw = cross(re_b, -im_b, re_n, -im_n)  # the exchange: now <- before, before <- now, im negated
    t0 = cross(re_b, im_b, re_n, im_n)  # T_0 alone
    cc = cross(re_n, -im_n, re_b, -im_b)  # C alone
    kept += (sw == W); t0_neg += (t0 == -W); c_neg += (cc == -W)
check('5 the swap is C T_0: W kept by the exchange, negated by T_0 alone and by C alone', kept == N and t0_neg == N and c_neg == N, {'drawn': N, 'W kept by the exchange': kept, 'W negated by T_0': t0_neg, 'W negated by C': c_neg})

# 6. the complement of the half wall; the mean wall against w X
w = rule3.wall_of(1021, 1000, 16)
half = w // 2
comp = w - 1 - half
X0, X1 = 1000, 1007
check('6 NOT unified: the complement of the half-wall origin is half - 1, the mean wall equals w X at X_0 = X_1 alone', comp == half - 1 and (w // 2) * (X0 + X0) == w * X0 and (w // 2) * (X0 + X1) != w * X1, {'w': w, 'half wall': half, 'complement of the half wall': comp, 'difference': half - comp, 'mean wall (X_0, X_1) = (1000, 1007)': (w // 2) * (X0 + X1), 'w X_1': w * X1, 'w X_0': w * X0})

# 7. the clock as a carried division
gamma = 1000; top = frozen_content(gamma)
exact = [clock_alone(gamma, c) for c in range(top + 1)]
# (a) K-S4: p_{c+1}, r_{c+1} from p_c (Gamma - 1) + r_c at the wall Gamma, the remainder carried from the half wall
p, r = gamma, gamma // 2; first = [p];
for c in range(top):
    q, r = rule3.carried_division(p * (gamma - 1), gamma, r, 1); p = q; first.append(p)
dev_a = [first[c] - exact[c] for c in range(top + 1)]
# (b) the three-term line of the geometric sequence: p_{c+1} = ((Gamma - 1)^2 + Gamma^2) p_c / (Gamma (Gamma - 1)) - p_{c-1}, the wall Gamma (Gamma - 1), carried
wall3 = gamma * (gamma - 1); S3 = (gamma - 1) ** 2 + gamma ** 2
a_b, a_n, r3 = gamma, exact[1], wall3 // 2; three = [a_b, a_n]
for c in range(1, top):
    q, r3 = rule3.carried_division(S3 * a_n - wall3 * a_b, wall3, r3, 1); a_b, a_n = a_n, q; three.append(a_n)
dev_b = [three[c] - exact[c] for c in range(top + 1)]
check('7 the clock: K-S4 first-order carried division against the exact power', max(abs(d) for d in dev_a) <= 1, {'Gamma': gamma, 'contents 0..frozen': top, 'frozen content': top, 'equal to clock_alone': sum(1 for d in dev_a if d == 0), 'off by one': sum(1 for d in dev_a if abs(d) == 1), 'largest deviation': max(abs(d) for d in dev_a), 'clock at the frozen content: exact, carried': [exact[top], first[top]]})
check('7b NOT unified: Rule3 three-term line with the hyperbolic coefficient as the clock (the second root grows)', max(abs(d) for d in dev_b) > 1, {'equal to clock_alone': sum(1 for d in dev_b if d == 0), 'off by one': sum(1 for d in dev_b if abs(d) == 1), 'largest deviation': max(abs(d) for d in dev_b), 'first content off by more than one': next((c for c, d in enumerate(dev_b) if abs(d) > 1), None), 'clock at the frozen content: exact, three-term': [exact[top], three[top]], 'S over the wall as a fraction': str(Fraction(S3, wall3))})

# 8. the beat and the band: S = 0 at the vacuum, D(c) Gamma^2 = D(0) p0^2
den, G = 1021, 16; ok8 = True; numbers = {}
for num in (779, 1020, 1021):
    rule = rule3.rule_integers(num, den, gamma, gamma, gamma, None, G)
    six_R = sum(rule.reaches); wv = rule.wall
    ok8 &= rule.self_coefficient == 0 and six_R * den == 2 * wv * num
    numbers['num %d: S at the vacuum, 6R den - 2 w num' % num] = [int(rule.self_coefficient), int(six_R * den - 2 * wv * num)]
for c in (0, 7, 300, 1500):
    p0 = paces.clock(gamma, c)
    D0, Dc = rule3.mass(779, den, gamma, G), rule3.mass(779, den, p0, G)
    ok8 &= Dc * gamma * gamma == D0 * p0 * p0
    numbers['content %d: D(c) Gamma^2 - D(0) p0^2' % c] = int(Dc * gamma * gamma - D0 * p0 * p0)
check('8 one dispersion law: S = 0 at the vacuum (the band is the Links alone) and D(c) Gamma^2 = D(0) p0^2 (the beat is N sin(omega_0 / 2))', ok8, numbers)

# 9. the unit at the gap 0
T = 36000
check('9 NOT unified: the unit 3 T sine_den at num = den is 0; the massless unit 3 den T', 3 * T * sine_den(den, den) == 0 and 3 * den * T > 0, {'3 T sine_den(den, den)': 3 * T * sine_den(den, den), '3 den T': 3 * den * T, '3 T sine_den(779, 1021)': 3 * T * sine_den(779, den)})

# 10. the exclusion's dot with a one-component density
agree = 0
for _ in range(N):
    standing = rng.randint(0, 10 ** 6); child = rng.randint(1, 10 ** 6)
    agree += ((standing > 0) == (standing * child > 0))
check('10 the lay refusal is the exclusion dot with one component', agree == N, {'drawn': N, 'equal': agree})

# 11. the one turn: the toy's two roundings as one function
agree = 0
for _ in range(N):
    re_, im_, c, s, X = R(), R(), R(), R(), rng.randint(1, 10 ** 10)
    a_re = (c * re_ - s * im_); a_im = (s * re_ + c * im_)
    agree += turn_pair(re_, im_, c, s, X) == ((2 * a_re + X) // (2 * X), (2 * a_im + X) // (2 * X))
check('11 U2 one turn equals the inline spelling', agree == N, {'drawn': N, 'equal': agree})

print(json.dumps({'fd2 one-Node test': 'every check holds' if not failed else 'FAILED: %s' % failed}))
sys.exit(0 if not failed else 1)
