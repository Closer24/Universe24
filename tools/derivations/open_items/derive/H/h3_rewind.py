"""Draft H, probe h3: the exact rewind at every teeth count (pure integers, no engine; python3 -I).

A gear is (now, before, r, b) at its teeth count w: the notch now and before, the fine tooth r, and the
gear's going b (0 or 1, the parity of its reversals; read only by the FRAME variant). Its stride, in the
variant's own origin o(w, b), is P = w (now - before) + r - o(w, b). The step of one tick from the start
teeth w to the end teeth w2 (law 2): P2 = P + F(now), the carry (d, r2) = Rule3(P2 + o(w2, b), w2), the
new gear (now + d, now, r2, b). The turnover T exchanges the two notches and reflects the fine tooth; the
negation N (a gear's sign, the 24's image of a turn that negates it) negates both notches and reflects.

Variants (the head's, Animate's two candidates, the frame-free flip, and this draft's FRAME):
  MIRROR   the head: o = w div 2; T: r -> (2 o - r) mod w
  FLIP     the frame-free flip: o = w div 2; T: r -> w - 1 - r
  CARRIED  Animate (i), the mirror with its carry kept in the stride: before' = now - c, c = (2 o - r) div w
  EVEN     Animate (ii), the tie sent to the even quotient: the remainder in [0, w], T: r -> 2 o - r
  FRAME    this draft: o = (w - b) div 2; T: r -> w - 1 - r and b -> 1 - b; N alike with the notches negated

Usage: python3 -I h3_rewind.py [VARIANT ...] [--mutants]
Pass criterion (printed per line): FRAME passes every property at every parity class; a property that
cannot hold for a variant is reported with its count of failures, and the mutants (--mutants) must fail.
"""

import random
import sys

SIDES = 2  # the two sides of a Spoke: the half by the carry on 2


def rule3(n, d):
    """Rule3: n = q d + r', 0 <= r' < d (d >= 1)."""
    return divmod(n, d)


# --- the variants ---------------------------------------------------------------------------------


class Variant:
    name = "?"

    def origin(self, w, b):
        return w // SIDES

    def carry(self, total, w2, b):
        return rule3(total + self.origin(w2, b), w2)

    def stride(self, x, w):
        now, before, r, b = x
        return w * (now - before) + r - self.origin(w, b)

    def step(self, x, w, w2, force):
        now, before, r, b = x
        p2 = self.stride(x, w) + force(now)
        d, r2 = self.carry(p2, w2, b)
        return (now + d, now, r2, b)

    def T(self, x, w):
        raise NotImplementedError

    def N(self, x, w):
        raise NotImplementedError

    def in_range(self, x, w):
        return 0 <= x[2] < w


class Mirror(Variant):
    name = "MIRROR"

    def T(self, x, w):
        now, before, r, b = x
        return (before, now, (2 * self.origin(w, b) - r) % w, b)

    def N(self, x, w):
        now, before, r, b = x
        return (-now, -before, (2 * self.origin(w, b) - r) % w, b)


class Flip(Variant):
    name = "FLIP"

    def T(self, x, w):
        now, before, r, b = x
        return (before, now, w - 1 - r, b)

    def N(self, x, w):
        now, before, r, b = x
        return (-now, -before, w - 1 - r, b)


class Carried(Variant):
    name = "CARRIED"

    def T(self, x, w):
        now, before, r, b = x
        c, r2 = divmod(2 * self.origin(w, b) - r, w)
        return (before, now - c, r2, b)

    def N(self, x, w):
        now, before, r, b = x
        c, r2 = divmod(2 * self.origin(w, b) - r, w)
        return (-now, -before - c, r2, b)


class Even(Variant):
    name = "EVEN"

    def carry(self, total, w2, b):
        q, s = rule3(total + self.origin(w2, b), w2)
        tie = 1 if (w2 % 2 == 0 and s == 0) else 0
        q2 = q - tie * (q % 2)
        return q2, total + self.origin(w2, b) - w2 * q2

    def T(self, x, w):
        now, before, r, b = x
        return (before, now, 2 * self.origin(w, b) - r, b)

    def N(self, x, w):
        now, before, r, b = x
        return (-now, -before, 2 * self.origin(w, b) - r, b)


class Frame(Variant):
    name = "FRAME"

    def origin(self, w, b):
        return (w - b) // SIDES

    def T(self, x, w):
        now, before, r, b = x
        return (before, now, w - 1 - r, 1 - b)

    def N(self, x, w):
        now, before, r, b = x
        return (-now, -before, w - 1 - r, 1 - b)


# --- the mutants of FRAME (one term changed each) --------------------------------------------------


class FrameOrigin(Frame):
    name = "MUT frame origin (w + b) div 2"

    def origin(self, w, b):
        return (w + b) // SIDES


class FrameNoToggle(Frame):
    name = "MUT frame T keeps b"

    def T(self, x, w):
        now, before, r, b = x
        return (before, now, w - 1 - r, b)


