"""Sofer's check of the owner's derivation of Pauli (2026-10-28, 10:4x UTC): the phase reversal of a family, in a click.

  python3 -I tools/derivations/open_items/SOFER-PAULI-PHASE-REVERSAL-1_PROBE.py

Integers only (Gaussian integers as pairs, no float, no division). A hand of the force carriers is one Gaussian integer z; a
hand of matter (the twin hands) is a spinor of two, phi = (z1, z2). The phase reversal T of a family: z to its conjugate for
one Gaussian integer, (z1, z2) to (-conj(z2), conj(z1)) for the spinor. Each claim is run over an exhaustive box and over
random integers, and then again on a mutated formula that must fail (the mutation proof). The owner's chain of 10:59 UTC
(the video's four steps: the amplitudes of two paths add, the exchange twice is the identity so the sign is plus or minus,
two identical hands give A - A = 0, the exchange is the full turn of one and the full turn of a spinor is minus one) is
section 11.
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


def matmul(a, b):
    """The product of two square matrices of Gaussian integers (pairs)."""
    n = len(a)
    return tuple(
        tuple(
            (
                sum(mul(a[i][k], b[k][j])[0] for k in range(n)),
                sum(mul(a[i][k], b[k][j])[1] for k in range(n)),
            )
            for j in range(n)
        )
        for i in range(n)
    )


def matpow(m, k):
    out = m
    for _ in range(k - 1):
        out = matmul(out, m)
    return out


def matvec(m, v):
    return tuple(
        (
            sum(mul(m[i][j], v[j])[0] for j in range(len(v))),
            sum(mul(m[i][j], v[j])[1] for j in range(len(v))),
        )
        for i in range(len(m))
    )


def scalar_matrix(n, s):
    return tuple(tuple(s if i == j else (0, 0) for j in range(n)) for i in range(n))


# The quarter turns, with their integer norm factor (the unit turn is the matrix over the root of the factor):
# the twin hands (the double cover's spinor) take (1 - i, 1 + i) about z and the rows (1, -i), (-i, 1) about x, factor 2;
# the three-component kind takes the integer rotations, factor 1.
SPINOR_Z = (((1, -1), (0, 0)), ((0, 0), (1, 1)))
SPINOR_X = (((1, 0), (0, -1)), ((0, -1), (1, 0)))
VECTOR_Z = (((0, 0), (-1, 0), (0, 0)), ((1, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (1, 0)))
VECTOR_X = (((1, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (-1, 0)), ((0, 0), (1, 0), (0, 0)))


def turn_sign(quarter, n, factor):
    """+1 if four quarter turns are the identity, -1 if minus the identity (the matrix over factor squared), else 0."""
    full = matpow(quarter, 4)
    if full == scalar_matrix(n, (factor * factor, 0)):
        return 1
    if full == scalar_matrix(n, (-factor * factor, 0)):
        return -1
    return 0


def outer(phi, chi):
    """The pair's amplitudes phi_i chi_j, one matrix of Gaussian integers (the two paths of the video)."""
    return tuple(tuple(mul(phi[i], chi[j]) for j in range(2)) for i in range(2))


def swap(m):
    """The exchange of the two particles: the transpose of the pair's matrix."""
    return tuple(tuple(m[j][i] for j in range(2)) for i in range(2))


def madd(a, b):
    return tuple(tuple(add(a[i][j], b[i][j]) for j in range(2)) for i in range(2))


def msub(a, b):
    return tuple(tuple(add(a[i][j], neg(b[i][j])) for j in range(2)) for i in range(2))


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


