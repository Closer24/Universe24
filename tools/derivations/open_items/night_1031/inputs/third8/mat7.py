"""THIRD7's matrices, exact over the integers (no dial, no run), for the click world's triangle: the clocks held 2,
giver 3, taker 4 and the edges in Big Pic's index order ga = (2, 3), gb = (2, 4), ab = (3, 4). Whole numbers only.
1. B, the edges' incidence on the clocks (+1 at an edge's first train, -1 at its second), and c, the triangle's
   boundary on the edges (ga +1, ab +1, gb -1): B c = 0; rank B = 2, so ker B is c's line (the lemma's ground);
2. G = c^T c = C^T C, and the split E = G I - c c^T: c^T E = 0, B E = G B, E E = G E, E + c c^T = G I;
3. the triangle's pair (tau kept, eta flipped) at K = G: the round's L between carries, its trace and det, det(L - I),
   det(L + I), and the mirror R L R L = I;
4. the full C C^T on the circulation: C C^T c = G c, so its palindrome (Big Pic's mode 8, h += C C^T g, g += C C^T h)
   restricted to g = alpha c, h = beta c is the pair at K = G; and C C^T reads the twins only through c^T h;
5. the swap P (giver with taker): P c = -c, P E = E P, B's rows exchanged;
6. a lone edge at the dial G D with its passing G x, born (G D - 1) div 2, is the first click at D exactly, tooth for
   tooth (r -> G r + (G - 1) div 2), checked over every tooth and a range of passings at a small odd dial, and at the
   click world's dial on a sample.
argv: none (the small dials are a reading's own)."""
import sys
from pathlib import Path

S = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(S.joinpath("third6_frozen", "c5n", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

EDGES = [(2, 3), (2, 4), (3, 4)]
CLOCKS = [2, 3, 4]
B = [[(1 if e[0] == v else -1) if v in e else 0 for e in EDGES] for v in CLOCKS]
c = [1, -1, 1]  # ga +1, gb -1, ab +1 in the index order


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def col(v):
    return [[z] for z in v]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def add(a, b, s=1):
    return [[a[i][j] + s * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for cc in range(len(a[0])):
        piv = next((i for i in range(r, len(a)) if a[i][cc]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        for i in range(len(a)):
            if i != r and a[i][cc]:
                x, y = a[i][cc], a[r][cc]
                a[i] = [p * y - q * x for p, q in zip(a[i], a[r])]
        r += 1
    return r


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


print(f"1. B (rows the clocks {CLOCKS}, columns the edges {EDGES}) = {B}; c = {c}; B c = {[r[0] for r in mul(B, col(c))]};"
      f" rank B = {rank(B)}, so ker B is c's line: a change of the edges' content that keeps every clock's total is a"
      f" multiple of c")
G = sum(z * z for z in c)
cct = [[ci * cj for cj in c] for ci in c]
E = add([[G * z for z in row] for row in eye(3)], cct, -1)
print(f"2. G = c^T c = {G}; E = G I - c c^T = {E}; c^T E = {mul([c], E)[0]}; B E = G B: {mul(B, E) == [[G * z for z in r] for r in B]};"
      f" E E = G E: {mul(E, E) == [[G * z for z in r] for r in E]}; E + c c^T = G I: {add(E, cct) == [[G * z for z in r] for r in eye(3)]}")
K = G
A = [[1, 0], [K, 1]]  # eta += K tau (coordinates (tau, eta))
Bs = [[1, K], [0, 1]]  # tau += K eta
F = mul(Bs, A)  # the first half: eta first, then tau
Rv = mul(A, Bs)  # the reversed half: tau first, then eta
L = mul(F, Rv)
Rm = [[1, 0], [0, -1]]
print(f"3. the pair at K = G = {K}: the first half {F}, the reversed {Rv}; L = {L}: trace {L[0][0] + L[1][1]}, det {det2(L)},"
      f" det(L - I) {det2(add(L, eye(2), -1))}, det(L + I) {det2(add(L, eye(2)))}; the mirror R L R L = I:"
      f" {mul(mul(Rm, mul(L, Rm)), L) == eye(2)}")
ccc = mul(cct, col(c))
print(f"4. C C^T c = {[r[0] for r in ccc]} = G c: {[r[0] for r in ccc] == [G * z for z in c]}; on g = alpha c, h = beta c,"
      f" h += C C^T g gives beta += {G} alpha and g += C C^T h gives alpha += {G} beta: the pair at K = G; (C C^T h)_e ="
      f" c_e (c^T h) for every h: {all(mul(cct, col(h))[e][0] == c[e] * sum(ci * hi for ci, hi in zip(c, h)) for h in ([1, 0, 0], [0, 1, 0], [0, 0, 1], [2, -3, 5]) for e in range(3))}")
# mode 8 on six teeth (g_ga, g_gb, g_ab, h_ga, h_gb, h_ab): the half h += C C^T g, then g += C C^T h
N = 6
def shear6(dst_block, src_block):
    m = eye(N)
    for i in range(3):
        for j in range(3):
            m[dst_block * 3 + i][src_block * 3 + j] += cct[i][j]
    return m
half8 = mul(shear6(0, 1), shear6(1, 0))
rev8 = mul(shear6(1, 0), shear6(0, 1))
L8 = mul(half8, rev8)
v = c + [0, 0, 0]
w = [0, 0, 0] + c
Lv = [r[0] for r in mul(L8, col(v))]
Lw = [r[0] for r in mul(L8, col(w))]
print(f"   mode 8's round on (g, h): L8 c_g = {Lv}, L8 c_h = {Lw}: on the plane (c_g, c_h) it is"
      f" [[{Lv[0]}, {Lw[0]}], [{Lv[3]}, {Lw[3]}]] against the pair's L {L}; L8 on c's complement (g and h both"
      f" orthogonal to c) is the identity: {all(mul(L8, col(u))[i][0] == u[i] for u in ([1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0], [1, 0, -1, 0, 0, 0], [0, 0, 0, 1, 0, -1]) for i in range(N))}")
P = [[0, 1, 0], [1, 0, 0], [0, 0, -1]]  # the swap on the edges: ga <-> gb, ab read from its other end
print(f"5. the swap P = {P}: P c = {[r[0] for r in mul(P, col(c))]} (= -c); P E = E P: {mul(P, E) == mul(E, P)};"
      f" P c c^T = c c^T P: {mul(P, cct) == mul(cct, P)}")
# 6. the lone edge's embedding, exhaustively at a small odd dial, and on a sample at the click world's
bad = 0
n = 0
for Dd in (7, 9, 15):
    Bd = carry(Dd - 1, 2, 0)[0]
    D3 = G * Dd
    B3 = carry(D3 - 1, 2, 0)[0]
    for x in range(-60, 61):
        for r in range(Dd):
            q1, r1 = carry(x, Dd, r)
            q3, r3 = carry(G * x, D3, G * r + carry(G - 1, 2, 0)[0])
            bad += int(q1 != q3 or r3 != G * r1 + carry(G - 1, 2, 0)[0])
            n += 1
    assert B3 == G * Bd + carry(G - 1, 2, 0)[0]
Dw = 3 * 50811429
Bw = carry(Dw - 1, 2, 0)[0]
seed = 17
for _ in range(20000):
    seed = carry(seed * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)[1]
    x = carry(seed, 4 * Dw, 0)[1] - 2 * Dw
    seed = carry(seed * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)[1]
    r = carry(seed, Dw, 0)[1]
    q1, r1 = carry(x, Dw, r)
    q3, r3 = carry(G * x, G * Dw, G * r + carry(G - 1, 2, 0)[0])
    bad += int(q1 != q3 or r3 != G * r1 + carry(G - 1, 2, 0)[0])
    n += 1
print(f"6. a lone edge at G D with G x against the first click at D, tooth r <-> G r + (G - 1) div 2: {bad} of {n} carries"
      f" apart (dials 7, 9, 15 exhaustively over x in -60..60; the click world's D = {Dw} on 20,000 stand-in draws); the"
      f" births agree: G B + (G - 1) div 2 = {G * Bw + carry(G - 1, 2, 0)[0]} against (G D - 1) div 2 = {carry(G * Dw - 1, 2, 0)[0]}")
