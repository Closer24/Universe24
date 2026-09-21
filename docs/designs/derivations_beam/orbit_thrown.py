"""The orbit as the bond, thrown at v: the law's continuum equations on the
plane integrated by the host (read-only, the derivation mathematician,
2026-09-21; DERIVATIONS_BEAM.md section 12b). The registered geometry of
series D's `s32_r24` (a source of content 2^10 releasing q = 12 units per
interval on a fan of every in-plane direction, the width S = 32, a probe
of content 1 at r = 24 with the tangential momentum 576 label units): at
rest, then the pair thrown along +x at v = 1 / 8 and 1 / 4 Links per
interval (beta = v / c, c = 32 / 55), the probe reading the moving source's
retarded flux with the crossing rule's factor on its own velocity and,
in the second case, the aberration of the source's fan. No engine run: the
formulas of sections 3, 12 and 12b on the registered integers.

Run from the repository root:

    python docs/designs/derivations_beam/orbit_thrown.py > docs/designs/derivations_beam/orbit_thrown.out
"""

from __future__ import annotations

import math

Q = 64
C = 32 / 55  # the rows' pace on the plane's headings, Links per interval
S = 32  # the width (the registered s32_r24; a Newtonian regime at S = 512 below)
M_PROBE = 1
Q_RELEASE = 12.0  # units released per interval into the plane (the register: 120 rays per 10 intervals)
R0 = 24.0
P_ORBIT = 576.0  # label units, the registered s32_r24
WALL = Q * S * M_PROBE  # 2048 label units: Q S m


def set_width(width: int, p_orbit: float) -> None:
    global S, WALL, P_ORBIT
    S, WALL, P_ORBIT = width, Q * width * M_PROBE, p_orbit


F0 = (
    Q * M_PROBE * Q_RELEASE / (2 * math.pi)
)  # the plane's push: F = m q L C Q / (2 pi r) label units per interval at r = 1


def speed(p: tuple[float, float]) -> tuple[float, float]:
    """Form B in the continuum: the velocity along p at |p| / (Q S m + |p| / c), the cap c."""
    mag = math.hypot(*p)
    if mag == 0:
        return (0.0, 0.0)
    v = mag / (WALL + mag / C)
    return (v * p[0] / mag, v * p[1] / mag)


def retarded(x: tuple[float, float], beta: float) -> tuple[float, tuple[float, float]]:
    """A source moving at beta c along +x, at the origin now; x the probe's position relative to
    its PRESENT position: the retarded distance R_ret and the unit vector n_ret from the retarded
    position (the rows' direction of flight)."""
    b = x[0] * beta
    disc = b * b + (1 - beta * beta) * (x[0] ** 2 + x[1] ** 2)
    tau = (b + math.sqrt(disc)) / (1 - beta * beta)  # in units of Links / c
    r_ret = (x[0] + beta * tau, x[1])
    dist = math.hypot(*r_ret)
    return dist, (r_ret[0] / dist, r_ret[1] / dist)


def jacobian_2d(beta: float, theta_prime: float) -> float:
    """dtheta / dtheta' of the aberration n -> (n + beta x_hat) / |n + beta x_hat| on the plane."""

    def forward(theta: float) -> float:
        return math.atan2(math.sin(theta), math.cos(theta) + beta)

    lo, hi = -math.pi, math.pi
    for _ in range(200):
        mid = (lo + hi) / 2
        if forward(mid) < theta_prime:
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    c = math.cos(theta)
    # d theta' / d theta = (1 + beta cos theta) / (1 + 2 beta cos theta + beta^2)
    return (1 + 2 * beta * c + beta * beta) / (1 + beta * c)


def push(
    x: tuple[float, float], v_probe: tuple[float, float], beta: float, aberrated: bool
) -> tuple[float, float]:
    """The push on the probe per interval: the retarded flux of the moving source on the plane,
    q dwell / (2 pi R_ret (1 - n_ret . beta_s)) rows per Node, met at the rate (1 - n_ret . beta_probe)
    (the crossing rule's factor), each row's label Q along n_ret; the aberration multiplies the fan's
    density by the Jacobian at the emission angle. At beta = 0 this is the register's F = F0 / r."""
    dist, n = retarded(x, beta)
    kappa_s = 1 - n[0] * beta
    kappa_p = 1 - (n[0] * v_probe[0] + n[1] * v_probe[1]) / C
    density = 1 / (dist * kappa_s)
    if aberrated:
        density *= jacobian_2d(beta, math.atan2(n[1], n[0]))
    magnitude = F0 * density * kappa_p
    return (-magnitude * n[0], -magnitude * n[1])  # gravity: toward the source's retarded position


