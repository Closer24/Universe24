"""The side check of hypothesis B (ALGEBRA.md 9.103 item 6; the model owner's
word of 2026-09-26, "why bit for bit, when a transformation can be checked; a
simple check on the side; in the end you check clicks against experiment"):
the rule 9.57 (1) in integers on a Laves graph box (three exits per Node), with
the three reads weighed 2 R so that the long-wave line per Link is the cubic
lattice's, and two readings at the level of a row.

(1) LIGHT: a plane wave of the pair [1, 1] on a periodic 12^3-cell box (13824
Nodes), along an axis and along the body diagonal; the rotation per interval
read from the integer run (the projection on the start after 400 intervals)
against the Bloch dispersion cos omega = lambda_max(K) / 3.

(2) THE FALL: a matter packet [800, 809] of width 20 cells (57 Links) on a
periodic tube of 500 x 2 x 2 cells (16000 Nodes) in a content c = 1000 + g x
per cell, 3000 intervals; the centroid of the amplitude envelope (a GameBoard
reading of the host) against 9.98 (7)'s prediction per Link, a = (num / den)
g_Link / (6 Gamma) x 2 (1 - 2U)^3 / (1 + (1 - 2U)^2), converted to cells with
the Link 0.354 cells; the control g = 0 beside it.

Read on 2026-09-26 (host, no pin): light's rotation from the integer run within
0.13 percent of the Bloch value on the axis and 0.08 percent on the diagonal;
the fall at 0.94 to 1.03 of the prediction over the five windows of 500
intervals (1.6 x 10^-6 cells per interval squared at U = 0.0575), the control
at 150.000 to 150.003. The rule's physics per Link on the Laves graph is the
cubic lattice's.

Run: python docs/designs/laves_graph/laves_side_check.py (a few seconds).
"""

import itertools
import time

import numpy as np
import scipy.sparse as sp

GAMMA = 10_000
base = np.array([[1, 1, 1], [3, 7, 5], [7, 5, 3], [5, 3, 7]]) / 8.0
POS = np.vstack([base, (base + 0.5) % 1.0])  # 8 Nodes per cubic cell
EDGE = np.sqrt(2) / 4  # the Link, in cells


def laves_links():
    """(type i, type j, cell shift) for the 3 exits of each of the 8 types."""
    out = []
    for i in range(8):
        cands = []
        for j in range(8):
            for sh in itertools.product((-1, 0, 1), repeat=3):
                d = POS[j] + np.array(sh) - POS[i]
                r = np.linalg.norm(d)
                if r > 1e-9:
                    cands.append((r, j, sh))
        cands.sort(key=lambda c: c[0])
        near = [c for c in cands if abs(c[0] - cands[0][0]) < 1e-9]
        assert len(near) == 3
        out += [(i, j, sh) for _, j, sh in near]
    return out


LINKS = laves_links()


def build(nx, ny, nz):
    """The periodic box of nx x ny x nz cells: the adjacency (int64) and the Node positions."""
    cells = np.array(list(itertools.product(range(nx), range(ny), range(nz))))
    ncell = len(cells)
    idx = {tuple(c): k for k, c in enumerate(cells)}
    rows, cols = [], []
    for k, c in enumerate(cells):
        for i, j, sh in LINKS:
            c2 = ((c[0] + sh[0]) % nx, (c[1] + sh[1]) % ny, (c[2] + sh[2]) % nz)
            rows.append(8 * k + i)
            cols.append(8 * idx[c2] + j)
    n = 8 * ncell
    A = sp.csr_matrix((np.ones(len(rows), dtype=np.int64), (rows, cols)), shape=(n, n))
    assert (np.asarray(A.sum(axis=1)).ravel() == 3).all()
    pos = np.repeat(cells, 8, axis=0).astype(float) + np.tile(POS, (ncell, 1))
    return A, pos


def coefficients(num, den, p):
    """The cubic rule's (R, S, w) at the pace p; on the Laves graph the three reads weigh 2 R."""
    g2 = GAMMA * GAMMA
    R = 2 * num * p * p
    S = 12 * den * g2 - 6 * (p * p + g2) * (den - num) - 12 * num * p * p
    w = 6 * den * g2
    return R, S, w


def step(A, a_now, a_before, r, R, S, w):
    total = 2 * R * (A @ a_now) + S * a_now - w * a_before + r
    a_next = total // w
    return a_next, a_now, total - w * a_next


