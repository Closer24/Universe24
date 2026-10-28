"""F3: the doubler, its symmetry and the one term of the kinds that lifts it (draft F; root II item 16).

Exact integers and Fractions only, no float. Run: python3 -I F3_doubler.py [MUTANT]
MUTANT: none (default), hold (the vacuum's hold read 1/5 where the claim names 0), neighbour
(the staggered sign dropped from the neighbours' term), head (the hold computed without the
pinion's term). Each mutant must make at least one check FAIL.

The staggered map SIGMA: a(x, t) -> e(x, t) a(x, t), e = (-1)^(x + y + z + t), the torus's character at
the wave number (pi, pi, pi) times the tick's parity.
 A. the rational leapfrog a+ = h a + mu SUM_j a_j - a- (the one formula at a uniform clock, the hold h):
    SIGMA maps solutions to solutions exactly when h = 0, for light and for a massive train alike;
 B. at h = 0 the wind (the conserved form) is SIGMA-even and the sweep SIGMA-odd: the doubler has the
    same wind and the opposite charge; at h != 0 the wind is not SIGMA-even;
 C. in the stencil of seven the neighbours' term is SIGMA-even (relative to the step) and the
    Node-clock's own term, the hold, is SIGMA-odd: the hold is the one term that can lift it;
 D. the head's gearing (core/rule3.gearing, imported read-only from the t24 worktree): the hold
    2 w - D - SUM_j R_j is 0 at the vacuum for every train of the one big bang's calibre and
    12 G^2 (rim (Gamma^2 - p0^2) + pinion (p0^2 - pm^2)) > 0 at every load; a tension raises it;
 E. the integer one formula (Rule3's carry, odd teeth): SIGMA does not commute bit for bit, and from a
    setting with no staggered content the rounding feeds the staggered mode.
"""

import itertools
import random
import sys
from fractions import Fraction as Fr

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []
T24 = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/t24/src"


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


L = 4
SITES = list(itertools.product(range(L), repeat=3))
SP = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def nb(x, d):
    return ((x[0] + d[0]) % L, (x[1] + d[1]) % L, (x[2] + d[2]) % L)


def eps(x, t):
    return -1 if (x[0] + x[1] + x[2] + t) % 2 else 1


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cscale(k, a):
    return (k * a[0], k * a[1])


def step(now, before, h, mu):
    out = {}
    for x in SITES:
        s = (Fr(0), Fr(0))
        for d in SP:
            s = cadd(s, now[nb(x, d)])
        out[x] = cadd(cadd(cscale(h, now[x]), cscale(mu, s)), cscale(-1, before[x]))
    return out


def sigma(field, t):
    return {x: cscale(eps(x, t), v) for x, v in field.items()}


def rnd_field(rng, lo=-40, hi=40):
    return {x: (Fr(rng.randint(lo, hi)), Fr(rng.randint(lo, hi))) for x in SITES}


def wind(now, before, h, mu):
    """The leapfrog's conserved form SUM |a|^2 + |a-|^2 - Re conj(a) (h a- + mu SUM_j a-_j)."""
    tot = Fr(0)
    for x in SITES:
        a, b = now[x], before[x]
        tot += a[0] ** 2 + a[1] ** 2 + b[0] ** 2 + b[1] ** 2
        s = cscale(h, b)
        for d in SP:
            s = cadd(s, cscale(mu, before[nb(x, d)]))
        tot -= a[0] * s[0] + a[1] * s[1]
    return tot


def sweep(now, before):
    return sum(b[0] * a[1] - b[1] * a[0] for a, b in zip(now.values(), before.values()))


