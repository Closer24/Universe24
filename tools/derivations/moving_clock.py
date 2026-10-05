"""The moving clock from Rule3's exact band (docs/ALGEBRA.md, The rows against nature, row (e); the paper's Section 8 (e), Fig. 3 and S.21): the interval's factor f = Omega(k) / omega_0 with Omega(k) = omega(k) - k omega'(k) the rotation at the moving centre, on the free record's band cos omega = (num / (3 den)) (2 + cos k) of rule3; the kinetic scale c_m^2 = omega_0 / (3 tan omega_0), the fourth-order coefficient over Lorentz's omega_0 [(SUM_a n_a^4) tan omega_0 + cot omega_0], the largest group speeds, and the differences of c_m and the diagonal's speed from light's at nature's gap, read from the electron's gap bound sin omega_e <= m_e c^2 / E_LHAASO (The constants) and S.24's axis bound. The numbers of nature stand as named constants where the mark rests on them.

Usage: `python tools/derivations/moving_clock.py` prints them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent)
)  # the folder's root, rule3.py, beside this module
import rule3  # noqa: E402

COMPUTED_PAIR = (2, 3)  # the rule's own matter pair, the paper's computed pair
SMALL_GAP_PAIR = (999, 1000)  # the paper's small-gap illustration (Fig. 3)
LIGHT_SPEED_SQUARED = 1 / 3  # c^2 = 1 / 3 (The lattice constants; rule3.group_velocity as k -> 0)
ELECTRON_MASS_MEV = 0.511  # nature's electron rest energy
LHAASO_PHOTON_PEV = (
    1.4  # nature's: LHAASO's 1.4 PeV photons arrived (The constants, the share's ceiling)
)
OMEGA_E_MAGIC_AXIS = 2.0e-14  # the electron's gap at the MAGIC bound along an axis (S.24)
CRAB_SUBLUMINAL_BOUND = 6e-20  # nature's bound on matter's limiting speed below light's (Altschul)
# the unit vectors where the group velocity is parallel to k, with SUM_a n_a^4
DIRECTIONS = {"axis": 1.0, "face diagonal": 1 / 2, "body diagonal": 1 / 3}


def rest_rotation(num: int, den: int) -> float:
    """omega_0 = arccos(num / den), the band at k = 0 (rule3.plane_wave_dispersion)."""
    return math.acos(rule3.plane_wave_dispersion(0.0, num, den))


def rotation(k: float, num: int, den: int) -> float:
    """omega(k) along an axis, from rule3's band."""
    return math.acos(rule3.plane_wave_dispersion(k, num, den))


def interval_factor(k: float, num: int, den: int) -> tuple[float, float]:
    """(v, f) at the wave number k along an axis: the group velocity v = omega'(k) (rule3.group_velocity) and f = Omega / omega_0 with Omega = omega - k omega' (S.21)."""
    velocity = rule3.group_velocity(k, num, den)
    return velocity, (rotation(k, num, den) - k * velocity) / rest_rotation(num, den)


def kinetic_scale(num: int = 2, den: int = 3, step: float = 1e-3) -> list[float]:
    """[c_m^2 / c^2, c_m / c, the percent c_m lies below light's]: c_m^2 = omega_0 omega''(0), the band's curvature at rest times the gap (S.21, c_m^2 = omega_0 / (3 tan omega_0)): 0.752, 0.867 and 13 at [2, 3]."""
    omega_0 = rest_rotation(num, den)
    curvature = 2 * (rotation(step, num, den) - omega_0) / (step * step)
    ratio = omega_0 * curvature / LIGHT_SPEED_SQUARED
    return [ratio, math.sqrt(ratio), (1 - math.sqrt(ratio)) * 100]


def fourth_order_over_lorentz(num: int = 2, den: int = 3, speed: float = 0.02) -> list[float]:
    """S.21: the v^4 coefficient of f over Lorentz's -1 / (8 c_m^4), omega_0 [(SUM_a n_a^4) tan omega_0 + cot omega_0] along the axis, the face diagonal and the body diagonal, then the same ratio read on the exact band along the axis at v = 0.02, (f - 1 + v^2 / (2 c_m^2)) / v^4 over -1 / (8 c_m^4): 1.6926, 1.2224, 1.0657 and about 1.69 at [2, 3], 1 in every direction as the gap closes."""
    omega_0 = rest_rotation(num, den)
    analytic = [
        omega_0 * (fourth * math.tan(omega_0) + 1 / math.tan(omega_0)) for fourth in DIRECTIONS.values()
    ]
    c_m_squared = kinetic_scale(num, den)[0] * LIGHT_SPEED_SQUARED
    low, high = 0.0, 1.0
    for _ in range(100):  # invert v(k) on the band's rising side
        mid = (low + high) / 2
        low, high = (mid, high) if interval_factor(mid, num, den)[0] < speed else (low, mid)
    velocity, factor = interval_factor(low, num, den)
    residual = (factor - 1 + velocity**2 / (2 * c_m_squared)) / velocity**4
    return [*analytic, residual / (-1 / (8 * c_m_squared**2))]


def largest_group_speed(num: int = 2, den: int = 3) -> list[float]:
    """S.21: [the largest group speed along an axis on rule3's band, Link per interval; along the cube's diagonal at k = (pi / 2, pi / 2, pi / 2), c cos omega_0 = (num / den) / sqrt 3; the diagonal's as a fraction of light's, cos omega_0; sqrt 3 / 4 of light's beside the axis's]: about 0.2501, 0.3849, 2 / 3 and 0.25 at [2, 3]."""
    along_axis = max(rule3.group_velocity(i * math.pi / 20000, num, den) for i in range(1, 20000))
    light = math.sqrt(LIGHT_SPEED_SQUARED)
    return [along_axis, (num / den) * light, num / den, math.sqrt(3) / 4 * light]


