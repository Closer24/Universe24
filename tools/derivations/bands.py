"""Light's band and the guide's: light's speed at long wavelength and its group velocity at the two slits' k = pi / 4 with the arrival over 34 Links (ALGEBRA.md, The lattice constants; the two slits' blind); the width-one guide's wave number k_z = arccos(3 cos Omega - 2 cos(pi / (w + 1))) at cos Omega = 2 / 3, its wavelength and the reach (pi w / lambda) sqrt(S / L) with S = 43,963 (ALGEBRA.md, The giving's lay); the born quantum's closed form 3 / (4 sin k sin Omega) on the width-one guide at the pairs [2, 3], [4, 5] and [9, 10].

Since the derivations' map (the owner's order of 2026-10-04) the module roots in rule3.py and holds the paper's marks on the band along an axis and the diagonal, the slow limit, the rest energy's departure, the one pair, de Broglie, the folded axis and light's speed under the causal bound.

Usage: `python tools/derivations/bands.py` prints them.
"""

from __future__ import annotations

import math

try:
    import rule3
except ModuleNotFoundError:  # the gates load a module by its path, the folder not on sys.path
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import rule3

SOURCE_SUM = 43963  # S = T / (2 sin Omega) at T = 65,536 and cos Omega = 2 / 3


def light_speed() -> list[float]:
    """[c at long wavelength, the group velocity at k = pi / 4] in Links per interval."""
    k = math.pi / 4
    omega = math.acos((2 + math.cos(k)) / 3)
    return [1 / math.sqrt(3), math.sin(k) / (3 * math.sin(omega))]


def arrival_intervals(distance: int = 34) -> list[float]:
    """The continuum's arrival of the two slits' packet over `distance` Links at the group velocity, in intervals."""
    return [distance / light_speed()[1]]


def guide_wave_numbers(widths: tuple[int, ...] = (4, 8, 16)) -> list[float]:
    """k_z of the width-one transverse mode's guide at cos Omega = 2 / 3, per width."""
    return [math.acos(3 * (2 / 3) - 2 * math.cos(math.pi / (w + 1))) for w in widths]


def guide_wavelengths() -> list[float]:
    """The wavelength 2 pi / k_z along the axis, per width 4, 8, 16 Links."""
    return [2 * math.pi / k for k in guide_wave_numbers()]


def guide_reaches(length: int = 8) -> list[float]:
    """The reach (pi w / lambda) sqrt(S / L) at the widths 4, 8 and 16 for the length L."""
    return [
        math.pi * w / lam * math.sqrt(SOURCE_SUM / length)
        for w, lam in zip((4, 8, 16), guide_wavelengths(), strict=True)
    ]


def guide_reaches_short() -> list[float]:
    """The reaches at L = 32."""
    return guide_reaches(32)


def guide_reach_at_the_lays_length() -> list[float]:
    """The reach at w = 8 over the lay's length L = 456 intervals, and at L = 8 (R204)."""
    return [guide_reaches(456)[1], guide_reaches(8)[1]]


def born_quantum_closed_form(
    pairs: tuple[tuple[int, int], ...] = ((2, 3), (4, 5), (9, 10)),
) -> list[float]:
    """3 / (4 sin k sin Omega) with cos k = 3 cos Omega - 2 on the width-one guide, per pair (R198)."""
    found = []
    for num, den in pairs:
        omega = math.acos(num / den)
        k = math.acos(3 * math.cos(omega) - 2)
        found.append(3 / (4 * math.sin(k) * math.sin(omega)))
    return found


def band_coefficient(num: int, den: int, k: float = math.pi / 2) -> float:
    """num / (3 den), the band's coefficient (The conventions and the units, row 1: c_s^2), read from rule3's band as (cos omega_0 - cos omega(k)) / (1 - cos k), the same at every k."""
    return (rule3.plane_wave_dispersion(0.0, num, den) - rule3.plane_wave_dispersion(k, num, den)) / (
        1 - math.cos(k)
    )


def light_speed_squared() -> float:
    """c^2 = 1 / 3, light's band coefficient at [1, 1], the long-wavelength speed squared (The lattice constants)."""
    return band_coefficient(1, 1)


def inertia_from_the_band(num: int, den: int) -> float:
    """m* = 1 / omega''(0), the band's curvature at rest (The push on a moving record, the band's inertia): differentiating cos omega = cos omega_0 - (num / (3 den)) (1 - cos k) twice at k = 0 gives sin omega_0 omega''(0) = num / (3 den), so m* = 3 sin omega_0 / (num / den) = 3 tan omega_0; `two_body.curvature` is the finite-difference second method."""
    omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
    return math.sin(omega_0) / band_coefficient(num, den)


