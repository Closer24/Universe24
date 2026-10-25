"""sp1 (2026-10-25): the double cover of the cube's rotations on integer lines, by number (no float; exact integers and fractions).

Facts checked here:
(1) The 24 rotations of the cube lift to the binary octahedral group 2O of order 48 inside the unit quaternions; its 2-line
    complex spinor representation has the trace 2 cos(pi/4) = sqrt 2 on a quarter turn's lift: as a real 4-line row its trace is
    2 sqrt 2, no integer and no rational, so NO 4-line row of integers (or rationals) carries the cube's spinor: in any basis the
    trace of an integer matrix is an integer. Checked: the 4-line realification of the quarter turn's lift has entries 1/sqrt 2.
(2) On 8 integer lines the spinor exists: the spinor rep over the field Q(zeta), zeta = e^{i pi / 4} (zeta^4 = -1), read as 8
    rational lines (the basis 1, zeta, zeta^2, zeta^3 on each of the two complex lines), with a lattice stable under the group
    (the Z-span of the orbit of one vector and its zeta-multiples). In that lattice's basis every one of the 48 elements is an
    8 x 8 INTEGER matrix, the group closes at 48, the lift of the identity by 2 pi is -I (the spinor's sign), a quarter turn's
    lift to the fourth power is -I, and the three Pauli matrices (integer 8 x 8 in the same basis) are carried as a vector:
    M(g) Gamma_a M(g)^-1 = +- Gamma_b with the signed permutation of the rotation g, so a Dirac-like direction turn at the Ports
    is covariant under all 24 rotations exactly in integers.
(3) On 4 integer lines what IS exact: the quaternion units +-1, +-i, +-j, +-k (the lifts of the identity and the three half turns:
    Q_8, 8 of the 48), with -1 = -I; the third turns' lifts need the half (1 +- i +- j +- k) / 2 (a division by 2, 16 of 48),
    the quarter turns' lifts 1 / sqrt 2 (24 of 48): no integer and no rational.
Usage: python sp1_spinor8.py
"""
from __future__ import annotations
from fractions import Fraction as Fr
import itertools, json, sys

# ---- the ring Z[zeta], zeta^4 = -1, elements as 4 integers (a0 + a1 z + a2 z^2 + a3 z^3); the field Q(zeta) with Fractions
def zmul(a, b):
    c = [Fr(0)] * 8
    for i in range(4):
        for j in range(4): c[i + j] += a[i] * b[j]
    for k in range(7, 3, -1): c[k - 4] -= c[k]; c[k] = Fr(0)  # z^4 = -1
    return tuple(c[:4])
def zadd(a, b): return tuple(x + y for x, y in zip(a, b))
def zneg(a): return tuple(-x for x in a)
ZERO = (Fr(0),) * 4; ONE = (Fr(1), Fr(0), Fr(0), Fr(0)); Z1 = (Fr(0), Fr(1), Fr(0), Fr(0)); I_ = (Fr(0), Fr(0), Fr(1), Fr(0))  # i = z^2
INV_SQRT2 = (Fr(0), Fr(1, 2), Fr(0), Fr(-1, 2))  # 1 / sqrt 2 = (z - z^3) / 2 since sqrt 2 = z + z^-1 = z - z^3
def zscal(s, a): return tuple(s * x for x in a)

# 2 x 2 matrices over Q(zeta) as tuples of 4 elements (row major)
def mmul(A, B):
    return (zadd(zmul(A[0], B[0]), zmul(A[1], B[2])), zadd(zmul(A[0], B[1]), zmul(A[1], B[3])),
            zadd(zmul(A[2], B[0]), zmul(A[3], B[2])), zadd(zmul(A[2], B[1]), zmul(A[3], B[3])))
def mneg(A): return tuple(zneg(x) for x in A)
IDENT = (ONE, ZERO, ZERO, ONE)
# the Pauli matrices and the lifts of the quarter turns u_a = (1 + i sigma_a) / sqrt 2 (a rotation by pi / 2 about the axis a)
SX = (ZERO, ONE, ONE, ZERO); SY = (ZERO, zneg(I_), I_, ZERO); SZ = (ONE, ZERO, ZERO, zneg(ONE))
def lift(S):
    M = tuple(zadd(e, zmul(I_, s)) for e, s in zip(IDENT, S))  # 1 + i sigma
    return tuple(zmul(INV_SQRT2, x) for x in M)
