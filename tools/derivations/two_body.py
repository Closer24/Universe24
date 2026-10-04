"""The pair of two bound records, a hypothesis under its own name (ALGEBRA.md; the mathematician's derivation, #1836 comment 5975201670, the advisor's second 5975404293): a bound record's inertia is m* = 3 tan omega_0 (the band's curvature at rest, 1 / m* = d^2 omega / dk^2 at k = 0) and its rest content T sin omega_0; two bound records of inertias m_1 and m_2 are one record of two parts, the centre's part with 3 tan omega_M = m_1 + m_2 carrying the pair's whole rest and count, and the relative part with 3 tan omega_mu = m_1 m_2 / (m_1 + m_2), a part of the record and no family of quanta, laid for its inertia alone about the pinned centre and reading the sign holder with the charges' product, so that the bound modes of S.60 (a) hold with m* replaced by mu: -(mu / m_e) Z^2 / (2 n^2) hartree. The rest contents add in sin omega and the inertias in tan omega: at [2, 3] two records hold 2 sin omega_e = 1.4907 T against sin omega_M + sin omega_mu = 1.4008 T, and at nature's gaps sin omega_M is the two quanta's rest to O(omega^3) while a relative part counted as a quantum would add half a rest, which nature's pair has not.

Usage: `python tools/derivations/two_body.py` prints the pairs at [2, 3], the reduced masses and the levels against nature.
"""

from __future__ import annotations

import math

ELECTRON_MASSES = {
    "p": 1836.15267,
    "d": 3670.48297,
    "mu": 206.76828,
    "e": 1.0,
}  # CODATA, over the electron's
HARTREE_EV = 27.211386


def inertia(num: int, den: int) -> float:
    """m* = 3 tan omega_0 from cos omega_0 = num / den."""
    return 3 * math.tan(math.acos(num / den))


def curvature(num: int, den: int, step: float = 1e-4) -> float:
    """1 / m* as the band's second derivative at k = 0 by finite differences, the second method for `inertia`."""
    nu = num / den

    def omega(k: float) -> float:
        return math.acos(nu * (2 + math.cos(k)) / 3)

    return (omega(step) - 2 * omega(0) + omega(-step)) / (step * step)


def pair_rotations(m_1: float, m_2: float) -> list[float]:
    """[tan omega_M, tan omega_mu, cos omega_M, cos omega_mu] of the centre's and the relative part from two inertias."""
    centre, relative = (m_1 + m_2) / 3, (m_1 * m_2 / (m_1 + m_2)) / 3
    return [centre, relative, 1 / math.sqrt(1 + centre * centre), 1 / math.sqrt(1 + relative * relative)]


def composed_pairs_at_two_three(den: int = 6000) -> list[float]:
    """[the relative part's num, the centre's num] of two [2, 3] records at the declared den, by the floats (the loader's `universe.composed_pair` gives the same integers by the division act, the second method)."""
    m = inertia(2, 3)
    _, _, cos_centre, cos_relative = pair_rotations(m, m)
    return [round(den * cos_relative), round(den * cos_centre)]


def inertia_ratio(den: int = 6000) -> list[float]:
    """[3 tan omega of the relative pair over the record's, of the centre's over the record's] at [2, 3] and den 6,000: 1 / 2 and 2 within the pair's rounding."""
    relative, centre = composed_pairs_at_two_three(den)
    return [inertia(relative, den) / inertia(2, 3), inertia(centre, den) / inertia(2, 3)]


def reduced(first: str, second: str) -> float:
    """mu / m_e of two of nature's records by their masses over the electron's."""
    return (
        ELECTRON_MASSES[first]
        * ELECTRON_MASSES[second]
        / (ELECTRON_MASSES[first] + ELECTRON_MASSES[second])
    )


def level(mu: float, charge: int = 1, n: int = 1) -> float:
    """-mu Z^2 / (2 n^2) hartree, S.60 (a) with the relative part's inertia."""
    return -mu * charge * charge / (2 * n * n)


def reduced_masses() -> list[float]:
    """mu / m_e for hydrogen, deuterium, muonium, positronium and muonic hydrogen."""
    return [
        reduced("p", "e"),
        reduced("d", "e"),
        reduced("mu", "e"),
        reduced("e", "e"),
        reduced("mu", "p"),
    ]


def ground_levels() -> list[float]:
    """The 1s levels in hartree for hydrogen, deuterium, muonium and positronium."""
    return [level(mu) for mu in reduced_masses()[:4]]


def against_nature() -> list[float]:
    """[the hydrogen to deuterium 1s-2s isotope shift in meV (nature 2.775, 670.994 GHz), positronium's 1s in eV (nature -6.80) and its 1s-2s in eV (nature 5.10), muonic hydrogen's 1s in keV (nature -2.53)]."""
    shift = (level(reduced("d", "e"), n=2) - level(reduced("d", "e"))) - (
        level(reduced("p", "e"), n=2) - level(reduced("p", "e"))
    )
    positronium = reduced("e", "e")
    return [
        shift * HARTREE_EV * 1000,
        level(positronium) * HARTREE_EV,
        (level(positronium, n=2) - level(positronium)) * HARTREE_EV,
        level(reduced("mu", "p")) * HARTREE_EV / 1000,
    ]


def rest_contents() -> list[float]:
    """[2 sin omega_e, sin omega_M + sin omega_mu] in units of T for two [2, 3] records: the rest adds in sin omega, the inertia in tan omega; the centre's part alone carries the pair's rest at nature's gaps, to O(omega^3)."""
    m = inertia(2, 3)
    tan_centre, tan_relative, _, _ = pair_rotations(m, m)
    sine = lambda t: t / math.sqrt(1 + t * t)  # noqa: E731
    return [2 * sine(m / 3), sine(tan_centre) + sine(tan_relative)]


if __name__ == "__main__":
    print(
        "m* at [2, 3], by 3 tan omega_0 and by the band's curvature:",
        round(inertia(2, 3), 4),
        round(1 / curvature(2, 3), 4),
    )
    print(
        "tan omega_M, tan omega_mu, cos omega_M, cos omega_mu:",
        [round(v, 4) for v in pair_rotations(inertia(2, 3), inertia(2, 3))],
    )
    print("the relative part's and the centre's num at den 6,000:", composed_pairs_at_two_three())
    print("the inertia ratios:", [round(v, 4) for v in inertia_ratio()])
    print("mu / m_e: H, D, muonium, positronium, muonic H:", [round(v, 6) for v in reduced_masses()])
    print("1s hartree: H, D, muonium, positronium:", [round(v, 6) for v in ground_levels()])
    print(
        "H to D 1s-2s shift meV, positronium 1s eV, 1s-2s eV, muonic H 1s keV:",
        [round(v, 4) for v in against_nature()],
    )
    print(
        "rest contents at [2, 3], 2 sin omega_e against sin omega_M + sin omega_mu:",
        [round(v, 4) for v in rest_contents()],
    )