class FrameMirror(Frame):
    name = "MUT frame T mirrors (2 o - r) mod w"

    def T(self, x, w):
        now, before, r, b = x
        return (before, now, (2 * self.origin(w, b) - r) % w, 1 - b)


class FrameNNoToggle(Frame):
    name = "MUT frame N keeps b"

    def N(self, x, w):
        now, before, r, b = x
        return (-now, -before, w - 1 - r, b)


VARIANTS = [Mirror(), Flip(), Carried(), Even(), Frame()]
MUTANTS = [FrameOrigin(), FrameNoToggle(), FrameMirror(), FrameNNoToggle()]


# --- the states and the forces ----------------------------------------------------------------------


def teeth_pair(rng, cls, small):
    hi = 15 if small else 10**21
    lo = 2 if small else 10**20
    while True:
        w, w2 = rng.randint(lo, hi), rng.randint(lo, hi)
        if cls == "even->even" and w % 2 == 0 and w2 % 2 == 0:
            return w, w2
        if cls == "odd->odd" and w % 2 == 1 and w2 % 2 == 1:
            return w, w2
        if cls == "odd->even" and w % 2 == 1 and w2 % 2 == 0:
            return w, w2
        if cls == "even->odd" and w % 2 == 0 and w2 % 2 == 1:
            return w, w2


def a_state(rng, v, w, small, at_tie=False):
    span = 6 if small else 10**6
    now = rng.randint(-span, span)
    d = rng.randint(-3, 3) if small else rng.randint(-10**5, 10**5)
    if isinstance(v, Even):
        # a canonical state of the even-quotient carry: r in [1, w - 1], or r in {0, w} at an even stride
        r = rng.randint(0, w)
        if w % 2 == 0 and r in (0, w) and d % 2:
            d += 1
        if w % 2 == 1 and r == w:
            r = w - 1
    else:
        r = rng.randint(0, w - 1)
    if at_tie and not isinstance(v, Even):
        r = 0 if (w % 2 == 0) else r
    b = rng.randint(0, 1) if isinstance(v, Frame) else 0
    return (now, now - d, r, b)


def a_force(rng, small, odd=False):
    """A force read from the notch now alone (T-even, as every force of the step); odd under the sign if asked."""
    k = rng.randint(1, 5) if small else rng.randint(1, 10**9)
    c = 0 if odd else (rng.randint(-7, 7) if small else rng.randint(-10**12, 10**12))
    return lambda a: -k * a + c


# --- the properties ---------------------------------------------------------------------------------


def props(v, cls, small, trials, rng):
    fails = {"law1": 0, "TT": 0, "TSTi": 0, "STS": 0, "PNEG": 0, "REST": 0, "NSN": 0}
    for _ in range(trials):
        w, w2 = teeth_pair(rng, cls, small)
        x = a_state(rng, v, w, small, at_tie=(rng.random() < 0.3))
        f = a_force(rng, small)
        y = v.step(x, w, w2, f)
        fails["law1"] += not v.in_range(y, w2)
        fails["TT"] += v.T(v.T(x, w), w) != x
        # T S T = S^-1: T, then the reversed step (the teeth run back, w2 -> w), then T, lands on x = S^-1 y
        fails["TSTi"] += v.T(v.step(v.T(y, w2), w2, w, f), w) != x
        # S T S = T (the form the retrace uses, T S T = S^-1 with T T = 1): the reversed step lands on T x
        fails["STS"] += v.step(v.T(y, w2), w2, w, f) != v.T(x, w)
        fails["PNEG"] += v.stride(v.T(x, w), w) != -v.stride(x, w)
        rest = (x[0], x[0], v.origin(w, x[3]), x[3])
        fails["REST"] += v.stride(v.T(rest, w), w) != 0
        g = a_force(rng, small, odd=True)
        fails["NSN"] += v.step(v.N(x, w), w, w2, g) != v.N(v.step(x, w, w2, g), w2)
    return fails


def retrace(v, small, trials, rng, ticks=40, parity="mixed"):
    """S^n T x_n = T x_0 along a run whose teeth change from tick to tick (the retrace of law 10's circle)."""
    bad = 0
    for _ in range(trials):
        hi = 15 if small else 10**21
        lo = 2 if small else 10**20
        teeth = []
        for _k in range(ticks + 1):
            w = rng.randint(lo, hi)
            if parity == "even":
                w += w % 2
            if parity == "odd":
                w += 1 - w % 2
            teeth.append(w)
        f = a_force(rng, small)
        x0 = a_state(rng, v, teeth[0], small)
        x = x0
        for k in range(ticks):
            x = v.step(x, teeth[k], teeth[k + 1], f)
        y = v.T(x, teeth[ticks])
        for k in range(ticks, 0, -1):
            y = v.step(y, teeth[k], teeth[k - 1], f)
        bad += y != v.T(x0, teeth[0])
    return bad


