"""sr2 (2026-10-25): the spinor row's algebra by number, exact (integers and Fractions; no float).

The row of shape 8 read as four planes: a spinor (psi_1, psi_2) over Q(zeta), zeta^4 = -1, zeta^2 = i, with
psi_k = Z_k0 + zeta Z_k1 and Z_k0, Z_k1 Gaussian (re, im): the eight lines are the re and im of the four Gaussian
components (Dirac's count, 4 complex = 8 real); the two Galois-conjugate spinors (zeta -> zeta and zeta -> -zeta,
sqrt 2 -> -sqrt 2) are the two irrational eigen-halves of the same eight lines, not lines of their own.

Checked here:
 (1) multiplication by zeta is a signed permutation of the eight lines; a plane rotation of the four planes alike
     (any rational (c, s), here (3, 4) / 5) commutes with zeta, i and every 8 x 8 matrix below: the Link's pair (the
     charge's turn) commutes with the spin matrices;
 (2) the three Pauli matrices sigma_a and J (multiplication by i) as real 8 x 8 integer matrices in the plane basis:
     sigma symmetric and orthogonal, J antisymmetric, J sigma_a = sigma_a J;
 (3) the 48 elements of the double cover 2O (the closure of the quarter turns' lifts u_a = (1 + i sigma_a) / sqrt 2),
     as 8 x 8 rational matrices in the plane basis: 16 integer and monomial (signed permutations: the binary dihedral
     group of one axis), 32 with the denominator 2; all 48 orthogonal (the plane basis is orthonormal for the trace
     form); -I among them (the 2 pi turn), u_z^4 = -I; the traces integers;
 (4) the bilinears W = psi_now^T J psi_before (the charge) and s_a = psi_now^T J sigma_a psi_before (the spin) under
     all 48: W kept 48 of 48, s carried as a vector by the rotation's signed permutation 48 of 48; under the Pin lift
     of the reflections (Gamma_a times the rotations) W kept (a scalar) and s axial (det g times the signed
     permutation); under -I every bilinear kept;
 (5) the Port's turn: for a hop matrix T_(+a) with T_(-a) = T_(+a)^-1 the rest operator SUM_a (T_a + T_a^-1) on the
     eight lines: T = 1 gives 6 (the pair's gap kept, 2 cos omega_0 = 2 num / den); T = i sigma_a (the half turn's lift)
     gives 0 (the gap killed: cos omega_rest = 0 for every pair); T = u_a (the quarter turn's lift) gives the two
     eigenvalues 3 sqrt 2 and -3 sqrt 2 on the two Galois halves (the gap scaled by sqrt 2 on one half, above 1 for
     every pair with num / den > 1 / sqrt 2: no real rotation, growth; reversed on the other): so the Port's turn of
     the spinor row is the identity of the double cover and the spin enters at the Node;
 (6) the Node term Phi . sigma: symmetric (D M symmetric with D = I in the plane basis), so Rule3's conserved form
     holds with its bilinear term added; the stable lattice L (sp1's) has a Gram matrix 2 D integer and not diagonal:
     in L's basis the plain sum over lines is not the 48-invariant form (the alternative reading's cost, named);
 (7) the 2 pi turn: -I on the lines, +1 on every bilinear and on the share.
Usage: python sr2_algebra.py  (prints JSON; integers and fraction strings)
"""
from __future__ import annotations
from fractions import Fraction as Fr
import itertools, json, sys

# ---- Q(zeta): elements as 4 Fractions (a0 + a1 z + a2 z^2 + a3 z^3), z^4 = -1
def zmul(a, b):
    c = [Fr(0)] * 8
    for i in range(4):
        for j in range(4): c[i + j] += a[i] * b[j]
    for k in range(7, 3, -1): c[k - 4] -= c[k]; c[k] = Fr(0)
    return tuple(c[:4])
