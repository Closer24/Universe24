# Probe for RULING items 1, 7, 8: object arrays at 112+ bits; nonneg against the plan's whether; the rank count.
import numpy as np, itertools, random
print('numpy', np.__version__)
big = (1 << 112) + 12345
a = np.array([big, -big, 7, -7], dtype=object); d = np.array([3, 3, 5, 5], dtype=object)
q = a // d; r = a - q * d
print('carry exact on 112-bit object arrays:', all(int(q[i]) * int(d[i]) + int(r[i]) == int(a[i]) and 0 <= r[i] < d[i] for i in range(4)))
i64 = np.array([1 << 62], dtype=np.int64); print('int64 wraps silently:', (i64 * 4)[0])
M = np.array([[big, 1], [2, -big]], dtype=object); v = np.array([big, 3], dtype=object)
try:
    e = np.einsum('ij,j->i', M, v); print('einsum on object arrays:', e[0] == big * big + 3)
except Exception as ex: print('einsum on object arrays FAILS:', type(ex).__name__, ex)
acc = np.zeros(3, dtype=object); np.add.at(acc, np.array([0, 2, 0]), np.array([big, 1, big], dtype=object))
print('scatter-add (add.at) on object arrays:', acc[0] == 2 * big, acc.dtype)
nonneg = lambda n: 1 + n // (n * n + 1)
whether = lambda q: 1 - 1 // (q + 1)
print('nonneg exact on -50..50:', all(nonneg(n) == (1 if n >= 0 else 0) for n in range(-50, 51)))
bad = []
for qq in (-3, -2, 0, 1, 5):
    try: bad.append((qq, whether(qq)))
    except ZeroDivisionError: bad.append((qq, 'ZeroDivisionError'))
print("plan's whether(q) = 1 - 1 div (q+1) on q = -3,-2,0,1,5:", bad)
# the draw's 'in the order of their values' as a rank count: sums of nonneg bits, no sort, no loop in the act
def ranked_compose(v, place):
    v = np.array(v, dtype=object); n = len(v)
    D = v[None, :] - v[:, None]                      # D[i, j] = v_j - v_i
    less = 1 - np.vectorize(nonneg, otypes=[object])(D)          # v_j < v_i
    eq = np.vectorize(nonneg, otypes=[object])(D) * np.vectorize(nonneg, otypes=[object])(-D)
    tri = np.array([[1 if j < i else 0 for j in range(n)] for i in range(n)], dtype=object)  # layout, built at load
    rank = (less + eq * tri).sum(axis=1)
    P = np.vectorize(lambda x: nonneg(x) * nonneg(-x), otypes=[object])(np.arange(n, dtype=object)[:, None] - rank[None, :])
    return int((np.array(place, dtype=object) * (P @ v)).sum())
ok = True
for _ in range(300):
    n = random.randint(1, 7); v = [random.randint(-4, 9) for _ in range(n)]; place = [11 ** k for k in range(n)]
    ok &= ranked_compose(v, place) == sum(p * x for p, x in zip(place, sorted(v)))
    ok &= ranked_compose(random.sample(v, n), place) == ranked_compose(v, place)
print('rank-count composition equals the sorted composition and is order-free (300 draws):', ok)
