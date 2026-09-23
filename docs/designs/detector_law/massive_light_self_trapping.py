"""COMPUTATION on a chain (not an engine run): the self-trapping of the two record kinds
on a chain under the pace form (MASSIVE_RECORD.md section 4, form (III) of the second draft,
dropped): each record's pace pair at a cell lowered by the OTHER record's magnitude there,
the negative result printed.

    PYTHONPATH=src python docs/designs/detector_law/massive_light_self_trapping.py

The form: each record's pace pair at a cell lowered by the OTHER record's
magnitude there (the one-wall form [1, (1 + kappa M)^2], M the other's envelope amplitude in
units of the amplitude unit, the time average of |a_now| + |a_before| taken as the envelope).
A fixed-point iteration of the two bound-mode problems: light's lowest mode in the well made by the
massive envelope, the massive record's lowest mode in the well made by light's envelope; the
envelopes' peak amplitudes held at declared values (the records' energies are declarations); the
extent (the mode's width) and the frequencies read at the fixed point. A statement about one
dimension, where any well binds one mode; the board's threshold is Reviewer 3's.
"""

from __future__ import annotations

import math

import numpy as np

C2 = 1.0 / 3.0


def lowest_mode(n_index2: np.ndarray, mu2: float) -> tuple[float, np.ndarray]:
    """The lowest standing mode of the leapfrog's continuum form omega^2 a = -(c^2 / n^2) lap a + mu2 a
    with the pace lowered by the index (n^2 per cell): the generalised eigenproblem on the chain."""
    length = len(n_index2)
    main = 2 * C2 / n_index2 + mu2
    off = -C2 / np.sqrt(
        n_index2[:-1] * n_index2[1:]
    )  # the symmetric form of the Laplacian with a varying pace
    from scipy.linalg import eigh_tridiagonal

    vals, vecs = eigh_tridiagonal(main, off, select="i", select_range=(0, 0))
    v = vecs[:, 0]
    v = v / np.max(np.abs(v))
    if v[length // 2] < 0:
        v = -v
    return float(math.sqrt(max(vals[0], 0.0))), v


def width(v: np.ndarray) -> float:
    x = np.arange(len(v))
    w = v * v
    m = np.sum(x * w) / np.sum(w)
    return float(2 * math.sqrt(np.sum((x - m) ** 2 * w) / np.sum(w)))


def self_trap(mu2=1 / 16, kappa_l=1.0, kappa_m=1.0, amp_l=1.0, amp_m=1.0, length=400, iterations=60):
    x = np.arange(length)
    env_m = amp_m * np.exp(
        -(((x - length / 2) / 10.0) ** 2)
    )  # the first guess, a block of about 20 cells
    env_l = np.zeros(length)
    history = []
    for it in range(iterations):
        n2_l = (1 + kappa_l * env_m) ** 2  # light's pace lowered where the massive envelope is
        w_l, v_l = lowest_mode(n2_l, 0.0)
        env_l = amp_l * np.abs(v_l)
        n2_m = (1 + kappa_m * env_l) ** 2  # the massive record's pace lowered where light's envelope is
        w_m, v_m = lowest_mode(n2_m, mu2)
        env_m_new = amp_m * np.abs(v_m)
        change = float(np.max(np.abs(env_m_new - env_m)))
        env_m = 0.5 * env_m + 0.5 * env_m_new
        history.append((it, w_l, width(v_l), w_m, width(v_m), change))
    it, w_l, s_l, w_m, s_m, change = history[-1]
    free_l = "unbound (the chain's lowest free mode)" if s_l > length / 4 else "bound"
    print(
        f"mu2 = {mu2} (omega_0 = {math.sqrt(mu2):.4f}), kappa_l = {kappa_l}, kappa_m = {kappa_m}, the peaks amp_l = {amp_l}, amp_m = {amp_m}:"
        f" after {it + 1} iterations (the last change {change:.2e}): light's mode omega = {w_l:.4f}, width {s_l:.1f} cells ({free_l});"
        f" the massive mode omega = {w_m:.4f} (against omega_0 {math.sqrt(mu2):.4f}), width {s_m:.1f} cells"
    )
    return history


if __name__ == "__main__":
    for kl, km, al, am in (
        (1.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 0.2, 1.0),
        (0.3, 0.3, 1.0, 1.0),
        (3.0, 3.0, 1.0, 1.0),
        (1.0, 0.0, 1.0, 1.0),
    ):
        self_trap(kappa_l=kl, kappa_m=km, amp_l=al, amp_m=am)
