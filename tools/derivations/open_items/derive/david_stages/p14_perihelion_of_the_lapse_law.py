"""David's probe for stage 7's time gear: the perihelion each lapse law gives, against general relativity's.

usage: python3 -I p14_perihelion_of_the_lapse_law.py
The head's metric is -N^2 dt^2 + N^-2 (dr^2 + r^2 dphi^2) (N A = 1, p13). Its time gear X = Gamma N^-4 steps by a linear
wave equation, so outside matter X is harmonic: X = Gamma (1 + 4 M / r) for a mass M, and N = (X / Gamma)^(-1/4).
The same metric with the ruler Y = Gamma / N harmonic gives N = 1 / (1 + M / r); with ln Y harmonic (Y's equation
holding its self-source |grad Y|^2 / Y, Einstein's lapse equation for this metric) N = exp(-M / r).
For each, a bound orbit's turning points u1 = 1 / r1 and u2 = 1 / r2 fix its energy and angular momentum; the angle
from u1 to u2 is integrated exactly (u = c + d cos psi, the midpoint rule in psi), and the perihelion's advance per
orbit, 2 (angle) - 2 pi, is read as a multiple k of general relativity's 6 pi M / p (p the semi-latus rectum). In the
post-Newtonian reading k = (2 + 2 gamma - beta) / 3, with g_00 = -(1 - 2 U + 2 beta U^2) and g_ij = (1 + 2 gamma U).
Schwarzschild's own metric, in its own coordinates, is the control. Floats; no engine is run.
"""
import math


def isotropic(n2):
    """F(u) = (du / dphi)^2 on the metric with N^2 = n2(u) and A = 1 / N, for given E^2 and L^2."""

    def f(u, e2, l2):
        n = n2(u)
        return (e2 - n - n * n * l2 * u * u) / (l2 * n * n)

    def constants(u1, u2):
        n1, n2_ = n2(u1), n2(u2)
        l2 = (n1 - n2_) / (n2_ * n2_ * u2 * u2 - n1 * n1 * u1 * u1)
        return n1 + n1 * n1 * l2 * u1 * u1, l2

    return f, constants


def schwarzschild(m):
    def f(u, e2, l2):
        return (e2 - (1 - 2 * m * u) * (1 + l2 * u * u)) / l2

    def constants(u1, u2):
        l2 = 2 * m * (u2 - u1) / ((1 - 2 * m * u2) * u2 * u2 - (1 - 2 * m * u1) * u1 * u1)
        return (1 - 2 * m * u1) * (1 + l2 * u1 * u1), l2

    return f, constants


def advance(f, constants, u1, u2, n=4000):
    e2, l2 = constants(u1, u2)
    c, d = (u1 + u2) / 2, (u2 - u1) / 2
    total = 0.0
    for k in range(n):
        psi = (k + 0.5) * math.pi / n
        u = c + d * math.cos(psi)
        h = f(u, e2, l2) / ((u - u1) * (u2 - u))
        total += 1 / math.sqrt(h)
    return 2 * total * math.pi / n - 2 * math.pi


LAWS = {
    "the head's, X = Gamma N^-4 harmonic": lambda m: isotropic(lambda u: (1 + 4 * m * u) ** -0.5),
    "the ruler Y = Gamma / N harmonic": lambda m: isotropic(lambda u: (1 + m * u) ** -2),
    "ln Y harmonic (Einstein's lapse equation on this metric)": lambda m: isotropic(lambda u: math.exp(-2 * m * u)),
    "Schwarzschild's metric (the control)": schwarzschild,
}

U1, U2 = 0.8, 1.2  # the turning points, p = 2 / (u1 + u2) = 1
for name, law in LAWS.items():
    readings = []
    for m in (1e-3, 1e-4):
        f, constants = law(m)
        readings.append(advance(f, constants, U1, U2) / (6 * math.pi * m * (U1 + U2) / 2))
    print(f"{name}: the advance is k = {readings[0]:.4f} (M = 1e-3) and {readings[1]:.4f} (M = 1e-4) of general relativity's")
print("so k = (2 + 2 gamma - beta) / 3 with gamma = 1 reads beta = 3 for the head's law, 1.5 for the harmonic ruler and 1 for ln Y")
