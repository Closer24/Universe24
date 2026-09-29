"""The experiments run algebraically: every number of the paper's table computed from the law's
formulas alone (docs/ALGEBRA.md, the rows against nature), on a declared universe and declared
worlds, by no run of the engine. Run: python algebraic_runs.py."""

from __future__ import annotations

import math

GAMMA = 10_000
MATTER = (6_667, 10_000)
SECOND = (8_000, 10_000)
LIGHT = (1, 1)


def rotation(pair: tuple[int, int], k: float) -> float:
    """The band along an axis: cos omega = (num / (3 den)) (2 + cos k)."""
    num, den = pair
    return math.acos(num / (3 * den) * (2 + math.cos(k)))


def group_velocity(pair: tuple[int, int], k: float) -> float:
    """d omega / d k on the band along an axis."""
    num, den = pair
    return num / (3 * den) * math.sin(k) / math.sin(rotation(pair, k))


def top_velocity(pair: tuple[int, int]) -> float:
    """Delta, the second derivative of the band at k = 0: num / (3 den sin omega_0)."""
    num, den = pair
    return num / (3 * den) / math.sin(math.acos(num / den))


def redshift_per_level(pair: tuple[int, int]) -> float:
    """d omega_0 / d c at the vacuum's pace from the conformal pace: 2 tan(omega_0 / 2) / Gamma."""
    num, den = pair
    return 2 * math.tan(math.acos(num / den) / 2) / GAMMA


def solve(f, lo: float, hi: float) -> float:
    """The root of f between lo and hi by bisection."""
    flo = f(lo)
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def row_a() -> None:
    """The redshift: two clocks at the levels 500 and 1,000 of Gamma = 10^4."""
    u1, u2 = 500 / GAMMA, 1_000 / GAMMA
    law = math.sqrt((1 - 2 * u1 + 2 * u1**2) / (1 - 2 * u2 + 2 * u2**2))
    print(
        f"(a) tick ratio: the law's row {law:.4f}; first order {1 + (u2 - u1):.4f}; "
        f"one-Node conformal {(1 - u1) / (1 - u2):.4f}; Schwarzschild {math.sqrt((1 - 2 * u1) / (1 - 2 * u2)):.4f}"
    )


def row_b_c_d() -> None:
    """The bending, the delay and the perihelion at declared potentials."""
    ub, ell, up = 0.02, 200, 0.01
    print(
        f"(b) bending: shift {4 * ub * ell:.1f} Nodes at U_b = {ub}, L = {ell}; Newton's {2 * ub * ell:.1f}"
    )
    print(f"(c) delay: {4 * ub * 100:.1f} intervals over 100 Links within reach")
    print(
        f"(d) perihelion: {6 * math.pi * up:.4f} rad = {math.degrees(6 * math.pi * up):.2f} degrees per orbit at U_p = {up}"
    )


def row_e() -> None:
    """The moving clock at v = 0.1 on the matter pair."""
    v = 0.1
    w0 = math.acos(MATTER[0] / MATTER[1])
    delta = top_velocity(MATTER)
    k = math.asin(v / delta)
    omega_k = w0 + delta * (1 - math.cos(k))
    big_omega = omega_k - k * delta * math.sin(k)
    cb2 = delta * w0
    print(
        f"(e) moving clock: Delta {delta:.4f}, c_b^2 {cb2:.4f} (c_b {math.sqrt(cb2):.4f}), k {k:.4f}; "
        f"factor Omega/omega_0 {big_omega / w0:.4f}; Lorentz at c_b {math.sqrt(1 - v**2 / cb2):.4f}; "
        f"Lorentz at 1/sqrt3 {math.sqrt(1 - 3 * v**2):.4f}"
    )


def row_f_q() -> None:
    """The charge's and gravity's static field: Laplace's 1 / r outside a body."""
    c10 = 200
    for r in (10, 20):
        c = c10 * 10 / r
        a = top_velocity(MATTER) * redshift_per_level(MATTER) * c / r
        v = math.sqrt(r * a)
        print(
            f"(f, q) r = {r}: level {c:.0f}, acceleration {a:.3e}, orbit speed {v:.4f}, "
            f"period {2 * math.pi * r / v:.0f} intervals"
        )