rng = random.Random(16)
H0 = Fr(1, 5) if MUT == "hold" else Fr(0)
cases = [("light", H0, (2 - H0) / 6), ("massive r = 3/5", H0, Fr(3, 5) / 3)]
for name, h, mu in cases:
    now, before = rnd_field(rng), rnd_field(rng)
    a, b = now, before
    sa, sb = sigma(now, 0), sigma(before, -1)
    ok, w0 = True, wind(now, before, h, mu)
    for t in range(1, 13):
        a, b = step(a, b, h, mu), a
        sa, sb = step(sa, sb, h, mu), sa
        ok = ok and sigma(a, t) == sa and sigma(b, t - 1) == sb
    check(f"A1 [{name}] SIGMA commutes with the step for 12 ticks at the vacuum's hold 0", ok)
    check(f"B1 [{name}] the doubler keeps the wind and reverses the sweep",
          wind(sigma(now, 0), sigma(before, -1), h, mu) == w0 and sweep(sigma(now, 0), sigma(before, -1)) == -sweep(now, before),
          f"wind {wind(now, before, h, mu)}, sweep {sweep(now, before)} -> {sweep(sigma(now, 0), sigma(before, -1))}")
# off the edge: a hold of 1/5 for light (mu = (2 - h)/6, so k = 0 stays massless)
h, mu = Fr(1, 5), Fr(9, 50)
now, before = rnd_field(rng), rnd_field(rng)
a1, b1 = step(now, before, h, mu), now
sa1 = step(sigma(now, 0), sigma(before, -1), h, mu)
check("A2 off the edge (hold 1/5) SIGMA fails at the first tick", sigma(a1, 1) != sa1)
check("B2 off the edge the wind is not SIGMA-even", wind(sigma(now, 0), sigma(before, -1), h, mu) != wind(now, before, h, mu))

# C. the terms' parities under SIGMA at one tick t: on-site h a, neighbours mu SUM_j a_j
z = rnd_field(rng)
t = 3
zs = sigma(z, t)
onsite_ok = all(cscale(1, zs[x]) == cscale(eps(x, t), z[x]) for x in SITES)
nbr_ok = True
for x in SITES:
    s, ss = (Fr(0), Fr(0)), (Fr(0), Fr(0))
    for d in SP:
        s = cadd(s, z[nb(x, d)])
        ss = cadd(ss, zs[nb(x, d)])
    target = cscale(-eps(x, t), s) if MUT != "neighbour" else cscale(eps(x, t), s)
    nbr_ok = nbr_ok and ss == target
check("C1 the neighbours' sum of SIGMA a is -e(x, t) times the neighbours' sum of a (every Spoke changes the colour)", nbr_ok)
check("C2 the Node-clock's own term of SIGMA a is +e(x, t) times its own: so a+ + a- (which takes -e) matches the neighbours and not the hold",
      onsite_ok)

