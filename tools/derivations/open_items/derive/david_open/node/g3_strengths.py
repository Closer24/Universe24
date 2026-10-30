"""G3, term 6's four strengths on the head, whole numbers alone (corrected after both hostile readers of f89b76a33).

(a) every tied family's spring from an A1 held count through the head's own tables, per kind: S_K = g n C[K, K -> A1];
(b) lam's bound, exact and not strict: 8 kappa V = (2 kappa (k - n) + g c)^2 + 4 kappa g n c + (2 kappa lam - g^2) c^2,
    so V is bounded below exactly when 2 kappa lam >= g^2; the least whole lam is the ceiling of g^2 / (2 kappa),
    (g^2 + 2 kappa - 1) div (2 kappa), one carry; below it a point of the (k, c) plane with V < 0 is written down (c
    need not be a square: the bound is algebra); on g, kappa up to 40 the old form g^2 div (2 kappa) + 1 is one too
    high exactly where 2 kappa divides g^2;
(b2) several tied families sharing the one held count: with a four-leg term on each family's own c, 8 kappa V =
    (2 kappa (k - n) + g C)^2 + 4 kappa g n C + 2 kappa lam sum c_f^2 - g^2 C^2 (C the sum of the c_f), bounded below
    exactly when 2 kappa lam >= N g^2 for N alike families; with one four-leg term on the summed C, the one-family
    bound; a written point with V < 0 for two families at the one-family least lam, each with its own term;
(b2') families with their own g_f and lam_f: 8 kappa V = (2 kappa (k - n) + S)^2 + 4 kappa n S + 2 kappa (the sum of
    lam_f c_f^2) - S^2, S the sum of g_f c_f, on every case with g_f, lam_f and kappa from 1 to 4; where the sum of
    g_f^2 / (2 kappa lam_f) passes 1, a written point with V < 0 on the ray c_f along g_f / lam_f (Cauchy-Schwarz's
    equality); where it does not, V >= 0 on a grid; and a case with a negative g_f, bounded below though the sum is 4/3;
(b3) 4.2's hat for the held count in place of the quadratic held spring: the clock's state is not the least;
(c) Animate's operation on the head's gear at the swings that ran away with no four-leg term (m3 (i)), at the least
    lam and at twice it: the gear stays or runs away, the held hand's least K and the rounds it stands below 0, the
    valley's K at the largest swing seen (n - g c / (2 kappa)), that swing against its reach (the largest c the kept
    energy allows on the valley), and the gear's sign changes over 4,000 rounds (the mass alone gives 63.7);
(c2) two tied families sharing the held count, laid alike: each with its own four-leg term at the one-family least
    lam, at twice it and at the two-family least; one four-leg term on the summed C at the one-family least;
(c3) at the least lam, the held hand laid on its valley (n - g C / (2 kappa)) instead of at n: the gear's sign changes,
    one family and two under one summed term, the held hand's lag behind its moving valley;
(c3') laid on its valley at its own least lam for the held hand's spring at 100, 25, 9 and 4 g n: the gear's sign
     changes and the held hand's largest lag behind its valley against the valley's largest drop;
(c4) the beat's two scales: at the least lam up to the step's limit (laid at 1.4, 3, 4 and 5 x 10^7), and a few
    thousand above the least (least + 100 and + 3,000 at 4 x 10^7, + 10,000 at 2 x 10^7); two families, each with its
    own term at the two-family least, one swinging alone; the held hand's spring kappa at 25, 9, 4, 2 and 1 times g n,
    the held hand laid on its valley at that kappa's least lam;
(c5) the spread over 40 lays (laid + 7919 d) of every case of (c) to (c4) that a single run cannot stand for: one
     family from n and from its valley at 1 to 4 x 10^7, above the least at 4 x 10^7, two families at 2 x 10^7, and the
     held hand's spring at 25, 9, 4 and 2 g n;
(c6) the step's edge: the least swing on the valley where V's Hessian in (x, k), [[g k + 3 lam c, g x], [g x, kappa]],
     passes 4 W (whole numbers: 4 W I - H not positive semidefinite); five lays each at 4, 4.2, 4.4 and 5 x 10^7, which
     stay and which run away, how many rounds before the runaway the Hessian and lam c alone pass 4 W, and the reach's
     c against the edge's;
(d) the two beats at small swings: the gear's (spring g n = W div 400) and the held hand's own (spring kappa = W div 16),
    counted as sign changes over 4,000 rounds.

Usage: python3 -I g3_strengths.py <src of tensor24-review at 9751f91c1>
"""

import itertools
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

