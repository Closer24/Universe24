"""Does the node's initialization depend on a seed? (the owner's question of 2026-10-30, 09:4x UTC). Whole numbers alone.

(1) the 24 from the Node-clock's six Spokes alone, by Rule3's weight: how many candidates weigh 1, and whether they are
    closed under the product (a group) with the identity among them; no seed enters the construction;
(2) every channel's group sum P has trace 24 and P P = 24 P, so its invariant space is one line (multiplicity 1);
(3) the table read from that line by many seeds: every elementary seed e_j whose group sum is not 0, and x = B^(index),
    first index heaviest, for B = 2 to 7 through P P^T: each proportional to the head's table, compared by
    cross-multiplying (no gcd);
(4) the closed form with no search: B the Spokes count, read from the star, u = P P^T x.

Usage: python3 -I tb_seed.py <src of tensor24-review at ed745f7cc>
"""

import itertools
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

star = L.star(3)
matrix, weight = K.turns(star)
turns = [matrix[t] for t in range(len(weight)) if weight[t]]
keys = {tuple(m.reshape(-1).tolist()) for m in turns}
identity = tuple(np.eye(3, dtype=object).reshape(-1).tolist())
closed = all(tuple(a.dot(b).reshape(-1).tolist()) in keys for a in turns for b in turns)
print(
    f"(1) candidates {len(weight)}, weighing 1: {len(turns)}; the identity among them: {identity in keys};"
    f" closed under the product: {closed}; weights other than 0 and 1: {sorted({int(w) for w in weight} - {0, 1})}"
)

held = list(K.kinds(matrix))
inv = list(K.kinds(K.inverse(matrix)))
head = L.tables(held, inv, weight, K.projector)
spokes = star.shape[0]


def times(base, m):
    """base multiplied by itself m times (1 at m = 0)."""
    out = 1
    for _ in range(m):
        out *= base
    return out


def proportional(u, t):
    j = next(a for a in range(len(t)) if t[a])
    return u[j] != 0 and all(int(u[a]) * int(t[j]) == int(t[a]) * int(u[j]) for a in range(len(t)))


channels = line = 0
seeds_tried = seeds_same = 0
powers = {b: 0 for b in range(2, 8)}
closed_form = 0
for i, k, m in itertools.product(range(len(held)), repeat=3):
    shape = tuple(held[q].shape[-1] for q in (m, i, k))
    n = int(np.prod(shape))
    P = K.projector(weight, held[m], inv[i], inv[k]).reshape(n, n)
    if not P.any():
        continue
    channels += 1
    t = head[(i, k, m)].reshape(-1)
    trace = sum(int(P[a, a]) for a in range(n))
    line += int(trace == len(turns) and (P.dot(P) == len(turns) * P).all())
    for j in range(n):
        column = P[:, j]
        if column.any():
            seeds_tried += 1
            seeds_same += int(proportional(column, t))
    for b in powers:
        x = np.array([times(b, n - 1 - a) for a in range(n)], dtype=object)
        powers[b] += int(proportional(P.dot(P.T).dot(x), t))
    x = np.array([times(spokes, n - 1 - a) for a in range(n)], dtype=object)
    closed_form += int(proportional(P.dot(P.T).dot(x), t))
print(f"(2) channels {channels}; trace {len(turns)} and P P = {len(turns)} P, one invariant line, on {line}")
print(
    f"(3) elementary seeds with a group sum not 0: {seeds_tried}, each proportional to the head's table: {seeds_same};"
    f" x = B^(index) through P P^T, B = 2 to 7: {[powers[b] for b in powers]} of {channels}"
)
print(f"(4) B = the Spokes count, {spokes}, read from the star: {closed_form} of {channels}")
