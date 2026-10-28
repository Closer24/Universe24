# Mutant of probe 3: the doubled wheel with the flip R -> (2W - R) mod 2W must fail.
import random
def S(st, W, Wp, F):
    b, n, R = st
    P = 2 * W * (n - b) + R - W
    q, Rp = divmod(P + 2 * F(n) + Wp, 2 * Wp)
    return (n, n + q, Rp)
def T(st, W): b, n, R = st; return (n, b, (2 * W - R) % (2 * W))
rng = random.Random(7); bad = 0
for _ in range(20000):
    W = rng.randint(1, 16); Wp = rng.randint(1, 16); k = rng.randint(-5, 5)
    st = (rng.randint(-20, 20), rng.randint(-20, 20), rng.randint(0, 2 * W - 1))
    y = S(st, W, Wp, lambda n: k * n)
    if T(S(T(y, Wp), Wp, W, lambda n: k * n), W) != st: bad += 1
print("mutant flip (2W - R) mod 2W: T S T = S^-1 failures", bad, "of 20000")
