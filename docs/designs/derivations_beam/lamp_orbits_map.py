"""The lamp worlds of series D under the directional drive (form B), the pins'
arithmetic (read-only, the mathematician, 2026-09-21; the section "The lamp
worlds" of examples/events/orbit/README.md; DERIVATIONS_BEAM 21.5 row 58).
The generator `examples/events/orbit/make_worlds.py` is the one source of the
fan, the emission, the momentum and the pace; this script integrates the law's
continuum limit on the plane with that momentum (the smooth 1 / r push of the
fan's mean, the directional drive's pace on a heading, one step per interval
as the engine steps, the source unpushed) and reads from it what the run is
pinned to: the angular period T, the radial period, the extents, the
precession per radial period as the angle between successive closest
approaches, T(24) / T(12); and it counts the ring Nodes from which a fan line
runs into the source, the places the detector's clicks come from. Every number
is a GAMEBOARD reading of the design (derived before any run); the detector's
expected readings are labelled. No run.

Run from the repository root:

    PYTHONPATH=src python docs/designs/derivations_beam/lamp_orbits_map.py > docs/designs/derivations_beam/lamp_orbits_map.out
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "orbit_make_worlds", ROOT / "examples" / "events" / "orbit" / "make_worlds.py"
)
GEN = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(GEN)

S = GEN.LAMP_WIDTH
A = (
    GEN.EMISSION * GEN.LABEL_MAGNITUDE * GEN.FLOW_CONSTANT / (2 * math.pi)
)  # the push at r = 1, units of n per interval
C_ROWS = 64 / 110  # the rows' pace on a heading, Links per interval
STEP = 0.05  # the integration step in intervals (the engine steps once per interval; the smooth limit is stepped finer)


PACE_RULE = "form B"


def pace(n: float) -> float:
    """The pace per unit of content at the momentum n: the directional drive's
    (form B), today's per-axis rule, or the Newtonian n / S (the check)."""
    if PACE_RULE == "form B":
        return GEN.form_b_pace(n, S)
    if PACE_RULE == "today":
        return n / (S + n)
    return n / S


def integrate(radius: float, n0: float, intervals: int) -> dict[str, object]:
    """The continuum-mean orbit: dn/dt = -(A / r) r_hat per interval, dx/dt = pace(|n|) n_hat (RK2)."""
    x, y = radius, 0.0
    nx, ny = 0.0, n0
    t = 0.0
    angle_total = 0.0
    last_angle = 0.0
    radii: list[tuple[float, float]] = []
    pericentres: list[tuple[float, float, float]] = []  # (t, angle, r)
    r_prev2 = r_prev = radius
    t_prev = 0.0
    a_prev = 0.0
    angular_period: float | None = None

    def rates(px: float, py: float, qx: float, qy: float) -> tuple[float, float, float, float]:
        r = math.hypot(px, py)
        m = math.hypot(qx, qy)
        v = pace(m)
        return v * qx / m, v * qy / m, -A / r * px / r, -A / r * py / r

    while t < intervals:
        k1 = rates(x, y, nx, ny)
        k2 = rates(
            x + 0.5 * STEP * k1[0],
            y + 0.5 * STEP * k1[1],
            nx + 0.5 * STEP * k1[2],
            ny + 0.5 * STEP * k1[3],
        )
        x += STEP * k2[0]
        y += STEP * k2[1]
        nx += STEP * k2[2]
        ny += STEP * k2[3]
        t += STEP
        r = math.hypot(x, y)
        angle = math.atan2(y, x)
        d = angle - last_angle
        if d > math.pi:
            d -= 2 * math.pi
        if d < -math.pi:
            d += 2 * math.pi
        angle_total += d
        last_angle = angle
        if angular_period is None and angle_total >= 2 * math.pi:
            angular_period = t
        radii.append((t, r))
        # a closest approach: a local minimum of r between three successive samples
        if r_prev < r_prev2 and r_prev <= r and t > 2 * STEP:
            pericentres.append((t_prev, a_prev, r_prev))
        r_prev2, r_prev, t_prev, a_prev = r_prev, r, t, angle_total
    rs = [r for _, r in radii]
    return {
        "angular_period": angular_period,
        "r_min": min(rs),
        "r_max": max(rs),
        "r_mean_first": sum(r for tt, r in radii if angular_period and tt <= angular_period)
        / max(1, sum(1 for tt, _ in radii if angular_period and tt <= angular_period)),
        "pericentres": pericentres,
        "turns": angle_total / (2 * math.pi),
        "n_end": math.hypot(nx, ny),
    }


