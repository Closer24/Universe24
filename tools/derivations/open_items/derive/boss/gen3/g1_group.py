"""g1: the 24's structure from the engine's own kinds.py and main.made, exactly (beside the engine; no file changed).

usage: python3 -I g1_group.py > g1_group.txt, at tensor24-review 8a476db17, the head it was made at (its calls into src are that head's)

Reads the committed act at src/ (tensor24-review's clean copy). Computes:
 1. the 24 turns (kinds.turns), each kind a homomorphism (checked), classes, orders, characters, orthonormality;
 2. the normal subgroups (unions of classes closed under the product), V4 and A4, S4/V4 = S3 on the three axes;
 3. the 43 tables (main.made): which (i, k -> m) are not 0, against the characters' multiplicities; symmetry for i = k;
 4. every multiplicity of a kind in a triple product (the composites' channel counts);
 5. the kinds' A2-orbits and kernels;
 6. the twin kinds of the double cover 2O and of 2T (floats, only to name the irrational values sqrt 2 and omega).
"""

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[6] / "src")  # the worktree's committed act
sys.path.insert(0, SRC)

import numpy as np  # noqa: E402

from tensor24 import main as tensor24  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402

LABELS = ("A1", "A2", "E", "T1", "T2")


def mat(m):
    return tuple(tuple(int(x) for x in row) for row in m)


