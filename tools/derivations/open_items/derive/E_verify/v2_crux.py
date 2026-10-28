"""Verifier of draft E, probe v2: the crux, step 4. Is eps_T = nu forced, or a premise?

  python3 -I v2_crux.py            the claims (prints its counts; must end with 0 failures)
  python3 -I v2_crux.py mutants    the mutations (each must fail), and the mutant world eps = -nu read against every law

The joint click of two equal quanta: sigma_ab = N(M_a1 M_b2 + eps M_b1 M_a2), M_aj = <phi_a, psi_j>.
1. Step 2: which Gaussian units eps keep every size when the two quanta are relabelled.
2. Covariance: the 48 turning parts and quanta together keep every size, for eps = +1 AND eps = -1, on the twin hands
   (E1/2), the vectors (T1) and G3/2. So the 48's invariance of the click does not choose eps.
3. The A1 premise: the A1 component of psi1 x psi2 + eps psi2 x psi1 is (1 + eps nu) B(psi1, psi2), B the kind's one
   invariant form (solved, v1). It is nonzero for some pair iff eps = nu. This is the one place eps is chosen.
4. The world eps = -nu (spin one half bosons, spinless fermions) read against the draft's other laws: sizes are norms,
   relabelling, covariance, the books (Cauchy-Binet), T and Kramers (a property of the kind, not of eps).
5. A frame-blind click at one Node-clock (the quanta turned, the parts kept) chooses eps = -1 on the twin hands, but it
   fails for the vectors with either sign: it cannot be a law for every train alike.
Exact numbers only (Q(zeta24) from v1; Gaussian integers).
"""

from __future__ import annotations

import importlib.util
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

_spec = importlib.util.spec_from_file_location("v1g", Path(__file__).resolve().with_name("v1_group.py"))
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)

FAIL = []
RNG = random.Random(19281940)
add, sub, mul, conj, neg, sc, rat, Z0, E1, I_ = v1.add, v1.sub, v1.mul, v1.conj, v1.neg, v1.sc, v1.rat, v1.Z0, v1.E1, v1.I_


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


def gz(a, b):
    """The Gaussian integer a + b i as a number of Q(zeta24)."""
    return add(rat(a), sc(Fr(b), I_))


def rvec(n, k=6):
    while True:
        v = tuple(gz(RNG.randint(-k, k), RNG.randint(-k, k)) for _ in range(n))
        if any(any(x) for x in v):
            return v


def inner(u, v):
    out = Z0
    for x, y in zip(u, v):
        out = add(out, mul(conj(x), y))
    return out


def nrm(a):
    return mul(a, conj(a))


def apply(M, v):
    return tuple(v1._dot(list(M[r]), list(v)) for r in range(len(M)))


def inner_h(H, u, v):
    """u^dagger H v, H the kind's invariant Hermitian form (H = SUM_g rho(g)^dagger rho(g))."""
    return inner(u, apply(H, v))


def sizes(parts, q1, q2, eps, H=None):
    if H is None:
        M = [[inner(p, q1), inner(p, q2)] for p in parts]
    else:
        M = [[inner_h(H, p, q1), inner_h(H, p, q2)] for p in parts]
    K = len(parts)
    return {(a, b): nrm(add(mul(M[a][0], M[b][1]), mul(eps, mul(M[b][0], M[a][1])))) for a in range(K) for b in range(K)}


def bform(B, u, v):
    out = Z0
    for i in range(len(u)):
        for j in range(len(v)):
            if any(B[i][j]):
                out = add(out, mul(B[i][j], mul(u[i], v[j])))
    return out


