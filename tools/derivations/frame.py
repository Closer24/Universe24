"""The lattice's frame (docs/ALGEBRA.md, what is open, item 15, "the lattice's frame is read by gravity alone"; the paper's Section 10.3, S.35 and S.36): the band at the composed paces of rule3 is even in every k_a and its three Link paces are one number, so a static source's metric is diagonal in the lattice's frame, g_0a = 0 and no g_ab off the diagonal; the parametrised post-Newtonian metric then has 4 gamma + 4 + alpha_1 = 0, alpha_1 = -8 at gamma = 1, alpha_2 = -1 in the standard gauge, and a gyroscope's frame-dragging precession (4 gamma + 4 + alpha_1) / 8 of general relativity's, 0 (Gravity Probe B's 37.2 +/- 7.2 milliarcseconds per year against general relativity's 39.2 stand beside it as nature's numbers, named); the boosted static metric would carry g_0i = -4 U v_i; and of the five forms tried for a carrier, the one-sided real mixed term's complex rotation and the staggered clock's redshift 5 / 3, S.36's checks from rule3's coefficients.

Usage: `python tools/derivations/frame.py` prints them.
"""

from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent)
)  # the folder's root, rule3.py, beside this module
import rule3  # noqa: E402

PPN_GAMMA = 1.0  # the model's gamma under the composed paces, S.19 in U
GAMMA = 6000  # the engine's Gamma of the paper's worlds
GRAVITY_PROBE_B_MAS_PER_YEAR = (37.2, 7.2)  # nature's measurement (Everitt), a comparison
GENERAL_RELATIVITY_MAS_PER_YEAR = (
    39.2  # general relativity's prediction for Gravity Probe B, a comparison
)
PULSAR_ALPHA_1_BOUND = 4e-5  # nature's |alpha_1| from PSR J1738+0333 (Shao and Wex)


def preferred_frame_parameters(
    gamma_ppn: float = PPN_GAMMA, zeta_1: float = 0.0, xi: float = 0.0
) -> list[float]:
    """S.35: a metric with g_0j = 0 in its preferred frame has both g_0j coefficients of the parametrised post-Newtonian metric 0, the V_j coefficient (4 gamma + 3 + alpha_1 - alpha_2 + zeta_1 - 2 xi) / 2 and the W_j coefficient (1 + alpha_2 - zeta_1 + 2 xi) / 2 (Will's form), so the gauge-invariant sum 4 gamma + 4 + alpha_1 vanishes: [alpha_1 from the first, -4 (1 + gamma) at the standard gauge zeta_1 = xi = 0, -8 at gamma = 1; alpha_2 from the second, -1; the invariant sum, 0]."""
    alpha_2 = -(1 - zeta_1 + 2 * xi)  # the W_j coefficient vanishing
    alpha_1 = -(4 * gamma_ppn + 3 - alpha_2 + zeta_1 - 2 * xi)  # the V_j coefficient vanishing
    return [alpha_1, alpha_2, 4 * gamma_ppn + 4 + alpha_1]


def frame_dragging(gamma_ppn: float = PPN_GAMMA) -> list[float]:
    """S.35 (c): a gyroscope's frame-dragging precession is (4 gamma + 4 + alpha_1) / 8 of general relativity's Lense-Thirring value: [the law's fraction at alpha_1 = -4 (1 + gamma), 0; general relativity's at alpha_1 = 0, 1]; Gravity Probe B's 37.2 +/- 7.2 milliarcseconds per year against general relativity's 39.2 are the constants beside it."""
    alpha_1 = preferred_frame_parameters(gamma_ppn)[0]
    return [(4 * gamma_ppn + 4 + alpha_1) / 8, (4 * gamma_ppn + 4) / 8]


