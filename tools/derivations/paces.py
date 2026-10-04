"""Numbers of the composed paces (ALGEBRA.md, The paces compose): the clock p_0 = Gamma (1 - 1 / Gamma)^c and the Node's pace p_0^2 / Gamma; the not-conformal pair at c = 3,000 of 12,000 on [2, 3] (R168); the quadratic clock against the composition at U = 0.10 (R169 (h)); the total mirror's thresholds at Gamma = 10^4 for lambda = 4 and 4.78 Links (R46 with R68); a drifting Gamma's deceleration from the law's own H (R186); the band's curvature at rest and Newton's coefficient at [2, 3] (R179); the frozen content (Gamma / 2) ln 2 Gamma.

Usage: `python tools/derivations/paces.py` prints them.
"""

from __future__ import annotations

import math


def clock(gamma: int, content: int) -> float:
    """The composed clock p_0 = Gamma (1 - 1 / Gamma)^c."""
    return gamma * (1 - 1 / gamma) ** content


def not_conformal(gamma: int = 12000, content: int = 3000) -> list[float]:
    """[P_0, P_a, the k = pi mode's measure on one axis, on three axes] at [2, 3] (R168)."""
    p0 = (clock(gamma, content) / gamma) ** 2
    pa = p0 * p0
    return [p0, pa, (p0 / 3 + 4 * pa / 9) / (7 / 9), (p0 / 3 + 4 * pa / 3) / (5 / 3)]


def quadratic_against_composed(gamma: int = 6000, content: int = 600) -> list[float]:
    """[the quadratic clock Gamma - c + c^2 div 2 Gamma less the composition, Gamma U^3 / 6] (R169 (h))."""
    quadratic = gamma - content + content * content // (2 * gamma)
    return [quadratic - clock(gamma, content), gamma * (content / gamma) ** 3 / 6]


def mirror_thresholds(gamma: int = 10000) -> list[float]:
    """The content U = -ln(sin(k / 2)) / 2 of the total mirror at lambda = 4 and 4.78 Links (e^(-2U) = sin(k / 2))."""
    return [-math.log(math.sin(math.pi / wavelength)) / 2 for wavelength in (4, 4.78)]


def deceleration_range() -> list[float]:
    """[s at H = 5 x 10^-4 and 1.3 x 10^-3 per interval with t = 1,000, q = 1 / s - 1 for each, the clocks' ratio at Rosenband's bound in 10^6] (R186)."""
    exponents = [h * 1000 for h in (5e-4, 1.3e-3)]
    return [*exponents, *(1 / s - 1 for s in exponents), 7.25e-11 / 2.3e-17 / 1e6]


def newton_coefficients(num: int = 2, den: int = 3) -> list[float]:
    """[1 / m* = nu / (3 sin omega_0), d omega_0 / d l times Gamma = 2 tan(omega_0 / 2), their product, Eq. (14)'s c^2 2 cos omega_0 / (1 + cos omega_0), the band's largest group speed, that speed times the derivative] (R179)."""
    nu = num / den
    omega0 = math.acos(nu)
    curvature, slope = nu / (3 * math.sin(omega0)), 2 * math.tan(omega0 / 2)
    speeds = [
        nu / 3 * math.sin(k) / math.sin(math.acos(nu * (2 + math.cos(k)) / 3))
        for k in (i / 2000 * math.pi for i in range(1, 2000))
    ]
    top = max(speeds)
    return [curvature, slope, curvature * slope, (1 / 3) * 2 * nu / (1 + nu), top, top * slope]


def frozen_content(gamma: int = 6000) -> list[float]:
    """(Gamma / 2) ln 2 Gamma, the content past which the Node's integer pace rounds to 0."""
    return [gamma / 2 * math.log(2 * gamma)]


if __name__ == "__main__":
    print("not conformal:", [round(v, 4) for v in not_conformal()])
    print("quadratic against composed:", [round(v, 2) for v in quadratic_against_composed()])
    print("mirror thresholds U:", [round(v, 4) for v in mirror_thresholds()])
    print("deceleration:", [round(v, 2) for v in deceleration_range()])
    print("Newton's coefficients:", [round(v, 3) for v in newton_coefficients()])
    print("frozen content:", [round(v) for v in frozen_content()])
