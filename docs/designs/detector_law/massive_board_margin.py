"""COMPUTATION on a scratch board (scipy sparse eigenproblem, periodic faces; not an
engine run): the extent of a cube's bound mode in the massive medium under form (B),
and the margin an object needs from the board's faces (MASSIVE_RECORD.md section 11,
the margin rule). The medium carries the background pair D_out = 1 + mu^2 / 2 on
every Node; the cube of side s carries the lowered pair D_in = 1 + (mu^2 - g) / 2.
A mode: 2 cos omega_b D a = (L / 3) a, the symmetric form A = D^-1/2 (L / 3) D^-1/2,
lambda_max = 2 cos omega_b; outside the cube the tail decays along an axis as
exp(-kappa x) with cosh kappa = 3 D_out cos omega_b - 2; the extent 1 / kappa Links
(COMPUTATION), read also directly from the eigenvector's 1 / e fall from the face.
HOST: the time of one interval of the two rules (light and the massive record) on
the box, measured with numpy.

    PYTHONPATH=src python docs/designs/detector_law/massive_board_margin.py
"""

import time

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


def bound_mode(n, s, mu, g):
    L = periodic_sum6(n)
    x = np.arange(n) - (n - 1) / 2
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    inside = ((np.abs(X) < s / 2) & (np.abs(Y) < s / 2) & (np.abs(Z) < s / 2)).ravel()
    D_out = 1 + mu**2 / 2
    D = np.where(inside, 1 + (mu**2 - g) / 2, D_out)
    d = 1 / np.sqrt(D)
    A = sp.diags(d) @ (L / 3) @ sp.diags(d)
    t0 = time.time()
    val, vec = eigsh(A, k=1, which="LA", tol=1e-9, ncv=40, maxiter=20000)
    dt = time.time() - t0
    lam = val[0]
    omega_b = np.arccos(lam / 2)
    omega_0 = np.arccos(1 / D_out)
    eps = 1 - (omega_b / omega_0) ** 2
    ck = 3 * D_out * np.cos(omega_b) - 2
    kappa = np.arccosh(ck) if ck > 1 else 0.0
    v = np.abs(vec[:, 0]).reshape(n, n, n)
    c = n // 2
    face = int(np.ceil((n - 1) / 2 + s / 2))  # the first Node outside the cube along +x
    line = v[face:, c, c] / v[face, c, c]
    over = np.where(line < np.e**-1)[0]
    extent_read = float(over[0]) if len(over) else float("nan")
    return omega_b, omega_0, eps, kappa, extent_read, dt


def host_interval(n):
    """The time of one interval of the two rules on an n^3 periodic box (numpy, HOST)."""
    a = np.random.default_rng(0).standard_normal((n, n, n))
    b = a.copy()
    num = np.full((n, n, n), 128.0)
    den = np.full((n, n, n), 129.0)
    t0 = time.time()
    for _ in range(2):
        s6 = sum(np.roll(a, sh, ax) for ax in range(3) for sh in (1, -1))
        nxt = (num * s6) / (3 * den) - b
        b, a = a, nxt
        s6 = sum(
            np.roll(b, sh, ax) for ax in range(3) for sh in (1, -1)
        )  # light's rule, the second record
        _ = s6 / 3 - a
    return (time.time() - t0) / 2


print("the cube's bound mode in the massive medium (form (B), periodic box), and the margin rule")
print(
    "mu | s | g | box n | omega_b | omega_0 | eps | kappa | extent 1/kappa (Links) | extent read (1/e from the face) | the side by the rule s + 2 extent | eigsh s"
)
worlds = [
    (0.15, 10, 0.15**2, 96),
    (0.15, 14, 0.15**2 / 2, 96),
    (0.15, 20, 0.15**2, 96),
    (0.15, 28, 0.15**2 / 2, 96),
    (0.05, 30, 0.05**2, 128),
    (0.05, 42, 0.05**2 / 2, 128),
    (0.05, 60, 0.05**2, 128),
]
for mu, s, g, n in worlds:
    ob, o0, eps, kappa, ext_read, dt = bound_mode(n, s, mu, g)
    ext = 1 / kappa if kappa > 0 else float("inf")
    side = s + 2 * ext if np.isfinite(ext) else float("inf")
    print(
        f"{mu} | {s} | {g:.5f} | {n} | {ob:.5f} | {o0:.5f} | {eps:.4f} | {kappa:.5f} | {ext:.1f} | {ext_read:.0f} | {side:.0f} | {dt:.0f}"
    )

print("\nHOST: one interval of the two rules on a periodic box (numpy, this machine):")
for n in (64, 96, 128):
    t = host_interval(n)
    print(
        f"  n = {n} ({n**3:,} Nodes): {t:.3f} s per interval; a rest world of 3 periods at N_0 = 42 ({3 * 42} intervals) {3 * 42 * t:.0f} s; a moving world of 1500 + 8000 intervals {9500 * t / 60:.0f} min"
    )
