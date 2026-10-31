# Big Pic toy, pushed for the team at the Boss's ask (#2187 6538805478): the third click's pick as the carried form with its teeth kept,
# the teeth turned between carries by the triangle's three shears (one tooth per side), in whole numbers.
import random, sys
D = int(sys.argv[1]) if len(sys.argv) > 1 else 50811      # the dial (odd), stand-in size
R = int(sys.argv[2]) if len(sys.argv) > 2 else 1000000
TURN = int(sys.argv[3]) if len(sys.argv) > 3 else 1       # 1: turn the teeth each round; 0: the carried form as built
assert D % 2 == 1
c = (D - 1) // 2
def cen(v): return (v + c) % D - c                          # the tooth read about its birth, in [-c, c]
k = D // (int(sys.argv[4]) if len(sys.argv) > 4 else 1250)
xa, xb = 9 * k, 16 * k                                      # the giver's passings toward the two takers: k times the squares 3^2 and 4^2
def turn(u):                                                # two edges sheared in turn: det 1, whole, odd under negation
    ga, ab, gb = u                                          # two edges only: the giver's edge with each taker
    gb = cen(gb + ga); ga = cen(ga + gb)
    return [ga, ab, gb]
def unturn(u):
    ga, ab, gb = u
    ga = cen(ga - gb); gb = cen(gb - ga)
    return [ga, ab, gb]
def step(u, xa, xb, turned=TURN):
    if turned: u = turn(u)
    qa, ra = divmod(u[0] + c + xa, D)                       # side giver->a: the carry with its tooth kept
    qb, rb = divmod(u[2] + c + xb, D)                       # side giver->b
    return [ra - c, u[1], rb - c], qa, qb
def back(u, xa, xb, turned=TURN):
    qa, ra = divmod(u[0] + c - xa, D)                       # the run back: the same carry with the passing negated
    qb, rb = divmod(u[2] + c - xb, D)
    u = [ra - c, u[1], rb - c]
    if turned: u = unturn(u)
    return u, -qa, -qb
rng = random.Random(31)
u0 = [rng.randint(-c, c) for _ in range(3)]                 # a stand-in generic lay of the three side teeth
u = list(u0); A = []; B = []; down = 0; neg_ok = True; v = [-t for t in u0]
for t in range(R):
    u, qa, qb = step(u, xa, xb)
    v, na, nb = step(v, -xa, -xb)                           # the mirror world: every row negated, every tooth complemented
    if (na, nb) != (-qa, -qb) or v != [-z for z in u]: neg_ok = False
    if qa < 0 or qb < 0: down += 1
    A.append(qa); B.append(qb)
w = list(u)
for t in range(R - 1, -1, -1):
    w, qa, qb = back(w, xa, xb)
    assert (qa, qb) == (A[t], B[t])
print("dial", D, "rounds", R, "turned" if TURN else "carried (no turn)")
print("run back to the lay exactly:", w == u0, "| mirror world flips every click:", neg_ok, "| downward crossings:", down)
ta, tb = sum(A), sum(B)
print("takes a, b:", ta, tb, "| share of a: %.4f against the squares' %.4f" % (ta / (ta + tb), 9 / 25))
print("per round a: %.5f against xa/D %.5f" % (ta / R, xa / D))
def stats(S, name):
    idx = [i for i, q in enumerate(S) if q]
    gaps = [j - i for i, j in zip(idx, idx[1:])]
    m = sum(gaps) / len(gaps); var = sum((g - m) ** 2 for g in gaps) / len(gaps)
    p = sum(S) / len(S)
    # lag-1 correlation of the take indicator
    s1 = sum(1 for i in range(1, len(S)) if S[i] and S[i - 1]) / (len(S) - 1)
    corr = (s1 - p * p) / (p - p * p)
    # the last gap against the next: correlation
    g0 = gaps[:-1]; g1 = gaps[1:]; mg = sum(g0) / len(g0)
    cg = sum((a - mg) * (b - mg) for a, b in zip(g0, g1)) / len(g0) / var
    # after two takes in a row: the chance of a third
    pairs = sum(1 for i in range(2, len(S)) if S[i - 1] and S[i - 2]); tri = sum(1 for i in range(2, len(S)) if S[i - 1] and S[i - 2] and S[i])
    print("%s: p %.5f | gaps mean %.1f, var/mean^2 %.3f | lag-1 corr %.4f | gap-to-next-gap corr %.4f | after two takes in a row: %d of %d (p would give %.1f)" % (name, p, m, var / m / m, corr, cg, tri, pairs, pairs * p))
    # memoryless: chance to take within the mean life, for a young and an old wait
    L = int(m); young = old = yn = on = 0
    for i in range(len(idx) - 1):
        g = gaps[i]
        yn += 1; young += g <= L
        if g > L: on += 1; old += g <= 2 * L
    print("   within one mean life: from a fresh take %.3f, from an old wait %.3f (the exponential law gives %.3f)" % (young / yn, old / on, 1 - (1 - p) ** L))
stats(A, "taker a"); stats(B, "taker b")
# an empty taker: its passing 0 never clicks
u = list(u0); e = 0
for t in range(100000):
    u, qa, qb = step(u, xa, 0)
    e += qb != 0
print("empty taker (passing 0) clicks in 100,000 rounds:", e)
