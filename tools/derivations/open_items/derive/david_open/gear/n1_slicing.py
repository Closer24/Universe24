"""N1, the slicing is a law: one weight w in d_mu ((-g)^w g^(mu nu)) = 0, read in the course and in the static field.

The course: g_00 = -N^2, g_ij = a^2 delta_ij, so -g = N^2 a^6 and g^00 = -1 / N^2. The time row of the law makes
(N^2 a^6)^w / N^2 constant, so N goes as a^(3f) with (2w - 2) 3f + 6w = 0: f = w / (1 - w).

The static field at first order: g_00 = -(1 - 2U), g_ij = (1 + 2 gamma U) delta_ij. Then (-g)^w g^ij is
delta^ij (1 + (w (6 gamma - 2) - 2 gamma) U), and the space rows of the law ask w (6 gamma - 2) = 2 gamma:
gamma = w / (3w - 1).

The free count: each board count x^nu a free clock, its wave law Box_g x^nu = (-g)^(-1/2) d_mu ((-g)^(1/2) g^(mu nu)) = 0,
is the weight 1/2: the measure's own, the four-volume sqrt(-g) = N a^3.

Checks: the two lines exactly with fractions at every w = k/12; the static line again from the metric itself in
floats (the divergence of (-g)^w g^ij by central differences about a point mass, at U = 1e-6, over U), which is 0 at
the line's gamma to the differences' size and of order 1 at gamma = 1 unless w = 1/2; the free count's weight.

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


def static_float(w, gamma, eps=1e-6, h=1e-3):
    """The x row of d_j ((-g)^w g^jx) at the point (1, 0, 0) about a point mass, U = eps / r, over eps."""
    def flux(x, y, z, j):
        rr = (x * x + y * y + z * z) ** 0.5
        u = eps / rr
        minus_g = (1 - 2 * u) * (1 + 2 * gamma * u) ** 3
        gxx = 1 / (1 + 2 * gamma * u)
        return minus_g ** w * gxx if j == 0 else 0.0
    div = (flux(1 + h, 0, 0, 0) - flux(1 - h, 0, 0, 0)) / (2 * h)
    return div / eps


def main():
    print("w      f = w/(1-w)   gamma = w/(3w-1)   the static row in floats: at that gamma, at gamma = 1")
    for k in range(1, 12):
        w = F(k, 12)
        f = course_f(w)
        gamma = static_gamma(w) if 3 * w != 1 else None
        row = static_float(float(w), float(gamma)) if gamma is not None else float("nan")
        einstein = static_float(float(w), 1.0)
        print(f"{str(w):6} {str(f):13} {str(gamma) if gamma is not None else 'none (w = 1/3)':18} "
              f"{row:+.2e}  {einstein:+.3f}")
    print("w = 1/2 (the free count, Box_g x = 0):", f"f = {course_f(F(1, 2))}, gamma = {static_gamma(F(1, 2))}")
    print("f = 1/3 (the square cell):", f"w = {F(1, 3) / (1 + F(1, 3))}, gamma = {static_gamma(F(1, 4))}")


if __name__ == "__main__":
    main()
