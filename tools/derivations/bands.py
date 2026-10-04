"""Light's band and the guide's: light's speed at long wavelength and its group velocity at the two slits' k = pi / 4 with the arrival over 34 Links (ALGEBRA.md, The lattice constants; the two slits' blind); the width-one guide's wave number k_z = arccos(3 cos Omega - 2 cos(pi / (w + 1))) at cos Omega = 2 / 3, its wavelength and the reach (pi w / lambda) sqrt(S / L) with S = 43,963 (ALGEBRA.md, The giving's lay); the born quantum's closed form 3 / (4 sin k sin Omega) on the width-one guide at the pairs [2, 3], [4, 5] and [9, 10].

Usage: `python tools/derivations/bands.py` prints them.
"""

from __future__ import annotations

import math

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
