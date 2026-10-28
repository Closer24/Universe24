"""Probe 4: the checkerboard doubler of the vacuum step: an exact symmetry, same total wind, opposite sweep."""
import itertools
import random
from fractions import Fraction as F

n = 4
c0 = F(162120510851, 10**12)  # a massive train's cos w0 = pinion/rim (any value works)
R = c0 / 3  # grip over teeth; the hold is 0 at the vacuum
sites = list(itertools.product(range(n), repeat=3))
spokes = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

def nb(f, x, d):
    return f[tuple((x[i] + d[i]) % n for i in range(3))]

def step(now, before):
    return {x: R * sum(nb(now, x, d) for d in spokes) - before[x] for x in sites}

def wind(now, before):  # the conserved form with the hold 0, complex hand, summed over the torus
    tot = F(0)
    for x in sites:
        a, b = now[x], before[x]
        tot += (a[0] ** 2 + a[1] ** 2 + b[0] ** 2 + b[1] ** 2)
        for d in spokes:
            bj = nb(before, x, d)
            tot -= R * (a[0] * bj[0] + a[1] * bj[1])
    return tot

def sweep(now, before):
    return sum(now[x][0] * before[x][1] - now[x][1] * before[x][0] for x in sites)  # Im(conj(b) n)

random.seed(3)
now = {x: (F(random.randint(-50, 50)), F(random.randint(-50, 50))) for x in sites}
before = {x: (F(random.randint(-50, 50)), F(random.randint(-50, 50))) for x in sites}

def stepc(now, before):
    re = step({x: v[0] for x, v in now.items()}, {x: v[0] for x, v in before.items()})
    im = step({x: v[1] for x, v in now.items()}, {x: v[1] for x, v in before.items()})
    return {x: (re[x], im[x]) for x in sites}

def doubled(now, before, t):
    s = lambda x, tt: -1 if (sum(x) + tt) % 2 else 1
    return ({x: (s(x, t) * v[0], s(x, t) * v[1]) for x, v in now.items()},
            {x: (s(x, t - 1) * v[0], s(x, t - 1) * v[1]) for x, v in before.items()})

dn, db = doubled(now, before, 0)
print("wind", wind(now, before) == wind(dn, db), " sweep original", sweep(now, before), " doubler", sweep(dn, db))
ok = True
a, b = now, before
da, dbb = dn, db
for t in range(1, 12):
    a, b = stepc(a, b), a
    da, dbb = stepc(da, dbb), da
    ea, eb = doubled(a, b, t)
    ok = ok and ea == da and eb == dbb
    ok = ok and wind(a, b) == wind(now, before)
print("doubler map commutes with the step for 11 ticks:", ok, "; wind conserved:", wind(a, b) == wind(now, before))