def zadd(a, b): return tuple(x + y for x, y in zip(a, b))
def zneg(a): return tuple(-x for x in a)
def zconst(q): return (Fr(q), Fr(0), Fr(0), Fr(0))
ZERO, ONE = zconst(0), zconst(1); ZETA = (Fr(0), Fr(1), Fr(0), Fr(0)); I_ = (Fr(0), Fr(0), Fr(1), Fr(0))
INV_SQRT2 = (Fr(0), Fr(1, 2), Fr(0), Fr(-1, 2))  # (z - z^3) / 2
SQRT2 = (Fr(0), Fr(1), Fr(0), Fr(-1))
def mmul(A, B):
    return (zadd(zmul(A[0], B[0]), zmul(A[1], B[2])), zadd(zmul(A[0], B[1]), zmul(A[1], B[3])),
            zadd(zmul(A[2], B[0]), zmul(A[3], B[2])), zadd(zmul(A[2], B[1]), zmul(A[3], B[3])))
IDENT = (ONE, ZERO, ZERO, ONE)
SX = (ZERO, ONE, ONE, ZERO); SY = (ZERO, zneg(I_), I_, ZERO); SZ = (ONE, ZERO, ZERO, zneg(ONE))
def lift(S): return tuple(zmul(INV_SQRT2, zadd(e, zmul(I_, s))) for e, s in zip(IDENT, S))
UX, UY, UZ = lift(SX), lift(SY), lift(SZ)
def closure(gens):
    seen = {IDENT: ''}; frontier = [IDENT]
    while frontier:
        nxt = []
        for A in frontier:
            for name, G in gens:
                B = mmul(G, A)
                if B not in seen: seen[B] = name + seen[A]; nxt.append(B)
        frontier = nxt
    return seen
GROUP = closure([('x', UX), ('y', UY), ('z', UZ)])

# ---- the plane basis of Q(zeta)^2 as 8 rational lines: psi_k = Z_k0 + zeta Z_k1, lines (re Z_10, im Z_10, re Z_11, im Z_11, re Z_20, ...)
# an element a0 + a1 z + a2 z^2 + a3 z^3 = (a0 + i a2) + z (a1 + i a3): Z_0 = (a0, a2), Z_1 = (a1, a3)
def lines_of(A8):  # a 2-vector over Q(zeta) -> 8 lines
    out = []
    for comp in A8: out += [comp[0], comp[2], comp[1], comp[3]]
    return out
def vec_of(lines):  # 8 lines -> a 2-vector over Q(zeta)
    return tuple((lines[4 * k], lines[4 * k + 2], lines[4 * k + 1], lines[4 * k + 3]) for k in range(2))
def apply(A, v): return (zadd(zmul(A[0], v[0]), zmul(A[1], v[1])), zadd(zmul(A[2], v[0]), zmul(A[3], v[1])))
def real8(A):
    """The 8 x 8 rational matrix of a 2 x 2 matrix over Q(zeta) in the plane basis (columns = images of the unit lines)."""
    cols = []
    for c in range(8):
        e = [Fr(0)] * 8; e[c] = Fr(1)
        cols.append(lines_of(apply(A, vec_of(e))))
    return [[cols[c][r] for c in range(8)] for r in range(8)]
def scalar8(s):  # multiplication by an element s of Q(zeta) on the 8 lines
    return real8((s, ZERO, ZERO, s))
def mm(A, B): return [[sum(A[r][k] * B[k][c] for k in range(8)) for c in range(8)] for r in range(8)]
def mT(A): return [[A[c][r] for c in range(8)] for r in range(8)]
def mv(A, v): return [sum(A[r][c] * v[c] for c in range(8)) for r in range(8)]
def madd(A, B): return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]
def msc(s, A): return [[s * a for a in ra] for ra in A]
ID8 = [[Fr(int(r == c)) for c in range(8)] for r in range(8)]
NEG8 = msc(-1, ID8)
def is_int(M): return all(x.denominator == 1 for row in M for x in row)
def denominators(M): return sorted({x.denominator for row in M for x in row})
def monomial(M): return all(sum(1 for x in row if x != 0) == 1 for row in M) and all(sum(1 for r in range(8) if M[r][c] != 0) == 1 for c in range(8)) and all(abs(x) in (0, 1) for row in M for x in row)
def ints(M): return [[int(x) for x in row] for row in M]

