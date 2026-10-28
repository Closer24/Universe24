# Probe 4: the 24's negation of a gear, N: (b, n, r) -> (-b, -n, W - 1 - r), against law 2's step with
# the carry offset mid(W) = W div 2, at fixed teeth and across a change of the lapse's parity.
# Mutant: the law's mirror (2 mid - r) mod W in place of the flip.
import random
def mid(W): return W // 2
def S(st, W, Wp, F):
    b, n, r = st
    p = W * (n - b) + (r - mid(W))
    q, rp = divmod(p + F(n) + mid(Wp), Wp)
    return (n, n + q, rp)
def Nflip(st, W): b, n, r = st; return (-b, -n, W - 1 - r)
def Nmirror(st, W): b, n, r = st; return (-b, -n, (2 * mid(W) - r) % W)
rng = random.Random(11)
for name, Nf in (("flip W-1-r", Nflip), ("mutant mirror 2mid-r", Nmirror)):
    for same in (True, False):
        bad = 0; tot = 0
        for _ in range(100000):
            W = rng.randint(1, 16); Wp = W if same else rng.randint(1, 16)
            if not same and (W - Wp) % 2 == 0: continue
            k = rng.randint(-5, 5); F = lambda n, k=k: k * n
            st = (rng.randint(-20, 20), rng.randint(-20, 20), rng.randint(0, W - 1))
            tot += 1
            if S(Nf(st, W), W, Wp, F) != Nf(S(st, W, Wp, F), Wp): bad += 1
        print(name, "W+ = W" if same else "W+ of the other parity", "S N != N S in", bad, "of", tot)
