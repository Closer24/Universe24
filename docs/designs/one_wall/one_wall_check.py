"""One-wall-v1 (issue #605): the wall term and the push term of light's
deflection, checked by arithmetic on the closed forms (read-only, the
derivation mathematician, 2026-09-21). No engine run; the lattice numbers
quoted are the light-bending map's (docs/designs/open_problems/light_bending).

Three identities of the continuum limit, evaluated numerically:

1. Fermat's turn of a wavefront in the index n = 1 + k, k = G M / (r c^2),
   and Newton's push on a particle of energy E at the speed c in the
   potential Phi = -G M / r, are the same integral per unit length,
   d theta / dl = grad_perp k = -grad_perp Phi / c^2; each sums to
   2 G M / (b c^2) over the whole line (Newton's half of Einstein's 4).
2. The wavefront's tilt is the derivative of the Shapiro delay across the
   impact parameter b: c |d tau / db| -> 2 G M / (b c^2) as L / b -> infinity,
   the same number as the turn; so the wall's tilt and the push's turn are
   one deflection read in two languages, never a sum.
3. The wall's constant and the push's constant on the GameBoard (5.1, 3.3):
   k_wall = (n / d)_susp x A, A = q / (4 pi c^2 r), q = K (n / d)_rel M;
   k_push = G M / (r c^2), G = K (n / d)_rel / (4 pi S); their ratio is
   (n / d)_susp x S exactly: one constant when the suspension pair is [1, S].

Run from the repository root:

    python docs/designs/one_wall/one_wall_check.py > docs/designs/one_wall/one_wall_check.out
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr

GM_OVER_C2 = 1.0  # G M / c^2 in units of the impact parameter's Link; the form is what is checked


def fermat_turn(b: float, big_l: float, steps: int = 200000) -> float:
    """sum over the line of grad_perp k, k = (G M / c^2) / sqrt(b^2 + x^2)."""
    h = 2 * big_l / steps
    total = 0.0
    for i in range(steps):
        x = -big_l + (i + 0.5) * h
        total += GM_OVER_C2 * b / (b * b + x * x) ** 1.5 * h
    return total


def newton_push_turn(b: float, big_l: float, steps: int = 200000) -> float:
    """sum over the line of (-grad_perp Phi) / c^2, Phi = -G M / r, on a particle at c:
    d p_perp = (E / c^2) (-grad_perp Phi) dt, p = E / c, dl = c dt, so d theta = -grad_perp Phi dl / c^2."""
    h = 2 * big_l / steps
    total = 0.0
    for i in range(steps):
        x = -big_l + (i + 0.5) * h
        r3 = (b * b + x * x) ** 1.5
        total += (GM_OVER_C2 * b / r3) * h  # -grad_perp Phi / c^2 = (G M / c^2) b / r^3
    return total


def shapiro_delay_times_c(b: float, big_l: float) -> float:
    """c x the delay of the wall alone: integral of k dl = (G M / c^2) 2 asinh(L / b)."""
    return GM_OVER_C2 * 2 * math.asinh(big_l / b)


def main() -> None:
    print(
        "1. FERMAT'S TURN AGAINST NEWTON'S PUSH AT c, per unit G M / c^2 (the impact parameter in Links)"
    )
    for b, big_l in ((6, 26), (3, 26), (6, 1000), (3, 1000)):
        f, p = fermat_turn(b, big_l), newton_push_turn(b, big_l)
        closed = 2 * GM_OVER_C2 * big_l / (b * math.sqrt(big_l**2 + b * b))
        print(
            f"   b = {b}, L = {big_l:g}: Fermat {f:.6f}, the push {p:.6f}, the closed form "
            f"2 (G M / c^2) L / (b sqrt(L^2 + b^2)) = {closed:.6f}, the limit 2 / b = {2 / b:.6f}"
        )
    print(
        "   the two integrands are one expression: b / (b^2 + x^2)^(3/2) per unit G M / c^2; the difference is 0 exactly"
    )
    print()
    print("2. THE WAVEFRONT'S TILT IS THE DERIVATIVE OF THE SHAPIRO DELAY (the wall alone)")
    for b in (6.0, 3.0):
        for big_l in (26.0, 1e3, 1e6):
            eps = 1e-6 * b
            d = (shapiro_delay_times_c(b + eps, big_l) - shapiro_delay_times_c(b - eps, big_l)) / (
                2 * eps
            )
            print(
                f"   b = {b:g}, L = {big_l:g}: c |d tau / db| = {abs(d):.6f}; the turn's 2 / b = {2 / b:.6f}; "
                f"the exact 2 / sqrt(b^2 + L^2) x L / b = {2 * big_l / (b * math.sqrt(b * b + big_l**2)):.6f}"
            )
    print(
        "   at finite L the tilt is 2 L / (b sqrt(b^2 + L^2)), the turn's closed form exactly: one number, two readings"
    )
    print()
    print("3. THE TWO CONSTANTS ON THE GAMEBOARD (5.1 and 3.3), exact rationals")
    c2 = Fr(1, 3)
    for n_rel, d_rel, n_susp, d_susp, big_s in (
        (1, 1, 1, 2, 2),
        (1, 1, 1, 4096, 4096),
        (1, 1, 1, 16384, 4096),
        (1, 1, 1, 2, 4096),
    ):
        big_k, big_m, r = 290, 1, 1  # per direction, per unit content, per Link: the form only
        q = big_k * Fr(n_rel, d_rel) * big_m
        a_field = q / (
            4 * c2 * r
        )  # A = q / (4 pi c^2 r) with the 4 pi kept symbolic: both sides carry 1 / (4 pi)
        k_wall = Fr(n_susp, d_susp) * a_field
        g_newton = (
            big_k * Fr(n_rel, d_rel) / (4 * big_s)
        )  # G = K (n / d)_rel / (4 pi S), the 4 pi symbolic
        k_push = g_newton * big_m / (r * c2)
        ratio = k_wall / k_push
        print(
            f"   release [{n_rel}, {d_rel}], suspension [{n_susp}, {d_susp}], S = {big_s}: "
            f"k_wall / k_push = {ratio} = (n / d)_susp x S = {Fr(n_susp, d_susp) * big_s}"
        )
    print(
        "   one constant (the redshift's G the orbit's G, the wall's tilt the push's turn) if and only if (n / d)_susp = 1 / S"
    )
    print()
    print(
        "4. THE SUM 'WALL 2 + PUSH 2 = 4': what each reading gives, per unit G M / (b c^2), L / b -> infinity"
    )
    print(
        "   the heading of one row (a screen's centroid):   wall 0, push 2, both 2   (a scalar enters only the wall)"
    )
    print(
        "   the wavefront's tilt (the delay's gradient):     wall 2, push 0, both 2   (the push changes no pace)"
    )
    print(
        "   the delay (Shapiro, the coefficient of the log): wall 1, push 0, both 1   (nature's 1 + gamma = 2)"
    )
    print(
        "   no reading gives 4; the 4 counts the g_00 term in the wave language and in the ray language"
    )


if __name__ == "__main__":
    main()