matrix, weight = K.turns(L.star(3))
held = list(K.kinds(matrix))
inv = list(K.kinds(K.inverse(matrix)))
tab = L.tables(held, inv, weight, K.projector)
names = ["A1", "A2", "E", "T1", "T2"]
for kk in range(5):
    c = tab[(kk, kk, 0)]  # C[K, K -> A1], shape (1, d, d)
    print(f"(a) C[{names[kk]}, {names[kk]} -> A1] as the spring's matrix over g n: {c[0].tolist()}")


def ceiling(a, b):
    return carry(a + b - 1, b, 0)[0]


def four_v(g, lam, kappa, n, k, c):
    """4 V = 2 g k c + lam c^2 + 2 kappa (k - n)^2, the potential with its quarter cleared."""
    return 2 * g * k * c + lam * c * c + 2 * kappa * (k - n) ** 2


def identity_holds(g, lam, kappa, n, k, c):
    square = 2 * kappa * (k - n) + g * c
    return 2 * kappa * four_v(g, lam, kappa, n, k, c) == square * square + 4 * kappa * g * n * c + (2 * kappa * lam - g * g) * c * c


def below_zero(g, lam, kappa, n):
    """Below the bound (2 kappa lam < g^2): a whole point on the valley where V < 0."""
    c = 4 * kappa * g * n + kappa * kappa + 1
    k = n - carry(g * c + kappa, 2 * kappa, 0)[0]
    return k, c, four_v(g, lam, kappa, n, k, c) < 0


grid_identity = grid_bound = grid_below = old_high = old_high_where_divides = 0
for g in range(1, 41):
    for kappa in range(1, 41):
        least = ceiling(g * g, 2 * kappa)
        grid_identity += all(identity_holds(g, lam, kappa, 3, k, c) for lam in (least - 1, least, least + 1)
                             for k in range(-4, 5) for c in range(0, 9))
        grid_bound += int(2 * kappa * least >= g * g)
        grid_below += int(below_zero(g, least - 1, kappa, 3)[2])
        old = carry(g * g, 2 * kappa, 0)[0] + 1
        high = old != least
        divides = carry(g * g, 2 * kappa, 0)[1] == 0
        old_high += int(high)
        old_high_where_divides += int(high == divides)
print(f"(b) on g and kappa from 1 to 40 (1,600 pairs, n = 3): the identity holds at lam = least - 1, least, least + 1 on"
      f" 81 points each in {grid_identity} pairs; 2 kappa least >= g^2 in {grid_bound}; a point with V < 0 at least - 1 in"
      f" {grid_below}; g^2 div (2 kappa) + 1 above the ceiling in {old_high} pairs, exactly where 2 kappa divides g^2 in"
      f" {old_high_where_divides} of 1,600")

W = 6 * 15162856759112389 * 1000 * 1000
n, D, kappa = 10**6, carry(W, 400, 0)[0], carry(W, 16, 0)[0]
g, _ = carry(D, n, 0)
least = ceiling(g * g, 2 * kappa)
_, rest = carry(g * g, 2 * kappa, 0)
k0, c0, neg = below_zero(g, least - 1, kappa, n)
print(f"    on the probe's numbers: g = {g}, kappa = W div 16, 2 kappa divides g^2: {rest == 0}; the least whole lam"
      f" {least}; 2 kappa least - g^2 = {2 * kappa * least - g * g} >= 0; at {least - 1}, V < 0 at c = {c0}: {neg}")
least_two = ceiling(2 * g * g, 2 * kappa)


def four_v_families(lam, k, cs, summed):
    """4 V for families sharing k: a four-leg term on each c_f, or one on the summed C."""
    total = sum(cs)
    stop = lam * total * total if summed else lam * sum(c * c for c in cs)
    return 2 * g * k * total + stop + 2 * kappa * (k - n) ** 2


c_two = 4 * kappa * g * n + kappa * kappa + 1
k_two = n - carry(g * 2 * c_two + kappa, 2 * kappa, 0)[0]
own_neg = four_v_families(least, k_two, [c_two, c_two], False) < 0
summed_ok = all(
    2 * kappa * four_v_families(least, k, [c1, c2], True) >= 0
    for k in (k_two, n, -n) for c1, c2 in ((c_two, c_two), (c_two, 0), (10**14, 10**15))
)
identity_two = all(
    2 * kappa * four_v_families(lam, k, [c1, c2], False)
    == (2 * kappa * (k - n) + g * (c1 + c2)) ** 2 + 4 * kappa * g * n * (c1 + c2) + 2 * kappa * lam * (c1 * c1 + c2 * c2)
    - g * g * (c1 + c2) ** 2
    for lam in (least, least_two) for k in (-7, 0, 5, n) for c1 in (0, 3, 10**14) for c2 in (0, 2, 10**15)
)
print(f"(b2) two families sharing K, each with its own four-leg term: the identity on 72 points: {identity_two}; at the"
      f" one-family least lam, V < 0 at c1 = c2 = {c_two} on the valley: {own_neg}; the two-family least whole lam"
      f" {least_two} (the ceiling of 2 g^2 / (2 kappa)); one four-leg term on the summed C at the one-family least, V >= 0"
      f" at the same points: {summed_ok}")

