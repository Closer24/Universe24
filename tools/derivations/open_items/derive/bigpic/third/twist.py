"""The third click's write inside the round, a first stand-alone model (the owner's words of 13:0x to 13:5x UTC; the
Boss's 6544072212 item 4, 6544481574 item 3: the write inside the round, Big Pic's to lead). A test's lay, not the
engine's board. Whole numbers and Rule3's carry only.
The click world's triangle: the giver (0), the taker (1) and the held hand (2), each a clock of three axes (the star's
i, j and k), each axis on the engine's gear form with its own tooth, each clock with the click world's own spring.
The held hand is tied to the giver and to the taker, and the band joins the giver and the taker, every edge a two-leg
coupling at the click world's hands' tie (tooth.py's form).
The write: the band couples the giver's axes to the taker's axes turned by P^N, P the turn of the three axes (i to j
to k; conjugation by the order-3 unit w on the axes), N the triangle's landed count. So the write is a term of the
round itself, and the round reads N at its own centre:
  - tau, the triangle's tooth, carries the circulation of the untwisted passings, split into its two half-windows: the
    half (b, a) before the round and the half (a, a+) after it;
  - the round reads N after the first half, so the run back, the same round from the mirror, reads the same N at the
    same centre: the run back is exact by construction;
  - within a round the band is a whole bilinear coupling t a_g . P^N a_u, so the energy and each clock's books keep
    the board's own identity; when N moves between rounds, the band's cross term moves at fixed counts: the write's
    energy, read here as a cost.
Readings, the write against no write (N held at 0), over the run: the run back exact by the same act; each clock's
books within every round; E32 moved at the rounds where N moves, and E32's narrowest against its widest; the held
hand's lines and the ties' first clicks against the unwritten path's; the landings, and N's turns modulo 3.
Usage: python3 -I twist.py <node-all src> <the click world's universe.json> [rounds]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
chosen = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["chosen"]
S, TIE2, KEY = int(chosen["spring"]), int(chosen["tie"]), int(chosen["key"])
W = 600000000  # the click world's rest teeth (node-all's loader: gearing's rest)
GEAR = W + W
SPOKES, SENSES = 6, 2
HALF, _ = carry(SPOKES, SENSES, 0)  # kappa / two
D = HALF * KEY
G = 3
GD = G * D
AXES = 3
EDGES = [(0, 1), (1, 2), (0, 2)]  # the band (0, 1), the ties (1, 2) and (0, 2)
C = [1, 1, -1]  # the triangle's boundary on its sorted edges


def born(dial):
    return carry(dial - 1, SENSES, 0)[0]


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def turn(v, n):
    """P^n on three axes: i to j to k, n times (n taken modulo 3)."""
    for _ in range(carry(n, AXES, 0)[1]):
        v = [v[2], v[0], v[1]]
    return v


def back_turn(v, n):
    """The transpose, P^-n."""
    for _ in range(carry(n, AXES, 0)[1]):
        v = [v[1], v[2], v[0]]
    return v


def couple(e, n):
    """The coupling matrix of edge e: the band turned by P^n, the ties plain."""
    return n if e == 0 else 0


def pushes(a, n):
    f = [[-2 * S * x for x in clock] for clock in a]
    for e, (u, v) in enumerate(EDGES):
        m = couple(e, n)
        tu = turn(a[v], m)  # P^m a_v, pushing u
        tv = back_turn(a[u], m)  # P^-m a_u, pushing v
        for k in range(AXES):
            f[u][k] += -TIE2 * tu[k]
            f[v][k] += -TIE2 * tv[k]
    return f


def round_(a, b, s, n):
    f = pushes(a, n)
    a1, s1 = [], []
    for i in range(3):
        row, kept_row = [], []
        for k in range(AXES):
            q, kept = split(GEAR * (a[i][k] - b[i][k]) + GEAR * (a[i][k] - b[i][k]) + 4 * f[i][k] + s[i][k], GEAR)
            row.append(a[i][k] + q)
            kept_row.append(kept)
        a1.append(row)
        s1.append(kept_row)
    return a1, s1


def dot(p, r):
    return sum(x * y for x, y in zip(p, r))


def cross_l(p, r, u, v, m):
    """p_u . P^m r_v - r_u . P^m p_v: the edge's half-window form, the coupling turned by P^m."""
    return dot(p[u], turn(r[v], m)) - dot(r[u], turn(p[v], m))


def passings(b, a, a1, n):
    """Each edge's passing into its lower clock, the band turned by P^n (tooth.py's form)."""
    return [HALF * TIE2 * (cross_l(a, a1, u, v, couple(e, n)) + cross_l(b, a, u, v, couple(e, n)))
            for e, (u, v) in enumerate(EDGES)]


def half(p, r):
    """One half-window's untwisted passings, the record's: HALF t (p_u . r_v - r_u . p_v) on every edge."""
    return [HALF * TIE2 * cross_l(p, r, u, v, 0) for u, v in EDGES]


def own(a, b, n):
    """Each clock's own energy with half of each of its edges' cross terms, the band turned by P^n (E32's terms)."""
    out = []
    for i in range(3):
        e = sum(16 * W * W * (x - y) * (x - y) + 32 * W * S * x * y for x, y in zip(a[i], b[i]))
        out.append(e)
    for e, (u, v) in enumerate(EDGES):
        m = couple(e, n)
        cross = 8 * W * TIE2 * (dot(a[u], turn(b[v], m)) + dot(b[u], turn(a[v], m)))
        out[u] += cross
        out[v] += cross
    return out


