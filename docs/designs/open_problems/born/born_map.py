"""Born's square as an input (P10): the map of problem (5) of the seven (the open-problems
physicist, read-only, 2026-09-21; docs/designs/open_problems/born/NOTE.md).

Host arithmetic on the lattice Gleason's family (DERIVATIONS 6.5, 6.7) at N = 64; the tables
here the exact cosines (the built tables round at 1 / 256; the register's integers named
where they decide); no engine import, no run.

(A) The admissible family: R(f) = sum over odd j < N / 2 of c_j |sigma_j(f)|^2, the 16 free
    constants at N = 64; the kernel K_j(D) = cos(2 pi j D / N) of each member for two rows
    at the phase difference D; the flat mixture (every c_j equal) as the phase-blind reading.
(B) What the register reads under each member: Malus at 22.5 degrees (the registered 219 / 256
    and the chain 187 / 256, record 395), the two-slit fringe period (record 156's bands,
    23.5 pixels at j = 1), the Mach-Zehnder and pair worlds (blind: D in {0, N / 4, N / 2}).
(C) The relabelling: for j coprime to N the map p -> j p is an automorphism of Z_N, so the
    j-th member is Born's under the relabelled phase rate; the physical freedom is the
    mixture's cone, not the choice of j.
(D) The rank of the click's Gram matrix per member: G_j = E_j^T E_j has rank 2 (one pointer);
    a mixture of k harmonics rank 2 k; the flat mixture rank N / 2 (the projector on the odd
    subspace): the least-rank (least-cost) admissible click is one harmonic.

Run from the repository root:

    python docs/designs/open_problems/born/born_map.py > docs/designs/open_problems/born/born_map.out
"""

from __future__ import annotations

import math

N = 64
ODD = [j for j in range(1, N // 2) if j % 2 == 1]


def kernel(j: int, d: int) -> float:
    return math.cos(2 * math.pi * j * d / N)


print(
    f"A. THE ADMISSIBLE FAMILY AT N = {N}: {len(ODD)} free constants c_j, j odd below N / 2 = {N // 2}: {ODD}"
)
print(
    "   two rows a x^p and b x^(p + D) at one Node read C (a^2 + b^2) + 2 a b K(D), K(D) = sum c_j cos(2 pi j D / N); the members' kernels at D = 0 .. 8 (of 64):"
)
print("   j | K_j(0..8)")
for j in (1, 3, 5, 7, 9, 15, 31):
    print(f"   {j:2d} | " + " ".join(f"{kernel(j, d):+.3f}" for d in range(9)))
flat = [sum(kernel(j, d) for j in ODD) / len(ODD) for d in range(9)]
print(
    "   flat mixture (every c_j equal) | "
    + " ".join(f"{k:+.3f}" for k in flat)
    + "  (the comb [D = 0] - [D = 32]: phase-blind, R = sum f_p^2)"
)
print()

print("B. WHAT THE REGISTER READS UNDER EACH MEMBER")
# Malus: the polariser at the angle theta reads the fraction cos^2 of the rotation's angle; a member j reads cos^2(j theta)
print(
    "   Malus at 22.5 degrees (one polariser; the register's 219 / 256 = 0.8555, record 395; nature cos^2 = 0.8536) and the chain of four at 22.5-degree steps (187 / 256 = 0.7305; nature cos^8 ... the register's chain reads two reads, cos^4 = 0.7286):"
)
print("   j | one polariser cos^2(j x 22.5 deg) | x 256 | the chain cos^4(j x 22.5 deg) | x 256")
for j in (1, 3, 5, 7, 9, 15):
    one = math.cos(j * math.pi / 8) ** 2
    print(f"   {j:2d} | {one:.4f} | {one * 256:6.1f} | {one * one:.4f} | {one * one * 256:6.1f}")
print("   the flat mixture | 0.5000 | 128.0 | 0.2500 | 64.0")
print(
    "   Malus at 22.5 degrees admits j = 1, 7, 9, 15 (j = +-1 mod 8) and excludes j = 3, 5 and every mixture with weight on them above the bracket; at 45 and 90 degrees every member reads 1 / 2 and 0 (NATURE row 9 tests nothing of the harmonics)"
)
print()
print(
    "   the two slits (record 156's bands, the kernel cos(2 pi D / 64) at 64 steps per 23.5 pixels): the member j has the period 23.5 / j pixels"
)
for j in (1, 3, 5, 7, 9, 15, 31):
    print(
        f"   j = {j:2d}: the fringe period {23.5 / j:5.2f} pixels"
        + (
            "  (registered)"
            if j == 1
            else "  (excluded by the bands at y = 35 .. 38, 59 .. 61, 82 .. 85)"
            if j < 9
            else "  (below a pixel: no bands)"
        )
    )
print(
    "   so the two-slit register alone pins j = 1 among the single members, and every Mach-Zehnder and pair world (D in {0, 16, 32}) is blind: K(0) = C, K(16) = 0, K(32) = -C for every member"
)
print()

print("C. THE RELABELLING: p -> j p is an automorphism of Z_N for gcd(j, N) = 1")
for j in (3, 5, 7):
    image = sorted({(j * p) % N for p in range(N)})
    print(
        f"   j = {j}: the image of Z_64 has {len(image)} elements (a bijection); the member j reads the declared rate n / d as j n / d: Born's member under a relabelled declaration, the same law"
    )
print(
    "   so the physical content of P10 is not 'j = 1' but 'one harmonic, not a mixture': the mixtures are the different laws (the flat one phase-blind)"
)
print()

print(
    "D. THE RANK OF THE CLICK'S GRAM MATRIX PER MEMBER (the click without amplitudes, note 37 (xii): the weight f^T G f)"
)


def gram(js):
    """G = sum over j in js of E_j^T E_j with E_j the 2 x N matrix of the j-th harmonic's tables."""
    g = [[0.0] * N for _ in range(N)]
    for j in js:
        c = [math.cos(2 * math.pi * j * p / N) for p in range(N)]
        s = [math.sin(2 * math.pi * j * p / N) for p in range(N)]
        for a in range(N):
            for b in range(N):
                g[a][b] += c[a] * c[b] + s[a] * s[b]
    return g


def rank(m, tol=1e-6):
    """Gaussian elimination over the reals with full pivoting on the largest entry."""
    a = [row[:] for row in m]
    r = 0
    rows, cols = len(a), len(a[0])
    for col in range(cols):
        pivot = max(range(r, rows), key=lambda i: abs(a[i][col]), default=None)
        if pivot is None or abs(a[pivot][col]) <= tol:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(rows):
            if i != r and abs(a[i][col]) > tol:
                f = a[i][col] / a[r][col]
                a[i] = [x - f * y for x, y in zip(a[i], a[r], strict=True)]
        r += 1
        if r == rows:
            break
    return r


for name, js in (
    ("the fundamental alone (Born)", [1]),
    ("j = 3 alone", [3]),
    ("j = 1 and 3", [1, 3]),
    ("j = 1, 3, 5", [1, 3, 5]),
    ("the flat mixture, all 16 odd j", ODD),
):
    g = gram(js)
    print(
        f"   {name}: rank {rank(g)} (one pointer per harmonic: {2 * len(js)} integers of storage per set beside the count vector)"
    )
print(
    "   the least-rank positive form commuting with the rotation and nonzero on a single row is one Galois plane, rank 2: one pointer (X, Y); that is the click as built, and the least computation among the admissible clicks (2 k products per row for k harmonics)"
)
