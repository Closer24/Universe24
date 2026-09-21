"""The Bell sum S(N) of the law from 24.4's closed form, exact (read-only,
the derivation mathematician, 2026-09-21; the external reviewer's F01):
the tables' exact correlations at the CHSH settings, E_1 = 46565 / 65773
at (0, N/8) and (0, 3N/8) and E_2 = 46452 / 65773 at (N/4, N/8) and (N/4,
3N/8) (the paper's main.tex, the Gram form at the scale 256, independent
of N), the cells of a settings pair in the order ++, +-, -+, -- with the
weights (1 + E) / 4, (1 - E) / 4, (1 - E) / 4, (1 + E) / 4 of the total
(the second pair the reverse), the rungs b_k = floor(N C_k / T + 1 / 2)
(6.2: `(2 N C_k + T) // (2 T)`), the counts b_k - b_(k-1) over the N
births of the wheel, E_N per pair from the counts, S = E(0, N/8) - E(0,
3N/8) + E(N/4, N/8) + E(N/4, 3N/8). Exact rationals; no run.

Run from the repository root:

    python docs/designs/derivations_beam/bell_plateau.py > docs/designs/derivations_beam/bell_plateau.out
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr

E1 = Fr(46565, 65773)
E2 = Fr(46452, 65773)
POH = (2.82759, 0.00051)


def rungs(n: int, weights: list[Fr]) -> list[int]:
    cumulative, out = Fr(0), []
    for w in weights:
        cumulative += w
        out.append(int((2 * n * cumulative + 1) // 2))  # floor(n C_k / T + 1/2)
    return out


def pair(n: int, e: Fr, reverse: bool) -> tuple[Fr, list[int]]:
    same, diff = (1 + e) / 4, (1 - e) / 4
    weights = [diff, same, same, diff] if reverse else [same, diff, diff, same]
    b = rungs(n, weights)
    counts = [b[0], b[1] - b[0], b[2] - b[1], b[3] - b[2]]
    return Fr(counts[0] + counts[3] - counts[1] - counts[2], n), counts


def s_of(n: int) -> tuple[Fr, list[tuple[Fr, list[int]]]]:
    pairs = [pair(n, E1, False), pair(n, E1, True), pair(n, E2, False), pair(n, E2, False)]
    total = pairs[0][0] - pairs[1][0] + pairs[2][0] + pairs[3][0]
    return total, pairs


def closed(n: int) -> Fr:
    """S(N) = 8 [round(N (1 + E_1) / 4) + round(N (1 + E_2) / 4)] / N - 4 for
    even N (each pair's E_N = 4 b_1 / N - 1 when its rungs are symmetric)."""
    r1 = int((2 * n * (1 + E1) / 4 + 1) // 2)
    r2 = int((2 * n * (1 + E2) / 4 + 1) // 2)
    return Fr(8 * (r1 + r2), n) - 4


limit = 2 * E1 + 2 * E2
bound = 2 * math.sqrt(2)
print("S(N) from the rungs on the tables' exact correlations E_1 = 46565/65773, E_2 = 46452/65773:")
print(
    "  N | S(N) exact | decimal | S - 2 sqrt 2 | E_N per settings pair (0,N/8), (0,3N/8), (N/4,N/8), (N/4,3N/8) | the counts of the first pair | (S - Poh) / sigma"
)
for n in (64, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 1 << 20):
    s, pairs = s_of(n)
    assert s == closed(n), n
    es = ", ".join(str(p[0]) for p in pairs)
    print(
        f"  {n} | {s} | {float(s):.9f} | {float(s) - bound:+.2e} | {es} | {pairs[0][1]} |"
        f" {(float(s) - POH[0]) / POH[1]:+.2f}"
    )
print(
    f"  the limit N -> infinity: 2 (E_1 + E_2) = {limit} = {float(limit):.9f}, below 2 sqrt 2 by {bound - float(limit):.2e}"
)
print()
print(
    "Where the plateau ends: the plateau 181/64 needs round(N (1 + E_1) / 4) + round(N (1 + E_2) / 4) = 437 N / 512;"
)
for n in (512, 8192, 16384, 65536):
    x1, x2 = n * (1 + E1) / 4, n * (1 + E2) / 4
    print(
        f"  N = {n}: N (1 + E_1) / 4 = {float(x1):.3f} -> {int((2 * x1 + 1) // 2)}, N (1 + E_2) / 4 = {float(x2):.3f} -> {int((2 * x2 + 1) // 2)};"
        f" the sum {int((2 * x1 + 1) // 2) + int((2 * x2 + 1) // 2)} against 437 N / 512 = {437 * n // 512}"
    )
print(
    "  at N = 16384 both rungs round up (the fractional parts 0.83 and 0.79) and the sum exceeds 437 N / 512 by one: S leaves the plateau."
)
