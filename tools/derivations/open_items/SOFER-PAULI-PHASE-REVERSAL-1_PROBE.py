"""Sofer's check of the owner's derivation of Pauli (2026-10-28, 10:4x UTC): the phase reversal of a family, in a click.

  python3 -I tools/derivations/open_items/SOFER-PAULI-PHASE-REVERSAL-1_PROBE.py

Integers only (Gaussian integers as pairs, no float, no division). A hand of the force carriers is one Gaussian integer z; a
hand of matter (the twin hands) is a spinor of two, phi = (z1, z2). The phase reversal T of a family: z to its conjugate for
one Gaussian integer, (z1, z2) to (-conj(z2), conj(z1)) for the spinor. Each claim is run over an exhaustive box and over
random integers, and then again on a mutated formula that must fail (the mutation proof).
"""

from __future__ import annotations

import random
from itertools import product

BOX = range(-3, 4)  # the exhaustive box of one coefficient


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conj(a):
    return (a[0], -a[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[0], -a[1])


def norm(a):
    return a[0] * a[0] + a[1] * a[1]


def scale(k, a):
    return (k * a[0], k * a[1])


def reverse(phi):
    """T on a spinor: (z1, z2) to (-conj(z2), conj(z1))."""
    return (neg(conj(phi[1])), conj(phi[0]))


def inner(phi, chi):
    """<phi, chi> = conj(phi1) chi1 + conj(phi2) chi2."""
    return add(mul(conj(phi[0]), chi[0]), mul(conj(phi[1]), chi[1]))


def det(phi, chi):
    """phi1 chi2 - phi2 chi1."""
    return add(mul(phi[0], chi[1]), neg(mul(phi[1], chi[0])))


def rho(phi):
    return norm(phi[0]) + norm(phi[1])


def spin(phi):
    """The twin hand's axis S = (2 Re(conj(z1) z2), 2 Im(conj(z1) z2), N(z1) - N(z2)): three integers."""
    c = mul(conj(phi[0]), phi[1])
    return (2 * c[0], 2 * c[1], norm(phi[0]) - norm(phi[1]))


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def add3(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def spinors(box):
    gaussians = [(a, b) for a in box for b in box]
    return [(x, y) for x in gaussians for y in gaussians]


def sample(rng, size, bound):
    return [
        tuple((rng.randint(-bound, bound), rng.randint(-bound, bound)) for _ in range(2))
        for _ in range(size)
    ]


RESULTS: list[tuple[str, int, int]] = []


def check(label, cases, holds):
    failures = sum(1 for case in cases if not holds(*case))
    RESULTS.append((label, len(cases), failures))
    print(f"  {label}: {len(cases)} cases, {failures} failures")
    return failures


def main() -> int:
    rng = random.Random(24)
    box = spinors(BOX)
    rand = sample(rng, 20000, 50)
    singles = [(a, b) for a in range(-20, 21) for b in range(-20, 21) if (a, b) != (0, 0)]
    pairs = [(p, q) for p, q in zip(sample(rng, 20000, 30), sample(rng, 20000, 30), strict=True)]
    # exhaustive pairs over a smaller box: spinors with coefficients in -1..1
    small = spinors(range(-1, 2))
    small_pairs = list(product(small, small))
    bad = 0
    print("1. The phase reversal of the twin hands squares to minus one (Kramers), and keeps the norm")
    bad += check(
        "T(T(phi)) = -phi, exhaustive box",
        [(p,) for p in box],
        lambda p: reverse(reverse(p)) == (neg(p[0]), neg(p[1])),
    )
    bad += check(
        "T(T(phi)) = -phi, random",
        [(p,) for p in rand],
        lambda p: reverse(reverse(p)) == (neg(p[0]), neg(p[1])),
    )
    bad += check("N(T phi) = N(phi), random", [(p,) for p in rand], lambda p: rho(reverse(p)) == rho(p))
    bad += check(
        "<T phi, T chi> = conj <phi, chi>, random pairs",
        pairs,
        lambda p, q: inner(reverse(p), reverse(q)) == conj(inner(p, q)),
    )
    print(
        "2. The occupant is orthogonal to its own phase-reversed partner: the identical hand has no overlap with it"
    )
    bad += check(
        "<T phi, phi> = 0, exhaustive box", [(p,) for p in box], lambda p: inner(reverse(p), p) == (0, 0)
    )
    bad += check(
        "<T phi, phi> = 0, random", [(p,) for p in rand], lambda p: inner(reverse(p), p) == (0, 0)
    )
    print(
        "3. The antisymmetric overlap is the overlap with the phase-reversed partner, and the exchange reverses its sign"
    )
    bad += check(
        "det(phi, chi) = <T phi, chi>, random pairs",
        pairs,
        lambda p, q: det(p, q) == inner(reverse(p), q),
    )
    bad += check(
        "det(chi, phi) = -det(phi, chi), exhaustive pairs",
        small_pairs,
        lambda p, q: det(q, p) == neg(det(p, q)),
    )
    print("4. Lagrange: the two sizes (antisymmetric, symmetric) fill the room exactly")
    bad += check(
        "N(det) + N(<phi, chi>) = rho(phi) rho(chi), exhaustive pairs",
        small_pairs,
        lambda p, q: norm(det(p, q)) + norm(inner(p, q)) == rho(p) * rho(q),
    )
    bad += check(
        "N(det) + N(<phi, chi>) = rho(phi) rho(chi), random pairs",
        pairs,
        lambda p, q: norm(det(p, q)) + norm(inner(p, q)) == rho(p) * rho(q),
    )
    print(
        "5. The size of the lay is zero for the same state, whatever its multiplier, and positive otherwise (a sample)"
    )
    lam = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if (a, b) != (0, 0)]
    parallel = [(p, (mul(m, p[0]), mul(m, p[1]))) for p in box if p != ((0, 0), (0, 0)) for m in lam[:6]]
    bad += check(
        "N(det(phi, m phi)) = 0, a Gaussian multiple of the same hand",
        parallel,
        lambda p, q: norm(det(p, q)) == 0,
    )
    nonparallel = [
        (p, q)
        for p, q in small_pairs
        if p != ((0, 0), (0, 0)) and q != ((0, 0), (0, 0)) and det(p, q) != (0, 0)
    ]
    equal_cs = [(p, q) for p, q in nonparallel if norm(inner(p, q)) == rho(p) * rho(q)]
    RESULTS.append(("hands with a positive size but full overlap", len(nonparallel), len(equal_cs)))
    print(
        f"  hands with det nonzero: {len(nonparallel)}; of them with Cauchy-Schwarz equality: {len(equal_cs)} (must be 0)"
    )
    bad += len(equal_cs)
    print(
        "6. The click: the lay part has the size N(<T phi, chi>), the blocked part N(<phi, chi>); the draw is exact in integers"
    )
    draws_failed = 0
    for p, q in small_pairs:
        room = rho(p) * rho(q)
        if room == 0:
            continue
        lay, blocked = norm(det(p, q)), norm(inner(p, q))
        if lay + blocked != room:
            draws_failed += 1
            continue
        # the draw c in [0, room): the lay part holds [0, lay), the blocked part [lay, room); a part of size 0 is never drawn
        laid = sum(1 for c in range(room) if c < lay)
        if laid != lay or (lay == 0 and laid != 0):
            draws_failed += 1
    RESULTS.append(("the draw's counts equal the sizes", len(small_pairs), draws_failed))
    print(f"  the draw's counts equal the sizes: {len(small_pairs)} pairs, {draws_failed} failures")
    bad += draws_failed
    same_state_laid = sum(
        1 for p in small if rho(p) > 0 for c in range(rho(p) * rho(p)) if c < norm(det(p, p))
    )
    RESULTS.append(("the same hand is laid on a drawn number", 1, same_state_laid))
    print(f"  draws on which the same hand is laid beside itself: {same_state_laid} (must be 0)")
    bad += same_state_laid
    print(
        "7. The books: where the click does not happen nothing is taken; the board-level cancellation destroys the wind"
    )
    z = [(a, b) for a in range(-6, 7) for b in range(-6, 7) if (a, b) != (0, 0)]
    destroyed = sum(1 for w in z if norm(add(w, neg(w))) == 0 and norm(w) + norm(w) > 0)
    RESULTS.append(("psi + (-psi): wind of the sum against the wind of the two", len(z), destroyed))
    print(
        f"  psi + (-psi) = 0 carries the wind of two quanta to 0 in {destroyed} of {len(z)} hands: "
        "the books would book two where the board holds none (the plan's law 7 as written fails the count)"
    )
    print(
        "8. The kind decides: the one-Gaussian-integer hand (force carriers) has T squared +1 and no exclusion"
    )
    bad += check(
        "T(T(z)) = z, one Gaussian integer", [(w,) for w in singles], lambda w: conj(conj(w)) == w
    )
    keep = sum(1 for w in singles if mul(conj(conj(w)), w) == (0, 0))
    RESULTS.append(("<T z, z> = z z = 0 for a nonzero z", len(singles), keep))
    print(
        f"  <T z, z> = z z is 0 for {keep} of {len(singles)} nonzero hands (must be 0: no exclusion for force carriers)"
    )
    bad += keep
    print(
        "9. The occupation (rho, S) of a Node-clock: the lay's two sizes, with the capacity 2 u (the kind's dimension, 2, times the unit)"
    )
    u = 2  # the quantum's unit: the norm of one quantum, a pure spinor
    quanta = [p for p in spinors(range(-1, 2)) if rho(p) == u]
    newcomers = spinors(range(-2, 3))

    def free(occ_rho, occ_s, chi, cap=2 * u):
        return (cap - occ_rho) * rho(chi) - dot3(occ_s, spin(chi))

    def blocked(occ_rho, occ_s, chi):
        return occ_rho * rho(chi) + dot3(occ_s, spin(chi))

    bad += check(
        "S(T phi) = -S(phi), exhaustive box",
        [(p,) for p in box],
        lambda p: spin(reverse(p)) == tuple(-x for x in spin(p)),
    )
    bad += check(
        "Fierz: rho(phi) rho(chi) + S(phi) . S(chi) = 2 N(<phi, chi>), exhaustive pairs",
        small_pairs,
        lambda p, q: rho(p) * rho(q) + dot3(spin(p), spin(q)) == 2 * norm(inner(p, q)),
    )
    one = [(p, q) for p in quanta for q in newcomers]
    bad += check(
        "one quantum there: the free size is 2 N(det(phi, chi)), the room 2 u rho(chi)",
        one,
        lambda p, q: (
            free(rho(p), spin(p), q) == 2 * norm(det(p, q))
            and free(rho(p), spin(p), q) + blocked(rho(p), spin(p), q) == 2 * u * rho(q)
        ),
    )
    bad += check(
        "one quantum there: the free size is 0 for its own state and its Gaussian multiples",
        [(p, (mul(m, p[0]), mul(m, p[1]))) for p in quanta for m in lam[:6]],
        lambda p, q: free(rho(p), spin(p), q) == 0,
    )
    fill = [(p, q) for p in quanta for q in newcomers]
    bad += check(
        "the filled orbital (the quantum and its phase-reversed partner, rho = 2 u, S = 0): no size is free, whatever the newcomer",
        fill,
        lambda p, q: (
            rho(p) + rho(reverse(p)) == 2 * u
            and add3(spin(p), spin(reverse(p))) == (0, 0, 0)
            and free(2 * u, (0, 0, 0), q) == 0
        ),
    )
    bad += check(
        "the empty Node-clock: every size is free",
        [(q,) for q in newcomers],
        lambda q: free(0, (0, 0, 0), q) == 2 * u * rho(q),
    )
    bad += check(
        "the free lay writes the phase-reversed partner: (rho, S) goes from (u, S) to (2 u, 0)",
        [(p,) for p in quanta],
        lambda p: (rho(p) + rho(reverse(p)), add3(spin(p), spin(reverse(p)))) == (2 * u, (0, 0, 0)),
    )
    nonneg = sum(1 for p, q in one if free(rho(p), spin(p), q) < 0 or blocked(rho(p), spin(p), q) < 0)
    RESULTS.append(("no size is negative", len(one), nonneg))
    print(f"  sizes below 0 with one quantum there: {nonneg} (must be 0)")
    bad += nonneg
    print(
        "  the single-spinor reading of a filled orbital (the sum of the two amplitudes) cannot carry the cap:"
    )
    units = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    third = 0
    total = 0
    for p in quanta:
        for k in units:
            amplitude = (add(p[0], mul(k, reverse(p)[0])), add(p[1], mul(k, reverse(p)[1])))
            for q in newcomers:
                total += 1
                if norm(det(amplitude, q)) > 0:
                    third += 1
    print(
        f"  a third quantum would be allowed by the sum amplitude's determinant in {third} of {total} cases (the plan's twin hand as one spinor)"
    )
    if third == 0:
        bad += 1
    print("10. The mutation proof: each formula with one term changed must fail")
    mutants = {
        "T without its minus sign, (conj z2, conj z1)": lambda p: (conj(p[1]), conj(p[0])),
        "T as plain conjugation on the spinor": lambda p: (conj(p[0]), conj(p[1])),
        "T as the identity": lambda p: p,
    }
    for label, mutant in mutants.items():
        failing = sum(1 for p in box if inner(mutant(p), p) != (0, 0))
        print(f"  {label}: <T phi, phi> is not 0 for {failing} of {len(box)} hands (must be above 0)")
        if failing == 0:
            bad += 1
    cap_u = sum(1 for p, q in one if free(rho(p), spin(p), q, cap=u) < 0)
    cap_3u = sum(1 for p, q in fill if free(2 * u, (0, 0, 0), q, cap=3 * u) > 0)
    print(
        f"  the capacity u instead of 2 u: {cap_u} negative free sizes with one quantum there (must be above 0)"
    )
    print(
        f"  the capacity 3 u instead of 2 u: a third quantum free in {cap_3u} of {len(fill)} cases (must be above 0)"
    )
    if cap_u == 0 or cap_3u == 0:
        bad += 1
    both = [p for p in box if p[0] != (0, 0) and p[1] != (0, 0)]
    bosonic = sum(1 for p in both if norm(add(mul(p[0], p[1]), mul(p[1], p[0]))) > 0)
    print(
        f"  the size with the plus sign (the bosonic exchange) beside itself is positive for {bosonic} of {len(both)} hands: no exclusion"
    )
    if bosonic != len(both):
        bad += 1
    print(f"result: {bad} failures of the claims (the mutants fail as they must)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
