"""Draft H, probe h1: the turnover's trigger, the top and the bottom as one rule under T (pure integers; python3 -I).

(a) Reversal symmetry: a trigger tau(X0, X1, X2) on the time gear's three notches (the notch before, the notch now,
    the step's output) gives a tick M with M^-1 = T M T only if tau(X0, X1, X2) = tau(X2, X1, X0) (draft H, 4.2).
    Every trigger below is tested exhaustively on the triples in [-6, 6]^3 (and with the full rate 3 for the
    floors); the asymmetric one is the law's own counterexample (ALGEBRA.md line 1602) and must fail.
(b) The top or the bottom in one carry: with v1 = X1 - X0, v2 = X2 - X1, s = v1 v1 + v2 v2,
        tau = (1 + (-v1 v2) div (v1 v1 v2 v2 + 1)) * (-((-s) div (s s + 1))),
    which must equal the weak maximum or the weak minimum on every triple.
(c) One Node-clock (a time gear at the teeth TR with its own spring toward X0 and a drive carried at DD from its
    hand's forms, and one hand gear at the mean teeth c (X- + X)), FRAME's T: from a setting at rest (X- = X,
    the hand at rest) the course under each trigger: the Node-clocks pinned in the two-cycle {x, T x}; the period
    of the course; whether the course passes through its setting again (the bounce at a T-symmetric setting).
Usage: python3 -I h1_trigger.py
"""

SIDES = 2


def weak_max(x0, x1, x2):
    return x0 <= x1 and x2 <= x1 and (x0 < x1 or x2 < x1)


def weak_min(x0, x1, x2):
    return x0 >= x1 and x2 >= x1 and (x0 > x1 or x2 > x1)


def union(x0, x1, x2):
    return weak_max(x0, x1, x2) or weak_min(x0, x1, x2)


def strict_min(x0, x1, x2):
    return x0 > x1 and x2 > x1


def top_or_strict_bottom(x0, x1, x2):
    return weak_max(x0, x1, x2) or strict_min(x0, x1, x2)


def law_floor(xf):
    return lambda x0, x1, x2: weak_max(x0, x1, x2) or x0 < xf or x2 < xf


def asym_top(x0, x1, x2):
    return x0 < x1 and x2 <= x1


