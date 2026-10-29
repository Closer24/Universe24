"""The stable swing, the runaway threshold and the runaway's factor against the pinion, on the committed act.

usage: python3 -I swing.py > swing.txt

Same setting as runaway.py (one Node-clock, one matter hand, the time gear from the bang at 0 at rest).
A. U_top per quantum against 2 tan(w/2) (Gamma-free prediction) and the period against 2 pi sqrt(Gamma/2).
B. The runaway threshold n_crit(Gamma): the least content (quanta per Node-clock) whose load passes the ruler's last
   count within 3 swings, by bisection; against the ruler's end u_L = L / Gamma and the freezing load
   u_f = ln(w sqrt(Gamma/2)) (the hand's local beat w e^-u falls to the swing's 1 per radian of swing time).
C. The runaway's per-swing factor F against the pinion (w) at Gamma 1000: is F Gamma's alone?
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py

import rig  # noqa: E402

from tensor24.engine import step  # noqa: E402


def counts_of(gamma, n, ticks, off=50, stop_past=False):
    layout, s, info = rig.matter_hand(gamma, n, pinion_off=off)
    allowed = np.ones((1, 1), dtype=object)
    last = int(layout.ruler.last)
    counts = [0]
    for _ in range(ticks):
        s, _ = step.tick(layout, s, allowed)
        c = int(s.a[layout.ruler.row, 0])
        counts.append(c)
        if stop_past and c > last:
            break
    return info, counts, last


def windows(counts, period):
    """The top of each swing: the max over successive windows of one period, from the bang."""
    p = int(round(period))
    out = []
    for k in range(len(counts) // p):
        seg = counts[k * p : (k + 1) * p]
        m = max(seg)
        out.append((k * p + seg.index(m), m))
    return out


def main() -> None:
    out = [
        "The swing on tensor24-review's act: one Node-clock, one matter hand (part 2) and the time gear",
        "",
    ]
    out.append(
        "A. U_top per quantum (Gamma-free prediction 2 tan(w/2) = 0.2007 at w = 0.2003) and the period"
    )
    for gamma in (250, 1000, 4000):
        period = 2 * math.pi * math.sqrt(gamma / 2)
        for n in (Fraction(1, 2), Fraction(1), Fraction(2), Fraction(4)):
            info, counts, last = counts_of(gamma, n, int(4 * period) + 3)
            tops = windows(counts, period)
            u = [c / gamma for _, c in tops]
            ticks = [t for t, _ in tops]
            per = [b - a for a, b in zip(ticks, ticks[1:], strict=False)]
            out.append(
                f"   Gamma {gamma:5d}, n = {info['quanta_per_node']:.3f}: U_top per swing {[round(x, 4) for x in u]}, "
                f"U_top / n = {u[0] / info['quanta_per_node']:.4f}; top-to-top {per} vs {period:.1f}"
            )
    out.append("")
    out.append(
        "B. The runaway threshold: least n whose load passes the ruler's last count within 3 swings"
    )
    w = math.acos(1 - 1 / 50)
    for gamma in (250, 500, 1000, 2000, 4000, 8000):
        period = 2 * math.pi * math.sqrt(gamma / 2)
        ticks = int(3 * period) + 3
        lo, hi = Fraction(1, 4), Fraction(40)
        info, counts, last = counts_of(gamma, hi, ticks, stop_past=True)
        assert max(counts) > last
        for _ in range(9):
            mid = (lo + hi) / 2
            info, counts, last = counts_of(gamma, mid, ticks, stop_past=True)
            if max(counts) > last:
                hi = mid
            else:
                lo = mid
        info, counts, last = counts_of(gamma, lo, ticks)
        u_top = max(counts) / gamma
        u_l = (last + 1) / gamma
        u_f = math.log(w * math.sqrt(gamma / 2))
        out.append(
            f"   Gamma {gamma:5d}: n_crit in [{float(lo):.3f}, {float(hi):.3f}] quanta per Node-clock; "
            f"just below it U_top = {u_top:.3f}; ruler's end u_L = {u_l:.3f}; u_f = ln(w sqrt(Gamma/2)) = {u_f:.3f}; "
            f"2 n_crit tan(w/2) = {2 * float(lo) * math.tan(w / 2):.3f}"
        )
    out.append("")
    out.append(
        "C. The runaway's per-swing factor F at Gamma 1000 against the pinion (den - den div k): Gamma's alone or w's too?"
    )
    gamma = 1000
    period = 2 * math.pi * math.sqrt(gamma / 2)
    for off in (20, 50, 200, 1000):
        wk = math.acos(1 - 1 / off)
        info, counts, last = counts_of(gamma, Fraction(20 * off, 50), int(4.6 * period), off=off)
        tops = windows(counts, period)
        facs = [b[1] / a[1] for a, b in zip(tops, tops[1:], strict=False) if a[1] > last and b[1] > a[1]]
        out.append(
            f"   pinion den - den div {off} (w = {wk:.4f}), n = {info['quanta_per_node']:.1f}: tops "
            f"{[f'{c:.3e}' for _, c in tops]}; factors {[f'{f:.4e}' for f in facs]}"
        )
    print("\n".join(out))


if __name__ == "__main__":
    main()
