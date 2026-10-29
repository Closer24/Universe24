"""The runaway past the ruler on the committed act: its per-swing growth against Gamma, and the run back through it.

usage: python3 -I runaway.py > runaway.txt

Setting: one Node-clock (1 x 1 x 1 board, every neighbour itself), one matter hand (part 2) at its rest rotation,
cos w = pinion / den with pinion = den - den div 50 (w = 0.2003), |L|^2 sin w = n key / 2 (n quanta per Node-clock,
BIG_PICTURE 5.1), the time gear at 0 at rest: the bang.  Nothing else is laid.

Derivation chain for the stable swing (section 4 of BIG_PICTURE, load.geared): the time gear's push per tick is
q = J / T_d with J = D |L|^2 (a hand at rest rotation: J = -2 a.F - D a.a = D a.a), D = 12 (den - p) G^2 Y^2,
T_d = (T div 2) key, T = 6 den Gamma^2 G^2, so at the bang q = 4 (1 - cos w) |L|^2 / key = 2 n tan(w/2); the time gear
c'' = -(2/Gamma) c + q gives c* = q Gamma / 2 and a first top 2 c*, i.e. U_top = 2 n tan(w/2): no Gamma in it.

Readings: the first top (tick, count), the tops of every later swing, the per-swing factor top_{k+1} / top_k, its
log over log(2 Gamma), the largest integer's bits, and the run back (engine/step.untick) to the bang: exact or not.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py

import rig  # noqa: E402

from tensor24.engine import step  # noqa: E402


def swing_tops(counts):
    """Tops: a tick where the count stops rising after rising, with the count above every count since the last bottom."""
    tops = []
    for n in range(1, len(counts) - 1):
        if counts[n] > counts[n - 1] and counts[n + 1] <= counts[n]:
            tops.append((n, counts[n]))
    # keep the swing's top: the largest between two passes below the first top's half
    merged = []
    for t, c in tops:
        if merged and t - merged[-1][0] < 40:
            if c > merged[-1][1]:
                merged[-1] = (t, c)
        else:
            merged.append((t, c))
    return merged


def one(gamma: int, n: Fraction, ticks: int, rewind: bool):
    layout, s0, info = rig.matter_hand(gamma, n)
    allowed = np.ones((1, 1), dtype=object)
    s = s0
    counts = [0]
    outs = []
    maxbits = 0
    for _ in range(ticks):
        s, out = step.tick(layout, s, allowed)
        counts.append(int(s.a[layout.ruler.row, 0]))
        if rewind:
            outs.append(out)
        maxbits = max(maxbits, rig.bits(s))
    exact = None
    if rewind:
        back = rig.rewound(layout, s, outs)
        exact = rig.same(back, s0)
    return info, counts, maxbits, exact, int(layout.ruler.last)


def main() -> None:
    out = [
        "The runaway past the ruler on tensor24-review's act (one Node-clock, one matter hand, w = 0.2003)",
        "",
    ]
    out.append(
        "A. The stable swing: the first top against U_top = 2 n tan(w/2), Gamma-free (period against 2 pi sqrt(Gamma/2))"
    )
    for gamma in (250, 1000, 4000):
        for n in (Fraction(1, 2), Fraction(1), Fraction(2)):
            info, counts, maxbits, exact, last = one(
                gamma, n, int(3 * 2 * math.pi * math.sqrt(gamma / 2)) + 5, True
            )
            tops = swing_tops(counts)
            pred = 2 * info["quanta_per_node"] * math.tan(info["w"] / 2)
            per = [b[0] - a[0] for a, b in zip(tops, tops[1:], strict=False)]
            out.append(
                f"   Gamma {gamma}, n = {info['quanta_per_node']:.3f}: first top at tick {tops[0][0]}, count {tops[0][1]}, "
                f"U_top {tops[0][1] / gamma:.4f} vs predicted {pred:.4f}; periods {per} vs {2 * math.pi * math.sqrt(gamma / 2):.1f}; "
                f"run back exact: {exact}"
            )
    out.append("")
    out.append(
        "B. The runaway: tops per swing, the per-swing factor F = top_{k+1}/top_k, and log F / log(2 Gamma)"
    )
    for gamma in (250, 500, 1000, 2000, 4000):
        period = 2 * math.pi * math.sqrt(gamma / 2)
        ticks = int(4.6 * period)
        for n in (Fraction(10), Fraction(20)):
            info, counts, maxbits, exact, last = one(gamma, n, ticks, True)
            tops = swing_tops(counts)
            facs = [
                b[1] / a[1] for a, b in zip(tops, tops[1:], strict=False) if a[1] > last and b[1] > 0
            ]
            logs = [math.log(f) / math.log(2 * gamma) for f in facs if f > 1]
            past = next((t for t, c in enumerate(counts) if c > last), None)
            out.append(
                f"   Gamma {gamma} (last count {last}), n = {info['quanta_per_node']:.2f}: passes the last count at tick {past}; "
                f"tops {[(t, f'{c:.3e}') for t, c in tops[:5]]}"
            )
            out.append(
                f"      per-swing factors {[f'{f:.3e}' for f in facs]}; log F / log(2 Gamma) = {[round(x, 3) for x in logs]}; "
                f"largest integer {maxbits} bits; run back to the bang exact: {exact}"
            )
    print("\n".join(out))


if __name__ == "__main__":
    main()
