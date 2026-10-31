"""Four turned teeth, two carrying (g1, g2: kept by the mirror, their passings negated, the click tooth's rule) and two hidden
(t1, t2: flipped by the mirror, the drive's rule): every palindrome of k 4 or 5 shears between the classes, its linear part L
between two rounds' carries (L reversible under the mirror diag(1, 1, -1, -1)), det(L - I) and det(L + I) (no kept direction
where both are not 0) and the trace. In odd dimension a reversible L keeps a direction (its eigenvalues pair as x, 1/x), as the
triangle's three teeth show (g1 - g2 kept by every three-tooth palindrome found). Whole numbers only."""
from itertools import product
N = 4
SH = {}
for a in (2, 3):
    for g in (0, 1):
        for sg in (1, -1):
            SH[f"t{a - 1}{'+' if sg > 0 else '-'}=g{g + 1}"] = (a, g, sg)
            SH[f"g{g + 1}{'+' if sg > 0 else '-'}=t{a - 1}"] = (g, a, sg)
def mat(seq):
    cols = []
    for e in range(N):
        v = [int(i == e) for i in range(N)]
        for nm in seq:
            i, j, sg = SH[nm]
            v[i] = v[i] + sg * v[j]
        cols.append(v)
    return [[cols[c][r] for c in range(N)] for r in range(N)]
def det(A):
    A = [row[:] for row in A]; n = len(A)
    if n == 1: return A[0][0]
    return sum((-1) ** c * A[0][c] * det([row[:c] + row[c + 1:] for row in A[1:]]) for c in range(n))
def tr(A): return sum(A[i][i] for i in range(N))
I = [[int(i == j) for j in range(N)] for i in range(N)]
found = []
for k in range(4, 6):
    for seq in product(list(SH), repeat=k):
        if any(SH[seq[i]][0] == SH[seq[i + 1]][0] for i in range(k - 1)):
            continue
        if len({SH[nm][0] for nm in seq}) < N:
            continue
        L = mat(list(reversed(seq)) + list(seq))
        d1 = det([[L[i][j] - I[i][j] for j in range(N)] for i in range(N)])
        d2 = det([[L[i][j] + I[i][j] for j in range(N)] for i in range(N)])
        if d1 == 0 or d2 == 0:
            continue
        found.append((k, abs(tr(L)), seq, L, det(L), d1, d2))
found.sort(key=lambda z: (z[0], z[1]))
print("four-tooth palindromes of k 4 or 5 shears moving every tooth, keeping no direction (det(L - I) and det(L + I) not 0):", len(found))
for z in found[:8]:
    print("  k", z[0], "|trace|", z[1], "shears", z[2], "L", z[3], "det", z[4], "det(L-I)", z[5], "det(L+I)", z[6])
def trace2(L): return sum(L[i][j] * L[j][i] for i in range(N) for j in range(N))
both = []
for z in found:
    L = z[3]; a = tr(L); b = (a * a - trace2(L)) // 2
    disc = a * a - 4 * (b - 2); p2 = b - 2 * a + 2; pm2 = b + 2 * a + 2
    hyp = disc > 0 and ((p2 > 0 and pm2 > 0 and abs(a) > 4) or (p2 < 0 and pm2 < 0))
    if hyp:
        both.append((z[0], max(abs(x) for row in L for x in row), a, b, z[2], L))
both.sort(key=lambda w: (w[0], w[1]))
print("both pairs hyperbolic (x + 1/x = y, y^2 - tr y + (b - 2) = 0, both |y| > 2):", len(both))
for w in both[:6]:
    print("  k", w[0], "largest entry", w[1], "trace", w[2], "b", w[3], "shears", w[4], "L", w[5])
