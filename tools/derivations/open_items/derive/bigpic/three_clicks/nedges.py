# Big Pic toy, pushed for the team at the Boss's ask (#2187 6538805478): the turn over n edge teeth at a place, sheared in a cycle; two takers sit on edges 0 and 1
import random, sys
import numpy as np
n = int(sys.argv[1]); D = 50811; R = 400000; c = (D - 1) // 2
def cen(v): return (v + c) % D - c
k = D // 50; xa, xb = 9 * k, 16 * k
def turn(u):
    u = list(u)
    for i in range(1, n): u[i] = cen(u[i] + u[i - 1])
    u[0] = cen(u[0] + u[n - 1])
    return u
M = np.zeros((n, n))
for j in range(n):
    e = [0] * n; e[j] = 1
    for i in range(1, n): e[i] = e[i] + e[i - 1]
    e[0] = e[0] + e[n - 1]
    M[:, j] = e
ev = sorted(abs(x) for x in np.linalg.eigvals(M))
rng = random.Random(31); u = [rng.randint(-c, c) for _ in range(n)]
A = []; B = []
for t in range(R):
    u = turn(u)
    qa, r = divmod(u[0] + c + xa, D); u[0] = r - c
    qb, r = divmod(u[1] + c + xb, D); u[1] = r - c
    A.append(qa); B.append(qb)
print("edges", n, "| det", round(np.linalg.det(M)), "| largest eigenvalue modulus %.3f, smallest %.3f" % (ev[-1], ev[0]))
for name, S in (("a", A), ("b", B)):
    p = sum(S) / len(S); out = []
    for m in (2, 3, 4):
        nn = sum(1 for i in range(m, len(S)) if all(S[i - j] for j in range(1, m + 1)))
        h = sum(1 for i in range(m, len(S)) if all(S[i - j] for j in range(1, m + 1)) and S[i])
        out.append("after %d in a row %d of %d (independent %.0f)" % (m, h, nn, nn * p))
    print("  taker", name, "p %.3f |" % p, "; ".join(out))