out = {}
# (1) zeta a signed permutation; the plane rotation commutes
Zm = scalar8(ZETA); Jm = scalar8(I_)
out['(1) multiplication by zeta on the 8 lines is a signed permutation'] = monomial(Zm)
out['(1) zeta as a signed permutation (row: the line it reads, with sign)'] = [[(c, int(Zm[r][c])) for c in range(8) if Zm[r][c] != 0][0] for r in range(8)]
def plane_rotation(c, s):  # the same rotation (c, s) on each of the four planes (re, im)
    M = [[Fr(0)] * 8 for _ in range(8)]
    for k in range(4):
        M[2 * k][2 * k], M[2 * k][2 * k + 1], M[2 * k + 1][2 * k], M[2 * k + 1][2 * k + 1] = c, -s, s, c
    return M
Rot = plane_rotation(Fr(3, 5), Fr(4, 5))
out['(1) the plane rotation (3, 4) / 5 on the four planes alike commutes with zeta and with i'] = mm(Rot, Zm) == mm(Zm, Rot) and mm(Rot, Jm) == mm(Jm, Rot)
# (2) the Pauli matrices and J on the 8 lines
sig = {'x': real8(SX), 'y': real8(SY), 'z': real8(SZ)}
out['(2) sigma_a integer on the 8 lines'] = {a: is_int(M) for a, M in sig.items()}
out['(2) sigma_a symmetric'] = {a: mT(M) == M for a, M in sig.items()}
out['(2) sigma_a orthogonal (sigma^T sigma = I)'] = {a: mm(mT(M), M) == ID8 for a, M in sig.items()}
out['(2) J (multiplication by i) antisymmetric, J^2 = -I, J sigma_a = sigma_a J'] = [mT(Jm) == msc(-1, Jm), mm(Jm, Jm) == NEG8, all(mm(Jm, M) == mm(M, Jm) for M in sig.values())]
out['(2) the plane rotation commutes with every sigma_a'] = all(mm(Rot, M) == mm(M, Rot) for M in sig.values())
out['(2) sigma_x rows (line read, sign)'] = [[(c, int(sig['x'][r][c])) for c in range(8) if sig['x'][r][c] != 0] for r in range(8)]
out['(2) sigma_y rows (line read, sign)'] = [[(c, int(sig['y'][r][c])) for c in range(8) if sig['y'][r][c] != 0] for r in range(8)]
out['(2) sigma_z diagonal'] = [int(sig['z'][r][r]) for r in range(8)]
# (3) the 48 in the plane basis
elems = list(GROUP)
mats = {A: real8(A) for A in elems}
out['(3) group order'] = len(elems)
out['(3) elements integer in the plane basis'] = sum(1 for M in mats.values() if is_int(M))
out['(3) elements monomial (signed permutations of the 8 lines)'] = sum(1 for M in mats.values() if monomial(M))
out['(3) denominators over the 48 (denominator: count of elements whose largest denominator is it)'] = {str(d): sum(1 for M in mats.values() if max(denominators(M)) == d) for d in (1, 2)}
out['(3) all 48 orthogonal in the plane basis (M^T M = I: the trace form)'] = all(mm(mT(M), M) == ID8 for M in mats.values())
out['(3) -I among them'] = NEG8 in mats.values()
uz4 = mm(mm(mats[UZ], mats[UZ]), mm(mats[UZ], mats[UZ])); out['(3) u_z^4 = -I (the 2 pi turn)'] = uz4 == NEG8
out['(3) traces of the 48 (all integers)'] = sorted({str(sum(M[r][r] for r in range(8))) for M in mats.values()})
# which rotations are the monomial lifts: the fixed axis
def rot_of(A):
    """The rotation of a lift as the signed permutation of the Pauli triple: sigma_a -> s sigma_b."""
    perm = {}
    Minv = mT(mats[A])
    for a, G in sig.items():
        conj = mm(mm(mats[A], G), Minv)
        for b, Gb in sig.items():
            if conj == Gb: perm[a] = (b, 1)
            elif conj == msc(-1, Gb): perm[a] = (b, -1)
    return perm
