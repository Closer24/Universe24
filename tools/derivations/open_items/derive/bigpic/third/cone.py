"""The third click's cone (the owner's word of 12:4x UTC to Big Pic: "check whether the board needs the cone... of the
third click... is it a cone to the past and to the future?"). A stand-alone model, a test's lay, not the engine's board.
turns.py's three like hands on a triangle of bands, each hand also banded to one hub clock, and the hub at the end of
a chain of L clocks, each link a band, every band its own square (t/2)(x_i + x_j)^2 at the click world's hands' tie,
no own spring laid. The rest of the board reads the three hands only through the hub, alike, so the third click's turn
of the hands' whole state (turns.py's write at tau's landings) is a symmetry of the whole round. Whole numbers and
Rule3's carry only. The round reads a clock's own state and its neighbours' counts alone, so nothing reaches farther
than one edge per round, in either sense of time; the readings check it and read what the write reaches.
Readings, the writes on, over N rounds:
  - the books: E32's change against the teeth's share at every round, the turns included; the widest count;
  - the past cone: two starts apart at the chain's far clock alone (laid there at the test's swing); the first round
    each clock's count differs, against its distance from the far clock; the first round tau's landings differ;
  - the future cone: two ends apart at the far clock alone (the same swing added), each run back from its end state
    alone; the first round, counted back from the end, at which each clock's count differs, against its distance;
  - the write's own reach: with the writes and without, the hub's and the chain's lines alike at every round, and the
    first round the hands' own lines differ.
Usage: python3 -I cone.py <node-all src> <the click world's universe.json> [rounds] [chain]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
L = int(sys.argv[4]) if len(sys.argv) > 4 else 6
chosen = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["chosen"]
TIE2, KEY = int(chosen["tie"]), int(chosen["key"])
W = 600000000  # the click world's rest teeth (node-all's loader: gearing's rest)
GEAR = W + W
SPOKES, SENSES = 6, 2
HALF, _ = carry(SPOKES, SENSES, 0)  # kappa / two
D = HALF * KEY
HUB = 3
FAR = HUB + L
N = HUB + L + 1
TRI = [(0, 1), (1, 2), (0, 2)]  # the triangle's sorted edges, its member's
BANDS = TRI + [(0, HUB), (1, HUB), (2, HUB)] + [(HUB + j, HUB + j + 1) for j in range(L)]
C = [1, 1, -1]  # the triangle's boundary on its sorted edges
G = 3
GD = G * D
SWING = 40 * 2 ** 12  # amplitudes.py's top swing, a test's lay


def born(dial):
    return carry(dial - 1, SENSES, 0)[0]


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def pushes(a):
    f = [0] * N
    for i, j in BANDS:
        p = -TIE2 * (a[i] + a[j])
        f[i] += p
        f[j] += p
    return f


def round_(a, b, s):
    f = pushes(a)
    a1, s1 = [], []
    for i in range(N):
        q, kept = split(GEAR * (a[i] - b[i]) + GEAR * (a[i] - b[i]) + 4 * f[i] + s[i], GEAR)
        a1.append(a[i] + q)
        s1.append(kept)
    return a1, s1


def energy(a, b):
    e = sum(16 * W * W * (x - y) * (x - y) for x, y in zip(a, b))
    for i, j in BANDS:
        e += 16 * W * TIE2 * (a[i] + a[j]) * (b[i] + b[j])
    return e


def share(b, a1, s, s1):
    return sum(4 * W * (z - y) * (p - r) for z, y, p, r in zip(a1, b, s, s1))


def lw(p, r, u, v):
    return p[u] * r[v] - p[v] * r[u]


def passings(b, a, a1):
    return [HALF * TIE2 * (lw(a, a1, u, v) + lw(b, a, u, v)) for u, v in TRI]


def record(x, f, tau):
    y = sum(c * xe for c, xe in zip(C, x))
    f1 = []
    for e in range(3):
        _, fe = carry(G * x[e] - C[e] * y, GD, f[e])
        f1.append(fe)
    w, tau1 = carry(y, GD, tau)
    return f1, tau1, w


def turn_once(a, b, s, f):
    """turns.py's cycle (0 1 2) on the hands alone; the hub and the chain stay."""
    na, nb, ns = [a[2], a[0], a[1]] + a[3:], [b[2], b[0], b[1]] + b[3:], [s[2], s[0], s[1]] + s[3:]
    nf = [GD - 1 - f[2], f[0], GD - 1 - f[1]]
    return na, nb, ns, nf


def turn(a, b, s, f, w):
    for _ in range(carry(w, 3, 0)[1]):
        a, b, s, f = turn_once(a, b, s, f)
    return a, b, s, f