def four_v_any(gs, lams, kap, base, k, cs):
    """4 V for families with their own g_f and lam_f sharing k: 2 k S + the sum of lam_f c_f^2 + 2 kappa (k - n)^2."""
    s = sum(gf * cf for gf, cf in zip(gs, cs, strict=True))
    return 2 * k * s + sum(lf * cf * cf for lf, cf in zip(lams, cs, strict=True)) + 2 * kap * (k - base) ** 2


def identity_any(gs, lams, kap, base, k, cs):
    """8 kappa V = (2 kappa (k - n) + S)^2 + 4 kappa n S + 2 kappa (the sum of lam_f c_f^2) - S^2, S = the sum of g_f c_f."""
    s = sum(gf * cf for gf, cf in zip(gs, cs, strict=True))
    stops = sum(lf * cf * cf for lf, cf in zip(lams, cs, strict=True))
    right = (2 * kap * (k - base) + s) ** 2 + 4 * kap * base * s + 2 * kap * stops - s * s
    return 2 * kap * four_v_any(gs, lams, kap, base, k, cs) == right


holds = combos = over_one = written = under_one = nonneg = 0
for g1, g2, l1, l2, kap in itertools.product(range(1, 5), repeat=5):
    combos += 1
    holds += all(identity_any((g1, g2), (l1, l2), kap, 3, k, (c1, c2))
                 for k in range(-4, 5) for c1 in (0, 1, 2, 5, 9) for c2 in (0, 1, 2, 5, 9))
    a_sum = g1 * g1 * l2 + g2 * g2 * l1  # the sum of g_f^2 / (2 kappa lam_f) is A / (2 kappa l1 l2)
    if a_sum > 2 * kap * l1 * l2:
        over_one += 1
        t = carry(4 * kap * 3 * a_sum + 4 * kap * kap, a_sum * (a_sum - 2 * kap * l1 * l2), 0)[0] + 1
        c1, c2 = t * g1 * l2, t * g2 * l1  # c_f along g_f / lam_f, Cauchy-Schwarz's equality
        k = 3 - carry(g1 * c1 + g2 * c2, 2 * kap, 0)[0]
        written += int(four_v_any((g1, g2), (l1, l2), kap, 3, k, (c1, c2)) < 0)
    else:
        under_one += 1
        nonneg += all(four_v_any((g1, g2), (l1, l2), kap, 3, k, (c1, c2)) >= 0
                      for k in range(-10, 11) for c1 in range(13) for c2 in range(13))
mixed = [four_v_any((2, -2), (1, 1), 3, 3, k, (c1, c2)) for k in range(-12, 13) for c1 in range(40) for c2 in range(40)]
wider = [four_v_any((2, -2), (1, 1), 3, 3, k, (c1, c2)) for k in range(-24, 25) for c1 in range(80) for c2 in range(80)]
print(f"(b2') two families with their own g_f and lam_f (1 to 4 each, kappa 1 to 4, n = 3; {combos} cases): the identity"
      f" on 225 points each in {holds}; the sum of g_f^2 / (2 kappa lam_f) above 1 in {over_one}, each with a written point"
      f" on the ray c_f along g_f / lam_f where V < 0: {written}; at or below 1 in {under_one}, V >= 0 on 3,549 points in"
      f" {nonneg}. With g = (2, -2), lam = (1, 1), kappa = 3 the sum is 4 / 3, yet 4 V stays at or above {min(mixed)} on"
      f" 40,000 points and {min(wider)} on 313,600: bounded below, while the clock's state (k = n, c = 0) gives 0 and is not"
      f" the least, since a negative g_f is a negative spring")


def four_v_hat(gg, mu, nu, lam_, k, c):
    """4 V with 4.2's hat for the held count, -(mu / 2) k^2 + (nu / 4) k^4, in place of (kappa / 2) (k - n)^2."""
    return 2 * gg * k * c + lam_ * c * c - 2 * mu * k * k + nu * k * k * k * k


