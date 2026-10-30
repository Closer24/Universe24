"""G3, term 6's four strengths on the head, whole numbers alone (corrected after both hostile readers of f89b76a33).

(a) every tied family's spring from an A1 held count through the head's own tables, per kind: S_K = g n C[K, K -> A1];
(b) lam's bound, exact and not strict: 8 kappa V = (2 kappa (k - n) + g c)^2 + 4 kappa g n c + (2 kappa lam - g^2) c^2,
    so V is bounded below exactly when 2 kappa lam >= g^2; the least whole lam is the ceiling of g^2 / (2 kappa),
    (g^2 + 2 kappa - 1) div (2 kappa), one carry; below it a point with V < 0 is written down; on g, kappa up to 40 the
    old form g^2 div (2 kappa) + 1 is one too high exactly where 2 kappa divides g^2;
(b2) several tied families sharing the one held count: with a four-leg term on each family's own c, 8 kappa V =
    (2 kappa (k - n) + g C)^2 + 4 kappa g n C + 2 kappa lam sum c_f^2 - g^2 C^2 (C the sum of the c_f), bounded below
    exactly when 2 kappa lam >= N g^2 for N alike families; with one four-leg term on the summed C, the one-family
    bound; a written point with V < 0 for two families at the one-family least lam, each with its own term;
(c) Animate's operation on the head's gear at the swings that ran away with no four-leg term (m3 (i)), at the least
    lam and at twice it: the gear stays or runs away, the held hand's least K and the rounds it stands below 0, the
    valley's K at the largest swing seen (n - g c / (2 kappa)), that swing against its reach (the largest c the kept
    energy allows on the valley), and the gear's sign changes over 4,000 rounds (the mass alone gives 63.7);
(c2) two tied families sharing the held count, laid alike: each with its own four-leg term at the one-family least
    lam, at twice it and at the two-family least; one four-leg term on the summed C at the one-family least;
(c3) at the least lam, the held hand laid on its valley (n - g C / (2 kappa)) instead of at n: the gear's sign changes,
    one family and two under one summed term, the held hand's lag behind its moving valley;
(c4) the beat's two scales: at the least lam up to the step's limit (laid at 1.4, 3, 4 and 5 x 10^7), and a few
    thousand above the least (least + 100 and + 3,000 at 4 x 10^7, + 10,000 at 2 x 10^7); two families, each with its
    own term at the two-family least, one swinging alone; the held hand's spring kappa at 25, 9, 4, 2 and 1 times g n,
    the held hand laid on its valley at that kappa's least lam;
(d) the two beats at small swings: the gear's (spring g n = W div 400) and the held hand's own (spring kappa = W div 16),
    counted as sign changes over 4,000 rounds.

Usage: python3 -I g3_strengths.py <src of tensor24-review at 9751f91c1>
"""

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
n, D, kappa = 10**6, W // 400, W // 16
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
CAP = 10**60


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
    tenths, _ = carry(10 * most_c, laid * laid, 0)
    reach_tenths, _ = carry(10 * reach(lam, laid), laid * laid, 0)
    return (f"stays over {rounds} rounds; least K {least_k}, below 0 in {below} rounds; the valley's K at the largest"
            f" swing {valley}; the largest c {tenths} tenths of the laid one, its reach {reach_tenths} tenths; the gear's"
            f" sign changes {changes}")


print("(c) X laid at rest, K at n:")
for laid in (10**5, 10**7, 2 * 10**7, 10**8):
    print(f"    at {laid}: lam 0: {run(0, laid)}")
    print(f"      the least lam: {run(least, laid)}")
    print(f"      twice the least: {run(2 * least, laid)}")


def run_two(lam, laid, summed, rounds=4000):
    xs, k = [(laid, laid, 0), (laid, laid, 0)], (n, n, 0)
    least_k, changes, last = n, [0, 0], [laid, laid]
    for t in range(1, rounds + 1):
        a = [x[0] for x in xs]
        kk = k[0]
        cs = [v * v for v in a]
        total = cs[0] + cs[1]
        half, _ = carry(g * total, 2, 0)
        xs = [step.gear(*x, W, -g * kk * v - lam * (total if summed else cf) * v) for x, v, cf in zip(xs, a, cs, strict=True)]
        k = step.gear(*k, W, -half - kappa * (kk - n))
        least_k = min(least_k, k[0])
        for i in range(2):
            changes[i] += int(xs[i][0] * last[i] < 0)
            last[i] = xs[i][0] if xs[i][0] else last[i]
        if max(abs(xs[0][0]), abs(xs[1][0]), abs(k[0])) > CAP:
            return f"runs past 10^60 at round {t}"
    return f"stays over {rounds} rounds, least K {least_k}, sign changes {changes[0]} and {changes[1]}"