def run(a, b, s, f, tau, rounds, writes=True):
    a, b, s, f = list(a), list(b), list(s), list(f)
    held = widest = 0
    lines, ws = [], []
    for _ in range(rounds):
        a1, s1 = round_(a, b, s)
        f1, tau1, w = record(passings(b, a, a1), f, tau)
        e0 = energy(a, b)
        sh = share(b, a1, s, s1)
        na, nb, ns, nf = a1, list(a), s1, f1
        if writes:
            na, nb, ns, nf = turn(na, nb, ns, nf, w)
        held += energy(na, nb) - e0 == sh
        a, b, s, f, tau = na, nb, ns, nf, tau1
        widest = max([widest] + [abs(x).bit_length() for x in a])
        lines.append(list(a))
        ws.append(w)
    return (a, b, s, f, tau), held, widest, lines, ws


def mirror(a, b, s):
    return list(b), list(a), [-1 - v for v in s]


def back(end, rounds):
    """The run back from the end state alone; the lines, round by round, counted back from the end."""
    ma, mb, ms = mirror(end[0], end[1], end[2])
    start, _, _, lines, _ = run(ma, mb, ms, end[3], end[4], rounds, True)
    return start, lines


def first_apart(p, q, clock):
    for r, (x, y) in enumerate(zip(p, q), start=1):
        if x[clock] != y[clock]:
            return r
    return None


def distance(clock):
    return FAR - clock if clock >= HUB else FAR - HUB + 1


def cone(p, q):
    """Each clock's first round apart against its distance from the far clock; True when none comes sooner."""
    firsts = [first_apart(p, q, c) for c in range(N)]
    holds = all(r is None or r >= distance(c) for c, r in enumerate(firsts) if c != FAR)
    return firsts, holds


a0, b0 = [40, -20, -20] + [0] * (L + 1), [20, -40, 20] + [0] * (L + 1)
print(f"== three like hands on a triangle of bands (laid turning, turns.py's lay), each banded to one hub,"
      f" the hub at the"
      f" end of a chain of {L} bands; {ROUNDS} rounds; the hands' tie {TIE2}, W {W}, the triangle's dial G D {GD}; the"
      f" far clock {FAR}, the hands {distance(0)} edges from it; the test's swing at the far clock {SWING}", flush=True)
for t0 in (born(GD), 0):
    s0, f0 = [0] * N, [born(GD)] * 3
    end, held, widest, lines, ws = run(a0, b0, s0, f0, t0, ROUNDS, True)
    print(f"   tau born at {t0}: E32's change = the teeth's share in {held} of {ROUNDS} rounds; widest count {widest}"
          f" bits; landings net {sum(ws)}", flush=True)
    a1, b1 = list(a0), list(b0)
    a1[FAR] += SWING
    b1[FAR] += SWING
    _, _, _, lines1, ws1 = run(a1, b1, s0, f0, t0, ROUNDS, True)
    firsts, holds = cone(lines, lines1)
    w_first = next((r for r, (x, y) in enumerate(zip(ws, ws1), start=1) if x != y), None)
    print(f"      the past cone: each clock's first round apart (the hands first, the hub, the chain to the far clock)"
          f" {firsts}; none sooner than its distance: {holds}; tau's landings first apart at round {w_first}",
          flush=True)
    start, back0 = back(end, ROUNDS)
    exact = mirror(start[0], start[1], start[2]) == (a0, b0, s0) and start[3] == f0 and start[4] == t0
    e1 = (list(end[0]), list(end[1]), list(end[2]), list(end[3]), end[4])
    e1[0][FAR] += SWING
    e1[1][FAR] += SWING
    _, back1 = back(e1, ROUNDS)
    bfirsts, bholds = cone(back0, back1)
    print(f"      the future cone: the run back exact {exact}; each clock's first round apart,"
          f" counted back from the end,"
          f" {bfirsts}; none sooner than its distance: {bholds}", flush=True)
    _, _, _, lines_u, _ = run(a0, b0, s0, f0, t0, ROUNDS, False)
    outside = all(x[HUB:] == y[HUB:] for x, y in zip(lines, lines_u))
    hands_first = next((r for r, (x, y) in enumerate(zip(lines, lines_u), start=1) if x[:HUB] != y[:HUB]), None)
    first_w = next((r for r, w in enumerate(ws, start=1) if w), None)
    print(f"      the write's own reach: the hub's and the chain's lines the unwritten path's"
          f" at every round: {outside};"
          f" the hands' own lines first apart at round {hands_first}; tau's first landing at round {first_w}",
          flush=True)
print("exit", flush=True)