rots = {A: rot_of(A) for A in elems}
out['(3) every element carries the Pauli triple as a signed permutation'] = all(len(p) == 3 for p in rots.values())
out['(3) distinct rotations (24)'] = len({json.dumps(p, sort_keys=True) for p in rots.values()})
def axis_fixed(p):
    fixed = [a for a in 'xyz' if p[a] == (a, 1)]
    return fixed
out['(3) the monomial lifts: the rotations they lift, by the axes kept'] = sorted(json.dumps({'word': GROUP[A], 'fixed': axis_fixed(rots[A]), 'perm': rots[A]}) for A in elems if monomial(mats[A]))
# (4) the bilinears under the 48 and the Pin lift
import random
random.seed(7)
def bil(psi_n, psi_b):
    Jn = mv(Jm, psi_b)
    W = sum(a * b for a, b in zip(psi_n, Jn))
    s = [sum(a * b for a, b in zip(psi_n, mv(mm(Jm, sig[c]), psi_b))) for c in 'xyz']
    return W, s
def dens(psi_n, psi_b):
    return [sum(a * b for a, b in zip(psi_n, mv(sig[c], psi_b))) for c in 'xyz']
tests = [([Fr(random.randint(-9, 9)) for _ in range(8)], [Fr(random.randint(-9, 9)) for _ in range(8)]) for _ in range(6)]
W_kept = s_vector = 0; s_fail = 0
for A in elems:
    M = mats[A]; p = rots[A]
    for pn, pb in tests:
        W0, s0 = bil(pn, pb); W1, s1 = bil(mv(M, pn), mv(M, pb))
        if W1 == W0: W_kept += 1
        # s'(image) carried as the vector: s1_b = sign * s0_a where sigma_a -> sign sigma_b
        expected = [None] * 3
        for a_i, a in enumerate('xyz'):
            b, sgn = p[a]; expected['xyz'.index(b)] = sgn * s0[a_i]
        if s1 == expected: s_vector += 1
        else: s_fail += 1
out['(4) W kept under the 48 (elements x tests)'] = [W_kept, 48 * len(tests)]
out['(4) s carried as the rotation\'s signed permutation (a vector), elements x tests'] = [s_vector, 48 * len(tests), 'failures', s_fail]
# the Pin lift of the reflections: the reflection r_a (flipping the axis a) lifted to Gamma_a times a rotation's lift
refl_W = refl_axial = refl_fail = 0
for a in 'xyz':
    G = sig[a]
    for A in elems:
        M = mm(G, mats[A]); p = rots[A]
        # the reflection's signed permutation: the rotation's, then flip the a component
        pr = {x: (p[x][0], p[x][1] * (-1 if p[x][0] == a else 1)) for x in 'xyz'}
        det = -1
        for pn, pb in tests:
            W0, s0 = bil(pn, pb); W1, s1 = bil(mv(M, pn), mv(M, pb))
            if W1 == W0: refl_W += 1
            expected = [None] * 3
            for a_i, x in enumerate('xyz'):
                b, sgn = pr[x]; expected['xyz'.index(b)] = det * sgn * s0[a_i]
            if s1 == expected: refl_axial += 1
            else: refl_fail += 1
