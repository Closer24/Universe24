"""Probe 1: is the key a constant of the act, or the notch^2 of one quantum?  Covariance under (amplitude x L, key x L^2).

Claim (derived from step.py and load.geared): the key enters the committed act at one place, the time gear's drive
teeth T_d = (T div 2) key.  The time gear's source J = -2 value.force - D value.value is quadratic in the file trains'
amplitudes, so under a -> L a (every file train), key -> L^2 key, rd -> L^2 rd the drive's carry
    (q, rd') = carry(J, T_d, rd)
gives the same quotient q and L^2 rd' exactly; the trains' own gears are linear in a, so they scale too, up to their
carries' rounding (the fine tooth r does not scale).  So at a fixed number of quanta (n = 2 H / (T key sin w) here,
the swept-area count n = 2 Q div key for hands) the great clock's course, the count at every tick, is the same at
every key, to the trains' rounding, which falls as L grows.  If the key were a constant the act could fix, some
reading of the course would move with it at a fixed count of quanta.  The probe can fail: the scaled worlds' courses
could part by more than the rounding allows, or fail to converge as L grows.

Mutants: amplitude x 2 with the key unchanged (4 times the quanta), and the key x 4 at one amplitude (a quarter).
Worlds: 4 x 4 x 4, one file train beside the time gear: light, a standing wave (1, 0, -1, 0) at rest; matter
(pinion den - den div 50), uniform at rest.  Every fine tooth at its home, the drive's at T_d div 2.

usage: python3 -I p1_covariance.py   (about 20 s)
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py
import rig  # noqa: E402

SHAPE = (4, 4, 4)
N = 64
TICKS = 100
T = rig.teeth()
SIN_LIGHT = math.sqrt(11) / 6  # light at k = pi/2 on one axis: 2 - 2 cos w = (1/6) 2, cos w = 5/6
COS_MATTER = (rig.DEN - rig.DEN // 50) / rig.DEN
SIN_MATTER = math.sqrt(1 - COS_MATTER**2)


def course(train, laid, key):
    L, s = rig.built([train], laid, SHAPE, rig.integers(key=key))
    h0 = rig.forms(L, s)[0]  # 2H of the file train at the start
    cs = []
    for _ in range(TICKS + 1):
        cs.append(rig.count(L, s))
        s = rig.tick(L, s)
    return L, cs, h0


def top(cs):
    """The highest mean count of the run and its first tick (a plateau of the kicks is no top)."""
    h = max(cs)
    return cs.index(h), h


def family(name, train, pattern, base_amp, base_key, sine, scales, mutants):
    lines = [f"{name}: the base world A = {base_amp}, key = {base_key}"]
    runs = {}
    for lam in scales:
        amp, key = int(base_amp * lam), int(base_key * lam * lam)
        L, cs, h0 = course(train, pattern(amp), key)
        n = float(h0 / (T * key * sine))  # quanta: 2H = n T key sin w
        runs[(amp, key)] = (cs, n)
    ref_amp, ref_key = int(base_amp * scales[-1]), int(base_key * scales[-1] ** 2)
    ref, _ = runs[(ref_amp, ref_key)]
    tt, th = top(ref)
    lines.append(
        f"  the reference (largest A): A = {ref_amp}, key = {ref_key}: top at tick {tt}, height {float(th):.2f}"
    )
    lines.append(
        "  A        key           quanta n   top tick  height     max |c(t) - c_ref(t)| over 0..100   (in counts)"
    )
    for (amp, key), (cs, n) in runs.items():
        t_, h_ = top(cs)
        dev = max(abs(float(a - b)) for a, b in zip(cs, ref, strict=True))
        rise = max(abs(float(a - b)) for a, b in zip(cs[: tt + 1], ref[: tt + 1], strict=True))
        lines.append(
            f"  {amp:<8} {key:<13} {n:9.4f}   {t_!s:>8}  {float(h_):9.2f}  {dev:10.3f}  (to the top: {rise:.3f})"
        )
    for amp, key, why in mutants:
        L, cs, h0 = course(train, pattern(amp), key)
        n = float(h0 / (T * key * sine))
        t_, h_ = top(cs)
        dev = max(abs(float(a - b)) for a, b in zip(cs, ref, strict=True))
        rise = max(abs(float(a - b)) for a, b in zip(cs[: tt + 1], ref[: tt + 1], strict=True))
        lines.append(
            f"  {amp:<8} {key:<13} {n:9.4f}   {t_!s:>8}  {float(h_):9.2f}  {dev:10.3f}  (to the top: {rise:.3f})   MUTANT: {why}"
        )
    return lines


def main():
    out = [
        "Probe 1: the act's course at a fixed count of quanta, the amplitudes x L and the key x L^2 (committed 7b act)",
        "",
    ]
    out += family(
        "light (standing wave, deep well: the top near 1,400 counts, N about e^-1.4)",
        rig.light(),
        lambda A: rig.standing(SHAPE, A),
        150,
        2250,
        SIN_LIGHT,
        [1, 2, 4, 8, 16, 32],
        [
            (1200, 36000, "A x 2, key kept (4 x the quanta)"),
            (600, 144000, "key x 4, A kept (1/4 the quanta)"),
        ],
    )
    out.append("")
    out += family(
        "light, few quanta (the linear regime)",
        rig.light(),
        lambda A: rig.standing(SHAPE, A),
        16,
        2250,
        SIN_LIGHT,
        [1, 2, 4, 8, 16, 32],
        [(128, 36000, "A x 2, key kept"), (64, 144000, "key x 4, A kept")],
    )
    out.append("")
    out += family(
        "matter (uniform at rest, pinion den - den div 50)",
        rig.matter(),
        lambda A: rig.uniform(SHAPE, A),
        153,
        562,
        SIN_MATTER,
        [1, 2, 4, 8, 16, 32],
        [
            (2448, 35968, "A x 2, key kept (4 x the quanta)"),
            (1224, 143872, "key x 4, A kept (1/4 the quanta)"),
        ],
    )
    out.append("")
    # the kicks a quantum gives the great clock, booked exactly from J (SUM q T_d = SUM J + rd_start - rd_end)
    w_l = math.acos(5 / 6)
    w_m = math.acos(COS_MATTER)
    out.append(
        "The kicks per quantum (the count's scale, BIG_PICTURE 4's open item).  Derived: J = -2 a.F - D a.a has the"
    )
    out.append(
        "board mean <SUM J> = 4 tan(w/2) (T_d) per quantum of light and 2 tan(w/2) (T_d) per quantum of matter at"
    )
    out.append(
        "rest (2H = n T key sin w; T_d = (T div 2) key), so a quantum gives the board 4 tan(w/2) or 2 tan(w/2) whole"
    )
    out.append(
        "kicks a tick, each a time gear's one count a tick, whatever the key.  Read over one linear swing (141 ticks):"
    )
    for name, train, pattern, w, f, cases in (
        (
            "light",
            rig.light(),
            lambda A: rig.standing(SHAPE, A),
            w_l,
            4,
            ((64, 36000), (512, 2304000), (180, 36000)),
        ),
        (
            "matter",
            rig.matter(),
            lambda A: rig.uniform(SHAPE, A),
            w_m,
            2,
            ((75, 36000), (601, 2304000), (212, 36000)),
        ),
    ):
        for amp, key in cases:
            L, s = rig.built([train], pattern(amp), SHAPE, rig.integers(key=key))
            row = L.ruler.row
            td = int(L.gearing.drive[row, 0])
            sine = math.sin(w)
            n = float(rig.forms(L, s)[0] / (T * key * sine))
            total, cs = 0, []
            for _ in range(141):
                total += int(rig.source(L, s).sum())
                cs.append(rig.count(L, s))
                s = rig.tick(L, s)
            per_tick = total / td / 141
            out.append(
                f"  {name}: A = {amp}, key = {key}, n = {n:.4f}: board kicks a tick {per_tick:.4f}, per quantum "
                f"{per_tick / n:.4f} (derived {f * math.tan(w / 2):.4f}); the highest mean count {float(max(cs)):.2f} "
                f"(the smooth swing's Gamma qbar = {rig.GAMMA * per_tick / N:.2f})"
            )
    print("\n".join(out))


if __name__ == "__main__":
    main()