print(
    "1. THE DECLARED MOMENTUM AND THE ANALYTIC CIRCLE UNDER THE DIRECTIONAL DRIVE (GAMEBOARD, derived)"
)
real, whole = GEN.orbit_momentum_form_b(S)
print(
    f"   the fan: {len(GEN.FAN)} directions, q = {GEN.EMISSION:.2f} units per interval, L = {GEN.LABEL_MAGNITUDE:.4f}; A = q L C / (2 pi) = {A:.5f} units of n per interval at r = 1 (the plane's 1 / r push)"
)
print(
    f"   the pace on a heading v = 64 n / (64 S + 110 n) at S = {S}; the circular condition n v = A: 64 n^2 = A (64 S + 110 n), n = {real:.3f}; the declared whole n = {whole} ({whole * GEN.LABEL_SCALE} label units per unit of content; today's rule gave n = 8.831 -> 9, 576)"
)
v_whole = pace(whole)
v_real = pace(real)
print(
    f"   the pace at n = {whole}: {v_whole:.4f} Links per interval (beta = {v_whole / C_ROWS:.3f}); at the real root {v_real:.4f}; the kept momentum 576 (n = 9) gives {pace(9):.4f} (the implementer's 0.1896)"
)
for r in GEN.RADII:
    print(
        f"   the analytic circle at r = {r}: T = 2 pi r / v = {2 * math.pi * r / v_whole:.1f} intervals at n = {whole} ({2 * math.pi * r / pace(9):.1f} at the kept 576)"
    )
print(
    f"   the ratio T(24) / T(12) = 2 exactly on the plane (the same v at every r); the kicks: 64 label units on {whole * 64}: {math.degrees(64 / (whole * 64)):.1f} degrees per ray, {2 * math.pi * 24 / v_whole / 10:.0f} shells per orbit at r = 24"
)
print()

print(
    f"2. THE CONTINUUM-MEAN ORBIT INTEGRATED WITH THE DECLARED n = {whole} (GAMEBOARD, derived): the whole n above the circle's {real:.3f} makes a rosette, not a circle"
)
results = {}
for r in GEN.RADII:
    res = integrate(float(r), float(whole), 4000)
    results[r] = res
    peris = res["pericentres"]
    radial = [peris[i + 1][0] - peris[i][0] for i in range(len(peris) - 1)]
    advance = [math.degrees(peris[i + 1][1] - peris[i][1]) for i in range(len(peris) - 1)]
    print(
        f"   r = {r}: the angular period T = {res['angular_period']:.0f} intervals; r from {res['r_min']:.1f} to {res['r_max']:.1f}, the mean over the first turn {res['r_mean_first']:.1f}; {res['turns']:.2f} turns in 4000 intervals; |n| at the end {res['n_end']:.2f}"
    )
    print(
        f"      the closest approaches at t = {', '.join(f'{p[0]:.0f}' for p in peris[:6])} (r = {', '.join(f'{p[2]:.1f}' for p in peris[:6])}): the radial period {', '.join(f'{x:.0f}' for x in radial[:5])}; the angle between successive closest approaches {', '.join(f'{x:.1f}' for x in advance[:5])} degrees, the precession per radial period {', '.join(f'{x - 360:+.1f}' for x in advance[:5])} degrees (the 1 / r force's apsidal angle pi / sqrt 2 = 127.28: {2 * 127.28 - 360:+.2f})"
    )
t24, t12 = results[24]["angular_period"], results[12]["angular_period"]
print(f"   T(24) / T(12) = {t24 / t12:.3f} (the plane's exponent 1: 2; space's 3 / 2: 2.83)")
print()

print(
    "2b. WHY NOT -105.4: THE APSIDAL ANGLE DEPENDS ON THE PACE'S DEPENDENCE ON THE MOMENTUM (the integrator checked on the Newtonian pace)"
)
for rule, n_start, label in (
    ("newton", 10.0, "the Newtonian pace v = n / S (the plane's own law, row 58's -105.44)"),
    ("today", 9.0, "today's per-axis pace n / (S + n) at the registered n = 9"),
    ("form B", 10.0, "the directional drive's pace at n = 10"),
):
    PACE_RULE = rule
    if rule == "newton":
        # the circular n under v = n / S: n^2 / S = A
        n_start = math.sqrt(A * S) * 1.04  # 4 percent above the circle, as 10 is above 9.63
    res = integrate(24.0, n_start, 4000)
    peris = res["pericentres"]
    adv = [math.degrees(peris[i + 1][1] - peris[i][1]) - 360 for i in range(min(3, len(peris) - 1))]
    local = {"newton": 1.0, "today": S / (S + n_start), "form B": 64 * S / (64 * S + 110 * n_start)}[
        rule
    ]
    print(
        f"   {label}: the precession per radial period {', '.join(f'{x:+.1f}' for x in adv)} degrees; the pace's local exponent d ln v / d ln n = {local:.3f}, the apsidal angle {(adv[0] + 360) / 2:.1f} degrees"
    )
