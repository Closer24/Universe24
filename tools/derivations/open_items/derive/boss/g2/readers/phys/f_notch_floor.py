"""Hostile physicist, check F: does W's late growth in t13 probe 2 depend on the hand's energy? Hands laid with
p = -1, -300, -3000 (a stride of -1) and the probe's 30000 (a stride of 10), 12000 rounds each, one Node-clock.

Clock: a hand on its spring winding its own 00 slot, as in t13 probe 2.
Algebra: whole numbers; the one-site replica of the first-order form (checked in check A).
Board: one Node-clock.
Clicks: n/a.

Run: <t24b>/.venv/bin/python -I f_notch_floor.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from a_source_and_energy_lib import tick1  # noqa: E402

REST = 3000
print("== F. W at rounds 0, 2000, ..., 12000 for hands of very different energy (2E0 = p0^2 / W)")
for p0 in (-1, -300, -3000, 30000):
    x = (0, p0, 0, 0, 0, 0, 0, 0)
    marks = []
    for t in range(12001):
        if t % 2000 == 0:
            marks.append(REST + x[2])
        if t < 12000:
            x, _ = tick1(x)
    e0 = (p0 * p0) // REST
    print(f"  p0 = {p0:6d} (2E0 = {e0:6d}): W = {marks}")
print("  reading: once a hand's swing has fallen to the notch (strides 0 and 1) its source is set by W and the notch, not by the energy it was laid with; the growth then is the act's at sub-notch strides, which no continuum energy argument describes")
