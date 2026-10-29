"""The closure of the whole history over a swing, on the committed act: does the past bang come back exactly, at which
Gamma, and does the run back (the dual run's backward pass) exclude any history?

usage: python3 -I closure.py > closure.txt

The dynamical state is (a, b, r, rd) of every gear: the dial ph stands still at the full rate (carry(ph, Gamma,
Gamma) keeps ph), the beat count c and the time tn only count ticks.  "The past bang and the next bang agree" is read
as that state returning exactly (a fixed point of the history map over a whole number of ticks).

1. The time gear alone (one light train laid at zero amplitude, so J = 0): from the bang (load 0, velocity v0 counts a
   tick) the integer leapfrog with its exact remainder; its exact return time tau(Gamma, v0) against the swing's
   period P = 2 pi sqrt(Gamma/2).  Derivation: the momentum p = W (a - b) + r - home is updated exactly,
   p' = p - D a, so p returns iff the sum of the loads over the loop is 0, and the load is the floor of p / W: a
   discretized rotation of angle w_t, cos w_t = 1 - (den div Gamma)/den.  The exact linear map never returns (w_t / 2 pi
   is irrational: cos w_t rational and not 0, +-1/2, +-1, Niven), so any exact return is the integers' doing.
2. A stable swing with matter (n = 1 quantum of the hand per Node-clock): the exact return of the whole state, and the
   nearest approach at the bottoms (the load back at or below 0).
3. The dual run's consistency: the run back (step.untick) from the end of every history above, stable and runaway,
   lands on its start exactly (tested in runaway.py too); so self-consistency at both ends holds for every Gamma and
   every seed, and excludes no history.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py

import rig  # noqa: E402

from tensor24.engine import step  # noqa: E402


def key_of(s):
    return tuple(
        tuple(int(v) for v in np.asarray(x, dtype=object).ravel()) for x in (s.a, s.b, s.r, s.rd)
    )


def time_gear_alone(gamma: int, v0: int, cap: int):
    light = {"name": "light", "kinds": ["A1"], "part": 1, "pinion": rig.DEN}
    # the time gear is the row after the file's train: component 0 of train 1
    gears = [[1, 0, 0, 0, -v0, 0]]
    layout, s = rig.built(rig.integers(gamma), [light], [1, 1, 1], gears)
    start = key_of(s)
    allowed = np.ones((1, 1), dtype=object)
    outs = []
    top = 0
    for t in range(1, cap + 1):
        s, out = step.tick(layout, s, allowed)
        outs.append(out)
        top = max(top, int(s.a[layout.ruler.row, 0]))
        if key_of(s) == start:
            back = rig.rewound(layout, s, outs)
            return t, top, rig.same(back, rig.built(rig.integers(gamma), [light], [1, 1, 1], gears)[1])
    return None, top, None


def main() -> None:
    out = ["The closure of the history over a swing on tensor24-review's act (one Node-clock)", ""]
    out.append(
        "1. The time gear alone from the bang at velocity v0: exact return time tau, against P = 2 pi sqrt(Gamma/2)"
    )
    cap = 40000
    for gamma in (250, 251, 500, 1000, 1001, 2000, 4000):
        p = 2 * math.pi * math.sqrt(gamma / 2)
        row = []
        for v0 in (1, 2, 3, 5, 10, 40):
            tau, top, exact = time_gear_alone(gamma, v0, cap)
            row.append(f"v0={v0}: tau={tau} ({'%.3f' % (tau / p) if tau else '-'} P), top {top}")
        out.append(f"   Gamma {gamma} (P = {p:.2f}): " + "; ".join(row))
    out.append("")
    out.append(
        "2. A stable swing with one quantum of the matter hand per Node-clock: exact return of the whole state?"
    )
    for gamma in (250, 1000):
        layout, s, info = rig.matter_hand(gamma, Fraction(1))
        start = key_of(s)
        s0 = s
        allowed = np.ones((1, 1), dtype=object)
        seen = {start: 0}
        repeat = None
        bottoms = []
        prev = 0
        outs = []
        ticks = 30000
        for t in range(1, ticks + 1):
            s, o = step.tick(layout, s, allowed)
            outs.append(o)
            k = key_of(s)
            if k in seen:
                repeat = (seen[k], t)
                break
            seen[k] = t
            c = int(s.a[layout.ruler.row, 0])
            if c <= 0 < prev:
                re, im = int(s.a[0, 0]), int(s.a[1, 0])
                bottoms.append((t, c, re * re + im * im))
            prev = c
        back = rig.rewound(layout, s, outs)
        l2 = info["L"] ** 2
        spread = [b[2] / l2 for b in bottoms]
        out.append(
            f"   Gamma {gamma}, n = {info['quanta_per_node']:.3f}: {len(seen)} distinct states in {t} ticks, "
            f"first repeat {repeat}; {len(bottoms)} bottoms, the hand's |L|^2 at them over its start: "
            f"min {min(spread):.4f}, max {max(spread):.4f}; run back over {t} ticks exact: {rig.same(back, s0)}"
        )
    print("\n".join(out))


if __name__ == "__main__":
    main()
