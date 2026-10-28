"""David's probe for M1's U_j on Z[i]: the Mesh's turn read from its two ends, Hermitian bit for bit through the pawl.

usage: python3 -I p5_link.py   (no worktree needed)
The link of the Mesh from x to its neighbour y across Spoke j (side_j = +1 on +j, -1 on -j):
  f = eps_x eps_y (the pawls agree +1, differ -1), n = side_j (A_x + f A_y) (QR1), u = T + i n,
  the read U a_y = u K^f(a_y) / T, K^f the conjugation where the pawls differ; T the Mesh's teeth, a run integer.
The pull times T: (L a)_x = sum_j g_xj (u_xj K^f(a_y) - T a_x), g read the same from both ends.
Checks (exact integers and exact rationals):
  (1) L symmetric for the real pairing Re<b, L a> = Re<a, L b> (the wind's metric kept: law 2), 2,000 boards;
  (2) L commutes with the framed quarter turn a_x -> i^eps_x a_x (Noether's symmetry), 2,000 boards;
  (3) the rational leapfrog w (a+ - 2a + a-) = s L a / T keeps C = <a-, i eps a> exactly, 200 boards x 40 ticks;
  (4) mutants: the triple summed with no pawl, n = side (A_x + A_y), fails (1) to (3) on boards with a pawl wall;
      the far end read without K fails them too;
  (5) the neutral train, n = 0: u = T, U = 1 exactly, the plain Laplacian (stage 4's light).
"""
import random
from fractions import Fraction

rng = random.Random(1028)
SIDE = 4
SITES = [(x, y, z) for x in range(SIDE) for y in range(SIDE) for z in range(SIDE)]
INDEX = {s: k for k, s in enumerate(SITES)}
SPOKES = [(ax, sd) for ax in range(3) for sd in (1, -1)]


def nb(k, j):
    ax, sd = SPOKES[j]
    s = list(SITES[k])
    s[ax] = (s[ax] + sd) % SIDE
    return INDEX[tuple(s)]


NB = [[nb(k, j) for j in range(6)] for k in range(len(SITES))]


def mul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def conj(z):
    return (z[0], -z[1])


def board(wall=True):
    n = len(SITES)
    eps = [1 - 2 * (rng.random() < 0.5) if wall else 1 for _ in range(n)]
    A = [rng.randint(-50, 50) for _ in range(n)]
    g = {}
    for k in range(n):
        for j in (0, 2, 4):
            v = rng.randint(1, 9)
            g[(k, j)] = v
            g[(NB[k][j], j + 1)] = v  # the same grip read from both ends
    T = rng.randint(1, 60)
    return eps, A, g, T


def L(a, eps, A, g, T, mode="law"):
    out = []
    for k in range(len(SITES)):
        acc = (0, 0)
        for j in range(6):
            y = NB[k][j]
            side = SPOKES[j][1]
            f = eps[k] * eps[y]
            n = side * (A[k] + (f if mode != "nopawl" else 1) * A[y])
            u = (T, n)
            far = a[y] if (f == 1 or mode == "noK") else conj(a[y])
            t = mul(u, far)
            acc = (acc[0] + g[(k, j)] * (t[0] - T * a[k][0]), acc[1] + g[(k, j)] * (t[1] - T * a[k][1]))
        out.append(acc)
    return out


def rpair(b, a):
    return sum(x[0] * y[0] + x[1] * y[1] for x, y in zip(b, a))


def hands():
    return [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in SITES]


def turn(a, eps):
    return [((-z[1], z[0]) if e == 1 else (z[1], -z[0])) for z, e in zip(a, eps)]


res = {}
for mode in ("law", "nopawl", "noK"):
    sym = com = 0
    for _ in range(2000 if mode == "law" else 300):
        eps, A, g, T = board()
        a, b = hands(), hands()
        sym += rpair(b, L(a, eps, A, g, T, mode)) != rpair(a, L(b, eps, A, g, T, mode))
        com += L(turn(a, eps), eps, A, g, T, mode) != turn(L(a, eps, A, g, T, mode), eps)
    keep = 0
    boards = 200 if mode == "law" else 40
    for _ in range(boards):
        eps, A, g, T = board()
        w, s = rng.randint(50, 400), 1
        prev = [(Fraction(x), Fraction(y)) for x, y in hands()]
        now = [(Fraction(x), Fraction(y)) for x, y in hands()]
        def charge(prev, now):
            return sum(e * (p[0] * q[1] - p[1] * q[0]) for e, p, q in zip(eps, prev, now))
        c0, moved = charge(prev, now), False
        for _ in range(40):
            la = L(now, eps, A, g, T, mode)
            nxt = [(2 * q[0] - p[0] + Fraction(s * l[0], w * T), 2 * q[1] - p[1] + Fraction(s * l[1], w * T))
                   for p, q, l in zip(prev, now, la)]
            prev, now = now, nxt
            moved |= charge(prev, now) != c0
        keep += moved
    res[mode] = (sym, com, keep, 2000 if mode == "law" else 300, boards)

for mode, (sym, com, keep, n, b) in res.items():
    print(f"{mode:7s}: (1) L not symmetric on {sym} of {n} boards; (2) not commuting with the framed quarter turn on {com} of {n};"
          f" (3) the charge moved on {keep} of {b} boards over 40 ticks")

# (5) the neutral train
eps, A, g, T = board(wall=False)
A0 = [0] * len(SITES)
a = hands()
plain = [(sum(g[(k, j)] * (a[NB[k][j]][0] - a[k][0]) for j in range(6)) * T,
          sum(g[(k, j)] * (a[NB[k][j]][1] - a[k][1]) for j in range(6)) * T) for k in range(len(SITES))]
print("(5) n = 0: the pull is T times the plain Laplacian at every site:", L(a, eps, A0, g, T) == plain)
