"""The runaway's per-swing factor F against the pinion and Gamma (separated tops, as runaway.py), on the committed act.

usage: python3 -I factor.py > factor.txt
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py and runaway.py
import rig
from runaway import swing_tops

from tensor24.engine import step
from tensor24.runner.load import ruler_of

print(
    "Per-swing factor F of the runaway (top_{k+1}/top_k once past the ruler), one Node-clock, one matter hand"
)
for gamma in (250, 1000, 4000):
    period = 2 * math.pi * math.sqrt(gamma / 2)
    R = ruler_of(gamma)[-1] / gamma
    for off in (20, 50, 200, 1000):
        w = math.acos(1 - 1 / off)
        n = Fraction(40 * off, 50) if off <= 200 else Fraction(800)
        layout, s, info = rig.matter_hand(gamma, n, pinion_off=off)
        last = int(layout.ruler.last)
        allowed = np.ones((1, 1), dtype=object)
        counts = [0]
        for _ in range(int(6 * period)):
            s, _ = step.tick(layout, s, allowed)
            counts.append(int(s.a[layout.ruler.row, 0]))
            if abs(counts[-1]).bit_length() > 400:
                break
        tops = swing_tops(counts)
        facs = [b[1] / a[1] for a, b in zip(tops, tops[1:], strict=False) if a[1] > last and b[1] > 0]
        spacing = [b[0] - a[0] for a, b in zip(tops, tops[1:], strict=False)]
        print(
            f"  Gamma {gamma:4d} (R = Y_last/Gamma = {R:.3f}), w = {w:.4f}, n = {info['quanta_per_node']:.0f}: "
            f"F per swing {[f'{f:.4e}' for f in facs[:5]]}; top spacing {spacing[:5]} vs P = {period:.1f}; "
            f"log F/log R = {[round(math.log(f) / math.log(R), 3) for f in facs[:5] if f > 1]}"
        )
