"""Malus's law from the table entries in force, the pin's integers (read-only,
the mathematician, 2026-09-21; docs/designs/malus/NOTE.md). The half-angle
tables of 2N from the engine's own `phase_cosines` and `phase_sines` (the one
import), the cell weights of the click for a row born on label 0 through a
rotation of the label bit by a setting s (the design's 2.2), a which-path
`read` and a `sum` set's window s' (the design's 4.1), and the counts over W
births by the click's rungs b_k = (2 W C_k + T) // (2 T) (BEAM_LAW note 46).
Every count is an integer of the tables; a float appears only as a report
beside its integer. No run.

Run from the repository root:

    PYTHONPATH=src python docs/designs/malus/malus_map.py > docs/designs/malus/malus_map.out
"""

from __future__ import annotations

import math

from event_universe.core.phase import phase_cosines, phase_sines

N = 256  # the phase circle of the pinned worlds (the entry A12's N = 2^8)
W = 256  # the wheel's W: W births, u = ordinal x r mod W over every residue once for r odd
C2, S2 = phase_cosines(2 * N), phase_sines(2 * N)  # the half-angle tables of 2N at scale 256


def degrees(s: int) -> float:
    """The angle of the setting s on the half-angle tables: 180 s / N degrees."""
    return 180.0 * s / N


