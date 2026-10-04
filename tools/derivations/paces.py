"""Numbers of the composed paces (ALGEBRA.md, The paces compose): the clock p_0 = Gamma (1 - 1 / Gamma)^c and the Node's pace p_0^2 / Gamma; the not-conformal pair at c = 3,000 of 12,000 on [2, 3] (R168); the quadratic clock against the composition at U = 0.10 (R169 (h)); the total mirror's thresholds at Gamma = 10^4 for lambda = 4 and 4.78 Links (R46 with R68); a drifting Gamma's deceleration from the law's own H (R186); the band's curvature at rest and Newton's coefficient at [2, 3] (R179); the frozen content (Gamma / 2) ln 2 Gamma.

Since the derivations' map (the owner's order of 2026-10-04) the module roots in rule3.py and holds the paper's marks on the clock's composition, the acts' factors, the exact variable of the metric, light's index, the total mirror, the absent horizon, the Link's pace as curved space and the two clocks.

Usage: `python tools/derivations/paces.py` prints them.
"""

from __future__ import annotations

import math
from fractions import Fraction

try:
    import rule3
except ModuleNotFoundError:  # the gates load a module by its path, the folder not on sys.path
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import rule3

MAGIC_OMEGA_E = (
    2.0e-14  # omega_e's bound along an axis from MAGIC's dispersion limit (the paper's line 571; S.24)
)
LHAASO_OMEGA_E = (
    3.7e-10  # omega_e's bound from LHAASO's 1.4 PeV photon read as a share (the paper's line 571; S.27)
)


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
    """The least content at which the Link's pace p_0^2 / Gamma rounds to 0 in the engine's integers, the clock p_0 = Gamma (Gamma - 1)^c / Gamma^c rounded half up and p_0^2 < Gamma / 2, found by doubling and bisection on the exact fraction; beside it the formula's approximation (Gamma / 2) ln 2 Gamma: 28,206 and 28,178 at Gamma 6,000 (the law's R205 and R208)."""

    def clock(content: int) -> int:
        numerator, wall = gamma * (gamma - 1) ** content, gamma**content
        return int((2 * numerator + wall) // (2 * wall))

    def frozen(content: int) -> bool:
        return 2 * clock(content) ** 2 < gamma

    low, high = 0, 1
    while not frozen(high):
        low, high = high, 2 * high
    while high - low > 1:
        middle = (low + high) // 2
        low, high = (low, middle) if frozen(middle) else (middle, high)
    return [float(high), gamma / 2 * math.log(2 * gamma)]


def light_band_speed(gamma: int, content: int, k: float = 1e-3) -> float:
    """Light's speed at a content over its vacuum speed, from rule3's band at the paces p_0 = Gamma (1 - 1 / Gamma)^c and p_a = p_0^2 / Gamma: omega(k) sqrt 3 / k as k -> 0, N^2 (S.2)."""
    clock = rule3.clock_pace(gamma, content)
    pace = rule3.node_pace(clock, gamma)
    omega = math.acos(rule3.dispersion_at_paces((k, 0.0, 0.0), 1, 1, gamma, clock, (pace,) * 3))
    return omega * math.sqrt(3) / k


def clock_composes(gamma: int = 6000, content: int = 300, other: int = 200) -> list[float]:
    """The clock composes, p_0 = Gamma (1 - 1 / Gamma)^c, each unit slowing the clock as it stands by the same fraction (line 187; The paces compose; S.34 (a)): [N = p_0 / Gamma at the content, e^(-U) with U = c / Gamma, the composition's residual P(c + l) Gamma - P(c) P(l) in the rationals, p_0(c + 1) / p_0(c) - (1 - 1 / Gamma)], the residuals 0."""
    clock = rule3.clock_pace
    composed = clock(gamma, content + other) * gamma - clock(gamma, content) * clock(gamma, other)
    unit = clock(gamma, content + 1) / clock(gamma, content) - Fraction(gamma - 1, gamma)
    return [
        float(clock(gamma, content) / gamma),
        math.exp(-content / gamma),
        float(composed),
        float(unit),
    ]


def acts_factors(gamma: int = 6000, content: int = 300) -> list[float]:
    """The write carries p_x p_y p_z / (p_0 Gamma^2) on the form and p_x p_y p_z / (p_0^2 Gamma) on the Wronskian, and the turn carries p_0 / Gamma, per proper volume and per proper interval (line 187; S.34 (d)): with p_0 = Gamma N and p_a = p_0^2 / Gamma = Gamma N^2 on every axis the three are N^5, N^4 and N, a count per proper volume h^3 = N^-3 and per proper interval N twice, once and once with the turn; [each factor over its power of N in the rationals], all 1."""
    clock = rule3.clock_pace(gamma, content)
    pace = rule3.node_pace(clock, gamma)
    rate = clock / gamma
    form = pace**3 / (clock * gamma * gamma)
    wronskian = pace**3 / (clock * clock * gamma)
    return [float(form / rate**5), float(wronskian / rate**4), float((clock / gamma) / rate)]


def exact_variable(num: int = 2, den: int = 3, gamma: int = 6000, content: int = 600) -> list[float]:
    """The metric is stated in the variable in which it is exact (line 187; S.31): the clock acts on 2 sin(omega / 2) exactly, 1 - cos omega_b = N^2 (1 - cos omega_0) at k = 0 by the band at a pace, and in omega up to the finite-rotation correction omega_0^2 / 12; [2 sin(omega_b / 2) / (N 2 sin(omega_0 / 2)) - 1 at the content, the rate in omega per unit U less the rate in the exact variable in percent, f(omega_0) - 1 = 2 tan(omega_0 / 2) / omega_0 - 1 (6.3 at [2, 3]), omega_0^2 / 12 in percent (5.9)]."""
    clock = rule3.clock_pace(gamma, content)
    pace = rule3.node_pace(clock, gamma)
    rate = float(clock / gamma)
    omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
    omega_b = math.acos(rule3.dispersion_at_paces((0.0, 0.0, 0.0), num, den, gamma, clock, (pace,) * 3))
    residual = math.sin(omega_b / 2) / (rate * math.sin(omega_0 / 2)) - 1
    return [residual, 100 * (2 * math.tan(omega_0 / 2) / omega_0 - 1), 100 * omega_0**2 / 12]


def finite_rotation_correction_at_natures_bounds() -> list[float]:
    """The finite-rotation correction omega_0^2 / 12 at nature's gap: [at MAGIC's bound on omega_e in units of 10^-29, at LHAASO's in units of 10^-20] (line 187), 3 and 1."""
    return [MAGIC_OMEGA_E**2 / 12 / 1e-29, LHAASO_OMEGA_E**2 / 12 / 1e-20]


def light_index(gamma: int = 6000, content: int = 300) -> list[float]:
    """Light's speed at a content is N^2 = e^(-2 x) times its vacuum speed, an index n = e^(2 x), 1 / (1 - 2 x) to the first order, n - 1 = 2 x (line 193; S.2): from rule3's band at the paces p_0 = Gamma N, p_a = Gamma N^2, the band term (1 / 3) N^4 SUM_a (1 - cos k_a) giving omega = N^2 |k| / sqrt 3 at long wavelength; [N^2 from the band's slope, e^(-2 x), n = 1 / N^2, 1 / (1 - 2 x), n - 1, 2 x]."""
    x = content / gamma
    speed = light_band_speed(gamma, content)
    return [speed, math.exp(-2 * x), 1 / speed, 1 / (1 - 2 * x), 1 / speed - 1, 2 * x]


def least_mirrored_content(gamma: int, edge: float) -> int:
    """The least content c at which the Node's pace p_0^2 / Gamma, p_0 = Gamma (1 - 1 / Gamma)^c exact in the rationals, falls below the edge, by doubling and bisection."""

    def mirrored(content: int) -> bool:
        return float(rule3.node_pace(rule3.clock_pace(gamma, content), gamma)) < edge

    low, high = 0, 1
    while not mirrored(high):
        low, high = high, 2 * high
    while high - low > 1:
        middle = (low + high) // 2
        low, high = (low, middle) if mirrored(middle) else (middle, high)
    return high


def mirror_threshold(gamma: int = 10000, wavelengths: tuple[float, ...] = (4, 4.78)) -> list[float]:
    """Light meets a total mirror where p_a < Gamma sin(k / 2) (line 193; The band at a pace): the band at the Link's pace p_a has its top at 1 - cos omega = (2 / 3) (p_a / Gamma)^2 along an axis and the vacuum wave's 1 - cos omega = (2 / 3) sin^2(k / 2), so the wave is evanescent exactly where sin(k / 2) > p_a / Gamma; [the least content c at which p_a = p_0^2 / Gamma falls below Gamma sin(pi / lambda) under the composed paces, per wavelength], 1,733 and 2,464 at Gamma = 10^4 (the law's 2,465 at lambda = 4.78 reads 2,464 from the exact fraction, one unit, the wavelength's third digit)."""
    found = []
    for wavelength in wavelengths:
        edge = gamma * math.sin(math.pi / wavelength)
        # the band's top at the pace against the wave's rotation, both from rule3's band
        top = 1 - rule3.dispersion_at_paces((math.pi, 0.0, 0.0), 1, 1, gamma, gamma, (edge,) * 3)
        wave = 1 - rule3.plane_wave_dispersion(2 * math.pi / wavelength, 1, 1)
        assert abs(top - wave) < 1e-9
        found.append(float(least_mirrored_content(gamma, edge)))
    return found


def no_horizon(gamma: int = 6000) -> list[float]:
    """A deep well freezes a clock and closes nothing; the horizon of the quadratic form at Gamma / 2 is the truncation's (line 196; S.3): [the composed Link pace p_0^2 / Gamma at c = Gamma div 2, Gamma / e, the quadratic truncation's Gamma - 2 c there, the frozen content (Gamma / 2) ln 2 Gamma where the integer booking alone rounds the Link's pace to 0]."""
    content = gamma // 2
    return [
        float(rule3.node_pace(rule3.clock_pace(gamma, content), gamma)),
        float(gamma - 2 * content),
        gamma / 2 * math.log(2 * gamma),
    ]


def index_is_the_links_pace(gamma: int = 6000, content: int = 300, k: float = 0.01) -> list[float]:
    """What general relativity calls curved space stands as the Link's pace, light's index n = e^(2 x) (line 412; S.2; The paces compose, the phase index): a vacuum wave of wave number k runs inside at k_in with 1 - cos k_in = (Gamma / p_a)^2 (1 - cos k) by rule3's band at the Link's pace, sin(k_in / 2) = sin(k / 2) Gamma / p_a; [Gamma / p_a the ray index, k_in / k the phase index at k, e^(2 x)]."""
    pace = rule3.node_pace(rule3.clock_pace(gamma, content), gamma)
    inside = math.acos(1 - float(gamma / pace) ** 2 * (1 - math.cos(k)))
    assert (
        abs(
            rule3.dispersion_at_paces((inside, 0.0, 0.0), 1, 1, gamma, gamma, (pace,) * 3)
            - rule3.plane_wave_dispersion(k, 1, 1)
        )
        < 1e-12
    )
    return [float(gamma / pace), inside / k, math.exp(2 * content / gamma)]


def two_clocks(rate: float = 0.8, omega_1: float = 0.4, omega_2: float = 0.9) -> list[float]:
    """A cavity of bodies and an atom's beat shift alike by N at long wavelength, a cavity of declared faces at N^2 (line 577; S.31): the rest line of a bound mode at the clock N has 2 sin(omega' / 2) = N 2 sin(omega / 2) by the band at a pace, a body in the level is the flat body in local units of size N Links and light runs at N^2; [the exact beat omega_2' - omega_1', N (omega_2 - omega_1), the series N Delta [1 - (1 - N^2) (omega_1^2 + omega_1 omega_2 + omega_2^2) / 24], the cavity of bodies' rate N^2 / N, the declared faces' N^2]."""

    def shifted(omega: float) -> float:
        pair = Fraction(math.cos(omega)).limit_denominator(10**9)
        clock = (rate,) * 3
        return math.acos(
            rule3.dispersion_at_paces((0.0, 0.0, 0.0), pair.numerator, pair.denominator, 1, rate, clock)
        )

    delta = omega_2 - omega_1
    series = rate * delta * (1 - (1 - rate * rate) * (omega_1**2 + omega_1 * omega_2 + omega_2**2) / 24)
    return [shifted(omega_2) - shifted(omega_1), rate * delta, series, rate * rate / rate, rate * rate]


if __name__ == "__main__":
    print("not conformal:", [round(v, 4) for v in not_conformal()])
    print("quadratic against composed:", [round(v, 2) for v in quadratic_against_composed()])
    print("mirror thresholds U:", [round(v, 4) for v in mirror_thresholds()])
    print("deceleration:", [round(v, 2) for v in deceleration_range()])
    print("Newton's coefficients:", [round(v, 3) for v in newton_coefficients()])
    print("frozen content, exact and (Gamma / 2) ln 2 Gamma:", [round(v) for v in frozen_content()])
    print("the clock composes:", [round(v, 6) for v in clock_composes()])
    print("the acts' factors over N^5, N^4, N:", acts_factors())
    print(
        "the exact variable, residual and the two percentages:", [round(v, 4) for v in exact_variable()]
    )
    print(
        "omega^2 / 12 at MAGIC (10^-29) and LHAASO (10^-20):",
        finite_rotation_correction_at_natures_bounds(),
    )
    print("light's index:", [round(v, 5) for v in light_index()])
    print("the total mirror's contents at lambda = 4 and 4.78:", mirror_threshold())
    print("no horizon:", [round(v, 1) for v in no_horizon()])
    print("the index is the Link's pace:", [round(v, 5) for v in index_is_the_links_pace()])
    print("the two clocks:", [round(v, 4) for v in two_clocks()])