def boosted_cross_term(share: float = 1e-4) -> list[float]:
    """S.35 (d): had the read been covariant, the boost of N^2 = e^(-2U), h^2 = e^(2U) would give g_0i = gamma^2 v_i (N^2 - h^2), [(N^2 - h^2) / U at first order]: -4.000, Einstein's, which the diagonal read in the lattice's frame removes."""
    return [(math.exp(-2 * share) - math.exp(2 * share)) / share]


def no_cross_terms(
    num: int = 2, den: int = 3, gamma: int = GAMMA, content: int = 300, k: float = 0.3
) -> list[float]:
    """The content's Poisson rest in the lattice's frame gives a moving mass no g_0a and no g_ab: at the composed paces, clock Gamma N and Link paces Gamma N^2, rule3's band is even in every k_a, [cos omega(k) - cos omega(-k) along each axis, 0, the term odd in time and space together absent], and the three Link paces are one number, [the spread of the Link paces, 0, no anisotropic g_ab]."""
    clock = float(rule3.clock_pace(gamma, content))
    links = (float(rule3.node_pace(clock, gamma)),) * 3
    odd = max(
        abs(
            rule3.dispersion_at_paces(
                tuple(k if a == axis else 0.0 for a in range(3)), num, den, gamma, clock, links
            )
            - rule3.dispersion_at_paces(
                tuple(-k if a == axis else 0.0 for a in range(3)), num, den, gamma, clock, links
            )
        )
        for axis in range(3)
    )
    return [odd, max(links) - min(links)]


def five_forms(
    gamma: int = GAMMA, k: float = 0.3, mixed_over_wall: float = 1e-2, n_factor: float = 0.9
) -> list[float]:
    """S.36: (i) the one-sided real mixed term C [(a_+ - a_-)_now - (a_+ - a_-)_before] added to light's line gives 2 w cos omega = S + 2 SUM_a R_a cos k_a + 2 i C sin k (1 - e^(i omega)), solved for the complex omega by Newton from the band's omega, with w, R and S rule3's coefficients at Gamma = 6,000: [Re omega, Im omega, the band's omega] = [0.16984, -2.47 x 10^-4, 0.17277] at k = 0.3 and C / w = 10^-2, the imaginary part a growth or decay that breaks the form; (v) the staggered clock: S.36 (v)'s closed forms written in and not derived here, the rest rotation in a content omega / omega_0 = N sqrt(3 / (4 - N^4)) at nu -> 1 and its first order N (1 - 2 U / 3), a clock in a well at omega_0 (1 - 5 U / 3); [sqrt(3 / (4 - N^4)) at N = 0.9, S.36's check, 0.9472; the redshift's factor 5 / 3]."""
    wall, reads, self_coefficient = rule3.coefficients(1, 1, gamma)
    mixed = mixed_over_wall * wall
    right_fixed = self_coefficient + 2 * reads[0] * math.cos(k) + 2 * reads[1] + 2 * reads[2]

    def residual(omega: complex) -> complex:
        return (
            2 * wall * cmath.cos(omega)
            - right_fixed
            - 2j * mixed * math.sin(k) * (1 - cmath.exp(1j * omega))
        )

    def slope(omega: complex) -> complex:
        return -2 * wall * cmath.sin(omega) - 2 * mixed * math.sin(k) * cmath.exp(1j * omega)

    band = math.acos(rule3.plane_wave_dispersion(k, 1, 1))
    omega = complex(band, 0.0)
    for _ in range(50):
        omega -= residual(omega) / slope(omega)
    return [omega.real, omega.imag, band, math.sqrt(3 / (4 - n_factor**4)), 5 / 3]


if __name__ == "__main__":
    print("alpha_1, alpha_2, the invariant sum:", preferred_frame_parameters())
    print("the frame dragging, the law's and general relativity's fractions:", frame_dragging())
    print("the boosted cross term's coefficient:", [round(v, 4) for v in boosted_cross_term()])
    print("the odd part of the band and the Link paces' spread:", no_cross_terms())
    print(
        "the five forms: Re omega, Im omega, the band, the staggered clock's 0.9472, 5 / 3:",
        five_forms(),
    )
