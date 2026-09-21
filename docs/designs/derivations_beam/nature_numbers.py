"""Section 16 of DERIVATIONS_BEAM.md: the numbers of nature against the
law's structure. Host arithmetic; no run.

(A) The minimal mass: the smallest electron count k at which the measured
    mass ratios are whole numbers of units within their published
    uncertainties (CODATA 2022), for the proton alone, the muon alone,
    both, and with the neutron.
(B) The one-constant identity k_C = G: the proton's charge per unit of
    content that nature's alpha and alpha_G would declare.
(C) The rule against numerology, applied: every product and quotient of
    two of the law's structural numbers with exponents in {1, 2}, the
    nearest to 1 / alpha, m_p / m_e and m_mu / m_e, and the expected
    number of hits within the same tolerance from the set's own density.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

# CODATA 2022 (Mohr, Newell, Taylor, Tiesinga, Rev. Mod. Phys. 2025) and
# PDG 2024 (Navas et al., Phys. Rev. D 110, 030001).
RATIOS = {
    "m_p / m_e": (1836.152673426, 0.000000032),
    "m_mu / m_e": (206.7682827, 0.0000046),
    "m_n / m_e": (1838.68366200, 0.00000074),
    "m_tau / m_e": (3477.23, 0.23),
}
ALPHA_INV = 137.035999177
ALPHA_G = 5.906e-39  # G m_p^2 / (hbar c)

# The law's structural numbers (section 16.3): counts of the cube, the
# collision table, the register's widths and the flight's rationals.
STRUCTURE = {
    "48 (the cube's group)": 48,
    "24 (its rotations)": 24,
    "6 (the Ports)": 6,
    "3 (the axes)": 3,
    "2 (the hands)": 2,
    "8 (the slots)": 8,
    "6561 (3^8 slot states)": 6561,
    "5440 (collision classes)": 5440,
    "4429 (fixed states)": 4429,
    "2132 (moving states)": 2132,
    "933 (2-cycles)": 933,
    "N = 64": 64,
    "Q = 64": 64,
    "W = 4096": 4096,
    "290 (the nucleus fan)": 290,
    "1423 (the two-slit fan)": 1423,
    "sqrt 3": math.sqrt(3),
    "pi": math.pi,
    "4 pi": 4 * math.pi,
    "110 (T_d on a heading)": 110,
    "156 (T_d on a face diagonal)": 156,
    "192 (T_d on a cube diagonal)": 192,
    "2 sqrt 2 (the Bell bound)": 2 * math.sqrt(2),
    "log2 N = 6": 6,
}


def smallest_count(names: list[str], k_max: int = 10**7) -> tuple[int, dict[str, int]]:
    """The smallest k such that k x ratio is within k x sigma of a whole
    number for every ratio named (the electron at k units)."""
    for k in range(1, k_max + 1):
        counts = {}
        for name in names:
            r, s = RATIOS[name]
            n = round(k * r)
            if abs(k * r - n) > k * s:
                break
            counts[name] = n
        else:
            return k, counts
    raise ValueError("no k below the bound")


def combinations() -> list[tuple[float, str]]:
    items = list(STRUCTURE.items())
    values: list[tuple[float, str]] = []
    exps = (1, 2)
    for i, (na, a) in enumerate(items):
        for ea in exps:
            values.append((a**ea, f"{na}^{ea}" if ea > 1 else na))
        for nb, b in items[i + 1 :]:
            for ea in exps:
                for eb in exps:
                    values.append((a**ea * b**eb, f"{na}^{ea} x {nb}^{eb}"))
                    values.append((a**ea / b**eb, f"{na}^{ea} / {nb}^{eb}"))
                    values.append((b**eb / a**ea, f"{nb}^{eb} / {na}^{ea}"))
    return values


def main() -> None:
    out = []
    out.append("(A) The minimal mass: the electron's count k (CODATA 2022 uncertainties)")
    for names in (
        ["m_p / m_e"],
        ["m_mu / m_e"],
        ["m_p / m_e", "m_mu / m_e"],
        ["m_p / m_e", "m_mu / m_e", "m_n / m_e"],
    ):
        k, counts = smallest_count(names)
        out.append(f"  {' and '.join(names)}: k = {k}; the counts {counts}")
    r, s = RATIOS["m_p / m_e"]
    out.append(
        f"  at k = 1 the proton would be 1836 units: off by {r - 1836:.6f} = {(r - 1836) / r:.2e} of the ratio, {(r - 1836) / s:.1e} sigma"
    )
    cf = Fraction(r).limit_denominator(10**7)
    out.append(f"  the best rational below 10^7: {cf.numerator} / {cf.denominator}")

    out.append("")
    out.append("(B) k_C = G with the charge in units of content: rho_p^2 = alpha / alpha_G")
    alpha = 1 / ALPHA_INV
    rho_p = math.sqrt(alpha / ALPHA_G)
    out.append(
        f"  rho_p = sqrt(alpha / alpha_G) = {rho_p:.4e} per unit of content (e in units of sqrt G m_p)"
    )
    out.append(
        f"  rho_e = -rho_p m_p / m_e = {-rho_p * r:.4e} (the neutrality of matter); the register's are [1, 1] and -15"
    )
    out.append(f"  F_e / F_g for e and p = alpha m_p / (alpha_G m_e) = {alpha * r / ALPHA_G:.3e}")

    out.append("")
    out.append("(C) The rule against numerology, applied")
    values = combinations()
    out.append(f"  combinations of two structural numbers with exponents 1 and 2: {len(values)}")
    for name, target in (
        ("1 / alpha", ALPHA_INV),
        ("m_p / m_e", r),
        ("m_mu / m_e", RATIOS["m_mu / m_e"][0]),
    ):
        near = sorted(values, key=lambda t: abs(math.log(t[0] / target)))[:3]
        tol = 3e-3
        hits = sum(1 for v, _ in values if abs(math.log(v / target)) < tol)
        # the density of the set near the target: values within a factor e^0.5
        dens = sum(1 for v, _ in values if abs(math.log(v / target)) < 0.5) / 1.0
        expected = dens * 2 * tol
        out.append(
            f"  {name} = {target:.6f}: nearest {near[0][1]} = {near[0][0]:.4f} ({near[0][0] / target - 1:+.2%}),"
            f" then {near[1][1]} = {near[1][0]:.4f} ({near[1][0] / target - 1:+.2%}), {near[2][1]} = {near[2][0]:.4f} ({near[2][0] / target - 1:+.2%})"
        )
        out.append(
            f"    hits within {tol:.1%}: {hits}; expected from the set's density ({dens:.0f} values within a factor e^0.5): {expected:.2f}"
        )

    out.append("")
    out.append("(D) q of nature against the law's 0: Planck 2018 Omega_m = 0.315, Omega_Lambda = 0.685")
    out.append(
        f"  q_0 = Omega_m / 2 - Omega_Lambda = {0.315 / 2 - 0.685:.3f}; the law's Milne 0 and the register's -0.108 +- 0.25"
    )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
