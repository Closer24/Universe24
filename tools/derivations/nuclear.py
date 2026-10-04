"""The pion-gap holder at the law's coupling (ALGEBRA.md L176; the paper's S.38 (b), R184): a screened Coulomb well -g e^(-r / R) / r binds an s state only for mu g R / (hbar c)^2 >= 0.840; at g = alpha hbar c, R = 1.414 fm and the reduced mass 469.5 MeV the number, the threshold and the coupling the threshold needs in units of alpha. And the nuclear holder's well under the families' reading (the paper's Section 10.3, S.45 (a)): the pair's Yukawa well V = -g^2 e^(-kappa r) / r with g^2 = 3 W omega_p sin omega_p / (4 pi Gamma) binds where 2 mu g^2 / kappa >= 1.6798, that is W >= 1.6798 x 4 pi Gamma kappa / (6 mu omega_p sin omega_p); the law's reading of mu is m* = 3 tan omega_p, each record at its own inertia about the pinned centre, a Node holding no joint amplitude of two records (postulate 2; ALGEBRA.md, the reduced mass unsupported), so W >= 1.17 Gamma kappa / omega_p^3 at a small gap, 591 in the implementation's units ([2, 3] as the nucleon, kappa = 1 / 20, Gamma = 6,000) and 502 by the exact inertia; under the pair hypothesis alone (The pair of two bound records, a line under its own name; two_body.py) the relative part carries mu = m* / 2 and the threshold doubles, 2.35 Gamma kappa / omega_p^3, 1,183 and 1,004; the binding fraction at a body's size b = (lambda_s / R)^2 / 2 with the Compton length lambda_s = hbar / (m_s c); and the size law of one well, R proportional to 1 / n.

Usage: `python tools/derivations/nuclear.py` prints them.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
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
    """S.45 (a): the Yukawa well -g^2 e^(-kappa r) / r with g^2 = 3 W omega_p sin omega_p / (4 pi Gamma) binds where 2 mu g^2 / kappa >= 1.6798, so W >= 1.6798 x 4 pi Gamma kappa / (6 mu omega_p sin omega_p), omega_p the pair's rest rotation from rule3's band and m* = 3 tan omega_p its inertia. The law's reading first: mu = m*, each record at its own inertia about the pinned centre, no joint amplitude of two records at a Node (postulate 2), [the small-gap coefficient 1.6798 x 4 pi / 18 with m* = 3 omega_p and sin omega_p = omega_p, 1.17; W >= 1.17 Gamma kappa / omega_p^3 at [2, 3], kappa = 1 / 20, Gamma = 6,000, 591; W by the exact m* and sin omega_p, 502]; the pair hypothesis' beside it, the relative part at mu = m* / 2 (The pair of two bound records, a line under its own name), [its coefficient 1.6798 x 4 pi / 9, 2.35; its small-gap W, 1,183; its exact W, 1,004]."""
    omega_p = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
    kappa = 1 / range_links
    inertia = 3 * math.tan(omega_p)  # m*, the band's inertia 3 tan omega_p (S.22)
    found = []
    for mu_over_inertia in (1, Fraction(1, 2)):  # the law's mu = m*, then the pair hypothesis' m* / 2
        mu = inertia * mu_over_inertia
        coefficient = YUKAWA_THRESHOLD * 4 * math.pi / (18 * mu_over_inertia)
        exact = YUKAWA_THRESHOLD * kappa * 4 * math.pi * gamma / (6 * mu * omega_p * math.sin(omega_p))
        found += [coefficient, coefficient * gamma * kappa / omega_p**3, exact]
    return found


def binding_at_a_size() -> list[float]:
    """S.45 (b) and (e): b = (lambda_s / R)^2 / 2 with lambda_p = hbar c / (m_p c^2), [the proton at 0.84 fm, the deuteron at 2.13 fm, iron at 3.75 fm]: 3.1 x 10^-2, 4.9 x 10^-3 and 1.6 x 10^-3; one well's size law R proportional to 1 / n and b to n^2, [iron over the deuteron: 28 times smaller, 784 times harder bound]."""
    compton = HBAR_C / PROTON_MASS_MEV
    fractions = [(compton / radius) ** 2 / 2 for radius in NUCLEAR_RADII_FM.values()]
    return [*fractions, IRON_OVER_DEUTERON_QUANTA, IRON_OVER_DEUTERON_QUANTA**2]


def findings() -> list[float]:
    """S.45's findings in one list: W at the threshold under the law's reading, mu = m*, by the small-gap formula and by the exact inertia, then under the pair hypothesis, mu = m* / 2, the same two ways, then the binding fractions and the size law of `binding_at_a_size`: [591, 502, 1,183, 1,004, 3.1 x 10^-2, 4.9 x 10^-3, 1.6 x 10^-3, 28, 784]."""
    _, law_small_gap, law_exact, _, pair_small_gap, pair_exact = nuclear_well_threshold()
    return [law_small_gap, law_exact, pair_small_gap, pair_exact, *binding_at_a_size()]


def yukawa_threshold() -> list[float]:
    """[mu g R / (hbar c)^2 at g = alpha hbar c, the threshold, the coupling needed over alpha, the well's depth at r = R in MeV]."""
    number = REDUCED_MASS_MEV * ALPHA * RANGE_FM / HBAR_C
    needed = THRESHOLD * HBAR_C / (REDUCED_MASS_MEV * RANGE_FM)
    depth = ALPHA * HBAR_C * 2.718281828459045**-1 / RANGE_FM
    return [number, THRESHOLD, needed / ALPHA, depth]


if __name__ == "__main__":
    print("mu g R, threshold, needed / alpha, depth:", [round(v, 4) for v in yukawa_threshold()])
    print(
        "the nuclear well: the law's 1.17, 591, 502, then the pair hypothesis' 2.35, 1,183, 1,004:",
        [round(v, 3) for v in nuclear_well_threshold()],
    )
    print("the binding at a size and the size law:", binding_at_a_size())
