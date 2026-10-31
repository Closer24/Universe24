import sys
which = sys.argv[1]
sys.argv = [sys.argv[0], "50811", "400000", "1", "50"]
src = open(which).read().split("rng = random.Random(31)")[0]
exec(src)
import random
rng = random.Random(31)
u = [rng.randint(-c, c) for _ in range(3)]
A = []; B = []
for t in range(400000):
    u, qa, qb = step(u, xa, xb); A.append(qa); B.append(qb)
for name, S in (("a", A), ("b", B)):
    p = sum(S) / len(S)
    for m in (2, 3, 4):
        n = sum(1 for i in range(m, len(S)) if all(S[i - j] for j in range(1, m + 1)))
        h = sum(1 for i in range(m, len(S)) if all(S[i - j] for j in range(1, m + 1)) and S[i])
        # and after m rounds with no click
        n0 = sum(1 for i in range(m, len(S)) if not any(S[i - j] for j in range(1, m + 1)))
        h0 = sum(1 for i in range(m, len(S)) if not any(S[i - j] for j in range(1, m + 1)) and S[i])
        print("%s %s: after %d clicks in a row, a click %d of %d (independent %.0f); after %d silent rounds, %d of %d (independent %.0f)" % (which, name, m, h, n, n * p, m, h0, n0, n0 * p))
