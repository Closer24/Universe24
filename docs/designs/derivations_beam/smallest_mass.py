"""Section 16.2 (d) of DERIVATIONS_BEAM.md: the smallest mass per kind.
Host arithmetic; no run.

(A) A family's charge per unit of content is a reduced pair [n, d]; a
    body's charge rho x M is whole iff d divides M, so the smallest
    content with a whole charge is d.
(B) The quark tower at the floors (u and d three units each) and the
    smallest electron counts k at which the proton's and the neutron's
    counts are multiples of 3 within CODATA 2022 (the binding carrying
    no held content).
"""

from __future__ import annotations

import math
from pathlib import Path

RATIOS = {
    "m_p / m_e": (1836.152673426, 0.000000032),
    "m_n / m_e": (1838.68366200, 0.00000074),
    "m_mu / m_e": (206.7682827, 0.0000046),
}
FAMILIES = {
    "e (the catalog)": (-15, 1),
    "p (the catalog)": (1, 1),
    "beta, w (the catalog)": (-7344, 1),
    "u (records 249, 251)": (2, 3),
    "d (records 249, 251)": (-1, 3),
    "a family at [-5, 69]": (-5, 69),
}


def floor_of(n: int, d: int) -> int:
    g = math.gcd(abs(n), d)
    return d // g


def smallest_k(names: list[str], mod3: list[str], k_max: int = 10**7) -> tuple[int, dict[str, int]]:
    for k in range(1, k_max + 1):
        counts = {}
        for name in names:
            r, s = RATIOS[name]
            c = round(k * r)
            if abs(k * r - c) > k * s or (name in mod3 and c % 3):
                break
            counts[name] = c
        else:
            return k, counts
    raise ValueError


def main() -> None:
    out = ["(A) The floor of a charged family: the reduced denominator of rho"]
    for name, (n, d) in FAMILIES.items():
        out.append(
            f"  {name}: rho = [{n}, {d}], the smallest content with a whole charge {floor_of(n, d)}"
        )
    out.append("")
    out.append(
        "(B) The quark tower at the floors: u = 3, d = 3; the proton u u d = 9 (charge 2/3 + 2/3 - 1/3 = 1),"
    )
    out.append(
        "    the neutron u d d = 9 (charge 0), m_n / m_p = 1 exactly (nature 1.00138), m_p / m_e = 9 at e = 1 (nature 1836.15)"
    )
    for names, mod3 in (
        (["m_p / m_e"], ["m_p / m_e"]),
        (["m_p / m_e", "m_n / m_e"], ["m_p / m_e", "m_n / m_e"]),
        (["m_p / m_e", "m_n / m_e", "m_mu / m_e"], ["m_p / m_e", "m_n / m_e"]),
    ):
        k, counts = smallest_k(names, mod3)
        out.append(
            f"  {' and '.join(names)} with the nucleons' counts multiples of 3: k = {k}; {counts}"
        )
    r = RATIOS["m_p / m_e"][0]
    out.append(
        f"  at k = 4526 (section 16.2 (a)) the proton's count {round(4526 * r)} mod 3 = {round(4526 * r) % 3}: not a sum of quark floors"
    )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
