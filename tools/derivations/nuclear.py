"""The pion-gap holder at the law's coupling (ALGEBRA.md L176; the paper's S.38 (b), R184): a screened Coulomb well -g e^(-r / R) / r binds an s state only for mu g R / (hbar c)^2 >= 0.840; at g = alpha hbar c, R = 1.414 fm and the reduced mass 469.5 MeV the number, the threshold and the coupling the threshold needs in units of alpha. And the nuclear holder's well under the families' reading (the paper's Section 10.3, S.45): the pair's Yukawa well V = -g^2 e^(-kappa r) / r with g^2 = 3 W omega_p sin omega_p / (4 pi Gamma) and the relative inertia mu = m* / 2 from rule3's band binds where 2 mu g^2 / kappa >= 1.6798, that is W >= (1.6798 x 4 pi / 9) Gamma kappa / omega_p^3 = 2.35 Gamma kappa / omega_p^3 at a small gap, 1,182 in the implementation's units ([2, 3] as the nucleon, kappa = 1 / 20, Gamma = 6,000); the binding fraction at a body's size b = (lambda_s / R)^2 / 2 with the Compton length lambda_s = hbar / (m_s c); and the size law of one well, R proportional to 1 / n.

Usage: `python tools/derivations/nuclear.py` prints them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent)
)  # the folder's root, rule3.py, beside this module
import rule3  # noqa: E402

HBAR_C = 197.327  # MeV fm
ALPHA = 1 / 137.036
THRESHOLD = 0.840  # the screened Coulomb well's first bound state, in mu g R / (hbar c)^2
RANGE_FM, REDUCED_MASS_MEV = 1.414, 469.46  # the proton-neutron reduced mass m_p m_n / (m_p + m_n)
YUKAWA_THRESHOLD = 1.6798  # the slow limit's own equation binds in -g^2 e^(-kappa r) / r iff 2 mu g^2 / kappa >= this (mathematics; S.45)
PROTON_MASS_MEV = 938.272  # nature's proton mass, the Compton length's input
NUCLEAR_RADII_FM = {
    "proton": 0.84,
    "deuteron": 2.13,
    "iron": 3.75,
}  # nature's radii the estimate is read at (S.45 (b))
IRON_OVER_DEUTERON_QUANTA = 56 / 2  # iron-56's nucleons over the deuteron's


def nuclear_well_threshold(
    num: int = 2, den: int = 3, gamma: int = 6000, range_links: float = 20.0
) -> list[float]:
    """S.45 (a): [the threshold's coefficient 1.6798 x 4 pi / 9, 2.35, the small-gap form W >= 2.35 Gamma kappa / omega_p^3; W at the threshold with the exact inertia mu = m* / 2 = 1.5 tan omega_p and g^2 = 3 W omega_p sin omega_p / (4 pi Gamma), [2, 3] as the nucleon, kappa = 1 / 20 and Gamma = 6,000; the small-gap form's number there]: 2.35, about 1,182 and 1,183."""
    omega_p = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
    kappa = 1 / range_links
    coefficient = YUKAWA_THRESHOLD * 4 * math.pi / 9
    inertia = 3 * math.tan(omega_p) / 2  # mu = m* / 2, the band's inertia 3 tan omega_p (S.22)
    exact = (
        YUKAWA_THRESHOLD * kappa * 4 * math.pi * gamma / (2 * inertia * 3 * omega_p * math.sin(omega_p))
    )
    return [coefficient, exact, coefficient * gamma * kappa / omega_p**3]


def binding_at_a_size() -> list[float]:
    """S.45 (b) and (e): b = (lambda_s / R)^2 / 2 with lambda_p = hbar c / (m_p c^2), [the proton at 0.84 fm, the deuteron at 2.13 fm, iron at 3.75 fm]: 3.1 x 10^-2, 4.9 x 10^-3 and 1.6 x 10^-3; one well's size law R proportional to 1 / n and b to n^2, [iron over the deuteron: 28 times smaller, 784 times harder bound]."""
    compton = HBAR_C / PROTON_MASS_MEV
    fractions = [(compton / radius) ** 2 / 2 for radius in NUCLEAR_RADII_FM.values()]
    return [*fractions, IRON_OVER_DEUTERON_QUANTA, IRON_OVER_DEUTERON_QUANTA**2]


def findings() -> list[float]:
    """S.45's findings in one list: the threshold's coefficient and W at the threshold (small-gap form), then the binding fractions and the size law of `binding_at_a_size`: [2.35, about 1,183, 3.1 x 10^-2, 4.9 x 10^-3, 1.6 x 10^-3, 28, 784]."""
    coefficient, _, small_gap = nuclear_well_threshold()
    return [coefficient, small_gap, *binding_at_a_size()]


def yukawa_threshold() -> list[float]:
    """[mu g R / (hbar c)^2 at g = alpha hbar c, the threshold, the coupling needed over alpha, the well's depth at r = R in MeV]."""
    number = REDUCED_MASS_MEV * ALPHA * RANGE_FM / HBAR_C
    needed = THRESHOLD * HBAR_C / (REDUCED_MASS_MEV * RANGE_FM)
    depth = ALPHA * HBAR_C * 2.718281828459045**-1 / RANGE_FM
    return [number, THRESHOLD, needed / ALPHA, depth]


if __name__ == "__main__":
    print("mu g R, threshold, needed / alpha, depth:", [round(v, 4) for v in yukawa_threshold()])
    print(
        "the nuclear well's 2.35, W at the threshold, the small-gap form:",
        [round(v, 3) for v in nuclear_well_threshold()],
    )
    print("the binding at a size and the size law:", binding_at_a_size())
