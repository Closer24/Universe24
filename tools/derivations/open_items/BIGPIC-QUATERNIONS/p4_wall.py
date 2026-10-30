"""p4: the wall for a half-speed hand of 4 or 8 whole parts, exact (Big Pic, 2026-10-30).

1. The per-gear carry, centred, commutes with a whole matrix at every input only if the matrix permutes the gears with
   signs (exhaustive: two gears, entries -2..2, dials 3 and 5).
2. A remainder fixed per class mod W that the units keep exists only if no unit other than 1 fixes a non-zero class
   (a unit other than 1 fixes no non-zero quaternion). Counted: Hurwitz under its 24 units, W = 1 to 13; the eight-part
   order under the 48, W = 1 to 5. The prediction: such classes exist iff W shares a factor with 6.
3. Even at dials prime to 6 the nearest lift ties: Hurwitz at W = 5 and 7.
Run: python3 .../p4_wall.py (about a minute; output p4_wall.txt). numpy arrays are whole (dtype int64).
"""

import itertools

import numpy as np
from qlib import ONE, TWO, carry, coords, exact, mul, order_basis, report, units, units_y, ymul

lines = []


def centred(x, w):
    """The per-gear carry with the centred tooth for an odd dial w: x = q w + r, r in [-(w-1)/2, (w-1)/2]."""
    h = exact(w - ONE, TWO)
    q, r = carry(x + h, w, 0)
    return q, r - h


# 1. the lemma, exhaustive on two gears
for w in (3, 5):
    keep = []
    for m in itertools.product(range(-2, 3), repeat=4):
        M = ((m[0], m[1]), (m[2], m[3]))
        if M[0][0] * M[1][1] - M[0][1] * M[1][0] not in (ONE, -ONE):
            continue
        ok = True
        for x in itertools.product(range(-3 * w, 3 * w + 1), repeat=2):
            qx = [centred(v, w)[0] for v in x]
            mx = (M[0][0] * x[0] + M[0][1] * x[1], M[1][0] * x[0] + M[1][1] * x[1])
            if [centred(v, w)[0] for v in mx] != [
                M[0][0] * qx[0] + M[0][1] * qx[1],
                M[1][0] * qx[0] + M[1][1] * qx[1],
            ]:
                ok = False
                break
        if ok:
            keep.append(M)
    signed = all(sum(abs(v) for v in row) == ONE for M in keep for row in M)
    report(
        lines,
        f"1. dial {w}: of the whole 2 x 2 matrices of determinant +-1 with entries -2..2, those the centred "
        f"per-gear carry commutes with are {len(keep)}, all signed permutations",
        len(keep) == 8 and signed,
    )


# 2. classes fixed by a unit other than 1
def fixed_count(mats, n, W):
    C = np.array(list(itertools.product(range(W), repeat=n)), dtype=np.int64)
    nonzero = np.any(C != 0, axis=1)
    bad = np.zeros(len(C), dtype=np.int64) != 0
    eye = np.eye(n, dtype=np.int64)
    for M in mats:
        if np.array_equal(M, eye):
            continue
        _, rem = carry(C @ (M - eye).T, W, 0)
        bad |= np.all(rem == 0, axis=1) & nonzero
    return int(bad.sum()), len(C)


def q2_of(c):  # Hurwitz in the basis h1 = (1 + i + j + k)/2, i, j, k; returns 2x
    return (c[0], c[0] + TWO * c[1], c[0] + TWO * c[2], c[0] + TWO * c[3])


def c_of(q2):
    c0 = q2[0]
    return (c0, exact(q2[1] - c0, TWO), exact(q2[2] - c0, TWO), exact(q2[3] - c0, TWO))


hur = []
for u, s, kind in units():
    if kind == "root2":
        continue
    g2 = tuple(TWO * v for v in u) if s == ONE else u  # 2g
    cols = [
        c_of(tuple(exact(v, TWO) for v in mul(g2, q2_of(e)))) for e in np.eye(4, dtype=np.int64).tolist()
    ]
    hur.append(np.array(cols, dtype=np.int64).T)
rows = []
for W in range(1, 14):
    b, n = fixed_count(hur, 4, W)
    _, odd = carry(W, TWO, 0)
    _, by3 = carry(W, 3, 0)
    shares = odd == 0 or by3 == 0
    rows.append((W, b, shares))
lines.append(
    "   Hurwitz, 24 units: (W, non-zero classes fixed by a unit other than 1, W shares a factor with 6): "
    + str(rows)
)
report(
    lines,
    "2. Hurwitz: a unit other than 1 fixes a non-zero class mod W exactly when W shares a factor with 6 (W = 1..13)",
    all((b > 0) == sh for _, b, sh in rows),
)

B, D, adj = order_basis()
eight = []
for y in units_y():
    M = [coords(ymul(y, tuple(Bi)), adj, D) for Bi in B]
    eight.append(np.array(M, dtype=np.int64).T)
rows8 = []
for W in range(1, 6):
    b, n = fixed_count(eight, 8, W)
    _, odd = carry(W, TWO, 0)
    _, by3 = carry(W, 3, 0)
    rows8.append((W, b, n, odd == 0 or by3 == 0))
lines.append(
    "   the eight-part order, 48 units: (W, fixed non-zero classes, classes, W shares a factor with 6): "
    + str(rows8)
)
report(
    lines,
    "   the eight-part order under the 48: the same, W = 1..5",
    all((b > 0) == sh for _, b, _, sh in rows8),
)


# 3. ties of the nearest lift, Hurwitz mod W (W prime to 6)
def ties(W):
    best = {}
    for q2 in itertools.product(range(-TWO * W, TWO * W + 1), repeat=4):
        par = {carry(v, TWO, 0)[1] for v in q2}
        if len(par) != ONE:
            continue
        key = tuple(carry(v, W, 0)[1] for v in c_of(q2))
        n = sum(v * v for v in q2)
        if key not in best or n < best[key][0]:
            best[key] = [n, ONE]
        elif n == best[key][0]:
            best[key][1] += ONE
    return sum(1 for v in best.values() if v[1] > ONE), len(best)


t5, n5 = ties(5)
t7, n7 = ties(7)
report(
    lines,
    f"3. at dials prime to 6 the nearest lift still ties: W = 5, {t5} of {n5} classes; W = 7, {t7} of {n7}",
    t5 > 0 and t7 > 0 and n5 == 625 and n7 == 2401,
)
x2 = (5, 1, 1, 1)
report(
    lines,
    "   one tie written out: (5 + i + j + k)/2 lies at |.|^2 = 7 from both 0 and 5",
    sum(v * v for v in x2) == 28 and sum(v * v for v in (x2[0] - 10,) + x2[1:]) == 28,
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
