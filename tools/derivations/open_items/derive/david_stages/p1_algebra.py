"""David's probe of stage 1 (algebra/carry.py) and the tie rule, on the module's own functions.

usage: python3 -I p1_algebra.py <worktree>/src
Checks, exact integers only:
  (1) carry: n + r = q d + r', 0 <= r' < d, unique (against divmod), d from 1, to 300 bits;
  (2) nonneg: 1 for n >= 0, 0 below, on [-400, 400] and at +-2^k for k to 300;
  (3) home(w, 1 - go) = w - 1 - home(w, go), every w from 1 to 400, both goings (the identity the tie rule rests on);
  (4) the tie rule on engine/step.gear: N (a, b, r, go) = (-a, -b, w-1-r, 1-go), push -> -push, commutes with the
      step, W and W+ from 1 to 12, every r in [0, W), 200,000 draws; the fine tooth stays in [0, W+);
  (5) the gear's own time reversal: T (a, b, r, go) = (b, a, w-1-r, 1-go) at the step's end teeth; T gear T = ungear,
      200,000 draws (item (h): the tick is its own reversal gear by gear, at every teeth count);
  (6) controls: home without the going (w div 2) fails (4); the flip w - r fails (5).
"""
import random
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry, choose, flip, home, nonneg, uncarry
from tensor24.engine.step import gear, ungear

rng = random.Random(20261028)
bad = {k: 0 for k in ("carry", "nonneg", "home", "N", "Nrange", "T", "ctlN", "ctlT")}

for _ in range(100000):
    d = rng.randint(1, 1 << rng.choice((3, 20, 64, 200, 300)))
    n = rng.randint(-(1 << 300), 1 << 300)
    r = rng.randint(-(1 << 40), 1 << 40)
    q, k = carry(n, d, r)
    bad["carry"] += not (n + r == q * d + k and 0 <= k < d and (q, k) == divmod(n + r, d) and uncarry(q, d, k) == n + r)

for n in list(range(-400, 401)) + [s * (1 << e) + t for e in range(1, 301) for s in (1, -1) for t in (-1, 0, 1)]:
    bad["nonneg"] += nonneg(n) != (1 if n >= 0 else 0)

for w in range(1, 401):
    for go in (0, 1):
        bad["home"] += home(w, 1 - go) != w - 1 - home(w, go)
        bad["home"] += flip(flip(0, w), w) != 0 or choose(1, w, go) != w or choose(0, w, go) != go


def neg(a, b, r, go, w):
    return -a, -b, w - 1 - r, 1 - go


def gear4(a, b, r, go, w, wp, push):
    return (*gear(a, b, r, go, w, wp, push), go)


for _ in range(200000):
    w, wp = rng.randint(1, 12), rng.randint(1, 12)
    a, b, push = rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6), rng.randint(-10**9, 10**9)
    r, go = rng.randint(0, w - 1), rng.randint(0, 1)
    # (4) N commutes with the step
    left = gear4(*neg(a, b, r, go, w), w, wp, -push)
    a1, b1, r1, g1 = gear4(a, b, r, go, w, wp, push)
    right = neg(a1, b1, r1, g1, wp)
    bad["N"] += left != right
    bad["Nrange"] += not (0 <= r1 < wp)
    # (5) T gear T = ungear: the step from (a, b) at w to (a1, a) at wp, reversed at wp -> w
    t = (a, a1, wp - 1 - r1, 1 - go)          # T on the end state
    s2 = gear4(*t, wp, w, push)                # the same step, run on the reversed state, teeth wp -> w
    back = (s2[1], s2[0], w - 1 - s2[2], 1 - s2[3])  # T again
    bad["T"] += back != (a, b, r, go) or back[:3] != ungear(a1, a, r1, go, w, wp, push)
    # (6) controls
    h0 = lambda w_, go_: w_ // 2  # noqa: E731
    p = w * (-a + b) + ((w - 1 - r) - h0(w, 1 - go))
    q, k = divmod(p - push + h0(wp, 1 - go), wp)
    bad["ctlN"] += (-a + q, -a, k) != (-a1, -a, wp - 1 - r1)
    t2 = (a, a1, wp - r1, 1 - go)
    if 0 <= t2[2] < wp:
        s3 = gear4(*t2, wp, w, push)
        bad["ctlT"] += (s3[1], s3[0], w - s3[2]) != (a, b, r)
    else:
        bad["ctlT"] += 1

print("(1) carry exact and unique, 100,000 draws to 300 bits: failures", bad["carry"])
print("(2) nonneg exact on [-400, 400] and at +-2^k +- 1 to 2^300: failures", bad["nonneg"])
print("(3) home(w, 1-go) = w-1-home(w, go), w 1..400, both goings: failures", bad["home"])
print("(4) the tie rule: N commutes with engine/step.gear, 200,000 draws, W, W+ in 1..12: failures", bad["N"],
      "; fine tooth outside [0, W+):", bad["Nrange"])
print("(5) T gear T = ungear (slots exchanged, w-1-r, going advanced), 200,000 draws: failures", bad["T"])
print("(6) controls: home ignoring the going breaks (4) in", bad["ctlN"], "of 200,000; the flip w - r breaks (5) in",
      bad["ctlT"], "of 200,000")
