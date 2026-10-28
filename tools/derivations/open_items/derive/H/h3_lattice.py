"""Draft H, probe h3_lattice: the whole tick's time reversal on a small great clock (pure integers; python3 -I).

A periodic L^3 great clock in the head's act order (tick.py): at every Node-clock a regulator time gear X
(fixed teeth TR) with its drive's fine tooth (fixed drive teeth DD), and one hand (three, twelve) whose two
gears ride at the mean teeth W = c (X_before + X_now). One tick M:
  (1) every hand's stride P = W (now - before) + r - o(W, b) and its impulse P' = P + X_now F, F the Meshes'
      pull and the spring, read from the notches now; the forms SUM P P' (even under T and under the sign);
  (2) the regulator: its stride PX, the pull of its six Meshes and its own spring toward X0, the drive's carry
      q = (kappa X_now forms + d) div DD landing as the kick TR q, one carry at TR;
  (3) the turnover's trigger on (X_before, X_now, X_next); every hand gear carried at W+ = c (X_now + X_next);
  (4) where the trigger fires, the Node-clock ends the tick at its start state reversed: the regulator and the
      three gear exchanged and reflected, the twelve gear exchanged and negated (the head's K), the drive's
      fine tooth reflected.
T is that reversal at every Node-clock. The variants are h3_rewind's MIRROR (the head) and FRAME (this draft).

Checks (counts of failures over random states; FRAME must show 0 everywhere, MIRROR fails at even counts):
  TMTM   T M T M x == x            (the tick's rewind with no log, M^-1 = T M T)
  CIRCLE T M^n T M^n x == x         (law 10's circle: forward, turnover, the retrace, turnover)
  24     M(g x) == g M(x), g a quarter turn of the great clock with the hand's sign (the 24's image)
  LAW1   every fine tooth inside its teeth
Usage: python3 -I h3_lattice.py [--mutant NAME]
"""

import random
import sys

