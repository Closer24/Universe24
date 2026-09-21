"""The click without amplitudes, as integers (read-only, the derivation
mathematician, 2026-09-21; DERIVATIONS_BEAM.md section 6.7): the cell's
weight as the bilinear form f^T G f of the record's integer vector f on the
Gram matrix G = E^T E of the tables, checked bit for bit against the
click's own pointers (E f, then the square) on the registered cells of
`mz_equal` (1681 / 1682), `slits_low` (the 64 clicks) and the pair's CHSH
cells (27, 5, 5, 27 and 5, 27, 27, 5), and the several-arm click as one
bilinear form on the tensor product of the arms' vectors; the group-ring
convolution form beside it, which is exact arithmetic and not bit-identical.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/derivations_beam/click_gram.py > docs/designs/derivations_beam/click_gram.out

A host computation on the engine's own tables; no engine run.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events.amplitude import AMPLITUDE_SCALE, cell_of, cmul, half_angle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fraction_free"))
import two_slits_map as tsm  # noqa: E402  (the registered two-slit walk, its constants and functions)

N = 64
C = phase_cosines(N)
S = phase_sines(N)
E = [list(C), list(S)]  # the 2 x N matrix of the tables
G = [[C[j] * C[k] + S[j] * S[k] for k in range(N)] for j in range(N)]  # E^T E


def ev(f: list[int]) -> tuple[int, int]:
    """E f: the pointer of the integer vector f (amounts per phase), at the tables' scale."""
    return (sum(f[p] * C[p] for p in range(N)), sum(f[p] * S[p] for p in range(N)))


def gram(f: list[int]) -> int:
    """f^T G f."""
    return sum(f[j] * G[j][k] * f[k] for j in range(N) for k in range(N) if f[j] and f[k])


def unit(p: int, a: int = 1) -> list[int]:
    f = [0] * N
    f[p % N] += a
    return f


def add(f, g):
    return [x + y for x, y in zip(f, g, strict=True)]


def convolve(f, g):
    h = [0] * N
    for j in range(N):
        if f[j]:
            for k in range(N):
                if g[k]:
                    h[(j + k) % N] += f[j] * g[k]
    return h


def scale(f, a):
    return [a * x for x in f]


print("THE CLICK WITHOUT AMPLITUDES: f^T G f against (E f)^2, integer by integer")

# 1. The identity on random vectors, and what G is.
print("\n1. THE IDENTITY (E f)_x^2 + (E f)_y^2 = f^T G f, G = E^T E")
random.seed(1)
ok = True
for _ in range(200):
    f = [random.randint(-5, 5) if random.random() < 0.3 else 0 for _ in range(N)]
    x, y = ev(f)
    ok &= x * x + y * y == gram(f)
print(f"  200 random integer vectors of Z^64: identical {ok}")
diag = sorted({G[j][j] for j in range(N)})
print(
    f"  G symmetric: {all(G[j][k] == G[k][j] for j in range(N) for k in range(N))}; rank 2 (E has two rows); diagonal values {diag} (256^2 = 65536)"
)
dev = max(
    abs(G[j][k] - round(65536 * math.cos(2 * math.pi * (j - k) / N))) for j in range(N) for k in range(N)
)
circ = sum(1 for j in range(N) for k in range(N) if G[j][k] != G[(j + 1) % N][(k + 1) % N])
print(
    f"  deviation from 65536 cos(2 pi (j - k) / N): at most {dev}; entries not circulant (G[j+1][k+1] != G[j][k]): {circ} of {N * N}"
)
kills = all(
    all(
        v == 0
        for v in [sum(G[j][k] * (unit(p)[k] + unit(p + 32)[k]) for k in range(N)) for j in range(N)]
    )
    for p in range(N)
)
print(
    f"  G kills every antipodal pair e_p + e_(p+32) exactly (C[p+32] = -C[p], S[p+32] = -S[p]): {kills}"
)
rot = sum(1 for p in range(N) if gram(unit(p)) != gram(unit(0)))
print(
    f"  rotation invariance broken by the rounding: e_p^T G e_p differs from 65536 at {rot} of 64 phases (the eight values over the births)"
)
e1sq = cmul(ev(unit(1)), ev(unit(1)))
print(
    f"  E is not a ring homomorphism on the rounded tables: E(e_1)^2 = {e1sq}, 256 E(e_2) = {tuple(256 * v for v in ev(unit(2)))}"
)

