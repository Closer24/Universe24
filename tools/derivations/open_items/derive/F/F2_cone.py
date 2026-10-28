"""F2: the act's cone against light's (draft F; root II items 21 and 23).

Exact integers and Fractions only, no float. Run: python3 -I F2_cone.py [MUTANT]
MUTANT: none (default), edge (the grip over the teeth read 1/3 + 1/300), pell (the boost
[[2, 3], [1, 2]] read [[2, 3], [1, 1]]), parity (the Green's function started on both slots,
which a one-slot pulse is not). Each mutant must make at least one check FAIL.

 A. the stencil's cone after t ticks is the L1 ball |x|+|y|+|z| <= t; light's long-wave sphere at
    the edge lambda = 1/3 has radius^2 = t^2 / 3, the L1 ball's inradius^2: Cauchy-Schwarz,
    (|x|+|y|+|z|)^2 <= 3 (x^2+y^2+z^2), equal only on the body diagonals;
 B. the rational leapfrog a+ = lambda SUM_j a_j - a- (the hold 0), a one-site pulse: its support is
    inside the L1 ball with the checkerboard's parity, every point of the ball's surface is reached,
    and the axis tip carries exactly 3^-t of the pulse;
 C. the integer one formula (p+ = p + F, a+ = a + (p+ + mid) div W, odd W) from a pulse of A notches:
    the farthest nonzero notch in L1 and in light's measure 3|x|^2 against t^2, so the reach
    beyond light's cone is read in integers;
 D. light's cone t^2 = 3 |x|^2 has an infinite group of integer boosts (Pell's unit 2 + sqrt 3),
    but a linear map that keeps both the cone's form and the stencil of one tick is in {+-1} x the
    48: no boost keeps the one act.
"""

import itertools
import sys
from fractions import Fraction as Fr

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


LAM = Fr(1, 3) + (Fr(1, 300) if MUT == "edge" else 0)

# ---------------------------------------------------------------- A. the geometry
ok_cs, eq_dirs = True, set()
R = 6
for x in itertools.product(range(-R, R + 1), repeat=3):
    l1 = sum(abs(v) for v in x)
    l2 = sum(v * v for v in x)
    if l1 * l1 > 3 * l2:
        ok_cs = False
    if l2 > 0 and l1 * l1 == 3 * l2:
        eq_dirs.add(tuple((v > 0) - (v < 0) for v in x))
check("A1 (|x|+|y|+|z|)^2 <= 3 |x|^2 on the box of side 13", ok_cs)
check("A2 equality only on the 8 body diagonals", len(eq_dirs) == 8 and all(0 not in d for d in eq_dirs), str(len(eq_dirs)))
# inradius of the L1 ball of radius 1: the point (1/3, 1/3, 1/3) of the face x + y + z = 1
foot = (Fr(1, 3),) * 3
check("A3 the L1 ball's inradius^2 is 1/3, light's c^2 at the edge", sum(v * v for v in foot) == LAM,
      f"inradius^2 1/3 against c^2 {LAM}")

# ---------------------------------------------------------------- B. the rational Green's function
N = 21  # torus side, more than 2 t + 1 for t <= 9
TT = 9
SP = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
SITES = list(itertools.product(range(N), repeat=3))


def wrap(v):
    return v - N if v > N // 2 else v


def step(now, before, lam):
    out = {}
    for x in SITES:
        s = Fr(0)
        for d in SP:
            y = ((x[0] + d[0]) % N, (x[1] + d[1]) % N, (x[2] + d[2]) % N)
            s += now.get(y, 0)
        v = lam * s - before.get(x, 0)
        if v != 0:
            out[x] = v
    return out


now = {(0, 0, 0): Fr(1)}
before = {(0, 0, 0): Fr(1)} if MUT == "parity" else {}
inside = parity = surface = tip = True
for t in range(1, TT + 1):
    now, before = step(now, before, LAM), now
    for x, v in now.items():
        c = tuple(wrap(u) for u in x)
        l1 = sum(abs(u) for u in c)
        if l1 > t:
            inside = False
        if (l1 - t) % 2 != 0:
            parity = False
    for x in SITES:
        c = tuple(wrap(u) for u in x)
        if sum(abs(u) for u in c) == t and now.get(x, 0) == 0:
            surface = False
    if now.get((t % N, 0, 0), 0) != Fr(1, 3 ** t):
        tip = False
check("B1 the support stays in the L1 ball |x|_1 <= t", inside)
check("B2 with the checkerboard's parity |x|_1 = t mod 2", parity)
check("B3 every point of the ball's surface |x|_1 = t is reached", surface)
check("B4 the axis tip carries exactly 3^-t of the pulse", tip)


