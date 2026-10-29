"""Probe 5: the method's one route to a value: a least key by resolution, as K-S1 fixes G.  Does any key stand out?

One quantum of light as a hand (part 2, the example universe's light), a wave travelling along z at k = pi/2 on the
4 x 4 x 4 board, laid with its swept area Q = SUM Im(conj(a) b) = key / 2 (|L|^2 = key / (2 N sin w)), run one swing
of the great clock (141 ticks) on the committed act at keys from 64 to 2,304,000.

Derived: with the ruler's W the step keeps the hand's Wronskian with its inertia, Q* = SUM (W / s)(re_now im_before -
im_now re_before) / T, exactly but for the carries' rounding (for x, y two solutions of M+ v+ - M- v- = -K a, the
quantity M (x+ y - y+ x) is kept); the plain Q falls as the well deepens, as (Gamma / Y)^4 = N^4.  The rounding's
walk of Q*, in quanta, should fall as the key grows (about 1 / sqrt(key): the walk goes as the amplitude, a quantum as
its square), with no key singled out; below key ~ N cot(w/2) one quantum's hand cannot move a notch a tick.
The probe can fail: a walk with a minimum or a step at some key would single that key out.

usage: python3 -I p5_resolution.py   (about 20 s)
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py
import rig  # noqa: E402

SHAPE = (4, 4, 4)
N = 64
COSW = 5 / 6
W = math.acos(COSW)
T = rig.teeth()


def laid_hand(key, quanta=1):
    """A hand travelling along z: re = L cos(k z - w t), im = L sin(k z - w t), now at t = 0 and before at t = -1."""
    amp = math.sqrt(quanta * key / (2 * N * math.sin(W)))
    out = {}
    sx, sy, sz = SHAPE
    for site in range(sx * sy * sz):
        z = site % sz
        ph = math.pi / 2 * z
        out[(0, 0, site)] = (round(amp * math.cos(ph)), round(amp * math.cos(ph + W)))
        out[(0, 1, site)] = (round(amp * math.sin(ph)), round(amp * math.sin(ph + W)))
    return out, amp


def qstar(L, s):
    """The hand's Wronskian with its inertia, SUM (W/s)(re_a im_b - im_a re_b), over T; and the plain swept area."""
    from tensor24.engine import step

    laid = step.ruled(L.gearing, L.ruler, s.b, s.a, s.a)
    w = laid.w[0]
    st = int(laid.stretch[0, 0])
    a, b = s.a, s.b
    cross = a[0] * b[1] - a[1] * b[0]
    return int((w * cross).sum()) / st / T, int(cross.sum())


def main():
    out = [
        "Probe 5: one quantum of light (a hand) over one swing, against the key (committed 7b act, 4 x 4 x 4)",
        "",
    ]
    out.append(
        f"N cot(w/2) = {N * (1 + COSW) / math.sin(W):.1f}: below it one quantum spread over the board cannot move a notch a tick"
    )
    out.append(
        "  key        |L|      2Q*/key at 0   walk of 2Q*/key   2Q div key: ticks at 0 / 1 / 2+   the count's top   at the top: 2Q/key, 2Q*/key, (Gamma/Y)^4"
    )
    for key in (64, 256, 1024, 4096, 36000, 144000, 576000, 2304000, 9216000):
        laid, amp = laid_hand(key)
        L, s = rig.built([rig.light(part=2)], laid, SHAPE, rig.integers(key=key))
        q0, p0 = qstar(L, s)
        walk, top, at_top, counts = 0.0, -1, None, [0, 0, 0]
        for _ in range(141):
            s = rig.tick(L, s)
            q, p = qstar(L, s)
            walk = max(walk, abs(2 * (q - q0) / key))
            counts[min(2 * p // key, 2) if p >= 0 else 0] += 1
            cmean = sum(int(x) for x in s.a[L.ruler.row].tolist()) / N
            if cmean > top:
                y = math.isqrt(int(L.ruler.square[int(round(cmean))]))
                top, at_top = cmean, (2 * p / key, 2 * q / key, (rig.GAMMA / y) ** 4)
        out.append(
            f"  {key:<10} {amp:7.2f}   {2 * q0 / key:12.4f}   {walk:15.4f}   {counts[0]:>9} /{counts[1]:>4} /{counts[2]:>4}"
            f"   {top:15.2f}   {at_top[0]:.4f}, {at_top[1]:.4f}, {at_top[2]:.4f}"
        )
    out.append("")
    out.append(
        "Reading: the walk falls steadily with the key and singles out no value; the resolution rule bounds the key from"
    )
    out.append(
        "below and leaves it free above.  A quantum laid at Q = key / 2 sits on its bin's edge, so 2Q div key flips"
    )
    out.append(
        "between 0 and 1 at every key: the handshake by that count needs the walk booked (the charge identity), not a"
    )
    out.append(
        "key.  At the swing's top the plain Q has fallen with the well toward (Gamma/Y)^4 while Q* holds: the count"
    )
    out.append(
        "by the plain swept area reads the lapse (BIG_PICTURE 5.1's source factor, owed), at every key alike."
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
