"""ITEM 5 of record 2134: a wound record, the spin as winding (9.98 (3), (9) (c)): does it keep
its winding and precess? The rule alone, the well fixed (a body at rest).

The board [64, 64, 64] periodic; a body of s = 2000 on a well of side 5 at the kind [800, 850];
the record the standing mode times the winding of m = 1 about the z axis as a rotating pattern
of the two levels: now = p (x - x_c), before = p ((x - x_c) cos omega_b + (y - y_c) sin omega_b),
the pattern turning by omega_b per interval (the phase m theta added to the standing rotation,
9.98 (9) (c), written as a real pair). Read every 25 intervals (HOST): the angular momentum
about z from the record's own current, L = SUM (x J_y - y J_x) over the board; the pattern's
orientation from the dipole moments D_x = SUM x now, D_y = SUM y now (its angle, its size); the
envelope's width. The winding is kept if L holds its value and the dipole its size; it precesses
if the dipole's angle drifts from omega_b per interval.

    PYTHONPATH=src python docs/designs/rule_alone/item5_winding.py [intervals] [side]

The second argument is the well's side (5 by default; 9 for a deeper well, since the m = 1
pattern lies at the well's edge and a well of side 5 may bind no state of that sector).
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402
import rule_alone as R  # noqa: E402

SHAPE = (64, 64, 64)
WRAP = (True, True, True)
AMOUNT = 2000
EVERY = 25


def readings(now, before, cos_b, xs, ys):
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    jx = np.roll(n, -1, axis=0) * b - np.roll(b, -1, axis=0) * n
    jy = np.roll(n, -1, axis=1) * b - np.roll(b, -1, axis=1) * n
    angular = float((xs * jy - ys * jx).sum())
    dx = float((xs * n).sum())
    dy = float((ys * n).sum())
    form = n * n + b * b - 2.0 * n * b * cos_b
    total = float(form.sum())
    width = float(np.sqrt(((xs * xs + ys * ys) * form).sum() / total)) if total > 0 else math.nan
    return angular, math.hypot(dx, dy), math.atan2(dy, dx), width, int(np.abs(now).max())


def run(intervals: int, side: int = 5) -> dict:
    middle = SHAPE[0] // 2
    body = B.Body([middle, middle, middle], AMOUNT, side=side)
    t0 = time.time()
    profile, clock = B.bound_mode(SHAPE, WRAP, body)
    cos_b = clock[0] / (2.0 * clock[1])
    sin_b = math.sqrt(1.0 - cos_b * cos_b)
    xs = (np.arange(SHAPE[0]) - middle).reshape(-1, 1, 1).astype(np.float64)
    ys = (np.arange(SHAPE[1]) - middle).reshape(1, -1, 1).astype(np.float64)
    p = (
        profile.astype(np.float64) / 4.0
    )  # the pattern p (x - x_c) at the well's edge is 2 p; keep the bound
    now = np.rint(p * xs).astype(R.INT)
    before = np.rint(p * (xs * cos_b + ys * sin_b)).astype(R.INT)
    rem = np.zeros(SHAPE, dtype=R.INT)
    seeding = time.time() - t0
    content = np.zeros(SHAPE, dtype=R.INT)
    content[body.mask(SHAPE)] = AMOUNT
    num, den = body.pairs(SHAPE)
    read, own, wall = R.coefficients(num, den, content)
    rows = []
    angles = []
    t0 = time.time()
    for t in range(intervals + 1):
        angular, dipole, angle, width, peak = readings(now, before, cos_b, xs, ys)
        angles.append(angle)
        if t % EVERY == 0:
            rows.append(
                {
                    "t": t,
                    "angular": angular,
                    "dipole": dipole,
                    "angle": angle,
                    "width": width,
                    "peak": peak,
                }
            )
        if t == intervals:
            break
        now, before, rem = R.step(now, before, rem, read, own, wall, WRAP)
    unwrapped = np.unwrap(np.array(angles))
    rate = float((unwrapped[-1] - unwrapped[0]) / (len(unwrapped) - 1))
    return {
        "shape": SHAPE,
        "side": side,
        "clock": clock,
        "omega_b": math.acos(cos_b),
        "dipole_angle_rate": rate,
        "rows": rows,
        "seeding_seconds": seeding,
        "host_seconds": time.time() - t0,
    }


def main() -> None:
    intervals = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    side = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    result = run(intervals, side)
    (Path(__file__).resolve().parent / f"item5_winding_side{side}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )
    first = result["rows"][0]
    for r in result["rows"][::4]:
        print(
            f"t {r['t']:5d}  L/L0 {r['angular'] / first['angular']:8.4f}  dipole/D0 {r['dipole'] / first['dipole']:7.4f}  angle {r['angle']:7.3f}  width {r['width']:6.2f}  peak {r['peak']}"
        )
    print(
        f"the dipole's angle advances {result['dipole_angle_rate']:.5f} per interval; the mode's omega_b {result['omega_b']:.5f}; clock {result['clock']}"
    )
    print(f"HOST seeding {result['seeding_seconds']:.1f} s, run {result['host_seconds']:.1f} s")


if __name__ == "__main__":
    main()
