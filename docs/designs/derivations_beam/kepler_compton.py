"""Kepler's laws and Compton's shift from the law's declared integers, the
pins before any run (DERIVATIONS_BEAM.md 21.5, rows 58 and 59).

A host check of the section's formulas, not a run: form B's pace on the
registered orbit worlds of series D, the periods and the exponent on the
plane and in space, the apsidal angle of the plane's 1 / r force, and the
Compton relation from the exact square of covariant-readings-v1 at the fan's
directions. Integers and fractions throughout; the two irrationals of the
formulas (sqrt 3 and sqrt 2) are carried by `decimal` at 30 digits and
every pinned integer is a floor of them.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from math import isqrt

getcontext().prec = 30
Q = 64
PI = Decimal("3.14159265358979323846264338328")
SQRT3 = Decimal(3).sqrt()
SQRT2 = Decimal(2).sqrt()


def t_d(direction: tuple[int, int, int]) -> int:
    """The direction's resolution T_D = isqrt(3 |D|^2 Q^2), the flight table's."""
    return isqrt(3 * sum(c * c for c in direction) * Q * Q)


def pace_form_b(p: tuple[int, int, int], s: int, m: int) -> Fraction:
    """Form B's Manhattan pace |p|_1 S_1 Q / (Q S M S_1 Q + |p|_1 T_D) on the
    primitive direction of p (FORM.md section 3), Links per interval."""
    g = 0
    for c in p:
        g = _gcd(g, abs(c))
    direction = tuple(c // g for c in p)
    s1 = sum(abs(c) for c in direction)
    p1 = sum(abs(c) for c in p)
    return Fraction(p1 * s1 * Q, Q * s * m * s1 * Q + p1 * t_d(direction))


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def euclid_of_manhattan(v_m: Fraction, direction: tuple[int, int, int]) -> Decimal:
    s1 = sum(abs(c) for c in direction)
    norm = Decimal(sum(c * c for c in direction)).sqrt()
    return Decimal(v_m.numerator) / Decimal(v_m.denominator) * norm / s1


def kepler_plane() -> None:
    print("(A) Series D's plane, S = 32, m = 1, q = 12 rows per interval, p = 576 label units (n = 9):")
    for direction in ((0, 1, 0), (1, 1, 0)):
        p = tuple(576 * c for c in direction) if direction == (0, 1, 0) else (407, 407, 0)
        v_m = pace_form_b(p, 32, 1)
        v_e = euclid_of_manhattan(v_m, direction)
        print(
            f"  form B on {direction}: Manhattan pace {v_m} = {float(v_m):.4f}, Euclidean {v_e:.4f} Links per interval"
        )
    v = pace_form_b((0, 576, 0), 32, 1)
    vd = Decimal(v.numerator) / Decimal(v.denominator)
    for r in (12, 24):
        t = 2 * PI * r / vd
        print(
            f"  the analytic period at r = {r}: 2 pi r / v = {t:.1f} intervals (today's drive: {2 * PI * r / Decimal('0.2195'):.0f})"
        )
    print(
        "  the exponent of T against r on the plane: T(24) / T(12) = 2 exactly (a 1 / r force), the ratio of the squares 4"
    )
    apsidal = PI / SQRT2
    print(
        f"  the apsidal angle of a 1 / r force (near-circular): pi / sqrt 2 = {apsidal:.4f} rad = {apsidal * 180 / PI:.2f} degrees,"
    )
    print(
        f"  so the perihelion moves by 2 x that less 360 = {(2 * apsidal * 180 / PI - 360):.2f} degrees per radial period (the plane's own law, not the lattice's)"
    )
    print()


def kepler_space() -> None:
    print(
        "(B) Kepler in space (the shell mean, series E's fan: q = 290 rows per interval, one row per direction per interval):"
    )
    print(
        "  a = -q / (4 pi S r^2) Links per interval^2 (3.3: G M_B = q / (4 pi S)); the circular orbit n = sqrt(S q / (4 pi r)), T = 2 pi r^(3/2) sqrt(4 pi S / q)"
    )
    q = 290
    for s in (512, 8192):
        ts = []
        for r in (12, 24):
            n = (Decimal(s * q) / (4 * PI * r)).sqrt()
            p = int(Q * n)
            v = n / s
            t = 2 * PI * r / v
            ts.append(t)
            print(
                f"  S = {s}, r = {r}: n = {n:.2f}, p = Q n = {p} label units, v = {v:.4f} Links per interval ({v / (1 / SQRT3):.3f} c), T = {t:.0f}"
            )
        print(
            f"  S = {s}: T(24) / T(12) = {ts[1] / ts[0]:.4f} against 2^(3/2) = {Decimal(2) ** Decimal('1.5'):.4f}; the exponent log2 of the ratio = {(ts[1] / ts[0]).ln() / Decimal(2).ln():.4f}"
        )
    print()


def compton() -> None:
    print(
        "(C) Compton from the exact square W = E'_0^2 + 3 p . p: a row of momentum k absorbed by a body at rest, a row of momentum k' released at the angle theta;"
    )
    print(
        "  W before = (E'_0 + sqrt 3 k)^2 with the row's energy sqrt 3 k in E' units on the pair c^2 = [1, 3]; after: (E'_0 + sqrt 3 k - sqrt 3 k')^2 = E'_0^2 + 3 |k - k'|^2"
    )
    print(
        "  => 1 / k' - 1 / k = sqrt 3 (1 - cos theta) / E'_0, i.e. lambda' - lambda = (h / (Q S M c)) (1 - cos theta) with lambda = h / k, c = 1 / sqrt 3, exactly."
    )
    e0 = 64  # Q S M with S = 1, M = 1
    h, s = 1, 16
    k = h * s
    print(
        f"  the declared world: Q S M = {e0} (S = 1, M = 1), the lamp's quantum h = {h} at the turn s = {s} steps per self-creation, so k = h s = {k} label units;"
    )
    print(
        "  the fan of the re-emitter: the six headings (cos theta = 1, 0, 0, 0, 0, -1) and the twelve face diagonals (cos theta = +-1/sqrt 2 or 0)"
    )
    for name, cos_t in (
        ("theta = 0 (+x)", Decimal(1)),
        ("theta = 45 deg (face diagonal forward)", 1 / SQRT2),
        ("theta = 90 deg (+-y, +-z)", Decimal(0)),
        ("theta = 135 deg (face diagonal back)", -1 / SQRT2),
        ("theta = 180 deg (-x)", Decimal(-1)),
    ):
        inv = Decimal(1) / k + SQRT3 * (1 - cos_t) / e0
        kp = 1 / inv
        sp = int(kp / h)
        recoil = ((k - kp * cos_t) ** 2 + (kp * (1 - cos_t * cos_t).sqrt()) ** 2).sqrt()
        print(
            f"  {name}: k' = {kp:.3f} label units, the released turn s' = floor(k' / h) = {sp} steps (from {s}), the body's recoil |p| = {recoil:.2f} label units ({recoil / e0:.3f} of Q S M)"
        )
    gamma = Fraction(96, 55)
    print(
        f"  at the heading's own c = 32 / 55 the row's energy is (96 / 55) k (17.6 M7) and gamma^2 - 3 = {gamma * gamma - 3} = {float(gamma * gamma - 3):.4f}:"
    )
    print(
        "  the relation then holds to first order in (k - k') / k with the residual (gamma^2 - 3) (k - k')^2 / (2 E'_0 gamma) in k', second order (the error term at the heading's c)."
    )
    for name, cos_t in (("90 deg", Decimal(0)), ("180 deg", Decimal(-1))):
        g = Decimal(96) / Decimal(55)
        # solve 2 E0 g (k - k') + g^2 (k-k')^2 = 3 k^2 + 3 k'^2 - 6 k k' cos by bisection on k'
        lo, hi = Decimal(1), Decimal(k)
        for _ in range(200):
            mid = (lo + hi) / 2
            lhs = 2 * e0 * g * (k - mid) + g * g * (k - mid) ** 2
            rhs = 3 * k * k + 3 * mid * mid - 6 * k * mid * cos_t
            if lhs > rhs:
                lo = mid
            else:
                hi = mid
        print(
            f"  at {name} with the heading's c: k' = {lo:.3f} (against {1 / (Decimal(1) / k + SQRT3 * (1 - cos_t) / e0):.3f} on the pair), the floor of k' / h the same or one less"
        )
    print()


if __name__ == "__main__":
    kepler_plane()
    kepler_space()
    compton()