def one_carry(x0, x1, x2):
    v1, v2 = x1 - x0, x2 - x1
    s = v1 * v1 + v2 * v2
    p = v1 * v2
    return (1 + (-p) // (p * p + 1)) * (-((-s) // (s * s + 1)))


def part_a():
    rows = []
    span = range(-6, 7)
    cases = [("the weak top (law 4's top)", weak_max), ("the weak bottom (the candidate)", weak_min),
             ("the top or the weak bottom", union), ("the strict bottom", strict_min),
             ("the top or the strict bottom", top_or_strict_bottom), ("the top or the law's floor (X_f = -3)", law_floor(-3)),
             ("the top or the full rate's bottom (Gamma = 3)", law_floor(3)),
             ("MUTANT: the asymmetric top X0 < X1 >= X2", asym_top)]
    for name, tau in cases:
        bad = sum(1 for a in span for b in span for c in span if tau(a, b, c) != tau(c, b, a))
        rows.append(f"(a) {name:46s}: triples where tau(X0, X1, X2) != tau(X2, X1, X0): {bad} of {13 ** 3}")
    bad = sum(1 for a in span for b in span for c in span if bool(one_carry(a, b, c)) != union(a, b, c))
    rows.append(f"(b) the one carry (1 + (-v1 v2) div (v1^2 v2^2 + 1)) (-((-s) div (s^2 + 1))) against the top or the weak bottom: "
                f"{bad} of {13 ** 3} differ")
    big = [(10**30 + 7, 10**30 + 9, 10**30 + 8), (-10**30, 10**30, -10**30), (5, 5, 5), (5, 5, 6), (6, 5, 5)]
    bad = sum(1 for t in big if bool(one_carry(*t)) != union(*t))
    rows.append(f"(b) the one carry at the largest integers and the rests: {bad} of {len(big)} differ")
    return rows


# --- (c) one Node-clock under FRAME ------------------------------------------------------------------------


def origin(w, b):
    return (w - b) // SIDES


def stride(g, w):
    now, before, r, b = g
    return w * (now - before) + r - origin(w, b)


def rev(g, w):
    now, before, r, b = g
    return (before, now, w - 1 - r, 1 - b)


class OneClock:
    def __init__(self, TR, c, DD, DX, X0, D, kappa, trigger):
        self.TR, self.c, self.DD, self.DX, self.X0, self.D, self.kappa = TR, c, DD, DX, X0, D, kappa
        self.trigger = trigger

    def M(self, st):
        X, dX, a = st
        w = self.c * (X[1] + X[0])
        P = stride(a, w)
        P2 = P + X[0] * (-self.D * a[0])
        forms = P * P2
        q, dX2 = divmod(self.kappa * forms + dX, self.DD)
        PX = stride(X, self.TR) - self.DX * (X[0] - self.X0) + self.TR * q
        dx, rX = divmod(PX + origin(self.TR, X[3]), self.TR)
        Xn = (X[0] + dx, X[0], rX, X[3])
        if self.trigger(X[1], X[0], Xn[0]):
            return (rev(X, self.TR), self.DD - 1 - dX, rev(a, w)), True
        w2 = self.c * (X[0] + Xn[0])
        if w2 < 1:
            raise ArithmeticError("end teeth at or below 0")
        d, r2 = divmod(P2 + origin(w2, a[3]), w2)
        return (Xn, dX2, (a[0] + d, a[0], r2, a[3])), False


def course(clock, st, ticks):
    seen, turned, xs, pinned, prev = {st: 0}, 0, [st[0][0]], 0, False
    period = None
    for k in range(1, ticks + 1):
        st, top = clock.M(st)
        turned += top
        pinned += top and prev
        prev = top
        xs.append(st[0][0])
        if st in seen and period is None:
            period = k - seen[st]
        seen.setdefault(st, k)
    return turned, pinned, period, xs


def part_c():
    rows = []
    triggers = [("the weak top alone (the head with no floor)", weak_max), ("the top or the weak bottom", union),
                ("the top or the strict bottom", top_or_strict_bottom),
                ("the top or the full rate's bottom (X0 = 40)", law_floor(40))]
    # the setting: the time gear at rest at X = 40 (its full rate here), the hand at rest at notch 3, frame 0;
    # a second setting with the drive's fine tooth at 0 (not at its origin), which T does not fix
    for push, label in ((+1, "pushed up by its spring (X0 = 60 above the setting)"),
                        (-1, "pulled down by its spring (X0 = 20 below the setting)")):
        X0 = 60 if push > 0 else 20
        for name, tau in triggers:
            clock = OneClock(TR=10, c=3, DD=10**6, DX=1, X0=X0, D=1, kappa=1, trigger=tau)
            w = clock.c * 80
            # every fine tooth born at its origin (the head's trains.gears_of: the mid tooth), the drive's too
            st = ((40, 40, origin(10, 0), 0), origin(clock.DD, 0), (3, 3, origin(w, 0), 0))
            turned, pinned, period, xs = course(clock, st, 200)
            back = sum(1 for k, x in enumerate(xs) if k and x == 40)
            rows.append(f"(c) {label:52s} {name:44s}: turnovers {turned:3d}, pinned {pinned:3d}, period {period}, "
                        f"returns to X = 40: {back}; X over ticks 0-24: {xs[:25]}")
    clock = OneClock(TR=10, c=3, DD=10**6, DX=1, X0=60, D=1, kappa=1, trigger=weak_max)
    st = ((40, 40, origin(10, 0), 0), 0, (3, 3, origin(240, 0), 0))
    turned, pinned, period, xs = course(clock, st, 200)
    rows.append(f"(c) the setting with the drive's fine tooth at 0 (no fixed point of T), the weak top alone: turnovers {turned}, "
                f"period {period}; X over ticks 0-40: {xs[:41]}")
    return rows


if __name__ == "__main__":
    for line in part_a() + part_c():
        print(line)
