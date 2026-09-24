"""Row M1's pin under the counting form (SIZING.md: the take lines sinks outside the ladder, the
screen's 121 sets the ladder, the matter lamp's wheel [1, 2048] with each u once), computed BLIND
on the declared layer of DECLARATIONS.md section 12 before any run of the world: the lattice map of
`two_slits_1024.py` (imported) run with the matter kind's pair [800, 809] in the well form (the
massive family's rule, omega_0 = acos(800 / 809)), the lamp driven at the declared omega = 0.33408
(lambda_dB = 12 Links) for 8 periods, the mirror line at x = 40 with the openings of width 1 at y =
48 and 80, the screen at x = 104, the layer 128 x 128 with y PERIODIC as declared (the form of
record, its images folded onto the screen), and beside it the margin form (the two-source geometry
of `matter_wave_pins.py`) and the sponge form (y open with lossy faces). The click pattern of one
wheel by the engine's cell choice ((u + 1 / 2) / W in the cell's cumulative interval, `cell_of`
over the ladder's own sum); THE PIN'S STATISTIC, the side lobe's count centroid over y in [64 + 14,
64 + 40], read on the counts against the map's own offer centroid (the difference the grain, which
replaces section 12's Poisson sd 0.23); the two-source formula's centroid (27.79, the band's k per
ray, no lattice) printed beside as the statistic's earlier derivation. The dimmest chosen cell's
share gives the rung wheel the screen's sets need, the screen's share of the norm taken as the
light row's 3 percent (a declaration with a margin; the matter world's own share is read at its
preliminary, GAMEBOARD).

    PYTHONPATH=src python docs/designs/detector_law/matter_waves_2048.py > docs/designs/detector_law/matter_waves_2048.out
"""

import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matter_wave_pins as mw  # noqa: E402
from two_slits_1024 import FIRST_DRAFT, counts_of, run_layer, rung_line, screen_of  # noqa: E402

MATTER = (mw.NUM, mw.DEN)
WHEEL = 2048
PERIODS = 8
LOBE = (14, 40)


def main() -> None:
    g = FIRST_DRAFT  # section 12's layer: 128 x 128, d = 32, L = 64, the openings of width 1
    omega = mw.omega_of_k(2 * math.pi / 12.0)
    ys, pat = mw.screen_pattern(omega, g.separation, g.length, 60, per_direction=True)
    lo, hi = LOBE
    inside = (ys >= lo) & (ys <= hi)
    formula = float(np.sum(ys[inside] * pat[inside]) / pat[inside].sum())
    print(
        f"lambda_dB = 12 Links, omega = {omega:.5f} (the period {2 * math.pi / omega:.2f} intervals), the"
        f" matter pair [{MATTER[0]}, {MATTER[1]}] in the well form, the train {PERIODS} periods; the layer"
        f" {g.height} tall, d = {g.separation}, L = {g.length}, the openings of width {g.width}; the screen's"
        f" cells y = {g.screen[0]} .. {g.screen[1]}; the wheel [1, {WHEEL}] each u once; the side lobe's"
        f" window y in [64 + {lo}, 64 + {hi}]; the two-source formula's centroid (matter_wave_pins.py, the"
        f" band's k per ray, no lattice): 64 + {formula:.3f}"
    )
    for boundary in ("periodic", "margin", "sponge"):
        t0 = time.time()
        offer, train = run_layer(
            g, g.openings(g.two), PERIODS, boundary, pair=MATTER, period=2 * math.pi / omega, well=True
        )
        screen = screen_of(g, offer)
        shares = screen / screen.sum()
        counts = counts_of(shares, WHEEL)
        y = np.arange(g.screen[0], g.screen[1] + 1) - g.axis
        lobe = (y >= lo) & (y <= hi)
        exact = float(np.sum(y[lobe] * shares[lobe]) / shares[lobe].sum())
        n_lobe = int(counts[lobe].sum())
        by_counts = float(np.sum(y[lobe] * counts[lobe]) / n_lobe) if n_lobe else float("nan")
        side = int(y[lobe][np.argmax(shares[lobe])])
        maxima = [
            int(y[i])
            for i in range(1, len(y) - 1)
            if shares[i] > shares[i - 1]
            and shares[i] >= shares[i + 1]
            and shares[i] > 0.3 * shares.max()
        ]
        label = "AS DECLARED, the form of record" if boundary == "periodic" else "beside"
        print(
            f"\nTHE MATTER WAVES, the y boundary {boundary.upper()} ({label}), the train {train} intervals;"
            f" {time.time() - t0:.1f} s HOST"
        )
        print(
            f"   THE PIN'S STATISTIC, the side lobe's count centroid: 64 + {by_counts:.3f} on the counts"
            f" ({n_lobe} clicks in the lobe) against the map's own offer centroid 64 + {exact:.3f}: the"
            f" grain {abs(by_counts - exact):.3f} Node at this wheel; the side maximum at y = 64 + {side}"
            f" ({int(counts[lobe][np.argmax(shares[lobe])])} clicks), the centre"
            f" {int(counts[g.axis - g.screen[0]])}; the pattern's maxima above 0.3 of the centre at y = 64 +"
            f" {maxima}"
        )
        print("   " + rung_line(shares, counts, g.screen[0]))
        print(
            f"   the counts per Node, y = {g.screen[0]} .. {g.screen[1]}: "
            + " ".join(str(int(c)) for c in counts)
        )


if __name__ == "__main__":
    main()