def integrate(beta: float, aberrated: bool, intervals: int = 6000):
    """The probe about a source moving at beta c along +x, both starting with the throw's velocity;
    returns the relative orbit's period (the angle about the source reaching 2 pi), its extents
    along and across the motion, and the drift of the relative centre per orbit."""
    v_throw = beta * C
    # the throw momentum that gives the speed v_throw under form B: p = v Q S m / (1 - v / c)
    p_throw = v_throw * WALL / (1 - v_throw / C)
    p = [p_throw, P_ORBIT]
    x = [R0, 0.0]  # relative to the source's present position
    angle = 0.0
    last = math.atan2(x[1], x[0])
    xs, ys = [], []
    periods = []
    t_last = 0
    for t in range(1, intervals + 1):
        v = speed((p[0], p[1]))
        f = push((x[0], x[1]), v, beta, aberrated)
        p[0] += f[0]
        p[1] += f[1]
        v = speed((p[0], p[1]))
        x[0] += v[0] - v_throw  # relative to the source moving at v_throw
        x[1] += v[1]
        a = math.atan2(x[1], x[0])
        d = a - last
        if d > math.pi:
            d -= 2 * math.pi
        if d < -math.pi:
            d += 2 * math.pi
        angle += d
        last = a
        xs.append(x[0])
        ys.append(x[1])
        if angle >= 2 * math.pi * (len(periods) + 1):
            periods.append(t - t_last)
            t_last = t
            if len(periods) == 3:
                break
        if math.hypot(*x) > 200 or math.hypot(*x) < 1:
            break
    n = len(xs)
    first = periods[0] if periods else n
    seg_x, seg_y = xs[:first], ys[:first]
    extent_x = (max(seg_x) - min(seg_x)) / 2 if seg_x else float("nan")
    extent_y = (max(seg_y) - min(seg_y)) / 2 if seg_y else float("nan")
    centre = (
        ((max(seg_x) + min(seg_x)) / 2, (max(seg_y) + min(seg_y)) / 2)
        if seg_x
        else (float("nan"), float("nan"))
    )
    return periods, extent_x, extent_y, centre, math.hypot(*x), n


print(
    "THE ORBIT AS THE BOND, THROWN (the registered s32_r24: S = 32, r = 24, p = 576, q = 12; the plane's 1 / r push)"
)
rest = integrate(0.0, False)
print(
    f"at rest: periods {rest[0]} (the derived 2 pi r / v = {2 * math.pi * R0 / (P_ORBIT / (WALL + P_ORBIT / C)):.0f}; the registered closing 623), extents along / across {rest[1]:.2f} / {rest[2]:.2f}, centre {rest[3][0]:.2f}, {rest[3][1]:.2f}"
)
for k in (8, 4):
    beta = (1 / k) / C
    gamma = 1 / math.sqrt(1 - beta * beta)
    for aberrated in (False, True):
        periods, ex, ey, centre, r_end, n = integrate(beta, aberrated)
        label = "aberrated  " if aberrated else "no aberration"
        print(
            f"thrown at v = 1/{k} (beta {beta:.4f}, gamma {gamma:.3f}), {label}: periods {periods}, extents along / across {ex:.2f} / {ey:.2f} (ratio {ex / ey if ey else float('nan'):.3f}; Lorentz would give {1 / gamma:.3f}), centre's offset from the source {centre[0]:+.2f}, {centre[1]:+.2f}, period over rest {periods[0] / rest[0][0] if periods and rest[0] else float('nan'):.3f} (Lorentz: gamma {gamma:.3f}); after {n} intervals at r = {r_end:.1f}"
        )
# the dispersion alone: the relative speed forward and backward of the throw at the rest orbital momentum
for k in (8, 4):
    beta = (1 / k) / C
    v_throw = beta * C
    p_throw = v_throw * WALL / (1 - v_throw / C)
    fwd = speed((p_throw + P_ORBIT, 0.0))[0] - v_throw
    back = speed((p_throw - P_ORBIT, 0.0))[0] - v_throw
    print(
        f"the dispersion's asymmetry at v = 1/{k}: the probe's speed relative to the source, forward {fwd:+.4f}, backward {back:+.4f} Links per interval (at rest +-{speed((P_ORBIT, 0.0))[0]:.4f})"
    )

# The Newtonian regime: the width raised so that the orbital speed is small against c (the
# register's derivation n v = q L C / (2 pi), p = 64 n, at S = 512 and 8192).
for width in (512, 8192):
    a_const = Q_RELEASE / (2 * math.pi)
    n_orb = (a_const + math.sqrt(a_const * a_const + 4 * width * a_const)) / 2
    set_width(width, 64 * n_orb)
    rest = integrate(0.0, False, intervals=200000)
    v_orb = speed((P_ORBIT, 0.0))[0]
    print(
        f"\nS = {width}, p = {P_ORBIT:.0f} (n = {n_orb:.2f}), orbital speed {v_orb:.4f} Links per interval ({v_orb / C:.3f} c): at rest periods {rest[0]}, extents {rest[1]:.2f} / {rest[2]:.2f}"
    )
    for k in (8, 4):
        beta = (1 / k) / C
        gamma = 1 / math.sqrt(1 - beta * beta)
        for aberrated in (False, True):
            periods, ex, ey, centre, r_end, n = integrate(beta, aberrated, intervals=200000)
            label = "aberrated  " if aberrated else "no aberration"
            ratio = periods[0] / rest[0][0] if periods and rest[0] else float("nan")
            print(
                f"  thrown at v = 1/{k} (beta {beta:.4f}, gamma {gamma:.3f}), {label}: periods {periods}, extents along / across {ex:.2f} / {ey:.2f} (ratio {ex / ey if ey else float('nan'):.3f}; Lorentz {1 / gamma:.3f}), centre {centre[0]:+.2f}, {centre[1]:+.2f}, period over rest {ratio:.3f} (Lorentz gamma {gamma:.3f}); {n} intervals, r = {r_end:.1f}"
            )