def mul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def main():
    out = []
    p = out.append
    matrix, weight = K.turns(K.axes(3))
    held = K.kinds(matrix)
    sel = [g for g in range(len(weight)) if int(weight[g]) == 1]
    p(f"1. The turns: {len(weight)} candidate matrices of three Spokes, weight 1 on {len(sel)} (det 1).")
    T1 = [mat(matrix[g]) for g in sel]
    rho = {lab: [mat(getattr(held, lab.lower())[g]) for g in sel] for lab in LABELS}
    index = {t: n for n, t in enumerate(T1)}
    # group law by T1's product; check every kind is a homomorphism for that law
    table = [[index[mul(T1[a], T1[b])] for b in range(24)] for a in range(24)]
    hom = {
        lab: all(
            mul(rho[lab][a], rho[lab][b]) == rho[lab][table[a][b]] for a in range(24) for b in range(24)
        )
        for lab in LABELS
    }
    p(f"   each kind a homomorphism of the 24 under T1's product: {hom}")
    e = index[mat(np.eye(3, dtype=int))]
    inv = [next(b for b in range(24) if table[a][b] == e) for a in range(24)]

    def order(a):
        n, x = 1, a
        while x != e:
            x, n = table[x][a], n + 1
        return n

    classes, seen = [], set()
    for a in range(24):
        if a in seen:
            continue
        c = sorted({table[table[h][a]][inv[h]] for h in range(24)})
        seen |= set(c)
        classes.append(c)
    classes.sort(key=lambda c: (order(c[0]), len(c)))
    names = []
    for c in classes:
        o = order(c[0])
        if o == 1:
            name = "identity"
        elif o == 4:
            name = "C4: 90-deg turns about the 3 axes"
        elif o == 3:
            name = "C3: 120-deg turns about the 4 body diagonals"
        elif o == 2 and len(c) == 3:
            name = "C2 = C4^2: 180-deg turns about the 3 axes"
        else:
            name = "C2': 180-deg turns about the 6 face diagonals"
        names.append(name)
    p("   classes (order, size): " + ", ".join(f"({order(c[0])}, {len(c)})" for c in classes))
    for c, name in zip(classes, names, strict=True):
        perm = tuple(tuple(abs(x) for x in row) for row in T1[c[0]])
        cyc = (
            "identity"
            if perm == ((1, 0, 0), (0, 1, 0), (0, 0, 1))
            else ("3-cycle" if trace(perm) == 0 else "transposition")
        )
        p(f"     ({order(c[0])}, {len(c)}) {name}; its image on the three axes (S4 -> S3): {cyc}")
    chars = {lab: [trace(rho[lab][c[0]]) for c in classes] for lab in LABELS}
    p("   characters (traces of the kinds' whole matrices) on the classes in that order:")
    for lab in LABELS:
        p(f"     {lab:2s} {chars[lab]}")
    sizes = [len(c) for c in classes]

    def inner(x, y):
        return Fraction(sum(s * a * b for s, a, b in zip(sizes, x, y, strict=True)), 24)

    ortho = all(inner(chars[a], chars[b]) == (1 if a == b else 0) for a in LABELS for b in LABELS)
    p(
        f"   orthonormal over the 24: {ortho}; sum of squared dimensions {sum(chars[lab][0] ** 2 for lab in LABELS)}"
    )

    p("")
    p("2. Normal subgroups (unions of classes holding the identity, closed under the product):")
    normal = []
    for r in range(len(classes) + 1):
        for pick in itertools.combinations(range(1, len(classes)), r):
            s = set(classes[0])
            for i in pick:
                s |= set(classes[i])
            if all(table[a][b] in s for a in s for b in s):
                normal.append((len(s), pick))
    for size, pick in sorted(normal):
        p(
            f"   order {size:2d}: identity + "
            + (" + ".join(f"({order(classes[i][0])}, {len(classes[i])})" for i in pick) or "nothing")
        )
    v4 = set(classes[0]) | set(next(c for c in classes if order(c[0]) == 2 and len(c) == 3))
    a4 = {a for a in range(24) if trace(rho["A2"][a]) == 1}
    kernel_axes = {a for a in range(24) if all(abs(T1[a][i][i]) == 1 for i in range(3))}
    p(
        f"   V4 = the 180-deg turns about the axes with the identity: order {len(v4)}; the kernel of the axes' "
        f"permutation (S4 -> S3) equals V4: {kernel_axes == v4}"
    )
    p(
        f"   A4 = the kernel of A2 (the sign of the axes' permutation): order {len(a4)}; V4 inside A4: {v4 <= a4}; "
        f"A4 / V4 is the C3 class's image, the 3-cycles of the axes"
    )
    kernels = {
        lab: len([a for a in range(24) if rho[lab][a] == mat(np.eye(len(rho[lab][0]), dtype=int))])
        for lab in LABELS
    }
    p(f"   each kind's kernel order: {kernels} (A1 the 24, A2 A4, E V4, T1 and T2 faithful)")

    p("")
    p(
        "3. The tables (main.made), C[i, k -> m], against the multiplicities (1/24) SUM chi_i chi_k chi_m:"
    )
    _, tables = tensor24.made((3, 3, 3))
    nonzero = sorted(key for key, t in tables.items() if np.asarray(t).any())
    mult = {
        (i, k, m): inner(
            [a * b for a, b in zip(chars[LABELS[i]], chars[LABELS[k]], strict=True)], chars[LABELS[m]]
        )
        for i in range(5)
        for k in range(5)
        for m in range(5)
    }
    p(
        f"   tables not 0: {len(nonzero)} of {len(tables)}; every multiplicity in {sorted(set(mult.values()))}; "
        f"not 0 exactly where the multiplicity is 1: {set(nonzero) == {key for key, v in mult.items() if v == 1}}"
    )
    for i in range(5):
        for k in range(i, 5):
            targets = [LABELS[m] for m in range(5) if (i, k, m) in nonzero]
            sym = []
            for m in range(5):
                if (i, k, m) in nonzero and i == k:
                    t = np.asarray(tables[(i, k, m)])
                    sym.append(
                        f"{LABELS[m]}:{'sym' if (t == np.swapaxes(t, 1, 2)).all() else 'anti' if (t == -np.swapaxes(t, 1, 2)).all() else 'mixed'}"
                    )
            p(
                f"   {LABELS[i]} x {LABELS[k]} -> {' + '.join(targets)}"
                + (f"   (exchange: {', '.join(sym)})" if sym else "")
            )
    lands = {LABELS[m]: sum(1 for key in nonzero if key[2] == m) for m in range(5)}
    p(f"   ordered pairs (i, k) landing on each kind: {lands} (sum {sum(lands.values())})")

    p("")
    p(
        "4. Triple products: the multiplicity of each kind in i x j x k (the composite's channels), ordered triples:"
    )
    found3 = []
    for i, j, k in itertools.combinations_with_replacement(range(5), 3):
        prod = [
            a * b * c
            for a, b, c in zip(chars[LABELS[i]], chars[LABELS[j]], chars[LABELS[k]], strict=True)
        ]
        ms = {LABELS[m]: inner(prod, chars[LABELS[m]]) for m in range(5)}
        line = " + ".join(f"{int(v)} {lab}" if v != 1 else lab for lab, v in ms.items() if v)
        if max(ms.values()) >= 3:
            found3.append(f"{LABELS[i]} x {LABELS[j]} x {LABELS[k]} = {line}")
    p("   triples with some kind three times or more:")
    for line in found3:
        p("     " + line)
    p(
        "   (T2 three times in T1^3 and T1 three times in T2^3: the multiplicity of spin 1 in 1 x 1 x 1 under SO(3) is 3, "
        "the intermediate spins 0, 1, 2; E three times in E^3: S3's 2 x 2 x 2 = 1 + 1' + 3 x 2)"
    )

    p("")
    p("5. The kinds under the A2 twist (K -> A2 x K): orbits and dimensions:")
    twist = {}
    for lab in LABELS:
        prod = [a * b for a, b in zip(chars["A2"], chars[lab], strict=True)]
        twist[lab] = next(m for m in LABELS if inner(prod, chars[m]) == 1)
    orbits = []
    for lab in LABELS:
        o = tuple(sorted({lab, twist[lab]}))
        if o not in orbits:
            orbits.append(o)
    p(
        f"   {twist}; orbits {orbits}: three orbits, of dimensions 1, 2, 3 (the kernels' layers S4/A4, S4/V4, S4)"
    )

    p("")
    p("6. The double cover (twin kinds), floats only to name the irrational character values:")
    # unit quaternions over every turn: q = +-(cos a, sin a n), a = half the angle
    quats = []
    for t in T1:
        m = np.array(t, dtype=float)
        tr = np.trace(m)
        ang = math.acos(max(-1.0, min(1.0, (tr - 1) / 2)))
        if abs(ang) < 1e-12:
            axis = np.array([0.0, 0.0, 1.0])
        elif abs(ang - math.pi) < 1e-9:
            w, v = np.linalg.eigh((m + m.T) / 2)
            axis = v[:, np.argmax(w)]
        else:
            axis = np.array([m[2, 1] - m[1, 2], m[0, 2] - m[2, 0], m[1, 0] - m[0, 1]]) / (
                2 * math.sin(ang)
            )
        for sign in (1, -1):
            quats.append(sign * np.concatenate(([math.cos(ang / 2)], math.sin(ang / 2) * axis)))

    def qmul(a, b):
        w1, x1, y1, z1 = a
        w2, x2, y2, z2 = b
        return np.array(
            [
                w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
            ]
        )

    def find(q):
        return next(n for n, r in enumerate(quats) if np.allclose(q, r, atol=1e-9))

    closed = all(find(qmul(a, b)) is not None for a in quats for b in quats)
    qinv = [np.array([q[0], -q[1], -q[2], -q[3]]) for q in quats]
    cls2, seen2 = [], set()
    for n, q in enumerate(quats):
        if n in seen2:
            continue
        c = sorted({find(qmul(qmul(quats[h], q), qinv[h])) for h in range(48)})
        seen2 |= set(c)
        cls2.append(c)

    def spin(j, q):
        a = math.acos(max(-1.0, min(1.0, q[0])))
        if abs(math.sin(a)) < 1e-12:
            return (2 * j + 1) * (1 if math.cos(a) > 0 else (-1) ** int(round(2 * j)))
        return math.sin((2 * j + 1) * a) / math.sin(a)

    reps = [quats[c[0]] for c in cls2]
    e12 = [spin(0.5, q) for q in reps]
    g32 = [spin(1.5, q) for q in reps]
    s52 = [spin(2.5, q) for q in reps]
    e52 = [a - b for a, b in zip(s52, g32, strict=True)]
    sz = [len(c) for c in cls2]

    def norm(x):
        return sum(s * v * v for s, v in zip(sz, x, strict=True)) / 48

    p(f"   2O: {len(quats)} unit quaternions, closed: {closed}; {len(cls2)} classes, sizes {sz}")
    p(f"   E1/2 {[round(v, 5) for v in e12]} norm {norm(e12):.3f}")
    p(f"   E5/2 {[round(v, 5) for v in e52]} norm {norm(e52):.3f}")
    p(f"   G3/2 {[round(v, 5) for v in g32]} norm {norm(g32):.3f}")
    p(
        f"   so three twin kinds of dimensions 2, 2, 4 (4 + 4 + 16 = 24); E1/2 and E5/2 take +-sqrt 2 = +-{math.sqrt(2):.5f} "
        "on the 90-deg turns' lifts, a value outside Q(i), so neither is a kind of Gaussian twin hands alone; "
        "their sum, with 0 there, is rational"
    )
    # 2T: lifts of A4
    a4q = [n for n in range(len(quats)) if trace(rho["A2"][n // 2]) == 1]  # quats[n] lifts T1[n // 2]
    cls_t, seen_t = [], set()
    for n in a4q:
        if n in seen_t:
            continue
        c = sorted({find(qmul(qmul(quats[h], quats[n]), qinv[h])) for h in a4q})
        seen_t |= set(c)
        cls_t.append(c)
    reps_t = [quats[c[0]] for c in cls_t]
    szt = [len(c) for c in cls_t]
    d2 = [spin(0.5, q) for q in reps_t]
    # the Z3 characters of A4 / V4 on these classes: 1 on the lifts of V4, omega on one C3 class, omega^2 on the other
    p(f"   2T (lifts of A4): {len(a4q)} elements, {len(cls_t)} classes, sizes {szt}")
    # the Z3 label of each lift: the cyclic shift of the axes its rotation makes (A4 / V4)
    cyc = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
    shifts = [((1, 0, 0), (0, 1, 0), (0, 0, 1)), cyc, mul(cyc, cyc)]

    def label(n):
        perm = tuple(tuple(abs(x) for x in row) for row in T1[n // 2])
        return shifts.index(perm)

    om = complex(math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3))
    chi2 = {n: spin(0.5, quats[n]) for n in a4q}
    chi2p = {n: chi2[n] * om ** label(n) for n in a4q}
    chi2pp = {n: chi2[n] * om ** (-label(n)) for n in a4q}
    g32_t = {n: spin(1.5, quats[n]) for n in a4q}
    glued = all(abs(chi2p[n] + chi2pp[n] - g32_t[n]) < 1e-9 for n in a4q)
    norm_2p = sum(abs(chi2p[n]) ** 2 for n in a4q) / len(a4q)
    values = sorted(
        {complex(round(chi2p[n].real, 5), round(chi2p[n].imag, 5)) for n in a4q},
        key=lambda z: (z.real, z.imag),
    )
    p(
        f"   check: chi(2') + chi(2'') = chi(G3/2) on all 24 lifts: {glued}; |chi(2')|^2 averaged {norm_2p:.6f} (irreducible); "
        f"chi(2') takes {values}"
    )
    p(
        f"   its natural doublet 2: {[round(v, 5) for v in d2]}; 2' = 2 x 1' and 2'' = 2 x 1'' take omega and "
        "omega^2 times these on the 120-deg lifts: values outside Q(i), so 2' and 2'' come glued as one rational "
        "four (the restriction of G3/2), the 1 + 2 pattern again"
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