hat_least = min((four_v_hat(4, 4, 1, 1, k, c), k, c) for k in range(-20, 21) for c in range(200))
print(f"(b3) 4.2's hat for the held count with g = 4, mu = 4, nu = 1 (so n = 2 and its spring kappa = 2 mu = 8), lam = 1,"
      f" the quadratic spring's least: 4 V at the clock's state (n, 0) {four_v_hat(4, 4, 1, 1, 2, 0)}, at (k, c) = (-3, 12)"
      f" {four_v_hat(4, 4, 1, 1, -3, 12)}; the least on k from -20 to 20 and c from 0 to 199, {hat_least[0]} at"
      f" (k, c) = ({hat_least[1]}, {hat_least[2]}): the clock's state is not the least")


def four_v_square(h, lam_, kap, base, k, c):
    """4 V with the tie through k^2 (the four-leg monomial A1 x A1 x K x K -> A1): 2 h k^2 c + lam c^2 + 2 kappa (k - n)^2."""
    return 2 * h * k * k * c + lam_ * c * c + 2 * kap * (k - base) ** 2


square_nonneg = all(four_v_square(h, 0, kap, 3, k, c) >= 0 for h in range(1, 5) for kap in range(1, 5)
                    for k in range(-12, 13) for c in range(40))
square_level = all(four_v_square(h, 0, kap, 3, 0, c) == 2 * kap * 9 for h in range(1, 5) for kap in range(1, 5)
                   for c in (0, 1, 7, 10**9, 10**30))
square_mirror = all(2 * h * 3 * 3 == 2 * h * (-3) * (-3) for h in range(1, 5))
print(f"(b4) the tie through k^2 in place of g k: 4 V >= 0 at lam = 0 on h and kappa from 1 to 4, k from -12 to 12 and c"
      f" from 0 to 39 (n = 3): {square_nonneg}; at k = 0, 4 V = 2 kappa n^2 for every c, so at lam = 0 the swing's potential"
      f" levels off: {square_level}; the tied spring h k^2 alike at k = n and k = -n: {square_mirror}")

CAP = 10**60



def rounded(a, b):
    """a / b rounded half up (a >= 0, b > 0): one carry."""
    return carry(2 * a + b, 2 * b, 0)[0]


def reach(lam, laid):
    """The largest c the kept energy allows on the valley: 4 kappa g n c + (2 kappa lam - g^2) c^2 <= 8 kappa E0."""
    e0 = 4 * kappa * g * n * laid * laid + 2 * kappa * lam * laid**4
    lo, hi = 0, 2
    while 4 * kappa * g * n * hi + (2 * kappa * lam - g * g) * hi * hi <= e0:
        hi *= 2
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        if 4 * kappa * g * n * mid + (2 * kappa * lam - g * g) * mid * mid <= e0:
            lo = mid
        else:
            hi = mid
    return lo


def run(lam, laid, rounds=4000):
    x, k = (laid, laid, 0), (n, n, 0)
    least_k, most_c = n, laid * laid
    below = changes = 0
    last = laid
    for t in range(1, rounds + 1):
        xx, kk = x[0], k[0]
        c = xx * xx
        half, _ = carry(g * c, 2, 0)
        px = -g * kk * xx - lam * c * xx
        pk = -half - kappa * (kk - n)
        x, k = step.gear(*x, W, px), step.gear(*k, W, pk)
        least_k = min(least_k, k[0])
        most_c = max(most_c, x[0] * x[0])
        below += int(k[0] < 0)
        changes += int(x[0] * last < 0)
        last = x[0] if x[0] else last
        if abs(x[0]) > CAP or abs(k[0]) > CAP:
            return f"runs past 10^60 at round {t}"
    valley = n - carry(g * most_c, 2 * kappa, 0)[0]
    tenths = rounded(10 * most_c, laid * laid)
    reach_tenths = rounded(10 * reach(lam, laid), laid * laid)
    return (f"stays over {rounds} rounds; least K {least_k}, below 0 in {below} rounds; the valley's K at the largest"
            f" swing {valley}; the largest c {tenths} tenths of the laid one, its reach {reach_tenths} tenths (rounded);"
            f" the gear's sign changes {changes}")


print("(c) X laid at rest, K at n:")
for laid in (10**5, 10**7, 2 * 10**7, 10**8):
    print(f"    at {laid}: lam 0: {run(0, laid)}")
    print(f"      the least lam: {run(least, laid)}")
    print(f"      twice the least: {run(2 * least, laid)}")

FOUR_W = 4 * W


def hessian_over(x, k, lam, spring=kappa):
    """The largest root of V's Hessian in (x, k), [[g k + 3 lam c, g x], [g x, spring]], passes 4 W: 4 W I - H is not
    positive semidefinite, read by its two diagonal entries and its determinant, whole numbers."""
    a, b = g * k + 3 * lam * x * x, g * x
    return not (FOUR_W - a >= 0 and FOUR_W - spring >= 0 and (FOUR_W - a) * (FOUR_W - spring) >= b * b)


