"""Verifier of draft E, probe v6: the side question. Is draft D's premise this draft's click law?

  python3 -I v6_side.py            the claims (must end with 0 failures)
  python3 -I v6_side.py mutants    the mutations (each must fail)

1. The states of E1/2 x E1/2 fixed by a group H of lifts, counted two ways: (1/|H|) SUM chi(h)^2, and the dimension of
   the solved fixed space (U x U) v = v for H's generators. For the 48, the 16 lifts of the Mesh's line, the 8 lifts of
   the quarter turns about it, and Q8.
2. Independence of the two premises:
   (a) draft D's (the fitting's spin write commutes with the 48: an axis-blind write) gives the singlet with no word on
       the exchange sign, since the fitted pair, a quantum and its antiquantum, carries no exchange term (draft E, part 1):
       the fixed space is one state for eps = +1 and eps = -1 alike;
   (b) draft E's (eps = nu, the A1 of two equal quanta) leaves a write that reads the Mesh's axis free to lay the
       triplet's component along the Mesh: two fixed states under the 8, whatever eps is.
   So neither premise gives the other.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction as Fr
from pathlib import Path

_spec = importlib.util.spec_from_file_location("v1g", Path(__file__).resolve().with_name("v1_group.py"))
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)

FAIL = []


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


def kron(U):
    return tuple(tuple(v1.mul(U[a][c], U[b][d]) for c in range(2) for d in range(2)) for a in range(2) for b in range(2))


def fixed_space(gens):
    rows = []
    for U in gens:
        W = kron(U)
        for r in range(4):
            eq = [W[r][c] for c in range(4)]
            eq[r] = v1.sub(eq[r], v1.E1)
            rows.append(eq)
    return v1.nullspace_field(rows, 4)


def count_by_characters(H):
    tot = v1.Z0
    for h in H:
        t = v1.tr(h)
        tot = v1.add(tot, v1.mul(t, t))
    return v1.sc(Fr(1, len(H)), tot)


def vec(*xs):
    return tuple(v1.rat(x) for x in xs)


def act(U, v):
    W = kron(U)
    return tuple(v1._dot(list(W[r]), list(v)) for r in range(4))


def main():
    G = v1.closure([v1.QA, v1.QB])
    d4 = v1.closure([v1.QA, v1.HX])
    c4 = v1.closure([v1.QA])
    q8 = v1.closure([v1.HZ, v1.HX])
    print("1. Fixed two-spinor states, by characters and by the solved fixed space")
    for name, H, gens, want in (("the 48", G, [v1.QA, v1.QB], 1), ("the 16 lifts of the Mesh's line (D4)", d4, [v1.QA, v1.HX], 1), ("the 8 quarter-turn lifts about the Mesh (C4)", c4, [v1.QA], 2), ("Q8", q8, [v1.HZ, v1.HX], 1)):
        n_char = count_by_characters(H)
        n_sol = len(fixed_space(gens))
        check(f"{name} ({len(H)} lifts): {v1.fmt(n_char)} by characters, {n_sol} solved", n_char == v1.rat(want) and n_sol == want)
    singlet, along = vec(0, 1, -1, 0), vec(0, 1, 1, 0)
    check("the singlet (0, 1, -1, 0) fixed by all 48", all(act(U, singlet) == singlet for U in G), 48)
    check("the triplet along the Mesh (0, 1, 1, 0) fixed by the 8", all(act(U, along) == along for U in c4), 8)
    perp = [U for U in d4 if U not in set(c4)]
    check("and reversed by the 8 end-exchanging half-turn lifts", all(act(U, along) == tuple(v1.neg(x) for x in along) for U in perp), len(perp))

    print("2. Independence of the two premises")
    swap = lambda v: (v[0], v[2], v[1], v[3])  # noqa: E731  the exchange of the two hands in E1/2 x E1/2
    fixed48 = fixed_space([v1.QA, v1.QB])
    s = fixed48[0]
    print(f"    the one state fixed by the 48: {[v1.fmt(x) for x in s]}, under the exchange of the two hands: {'odd' if swap(s) == tuple(v1.neg(x) for x in s) else 'even'}")
    check("(a) an axis-blind write gives one state, the same for eps = +1 and eps = -1 (the fitted pair has no exchange term)", len(fixed48) == 1)
    fixed8 = fixed_space([v1.QA])
    sym = sum(1 for v in fixed8 if swap(v) == v)
    check("(b) a write that reads the Mesh's axis keeps two states (the singlet and the triplet along the Mesh), whatever eps", len(fixed8) == 2, f"{len(fixed8)} states")
    print("   so 'draft D's premise is therefore this draft's click law' does not follow: D's is a covariance of the fitting's")
    print("   write, E's is the A1 of two equal quanta choosing eps; the head's fitting breaks D's and leaves E's untouched")


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    G = v1.closure([v1.QA, v1.QB])
    print("M1. the triplet along the Mesh in place of the singlet: the 48 must move it")
    along = vec(0, 1, 1, 0)
    report("lifts that move it", sum(act(U, along) != along for U in G), 48)
    print("M2. the C4 count read as one: the fixed states under the 8 must not be 1")
    n = len(fixed_space([v1.QA]))
    report("fixed states beyond one", n - 1, 1)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)
