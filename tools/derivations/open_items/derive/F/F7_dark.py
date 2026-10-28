"""F7: a dark train from the kinds (draft F; root VI, the owner's question of 2026-10-28, 13:1x UTC).

Exact integers and Fractions only, no float. Run: python3 -I F7_dark.py [MUTANT]
MUTANT: none (default), complex (the one-gear train given an imaginary part), pressure (the spring's
term in the discrete Lagrangian doubled), axion (E . B read with B polar). Each mutant must make at
least one check FAIL.

 A. a one-gear train (a real field, its own conjugate) has the sweep and the lead identically 0 at every
    Node-clock and Mesh: it sources neither the offset's time gear nor its odd gears, and the charge's
    couplings Q A0 and J . A of F4 vanish on it;
 B. of the four exact turns of a hand (1, i, -1, -i) only 1 and -1 keep a real gear real: a phase cannot act
    on it, so it carries no charge under the hand's phase;
 C. the homogeneous beat of a sprung one-gear train, a+ + a- = 2 c a, on exact periodic orbits (c = 1/2, 0,
    -1/2: periods 6, 4, 3): the discrete Lagrangian, the homogeneous pressure, averages to 0 over a period
    (dust, Turner 1983) while the wind stays positive;
 D. the one door the kinds leave between a real train and the link light: E . B is kept by the 24 and
    reversed by every mirror (the axion's coupling), E . E - B . B kept by all 48;
 E. the twin train's charge (the two-time density) is kept by the hands' common phase, a symmetry of the
    free twin step: a neutral twin train is a coupling of 0, not its kind (and F4: no twin pair is its own
    conjugate, so no Majorana twin train).
"""

import itertools
import random
import sys
from fractions import Fraction as Fr

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


def im_cx(a, b):
    return a[0] * b[1] - a[1] * b[0]


rng = random.Random(33)
L = 4
SITES = list(itertools.product(range(L), repeat=3))
E3 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def add(x, d):
    return tuple((x[i] + d[i]) % L for i in range(3))


# ---------------------------------------------------------------- A. no sweep, no lead
im_part = 1 if MUT == "complex" else 0
ok_sweep = ok_lead = True
for _ in range(20):
    now = {x: (rng.randint(-99, 99), im_part * rng.randint(-3, 3)) for x in SITES}
    before = {x: (rng.randint(-99, 99), im_part * rng.randint(-3, 3)) for x in SITES}
    ok_sweep = ok_sweep and all(im_cx(before[x], now[x]) == 0 for x in SITES)
    ok_lead = ok_lead and all(im_cx(now[x], now[add(x, E3[a])]) == 0 for x in SITES for a in range(3))
check("A1 a one-gear train's sweep Im(conj(a-) a) is 0 at every Node-clock (20 random boards)", ok_sweep)
check("A2 its lead Im(conj(a) a_j) is 0 on every Mesh: it sources nothing in the offset and the light's couplings Q A0, J . A vanish on it", ok_lead)

# ---------------------------------------------------------------- B. no phase on a real gear
units = [(1, 0), (0, 1), (-1, 0), (0, -1)]
keep_real = [u for u in units if all((u[0] * v - u[1] * 0, u[0] * 0 + u[1] * v)[1] == 0 for v in range(-5, 6))]
check("B1 of the hand's four exact turns only 1 and -1 keep a real gear real", sorted(keep_real) == [(-1, 0), (1, 0)], str(keep_real))


# ---------------------------------------------------------------- C. dust
def beat(c, a0, a1, n):
    seq = [a0, a1]
    while len(seq) < n + 2:
        seq.append(2 * c * seq[-1] - seq[-2])
    return seq


ok_dust, ok_wind, periods = True, True, {}
for c, period in ((Fr(1, 2), 6), (Fr(0), 4), (Fr(-1, 2), 3)):
    for _ in range(10):
        a0, a1 = Fr(rng.randint(-50, 50)), Fr(rng.randint(-50, 50))
        if a0 == 0 and a1 == 0:
            continue
        seq = beat(c, a0, a1, 3 * period)
        periodic = seq[period] == seq[0] and seq[period + 1] == seq[1]
        w = 2 if MUT == "pressure" else 1
        lag = [(seq[t] - seq[t - 1]) ** 2 / 2 - w * (1 - c) * (seq[t] ** 2 + seq[t - 1] ** 2) / 2 for t in range(1, period + 1)]
        wind = [seq[t] ** 2 + seq[t - 1] ** 2 - 2 * c * seq[t] * seq[t - 1] for t in range(1, period + 1)]
        ok_dust = ok_dust and periodic and sum(lag) == 0
        ok_wind = ok_wind and all(x == wind[0] for x in wind) and wind[0] > 0
    periods[str(c)] = period
check("C1 a sprung one-gear train's homogeneous beat: its Lagrangian (the homogeneous pressure) averages to 0 over each exact period (dust)",
      ok_dust, f"periods {periods}")
check("C2 while its wind is constant and positive on the orbit", ok_wind)

# ---------------------------------------------------------------- D. the door E . B
G48 = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        m = [[0] * 3 for _ in range(3)]
        for i in range(3):
            m[p[i]][i] = sg[i]
        G48.append(tuple(tuple(r) for r in m))


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def app(g, v):
    return tuple(sum(g[i][j] * v[j] for j in range(3)) for i in range(3))


Ev = (rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-9, 9))
Bv = (rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-9, 9))
dot = lambda u, v: sum(a * b for a, b in zip(u, v))  # noqa: E731
eb0, ee0 = dot(Ev, Bv), dot(Ev, Ev) - dot(Bv, Bv)
ok24 = ok_mirror = ok_ee = True
for g in G48:
    d = det3(g)
    Eg = app(g, Ev)
    Bg = tuple((1 if MUT == "axion" else d) * x for x in app(g, Bv))  # B axial: det g times g B
    if d == 1:
        ok24 = ok24 and dot(Eg, Bg) == eb0
    else:
        ok_mirror = ok_mirror and dot(Eg, Bg) == -eb0
    ok_ee = ok_ee and dot(Eg, Eg) - dot(Bg, Bg) == ee0
check("D1 E . B is kept by the 24 and reversed by every mirror (a pseudoscalar of the 48: the axion's coupling)",
      ok24 and ok_mirror and eb0 != 0, f"E . B = {eb0}")
check("D2 E . E - B . B is kept by all 48", ok_ee)


# ---------------------------------------------------------------- E. the twin train's charge
def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gc(a):
    return (a[0], -a[1])


def twin_density(n, b):
    return sum(im_cx(b[i], n[i]) for i in range(2))


ok_phase = True
for _ in range(50):
    n = ((rng.randint(-9, 9), rng.randint(-9, 9)), (rng.randint(-9, 9), rng.randint(-9, 9)))
    b = ((rng.randint(-9, 9), rng.randint(-9, 9)), (rng.randint(-9, 9), rng.randint(-9, 9)))
    for u in units:
        n2 = tuple(gm(u, c) for c in n)
        b2 = tuple(gm(u, c) for c in b)
        ok_phase = ok_phase and twin_density(n2, b2) == twin_density(n, b)
check("E1 the twin pair's two-time density (its charge) is kept by the common quarter turn of both hands", ok_phase)

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