# ---------------------------------------------------------------- C. the integer one formula's front
def integer_front(A, ticks, W, g):
    """The one formula p+ = p + F, a+ = a + (p+ + mid) div W from a one-site pulse of A notches (the before
    0, every fine tooth at mid). The pulse is symmetric under the 48, so the octant |x|, |y|, |z| holds it."""
    mid = (W - 1) // 2
    M = ticks + 2
    size = (M + 1) ** 3

    def idx(i, j, k):
        return (i * (M + 1) + j) * (M + 1) + k

    nbr = []
    for i in range(M + 1):
        for j in range(M + 1):
            for k in range(M + 1):
                nbr.append([idx(min(abs(i + d[0]), M), min(abs(j + d[1]), M), min(abs(k + d[2]), M)) for d in SP])
    a, am, r = [0] * size, [0] * size, [mid] * size
    a[idx(0, 0, 0)] = A
    rows = []
    for t in range(1, ticks + 1):
        na, nr = [0] * size, [0] * size
        for s_ in range(size):
            F = 0
            for y in nbr[s_]:
                F += g * (a[y] - a[s_])
            pp = W * (a[s_] - am[s_]) + (r[s_] - mid) + F
            na[s_] = a[s_] + (pp + mid) // W
            nr[s_] = (pp + mid) % W
        am, a, r = a, na, nr
        l1max, far = 0, 0
        for i in range(M + 1):
            for j in range(M + 1):
                for k in range(M + 1):
                    if a[idx(i, j, k)] != 0:
                        l1max = max(l1max, i + j + k)
                        far = max(far, i * i + j * j + k * k)
        rows.append((t, a[idx(t, 0, 0)] if t <= M else 0, l1max, far))
    return rows


W, g = 999, 333  # g / W = 1/3: the hold 2 W - 6 g = 0, the edge; W odd, so the carry rounds to the nearest
TICKS = 24
fronts = {}
for A in (10 ** 3, 10 ** 6):
    rows = integer_front(A, TICKS, W, g)
    fronts[A] = rows
    print(f"   pulse of {A} notches: (tick, axis tip notch, farthest L1, farthest |x|^2), every fourth tick:",
          [row for row in rows if row[0] % 4 == 0])


def thirds(A):
    """The axis tip's notch by the rounded third: the tip reads only the tip behind it, (g a + mid) div W."""
    out, v = [], A
    for _ in range(TICKS):
        v = (g * v + (W - 1) // 2) // W
        out.append(v)
    return out


ok_tip = all([row[1] for row in fronts[A]] == thirds(A) for A in fronts)
last_tip = {A: max([row[0] for row in fronts[A] if row[1] != 0] + [0]) for A in fronts}
check("C1 the axis tip carries the pulse's rounded thirds and goes dark after log3 of the notches",
      ok_tip and last_tip[10 ** 3] == 6 and last_tip[10 ** 6] == 13, str(last_tip))
check("C2 yet nonzero notches stand on the act's L1 surface |x|_1 = t at every tick to 24 (near the body diagonals)",
      all(row[2] == row[0] for A in fronts for row in fronts[A]))
ex = {A: 3 * fronts[A][-1][3] - TICKS * TICKS for A in fronts}
check("C3 at tick 24 the farthest nonzero notch stands beyond light's long-wave sphere (3|x|^2 > t^2), farther for more notches",
      0 < ex[10 ** 3] < ex[10 ** 6], f"3|x|^2 - t^2 = {ex[10 ** 3]} at 10^3 notches and {ex[10 ** 6]} at 10^6")

# ---------------------------------------------------------------- D. integer boosts of light's cone
B = ((2, 3), (1, 1)) if MUT == "pell" else ((2, 3), (1, 2))
Qm = ((1, 0), (0, -3))


def m2(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


Bt = ((B[0][0], B[1][0]), (B[0][1], B[1][1]))
check("D1 the boost (t, x) -> (2t + 3x, t + 2x) keeps t^2 - 3 x^2 and has determinant 1",
      m2(m2(Bt, Qm), B) == Qm and B[0][0] * B[1][1] - B[0][1] * B[1][0] == 1)
P = ((1, 0), (0, 1))
lengths = []
for k in range(1, 9):
    P = m2(P, B)
    lengths.append(P[0][0])
check("D2 its powers grow without bound (an infinite group of integer boosts)",
      all(lengths[i] < lengths[i + 1] for i in range(len(lengths) - 1)), str(lengths))
# the stencil of one tick in (t; x, y, z): two time steps and six Spokes
stencil = [(1, 0, 0, 0), (-1, 0, 0, 0)] + [(0,) + d for d in SP]


def Q4(v):
    return v[0] * v[0] - 3 * (v[1] * v[1] + v[2] * v[2] + v[3] * v[3])


img = [(2 * v[0] + 3 * v[1], v[0] + 2 * v[1], v[2], v[3]) for v in stencil]
check("D3 the boost maps the stencil off itself ((1;0,0,0) -> (2;1,0,0))", not set(img) <= set(stencil), str(img[0]))
# any linear map keeping the stencil permutes its 8 vectors and keeps Q4: time steps (Q4 = 1)
# go to time steps, Spokes (Q4 = -3) to Spokes, so it is +-1 on time times a signed permutation
check("D4 the stencil's Q4 values: 1 on the two time steps, -3 on the six Spokes, so no map keeping both mixes them",
      all(Q4(v) == 1 for v in stencil[:2]) and all(Q4(v) == -3 for v in stencil[2:]))

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