def trace(lam, lays, k_laid, spring, summed=True, rounds=4000):
    """Families sharing the held count with the one g, laid at lays, the held hand laid at k_laid with its spring, a
    four-leg term on the summed C or on each family's own c. The first family's sign changes, the round past 10^60 or
    None, the least K, the first family's largest c, the held hand's largest lag behind its valley n - g C / (2 spring)
    against the valley's largest drop, and for one family whether V's Hessian ever passes 4 W."""
    xs, k = [(v, v, 0) for v in lays], (k_laid, k_laid, 0)
    changes, last = 0, lays[0]
    least_k, most_c = k_laid, lays[0] * lays[0]
    most_lag = most_drop = 0
    over = False
    for t in range(1, rounds + 1):
        a = [x[0] for x in xs]
        kk = k[0]
        cs = [v * v for v in a]
        total = sum(cs)
        half, _ = carry(g * total, 2, 0)
        xs = [step.gear(*x, W, -g * kk * v - lam * (total if summed else cf) * v) for x, v, cf in zip(xs, a, cs, strict=True)]
        k = step.gear(*k, W, -half - spring * (kk - n))
        now = xs[0][0]
        changes += int(now * last < 0)
        last = now if now else last
        least_k = min(least_k, k[0])
        most_c = max(most_c, now * now)
        drop = carry(g * sum(x[0] * x[0] for x in xs), 2 * spring, 0)[0]
        most_drop = max(most_drop, drop)
        most_lag = max(most_lag, abs(k[0] - (n - drop)))
        if len(lays) == 1:
            over = over or hessian_over(now, k[0], lam, spring)
        if max(abs(x[0]) for x in xs) > CAP or abs(k[0]) > CAP:
            return {"gone": t, "changes": changes}
    return {"gone": None, "changes": changes, "least_k": least_k, "most_c": most_c, "lag": most_lag, "drop": most_drop,
            "over": over}


def swings(lam, laid, rounds):
    """The one family's swing after each round, the held hand laid at n: out[t] after round t, out[0] the lay."""
    x, k = (laid, laid, 0), (n, n, 0)
    out = [laid]
    for _ in range(rounds):
        xx, kk = x[0], k[0]
        c = xx * xx
        half, _ = carry(g * c, 2, 0)
        x = step.gear(*x, W, -g * kk * xx - lam * c * xx)
        k = step.gear(*k, W, -half - kappa * (kk - n))
        out.append(x[0])
    return out


LAYS, STRIDE = 40, 7919


def lays_of(laid):
    return [laid + STRIDE * d for d in range(LAYS)]


def mean_range(values):
    """The mean to one place, rounded half up, then the least to the most."""
    whole, tenth = carry(rounded(10 * sum(values), len(values)), 10, 0)
    return f"{whole}.{tenth} ({min(values)} to {max(values)})"


def over_lays(lam, laid, k_rule, spring, fams=1, summed=True, alone=False):
    """The trace over the 40 lays: k_rule 'n' lays the held hand at n, 'valley' on the laid swing's valley; alone lays
    every family past the first at rest."""
    out = []
    for lay in lays_of(laid):
        lays_f = [lay] + [0 if alone else lay] * (fams - 1)
        total = sum(v * v for v in lays_f)
        k_laid = n if k_rule == "n" else n - carry(g * total, 2 * spring, 0)[0]
        out.append(trace(lam, lays_f, k_laid, spring, summed))
    return out


def counts_text(results, lag=False, hessian=False):
    kept = [r for r in results if r["gone"] is None]
    gone = [r["gone"] for r in results if r["gone"] is not None]
    if not kept:
        return f"all {len(results)} run away (rounds {min(gone)} to {max(gone)})"
    counts = [r["changes"] for r in kept]
    text = f"{mean_range(counts)}, above the mass in {sum(1 for c in counts if c >= 65)}"
    if gone:
        text += f", {len(gone)} run away (rounds {min(gone)} to {max(gone)})"
    if lag:
        text += f", the lag {mean_range([carry(1000 * r['lag'], r['drop'], 0)[0] for r in kept])} per mille"
    if hessian:
        text += f", the Hessian past 4 W in {sum(1 for r in kept if r['over'])}"
    return text


