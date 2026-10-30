"""g2: which vacua of the 24 leave one triplet three states the act can tell apart, exactly (beside the engine).

usage: python3 -I g2_breaking.py > g2_breaking.txt, at tensor24-review 8a476db17, the head it was made at (its calls into src are that head's)

From the engine's kinds.py (the 24 and their kinds, integer matrices), in Fractions:
 1. every subgroup of the 24 and its conjugacy class;
 2. for each subgroup H and each triplet kind (T1, T2): the H-invariant real symmetric 3 x 3 operators (a rest term on
    gears) and the H-invariant Hermitian ones (a rest term on Gaussian hands, re <-> im), their dimensions, and whether
    the generic one has three distinct eigenvalues (the cubic's discriminant not 0) or a pair is forced;
 3. the isotropy subgroups of each kind (A2, E, T1, T2: the stabilizers of a background vector) and the maximal ones
    (Michel: their orbits are critical for every invariant function, so a vacuum of the act's own invariants sits there);
 4. the Molien counts of invariant polynomials of each kind to degree 6, the lowest anisotropic invariant, and which
    maximal orbit it selects (its extrema, exactly on rational points near each orbit);
 5. the table: background kind x maximal orbit -> the triplet's pattern (1+1+1, 1+2, 3).
"""

import random
import sys
from fractions import Fraction as F
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[6] / "src")  # the worktree's committed act
sys.path.insert(0, SRC)

from tensor24.engine import kinds as K  # noqa: E402

LABELS = ("A1", "A2", "E", "T1", "T2")
rnd = random.Random(2026)


def mat(m):
    return tuple(tuple(int(x) for x in row) for row in m)


def mm(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0])))
        for i in range(len(a))
    )


def tr(a):
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def mv(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a)))


