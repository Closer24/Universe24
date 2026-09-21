"""Section 16.2 (f) of DERIVATIONS_BEAM.md: the Link, the interval and the
unit of content from c, G and hbar; the computation in G; the growing
board against lunar laser ranging. Host arithmetic; no run.

The law's units: c_law = 1 / sqrt 3 Links per interval, G_law = K_fan
(n / d) / (4 pi S) in Links^3 per unit of content per interval^2,
hbar_law = h / (2 pi) in units of content x Links^2 per interval. With
L, T, M the Link, the interval and the unit in SI:
    c = c_law L / T,  G = G_law L^3 / (M T^2),  hbar = hbar_law M L^2 / T,
so  L = l_Planck / sqrt(3 sqrt 3 G_law hbar_law),  T = L / (sqrt 3 c),
    M = m_Planck sqrt(sqrt 3 G_law / hbar_law).
"""

from __future__ import annotations

import math
from pathlib import Path

G = 6.67430e-11  # CODATA 2022
HBAR = 1.054571817e-34
C = 299792458.0
M_E = 9.1093837e-31
M_PLANCK = math.sqrt(HBAR * C / G)
L_PLANCK = math.sqrt(HBAR * G / C**3)
SIZE = 8.8e26  # the observable universe's diameter, metres
AGE = 4.35e17  # seconds


def units(g_law: float, hbar_law: float) -> tuple[float, float, float]:
    length = L_PLANCK / math.sqrt(3 * math.sqrt(3) * g_law * hbar_law)
    interval = length / (math.sqrt(3) * C)
    mass = M_PLANCK * math.sqrt(math.sqrt(3) * g_law / hbar_law)
    return length, interval, mass


def main() -> None:
    out = []
    out.append(f"l_Planck {L_PLANCK:.4e} m, m_Planck {M_PLANCK:.4e} kg")
    ratio_max = (M_E / 4526 / M_PLANCK) ** 2 / math.sqrt(3)
    out.append(
        f"the mass bound m_unit <= m_e / 4526 = {M_E / 4526:.3e} kg gives G_law / hbar_law <= {ratio_max:.2e}"
    )
    out.append("")
    out.append("(A) The three cases")
    for g_law, hbar_law, name in (
        (1.0, 1.0, "both 1 (the Planck choice)"),
        (ratio_max, 1.0, "the bound, h = 2 pi"),
        (ratio_max, 1e6, "the bound, hbar_law = 10^6"),
    ):
        length, interval, mass = units(g_law, hbar_law)
        out.append(
            f"  {name}: Link {length:.2e} m, interval {interval:.2e} s, unit {mass:.2e} kg = {mass / M_E:.2e} m_e;"
            f" the universe {SIZE / length:.1e} Links across, {AGE / interval:.1e} intervals old"
        )
    out.append("")
    out.append("(B) The computation in G: G = 26 K_fan (n / d) / (4 pi K_budget) with hbar_law = 1")
    for k_fan, rate in ((290, 1 / 4096), (290, 1.0), (6, 1.0)):
        k_min = 26 * k_fan * rate / (4 * math.pi * ratio_max)
        out.append(
            f"  K_fan {k_fan}, n / d {rate:.2e}: K_budget >= {k_min:.1e} operations per Node per interval"
        )
    out.append("")
    out.append(
        "(C) A constant total computation over a growing board, K_budget ~ 1 / a^3, G ~ a^3, Milne a ~ t"
    )
    hubble = 1 / 1.4e10
    out.append(
        f"  Gdot / G = 3 H = {3 * hubble:.1e} per year; lunar laser ranging's bound about 1e-13 per year (Hofmann and Muller 2018)"
    )
    out.append(
        "  under the growing wall (15.1 (b)) X^3 and K are fixed, the total is constant, G is constant, c_0 / a varies"
    )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