def drive_carry(trials, rng):
    """A drive's fine tooth at its fixed teeth D, q = (N + d) div D with N read alike in both goings: the
    reversed carry from the reflected tooth must give the same q and return d."""
    out = {}
    for name, tau in (("flip", lambda d, D: D - 1 - d), ("mirror", lambda d, D: (2 * (D // 2) - d) % D)):
        bad = {"even D": 0, "odd D": 0}
        for _ in range(trials):
            D = rng.randint(2, 40)
            n = rng.randint(-10 * D, 10 * D)
            d = rng.randint(0, D - 1)
            q, d2 = divmod(n + d, D)
            q3, d3 = divmod(n + tau(d2, D), D)
            ok = q3 == q and tau(d3, D) == d
            bad["even D" if D % 2 == 0 else "odd D"] += not ok
        out[name] = bad
    return out


def box(v, w, D, trigger, span=12):
    """The mathematician's one-gear toy (derive/mathematician/turnover.py), generalised: a gear with no Mesh,
    F(a) = -D a, at the fixed teeth w; the tick M is the turnover T where the trigger fires on the gear's own
    triple (before, now, the step's output), else the step S. Counts the images hit twice (M not injective)
    and the states where T M T M x != x (the rewind with no log, M^-1 = T M T, fails)."""
    f = lambda a: -D * a
    seen, hits, bad = {}, 0, 0
    frames = (0, 1) if isinstance(v, Frame) else (0,)
    rs = range(w + 1) if isinstance(v, Even) else range(w)
    for am in range(-span, span + 1):
        for a in range(-span, span + 1):
            for r in rs:
                for b in frames:
                    x = (a, am, r, b)
                    if isinstance(v, Even) and w % 2 == 0 and r in (0, w) and (a - am) % 2:
                        continue
                    if isinstance(v, Even) and w % 2 == 1 and r == w:
                        continue
                    y = v.step(x, w, w, f)
                    top = trigger(am, a, y[0])
                    m = v.T(x, w) if top else y
                    hits += m in seen
                    seen.setdefault(m, x)
                    y2 = v.step(v.T(m, w), w, w, f)
                    m2 = v.T(v.T(m, w), w) if trigger(v.T(m, w)[1], v.T(m, w)[0], y2[0]) else y2
                    bad += v.T(m2, w) != x
    return hits, bad


def weak_max(x0, x1, x2):
    return x0 <= x1 and x2 <= x1 and (x0 < x1 or x2 < x1)


def weak_min(x0, x1, x2):
    return x0 >= x1 and x2 >= x1 and (x0 > x1 or x2 > x1)


def main(argv):
    rng = random.Random(20261028)
    names = [a for a in argv if not a.startswith("--")]
    pool = MUTANTS if "--mutants" in argv else VARIANTS
    chosen = [v for v in pool if not names or v.name in names]
    trials = 4000
    classes = ["even->even", "odd->odd", "odd->even", "even->odd"]
    for v in chosen:
        for small in (True, False):
            for cls in classes:
                f = props(v, cls, small, trials, rng)
                size = "w 2..15" if small else "w ~1e20"
                print(f"{v.name:34s} {size:8s} {cls:10s} " + " ".join(f"{k} {f[k]:4d}" for k in f)
                      + f"  (of {trials})")
        for small in (True, False):
            for parity in ("even", "odd", "mixed"):
                bad = retrace(v, small, 1000, rng, parity=parity)
                size = "w 2..15" if small else "w ~1e20"
                print(f"{v.name:34s} {size:8s} retrace 40 ticks, teeth {parity:5s}: S^n T x_n != T x_0 in {bad:4d} of 1000")
        for D in (3, 5):
            for w in range(8, 16):
                hits, bad = box(v, w, D, weak_max)
                hits2, bad2 = box(v, w, D, lambda p, q, u: weak_max(p, q, u) or weak_min(p, q, u))
                print(f"{v.name:34s} one-gear tick, D {D}, w {w:2d} ({'even' if w % 2 == 0 else 'odd '}): "
                      f"weak top: images hit twice {hits:3d}, T M T M x != x {bad:3d}; "
                      f"top or bottom: hit twice {hits2:3d}, T M T M x != x {bad2:3d}")
    if "--mutants" not in argv:
        # the mathematician's own box (derive/mathematician/turnover.py: span 25, D 3), reproduced
        for v in (Mirror(), Flip(), Frame()):
            for w in (10, 11):
                hits, bad = box(v, w, 3, weak_max, span=25)
                print(f"the mathematician's box (span 25, D 3), {v.name:7s} w {w}: images hit twice {hits}, T M T M x != x {bad}")
        dc = drive_carry(20000, rng)
        for k, bad in dc.items():
            print(f"drive fine tooth reflected by the {k:6s}: reversed carry wrong in even D {bad['even D']}, odd D {bad['odd D']} (of about 10000 each)")


if __name__ == "__main__":
    main(sys.argv[1:])
