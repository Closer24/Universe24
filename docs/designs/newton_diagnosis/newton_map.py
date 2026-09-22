"""COMPUTATION: the continuum map of the law's own algebra on the plane, no
lattice (docs/designs/newton_diagnosis/DIAGNOSIS.md section 2). The body's
momentum n per axis in n-units (n = p / (Q M_total), one n-unit the label
of one unit of content at the scale Q = 64); the per-axis drive's pace
v_a = n_a / (S + n_a) Links per interval (BEAM_LAW note 17) or the line
drive's v_a = 64 n_a / (64 S + 110 |n|_1) (note 17 as amended on the branch
drive-default); the ring-mean push A / r toward the centre with A the
circular balance q L C / (2 pi F_plane) = 1.4838 under the key flow_link
and 1.9098 as built (DERIVATIONS_BEAM 3.3, flow_weight/ALGEBRA.md 5); and
the arrival rate's factor (1 + u / c), u the inward radial speed and c =
64 / 110 the rows' pace on a heading: a body meets each shell of rows once,
at the crossing of the world lines (the crossing rule, BEAM_LAW note 48),
so it meets the outgoing shells at the rate (1 + u / c) / 10 per interval.
One interval per step in the engine's order (the step by the momentum after
the interval before, then the push read at the new place); the launch of
the register (n tangential at r). The reading is the tool's: the mean
spacing of successive crossings of the centre column in one direction
(tools/orbit_lamp_readings.py). Every number is GAMEBOARD by formula."""

from __future__ import annotations

import math

S = 32
C = 64 / 110
TICKS = 4000


def run(
    r0: float, n0: float, a: float, doppler: bool, line_drive: bool = False
) -> list[tuple[int, float, float, float, float]]:
    x, y = float(r0), 0.0
    nx, ny = 0.0, float(n0)
    path = []
    for t in range(TICKS):
        if line_drive:
            wall = S * 64 + (abs(nx) + abs(ny)) * 110
            vx, vy = nx * 64 / wall, ny * 64 / wall
        else:
            vx, vy = nx / (S + abs(nx)), ny / (S + abs(ny))
        x += vx
        y += vy
        r = math.hypot(x, y)
        inward = -(x * vx + y * vy) / r
        push = (a / r) * ((1 + inward / C) if doppler else 1.0)
        nx -= push * x / r
        ny -= push * y / r
        path.append((t, x, y, r, math.hypot(nx, ny)))
    return path


def readings(path: list[tuple[int, float, float, float, float]]) -> dict[str, object]:
    downs, ups = [], []
    for (t0, x0, *_), (_, x1, *_) in zip(path, path[1:], strict=False):
        if x0 > 0 >= x1:
            downs.append(t0 + x0 / (x0 - x1))
        if x0 <= 0 < x1:
            ups.append(t0 + x0 / (x0 - x1))
    spacings = [b - a for a, b in zip(downs, downs[1:], strict=False)]
    spacings += [b - a for a, b in zip(ups, ups[1:], strict=False)]
    radii = [p[3] for p in path]
    turns = 0.0
    angles = [math.atan2(p[2], p[1]) for p in path]
    for a0, a1 in zip(angles, angles[1:], strict=False):
        d = a1 - a0
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        turns += d / (2 * math.pi)
    peri, apo = [], []
    for i in range(1, len(radii) - 1):
        if radii[i] < radii[i - 1] and radii[i] <= radii[i + 1]:
            peri.append((path[i][0], round(radii[i], 1)))
        if radii[i] > radii[i - 1] and radii[i] >= radii[i + 1]:
            apo.append((path[i][0], round(radii[i], 1)))
    return {
        "T": sum(spacings) / len(spacings) if spacings else None,
        "r_min": min(radii),
        "r_max": max(radii),
        "r_mean": sum(radii) / len(radii),
        "turns": turns,
        "crossings": (len(downs), len(ups)),
        "peri": peri[:10],
        "apo": apo[:10],
    }


CASES = (
    (
        "the ring-mean push A / r alone, n = 8 under the key (the pins' algebra with the drive's anisotropy and the whole 8)",
        1.4838,
        8,
        False,
        False,
    ),
    ("the same with the arrival rate's factor (1 + u / c)", 1.4838, 8, True, False),
    (
        "the factor at the exact balance n = 7.672 (a circle launched exactly)",
        1.4838,
        7.672,
        True,
        False,
    ),
    (
        "as built, A = 1.9098, n = 9, with the factor (the registered per-axis run)",
        1.9098,
        9,
        True,
        False,
    ),
    (
        "the line drive, A = 1.9098, n = 10, with the factor (the branch drive-default)",
        1.9098,
        10,
        True,
        True,
    ),
)


def main() -> None:
    print("THE NEWTON MAP: the law's continuum algebra on the plane, GAMEBOARD by formula, not a run")
    print(f"S = {S}, c = 64 / 110, {TICKS} intervals, the launch tangential at r = 12 and 24")
    for label, a, n0, doppler, line_drive in CASES:
        print(f"\n== {label}")
        periods = {}
        for r0 in (12, 24):
            found = readings(run(r0, n0, a, doppler, line_drive))
            periods[r0] = found["T"]
            t = found["T"]
            print(
                f"  r = {r0}: the tool's T over {TICKS} = {t if t is None else round(t, 1)}; "
                f"r from {found['r_min']:.1f} to {found['r_max']:.1f}, the mean {found['r_mean']:.1f}; "
                f"turns {found['turns']:.2f}; crossings {found['crossings']}"
            )
            print(f"     the pericentres (tick, r): {found['peri']}")
            print(f"     the apocentres  (tick, r): {found['apo']}")
        if periods[12] and periods[24]:
            print(f"  the ratio T(24) / T(12) = {periods[24] / periods[12]:.3f}")


if __name__ == "__main__":
    main()