L = 3
SITES = [(x, y, z) for x in range(L) for y in range(L) for z in range(L)]
NB = {s: [((s[0] + dx) % L, (s[1] + dy) % L, (s[2] + dz) % L)
          for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
      for s in SITES}
MUTANT = None


def origin(variant, w, b):
    if variant == "FRAME":
        if MUTANT == "origin":
            return (w + b) // 2
        return (w - b) // 2
    return w // 2


def reflect(variant, r, w, b):
    """The fine tooth's reflection for one reversal of its gear, and the new going."""
    if variant == "FRAME":
        if MUTANT == "mirror":
            return (2 * origin(variant, w, b) - r) % w, 1 - b
        if MUTANT == "keep":
            return w - 1 - r, b
        return w - 1 - r, 1 - b
    return (2 * (w // 2) - r) % w, b


def rev_gear(variant, g, w):
    """Time's reversal of one gear: the slots exchanged, the fine tooth reflected once."""
    now, before, r, b = g
    r2, b2 = reflect(variant, r, w, b)
    return (before, now, r2, b2)


def neg_gear(variant, g, w):
    """The gear's sign: both notches negated, the fine tooth reflected once (a reversal of the gear)."""
    now, before, r, b = g
    r2, b2 = reflect(variant, r, w, b)
    return (-now, -before, r2, b2)


def reflect_drive(variant, d, D):
    if variant == "FRAME" and MUTANT != "drive":
        return D - 1 - d
    return (2 * (D // 2) - d) % D


class Toy:
    def __init__(self, variant, TR, c, DD, g, D, gX, DX, X0, kappa, trigger):
        self.v, self.TR, self.c, self.DD = variant, TR, c, DD
        self.g, self.D, self.gX, self.DX, self.X0, self.kappa = g, D, gX, DX, X0, kappa
        self.trigger = trigger

    def W(self, X):
        return self.c * (X[1] + X[0])

    def stride(self, gear, w):
        now, before, r, b = gear
        return w * (now - before) + r - origin(self.v, w, b)

    def carry(self, total, w, b):
        return divmod(total + origin(self.v, w, b), w)

    def M(self, st):
        v = self.v
        out = {}
        imp, forms = {}, {}
        self.turned = 0
        for s in SITES:
            X, dX, a3, a12, pawl = st[s]
            w = self.W(X)
            p = []
            for k, gear in ((0, a3), (1, a12)):
                # the Mesh read through the pawl: the neighbour's twelve gear read negated where the pawls differ
                F = self.g * sum(self.seen(st[n], k, pawl) - gear[0] for n in NB[s]) - self.D * gear[0]
                P = self.stride(gear, w)
                p.append((P, P + X[0] * F))
            imp[s] = p
            forms[s] = sum(P * Q for P, Q in p)
        for s in SITES:
            X, dX, a3, a12, pawl = st[s]
            w = self.W(X)
            PX = self.stride(X, self.TR)
            FX = self.gX * sum(st[n][0][0] - X[0] for n in NB[s]) - self.DX * (X[0] - self.X0)
            q, dX2 = divmod(self.kappa * forms[s] + dX, self.DD)
            dx, rX2 = self.carry(PX + FX + self.TR * q, self.TR, X[3])
            Xn = (X[0] + dx, X[0], rX2, X[3])
            if self.trigger(X[1], X[0], Xn[0]):
                out[s] = self.reverse(st[s])
                self.turned += 1
                continue
            w2 = self.c * (X[0] + Xn[0])
            if w2 < 1:
                raise ArithmeticError("the end teeth at or below 0: the step is undefined")
            gears = []
            for k, gear in ((0, a3), (1, a12)):
                d, r2 = self.carry(imp[s][k][1], w2, gear[3])
                gears.append((gear[0] + d, gear[0], r2, gear[3]))
            out[s] = (Xn, dX2, gears[0], gears[1], pawl)
        return out

    def seen(self, site, k, pawl):
        now = site[2 + k][0]
        if k == 1 and site[4] != pawl and MUTANT != "nopawl":
            return -now
        return now

    def reverse(self, site):
        X, dX, a3, a12, pawl = site
        w = self.W(X)
        a12r = rev_gear(self.v, a12, w)
        return (rev_gear(self.v, X, self.TR), reflect_drive(self.v, dX, self.DD), rev_gear(self.v, a3, w),
                neg_gear(self.v, a12r, w), 1 - pawl)

    def T(self, st):
        return {s: self.reverse(st[s]) for s in SITES}

    def g24(self, st):
        """A quarter turn of the great clock about z with the hand's sign (both gears negated)."""
        out = {}
        for (x, y, z), (X, dX, a3, a12, pawl) in st.items():
            w = self.W(X)
            out[((-y) % L, x, z)] = (X, dX, neg_gear(self.v, a3, w), neg_gear(self.v, a12, w), pawl)
        return out

    def law1(self, st):
        bad = 0
        for s in SITES:
            X, dX, a3, a12, pawl = st[s]
            w = self.W(X)
            bad += not (0 <= X[2] < self.TR) + 0
            bad += not (0 <= dX < self.DD)
            bad += sum(not (0 <= gear[2] < w) for gear in (a3, a12))
        return bad


def weak_max(x0, x1, x2):
    return x0 <= x1 and x2 <= x1 and (x0 < x1 or x2 < x1)


def weak_min(x0, x1, x2):
    return x0 >= x1 and x2 >= x1 and (x0 > x1 or x2 > x1)


def union(x0, x1, x2):
    return weak_max(x0, x1, x2) or weak_min(x0, x1, x2)


def asym(x0, x1, x2):
    return x0 < x1 and x2 <= x1  # an asymmetric trigger: a rise into the top alone (the law's own example)


def random_state(toy, rng, xs):
    st = {}
    for s in SITES:
        Xn = rng.randint(xs[0], xs[1])
        Xb = Xn - rng.randint(-2, 2)
        b = rng.randint(0, 1) if toy.v == "FRAME" else 0
        X = (Xn, Xb, rng.randint(0, toy.TR - 1), b)
        w = toy.c * (Xb + Xn)
        hand = []
        for _k in range(2):
            now = rng.randint(-2, 2)
            hand.append((now, now - rng.randint(-1, 1), rng.randint(0, w - 1),
                         rng.randint(0, 1) if toy.v == "FRAME" else 0))
        st[s] = (X, rng.randint(0, toy.DD - 1), hand[0], hand[1], rng.randint(0, 1))
    return st


def positive(st):
    return all(st[s][0][0] > 0 and st[s][0][1] > 0 for s in SITES)


def run(variant, TR, c, DD, trigger, trials, rng, ticks=12):
    toy = Toy(variant, TR, c, DD, g=1, D=2, gX=1, DX=1, X0=30, kappa=1, trigger=trigger)
    fails = {"TMTM": 0, "CIRCLE": 0, "24": 0, "LAW1": 0, "turned": 0, "ran": 0, "circles": 0}
    for _ in range(trials):
        x = random_state(toy, rng, (25, 35))
        try:
            y = toy.M(x)
            turned = toy.turned
            if not positive(y):
                continue
            back = toy.T(toy.M(toy.T(y)))
            image = toy.M(toy.g24(x))
        except ArithmeticError:
            continue
        fails["ran"] += 1
        fails["turned"] += turned
        fails["TMTM"] += back != x
        fails["24"] += image != toy.g24(y)
        fails["LAW1"] += toy.law1(y) > 0
        try:
            z = x
            for _k in range(ticks):
                z = toy.M(z)
                fails["turned"] += toy.turned
                assert positive(z)
            u = toy.T(z)
            for _k in range(ticks):
                u = toy.M(u)
                assert positive(u)
        except (ArithmeticError, AssertionError):
            continue
        fails["circles"] += 1
        fails["CIRCLE"] += toy.T(u) != x
    return fails


def main(argv):
    global MUTANT
    if "--mutant" in argv:
        MUTANT = argv[argv.index("--mutant") + 1]
    rng = random.Random(28102026)
    triggers = (("weak top", weak_max), ("top or bottom", union))
    if MUTANT == "asym":
        triggers = (("asymmetric top", asym),)
    for variant in ("MIRROR", "FRAME"):
        if MUTANT and variant == "MIRROR":
            continue
        for TR, c, DD, label in ((10, 2, 50000, "TR 10, W = 2 (X- + X) even, DD 50000"),
                                 (11, 5, 49999, "TR 11, W = 5 (X- + X) of either parity, DD 49999"),
                                 (12, 3, 50000, "TR 12, W = 3 (X- + X) of either parity, DD 50000"),
                                 (9, 3, 49999, "TR 9, W = 3 (X- + X) of either parity, DD 49999")):
            for tname, trig in triggers:
                f = run(variant, TR, c, DD, trig, 300, rng)
                tag = f"MUT {MUTANT}" if MUTANT else variant
                print(f"{tag:12s} {label:50s} {tname:14s} ran {f['ran']:3d} (circles {f['circles']:3d}), "
                      f"turnovers {f['turned']:5d}: TMTM {f['TMTM']:3d}  CIRCLE {f['CIRCLE']:3d}  24 {f['24']:3d}  "
                      f"LAW1 {f['LAW1']:3d}")


if __name__ == "__main__":
    main(sys.argv[1:])