def table_rows(lam, laid):
    """The (c) table's numbers over the 40 lays."""
    rows = [(trace(lam, [lay], n, kappa), lay) for lay in lays_of(laid)]
    kept = [(r, lay) for r, lay in rows if r["gone"] is None]
    least_ks = [r["least_k"] for r, _ in kept]
    valleys = [n - carry(g * r["most_c"], 2 * kappa, 0)[0] for r, _ in kept]
    cs = [rounded(10 * r["most_c"], lay * lay) for r, lay in kept]
    reaches = [rounded(10 * reach(lam, lay), lay * lay) for _, lay in kept]
    return (f"the least K from {min(least_ks)} to {max(least_ks)}, the valley's K at the largest swing from {min(valleys)}"
            f" to {max(valleys)}, the largest c from {min(cs)} to {max(cs)} tenths and its reach from {min(reaches)} to"
            f" {max(reaches)}, the sign changes {mean_range([r['changes'] for r, _ in kept])},"
            f" {len(rows) - len(kept)} run away")


near, far = swings(least, 2 * 10**7, 1000), swings(least, 2 * 10**7 + 1, 1000)
gaps = [abs(near[t] - far[t]) for t in (1, 250, 500, 1000)]
near, far = swings(least, 10**7, 4000), swings(least, 10**7 + 1, 4000)
print(f"(c5) two runs laid one count apart, the least lam, the held hand at n: at 2 x 10^7 they part by {gaps[0]}, {gaps[1]},"
      f" {gaps[2]} and {gaps[3]} counts after rounds 1, 250, 500 and 1,000; at 10^7 by {abs(near[4000] - far[4000])} after"
      " round 4,000. Every case below is read over the 40 lays laid + 7919 d (d = 0 to 39): the gear's sign changes in"
      " 4,000 rounds, the mean (rounded), the least to the most, and how many count above the mass (65 or more; the mass's"
      " 63.7 counts 63 or 64); on the valley the held hand's largest lag behind it against its largest drop")
for laid in (10**7, 2 * 10**7, 3 * 10**7, 4 * 10**7):
    print(f"    one family, the least lam, laid at {carry(laid, 10**7, 0)[0]} x 10^7: the held hand at n"
          f" {counts_text(over_lays(least, laid, 'n', kappa))}; on its valley"
          f" {counts_text(over_lays(least, laid, 'valley', kappa), lag=True)}")
for laid in (10**7, 2 * 10**7):
    print(f"    twice the least, the held hand at n, laid at {carry(laid, 10**7, 0)[0]} x 10^7:"
          f" {counts_text(over_lays(2 * least, laid, 'n', kappa))}")
for extra in (100, 3000, 10000):
    print(f"    least + {extra} at 4 x 10^7, the held hand at n: {counts_text(over_lays(least + extra, 4 * 10**7, 'n', kappa))}")
for laid in (10**7, 2 * 10**7):
    m = carry(laid, 10**7, 0)[0]
    print(f"    two families laid alike at {m} x 10^7, the held hand at n: each its own term at the one-family least"
          f" {counts_text(over_lays(least, laid, 'n', kappa, 2, False))}; each its own term at twice it"
          f" {counts_text(over_lays(2 * least, laid, 'n', kappa, 2, False))}; each its own term at the two-family least"
          f" {counts_text(over_lays(least_two, laid, 'n', kappa, 2, False))}; one summed term at the one-family least"
          f" {counts_text(over_lays(least, laid, 'n', kappa, 2))}")
    print(f"    two families at {m} x 10^7, the first swinging alone, the held hand at n: one summed term at the one-family"
          f" least {counts_text(over_lays(least, laid, 'n', kappa, 2, True, True))}; each its own term at the two-family"
          f" least {counts_text(over_lays(least_two, laid, 'n', kappa, 2, False, True))}; laid alike on their valley,"
          f" one summed term {counts_text(over_lays(least, laid, 'valley', kappa, 2))}")
for times, laids in ((100, (1, 2, 3)), (25, (1, 2, 3, 4)), (9, (1, 2)), (4, (1, 2)), (2, (1, 2))):
    spring = times * g * n
    lam_k = ceiling(g * g, 2 * spring)
    parts = [f"at {m} x 10^7 {counts_text(over_lays(lam_k, m * 10**7, 'valley', spring), lag=True)}" for m in laids]
    print(f"    the held hand's spring at {times} g n, its own least lam, laid on its valley: " + "; ".join(parts))
spring = 100 * g * n
lam_k = ceiling(g * g, 2 * spring)
parts = [f"at {4 * m} x 10^7 ((g x / kappa)^2 = {16 * m * m} hundredths)"
         f" {counts_text(over_lays(lam_k, 4 * m * 10**7, 'valley', spring), lag=True, hessian=True)}" for m in (1, 2, 3, 4)]
print("    the inertia's own reading, the held hand's spring at 100 g n on its valley at four times 25 g n's lays, where"
      " (g x / kappa)^2 is the same: " + "; ".join(parts))
print(f"    the (c) table's rows over the 40 lays: the least lam at 10^7: {table_rows(least, 10**7)}; twice the least at"
      f" 10^7: {table_rows(2 * least, 10**7)}; the least lam at 2 x 10^7: {table_rows(least, 2 * 10**7)}")


