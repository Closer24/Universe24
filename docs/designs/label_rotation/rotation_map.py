"""The label rotation per Link, read in integers (the mathematician,
2026-09-20, read-only): the tables of 2N from the engine's `phase_cosines`
(the one import), the record click's ladder restated, the angle-index form
(the rotation kept as an index added per Link mod 2N and the tables applied
once at the click), the growth of the norm and the multiplicity under a
rotation applied per Link, the two-label counts at three distances and
the three-label (neutrino) form for one declared mixing at N = 64. Output
beside this file: `rotation_map.out`. Every count is exact; a float appears
only as a report beside its integer.
"""

from __future__ import annotations

import math

from event_universe.core.phase import phase_cosines, phase_sines

N = 64
C2, S2 = phase_cosines(2 * N), phase_sines(2 * N)  # the half-angle tables of 2N, scale 256
C1, S1 = phase_cosines(N), phase_sines(N)  # the circle's tables, scale 256
CEILING = 2**62 - 1


def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def ladder(weights: list[int]) -> list[int]:
    """The record click's counts over the N births u = 0 .. N - 1: the rungs
    b_k = (2 N C_k + Total) // (2 Total) on the cumulative weights."""
    total = sum(weights)
    rungs = [0]
    cumulative = 0
    for w in weights:
        cumulative += w
        rungs.append((2 * N * cumulative + total) // (2 * total))
    return [rungs[k + 1] - rungs[k] for k in range(len(weights))]


# --------------------------------------------------------------------------
section("A. The isometry fact and the growth under a rotation applied per Link")
norms = sorted({C2[s] ** 2 + S2[s] ** 2 for s in range(2 * N)})
print(
    f"n_s = C'[s]^2 + S'[s]^2 over the 2N = {2 * N} settings: min {norms[0]}, max {norms[-1]} (65536 exact only where an entry is 0 or 256)"
)
s = 21
n_s = C2[s] ** 2 + S2[s] ** 2
print(
    f"a rotation at s = {s} applied once per Link: the amplitude norm x n_s = {n_s} and the multiplicity x 65536 per Link;"
)
for L in (1, 2, 3, 4, 8, 64):
    m = 65536**L
    print(
        f"   L = {L:2d}: multiplicity 65536^L = 2^{16 * L}, {'within' if m <= CEILING else 'BEYOND'} 2^62; norm factor n_s^L = {n_s**L:.3e}"
        if L <= 8
        else f"   L = {L:2d}: multiplicity 2^{16 * L}: BEYOND 2^62 by 2^{16 * L - 62}"
    )
print(
    "so a per-Link application of the tables overflows the register's ceiling at the fourth Link of any path."
)

# --------------------------------------------------------------------------
section("B. The angle-index form: two labels, one rate per Link, the tables once at the click")
print(
    "a row born on label 0 (amplitude 1), the record's label angle sigma advanced by s per Link mod 2N,"
)
print(
    "the click at an analyser of setting a applies U_(sigma + a) once: channel + weight C'^2, channel - weight S'^2;"
)
print("the counts over the 64 births by the ladder, at three distances, for s = 3 per Link and a = 0:")
rate, a = 3, 0
print(
    f"{'L':>4s} {'sigma':>5s} {'C2':>6s} {'S2':>6s} {'w+':>7s} {'w-':>7s} {'counts +/-':>11s} {'cos^2 (report)':>15s}"
)
for L in (0, 5, 10, 16, 21, 32, 43, 64):
    sigma = (L * rate + a) % (2 * N)
    w_plus, w_minus = C2[sigma] ** 2, S2[sigma] ** 2
    counts = ladder([w_plus, w_minus])
    print(
        f"{L:4d} {sigma:5d} {C2[sigma]:6d} {S2[sigma]:6d} {w_plus:7d} {w_minus:7d} {counts!s:>11s} {math.cos(math.pi * sigma / N) ** 2:15.4f}"
    )
print(
    "the multiplicity: the birth's norm x 65536 once (the click's table), whatever L: within the ceiling for every path length."
)
print(
    "exactness: an angle added mod 2N is exact; the one table lookup rounds once (n_sigma / 65536 within 0.36 %), as the design's window does."
)

# --------------------------------------------------------------------------
section("C. Three labels (the neutrino's families): the mixing at the ends, a phase per Link per label")
# The declared mixing: U = R23(s23) R12(s12), theta13 = 0, on the half-angle
# tables at scale 256; the entries of U at scale 65536 (products of two).
s12, s23 = 11, 16  # settings of 2N = 128: the angles pi s / N = 30.9 and 45 degrees
c12, sn12, c23, sn23 = C2[s12], S2[s12], C2[s23], S2[s23]
U = [
    [c12 * 256, sn12 * 256, 0],
    [-sn12 * c23, c12 * c23, sn23 * 256],
    [sn12 * sn23, -c12 * sn23, c23 * 256],
]
print(f"U at scale 65536 (s12 = {s12}, s23 = {s23}): {U}")
rows_norm = [sum(x * x for x in row) for row in U]
print(f"the rows' norms (65536^2 = {65536**2} ideal): {rows_norm}")
rates = (0, 5, 9)  # phase steps per Link per label (the mass differences), N = 64
print(
    f"the phase rates per Link per label: {rates} steps of N = {N}; born as flavour 0 (row 0 of U): the labels' amplitudes {U[0]}"
)
print(
    "at the click the analyser reads flavour beta: a_beta = sum_j U[beta][j] x U[0][j] x (C[phi_j], S[phi_j]), phi_j = rates_j x L mod N;"
)
print(
    "the weights |a_beta|^2 (scale 65536^2 x 256 per amplitude component), the counts over 64 births by the ladder:"
)
print(f"{'L':>4s} {'phases':>14s} {'weights (0, 1, 2)':>52s} {'counts':>14s} {'P (report)':>22s}")
for L in (0, 8, 16, 24, 32, 48, 64):
    phases = [(r * L) % N for r in rates]
    weights = []
    for beta in range(3):
        re = sum(U[beta][j] * U[0][j] * C1[phases[j]] for j in range(3))
        im = sum(U[beta][j] * U[0][j] * S1[phases[j]] for j in range(3))
        weights.append(re * re + im * im)
    counts = ladder(weights)
    total = sum(weights)
    print(
        f"{L:4d} {phases!s:>14s} {weights!s:>52s} {counts!s:>14s} {[round(w / total, 3) for w in weights]!s:>22s}"
    )

print(
    "the multiplicity: the birth's row at scale 256 (norm 65536 = 2^16) and the click's rows at scale 65536 (norm 2^32): 2^48 per path, within 2^62;"
)
print(
    "   a mixing applied per Link instead would multiply by 2^32 per Link: beyond the ceiling at the second Link."
)
