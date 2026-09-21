"""Bell's one nonlocal gather: the map of problem (4) of the seven (the open-problems
physicist, read-only, 2026-09-21; docs/designs/open_problems/bell/NOTE.md).

Host arithmetic on the click's own forms (BEAM_LAW note 37, the amplitude design's 4.2
and 4.3, DERIVATIONS 6.2 and 6.5), the tables here the exact cosines at the half angle
theta_s = pi s / N (the built click rounds them at 1 / 256; the register's cells are
reproduced below to the rung); no engine import, no run.

(A) The law's click of a pair at N = 64: the joint weight is the SQUARE OF THE SUM over
    the labels of the products of the two arms' rotation entries, W(o_A, o_B) = J^2, one
    gather of one record reading both settings; the cells by the rungs at the nearest
    integer; E and S at the CHSH settings (the design's 27, 5, 5, 27 and 176 / 64); the
    marginals over all 64 x 64 setting pairs (no-signalling).
(B) The same rows read LOCALLY, each arm by its own window against its own setting on the
    same birth phase u (the register's A2 under the Beam Law): each outcome a function of
    (u, its setting), the correlation the triangle 1 - 4 k / N, S = 2 exactly.
(C) Fine's theorem on the lattice, brute force: over every deterministic assignment of the
    two outcomes to (u, setting) with u the shared hidden variable, the largest CHSH sum;
    and the same with the far setting allowed into the near outcome (parameter dependence).
(D) Where the cross term lives: the square of a sum against the sum of the squares, the
    difference 2 C'_a S'_a C'_b S'_b per label pair, one number that needs both settings.

Run from the repository root:

    python docs/designs/open_problems/bell/bell_map.py > docs/designs/open_problems/bell/bell_map.out
"""

from __future__ import annotations

import math

N = 64


def rotation(s: int):
    """The half-angle rotation U_s of the amplitude design's 2.2: the entries at
    theta_s = pi s / N (exact here; the tables round them at 1 / 256)."""
    t = math.pi * s / N
    return ((math.cos(t), math.sin(t)), (-math.sin(t), math.cos(t)))


def joint_weights(a: int, b: int):
    """W(o_A, o_B) = (sum over the labels of U_a[o_A][label] U_b[o_B][label])^2: the pair
    [[0, 1], [1, 1]] of the Bell lamp, both labels with amplitude 1."""
    ua, ub = rotation(a), rotation(b)
    w = {}
    for oa in (0, 1):
        for ob in (0, 1):
            j = sum(ua[oa][label] * ub[ob][label] for label in (0, 1))
            w[(oa, ob)] = j * j
    return w


def rungs(weights, order):
    total = sum(weights.values())
    cum = 0.0
    out = []
    for cell in order:
        cum += weights[cell]
        out.append(math.floor((2 * N * cum + total) / (2 * total)))
    return out


ORDER = [(0, 0), (0, 1), (1, 0), (1, 1)]  # A's channel first (the coarse rungs), then B's (the fine)


def counts(a: int, b: int):
    w = joint_weights(a, b)
    r = rungs(w, ORDER)
    c = [r[0]] + [r[i] - r[i - 1] for i in range(1, 4)]
    return dict(zip(ORDER, c, strict=True))


def correlation(a: int, b: int) -> float:
    c = counts(a, b)
    return (c[(0, 0)] + c[(1, 1)] - c[(0, 1)] - c[(1, 0)]) / N


print(
    "A. THE LAW'S CLICK OF A PAIR AT N = 64: one gather of one record reading both settings, the cells by the rungs (the amplitude design's 4.3)"
)
print("   (a, b) | counts ++ +- -+ -- | E = (c++ + c-- - c+- - c-+) / N | cos(2 pi (a - b) / N)")
chsh = [(0, 8), (0, 24), (16, 8), (16, 24)]
es = []
for a, b in chsh:
    c = counts(a, b)
    e = correlation(a, b)
    es.append(e)
    print(
        f"   ({a:2d}, {b:2d}) | {c[(0, 0)]:2d} {c[(0, 1)]:2d} {c[(1, 0)]:2d} {c[(1, 1)]:2d} | {e:+.4f} = {round(e * N):+d}/64 | {math.cos(2 * math.pi * (a - b) / N):+.4f}"
    )
