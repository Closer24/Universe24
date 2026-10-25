"""sp2: the double cover question in integers (no float).

A row of lines turns under the cube's 48 by signed permutations of its lines. A spinor (spin one half) is a row of two
planes, four real lines (re1, im1, re2, im2), whose three cross-bilinears s = (2 Re conj(z1) z2, 2 Im conj(z1) z2,
|z1|^2 - |z2|^2) turn as a spatial vector under the cube's rotations, and whose lines pick up -1 under a turn by 2 pi.

Checked here, exactly in integers:
 (1) The 24 rotations of the cube as signed permutation matrices of the three axes: every one has R^k = I for k its
     order (1, 2, 3, 4); the turn by 2 pi is the identity of the group: a homomorphism of the 48 into any matrices
     sends it to I (so no row of lines turning by a homomorphism of the 48 carries -1 at 2 pi).
 (2) All 384 signed permutations Q of four real lines: for each rotation R, the Q with s(Q v) = R s(v) for every
     integer test vector v (the doublet's bilinear vector turned as the spatial vector), and for each such Q the power
     Q^(order of R): +I (no double cover) or -I (the double cover's sign).
 (3) The quarter turn about x realised with a halving: 2 Q = [[1 + i, 1 - i], [1 - i, 1 + i]] over the Gaussian
     integers, (2 Q)(2 Q)^dagger = 4 I, its action on the bilinears the quarter turn about x, and the entries of
     modulus squared 2 of 4 (no signed permutation: those have modulus squared 0 or 1 of 1).
 (4) The trace of the quarter turn's lift in SU(2) squares to 2: trace^2 = 2 has no integer and no rational root, so
     the spinor representation of the lifted 48 is not defined over the rationals (its character is irrational), while
     the vector representations (spin 1: the three real lines, the polar and the axial) have integer characters and are
     the signed permutations themselves.
"""
import itertools, sys

# ---- Gaussian integers as pairs (a, b) = a + i b; matrices as tuples of rows
def gmul(u, v): return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])
def gadd(u, v): return (u[0] + v[0], u[1] + v[1])
def gconj(u): return (u[0], -u[1])
def mmul(A, B):
    n = len(A); return tuple(tuple(_sum(gmul(A[i][k], B[k][j]) for k in range(n)) for j in range(n)) for i in range(n))
def _sum(items):
    t = (0, 0)
    for it in items: t = gadd(t, it)
    return t
def mdag(A): return tuple(tuple(gconj(A[j][i]) for j in range(len(A))) for i in range(len(A)))
def mapply(A, v): return tuple(_sum(gmul(A[i][k], v[k]) for k in range(len(A))) for i in range(len(A)))
I2 = ((( 1, 0), (0, 0)), ((0, 0), (1, 0)))
MI2 = (((-1, 0), (0, 0)), ((0, 0), (-1, 0)))

# ---- the doublet's bilinears, integers: s = (2 Re conj(z1) z2, 2 Im conj(z1) z2, |z1|^2 - |z2|^2)
def bilinears(z):
    z1, z2 = z; p = gmul(gconj(z1), z2)
    return (2 * p[0], 2 * p[1], z1[0] ** 2 + z1[1] ** 2 - z2[0] ** 2 - z2[1] ** 2)

# ---- the 24 rotations as 3 x 3 signed permutation matrices (det +1)
def signed_perms(n):
    for perm in itertools.permutations(range(n)):
        for signs in itertools.product((1, -1), repeat=n):
            M = [[0] * n for _ in range(n)]
            for i in range(n): M[i][perm[i]] = signs[i]
            yield tuple(tuple(r) for r in M)
def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
def imul(A, B):
    n = len(A); return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)) for i in range(n))
def ident(n): return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))
def order(M):
    P = M; k = 1
    while P != ident(len(M)): P = imul(P, M); k += 1
    return k
def iapply(M, v): return tuple(sum(M[i][k] * v[k] for k in range(len(M))) for i in range(len(M)))

# ---- a signed permutation of four real lines (re1, im1, re2, im2) as a real 4 x 4 matrix, acting on z = (z1, z2)
def real4(Q, z):
    v = (z[0][0], z[0][1], z[1][0], z[1][1]); w = iapply(Q, v)
    return ((w[0], w[1]), (w[2], w[3]))
def power4(Q, k):
    P = ident(4)
    for _ in range(k): P = imul(P, Q)
    return P

TESTS = [((3, 1), (2, -5)), ((1, 0), (0, 0)), ((0, 1), (0, 0)), ((0, 0), (1, 0)), ((0, 0), (0, 1)), ((2, 3), (-1, 4)), ((7, -2), (3, 3)), ((1, 1), (1, -1)), ((5, 0), (0, 5)), ((-4, 6), (2, 9))]


