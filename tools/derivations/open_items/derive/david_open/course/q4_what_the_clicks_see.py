"""What the clicks see of the swing: the deceleration parameter on 7b's time gear and on the volume form, a toy in floats.

David's probe for the Boss's ask of 2026-10-29, 10:01 UTC (comment 6493676846, item 3: what the clicks see of the swing,
against nature's deceleration parameter), and for the owner's word to David of 10:4x UTC ("I see the clicks as pushing
the contraction away, to allow the future to continue by the clicks... maybe the solution is from there...").

usage: python3 -I q4_what_the_clicks_see.py

The clicks' scale and time (the picture's own lines): the Mesh is 1/N long (h N = 1) and a click's tick lasts N, with
N = e^-U, so in the clicks' units a = e^U and d tau = e^-U dt, and light's redshift is 1 + z = e^(U_obs - U_emit).
Then, exactly, H = dU / d tau = e^U U' and q = -2 - U'' / U'^2, primes in the board's ticks. Two gears for the load U:
  A. 7b's time gear on the load's count: W U'' = J - D U, the push J = A_L e^(-2U) + A_M e^(-U) (light's push as N^2 and
     matter's as N, the Boss's act_push), W = 1;
  B. the volume form, the head's (ALGEBRA.md lines 430 and 432: U'' + 4 U'^2 = f): the gear on X = e^(4U) with the same
     pushing source per proper volume and a spring linear in X, so U'' = -4 U'^2 + A_L e^(-6U) + A_M e^(-5U) - kappa;
  C. on B, clicks that turn matter into light at a rate r per click-time (energy kept, light pushing twice its forms);
  D. 7b's own carry with the time gear reading the ruler as every gear does (ALGEBRA.md line 693, with no exception): the
     momentum W U' changes by the force, W = W0 e^(4U) (Z = T Y^4 div Gamma^4) and the spring by Y^2 as a massive
     train's, so d/dt (W U') = s J - D U gives U'' = -4 U'^2 + (s J - D0 e^(2U) U) / (W0 e^(4U)), J as in A. B breaks
     Postulate 6 (linear in X); D keeps the act linear in its count, its teeth read from the ruler as every gear's are.
A toy of the logic: floats, a small step, and every rate typed; the formula for q is exact.
"""

import math


def gear_a(al: float, am: float, d: float):
    """7b's gear from the bang at rest; the expansion's (U, q) until the top."""
    u, v, dt, rows = 0.0, 0.0, 1e-4, []
    for i in range(2_000_000):
        acc = al * math.exp(-2 * u) + am * math.exp(-u) - d * u
        if i and v <= 0:
            break
        if v > 1e-9:
            rows.append((u, -2 - acc / (v * v)))
        v += acc * dt
        u += v * dt
    return rows


def decelerating_share(rows) -> float:
    """The span of U, in e-folds, over which the clicks see q > 0 on the expansion."""
    pos = [u for u, q in rows if q > 0]
    return max(pos) - min(pos) if pos else 0.0


def gear_b(al: float, am: float, kappa: float, u0: float, frac: float, swings: int = 2):
    """The volume form from u0, expanding at frac of the zero-energy fall; the bounces, the tops and the expansion's q."""
    free = al * math.exp(-6 * u0) + 2 * am / 3 * math.exp(-5 * u0)
    u, p = u0, math.sqrt(frac * free)
    tops, bottoms, rows, sign = [], [], [], 1

    def f(uu, pp):
        return pp, -4 * pp * pp + al * math.exp(-6 * uu) + am * math.exp(-5 * uu) - kappa

    while len(bottoms) < swings:
        acc = f(u, p)[1]
        h = 1e-3 / (abs(p) + math.sqrt(abs(acc)) + 1e-12)
        k1 = f(u, p)
        k2 = f(u + h / 2 * k1[0], p + h / 2 * k1[1])
        k3 = f(u + h / 2 * k2[0], p + h / 2 * k2[1])
        k4 = f(u + h * k3[0], p + h * k3[1])
        u += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        p += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        s = 1 if p > 0 else -1
        if s != sign:
            (tops if sign > 0 else bottoms).append(u)
            sign = s
        if p > 1e-12 and not tops:
            rows.append((u, -2 - f(u, p)[1] / (p * p)))
    return tops, bottoms, rows


def gear_c(r: float, kappa: float = 1e-9, u0: float = -3.0, frac: float = 0.99):
    """The volume form with clicks turning matter into light at rate r; the top and the least late q."""
    u, m, rl = u0, 1.0, 0.0
    p = math.sqrt(frac * 2 / 3 * math.exp(-5 * u))
    tau, rows = 0.0, []
    while p > 0:
        rho_m = m * math.exp(-3 * u)
        acc = -4 * p * p + (rho_m + 2 * rl) * math.exp(-2 * u) - kappa
        h = 2e-3 / (abs(p) + math.sqrt(abs(acc)) + 1e-15)
        dtau = math.exp(-u) * h
        rl += (-4 * math.exp(u) * p * rl + r * rho_m) * dtau
        m -= r * m * dtau
        p += acc * h
        u += p * h
        tau += dtau
        if p > 0:
            rows.append((u, -2 - acc / (p * p)))
    late = [q for uu, q in rows if uu > u - 1.5]
    return u, tau, min(late)


