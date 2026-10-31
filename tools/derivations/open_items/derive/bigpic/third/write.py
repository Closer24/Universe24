"""The write the rest read (the owner's word of 13:0x UTC: "There is a connection between click 3 and click 3 and the
rest, because the universe must return to what the future fixed... and it changes its path only through click 3";
the Boss's 6543746068 item 3, 6543768769 item 3 and 6543794891 item 4: a write the rest read, that keeps each clock's
books by a passing, on a meshed board, whose sum over every triangle meets the fixed end, read by label; the THIRD
pair's B1 and B2 on turns.py: its turn is a relabelling, and each clock's books break at every write).
A stand-alone model, a test's lay, not the engine's board. Two triangles of like hands, A (clocks 0, 1, 2) and B
(clocks 3, 4, 5), each a triangle of bands, every band its own square (t/2)(x_i + x_j)^2 at the click world's hands'
tie, joined by one band between clock 0 and clock 3: the two places' one edge, so the rest reads each triangle's
hands apart (a stand-in for a meshed board; the Mesh's own crossing is not built here). Each triangle's tooth tau
carries its bands' circulation (turns.py). Whole numbers and Rule3's carry only.
DERIVED, the condition on a write between rounds. Let R be the round, M the mirror (the run back is M R M = R^-1),
and W(w) the write at a landing w, so a step is F = W(w(X)) R. The same act runs back exactly when M F M = F^-1,
that is when R^-1 W(w) R = M W(w')^-1 M, w' the landing the run back reads (-w). The left side moves the write one
round back, which the round spreads to the write's neighbours; the right side is a write at the same place. So a
local write is undone by the same act only when it commutes with the round: a symmetry of the whole round. On a board
that reads the hands apart, such a write fixes all that the rest reads. So the three asks, the rest read it, each
clock's books, and the same act's run back, do not hold together for any write between rounds.
Writes read, at each landing w of each triangle's tau:
  - none: the unwritten path;
  - the whole turn: turns.py's turn of the hands' whole state by the cycle (0 1 2), w times (mod 3);
  - the momenta turn: the hands' exact momenta P = 2 G (a - b) + s turned by the cycle, w times (mod 3), the counts
    kept, so the teeth alone move: no clock's count or energy moves at the write, and the momentum it moves enters
    each hand through its own tooth at the next round.
Readings, per write, over the run: each clock's books at every round, read across the write as the THIRD pair read
them (half_kappa (E_i' - E_i - share_i) = 8 W times its sides' passings, E_i' after the write); E32 at each write;
E32's widest and narrowest over the run; the other triangle's counts against the unwritten path; the widest count;
the run back from the end state alone by the same act. Then, under the momenta turn, the ends over a grid of both
triangles' births: how many distinct ends, how many pairs of births reach each, and how many values each
triangle's own part of the end takes (more than the grid's side when it hangs on the other triangle's birth).
Usage: python3 -I write.py <node-all src> <the click world's universe.json> [rounds] [grid] [grid rounds]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
GRID = int(sys.argv[4]) if len(sys.argv) > 4 else 12
GRID_ROUNDS = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
chosen = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["chosen"]
TIE2, KEY = int(chosen["tie"]), int(chosen["key"])
W = 600000000  # the click world's rest teeth (node-all's loader: gearing's rest)
GEAR = W + W
SPOKES, SENSES = 6, 2
HALF, _ = carry(SPOKES, SENSES, 0)  # kappa / two
D = HALF * KEY
G = 3
GD = G * D
N = 6
TRI = [[(0, 1), (1, 2), (0, 2)], [(3, 4), (4, 5), (3, 5)]]
HANDS = [[0, 1, 2], [3, 4, 5]]
BANDS = TRI[0] + TRI[1] + [(0, 3)]
C = [1, 1, -1]  # each triangle's boundary on its sorted edges


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


def lw(p, r, u, v):
    return p[u] * r[v] - p[v] * r[u]


def passings(b, a, a1, edges):
    return [HALF * TIE2 * (lw(a, a1, u, v) + lw(b, a, u, v)) for u, v in edges]


def own(a, b):
    """Each clock's own energy with half of each of its bands' cross terms (E32's terms)."""
    out = [16 * W * W * (a[i] - b[i]) * (a[i] - b[i]) for i in range(N)]
    for i, j in BANDS:
        cross = 8 * W * TIE2 * (a[i] * b[j] + a[j] * b[i])
        out[i] += 16 * W * TIE2 * a[i] * b[i] + cross
        out[j] += 16 * W * TIE2 * a[j] * b[j] + cross
    return out


def record(x, f, tau):
    y = sum(c * xe for c, xe in zip(C, x))
    f1 = []
    for e in range(3):
        _, fe = carry(G * x[e] - C[e] * y, GD, f[e])
        f1.append(fe)
    w, tau1 = carry(y, GD, tau)
    return f1, tau1, w


def whole_turn(a, b, s, f, t, w):
    """turns.py's write: the hands' whole state and the triangle's edge teeth turned by the cycle."""
    h = HANDS[t]
    a, b, s = list(a), list(b), list(s)
    for _ in range(carry(w, 3, 0)[1]):
        for v in (a, b, s):
            v[h[0]], v[h[1]], v[h[2]] = v[h[2]], v[h[0]], v[h[1]]
        f = [GD - 1 - f[2], f[0], GD - 1 - f[1]]
    return a, b, s, f


def momenta_turn(a, b, s, f, t, w):
    """The hands' exact momenta P = 2 G (a - b) + s turned by the cycle, the counts kept: the teeth alone move."""
    h = HANDS[t]
    s = list(s)
    for _ in range(carry(w, 3, 0)[1]):
        p = [GEAR * (a[i] - b[i]) + GEAR * (a[i] - b[i]) + s[i] for i in h]
        turned = [p[2], p[0], p[1]]
        for k, i in enumerate(h):
            s[i] = turned[k] - GEAR * (a[i] - b[i]) - GEAR * (a[i] - b[i])
    return a, b, s, f


def run(a, b, s, fs, taus, rounds, write, log=None):
    a, b, s = list(a), list(b), list(s)
    fs, taus = [list(f) for f in fs], list(taus)
    books = writes = jumps = 0
    e_low = e_high = sum(own(a, b))
    for _ in range(rounds):
        a1, s1 = round_(a, b, s)
        x = passings(b, a, a1, BANDS)
        e0 = own(a, b)
        share = [4 * W * (a1[i] - b[i]) * (s[i] - s1[i]) for i in range(N)]
        na, nb, ns = a1, list(a), s1
        for t in range(2):
            fs[t], taus[t], w = record(passings(b, a, a1, TRI[t]), fs[t], taus[t])
            if write is not None and w:
                before = sum(own(na, nb))
                na, nb, ns, fs[t] = write(na, nb, ns, fs[t], t, w)
                writes += 1
                jumps += sum(own(na, nb)) != before
        e1 = own(na, nb)
        for i in range(N):
            net = sum((1 if u == i else -1 if v == i else 0) * xe for (u, v), xe in zip(BANDS, x))
            books += HALF * (e1[i] - e0[i] - share[i]) == 8 * W * net
        a, b, s = na, nb, ns
        total = sum(e1)
        e_low, e_high = min(e_low, total), max(e_high, total)
        if log is not None:
            log.append(list(a))
    return (a, b, s, fs, taus), books, writes, jumps, e_low, e_high


def mirror(a, b, s):
    return list(b), list(a), [-1 - v for v in s]


def per_mille(n, d):
    return carry(1000 * n + carry(d, 2, 0)[0], d, 0)[0]


A0 = [40, -20, -20, -20, 40, -20]  # A laid as turns.py's turning lay, B as that lay turned once
B0 = [20, -40, 20, -40, 20, 20]
F0 = [[born(GD)] * 3, [born(GD)] * 3]
T0 = [born(GD), 0]
print(f"two triangles of like hands joined by one band (0, 3); {ROUNDS} rounds; the hands' tie {TIE2}, W {W}, each"
      f" triangle's dial G D {GD}; A laid {A0[:3]} now and {B0[:3]} before, B {A0[3:]} and {B0[3:]}", flush=True)
base = None
for name, write in (("none", None), ("the whole turn", whole_turn), ("the momenta turn", momenta_turn)):
    log = []
    end, books, writes, jumps, e_low, e_high = run(A0, B0, [0] * N, F0, T0, ROUNDS, write, log)
    ma, mb, ms = mirror(end[0], end[1], end[2])
    back, _, _, _, _, _ = run(ma, mb, ms, end[3], end[4], ROUNDS, write)
    ba, bb, bs = mirror(back[0], back[1], back[2])
    exact = (ba, bb, bs) == (A0, B0, [0] * N) and back[3] == F0 and back[4] == T0
    widest = max(abs(v).bit_length() for x in log for v in x)
    print(f"== {name}: writes {writes}; each clock's books, read across the write, in {books} of {N * ROUNDS}; E32"
          f" moved at {jumps} of {writes} writes; E32's narrowest {per_mille(e_low, e_high)} per mille of its widest;"
          f" widest count {widest} bits; the run back by the same act exact: {exact}", flush=True)
    if base is None:
        base = log
    else:
        rest = [sum(1 for x, y in zip(log, base) if x[k] != y[k]) for k in (3, 0)]
        print(f"   B's clock 3 apart from the unwritten path in {rest[0]} rounds, A's clock 0 in {rest[1]}", flush=True)
print(f"== the ends over a grid of {GRID} x {GRID} births of A's and B's taus, {GRID_ROUNDS} rounds", flush=True)
for name, write in (("none", None), ("the momenta turn", momenta_turn)):
    ends = {}
    for i in range(GRID):
        for j in range(GRID):
            births = [carry(i * GD, GRID, 0)[0], carry(j * GD, GRID, 0)[0]]
            end, _, _, _, _, _ = run(A0, B0, [0] * N, F0, births, GRID_ROUNDS, write)
            ends.setdefault((tuple(end[0]), tuple(end[1])), []).append((i, j))
    sizes = sorted(len(v) for v in ends.values())
    parts = [len({(k[0][3 * t:3 * t + 3], k[1][3 * t:3 * t + 3]) for k in ends}) for t in range(2)]
    print(f"   {name}: {len(ends)} distinct board ends over {GRID * GRID} pairs of births;"
          f" pairs per end from {sizes[0]} to {sizes[-1]}; A's own part of the end takes {parts[0]} values,"
          f" B's {parts[1]}", flush=True)
print("exit", flush=True)
