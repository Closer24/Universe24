"""The tie rule: does negating a gear commute with the step bit for bit at every teeth count?

The step of one gear: p = W (a - b) + (r - home), p+ = p + f, (q, r+) = carry(p+ + home+, W+), a+ = a + q,
with home = (W - go) div 2 (draft H's going). Negation N: (a, b, r, go) -> (-a, -b, W - 1 - r, 1 - go), f -> -f.
Claim: step(N x) = N step(x) exactly, for every W, W+ (both parities) and every r in [0, W), when the going is
toggled per gear. Control: a going shared by two gears, of which a turn negates one, fails at even counts.

usage: python3 -I probe.py
"""

import random


def home(w, go):
    return (w - go) // 2


def step(a, b, r, go, w, wp, f):
    p = w * (a - b) + (r - home(w, go))
    q, rp = divmod(p + f + home(wp, go), wp)
    return a + q, a, rp, go


def neg(a, b, r, go, w):
    return -a, -b, w - 1 - r, 1 - go


def main():
    rng = random.Random(20261028)
    fails_per_gear = fails_shared = 0
    cases = 200000
    for _ in range(cases):
        w, wp = rng.randint(1, 12), rng.randint(1, 12)
        a, b, f = rng.randint(-60, 60), rng.randint(-60, 60), rng.randint(-200, 200)
        r, go = rng.randint(0, w - 1), rng.randint(0, 1)
        # per gear: N then step against step then N
        left = step(*neg(a, b, r, go, w), w, wp, -f)
        right = neg(*step(a, b, r, go, w, wp, f)[:3], step(a, b, r, go, w, wp, f)[3], wp)
        fails_per_gear += left != right
        # shared going: a second gear on the same dial, not negated by the turn, keeps the dial; so the
        # negated gear must be negated with its going unchanged: r -> 2 home - r, which may leave [0, W)
        r2 = 2 * home(w, go) - r
        if not 0 <= r2 < w:
            fails_shared += 1
            continue
        left2 = step(-a, -b, r2, go, w, wp, -f)
        a1, b1, rp1, _ = step(a, b, r, go, w, wp, f)
        right2 = (-a1, -b1, 2 * home(wp, go) - rp1)
        fails_shared += (left2[:3] != right2) or not (0 <= right2[2] < wp)
    print(f"going per gear: N commutes with the step in {cases - fails_per_gear} of {cases} cases")
    print(f"going shared by the Node-clock: in {cases - fails_shared} of {cases} cases")
    return 0 if fails_per_gear == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