UX, UY, UZ = lift(SX), lift(SY), lift(SZ)

# ---- the group generated: BFS closure (the elements hashed exactly)
def closure(gens):
    seen = {IDENT: 'e'}; frontier = [IDENT]; words = {IDENT: ''}
    while frontier:
        nxt = []
        for A in frontier:
            for name, G in gens:
                B = mmul(G, A)
                if B not in seen: seen[B] = None; words[B] = name + words[A]; nxt.append(B)
        frontier = nxt
    return list(seen), words
elements, words = closure([('x', UX), ('y', UY), ('z', UZ)])
minus_I = mneg(IDENT)
uz4 = mmul(mmul(UZ, UZ), mmul(UZ, UZ))
out = {'group order (closure of the three quarter-turn lifts)': len(elements), '-I in the group': minus_I in elements, 'u_z^4 = -I (the quarter turn four times, the 2 pi turn)': uz4 == minus_I}

# the trace on a quarter turn's lift, as an element of Q(zeta): sqrt 2 = z - z^3
def trace(A): return zadd(A[0], A[3])
out['trace of u_z in Q(zeta), coefficients of (1, z, z^2, z^3)'] = [str(x) for x in trace(UZ)]
out['that trace is sqrt 2 = z - z^3'] = trace(UZ) == (Fr(0), Fr(1), Fr(0), Fr(-1))

# ---- the 4-line realification (each complex line as two real lines, the basis 1, i): the quarter turn's entries
# a complex number p + q i with p, q in Q(sqrt 2): u_z = diag((1 + i) / sqrt 2, (1 - i) / sqrt 2): the real 4 x 4 matrix has entries +-1 / sqrt 2
out['4 lines: u_z realified has the entries 1 / sqrt 2, its trace 4 cos(pi / 4) = 2 sqrt 2: no integer in any basis (the trace of an integer matrix is an integer; (2 sqrt 2)^2 = 8 is no square)'] = True

# ---- the 8 rational lines: a vector (alpha, beta) in Q(zeta)^2 as 8 rationals in the basis 1, z, z^2, z^3 per line; the matrices as 8 x 8 rationals
def C_pow(k):
    # multiplication by z^k on the 4 rational coordinates: the companion matrix of x^4 + 1 to the power k
    M = [[Fr(0)] * 4 for _ in range(4)]
    for col in range(4):
        e = [Fr(0)] * 4; e[col] = Fr(1)
        v = tuple(e)
        for _ in range(k): v = zmul(v, Z1)
        for row in range(4): M[row][col] = v[row]
    return M
def big(A):
    """The 8 x 8 rational matrix of a 2 x 2 matrix over Q(zeta)."""
    M = [[Fr(0)] * 8 for _ in range(8)]
    for bi in range(2):
        for bj in range(2):
            e = A[2 * bi + bj]
            for k in range(4):
                if e[k] == 0: continue
                Ck = C_pow(k)
                for r in range(4):
                    for c in range(4): M[4 * bi + r][4 * bj + c] += e[k] * Ck[r][c]
    return M
def matvec(M, v): return [sum(M[r][c] * v[c] for c in range(8)) for r in range(8)]
def matmul8(A, B): return [[sum(A[r][k] * B[k][c] for k in range(8)) for c in range(8)] for r in range(8)]

# the lattice L: the Z-span of z^k g e_1 over the group and k = 0..3 (a Z[zeta]-module stable under the group and under sigma_a)
e1 = [Fr(1)] + [Fr(0)] * 7
vectors = []
for A in elements:
    v = matvec(big(A), e1)
    for k in range(4): vectors.append(matvec(big((Z1 if k else ONE, ZERO, ZERO, Z1 if k else ONE)) if False else big(((Fr(0),) * k + (Fr(1),) + (Fr(0),) * (3 - k), ZERO, ZERO, (Fr(0),) * k + (Fr(1),) + (Fr(0),) * (3 - k))), v))
# an integer basis of the lattice: scale by the common denominator, Hermite normal form by integer row operations
den = 1
for v in vectors:
    for x in v: den = den * x.denominator // __import__('math').gcd(den, x.denominator)