def edge_swing(lam):
    """The least whole swing, on the valley at lam, where the Hessian's largest root passes 4 W: a search on the swing."""
    def past(x):
        return hessian_over(x, n - carry(g * x * x, 2 * kappa, 0)[0], lam)

    lo, hi = 0, 1
    while not past(hi):
        hi *= 2
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        if past(mid):
            hi = mid
        else:
            lo = mid
    return hi


edge = edge_swing(least)
TEN_EDGES = 10 * edge


def domain_run(lam, laid, rounds=4000):
    """The held hand at n. Returns the round the swing passes ten edges (or None), the largest swing, the first rounds the
    Hessian and lam c alone pass 4 W, and, for a run past ten edges, whether it passes 10^60 within 400 more rounds."""
    x, k = (laid, laid, 0), (n, n, 0)
    first_h = first_l = None
    most = abs(laid)
    for t in range(1, rounds + 1):
        xx, kk = x[0], k[0]
        c = xx * xx
        half, _ = carry(g * c, 2, 0)
        x = step.gear(*x, W, -g * kk * xx - lam * c * xx)
        k = step.gear(*k, W, -half - kappa * (kk - n))
        most = max(most, abs(x[0]))
        if first_h is None and hessian_over(x[0], k[0], lam):
            first_h = t
        if first_l is None and lam * x[0] * x[0] > FOUR_W:
            first_l = t
        if abs(x[0]) > TEN_EDGES:
            for _ in range(400):
                xx, kk = x[0], k[0]
                c = xx * xx
                half, _ = carry(g * c, 2, 0)
                x = step.gear(*x, W, -g * kk * xx - lam * c * xx)
                k = step.gear(*k, W, -half - kappa * (kk - n))
                if abs(x[0]) > CAP or abs(k[0]) > CAP:
                    return t, most, first_h, first_l, True
            return t, most, first_h, first_l, False
    return None, most, first_h, first_l, None


meets = ceiling(4 * kappa * g * n + g * g * edge * edge, 2 * kappa * edge * edge) - least
print(f"(c6) the step's edge at the least lam: the Hessian's largest root passes 4 W on the valley from a swing of {edge}"
      f" (lam c alone reaches 4 W only at c = 4 W / lam, {carry(FOUR_W, least, 0)[0]}); the excess's scale,"
      f" C = 4 kappa g n / (2 kappa lam - g^2), meets the edge's c at lam = the least + {meets} (lam / 400 ="
      f" {carry(least, 400, 0)[0]}). 40 lays each, the held hand at n: a run away passes ten edges' swing; the rest stay"
      " within the edge or past it, bounded over 4,000 rounds")
for laid in (40 * 10**6, 42 * 10**6, 44 * 10**6, 50 * 10**6):
    away, inside, past_edge, leads_h, leads_l, hess_kept, to_cap = [], 0, [], [], [], 0, True
    for lay in lays_of(laid):
        gone, most, first_h, first_l, capped = domain_run(least, lay)
        if gone:
            away.append(gone)
            to_cap = to_cap and capped
            leads_h.append(gone - first_h if first_h is not None and first_h <= gone else -1)
            leads_l.append(gone - first_l if first_l is not None and first_l <= gone else -1)
        else:
            hess_kept += int(first_h is not None)
            if most <= edge:
                inside += 1
            else:
                past_edge.append(most)
    text = f"    laid at {carry(laid, 10**6, 0)[0]} x 10^6: {len(away)} run away"
    if away:
        text += (f" (past ten edges at rounds {min(away)} to {max(away)}, each past 10^60 within 400 more rounds: {to_cap};"
                 f" the Hessian passes 4 W first in {sum(1 for v in leads_h if v >= 0)} of them, {min(leads_h)} to"
                 f" {max(leads_h)} rounds before, lam c alone {min(leads_l)} to {max(leads_l)})")
    text += f", {inside} stay within the edge, {len(past_edge)} past it and bounded"
    if past_edge:
        text += f" (largest swing {min(past_edge)} to {max(past_edge)})"
    text += (f"; of the {LAYS - len(away)} that do not run away, the Hessian passes 4 W in {hess_kept}; the reach's c over"
             f" the edge's, {carry(100 * reach(least, laid), edge * edge, 0)[0]} hundredths")
    print(text)


