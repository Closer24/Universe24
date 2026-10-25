"""Hand g3 (2026-10-25): the gapped line's numbers as functions of the gap g = (den - num) / den, from the law's clauses
(The band at a pace, The mass read at the content, The paces compose, The lattice momentum, The two branches, The stable body),
and the window of g the brief asks for. Exact rationals where the formula is rational (fractions.Fraction); where omega_0 =
acos(1 - g) enters, the float is a check named `float_check` and the integer reading beside it is the value in thousandths.

The functions, at the vacuum (U = 0), g = 1 - num / den, sin omega_0 = s / den, sin^2 omega_0 = g (2 - g):
  cos omega(k) = (1 - g) / 3 x (cos kx + cos ky + cos kz)       the band: omega from omega_0 to pi - omega_0
  hopping t = (1 - g) / 3 per Link; the band in 2 cos omega spans 4 (1 - g)
  curvature Delta = t / sin omega_0 = (1 - g) / (3 sqrt(g (2 - g)))  omega = omega_0 + Delta k^2 / 2 near k = 0
  group velocity v_g = Delta k; largest along an axis (1 - g) / (3 sin omega(pi/2)), cos omega(pi/2) = 2 (1 - g) / 3
  Compton length L_C = 1 / (sqrt 3 omega_0) Links
  the fall of a free packet a = c(g) dU/dx with c(g) = 2 g t / sin^2 omega_0 = 2 (1 - g) / (3 (2 - g))  (W2's 0.0930 at g 0.8379)
  the force on the wave number dk/dt = (2 g / sin omega_0) dU/dx, the Bloch period 2 pi / (dk/dt)
  the one-Node binding threshold V_c = 2 (1 - g) / W_S (W_S = 1.516386, Watson) in 2 cos omega; the on-site rise (8 - 4 g) U
      (W2's reading) or 4 g U (W1's): U_c = V_c / (8 - 4 g) or V_c / (4 g); c_c = Gamma U_c levels
  the beat's redshift factor per unit U at U = 0: f = 2 g / (omega_0 sin omega_0) = 1 + g / 6 + O(g^2), the clock's 1
  the spreading of a free Gaussian packet of rms sigma_0: sigma(t)^2 = sigma_0^2 + (Delta t / (2 sigma_0))^2
      localised over T intervals (sigma(T) <= 2 sigma_0) iff Delta <= 2 sqrt 3 sigma_0^2 / T
Run: PYTHONPATH=<worktree>/src python tools/derivations/g3/window.py > tools/derivations/g3/window.out
"""

from __future__ import annotations

import json
import math
from fractions import Fraction as F

WATSON_THOUSANDTHS = 1516  # W_S = 1.516386, Watson's integral on the simple cubic lattice, to thousandths (a constant of the lattice)