def main():
    G = v1.closure([v1.QA, v1.QB])
    reps, _r = v1.kinds_explicit(G)
    gens = [v1.QA, v1.QB]
    units = {"+1": rat(1), "-1": rat(-1), "+i": I_, "-i": neg(I_)}

    print("1. Step 2: the units eps that keep every size when the quanta are relabelled (psi1 <-> psi2)")
    keep = {}
    for name, eps in units.items():
        n = 0
        for _ in range(300):
            parts = [rvec(2), rvec(2)]
            q1, q2 = rvec(2), rvec(2)
            n += sizes(parts, q1, q2, eps) == sizes(parts, q2, q1, eps)
        keep[name] = n
    print(f"    configurations of 300 whose sizes are label-free: {keep}")
    check("only eps = +1 and eps = -1 make the sizes label-free (eps eps = 1 forced by relabelling, no 3D topology used)", keep["+1"] == keep["-1"] == 300 and keep["+i"] < 300 and keep["-i"] < 300)

    print("2. Covariance: the 48 turning parts and quanta together keep every size, for both signs")
    for kind, trials in (("E1/2", 12), ("T1", 12), ("G3/2", 4)):
        rep = reps[kind]
        n = len(rep[G[0]])
        H = v1.ident(n)
        H = tuple(tuple(Z0 for _ in range(n)) for _ in range(n))
        for g in G:
            P = v1.mm(v1.mdag(rep[g]), rep[g])
            H = tuple(tuple(add(H[i][j], P[i][j]) for j in range(n)) for i in range(n))
        unitary = all(v1.mm(v1.mdag(rep[g]), rep[g]) == v1.ident(n) for g in G)
        kept = {"+1": 0, "-1": 0}
        total = 0
        for _ in range(trials):
            parts = [rvec(n) for _ in range(n)]
            q1, q2 = rvec(n), rvec(n)
            base = {e: sizes(parts, q1, q2, units[e], H) for e in kept}
            for g in G:
                M = rep[g]
                gp = [apply(M, p) for p in parts]
                total += 1
                for e in kept:
                    kept[e] += sizes(gp, apply(M, q1), apply(M, q2), units[e], H) == base[e]
        print(f"    {kind}: matrices unitary in the plain form: {unitary}; overlaps read with the invariant form H = SUM g^dagger g")
        check(f"{kind}: sizes kept by every lift, eps = +1 and eps = -1", kept["+1"] == kept["-1"] == total, f"+1: {kept['+1']} of {total}, -1: {kept['-1']} of {total}")
    print("   so the 48's invariance of the joint click holds for either sign on every kind: it does not choose eps")

    print("3. The A1 premise chooses eps: the A1 part of psi1 x psi2 + eps psi2 x psi1 is (1 + eps nu) B(psi1, psi2)")
    chosen = {}
    for kind, rep in reps.items():
        n = len(rep[G[0]])
        B = v1.invariant_forms(rep, gens, n)[0]
        nu = 1 if v1.mT(B) == B else -1
        nonzero = {"+1": 0, "-1": 0}
        for _ in range(40):
            q1, q2 = rvec(n), rvec(n)
            for e in nonzero:
                a1 = add(bform(B, q1, q2), mul(units[e], bform(B, q2, q1)))
                nonzero[e] += any(a1)
        allowed = [e for e in nonzero if nonzero[e] > 0]
        chosen[kind] = (nu, allowed)
        print(f"    {kind:5s}: nu = {nu:+d}; pairs of 40 with a nonzero A1 part: eps = +1 {nonzero['+1']}, eps = -1 {nonzero['-1']}")
    check("on every kind exactly one sign lets two equal quanta reach the A1, and it is nu", all(allowed == [f"{nu:+d}"] for nu, allowed in chosen.values()), f"{sum(allowed == [f'{nu:+d}'] for nu, allowed in chosen.values())} of 8")

    print("4. The world eps = -nu read against the draft's other laws (twin hands as bosons, a hand as a fermion)")
    T = lambda v: (neg(conj(v[1])), conj(v[0]))  # noqa: E731
    rho = lambda v: add(nrm(v[0]), nrm(v[1]))  # noqa: E731
    ok = {"sizes are norms (non-negative rationals)": 0, "books: SUM sigma = 2 lam^2 (rho1 rho2 + eps N<psi1, psi2>), the frame (phi, T phi)": 0, "relabelling keeps every size": 0, "T commutes with all 48 and T T = -1 (the kind's, not eps's)": 0}
    trials = 200
    for _ in range(trials):
        f = rvec(2)
        parts = [f, T(f)]
        q1, q2 = rvec(2), rvec(2)
        s = sizes(parts, q1, q2, rat(1))
        lam = rho(f)
        ok["sizes are norms (non-negative rationals)"] += all(all(c == 0 for c in x[1:]) and x[0] >= 0 for x in s.values())
        tot = Z0
        for x in s.values():
            tot = add(tot, x)
        want = sc(Fr(2), mul(mul(lam, lam), add(mul(rho(q1), rho(q2)), nrm(inner(q1, q2)))))
        ok["books: SUM sigma = 2 lam^2 (rho1 rho2 + eps N<psi1, psi2>), the frame (phi, T phi)"] += tot == want
        ok["relabelling keeps every size"] += s == sizes(parts, q2, q1, rat(1))
    for g in G:
        v = rvec(2)
        ok["T commutes with all 48 and T T = -1 (the kind's, not eps's)"] += apply(g, T(v)) == T(apply(g, v)) and T(T(v)) == (neg(v[0]), neg(v[1]))
    for name, c in ok.items():
        of = 48 if name.startswith("T ") else trials
        check(f"eps = +1 on the twin hands: {name}", c == of, f"{c} of {of}")
    pz = 0
    for _ in range(trials):
        f = rvec(2)
        s = sizes([f, T(f)], rvec(2), rvec(2), rat(1))
        pz += any(s[(a, a)] != Z0 for a in range(2))
    a1_two = 0
    for _ in range(trials):
        q1, q2 = rvec(2), rvec(2)
        a1_two += any(add(v1.sub(mul(q1[0], q2[1]), mul(q1[1], q2[0])), v1.sub(mul(q2[0], q1[1]), mul(q2[1], q1[0]))))
    print(f"    what the eps = +1 world fails: Pauli's zero (sigma_aa > 0 at {pz} of {trials}); the A1 of two quanta (nonzero at {a1_two} of {trials})")
    check("so on the twin hands eps = +1 breaks only Pauli and the A1 premise, nothing else the draft states", pz == trials and a1_two == 0)
    hand_zero = 0
    for _ in range(trials):
        p = rvec(1)
        q1, q2 = rvec(1), rvec(1)
        hand_zero += sizes([p], q1, q2, rat(-1))[(0, 0)] == Z0
    check("eps = -1 on a hand (A1): two quanta at one Node-clock never click (spinless fermions), consistent but no A1 pair", hand_zero == trials, f"{hand_zero} of {trials}")

    print("5. A frame-blind click at one Node-clock (the two quanta turned, the parts kept): a law for every train?")
    for kind, trials2 in (("E1/2", 10), ("T1", 10)):
        rep = reps[kind]
        n = len(rep[G[0]])
        blind = {"+1": 0, "-1": 0}
        tot = 0
        for _ in range(trials2):
            if kind == "E1/2":
                f = rvec(2)
                parts = [f, T(f)]
            else:
                parts = [tuple(rat(1 if i == j else 0) for i in range(3)) for j in range(3)]
            q1, q2 = rvec(n), rvec(n)
            base = {e: sizes(parts, q1, q2, units[e]) for e in blind}
            moved = {e: False for e in blind}
            for g in G:
                M = rep[g]
                for e in blind:
                    if sizes(parts, apply(M, q1), apply(M, q2), units[e]) != base[e]:
                        moved[e] = True
            tot += 1
            for e in blind:
                blind[e] += not moved[e]
        print(f"    {kind}: configurations frame-blind under all 48 (parts kept): eps = +1 {blind['+1']} of {tot}, eps = -1 {blind['-1']} of {tot}")
        if kind == "E1/2":
            check("twin hands: frame-blind for eps = -1 only (the singlet is the whole Alt^2)", blind["-1"] == tot and blind["+1"] == 0)
        else:
            check("vectors: frame-blind for neither sign, so this cannot be the law of every train", blind["-1"] == 0 and blind["+1"] == 0)

    print("6. The fitting: a quantum and its antiquantum carry no exchange term (draft part 1), so V x V's one invariant is open to")
    print("   an A1 source whatever eps is; the fitting cannot choose eps. Invariants of V x V (no symmetry asked), per kind:")
    counts = {k: len(v1.invariant_forms(rep, gens, len(rep[G[0]]))) for k, rep in reps.items()}
    print(f"    {counts}")
    check("one invariant pair state on every kind, with no condition on the exchange sign", all(c == 1 for c in counts.values()))


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    T = lambda v: (neg(conj(v[1])), conj(v[0]))  # noqa: E731
    print("M1. eps = +1 on the twin hands: Pauli's zero must fail")
    c = 0
    for _ in range(200):
        f = rvec(2)
        s = sizes([f, T(f)], rvec(2), rvec(2), rat(1))
        c += s[(0, 0)] != Z0
    report("pairs with sigma_++ > 0 in the frame (phi, T phi)", c, 200)
    print("M2. eps read from the head's K (K K = +1 on the twin hands): the twin hands' sign must come out wrong")
    K = lambda v: (conj(v[0]), conj(v[1]))  # noqa: E731
    c = 0
    for _ in range(200):
        v = rvec(2)
        c += K(K(v)) == v  # K K = +1, so eps would be +1
    report("twin pairs where K K = +1 (eps = +1, the boson's sign)", c, 200)
    print("M3. eps = i: relabelling must move a size")
    c = 0
    for _ in range(200):
        parts = [rvec(2), rvec(2)]
        q1, q2 = rvec(2), rvec(2)
        c += sizes(parts, q1, q2, I_) != sizes(parts, q2, q1, I_)
    report("configurations with a size moved by relabelling", c, 200)
    print("M4. the A1 premise with the sign flipped (eps = -nu): two equal quanta must lose the A1 on every kind")
    G = v1.closure([v1.QA, v1.QB])
    reps, _r = v1.kinds_explicit(G)
    lost = 0
    for kind, rep in reps.items():
        n = len(rep[G[0]])
        B = v1.invariant_forms(rep, [v1.QA, v1.QB], n)[0]
        nu = 1 if v1.mT(B) == B else -1
        q1, q2 = rvec(n), rvec(n)
        lost += not any(add(bform(B, q1, q2), mul(rat(-nu), bform(B, q2, q1))))
    report("kinds where eps = -nu leaves the pair no A1", lost, 8)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)
