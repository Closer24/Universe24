# Probe 1: T S T = S^-1 for one gear, law 2's form, integers only.
# State (b, n, r): notch before, now, fine tooth in [0, W).  p = W (n - b) + (r - mid(W)).
# S: p+ = p + F(n); n+ = n + (p+ + mid(W+)) div W+; r+ = (p+ + mid(W+)) mod W+.
# T_a: law 4 as written: swap b,n; r -> 2 mid(W) - r (reduced mod W, as acts.mirror does).
# T_b: swap b,n; r -> W - 1 - r (item 11 (e), acts.flip).
import random, sys
def mid(W): return W // 2
def S(st, W, Wp, F):
    b, n, r = st
    p = W * (n - b) + (r - mid(W))
    pp = p + F(n)
    q, rp = divmod(pp + mid(Wp), Wp)
    return (n, n + q, rp)
def Ta(st, W):
    b, n, r = st
    return (n, b, (2 * mid(W) - r) % W)
def Tb(st, W):
    b, n, r = st
    return (n, b, W - 1 - r)
def check(T, label, same_parity, trials=200000, seed=1):
    rng = random.Random(seed)
    bad = 0; ex = None
    for _ in range(trials):
        W = rng.randint(1, 16)
        Wp = rng.randint(1, 16)
        if same_parity and (W - Wp) % 2: Wp = Wp + 1 if Wp < 16 else Wp - 1
        k = rng.randint(-5, 5); c0 = rng.randint(-7, 7)
        F = lambda n, k=k, c0=c0: k * n + c0
        st = (rng.randint(-20, 20), rng.randint(-20, 20), rng.randint(0, W - 1))
        # forward one step with (W -> Wp), turn over at Wp, step back with (Wp -> W), turn over at W
        y = S(st, W, Wp, F)
        z = T(S(T(y, Wp), Wp, W, F), W)
        if z != st:
            bad += 1
            if ex is None: ex = (W, Wp, k, c0, st, y, z)
    print(label, "same parity" if same_parity else "any parity", "failures", bad, "of", trials, "first", ex)
for T, lab in ((Ta, "T_a law4 2mid-r"), (Tb, "T_b W-1-r")):
    check(T, lab, True); check(T, lab, False)