def lattice_wavevector(theta: float, cos_omega: float) -> float:
    """|k| in the direction theta on the light band cos k_x + cos k_y + 1 = 3 cos omega (k_z = 0)."""
    target = 3 * cos_omega - 1

    def f(k: float) -> float:
        return math.cos(k * math.cos(theta)) + math.cos(k * math.sin(theta)) - target

    return solve(f, 1e-9, math.pi)


def arriving_wavevector(rx: float, ry: float, cos_omega: float) -> tuple[float, float]:
    """The wavevector whose group velocity (sin k_x, sin k_y) points along (rx, ry)."""
    target = 3 * cos_omega - 1

    def f(ky: float) -> float:
        kx = math.acos(max(-1.0, min(1.0, target - math.cos(ky))))
        return math.sin(ky) * rx - math.sin(kx) * ry

    ky = solve(f, 0.0 if ry >= 0 else -math.pi / 2, math.pi / 2 if ry >= 0 else 0.0)
    kx = math.acos(target - math.cos(ky))
    return kx, ky


def row_g() -> None:
    """The two slits at lambda = 4, d = 16, L = 97: the bright strips on the lattice's dispersion."""
    lam, d, ell = 4, 16, 97
    cos_omega = 2 / 3
    first_order = lam * ell / d
    print(f"(g) first-order strip spacing {first_order:.2f} Nodes = {first_order / 4:.2f} strips of 4")

    def phase_difference(y: float) -> float:
        total = []
        for yi in (d / 2, -d / 2):
            kx, ky = arriving_wavevector(ell, y - yi, cos_omega)
            total.append(kx * ell + ky * (y - yi))
        return total[0] - total[1]

    for m in (1, 2):
        y = solve(lambda yy, m=m: phase_difference(yy) + 2 * math.pi * m, 0.1, 3 * first_order * m)
        print(
            f"    bright pair m = {m} on the lattice at y = {y:.1f} Nodes = {y / 4:.2f} strips "
            f"(first order {first_order * m / 4:.2f} strips); paraxial 2 pi L m / d = {2 * math.pi * ell * m / d / 4:.2f} strips"
        )


def row_h() -> None:
    """Bell at the settings 0, pi/4 and pi/8, 3pi/8."""
    a, a2, b, b2 = 0, math.pi / 4, math.pi / 8, 3 * math.pi / 8
    e = lambda x, y: math.cos(2 * (x - y))  # noqa: E731
    s = e(a, b) - e(a, b2) + e(a2, b) + e(a2, b2)
    print(
        f"(h) E(a,b) {e(a, b):.4f}, E(a,b') {e(a, b2):.4f}, E(a',b) {e(a2, b):.4f}, E(a',b') {e(a2, b2):.4f}; S {s:.4f}"
    )


def row_i() -> None:
    """The fall of a light body in a tent of slope 2 levels per Link, L = 50 Links, two families."""
    slope, ell = 2, 50
    for pair in (MATTER, SECOND):
        a = top_velocity(pair) * redshift_per_level(pair) * slope
        t = math.sqrt(2 * ell / a)
        print(
            f"(i) pair {pair}: Delta x d omega/dc {top_velocity(pair) * redshift_per_level(pair) * GAMMA:.4f} per unit U, "
            f"a {a:.3e} Links/interval^2, fall of {ell} Links in {t:.0f} intervals at {a * t:.4f} Links/interval"
        )


def row_j_o() -> None:
    """De Broglie's record from a giver of cos omega_b = 0.60 on the matter band, and the moving mass."""
    num, den = MATTER
    cos_wb = 0.60
    wb = math.acos(cos_wb)
    k = math.acos(3 * cos_wb * den / num - 2)
    v = num / (3 * den) * math.sin(k) / math.sin(wb)
    w0 = math.acos(num / den)
    cm2 = w0 / (3 * math.tan(w0))
    print(
        f"(j) k {k:.4f} (lambda {2 * math.pi / k:.2f} Links), v {v:.4f}; de Broglie's second order k {wb * v / cm2:.4f} at c_m^2 {cm2:.4f}"
    )
    print(
        f"(o) the set 100 Links away clicks {100 / v:.0f} intervals after each giving; "
        f"the giver's velocity moves by {num / (3 * den * math.sin(wb)) * k:.4f} / M per quantum"
    )


def row_k() -> None:
    """The two-qubit computer: the wobble's second-order phase at a control amplitude 100."""
    amp, gc = 100, 1
    shift = gc**2 * amp**2 / (4 * GAMMA)
    rate = 2 * math.tan(math.acos(MATTER[0] / MATTER[1]) / 2) * shift / GAMMA
    print(
        f"(k) pace shift {shift:.3f} levels; phase {rate:.2e} rad per interval, {rate * 1000:.3f} rad over 1,000 intervals"
    )


