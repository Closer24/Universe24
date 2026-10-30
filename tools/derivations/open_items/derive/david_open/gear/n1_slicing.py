"""N1, the slicing is a law: one weight w in d_mu ((-g)^w g^(mu nu)) = 0, read in the course and in the static field.

The course: g_00 = -N^2, g_ij = a^2 delta_ij, so -g = N^2 a^6 and g^00 = -1 / N^2. The time row of the law makes
(N^2 a^6)^w / N^2 constant, so N goes as a^(3f) with (2w - 2) 3f + 6w = 0: f = w / (1 - w).

The static field at first order: g_00 = -(1 - 2U), g_ij = (1 + 2 gamma U) delta_ij. Then (-g)^w g^ij is
delta^ij (1 + (w (6 gamma - 2) - 2 gamma) U), and the space rows of the law ask w (6 gamma - 2) = 2 gamma:
gamma = w / (3w - 1).

The free count: each board count x^nu a free clock, its wave law Box_g x^nu = (-g)^(-1/2) d_mu ((-g)^(1/2) g^(mu nu)) = 0,
is the weight 1/2: the measure's own, the four-volume N a^3.

Checks, all exact with fractions and no root (the owner's word to David of 2026-10-30, 02:2x UTC): the two lines at
every w = k/12; the static row again from the metric itself, as the first-order coefficient of grad U in the divergence
of (-g)^w g^ij, each factor's first-order term taken from its polynomial (-g = (1 - 2U)(1 + 2 gamma U)^3) and its
series ((1 + x)^w = 1 + w x, (1 + x)^-1 = 1 - x), which is 0 at the line's gamma and 4w - 2 at gamma = 1, so 0 there
only at w = 1/2; the free count's weight.

Usage: python3 -I n1_slicing.py
"""

from fractions import Fraction as F


def course_f(w):
    f = w / (1 - w)
    assert (2 * w - 2) * 3 * f + 6 * w == 0
    return f


def static_gamma(w):
    gamma = w / (3 * w - 1)
    assert w * (6 * gamma - 2) == 2 * gamma
    return gamma


def first_order(poly_a, poly_b):
    """The constant and the U term of a product of two polynomials in U, each given as (constant, U term)."""
    return poly_a[0] * poly_b[0], poly_a[0] * poly_b[1] + poly_a[1] * poly_b[0]


def static_row(w, gamma):
    """The coefficient of grad U in d_j ((-g)^w g^jx) at first order, from the metric itself."""
    minus_g = (F(1), F(-2))
    for _ in range(3):
        minus_g = first_order(minus_g, (F(1), 2 * gamma))
    assert minus_g[0] == 1
    power = (F(1), w * minus_g[1])
    inverse = (F(1), -2 * gamma)
    return first_order(power, inverse)[1]


def main():
    print("w      f = w/(1-w)   gamma = w/(3w-1)   the static row from the metric: at that gamma, at gamma = 1")
    for k in range(1, 12):
        w = F(k, 12)
        f = course_f(w)
        gamma = static_gamma(w) if 3 * w != 1 else None
        row = static_row(w, gamma) if gamma is not None else None
        einstein = static_row(w, F(1))
        assert einstein == 4 * w - 2
        print(f"{str(w):6} {str(f):13} {str(gamma) if gamma is not None else 'none (w = 1/3)':18} "
              f"{str(row) if row is not None else '-':>4}  {str(einstein):>5}")
    print("w = 1/2 (the free count, Box_g x = 0):", f"f = {course_f(F(1, 2))}, gamma = {static_gamma(F(1, 2))}")
    print("f = 1/3 (the square cell):", f"w = {F(1, 3) / (1 + F(1, 3))}, gamma = {static_gamma(F(1, 4))}")


if __name__ == "__main__":
    main()
