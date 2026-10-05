"""The ball of dust's deceleration and the Doppler period times the moving clock (ALGEBRA.md, The clusters' cosmology; R186 and R48): a finite ball of dust flying through the static lattice, every body pulled by the others' 1 / r^2 at Kepler's G_K, obeys Friedmann's dust equations for its interior and decelerates either way, bound or free, q_0 = Omega_m / 2, +0.15 at nature's fitted Omega_m = 0.3 against nature's -0.55, a finding against nature by name with no mend; the law's lines have no repulsive sector.

And the redshift's two derivations (the paper's Section 7.5, S.29): the Doppler period of a receding source, (1 + beta) at the resting NodeDetector (row (m)), times the source's own interval on rule3's band at the small gap, Lorentz's 1 / sqrt(1 - beta^2) at c_m -> c (row (e)), is sqrt((1 + beta) / (1 - beta)), nature's relativistic Doppler form, 1 + beta + beta^2 / 2 + ... to the second order.

Usage: `python tools/derivations/cosmology.py` prints them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent)
)  # the folder's root, rule3.py, beside this module
import rule3  # noqa: E402


def doppler_times_moving_clock(
    beta: float = 0.01, num: int = 999_999, den: int = 1_000_000
) -> list[float]:
    """S.29, the redshift: [1 + z as the Doppler period (1 + beta) times the moving clock 1 / f, f = Omega(k) / omega_0 on rule3's band at a small gap where c_m = c, at the group velocity beta c; the relativistic Doppler form sqrt((1 + beta) / (1 - beta)); their difference, 0 to the band's own corrections; the second order's coefficient (1 + z - 1 - beta) / beta^2, 1 / 2]."""
    omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
    speed = beta / math.sqrt(3)
    low, high = 0.0, math.pi / 2
    for _ in range(200):  # invert the group velocity on the band's rising side
        mid = (low + high) / 2
        low, high = (mid, high) if rule3.group_velocity(mid, num, den) < speed else (low, mid)
    omega = math.acos(rule3.plane_wave_dispersion(low, num, den))
    interval = (omega - low * rule3.group_velocity(low, num, den)) / omega_0
    doppler = (1 + beta) / interval
    relativistic = math.sqrt((1 + beta) / (1 - beta))
    return [doppler, relativistic, doppler - relativistic, (relativistic - 1 - beta) / beta**2]


def deceleration(matter: float = 0.3) -> list[float]:
    """[q_0 of the ball of dust, Omega_m / 2] at Omega_m = 0.3, nature's fitted fraction (flat Lambda-CDM's) as the input, the comparison column and no number of the law."""
    return [matter / 2]


if __name__ == "__main__":
    print(
        "the Doppler period times the moving clock, the relativistic form, their difference, the second order:",
        doppler_times_moving_clock(),
    )
    print("q_0 = Omega_m / 2 at Omega_m = 0.3:", [round(v, 3) for v in deceleration()])
