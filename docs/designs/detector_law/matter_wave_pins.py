"""COMPUTATION (not an engine run): the pins of the two matter-wave rows (DECLARATIONS.md
section 12; SCHEDULE.md rows M1 and M2), on the model owner's word of 2026-09-24 and the
Boss's decision of 23:32Z: a lamp of the MATTER family (the kind [800, 809], mu = 0.15)
sends a train at a declared omega above omega_0 through two openings in a mirror line on
a 128^2 layer; the screen's clicks fringe, and the front's arrival gives the group pace.

The band (ALGEBRA.md 8.1): cos omega = cos omega_0 cos omega_l(k), along an axis
cos omega_l(k) = (cos k + 2) / 3. Printed:
  (a) DE BROGLIE (K): for the declared omega the wavenumber k, lambda_dB = 2 pi / k, and
      the screen's maxima on the declared geometry by the two-source sum with this k
      (exact, no far-field step): the fringe spacing;
  (b) E = m c^2 (K in the form, P in the correction): the group pace v_g = d omega / dk at
      that k, the inertia m = k / v_g, the small-mass limit m -> 3 tan omega_0, and
      omega_0 / (m c^2) with c^2 = 1 / 3: exactly omega_0 / tan omega_0 in the limit,
      the GameBoard's own correction to E = m c^2 at finite mass.

    PYTHONPATH=src python docs/designs/detector_law/matter_wave_pins.py
"""

import math

import numpy as np

NUM, DEN = 800, 809
OMEGA_0 = math.acos(NUM / DEN)
C2 = 1 / 3


def omega_of_k(k):
    return math.acos((NUM / DEN) * (math.cos(k) + 2) / 3)


def k_of_omega(omega, lo=1e-6, hi=math.pi - 1e-6):
    for _ in range(200):
        mid = (lo + hi) / 2
        if omega_of_k(mid) < omega:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def group_pace(k, h=1e-6):
    return (omega_of_k(k + h) - omega_of_k(k - h)) / (2 * h)


def screen_pattern(k, d, length, half_width):
    """The two-source sum on the screen at distance `length` from the openings separated by
    `d` (the openings at y = +- d / 2), |e^{i k r1} / sqrt r1 + e^{i k r2} / sqrt r2|^2 on
    the layer (a line source's fall-off), sampled at every screen Node."""
    ys = np.arange(-half_width, half_width + 1)
    r1 = np.hypot(length, ys - d / 2)
    r2 = np.hypot(length, ys + d / 2)
    amp = np.exp(1j * k * r1) / np.sqrt(r1) + np.exp(1j * k * r2) / np.sqrt(r2)
    return ys, np.abs(amp) ** 2


if __name__ == "__main__":
    print(
        f"the matter family [{NUM}, {DEN}]: omega_0 = {OMEGA_0:.5f}; the small-mass limit m = 3 tan omega_0 = {3 * math.tan(OMEGA_0):.5f}"
    )
    d, length, half_width = 32, 64, 60
    for lam in (12.0, 16.0):
        k = 2 * math.pi / lam
        omega = omega_of_k(k)
        k_back = k_of_omega(omega)
        vg = group_pace(k)
        m = k / vg
        ys, pat = screen_pattern(k, d, length, half_width)
        maxima = [
            int(ys[i]) for i in range(1, len(ys) - 1) if pat[i] > pat[i - 1] and pat[i] >= pat[i + 1]
        ]
        spacing = np.diff(maxima)
        print(
            f"(a) DE BROGLIE at the declared omega = {omega:.5f} (the period {2 * math.pi / omega:.2f} intervals):"
            f" k = {k_back:.5f} per Link, lambda_dB = {2 * math.pi / k_back:.3f} Links; the screen at L = {length} with the"
            f" openings d = {d} apart: the maxima at y = {maxima}, the spacings {list(spacing)} Links (the far-field"
            f" lambda L / d = {lam * length / d:.1f}); THE PIN the maxima's positions, the band one Node"
        )
        print(
            f"(b) E = m c^2 at that k: v_g = {vg:.5f} Link per interval (the front's arrival over L = {length}: {length / vg:.1f}"
            f" intervals), m = k / v_g = {m:.5f}; omega_0 / (m c^2) = {OMEGA_0 / (m * C2):.5f} (the small-mass limit"
            f" omega_0 / tan omega_0 = {OMEGA_0 / math.tan(OMEGA_0):.5f}; E = m c^2 exactly would read 1)"
        )
    print(
        "    the form (K): omega_0 = m c^2 with c^2 = 1 / 3 in the small-mass limit, from the one band;"
        " the correction omega_0 / tan omega_0 - 1 = -0.74 percent at mu = 0.15 is the GameBoard's (P)."
    )
