"""The stable body's functional and the binding bound (docs/ALGEBRA.md, The stable body, "The functional and the dilation"; the paper's Section 7.2, S.13 and Section 10.3, S.38): the pressure's coefficient num / (3 den) is rule3's R_a / w; on a Gaussian body the functional F = a / R^2 - b / R^3 - c / R has its critical points at c R^2 - 2 a R + 3 b = 0, the wide one a minimum, the narrow one a saddle, none where 3 b c > a^2, the collapse, and Pekar's F = a / R^2 - c / R one minimum at R = 2 a / c; a body's binding per quantum is bounded by its self-level at one Node, 3 G(0) C W / (Gamma E) with G(0) Watson's integral of the simple cubic lattice (0.2527, in Glasser and Zucker's closed form), 0.76, and for a uniform ball of r Links the centre's self-level is 1.5 and the share-weighted mean 1.2 times the whole count's far level 3 / (4 pi r), 0.36 and 0.29.

Usage: `python tools/derivations/bodies.py` prints them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent)
)  # the folder's root, rule3.py, beside this module
import rule3  # noqa: E402


def pressure_coefficient(num: int = 2, den: int = 3) -> float:
    """num / (3 den), the coefficient of the Link sum in F (S.13, the paper's Eq. (12)), rule3's R_a / w at the vacuum's paces: 2 / 9 at [2, 3]."""
    wall, reads, _ = rule3.coefficients(num, den)
    return reads[0] / wall


def functional_critical_points(a: float = 1.0, b: float = 0.1, c: float = 1.0) -> list[float]:
    """F(R) = a / R^2 - b / R^3 - c / R: F' = 0 is c R^2 - 2 a R + 3 b = 0; [the count of critical points where a^2 > 3 b c, 2; the sign of F'' at the wide one, +1, a minimum; at the narrow one, -1, a saddle; the count where 3 b c > a^2, 0, the collapse; Pekar's R = 2 a / c at b = 0 and the sign of F'' there, +1]."""
    discriminant = a * a - 3 * b * c

    def second(radius: float, hollow: float) -> float:
        return 6 * a / radius**4 - 12 * hollow / radius**5 - 2 * c / radius**3

    wide, narrow = (a + math.sqrt(discriminant)) / c, (a - math.sqrt(discriminant)) / c
    collapsed = a * a - 3 * (b * 10) * c  # a hollow ten times stronger, 3 b c > a^2
    count_collapsed = 0 if collapsed < 0 else 2
    pekar = 2 * a / c
    return [
        2.0,
        math.copysign(1, second(wide, b)),
        math.copysign(1, second(narrow, b)),
        count_collapsed,
        pekar,
        math.copysign(1, second(pekar, 0.0)),
    ]


def watson_green_at_the_source() -> float:
    """G(0) of the simple cubic lattice's Laplacian with the unit source: Watson's integral (1 / (2 pi)^3) INTEGRAL d^3k / (6 - 2 SUM_a cos k_a) in Glasser and Zucker's closed form, W_S / 6 with W_S = (sqrt 6 / (32 pi^3)) Gamma(1 / 24) Gamma(5 / 24) Gamma(7 / 24) Gamma(11 / 24): 0.252731."""
    watson = math.sqrt(6) / (32 * math.pi**3) * math.prod(math.gamma(n / 24) for n in (1, 5, 7, 11))
    return watson / 6


def uniform_ball_factors(steps: int = 100_000) -> list[float]:
    """A uniform ball's level over the whole count's far level at its radius, (3 R^2 - r^2) / (2 R^2) inside: [at the centre, 1.5; the mass-weighted mean, INTEGRAL (3 - x^2) / 2 x 3 x^2 dx over x in [0, 1], 1.2]."""
    mean = sum((3 - x * x) / 2 * 3 * x * x / steps for x in ((i + 0.5) / steps for i in range(steps)))
    return [1.5, mean]


def binding_bound() -> list[float]:
    """S.38 (c): [3 G(0), the one-Node self-level per C W / (Gamma E), 0.76; the uniform ball's share-weighted mean 1.2 x 3 / (4 pi), per C W / (Gamma E r), 0.29; its centre's 1.5 x 3 / (4 pi), 0.36]."""
    centre, mean = uniform_ball_factors()
    far = 3 / (4 * math.pi)
    return [3 * watson_green_at_the_source(), mean * far, centre * far]


if __name__ == "__main__":
    print("the pressure's coefficient at [2, 3]:", pressure_coefficient())
    print("the functional's critical points:", functional_critical_points())
    print("G(0):", watson_green_at_the_source())
    print(
        "the binding bound: 3 G(0), the ball's mean, its centre:", [round(v, 4) for v in binding_bound()]
    )
