"""The turned tooth against the board's run back law (the same act on the mirrored state), in whole numbers on the click
world's key D = 50,811,429 (examples/tensor24-click/universe.json), the birth c = (D - 1) div senses with senses 2, Big Pic's
stand-in passings 9 k and 16 k with k = D div 1250 (his toy's, a toy's pick, not the board's), the lay from a carry sequence.
(1) Big Pic's triangle turn (turnteeth.py: turn, then the carries): the same act on the mirrored state under the click
tooth's rule (teeth kept, passings negated) and under the drive's rule (teeth flipped, passings kept), one round each, against
his own inverse path back(). (2) The palindrome on four teeth (g1, g2 carrying, kept; t1, t2 hidden, flipped): sigma_1 ..
sigma_5, the carries, sigma_5 .. sigma_1, with the shears t1 += g1, g1 -= t1, t2 += g2, g2 += t1, g1 += t2: the same act on
the mirrored state round by round and as a window; the flip (every passing negated, every tooth complemented); shares;
lives; lag-1; R2 (two lays alike but one unit in t1, the same click past, a later click differing); an empty taker; and the
three-tooth palindrome (t += g1, g1 += t, g2 += t) for the kept direction g1 - g2. No float in the act; the readings' ratios
in thousandths by the carry. argv: rounds."""
import sys
R = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
D = 50811429; senses = 2
c, _ = divmod(D - 1, senses)
def cen(v): return (v + c) % D - c
k, _ = divmod(D, 1250)
X1, X2 = 9 * k, 16 * k
def carry(u, i, x):
    q, r = divmod(u[i] + c + x, D); u[i] = r - c; return q
# (1) Big Pic's triangle (g1, t, g2)
def bp_turn(u):
    ga, ab, gb = u; ab = cen(ab + ga); gb = cen(gb - ab); ga = cen(ga - gb); return [ga, ab, gb]
def bp_unturn(u):
    ga, ab, gb = u; ga = cen(ga + gb); gb = cen(gb + ab); ab = cen(ab - ga); return [ga, ab, gb]
def bp_step(u, x1, x2):
    u = bp_turn(u); q1 = carry(u, 0, x1); q2 = carry(u, 2, x2); return u, (q1, q2)
def bp_back(u, x1, x2):
    u = list(u); q1 = carry(u, 0, -x1); q2 = carry(u, 2, -x2); return bp_unturn(u), (q1, q2)
def lay(n, seed):
    out, r = [], seed
    for _ in range(n):
        r = (r * 1103515245 + 12345) % 2147483648
        out.append(cen(r))
    return out
u = lay(3, 7); fail_click = fail_drive = fail_back = 0
for t in range(2000):
    u1, q = bp_step(list(u), X1, X2)
    m, qb = bp_step(list(u1), -X1, -X2)                                   # the click tooth's rule: kept, passings negated
    fail_click += int(m != u)
    m2, _ = bp_step([-z for z in u1], X1, X2); m2 = [-z for z in m2]         # the drive's rule: flipped, passings kept
    fail_drive += int(m2 != u)
    b, _ = bp_back(u1, X1, X2); fail_back += int(b != u)
    u = u1
print(f"(1) Big Pic's triangle turn, 2,000 rounds: the same act on the mirrored state fails at {fail_click} (the click tooth's rule) and {fail_drive} (the drive's rule); his inverse path back() at {fail_back}")
# (2) the four-tooth palindrome: u = [g1, g2, t1, t2]
SHEARS = [(2, 0, 1), (0, 2, -1), (3, 1, 1), (1, 2, 1), (0, 3, 1)]          # t1 += g1, g1 -= t1, t2 += g2, g2 += t1, g1 += t2
def shear(u, s):
    i, j, sg = s; u[i] = cen(u[i] + sg * u[j])
def step4(u, x1, x2, turned=True):
    u = list(u)
    if turned:
        for s in SHEARS: shear(u, s)
    q1 = carry(u, 0, x1); q2 = carry(u, 1, x2)
    if turned:
        for s in reversed(SHEARS): shear(u, s)
    return u, (q1, q2)
def mir(u): return [u[0], u[1], -u[2], -u[3]]                               # carrying kept, hidden flipped
u0 = lay(4, 11); u = list(u0); rec = []; fails = 0; flipbad = 0; down = 0
for t in range(R):
    u1, q = step4(u, X1, X2)
    back, qb = step4(mir(u1), -X1, -X2); back = mir(back)
    fails += int(back != u or qb != (-q[0], -q[1]))
    v1, qv = step4([-z for z in u], -X1, -X2)
    flipbad += int(v1 != [-z for z in u1] or qv != (-q[0], -q[1]))
    down += int(q[0] < 0 or q[1] < 0)
    rec.append(q); u = u1
