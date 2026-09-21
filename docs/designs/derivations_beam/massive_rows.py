"""massive-rows-v1: the numbers of DERIVATIONS_BEAM.md section 23 (the
massive row's pace, wavelength and dispersion; the two-slit pin), a host
check of the section's formulas, not a run.

Integers and fractions; the irrationals of the two-path law (the Euclidean
paths) in `decimal` at 30 digits, every pinned integer a floor or a rounded
pixel of them, as 7.1's numbers were.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from math import isqrt

getcontext().prec = 30
Q, N = 64, 64
SQRT3 = Decimal(3).sqrt()


def energy(e0: int, p: tuple[int, int, int]) -> tuple[int, int]:
    """W = E'_0^2 + 3 p . p and E' the largest integer with E'^2 <= W."""
    w = e0 * e0 + 3 * sum(c * c for c in p)
    return w, isqrt(w)


def main() -> None:
    print(
        "(A) The declared world slits_matter: S = 1, the family `matter` of content M = 64 units per row, so E'_0 = Q S M = 4096;"
    )
    print(
        "    the action h = 1024, the momentum p = 220 label units along each fan direction (the same |p| on every row of a record)."
    )
    e0 = 4096
    h, p = 1024, 220
    w, e = energy(e0, (p, 0, 0))
    print(
        f"  W = {w}, E' = isqrt(W) = {e} ({e}^2 = {e * e} <= W < {(e + 1) ** 2}); gamma = E' / E'_0 = {Fraction(e, e0)} = {e / e0:.5f}"
    )
    v = Fraction(p, e)
    print(
        f"  the pace p / E' = {v} = {float(v):.5f} Links per interval = {float(v) * float(SQRT3):.4f} c; the photon's 32 / 55 = 0.5818"
    )
    lam = Fraction(h, p)
    print(
        f"  de Broglie: the turn per Link |p| N / h = {Fraction(p * N, h)} steps (by_drive(acc, {p * N}, {h}) per Link), lambda = h / |p| = {lam} = {float(lam):.4f} Links (the photon world's 4.654)"
    )
    print(
        f"  the small-momentum expansion: E' - E'_0 = {e - e0} against 3 p^2 / (2 E'_0) = {Fraction(3 * p * p, 2 * e0)} = {3 * p * p / (2 * e0):.2f}; the next term -9 p^4 / (8 E'_0^3) = {-9 * p**4 / (8 * e0**3):.4f}"
    )
    print(
        "  the dispersion's grain: E'^2 <= W < (E' + 1)^2, so the pace |p| / E' is within a part in E' of |p| / sqrt W: a part in 4113 here"
    )
    print()
    print(
        "(B) The two-path law of 7.1 with lambda = h / |p| (slits_low's geometry: s = 10, D = 44, the screen's fan by angle):"
    )
    D, s = Decimal(44), Decimal(10)
    lam_d = Decimal(h) / Decimal(p)
    # the first bright fringes: sqrt(D^2 + (y + 5)^2) - sqrt(D^2 + (y - 5)^2) = j lambda
    for j in (1,):
        lo, hi = Decimal(0), Decimal(60)
        for _ in range(100):
            mid = (lo + hi) / 2
            diff = (D * D + (mid + s / 2) ** 2).sqrt() - (D * D + (mid - s / 2) ** 2).sqrt()
            if diff < j * lam_d:
                lo = mid
            else:
                hi = mid
        print(
            f"  the bright fringe j = {j} at |y| = {lo:.1f} about the centre, the pixels {60 - lo:.1f} and {60 + lo:.1f} (7.1 at the photon's lambda: 23.3, the pixels 36.7 and 83.3)"
        )
    print(
        f"  the paraxial spacing lambda D / s = {lam_d * D / s:.1f} pixels (not the check: y / D is 0.5 at the first fringe)"
    )
    print()
    print(
        "(C) The arrival: the flight time L / v for the centre pixel and the edge of the first fringe:"
    )
    for name, y in (("the centre", Decimal(0)), ("the first fringe", Decimal("23.3"))):
        L = (D * D + (y + s / 2) ** 2).sqrt()
        L2 = (D * D + (y - s / 2) ** 2).sqrt()
        t1 = L / (Decimal(v.numerator) / Decimal(v.denominator))
        t2 = L2 / (Decimal(v.numerator) / Decimal(v.denominator))
        print(
            f"  {name}: the paths {L:.2f} and {L2:.2f} Links, the arrivals {t1:.0f} and {t2:.0f} intervals after the birth (the photon's {L / Decimal(32) * 55:.0f} and {L2 / Decimal(32) * 55:.0f})"
        )
    print()
    print(
        "(D) The confrontation's numbers (dimensionless): Jonsson 1961 (50 keV electrons, the slits 0.3 micrometre wide, 1 micrometre apart):"
    )
    # relativistic de Broglie wavelength at 50 keV: lambda = h / sqrt(2 m E (1 + E / (2 m c^2)))
    me_c2 = Decimal("510998.95")  # eV
    E = Decimal(50000)
    hc = Decimal("1239.84198")  # eV nm
    pc = (2 * me_c2 * E * (1 + E / (2 * me_c2))).sqrt()
    lam_nm = hc / pc
    print(
        f"  lambda = h c / (p c) with p c = sqrt(2 m c^2 E (1 + E / (2 m c^2))) = {pc:.1f} eV: lambda = {lam_nm * 1000:.3f} pm; lambda / s = {lam_nm * Decimal('1e-9') / Decimal('1e-6'):.2e} (the law's world: {float(lam) / 10:.3f})"
    )
    print(
        "  Tonomura 1989: 50 kV electrons through an electron biprism, the pattern built one electron at a time (the law's wheel, one click per birth)."
    )


if __name__ == "__main__":
    main()