out['(4) under the Pin lift of the reflections (Gamma_a times the 48): W kept (a scalar), s axial (det times the signed permutation), failures'] = [refl_W, refl_axial, refl_fail, 'of', 3 * 48 * len(tests)]
pn, pb = tests[0]
out['(4) the 2 pi turn -I: the lines negated, W and s kept, the share kept'] = [bil(mv(NEG8, pn), mv(NEG8, pb)) == bil(pn, pb), sum(x * x for x in mv(NEG8, pn)) == sum(x * x for x in pn)]
# (5) the Port's turn: the rest operator SUM_a (T_a + T_a^-1) for T = 1, i sigma_a, u_a
def inv(A):  # the inverse of a unitary 2 x 2 over Q(zeta): the conjugate transpose
    def conj(e): return (e[0], -e[3], -e[2], -e[1])  # z -> z^-1 = -z^3: a0 + a1 z^-1 + a2 z^-2 + a3 z^-3 = a0 - a3 z - a2 z^2 - a1 z^3
    return (conj(A[0]), conj(A[2]), conj(A[1]), conj(A[3]))
def rest_operator(Ts):
    tot = [[Fr(0)] * 8 for _ in range(8)]
    for T in Ts: tot = madd(tot, madd(real8(T), real8(inv(T))))
    return tot
isig = {a: tuple(zmul(I_, s) for s in S) for a, S in (('x', SX), ('y', SY), ('z', SZ))}
for name, Ts in (('T = 1 (the identity of the double cover)', [IDENT] * 3), ('T = i sigma_a (the half turn\'s lift)', list(isig.values())), ('T = u_a (the quarter turn\'s lift)', [UX, UY, UZ])):
    Op = rest_operator(Ts)
    # eigenvalues: Op acts as a scalar on each Galois half; read them as Op applied to the embeddings: compute Op^2 and Op on e
    e0 = [Fr(1)] + [Fr(0)] * 7
    v1 = mv(Op, e0); v2 = mv(Op, v1)
    # if Op = lambda I: v1 = lambda e0; if Op has eigenvalues +-c on the two halves with Op^2 = c^2 I: v2 = c^2 e0
    scalar = all(v1[k] == 0 for k in range(1, 8))
    out['(5) ' + name + ': the rest operator SUM_a (T_a + T_a^-1)'] = {'a scalar on the 8 lines': scalar, 'that scalar': str(v1[0]) if scalar else None, 'Op^2 e0 = c^2 e0 with c^2': str(v2[0]) if all(v2[k] == 0 for k in range(1, 8)) else None, 'integer matrix': is_int(Op)}
# the rest rotation with the middle universe's heavy pair at the vacuum: S = 0, R / w = num / (3 den): 2 cos omega = (R / w) x eigenvalue
num, den = 506298091, 1655909141
out['(5) at the vacuum S = 12 den Gamma^2 - 12 (den - num) Gamma^2 - 6 R = 0 for every pair; R / w = num / (3 den); so 2 cos omega_rest = (num / (3 den)) x the eigenvalue'] = {
    'T = 1: cos omega_rest = num / den': str(Fr(num, den)), 'T = i sigma: cos omega_rest = 0 (a quarter turn per interval, the pair\'s gap lost)': '0',
    'T = u_a: cos omega_rest = +- (num / den) sqrt 2 / 2 x 2 ... = +- sqrt 2 num / den on the two halves; squared': str(2 * Fr(num, den) ** 2), 'above 1 (no real rotation, growth) when 2 num^2 > den^2': 2 * num * num > den * den}
