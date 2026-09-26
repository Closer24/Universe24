"""ITEM 1 of record 2134: a matter record falls in a content gradient in three dimensions,
measured on the amplitude envelope. The rule alone (rule_alone.py), no motion rule.

The board [400, 64, 64], periodic across, open along x (the level 0 beyond the faces), the
packet at the board's middle so that the two faces' reflections are symmetric. The content
c(x) = C0 + g (x - 200) (the declared gradient; U = c / (2 Gamma) about 0.05). The record: a
Gaussian packet of width 20 Links at the amplitude 2^19, its before level the standing
rotation of the kind [800, 850] (no well: a free packet, as the reviewer's of record 2132; a
first run with a packet of width 8 on [200, 24, 24] spread to the board in 500 intervals and
its control drifted by the near face's reflection, so it is not read). The control: g = 0.
Read: the envelope's centroid along x every 100 intervals, the acceleration by second
differences over windows of 300. HOST.

    PYTHONPATH=src python docs/designs/rule_alone/item1_fall.py [g] [intervals]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule_alone as R  # noqa: E402

SHAPE = (400, 64, 64)
WRAP = (False, True, True)
KIND = (800, 850)
C0 = 1000
START_X = 200.0
WIDTH = 20.0
AMPLITUDE = 1 << 19
WINDOW = 300


def run(g: int, intervals: int) -> dict:
    num = np.full(SHAPE, KIND[0], dtype=R.INT)
    den = np.full(SHAPE, KIND[1], dtype=R.INT)
    x = np.arange(SHAPE[0], dtype=R.INT).reshape(SHAPE[0], 1, 1)
    content = np.broadcast_to(C0 + g * (x - int(START_X)), SHAPE).astype(R.INT)
    read, own, wall = R.coefficients(num, den, content)
    cos_omega = R.rest_rotation(read, own, wall)
    middle = SHAPE[1] // 2
    cos_start = float(cos_omega[int(START_X), middle, middle])
    now, before = R.gaussian_packet(
        SHAPE, (START_X, float(middle), float(middle)), WIDTH, AMPLITUDE, cos_start
    )
    remainder = np.zeros(SHAPE, dtype=R.INT)
    readings = []
    t0 = time.time()
    for t in range(intervals + 1):
        if t % 100 == 0:
            e2 = R.envelope_squared(now, before, cos_omega)
            cx, cy, cz = R.centroid(e2)
            spread = float(
                np.sqrt((e2 * (np.arange(SHAPE[0]).reshape(-1, 1, 1) - cx) ** 2).sum() / e2.sum())
            )
            readings.append(
                {"t": t, "x": cx, "y": cy, "z": cz, "width_x": spread, "peak": int(np.abs(now).max())}
            )
        if t < intervals:
            now, before, remainder = R.step(now, before, remainder, read, own, wall, WRAP)
    seconds = time.time() - t0
    # the acceleration by second differences over windows of WINDOW intervals
    xs = {r["t"]: r["x"] for r in readings}
    accelerations = []
    for t in range(WINDOW, intervals - WINDOW + 1, WINDOW):
        if t - WINDOW in xs and t + WINDOW in xs:
            a = (xs[t + WINDOW] - 2 * xs[t] + xs[t - WINDOW]) / (WINDOW * WINDOW)
            accelerations.append({"t": t, "a": a})
    return {
        "g": g,
        "intervals": intervals,
        "shape": SHAPE,
        "kind": KIND,
        "C0": C0,
        "width": WIDTH,
        "amplitude": AMPLITUDE,
        "cos_omega_at_start": cos_start,
        "readings": readings,
        "accelerations": accelerations,
        "host_seconds": seconds,
    }


def main() -> None:
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    result = run(g, intervals)
    out = Path(__file__).resolve().parent / f"item1_fall_g{g}.json"
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    for r in result["readings"]:
        print(
            f"t {r['t']:5d}  x {r['x']:9.4f}  y {r['y']:7.3f}  z {r['z']:7.3f}  width {r['width_x']:7.3f}  peak {r['peak']}"
        )
    for a in result["accelerations"]:
        print(f"acceleration at t {a['t']}: {a['a']:.4e} Links per interval^2")
    print(f"HOST {result['host_seconds']:.1f} s; written {out.name}")


if __name__ == "__main__":
    main()