PACE_RULE = "form B"
print(
    "   the integrator reproduces the plane's -105.4 under the Newtonian pace; under the cap the pace grows more slowly than the momentum (the local exponent 0.65 at n = 10, beta = 0.35), the radial oscillation is faster against the turning, and the apsidal angle is 139.7 degrees in place of 127.3: the restated pin for these worlds is -81 +- 15 degrees per radial period, the difference form B's, not the fan's"
)
print()

print(
    "3. THE DETECTOR AT THE SOURCE: WHERE ITS CLICKS COME FROM (the detector's EXPECTED readings, derived)"
)
fan = {(a, b) for a, b, _c in GEN.FAN}
for r in GEN.RADII:
    ring = [
        (x, y)
        for x in range(-r - 2, r + 3)
        for y in range(-r - 2, r + 3)
        if r - 0.5 < math.hypot(x, y) <= r + 0.5
    ]
    lit = [
        (x, y)
        for x, y in ring
        if (x // math.gcd(abs(x), abs(y)), y // math.gcd(abs(x), abs(y))) in {(-a, -b) for a, b in fan}
    ]
    print(
        f"   r = {r}: of the {len(ring)} Nodes of the ring, {len(lit)} lie on a fan line through the source (the probe's ray toward the source exists there): a fraction {len(lit) / len(ring):.2f}; one shell every 10 intervals, so about {len(lit) / len(ring) * 2 * math.pi * r / v_whole / 10:.0f} clicks per orbit of {2 * math.pi * r / v_whole / 10:.0f} shells"
    )
    print(
        f"      each click's arrival direction is the probe's direction from the source reversed, and its age the flight {r} Links x 110 / 64 = {r * 110 / 64:.0f} intervals on a heading: r = age x c per direction; the clicks' directions turn through 2 pi in T, the ages' minimum in the direction of the closest approach"
    )
print()

print("4. THE PINS RESTATED FROM ROW 58 FOR THESE WORLDS, AND WHAT REFUTES THEM")
margin = 0.09
print(
    f"   s32_r24_lamp: T = {t24:.0f} intervals (the analytic {2 * math.pi * 24 / v_whole:.0f}; 21.5 wrote 795 at the kept 576), within the continuum's own margin of {margin:.0%} (12b.2: the burst field and the fan's grain): {t24 * (1 - margin):.0f} to {t24 * (1 + margin):.0f}; the mean radius {results[24]['r_mean_first']:.1f} +- 1 (the extents {results[24]['r_min']:.1f} to {results[24]['r_max']:.1f}); the precession per radial period {sum(math.degrees(results[24]['pericentres'][i + 1][1] - results[24]['pericentres'][i][1]) - 360 for i in range(3)) / 3:.0f} +- 15 degrees (row 58's -105 the Newtonian pace's; section 2b)"
)
print(
    f"   s32_r12_lamp: T = {t12:.0f} ({2 * math.pi * 12 / v_whole:.0f} analytic): {t12 * (1 - margin):.0f} to {t12 * (1 + margin):.0f}; the mean radius {results[12]['r_mean_first']:.1f} +- 1 (the extents {results[12]['r_min']:.1f} to {results[12]['r_max']:.1f}); the precession {sum(math.degrees(results[12]['pericentres'][i + 1][1] - results[12]['pericentres'][i][1]) - 360 for i in range(3)) / 3:.0f} +- 15 degrees"
)
print(f"   T(24) / T(12) = 2.00 +- 0.15 (the integrated {t24 / t12:.2f})")
print(
    "   what refutes: a period outside its bracket (form B's pace, the first-order slowing of the cap); a ratio at 2.83 (space's exponent on the plane) or outside 2.00 +- 0.15; a precession outside -81 +- 15 degrees (-105 would be the Newtonian pace's, 0 a closed ellipse, the 1 / r^2 force's, not the plane's 1 / r); a closed return within one Link is a circle's criterion and is not expected"
)
