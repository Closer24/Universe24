# Probe 1b: the flip r -> W-1-r against T S T = S^-1, counting only draws where W and W+ differ in parity.
import random
def mid(W): return W // 2
def S(st, W, Wp, F):
    b, n, r = st
    p = W * (n - b) + (r - mid(W))
    q, rp = divmod(p + F(n) + mid(Wp), Wp)
    return (n, n + q, rp)
def Tb(st, W): b, n, r = st; return (n, b, W - 1 - r)
rng = random.Random(1); bad = tot = 0
while tot < 100000:
    W = rng.randint(1, 16); Wp = rng.randint(1, 16)
    if (W - Wp) % 2 == 0: continue
    k = rng.randint(-5, 5); c0 = rng.randint(-7, 7); F = lambda n: k * n + c0
    st = (rng.randint(-20, 20), rng.randint(-20, 20), rng.randint(0, W - 1)); tot += 1
    y = S(st, W, Wp, F)
    if Tb(S(Tb(y, Wp), Wp, W, F), W) != st: bad += 1
print("flip W-1-r, W and W+ of different parity: T S T != S^-1 in", bad, "of", tot)