# 2. mz_equal: the record's elements at the ports, all 64 birth phases.
print("\n2. mz_equal (L1): D1 = 41 rows in phase at u + 16, D2 = 1 at u + 32, multiplicity 1682")
same = True
clicks = [0, 0]
offers = set()
for u in range(N):
    f1 = unit(u + 16, AMPLITUDE_SCALE * 41)
    f2 = unit(u + 32, AMPLITUDE_SCALE * 1)
    w1, w2 = gram(f1), gram(f2)
    x1, y1 = ev(f1)
    x2, y2 = ev(f2)
    same &= (w1 == x1 * x1 + y1 * y1) and (w2 == x2 * x2 + y2 * y2)
    weights = [(w1, 1682), (w2, 1682)]
    clicks[cell_of(weights, N, u)] += 1
    offers.add((Fraction(w1, w1 + w2), Fraction(w2, w1 + w2)))
print(
    f"  f^T G f == (E f)^2 at every u: {same}; clicks D1 {clicks[0]}, D2 {clicks[1]} (registered 64, 0)"
)
print(
    f"  the offers over the total: {sorted(offers)[0]} .. {sorted(offers)[-1]} ({len(offers)} distinct values; 1681/1682 and 1/1682 registered as the design's integers, exact where C^2 + S^2 = 65536)"
)

# 3. slits_low: the registered walk's cells, each via G and via E, then the ladder.
print("\n3. slits_low (L2): the 80 sets' cells via f^T G f against the pointers, and the 64 clicks")
n, d = tsm.PHASE_PER_LINK
fan = [(1, 0)] + [
    (a, b)
    for a in range(1, 12)
    for b in range(-11, 12)
    if b and a + abs(b) <= 12 and math.gcd(a, b) == 1
]
lamp_rows = []
for vector in tsm.LAMP_DIRECTIONS:
    end, node, age, made = tsm.walk(tsm.LAMP, vector, tsm.stop_lamp)
    lamp_rows.append((vector, end, node, age, made))
leg_phase = {
    node: tsm.phase_by_clock(age, n, d) for _, end, node, age, _ in lamp_rows if end == "opening"
}
rows = []
for o, opening in enumerate(tsm.OPENINGS):
    for vector in fan:
        end, node, age, made = tsm.walk(opening, vector, tsm.stop_fan)
        rows.append(
            (o, vector, end, node, age, (leg_phase[opening] + tsm.phase_by_clock(age, n, d)) % N)
        )
screen_rows = {}
for row in rows:
    if row[2] == "screen":
        screen_rows.setdefault(row[3][1], []).append(row)
order = []  # (name, multiplicity, groups of phases: one group per Node)
for _vector, end, node, age, _made in lamp_rows:
    if end == "wall":
        order.append((f"wall {node}", 5, [[tsm.phase_by_clock(age, n, d)]]))
for y in range(tsm.HEIGHT):
    at = screen_rows.get(y, [])
    order.append((f"screen_{y}", 455, [[r[5] for r in at]] if at else []))
for face, side in (("+y", tsm.HEIGHT - 1), ("-y", 0)):
    groups = {}
    for row in rows:
        if row[2] == "face" and (row[3][1] >= tsm.HEIGHT if side else row[3][1] < 0):
            groups.setdefault(row[3][0], []).append(row[5])
    order.append((f"face {face}", 455, list(groups.values())))
same = True
counts = [0] * len(order)
for u in range(N):
    weights = []
    for _name, m, groups in order:
        via_g = 0
        via_e = 0
        for group in groups:  # one Node: coherent within, the record's element there
            f = [0] * N
            for ph in group:
                f[(ph + u) % N] += AMPLITUDE_SCALE
            via_g += gram(f)
            x, y = ev(f)
            via_e += x * x + y * y
        same &= via_g == via_e
        weights.append((via_g, m))
    counts[cell_of(weights, N, u)] += 1
wall = tuple(counts[i] for i, (name, _, _) in enumerate(order) if name.startswith("wall"))
screen = {
    int(name.split("_")[1]): counts[i]
    for i, (name, _, _) in enumerate(order)
    if name.startswith("screen") and counts[i]
}
faces = tuple(counts[i] for i, (name, _, _) in enumerate(order) if name.startswith("face"))
print(f"  {len(order)} sets; f^T G f == (E f)^2 on every (set, Node, u): {same}")
print(f"  clicks by the Gram form: wall {wall}, screen {screen}, faces {faces}")
print(
    f"  registered: wall {tsm.REGISTERED_WALL}, screen {tsm.REGISTERED_SCREEN}, faces {tsm.REGISTERED_FACES}; reproduced: {wall == tsm.REGISTERED_WALL and screen == tsm.REGISTERED_SCREEN and faces == tsm.REGISTERED_FACES}"
)

# 4. The pair (L3): two arms, the labels 0 and 3, the counters' half-angle rotation at the turn 0.
print(
    "\n4. THE PAIR (L3): the cells (c_A, c_B) as built (cmul on the evaluated residuals), as one bilinear form on f_A (x) f_B, and by the ring convolution"
)


