"""The shadow's curvature: road A read in 3 + 1, the push it needs, light's weight and the spring's door, a toy in floats.

David's check in clocks for the Boss's asks of 2026-10-29 (comments 6495563410 item 3, 6495615190 item 1 and
6495923568 item 3), on the owner's word to David of 11:5x UTC ("Sync from the Boss on Minkowski and the clicks").

usage: python3 -I q5_the_shadow.py

The identity. In the clicks' units (h N = 1) a = e^U, d tau = e^-U dt and H = e^U U', primes in the board's ticks. With
the time gear's teeth read from the ruler, Z = e^(4U) (Z = T Y^4 div Gamma^4, Y = Gamma e^U, at T = 1), the chain rule
gives, exactly,
    d/dt (Z U') = e^(4U) (U'' + 4 U'^2) = e^(2U) (dH/dtau + 3 H^2) = (N a^3) R_xx,
the cell's four-volume N a^3 = e^(2U) (Y^2 over Gamma^2, the spring's factor) times the shadow's spatial curvature
R_xx = dH/dtau + 3 H^2 (Ricci's space-space part in an orthonormal frame, flat Friedmann). Z itself is a^3 / N, the
3 + 1 split's weight (three lengths over one tick), and not a four-volume. So road A (q4's part D, d/dt (Z U') =
s J - D U, with J = e^(2U) (rho + 3p) by the act's count of 4 tan(w/2) kicks a light quantum against 2 tan(w/2) a matter
quantum at rest, and the spring D = D0 e^(2U), Y^2's) reads
    R_xx = s (rho + 3p) - D0 (U - U_c),
while Einstein's equation (8 pi G = 1) reads R_xx = (rho - p) / 2 + Lambda, with his constraint H^2 = rho / 3.

On the attractor of R_xx = k rho for a fluid p = w rho (rho as a^(-3 (1 + w))), H^2 = 2 k rho / (3 (1 - w)) exactly; the
first integral adds C a^-6 (the Boss's stiff mode; Einstein's constraint is C = 0). Three parts:
  A. the weights, exact: Einstein's k = (1 - w) / 2 gives every fluid its share rho / 3; the act's k = s (1 + 3w), with
     s = 1/2 fixed by dust, gives each fluid (1 + 3w) / (1 - w) of its share: dust 1, light 3, a vacuum energy -1;
  B. the courses in floats from a mix of light and matter: Einstein's, road A with the push (rho - p) / 2 and C = 0,
     and road A with the act's push;
  C. the spring as a Lambda linear in the load: with its rest at the load 0, which is the bang (the picture's sections
     4 and 7: "a count below 0 reads at 0"; the bang is "the load at 0"), and with a rest above the expansion, which
     the act does not hold.
A toy of the logic: floats, a small step, every rate typed; the identity and the weights are exact.
"""

import math
from fractions import Fraction


def attractor(k: Fraction, w: Fraction) -> Fraction:
    """c in y = c rho0 e^(-(5 + 3w) U), solving dy/dU = -8 y + 2 k rho0 e^(-(5 + 3w) U) exactly; then H^2 = c rho."""
    c = 2 * k / (3 * (1 - w))
    assert -(5 + 3 * w) * c == -8 * c + 2 * k
    return c


def part_a() -> list[str]:
    lines = ["A. each fluid's weight in the clicks' H^2, as a share of Einstein's rho / 3 (exact):"]
    for name, w in (("dust", Fraction(0)), ("light", Fraction(1, 3)), ("a string gas", Fraction(-1, 3)),
                    ("a vacuum energy", Fraction(-1))):
        einstein = attractor((1 - w) / 2, w) * 3
        act = attractor(Fraction(1, 2) * (1 + 3 * w), w) * 3
        lines.append(f"  {name} (w = {w}): Einstein's push (rho - p) / 2 gives {einstein}; the act's s (rho + 3p) gives {act}")
    return lines


