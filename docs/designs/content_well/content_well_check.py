"""Record 2151, line 1 (the model owner's question, "how would a body hold itself
without a well, with one uniform rule?"): the content at a body's Nodes needed to
bind a matter mode of side 3, 5 or 9 Links by the rule's own pace, with no declared
pair well; a body bound by its own content through gravity's time part.

A host computation, no engine, no pin: the rule's rest operator 2 cos omega a =
(R_i S6(a)_i + S_i a_i) / w with the pace p_i = Gamma - c_i at every Node
(ALGEBRA.md 9.57 (1), 9.94), symmetrised by sqrt(R), on an open cube of 31^3
Nodes, a uniform content c inside a cube of side w and 0 outside, the largest
eigenvalue by Lanczos. A mode is bound when its eigenvalue exceeds the free
medium's band top 2 num / den; its tail is 1 / kappa with cosh kappa = 3 lambda
den / (2 num) - 2 (the margin rule's own form); the rms extent is a GameBoard
reading of the mode. The content well's depth is bounded by the guard p > 0: at c
= Gamma it is 1 - num / den, half the pair well's ceiling, and near c = Gamma the
Node freezes (R = 0) rather than binds.

Read on 2026-09-26: at the shipped kind [800, 809] no mode of side 3 or 5 binds
below the guard, and side 9 binds from c near 5000 (U = c / (2 Gamma) = 0.25,
the tail 10 Links at 6000); at [800, 850] side 9 binds from c near 2000 (U =
0.10), side 5 from near 3500 (U = 0.18, the tail 12 Links at 4000) and side 3
from near 5000 (U = 0.25). So gravity's time part holds a body only at the
compactness of a neutron star's surface, U from 0.1 to 0.3; the shipped bodies
(s = 2000, U = 0.1 at their Nodes) bind by their own content only at side 9 of
the heavier kind.

Run: python docs/designs/content_well/content_well_check.py (a few minutes).
"""

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

G = 10_000


def operator(num, den, c):
    """2 cos omega a = (R_i S6(a)_i + S_i a_i) / w, symmetrised by sqrt(R): M = sqrt(R) S6 sqrt(R) + diag(S), over w."""
    p = (G - c).astype(np.float64)
    R = 2 * num * p**2
    Sd = 12 * den * G**2 - 6 * (p**2 + G**2) * (den - num) - 12 * num * p**2
    w = 6 * den * G**2
    n = c.shape[0]
    N = n**3
    idx = np.arange(N).reshape(n, n, n)
    rows, cols = [], []
    for axis in range(3):
        for sgn in (1, -1):
            j = np.roll(idx, sgn, axis=axis)
            # open cube: drop the wrapped links
            mask = np.ones_like(idx, dtype=bool)
            sl = [slice(None)] * 3
            sl[axis] = 0 if sgn == 1 else n - 1
            mask[tuple(sl)] = False
            rows.append(idx[mask].ravel())
            cols.append(j[mask].ravel())
    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    sq = np.sqrt(R).ravel()
    A = sp.csr_matrix((sq[rows] * sq[cols], (rows, cols)), shape=(N, N))
    M = (A + sp.diags(Sd.ravel())) / w
    return M


def bound(num, den, side, cpeak, n=31):
    c = np.zeros((n, n, n))
    lo = n // 2 - side // 2
    c[lo : lo + side, lo : lo + side, lo : lo + side] = cpeak
    M = operator(num, den, c)
    lam, vec = eigsh(M, k=1, which="LA", tol=1e-6)
    lam = float(lam[0])
    top = 2 * num / den
    v = vec[:, 0].reshape(n, n, n)
    dens = v**2 / (v**2).sum()
    x = np.arange(n) - n // 2
    rms = np.sqrt((dens * (x[:, None, None] ** 2 + x[None, :, None] ** 2 + x[None, None, :] ** 2)).sum())
    ch = 3 * lam * den / (2 * num) - 2
    extent = 1 / np.arccosh(ch) if ch > 1 else float("inf")
    return lam - top, extent, rms


for num, den in ((800, 809), (800, 850)):
    print(
        f"kind [{num}, {den}]: band top 2 num/den = {2 * num / den:.5f}; the content ceiling at c = Gamma gives depth {1 - num / den:.4f}"
    )
    for side in (3, 5, 9):
        line = []
        for cpeak in (1000, 2000, 3000, 4000, 6000, 8000, 9999):
            d, ext, rms = bound(num, den, side, cpeak)
            line.append(f"c={cpeak}: depth {d:+.2e}, tail {ext:6.1f} L, rms {rms:5.1f}")
        print(f"  side {side}:")
        [print("     " + s) for s in line]
