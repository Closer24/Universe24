"""The third click's turn read as a whole-number matrix, on the structure alone (no dial, no run): for each palindrome
form, the round's linear turn L (the forward shears, then the backward ones, the carries between them adding nothing
to the twins), and three laws read exactly:
- the mirror: R L R L = I, R keeping the edge teeth and flipping the twins (the board's run back by the same act);
- the label rule: P L = L P, P the swap of the two trains alike in kinds, the alike pair's own edge read from its other
  end (its tooth and twin negated);
- no direction kept: det(L - I) and det(L + I), and for the two parts of C C^T the turn as a polynomial in K,
  L = [[I + 2 K^2, 2 K], [2 K + 2 K^3, I + 2 K^2]], so each eigenvalue kappa of K gives a pair of trace 2 + 4 kappa^2.

Usage: python3 -I kturn.py <src> [world]
"""
import sys

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402

world_dir = sys.argv[2] if len(sys.argv) > 2 else "tensor24-click"
universe, shape, held, lay, s, world = E.load_world(sys.argv[1], world_dir)
kinds_of = [t["kinds"] for t in universe["trains"]]
ed = E.Edges(world, 1, 1, kinds_of)
n = len(ed.pairs)
N = 2 * n


def eye(m):
    return [[int(i == j) for j in range(m)] for i in range(m)]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b, sb=1):
    return [[a[i][j] + sb * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def at(kind, i):
    return i if kind == "g" else n + i


def of(order):
    m = eye(N)
    for (dk, di), (sk, si), sign in order:
        sh = eye(N)
        sh[at(dk, di)][at(sk, si)] += sign
        m = mul(sh, m)
    return m


def det(a):
    """Bareiss's fraction-free elimination: every division exact, taken by the carry with its remainder 0."""
    a = [row[:] for row in a]
    m, sign, prev = len(a), 1, 1
    for k in range(m - 1):
        if a[k][k] == 0:
            swap = next((i for i in range(k + 1, m) if a[i][k]), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign = -sign
        for i in range(k + 1, m):
            for j in range(k + 1, m):
                q, r = carry(a[i][j] * a[k][k] - a[i][k] * a[k][j], prev, 0)
                assert r == 0
                a[i][j] = q
        prev = a[k][k]
    return sign * a[m - 1][m - 1]


alike = [t for t in world.trains if sum(1 for u in world.trains if kinds_of[u] == kinds_of[t]) == 2]
p, q = alike
swap_t = {t: t for t in world.trains}
swap_t[p], swap_t[q] = q, p
P = [[0] * N for _ in range(N)]
for e, (u, v) in enumerate(ed.pairs):
    su, sv = swap_t[u], swap_t[v]
    f, sign = (ed.index[(su, sv)], 1) if su < sv else (ed.index[(sv, su)], -1)
    P[f][e] = P[n + f][n + e] = sign
R = [[int(i == j) * (1 if i < n else -1) for j in range(N)] for i in range(N)]
print(f"{world_dir}: edges {ed.pairs}, triangles {ed.triangles}, the alike trains {alike}; C C^T = {ed.cc}")
for mode in (2, 3, 4, 5):
    L = mul(of(ed.backward(mode)), of(ed.forward(mode)))
    mirror = mul(mul(R, mul(L, R)), L) == eye(N)
    label = mul(P, L) == mul(L, P)
    dm, dp = det(add(L, eye(N), -1)), det(add(L, eye(N)))
    print(f"  {E.NAMES[mode]}: trace {sum(L[i][i] for i in range(N))}; the mirror R L R L = I: {mirror};"
          f" the label rule P L = L P: {label}; det(L - I) {dm}, det(L + I) {dp}")


def charpoly(a):
    """Faddeev and LeVerrier's recursion, each division exact by the carry: the coefficients of det(x I - a), the
    highest first."""
    m = len(a)
    c, mk = [1], [[0] * m for _ in range(m)]
    for k in range(1, m + 1):
        mk = add(mul(a, mk), [[c[-1] * x for x in row] for row in eye(m)])
        q, r = carry(-sum(mul(a, mk)[i][i] for i in range(m)), k, 0)
        assert r == 0
        c.append(q)
    return c


def whole_roots(c):
    """The whole roots of the polynomial, each as often as it divides it: every whole root divides the last
    coefficient, so the search is over the divisors alone."""
    out, c = [], list(c)
    while c[-1] == 0 and len(c) > 1:
        out.append(0)
        c = c[:-1]
    for r in sorted({d for d in range(1, abs(c[-1]) + 1) if carry(c[-1], d, 0)[1] == 0} | set()):
        for root in (r, -r):
            while len(c) > 1:
                acc, quot = 0, []
                for x in c:
                    acc = acc * root + x
                    quot.append(acc)
                if quot[-1] != 0:
                    break
                out.append(root)
                c = quot[:-1]
    return sorted(out), c


for name, mode, k in (("off its diagonal", 4, ed.kcoup), ("its diagonal", 5, ed.kdiag)):
    two_k2 = [[2 * x for x in row] for row in mul(k, k)]
    two_k = [[2 * x for x in row] for row in k]
    top = add(eye(n), two_k2)
    low = add(two_k, mul(two_k2, k))
    blockform = [ra + rb for ra, rb in zip(top, two_k)] + [ra + rb for ra, rb in zip(low, top)]
    L = mul(of(ed.backward(mode)), of(ed.forward(mode)))
    cp = charpoly(k)
    roots, rest = whole_roots(cp)
    print(f"  C C^T {name} (mode {mode}): K = {k}; L is the polynomial form in K: {L == blockform}; det(x I - K) has the"
          f" coefficients {cp}, whole roots {roots} (left over {rest}), so the pairs' traces 2 + 4 kappa^2 are"
          f" {[2 + 4 * r * r for r in roots]}: {'every one above 2, no direction kept' if rest == [1] and all(r for r in roots) else 'not every direction turned'}")
cp = charpoly(ed.cc)
print(f"  C C^T itself: det(x I - C C^T) has the coefficients {cp}, whole roots {whole_roots(cp)[0]}: its zero roots are the"
      f" directions its palindrome would keep unturned")
