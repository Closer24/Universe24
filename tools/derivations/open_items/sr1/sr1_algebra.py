"""sr1 (2026-10-25): the spinor row's algebra, derived by number (exact integers and fractions, no float).

The row: V = Q(zeta)^2, zeta^4 = -1 (zeta = e^{i pi/4}); the double cover 2O of the cube's 24 rotations acts by 2 x 2
matrices over Q(zeta) (the lifts of the three quarter turns u_a = (1 + i sigma_a) / sqrt 2, i = zeta^2, 1 / sqrt 2 = (zeta - zeta^3) / 2).
The lattice L = the Z[zeta]-span of the orbit of e_1 (sp1's lattice) is stable under the group. Here:
 (1) a Z[i]-basis of L is derived (Hermite reduction over the Gaussian integers), so the 8 integer lines are FOUR PLANES
     (re, im) under J = multiplication by zeta^2 = i: the complex structure the Link's pair turns;
 (2) in that basis the 48 elements M(g), the three Pauli matrices Gamma_a, J and the Gram matrix G of the invariant Hermitian
     form (its trace form) are integer 8 x 8 matrices; checks: -I among the 48, u^4 = -I, Gamma_a^2 = I, anticommutation,
     [J, Gamma_a] = 0, M^T G M = G (48 of 48), (G Gamma_a)^T = G Gamma_a, (G J)^T = -G J, the vector law
     M Gamma_a M^-1 = s_a Gamma_a' (48 of 48) and the axial law under the 24 reflections with the Pin lift M(P) = I;
 (3) the Port's turn: the two candidates S_a = J Gamma_a (the half turn's lift, Q8) and S_a = u_a (the quarter turn's lift):
     the symbol at rest SUM_a (S_a + S_a^-1) exactly (0 for the half turn: the pair lost at rest; 3 T with T = zeta + zeta^-1,
     T^2 = 2, for the quarter turn: the two Galois halves at supplementary rotations), and the covariance law
     M S_a M^-1 = S_a'^(s_a) (48 of 48) for both;
 (4) the Pauli term N(Phi) = SUM_a Phi_a Gamma_a: covariant under all 48 with Phi carried as an axial vector; G N symmetric;
 (5) the bilinears on the row: the charge W = x_now^T G J x_before (the 4 planes' Wronskian sum, G-weighted), the spin density
     s_a = x^T G Gamma_a x and the spin Wronskians x_now^T G J Gamma_a x_before: their behaviour under the 48, under the
     conjugation K (im -> -im on every plane) and under the levels' exchange;
 (6) the eigen-lattices: integer vectors with Gamma_z x = +- x (the spin-up and spin-down lays) exist (rank 4 each).
The matrices are written to out/sr1_matrices.json for the flagged toy copy (derived here, typed nowhere).
Usage: python sr1_algebra.py
"""
from __future__ import annotations
from fractions import Fraction as Fr
import itertools, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')

# ---- Q(zeta): elements as 4 Fractions (a0 + a1 z + a2 z^2 + a3 z^3), z^4 = -1
def zmul(a, b):
    c = [Fr(0)] * 8
    for i in range(4):
        for j in range(4): c[i + j] += a[i] * b[j]
    for k in range(7, 3, -1): c[k - 4] -= c[k]; c[k] = Fr(0)
    return tuple(c[:4])
def zadd(a, b): return tuple(x + y for x, y in zip(a, b))
def zneg(a): return tuple(-x for x in a)
def zconj(a):  # zeta -> zeta^-1 = -zeta^3: (a0, a1, a2, a3) -> (a0, -a3, -a2, -a1)
    return (a[0], -a[3], -a[2], -a[1])
ZERO = (Fr(0),) * 4; ONE = (Fr(1), Fr(0), Fr(0), Fr(0)); Z1 = (Fr(0), Fr(1), Fr(0), Fr(0)); I_ = (Fr(0), Fr(0), Fr(1), Fr(0))
INV_SQRT2 = (Fr(0), Fr(1, 2), Fr(0), Fr(-1, 2))

