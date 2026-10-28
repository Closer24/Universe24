"""Toy reading: the Mesh tension F2 clamps on the A1 course (Animate; the owner's word of 2026-10-28, 14:3x UTC:
"think through the clocks and the tensor what its carry is").

It runs the one big bang at 5,000,000 quanta for 60 ticks with draft C's push and the `dial` variant of many_bangs.py
read at the tick's start (draft C bit for bit), and prints per tick:
  - the stretch X (the time gear);
  - the axis gears and their sum (the trace);
  - the tension t of every Spoke, the mean of its two ends' axis gears rounded half up, as meshes.factors reads it;
  - how many of the 6 x 64 Mesh readings fall inside [0, Gamma];
  - the tension over the stretch, t / X.
Usage: copy beside many_bangs.py (draft C's tree at 33d9ecaa) and run `python -I tension_scale.py`.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("TREE", "/tmp/reader/t24")
sys.argv = [os.path.join(HERE, "many_bangs.py"), ROOT, "dial", "5000000", "0"]
os.environ["READ"] = "start"
sys.path[:0] = [ROOT + "/src", ROOT, HERE]

# the harness's set-up alone (its drives, its turnover and its audit), not its run
SETUP = open(os.path.join(HERE, "many_bangs.py")).read().split("click.click = booked")[0]
exec(SETUP)  # noqa: S102

import numpy as np  # noqa: E402

from event_universe.core.rule3 import carries  # noqa: E402
from event_universe.core.spokes import SPOKE_SIDES  # noqa: E402
from event_universe.meshes import even  # noqa: E402

clock = make_clock()  # noqa: F821
regulator = clock.train(REGULATOR)  # noqa: F821
print("Gamma", clock.full_rate, "the regulator's gears", len(regulator.gears))
for at in range(1, 61):
    clock.tick()
    X = clock.train(REGULATOR).gears[0].now  # noqa: F821
    axes = [g.now for g in clock.train(REGULATOR).gears[1:4]]  # noqa: F821
    ts = [carries(even(axes[a], s) + 1, 2) for s, (a, _side) in enumerate(SPOKE_SIDES)]
    tmin, tmax = min(int(np.min(t)) for t in ts), max(int(np.max(t)) for t in ts)
    inside = sum(int(((t >= 0) & (t <= clock.full_rate)).sum()) for t in ts)
    amin, amax = min(int(np.min(a)) for a in axes), max(int(np.max(a)) for a in axes)
    sums = axes[0] + axes[1] + axes[2]
    if at % 3 == 0 or at < 4:
        print(
            f"tick {at}: X {int(X.min())}..{int(X.max())}  axis gears {amin}..{amax}  "
            f"trace {int(np.min(sums))}..{int(np.max(sums))}  tension {tmin}..{tmax}  "
            f"inside [0, Gamma] {inside} of {6 * X.size}  t/X {tmin / int(X.max()):.3g}..{tmax / int(X.max()):.3g}"
        )