w = list(u)
for t in range(R - 1, -1, -1):
    w, qb = step4(mir(w), -X1, -X2); w = mir(w)
print(f"(2) the palindrome, {R} rounds: the one-round run back by the same act on the mirrored state fails at {fails}; the window back to the lay exact {int(w == u0)}; the flip fails at {flipbad}; downward crossings {down}")
A = [q[0] for q in rec]; B = [q[1] for q in rec]
ta, tb = sum(A), sum(B)
sh, _ = divmod(1000 * ta, ta + tb)
print(f"   takes {ta} and {tb}: the first's share {sh} thousandths against the squares' 9/25 = 360")
def lives(S):
    idx = [i for i, q in enumerate(S) if q]
    g = [b - a for a, b in zip(idx, idx[1:])]
    n_, s1, s2 = len(g), sum(g), sum(x * x for x in g)
    ratio, _ = divmod(1000 * (n_ * s2 - s1 * s1), s1 * s1)
    n = len(S); m = sum(S); pairs = sum(S[i] * S[i - 1] for i in range(1, n))
    corr, _ = divmod(1000 * (pairs * n - m * m * (n - 1) // n * 1), (m * n - m * m) * (n - 1) // n) if m else (0, 0)
    return ratio, corr
for nm, S in (("first", A), ("second", B)):
    ratio, corr = lives(S)
    print(f"   the {nm} taker's lives: variance over mean squared {ratio} thousandths (1,000 the exponential law); lag-1 of its takes {corr} thousandths")
# R2: two lays alike but one unit in t1 (hidden, never clicks)
differ = 0; firsts = []
for trial in range(200):
    a = lay(4, 1000 + trial); b = list(a); b[2] = cen(b[2] + 1)
    for t in range(3000):
        a, qa = step4(a, X1, X2); b, qb = step4(b, X1, X2)
        if qa != qb:
            differ += 1; firsts.append(t + 1); break
firsts.sort()
print(f"   R2: two lays one unit apart in a hidden tooth, the same click past: a later click differs in {differ} of 200, the first at round {firsts[len(firsts) // 2] if firsts else None} (the median)")
differ0 = 0
for trial in range(200):
    a = lay(4, 1000 + trial); b = list(a); b[2] = cen(b[2] + 1)
    for t in range(3000):
        a, qa = step4(a, X1, X2, False); b, qb = step4(b, X1, X2, False)
        if qa != qb:
            differ0 += 1; break
print(f"   no turn (the carried form): a later click differs in {differ0} of 200")
e = 0; u = list(u0)
for t in range(100000):
    u, q = step4(u, X1, 0); e += int(q[1] != 0)
print(f"   an empty taker (passing 0) clicks in 100,000 rounds: {e}")
# the three-tooth palindrome keeps g1 - g2 (odd dimension)
def step3(u, x1, x2):
    u = list(u)
    for (i, j, sg) in ((1, 0, 1), (0, 1, 1), (2, 1, 1)): u[i] = cen(u[i] + sg * u[j])   # t += g1, g1 += t, g2 += t on (g1, t, g2)
    q1 = carry(u, 0, x1); q2 = carry(u, 2, x2)
    for (i, j, sg) in ((2, 1, 1), (0, 1, 1), (1, 0, 1)): u[i] = cen(u[i] + sg * u[j])
    return u, (q1, q2)
u = lay(3, 5); kept = 0
for t in range(1000):
    u1, _ = step3(u, X1, X2)
    kept += int(cen(u1[0] - u1[2] - (u[0] - u[2]) - (X1 - X2)) == 0)
    u = u1
print(f"   the three-tooth palindrome: g1 - g2 moves by exactly x1 - x2 at {kept} of 1,000 rounds (a kept direction)")
# the three-tooth palindrome's own readings, and both takers landing in one round against independent landings
u0 = lay(3, 5); u = list(u0); rec3 = []
for t in range(R):
    u, q = step3(u, X1, X2); rec3.append(q)
A3 = [q[0] for q in rec3]; B3 = [q[1] for q in rec3]
r1, c1 = lives(A3); r2_, c2 = lives(B3)
both = sum(a * b for a, b in zip(A3, B3)); ind, _ = divmod(sum(A3) * sum(B3), R)
both4 = sum(a * b for a, b in zip(A, B)); ind4, _ = divmod(sum(A) * sum(B), R)
print(f"   the three-tooth palindrome: lives {r1} and {r2_} thousandths, lag-1 {c1} and {c2}; both takers in one round {both} against independent {ind}")
print(f"   the four-tooth palindrome: both takers in one round {both4} against independent {ind4}")
