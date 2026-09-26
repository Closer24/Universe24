"""HOST calibration: the centroid speed of a free packet of rms sigma at K = 0.11 under the rule."""

import math, sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import rule_alone as R, item9_pair as Pm

SHAPE = (160, 48, 48)
WRAP = (True, True, True)
num = np.full(SHAPE, 800, dtype=R.INT)
den = np.full(SHAPE, 850, dtype=R.INT)
read, own, wall = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
cos0 = float(R.rest_rotation(read, own, wall)[0, 0, 0])
k, wk = Pm.wave_number(0.1, 800, 850)
print(f"K {k:.4f} omega_K {wk:.4f} v_g(plane wave) 0.1")
for sigma in (3.0, 4.2, 7.0, 12.0):
    grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in SHAPE], indexing="ij")
    r2 = sum((g - c) ** 2 for g, c in zip(grids, (40.0, 24.0, 24.0)))
    e = (1 << 11) * np.exp(-r2 / (2 * sigma * sigma))
    dx = grids[0] - 40.0
    now = np.rint(e * np.cos(k * dx - wk / 2)).astype(R.INT)
    before = np.rint(e * np.cos(k * dx + wk / 2)).astype(R.INT)
    rem = np.zeros(SHAPE, dtype=R.INT)
    xs = []
    for t in range(601):
        if t % 100 == 0:
            e2 = R.envelope_squared(now, before, np.full(SHAPE, cos0))
            xs.append(R.centroid(e2)[0])
        now, before, rem = R.step(now, before, rem, read, own, wall, WRAP)
    speeds = [(xs[i + 1] - xs[i]) / 100 for i in range(len(xs) - 1)]
    print(
        f"sigma {sigma}: centroid x {[round(x, 1) for x in xs]}; speed per 100 {[round(s, 3) for s in speeds]}; mean {(xs[-1] - xs[0]) / 600:.3f}"
    )