s_law = es[0] - es[1] + es[2] + es[3]
print(
    f"   S = E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24) = {s_law:.5f} = {round(s_law * N)}/64 (the register's 176 / 64 = 2.75; 2 sqrt 2 = {2 * math.sqrt(2):.5f})"
)
# no-signalling over all pairs
bad = 0
for a in range(N):
    for b in range(N):
        c = counts(a, b)
        if c[(0, 0)] + c[(0, 1)] != N // 2 or c[(0, 0)] + c[(1, 0)] != N // 2:
            bad += 1
print(
    f"   the marginals over all {N * N} setting pairs: A's and B's both {N // 2} / {N} in {N * N - bad} pairs, off in {bad} (the design's 'in all 4096 pairs'): no signalling exact in the counts"
)
print()

print(
    "B. THE SAME ROWS READ LOCALLY (the register's A2 under the Beam Law, S = 2 exactly): each arm's window against its own setting on the shared birth phase u"
)


def local_outcome(u: int, s: int) -> int:
    """The window gate: the ray of phase u clicks + if (u - s) mod N < N / 2, else -."""
    return 1 if (u - s) % N < N // 2 else -1


def local_correlation(a: int, b: int) -> float:
    return sum(local_outcome(u, a) * local_outcome(u, b) for u in range(N)) / N


print("   (a, b) | E_local | the triangle 1 - 4 k / N, k = |a - b| mod N folded")
es_local = []
for a, b in chsh:
    e = local_correlation(a, b)
    es_local.append(e)
    k = min((a - b) % N, (b - a) % N)
    print(f"   ({a:2d}, {b:2d}) | {e:+.4f} | {1 - 4 * k / N:+.4f}")
s_local = es_local[0] - es_local[1] + es_local[2] + es_local[3]
print(
    f"   S_local = {s_local:.4f}: Bell's bound, exactly (the register: 'S = 2 exactly, E(a, b) the triangle 1 - 4 k / N')"
)
print()

print(
    "C. FINE'S THEOREM ON THE LATTICE, BRUTE FORCE: the largest CHSH sum over deterministic assignments"
)
# at a fixed u each side chooses an outcome per setting: A(a), A(a'), B(b), B(b'): 16 assignments; S is linear in the mixture, so the max over u-mixtures is the max over assignments
best_local = max(
    abs(A0 * B0 - A0 * B1 + A1 * B0 + A1 * B1)
    for A0 in (1, -1)
    for A1 in (1, -1)
    for B0 in (1, -1)
    for B1 in (1, -1)
)
print(
    f"   local: each outcome a function of (u, its own setting): the largest |S| over the 16 assignments per u is {best_local}; a mixture over u cannot exceed it: S <= 2 for every local mechanism, whatever the six verbs do with u"
)
# parameter dependence: B may read a as well: B(a, b) four values per u
best_pd = max(
    abs(A0 * B00 - A0 * B01 + A1 * B10 + A1 * B11)
    for A0 in (1, -1)
    for A1 in (1, -1)
    for B00 in (1, -1)
    for B01 in (1, -1)
    for B10 in (1, -1)
    for B11 in (1, -1)
)
print(
    f"   parameter-dependent: B reads both settings: the largest |S| is {best_pd} (the algebraic bound 4; the law's gather reaches 2.75 at N = 64, 2.828 on the plateau, below Tsirelson's 2.828 by the tables)"
)
print()

print(
    "D. WHERE THE CROSS TERM LIVES: at the CHSH settings, per label pair, the square of the sum against the sum of the squares"
)
for a, b in chsh[2:3]:
    ua, ub = rotation(a), rotation(b)
    for oa, ob in ORDER[:2]:
        terms = [ua[oa][label] * ub[ob][label] for label in (0, 1)]
        sq_sum = sum(terms) ** 2
        sum_sq = sum(t * t for t in terms)
        print(
            f"   (a, b) = ({a}, {b}), (o_A, o_B) = ({'+' if oa == 0 else '-'}, {'+' if ob == 0 else '-'}): the products per label {terms[0]:+.4f}, {terms[1]:+.4f}; (sum)^2 = {sq_sum:.4f}; sum of squares = {sum_sq:.4f}; the cross term 2 U_a U_a' U_b U_b' = {sq_sum - sum_sq:+.4f}"
        )
print(
    "   the cross term is a product of one entry of A's rotation with one of B's: it exists nowhere on the GameBoard, only at the gather, which reads both settings; a click that reads one arm's rows against one setting forms the sum of squares and stops at 2"
)