def sample(rows, n: int = 10) -> str:
    lo, hi = rows[0][0], rows[-1][0]
    out = []
    for k in range(n + 1):
        mark = lo + (hi - lo) * k / n
        uu, q = min(rows, key=lambda row: abs(row[0] - mark))
        out.append(f"U {uu:.1f} q {q:+.2f}")
    return "; ".join(out)


def main() -> None:
    lines = [
        "What the clicks see of the swing (David, 2026-10-29): q = -2 - U''/U'^2, a toy in floats",
        "",
    ]
    lines.append("A. 7b's time gear, W U'' = J - D U, from the bang at rest:")
    for al, am, d in ((1.0, 0.0, 0.5), (0.0, 1.0, 0.5), (1.0, 1.0, 0.2), (5.0, 0.0, 0.1)):
        rows = gear_a(al, am, d)
        lines.append(
            f"  A_L {al}, A_M {am}, D {d}: the top at U {rows[-1][0]:.2f}; the clicks see q > 0 over "
            f"{decelerating_share(rows):.2f} e-folds of it"
        )
        lines.append("    " + sample(rows, 5))
    lines.append(
        "  (near any smooth top the clicks see q > 0 over at most a quarter e-fold: there U'^2 = 2 |U''| (U_top - U))"
    )
    lines.append("")
    lines.append("B. the volume form, U'' = -4 U'^2 + A_L e^(-6U) + A_M e^(-5U) - kappa:")
    for al, am, kappa, u0 in ((1e-3, 1.0, 1e-12, 0.0), (1.0, 1e-3, 1e-12, 0.0)):
        tops, bottoms, rows = gear_b(al, am, kappa, u0, 0.999)
        lines.append(
            f"  A_L {al}, A_M {am}, kappa {kappa}: bounces at U {', '.join(f'{b:.2f}' for b in bottoms)}; "
            f"tops at U {', '.join(f'{t:.2f}' for t in tops)}"
        )
        lines.append("    the first expansion: " + sample(rows, 5))
    lines.append("")
    lines.append(
        "C. on B, clicks turning matter into light at a rate r per click-time (kappa 1e-9, from U -3):"
    )
    for r in (0.0, 1e-3, 1e-2, 1e-1):
        top, tau, qmin = gear_c(r)
        lines.append(
            f"  r {r}: the top at U {top:.3f}, click-time to it {tau:.4g}; the least q in the last 1.5 e-folds {qmin:+.3f}"
        )
    lines.append("")
    lines.append(
        "D. the time gear reading the ruler, d/dt (W U') = s J - D U, W = e^(4U), the spring D0 e^(2U), from U -3:"
    )
    for al, am in ((1e-3, 1.0), (1.0, 1e-3)):
        events, rows = gear_d(al, am)
        lines.append(
            f"  A_L {al}, A_M {am}, D0 1e-9: " + ", ".join(f"{e} at U {u:.2f}" for e, u in events)
        )
        lines.append("    the first expansion: " + sample(rows, 5))
    lines.append(
        "  the time gear's waves: as built (its own teeth) they keep c0 while light runs at c0 N^2, so locally"
    )
    lines.append(
        "  they outrun light by 1 / N^2 = e^(2U); reading the ruler, both read Z and share one cone at every notch"
    )
    print("\n".join(lines))


def gear_d(al: float, am: float, d0: float = 1e-9, u0: float = -3.0, frac: float = 0.99):
    """7b's momentum carry with the time gear reading the ruler: two tops and the bounces between, and the first q."""

    def acc(uu, pp):
        push = al * math.exp(-2 * uu) + am * math.exp(-uu)
        return -4 * pp * pp + (push - d0 * math.exp(2 * uu) * uu) / math.exp(4 * uu)

    free = al * math.exp(-6 * u0) + 2 * am / 3 * math.exp(-5 * u0)
    u, p = u0, math.sqrt(frac * free)
    events: list[tuple[str, float]] = []
    rows, sign = [], 1
    while len(events) < 3:
        a = acc(u, p)
        h = min(1e-3 / (abs(p) + math.sqrt(abs(a)) + 1e-14), 1e-4 / (abs(p) + 1e-300))
        k1 = (p, a)
        k2 = (p + h / 2 * k1[1], acc(u + h / 2 * k1[0], p + h / 2 * k1[1]))
        k3 = (p + h / 2 * k2[1], acc(u + h / 2 * k2[0], p + h / 2 * k2[1]))
        k4 = (p + h * k3[1], acc(u + h * k3[0], p + h * k3[1]))
        u += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        p += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        s = 1 if p > 0 else -1
        if s != sign:
            events.append(("a top" if sign > 0 else "a bounce", u))
            sign = s
        if p > 1e-12 and not events:
            rows.append((u, -2 - acc(u, p) / (p * p)))
    return events, rows


if __name__ == "__main__":
    main()
