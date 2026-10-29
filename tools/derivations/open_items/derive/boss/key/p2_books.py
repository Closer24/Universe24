"""Probe 2: where the key meets a number the act fixes: the great clock's weight in the joint books.

Derivation (from step.py and load.geared; the clock's count c slow against the train):
  a file train (W = Z_b + Z_n, W+ = Z_n + Z_+, s = 2, Z = T Y(c)^4 div Gamma^4) steps
      M+ (a+ - a) - M- (a - b) = F = -(L_grip + D(c)) a,   M+- the half-tick masses (Z + Z')/2;
  the time gear (W = W+ = T, s = 1, kick T, drive teeth T_d = (T div 2) key) steps T (c+ - 2c + c-) = F_c + T q,
      q = (J + rd) div T_d, J = -2 a.F - D0 a.a (light: D = 0, J = 2 a.L_grip a);
  exactly per tick, each gear's leapfrog form H = (1/2) M (a - b)^2 + (1/2) a.K b moves by
      train:  -(1/2) dM v+ v-     (v+- = a+ - a, a - b;  dM = M+ - M-, = 2 ell Z (c+ - c-) on the ruler's mean slope)
      clock:  +(1/2) T q (c+ - c-)   (a whole kick at rest lays (1/2) T)
  and for a mode of frequency w, <v+ v-> = 2 A^2 sin^2(w/2) cos w while <J> = 4 Z A^2 sin^2(w/2), so the act keeps
      H_m + lam H_c   with   lam = (ell key / 2) cos w,   ell = ln(Gamma / (Gamma - 1)) the ruler's mean log-slope.
  At fixed quanta H_m grows as the key (probe 1), so lam is the clock's count^2 weighed against a train's notch^2:
  the one number of the act that holds the key and no rounding.  It depends on the train's own w (discrete time).

Reading: the rise from the bang (c = 0 at rest), between the ticks the board's mean count reaches a tenth and a third
of its first top (before, each whole kick's (1/2) T outweighs the smooth work; after, the clock is no longer slow);
lam_early is the least-squares slope -dH_m / dH_c there.  The probe can fail three ways: lam not moving with the key,
missing (ell key / 2) cos w, or not following cos w across the board's three light frequencies, cos w = 5/6, 2/3, 1/2.

usage: python3 -I p2_books.py   (about 2 minutes)
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py
import rig  # noqa: E402

SHAPE = (4, 4, 4)
ONE_AXIS = (1, 0, -1, 0)  # cos(pi x / 2) on a side of 4
PI_AXIS = (1, -1, 1, -1)  # cos(pi x)
FLAT = (1, 1, 1, 1)


def pattern(per_axis):
    """A standing wave, the product of one profile per axis (x, y, z), at rest; site = (x sy + y) sz + z."""

    def laid(amp):
        sx, sy, sz = SHAPE
        out = {}
        for x in range(sx):
            for y in range(sy):
                for z in range(sz):
                    v = amp * per_axis[0][x] * per_axis[1][y] * per_axis[2][z]
                    if v:
                        out[(0, 0, (x * sy + y) * sz + z)] = (v, v)
        return out

    return laid


WAVES = {  # name: (profile per axis, cos w): 2 - 2 cos w = (1/6) SUM over axes of (2 - 2 cos k)
    "k = (0, 0, pi/2)": ((FLAT, FLAT, ONE_AXIS), Fraction(5, 6)),
    "k = (0, 0, pi)": ((FLAT, FLAT, PI_AXIS), Fraction(2, 3)),
    "k = (pi/2, pi/2, pi/2)": ((ONE_AXIS, ONE_AXIS, ONE_AXIS), Fraction(1, 2)),
}


def run(laid, key, gamma, ticks):
    L, s = rig.built([rig.light()], laid, SHAPE, rig.integers(key=key, gamma=gamma))
    hs, cs = [], []
    for _ in range(ticks + 1):
        h = rig.forms(L, s)
        hs.append((h[0] / 2, h[-1] / 2))  # H of the light, H of the time gear
        cs.append(rig.count(L, s))
        s = rig.tick(L, s)
    return L, hs, cs


def first_top(cs):
    best = 0
    for n in range(1, len(cs)):
        if cs[n] > cs[best]:
            best = n
        if cs[n] < cs[best] - max(Fraction(1), cs[best] / 50):
            break
    return best


def slope(hs, lo, hi):
    """The least-squares lam keeping H_m + lam H_c flattest over ticks lo..hi."""
    xs = [float(h[1]) for h in hs[lo : hi + 1]]
    ys = [float(h[0]) for h in hs[lo : hi + 1]]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return -sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / sum(
        (x - mx) ** 2 for x in xs
    )


def main():
    out = [
        "Probe 2: the great clock's weight lam in the joint books H_m + lam H_c (committed 7b act, 4 x 4 x 4, light)",
        "",
    ]
    L0, _ = rig.built([rig.light()], pattern(WAVES["k = (0, 0, pi/2)"][0])(1), SHAPE, rig.integers())
    ys = [math.isqrt(int(v)) for v in L0.ruler.square]
    steps = [math.log(ys[c + 1] / ys[c]) for c in range(len(ys) - 1)]
    out.append(
        f"the ruler at Gamma 1,000: Y(0..5) = {ys[:6]}, Y(1000) = {ys[1000]}, Y(last = {len(ys) - 1}) = {ys[-1]};"
    )
    out.append(
        f"  its mean log-slope ln(Y(1000)/Y(0))/1000 = {math.log(ys[1000] / ys[0]) / 1000:.7f} against ln(1000/999) = "
        f"{math.log(1000 / 999):.7f}; its step ln(Y(c+1)/Y(c)) runs over [{min(steps):.6f}, {max(steps):.6f}] count by count"
    )
    out.append("")
    out.append(
        "  cos w_loc = 1 - (1 - cos w)(Gamma / Y(c))^4 at the window's mean count: the light's own frequency in the well"
    )
    out.append(
        "  wave                     cos w  Gamma   key       A     quanta  top tick  top count  lam_early  (ell key/2) cos w_loc"
        "  ratio   lam_early/(ell key/2)"
    )
    plan = [
        (100000, 576000, 562, 1600, "k = (0, 0, pi/2)"),
        (100000, 2304000, 1124, 1600, "k = (0, 0, pi/2)"),
        (100000, 576000, 269, 1600, "k = (0, 0, pi)"),
        (100000, 2304000, 538, 1600, "k = (0, 0, pi)"),
        (100000, 576000, 586, 1600, "k = (pi/2, pi/2, pi/2)"),
        (100000, 2304000, 1172, 1600, "k = (pi/2, pi/2, pi/2)"),
    ]
    plan += [(10000, key, 600, 360, name) for name in WAVES for key in (144000, 288000, 576000)]
    plan += [(1000, key, 600, 110, name) for name in WAVES for key in (72000, 144000, 288000)]
    last_gamma = None
    for gamma, key, amp, ticks, name in plan:
        if last_gamma is not None and gamma != last_gamma:
            out.append("")
        last_gamma = gamma
        axes, cosw = WAVES[name]
        if True:
            L, hs, cs = run(pattern(axes)(amp), key, gamma, ticks)
            yy = L.ruler.square
            top = first_top(cs)
            lo = next(n for n in range(len(cs)) if cs[n] >= cs[top] / 10)
            hi = next(n for n in range(len(cs)) if cs[n] >= cs[top] / 3)
            lam = slope(hs, lo, max(hi, lo + 3))
            ell = math.log(gamma / (gamma - 1))
            c_mid = float(sum(cs[lo : hi + 1]) / (hi + 1 - lo))
            y_mid = math.isqrt(int(yy[int(round(c_mid))]))
            cos_loc = 1 - (1 - float(cosw)) * (gamma / y_mid) ** 4
            pred = ell * key / 2 * cos_loc
            sine = math.sqrt(1 - float(cosw) ** 2)
            n = float(2 * hs[0][0] / (rig.teeth(gamma=gamma) * key * sine))
            out.append(
                f"  {name:<24} {str(cosw):<6} {gamma:<7} {key:<9} {amp:<5} {n:7.2f}  {top:7}  {float(cs[top]):9.1f}  {lam:9.3f}"
                f"  {pred:20.3f}  {lam / pred:6.3f}   {lam / (ell * key / 2):6.3f}"
            )
    out.append("")
    out.append(
        "The closure 'one key for every train, the great clock among them' asks the clock's count^2 to weigh as a"
    )
    out.append("train's notch^2 in the books, lam = 1:  key = 2 / (ell cos w).")
    for g in (1000, 10**6):
        ell = math.log(g / (g - 1))
        for cosw in (1, Fraction(5, 6), Fraction(1, 2)):
            k = 2 / (ell * float(cosw))
            out.append(
                f"  Gamma = {g}, cos w = {cosw}: key = {k:.6f}, the nearest whole key {round(k)}, missed by {k - round(k):+.6f}"
            )
    out.append(
        "  2 / (ell cos w) with cos w rational is transcendental (ln of a rational other than 1 is, by Hermite-Lindemann),"
    )
    out.append(
        "  so no whole key closes it; it differs train by train (cos w) and moves with the well (w falls as N^2), so no"
    )
    out.append(
        "  single key closes it for two trains; and the ruler's whole Y makes ell move count by count."
    )
    ell = math.log(1000 / 999)
    out.append(
        f"  The file's key 36,000 at Gamma 1,000: ell key / 2 = {ell * 36000 / 2:.4f} (36000 / 1999 = {36000 / 1999:.4f}), times cos w."
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