def rungs(weights: list[int], births: int) -> list[int]:
    """The click's rungs on the cumulative weights, b_k = (2 W C_k + T) // (2 T), b_0 = 0."""
    total = sum(weights)
    out, cumulative = [0], 0
    for w in weights:
        cumulative += w
        out.append((2 * births * cumulative + total) // (2 * total))
    return out


def counts(weights: list[int], births: int) -> list[int]:
    """The counts per cell over the births: the widths of the rungs."""
    b = rungs(weights, births)
    return [b[k + 1] - b[k] for k in range(len(weights))]


def one_polariser(s: int) -> tuple[list[str], list[int]]:
    """A row born on label 0 (along y) read at a `sum` set whose window is s: the
    channels + and - with the residual amplitudes (C'[s], -S'[s]) on label 0
    (the design's 4.1); the weights their squares."""
    return ["+", "-"], [C2[s] ** 2, S2[s] ** 2]


def read_then_window(s2: int) -> tuple[list[str], list[int]]:
    """A row born on label 0 with no rotation before the which-path `read` (the
    polariser at 0 degrees, the born axis: one cell at the read, the label 0),
    then a `sum` set whose window is s2: the cells 0+ and 0-."""
    return ["0+", "0-"], [(256 * C2[s2]) ** 2, (256 * S2[s2]) ** 2]


def chain(s1: int, s2: int) -> tuple[list[str], list[int]]:
    """A row born on label 0, rotated on the GameBoard by s1 (`rotate`: the rows
    (w C'[s1]) on label 0 and (w S'[s1]) on label 1), read by a which-path
    `read` (the factor selecting the label: the cells split by the label),
    then a `sum` set whose window is s2 (+: C'[s2] on label 0, S'[s2] on label
    1; -: -S'[s2] on label 0, C'[s2] on label 1). The cells in the click's
    order: the read's labels ascending, then the channels + before -."""
    a0, a1 = C2[s1], S2[s1]
    names = ["0+", "0-", "1+", "1-"]
    weights = [
        (a0 * C2[s2]) ** 2,
        (a0 * S2[s2]) ** 2,
        (a1 * S2[s2]) ** 2,
        (a1 * C2[s2]) ** 2,
    ]
    return names, weights


print("1. THE HALF-ANGLE TABLES OF 2N AT N = 256 (SCALE 256), THE SETTINGS OF THE PIN")
for s in (0, 32, 64, 96, 128):
    n_s = C2[s] ** 2 + S2[s] ** 2
    print(
        f"   s = {s:3d} ({degrees(s):5.1f} degrees): C'[s] = {C2[s]:4d}, S'[s] = {S2[s]:4d}, n_s = C'^2 + S'^2 = {n_s}"
        f" (65536 x {n_s / 65536:.5f}); cos^2 = {math.cos(math.radians(degrees(s))) ** 2:.5f}, the table's C'^2 / n_s = {C2[s] ** 2 / n_s:.5f}"
    )
print()

print("2. ONE POLARISER: THE ROW BORN ALONG y READ AT A WINDOW s, THE COUNTS OVER W = 256 BIRTHS")
print(
    "   the cells (+ the pass, - the absorbed), the weights C'^2 and S'^2, the rungs b_k = (2 W C_k + T) // (2 T)"
)
for s in (0, 32, 64, 96, 128):
    names, weights = one_polariser(s)
    b = rungs(weights, W)
    c = counts(weights, W)
    print(
        f"   s = {s:3d} ({degrees(s):5.1f} degrees): weights {dict(zip(names, weights, strict=True))}, rungs {b},"
        f" counts {dict(zip(names, c, strict=True))}: the pass {c[0]} of {W} = {c[0] / W:.5f} (Malus cos^2 {math.cos(math.radians(degrees(s))) ** 2:.5f}, x 256 = {256 * math.cos(math.radians(degrees(s))) ** 2:.2f})"
    )
print()

print("3. THE THREE ARRANGEMENTS OF THE PIN (NATURE ROW 9), THE EXACT INTEGERS AT N = W = 256")
names, weights = read_then_window(64)
print(
    "   (a) one polariser at 45 degrees: the read at label 0 (the born axis: the polariser at 0 degrees passes the whole) then the window s = 64:"
)
print(
    f"       weights {dict(zip(names, weights, strict=True))}, counts {dict(zip(names, counts(weights, W), strict=True))}: the pass cell 0+ = {counts(weights, W)[0]} of 256 = 1/2 exactly"
)
names, weights = read_then_window(128)
print(
    "   (b) two crossed: the read at label 0 (the polariser at 0 degrees) then the window s = 128 (90 degrees):"
)
print(
    f"       weights {dict(zip(names, weights, strict=True))}, counts {dict(zip(names, counts(weights, W), strict=True))}: the pass cell 0+ = {counts(weights, W)[0]} of 256 = 0 exactly"
)
names, weights = chain(64, 64)
c = counts(weights, W)
print(
    "   (c) a third at 45 degrees between two crossed: the rotate s1 = 64 (45 degrees from y), the read, the window s2 = 64 (45 degrees on: 90 from y):"
)
print(
    f"       weights {dict(zip(names, weights, strict=True))}, counts {dict(zip(names, c, strict=True))}: the pass cell 0+ = {c[0]} of 256 = 1/4 exactly;"
)
print(
    f"       passed the first (the cells 0+ and 0-): {c[0] + c[1]} = 1/2 of the births; of those, passed the second: {c[0]} = 1/2 of the polarised: Malus's 1/4"
)
print(
    f"       (the cells 1+ and 1- are the rows the first polariser absorbed, {c[2]} and {c[3]}: they go on to the end and click there, no body sinks them)"
)
print()

print(
    "4. THE SAME CHAIN AT 22.5-DEGREE STEPS (A12's four-polariser chain is NOT covered: it needs a second read after a rotate)"
)
names, weights = chain(32, 32)
c = counts(weights, W)
print(
    f"   the rotate s1 = 32, the read, the window s2 = 32: weights {dict(zip(names, weights, strict=True))}, counts {dict(zip(names, c, strict=True))}:"
)
print(
    f"   the pass cell 0+ = {c[0]} of 256 = {c[0] / 256:.5f} against cos^4(22.5 degrees) = {math.cos(math.radians(22.5)) ** 4:.5f} (x 256 = {256 * math.cos(math.radians(22.5)) ** 4:.2f}); the table's (C'[32]^2 / n_32)^2 = {(C2[32] ** 2 / (C2[32] ** 2 + S2[32] ** 2)) ** 2:.5f}"
)
print()

print("5. THE ROBUSTNESS OF THE INTEGERS TO THE WHEEL'S RATE r AND TO THE COUNT u RUNS ON")
for r in (1, 157, 159, 255):
    residues = sorted({(ordinal * r) % W for ordinal in range(W)})
    print(
        f"   r = {r:3d}: u = ordinal x r mod 256 over 256 births covers {len(residues)} residues (every one once: {len(residues) == W})"
    )
names, weights = chain(64, 64)
b = rungs(weights, W)
print(
    f"   the chain's rungs {b}: with u over every residue once, the cell k holds b_k - b_(k-1) births whatever r; with u stepping by 2 (a rebirth's count per row, if the rotate counted so), every even residue twice, the same widths {counts(weights, W)} since every width is even"
)
print()

print(
    "6. THE MULTIPLICITY BUDGET: the birth's norm 1 (branches [[0, 1]] by default), the rotate x 65536, the click x 2^32: 2^48 per path, within 2^62 (three rotations fit, four do not: the register's L5)"
)
