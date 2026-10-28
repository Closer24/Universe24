"""Sofer's check of David's turning clock (DAVID-TENSOR24-THE-CAP.md, section 2): the tick U = W_z W_y W_x with
W_a = P_a^+ T_+a + P_a^- T_-a, P_a^+- = (1 +- sigma_a) / 2, (T_+-a psi)(x) = psi(x -+ e_a).
Two readings, exact in Gaussian rationals (Fractions of complex via sympy-free pairs): (1) the tick's reach: which offsets
it reads; (2) whether the tick commutes with the cube's 24 turns (the law's line 94), the spinor lifted from the double cover.
Integers/Fractions only."""
import itertools
from fractions import Fraction as Fr

L = 5  # side of the torus: offsets (-1, 0, 1) are distinct and wrap does not mix them

class G:  # Gaussian rational a + b i
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def __sub__(s, o): return G(s.a - o.a, s.b - o.b)
    def __neg__(s): return G(-s.a, -s.b)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def iszero(s): return s.a == 0 and s.b == 0
    def __repr__(s): return f"({s.a}+{s.b}i)"
ONE, ZERO, I = G(1), G(0), G(0, 1)
SIG = {
    0: [[ZERO, ONE], [ONE, ZERO]],
    1: [[ZERO, -I], [I, ZERO]],
    2: [[ONE, ZERO], [ZERO, -ONE]],
}
def mat_add(A, B): return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]
def mat_scale(A, c): return [[A[i][j] * c for j in range(2)] for i in range(2)]
ID = [[ONE, ZERO], [ZERO, ONE]]
HALF = G(Fr(1, 2))
def proj(a, sign):
    s = mat_scale(SIG[a], G(sign))
    return mat_scale(mat_add(ID, s), HALF)

# an operator on the torus as a dict: (dest_site, dest_comp, src_site, src_comp) -> G, sparse
def add_site(x, d): return tuple((x[i] + d[i]) % L for i in range(3))
SITES = list(itertools.product(range(L), repeat=3))
def W(a):
    op = {}
    for x in SITES:
        for sign in (+1, -1):
            P = proj(a, sign)
            d = [0, 0, 0]; d[a] = -sign   # psi(x - sign e_a)
            src = add_site(x, d)
            for i in range(2):
                for j in range(2):
                    c = P[i][j]
                    if not c.iszero():
                        k = (x, i, src, j)
                        op[k] = op.get(k, ZERO) + c
    return op
def compose(A, B):  # A after B
    byA = {}
    for (x, i, y, j), c in A.items():
        byA.setdefault((y, j), []).append((x, i, c))
    out = {}
    for (y, j, z, k), c2 in B.items():
        for (x, i, c1) in byA.get((y, j), []):
            key = (x, i, z, k)
            out[key] = out.get(key, ZERO) + c1 * c2
    return {k: v for k, v in out.items() if not v.iszero()}

Wx, Wy, Wz = W(0), W(1), W(2)
SUBS = {'x': Wx, 'y': Wy, 'z': Wz}
def tick(order):
    a, b, c = order
    return compose(SUBS[a], compose(SUBS[b], SUBS[c]))
U = tick('zyx')

