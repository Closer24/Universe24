"""V6 (verifier A): the head's step written exactly (no carry, no rounding) on a ring, to test which charge it keeps.

At each Node-clock x: a Gaussian rational hand a, teeth w(x) = T X(x), stretch X(x), mesh rate mr(x), pawl frame
eps(x) in {1, -1}.  Each Mesh (x, y) has a symmetric S_xy, the grip at x is grip = mr(x)^2 S_xy (as rule3.gearing:
2 pinion p_i^2 Q_ij), the neighbour is read conjugated where f = eps_x eps_y = -1 (hands.seen), turned by the
offset's count n_xy = K_x - f K_y (meshes.offsets) and by a tangent triple of the odd count m_xy = -m_yx read with
no pawl (meshes.meshes_of's odd_sum).  The step: P' = P + X SUM grip (m - a) - X D a, a' = a + P' / w.
Charges: plain SUM W; framed SUM eps W; Q* = SUM eps w W / (X mr^2).  W = Im(conj(a_now) a_before).
Exact rationals: a change is a change, not a rounding.  python3 -I v6_toy_current.py
"""
import random
from fractions import Fraction as Fr

rng = random.Random(7)
N = 8


def mul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def conj(p):
    return (p[0], -p[1])


def unit(t):  # an exact unit complex from a rational t: ((1 - t^2), 2t) / (1 + t^2)
    d = 1 + t * t
    return ((1 - t * t) / d, 2 * t / d)


def Wof(now, before):
    return now[0] * before[1] - now[1] * before[0]


def run(walls, triple, ticks=30):
    X = [Fr(rng.randint(500, 1500)) for _ in range(N)]
    mr = [Fr(rng.randint(300, 1000)) for _ in range(N)]
    T = Fr(10 ** 7)
    w = [T * x for x in X]
    eps = [rng.choice((1, -1)) if walls else 1 for _ in range(N)]
    S = {}
    for x in range(N):
        S[(x, (x + 1) % N)] = S[((x + 1) % N, x)] = Fr(rng.randint(1, 9), 10 ** 6)
    K = [Fr(rng.randint(-3, 3), 11) for _ in range(N)]
    m = {}
    for x in range(N):
        v = Fr(rng.randint(-3, 3), 13) if triple else Fr(0)
        m[(x, (x + 1) % N)], m[((x + 1) % N, x)] = v, -v
    D = [Fr(rng.randint(0, 5)) for _ in range(N)]
    a = [(Fr(rng.randint(-99, 99)), Fr(rng.randint(-99, 99))) for _ in range(N)]
    b = [(p[0] + rng.randint(-9, 9), p[1] + rng.randint(-9, 9)) for p in a]
    P = [((a[x][0] - b[x][0]) * w[x], (a[x][1] - b[x][1]) * w[x]) for x in range(N)]

    def charges(a_, b_):
        Ws = [Wof(a_[x], b_[x]) for x in range(N)]
        return (sum(Ws), sum(eps[x] * Ws[x] for x in range(N)),
                sum(eps[x] * w[x] * Ws[x] / (X[x] * mr[x] ** 2) for x in range(N)))

    first = charges(a, b)
    moved = [0, 0, 0]
    for _ in range(ticks):
        newP = []
        for x in range(N):
            pull = (Fr(0), Fr(0))
            for y in ((x + 1) % N, (x - 1) % N):
                f = eps[x] * eps[y]
                seen = a[y] if f == 1 else conj(a[y])
                turned = mul(mul(unit(K[x] - f * K[y]), unit(m[(x, y)])), seen)
                g = mr[x] ** 2 * S[(x, y)]
                pull = (pull[0] + g * (turned[0] - a[x][0]), pull[1] + g * (turned[1] - a[x][1]))
            pull = (pull[0] - D[x] * a[x][0], pull[1] - D[x] * a[x][1])
            newP.append((P[x][0] + X[x] * pull[0], P[x][1] + X[x] * pull[1]))
        na = [(a[x][0] + newP[x][0] / w[x], a[x][1] + newP[x][1] / w[x]) for x in range(N)]
        before = charges(a, b)
        b, a, P = a, na, newP
        after = charges(a, b)
        for i in range(3):
            moved[i] += int(after[i] != before[i])
    return first, charges(a, b), moved


for walls, triple in ((False, False), (True, False), (False, True), (True, True)):
    first, last, moved = run(walls, triple)
    print(f"pawl walls {walls!s:5s}, triple turn {triple!s:5s}: ticks the charge moved of 30 -- plain {moved[0]:2d},"
          f" framed {moved[1]:2d}, Q* {moved[2]:2d};  Q* first {float(first[2]):.6g}, last {float(last[2]):.6g}")