def course(source, u0: float, u1: float, y0: float, n: int = 40_000):
    """dy/dU = source(U, y) by RK4 from y(u0) = y0; rows (U, y, q, tau), tau the clicks' time from u0."""
    h = (u1 - u0) / n
    u, y, tau, rows = u0, y0, 0.0, []
    for i in range(n + 1):
        dy = source(u, y)
        if i % (n // 8) == 0:
            rows.append((u, y, -2 - dy / (2 * y), tau))
        if i == n or y <= 0:
            break
        k1 = dy
        k2 = source(u + h / 2, y + h / 2 * k1)
        k3 = source(u + h / 2, y + h / 2 * k2)
        k4 = source(u + h, y + h * k3)
        y_next = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if y_next > 0:
            tau += h * 0.5 * (math.exp(-u) / math.sqrt(y) + math.exp(-u - h) / math.sqrt(y_next))
        u, y = u + h, y_next
    return rows


def part_b() -> list[str]:
    """Light and matter equal (Einstein) at U = 4: rho_m = e^(-3U), rho_r = e^(4 - 4U), from U 0 to 8."""

    def rho_m(u):
        return math.exp(-3 * u)

    def rho_r(u):
        return math.exp(4 - 4 * u)

    def einstein(u, y):
        return -4 * y - math.exp(-2 * u) * (rho_m(u) + 2 * rho_r(u)) / 3

    def road_a_volume(u, y):
        return -8 * y + 2 * math.exp(-2 * u) * (rho_m(u) + 2 * rho_r(u) / 3) / 2

    def road_a_act(u, y):
        return -8 * y + 2 * math.exp(-2 * u) * (rho_m(u) + 2 * rho_r(u)) / 2

    def constraint(u):
        return math.exp(-2 * u) * (rho_m(u) + rho_r(u)) / 3

    e_rows = course(einstein, 0.0, 8.0, constraint(0.0))
    v_rows = course(road_a_volume, 0.0, 8.0, constraint(0.0))
    a_rows = course(road_a_act, 0.0, 8.0, (rho_m(0.0) / 3 + rho_r(0.0)) * math.exp(0.0))
    lines = ["B. the courses from U 0 to 8, light and matter equal in Einstein's at U 4 (H^2 = e^(2U) y):"]
    worst = max(abs(ve[1] / constraint(ve[0]) - 1) for ve in e_rows)
    lines.append(f"  Einstein's evolution keeps his constraint to {worst:.1e}")
    for (u, ye, qe, te), (_, yv, qv, tv), (_, ya, qa, ta) in zip(e_rows, v_rows, a_rows, strict=True):
        lines.append(
            f"  U {u:.0f}: q Einstein {qe:+.4f}, road A (rho - p) {qv:+.4f}, road A act {qa:+.4f}; "
            f"H^2 against Einstein's {yv / ye:.6f} and {ya / ye:.4f}; clicks' time {tv / te if te else 1:.6f} "
            f"and {ta / te if te else 1:.4f}"
        )
    lines.append(
        "  under the act's push light and matter weigh equally where rho_m = 3 rho_r, ln 3 = "
        f"{math.log(3):.4f} e-folds after Einstein's equality"
    )
    return lines


def part_c() -> list[str]:
    """The spring as Lambda = -D0 (U - U_c) in R_xx, with dust, from the floor U = 0 on the attractor to the top."""
    lines = ["C. the spring, R_xx's term -D0 (U - U_c), with dust rho_m = e^(-3U), from the floor U 0 to the top:"]
    for u_c, d0, note in ((0.0, 1e-3, "the act's rest, the load 0"), (0.0, 0.1, "the act's rest, a strong spring"),
                          (5.0, math.exp(-9) / 2.17, "a rest five e-folds up, not in the act")):

        def spring(u, y, u_c=u_c, d0=d0):
            return -8 * y + 2 * math.exp(-2 * u) * (math.exp(-3 * u) / 2 - d0 * (u - u_c))

        y0 = 1 / 3 + d0 / 3 * (u_c + 1 / 6)
        u, y, qmin, umin = 0.0, y0, 9.0, 0.0
        h = 1e-4
        while y > 0 and u < 40:
            dy = spring(u, y)
            q = -2 - dy / (2 * y)
            if q < qmin:
                qmin, umin = q, u
            k2 = spring(u + h / 2, y + h / 2 * dy)
            k3 = spring(u + h / 2, y + h / 2 * k2)
            k4 = spring(u + h, y + h * k3)
            y += h / 6 * (dy + 2 * k2 + 2 * k3 + k4)
            u += h
        lines.append(f"  {note} (U_c {u_c}, D0 {d0:.3g}): the top at U {u:.3f}; the least q {qmin:+.3f}, at U {umin:.2f}")
    lines.append(
        "  on the attractor the spring reads as a fluid of w = -1 + 1 / (3 (U_c - U + 1/6)), so wa = -3 (1 + w0)^2"
    )
    return lines


def main() -> None:
    lines = [
        "The shadow's curvature (David, 2026-10-29): road A read in 3 + 1, a toy in floats with exact weights",
        "",
        "d/dt (Z U') = (N a^3) R_xx exactly; Z = a^3 / N = e^(4U), the cell's four-volume N a^3 = e^(2U)",
        "",
    ]
    lines += part_a() + [""] + part_b() + [""] + part_c()
    print("\n".join(lines))


if __name__ == "__main__":
    main()