# ---------- (1) LIGHT: the plane wave's rotation against the Bloch dispersion ----------
def light_check():
    n = 12
    A, pos = build(n, n, n)
    N = A.shape[0]
    num = den = 1
    p = GAMMA
    R, S, w = coefficients(num, den, p)
    print(f"(1) LIGHT on a {n}^3-cell Laves box, {N} Nodes, pair [1, 1], pace Gamma")
    for label, K in (
        ("axis x", np.array([2 * np.pi * 2 / n, 0, 0])),
        ("body diagonal", 2 * np.pi * 1 / n * np.array([1, 1, 1])),
    ):
        # the Bloch prediction: cos omega = lambda_max(K) / 3 (the rule on three reads, 2R x S_3 / w at S = 0)
        H = np.zeros((8, 8), dtype=complex)
        for i, j, sh in LINKS:
            d = POS[j] + np.array(sh) - POS[i]
            H[i, j] += np.exp(1j * K @ d)
        lam = np.linalg.eigvalsh(H).max()
        omega_bloch = np.arccos(lam / 3)
        # the integer run: the Bloch eigenvector's plane wave, amplitude 2^16
        vals, vecs = np.linalg.eigh(H)
        v = vecs[:, np.argmax(vals)]
        cellphase = np.exp(1j * ((pos - np.tile(POS, (N // 8, 1))) @ K))  # phase of the cell origin
        field = np.real(np.tile(v, N // 8) * cellphase) * 0 + np.real(np.tile(v, N // 8) * cellphase)
        # a Bloch wave: u_type x exp(i K . cell); use the real part with amplitude 2^16
        amp = (1 << 16) / np.abs(field).max()
        a_now = np.rint(amp * field).astype(np.int64)
        a_before = np.rint(
            amp * np.real(np.tile(v, N // 8) * cellphase * np.exp(-1j * omega_bloch))
        ).astype(np.int64)
        r = np.zeros(N, dtype=np.int64)
        T = 400
        a0 = a_now.astype(float).copy()
        for _t in range(T):
            a_now, a_before, r = step(A, a_now, a_before, r, R, S, w)
        # the rotation per interval read from the projection on the start: cos(omega T) = <a_T, a_0> / <a_0, a_0>
        c = float(a_now.astype(float) @ a0) / float(a0 @ a0)
        # recover omega T modulo the branch by comparing with the Bloch value
        omega_run = np.arccos(np.clip(c, -1, 1)) / T
        cands = [
            (
                np.abs(((2 * np.pi * m + s * np.arccos(np.clip(c, -1, 1))) / T) - omega_bloch),
                (2 * np.pi * m + s * np.arccos(np.clip(c, -1, 1))) / T,
            )
            for m in range(0, 40)
            for s in (1, -1)
        ]
        omega_run = min(cands)[1]
        print(
            f"   {label:14s}: |K| = {np.linalg.norm(K):.4f} per cell = {np.linalg.norm(K) * EDGE:.4f} per Link; omega Bloch = {omega_bloch:.6f}, integer run = {omega_run:.6f}, ratio {omega_run / omega_bloch:.6f}"
        )


# ---------- (2) THE FALL on a Laves tube ----------
def fall_check(g, sigma_cells=20.0, T=3000, every=250, ny=2, nz=2, nx=500, x0=150.0):
    A, pos = build(nx, ny, nz)
    N = A.shape[0]
    x = pos[:, 0]
    num, den = 800, 809
    c = np.rint(1000 + g * x).astype(np.int64)  # the content, rising by g per cell along x
    p = (GAMMA - c).astype(np.int64)
    R, S, w = coefficients(num, den, p)
    cosw = 1 - (1 - num / den) * (1 + (p / GAMMA) ** 2) / 2
    sinw2 = 1 - cosw**2
    env = (1 << 16) * np.exp(-((x - x0) ** 2) / (2 * sigma_cells**2))
    a_now = np.rint(env).astype(np.int64)
    a_before = np.rint(env * cosw).astype(np.int64)
    r = np.zeros(N, dtype=np.int64)
    cents = {}
    for t in range(T + 1):
        if t % every == 0:
            n_ = a_now.astype(float)
            b_ = a_before.astype(float)
            d = (n_ * n_ - 2 * n_ * b_ * cosw + b_ * b_) / sinw2
            cents[t] = float((d * x).sum() / d.sum())
        a_now, a_before, r = step(A, a_now, a_before, r, R, S, w)
    return cents


if __name__ == "__main__":
    t0 = time.time()
    light_check()
    print(f"   light done in {time.time() - t0:.1f} s")
    num, den = 800, 809
    U = (1000 + 150) / (2 * GAMMA)
    factor = 2 * (1 - 2 * U) ** 3 / (1 + (1 - 2 * U) ** 2)
    # the prediction per Link, then per cell: a = (num/den) g_Link / (6 Gamma) x factor, in Links per interval^2
    g_link = 1.0 * EDGE  # g = 1 per cell is EDGE per Link
    a_link = (num / den) * g_link / (6 * GAMMA) * factor
    a_cell = a_link * EDGE
    print(
        f"(2) THE FALL on a Laves tube, g = 1 per cell, U = {U:.4f}, factor {factor:.4f}: predicted a = {a_cell:.4e} cells per interval^2 (= {a_link:.4e} Links per interval^2)"
    )
    for label, g in (("control g = 0", 0), ("g = 1", 1)):
        t0 = time.time()
        cents = fall_check(g)
        print(
            f"   {label}: centroid t = 0, 1000, 2000, 3000: {[round(cents[t], 3) for t in (0, 1000, 2000, 3000)]}  ({time.time() - t0:.0f} s)"
        )
        for t in (500, 1000, 1500, 2000, 2500):
            acc = (cents[t + 500] - 2 * cents[t] + cents[t - 500]) / 500**2
            print(
                f"      t = {t}: a = {acc:.3e} cells/interval^2, ratio to the prediction {acc / a_cell:+.3f}"
            )
