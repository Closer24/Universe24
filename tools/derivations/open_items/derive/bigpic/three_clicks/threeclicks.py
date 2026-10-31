# Big Pic toy, pushed for the team at the Boss's ask (#2187 6538805478): the owner's three clicks in one code path, no condition, no picked number.
# A giver passes toward n takers. Each giver-taker edge has its tooth (the far end its complement).
# Each takers' edge (i, j) has its tooth too. Between carries, the triangle (g-i, i-j, g-j) of every takers' edge turns.
# n = 1: no takers' edge, so nothing turns: the first click, carried, no draw.
# n >= 2: the passing splits over a triangle: the split click; its landing by the turn: the third click.
import random, sys
D = 50811429; c = (D - 1) // 2
def cen(v): return (v + c) % D - c
def edges(n): return [(i, j) for i in range(n) for j in range(i + 1, n)]
def turn(ug, ut, n):
    for (i, j) in edges(n):
        t = cen(ut[(i, j)] + ug[i]); ug[j] = cen(ug[j] - t); ug[i] = cen(ug[i] - ug[j]); ut[(i, j)] = t
def unturn(ug, ut, n):
    for (i, j) in reversed(edges(n)):
        t = ut[(i, j)]; ug[i] = cen(ug[i] + ug[j]); ug[j] = cen(ug[j] + t); ut[(i, j)] = cen(t - ug[i])
def step(ug, ut, xs, n):
    turn(ug, ut, n); qs = []
    for i in range(n):
        q, r = divmod(ug[i] + c + xs[i], D); ug[i] = r - c; qs.append(q)
    return qs
def back(ug, ut, xs, n):
    qs = []
    for i in range(n):
        q, r = divmod(ug[i] + c - xs[i], D); ug[i] = r - c; qs.append(-q)
    unturn(ug, ut, n); return qs
squares = {1: [16], 2: [9, 16], 3: [4, 9, 16]}
k = D // 1250; R = 300000
for n in (1, 2, 3):
    xs = [s * k for s in squares[n]]
    rng = random.Random(10 + n)
    ug0 = [rng.randint(-c, c) for _ in range(n)]; ut0 = {e: rng.randint(-c, c) for e in edges(n)}
    ug = list(ug0); ut = dict(ut0); rec = []
    for t in range(R): rec.append(step(ug, ut, xs, n))
    for t in range(R - 1, -1, -1): assert back(ug, ut, xs, n) == rec[t]
    runback = (ug == ug0 and ut == ut0)
    tot = [sum(r[i] for r in rec) for i in range(n)]
    S = rec and [r[0] for r in rec]
    idx = [t for t, q in enumerate(S) if q]; gaps = [b - a for a, b in zip(idx, idx[1:])]
    m = sum(gaps) / len(gaps); v = sum((g - m) ** 2 for g in gaps) / len(gaps)
    # the law's own reading: one hidden unit apart, the same click past, a later click?
    differ = 0
    for trial in range(200):
        r2 = random.Random(1000 + trial)
        a_g = [r2.randint(-c, c) for _ in range(n)]; a_t = {e: r2.randint(-c, c) for e in edges(n)}
        b_g = list(a_g); b_t = dict(a_t)
        if edges(n): e0 = edges(n)[0]; b_t[e0] = cen(b_t[e0] + 1)      # a unit in a takers' edge, which never clicks
        else: b_g[0] = cen(b_g[0] + 1)                                  # no takers' edge: a unit in the giver edge itself
        d = False
        for t in range(3000):
            qa = step(a_g, a_t, xs, n); qb = step(b_g, b_t, xs, n)
            if qa != qb: d = True; break
        differ += d
    sh = ", ".join("%.3f" % (tt / sum(tot)) for tt in tot); want = ", ".join("%.3f" % (s / sum(squares[n])) for s in squares[n])
    print("takers %d | run back exact: %s | shares %s against the squares' %s | first taker's lives var/mean^2 %.3f | the same click past, one hidden unit apart: a later click differs in %d of 200"
          % (n, runback, sh, want, v / m / m, differ))