def figure_bands() -> list[float]:
    """The bands figure's numbers (the paper's Fig. bands, line 170), from cos omega = (num / (3 den)) (2 + cos k), rule3's band at the vacuum's paces: [matter's gap omega_0 at [2, 3], its inertia m* from the band's curvature (3 tan omega_0), light's top at k = pi, matter's top at k = pi, the two slits' omega at k = pi / 4 on light's band, sin omega_0 / omega_0, the click's energy over T omega_0]; the period 14.1 is `two_slits_period`'s, printed to one decimal."""
    omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, 2, 3))
    return [
        omega_0,
        inertia_from_the_band(2, 3),
        math.acos(rule3.plane_wave_dispersion(math.pi, 1, 1)),
        math.acos(rule3.plane_wave_dispersion(math.pi, 2, 3)),
        math.acos(rule3.plane_wave_dispersion(math.pi / 4, 1, 1)),
        math.sin(omega_0) / omega_0,
    ]


def two_slits_period() -> list[float]:
    """The two slits' wave at k = pi / 4 on light's band has the period 2 pi / omega, 14.1 intervals (line 170), the caption's one number printed to one decimal."""
    return [2 * math.pi / math.acos(rule3.plane_wave_dispersion(math.pi / 4, 1, 1))]


def diagonal_dispersion(samples: int = 12) -> list[float]:
    """Along the cube's diagonal light has cos omega = cos k exactly, no dispersion (line 175; S.1): with k_a = q on every axis the band cos omega = (num / (3 den)) SUM_a cos k_a is cos q at [1, 1]; [the largest |cos omega - cos q| over q in (0, pi), d omega / d|k| along the diagonal, |k| = q sqrt 3, light's 1 / sqrt 3], the first 0."""
    vacuum = (1, 1, (1, 1, 1))
    worst = max(
        abs(rule3.dispersion_at_paces((q, q, q), 1, 1, *vacuum) - math.cos(q))
        for q in (i * math.pi / (samples + 1) for i in range(1, samples + 1))
    )
    q, h = 0.7, 1e-5
    slope = (
        math.acos(rule3.dispersion_at_paces((q + h,) * 3, 1, 1, *vacuum))
        - math.acos(rule3.dispersion_at_paces((q - h,) * 3, 1, 1, *vacuum))
    ) / (2 * h * math.sqrt(3))
    return [worst, slope]


def schroedinger_limit(num: int = 2, den: int = 3) -> list[float]:
    """The band's slow limit is Schroedinger's equation with the inertia m* = 3 tan omega_0 and, in a content U, the potential omega_0 f(omega_0) U (line 175; The push on a moving record, the rest push f(omega_0) = 2 tan(omega_0 / 2) / omega_0): [m* from the band's curvature, -d omega_0 / dU at U = 0 from the band at a pace with the clock Gamma e^(-U) and the Link Gamma e^(-2 U), f(omega_0) = that slope over omega_0, omega_0 f(omega_0) the potential's coefficient]."""
    omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, num, den))

    def rest(content: float) -> float:
        clock = math.exp(-content)
        return math.acos(
            rule3.dispersion_at_paces((0.0, 0.0, 0.0), num, den, 1, clock, (clock * clock,) * 3)
        )

    h = 1e-4
    slope = -(rest(h) - rest(-h)) / (2 * h)
    return [inertia_from_the_band(num, den), slope, slope / omega_0, slope]


def rest_energy_departure(pairs: tuple[tuple[int, int], ...] = ((2, 3), (999, 1000))) -> list[float]:
    """E = m* c_m^2 = omega_0 by the definition c_m^2 = omega_0 / m*; the departure of c_m^2 from the band's c^2 = 1 / 3 is omega_0 / tan omega_0, which is 1 - omega_0^2 / 3 to the order omega_0^2 (line 175; S.18, S.21): [c_m^2 / c^2 at the first pair, 1 - omega_0^2 / 3 there, (1 - c_m^2 / c^2) / (omega_0^2 / 3) at the second pair, 1 as the gap closes]."""
    light = light_speed_squared()
    found = []
    for num, den in pairs:
        omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
        found.append(omega_0 / inertia_from_the_band(num, den) / light)
    omega_first = math.acos(rule3.plane_wave_dispersion(0.0, *pairs[0]))
    omega_second = math.acos(rule3.plane_wave_dispersion(0.0, *pairs[1]))
    return [found[0], 1 - omega_first**2 / 3, (1 - found[1]) / (omega_second**2 / 3)]


