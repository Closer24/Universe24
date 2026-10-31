"""David's one cell on the board (6542802335 item 2, for Big Pic's one algebra): the click world's triangle with its two
four-leg ties and its band read as the square of one cell, f (h (g + u))^2 = f h^2 g^2 + f h^2 u^2 + 2 f h^2 g u, g the
giver, u the taker, h the held hand, f the tie at hold 1 (W div Gamma, the click world's 60,000), beside the held hand's
own spring S h^2 (Gamma^2, the click world's 100,000,000). Nothing else is laid: the band is 2 f h^2, no 96,000.
Road B's round, as in equil.py: the giver and the taker step first by the engine's own gear (dial 2 W, every push at the
now slot); the held hand is dialed, d = 2 W + g_e, g_e = S + f G(start) G(end), G = g + u its partners' together count,
its push -(g_in + g_out) h. The cell is quadratic in h given g and u, so the dial carries all of it.
Readings, per lay, ROUNDS rounds: E32 = 32 W E against the teeth's share each round (the identity); the run back from the
end state alone; the swap of the giver and the taker, the lay swapped against the run swapped; the widest count; the
opposite swing g - u, the together swing g + u and the held hand, each with its range and its step at the end; the
round at which the held hand's lend f h^2 reaches W, where the together swing's explicit step meets its limit (its
leapfrog factor 8 f h^2 / 2 W reaches 4), and the round at which a count passes 64 bits.
The control: equil.py's click world triangle as shipped (the ties f g^2 h^2 and f u^2 h^2, the laid band 96,000 g u).
Usage: python3 -I cell.py <src> [rounds, 5000 unless given]
"""
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
W, S = 600000000, 100000000  # the click world's rest teeth and its held spring (examples/tensor24-click)
F, BAND = 60000, 96000  # the tie at hold 1, and the shipped world's laid band (the control only)
D = W + W


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def gear(a, b, s, d_in, d_out, push):
    q, kept = split(d_in * (a - b) + d_in * (a - b) + 4 * push + s, d_out)
    return a + q, kept


class Triangle:
    """cell=True: S h^2 + f (h (g + u))^2. cell=False: S h^2 + f g^2 h^2 + f u^2 h^2 + BAND g u (the shipped triangle)."""

    def __init__(self, cell):
        self.cell = cell

    def g(self, x, y):
        if self.cell:
            return S + F * (x[0] + x[1]) * (y[0] + y[1])
        return S + F * (x[0] * y[0] + x[1] * y[1])

    def round_(self, st):
        a, b, s = st
        a1, s1 = list(a), list(s)
        held = a[2] * a[2]
        for i in (0, 1):
            j = 1 - i
            if self.cell:
                push = -2 * F * held * (a[i] + a[j])
            else:
                push = -2 * F * held * a[i] - BAND * a[j]
            a1[i], s1[i] = gear(a[i], b[i], s[i], D, D, push)
        g_in, g_out = self.g(b, a), self.g(a, a1)
        a1[2], s1[2] = gear(a[2], b[2], s[2], D + g_in, D + g_out, -(g_in + g_out) * a[2])
        return a1, list(a), s1

    def e32(self, st):
        a, b, _ = st
        e = 0
        for i in range(3):
            e += 16 * W * W * (a[i] - b[i]) * (a[i] - b[i])
        g = self.g(b, a)
        e += 16 * W * g * (a[2] * a[2] + b[2] * b[2]) + 4 * g * g * (a[2] + b[2]) * (a[2] + b[2])
        if not self.cell:
            e += 16 * W * BAND * (b[0] * a[1] + a[0] * b[1])
        return e

    def share(self, st, st1):
        a, b, s = st
        a1, _, s1 = st1
        out = 0
        for i in range(3):
            g_in = self.g(b, a) if i == 2 else 0
            g_out = self.g(a, a1) if i == 2 else 0
            out += (s[i] - s1[i]) * (4 * W * (a1[i] - b[i]) + 2 * g_out * (a[i] + a1[i]) - 2 * g_in * (a[i] + b[i]))
        return out


def mirror(st):
    a, b, s = st
    return list(b), list(a), [-1 - x for x in s]


def swapped(st):
    return tuple([x[1], x[0], x[2]] for x in st)


def run(w, st, rounds):
    for _ in range(rounds):
        st = w.round_(st)
    return st


def read(name, w, now, before, rounds=ROUNDS):
    st0 = (list(now), list(before), [0, 0, 0])
    st, kept, widest = st0, 0, 0
    ranges = {"opposite": [], "together": [], "held": []}
    limit = past = None
    for n in range(1, rounds + 1):
        st1 = w.round_(st)
        kept += 1 if w.e32(st1) - w.e32(st) == w.share(st, st1) else 0
        widest = max([widest] + [abs(x).bit_length() for x in st1[0]])
        a = st1[0]
        ranges["opposite"].append(a[0] - a[1])
        ranges["together"].append(a[0] + a[1])
        ranges["held"].append(a[2])
        if limit is None and F * a[2] * a[2] >= W:
            limit = (n, max(abs(x) for x in ranges["held"]))
        if past is None and max(abs(x) for x in a).bit_length() > 64:
            past = n
        st = st1
    back = mirror(run(w, mirror(st), rounds)) == st0
    swap = run(w, swapped(st0), rounds) == swapped(st)
    a, b, _ = st
    steps = {"opposite": (a[0] - a[1]) - (b[0] - b[1]), "together": (a[0] + a[1]) - (b[0] + b[1]), "held": a[2] - b[2]}
    print(f"== {name}: the lay {now} now, {before} before; {rounds} rounds", flush=True)
    print(f"   E32's change = the teeth's share in {kept} of {rounds} rounds; widest count {widest} bits; the run back exact:"
          f" {back}; the giver and the taker swapped, alike: {swap}", flush=True)
    if limit is not None:
        print(f"   the held hand's lend f h^2 reaches the rest teeth W (the explicit step's limit for the cell's together"
              f" swing, 8 f h^2 / 2 W = 4) at round {limit[0]}, the held hand then at {limit[1]}; a count passes 64 bits at"
              f" round {past}", flush=True)
    for key, vals in ranges.items():
        lo, hi = min(vals), max(vals)
        if max(abs(lo), abs(hi)).bit_length() > 64:
            print(f"   the {key} swing: past 64 bits ({max(abs(lo), abs(hi)).bit_length()} bits)", flush=True)
        else:
            print(f"   the {key} swing: from {lo} to {hi}, at the end {vals[-1]}, its step at the end {steps[key]}", flush=True)


print(f"W {W}, the held spring S {S}, the tie f {F}; the cell's band 2 f h^2, {2 * F} at h = 1; the shipped band {BAND}",
      flush=True)
cell, shipped = Triangle(True), Triangle(False)
for w, label in ((cell, "the one cell f (h (g + u))^2"), (shipped, "the control, the shipped triangle")):
    read(f"{label}, the click world's lay at rest", w, (40, 0, 1), (40, 0, 1))
    read(f"{label}, the opposite swing laid moving", w, (40, 0, 1), (39, 1, 1))
    read(f"{label}, the together swing laid moving", w, (40, 0, 1), (39, -1, 1))
    read(f"{label}, the giver at ten times its count, the held hand at its unit, at rest", w, (400, 0, 1), (400, 0, 1))
    read(f"{label}, every count at ten times, at rest (past the gear's grain: f h^2 outgrows the dial)", w, (400, 0, 10),
         (400, 0, 10), 300)
print("exit", flush=True)
