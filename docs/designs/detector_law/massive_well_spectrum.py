"""COMPUTATION on a scratch board (scipy sparse eigenproblem, periodic faces; not an
engine run): the bound spectrum of the pair's well, the atom's levels in the design's
terms (MASSIVE_RECORD.md section 9, the owner's question of record 1430: what is an
atom, what is an electron, in the algebra).

The massive kind in form (B) with the medium's pair D_out = 1 + mu^2 / 2 on every Node
and a lowered pair D(x) = 1 + (mu^2 - g(x)) / 2 on the well's Nodes (the inside's gap
reduced, never reversed: g <= mu^2). A mode: 2 cos omega D a = (L / 3) a; the symmetric
form A = D^-1/2 (L / 3) D^-1/2, lambda = 2 cos omega; bound iff lambda > 2 / D_out. The
first bound modes' frequencies below the medium's gap, their binding depths eps_n = 1 -
omega_n^2 / omega_0^2 and the ratios eps_n / eps_1, printed against Balmer's 1 / n^2
(the Coulomb ladder, NATURE) for three declared well shapes: a cube (section 4), a
sphere, and a Coulomb-like profile g(r) = mu^2 min(1, r_0 / r). The scale condition is
said in the record: nature's hydrogen has a Bohr radius 137 times c / omega_0.

    PYTHONPATH=src python docs/designs/detector_law/massive_well_spectrum.py
"""

import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

MU = 0.15


def periodic_sum6(n):
    o = np.ones(n - 1)
    S1 = sp.diags([o, o, [1.0], [1.0]], [-1, 1, n - 1, -(n - 1)], shape=(n, n))
    I1 = sp.identity(n)
    return (
        sp.kron(sp.kron(S1, I1), I1) + sp.kron(sp.kron(I1, S1), I1) + sp.kron(sp.kron(I1, I1), S1)
    ).tocsr()


def spectrum(n, g, k=8):
    L = periodic_sum6(n)
    D_out = 1 + MU**2 / 2
    D = 1 + (MU**2 - g) / 2
    d = 1 / np.sqrt(D)
    A = sp.diags(d) @ (L / 3) @ sp.diags(d)
    t0 = time.time()
    vals = eigsh(A, k=k, which="LA", tol=1e-9, ncv=48, maxiter=20000, return_eigenvectors=False)
    vals = np.sort(vals)[::-1]
    omega_0 = np.arccos(1 / D_out)
    top = 2 / D_out
    bound = [np.arccos(v / 2) for v in vals if v > top]
    return omega_0, bound, time.time() - t0


def profiles(n):
    x = np.arange(n) - (n - 1) / 2
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    R = np.sqrt(X**2 + Y**2 + Z**2)
    cube = (np.abs(X) < 10) & (np.abs(Y) < 10) & (np.abs(Z) < 10)
    return {
        "a cube of side 20, the full depth mu^2": (MU**2 * cube).ravel(),
        "a sphere of radius 10, the full depth mu^2": (MU**2 * (R < 10)).ravel(),
        "a Coulomb-like profile g(r) = mu^2 min(1, 6 / r)": (
            MU**2 * np.minimum(1.0, 6 / np.maximum(R, 1e-9))
        ).ravel(),
        "a Coulomb-like profile g(r) = mu^2 min(1, 12 / r)": (
            MU**2 * np.minimum(1.0, 12 / np.maximum(R, 1e-9))
        ).ravel(),
    }


def main():
    n = 64
    print(
        f"a periodic box of {n}^3 Nodes; mu = {MU}; c / omega_0 = {(1 / np.sqrt(3)) / MU:.2f} Links; nature's Bohr radius 137 c / omega_0 = {137 * (1 / np.sqrt(3)) / MU:.0f} Links (NOT affordable here: the scale condition)"
    )
    for name, g in profiles(n).items():
        omega_0, bound, dt = spectrum(n, g)
        eps = [1 - (w / omega_0) ** 2 for w in bound]
        ratios = [e / eps[0] for e in eps] if eps else []
        print(
            f"{name}: omega_0 = {omega_0:.4f}; bound modes below the gap: {len(bound)} of 8 asked ({dt:.0f} s)"
        )
        for i, (w, e, r) in enumerate(zip(bound, eps, ratios, strict=True)):
            print(
                f"   mode {i + 1}: omega = {w:.5f}, eps = {e:.4f}, eps / eps_1 = {r:.3f}   (Balmer's 1 / n^2 for n = 1, 2, 3: 1.000, 0.250, 0.111; the old 27 / 20 = 1.350 as a ratio of radii)"
            )


if __name__ == "__main__":
    main()
