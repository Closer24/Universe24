"""H_verify v1: an independent check of draft H's gear claims (claims P1 to P3 and P3''), pure integers, python3 -I.

Written from the draft's formulas, not from its probes. A gear is (now, before, r, b) at teeth w.
The step from teeth w to w2 with a force f(now): P2 = w (now - before) + r - o(w, b) + f(now);
(d, r2) = divmod(P2 + o(w2, b), w2); the gear goes to (now + d, now, r2, b).
Exhaustive boxes: w, w2 in 1..12, now and before in -3..3, every r and b, several force tables.
"""

import random
import sys


def o_frame(w, b):
    return (w - b) // 2


def stride(x, w, o):
    now, before, r, b = x
    return w * (now - before) + r - o(w, b)


def step(x, w, w2, f, o):
    now, before, r, b = x
    p2 = stride(x, w, o) + f(now)
    d, r2 = divmod(p2 + o(w2, b), w2)
    return (now + d, now, r2, b)


def T_frame(x, w):
    now, before, r, b = x
    return (before, now, w - 1 - r, 1 - b)


def N_frame(x, w):
    now, before, r, b = x
    return (-now, -before, w - 1 - r, 1 - b)


def forces(rng, k):
    out = []
    for _ in range(k):
        table = {a: rng.randint(-40, 40) for a in range(-60, 61)}
        out.append(lambda a, t=table: t[a])
    return out


def odd_forces(rng, k):
    out = []
    for _ in range(k):
        table = {0: 0}
        for a in range(1, 61):
            table[a] = rng.randint(-40, 40)
            table[-a] = -table[a]
        out.append(lambda a, t=table: t[a])
    return out


def frame_box(rng):
    fs, ofs = forces(rng, 3), odd_forces(rng, 3)
    tally = {"states": 0, "TT": 0, "TSTi": 0, "NS": 0, "rest": 0, "range": 0, "P to -P": 0}
    by_class = {}
    for w in range(1, 13):
        for w2 in range(1, 13):
            cls = ("even" if w % 2 == 0 else "odd") + "->" + ("even" if w2 % 2 == 0 else "odd")
            c = by_class.setdefault(cls, {"states": 0, "fail": 0})
            for now in range(-3, 4):
                for before in range(-3, 4):
                    for r in range(w):
                        for b in (0, 1):
                            x = (now, before, r, b)
                            tally["states"] += 1
                            c["states"] += 1
                            bad = 0
                            if T_frame(T_frame(x, w), w) != x:
                                tally["TT"] += 1
                                bad = 1
                            if stride(T_frame(x, w), w, o_frame) != -stride(x, w, o_frame):
                                tally["P to -P"] += 1
                                bad = 1
                            if stride(x, w, o_frame) == 0 and stride(T_frame(x, w), w, o_frame) != 0:
                                tally["rest"] += 1
                                bad = 1
                            for f in fs:
                                y = step(x, w, w2, f, o_frame)
                                if not 0 <= y[2] < w2:
                                    tally["range"] += 1
                                    bad = 1
                                back = step(T_frame(y, w2), w2, w, f, o_frame)
                                if back != T_frame(x, w):
                                    tally["TSTi"] += 1
                                    bad = 1
                            for f in ofs:
                                if step(N_frame(x, w), w, w2, f, o_frame) != N_frame(step(x, w, w2, f, o_frame), w2):
                                    tally["NS"] += 1
                                    bad = 1
                            c["fail"] += bad
    return tally, by_class


# --- Animate's (i): the carried mirror with the head's rounding (half up), one going ------------------------


def o_head(w, b):
    return w // 2


