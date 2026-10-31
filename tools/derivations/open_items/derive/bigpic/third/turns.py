"""The third click that writes and chooses, a first stand-alone model (the owner's words of 12:23, 12:25 and 12:28 UTC:
"Only the third click writes to the board and chooses... it is the important one"; "The clicks' floor, from their
structure alone..."; "the first 2 clicks represent the initial conditions of the universe; the third, the choices that
change the universe from the path without the choices"; the Boss's 6543327690, 6543337835 and 6543366692).
Three like hands on one triangle of bands, each band its own square (t/2)(x_i + x_j)^2 at the click world's hands' tie,
with no own spring laid and no held hand: the frustrated loop that holds a floor by itself (frustration.py). The round
is the engine's gear form (frustration.py), whole numbers and Rule3's carry only. The triangle's one tooth tau carries
the circulation of the bands' passings (tooth.py's member, unturned), and at each landing w the third click writes on
its own triangle: it turns the three hands' whole state (counts, teeth, and the triangle's edge teeth) by the cycle
(0 1 2) taken w times. The turn is a symmetry of the triangle's law, so the round commutes with it, and the
circulation and the total energy are kept by it. Each clock's books, read per clock, are not: a write moves each
clock's whole state and its energy to the next clock, which no side carries (the THIRD pair's B1, NOT PASSED).
Readings, per lay and per birth of tau: E32's change against the teeth's share at every round (the turn included); the
widest count (the floor); the turned path against the path with no writes: every round's three states alike as a set,
and the rounds where a clock's own count differs (the writes seen in the lines); the net turn over the run, modulo 3,
and the end against the unwritten end; the run back from the end state alone, the writes part of the state.
Usage: python3 -I turns.py <node-all src> <the click world's universe.json> [rounds]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
chosen = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["chosen"]
TIE2, KEY = int(chosen["tie"]), int(chosen["key"])
W = 600000000  # the click world's rest teeth (node-all's loader: gearing's rest)
GEAR = W + W
SPOKES, SENSES = 6, 2
HALF, _ = carry(SPOKES, SENSES, 0)  # kappa / two
D = HALF * KEY
EDGES = [(0, 1), (1, 2), (0, 2)]
C = [1, 1, -1]  # the triangle's boundary on its sorted edges
G = 3
GD = G * D


def born(dial):
    return carry(dial - 1, SENSES, 0)[0]


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def pushes(a):
    """Each band (t/2)(x_i + x_j)^2 pushes both its hands by -t (x_i + x_j)."""
    f = [0, 0, 0]
    for i, j in EDGES:
        p = -TIE2 * (a[i] + a[j])
        f[i] += p
        f[j] += p
    return f


def round_(a, b, s):
    f = pushes(a)
    a1, s1 = [], []
    for i in range(3):
        q, kept = split(GEAR * (a[i] - b[i]) + GEAR * (a[i] - b[i]) + 4 * f[i] + s[i], GEAR)
        a1.append(a[i] + q)
        s1.append(kept)
    return a1, s1


def energy(a, b):
    e = sum(16 * W * W * (x - y) * (x - y) for x, y in zip(a, b))
    for i, j in EDGES:
        e += 16 * W * TIE2 * (a[i] + a[j]) * (b[i] + b[j])
    return e


def share(b, a1, s, s1):
    return sum(4 * W * (z - y) * (p - r) for z, y, p, r in zip(a1, b, s, s1))


def lw(p, r, u, v):
    return p[u] * r[v] - p[v] * r[u]


def passings(b, a, a1):
    """The bands' cross terms t x_u x_v pass along their edges (the own squares pass nothing): tooth.py's form."""
    return [HALF * TIE2 * (lw(a, a1, u, v) + lw(b, a, u, v)) for u, v in EDGES]


def record(x, f, tau):
    """The triangle's tooth (tooth.py's member): each edge carries G x_e - c_e y at G D, tau carries y at G D."""
    y = sum(c * xe for c, xe in zip(C, x))
    f1 = []
    for e in range(3):
        _, fe = carry(G * x[e] - C[e] * y, GD, f[e])
        f1.append(fe)
    w, tau1 = carry(y, GD, tau)
    return f1, tau1, w


def turn_once(a, b, s, f):
    """The cycle (0 1 2) once: clock i's whole state moves to clock i + 1. Edge (0, 1) goes to (1, 2) as it stands;
    edge (1, 2) goes to (2, 0), which is edge (0, 2) read from its other end; edge (0, 2) goes to (1, 0), which is edge
    (0, 1) read from its other end. A tooth read from its other end is G D - 1 - itself (the carry's sign law)."""
    na, nb, ns = [a[2], a[0], a[1]], [b[2], b[0], b[1]], [s[2], s[0], s[1]]
    nf = [GD - 1 - f[2], f[0], GD - 1 - f[1]]
    return na, nb, ns, nf


def turn(a, b, s, f, w):
    times = carry(w, 3, 0)[1]
    for _ in range(times):
        a, b, s, f = turn_once(a, b, s, f)
    return a, b, s, f


def run(a, b, s, f, tau, rounds, writes=True, log=None):
    a, b, s, f = list(a), list(b), list(s), list(f)
    held = widest = net = 0
    for _ in range(rounds):
        a1, s1 = round_(a, b, s)
        f1, tau1, w = record(passings(b, a, a1), f, tau)
        e0 = energy(a, b)
        sh = share(b, a1, s, s1)
        na, nb, ns, nf = a1, list(a), s1, f1
        if writes:
            na, nb, ns, nf = turn(na, nb, ns, nf, w)
        held += energy(na, nb) - e0 == sh
        net += w
        a, b, s, f, tau = na, nb, ns, nf, tau1
        widest = max([widest] + [abs(x).bit_length() for x in a])
        if log is not None:
            log.append((list(a), w))
    return (a, b, s, f, tau), held, widest, net


def mirror(a, b, s):
    return list(b), list(a), [-1 - v for v in s]


def read(name, lay_a, lay_b):
    print(f"== {name}: the lay {lay_a} now, {lay_b} before; {ROUNDS} rounds; the hands' tie {TIE2}, W {W}, the"
          f" triangle's dial G D {GD}", flush=True)
    third, _ = carry(GD, 3, 0)
    for t0 in (born(GD), 0, third, third + third):
        start = (list(lay_a), list(lay_b), [0, 0, 0], [born(GD)] * 3, t0)
        log_w, log_u = [], []
        end_w, held, widest, net = run(*start, ROUNDS, True, log_w)
        end_u, _, _, net_u = run(*start, ROUNDS, False, log_u)
        alike_as_set = all(sorted(x) == sorted(y) for (x, _), (y, _) in zip(log_w, log_u))
        lines_apart = sum(1 for (x, _), (y, _) in zip(log_w, log_u) if x != y)
        net3 = carry(net, 3, 0)[1]
        turned_u = turn(end_u[0], end_u[1], end_u[2], end_u[3], net)
        end_is_turned = (end_w[0], end_w[1], end_w[2], end_w[3]) == turned_u and end_w[4] == end_u[4]
        same_end = end_w[:4] == end_u[:4]
        ma, mb, ms = mirror(end_w[0], end_w[1], end_w[2])
        back, _, _, _ = run(ma, mb, ms, end_w[3], end_w[4], ROUNDS, True)
        ba, bb, bs = mirror(back[0], back[1], back[2])
        exact = (ba, bb, bs, back[3], back[4]) == start
        print(f"   tau born at {t0}: E32's change = the teeth's share in {held} of {ROUNDS} rounds; widest count"
              f" {widest} bits; landings net {net} (unwritten {net_u}), the net turn {net3} of 3; the three states"
              f" alike as a set at every round: {alike_as_set}; a clock's own count apart from the unwritten path in"
              f" {lines_apart} rounds; the end the unwritten end turned by the net: {end_is_turned}; the end the"
              f" unwritten end itself: {same_end}; the run back exact, the writes in the state: {exact}", flush=True)


read("three like hands on a triangle of bands, laid turning in the plane", [40, -20, -20], [20, -40, 20])
read("three like hands on a triangle of bands, the hands' difference moving", [40, -40, 0], [39, -39, 0])
print("exit", flush=True)
