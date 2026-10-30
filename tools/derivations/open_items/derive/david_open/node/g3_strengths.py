"""G3, the four strengths of term 6 on the head, whole numbers alone.

(a) every family's spring from an A1 held count through the head's own tables, per kind: S_K = g n C[K, K -> A1];
(b) the least whole lam that bounds the potential, lam = g^2 div (2 kappa) + 1, run on Animate's operation with the
    head's gear at the swings that ran away without it (m3 (i)): does the gear stay?

Usage: python3 -I g3_strengths.py <src of tensor24-review at 9751f91c1>
"""
import sys
import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds as K, step  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

matrix, weight = K.turns(L.star(3))
held = list(K.kinds(matrix))
inv = list(K.kinds(K.inverse(matrix)))
tab = L.tables(held, inv, weight, K.projector)
names = ["A1", "A2", "E", "T1", "T2"]
for kk in range(5):
    c = tab[(kk, kk, 0)]  # C[K, K -> A1], shape (1, d, d)
    print(f"(a) C[{names[kk]}, {names[kk]} -> A1] as the spring's matrix over g n: {c[0].tolist()}")

W = 6 * 15162856759112389 * 1000 * 1000
n, D, kappa = 10**6, W // 400, W // 16
g, _ = carry(D, n, 0)
lam_bound, _ = carry(g * g, 2 * kappa, 0)
lam_least = lam_bound + 1
CAP = 10**60


def run(lam, laid, rounds=4000):
    x, k = (laid, laid, 0), (n, n, 0)
    least_k = n
    for t in range(1, rounds + 1):
        xx, kk = x[0], k[0]
        c = xx * xx
        half, _ = carry(g * c, 2, 0)
        px = -g * kk * xx - lam * c * xx
        pk = -half - kappa * (kk - n)
        x, k = step.gear(*x, W, px), step.gear(*k, W, pk)
        least_k = min(least_k, k[0])
        if abs(x[0]) > CAP or abs(k[0]) > CAP:
            return f"ran past 10^60 at round {t}"
    return f"stays over {rounds} rounds, least K {least_k}"


print(f"(b) g = {g}, kappa = W div 16, g^2 div 2 kappa = {lam_bound}, so the least whole lam is {lam_least}")
for laid in (10**5, 10**7, 2 * 10**7, 10**8):
    print(f"    X laid at {laid}: lam 0: {run(0, laid)}; lam least: {run(lam_least, laid)}; lam twice the bound: {run(2 * lam_least, laid)}")
