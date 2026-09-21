"""Section 19.5 of DERIVATIONS_BEAM.md: the rest of the masses as readings
after a detector. Host arithmetic on PDG 2024 numbers; no run.

(A) The hadrons against "one content in flight per bond": the pion
    (two bodies, one contact) and the nucleon (three bodies, two
    contacts on a chain, three on the face-diagonal triangle).
(B) The leptons: Koide's relation as a coincidence, with its precision.
(C) The neutrino: the law's massless family against oscillations.
"""

from __future__ import annotations

import math
from pathlib import Path

M_U, M_D = 2.16, 4.70  # MeV
M_PION, M_PROTON, M_RHO = 139.57, 938.27, 775.26
M_E, M_MU, M_TAU = 0.51099895, 105.6583755, 1776.93


def main() -> None:
    out = ["(A) The hadrons against one content in flight per contact (MeV)"]
    held_pi = M_U + M_D
    f_pi = M_PION - held_pi
    held_n = 2 * M_U + M_D
    f_n = M_PROTON - held_n
    out.append(
        f"  the pion u d-bar: held {held_pi:.2f}, in flight {f_pi:.1f}, one contact: F per contact {f_pi:.1f}"
    )
    for contacts, shape in ((2, "the chain"), (3, "the triangle")):
        out.append(
            f"  the proton on {shape}: held {held_n:.2f}, in flight {f_n:.1f}, {contacts} contacts: F per contact {f_n / contacts:.1f}"
        )
    out.append(
        f"  the pion's F per contact against the chain's: {f_pi / (f_n / 2):.2f}; a nucleon at the pion's F per contact: {held_n + 2 * f_pi:.0f} against {M_PROTON:.0f}"
    )
    out.append(
        f"  the rho u d-bar (the same pair, another state): {M_RHO:.1f}, in flight {M_RHO - held_pi:.1f}: two masses for one pair and one contact"
    )
    out.append(
        f"  the steady-state form F = H (n / d) tau with one (n / d) tau: the pion at the nucleon's {f_n / held_n:.0f}: {held_pi * (1 + f_n / held_n):.0f} against {M_PION:.1f}"
    )

    out.append("")
    out.append("(B) The leptons: Koide's relation")
    s = M_E + M_MU + M_TAU
    r = (math.sqrt(M_E) + math.sqrt(M_MU) + math.sqrt(M_TAU)) ** 2
    out.append(
        f"  (m_e + m_mu + m_tau) / (sqrt m_e + sqrt m_mu + sqrt m_tau)^2 = {s / r:.6f} against 2 / 3 = {2 / 3:.6f}: {s / r / (2 / 3) - 1:+.1e}"
    )
    out.append(
        f"  the ratios m_mu / m_e = {M_MU / M_E:.4f}, m_tau / m_e = {M_TAU / M_E:.2f}: free families of the law, no bond, no path"
    )

    out.append("")
    out.append("(C) The neutrino")
    out.append(
        "  the law's nu: quantum 0, no charge, a free family of declared content; the register's 0"
    )
    out.append(
        "  nature: the squared mass differences 7.4 x 10^-5 and 2.5 x 10^-3 eV^2 (oscillations, PDG 2024), so at least one mass above 0.05 eV; KATRIN 2022: m below 0.8 eV"
    )
    out.append(
        "  a massless nu (content 0) is refuted by the oscillations; a content above 0 is an input, at least 10^-7 of the electron's"
    )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