def entries(setting: int, bit: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """amplitude.py's `rotation` at the turn 0: the column `bit` of U_s for the channels + and -."""
    c, sn = half_angle(setting, N)
    turn = (C[0], S[0])
    if bit == 0:
        return (c * 256, 0), (-sn * 256, 0)
    return cmul((sn, 0), turn), cmul((c, 0), turn)


def pair_cells(a: int, b: int, u: int):
    labels = (0, 3)  # the joint labels: bit 0 on both arms, bit 1 on both arms
    built = []
    ring = []
    for ca in (0, 1):
        for cb in (0, 1):
            amp = (0, 0)
            f_ring = [0] * N
            for label in labels:
                bit = 1 if label == 3 else 0
                ra = entries(a, bit)[ca]
                rb = entries(b, bit)[cb]
                pa = ev(unit(u, AMPLITUDE_SCALE))
                pb = ev(unit(u, AMPLITUDE_SCALE))
                # as built: residual = cmul(entry, pointer) per arm, the arms' product, the label sum
                amp = tuple(x + y for x, y in zip(amp, cmul(cmul(ra, pa), cmul(rb, pb)), strict=True))
                # the ring form: real entries at the turn 0; the arms' product is the convolution
                pair = convolve(unit(u, AMPLITUDE_SCALE), unit(u, AMPLITUDE_SCALE))
                f_ring = add(f_ring, scale(pair, ra[0] * rb[0]))
            built.append(amp[0] ** 2 + amp[1] ** 2)
            x, y = ev(f_ring)
            ring.append(256 * 256 * (x * x + y * y))  # the scale of one evaluation against two
    return built, ring


def counts_of(weights, ms=1):
    counts = [0] * 4
    for u in range(N):
        w = weights(u)
        counts[cell_of([(v, 1) for v in w], N, u)] += 1
    return counts


chsh = {
    (0, 8): (27, 5, 5, 27, 44),
    (0, 24): (5, 27, 27, 5, -44),
    (16, 8): (27, 5, 5, 27, 44),
    (16, 24): (27, 5, 5, 27, 44),
}
S_built = 0
S_ring = 0
for (a, b), reg in chsh.items():
    cb = counts_of(lambda u, a=a, b=b: pair_cells(a, b, u)[0])
    cr = counts_of(lambda u, a=a, b=b: pair_cells(a, b, u)[1])
    identical = all(pair_cells(a, b, u)[0] == pair_cells(a, b, u)[1] for u in range(N))
    eb = cb[0] + cb[3] - cb[1] - cb[2]
    er = cr[0] + cr[3] - cr[1] - cr[2]
    S_built += eb if (a, b) != (0, 24) else -eb
    S_ring += er if (a, b) != (0, 24) else -er
    print(
        f"  settings ({a}, {b}): built {cb} E x 64 = {eb}; ring convolution {cr} E x 64 = {er}; the weights bit-identical at every u: {identical}; registered {reg[:4]}, E {reg[4]}"
    )
print(f"  S x 64: built {S_built}, ring {S_ring}, registered 176")
# the tensor form: the weight as F^T G2 F with F = sum_l f_A^l (x) f_B^l (with the entries' scalars), G2 = (M (E (x) E))^T (M (E (x) E))
u = 5
a, b = 16, 8
same = True
for ca in (0, 1):
    for cb in (0, 1):
        F = {}
        for label in (0, 3):
            bit = 1 if label == 3 else 0
            ra = entries(a, bit)[ca][0]
            rb = entries(b, bit)[cb][0]
            F[(u, u)] = F.get((u, u), 0) + ra * rb * AMPLITUDE_SCALE * AMPLITUDE_SCALE
        # (E (x) E) F: the four products x_a x_b, x_a y_b, y_a x_b, y_a y_b summed; then M: (xx - yy, xy + yx)
        xx = sum(v * C[p] * C[q] for (p, q), v in F.items())
        xy = sum(v * C[p] * S[q] for (p, q), v in F.items())
        yx = sum(v * S[p] * C[q] for (p, q), v in F.items())
        yy = sum(v * S[p] * S[q] for (p, q), v in F.items())
        w_tensor = (xx - yy) ** 2 + (xy + yx) ** 2
        same &= w_tensor == pair_cells(a, b, u)[0][ca * 2 + cb]
print(
    f"  the tensor form F^T G2 F (G2 of size N^2 x N^2, rank 2) equals the built weight on the four cells at u = {u}, settings ({a}, {b}): {same}"
)

# 5. The cost.
k = 2
print(
    f"\n5. THE COST per cell of k rows at one Node: the pointer 2k products and 2 squares; f^T G f k^2 products on the sparse f (N^2 = {N * N} dense); the tensor form N^arms (4096 at two arms, 262144 at three)"
)
