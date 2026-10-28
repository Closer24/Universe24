"""F1: the 24's invariants and the long waves (draft F; root II items 3 and 21; root V item 22).

Exact integers and Fractions only, no float. Run: python3 -I F1_kinds.py [MUTANT]
MUTANT is one of: none (default), sign_E (E's character with a wrong sign), hold (the band's
light coefficient lambda read as 1/4 where the claim names 1/3), gauge (the gauge condition
dropped from the T1 operator count). Each mutant must make at least one check FAIL.

What it checks:
 A. the 24 and the 48 as signed permutation matrices; the five kinds' characters; orthonormality;
 B. the 24-invariant polynomials of degree n in the wave vector k (n = 0..9), against the 48;
 C. for a train of each kind K, the number of 24-invariant long-wave operators
    M_ab(k) = C_ab,cd k_c k_d (symmetric in ab): dim Hom_O(1, Sym2(K) x Sym2(T1));
 D. for K = T1, the operators that kill a pure gauge wave, M(k) k = 0 for every k: one left,
    the Maxwell form |k|^2 delta - k k^T; the cubic one diag(k_a^2) is not SO(3)-covariant
    (checked against the rational rotation (3/5, 4/5) about z);
 E. the band cos w = 1 - lambda SUM_a (1 - cos k_a): the long-wave speed's first correction,
    v = sqrt(lambda) (1 - kappa(d) p^2 + ...), kappa(d) = (S4(d) - lambda) / 8, S4 = SUM d_a^4,
    from exact power series; at lambda = 1/3 it is 1/12 on an axis, 1/48 on a face diagonal and
    0 on a body diagonal; for a massive train cos w = r (1/3) SUM cos k_a, the k^2 coefficient
    of (2 sin(w / 2))^2 is r / 3.
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


# ---------------------------------------------------------------- A. the group and its kinds
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def signed_perms():
    out = []
    for p in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i in range(3):
                m[p[i]][i] = s[i]  # column i: e_i -> s_i e_{p(i)}
            out.append(tuple(tuple(r) for r in m))
    return out


G48 = signed_perms()
G24 = [g for g in G48 if det3(g) == 1]
check("A1 the 48 and the 24", len(G48) == 48 and len(G24) == 24, f"{len(G48)} and {len(G24)}")


def perm_of(g):
    return tuple(next(j for j in range(3) if g[j][i] != 0) for i in range(3))


def perm_sign(p):
    s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]:
                s = -s
    return s


def chi(kind, g):
    tr = g[0][0] + g[1][1] + g[2][2]
    p = perm_of(g)
    fixed = sum(1 for i in range(3) if p[i] == i)
    if kind == "A1":
        return 1
    if kind == "A2":
        return perm_sign(p)
    if kind == "E":
        return (fixed - 1) * (-1 if MUT == "sign_E" else 1)
    if kind == "T1":
        return tr
    if kind == "T2":
        return perm_sign(p) * tr
    raise ValueError(kind)


KINDS = ["A1", "A2", "E", "T1", "T2"]
gram = {(a, b): sum(chi(a, g) * chi(b, g) for g in G24) for a in KINDS for b in KINDS}
ok = all(gram[(a, b)] == (24 if a == b else 0) for a in KINDS for b in KINDS)
check("A2 the five kinds' characters orthonormal over the 24", ok,
      "sum of squares of dims " + str(sum(chi(k, G24[0]) ** 2 for k in KINDS)))
classes = {}
for g in G24:
    key = (g[0][0] + g[1][1] + g[2][2], perm_sign(perm_of(g)))
    classes[key] = classes.get(key, 0) + 1
check("A3 the classes 1 + 6 + 3 + 8 + 6", sorted(classes.values()) == [1, 3, 6, 6, 8], str(sorted(classes.values())))


# ---------------------------------------------------------------- B. invariant polynomials in k
def monomials(n):
    return [e for e in itertools.product(range(n + 1), repeat=3) if sum(e) == n]


def trace_on_sym(g, n):
    """Trace of g acting on degree-n polynomials, (g f)(k) = f(g^T k)."""
    p = perm_of(g)
    s = [g[p[i]][i] for i in range(3)]
    tot = 0
    for e in monomials(n):
        e2 = [0, 0, 0]
        for i in range(3):
            e2[p[i]] = e[i]
        if tuple(e2) == e:
            sign = 1
            for i in range(3):
                if s[i] == -1 and e[i] % 2 == 1:
                    sign = -sign
            tot += sign
    return tot


inv24 = [Fr(sum(trace_on_sym(g, n) for g in G24), 24) for n in range(10)]
inv48 = [Fr(sum(trace_on_sym(g, n) for g in G48), 48) for n in range(10)]
print("   invariants of degree n = 0..9 under the 24:", [int(x) for x in inv24])
print("   invariants of degree n = 0..9 under the 48:", [int(x) for x in inv48])
check("B1 degree 2: one invariant, |k|^2 (so every scalar train's long-wave form is isotropic)", inv24[2] == 1)
check("B2 degree 4: two invariants, |k|^4 and SUM k_a^4 (the first cube invariant)", inv24[4] == 2)
check("B3 degree 6: three; degree 8: four; degree 9: one under the 24 and none under the 48",
      inv24[6] == 3 and inv24[8] == 4 and inv24[9] == 1 and inv48[9] == 0)


def s4(k):
    return sum(x ** 4 for x in k)


def n2(k):
    return sum(x * x for x in k)


ratio_axis = Fr(s4((1, 0, 0)), n2((1, 0, 0)) ** 2)
ratio_face = Fr(s4((1, 1, 0)), n2((1, 1, 0)) ** 2)
check("B4 SUM k_a^4 is no multiple of |k|^4 (axis 1, face diagonal 1/2)",
      ratio_axis == 1 and ratio_face == Fr(1, 2), f"{ratio_axis} and {ratio_face}")


# ---------------------------------------------------------------- C. long-wave operators by kind
def chi_sym2(kind, g):
    return Fr(chi(kind, g) ** 2 + chi(kind, mul(g, g)), 2)


counts = {}
for K in KINDS:
    counts[K] = sum(chi_sym2(K, g) * chi_sym2("T1", g) for g in G24) / 24
print("   24-invariant long-wave operators by kind:", {k: int(v) for k, v in counts.items()})
check("C1 A1 and A2 trains: one constant each (isotropic by the 24 alone)",
      counts["A1"] == 1 and counts["A2"] == 1)
check("C2 E: two constants; T1 and T2: three each (a cubic crystal's elasticity, not isotropic by the 24)",
      counts["E"] == 2 and counts["T1"] == 3 and counts["T2"] == 3)

# ---------------------------------------------------------------- D. the T1 operators and the gauge
# basis of 4-index tensors C[a][b][c][d] symmetric in (a,b) and (c,d): average over the 24
idx = [(a, b) for a in range(3) for b in range(a, 3)]


def basis_tensor(ab, cd):
    C = {}
    for (a, b) in [ab, ab[::-1]]:
        for (c, d) in [cd, cd[::-1]]:
            C[(a, b, c, d)] = 1
    return C


def act(g, C):
    """(g C)_abcd = SUM g_aa' g_bb' g_cc' g_dd' C_a'b'c'd'."""
    out = {}
    for (a2, b2, c2, d2), v in C.items():
        for a in range(3):
            if g[a][a2] == 0:
                continue
            for b in range(3):
                if g[b][b2] == 0:
                    continue
                for c in range(3):
                    if g[c][c2] == 0:
                        continue
                    for d in range(3):
                        if g[d][d2] == 0:
                            continue
                        key = (a, b, c, d)
                        out[key] = out.get(key, 0) + g[a][a2] * g[b][b2] * g[c][c2] * g[d][d2] * v
    return {k: v for k, v in out.items() if v != 0}


def reynolds(C):
    tot = {}
    for g in G24:
        for k, v in act(g, C).items():
            tot[k] = tot.get(k, 0) + v
    return {k: v for k, v in tot.items() if v != 0}


KEYS = [(a, b, c, d) for a in range(3) for b in range(3) for c in range(3) for d in range(3)]


def vec(C):
    return [Fr(C.get(k, 0)) for k in KEYS]


def rank(rows):
    rows = [r[:] for r in rows]
    rk, col, ncol = 0, 0, len(rows[0]) if rows else 0
    while rk < len(rows) and col < ncol:
        piv = next((i for i in range(rk, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            col += 1
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][col] != 0:
                f = rows[i][col] / rows[rk][col]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[rk])]
        rk += 1
        col += 1
    return rk


invariants = [vec(reynolds(basis_tensor(ab, cd))) for ab in idx for cd in idx]
dim_inv = rank(invariants)
check("D1 the 24-invariant T1 operators span a space of dimension 3 (= C2's count)", dim_inv == 3, str(dim_inv))


# the three named operators: alpha |k|^2 delta_ab, beta k_a k_b, gamma k_a^2 delta_ab
def op_alpha():
    return {(a, a, c, c): 1 for a in range(3) for c in range(3)}


def op_beta():
    """k_a k_b, written symmetric in (c, d): C_abcd = (delta_ac delta_bd + delta_ad delta_bc) / 2."""
    C = {}
    for a in range(3):
        for b in range(3):
            C[(a, b, a, b)] = C.get((a, b, a, b), 0) + Fr(1, 2)
            C[(a, b, b, a)] = C.get((a, b, b, a), 0) + Fr(1, 2)
    return C


def op_gamma():
    return {(a, a, a, a): 1 for a in range(3)}


named = [vec(op_alpha()), vec(op_beta()), vec(op_gamma())]
check("D2 alpha |k|^2 delta, beta k k^T and gamma diag(k_a^2) are invariant and span them",
      rank(invariants + named) == 3 and rank(named) == 3)


def M_of(C, k):
    return [[sum(Fr(C.get((a, b, c, d), 0)) * k[c] * k[d] for c in range(3) for d in range(3))
             for b in range(3)] for a in range(3)]


# gauge condition: M(k) k = 0 for every k  <=>  for the cubic polynomial in k, all coefficients 0
def gauge_rows():
    rows = []
    for a in range(3):
        for e in monomials(3):
            row = []
            for C in (op_alpha(), op_beta(), op_gamma()):
                # coefficient of k^e in SUM_bcd C_abcd k_b k_c k_d
                coef = 0
                for b in range(3):
                    for c in range(3):
                        for d in range(3):
                            ex = [0, 0, 0]
                            ex[b] += 1
                            ex[c] += 1
                            ex[d] += 1
                            if tuple(ex) == e:
                                coef += C.get((a, b, c, d), 0)
                row.append(Fr(coef))
            rows.append(row)
    return rows


gr = gauge_rows()
if MUT == "gauge":
    gr = []
null = 3 - (rank(gr) if gr else 0)
check("D3 the gauge condition M(k) k = 0 leaves one operator", null == 1, f"dimension {null}")
# the survivor: alpha = 1, beta = -1, gamma = 0
surv = {}
for k_, v in op_alpha().items():
    surv[k_] = surv.get(k_, 0) + v
for k_, v in op_beta().items():
    surv[k_] = surv.get(k_, 0) - v
ok = True
for k in [(1, 2, 3), (2, -1, 5), (0, 1, 7)]:
    M = M_of(surv, k)
    ok = ok and all(sum(M[a][b] * k[b] for b in range(3)) == 0 for a in range(3))
check("D4 the survivor is |k|^2 delta - k k^T (Maxwell's), killing every gradient wave", ok)
Rz = ((Fr(3, 5), Fr(-4, 5), Fr(0)), (Fr(4, 5), Fr(3, 5), Fr(0)), (Fr(0), Fr(0), Fr(1)))


def rot(R, k):
    return [sum(R[i][j] * k[j] for j in range(3)) for i in range(3)]


def covariant(C, R, k):
    Mk = M_of(C, rot(R, k))
    M = M_of(C, k)
    RMRt = [[sum(R[a][i] * M[i][j] * R[b][j] for i in range(3) for j in range(3)) for b in range(3)] for a in range(3)]
    return Mk == RMRt


k0 = (Fr(1), Fr(2), Fr(3))
check("D5 under the rational rotation (3/5, 4/5) about z: alpha and beta covariant, gamma not",
      covariant(op_alpha(), Rz, k0) and covariant(op_beta(), Rz, k0) and not covariant(op_gamma(), Rz, k0))

# ---------------------------------------------------------------- E. the band's long waves
ORDER = 4  # series in t = p^2 to t^ORDER
FACT = [1]
for i in range(1, 2 * ORDER + 4):
    FACT.append(FACT[-1] * i)


def ser_mul(a, b):
    out = [Fr(0)] * (ORDER + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j <= ORDER:
                out[i + j] += x * y
    return out


def one_minus_cos(q):
    """1 - cos(p d) as a series in t = p^2, with q = d^2 rational."""
    return [Fr(0)] + [Fr((-1) ** (m + 1)) * q ** m / FACT[2 * m] for m in range(1, ORDER + 1)]


def omega_sq(u):
    """s = w^2 as a series in t from 1 - cos(sqrt s) = u(t), by fixed-point iteration."""
    s = [Fr(0)] * (ORDER + 1)
    for _ in range(ORDER + 2):
        # 1 - cos sqrt(s) = s/2 - s^2/24 + s^3/720 - ...  =>  s = 2u + 2 SUM_{m>=2} (-1)^m s^m / (2m)!
        acc = [2 * x for x in u]
        power = s[:]
        for m in range(2, ORDER + 2):
            power = ser_mul(power, s)
            for i in range(ORDER + 1):
                acc[i] += 2 * Fr((-1) ** m) * power[i] / FACT[2 * m]
        s = acc
    return s


def band_coeffs(n, lam):
    nn = sum(x * x for x in n)
    q = [Fr(x * x, nn) for x in n]
    u = [Fr(0)] * (ORDER + 1)
    for qa in q:
        u = [x + lam * y for x, y in zip(u, one_minus_cos(qa))]
    s = omega_sq(u)
    A, B = s[1], s[2]
    kappa = -Fr(3) * B / (2 * A)  # v = sqrt(A) (1 - kappa t + ...)
    S4 = sum(x * x for x in q)
    return A, kappa, S4


lam = Fr(1, 4) if MUT == "hold" else Fr(1, 3)
rows = {}
for name, n in [("axis", (1, 0, 0)), ("face", (1, 1, 0)), ("body", (1, 1, 1)), ("(1,2,3)", (1, 2, 3))]:
    A, kappa, S4 = band_coeffs(n, Fr(1, 3))
    rows[name] = (A, kappa, S4)
    print(f"   lambda 1/3, {name}: w^2/p^2 -> {A}; first slowing kappa = {kappa}; (S4 - 1/3)/8 = {(S4 - Fr(1, 3)) / 8}")
ok = all(A == lam and kappa == (S4 - lam) / 8 for (A, kappa, S4) in rows.values())
check("E1 at the Courant edge every direction has c^2 = 1/3 and kappa = (S4 - 1/3)/8", ok)
check("E2 kappa: axis 1/12, face diagonal 1/48, body diagonal 0",
      rows["axis"][1] == Fr(1, 12) and rows["face"][1] == Fr(1, 48) and rows["body"][1] == 0)
A, kappa, S4 = band_coeffs((1, 1, 1), Fr(1, 6))
check("E3 below the edge (lambda 1/6, hold 1) the body diagonal slows too: kappa = 1/48",
      kappa == Fr(1, 48) and A == Fr(1, 6), str(kappa))
# a massive train at the vacuum: cos w = r (1/3) SUM cos k_a ; (2 sin(w/2))^2 = 2 - 2 cos w
for r in (Fr(1), Fr(4, 5), Fr(3, 5), Fr(1, 2)):
    two_minus = [Fr(2) - 2 * r] + [Fr(0)] * ORDER
    for qa in (Fr(1), Fr(0), Fr(0)):
        two_minus = [x + 2 * r / 3 * y for x, y in zip(two_minus, one_minus_cos(qa))]
    print(f"   massive r = {r}: (2 sin(w/2))^2 = {two_minus[0]} + {two_minus[1]} p^2 + ...")
    if two_minus[1] != r / 3:
        check("E4 k^2 coefficient r/3", False, str(r))
        break
else:
    check("E4 in the variable 2 sin(w/2) each train's long-wave speed^2 is r/3 = pinion/(3 rim)", True)

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