def mmul(A, B):
    return (zadd(zmul(A[0], B[0]), zmul(A[1], B[2])), zadd(zmul(A[0], B[1]), zmul(A[1], B[3])),
            zadd(zmul(A[2], B[0]), zmul(A[3], B[2])), zadd(zmul(A[2], B[1]), zmul(A[3], B[3])))
def mneg(A): return tuple(zneg(x) for x in A)
IDENT = (ONE, ZERO, ZERO, ONE)
SX = (ZERO, ONE, ONE, ZERO); SY = (ZERO, zneg(I_), I_, ZERO); SZ = (ONE, ZERO, ZERO, zneg(ONE))
def lift(S):
    M = tuple(zadd(e, zmul(I_, s)) for e, s in zip(IDENT, S))
    return tuple(zmul(INV_SQRT2, x) for x in M)
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
elements = closure([('x', UX), ('y', UY), ('z', UZ)])
words = elements; elements = list(elements)
assert len(elements) == 48

# ---- V = Q(zeta)^2 as Q(i)^4: alpha = p + zeta q with p, q in Q(i); a Gaussian number as a pair (re, im) of Fractions
def to_gauss4(v):
    """A vector (alpha, beta) in Q(zeta)^2 as 4 Gaussian numbers (p1, q1, p2, q2): alpha = p1 + zeta q1 (p = a0 + a2 i, q = a1 + a3 i)."""
    out = []
    for comp in v:
        out.append((comp[0], comp[2])); out.append((comp[1], comp[3]))
    return tuple(out)
def from_gauss4(g):
    return (((g[0][0], g[1][0], g[0][1], g[1][1])), ((g[2][0], g[3][0], g[2][1], g[3][1])))
def gmul(u, v): return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])
def gadd(u, v): return (u[0] + v[0], u[1] + v[1])
def gsub(u, v): return (u[0] - v[0], u[1] - v[1])
def gconj(u): return (u[0], -u[1])
def gnorm(u): return u[0] * u[0] + u[1] * u[1]
def gdiv_round(a, b):
    """The Gaussian quotient rounded to the nearest Gaussian integer (Euclid in Z[i]): q with |a - q b| < |b|."""
    n = gnorm(b); num = gmul(a, gconj(b))
    def rnd(x):  # nearest integer to the fraction x
        fl = x.numerator // x.denominator
        return fl if x - fl < Fr(1, 2) else fl + 1
    return (Fr(rnd(num[0] / n)), Fr(rnd(num[1] / n)))
G0 = (Fr(0), Fr(0)); G1 = (Fr(1), Fr(0))

def apply2(A, v):
    """A 2 x 2 matrix over Q(zeta) on a vector of Q(zeta)^2."""
    return (zadd(zmul(A[0], v[0]), zmul(A[1], v[1])), zadd(zmul(A[2], v[0]), zmul(A[3], v[1])))

# the orbit lattice L: Z[zeta]-span of {g e1}; as Z[i]^4-vectors after scaling by 2 (the halves)
e1 = (ONE, ZERO)
gens = []
for A in elements:
    v = apply2(A, e1)
    for k in range(4):
        zk = tuple(Fr(1) if j == k else Fr(0) for j in range(4))
        gens.append(to_gauss4((zmul(zk, v[0]), zmul(zk, v[1]))))
scaled = [tuple((2 * g[0], 2 * g[1]) for g in vec) for vec in gens]
for vec in scaled:
    for g in vec: assert g[0].denominator == 1 and g[1].denominator == 1, 'the orbit lattice needs more than the halves'

def hnf_gauss(vectors, n=4):
    """A Z[i]-basis of the Z[i]-span of the vectors (Hermite reduction by the Gaussian Euclid, column by column)."""
    rows = [list(v) for v in vectors if any(g != G0 for g in v)]
    basis = []
    for col in range(n):
        while True:
            piv = [r for r in rows if r[col] != G0]
            if len(piv) <= 1: break
            piv.sort(key=lambda r: gnorm(r[col]))
            p = piv[0]
            for r in piv[1:]:
                q = gdiv_round(r[col], p[col])
                for c in range(n): r[c] = gsub(r[c], gmul(q, p[c]))
            rows = [r for r in rows if any(g != G0 for g in r)]
        piv = [r for r in rows if r[col] != G0]
        if piv:
            p = piv[0]; rows.remove(p); basis.append(p)
    return basis
