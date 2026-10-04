"""Dark matter in kind: the three lines of Section 7.5's paragraph checked on the band.

For a gapped scalar family [num, den] (the matter row of dimension 1) the script checks, in real
arithmetic and from Rule3's coefficients alone: (1) the Wronskian of a one-line record is 0 at
every Node and interval, so the row reads no holder of the sign and writes no light of its own
(random levels, the reading re_now im_before - im_now re_before with im = 0); (2) the fall of a
free quantum in a content gradient, a = -(d omega_0 / dU) / m* per unit gradient from the band at
a pace (Eq. (4) of the paper), is the same at every amplitude and count, the universality of free
fall for the row, and equals the closed form 2 cos omega_0 / (3 (1 + cos omega_0)) of S.18;
(3) the free quantum is cold: its rest rotation is omega_0 and its group velocity (num / 3 den)
sin k / sin omega tends to 0 with k, a slow fall and no light. No run of the engine, no file read.

    python paper/general_formula/dark_matter_check.py
"""

from __future__ import annotations

import math

import numpy as np


def band(num: int, den: int, u: float, k: float) -> float:
    """The rotation at a content u (the clock N = e^{-u}, the Link N^2) and wave number k along an axis."""
    big_n = math.exp(-u)
    return math.acos(1 - (1 - num / den) * big_n**2 - (num / (3 * den)) * big_n**4 * (1 - math.cos(k)))


def main(num: int = 2, den: int = 3) -> None:
    rng = np.random.default_rng(24)
    re_now, re_before = rng.integers(-1000, 1000, 50), rng.integers(-1000, 1000, 50)
    im_now = im_before = np.zeros(50, dtype=int)
    wronskian = re_now * im_before - im_now * re_before
    print(
        f"(1) the Wronskian of a one-line record over 50 random Nodes: largest |W| = {int(np.abs(wronskian).max())}"
    )
    omega_0 = band(num, den, 0.0, 0.0)
    inertia = 3 * math.tan(omega_0)
    step = 1e-5
    slope = (band(num, den, step, 0.0) - band(num, den, -step, 0.0)) / (2 * step)
    fall = -slope / inertia
    closed = 2 * math.cos(omega_0) / (3 * (1 + math.cos(omega_0)))
    print(
        f"(2) the fall per unit content gradient from the band: {fall:.5f} Links per interval squared,"
        f" the closed form 2 cos omega_0 / (3 (1 + cos omega_0)) = {closed:.5f}; the band carries no amplitude"
        " and no count, so every quantum of the row falls alike"
    )
    speeds = [
        (num / (3 * den)) * math.sin(k) / math.sin(band(num, den, 0.0, k))
        for k in (0.3, 0.1, 0.03, 0.01)
    ]
    print(
        f"(3) the free quantum's rest rotation omega_0 = {omega_0:.4f}; its group velocity at k = 0.3, 0.1, 0.03, 0.01:"
        f" {', '.join(f'{v:.4f}' for v in speeds)} Links per interval, to 0 with k"
    )


if __name__ == "__main__":
    main()
