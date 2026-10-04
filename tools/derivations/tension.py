"""The tension as the engine writes it against the energy it writes (ALGEBRA.md, The tension; R166): on a plane wave b cos(k i - omega t) the Node's own reading h_a = now_(i-a) now_(i+a) - now_i^2 is -b^2 sin^2 k and the form D = now^2 - next x before is b^2 sin^2 omega; the written stress over the written energy per Node, (num / den) sin^2 k / (3 sin^2 omega) with the tensions' wall 3 den T against the time part's T, is 1 on light's band as k goes to 0 (nature's T_xx = T_00 for light along its axis), and Eq. (8)'s stencil would write 2.

Usage: `python tools/derivations/tension.py` prints them.
"""

from __future__ import annotations

import math


def plane_wave_readings(
    amplitude: float = 1.0, k: float = 0.7, omega: float = 0.4, phase: float = 0.3
) -> list[float]:
    """[-h_a over b^2 sin^2 k, D over b^2 sin^2 omega] on the plane wave, both 1 exactly."""
    now = [amplitude * math.cos(k * i - phase) for i in (-1, 0, 1)]
    nxt, before = amplitude * math.cos(-omega - phase), amplitude * math.cos(omega - phase)
    h = now[0] * now[2] - now[1] ** 2
    form = now[1] ** 2 - nxt * before
    return [-h / (amplitude**2 * math.sin(k) ** 2), form / (amplitude**2 * math.sin(omega) ** 2)]


def written_stress_over_energy(
    wave_numbers: tuple[float, ...] = (0.01, 0.1, math.pi / 4),
) -> list[float]:
    """(num / den) sin^2 k / (3 sin^2 omega) on light's band (num = den), per wave number."""
    found = []
    for k in wave_numbers:
        omega = math.acos((2 + math.cos(k)) / 3)
        found.append(math.sin(k) ** 2 / (3 * math.sin(omega) ** 2))
    return found


def stencil_against_the_write() -> list[float]:
    """[Eq. (8)'s T_aa over the Node's own -num h_a on a plane wave] = 2: the (1, 2, 1) / 2 stencil sums to 2."""
    return [(1 + 2 + 1) / 2]


if __name__ == "__main__":
    print("plane wave readings:", [round(v, 6) for v in plane_wave_readings()])
    print(
        "written stress over energy at k = 0.01, 0.1, pi/4:",
        [round(v, 4) for v in written_stress_over_energy()],
    )
    print("Eq. (8) over the write:", stencil_against_the_write())
