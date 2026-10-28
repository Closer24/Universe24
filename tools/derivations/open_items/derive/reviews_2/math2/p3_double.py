# Probe 3: a candidate repair.  Carry every gear on a fine wheel of 2W teeth (2 = the sides of a Spoke),
# R in [0, 2W), stride P = 2W (n - b) + R - W, kick 2 F, flip R -> 2W - 1 - R.  Then the mirror constant
# 2W - 1 - 2 mid(2W) = -1 is the same at every W, so T S T = S^-1 and the gear's negation N commute with S
# at every pair (W, W+) of either parity.  Integers only.
import random
def S(st, W, Wp, F):
    b, n, R = st
    P = 2 * W * (n - b) + R - W
    Pp = P + 2 * F(n)
    q, Rp = divmod(Pp + Wp, 2 * Wp)
    return (n, n + q, Rp)
def T(st, W):
    b, n, R = st
    return (n, b, 2 * W - 1 - R)
def N(st, W):
    b, n, R = st
    return (-b, -n, 2 * W - 1 - R)
rng = random.Random(7)
badT = badN = badTa = 0
for _ in range(200000):
    W = rng.randint(1, 16); Wp = rng.randint(1, 16)
    k = rng.randint(-5, 5)
    F = lambda n, k=k: k * n            # odd in the notch, as a linear pull is
    st = (rng.randint(-20, 20), rng.randint(-20, 20), rng.randint(0, 2 * W - 1))
    y = S(st, W, Wp, F)
    if T(S(T(y, Wp), Wp, W, F), W) != st: badT += 1
    if S(N(st, W), W, Wp, F) != N(y, Wp): badN += 1
print("doubled wheel: T S T = S^-1 failures", badT, "of 200000 (W, W+ of any parity)")
print("doubled wheel: S N = N S failures", badN, "of 200000")
