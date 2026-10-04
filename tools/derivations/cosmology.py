"""The ball of dust's deceleration and the vacuum's write (ALGEBRA.md, the cosmological constant as the law's own write, a hypothesis under its own name; R186 and R48): the finite ball of dust decelerates at q_0 = Omega_m / 2 with no vacuum's write, +0.15 at Omega_m = 0.3 against nature's -0.55; with the write a shell obeys a_tt / a = -(4 pi G_K / 3) rho + Lambda_law c^2 / 3, Friedmann's dust-plus-Lambda equations for the finite ball, so q_0 = Omega_m / 2 - Omega_Lambda = -0.55 at Omega_Lambda = 0.7 and the transition from deceleration to acceleration stands at z_t = (2 Omega_Lambda / Omega_m)^(1 / 3) - 1 = 0.67; the write's rate Lambda_law = [6 cos omega_0 / (1 + cos omega_0)] |q_vac| / (E_v Gamma LW), the coefficient 3 at nature's gap and 2.4 at [2, 3]. One declared number, printed declared and never derived.

And the redshift's two derivations (the paper's Section 7.5, S.29): the Doppler period of a receding source, (1 + beta) at the resting NodeReader (row (m)), times the source's own tick on rule3's band at the small gap, Lorentz's 1 / sqrt(1 - beta^2) at c_m -> c (row (e)), is sqrt((1 + beta) / (1 - beta)), nature's relativistic Doppler form, 1 + beta + beta^2 / 2 + ... to the second order.

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
    tick = (omega - low * rule3.group_velocity(low, num, den)) / omega_0
    doppler = (1 + beta) / tick
    relativistic = math.sqrt((1 + beta) / (1 - beta))
    return [doppler, relativistic, doppler - relativistic, (relativistic - 1 - beta) / beta**2]


def deceleration(matter: float = 0.3, vacuum: float = 0.7) -> list[float]:
    """[q_0 of the ball of dust alone, Omega_m / 2; q_0 with the vacuum's write, Omega_m / 2 - Omega_Lambda] at Omega_m = 0.3 and Omega_Lambda = 0.7, nature's fitted fractions (flat Lambda-CDM's), the comparison column and no number of the law."""
    return [matter / 2, matter / 2 - vacuum]


def transition_redshift(matter: float = 0.3, vacuum: float = 0.7) -> list[float]:
    """[z_t = (2 Omega_Lambda / Omega_m)^(1 / 3) - 1], where the deceleration turns into acceleration."""
    return [(2 * vacuum / matter) ** (1 / 3) - 1]


def write_coefficient(pairs: tuple[tuple[int, int], ...] = ((1, 1), (2, 3))) -> list[float]:
    """6 cos omega_0 / (1 + cos omega_0), the factor of Lambda_law on |q_vac| / (E_v Gamma LW), per pair: 3 at nature's gap (cos omega_0 to 1) and 2.4 at [2, 3]."""
    return [6 * (num / den) / (1 + num / den) for num, den in pairs]


if __name__ == "__main__":
    print(
        "the Doppler period times the moving clock, the relativistic form, their difference, the second order:",
        doppler_times_moving_clock(),
    )
    print("q_0 without and with the vacuum's write:", [round(v, 3) for v in deceleration()])
    print("z_t:", [round(v, 3) for v in transition_redshift()])
    print(
        "6 cos omega_0 / (1 + cos omega_0) at [1, 1] and [2, 3]:",
        [round(v, 2) for v in write_coefficient()],
    )