print("(c2) two families laid alike, sharing K:")
for laid in (10**7, 2 * 10**7):
    print(f"    at {laid}: each its own term, the one-family least: {run_two(least, laid, False)}")
    print(f"      each its own term, twice the one-family least: {run_two(2 * least, laid, False)}")
    print(f"      each its own term, the two-family least {least_two}: {run_two(least_two, laid, False)}")
    print(f"      one term on the summed C, the one-family least: {run_two(least, laid, True)}")


def beats_from(laid, k_laid, fams, rounds=4000):
    xs, k = [(laid, laid, 0) for _ in range(fams)], (k_laid, k_laid, 0)
    changes, last = [0] * fams, [laid] * fams
    for _ in range(rounds):
        a = [x[0] for x in xs]
        kk = k[0]
        total = sum(v * v for v in a)
        half, _ = carry(g * total, 2, 0)
        xs = [step.gear(*x, W, -g * kk * v - least * total * v) for x, v in zip(xs, a, strict=True)]
        k = step.gear(*k, W, -half - kappa * (kk - n))
        for i in range(fams):
            changes[i] += int(xs[i][0] * last[i] < 0)
            last[i] = xs[i][0] if xs[i][0] else last[i]
    return changes


lines = []
for fams in (1, 2):
    for laid in (10**7, 2 * 10**7):
        valley = n - carry(g * fams * laid * laid, 2 * kappa, 0)[0]
        lines.append(f"{fams} at {laid}: from n {beats_from(laid, n, fams)}, from the valley {valley} {beats_from(laid, valley, fams)}")
print("(c3) the least lam, one family or two under one summed term, sign changes in 4,000 rounds (the mass 63.7): " + "; ".join(lines))


def general(lam, lays, k_laid, spring, summed, rounds=4000):
    """Families sharing K with the one g: lays per family, the held hand laid at k_laid with its spring; a four-leg
    term on the summed C or on each family's c. Returns the sign changes per family and the round it ran away."""
    xs, k = [(v, v, 0) for v in lays], (k_laid, k_laid, 0)
    changes, last = [0] * len(lays), list(lays)
    for t in range(1, rounds + 1):
        a = [x[0] for x in xs]
        kk = k[0]
        cs = [v * v for v in a]
        total = sum(cs)
        half, _ = carry(g * total, 2, 0)
        xs = [step.gear(*x, W, -g * kk * v - lam * (total if summed else cf) * v) for x, v, cf in zip(xs, a, cs, strict=True)]
        k = step.gear(*k, W, -half - spring * (kk - n))
        for i in range(len(lays)):
            changes[i] += int(xs[i][0] * last[i] < 0)
            last[i] = xs[i][0] if xs[i][0] else last[i]
        if max(abs(x[0]) for x in xs) > CAP or abs(k[0]) > CAP:
            return changes, t
    return changes, None


def shown_run(result):
    changes, gone = result
    return f"runs away at round {gone}" if gone else "/".join(str(c) for c in changes)


scale = [f"{laid // 10**6 / 10} x 10^7 {shown_run(general(least, [laid], n, kappa, True))}" for laid in (14 * 10**6, 3 * 10**7, 4 * 10**7, 5 * 10**7)]
above = [f"least + {extra} at {laid // 10**7} x 10^7 {shown_run(general(least + extra, [laid], n, kappa, True))}" for extra, laid in ((100, 4 * 10**7), (3000, 4 * 10**7), (10000, 2 * 10**7))]
alone = [f"{laid // 10**7} x 10^7: each its own term {shown_run(general(least_two, [laid, 0], n, kappa, False))}, one summed term at the one-family least {shown_run(general(least, [laid, 0], n, kappa, True))}" for laid in (10**7, 2 * 10**7)]
springs = []
for times in (25, 9, 4, 2, 1):
    spring = times * g * n
    lam_k = ceiling(g * g, 2 * spring)
    out = []
    for laid in (10**7, 2 * 10**7):
        valley = n - carry(g * laid * laid, 2 * spring, 0)[0]
        out.append(shown_run(general(lam_k, [laid], valley, spring, True)))
    springs.append(f"{times} g n: {' and '.join(out)}")
print("(c4) sign changes in 4,000 rounds (the mass 63.7), the held hand laid at n unless named:")
print("    the least lam laid at " + "; ".join(scale))
print("    above the least: " + "; ".join(above))
print("    two families, the first swinging alone, the second at rest: " + "; ".join(alone))
print("    kappa at k g n, its own least lam, the held hand laid on its valley, laid at 10^7 and 2 x 10^7: " + "; ".join(springs))


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


gear_beats, _ = crossings(least, 10**5, n)
_, held_beats = crossings(least, 0, n + 10**5)
print(f"(d) sign changes over 4,000 rounds: the gear laid at 10^5 with K at n, {gear_beats}; the held hand laid 10^5 off"
      f" n with no swing, {held_beats}; 4 sin^2 (omega / 2) = spring / W gives 4,000 omega / pi = 63.7 and 319.2")
