"""Section 19 of DERIVATIONS_BEAM.md: the masses generically, the nucleon
as a chain of three quarks on the bipartite lattice. Host arithmetic on
PDG 2024 and CODATA 2022 numbers; no run.

(A) The mass of a bound set as held plus in flight: the nucleon's held
    part (the quarks' current masses) and its bond part F; the
    neutron-proton difference as the held difference m_d - m_u, and the
    electric self-energy of a uniformly charged sphere of the proton's
    radius.
(B) The chain on the cubic lattice (bipartite: no triangle): the mean
    square charge radius of u-d-u and d-u-d about the charge centroid,
    against the measured r_p^2 and r_n^2.
(C) The held counts in units of the minimal mass at the electron's
    count k = 4526 (section 16.2).
"""

from __future__ import annotations

import math
from pathlib import Path

M_E = 0.51099895  # MeV, CODATA 2022
M_U, M_U_ERR = 2.16, 0.4  # MeV, PDG 2024 (MS-bar at 2 GeV; +0.49 / -0.26)
M_D, M_D_ERR = 4.70, 0.07
M_P = 938.27209
M_N = 939.56542
R_P = 0.8409  # fm, CODATA 2022
R_N2 = -0.1155  # fm^2, PDG 2024
ALPHA_HBARC = 1.43996  # MeV fm
DWELL = 55 / 32


def charge_radius2(charges: list[float], positions: list[float]) -> float:
    """Sum q_i (x_i - x_c)^2 about the charge centroid, in Link^2 (the
    centroid of a neutral set taken at the geometric centre)."""
    total = sum(charges)
    if abs(total) > 1e-12:
        x_c = sum(q * x for q, x in zip(charges, positions, strict=True)) / total
    else:
        x_c = sum(positions) / len(positions)
    return sum(q * (x - x_c) ** 2 for q, x in zip(charges, positions, strict=True))


def main() -> None:
    out = []
    out.append("(A) The nucleon as held plus in flight (MeV)")
    held_p = 2 * M_U + M_D
    held_n = M_U + 2 * M_D
    bond = M_P - held_p
    out.append(
        f"  the proton's held part 2 m_u + m_d = {held_p:.2f}, the bond's content in flight F = {bond:.2f} ({bond / M_P:.3f} of the mass)"
    )
    out.append(
        f"  the neutron's held part m_u + 2 m_d = {held_n:.2f}; with the same F: {held_n + bond:.2f} against {M_N:.2f}"
    )
    out.append(
        f"  m_n - m_p = m_d - m_u = {M_D - M_U:.2f} +- {math.hypot(M_U_ERR, M_D_ERR):.2f} against the measured {M_N - M_P:.3f}"
    )
    self_energy = 0.6 * ALPHA_HBARC / R_P
    out.append(
        f"  the electric self-energy of a uniform sphere of radius r_p: (3 / 5) alpha hbar c / r_p = {self_energy:.2f}"
    )
    out.append(
        f"  the difference less the self-energy: {M_D - M_U - self_energy:.2f} (lattice QCD's split, Borsanyi et al. 2015: 2.52 QCD, -1.00 QED, 1.51 total)"
    )
    out.append(
        f"  the steady state F = H (n / d) tau: (n / d) tau = F / H = {bond / held_p:.1f}; at one Link's round trip tau = 2 dwell = {2 * DWELL:.2f}, n / d = {bond / held_p / (2 * DWELL):.1f} per self-creation"
    )

    out.append("")
    out.append(
        "(B) The chain on the bipartite lattice, one Link between neighbours (charge radius^2 in Link^2)"
    )
    x = [-1.0, 0.0, 1.0]
    for name, charges in (
        ("u-d-u (the proton, the d at the centre)", [2 / 3, -1 / 3, 2 / 3]),
        ("u-u-d (the proton, the d at an end)", [2 / 3, 2 / 3, -1 / 3]),
        ("d-u-d (the neutron, the u at the centre)", [-1 / 3, 2 / 3, -1 / 3]),
        ("d-d-u (the neutron, the u at an end)", [-1 / 3, -1 / 3, 2 / 3]),
    ):
        out.append(f"  {name}: r^2 = {charge_radius2(charges, x):+.4f} L^2")
    link = math.sqrt(R_P**2 * 3 / 4)
    out.append(
        f"  measured: r_p^2 = {R_P**2:.4f} fm^2, r_n^2 = {R_N2:.4f} fm^2, the ratio {R_N2 / R_P**2:.3f}; the chain's ratio -1/2"
    )
    out.append(
        f"  the Link from the proton's chain, L = r_p sqrt(3/4) = {link:.3f} fm; the neutron predicted -(2/3) L^2 = {-2 / 3 * link**2:.3f} fm^2 against {R_N2}"
    )

    out.append("")
    out.append("(C) The held counts at the electron's count k = 4526 (units of the minimal mass)")
    k = 4526
    for name, m, err in (("u", M_U, M_U_ERR), ("d", M_D, M_D_ERR)):
        out.append(
            f"  {name}: {m / M_E * k:.0f} +- {err / M_E * k:.0f} (a multiple of the floor 3 within the uncertainty)"
        )
    out.append(f"  the bond's content in flight per nucleon: {bond / M_E * k:.3e} units")
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
