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


def control_with(gamma_x, n, s, mu, g, L, ob):
    """The one formula with another gamma, a CONTROL beside the pin."""
    wc = gamma_x * s
    lo_c, hi_c = int(np.floor(wc)), int(np.ceil(wc))
    ob_lo_c, _ = box_mode(n, lo_c, s, mu, g, L)
    ob_hi_c, _ = box_mode(n, hi_c, s, mu, g, L)
    return (ob_lo_c + (ob_hi_c - ob_lo_c) * (wc - lo_c)) / (gamma_x * ob)


K = 3
MU = 0.15
COS_OMEGA_0 = 1 / (1 + MU**2 / 2)  # num / den of the medium's pair [800, 809]
BETA = (1 / K) * np.sqrt(3)  # the pace over light's c
# Reviewer 3's MUST on PR #1053 (18:12Z), decided by derivation (MASSIVE_RECORD.md section 8): the
# massive rule's own cone is c_m = c sqrt(cos omega_0) (its band cos omega = cos omega_0 cos omega_light,
# so omega^2 = omega_0^2 + cos omega_0 c^2 k^2), and the boost that carries the well is at c_m; the one
# formula's gamma is gamma(c_m) = 1 / sqrt(1 - beta_c^2 / cos omega_0). gamma(c) beside it, a CONTROL.
GAMMA_C = 1 / np.sqrt(1 - BETA**2)  # light's gamma, a CONTROL beside
GAMMA_M = 1 / np.sqrt(1 - BETA**2 / COS_OMEGA_0)  # the second-order cone c_m, a CONTROL beside
# Reviewer 3's token on 26674947 (19:20Z), the exact form of the same derivation: the band's cone at its
# bottom, from cos omega = cos omega_0 cos omega_l(k) with no truncation, is c_eff^2 = cos omega_0
# (omega_0 / sin omega_0) c^2 (c_m^2 to second order); the one formula's named gamma is gamma(c_eff).
OMEGA_0 = np.arccos(COS_OMEGA_0)
C_EFF2 = COS_OMEGA_0 * OMEGA_0 / np.sin(OMEGA_0)  # over c^2
GAMMA = 1 / np.sqrt(1 - BETA**2 / C_EFF2)

print(
    f"k = {K}: beta_c = {BETA:.5f}; the one formula's named gamma = gamma(c_eff) = {GAMMA:.5f} at the exact cone"
    f" c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2 = {C_EFF2:.5f} c^2 (1 / gamma = {1 / GAMMA:.5f});"
    f" the CONTROLS beside: gamma(c_m) = {GAMMA_M:.5f} (the second-order cone), gamma(c) = {GAMMA_C:.5f} (light's)"
)
print(
    "world | mu | s | g | box | omega_b(s) | eps | gamma_m s | omega_b(lo) | omega_b(hi) | THE PIN f/f_0 (gamma at c_eff) | first order | the controls (gamma at c_m, at c)"
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

    # the CONTROLS beside: the same formula with gamma(c_m) and with gamma(c)
    control_m = control_with(GAMMA_M, n, s, mu, g, L, ob)
    control = control_with(GAMMA_C, n, s, mu, g, L, ob)
    print(
        f"{name} | {mu} | {s} | {g:.5f} | {n}^3 | {ob:.5f} | {eps:.4f} | {w:.2f} | {ob_lo:.5f} | {ob_hi:.5f} | {pin:.4f} | {first:.4f}"
        f" | the CONTROLS: with gamma(c_m) {control_m:.4f}, with gamma(c) {control:.4f}"
    )
print(
    "(ii-c) and the layer pin worlds: the same formula at pin time on the world's own board by pins.py,"
    " the inputs s, g and gamma_m at c_m per row; the layer's s = 14, g = mu^2 / 4 world by massive_layer_pins.out"
    " (massive_layer_pins.out)."
)
