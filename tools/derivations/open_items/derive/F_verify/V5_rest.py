"""V5: the rest (verifier of draft F, 1.1, 1.2 and 2.2). Integers, Gaussian integers and Fractions only.

Run: python3 -I V5_rest.py [MUTANT]   MUTANT: none, grip (both trains given the law of the grips' weight r/3)
 A. one limiting speed for two trains on one tick stencil of finite reach: cos w = r - lam SUM_a (1 - cos k_a) has
    c^2 = d(w^2)/d(k^2) at k = 0 equal to lam w0 / sin w0. Trains L (cos w0 = 4/5, lam 1/10) and K (cos w0 = 7/25,
    lam 2/25): (4 + 3i)^2 = 7 + 24i, so w0_K = 2 w0_L, and c_K^2 / c_L^2 = (lam_K / lam_L)(w0_K / w0_L)(sin w0_L /
    sin w0_K) = 1 exactly; both holds 2 (r - 3 lam) > 0 and both bands stable (r - 6 lam >= -1);
 B. by characters of the 24 (and of 2O through F4's rule chi(h) from tr(g)): long-wave constants at O(k^2) for a
    complex field of each kind, counted as A1 in Herm(K) x Sym2(T1); the O(k) terms, A1 in i Lambda2(K) x T1 (the
    helicity term), and for the spinor kinds A1 in Herm(K) x T1;
 C. F5 D1's token: of its 8 ticks, those with a density <= 0 somewhere, a density < 0 somewhere, and an outflow
    above the density somewhere.
"""

import itertools
import sys
from fractions import Fraction as Fr

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- A
def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


rL, sL, rK, sK = Fr(4, 5), Fr(3, 5), Fr(7, 25), Fr(24, 25)
lamL, lamK = (rL / 3, rK / 3) if MUT == "grip" else (Fr(1, 10), Fr(2, 25))
double = gm((4, 3), (4, 3)) == (7, 24)
ratio = (lamK / lamL) * 2 * (sL / sK)
check("A1 (4 + 3i)^2 = 7 + 24i: w0_K = 2 w0_L, both in (0, pi/2)", double and rK > 0 and rL > 0)
check("A2 c_K^2 / c_L^2 = 1 exactly: one limiting speed for two trains of different rest beats", ratio == 1, f"ratio {ratio}")
check("A3 both holds above 0 and both bands stable", all(2 * (r - 3 * lam) > 0 and r - 6 * lam >= -1 for r, lam in ((rL, lamL), (rK, lamK))),
      f"holds {2 * (rL - 3 * lamL)} and {2 * (rK - 3 * lamK)}")

# ---------------------------------------------------------------- B
G24 = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        m = [[0] * 3 for _ in range(3)]
        for i in range(3):
            m[p[i]][i] = sg[i]
        m = tuple(tuple(r) for r in m)
        d = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
             + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        if d == 1:
            G24.append(m)


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def chi(kind, g):
    tr = g[0][0] + g[1][1] + g[2][2]
    perm = tuple(next(j for j in range(3) if g[j][i] != 0) for i in range(3))
    sgn = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if perm[i] > perm[j]:
                sgn = -sgn
    fixed = sum(1 for i in range(3) if perm[i] == i)
    return {"A1": 1, "A2": sgn, "E": fixed - 1, "T1": tr, "T2": sgn * tr}[kind]


def sym2(c, c2):
    return Fr(c * c + c2, 2)


def alt2(c, c2):
    return Fr(c * c - c2, 2)


def herm_O(kind, g):  # Herm(K) for complex K of a real kind: K x K as a real space, character chi^2
    return chi(kind, g) ** 2


# spinor kinds: |chi(h)|^2 is a function of g = R(h): 4 cos^2(phi/2) = 1 + tr(g) for E1/2 and E5/2; times chi_E(g)^2 for G3/2
def herm_spin(kind, g):
    base = 1 + (g[0][0] + g[1][1] + g[2][2])
    return base * (chi("E", g) ** 2 if kind == "G3/2" else 1)


def count(f):
    return Fr(sum(f(g) for g in G24), 24)