def ends(i):
    return [1 if e[0] == i else -1 if e[1] == i else 0 for e in EDGES]


def record(x, tau):
    y = sum(c * xe for c, xe in zip(C, x))
    w, tau1 = carry(y, GD, tau)
    return tau1, w


def run(a, b, s, tau, n, k, rounds, writes=True, log=None):
    a, b, s, k = [list(r) for r in a], [list(r) for r in b], [list(r) for r in s], list(k)
    books = moved = landings = 0
    e_low = e_high = None
    for _ in range(rounds):
        tau, w = record(half(b, a), tau)
        n += w
        landings += w * w
        m = n if writes else 0
        a1, s1 = round_(a, b, s, m)
        x = passings(b, a, a1, m)
        e0, e1 = own(a, b, m), own(a1, a, m)
        share = [sum(4 * W * (z - y) * (p - r) for z, y, p, r in zip(a1[i], b[i], s[i], s1[i])) for i in range(3)]
        for i in range(3):
            net = sum(ends(i)[e] * x[e] for e in range(3))
            books += HALF * (e1[i] - e0[i] - share[i]) == 8 * W * net
        tau, w = record(half(a, a1), tau)
        n += w
        landings += w * w
        m_next = n if writes else 0
        moved += sum(own(a1, a, m_next)) != sum(e1)
        clicks = []
        for e in range(3):
            q, k[e] = carry(x[e], D, k[e])
            clicks.append(q)
        a, b, s = a1, a, s1
        total = sum(own(a, b, m_next))
        e_low = total if e_low is None else min(e_low, total)
        e_high = total if e_high is None else max(e_high, total)
        if log is not None:
            log.append(([list(r) for r in a], clicks))
    return (a, b, s, tau, n, k), books, moved, landings, e_low, e_high


def mirror(a, b, s):
    return [list(r) for r in b], [list(r) for r in a], [[-1 - v for v in r] for r in s]


def per_mille(p, q):
    return carry(1000 * p + carry(q, 2, 0)[0], q, 0)[0]


def free_swing(amp, k):
    """One axis of a lone clock with the click world's spring, laid at rest at amp, after k rounds of its own swing."""
    a, b, s = amp, amp, 0
    for _ in range(k):
        q, kept = split(GEAR * (a - b) + GEAR * (a - b) + 4 * (-2 * S * a) + s, GEAR)
        a, b, s = a + q, a, kept
    return a, b, s


SWING = 40  # the click world's giver's count (setting.json, gear 3)
LEAD = 3  # a test's lay: the taker laid where the giver's own free swing stands 3 rounds on, near a quarter swing
taker = free_swing(SWING, LEAD)
held_hand = free_swing(SWING, LEAD * 2)
now0 = [[SWING, 0, 0], [taker[0], 0, 0], [held_hand[0], 0, 0]]  # all three along i, the later two further on
before0 = [[SWING, 0, 0], [taker[1], 0, 0], [held_hand[1], 0, 0]]
teeth0 = [[0, 0, 0], [taker[2], 0, 0], [held_hand[2], 0, 0]]
print(f"the click world's triangle, three axes a clock, the band turned by P^N; {ROUNDS} rounds; the spring {S}, the"
      f" hands' tie {TIE2}, W {W}; the triangle's dial G D {GD}; the lay {now0} now and {before0} before", flush=True)
logs = {}
for name, writes in (("no write", False), ("the write inside the round", True)):
    for t0 in (born(GD), 0):
        log = []
        start = (now0, before0, teeth0, t0, 0, [born(D)] * 3)
        end, books, moved, landings, e_low, e_high = run(*start, ROUNDS, writes, log)
        ma, mb, ms = mirror(end[0], end[1], end[2])
        back, _, _, _, _, _ = run(ma, mb, ms, end[3], end[4], end[5], ROUNDS, writes)
        ba, bb, bs = mirror(back[0], back[1], back[2])
        exact = (ba, bb, bs, back[3], back[4], back[5]) == (now0, before0, teeth0, t0, 0, [born(D)] * 3)
        logs[(name, t0)] = log
        print(f"== {name}, tau born at {t0}: each clock's books within the round in {books} of {3 * ROUNDS}; E32 moved"
              f" between rounds at {moved}; E32's narrowest {per_mille(e_low, e_high)} per mille of its widest;"
              f" landings (each counted by its square) {landings}; N at the end {end[4]}, its turn"
              f" {carry(end[4], 3, 0)[1]} of 3; the run back by the same act exact: {exact}", flush=True)
for t0 in (born(GD), 0):
    unw, wri = logs[("no write", t0)], logs[("the write inside the round", t0)]
    clocks = [sum(1 for (x1, _), (x2, _) in zip(unw, wri) if x1[i] != x2[i]) for i in range(3)]
    edges = [sum(1 for (_, c1), (_, c2) in zip(unw, wri) if c1[e] != c2[e]) for e in range(3)]
    landed = [[sum(c[e] for _, c in log) for e in range(3)] for log in (unw, wri)]
    print(f"   tau born at {t0}: each clock's counts apart from the unwritten path (the giver, the taker, the held"
          f" hand) in {clocks} rounds; each edge's first clicks apart (the band, the taker's tie, the giver's tie) in"
          f" {edges}; each edge's net clicks unwritten {landed[0]}, written {landed[1]}", flush=True)
print("exit", flush=True)