def isqrt_ratio(num: int, den: int, scale: int = 1000) -> int:
    """floor(scale x sqrt(num / den)) in integers: the integer root of scale^2 num div den."""
    return math.isqrt(scale * scale * num // den)


def functions_of(g: F) -> dict:
    """Every function of the gap at one rational g, exact where rational, thousandths as the integer reading, floats as checks."""
    t = (1 - g) / 3
    sin2 = g * (2 - g)
    c_fall = 2 * (1 - g) / (3 * (2 - g))
    delta2 = t * t / sin2  # Delta^2 exact
    force2 = 4 * g * g / sin2  # (dk/dt per unit dU/dx)^2 exact
    v_c = 2 * (1 - g) * 1000 / WATSON_THOUSANDTHS  # in 2 cos omega, Watson to thousandths
    u_c_w2 = v_c / (8 - 4 * g)
    u_c_w1 = v_c / (4 * g) if g else None
    omega0 = math.acos(float(1 - g))  # float check
    sin0 = math.sqrt(float(sin2))
    f_beat = 2 * float(g) / (omega0 * sin0) if g else 1.0
    cos_half = 2 * (1 - g) / 3
    v_max = float(1 - g) / (3 * math.sqrt(1 - float(cos_half) ** 2))
    return {
        "g": [g.numerator, g.denominator],
        "cos_omega0_num_over_den": [(1 - g).numerator, (1 - g).denominator],
        "sin_omega0_thousandths": isqrt_ratio(sin2.numerator, sin2.denominator),
        "hopping_t_thousandths": int(t * 1000),
        "band_in_2cos_thousandths": int(4 * (1 - g) * 1000),
        "curvature_Delta_thousandths": isqrt_ratio(delta2.numerator, delta2.denominator),
        "fall_c_thousandths": [int(c_fall * 1000), str(c_fall)],
        "force_dk_per_dUdx_thousandths": isqrt_ratio(force2.numerator, force2.denominator),
        "threshold_V_c_in_2cos_thousandths": int(v_c * 1000),
        "threshold_levels_W2_reading_at_Gamma_1000": int(u_c_w2 * 1000),
        "threshold_levels_W1_reading_at_Gamma_1000": int(u_c_w1 * 1000) if u_c_w1 is not None else None,
        "float_check": {
            "omega0": round(omega0, 4),
            "compton_links": round(1 / (math.sqrt(3) * omega0), 3) if omega0 else None,
            "band_omega_from_to": [round(omega0, 4), round(math.pi - omega0, 4)],
            "period0_intervals": round(2 * math.pi / omega0, 3) if omega0 else None,
            "beat_factor_f": round(f_beat, 4),
            "beat_factor_first_order_1_plus_g_over_6": round(1 + float(g) / 6, 4),
            "v_group_max_axis": round(v_max, 4),
            "spread_T100_sigma0_2": round(math.sqrt(4 + (math.sqrt(float(delta2)) * 100 / 4) ** 2), 2),
        },
        "compton_links_thousandths": int(1000 / (math.sqrt(3) * omega0)) if omega0 else None,
        "beat_factor_thousandths": int(f_beat * 1000),
    }


def window_scan() -> dict:
    """The window in g by thousandths for the three conditions of the brief: (i) a width 2 to 4 Links, read two ways, the
    Compton length and the free packet's localisation over T intervals at the width w = 2 sigma_0; (ii) the fall of one Link
    within 100 intervals under a gradient of 20 levels per Link (a well of 300 levels at 3 Links, dU/dx = 0.02), c(g) x 0.02 x
    5000 >= 1; (iii) the beat's factor within 1/n of the clock's 1 for n = 4, 5, 6, 8, 10, 20."""
    found: dict = {"compton_2_to_4": [], "fall_one_link_100": [], "beat_within": {n: [] for n in (4, 5, 6, 8, 10, 20)},
                   "localised_T100": {w: [] for w in (2, 3, 4)}, "localised_T200": {w: [] for w in (2, 3, 4)}}
    for m in range(1, 1000):
        g = F(m, 1000)
        t = (1 - g) / 3
        sin2 = g * (2 - g)
        delta2 = t * t / sin2
        omega0 = math.acos(float(1 - g))
        compton = 1 / (math.sqrt(3) * omega0)
        if 2 <= compton <= 4:
            found["compton_2_to_4"].append(m)
        c_fall = 2 * (1 - g) / (3 * (2 - g))
        if c_fall * F(2, 100) * 5000 >= 1:
            found["fall_one_link_100"].append(m)
        f_beat = 2 * float(g) / (omega0 * math.sqrt(float(sin2)))
        for n in found["beat_within"]:
            if f_beat <= 1 + 1 / n:
                found["beat_within"][n].append(m)
        for T, key in ((100, "localised_T100"), (200, "localised_T200")):
            for w in (2, 3, 4):
                sigma0 = F(w, 2)
                bound2 = (2 * sigma0 * sigma0 / T) ** 2 * 3  # (2 sqrt3 sigma0^2 / T)^2 exact
                if delta2 <= bound2:
                    found[key][w].append(m)
    def span(ms: list[int]) -> list | None:
        return [min(ms), max(ms)] if ms else None
    return {
        "compton_2_to_4_links_g_thousandths": span(found["compton_2_to_4"]),
        "fall_one_link_in_100_at_20_levels_per_link_g_thousandths": span(found["fall_one_link_100"]),
        "beat_within_1_over_n_g_thousandths_at_most": {n: max(ms) if ms else None for n, ms in found["beat_within"].items()},
        "localised_100_intervals_width_links_g_thousandths_at_least": {w: min(ms) if ms else None for w, ms in found["localised_T100"].items()},
        "localised_200_intervals_width_links_g_thousandths_at_least": {w: min(ms) if ms else None for w, ms in found["localised_T200"].items()},
    }


def main() -> None:
    rows = {}
    for g in (F(1, 100), F(104, 10000), F(414, 10000), F(1, 10), F(3, 10), F(1, 2), F(62, 100), F(65, 100), F(7, 10), F(76, 100),
              F(8, 10), F(8298, 10000), F(8379, 10000), F(9, 10), F(99, 100)):
        rows[str(g)] = functions_of(g)
    out = {"functions_at_named_g": rows, "window": window_scan()}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
