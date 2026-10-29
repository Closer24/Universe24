"""Probe 4: the clocks and the dual run's closure, in exact arithmetic and on the act.

(a) The swing never closes in whole ticks.  The time gear's pair (den - den div Gamma, den) gives D_c / W_c =
    2 (den div Gamma) / den, so cos Omega = 1 - (den div Gamma) / den, a rational.  By Niven's theorem cos(r pi) is
    rational only at 0, +-1/2, +-1, so for Gamma >= 3 Omega / pi is irrational: no history of the linear swing closes
    on itself after a whole number of ticks.  (With the carries the integer orbit recurs only by accident.)
(b) The great clock's least swing is one whole kick: a kick at rest gives a time gear one count a tick, H = (1/2) T,
    so the uniform swing it starts has amplitude 1 / sin Omega counts (about sqrt(Gamma / 2)), whatever the key.
    Read on the act: the uniform matter world of probe 1, whose first kick fires at every site at once.
(c) A closure over one swing fixes the setting and not the key.  Over a swing of P ticks the drive's remainder returns
    (rd(P) = rd(0)) iff SUM_t J = k T_d at every Node-clock; for matter at rest J = D a^2 and n quanta on N sites
    (2H = n T key sin w) this is k = 2 tan(w/2) n P / N per site: the key cancels, so the closure is a condition on
    n / N, w and P.
(d) 'One key for every train, the great clock among them' (probe 2) needs key = 2 / (ell cos w): transcendental.
(e) K-S1's pattern (the least G at which one notch resolves) applied to the key: one quantum of a hand at frequency w,
    |L|^2 sin w = key / 2, moves at least one notch a tick iff |L| 2 sin(w/2) >= 1, i.e. key >= cot(w/2); at the great
    clock's own beat cot(Omega/2) = sqrt(2 Gamma - 1) where Gamma divides den.  A bound, with no value singled out.

usage: python3 -I p4_closure.py   (a few seconds)
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py
import rig  # noqa: E402

DEN, GAMMA = rig.DEN, rig.GAMMA


def main():
    out = [
        "Probe 4: the clocks and the closure of one swing (exact arithmetic, and the committed 7b act)",
        "",
    ]
    q = DEN // GAMMA
    cos_c = 1 - Fraction(q, DEN)
    omega = math.acos(float(cos_c))
    out.append(f"(a) den = {DEN}, den div Gamma = {q}, den mod Gamma = {DEN % GAMMA}")
    out.append(
        f"    cos Omega = 1 - {q}/{DEN} (rational, not 0, 1/2 or 1): Omega = {omega:.9f} rad a tick,"
    )
    out.append(
        f"    the linear swing's period 2 pi / Omega = {2 * math.pi / omega:.6f} ticks (2 pi sqrt(Gamma/2) = {2 * math.pi * math.sqrt(GAMMA / 2):.6f}),"
    )
    out.append(
        "    Omega / pi irrational by Niven: no whole number of ticks closes the swing, at any Gamma >= 3"
    )
    s2 = 1 - cos_c * cos_c  # sin^2 Omega, rational
    is_square = Fraction(math.isqrt(s2.numerator) ** 2, math.isqrt(s2.denominator) ** 2) == s2
    out.append(
        f"    sin^2 Omega = {float(s2):.12e} is a rational square: {is_square} (the time gear's pair is on den's circle only if it is),"
    )
    out.append(
        "    so law 5's winding 3 key s has no whole s for the great clock: the time gear has no whole winding"
    )
    out.append("")
    # (b) the least swing on the act: one kick at every site at once
    shape = (4, 4, 4)
    L, s = rig.built([rig.matter()], rig.uniform(shape, 601), shape, rig.integers(key=2304000))
    row = L.ruler.row
    first, cs = None, []
    for n in range(400):
        c = [int(x) for x in s.a[row].tolist()]
        cs.append(sum(c) / len(c))
        if first is None and any(c):
            first = n
        s = rig.tick(L, s)
    after = cs[first : first + 160]
    amp_read = (max(after) - min(after)) / 2
    out.append(
        f"(b) one whole kick: the uniform matter world (A = 601, key 2,304,000, 2 quanta) kicks first at tick {first}, at every site;"
    )
    out.append(
        f"    the swing it starts reads half-height {amp_read:.2f} counts against 1 / sin Omega = {1 / math.sqrt(float(s2)):.2f} (sqrt(Gamma/2) = {math.sqrt(GAMMA / 2):.2f});"
    )
    out.append(
        "    the great clock's least swing is set by Gamma alone: a kick is one count a tick, its energy (1/2) T a time gear"
    )
    out.append("")
    # (c) the closure over a swing, per quantum of matter at rest
    cos_m = Fraction(DEN - DEN // 50, DEN)
    w = math.acos(float(cos_m))
    period = 2 * math.pi / omega
    out.append(
        "(c) the drive's remainder returns over one swing iff SUM_t J = k T_d at every Node-clock; per quantum of matter"
    )
    out.append(
        f"    at rest (w = {w:.6f}) that is 2 tan(w/2) P / N = {2 * math.tan(w / 2) * period:.4f} / N kicks per quantum per swing:"
    )
    out.append(
        "    no key in it.  The closure asks n / N (quanta per Node-clock) to make it whole: a condition on the setting."
    )
    out.append("")
    # (d) the transcendental closure
    ell = math.log(GAMMA / (GAMMA - 1))
    out.append(
        f"(d) lam = 1 needs key = 2 / (ell cos w), ell = ln(Gamma/(Gamma-1)) = {ell:.10f}: {2 / ell:.6f} at cos w = 1 (no whole"
    )
    out.append(
        "    solution: ln of a rational other than 1 is transcendental), and a different value for every train's w."
    )
    out.append("")
    # (e) the K-S1 pattern
    g = rig.load.mesh_unit(GAMMA)
    out.append(
        f"(e) K-S1 fixes G = {g} as the least G with 2 G^2 (2 Gamma - 1) > Gamma^2.  The same pattern for the key: one quantum"
    )
    out.append("    of a hand moves a notch a tick iff key >= cot(w/2) = (1 + cos w) / sin w:")
    cot_c = (1 + float(cos_c)) / math.sqrt(float(s2))
    out.append(
        f"    the great clock's own beat: cot(Omega/2) = {cot_c:.6f}; sqrt(2 Gamma - 1) = {math.sqrt(2 * GAMMA - 1):.6f}; least whole key {math.ceil(cot_c)}"
    )
    for name, cw in (
        ("light, k = pi/2 on one axis", Fraction(5, 6)),
        ("matter at rest, pinion den - den div 50", cos_m),
    ):
        sw = math.sqrt(1 - float(cw) ** 2)
        out.append(f"    {name}: cot(w/2) = {(1 + float(cw)) / sw:.4f}")
    out.append(
        "    a quantum spread over N Node-clocks needs N times that.  The file's 36,000 is far above each: the rule bounds"
    )
    out.append(
        "    the key from below and singles out no value (probe 5 reads the count's walk against the key)."
    )
    out.append(
        "    Note: 2 G^2 (2 Gamma - 1) > Gamma^2 is G > Gamma / (sqrt 2 cot(Omega/2)) where Gamma divides den; both read the step"
    )
    out.append(
        "    from the rate Gamma to Gamma - 1 (2 Gamma - 1 = Gamma^2 - (Gamma - 1)^2): a shared origin, no relation of the key."
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
