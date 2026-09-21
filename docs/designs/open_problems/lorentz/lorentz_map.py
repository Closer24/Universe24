"""Special relativity from the six verbs: the map of problem (2) of the seven
(the open-problems physicist, read-only, 2026-09-21; docs/designs/open_problems/lorentz/NOTE.md).

Integers of the flight rule (BEAM_LAW section 3, transcribed; no engine import). Nothing run.

(A) The transverse light clock on the flight table: a row aimed at a partner co-moving
    across the motion flies a direction D = (a, b, 0); its transit is the direction's own
    age at its Manhattan length, and the partner's speed is the row's x pace. The ratio
    of that transit to the rest transit across the same distance, against gamma (the
    Lorentz factor) at the direction's own beta = a / |D|: gamma from Pythagoras in the
    table's integers, no rule of the bodies.
(B) The longitudinal light clock: the round trip along the motion, d / (c - v) + d / (c + v),
    on the heading's pace c_h = 64 / 110 at v = 1 / k: gamma^2, the ether clock; the
    transverse round trip gamma: the anisotropy that is NATURE row 5b.
(C) A co-moving detector's age reading (host arithmetic, the flight rule only, arrivals):
    a lamp moving at v = 1 / k Links per interval on x releasing one row per interval on
    every in-plane primitive direction within Manhattan P, a detector body co-moving at
    the transverse offset d; the ages of the rows that arrive at the detector's Node
    while it is there, against gamma times the rest transit: a DETECTOR reading of gamma
    with no new rule, to the fan's grain.
(D) The cube's 48 and the bilinear forms: the symmetric 3 x 3 integer matrices fixed by
    every signed axis permutation are the multiples of the identity: the only isotropic
    even reading of a momentum within the six verbs is p . p (the exact square).
(E) Form B's pace 1 / (1 + 0.72 v) beside 1 / gamma: two different objects.

Run from the repository root:

    python docs/designs/open_problems/lorentz/lorentz_map.py > docs/designs/open_problems/lorentz/lorentz_map.out
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

Q = 64
C_CONT = 1 / math.sqrt(3)


def isqrt(n: int) -> int:
    return math.isqrt(n)


def bresenham(vector):
    s1 = sum(abs(c) for c in vector)
    line = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


class Line:
    def __init__(self, vector):
        self.vector = vector
        self.s1 = sum(abs(c) for c in vector)
        self.t_d = isqrt(3 * sum(c * c for c in vector) * Q * Q)
        self.steps = bresenham(vector)

    def age_of(self, made: int) -> int:
        rate, wall, start = 2 * self.s1 * Q, 2 * self.t_d, self.t_d
        return max(0, -(-(made * wall - start) // rate))

    def made_at(self, age: int) -> int:
        return (2 * age * self.s1 * Q + self.t_d) // (2 * self.t_d)

    def position(self, made: int):
        x = y = z = 0
        for j in range(made):
            sx, sy, sz = self.steps[j % self.s1]
            x, y, z = x + sx, y + sy, z + sz
        return (x, y, z)


HEADING = Line((1, 0, 0))
C_H = Fraction(Q, HEADING.t_d)


def gamma(beta: float) -> float:
    return 1 / math.sqrt(1 - beta * beta)


print("A. THE TRANSVERSE LIGHT CLOCK ON THE FLIGHT TABLE (host arithmetic on the table's integers)")
print(
    "   a row on D = (a, b, 0) reaches the point D at the age tau_D = age_of(S_1); a partner co-moving at v = a / tau_D Links per interval,"
)
print(
    "   b Links across the motion, receives it there; at rest the same partner b Links away on the heading (0, 1, 0) receives at age_of(b)"
)
print(
    "   D | S_1 | T_D | tau_D (the transit) | v = a / tau_D | beta = v sqrt 3 | the rest transit age_of(b) on the heading | tau_D / rest | gamma(beta) | the exact |D| / b"
)
for a in range(0, 7):
    for b in range(1, 13):
        if math.gcd(a, b) != 1 or a > b:
            continue
        line = Line((a, b, 0))
        tau = line.age_of(line.s1)
        rest = HEADING.age_of(b)
        v = a / tau if tau else 0.0
        beta = v * math.sqrt(3)
        exact = math.sqrt(a * a + b * b) / b
        print(
            f"   ({a}, {b}) | {line.s1:2d} | {line.t_d:4d} | {tau:3d} | {v:.4f} | {beta:.4f} | {rest:3d} | {tau / rest:.3f} | {gamma(beta):.3f} | {exact:.3f}"
        )
print(
    "   the continuum: tau_D = |D| / c and the rest transit b / c, the ratio |D| / b = 1 / sqrt(1 - (a / |D|)^2) = gamma exactly (Pythagoras);"
)
print(
    "   on the lattice the ratio carries the accumulator's whole intervals (one interval on transits of 5 to 20) and isqrt's rounding of T_D: gamma to the flight's grain"
)
print()

print(
    "B. THE LONGITUDINAL LIGHT CLOCK (closed forms on the heading's pace c_h = 64 / 110, a partner d Links ahead or behind, both at v = 1 / k)"
)
print(
    "   k | v | beta = v / c_h | forward d / (c_h - v) + back d / (c_h + v), over 2 d / c_h | gamma^2 | transverse 2 gamma d / c_h over 2 d / c_h | gamma"
)
for k in (2, 4, 8, 16, 32):
    v = Fraction(1, k)
    beta = float(v / C_H)
    forward = 1 / (float(C_H) - float(v))
    back = 1 / (float(C_H) + float(v))
    ratio = (forward + back) / (2 / float(C_H))
    print(
        f"   {k:2d} | {float(v):.4f} | {beta:.4f} | {ratio:.4f} | {gamma(beta) ** 2:.4f} | {gamma(beta):.4f} | {gamma(beta):.4f}"
    )
print(
    "   two arms of one length at right angles differ by gamma: Lorentz's contraction of the arm along the motion by 1 / gamma would close it; no verb contracts a Link"
)
print()


def in_plane_fan(bound: int):
    found = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            if (a or b) and abs(a) + abs(b) <= bound and math.gcd(abs(a), abs(b)) == 1:
                found.append((a, b, 0))
    return sorted(found)


def detector_ages(k: int, d: int, bound: int, horizon: int):
    """The lamp at (t // k, 0, 0) at the interval t releases one row per direction per
    interval (born at age 0 at its Node); the detector at (t // k, d, 0). A row born at t0
    on D is at lamp(t0) + position(made_at(t - t0)) at the interval t; it ARRIVES at the
    detector's Node at t if it is there at t and was not there at t - 1 (the click reads
    arrivals). The ages of the arrivals over t < horizon."""
    fan = [Line(v) for v in in_plane_fan(bound)]
    ages = []
    for line in fan:
        # the row's trajectory relative to its birth Node, per age, up to the horizon
        rel = [line.position(line.made_at(age)) for age in range(horizon)]
        for t0 in range(horizon):
            x0 = t0 // k
            for age in range(1, horizon - t0):
                t = t0 + age
                px, py, pz = rel[age]
                if pz != 0 or py > d:
                    if py > d and line.vector[1] > 0:
                        break
                    if pz != 0:
                        break
                    continue
                if py == d and x0 + px == t // k:
                    qx, qy, qz = rel[age - 1]
                    if not (qy == d and x0 + qx == (t - 1) // k):
                        ages.append(age)
    return ages


print(
    "C. A CO-MOVING DETECTOR'S AGE READING (host arithmetic on the flight rule; the arrivals only; the in-plane fan within Manhattan P)"
)
print(
    "   the lamp and the detector both at v = 1 / k Links per interval on x, the detector d Links across; the rows' ages at their arrivals at the detector's Node"
)
print(
    "   k | beta | d | P | directions | arrivals | mean age | rest mean age (k -> infinity: the heading's age_of(d)) | mean / rest | gamma"
)
for k in (4, 8, 16):
    beta = float(Fraction(1, k) / C_H)
    for d in (6, 12):
        for bound in (6, 12):
            ages = detector_ages(k, d, bound, 400)
            rest = HEADING.age_of(d)
            fan_n = len(in_plane_fan(bound))
            mean = sum(ages) / len(ages) if ages else float("nan")
            print(
                f"   {k:2d} | {beta:.4f} | {d:2d} | {bound:2d} | {fan_n:3d} | {len(ages):5d} | {mean:7.2f} | {rest:3d} | {mean / rest:.3f} | {gamma(beta):.3f}"
            )
print(
    "   the rows that reach a co-moving transverse partner are the ones aimed at (v tau, d): their age is the transverse transit, gamma d / c to the fan's grain;"
)
print(
    "   at rest only the heading (0, 1, 0) reaches the partner; the reading is a detector's (the click's age moment under reads: age), no rule of the bodies"
)
print()

print(
    "D. THE CUBE'S 48 AND THE BILINEAR FORMS: symmetric integer matrices M with P^T M P = M for every signed axis permutation P"
)
perms = []
for order in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        m = [[0] * 3 for _ in range(3)]
        for i in range(3):
            m[i][order[i]] = signs[i]
        perms.append(m)


def transform(m, p):
    # P^T M P
    out = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            out[i][j] = sum(p[a][i] * m[a][b] * p[b][j] for a in range(3) for b in range(3))
    return out


basis = []
for i in range(3):
    for j in range(i, 3):
        m = [[0] * 3 for _ in range(3)]
        m[i][j] = m[j][i] = 1
        basis.append(m)
fixed = 0
for m in basis:
    if all(transform(m, p) == m for p in perms):
        fixed += 1
# the invariant subspace: brute force over small integer combinations
found = set()
for coeffs in itertools.product(range(-2, 3), repeat=6):
    m = [[0] * 3 for _ in range(3)]
    for c, b in zip(coeffs, basis, strict=True):
        for i in range(3):
            for j in range(3):
                m[i][j] += c * b[i][j]
    if all(transform(m, p) == m for p in perms):
        found.add(tuple(tuple(r) for r in m))
print(
    f"   {len(perms)} signed permutations; symmetric integer matrices with coefficients in -2 .. 2 fixed by all 48: {len(found)} (the multiples c I, c = -2 .. 2): the invariant forms are c p . p"
)
print(
    "   so a body's own reading of its momentum that is even and isotropic under the cube is a multiple of p . p: the exact square Xi = m^2 + 3 p . p of covariant-readings-v1, the 3 the declared c^2 = [1, 3]"
)
print()

print("E. FORM B'S PACE BESIDE 1 / gamma (two objects: a dispersion of the drive, a rate of a clock)")
print(
    "   v (today's, Links per interval) | form B's v / today's = 1 / (1 + 0.72 v) | beta = v_B / c_h | 1 / gamma(beta) | covariant pace p c^2 / E at the same p / m"
)
for v_today in (0.05, 0.1, 0.2, 0.3, 0.4):
    v_b = v_today / (1 + 0.72 * v_today)
    beta = v_b / float(C_H)
    # today's v = p / (m + p): p / m = v / (1 - v); covariant: v = p c^2 / E = (p / m) / sqrt(1 + 3 (p / m)^2) in Links per interval with c^2 = 1 / 3
    pm = v_today / (1 - v_today)
    v_cov = pm / math.sqrt(
        1 + 3 * pm * pm
    )  # p c^2 / E = p / (E / c^2), E / c^2 = sqrt(m^2 + 3 p^2): 1 / sqrt 3 as p -> infinity
    print(
        f"   {v_today:.2f} | {1 / (1 + 0.72 * v_today):.4f} | {beta:.4f} | {1 / gamma(beta):.4f} | {v_cov:.4f}"
    )
print(
    "   form B caps the drive at the rows' pace and slows no clock; 1 / gamma is a clock's rate; the covariant pace p c^2 / E (E^2 = m^2 c^4 + p^2 c^2) is the relativistic dispersion"
)
