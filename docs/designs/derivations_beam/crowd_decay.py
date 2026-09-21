"""Section 18.2's addendum: the background crowd decay-by-crowd-v1 needs,
and the beam-and-bottle pin. Host arithmetic; no run.

The presence a body reads from a source of content M at distance r is
proportional to M / r^2 (sections 3.2, 5.1), so the crowd at a Node is
the sum of M / r^2 over the sources within the horizon: the nearest
large mass dominates. In SI-like units, kg per m^2, for a neutron:
"""

from __future__ import annotations

import math
from pathlib import Path

SOURCES = {
    "the Earth at its surface": (5.972e24, 6.371e6),
    "the Moon at its surface": (7.346e22, 1.737e6),
    "Venus at 500 km altitude": (4.867e24, 6.052e6 + 5e5),
    "the Sun at 1 au": (1.989e30, 1.496e11),
    "the Sun at Voyager 1 (2.4 x 10^13 m)": (1.989e30, 2.4e13),
    "an apparatus of 10^3 kg at 1 m": (1e3, 1.0),
}
RHO_CRIT = 8.5e-27  # kg / m^3
HUBBLE_LENGTH = 1.3e26  # m
TAU_BEAM, TAU_BEAM_ERR = 887.7, 2.2  # s, Yue et al. 2013
TAU_BOTTLE, TAU_BOTTLE_ERR = 877.75, 0.36  # s, UCNtau 2021


def main() -> None:
    out = ["(A) The crowd's weight, M / r^2 in kg per m^2, and its ratio to the Earth's surface"]
    earth = SOURCES["the Earth at its surface"]
    w_earth = earth[0] / earth[1] ** 2
    for name, (m, r) in SOURCES.items():
        w = m / r**2
        out.append(f"  {name:<38} {w:.2e}   {w / w_earth:.1e}")
    cosmic = 4 * math.pi * RHO_CRIT * HUBBLE_LENGTH
    out.append(
        f"  {'the universe within the Hubble length':<38} {cosmic:.2e}   {cosmic / w_earth:.1e}   (4 pi rho R_H)"
    )
    out.append("")
    out.append("(B) The beam and the bottle")
    diff = TAU_BEAM - TAU_BOTTLE
    out.append(
        f"  beam {TAU_BEAM} +- {TAU_BEAM_ERR} s, bottle {TAU_BOTTLE} +- {TAU_BOTTLE_ERR} s: the difference {diff:.1f} s = {diff / TAU_BOTTLE:.2%} of the lifetime, {diff / math.hypot(TAU_BEAM_ERR, TAU_BOTTLE_ERR):.1f} standard deviations"
    )
    out.append(
        f"  a rate proportional to the crowd would need the beam's crowd {TAU_BOTTLE / TAU_BEAM:.4f} of the bottle's ({1 - TAU_BOTTLE / TAU_BEAM:.2%} thinner); the apparatus changes the Earth's crowd by {1e3 / w_earth:.0e}"
    )
    out.append("")
    out.append(
        "(C) The same rate off the Earth, rate proportional to the crowd (lifetime in units of the Earth's)"
    )
    for name in (
        "the Moon at its surface",
        "Venus at 500 km altitude",
        "the Sun at 1 au",
        "the Sun at Voyager 1 (2.4 x 10^13 m)",
    ):
        m, r = SOURCES[name]
        out.append(f"  {name:<38} lifetime x {w_earth / (m / r**2):.1e}")
    out.append(
        "  measured: Venus flyby (MESSENGER) tau_n = 780 +- 60 +- 70 s (Wilson et al. 2020); Voyager's Pu-238 output falling at the 87.7-year half-life for 45 years"
    )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