# (1) the reach: the offsets src - dest read by the tick
def off(x, y):
    o = []
    for i in range(3):
        d = (y[i] - x[i]) % L
        o.append(d if d <= L // 2 else d - L)
    return tuple(o)
reach = sorted({off(x, y) for (x, i, y, j) in U})
print('reach of one tick U = Wz Wy Wx (offsets read):', len(reach), reach)
print('offsets of the six Spokes read:', [o for o in reach if sum(abs(t) for t in o) == 1])
print('largest L1 distance read:', max(sum(abs(t) for t in o) for o in reach))
for name, op in (('Wx', Wx), ('Wy', Wy), ('Wz', Wz)):
    print(name, 'reads', sorted({off(x, y) for (x, i, y, j) in op}))

# (2) the 24: a rotation R (a signed permutation matrix of determinant 1) acts on sites x -> R x and on the spinor by a lift S
# with S sigma_a S^dagger = sum_b R_ba sigma_b  (so that sigma . p is invariant).  Lifts from axis-angle in Gaussian rationals
# exist for the 24 (up to the factor 1 + i or 1 - i), found here by solving S sigma_a = (sum_b R_ba sigma_b) S for S.
def mat_mul(A, B):
    return [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]
def rotations():
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            R = [[0] * 3 for _ in range(3)]
            for a in range(3):
                R[perm[a]][a] = signs[a]
            det = (R[0][0] * (R[1][1] * R[2][2] - R[1][2] * R[2][1])
                   - R[0][1] * (R[1][0] * R[2][2] - R[1][2] * R[2][0])
                   + R[0][2] * (R[1][0] * R[2][1] - R[1][1] * R[2][0]))
            if det == 1:
                out.append(R)
    return out
ROTS = rotations()
assert len(ROTS) == 24
def lift(R):
    # solve S sigma_a = (sum_b R[b][a] sigma_b) S for a = 0, 1, 2 over a small set of Gaussian-rational S = (p, q; r, s)
    cand = [G(a, b) for a in range(-2, 3) for b in range(-2, 3)]
    # linear: unknown S entries; brute force over small Gaussian integers (entries in -2..2 + i(-2..2)) is 25^4 = 390k: ok
    target = []
    for a in range(3):
        T = [[ZERO, ZERO], [ZERO, ZERO]]
        for b in range(3):
            if R[b][a] != 0:
                T = mat_add(T, mat_scale(SIG[b], G(R[b][a])))
        target.append(T)
    for p in cand:
        for q in cand:
            for r in cand:
                for s in cand:
                    S = [[p, q], [r, s]]
                    if all(x.iszero() for x in (p, q, r, s)):
                        continue
                    ok = True
                    for a in range(3):
                        lhs = mat_mul(S, SIG[a]); rhs = mat_mul(target[a], S)
                        if not all(lhs[i][j] == rhs[i][j] for i in range(2) for j in range(2)):
                            ok = False; break
                    if ok:
                        return S
    return None
def rot_site(R, x):
    c = [x[i] if x[i] <= L // 2 else x[i] - L for i in range(3)]
    y = [sum(R[i][j] * c[j] for j in range(3)) for i in range(3)]
    return tuple(t % L for t in y)
def conj_op(op, R, S):
    # (Rop psi)(x) = S psi(R^-1 x): matrix of the action Rg: (Rg)_(x i, y j) = S_ij delta(x, R y)
    # conjugate: Rg op Rg^-1.  Build Rg as a sparse operator and Rg^-1 as its adjoint (S is a scalar multiple of a unitary, so use the exact inverse).
    # Rg^-1: (y, j) <- (x, i) with weight (S^-1)_ji
    det = S[0][0] * S[1][1] - S[0][1] * S[1][0]
    # inverse of a 2x2 over Gaussian rationals
    def ginv(z):
        n = z.a * z.a + z.b * z.b
        return G(z.a / n, -z.b / n)
    di = ginv(det)
    Sinv = [[S[1][1] * di, -S[0][1] * di], [-S[1][0] * di, S[0][0] * di]]
    Rg = {}
    Rinv = {}
    for y in SITES:
        x = rot_site(R, y)
        for i in range(2):
            for j in range(2):
                if not S[i][j].iszero():
                    Rg[(x, i, y, j)] = S[i][j]
                if not Sinv[i][j].iszero():
                    Rinv[(y, i, x, j)] = Sinv[i][j]
    return compose(Rg, compose(op, Rinv))
def same(A, B):
    # equal up to nothing: exact equality
    keys = set(A) | set(B)
    return all((A.get(k, ZERO) - B.get(k, ZERO)).iszero() for k in keys)
# test on the three sub-acts (permuted, not equal individually) and on the tick
import sys
sys.setrecursionlimit(10000)
lifts = [(R, lift(R)) for R in ROTS]
print('rotations with an exact Gaussian-rational lift found:', sum(1 for R, S in lifts if S is not None), 'of 24')

# the lifts are right when each sub-act goes to the sub-act of the turned axis exactly
good = 0
for R, S in lifts:
    ok = True
    for a, name in enumerate('xyz'):
        b = next(bb for bb in range(3) if R[bb][a] != 0)
        if not same(conj_op(SUBS[name], R, S), SUBS['xyz'[b]]):
            ok = False
    good += 1 if ok else 0
print('turns under which each sub-act goes exactly to the sub-act of the turned axis:', good, 'of 24')
for order in ('zyx', 'yxz', 'xzy', 'xyz', 'zxy', 'yzx'):
    Uo = tick(order)
    reach = sorted({off(x, y) for (x, i, y, j) in Uo})
    keep = [R for R, S in lifts if S is not None and same(conj_op(Uo, R, S), Uo)]
    n = len(keep)
    print('order', order, '(' + order[2] + ' first): reads', len(reach), 'offsets, largest L1', max(sum(abs(t) for t in o) for o in reach),
          '| commutes with', n, 'of 24 turns')
    if order == 'zyx':
        print('   the turns it commutes with (rows of the signed permutation matrix):', [[tuple(row) for row in R] for R in keep])

# controls (the probe must be able to pass): two operators that read only the six Spokes and are symmetric under the 24
def add_ops(*ops):
    out = {}
    for op in ops:
        for k, v in op.items():
            out[k] = out.get(k, ZERO) + v
    return {k: v for k, v in out.items() if not v.iszero()}
def star():
    op = {}
    for x in SITES:
        for a in range(3):
            for sign in (+1, -1):
                d = [0, 0, 0]; d[a] = -sign
                src = add_site(x, d)
                for i in range(2):
                    k = (x, i, src, i)
                    op[k] = op.get(k, ZERO) + ONE
    return op
for name, op in (('control 1, the star over the six Spokes (a scalar on the components)', star()),
                 ('control 2, the SUM of the three sub-acts (not their product)', add_ops(Wx, Wy, Wz))):
    reach = sorted({off(x, y) for (x, i, y, j) in op})
    n = sum(1 for R, S in lifts if S is not None and same(conj_op(op, R, S), op))
    print(name + ': reads', len(reach), 'offsets, largest L1', max(sum(abs(t) for t in o) for o in reach),
          '| Spokes read', sum(1 for o in reach if sum(abs(t) for t in o) == 1), '| commutes with', n, 'of 24 turns')