def pair_fixes_mass_and_speed(num: int = 2, den: int = 3) -> list[float]:
    """One rational [num, den] fixes mass and speed together (line 175): from the one band [cos omega_0 = num / den the rest, c_s^2 = (cos omega_0 - cos omega(k)) / (1 - cos k) = num / (3 den) the band's coefficient (The conventions and the units, row 1), c_m^2 = omega_0 / m* the kinetic scale, m* the inertia]."""
    k = 0.5
    cos_rest = rule3.plane_wave_dispersion(0.0, num, den)
    omega_0 = math.acos(cos_rest)
    inertia = inertia_from_the_band(num, den)
    return [
        cos_rest,
        (cos_rest - rule3.plane_wave_dispersion(k, num, den)) / (1 - math.cos(k)),
        omega_0 / inertia,
        inertia,
    ]


def de_broglie(num: int = 2, den: int = 3, k: float = 0.01) -> list[float]:
    """De Broglie's relation, row (h) (line 520; S.22): a free record of a matter family has the group velocity v = (num / (3 den)) sin k / sin omega_b on rule3's band and, to second order, k = omega_b v / c_m^2 with c_m^2 = omega_0 / m*; [v at k, the relative residual (omega_b v / c_m^2 - k) / k, c_m^2], the residual 0 to the order k^2."""
    omega_b = math.acos(rule3.plane_wave_dispersion(k, num, den))
    omega_0 = math.acos(rule3.plane_wave_dispersion(0.0, num, den))
    kinetic_scale = omega_0 / inertia_from_the_band(num, den)
    velocity = rule3.group_velocity(k, num, den)
    return [velocity, (omega_b * velocity / kinetic_scale - k) / k, kinetic_scale]


def folded_axis_band(k: float = math.pi / 4) -> list[float]:
    """A record uniform along the folded axis has the three-dimensional band at k_z = 0, so the flat GameBoard carries the file's band exactly (line 538): on a folded axis the arrival is the Node's own level (The line), the two arrivals summing to 2 a_now as cos k_z = 1 does; [k_z, |cos omega at (k, 0, 0) - cos omega along one axis|, the plane wave's residual against the line on a chain with y and z folded], all 0."""
    difference = abs(
        rule3.dispersion_at_paces((k, 0.0, 0.0), 1, 1, 1, 1, (1, 1, 1))
        - rule3.plane_wave_dispersion(k, 1, 1)
    )
    return [0.0, difference, rule3.plane_wave_residual(k, 1, 1)]


def light_speed_and_causal_bound() -> list[float]:
    """Light's speed of 1 / sqrt 3 Links per interval from Rule3's vacuum band and the causal bound of 1 Link per interval, the step's reach (line 577; The lattice constants): [the group velocity as k -> 0 at [1, 1], 1 / sqrt 3, the reach of one step: the farthest arrival of `chain_arrivals` is the neighbour, one Link]."""
    count = 9
    reach = max(
        min(abs(j - i), count - abs(j - i))
        for i, ports in enumerate(rule3.chain_arrivals(count))
        for j in ports
    )
    return [rule3.group_velocity(1e-4, 1, 1), 1 / math.sqrt(3), float(reach)]


if __name__ == "__main__":
    print(
        "light: c, v_g(pi/4):",
        [round(v, 4) for v in light_speed()],
        "arrival:",
        [round(v, 1) for v in arrival_intervals()],
    )
    print(
        "k_z:",
        [round(v, 4) for v in guide_wave_numbers()],
        "lambda:",
        [round(v, 2) for v in guide_wavelengths()],
    )
    print(
        "reaches L = 8:",
        [round(v) for v in guide_reaches()],
        "L = 32:",
        [round(v) for v in guide_reaches_short()],
    )
    print("w = 8 at L = 456 and 8:", [round(v) for v in guide_reach_at_the_lays_length()])
    print("born quantum:", [round(v, 4) for v in born_quantum_closed_form()])
    print(
        "the figure's numbers:", [round(v, 4) for v in figure_bands()], "the period:", two_slits_period()
    )
    print("the diagonal, residual and speed:", [round(v, 6) for v in diagonal_dispersion()])
    print(
        "the slow limit, m*, the slope, f(omega_0), the potential:",
        [round(v, 4) for v in schroedinger_limit()],
    )
    print("the rest energy's departure:", [round(v, 4) for v in rest_energy_departure()])
    print("one pair, cos omega_0, c_s^2, c_m^2, m*:", [round(v, 4) for v in pair_fixes_mass_and_speed()])
    print("de Broglie, v, the residual, c_m^2:", [round(v, 5) for v in de_broglie()])
    print("the folded axis:", [round(v, 9) for v in folded_axis_band()])
    print("light's speed and the causal bound:", [round(v, 4) for v in light_speed_and_causal_bound()])
