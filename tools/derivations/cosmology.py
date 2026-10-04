"""The ball of dust's deceleration and the vacuum's write (ALGEBRA.md, the cosmological constant as the law's own write, a hypothesis under its own name; R186 and R48): the finite ball of dust decelerates at q_0 = Omega_m / 2 with no vacuum's write, +0.15 at Omega_m = 0.3 against nature's -0.55; with the write a shell obeys a_tt / a = -(4 pi G_K / 3) rho + Lambda_law c^2 / 3, Friedmann's dust-plus-Lambda equations for the finite ball, so q_0 = Omega_m / 2 - Omega_Lambda = -0.55 at Omega_Lambda = 0.7 and the transition from deceleration to acceleration stands at z_t = (2 Omega_Lambda / Omega_m)^(1 / 3) - 1 = 0.67; the write's rate Lambda_law = [6 cos omega_0 / (1 + cos omega_0)] |q_vac| / (E_v Gamma LW), the coefficient 3 at nature's gap and 2.4 at [2, 3]. One declared number, printed declared and never derived.

Usage: `python tools/derivations/cosmology.py` prints them.
"""

from __future__ import annotations


def deceleration(matter: float = 0.3, vacuum: float = 0.7) -> list[float]:
    """[q_0 of the ball of dust alone, Omega_m / 2; q_0 with the vacuum's write, Omega_m / 2 - Omega_Lambda] at the fitted fractions."""
    return [matter / 2, matter / 2 - vacuum]


def transition_redshift(matter: float = 0.3, vacuum: float = 0.7) -> list[float]:
    """[z_t = (2 Omega_Lambda / Omega_m)^(1 / 3) - 1], where the deceleration turns into acceleration."""
    return [(2 * vacuum / matter) ** (1 / 3) - 1]


def write_coefficient(pairs: tuple[tuple[int, int], ...] = ((1, 1), (2, 3))) -> list[float]:
    """6 cos omega_0 / (1 + cos omega_0), the factor of Lambda_law on |q_vac| / (E_v Gamma LW), per pair: 3 at nature's gap (cos omega_0 to 1) and 2.4 at [2, 3]."""
    return [6 * (num / den) / (1 + num / den) for num, den in pairs]


if __name__ == "__main__":
    print("q_0 without and with the vacuum's write:", [round(v, 3) for v in deceleration()])
    print("z_t:", [round(v, 3) for v in transition_redshift()])
    print(
        "6 cos omega_0 / (1 + cos omega_0) at [1, 1] and [2, 3]:",
        [round(v, 2) for v in write_coefficient()],
    )
