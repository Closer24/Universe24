# Big Pic toy, pushed for the team at the Boss's ask (#2187 6538805478): the pair's one hand drawn by the turned tooth, in whole numbers.
# Settings at Pythagorean angles: cos t = 12/13, so every weight is a whole ratio over the dial 13^6.
import random, sys
from fractions import Fraction as F
D = 13 ** 6; c = (D - 1) // 2; R = int(sys.argv[1]) if len(sys.argv) > 1 else 400000
def cen(v): return (v + c) % D - c
n = 4
def turn(u):
    u = list(u)
    for i in range(1, n): u[i] = cen(u[i] + u[i - 1])
    u[0] = cen(u[0] + u[n - 1]); return u
def unturn(u):
    u = list(u); u[0] = cen(u[0] - u[n - 1])
    for i in range(n - 1, 0, -1): u[i] = cen(u[i] - u[i - 1])
    return u
# cos^2 of the angle between the two settings, as whole numbers over D: one step t, or three steps 3t
cos1, sin1 = F(12, 13), F(5, 13)
cos3 = 4 * cos1 ** 3 - 3 * cos1
SAME = {1: int(cos1 ** 2 * D), 3: int(cos3 ** 2 * D)}
assert all(F(SAME[k], D) in (cos1 ** 2, cos3 ** 2) for k in SAME)
HALF = (D - 1) // 2
def carry(x, u, i):
    q, r = divmod(u[i] + c + x, D); u[i] = r - c; return q
def uncarry(x, u, i):
    q, r = divmod(u[i] + c - x, D); u[i] = r - c; return -q
rng = random.Random(5)
alice = [rng.randint(-c, c) for _ in range(n)]; bob = [rng.randint(-c, c) for _ in range(n)]; pair = [rng.randint(-c, c) for _ in range(n)]
lay = (list(alice), list(bob), list(pair))
rec = []
for t in range(R):
    alice = turn(alice); bob = turn(bob); pair = turn(pair)
    a = 2 * carry(HALF, alice, 0)            # Alice's setting: 0 or 2t, drawn at her own place
    b = 1 + 2 * carry(HALF, bob, 0)          # Bob's setting: t or 3t, drawn at his own place
    sa = 1 if carry(HALF, pair, 0) else -1   # the pair's one hand: the first click, by its marginal
    same = carry(SAME[abs(b - a)], pair, 1)  # the second click reads the same hand, pushed back to the first outcome
    sb = sa if same else -sa
    rec.append((a, b, sa, sb))
# the run back, every tooth to the lay
for t in range(R - 1, -1, -1):
    a, b, sa, sb = rec[t]
    assert 2 * uncarry(HALF, alice, 0) == a and 1 + 2 * uncarry(HALF, bob, 0) == b
    assert uncarry(SAME[abs(b - a)], pair, 1) == (1 if sa == sb else 0)
    assert (1 if uncarry(HALF, pair, 0) else -1) == sa
    alice = unturn(alice); bob = unturn(bob); pair = unturn(pair)
print("dial 13^6 =", D, "| rounds", R, "| run back to the lay:", (alice, bob, pair) == lay)
E = {}; N = {}
for a, b, sa, sb in rec:
    E[(a, b)] = E.get((a, b), 0) + sa * sb; N[(a, b)] = N.get((a, b), 0) + 1
e = {k: E[k] / N[k] for k in E}
S = e[(0, 1)] - e[(0, 3)] + e[(2, 1)] + e[(2, 3)]
exact = 3 * (2 * cos1 ** 2 - 1) - (2 * cos3 ** 2 - 1)
print("CHSH from the click counts: %.4f | the hand's own value %.4f (exact %s) | the local bound 2" % (S, float(exact), exact))
for k in sorted(e): print("   settings", k, "pairs", N[k], "E %.4f" % e[k])
# no signal: each place's own counts against the far setting
for far in (1, 3):
    sel = [r for r in rec if r[1] == far]; print("   Alice's +1 share with Bob's setting %dt: %.4f (%d)" % (far, sum(r[2] == 1 for r in sel) / len(sel), len(sel)))
for far in (0, 2):
    sel = [r for r in rec if r[0] == far]; print("   Bob's +1 share with Alice's setting %dt: %.4f (%d)" % (far, sum(r[3] == 1 for r in sel) / len(sel), len(sel)))
# the local road, for the bound: each place draws from its own teeth and a shared past copied at birth
rng = random.Random(6)
A2 = [rng.randint(-c, c) for _ in range(n)]; B2 = list(A2)   # one past, copied to both places
al = [rng.randint(-c, c) for _ in range(n)]; bo = [rng.randint(-c, c) for _ in range(n)]
E2 = {}; N2 = {}
for t in range(R):
    al = turn(al); bo = turn(bo); A2 = turn(A2); B2 = turn(B2)   # the copies turn alike, so the shared past stays shared
    a = 2 * carry(HALF, al, 0); b = 1 + 2 * carry(HALF, bo, 0)
    # each place's best local answer from the shared past alone: the sign read from the shared tooth, flipped at the setting 3t
    lam = carry(HALF, A2, 0); B2[0] = A2[0]
    sa = 1 if lam else -1
    sb = (1 if lam else -1) * (-1 if b == 3 else 1)
    E2[(a, b)] = E2.get((a, b), 0) + sa * sb; N2[(a, b)] = N2.get((a, b), 0) + 1
e2 = {k: E2[k] / N2[k] for k in E2}
print("the local road, a shared past with each place on its own: CHSH %.4f" % (e2[(0, 1)] - e2[(0, 3)] + e2[(2, 1)] + e2[(2, 3)]))
