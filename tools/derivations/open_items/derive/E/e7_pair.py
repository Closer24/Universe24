"""Draft E, probe e7 (the side question): does an A1 source give the fitting's pair the singlet?

  python3 -I e7_pair.py            the claims (must print 0 failures)
  python3 -I e7_pair.py mutants    the mutations (each must fail)

The two fitted hands' spins live in E1/2 x E1/2 = A1 + T1. The states left fixed by a group H of lifts number
(1/|H|) SUM_h chi(h)^2, chi(h) = 2 Re(h). The probe counts them for the 48, for the lift of the Mesh's axis stabilizer
(16) and for the lift of the quarter turns about the Mesh alone (8), and checks the vectors: the singlet (0, 1, -1, 0)
and the triplet's component along the Mesh (0, 1, 1, 0). Exact numbers of Q(r2)(i), held as four Fractions.
"""

from __future__ import annotations

import sys
from fractions import Fraction as Fr
from itertools import product

FAIL = []


def check(name, ok, count=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if count is None else f": {count}"))


def r2m(x, y):
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def r2a(x, y):
    return (x[0] + y[0], x[1] + y[1])


def r2n(x):
    return (-x[0], -x[1])


def cm(a, b):
    return r2a(r2m(a[:2], b[:2]), r2n(r2m(a[2:], b[2:]))) + r2a(r2m(a[:2], b[2:]), r2m(a[2:], b[:2]))


def ca(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


C0 = (Fr(0),) * 4
C1 = (Fr(1), Fr(0), Fr(0), Fr(0))


def group48():
    z, half, inv = (Fr(0), Fr(0)), (Fr(1, 2), Fr(0)), (Fr(0), Fr(1, 2))
    els = set()
    for k in range(4):
        for s in (1, -1):
            q = [z] * 4
            q[k] = (Fr(s), Fr(0))
            els.add(tuple(q))
    for sg in product((1, -1), repeat=4):
        els.add(tuple((s * half[0], s * half[1]) for s in sg))
    for a in range(4):
        for b in range(a + 1, 4):
            for sa, sb in product((1, -1), repeat=2):
                q = [z] * 4
                q[a], q[b] = (sa * inv[0], sa * inv[1]), (sb * inv[0], sb * inv[1])
                els.add(tuple(q))
    return sorted(els)


def mat(q):
    a, b, c, d = q
    return ((a + r2n(d), r2n(c) + r2n(b)), (c + r2n(b), a + d))


def kron_apply(U, v):
    """(U x U) v on C^2 x C^2, v indexed (s1, s2) -> 2 s1 + s2."""
    out = [C0] * 4
    for s1, s2 in product(range(2), repeat=2):
        for t1, t2 in product(range(2), repeat=2):
            out[2 * s1 + s2] = ca(out[2 * s1 + s2], cm(cm(U[s1][t1], U[s2][t2]), v[2 * t1 + t2]))
    return tuple(out)


def fixed_count(H):
    tot = (Fr(0), Fr(0))
    for q in H:
        two_re = (2 * q[0][0], 2 * q[0][1])
        tot = r2a(tot, r2m(two_re, two_re))
    return (tot[0] / len(H), tot[1] / len(H))


def stabilizers(G):
    """The lifts of the turns keeping the z axis as a line (D4: 16) and as a ray (C4: 8)."""
    d4 = [q for q in G if (q[1] == (0, 0) and q[2] == (0, 0)) or (q[0] == (0, 0) and q[3] == (0, 0))]
    c4 = [q for q in G if q[1] == (0, 0) and q[2] == (0, 0)]
    return d4, c4


def vec(*xs):
    return tuple((Fr(x), Fr(0), Fr(0), Fr(0)) for x in xs)


def neg(v):
    return tuple(tuple(-x for x in c) for c in v)


def main_claims():
    G = group48()
    d4, c4 = stabilizers(G)
    print("1. The count of fixed two-spinor states, (1/|H|) SUM chi(h)^2")
    for name, H, want in (("the 48 (every turn of the cube)", G, 1), ("the Mesh's axis as a line (16 lifts, D4)", d4, 1), ("the quarter turns about the Mesh alone (8 lifts, C4)", c4, 2)):
        n = fixed_count(H)
        check(f"{name}: {n[0]} fixed state(s)", n == (Fr(want), Fr(0)) and len(H) in (48, 16, 8), len(H))
    singlet, along = vec(0, 1, -1, 0), vec(0, 1, 1, 0)
    print("2. The vectors")
    check("the singlet (0, 1, -1, 0) is fixed by all 48", all(kron_apply(mat(q), singlet) == singlet for q in G), 48)
    check("the triplet along the Mesh (0, 1, 1, 0) is fixed by the 8 quarter-turn lifts about it", all(kron_apply(mat(q), along) == along for q in c4), 8)
    perp = [q for q in d4 if q not in c4]
    check("and reversed by the 8 lifts of the half turns across it (those that exchange the Mesh's two ends)", all(kron_apply(mat(q), along) == neg(along) for q in perp), 8)
    print("3. So: a spin write that reads the light's A1 part and no axis (the 48) gives the singlet alone; one that reads")
    print("   the Mesh's axis (the lead along it, as the head's fitting does) keeps only the 8 and admits S . e as well.")


def mutants():
    G = group48()
    d4, c4 = stabilizers(G)
    bad = []
    print("M1. The triplet along the Mesh in place of the singlet: it must fail to be fixed by the 48")
    c = sum(kron_apply(mat(q), vec(0, 1, 1, 0)) != vec(0, 1, 1, 0) for q in G)
    print(f"  lifts that move it: {c} of 48 (must be above 0)")
    bad += [] if c else ["M1"]
    print("M2. The C4 count read as the singlet's: the count of fixed states under the 8 must not be 1")
    n = fixed_count(c4)
    print(f"  fixed states under the 8: {n[0]} (must not be 1)")
    bad += [] if n != (Fr(1), Fr(0)) else ["M2"]
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main_claims()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)