def T_carried(x, w):
    now, before, r, b = x
    c, r2 = divmod(2 * (w // 2) - r, w)
    return (before, now - c, r2, b)


# --- Animate's (ii) / draft G's "carried mirror with half even": the tie to the even quotient ---------------


def step_even(x, w, w2, f):
    now, before, r, b = x
    p2 = w * (now - before) + r - w // 2 + f(now)
    q, s = divmod(p2 + w2 // 2, w2)
    if w2 % 2 == 0 and s == 0 and q % 2 == 1:
        q -= 1  # the tie sent to the even quotient
    r2 = p2 + w2 // 2 - w2 * q
    return (now + q, now, r2, b)


def T_even(x, w):
    now, before, r, b = x
    return (before, now, 2 * (w // 2) - r, b)  # the unreduced mirror


def animate_box(rng):
    fs = forces(rng, 3)
    tt_fail = tt_ties = tsti_fail = sts_fail = states = 0
    noncanon_fail = canon = 0
    reach_w = steps_even = tt_even_fail = tsti_even_fail = 0
    for w in range(2, 13, 2):
        for w2 in range(2, 13, 2):
            for now in range(-3, 4):
                for before in range(-3, 4):
                    for r in range(w):
                        x = (now, before, r, 0)
                        states += 1
                        if T_carried(T_carried(x, w), w) != x:
                            tt_fail += 1
                            tt_ties += r == 0
                        for f in fs:
                            y = step(x, w, w2, f, o_head)
                            if step(T_carried(y, w2), w2, w, f, o_head) != T_carried(x, w):
                                sts_fail += 1
                            if T_carried(step(T_carried(y, w2), w2, w, f, o_head), w) != x:
                                tsti_fail += 1
                    for r in range(w + 1):  # the even carry's remainders lie in [0, w]
                        x = (now, before, r, 0)
                        canonical = not (r in (0, w) and (now - before) % 2)
                        if not canonical:
                            for f in fs:
                                y = step_even(x, w, w2, f)
                                noncanon_fail += step_even(T_even(y, w2), w2, w, f) != T_even(x, w)
                            continue
                        canon += 1
                        if T_even(T_even(x, w), w) != x:
                            tt_even_fail += 1
                        for f in fs:
                            y = step_even(x, w, w2, f)
                            steps_even += 1
                            reach_w += y[2] == w2
                            if step_even(T_even(y, w2), w2, w, f) != T_even(x, w):
                                tsti_even_fail += 1
    return dict(states=states, tt_fail=tt_fail, tt_fail_at_r0=tt_ties, tsti_fail=tsti_fail, sts_fail=sts_fail,
                even_canonical_states=canon, even_noncanonical_sts_fail=noncanon_fail,
                even_steps=steps_even, even_r_at_w=reach_w, even_tt_fail=tt_even_fail, even_tsti_fail=tsti_even_fail)


def retrace(rng, n_runs=1000, ticks=40):
    """Forward n ticks at one even teeth count, T, n ticks, T: back at the start? (the carried mirror, the frame)"""
    fail_c = fail_f = 0
    for _ in range(n_runs):
        w = rng.choice([2, 4, 6, 8, 10, 12, 14])
        table = {a: rng.randint(-3, 3) for a in range(-400, 401)}
        f = lambda a, t=table: t[max(-400, min(400, a))]  # noqa: E731 (a bounded probe table, not a law)
        x = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randrange(w), 0)
        y = x
        for _t in range(ticks):
            y = step(y, w, w, f, o_head)
        y = T_carried(y, w)
        for _t in range(ticks):
            y = step(y, w, w, f, o_head)
        fail_c += T_carried(y, w) != x
        y = x
        for _t in range(ticks):
            y = step(y, w, w, f, o_frame)
        y = T_frame(y, w)
        for _t in range(ticks):
            y = step(y, w, w, f, o_frame)
        fail_f += T_frame(y, w) != x
    return fail_c, fail_f


def main():
    rng = random.Random(24)
    tally, by_class = frame_box(rng)
    print("FRAME exhaustive box (w, w2 in 1..12; now, before in -3..3; every r, b; 3 forces, 3 odd forces):")
    print("  ", tally)
    for cls in sorted(by_class):
        print("   class", cls, by_class[cls])
    a = animate_box(rng)
    print("Animate (i) carried mirror, half up, even w, w2 in 2..12:", {k: a[k] for k in ("states", "tt_fail", "tt_fail_at_r0", "tsti_fail", "sts_fail")})
    print("Animate (ii) / G: tie to even, unreduced mirror, even w, w2:", {k: a[k] for k in ("even_canonical_states", "even_steps", "even_r_at_w", "even_tt_fail", "even_tsti_fail", "even_noncanonical_sts_fail")})
    fc, ff = retrace(rng)
    print(f"retrace of 40 ticks at an even count, 1000 starts: carried mirror fails {fc}, frame fails {ff}")


if __name__ == "__main__":
    main()
    sys.exit(0)
