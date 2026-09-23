"""COMPUTATION (not an engine run): light's own dispersion on the GameBoard and the bound
it puts on the one scale (LIGHT_DISPERSION_BOUND.md, row A2 of the schedule).

Light's kind is the pair [1, 1]: 2 cos omega = S_6 / 3 for a plane wave, S_6 = 2 SUM_i
cos k_i. Along a direction n (unit vector) with |k| = k:
    cos omega = (1 / 3) SUM_i cos(k n_i)
    omega = (k / sqrt 3) (1 - (3 SUM_i n_i^4 - 1) k^2 / 72 + ...)
    group pace v_g / c = 1 - (3 SUM_i n_i^4 - 1) k^2 / 24 + ...
with c = 1 / sqrt 3 Link per interval. The coefficient (3 SUM n_i^4 - 1) runs from 0 on a
body diagonal to 2 on an axis and averages 4 / 5 over the sphere.

Nature parametrises a quadratic photon dispersion as v / c = 1 - s (3 / 2) (E / E_QG2)^2
(the n = 2 form of the gamma-ray-burst bounds; E_QG2 the published bound, s = +1 the
subluminal side, which is the GameBoard's sign). With k = E a / (hbar c), a the Link:
    (3 SUM n^4 - 1) / 24 (E a / hbar c)^2 <= (3 / 2) (E / E_QG2)^2
    a <= (hbar c / E_QG2) sqrt(36 / (3 SUM n^4 - 1))
and the one interval tau = a / (sqrt 3 c_nature), since light covers one Link in sqrt 3
intervals on the GameBoard (c = 1 / sqrt 3 Link per interval; Reviewer 3's line of 23:32Z). The published E_QG2 is the Source Verifier's
to confirm; this script takes it as an input and prints the bound it implies.

    PYTHONPATH=src python docs/designs/detector_law/light_dispersion_bound.py [E_QG2_GeV]
"""

import math
import sys

import numpy as np

HBAR_C_GEV_M = 1.973269804e-16  # hbar c in GeV m (CODATA, CONVERSION)
C_M_S = 299792458.0  # CONVERSION
PLANCK_LENGTH_M = 1.616e-35  # for scale (CONVERSION)
PLANCK_TIME_S = 5.391e-44  # for scale (CONVERSION)


def omega_exact(k, n):
    return math.acos(sum(math.cos(k * ni) for ni in n) / 3)


def group_pace(k, n, h=1e-6):
    return (omega_exact(k + h, n) - omega_exact(k - h, n)) / (2 * h)


if __name__ == "__main__":
    c = 1 / math.sqrt(3)
    print("(a) light's own dispersion on the GameBoard, exact against the series (COMPUTATION):")
    print("    direction | 3 SUM n^4 - 1 | k | v_g / c exact | 1 - coeff k^2 / 24")
    dirs = {
        "axis (1,0,0)": (1.0, 0.0, 0.0),
        "face diagonal (1,1,0)/sqrt2": (1 / math.sqrt(2), 1 / math.sqrt(2), 0.0),
        "body diagonal (1,1,1)/sqrt3": tuple([1 / math.sqrt(3)] * 3),
    }
    for name, n in dirs.items():
        coeff = 3 * sum(ni**4 for ni in n) - 1
        for k in (0.1, 0.3, 0.6):
            print(
                f"    {name:28s} | {coeff:.4f} | {k:.1f} | {group_pace(k, n) / c:.6f} | {1 - coeff * k * k / 24:.6f}"
            )
    # the sphere average of 3 SUM n^4 - 1
    rng = np.random.default_rng(0)
    v = rng.standard_normal((200000, 3))
    v /= np.linalg.norm(v, axis=1)[:, None]
    avg = float(np.mean(3 * np.sum(v**4, axis=1) - 1))
    print(f"    the sphere average of 3 SUM n^4 - 1: {avg:.4f} (exactly 4 / 5 = 0.8)")
    print(
        "(b) the PREDICTION of the form: the quadratic dispersion is ANISOTROPIC on the sky, its coefficient"
        " (3 SUM n^4 - 1) in [0, 2], zero along a body diagonal, 2 along an axis: a cubic pattern."
    )
    e_qg2 = float(sys.argv[1]) if len(sys.argv) > 1 else 1.3e11
    print(
        f"(c) the BOUND on the one scale from a published quadratic bound E_QG2 = {e_qg2:.3g} GeV"
        " (the input; RECALLED until the Source Verifier confirms it; the subluminal side):"
    )
    for name, coeff in (("axis", 2.0), ("sphere average", 0.8), ("face diagonal", 0.5)):
        a = (HBAR_C_GEV_M / e_qg2) * math.sqrt(36 / coeff)
        tau = a / (math.sqrt(3) * C_M_S)
        print(
            f"    {name:15s}: the Link a <= {a:.2e} m ({a / PLANCK_LENGTH_M:.1e} Planck lengths),"
            f" one interval tau <= {tau:.2e} s ({tau / PLANCK_TIME_S:.1e} Planck times)"
        )
    print(
        "    along a body diagonal the quadratic term vanishes and this bound does not apply; several bursts in"
        " different directions close that gap."
    )
    two_pace = 3.6e-28
    print(
        f"    beside it, row A's two-pace bound on the same interval, 3.6e-28 s: this one is tighter by"
        f" {two_pace / ((HBAR_C_GEV_M / e_qg2) * math.sqrt(36 / 0.8) / (math.sqrt(3) * C_M_S)):.1e}."
    )
