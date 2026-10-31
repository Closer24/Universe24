"""The equilateral triangle (the owner's word of about 09:30 UTC: "Check what an equilateral triangle gives, because that
seems to me the way"; the Boss's 6541793641): three clocks at one W, every pair joined by one edge, in whole numbers and
Rule3's carry (the engine's gear form: the momentum n = 2 d_in (a - b) + 4 push + s split at 2 d_out, by one carry from
the dial's half). Each edge is of one of two kinds: the hands' tie's, t x_i x_j (two legs), or the tie's, c x_i^2 x_j^2
(four legs). Road B's round, read faithfully: the clocks split into an explicit side, stepping first by the engine's
own gear (dial 2 W, every push at the now slot, the own spring among them), and a dialed side, each on dials polarized
over the explicit clocks' edges, d = 2 W + g_e, g_e = s + SUM over its four-leg edges to explicit clocks of
c x(start) x(end), its push -(g_in + g_out) a; a four-leg edge inside one side is pushed at the now slot on both legs.
Readings: E32 = 32 W E (the kinetic, the dialed clocks' whole edge energy, every other term polarized at the edge (b, a),
a four-leg edge inside a side as c (x_i(b) x_i(a)) (x_j(b) x_j(a))) against the exact teeth's share each round; the
widest count; the run back from the end state alone; the triangle's three turns and three flips (S_3), the lay turned
against the run turned.
Usage: python3 -I equil.py <src> [rounds, 5000 unless given]
"""
import itertools
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
W, S = 600000000, 100000000  # the click world's rest teeth and its held spring (examples/tensor24-click)
TIE2, TIE4 = 96000, 60000  # the click world's hands' tie and its tie's factor hold f
LAY = (40, 0, 1)  # the click world's lay: the giver at 40, the taker at 0, the held hand at 1, each at rest
MOVING = (40, 20, 1)  # every clock moving: a clock at 0 at rest feels no push from a product edge, and stays there
D = W + W


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def gear(a, b, s, d_in, d_out, push):
    q, kept = split(d_in * (a - b) + d_in * (a - b) + 4 * push + s, d_out)
    return a + q, kept


class World:
    def __init__(self, edges, springs, dialed):
        self.edges, self.springs, self.dialed = edges, springs, set(dialed)

    def g(self, i, x, y):
        """A dialed clock's coefficient of its own square on the edge (x, y): its own spring and its four-leg edges to
        explicit clocks, polarized."""
        out = self.springs[i]
        for (u, v), kind in self.edges.items():
            if kind == "four" and i in (u, v):
                j = v if u == i else u
                if j not in self.dialed:
                    out += TIE4 * x[j] * y[j]
        return out

    def explicit_push(self, i, a, whole):
        """The pushes at the now slot on clock i: on an explicit clock every term (whole=True); on a dialed one only its
        edges inside its own side."""
        f = -2 * self.springs[i] * a[i] if whole else 0
        for (u, v), kind in self.edges.items():
            if i not in (u, v):
                continue
            j = v if u == i else u
            inside = (j in self.dialed) == (i in self.dialed)
            if whole or inside:
                f += -TIE2 * a[j] if kind == "two" else -2 * TIE4 * a[i] * a[j] * a[j]
        return f

    def round_(self, st):
        a, b, s = st
        a1, s1 = list(a), list(s)
        for i in range(3):  # the explicit side first, by the engine's own gear
            if i not in self.dialed:
                a1[i], s1[i] = gear(a[i], b[i], s[i], D, D, self.explicit_push(i, a, True))
        for i in range(3):  # then the dialed side on dials polarized over the explicit clocks' edges
            if i in self.dialed:
                g_in, g_out = self.g(i, b, a), self.g(i, a, a1)
                push = self.explicit_push(i, a, False) - (g_in + g_out) * a[i]
                a1[i], s1[i] = gear(a[i], b[i], s[i], D + g_in, D + g_out, push)
        return a1, list(a), s1

    def e32(self, st):
        a, b, _ = st
        e = 0
        for i in range(3):
            e += 16 * W * W * (a[i] - b[i]) * (a[i] - b[i])
            if i in self.dialed:
                g = self.g(i, b, a)
                e += 16 * W * g * (a[i] * a[i] + b[i] * b[i]) + 4 * g * g * (a[i] + b[i]) * (a[i] + b[i])
            else:
                e += 16 * W * self.springs[i] * (b[i] * a[i] + a[i] * b[i])
        for (u, v), kind in self.edges.items():
            inside = (u in self.dialed) == (v in self.dialed)
            if kind == "two":
                e += 16 * W * TIE2 * (b[u] * a[v] + a[u] * b[v])
            elif inside:
                e += 32 * W * TIE4 * (b[u] * a[u]) * (b[v] * a[v])
        return e

    def share(self, st, st1):
        a, b, s = st
        a1, _, s1 = st1
        out = 0
        for i in range(3):
            g_in = self.g(i, b, a) if i in self.dialed else 0
            g_out = self.g(i, a, a1) if i in self.dialed else 0
            out += (s[i] - s1[i]) * (4 * W * (a1[i] - b[i]) + 2 * g_out * (a[i] + a1[i]) - 2 * g_in * (a[i] + b[i]))
        return out


def mirror(st):
    a, b, s = st
    return list(b), list(a), [-1 - x for x in s]


def run(w, st, rounds):
    for _ in range(rounds):
        st = w.round_(st)
    return st


def turned(p, w):
    """The world with its clocks relabelled by p: clock i of the new world is clock p[i] of the old."""
    inv = {p[i]: i for i in range(3)}
    edges = {tuple(sorted((inv[u], inv[v]))): kind for (u, v), kind in w.edges.items()}
    return World(edges, [w.springs[p[i]] for i in range(3)], [inv[i] for i in w.dialed])


def read(name, w, lay=LAY):
    st0 = (list(lay), list(lay), [0, 0, 0])
    st, kept, widest = st0, 0, 0
    for _ in range(ROUNDS):
        st1 = w.round_(st)
        kept += 1 if w.e32(st1) - w.e32(st) == w.share(st, st1) else 0
        widest = max([widest] + [abs(x).bit_length() for x in st1[0]])
        st = st1
    back = mirror(run(w, mirror(st), ROUNDS)) == st0
    alike = 0
    for p in itertools.permutations(range(3)):
        moved = tuple([x[p[i]] for i in range(3)] for x in st0)
        u = run(w, moved, 50)
        v = run(w, st0, 50)
        alike += 1 if u == tuple([x[p[i]] for i in range(3)] for x in v) else 0
    print(f"{name}, the lay {lay}: E32's change = the teeth's share in {kept} of {ROUNDS} rounds; widest count {widest} bits; the run"
          f" back exact: {back}; the round turned alike with the lay in {alike} of the 6 turns and flips", flush=True)
