"""Toy: the fitting's lay under the 24, and the ladder by the light's family (Animate; the owner's word of 2026-10-28,
15:2x UTC: the clocks' problems, the laws that are missing, the couplings and the families).

1. The lay of a fitting's two twin children is a pair state Psi (Psi_ab for u_a v_b, a 2 x 2 Gaussian matrix). A turn of
   the 24 with the twins' lift M sends it to M Psi M^T. A lay rule f (the state laid on a Mesh of axis a) keeps the 24
   iff M f(a) M^T is proportional to f(R a) for every turn R and every axis a (R a the image axis). Three rules:
     head      the up twin at one end and the down twin at the other, e_up x e_down, on every Mesh (click.fitted);
     singlet   the A1 part, eps = [[0, 1], [-1, 0]], on every Mesh (the light A1, the kind kept);
     vector    the T1 part along the Mesh's axis, sigma_a eps (the light's lead along the Mesh, the kind kept).
   The 24's lifts are closed from three generators in Gaussian rationals and counted up to a scalar (24 classes).
   Also read: each child's own state under the singlet (rho, S) = (1, 0): its winding split half and half between its
   twins along every axis, so a detector's click has something to decide.
2. The ladder of kinds per bang from the calibre's families, each bang fusing every pair of kinds present, with Pauli's
   rule (equal quanta take their kind's own symmetric part; ladder_pauli.py): the light as A1 (the head's one-gear
   light), the light as T1 (a vector light, three Gaussian gears, like nature's photon), each with and without the twin
   hands.
"""

import os
import sys
from fractions import Fraction as Q

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ANIMATE-PROBES-3"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ANIMATE-PROBES-2"))


# Gaussian rationals as pairs (re, im) of Fractions
def gr(a, b=0):
    return (Q(a), Q(b))


def gmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def gadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def gdiv(x, y):
    n = y[0] * y[0] + y[1] * y[1]
    return ((x[0] * y[0] + x[1] * y[1]) / n, (x[1] * y[0] - x[0] * y[1]) / n)


ZERO = gr(0)


def mmul(a, b):
    return [[gadd(gmul(a[i][0], b[0][j]), gmul(a[i][1], b[1][j])) for j in range(2)] for i in range(2)]


def transpose(a):
    return [[a[0][0], a[1][0]], [a[0][1], a[1][1]]]


def canon(m):
    """The matrix divided by its first nonzero entry: one representative per class up to a scalar."""
    first = next(x for row in m for x in row if x != ZERO)
    return tuple(gdiv(x, first) for row in m for x in row)


def proportional(a, b):
    flat_a = [x for row in a for x in row]
    flat_b = [x for row in b for x in row]
    if all(x == ZERO for x in flat_a) or all(x == ZERO for x in flat_b):
        return all(x == ZERO for x in flat_a) and all(x == ZERO for x in flat_b)
    return canon(a) == canon(b)


GENERATORS = [
    [[gr(1, -1), ZERO], [ZERO, gr(1, 1)]],  # a quarter turn about z
    [[gr(1), gr(0, -1)], [gr(0, -1), gr(1)]],  # a quarter turn about x
    [[gr(1, -1), gr(-1, -1)], [gr(1, -1), gr(1, 1)]],  # a third of a turn about (1, 1, 1)
]
SIGMA = {
    "x": [[ZERO, gr(1)], [gr(1), ZERO]],
    "y": [[ZERO, gr(0, -1)], [gr(0, 1), ZERO]],
    "z": [[gr(1), ZERO], [ZERO, gr(-1)]],
}
EPS = [[ZERO, gr(1)], [gr(-1), ZERO]]
UP_DOWN = [[ZERO, gr(1)], [ZERO, ZERO]]


def closure():
    found = {canon(GENERATORS[0]): GENERATORS[0]}
    frontier = list(found.values())
    while frontier:
        nxt = []
        for m in frontier:
            for g in GENERATORS:
                p = mmul(m, g)
                key = canon(p)
                if key not in found:
                    found[key] = p
                    nxt.append(p)
        frontier = nxt
    return list(found.values())


def inverse(m):
    det = gadd(gmul(m[0][0], m[1][1]), gmul((-m[0][1][0], -m[0][1][1]), m[1][0]))
    return [
        [gdiv(m[1][1], det), gdiv((-m[0][1][0], -m[0][1][1]), det)],
        [gdiv((-m[1][0][0], -m[1][0][1]), det), gdiv(m[0][0], det)],
    ]


def image_axis(m, a):
    """The axis b with M sigma_a M^-1 proportional to sigma_b."""
    turned = mmul(mmul(m, SIGMA[a]), inverse(m))
    return next(b for b in "xyz" if proportional(turned, SIGMA[b]))


def lay(rule, a):
    if rule == "head":
        return UP_DOWN
    if rule == "singlet":
        return EPS
    return mmul(SIGMA[a], EPS)


def covariant(rule, lifts):
    held = 0
    for m in lifts:
        for a in "xyz":
            b = image_axis(m, a)
            if proportional(mmul(mmul(m, lay(rule, a)), transpose(m)), lay(rule, b)):
                held += 1
    return held


def child_state(psi):
    """A child's own two-point reading from the pair: rho_ab = SUM_c Psi_ac conj(Psi_bc); returns (rho, S)."""
    conj = [[(x[0], -x[1]) for x in row] for row in psi]
    r = mmul(psi, transpose(conj))
    rho = r[0][0][0] + r[1][1][0]
    sx = 2 * r[1][0][0]
    sy = 2 * r[1][0][1]
    sz = r[0][0][0] - r[1][1][0]
    return rho, (sx, sy, sz)


def main():
    lifts = closure()
    print(f"1. the 24's lifts closed from three generators: {len(lifts)} classes up to a scalar")
    for rule in ("head", "singlet", "vector"):
        print(
            f"   the lay {rule:8s}: the 24 kept at {covariant(rule, lifts)} of {3 * len(lifts)} (turn, axis) cases"
        )
    for name, psi in (("head", UP_DOWN), ("singlet", EPS), ("vector z", mmul(SIGMA["z"], EPS))):
        rho, s = child_state(psi)
        print(f"   a child's own state under the {name:8s} lay: rho {rho}, S {tuple(int(x) for x in s)}")

    from kinds_ladder import KINDS  # noqa: E402
    from ladder_pauli import ladder  # noqa: E402

    print(
        "2. the ladder by the light's family (Pauli's rule: equal pairs take their own part; the fitting's pair unequal)"
    )
    starts = {
        "light A1": {"A1"},
        "light T1 (vector)": {"A1", "T1"},
        "light A1 + twins": {"A1", "E1/2"},
        "light T1 + twins": {"A1", "T1", "E1/2"},
    }
    for name, start in starts.items():
        rungs = ladder(start, lambda n: {"E1/2"} if n == 1 else set(), bangs=5)
        full = next((n for n, r in enumerate(rungs, start=1) if len(r) == len(KINDS)), None)
        print(
            f"   {name:18s}: kinds per bang {[len(r) for r in rungs]}; the last {rungs[-1]}; all eight at {full}"
        )


if __name__ == "__main__":
    main()
