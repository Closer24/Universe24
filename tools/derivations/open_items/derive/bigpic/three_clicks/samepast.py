# Big Pic toy, pushed for the team at the Boss's ask (#2187 6538805478): the law's reading for one clock: two lays alike in every click line before,
# apart by one unit in a tooth that no click line shows. Does a later click differ?
import random, sys
from fractions import Fraction
sys.argv = [sys.argv[0], "50811429", "1", "1", "1250"]
exec(open("turnteeth.py").read().split("rng = random.Random(31)")[0])
import numpy as np
M = np.zeros((3, 3), dtype=np.int64)
for j in range(3):
    e = [0, 0, 0]; e[j] = 1
    ga, ab, gb = e; ab = ab + ga; gb = gb - ab; ga = ga - gb   # the turn's matrix, read without the dial
    M[:, j] = [ga, ab, gb]
print("the turn's matrix (columns from ga, ab, gb):", M.tolist(), "det", round(np.linalg.det(M)), "| eigenvalue moduli:", sorted(round(abs(x), 4) for x in np.linalg.eigvals(M)))
def run(u, turned, T):
    out = []
    for t in range(T):
        u, qa, qb = step(u, xa, xb, turned)
        out.append((qa, qb))
    return out
rng = random.Random(7)
for turned in (1, 0):
    first = []; later_diff = 0; later_n = 0
    for trial in range(200):
        u0 = [rng.randint(-c, c) for _ in range(3)]
        u1 = list(u0); u1[1] = cen(u1[1] + 1)          # one unit in the takers' own side, which never clicks
        a = run(list(u0), turned, 3000); b = run(list(u1), turned, 3000)
        d = next((t for t in range(3000) if a[t] != b[t]), None)
        if d is not None: first.append(d)
        later_diff += sum(1 for t in range(1000, 3000) if a[t] != b[t]); later_n += 2000
    print("turned" if turned else "carried", "| lays apart by one hidden unit: a click differs in", len(first), "of 200 pairs;",
          ("first difference at round %d (median), after the same click past" % sorted(first)[len(first) // 2]) if first else "",
          "| rounds 1000 to 3000 differing: %.4f (independent takes would give %.4f)" % (later_diff / later_n, 1 - ((1 - xa / D) ** 2 + (xa / D) ** 2) * ((1 - xb / D) ** 2 + (xb / D) ** 2)))
