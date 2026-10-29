"""Bell's late choice on the fair draw: the pair's split click, read at the click with the axes chosen after the birth.

usage: python3 -I p4_bell_late.py <tensor24 worktree>/src
The detectors are Gaussian-integer spinors, a = (1, 0), a' = (1, 1), b = (5, 2), b' = (5, -2), each outcome's spinor
phi+ = phi and phi- = (-conj phi_2, conj phi_1); a spinor's axis m = (2 Re(p1* p2), 2 Im(p1* p2), |p1|^2 - |p2|^2).
(A) The pair clicks as one (the plan's item (l)): one draw over the four joint outcomes, sizes sigma_st =
    N(det[phi_A^s, phi_B^t]), L = SUM sigma = 2 rho_A rho_B, the outcomes ordered ++, +-, -+, -- for the rank count.
    Exact over the draw's full turn: E, S, and each side's marginal for every axis of the other (no signal).
(B) The same with the head's sorted draw's distribution in place of the fair one: the marginals then read the far axis.
(C) The pair carried along the Meshes (the local Bell click, task #37): the first click splits its open twins half
    and half by its own fair draw and sends the closure, one Mesh per tick; a partner that clicks after the closure
    lands reads the closed twins against its own axis, chosen late; one that clicks before reads them open.
    Exact over both draws' full turns, at each arrival.
(D) The same pairs on 7a's act, each draw d = (c + V) mod L at the clicking Node-clock (p2's board, pitch units), the
    four settings chosen at the click by a third Node-clock's draw: S and its spread.
(E) Tsirelson over every pair of axis pairs from small spinors: the largest |S| of exact integer cosines.
"""
import importlib.util
import itertools
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(z):
    return z.real * z.real + z.imag * z.imag


def perp(p):
    return (-p[1].conjugate(), p[0].conjugate())


def axis(p):
    x = p[0].conjugate() * p[1]
    return (int(2 * x.real), int(2 * x.imag), int(norm(p[0]) - norm(p[1])))


def rho(p):
    return int(norm(p[0]) + norm(p[1]))


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def sizes(pa, pb):
    out = []
    for u in (pa, perp(pa)):
        for v in (pb, perp(pb)):
            out.append(int(round(norm(det(u, v)))))
    return out  # ++, +-, -+, --


def part_of(d, sz):
    s = rank = 0
    for sigma in sz[:-1]:
        s += sigma
        rank += 1 if d >= s else 0
    return rank


def joint_by(sz, weight_of):
    """The four outcomes' probabilities when the draw number d over [0, L) has the weights weight_of(d, L)."""
    L = sum(sz)
    p = [Fraction(0)] * 4
    for d in range(L):
        p[part_of(d, sz)] += weight_of(d, L)
    return p


def fair(d, L):
    return Fraction(1, L)


def E_of(p):
    return p[0] - p[1] - p[2] + p[3]


A = {"a": (complex(1, 0), complex(0, 0)), "a'": (complex(1, 0), complex(1, 0))}
B = {"b": (complex(5, 0), complex(2, 0)), "b'": (complex(5, 0), complex(-2, 0))}
print("the axes:", {k: (axis(v), rho(v)) for k, v in {**A, **B}.items()})


def chsh(weight_of):
    E = {}
    marg = {}
    for ka, pa in A.items():
        for kb, pb in B.items():
            p = joint_by(sizes(pa, pb), weight_of)
            E[(ka, kb)] = E_of(p)
            marg[(ka, kb)] = (p[0] + p[1], p[0] + p[2])  # P(A +), P(B +)
    S = E[("a", "b")] + E[("a", "b'")] + E[("a'", "b")] - E[("a'", "b'")]
    return S, E, marg


S, E, marg = chsh(fair)
print(f"(A) the pair clicks as one, the fair draw over its full turn: E {dict((k, str(v)) for k, v in E.items())}")
print(f"    S = {S} = {float(S):.5f} (Tsirelson 2 sqrt 2 = {2 * math.sqrt(2):.5f}, the local bound 2)")
print(f"    the marginals P(A+), P(B+) at every setting: {sorted(set(str(x) for m in marg.values() for x in m))}: "
      f"no side reads the other's axis")


# (B) the head's sorted draw: c from three binary digits sorted and composed (c in {0, 1, 3, 7}: 1/8, 3/8, 3/8, 1/8 over
# the room 8), the part by c L = t room + r (the head's form), the number t = c L div room
head_c = {0: Fraction(1, 8), 1: Fraction(3, 8), 3: Fraction(3, 8), 7: Fraction(1, 8)}


def head_joint(sz):
    L = sum(sz)
    p = [Fraction(0)] * 4
    for c, w in head_c.items():
        t = c * L // 8
        p[part_of(t, sz)] += w
    return p


Eh, mh = {}, {}
for ka, pa in A.items():
    for kb, pb in B.items():
        p = head_joint(sizes(pa, pb))
        Eh[(ka, kb)] = E_of(p)
        mh[(ka, kb)] = (p[0] + p[1], p[0] + p[2])
Sh = Eh[("a", "b")] + Eh[("a", "b'")] + Eh[("a'", "b")] - Eh[("a'", "b'")]
print(f"(B) the head's sorted draw (three binary digits, c over room 8): S = {Sh} = {float(Sh):.4f}")
for k in sorted(mh):
    print(f"    setting {k}: P(A+) {mh[k][0]}, P(B+) {mh[k][1]}")
