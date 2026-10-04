"""The atom in the slow limit of Rule3's band (docs/ALGEBRA.md, "the atom is a bound body of the holder of the sign"; the paper's Section 7.3 and S.46): the band's inertia m* = 1 / omega''(0) = 3 tan omega_0 from rule3's band, light's c = 1 / sqrt 3; with the nucleus's angle Z alpha c / r alone the levels are Bohr's, E_n = -m* (Z alpha)^2 c^2 / (2 n^2) with a_0 = 1 / (m* Z alpha c) = sqrt 3 / (m* Z alpha); the orbital Zeeman splitting Phi m_l / (2 m*) has g = 1 because the Peierls phase shifts the kinetic term by its group velocity, k / m*; and a nuclear holder the electron reads is excluded by the finite-size shift of hydrogen's 1S, (2 / 3) alpha^4 m_e c^2 (r_p / lambda_e)^2, 1.1 MHz, 500 times its 2.2 kHz uncertainty, and by muonic hydrogen's 5.2275 r_p^2 meV, 5.2 meV at 1 fm against the 0.09 to 0.15 meV agreement of the radii, 35 to 58 times. The numbers of nature stand as named constants where the exclusion is a comparison.

Usage: `python tools/derivations/atom.py` prints them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent)
)  # the folder's root, rule3.py, beside this module
import rule3  # noqa: E402

LIGHT_SPEED = 1 / math.sqrt(3)  # Link per interval (The lattice constants)
FINE_STRUCTURE = 1 / 137.036  # nature's alpha, the comparison's coupling
ELECTRON_REST_EV = 510_998.95  # nature's electron rest energy
ELECTRON_COMPTON_FM = 386.159  # nature's reduced Compton wavelength of the electron, fm
PROTON_RADIUS_FM = 0.8414  # nature's proton charge radius (CODATA 2018)
PLANCK_EV_S = 4.135_667_696e-15  # h in eV s
HYDROGEN_1S_UNCERTAINTY_KHZ = 2.2  # nature's uncertainty of hydrogen's 1S level
MUONIC_COEFFICIENT_MEV_PER_FM2 = (
    5.2275  # the measured Lamb shift's finite-size coefficient, meV per fm^2
)
RADII_AGREEMENT_MEV = (
    0.15,
    0.09,
)  # the electronic and muonic radii agree to this in the Lamb shift, meV


def inertia(num: int = 2, den: int = 3, step: float = 1e-3) -> list[float]:
    """[m* = 1 / omega''(0) from rule3's band along an axis; 3 tan omega_0, S.22's closed form]: 3.354 twice at [2, 3]."""
    omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
    curvature = 2 * (math.acos(rule3.plane_wave_dispersion(step, num, den)) - omega_0) / (step * step)
    return [1 / curvature, 3 * math.tan(omega_0)]


def bohr_levels(
    num: int = 2, den: int = 3, charge: int = 1, alpha: float = FINE_STRUCTURE
) -> list[float]:
    """S.46 (a): E_n = -m* (Z alpha)^2 c^2 / (2 n^2) and a_0 = 1 / (m* Z alpha c): [E_1 / E_1, E_2 / E_1, E_3 / E_1, the 1 / n^2 form; a_0 m* Z alpha, which is sqrt 3, the paper's a_0 = sqrt 3 / (m* Z alpha)]: 1, 0.25, 0.1111 and 1.7321."""
    m_star = inertia(num, den)[0]
    levels = [-m_star * (charge * alpha) ** 2 * LIGHT_SPEED**2 / (2 * n * n) for n in (1, 2, 3)]
    radius = 1 / (m_star * charge * alpha * LIGHT_SPEED)
    return [*(level / levels[0] for level in levels), radius * m_star * charge * alpha]


def orbital_zeeman_g(num: int = 2, den: int = 3, k: float = 0.005, phase: float = 1e-4) -> list[float]:
    """S.46 (b): under S.33's covector the Peierls phase A shifts a plane record's rotation by [omega(k + A) - omega(k - A)] / (2 A) = omega'(k) = k / m* at small k, so a flux Phi splits the orbital levels by Phi m_l / (2 m*), one Bohr magneton 1 / (2 m*) per unit of angular momentum: [the shift's coefficient m* omega'(k) / k, 1; the orbital g, the splitting per m_l over the magneton, 1]."""
    m_star = inertia(num, den)[0]
    shift = (
        math.acos(rule3.plane_wave_dispersion(k + phase, num, den))
        - math.acos(rule3.plane_wave_dispersion(k - phase, num, den))
    ) / (2 * phase)
    coefficient = m_star * shift / k
    return [coefficient, coefficient * (1 / (2 * m_star)) / (1 / (2 * m_star))]


def nuclear_holder_shift() -> list[float]:
    """S.46 (d): a one-Node proton the electron reads lacks the finite-size part of hydrogen's 1S, the slow limit's own perturbation (2 / 3) alpha^4 m_e c^2 (r_p / lambda_e)^2: [the shift in MHz, 1.1; over the level's 2.2 kHz uncertainty, 500]; a 1 fm cloud by muonic hydrogen's coefficient: [5.2275 r_p^2 meV at 1 fm, 5.2; over the radii's agreement of 0.15 and 0.09 meV, 35 and 58]."""
    shift_ev = (
        2 / 3 * FINE_STRUCTURE**4 * ELECTRON_REST_EV * (PROTON_RADIUS_FM / ELECTRON_COMPTON_FM) ** 2
    )
    shift_mhz = shift_ev / PLANCK_EV_S / 1e6
    muonic = MUONIC_COEFFICIENT_MEV_PER_FM2 * 1.0**2
    return [
        shift_mhz,
        shift_mhz * 1e3 / HYDROGEN_1S_UNCERTAINTY_KHZ,
        muonic,
        *(muonic / agreement for agreement in RADII_AGREEMENT_MEV),
    ]


if __name__ == "__main__":
    print("m* from the band and 3 tan omega_0:", [round(v, 4) for v in inertia()])
    print("Bohr's levels over E_1 and a_0 m* Z alpha:", [round(v, 4) for v in bohr_levels()])
    print("the orbital shift's coefficient and g:", [round(v, 4) for v in orbital_zeeman_g()])
    print(
        "the nuclear holder's shift: MHz, over 2.2 kHz, meV at 1 fm, over 0.15 and 0.09:",
        [round(v, 2) for v in nuclear_holder_shift()],
    )
