"""The tension as the engine writes it against the energy it writes (ALGEBRA.md, The tension; R166): on a plane wave b cos(k i - omega t) the Node's own reading h_a = now_(i-a) now_(i+a) - now_i^2 is -b^2 sin^2 k and the form D = now^2 - next x before is b^2 sin^2 omega; the written stress over the written energy per Node, (num / den) sin^2 k / (3 sin^2 omega) with the tensions' wall 3 den T against the time part's T, is 1 on light's band as k goes to 0 (nature's T_xx = T_00 for light along its axis), and Eq. (8)'s stencil would write 2.

Since the derivations' map (the owner's order of 2026-10-04) the module roots in rule3.py and holds the paper's mark on the stress of dust, 2 c v_a v_b.

Usage: `python tools/derivations/tension.py` prints them.
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


def dust_stress(
    wave: tuple[float, float] = (0.3, 0.5),
    amplitude: float = 1.0,
    phase: float = 0.2,
    action: int = 32768,
) -> list[float]:
    """A packet of count c and velocity v has the stress 2 c v_a v_b, the two Links' currents summed, the stress of dust (line 274; S.7 for the plane wave): on light's plane wave b cos(k . x - omega t) the stress reading G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)) is -2 b^2 sin^2 k_a at every Node and the cross reading G_ab = -2 b^2 sin k_a sin k_b, the Link's booking -num G_ab over the tensions' wall 3 den T; against 2 c v_a v_b with c = D / T the form per Node over the action, D = now^2 - next x before = b^2 sin^2 omega (The conventions and the units, row 7), and v_a = d omega / d k_a = (num / (3 den)) sin k_a / sin omega the group velocity on rule3's band in units of light's c = 1 / sqrt 3; [the booking over 2 c v_x v_x, over 2 c v_x v_y], both 1 on light's band at every wave number."""
    k_x, k_y = wave
    num, den = 1, 1
    omega = math.acos(rule3.dispersion_at_paces((k_x, k_y, 0.0), num, den, 1, 1, (1, 1, 1)))
    # c^2 = 1 / 3, light's band coefficient (cos omega_0 - cos omega(k)) / (1 - cos k) at [1, 1]
    light_squared = (1 - rule3.plane_wave_dispersion(math.pi / 2, 1, 1)) / (1 - math.cos(math.pi / 2))
    # the Node's form D from the wave at one Node, now, next and before
    now, nxt, before = (amplitude * math.cos(phase + s * omega) for s in (0, -1, 1))
    form = now * now - nxt * before
    count = form / action
    # the stress reading along x from the levels at x - 1, x, x + 1, x + 2 (S.7's input)
    levels = [amplitude * math.cos(k_x * x + phase) for x in (-1, 0, 1, 2)]
    reading_xx = levels[1] * (levels[3] - levels[1]) - levels[2] * (levels[2] - levels[0])
    booking_xx = -num * reading_xx / (3 * den * action)
    booking_xy = -num * (-2 * amplitude * amplitude * math.sin(k_x) * math.sin(k_y)) / (3 * den * action)
    v_x = num / (3 * den) * math.sin(k_x) / math.sin(omega)
    v_y = num / (3 * den) * math.sin(k_y) / math.sin(omega)
    dust_xx = 2 * count * v_x * v_x / light_squared
    dust_xy = 2 * count * v_x * v_y / light_squared
    return [booking_xx / dust_xx, booking_xy / dust_xy]


if __name__ == "__main__":
    print("plane wave readings:", [round(v, 6) for v in plane_wave_readings()])
    print(
        "written stress over energy at k = 0.01, 0.1, pi/4:",
        [round(v, 4) for v in written_stress_over_energy()],
    )
    print("Eq. (8) over the write:", stencil_against_the_write())
    print(
        "the stress of dust, the booking over 2 c v_a v_b, xx and xy:",
        [round(v, 9) for v in dust_stress()],
    )