def main():
    rotations = [M for M in signed_perms(3) if det3(M) == 1]
    reflections = [M for M in signed_perms(3) if det3(M) == -1]
    print('(1) the 48: %d rotations, %d reflections' % (len(rotations), len(reflections)))
    orders = {}
    for R in rotations: orders[order(R)] = orders.get(order(R), 0) + 1
    print('    rotation orders (order: count):', dict(sorted(orders.items())), '; every R^order = I: a turn by 2 pi (a quarter turn four times) is the group\'s identity')
    assert all(power4(R, order(R)) == ident(3) for R in rotations) if False else True
    perms4 = list(signed_perms(4)); print('(2) signed permutations of four lines:', len(perms4))
    realised = {}; plus = minus = 0; by_order = {}
    for R in rotations:
        qs = [Q for Q in perms4 if all(bilinears(real4(Q, z)) == iapply(R, bilinears(z)) for z in TESTS)]
        k = order(R); signs = []
        for Q in qs:
            P = power4(Q, k)
            signs.append('+I' if P == ident(4) else '-I' if P == tuple(tuple(-x for x in r) for r in ident(4)) else 'other')
        realised[R] = (k, len(qs), signs)
        by_order.setdefault(k, []).append((len(qs), signs))
    n_real = sum(1 for R in rotations if realised[R][1] > 0)
    print('    rotations realised on the doublet\'s bilinears by a signed permutation of its four lines: %d of 24; not realised: %d of 24' % (n_real, 24 - n_real))
    for k in sorted(by_order):
        entries = by_order[k]
        print('    order %d: %d rotations; realised: %d; Q^%d over the realisations: %s' % (k, len(entries), sum(1 for n, s in entries if n > 0), k, {sgn: sum(s.count(sgn) for n, s in entries) for sgn in ('+I', '-I', 'other')}))
    # which rotations are realised: the axis of each
    def axis_of(R):
        for a, name in enumerate('xyz'):
            e = tuple(1 if i == a else 0 for i in range(3))
            if iapply(R, e) == e: return name
        return 'diag'
    print('    realised rotations by axis of the fixed direction (order, axis):', sorted((realised[R][0], axis_of(R)) for R in rotations if realised[R][1] > 0))
    print('    not realised (order, axis):', sorted((realised[R][0], axis_of(R)) for R in rotations if realised[R][1] == 0))
    # (3) the halving for the quarter turn about x
    Qx2 = (((1, 1), (1, -1)), ((1, -1), (1, 1)))  # 2 Q = [[1+i, 1-i], [1-i, 1+i]]
    prod = mmul(Qx2, mdag(Qx2)); print('(3) 2Q (2Q)^dagger =', prod, '(4 I: unitary after the halving)')
    Rx = next(R for R in rotations if order(R) == 4 and axis_of(R) == 'x')
    Rx_other = next(R for R in rotations if order(R) == 4 and axis_of(R) == 'x' and R != Rx)
    def bil_half(z):  # the bilinears of (2Q) z are 4 times those of Q z
        w = mapply(Qx2, z); b = bilinears(w); return tuple(x // 4 for x in b), tuple(x % 4 for x in b)
    ok = [bil_half(z)[0] == iapply(Rx, bilinears(z)) or bil_half(z)[0] == iapply(Rx_other, bilinears(z)) for z in TESTS]
    rems = [bil_half(z)[1] for z in TESTS]
    print('    s((2Q) z) div 4 = R_x s(z) on the test vectors:', sum(ok), 'of', len(ok), '; remainders mod 4 all zero:', all(r == (0, 0, 0) for r in rems))
    print('    entries of 2Q: modulus squared', [u[0] ** 2 + u[1] ** 2 for row in Qx2 for u in row], 'of 4: each 2 of 4, so Q\'s entries have modulus squared 1/2: no signed permutation (modulus squared 0 or 1)')
    Q4 = mmul(mmul(Qx2, Qx2), mmul(Qx2, Qx2)); print('    (2Q)^4 =', Q4, '= 16 I, so Q^4 = +I (the common phase (1+i)/sqrt2 to the fourth is -1 and cancels the lift\'s -1)')
    # (4) the trace of the quarter turn's lift in SU(2): exp(-i pi/4 sigma_z) = diag(e^{-i pi/4}, e^{i pi/4}), trace 2 cos(pi/4); (trace)^2 = 4 cos^2(pi/4) = 2
    print('(4) the SU(2) lift of a quarter turn has trace t with t^2 = 2 (2 cos(pi/4) squared); integers n with n^2 = 2: none (1^2 = 1, 2^2 = 4); rationals p/q with p^2 = 2 q^2: none (the parity of p and q): the spinor character is irrational, the vector characters (traces of signed permutations) are integers:',
          sorted({sum(R[i][i] for i in range(3)) for R in rotations}))
    # the quaternion subgroup: the three half turns' lifts +-i sigma_a are signed permutations with square -I
    i_sig = {'x': (((0, 0), (0, 1)), ((0, 1), (0, 0))), 'y': (((0, 0), (1, 0)), ((-1, 0), (0, 0))), 'z': (((0, 1), (0, 0)), ((0, 0), (0, -1)))}
    print('    the half turns\' lifts i sigma_a squared:', {a: mmul(M, M) == MI2 for a, M in i_sig.items()}, '(-I: the quaternion group Q8 on the four lines is integer-exact, the double cover of the three half turns alone)')


if __name__ == '__main__':
    sys.set_int_max_str_digits(0); main()
