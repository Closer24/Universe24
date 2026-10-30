"""David's probe: the turnover on a gear T negates (a T-odd gear), on engine/step.gear and ungear.

usage: python3 -I p6_odd_turnover.py <worktree>/src
T-even: T (a, b, r, go) = (b, a, w-1-r, 1-go), the push kept.        Claim: T gear T = ungear.
T-odd:  T (a, b, r, go) = (-b, -a, r, go), the push negated (its source odd under T): the exchange's flip and the
        negation's flip cancel, so the tooth and the going stand.     Claim: T gear T = ungear.
Control: on a T-odd gear the exchange negated with the tooth flipped and the going advanced, (-b, -a, w-1-r, 1-go).
And the time gear's course written as a product with its own notch (a source -L Omega): L = L+ = 0 forces L- = 0.
"""
import random
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.engine.step import gear, ungear  # noqa: E402

rng = random.Random(5)
even = odd = ctl = 0
CASES = 200000
for _ in range(CASES):
    w, wp = rng.randint(1, 12), rng.randint(1, 12)
    a, b, push = rng.randint(-10**5, 10**5), rng.randint(-10**5, 10**5), rng.randint(-10**7, 10**7)
    r, go = rng.randint(0, w - 1), rng.randint(0, 1)
    a1, b1, r1 = gear(a, b, r, go, w, wp, push)
    # T-even
    x = gear(a, a1, wp - 1 - r1, 1 - go, wp, w, push)
    even += (x[1], x[0], w - 1 - x[2]) != (a, b, r)
    # T-odd
    y = gear(-a, -a1, r1, go, wp, w, -push)
    odd += (-y[1], -y[0], y[2]) != (a, b, r) or (-y[1], -y[0], y[2]) != ungear(a1, a, r1, go, w, wp, push)
    # control
    z = gear(-a, -a1, wp - 1 - r1, 1 - go, wp, w, -push)
    ctl += (-z[1], -z[0], w - 1 - z[2]) != (a, b, r)
print(f"T-even: T gear T = ungear in {CASES - even} of {CASES}")
print(f"T-odd, tooth and going standing: T gear T = ungear in {CASES - odd} of {CASES}")
print(f"control, T-odd with the tooth flipped and the going advanced: fails in {ctl} of {CASES}")

# the course as a product with its own notch: source -L * Omega
dead = 0
for _ in range(CASES):
    w = rng.randint(1, 50)
    Lm, r, go, om = rng.randint(-50, 50), rng.randint(0, w - 1), rng.randint(0, 1), rng.randint(-10**4, 10**4)
    L1, _, _ = gear(0, Lm, r, go, w, w, -0 * om)
    dead += (L1 == 0) != (Lm == 0)
print(f"source -L Omega: L = 0 and L+ = 0 exactly where L- = 0, in {CASES - dead} of {CASES}")
