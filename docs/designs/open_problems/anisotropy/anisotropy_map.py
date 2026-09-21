"""The moving laboratory's anisotropy without contraction: the map of problem (3) of the seven
(the open-problems physicist, read-only, 2026-09-21; docs/designs/open_problems/anisotropy/NOTE.md).

(A) The anisotropy itself, closed: two arms of one length at right angles read round trips
    gamma^2 (along) and gamma (across) on the lattice's one pace; the fractional difference
    gamma - 1 = beta^2 / 2 at the laboratory's speeds in the lattice's frame (the Earth's
    orbital 30 km/s, the cosmic background's 370 km/s), against the resonator bounds.
(B) A rigid arm on the GameBoard is a contact bond of whole Links: no verb contracts it; the
    anisotropy is exact and the only fix is the frame.
(C) A push-bound arm (an orbit) in motion, integrated in the continuum (floating point, a
    check of closed forms, labelled so; the method of DERIVATIONS 12b.2's orbit_thrown.py):
    a light probe about a heavy source both moving at beta along x, the relativistic
    dispersion of covariant-readings-v1 (v = p c^2 / E), under three pushes:
      (i)  Lorentz's force on a co-moving charge from Maxwell's field of a moving source
           (the target: Lorentz 1904, the orbit contracted by 1 / gamma, the period gamma);
      (ii) minus the gradient of the age moment alone (covariant-readings-v1's reading (ii)
           as amended, 17.6 M4): the Lienard-Wiechert scalar potential's gradient;
      (iii) the same gradient times (1 - beta^2), which is (i) exactly (the identity proved in
           the note: the Lorentz force on a co-moving probe is (1 - beta^2) times -grad A).
    Read: the orbit's extents along and across the motion, its period, its drift.
(D) The source's velocity is encoded locally: at a Node beside a moving source the flow points
    along the retarded direction and the gradient of the age moment from the present
    position; the angle between them at a few Nodes, as a function of beta.

Run from the repository root:

    python docs/designs/open_problems/anisotropy/anisotropy_map.py > docs/designs/open_problems/anisotropy/anisotropy_map.out
"""

from __future__ import annotations

import math

C = 1.0  # the continuum's c as the unit of pace in section C and D; the lattice's 1 / sqrt 3 enters only through beta


def gamma(beta: float) -> float:
    return 1 / math.sqrt(1 - beta * beta)


print(
    "A. THE ANISOTROPY, CLOSED (two arms of one length d at right angles, the rows at one pace c in the lattice's frame)"
)
print(
    "   beta | along: 2 d / (c (1 - beta^2)) over 2 d / c = gamma^2 | across: gamma | the fractional difference gamma - 1 | beta^2 / 2"
)
for beta in (0.4297, 0.2148, 0.1074, 1.0e-4, 1.23e-3):
    g = gamma(beta)
    print(f"   {beta:.4e} | {g * g:.10f} | {g:.10f} | {g - 1:.3e} | {beta * beta / 2:.3e}")
print(
    "   the Earth's orbital speed 30 km/s (beta 1.0e-4): 5.0e-9; the cosmic background's 370 km/s (1.23e-3): 7.6e-7; the resonator bounds 1e-17 (Herrmann et al. 2009) and 9.2 +- 10.7 x 1e-19 (Nagel et al. 2015): FAIL by nine to twelve orders unless the laboratory is at rest in the lattice's frame to 1.3 m/s all year"
)
print()

print(
    "B. A RIGID ARM IS A CONTACT BOND OF WHOLE LINKS: nothing of the six verbs shortens a Link (the position accumulator carries one Link per carry; the contact refuses a step onto an occupant); the round trips of A are exact on it"
)
print()


def maxwell_force(x: float, y: float, beta: float, ux: float, uy: float) -> tuple[float, float]:
    """Lorentz's force on a unit probe moving at (ux, uy) from a unit source moving at beta
    along x; (x, y) from the source's PRESENT position: E = (1 - beta^2) (x, y) / D^3 with
    D^2 = x^2 + (1 - beta^2) y^2, B = beta x_hat x E (c = 1), and u x B = beta (x_hat (u . E)
    - E u_x), so F_x = E_x + beta u_y E_y and F_y = E_y (1 - beta u_x); for a co-moving probe
    (u = beta x_hat) F = (E_x, (1 - beta^2) E_y). Attractive: the sign minus."""
    b2 = 1 - beta * beta
    d3 = (x * x + b2 * y * y) ** 1.5
    ex, ey = b2 * x / d3, b2 * y / d3
    return -(ex + beta * uy * ey), -ey * (1 - beta * ux)


def gradient_force(x: float, y: float, beta: float, ux: float, uy: float) -> tuple[float, float]:
    """Minus the gradient of the age moment A = 1 / D, D^2 = x^2 + (1 - beta^2) y^2 (the
    Lienard-Wiechert scalar potential of a uniformly moving source, DERIVATIONS 12.1),
    attractive: -grad A = -(x, (1 - beta^2) y) / D^3; no velocity of the probe enters."""
    b2 = 1 - beta * beta
    d3 = (x * x + b2 * y * y) ** 1.5
    return -x / d3, -b2 * y / d3