def omega_e_lhaaso() -> float:
    """The electron's gap bound from LHAASO's photons: sin omega_e <= m_e c^2 / 1.4 PeV (The constants, the share's ceiling), 3.65 x 10^-10."""
    return math.asin(ELECTRON_MASS_MEV / (LHAASO_PHOTON_PEV * 1e9))


def nature_bounds() -> list[float]:
    """Row (e) at nature's matter pair: c_m below light's by omega_e^2 / 6 and the diagonal's largest group speed by 1 - cos omega_e = omega_e^2 / 2, [at the MAGIC axis bound: 7 x 10^-29 and 2.0 x 10^-28; at LHAASO's: 2.2 x 10^-20 and 6.7 x 10^-20]; then [omega_e that the Crab's subluminal bound 6 x 10^-20 = omega_e^2 / 6 binds, near 10^-10]."""
    lhaaso = omega_e_lhaaso()
    return [
        OMEGA_E_MAGIC_AXIS**2 / 6,
        OMEGA_E_MAGIC_AXIS**2 / 2,
        lhaaso**2 / 6,
        lhaaso**2 / 2,
        math.sqrt(6 * CRAB_SUBLUMINAL_BOUND),
    ]


def row_e(num: int = 2, den: int = 3) -> list[float]:
    """Row (e)'s printed numbers in their order: [the fourth order over Lorentz's along the axis, the face diagonal and the body diagonal (1.6926, 1.2224, 1.0657); c_m^2 / c^2 (0.752); the percent c_m lies below light's (13); the axis's largest group speed (0.2501); at nature's pair, c_m's and the diagonal's differences from light's at the MAGIC bound (7 x 10^-29, 2.0 x 10^-28) and at LHAASO's (2.2 x 10^-20, 6.7 x 10^-20)]."""
    scale = kinetic_scale(num, den)
    return [
        *fourth_order_over_lorentz(num, den)[:3],
        scale[0],
        scale[2],
        largest_group_speed(num, den)[0],
        *nature_bounds()[:4],
    ]


def figure(num: int = 2, den: int = 3) -> list[float]:
    """Fig. 3, drawn from the band: [the axis's largest group speed, the dot; c_m / c; f at that speed on the exact band; Lorentz's sqrt(1 - v^2 / c_m^2) there]: about 0.2501, 0.867, and the two factors the curve and the grey line reach at the dot."""
    top = largest_group_speed(num, den)[0]
    c_m = kinetic_scale(num, den)[1] * math.sqrt(LIGHT_SPEED_SQUARED)
    k_top = max(
        (i * math.pi / 20000 for i in range(1, 20000)), key=lambda k: rule3.group_velocity(k, num, den)
    )
    return [
        top,
        kinetic_scale(num, den)[1],
        interval_factor(k_top, num, den)[1],
        math.sqrt(1 - top**2 / c_m**2),
    ]


def lorentz_form(
    num: int = 999, den: int = 1000, gamma: int = 6000, content: float = 300.0, k: float = 1e-2
) -> list[float]:
    """The lattice's frame (the paper's Section 10.3, S.21, S.34 (c)): at long wavelength and small gap the band at the composed paces, clock Gamma N and Link pace Gamma N^2 with N = e^(-U) (rule3.dispersion_at_paces), gives omega^2 = omega_0^2 N^2 + c_m^2 k^2 N^4: [the k^2 term's coefficient over c_m^2, which is N^4; the same over c_m^2 N^4, 1; the printed form's residual (omega^2 - omega_0^2 N^2 - c_m^2 k^2) over c_m^2 k^2, which is N^4 - 1 and 0 at N = 1 alone]."""
    share = -content * math.log(1 - 1 / gamma)
    n_factor = math.exp(-share)
    clock, link = gamma * n_factor, gamma * n_factor**2

    def omega_squared(wave: float) -> float:
        return (
            math.acos(rule3.dispersion_at_paces((wave, 0.0, 0.0), num, den, gamma, clock, (link,) * 3))
            ** 2
        )

    c_m_squared = kinetic_scale(num, den)[0] * LIGHT_SPEED_SQUARED
    coefficient = (omega_squared(k) - omega_squared(0.0)) / (k * k)
    return [
        coefficient / c_m_squared,
        coefficient / (c_m_squared * n_factor**4),
        coefficient / c_m_squared - 1,
    ]


if __name__ == "__main__":
    print("c_m^2 / c^2, c_m / c, percent below light at [2, 3]:", [round(v, 4) for v in kinetic_scale()])
    print(
        "the fourth order over Lorentz's, axis, face, body, exact band:",
        [round(v, 4) for v in fourth_order_over_lorentz()],
    )
    print("the largest group speeds:", [round(v, 4) for v in largest_group_speed()])
    print("omega_e at LHAASO:", omega_e_lhaaso())
    print("nature's bounds, MAGIC x 2, LHAASO x 2, the Crab's omega_e:", nature_bounds())
    print("the figure's dot, c_m / c, f and Lorentz's at the dot:", [round(v, 4) for v in figure()])
    print(
        "the Lorentz form at a content: the k^2 coefficient over c_m^2, over c_m^2 N^4, the printed form's residual:",
        [round(v, 4) for v in lorentz_form()],
    )