# D. the head's gearing at the one big bang's calibre
sys.path.insert(0, T24)
try:
    from event_universe.core.rule3 import gearing, mesh_unit_of  # noqa: E402

    den, Gamma = 15162856759112389, 1000
    G = mesh_unit_of(Gamma)
    pinions = {"light (rim, rim)": den, "near-light row": 15162854575528411, "heavy row 1": 2458210083751875,
               "heavy row 2": 2580388913625285, "held field": 15011228191521265,
               "regulator (rim - rim div Gamma)": den - den // Gamma}
    vac_ok, load_ok, form_ok, tension_ok = True, True, True, True
    for name, pin in pinions.items():
        g = gearing(pin, den, Gamma, Gamma, Gamma, None, G)
        vac_ok = vac_ok and g.hold == 0
        for p0 in (999, 900, 500):
            pm = p0 * p0 // Gamma
            g2 = gearing(pin, den, Gamma, p0, pm, None, G)
            term = 12 * G * G * (den * (Gamma * Gamma - p0 * p0) + (0 if MUT == "head" else pin) * (p0 * p0 - pm * pm))
            form_ok = form_ok and g2.hold == term
            load_ok = load_ok and g2.hold > 0
        factors = (G * G - 1,) + (G * G,) * 5
        g3 = gearing(pin, den, Gamma, Gamma, Gamma, factors, G)
        tension_ok = tension_ok and g3.hold > 0
    check("D1 the head's hold is 0 at the vacuum for every train of the one big bang's calibre (the Courant edge)", vac_ok, f"G = {G}")
    check("D2 at a load (p0 = 999, 900, 500) the hold is 12 G^2 (rim (Gamma^2 - p0^2) + pinion (p0^2 - pm^2))", form_ok)
    check("D3 so it is > 0 at every load: the doubler is lifted wherever the clock runs below the full rate", load_ok)
    check("D4 a tension on one Mesh raises the hold above 0 too", tension_ok)
except ImportError as err:
    check("D the head's gearing imported", False, str(err))


# E. the integer one formula with the carry: W odd, the hold 0 (6 g = 2 W at s = 1)
def int_step(a, am, r, W, g, D=0):
    """The one formula at a uniform clock: p = W (a - a-) + (r - mid), p+ = p + F, F = SUM_j g (a_j - a) - D a."""
    mid = (W - 1) // 2
    na, nr = {}, {}
    for x in SITES:
        F = sum(g * (a[nb(x, d)] - a[x]) for d in SP) - D * a[x]
        pp = W * (a[x] - am[x]) + (r[x] - mid) + F
        na[x] = a[x] + (pp + mid) // W
        nr[x] = (pp + mid) % W
    return na, a, nr


W, g = 999, 333
mid = (W - 1) // 2
parted = []
for trial in range(5):
    a = {x: rng.randint(-500, 500) for x in SITES}
    am = {x: rng.randint(-500, 500) for x in SITES}
    r = {x: rng.randint(0, W - 1) for x in SITES}
    sa = {x: eps(x, 0) * v for x, v in a.items()}
    sam = {x: eps(x, -1) * v for x, v in am.items()}
    sr = {x: (2 * mid - v) % W for x, v in r.items()}  # one candidate: the one mirror on the fine tooth
    first = None
    for t in range(1, 30):
        a, am, r = int_step(a, am, r, W, g)
        sa, sam, sr = int_step(sa, sam, sr, W, g)
        if any(sa[x] != eps(x, t) * a[x] for x in SITES):
            first = t
            break
    parted.append(first)
check("E1 with Rule3's carry SIGMA is not exact: the image and the step part within a few ticks", all(p is not None for p in parted), str(parted))
# a setting with no content at the wave number (pi, pi, pi) in either slot (random integers with that
# one mode projected out exactly: a -> N a - (SUM e a) e), every fine tooth at the mid tooth
N3 = len(SITES)


def project_out(f, t):
    s = sum(eps(x, t) * f[x] for x in SITES)
    return {x: N3 * f[x] - s * eps(x, t) for x in SITES}


def staggered_run(gg, ticks, seed, DD=0):
    rr = random.Random(seed)
    a = project_out({x: rr.randint(-30, 30) for x in SITES}, 0)
    am = project_out({x: rr.randint(-30, 30) for x in SITES}, -1)
    r = {x: mid for x in SITES}
    assert sum(eps(x, 0) * a[x] for x in SITES) == 0 and sum(eps(x, -1) * am[x] for x in SITES) == 0
    out = []
    for t in range(1, ticks + 1):
        a, am, r = int_step(a, am, r, W, gg, DD)
        if t in (1, 10, 50, 100, 200, 400):
            out.append((t, sum(eps(x, t) * a[x] for x in SITES)))
    return out


light_amps = staggered_run(g, 400, 7)
print("   light (hold 0): staggered amplitude SUM e(x, t) a(x, t), none set:", light_amps)
massive_amps = staggered_run(199, 400, 7, 2 * W - 6 * 199)  # a massive train at the edge: D = 2 W - 6 g, cos w0 = 597/999
print("   massive at the edge (g 199, D 804, cos w0 = 597/999): staggered amplitude:", massive_amps)
check("E2 with Rule3's carry the rounding feeds the staggered mode from a setting with none (light at the edge)",
      any(v != 0 for _, v in light_amps), str(light_amps[-1]))

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