def integrate(beta: float, force, r0: float, turns: float, dt: float = 0.25):
    """A probe of mass 1 (E_0 = 1, c = 1) about a source of the coupling 1, both moving at
    beta along x; the relative coordinate (x, y) from the source's present position; the
    probe's momentum p with v = p / E, E = sqrt(1 + p . p); the rest orbit circular at r0
    with v_orb = 1 / sqrt(r0) (the coupling 1: v^2 / r = 1 / r^2), the Newtonian regime at
    r0 = 100 (v_orb = 0.1). The launch: at the top of the orbit the probe's velocity in
    the source's frame is v_orb along x; in the lattice's frame the relativistic sum
    u = (v_orb + beta) / (1 + v_orb beta), p = u / sqrt(1 - u^2). Leapfrog: half kick,
    drift, half kick."""
    v_orb = 1 / math.sqrt(r0)
    u = (v_orb + beta) / (1 + v_orb * beta)
    x, y = 0.0, r0
    px, py = u / math.sqrt(1 - u * u), 0.0
    period_rest = 2 * math.pi * r0 / v_orb
    t = 0.0
    xs, ys = [], []
    e = math.sqrt(1 + px * px + py * py)
    fx, fy = force(x, y, beta, px / e, py / e)
    while t < turns * period_rest * gamma(beta):
        px += 0.5 * fx * dt
        py += 0.5 * fy * dt
        e = math.sqrt(1 + px * px + py * py)
        x += (px / e - beta) * dt
        y += (py / e) * dt
        fx, fy = force(x, y, beta, px / e, py / e)
        px += 0.5 * fx * dt
        py += 0.5 * fy * dt
        t += dt
        xs.append(x)
        ys.append(y)
        if math.hypot(x, y) > 20 * r0 or math.hypot(x, y) < 0.02 * r0:
            break
    return xs, ys, t


def extents(xs, ys):
    return max(xs) - min(xs), max(ys) - min(ys)


def period(xs, ys, dt):
    """The first return of the angle to its start (the angle about the origin unwrapped)."""
    a0 = math.atan2(ys[0], xs[0])
    total = 0.0
    prev = a0
    for i in range(1, len(xs)):
        a = math.atan2(ys[i], xs[i])
        d = a - prev
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        total += d
        prev = a
        if abs(total) >= 2 * math.pi:
            return i * dt
    return float("nan")


print(
    "C. A PUSH-BOUND ARM IN MOTION (the continuum, floating point, labelled: the relative orbit of a light probe about a heavy source both at beta along x; the relativistic dispersion; the rest orbit circular at r0 = 100, v_orb = 0.1 c, its period 2 pi r0 / v_orb)"
)
print(
    "   beta | the push | the extents along / across over the rest diameter 2 | their ratio (Lorentz: 1 / gamma) | the period over the rest period (Lorentz: gamma) | the orbit's end"
)
for beta in (0.2148, 0.4297, 0.6):
    for name, force in (
        ("Lorentz's force (Maxwell's field of the moving source)", maxwell_force),
        ("-grad A alone (covariant-readings-v1's (ii) as amended)", gradient_force),
    ):
        r0 = 100.0
        xs, ys, t_end = integrate(beta, force, r0, 3)
        ex, ey = extents(xs, ys)
        per = period(xs, ys, 0.25)
        rest_period = 2 * math.pi * r0 / (1 / math.sqrt(r0))
        r_end = math.hypot(xs[-1], ys[-1])
        end = "bound" if 0.1 * r0 < r_end < 10 * r0 else ("escaped" if r_end >= 10 * r0 else "fell in")
        print(
            f"   {beta:.4f} | {name} | {ex / (2 * r0):.4f} / {ey / (2 * r0):.4f} | {ex / ey:.4f} (1 / gamma = {1 / gamma(beta):.4f}) | {per / rest_period:.4f} (gamma = {gamma(beta):.4f}) | {end} after {t_end / rest_period:.1f} rest periods"
        )
print(
    "   under Lorentz's force the thrown orbit is the rest orbit contracted by 1 / gamma along the motion with the period gamma (Lorentz 1904); under -grad A alone the force is gamma^2 times Lorentz's on every Node of the co-moving orbit (the identity of the note's section 3), a stiffer orbit, not the contracted one"
)
print()

print(
    "D. THE SOURCE'S VELOCITY IS ENCODED LOCALLY: the flow along the retarded direction n_ret, the gradient of A from the present position; the angle between them at the Node (x, y) from the present position"
)
print(
    "   beta | (x, y) | n_ret (the flow's direction) | -grad A's direction | the angle between them, degrees | asin(beta) for comparison at x = 0"
)
for beta in (0.2148, 0.4297):
    for x, y in ((0.0, 1.0), (1.0, 1.0), (-1.0, 1.0), (0.5, 2.0)):
        # the retarded position: the source was at x_ret = x_present - beta * R_ret with R_ret = |(x - (-beta R_ret)... solve R_ret: |(x + beta R, y)| = R
        # (x + beta R)^2 + y^2 = R^2 -> (1 - beta^2) R^2 - 2 beta x R - (x^2 + y^2) = 0
        a = 1 - beta * beta
        r_ret = (2 * beta * x + math.sqrt(4 * beta * beta * x * x + 4 * a * (x * x + y * y))) / (2 * a)
        nx, ny = (x + beta * r_ret) / r_ret, y / r_ret
        gx, gy = gradient_force(x, y, beta, 0.0, 0.0)
        gx, gy = -gx, -gy  # the direction away from the source, as n_ret is
        norm = math.hypot(gx, gy)
        gx, gy = gx / norm, gy / norm
        ang = math.degrees(math.acos(max(-1.0, min(1.0, nx * gx + ny * gy))))
        print(
            f"   {beta:.4f} | ({x:+.1f}, {y:+.1f}) | ({nx:+.4f}, {ny:+.4f}) | ({gx:+.4f}, {gy:+.4f}) | {ang:6.2f} | {math.degrees(math.asin(beta)):6.2f}"
        )
print(
    "   two readings of one Node (the first moment and the six-Port difference of the age moment) disagree in direction by the source's aberration: a road to the magnetic term without a label on the row, named for source-velocity-v1's designer; at series K's fan the Port difference is not a field (the light-bending note, section 4), so the road needs the dense fan"
)