def nullspace(rows, n):
    """Basis of {x : r . x = 0 for every row}, exact over Q."""
    m = [list(map(F, r)) for r in rows]
    piv, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        m[r] = [x / m[r][c] for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                m[i] = [a - m[i][c] * b for a, b in zip(m[i], m[r], strict=True)]
        piv.append(c)
        r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        x = [F(0)] * n
        x[f] = F(1)
        for i, c in enumerate(piv):
            x[c] = -m[i][f]
        basis.append(x)
    return basis


def charpoly3(m):
    """Coefficients (c2, c1, c0) of x^3 + c2 x^2 + c1 x + c0 for a 3 x 3 matrix over Q or Q(i) (pairs)."""

    def add(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def mul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def neg(a):
        return (-a[0], -a[1])

    t = add(add(m[0][0], m[1][1]), m[2][2])
    minors = (0, 0)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        minors = add(minors, add(mul(m[i][i], m[j][j]), neg(mul(m[i][j], m[j][i]))))
    det = (0, 0)
    for p, s in (
        ((0, 1, 2), 1),
        ((1, 2, 0), 1),
        ((2, 0, 1), 1),
        ((0, 2, 1), -1),
        ((2, 1, 0), -1),
        ((1, 0, 2), -1),
    ):
        term = mul(mul(m[0][p[0]], m[1][p[1]]), m[2][p[2]])
        det = add(det, term if s == 1 else neg(term))
    return neg(t), minors, neg(det)


def disc3(c):
    """The discriminant of x^3 + b x^2 + c x + d (real coefficients): 0 iff a repeated root."""
    b, cc, d = (x[0] for x in c)
    assert all(x[1] == 0 for x in c), "a Hermitian matrix's characteristic polynomial is real"
    return 18 * b * cc * d - 4 * b**3 * d + b * b * cc * cc - 4 * cc**3 - 27 * d * d


def main():
    out = []
    p = out.append
    matrix, weight = K.turns(K.axes(3))
    held = K.kinds(matrix)
    sel = [g for g in range(len(weight)) if int(weight[g]) == 1]
    T1 = [mat(matrix[g]) for g in sel]
    rho = {lab: [mat(getattr(held, lab.lower())[g]) for g in sel] for lab in LABELS}
    index = {t: n for n, t in enumerate(T1)}
    table = [[index[mm(T1[a], T1[b])] for b in range(24)] for a in range(24)]
    e = index[((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    inv = [next(b for b in range(24) if table[a][b] == e) for a in range(24)]

    def closure(gens):
        s = {e} | set(gens)
        while True:
            new = {table[a][b] for a in s for b in s} - s
            if not new:
                return frozenset(s)
            s |= new

    subs = {closure([a]) for a in range(24)}
    subs |= {closure([a, b]) for a in range(24) for b in range(24)}
    subs = sorted(subs, key=len)

    def conj(h, g):
        return frozenset(table[table[g][x]][inv[g]] for x in h)

    classes = []
    for h in subs:
        if not any(h in c for c in classes):
            classes.append({conj(h, g) for g in range(24)})

    def order(a):
        n, x = 1, a
        while x != e:
            x, n = table[x][a], n + 1
        return n

    def ctype(a):
        o, _t = order(a), sum(T1[a][i][i] for i in range(3))
        if o == 2:
            return "C2" if all(abs(T1[a][i][i]) == 1 for i in range(3)) else "C2'"
        return {1: "1", 3: "C3", 4: "C4"}[o]

    def name(h):
        n = len(h)
        types = sorted(ctype(a) for a in h)
        if n == 1:
            return "1"
        if n == 2:
            return "C2 (axis)" if "C2" in types else "C2' (face diagonal)"
        if n == 3:
            return "C3 (body diagonal)"
        if n == 4:
            if "C4" in types:
                return "C4 (axis)"
            return (
                "V4 (normal: the 3 axes' 180-deg turns)"
                if types.count("C2") == 3
                else "D2' (C2 + two C2')"
            )
        if n == 6:
            return "D3 (body diagonal)"
        if n == 8:
            return "D4 (axis)"
        if n == 12:
            return "A4"
        return "S4 (the 24)"

    p(f"1. Subgroups of the 24: {len(subs)}, in {len(classes)} conjugacy classes:")
    reps = []
    for c in classes:
        h = min(c, key=lambda s: sorted(s))
        reps.append(h)
        p(f"   order {len(h):2d}, {len(c)} conjugate(s): {name(h)}")

    def invariant_ops(h, lab):
        """H-invariant real symmetric and real antisymmetric 3 x 3 operators on a triplet kind: bases."""
        R = [rho[lab][a] for a in h]

        # unknown M (9 entries); equations rho M rho^T = M for each h; plus symmetry or antisymmetry
        def eqs(sign):
            rows = []
            for r in R:
                for i in range(3):
                    for j in range(3):
                        row = [0] * 9
                        for k in range(3):
                            for ll in range(3):
                                row[3 * k + ll] += r[i][k] * r[j][ll]
                        row[3 * i + j] -= 1
                        rows.append(row)
            for i in range(3):
                for j in range(3):
                    row = [0] * 9
                    row[3 * i + j] += 1
                    row[3 * j + i] -= sign
                    rows.append(row)
            return nullspace(rows, 9)

        return eqs(1), eqs(-1)

    def generic(basis):
        m = [[F(0)] * 3 for _ in range(3)]
        for b in basis:
            c = rnd.randint(-(10**6), 10**6) or 1
            for i in range(3):
                for j in range(3):
                    m[i][j] += c * b[3 * i + j]
        return m

    def pattern(h, lab):
        sym, anti = invariant_ops(h, lab)
        results = []
        for kind, (s, a) in (("real", (sym, [])), ("hermitian", (sym, anti))):
            distinct = 0
            for _ in range(6):
                x = generic(s)
                y = generic(a) if a else [[F(0)] * 3 for _ in range(3)]
                m = [[(x[i][j], y[i][j]) for j in range(3)] for i in range(3)]
                distinct += disc3(charpoly3(m)) != 0
            results.append((kind, len(s), len(a) if kind == "hermitian" else 0, distinct))
        return results

    p("")
    p(
        "2. Each subgroup's invariant rest operators on a triplet: dim symmetric (+ dim antisymmetric for hands); "
        "'3 distinct' if 6 of 6 generic operators (random integers to 10^6) have three distinct eigenvalues, "
        "'pair forced' if 0 of 6 (the discriminant vanishes on the whole space):"
    )
    pat = {}
    for h in reps:
        for lab in ("T1", "T2"):
            res = pattern(h, lab)
            pat[(h, lab)] = res
            words = []
            for kind, ds, da, d in res:
                verdict = "3 distinct" if d == 6 else "pair forced" if d == 0 else f"{d}/6"
                words.append(
                    f"{kind}: dims {ds}" + (f"+{da}" if kind == "hermitian" else "") + f", {verdict}"
                )
            p(f"   {name(h):42s} {lab}: " + "; ".join(words))

    p("")
    p(
        "3. Isotropy subgroups (stabilizers of a nonzero background vector) of each kind, and the maximal ones (Michel):"
    )
    iso = {}
    for lab in ("A2", "E", "T1", "T2"):
        R = rho[lab]
        dim = len(R[0])
        found = []
        for h in subs:
            rows = []
            for a in h:
                for i in range(dim):
                    rows.append([R[a][i][j] - (1 if i == j else 0) for j in range(dim)])
            basis = nullspace(rows, dim)
            if not basis:
                continue
            coef = [rnd.randint(1, 10**6) for _ in basis]  # one coefficient per basis vector
            v = [sum((c * b[i] for c, b in zip(coef, basis, strict=True)), F(0)) for i in range(dim)]
            stab = frozenset(a for a in range(24) if mv(R[a], v) == tuple(v))
            if stab == h and h not in found:
                found.append(h)
        maximal = [h for h in found if len(h) < 24 and not any(h < g and len(g) < 24 for g in found)]

        def cls(h):
            return next(i for i, c in enumerate(classes) if h in c)

        iso[lab] = sorted({cls(h) for h in maximal})
        allc = sorted({cls(h) for h in found})
        p(
            f"   {lab}: isotropy classes {[name(reps[i]) for i in allc]}; maximal {[name(reps[i]) for i in iso[lab]]}"
        )

    p("")
    p("4. Invariant polynomials (Molien, exact to degree 6) and the lowest anisotropic one:")

    def molien(lab, top=6):
        R = rho[lab]
        dim = len(R[0])
        total = [F(0)] * (top + 1)
        for a in range(24):
            # power sums of eigenvalues = traces of powers; h_d (complete homogeneous) by Newton's identities
            pw = [None] + [sum(_pow(R[a], k)[i][i] for i in range(dim)) for k in range(1, top + 1)]
            h = [F(1)] + [F(0)] * top
            for d in range(1, top + 1):
                h[d] = sum(pw[k] * h[d - k] for k in range(1, d + 1)) / d
            for d in range(top + 1):
                total[d] += h[d]
        return [x / 24 for x in total]

    def _pow(m, k):
        r = tuple(tuple(1 if i == j else 0 for j in range(len(m))) for i in range(len(m)))
        for _ in range(k):
            r = mm(r, m)
        return r

    for lab in ("A2", "E", "T1", "T2"):
        counts = [int(x) for x in molien(lab)]
        p(f"   {lab}: invariants of degree 0..6: {counts}")
    p(
        "   isotropic invariants are the powers of the norm (one in each even degree); so the lowest anisotropic "
        "invariant is of degree 3 for E (Re z^3) and T2 (u v w, the triple product), of degree 4 for T1 (x^4 + y^4 + "
        "z^4; x y z is A2, no invariant of T1), and A2's every value breaks the 24 to A4"
    )

    def ratio(f, v):
        n2 = sum(F(x) * x for x in v)
        deg = f[1]
        return F(f[0](v)) / n2 ** F(deg, 2) if deg % 2 == 0 else None

    quartic = (lambda v: sum(F(x) ** 4 for x in v), 4)
    p(
        "   T1's quartic f = (x^4 + y^4 + z^4) / |x|^4 at the three maximal orbits and on rational points 1/100 off:"
    )
    for label, pt, moves in (
        ("axis [100] (C4)", (1, 0, 0), [(1, F(1, 100), 0), (1, F(1, 100), F(1, 100))]),
        ("face [110] (C2')", (1, 1, 0), [(1, 1, F(1, 100)), (1 + F(1, 100), 1 - F(1, 100), 0)]),
        ("body [111] (C3)", (1, 1, 1), [(1 + F(1, 100), 1, 1 - F(1, 100)), (1 + F(1, 100), 1, 1)]),
    ):
        f0 = ratio(quartic, pt)
        moved = [ratio(quartic, m) - f0 for m in moves]
        kind = (
            "maximum"
            if all(x < 0 for x in moved)
            else "minimum"
            if all(x > 0 for x in moved)
            else "saddle"
        )
        p(f"     {label}: f = {f0}; off: {[float(x) for x in moved]} -> {kind}")
    p(
        "   T2's cubic g = u v w / |u|^3: on the axis 0 and degenerate; on the body diagonals +-1/(3 sqrt 3), its extrema "
        "on the sphere (the gradient (v w, w u, u v) is parallel to u exactly at axes and body diagonals; at a face "
        "diagonal (1, 1, 0) it is (0, 0, 1), not parallel: no critical point there)"
    )
    grad_face = (1 * 0, 0 * 1, 1 * 1)
    p(
        f"     check: gradient at (1, 1, 0) = {grad_face}; at (1, 1, 1) = (1, 1, 1); at (1, 0, 0) = (0, 0, 0)"
    )

    p("")
    p(
        "5. The table: a background at each maximal orbit -> its stabilizer -> a T1 triplet's (and a T2's) pattern:"
    )
    for lab in ("A2", "E", "T1", "T2"):
        for i in iso[lab]:
            h = reps[i]
            words = []
            for t in ("T1", "T2"):
                res = pattern(h, t)
                (k1, s1, _, d1), (k2, s2, a2, d2) = res
                v1 = "1+1+1" if d1 == 6 else "1+2 (a pair)" if d1 == 0 else "?"
                v2 = "1+1+1" if d2 == 6 else "1+2 (a pair)" if d2 == 0 else "?"
                if s1 == 1 and d1 == 0:
                    v1 = "3 (degenerate)"
                if s2 == 1 and a2 == 0 and d2 == 0:
                    v2 = "3 (degenerate)"
                words.append(f"{t}: gears {v1}, hands {v2}")
            p(f"   {lab} at {name(h):40s} -> " + "; ".join(words))
    p(
        "   the act's own lowest invariant selects: T1 -> an axis (C4) or a body diagonal (C3), the face diagonal a saddle;"
        " T2 -> a body diagonal (D3); E -> its D4 points; A2 -> A4. At every one of these a T1 or T2 triplet on gears "
        "keeps a pair (1+2) or all three (3); three apart on gears needs T2 on an axis (D2', the cubic's degenerate "
        "point) or T1 on a face diagonal (C2', a saddle of the quartic) or E off its D4 points (V4), none the lowest "
        "invariant's extremum; on hands (re <-> im, a cross product read with the Gaussian i) a T1 background on an axis "
        "(C4) or a body diagonal (C3) splits a triplet into three, the Zeeman pattern of g3/g4."
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