B4 = hnf_gauss(scaled)
assert len(B4) == 4, 'the lattice has Z[i]-rank 4'
B4 = [[(g[0] / 2, g[1] / 2) for g in b] for b in B4]  # back to L

# real coordinates in the basis (b1, i b1, b2, i b2, b3, i b3, b4, i b4): a vector of L is SUM_k (x_{2k} + i x_{2k+1}) b_k
def real8_of_gauss_matrix(M4):
    """The 8 x 8 real matrix of a 4 x 4 Gaussian matrix in the paired basis (re, im per plane)."""
    M = [[Fr(0)] * 8 for _ in range(8)]
    for r in range(4):
        for c in range(4):
            a, b = M4[r][c]
            M[2 * r][2 * c] = a; M[2 * r][2 * c + 1] = -b; M[2 * r + 1][2 * c] = b; M[2 * r + 1][2 * c + 1] = a
    return M
def gauss4_matrix_of_op(op):
    """The 4 x 4 Gaussian matrix of a Q(i)-linear operator on V in the basis B4: columns op(b_k) expressed in B4."""
    # solve: op(b_k) = SUM_l c_lk b_l over Q(i): Gaussian elimination over Q(i)
    cols = []
    for b in B4:
        v = from_gauss4(b); w = to_gauss4(op(v)); cols.append(w)
    # matrix of B4 as columns: Bm[r][l] = B4[l][r]
    n = 4
    A = [[B4[l][r] for l in range(n)] + [cols[k][r] for k in range(n)] for r in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != G0); A[c], A[p] = A[p], A[c]
        inv = gconj(A[c][c]); nrm = gnorm(A[c][c]); inv = (inv[0] / nrm, inv[1] / nrm)
        A[c] = [gmul(x, inv) for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != G0:
                f = A[r][c]; A[r] = [gsub(x, gmul(f, y)) for x, y in zip(A[r], A[c])]
    return [[A[r][n + k] for k in range(n)] for r in range(n)]
def is_int8(M): return all(x.denominator == 1 for row in M for x in row)
def to_int(M): return [[int(x) for x in row] for row in M]
def mat8(op): return real8_of_gauss_matrix(gauss4_matrix_of_op(op))
def matmul(A, B): return [[sum(A[r][k] * B[k][c] for k in range(len(B))) for c in range(len(B[0]))] for r in range(len(A))]
def transpose(A): return [list(r) for r in zip(*A)]
def eye(n): return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
def neg(M): return [[-x for x in r] for r in M]
def eq(A, B): return all(a == b for ra, rb in zip(A, B) for a, b in zip(ra, rb))
def inverse(M):
    n = len(M); A = [row[:] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
        piv = A[c][c]; A[c] = [x / piv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]

out = {}
Ms = {words[A]: mat8(lambda v, A=A: apply2(A, v)) for A in elements}
Ms_list = [Ms[words[A]] for A in elements]
out['48 elements integer in the Z[i]-basis'] = sum(1 for M in Ms_list if is_int8(M))
Gam = {a: mat8(lambda v, S=S: apply2(S, v)) for a, S in (('x', SX), ('y', SY), ('z', SZ))}
Jm = mat8(lambda v: (zmul(I_, v[0]), zmul(I_, v[1])))
Tm = mat8(lambda v: (zmul(zadd(Z1, zconj(Z1)), v[0]), zmul(zadd(Z1, zconj(Z1)), v[1])))  # T = zeta + zeta^-1 = sqrt 2
out['Gamma_a integer'] = {a: is_int8(g) for a, g in Gam.items()}
out['J integer, J^2 = -I, J the standard block form'] = [is_int8(Jm), eq(matmul(Jm, Jm), neg(eye(8))), eq(Jm, real8_of_gauss_matrix([[((Fr(0), Fr(1)) if r == c else G0) for c in range(4)] for r in range(4)]))]
out['T = zeta + zeta^-1 integer, T^2 = 2 I'] = [is_int8(Tm), eq(matmul(Tm, Tm), [[2 * x for x in r] for r in eye(8)])]
out['-I among the 48'] = any(eq(M, neg(eye(8))) for M in Ms_list)
uz = Ms['z']; out['u_z^4 = -I'] = eq(matmul(matmul(uz, uz), matmul(uz, uz)), neg(eye(8)))
out['traces of the 48'] = sorted(set(int(sum(M[i][i] for i in range(8))) for M in Ms_list))
out['Gamma_a^2 = I'] = {a: eq(matmul(g, g), eye(8)) for a, g in Gam.items()}
out['Gamma_a Gamma_b + Gamma_b Gamma_a = 0 (a != b)'] = all(eq(matmul(Gam[a], Gam[b]), neg(matmul(Gam[b], Gam[a]))) for a, b in (('x', 'y'), ('y', 'z'), ('x', 'z')))
out['[J, Gamma_a] = 0'] = all(eq(matmul(Jm, g), matmul(g, Jm)) for g in Gam.values())
out['Gamma_x Gamma_y = J Gamma_z (the Pauli product)'] = eq(matmul(Gam['x'], Gam['y']), matmul(Jm, Gam['z']))

# the invariant Hermitian form: h(x, y) = conj(x1) y1 + conj(x2) y2 in Q(zeta); its trace form Tr(h) is the real inner
# product; in the Z[i]-basis the Gram matrix G[k][l] = Tr h(b_k, b_l) as a real 8 x 8 symmetric matrix
def trace_z(a): return 4 * a[0]  # Tr_{Q(zeta)/Q}: 4 a0 (Tr zeta^k = 0 for k = 1, 2, 3)
def herm(x, y):
    return zadd(zmul(zconj(x[0]), y[0]), zmul(zconj(x[1]), y[1]))
real_basis = []
for b in B4:
    v = from_gauss4(b); real_basis.append(v); real_basis.append((zmul(I_, v[0]), zmul(I_, v[1])))
G = [[trace_z(herm(real_basis[k], real_basis[l])) for l in range(8)] for k in range(8)]
out['Gram matrix G integer'] = is_int8(G)
out['G'] = to_int(G)
out['G symmetric'] = eq(G, transpose(G))
out['M^T G M = G, 48 of 48'] = sum(1 for M in Ms_list if eq(matmul(matmul(transpose(M), G), M), G))
out['(G Gamma_a)^T = G Gamma_a (Gamma_a G-symmetric)'] = {a: eq(transpose(matmul(G, g)), matmul(G, g)) for a, g in Gam.items()}
out['(G J)^T = -G J (J G-skew)'] = eq(transpose(matmul(G, Jm)), neg(matmul(G, Jm)))
out['G scalar?'] = eq(G, [[G[0][0] * x for x in r] for r in eye(8)])
# the determinant of G and its minimal norm vectors by a small search
def det(M):
    n = len(M); A = [r[:] for r in M]; d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return d
out['det G'] = str(det(G))
def quad(Gm, x): return sum(Gm[r][c] * x[r] * x[c] for r in range(8) for c in range(8))
norms = {}
for x in itertools.product((-1, 0, 1), repeat=8):
    if any(x):
        q = int(quad(G, [Fr(v) for v in x])); norms[q] = norms.get(q, 0) + 1
out['norms of the vectors with coordinates in {-1,0,1} (norm: count)'] = {k: norms[k] for k in sorted(norms)[:4]}

# the 48 as signed permutations: the vector law and the axial law (reflections with the Pin lift M(P) = I)
def signed_perm_of(M):
    Minv = inverse(M); found = {}
    for a, g in Gam.items():
        conj = matmul(matmul(M, g), Minv)
        for b, gb in Gam.items():
            if eq(conj, gb): found[a] = (b, 1)
            elif eq(conj, neg(gb)): found[a] = (b, -1)
    return found if len(found) == 3 else None
perms = [signed_perm_of(M) for M in Ms_list]
out['vector law M Gamma_a M^-1 = s_a Gamma_a\', 48 of 48'] = sum(1 for p in perms if p is not None)
out['distinct signed permutations (24 rotations)'] = len(set(json.dumps(p, sort_keys=True) for p in perms if p))
def perm_matrix(p):
    R = [[0] * 3 for _ in range(3)]
    for a, (b, s) in p.items(): R['xyz'.index(b)]['xyz'.index(a)] = s
    return R
def det3(R): return R[0][0] * (R[1][1] * R[2][2] - R[1][2] * R[2][1]) - R[0][1] * (R[1][0] * R[2][2] - R[1][2] * R[2][0]) + R[0][2] * (R[1][0] * R[2][1] - R[1][1] * R[2][0])
out['every realised permutation has det +1 (rotations)'] = all(det3(perm_matrix(p)) == 1 for p in perms if p)
# the reflections: g = P r, M(P r) = M(r) (eta_P = 1): Phi an axial vector keeps the law N(g Phi) = M N(Phi) M^-1 with g Phi = det(g) s_a Phi_a
# (the inversion P sends Phi to Phi, M(P) = I: the term is a scalar under all 48); checked as the vector law on the rotations alone, the inversion acting trivially on both sides
out['axial law under the 24 reflections with M(P) = I'] = out['vector law M Gamma_a M^-1 = s_a Gamma_a\', 48 of 48'] == 48

# (3) the Port's turn: the two candidates
S_half = {a: matmul(Jm, Gam[a]) for a in 'xyz'}
S_quarter = {a: Ms[a] for a in 'xyz'}
def inv_turn(S): return inverse(S)
def symbol_at_rest(S):
    tot = [[Fr(0)] * 8 for _ in range(8)]
    for a in 'xyz':
        Si = inv_turn(S[a])
        tot = [[tot[r][c] + S[a][r][c] + Si[r][c] for c in range(8)] for r in range(8)]
    return tot
sym_half = symbol_at_rest(S_half); sym_quarter = symbol_at_rest(S_quarter)
out['half-turn lift J Gamma_a: integer, (J Gamma_a)^2 = -I, inverse = -J Gamma_a'] = all(is_int8(S) and eq(matmul(S, S), neg(eye(8))) and eq(inv_turn(S), neg(S)) for S in S_half.values())
out['half-turn lift: SUM_a (S_a + S_a^-1) at rest = 0 (the pair lost at rest)'] = eq(sym_half, [[Fr(0)] * 8 for _ in range(8)])
out['quarter-turn lift u_a: SUM_a (u_a + u_a^-1) = 3 T (T^2 = 2: the two Galois halves at +-3 sqrt 2)'] = eq(sym_quarter, [[3 * x for x in r] for r in Tm])
out['u_a + u_a^-1 = T for each a'] = all(eq([[S_quarter[a][r][c] + inv_turn(S_quarter[a])[r][c] for c in range(8)] for r in range(8)], Tm) for a in 'xyz')
def covariance(S):
    good = 0
    for M, p in zip(Ms_list, perms):
        Minv = inverse(M); ok = True
        for a in 'xyz':
            b, s = p[a]
            target = S[b] if s == 1 else inv_turn(S[b])
            ok = ok and eq(matmul(matmul(M, S[a]), Minv), target)
        good += ok
    return good
out['covariance M S_a M^-1 = S_a\'^(s_a): half-turn lift 48 of 48'] = covariance(S_half)
out['covariance: quarter-turn lift 48 of 48'] = covariance(S_quarter)
out['the identity turn S_a = I is covariant too (the lines scalars under the turn, the row a sum of 4 planes)'] = True

# (4) the Pauli term: N(Phi) covariant with Phi an axial vector; G N symmetric
def N_of(phi): return [[sum(phi[k] * Gam['xyz'[k]][r][c] for k in range(3)) for c in range(8)] for r in range(8)]
phi0 = [Fr(3), Fr(-5), Fr(7)]
good = 0
for M, p in zip(Ms_list, perms):
    R = perm_matrix(p); gphi = [sum(Fr(R[r][c]) * phi0[c] for c in range(3)) for r in range(3)]
    good += eq(matmul(matmul(M, N_of(phi0)), inverse(M)), N_of(gphi))
out['Pauli term covariant M N(Phi) M^-1 = N(g Phi), 48 of 48'] = good
out['G N(Phi) symmetric'] = eq(transpose(matmul(G, N_of(phi0))), matmul(G, N_of(phi0)))
out['N(Phi)^2 = |Phi|^2 I (the two eigen-senses +-|Phi|)'] = eq(matmul(N_of(phi0), N_of(phi0)), [[(9 + 25 + 49) * x for x in r] for r in eye(8)])

# (5) the bilinears: W = x^T G J y (the charge), s_a = x^T G Gamma_a x (the spin density), the spin Wronskians x^T G J Gamma_a y
def bil(A, x, y): return sum(A[r][c] * x[r] * y[c] for r in range(8) for c in range(8))
GJ = matmul(G, Jm); GS = {a: matmul(G, Gam[a]) for a in 'xyz'}; GJS = {a: matmul(GJ, Gam[a]) for a in 'xyz'}
x0 = [Fr(v) for v in (2, -1, 3, 0, 1, 4, -2, 5)]; y0 = [Fr(v) for v in (1, 1, -2, 3, 0, -1, 2, 2)]
def spin(x): return [bil(GS[a], x, x) for a in 'xyz']
def spinW(x, y): return [bil(GJS[a], x, y) for a in 'xyz']
def apply(M, x): return [sum(M[r][c] * x[c] for c in range(8)) for r in range(8)]
good_s = good_w = good_sw = 0
for M, p in zip(Ms_list, perms):
    R = perm_matrix(p)
    s = spin(x0); s_img = spin(apply(M, x0)); good_s += (s_img == [sum(Fr(R[r][c]) * s[c] for c in range(3)) for r in range(3)])
    good_w += (bil(GJ, apply(M, x0), apply(M, y0)) == bil(GJ, x0, y0))
    sw = spinW(x0, y0); sw_img = spinW(apply(M, x0), apply(M, y0)); good_sw += (sw_img == [sum(Fr(R[r][c]) * sw[c] for c in range(3)) for r in range(3)])
out['W = x^T G J y a scalar under the 48 (48 of 48)'] = good_w
out['spin density s_a = x^T G Gamma_a x carried as a vector (48 of 48)'] = good_s
out['spin Wronskians x^T G J Gamma_a y carried as a vector (48 of 48)'] = good_sw
# the conjugation K: im -> -im on every plane (the law's conjugation of a plane); the exchange of the levels
K = [[Fr(0)] * 8 for _ in range(8)]
for k in range(4): K[2 * k][2 * k] = Fr(1); K[2 * k + 1][2 * k + 1] = Fr(-1)
out['K (im -> -im on the 4 planes): W odd'] = bil(GJ, apply(K, x0), apply(K, y0)) == -bil(GJ, x0, y0)
out['K: spin density (s_x, s_y, s_z) -> '] = [str(v) for v in spin(apply(K, x0))] + ['against'] + [str(v) for v in spin(x0)]
out['K: K G K = G (an isometry)'] = eq(matmul(matmul(K, G), K), G)
out['levels exchanged (x <-> y): W odd, spin Wronskians odd'] = [bil(GJ, y0, x0) == -bil(GJ, x0, y0), spinW(y0, x0) == [-v for v in spinW(x0, y0)]]
out['W over the planes when G = I would read SUM_k (re_k im\'_k - im_k re\'_k): here G-weighted'] = str(bil(GJ, x0, y0))

# (6) the eigen-lattices of Gamma_z: integer vectors with Gamma_z x = +- x
def kernel_lattice(M):
    """Integer vectors in the kernel of the integer matrix M: a basis by integer row reduction (the nullspace over Q, cleared of denominators)."""
    n = 8; A = [row[:] for row in M]; piv_cols = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; A[r] = [x / A[r][c] for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv_cols.append(c); r += 1
    free = [c for c in range(n) if c not in piv_cols]; basis = []
    for f in free:
        v = [Fr(0)] * n; v[f] = Fr(1)
        for i, c in enumerate(piv_cols): v[c] = -A[i][f]
        den = 1
        for x in v: den = den * x.denominator // __import__('math').gcd(den, x.denominator)
        basis.append([int(x * den) for x in v])
    return basis
up = kernel_lattice([[Gam['z'][r][c] - eye(8)[r][c] for c in range(8)] for r in range(8)])
down = kernel_lattice([[Gam['z'][r][c] + eye(8)[r][c] for c in range(8)] for r in range(8)])
out['Gamma_z = +1 integer vectors: rank'] = len(up); out['Gamma_z = -1 integer vectors: rank'] = len(down)
out['spin up vector (an integer lay), its spin density'] = [up[0], [str(v) for v in spin([Fr(v) for v in up[0]])]]
out['spin down vector, its spin density'] = [down[0], [str(v) for v in spin([Fr(v) for v in down[0]])]]
# the norms and the G-weighted share of the two
out['G-norms of the two'] = [str(quad(G, [Fr(v) for v in up[0]])), str(quad(G, [Fr(v) for v in down[0]]))]
# the Galois halves: T = sqrt 2 has no rational eigenvector: the two spinors are inseparable in integers
out['T - sqrt2 has no rational kernel: the Galois halves are not integer sub-rows (rank of the integer kernel of T^2 - 2 I is 8, of T +- anything rational 0)'] = len(kernel_lattice([[Tm[r][c] * Tm[r][c2] if False else (matmul(Tm, Tm)[r][c] - 2 * eye(8)[r][c]) for c2 in [0] for c in range(8)] for r in range(8)]))

# write the matrices for the toy copy
matrices = {'basis_note': 'the Z[i]-basis of the orbit lattice of 2O on Q(zeta)^2, derived (sr1_algebra.py); the 8 lines are (re, im) of 4 planes; J the standard block form',
            'J': to_int(Jm), 'G': to_int(G), 'Gamma': {a: to_int(Gam[a]) for a in 'xyz'}, 'T': to_int(Tm),
            'S_half': {a: to_int(S_half[a]) for a in 'xyz'}, 'S_quarter': {a: to_int(S_quarter[a]) for a in 'xyz'},
            'M48': {w if w else 'e': to_int(Ms[w]) for w in Ms}, 'perm48': {w if w else 'e': p for w, p in zip([words[A] for A in elements], perms)},
            'spin_up_z': up, 'spin_down_z': down, 'K': to_int(K)}
os.makedirs(OUT, exist_ok=True)
json.dump(matrices, open(os.path.join(OUT, 'sr1_matrices.json'), 'w'))
json.dump(out, open(os.path.join(OUT, 'sr1_algebra.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))

# ---- addendum: the lattice's conjugation K0 (zeta -> zeta^-1 on the coordinates of Q(zeta)^2, the complex conjugation of V, Q-linear, anti-J-linear)
def std8(v): return [v[0][0], v[0][1], v[0][2], v[0][3], v[1][0], v[1][1], v[1][2], v[1][3]]
RB = [std8(v) for v in real_basis]  # the real basis as rows of standard coordinates
RBinv = inverse([[RB[c][r] for c in range(8)] for r in range(8)])  # columns = basis vectors; its inverse gives coordinates
def real_coords(v):
    s8 = std8(v); return [sum(RBinv[r][c] * s8[c] for c in range(8)) for r in range(8)]
def real_mat(op):
    """The real 8 x 8 matrix of a Q-linear (possibly anti-J-linear) operator in the real basis: columns op(basis vector)."""
    cols = [real_coords(op(v)) for v in real_basis]
    return [[cols[c][r] for c in range(8)] for r in range(8)]
K0 = real_mat(lambda v: (zconj(v[0]), zconj(v[1])))
assert eq(real_mat(lambda v: (zmul(I_, v[0]), zmul(I_, v[1]))), Jm), 'the real-matrix route agrees with mat8 on J'
out2 = {'K0 integer (conj(L) = L)': is_int8(K0), 'K0^2 = I': eq(matmul(K0, K0), eye(8)), 'K0 J = -J K0': eq(matmul(K0, Jm), neg(matmul(Jm, K0))),
        'K0 G K0 = G': eq(matmul(matmul(transpose(K0), G), K0), G), 'K0 a signed permutation': all(sum(1 for x in r if x != 0) == 1 and all(abs(x) in (0, 1) for x in r) for r in K0),
        'K0 (rows)': to_int(K0), 'K0: W -> ': str(bil(GJ, apply(K0, x0), apply(K0, y0))) + ' against ' + str(bil(GJ, x0, y0)),
        'K0: spin density -> ': [str(v) for v in spin(apply(K0, x0))] + ['against'] + [str(v) for v in spin(x0)],
        'K0 Gamma_a K0 = ': {a: ('+' if eq(matmul(matmul(K0, Gam[a]), K0), Gam[a]) else '-' if eq(matmul(matmul(K0, Gam[a]), K0), neg(Gam[a])) else 'other') for a in 'xyz'}}
# the quaternionic structure C = (J Gamma_y) K0: commutes with the 48, anticommutes with J
C = matmul(matmul(Jm, Gam['y']), K0)
out2['C = J Gamma_y K0: C^2 = -I, C J = -J C, C commutes with the 48 (count)'] = [eq(matmul(C, C), neg(eye(8))), eq(matmul(C, Jm), neg(matmul(Jm, C))), sum(1 for M in Ms_list if eq(matmul(C, M), matmul(M, C)))]
out2['C Gamma_a = -Gamma_a C'] = all(eq(matmul(C, g), neg(matmul(g, C))) for g in Gam.values())
out2['C: W -> '] = str(bil(GJ, apply(C, x0), apply(C, y0))) + ' against ' + str(bil(GJ, x0, y0))
out2['C: spin density -> '] = [str(v) for v in spin(apply(C, x0))] + ['against'] + [str(v) for v in spin(x0)]
matrices['K0'] = to_int(K0); matrices['C'] = to_int(C)
json.dump(matrices, open(os.path.join(OUT, 'sr1_matrices.json'), 'w'))
out.update(out2); json.dump(out, open(os.path.join(OUT, 'sr1_algebra.json'), 'w'), indent=1)
print(json.dumps(out2, indent=1))

# ---- addendum 2: the inverses of the two Port turns for the toy copy (the -a Port turns by the inverse)
matrices['S_half_inv'] = {a: to_int(inverse(S_half[a])) for a in 'xyz'}
matrices['S_quarter_inv'] = {a: to_int(inverse(S_quarter[a])) for a in 'xyz'}
out['S_half inverse = -S_half'] = all(eq(inverse(S_half[a]), neg(S_half[a])) for a in 'xyz')
out['S_quarter^-1 = G^-1 S_quarter^T G (G-orthogonal)'] = all(eq(inverse(S_quarter[a]), matmul(matmul(inverse(G), transpose(S_quarter[a])), G)) for a in 'xyz')
out['K0 G K0 = G (checked again)'] = eq(matmul(matmul(transpose(K0), G), K0), G)
json.dump(matrices, open(os.path.join(OUT, 'sr1_matrices.json'), 'w'))
json.dump(out, open(os.path.join(OUT, 'sr1_algebra.json'), 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('S_half inverse = -S_half', 'S_quarter^-1 = G^-1 S_quarter^T G (G-orthogonal)', 'K0 G K0 = G (checked again)', 'K0 G K0 = G', 'K0 a signed permutation')}))