S2T1 = lambda g: sym2(chi("T1", g), chi("T1", mul(g, g)))  # noqa: E731
k2 = {K: count(lambda g, K=K: herm_O(K, g) * S2T1(g)) for K in ("A1", "A2", "E", "T1", "T2")}
k2.update({K: count(lambda g, K=K: herm_spin(K, g) * S2T1(g)) for K in ("E1/2", "E5/2", "G3/2")})
k1_real = {K: count(lambda g, K=K: alt2(chi(K, g), chi(K, mul(g, g))) * chi("T1", g)) for K in ("A1", "A2", "E", "T1", "T2")}
k1_spin = {K: count(lambda g, K=K: herm_spin(K, g) * chi("T1", g)) for K in ("E1/2", "E5/2", "G3/2")}
print("   O(k^2) constants (A1 in Herm(K) x Sym2(T1)):", {k: int(v) for k, v in k2.items()})
print("   O(k) terms of a real field (A1 in Lambda2(K) x T1):", {k: int(v) for k, v in k1_real.items()})
print("   O(k) terms of a spinor field (A1 in Herm(K) x T1):", {k: int(v) for k, v in k1_spin.items()})
check("B1 complex fields of O's kinds: 1, 1, 2, 3, 3 constants (the draft's counts); E1/2 and E5/2: 1; G3/2: 4",
      [k2[k] for k in ("A1", "A2", "E", "T1", "T2", "E1/2", "E5/2", "G3/2")] == [1, 1, 2, 3, 3, 1, 1, 4])
check("B2 the 24 allow one O(k) helicity term for T1 and for T2 trains, none for A1, A2, E",
      [k1_real[k] for k in ("A1", "A2", "E", "T1", "T2")] == [0, 0, 0, 1, 1])
check("B3 each spinor kind allows O(k) terms: E1/2 and E5/2 one (sigma . k), G3/2 two",
      [k1_spin[k] for k in ("E1/2", "E5/2", "G3/2")] == [1, 1, 2])

# ---------------------------------------------------------------- C (F5 D1's two waves, its own code's sizes)
L = 4
SITES = list(itertools.product(range(L), repeat=3))
SP = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def nb(x, d):
    return ((x[0] + d[0]) % L, (x[1] + d[1]) % L, (x[2] + d[2]) % L)


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def im_cx(a, b):
    return a[0] * b[1] - a[1] * b[0]


r = Fr(3, 5)
mu = r / 3
modes = [(lambda x: (Fr(1), Fr(0)), (Fr(3, 5), Fr(4, 5))),
         (lambda x: [(Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(-1), Fr(0)), (Fr(0), Fr(-1))][(x[0] + x[1] + x[2]) % 4], (Fr(0), Fr(1)))]
A1, A2 = (Fr(3), Fr(-2)), (Fr(1), Fr(4))


def field(t):
    f = {x: (Fr(0), Fr(0)) for x in SITES}
    for (v, (c, s)), A in zip(modes, (A1, A2)):
        U = (c, -s) if t >= 0 else (c, s)
        Ut = (Fr(1), Fr(0))
        for _ in range(abs(t)):
            Ut = cmul(Ut, U)
        for x in SITES:
            w = cmul(cmul(A, Ut), v(x))
            f[x] = (f[x][0] + w[0], f[x][1] + w[1])
    return f


neg_or_zero, neg, over = [], [], []
for t in range(0, 8):
    zn, zb = field(t), field(t - 1)
    rho = {x: im_cx(zn[x], zb[x]) for x in SITES}
    flux = {(x, d): mu * im_cx(zn[x], zn[nb(x, d)]) for x in SITES for d in SP}
    outs = {x: sum(max(Fr(0), flux[(x, d)]) for d in SP) for x in SITES}
    if any(v <= 0 for v in rho.values()):
        neg_or_zero.append(t)
    if any(v < 0 for v in rho.values()):
        neg.append(t)
    if any(rho[x] - outs[x] < 0 for x in SITES):
        over.append(t)
print(f"   C: ticks with a density <= 0: {neg_or_zero}; with a density < 0: {neg}; with an outflow above the density: {over}")
check("C1 F5 D1's six failing ticks: counted by cause", len(set(neg_or_zero) | set(over)) == 6, f"{sorted(set(neg_or_zero) | set(over))}")
print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