def owner_chain(box, small_pairs, pairs) -> int:
    """The owner's chain of 10:59 UTC (the video's four steps), step by step in integers."""
    bad = 0
    zero = (((0, 0), (0, 0)), ((0, 0), (0, 0)))
    print(
        "11. The owner's chain: amplitudes add, the exchange twice is the identity, the sign is the full turn's, A - A = 0"
    )
    print(
        "  steps 1 to 3: the pair's two paths, the exchange twice, and the same hand at both detectors"
    )
    bad += check(
        "swap(swap(M)) = M for the pair's amplitudes (the exchange twice is the identity)",
        small_pairs,
        lambda p, q: swap(swap(outer(p, q))) == outer(p, q),
    )
    bad += check(
        "the sum of the two paths is even under the exchange, the difference odd (the two signs the video finds)",
        small_pairs,
        lambda p, q: (
            swap(madd(outer(p, q), swap(outer(p, q)))) == madd(outer(p, q), swap(outer(p, q)))
            and swap(msub(outer(p, q), swap(outer(p, q)))) == msub(swap(outer(p, q)), outer(p, q))
        ),
    )
    bad += check(
        "the difference of the two paths has one component, det(phi, chi), and is [[0, det], [-det, 0]]",
        small_pairs,
        lambda p, q: (
            msub(outer(p, q), swap(outer(p, q))) == ((((0, 0)), det(p, q)), (neg(det(p, q)), (0, 0)))
        ),
    )
    bad += check(
        "A - A = 0: the two paths of one hand cancel as matrices, so the pair's amplitude is 0",
        [(p,) for p in box],
        lambda p: msub(outer(p, p), swap(outer(p, p))) == zero,
    )
    print("  step 4: the sign is the full turn's; four quarter turns, exactly")
    kinds = (
        ("the twin hands, about z", SPINOR_Z, 2, 2, -1),
        ("the twin hands, about x", SPINOR_X, 2, 2, -1),
        ("the three-component kind, about z", VECTOR_Z, 3, 1, 1),
        ("the three-component kind, about x", VECTOR_X, 3, 1, 1),
    )
    for label, quarter, n, factor, want in kinds:
        got = turn_sign(quarter, n, factor)
        print(
            f"  {label}: four quarter turns are {got:+d} times the identity (the factor {factor} to the fourth)"
        )
        if got != want:
            bad += 1
    print(
        "  the scalar of the force carriers is the kind on which every turn acts as 1: its full turn is +1 by definition"
    )
    print(
        "  the half turns about two axes: commute on the three-component kind, anticommute on the twin hands"
    )
    half = (
        ("twin hands", matpow(SPINOR_Z, 2), matpow(SPINOR_X, 2), -1),
        ("three-component kind", matpow(VECTOR_Z, 2), matpow(VECTOR_X, 2), 1),
    )
    for label, hz, hx, sign in half:
        left, right = matmul(hz, hx), matmul(hx, hz)
        flipped = tuple(tuple(neg(e) for e in row) for row in right)
        ok = (left == right) if sign == 1 else (left == flipped and left != right)
        print(f"  {label}: {'commute' if sign == 1 else 'anticommute'}: {ok}")
        if not ok:
            bad += 1
    print(
        "  the singlet of the pair is invariant under the turns, and its exchange sign is the full turn's"
    )
    bad += check(
        "det(U phi, U chi) = 2 det(phi, chi) for the quarter turns about z and x (the factor 2, normalised 1)",
        pairs,
        lambda p, q: all(
            det(matvec(u, p), matvec(u, q)) == scale(2, det(p, q)) for u in (SPINOR_Z, SPINOR_X)
        ),
    )
    triples = [
        ((a, b), (b, c), (c, a)) for a in range(-2, 3) for b in range(-2, 3) for c in range(-2, 3)
    ]
    pairs3 = [(v, w) for v in triples[::7] for w in triples[::11]]

    def dot(v, w):
        return (
            sum(mul(v[i], w[i])[0] for i in range(3)),
            sum(mul(v[i], w[i])[1] for i in range(3)),
        )

    bad += check(
        "the three-component kind's singlet v . w is symmetric and invariant under both quarter turns",
        pairs3,
        lambda v, w: (
            dot(v, w) == dot(w, v)
            and all(dot(matvec(r, v), matvec(r, w)) == dot(v, w) for r in (VECTOR_Z, VECTOR_X))
        ),
    )
    bad += check(
        "the twin hands' singlet det is antisymmetric: det(chi, phi) = -det(phi, chi)",
        pairs,
        lambda p, q: det(q, p) == neg(det(p, q)),
    )

    def conj3(v):
        return tuple(conj(c) for c in v)

    def sign_of(image, items):
        """+1 if image(x) = x for every item, -1 if image(x) = -x for every item, else 0."""
        if all(image(x) == x for x in items):
            return 1
        if all(image(x) == tuple(neg(c) for c in x) for x in items):
            return -1
        return 0

    t2_spinor = sign_of(lambda p: reverse(reverse(p)), box)
    t2_vector = sign_of(lambda v: conj3(conj3(v)), [v for v, _ in pairs3])
    t2_scalar = sign_of(
        lambda z: (conj(conj(z[0])),), [((a, b),) for a in range(-6, 7) for b in range(-6, 7)]
    )
    turns = (
        ("twin hands", t2_spinor, turn_sign(SPINOR_Z, 2, 2), turn_sign(SPINOR_X, 2, 2)),
        ("three-component kind", t2_vector, turn_sign(VECTOR_Z, 3, 1), turn_sign(VECTOR_X, 3, 1)),
        ("scalar", t2_scalar, 1, 1),
    )
    for label, t2, about_z, about_x in turns:
        print(
            f"  {label}: T squared is {t2:+d}, the full turn about z is {about_z:+d} and about x {about_x:+d}"
        )
        if not t2 == about_z == about_x:
            bad += 1
    print("  the mutation proof for the chain")
    quarter_phase = (
        ((1, 0), (0, 0)),
        ((0, 0), (0, 1)),
    )  # diag(1, i): a plain phase quarter turn, factor 1
    got = turn_sign(quarter_phase, 2, 1)
    print(f"  the spinor's quarter turn as diag(1, i): four quarter turns are {got:+d} (must not be -1)")
    if got == -1:
        bad += 1
    sym_fail = sum(
        1
        for p, q in pairs
        if add(
            mul(matvec(SPINOR_X, p)[0], matvec(SPINOR_X, q)[1]),
            mul(matvec(SPINOR_X, p)[1], matvec(SPINOR_X, q)[0]),
        )
        != scale(2, add(mul(p[0], q[1]), mul(p[1], q[0])))
    )
    print(
        f"  the symmetric bilinear phi1 chi2 + phi2 chi1 as the pair's singlet: not invariant under the x turn in {sym_fail} of {len(pairs)} pairs (must be above 0)"
    )
    if sym_fail == 0:
        bad += 1
    plus = sum(1 for p in box if madd(outer(p, p), swap(outer(p, p))) != zero)
    print(
        f"  the sum of the two paths (the bosonic sign) of one hand is not 0 for {plus} of {len(box)} hands (must be above 0)"
    )
    if plus == 0:
        bad += 1
    return bad


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
    bad += owner_chain(box, small_pairs, pairs)
    print(f"result: {bad} failures of the claims (the mutants fail as they must)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