print("    so B's marginal moves with A's axis (and A's with B's): the composite click would signal on that draw")

# (C) the pair carried along the Meshes: A first, its open twins half and half; B after the closure lands, or before
def carried(pa, pb, landed):
    """Exact over A's full turn (its open twins: sizes rho_A, rho_A, L = 2 rho_A) and B's full turn."""
    ra, rb = rho(pa), rho(pb)
    ma, mb = axis(pa), axis(pb)
    p = [Fraction(0)] * 4
    for sA in (+1, -1):  # A's draw over its turn: up for rho_A of 2 rho_A values
        pA = Fraction(1, 2)
        if landed:
            # B's twins closed to the opposite of A's outcome along A's axis: S_B = -sA rho_B m_A / rho_A
            sm = Fraction(-sA * rb * sum(x * y for x, y in zip(ma, mb)), ra)
            LB = rb * rb
            up = (LB + sm) / 2  # sigma_up of B's closed twins against b
            pB = up / LB
        else:
            pB = Fraction(1, 2)  # still open: half and half
        p[0 if sA > 0 else 2] += pA * pB
        p[1 if sA > 0 else 3] += pA * (1 - pB)
    return p


for landed in (True, False):
    Ec = {}
    for ka, pa in A.items():
        for kb, pb in B.items():
            Ec[(ka, kb)] = E_of(carried(pa, pb, landed))
    Sc = Ec[("a", "b")] + Ec[("a", "b'")] + Ec[("a'", "b")] - Ec[("a'", "b'")]
    when = "after the closure lands" if landed else "before the closure lands (outside its cone)"
    print(f"(C) carried along the Meshes, B's axis chosen late and B clicking {when}: S = {Sc}")

# (D) on 7a's act: each pair at one beat, the settings drawn at the click by a third Node-clock's dial
spec = importlib.util.spec_from_file_location("p2", os.path.join(HERE, "p2_fair_draw_engine.py"))
argv, sys.argv = sys.argv, [sys.argv[0], sys.argv[1]]
p2 = importlib.util.module_from_spec(spec)
import builtins  # noqa: E402

_print, builtins.print = builtins.print, (lambda *a, **k: None)
spec.loader.exec_module(p2)
builtins.print = _print
nb, records = p2.run(13, True, ticks=4000, pitch=True)
SITE_A, SITE_B, SITE_S = 0, 3 + 6 * 3 + 36 * 3, 5 + 6 * 1 + 36 * 4  # three Node-clocks apart on the (6, 6, 6) board
tally = {k: [0, 0] for k in E}  # per setting: the sum of products and the count
for c, v in records[50:]:
    pick = (int(c[SITE_S]) + int(v[SITE_S])) % 4  # the late choice, a third Node-clock's draw at the click
    ka, kb = (("a", "b"), ("a", "b'"), ("a'", "b"), ("a'", "b'"))[pick]
    sz = sizes(A[ka], B[kb])
    L = sum(sz)
    d = (int(c[SITE_A]) + int(v[SITE_A])) % L  # the pair's one draw, at the Node-clock where it clicks
    k = part_of(d, sz)
    tally[(ka, kb)][0] += (1, -1, -1, 1)[k]
    tally[(ka, kb)][1] += 1
Ed = {k: Fraction(t[0], t[1]) for k, t in tally.items()}
Sd = Ed[("a", "b")] + Ed[("a", "b'")] + Ed[("a'", "b")] - Ed[("a'", "b'")]
spread = math.sqrt(sum((1 - float(Ed[k]) ** 2) / tally[k][1] for k in tally))
print(f"(D) on 7a's act, {sum(t[1] for t in tally.values())} pairs, the settings drawn late at a third Node-clock "
      f"({[tally[k][1] for k in sorted(tally)]} per setting): S = {float(Sd):.4f}, spread {spread:.4f}, against "
      f"{float(S):.4f}")

# (E) Tsirelson over the exact axes of real spinors (p, q), p and q from -6 to 6: m = (2 p q, 0, p^2 - q^2), rho = p^2 + q^2
units = {}
for p_, q_ in itertools.product(range(-6, 7), repeat=2):
    r = p_ * p_ + q_ * q_
    if r:
        u = (Fraction(2 * p_ * q_, r), Fraction(p_ * p_ - q_ * q_, r))
        units.setdefault(u, (p_, q_))
planar = list(units)
cos = lambda u, v: u[0] * v[0] + u[1] * v[1]  # noqa: E731
best, arg = Fraction(0), None
C = {(i, j): cos(planar[i], planar[j]) for i in range(len(planar)) for j in range(len(planar))}
n = len(planar)
for i in range(n):
    for i2 in range(n):
        if i2 == i:
            continue
        for j in range(n):
            ci_j, ci2_j = C[(i, j)], C[(i2, j)]
            for j2 in range(n):
                val = abs(ci_j + C[(i, j2)] + ci2_j - C[(i2, j2)])
                if val > best:
                    best, arg = val, (units[planar[i]], units[planar[i2]], units[planar[j]], units[planar[j2]])
print(f"(E) every CHSH of exact integer cosines over the axes of real spinors with parts from -6 to 6: the largest "
      f"|S| = {best} = {float(best):.6f} at the spinors {arg}, below 2 sqrt 2 = {2 * math.sqrt(2):.6f}: "
      f"{best * best < 8}")
sys.argv = argv
