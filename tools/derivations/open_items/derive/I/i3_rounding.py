"""I3 (drafter I): what Rule3's rounding does to the charge, in integers alone (no engine import).
Run: python3 -I i3_rounding.py [--mutant NAME]

The step of one hand at one Node-clock as the head writes it (tick.impulse, tick.carry, core/acts.carry):
  P  = w (a - b) + r - mid(w)                      the stride's exact momentum (a now, b before, r the fine tooth)
  P' = P + X pull                                  the impulse, pull a Gaussian integer
  v  = (P' + mid(w')) div w',  r' = (P' + mid(w')) mod w',  a' = a + v      one carry per gear (Rule3)
with mid(w) = w div 2. D = Im(conj(a) P), rho' = r' - mid(w').
Checks:
  R1 the identity D' - D = X Im(conj(a) pull) + Im(conj(v) rho') at every integer (random, to 2^200, both signs),
     and Im(conj(v) rho') = Im(conj(v) P')
  R2 the theorem: where gcd(P'_3, P'_12) = 1 and max |P'_k| >= w', no quotient v in Z[i] with every remainder
     |P'_k - w' v_k| < w' has Im(conj(v) P') = 0: exhaustive over a box
  R3 the quadratic invariants of one isolated Node-clock's integer step: the null space over Q of
     f(step(s)) - f(s) = 0 over the 28 monomials of degree <= 2 in (a3, a12, b3, b12, r3, r12);
     control: the exact rational step, whose null space holds the charge
  R4 the turn's rounding: the head's odd rounding of a turned hand (rates.rounded) leaves the Mesh current
     not antisymmetric, the exact turn leaves it antisymmetric
Mutants: no_rho (R1 without the carry's term), even_round (R4 with the exact turn replaced by the rounded one
         at both ends, as if a rounding could be antisymmetric), wrong_mid (R1 with mid(w) in place of mid(w')).
"""
import random
import sys
from fractions import Fraction as Fr
from math import gcd

MUT = sys.argv[sys.argv.index('--mutant') + 1] if '--mutant' in sys.argv else ''
RES = []


def report(name, ok, detail):
    RES.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")


def mid(w):
    return w // 2


def carry(total, teeth, fine):
    carried = total + fine
    q = carried // teeth
    return q, carried - teeth * q


def im_cb(p, q):
    return p[0] * q[1] - p[1] * q[0]


def step(a, b, r, w, w1, X, pull):
    P = tuple(w * (a[k] - b[k]) + r[k] - mid(w) for k in range(2))
    P1 = tuple(P[k] + X * pull[k] for k in range(2))
    v, r1 = zip(*(carry(P1[k], w1, mid(w1)) for k in range(2)))
    a1 = (a[0] + v[0], a[1] + v[1])
    rho1 = tuple(r1[k] - mid(w1 if MUT != 'wrong_mid' else w) for k in range(2))
    return P, P1, v, r1, rho1, a1


def r1():
    rng = random.Random(31)
    bad = bad2 = n = 0
    for trial in range(20000):
        bits = rng.choice((8, 30, 64, 200))
        w = rng.randint(2, 2 ** bits)
        w1 = rng.randint(2, 2 ** bits)
        X = rng.randint(-2 ** bits, 2 ** bits)
        a = (rng.randint(-2 ** bits, 2 ** bits), rng.randint(-2 ** bits, 2 ** bits))
        b = (a[0] + rng.randint(-2 ** 10, 2 ** 10), a[1] + rng.randint(-2 ** 10, 2 ** 10))
        r = (rng.randrange(w), rng.randrange(w))
        pull = (rng.randint(-2 ** bits, 2 ** bits), rng.randint(-2 ** bits, 2 ** bits))
        if trial < 40:                       # the edges: 0 and the smallest teeth
            w, w1 = 2, 2 + trial % 3
            a, b, r, pull, X = (0, 0), (0, 0), (0, trial % 2), (trial - 20, 0), trial % 5
        P, P1, v, r1_, rho1, a1 = step(a, b, r, w, w1, X, pull)
        D0 = im_cb(a, P)
        Pn = tuple(w1 * (a1[k] - a[k]) + r1_[k] - mid(w1) for k in range(2))   # the next tick's reading of P'
        D1 = im_cb(a1, Pn)
        E = im_cb(v, rho1)
        term = E if MUT != 'no_rho' else 0
        n += 1
        bad += int(D1 - D0 != X * im_cb(a, pull) + term) + int(Pn != P1)
        bad2 += int(E != im_cb(v, P1))
    report("R1 D' - D = X Im(conj(a) pull) + Im(conj(v) rho') exactly, and the momentum carried exactly", bad == 0,
           f"{bad} failures in {n} random steps to 2^200 (both signs, the edges 0 and teeth 2 among them)")
    report("R1b the carry's charge E = Im(conj(v) rho') = Im(conj(v) P')", bad2 == 0, f"{bad2} failures in {n}")