def crossings(lam, x_laid, k_laid, rounds=4000):
    x, k = (x_laid, x_laid, 0), (k_laid, k_laid, 0)
    seen_x = seen_k = 0
    last_x, last_k = x[0], k[0] - n
    for _ in range(rounds):
        xx, kk = x[0], k[0]
        c = xx * xx
        half, _ = carry(g * c, 2, 0)
        x = step.gear(*x, W, -g * kk * xx - lam * c * xx)
        k = step.gear(*k, W, -half - kappa * (kk - n))
        seen_x += int(x[0] * last_x < 0)
        seen_k += int((k[0] - n) * last_k < 0)
        last_x = x[0] if x[0] else last_x
        last_k = k[0] - n if k[0] != n else last_k
    return seen_x, seen_k


SCALE = 10**40


def arctan_inverse(m):
    """arctan(1 / m) times SCALE by its series, whole numbers."""
    total, power, j = 0, carry(SCALE, m, 0)[0], 0
    while power:
        term = carry(power, 2 * j + 1, 0)[0]
        total += -term if j % 2 else term
        power = carry(power, m * m, 0)[0]
        j += 1
    return total


PI = 16 * arctan_inverse(5) - 4 * arctan_inverse(239)  # Machin's formula, pi times SCALE


def sine(x):
    """sin(x / SCALE) times SCALE, 0 <= x <= SCALE * 2, by its series."""
    total, term, j = 0, x, 0
    while term:
        total += -term if j % 2 else term
        j += 1
        term = carry(carry(term * x, SCALE, 0)[0] * x, SCALE * (2 * j) * (2 * j + 1), 0)[0]
    return total


def beats_expected(spring, rounds=4000):
    """rounds omega / pi for 4 sin^2 (omega / 2) = spring / W, to one place: the largest h (hundredths) with
    4 W sin^2 (pi h / (200 rounds)) <= spring, the sine rising on [0, pi / 2], then rounded to tenths."""
    lo, hi = 0, 100 * rounds
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        s = sine(carry(PI * mid, 200 * rounds, 0)[0])
        if 4 * W * s * s <= spring * SCALE * SCALE:
            lo = mid
        else:
            hi = mid
    whole, tenth = carry(carry(lo + 5, 10, 0)[0], 10, 0)
    return f"{whole}.{tenth}"


gear_beats, _ = crossings(least, 10**5, n)
_, held_beats = crossings(least, 0, n + 10**5)
print(f"(d) sign changes over 4,000 rounds: the gear laid at 10^5 with K at n, {gear_beats}; the held hand laid 10^5 off"
      f" n with no swing, {held_beats}; 4 sin^2 (omega / 2) = spring / W gives 4,000 omega / pi = {beats_expected(g * n)}"
      f" and {beats_expected(kappa)} (computed: the sine by its series, pi by Machin's formula, to 40 places); kappa ="
      f" W div 16 is 25 g n + {kappa - 25 * g * n}")


def root(m):
    """The largest r with r^2 <= m, by bisection."""
    lo, hi = 0, m + 1
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        if mid * mid <= m:
            lo = mid
        else:
            hi = mid
    return lo


def held_on_valley(q_hundredths):
    """The motion held exactly on its valley at the least lam: the kinetic energy (W / 2) (1 + (g x / kappa)^2) x'^2 and
    the potential (g n / 2) x^2, so its period over the small swing's is (2 / pi) times the integral over [0, pi / 2] of
    root(1 + q sin^2), q = (g A / kappa)^2: Gauss's arithmetic-geometric mean, (a0^2 - the sum of 2^(j - 1) c_j^2) / M
    with a0 = root(1 + q), b0 = 1, c0^2 = q; times SCALE."""
    s2 = SCALE * SCALE
    a0_squared = carry((100 + q_hundredths) * s2, 100, 0)[0]
    a, b = root(a0_squared), SCALE
    total = carry(q_hundredths * s2, 200, 0)[0]
    weight = 1
    for _ in range(80):
        c = carry(a - b, 2, 0)[0]
        if c == 0:
            break
        a, b = carry(a + b, 2, 0)[0], root(a * b)
        total += weight * c * c
        weight *= 2
    return carry(a0_squared - total, a, 0)[0]


def hundredths_of_beats(spring, rounds=4000):
    lo, hi = 0, 100 * rounds
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        s = sine(carry(PI * mid, 200 * rounds, 0)[0])
        if 4 * W * s * s <= spring * SCALE * SCALE:
            lo = mid
        else:
            hi = mid
    return lo


small = hundredths_of_beats(g * n)
held = []
for q in (16, 64, 144, 256):
    count = carry(small * SCALE, held_on_valley(q), 0)[0]
    whole, part = carry(count, 100, 0)
    held.append(f"{whole}.{part:02d} at (g x / kappa)^2 = {q} hundredths")
print("(e) the motion held exactly on its valley at the least lam beats slower than the small swing (its period by the"
      " arithmetic-geometric mean): the sign changes in 4,000 rounds, " + "; ".join(held))
