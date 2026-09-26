"""Record 2157: a bound record in a declared pair well that moves rigidly with the record, the
algebra's number beside the reviewer's (ALGEBRA.md 9.105). HOST computation on the rule's rest
operator, symmetrised by sqrt(R / w), on an open cube of side 31: the well of Nature24's
bodies.py (the kind [800, 850], the well [800, 801] on a cube of side 5), the pace p = Gamma - c
uniform. Three readings of the mode: its rotation's response to a uniform content, X = 2 Gamma
|d omega_b / d c| (the force on the mode in a content gradient g is |d omega_b / d c| g); its
Rayleigh mass m* = 2 sin omega_b / Q, Q the mode's x-hop expectation (the mode times the
character of K carries the current Q sin K, so its speed at the start is Q sin K / (2 sin
omega_b) = K / m* by the rule's continuity); and its first excited rotation, the trap's rate
omega_t = omega_1 - omega_b, which sets the drag of a well one interval behind the record,
gamma = omega_t^2 per interval. Every number a GameBoard reading of the host.

Run: .venv/bin/python docs/designs/content_well/pair_well_fall_check.py
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

GAMMA = 10_000
KIND = (800, 850)
WELL = (800, 801)
SIDE = 5
CUBE = 31


def operator(
    content: float, bloch: float = 0.0
) -> tuple[sp.spmatrix, np.ndarray, np.ndarray, np.ndarray]:
    """The rest operator at the uniform content: 2 cos omega a = M a, M = sqrt(R / w) A sqrt(R / w) +
    diag(S / w) with A the six-neighbour adjacency of the open cube, the x hops carrying the Bloch
    phase; returns M and the x-link index arrays for the hop expectation."""
    n, count = CUBE, CUBE**3
    index = np.arange(count).reshape(n, n, n)
    num = np.full((n, n, n), KIND[0], float)
    den = np.full((n, n, n), KIND[1], float)
    low = n // 2 - SIDE // 2
    num[low : low + SIDE, low : low + SIDE, low : low + SIDE] = WELL[0]
    den[low : low + SIDE, low : low + SIDE, low : low + SIDE] = WELL[1]
    pace = float(GAMMA - content)
    hop = 2 * num * pace**2
    rest = 12 * den * GAMMA**2 - 6 * (pace**2 + GAMMA**2) * (den - num) - 12 * num * pace**2
    wall = 6 * den * GAMMA**2
    root = np.sqrt(hop / wall).ravel()
    rows, cols, values, on_x = [], [], [], []
    for axis in range(3):
        for sign in (1, -1):
            shifted = np.roll(index, sign, axis=axis)
            mask = np.ones_like(index, dtype=bool)
            face = [slice(None)] * 3
            face[axis] = 0 if sign == 1 else n - 1
            mask[tuple(face)] = False
            r, c = index[mask].ravel(), shifted[mask].ravel()
            phase = np.exp(1j * sign * bloch) if axis == 0 and bloch else 1.0
            rows.append(r)
            cols.append(c)
            values.append(root[r] * root[c] * phase)
            on_x.append(np.full(r.shape, axis == 0))
    rows_a, cols_a = np.concatenate(rows), np.concatenate(cols)
    values_a, on_x_a = np.concatenate(values), np.concatenate(on_x)
    dtype = complex if bloch else float
    matrix = sp.csr_matrix((values_a.astype(dtype), (rows_a, cols_a)), shape=(count, count)) + sp.diags(
        (rest / wall).ravel().astype(dtype)
    )
    return matrix, rows_a[on_x_a], cols_a[on_x_a], root


def rotations(
    content: float, modes: int = 1
) -> tuple[np.ndarray, np.ndarray, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    matrix, xr, xc, root = operator(content)
    values, vectors = eigsh(matrix, k=modes, which="LA", tol=1e-9)
    order = np.argsort(-values)
    return np.arccos(values[order] / 2), vectors[:, order], (xr, xc, root)


def main() -> None:
    omega, vectors, (xr, xc, root) = rotations(0.0, modes=2)
    omega_b, omega_1 = float(omega[0]), float(omega[1])
    omega_0 = float(np.arccos(KIND[0] / KIND[1]))
    print(f"omega_b {omega_b:.5f} (the vacuum's omega_0 {omega_0:.5f}); omega_1 {omega_1:.5f}")
    shift = 200.0
    up, _, _ = rotations(shift)
    down, _, _ = rotations(-shift)
    response = (float(up[0]) - float(down[0])) / (2 * shift)
    x_factor = 2 * GAMMA * abs(response)
    print(
        f"d omega_b / d c = {response:.4e} per level; X = 2 Gamma |d omega_b / d c| = {x_factor:.4f} (the clock alone: omega_b {omega_b:.4f})"
    )
    psi = vectors[:, 0] / np.linalg.norm(vectors[:, 0])
    hop_expectation = float(np.sum(root[xr] * root[xc] * psi[xr] * psi[xc]))
    mass = 2 * np.sin(omega_b) / hop_expectation
    vacuum_mass = 3 * KIND[1] * np.sin(omega_0) / KIND[0]
    print(
        f"Q {hop_expectation:.5f}; m* = 2 sin omega_b / Q = {mass:.4f} (the vacuum's 3 den sin omega_0 / num = {vacuum_mass:.4f})"
    )
    wavenumber = 0.1242
    print(
        f"the mode times the character K = {wavenumber}: speed at the start Q sin K / (2 sin omega_b) = {hop_expectation * np.sin(wavenumber) / (2 * np.sin(omega_b)):.4f} Links per interval"
    )
    slope = 4
    fall = abs(response) * slope / mass
    free = (KIND[0] / KIND[1]) * slope / (6 * GAMMA)
    print(
        f"g = {slope} per Link: a = |d omega_b / d c| g / m* = {fall:.3e}; the free packet (num / den) g / (6 Gamma) = {free:.3e}; X / m* = {x_factor / mass:.4f}"
    )
    trap = omega_1 - omega_b
    drag = trap**2
    print(
        f"the trap's rate omega_t = {trap:.5f} per interval; a well one interval behind: gamma = omega_t^2 = {drag:.3e} per interval"
    )
    for span in (1200, 1500, 3000):
        x = drag * span
        print(
            f"  over {span} intervals: mean speed fraction {(1 - np.exp(-x)) / x:.3f}; fall fraction {2 * (x - 1 + np.exp(-x)) / x**2:.3f}"
        )


if __name__ == "__main__":
    main()