def row_l() -> None:
    """Mach-Zehnder: the one-Node splitter's reflected share at the light's pace P = Gamma - c."""
    k = math.pi / 2
    mirror = GAMMA * (1 - math.sin(k / 2))
    for c in (1_000, 2_000, mirror, 4_000):
        rho = ((GAMMA - c) / GAMMA) ** 2
        s = (rho - 1) ** 2 / ((rho - 1) ** 2 + rho**2)
        print(f"(l) slab count {c:.0f}: reflected share {s:.3f}")
    s = 0.5
    for delta in (0.0, math.pi / 2, math.pi):
        print(
            f"    s = 1/2, arms' phase difference {delta:.4f}: cross exit {4 * s * (1 - s) * math.cos(delta / 2) ** 2:.3f}"
        )


def row_m() -> None:
    """The round trip: a giver receding at v = 0.05 from a mirror, giving every 8 intervals."""
    v, period = 0.05, 8
    wb = rotation(LIGHT, math.pi / 2)
    k = solve(lambda kk: rotation(LIGHT, kk) + kk * v - wb, 0.5, math.pi / 2)
    u = group_velocity(LIGHT, k)
    print(
        f"(m) k {k:.4f}, u {u:.4f}; returned clicks every {period * (u + v) / (u - v):.2f} intervals (ratio {(u + v) / (u - v):.4f})"
    )


def row_n() -> None:
    """Sagnac on a ring of 400 Links at v = 0.05 with light of lambda = 4."""
    big_n, v = 400, 0.05
    u = group_velocity(LIGHT, math.pi / 2)
    t1, t2 = big_n / (u + v), big_n / (u - v)
    print(
        f"(n) u {u:.4f}; the arms return after {t1:.1f} and {t2:.1f} intervals; difference {t2 - t1:.1f} "
        f"= 2 N v / (u^2 - v^2) {2 * big_n * v / (u**2 - v**2):.1f}"
    )


def row_p() -> None:
    """The medium: a window of level 1,000 for light of lambda = 4, depth 20; the window moving at 0.05."""
    c, depth, w = 1_000, 20, 0.05
    p = (GAMMA - c) / GAMMA
    k = math.pi / 2
    omega = rotation(LIGHT, k)
    u = group_velocity(LIGHT, k)
    cos_kin = 1 - (1 - math.cos(k)) / p**2
    kin = math.acos(cos_kin)
    v_in = p**2 * math.sin(kin) / (3 * math.sin(omega))
    print(
        f"(p) k_in {kin:.4f}, v_in {v_in:.4f}, u {u:.4f}, index {u / v_in:.3f}; passage longer by {depth * (1 / v_in - 1 / u):.1f} intervals"
    )

    def omega_in(kk: float) -> float:
        return math.acos(1 - p**2 * (1 - math.cos(kk)) / 3)

    kin_moving = solve(lambda kk: omega_in(kk) - kk * w - (omega - k * w), 0.5, math.pi)
    v_moving = p**2 * math.sin(kin_moving) / (3 * math.sin(omega_in(kin_moving)))
    fresnel = v_in + w * (1 - v_in**2 / u**2)
    print(
        f"    moving window: k_in {kin_moving:.4f}, speed inside {v_moving:.4f}; v_in + w {v_in + w:.4f}; Fresnel's {fresnel:.4f}"
    )


def row_r() -> None:
    """Dark energy: a giver's period at two far sets, and the packet's spread by the dispersion."""
    k = math.pi / 2
    u = group_velocity(LIGHT, k)
    h = 1e-5
    curvature = (group_velocity(LIGHT, k + h) - group_velocity(LIGHT, k - h)) / (2 * h)
    for distance in (1_000, 10_000):
        t = distance / u
        width = abs(curvature) * t / (2 * 10)
        print(
            f"(r) set at {distance} Links: flight {t:.0f} intervals, mean click interval 8.00, the packet of width 10 spread to about {width:.0f} Links"
        )


if __name__ == "__main__":
    for row in (
        row_a,
        row_b_c_d,
        row_e,
        row_f_q,
        row_g,
        row_h,
        row_i,
        row_j_o,
        row_k,
        row_l,
        row_m,
        row_n,
        row_p,
        row_r,
    ):
        row()