def r2():
    found_any = primitive_cases = keep_possible = nonprim_keep = nonprim = 0
    head_E0 = head_n = 0
    for w1 in range(2, 13):
        for p3 in range(-60, 61):
            for p12 in range(-60, 61):
                if (p3, p12) == (0, 0):
                    continue
                cands = []
                for v3 in range(p3 // w1 - 1, p3 // w1 + 3):
                    for v12 in range(p12 // w1 - 1, p12 // w1 + 3):
                        if abs(p3 - w1 * v3) < w1 and abs(p12 - w1 * v12) < w1:
                            cands.append((v3, v12))
                keeps = [v for v in cands if im_cb(v, (p3, p12)) == 0]
                big = max(abs(p3), abs(p12)) >= w1
                if gcd(abs(p3), abs(p12)) == 1 and big:
                    primitive_cases += 1
                    found_any += int(len(keeps) > 0)
                elif big:
                    nonprim += 1
                    nonprim_keep += int(len(keeps) > 0)
                v = ((p3 + mid(w1)) // w1, (p12 + mid(w1)) // w1)
                head_n += 1
                head_E0 += int(im_cb(v, (p3, p12)) == 0)
    report("R2 no carry keeps the charge where P' is primitive and outgrows the teeth", found_any == 0,
           f"{primitive_cases} primitive momenta with max |P'_k| >= w' (w' = 2..12, |P'_k| <= 60): a charge-keeping "
           f"quotient with every remainder inside the teeth at {found_any}; among the {nonprim} non-primitive ones it "
           f"exists at {nonprim_keep}; the head's mid carry keeps E = 0 at {head_E0} of {head_n} momenta (mostly v = 0)")


def null_space(rows, ncols):
    """The null space dimension of an exact rational matrix, by Gaussian elimination."""
    M = [list(r) for r in rows]
    rank, col = 0, 0
    piv_cols = []
    for col in range(ncols):
        piv = next((i for i in range(rank, len(M)) if M[i][col] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][col]
        M[rank] = [x / pv for x in M[rank]]
        for i in range(len(M)):
            if i != rank and M[i][col] != 0:
                f = M[i][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[rank])]
        piv_cols.append(col)
        rank += 1
    free = [c for c in range(ncols) if c not in piv_cols]
    basis = []
    for fc in free:
        vec = [Fr(0)] * ncols
        vec[fc] = Fr(1)
        for i, pc in enumerate(piv_cols):
            vec[pc] = -M[i][fc]
        basis.append(vec)
    return ncols - rank, basis


def monomials(s):
    out = [Fr(1)] + [Fr(v) for v in s]
    for i in range(len(s)):
        for j in range(i, len(s)):
            out.append(Fr(s[i]) * Fr(s[j]))
    return out


def r3():
    rng = random.Random(33)
    w, X, c = 1009, 3, 17          # teeth (odd, so the mirror has no tie), stretch, the hold's shortfall D + SUM grips

    def int_step(s):
        a3, a12, b3, b12, r3_, r12 = s
        P = [w * (a3 - b3) + r3_ - mid(w), w * (a12 - b12) + r12 - mid(w)]
        P1 = [P[0] - X * c * a3, P[1] - X * c * a12]
        v3, n3 = carry(P1[0], w, mid(w))
        v12, n12 = carry(P1[1], w, mid(w))
        return (a3 + v3, a12 + v12, a3, a12, n3, n12)

    rows = []
    for _ in range(400):
        s = (rng.randint(-3000, 3000), rng.randint(-3000, 3000), 0, 0, rng.randrange(w), rng.randrange(w))
        s = (s[0], s[1], s[0] + rng.randint(-40, 40), s[1] + rng.randint(-40, 40), s[4], s[5])
        t = int_step(s)
        rows.append([x - y for x, y in zip(monomials(t), monomials(s))])
    dim_int, basis = null_space(rows, 28)
    only_const = dim_int == 1 and all(v == 0 for v in basis[0][1:])

    def exact_step(s):              # (a3, a12, P3, P12) rational, no carry
        a3, a12, P3, P12 = s
        P1 = (P3 - X * c * a3, P12 - X * c * a12)
        return (a3 + P1[0] / w, a12 + P1[1] / w, P1[0], P1[1])

    rows_e = []
    for _ in range(200):
        s = tuple(Fr(rng.randint(-3000, 3000), rng.randint(1, 9)) for _ in range(4))
        t = exact_step(s)
        rows_e.append([x - y for x, y in zip(monomials(t), monomials(s))])
    dim_ex, basis_e = null_space(rows_e, 15)
    # the charge Im(conj(a) P) = a3 P12 - a12 P3 in the monomial order of 4 variables
    quad = [(i, j) for i in range(4) for j in range(i, 4)]
    charge = [Fr(0)] * 15
    charge[5 + quad.index((0, 3))] = Fr(1)
    charge[5 + quad.index((1, 2))] = Fr(-1)
    # direct test: the charge is invariant under the exact step at every sample
    inv = all(sum(cc * m for cc, m in zip(charge, row)) == 0 for row in rows_e)
    report("R3 the integer step of one Node-clock keeps no quadratic form but the constants (the law's line 785)",
           only_const, f"null space dimension {dim_int} over the 28 monomials of degree <= 2 (constants alone: {only_const})")
    report("R3b control: the exact rational step's null space holds the charge Im(conj(a) P)", dim_ex >= 2 and inv,
           f"null space dimension {dim_ex} over the 15 monomials of (a3, a12, P3, P12); the charge invariant at every "
           f"sample: {inv}")


def rounded(numerator, teeth):     # rates.rounded: half up on the magnitude, the sign after (odd)
    s = 1 if numerator >= 0 else -1
    return s * ((2 * abs(numerator) + teeth) // (2 * teeth))


def r4():
    rng = random.Random(34)
    bad_round = bad_exact = n = 0
    for trial in range(5000):
        scale = rng.randint(10 ** 3, 10 ** 6)
        # a near-unit pair (c, s) over the scale, conjugate-symmetric between the ends as the head's offsets are
        c, s = rng.randint(-scale, scale), rng.randint(-scale, scale)
        ax = (rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6))
        ay = (rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6))

        def turned_round(cc, ss, z):
            return (rounded(cc * z[0] - ss * z[1], scale), rounded(ss * z[0] + cc * z[1], scale))

        def turned_exact(cc, ss, z):
            return (Fr(cc * z[0] - ss * z[1], scale), Fr(ss * z[0] + cc * z[1], scale))

        # one frame (f = 1): x reads y turned by (c, s), y reads x turned by (c, -s)
        jr = im_cb(ax, turned_round(c, s, ay)) + im_cb(ay, turned_round(c, -s, ax))
        je = im_cb(ax, turned_exact(c, s, ay)) + im_cb(ay, turned_exact(c, -s, ax))
        if MUT == 'even_round':
            je = jr
        n += 1
        bad_round += int(jr != 0)
        bad_exact += int(je != 0)
    report("R4 the turn's rounding: the rounded current not antisymmetric, the exact one antisymmetric",
           bad_exact == 0 and bad_round > 0,
           f"of {n} Meshes the rounded turn leaves {bad_round} not antisymmetric, the exact turn {bad_exact}")


if __name__ == '__main__':
    print(f"I3 the rounding; mutant: {MUT or 'none'}")
    for f in (r1, r2, r3, r4):
        f()
    fails = [n for n, ok in RES if not ok]
    print(f"{len(RES) - len(fails)} of {len(RES)} checks PASS" + (f"; FAIL: {fails}" if fails else ''))
