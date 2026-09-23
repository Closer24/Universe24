"""COMPUTATION (scipy sparse eigenproblem on the world's own periodic box; not an engine
run): the pin of each MOVING world of MASSIVE_RECORD.md section 11, computed per world
from its own s, g and gamma_m before that world's run (Reviewer 3's line on the schedule
table, through the Boss, 16:42Z): section 8's one formula

    f / f_0 = omega_b(gamma_m s, g) / (gamma_m omega_b(s, g)),

the moving block a resting well of width gamma_m s ALONG the motion and s across, its
phase read at 1 / gamma_m; the non-integer width interpolated between the two integer
widths. gamma_m at k = 3 on the lattice: beta = (1 / k) / c with c = 1 / sqrt 3, so
beta = sqrt 3 / 3 and gamma_m = sqrt(3 / 2) = 1.22474. Printed per world: omega_b at
rest, the two widths' omega_b, the pin, and the first-order 1 / gamma_m (1 - eps
(gamma_m^2 - 1) / 2) beside it as the band's second term only.

    PYTHONPATH=src python docs/designs/detector_law/massive_moving_pins.py
"""

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh


def periodic_sum6(n):
    o = np.ones(n - 1)
    S1 = sp.diags([o, o, [1.0], [1.0]], [-1, 1, n - 1, -(n - 1)], shape=(n, n))
    I1 = sp.identity(n)
    return (
        sp.kron(sp.kron(S1, I1), I1) + sp.kron(sp.kron(I1, S1), I1) + sp.kron(sp.kron(I1, I1), S1)
    ).tocsr()


def box_mode(n, sx, s, mu, g, L):
    idx = np.arange(n)
    # exactly sx cells along x and s across: an index range, so that an odd width is its own
    # (a half-width test on an even box would fold 25 onto 24)
    ax = (idx >= (n - sx) // 2) & (idx < (n - sx) // 2 + sx)
    ac = (idx >= (n - s) // 2) & (idx < (n - s) // 2 + s)
    X, Y, Z = np.meshgrid(ax, ac, ac, indexing="ij")
    inside = (X & Y & Z).ravel()
    D_out = 1 + mu**2 / 2
    D = np.where(inside, 1 + (mu**2 - g) / 2, D_out)
    d = 1 / np.sqrt(D)
    A = sp.diags(d) @ (L / 3) @ sp.diags(d)
    val = eigsh(A, k=1, which="LA", tol=1e-9, ncv=40, maxiter=50000, return_eigenvectors=False)
    return np.arccos(val[0] / 2), np.arccos(1 / D_out)


K = 3
BETA = (1 / K) * np.sqrt(3)
GAMMA = 1 / np.sqrt(1 - BETA**2)

print(f"k = {K}: beta_c = {BETA:.5f}, gamma_m = {GAMMA:.5f}, 1 / gamma_m = {1 / GAMMA:.5f}")
print(
    "world | mu | s | g | box | omega_b(s) | eps | gamma_m s | omega_b(lo) | omega_b(hi) | THE PIN f/f_0 | first order"
)
worlds = [
    ("(ii-a) moving_20", 0.15, 20, 0.15**2, 64),
    ("(ii-b) moving_28", 0.15, 28, 0.15**2 / 2, 64),
]
for name, mu, s, g, n in worlds:
    L = periodic_sum6(n)
    ob, o0 = box_mode(n, s, s, mu, g, L)
    eps = 1 - (ob / o0) ** 2
    w = GAMMA * s
    lo, hi = int(np.floor(w)), int(np.ceil(w))
    ob_lo, _ = box_mode(n, lo, s, mu, g, L)
    ob_hi, _ = box_mode(n, hi, s, mu, g, L)
    ob_w = ob_lo + (ob_hi - ob_lo) * (w - lo)
    pin = ob_w / (GAMMA * ob)
    first = (1 / GAMMA) * (1 - eps * (GAMMA**2 - 1) / 2)
    print(
        f"{name} | {mu} | {s} | {g:.5f} | {n}^3 | {ob:.5f} | {eps:.4f} | {w:.2f} | {ob_lo:.5f} | {ob_hi:.5f} | {pin:.4f} | {first:.4f}"
    )
print(
    "(ii-c) and the layer pin worlds: the same formula at pin time on the world's own board by pins.py,"
    " the inputs s, g, gamma_m = sqrt(3 / 2) per row; the layer's s = 14, g = mu^2 / 4 world 0.8132"
    " (massive_layer_pins.out)."
)