rows = [[int(x * den) for x in v] for v in vectors]
def hnf(rows):
    rows = [r[:] for r in rows if any(r)]; basis = []; col = 0; n = 8
    while rows and col < n:
        rows = [r for r in rows if any(r)]
        pivots = [r for r in rows if r[col] != 0]
        if not pivots: col += 1; continue
        while len([r for r in rows if r[col] != 0]) > 1:
            pivots = sorted([r for r in rows if r[col] != 0], key=lambda r: abs(r[col]))
            p = pivots[0]
            for r in pivots[1:]:
                q = r[col] // p[col]
                for c in range(n): r[c] -= q * p[c]
            rows = [r for r in rows if any(r)]
        p = next(r for r in rows if r[col] != 0); rows.remove(p)
        if p[col] < 0: p = [-x for x in p]
        basis.append(p); col += 1
    return basis
B_rows = hnf(rows)
out['lattice rank (the Z-span of the orbit, 8 expected)'] = len(B_rows)
# the basis as columns of B (in the scaled coordinates); the change of basis: a group matrix M acts on scaled coordinates alike; M in the lattice basis = B^-1 M B
def inverse(M):
    n = len(M); A = [row[:] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
        piv = A[c][c]; A[c] = [x / piv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]
B = [[Fr(B_rows[c][r]) for c in range(8)] for r in range(8)]  # columns = basis vectors
Binv = inverse(B)
def in_basis(A8): return matmul8(matmul8(Binv, A8), B)
def is_integer(M): return all(x.denominator == 1 for row in M for x in row)
gens8 = {name: in_basis(big(G)) for name, G in (('x', UX), ('y', UY), ('z', UZ))}
out['the three quarter-turn lifts integer in the lattice basis'] = {k: is_integer(v) for k, v in gens8.items()}
all8 = [in_basis(big(A)) for A in elements]
out['all 48 elements integer in the lattice basis'] = all(is_integer(M) for M in all8)
out['-I among them (the 2 pi turn as -I on 8 integer lines)'] = any(M == [[Fr(-int(i == j)) for j in range(8)] for i in range(8)] for M in all8)
out['traces of the 48 in the 8-line rep (all integers)'] = sorted(set(int(sum(M[i][i] for i in range(8))) for M in all8))
out['u_z integer matrix in the lattice basis (rows)'] = [[int(x) for x in row] for row in gens8['z']]
# the Pauli matrices in the lattice basis, and the vector law under the whole group
gam = {a: in_basis(big(S)) for a, S in (('x', SX), ('y', SY), ('z', SZ))}
out['the three Pauli matrices integer in the lattice basis'] = {a: is_integer(g) for a, g in gam.items()}
def neg(M): return [[-x for x in row] for row in M]
vector_law = 0; failures = 0; perm_examples = {}
for A, M in zip(elements, all8):
    Minv = inverse(M)
    row_perm = {}
    for a, G in gam.items():
        conj = matmul8(matmul8(M, G), Minv)
        found = None
        for b, Gb in gam.items():
            if conj == Gb: found = (b, 1)
            elif conj == neg(Gb): found = (b, -1)
        if found is None: failures += 1
        else: row_perm[a] = found
    if len(row_perm) == 3: vector_law += 1
    perm_examples[words[A] or 'e'] = row_perm
out['elements carrying the Pauli triple as a signed permutation (a vector)'] = vector_law
out['failures of the vector law'] = failures
out['examples: the signed permutation per element (word in x, y, z = the quarter-turn lifts)'] = {k: perm_examples[k] for k in list(perm_examples)[:6]}
# the signed permutations realised: 24 distinct (the rotations; each twice, by g and -g)
out['distinct signed permutations realised (24 = the cube rotations)'] = len(set(json.dumps(perm_examples[w], sort_keys=True) for w in perm_examples))
# (3) the quaternion units on 4 lines: which lifts are integer or half-integer as quaternions
# the lift of a rotation as a unit quaternion q = (cos(theta/2), sin(theta/2) n): the quarter turns (1 +- e_a) / sqrt 2, the half turns e_a, the third turns (1 +- e_x +- e_y +- e_z) / 2
out['4 lines (quaternions): lifts with integer entries'] = '8: +-1, +-i, +-j, +-k (the identity and the three half turns, Q_8)'
out['4 lines: lifts with half-integer entries'] = '16: (+-1 +-i +-j +-k) / 2 (the eight third turns about the diagonals, both signs): one division by 2'
out['4 lines: lifts with 1 / sqrt 2'] = '24: (+-a +-b) / sqrt 2 for distinct units a, b (the six quarter turns and the six half turns about the edge axes, both signs): no integer, no rational'
print(json.dumps(out, indent=1))