# (6) D M symmetric: the Node term Phi . sigma symmetric in the plane basis; the Gram matrix of sp1's lattice L
Phi = [Fr(3), Fr(-5), Fr(7)]
PhiSigma = madd(madd(msc(Phi[0], sig['x']), msc(Phi[1], sig['y'])), msc(Phi[2], sig['z']))
out['(6) Phi . sigma symmetric (D = I in the plane basis): the conserved form holds with its term'] = mT(PhiSigma) == PhiSigma
out['(6) Phi . sigma squared = |Phi|^2 I (the two eigen-senses +- |Phi|)'] = mm(PhiSigma, PhiSigma) == msc(Phi[0] ** 2 + Phi[1] ** 2 + Phi[2] ** 2, ID8)
# the lattice L = Z[zeta] e_1 + Z[zeta] f_2, f_2 = u_x e_1: its Gram matrix in the plane basis of (e_1, f_2) blocks
f2 = apply(UX, (ONE, ZERO))
basisL = []
for base in ((ONE, ZERO), f2):
    for k in (ONE, I_, ZETA, zmul(ZETA, I_)):  # the plane order re, im per Gaussian coordinate: 1, i, zeta, zeta i
        basisL.append(lines_of(apply((k, ZERO, ZERO, k), base)))
gram = [[sum(a * b for a, b in zip(u, v)) for v in basisL] for u in basisL]
out['(6) L (the orbit lattice, sp1) in the basis (e_1, i e_1, zeta e_1, zeta i e_1, f_2, ...): 2 x Gram integer, Gram not diagonal'] = [is_int(msc(2, gram)), gram != ID8, ints(msc(2, gram))]
# all 48 integer in L's basis (the change of basis)
def inverse(M):
    n = 8; A = [row[:] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
        piv = A[c][c]; A[c] = [x / piv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]
B = [[basisL[c][r] for c in range(8)] for r in range(8)]; Binv = inverse(B)
inL = {A: mm(mm(Binv, M), B) for A, M in mats.items()}
out['(6) all 48 integer in L\'s basis'] = all(is_int(M) for M in inL.values())
out['(6) monomial in L\'s basis'] = sum(1 for M in inL.values() if monomial(M))
out['(6) largest entry over the 48 in L\'s basis'] = max(abs(int(x)) for M in inL.values() for row in M for x in row)
# the plain sum over lines is not invariant in L's basis: a lay and its image under u_x
psi = [Fr(1), Fr(0), Fr(0), Fr(0), Fr(1), Fr(0), Fr(0), Fr(0)]  # e_1 + f_2 in L's basis
img = mv(inL[UX], psi)
out['(6) in L\'s basis the plain share of e_1 + f_2 and of its image under u_x'] = [str(sum(x * x for x in psi)), str(sum(x * x for x in img))]
# (7) the character argument: no signed-permutation basis for all 48 (the trace at an order-6 element is 2, at its square -2: a signed permutation of 8 lines cannot give both)
orders = {}
for A in elems:
    P = IDENT; k = 0
    while True:
        P = mmul(P, A); k += 1
        if P == IDENT: break
    orders.setdefault(k, []).append(A)
out['(7) element orders (order: count)'] = {str(k): len(v) for k, v in sorted(orders.items())}
out['(7) traces: order 6 elements, order 3 elements'] = [sorted({str(sum(mats[A][r][r] for r in range(8))) for A in orders[6]}), sorted({str(sum(mats[A][r][r] for r in range(8))) for A in orders[3]})]
# the spin-up states along each axis as integer lines: (1 + sigma_a) e_1, reduced
def chi(a):
    v = mv(madd(ID8, sig[a]), [Fr(1)] + [Fr(0)] * 7)
    import math
    g = 0
    for x in v: g = math.gcd(g, int(x))
    return [int(x) // g for x in v]
out['(8) the spin-up states along x, y, z as the 8 lines, (1 + sigma_a) e_1 reduced'] = {a: chi(a) for a in 'xyz'}
out['(8) sigma_a chi_a = chi_a'] = {a: mv(sig[a], [Fr(x) for x in chi(a)]) == [Fr(x) for x in chi(a)] for a in 'xyz'}
out['(8) the densities (psi^T sigma psi) of chi_x, chi_y, chi_z: along the axis the norm, 0 across'] = {a: [str(x) for x in dens([Fr(x) for x in chi(a)], [Fr(x) for x in chi(a)])] for a in 'xyz'}
print(json.dumps(out, indent=1))
