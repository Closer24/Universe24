"""The simple cubic lattice's Green's function on an axis, the law's kernel row 3 G(r) (ALGEBRA.md, The lattice constants): the differences G(0) - G(r) from the periodic Green's function of a box of 128 Nodes by one Fourier transform (the images' leading terms cancel, the remaining term 2 x 10^-6 at r = 5 and below 10^-6 at r <= 3, 4 pi r G(r) at r = 5 reading 1.01179 against 1.01166 from a box of 512, harmless at the printed 1.012), anchored at Watson's G(0) = 0.2527310098 for the infinite lattice, with 3 G(0) - 3 G(1) = 1 / 2 exactly as the check.

Usage: `python tools/derivations/greens_function.py` prints 3 G(r) at r = 0 to 5 and 4 pi r G(r) at r = 1 to 5.
"""

from __future__ import annotations

import numpy as np

WATSON = 0.2527310098  # G(0) of the simple cubic lattice, Watson's integral over (2 pi)^3
BOX = 128


def green(reach: int = 5, box: int = BOX) -> list[float]:
    """G(r) at r = 0 to `reach` along an axis."""
    cosine = np.cos(2 * np.pi * np.fft.fftfreq(box))
    denominator = 6 - 2 * (cosine[:, None, None] + cosine[None, :, None] + cosine[None, None, :])
    denominator[0, 0, 0] = np.inf  # the uniform mode, the periodic function's free constant
    periodic = np.fft.ifftn(1 / denominator).real
    return [WATSON - float(periodic[0, 0, 0] - periodic[r, 0, 0]) for r in range(reach + 1)]


def three_g() -> list[float]:
    """3 G(r) at r = 0 to 5, the kernel row of the law."""
    return [3 * g for g in green()]


def four_pi_r_g() -> list[float]:
    """4 pi r G(r) at r = 1 to 5, the approach to the continuum's 1."""
    return [4 * np.pi * r * g for r, g in enumerate(green()) if r]


if __name__ == "__main__":
    print("3 G(r), r = 0..5:", [round(v, 5) for v in three_g()])
    print("4 pi r G(r), r = 1..5:", [round(v, 5) for v in four_pi_r_g()])
