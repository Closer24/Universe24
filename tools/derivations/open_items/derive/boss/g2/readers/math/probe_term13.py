"""The hostile mathematician's checks on term 13 (the frozen clock): whole numbers only.

Clock: the beat against the teeth; the 00 slot wound by the matter's source; the well against the mean.
Algebra: t13_probe's own energy_source and the first-order form (n2b_lib), unchanged; the sums read from outside.
Board: one Node-clock (the uniform swing), 3 x 3 x 16 (the lump), a ring of 6 (the beat).
Clicks: n/a.

Run: <t24b>/.venv/bin/python -I probe_term13.py; the output is probe_term13.txt.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "g2" / "n2_second"))
sys.path.insert(0, str(HERE.parent / "g2" / "term13"))

import numpy as np  # noqa: E402
from n2b_lib import (  # noqa: E402
    A1ROWS,
    ROWS,
    S00,
    SII,
    State,
    carry,
    engine_plan,
    layout,
    metric_source,
    step,
    tick_first,
    to_first,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line, flush=True)
    OUT.append(line)


REST, GRIP, G, TD = 3000, 500, 210, 1000
CLOCK = A1ROWS[0]

# t13_probe's plans, rebuilt from its own functions without running its probes (its module runs them at import)
src = (HERE.parent / "g2" / "term13" / "t13_probe.py").read_text(encoding="utf-8")
head = src.split("# ------------------------------------------------------------------------------ 1. the beat")[0]
ns = {"__file__": str(HERE.parent / "g2" / "term13" / "t13_probe.py")}
exec(compile(head, "t13_head", "exec"), ns)  # the definitions only: energy_source, NOW, RATE, still, crossings, ...
NOW, RATE, T5, SPRING = ns["NOW"], ns["RATE"], ns["T5"], ns["SPRING"]
still, crossings = ns["still"], ns["crossings"]


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


# ------------------------------------------------------------------- 1. the beat: W / rest against the discrete dispersion
say("== 1. probe 1's period^2 ratios against W / rest and against the discrete oscillator's own law 4 sin^2 (omega / 2) = g / W")
say("  (to the next order, period^2 goes as (12 W - g) / (12 rest - g), not W / rest)")
L6 = layout((1, 1, 6), REST, REST, GRIP, 1, 1, clock="others")
base = None
for mult in (1, 2, 4, 8, 16):
    c00 = (mult - 1) * REST
    t = crossings(L6, still(L6, {CLOCK: 10**6}, {S00: c00}), SPRING, CLOCK, 0, 40)
    base = base or t
    W = mult * REST
    measured = permille(t * t, base * base)
    first = 1000 * mult
    second = permille(12 * W - G, 12 * REST - G)
    # one round's resolution in the count of 40 sign changes, in permille of the ratio
    res = permille((t + 1) * (t + 1), base * base) - measured
    say(f"  W = {mult:2d} rest: measured {measured} permille; W / rest {first}; (12 W - g) / (12 rest - g) {second}; one round's resolution {res} permille")

# ------------------------------------------------------------------- 2. the uniform swing: the source against the energy
say("\n== 2. probe 2's swing: the 00 source's mean against the matter's energy, by windows of 500 rounds")
L1 = layout((1, 1, 1), REST, REST, GRIP, 1, TD, clock="others")
s_ = to_first(L1, still(L1, {}, {}))
s_.b[CLOCK, 0] = 10 * REST
st = s_
T = 3000
win = {"j00": 0, "twoE": 0, "floor_rounds": 0, "floor_part": 0, "sig2": 0, "rounds": 0}
say("  window      W at end   mean 00 push   mean 2E (p^2/W + g a^2)   push / 2E   rounds with a stride of -1 from |p| < W   their share of the push   adiabatic 2E (from the start, 2E0 sqrt(rest / W))")
E0_twice = 10 * REST * 10 * REST // REST  # 2E at the start: p^2 / W with p = 10 rest, a = 0
for t in range(1, T + 1):
    a, p, _, rd = st
    w = step.weight(L1.gearing, L1.clock, a)
    W = int(w[CLOCK, 0])
    j = metric_source(L1, st, NOW, RATE, first=True)
    j00 = int(j[S00, 0])
    pc, ac = int(p[CLOCK, 0]), int(a[CLOCK, 0])
    twoE = pc * pc // W + G * ac * ac
    sb = pc // W
    # the stride out as pass 2 reads it: (p + spring) div W
    sa = (pc - G * ac) // W
    floor_here = (sb == -1 and -W < pc < 0) or (sa == -1 and -W < pc - G * ac < 0)
    win["j00"] += j00
    win["twoE"] += twoE
    win["rounds"] += 1
    if floor_here:
        win["floor_rounds"] += 1
        # the part of the push that the -1 strides carry: 2 W per such stride
        win["floor_part"] += 2 * W * ((sb == -1 and -W < pc < 0) + (sa == -1 and -W < pc - G * ac < 0))
    st = tick_first(L1, st, NOW, RATE)
    if t % 500 == 0:
        Wend = int(step.weight(L1.gearing, L1.clock, st.a)[CLOCK, 0])
        # 2E0 sqrt(rest / W): squared, 4 E0^2 rest / W, then the whole root by Rule3's carry on a search-free bound: use permille of the square
        adiab_sq = E0_twice * E0_twice * REST // Wend
        r = 0
        # the whole root of adiab_sq by doubling and halving in whole numbers (no float): bisection on integers
        lo, hi = 0, E0_twice
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if mid * mid <= adiab_sq:
                lo = mid
            else:
                hi = mid - 1
        say(f"  {t - 499:5d}-{t:5d}  {Wend:9d}   {win['j00'] // 500:12d}   {win['twoE'] // 500:22d}   {permille(win['j00'], win['twoE']):6d} permille   {win['floor_rounds']:4d} of 500   {permille(win['floor_part'], win['j00']) if win['j00'] else 0:6d} permille   {lo:8d}")
        win = {"j00": 0, "twoE": 0, "floor_rounds": 0, "floor_part": 0, "sig2": 0, "rounds": 0}
say("  the text: '4K - 2V averages to the swing's energy'; the push is 2 (4K - 2V) in the probe's doubled units, so push / 2E = 1000 permille is the claim")

# ------------------------------------------------------------------- 3. the lump: the well, sampled finely
say("\n== 3. probe 3's well (lump - far), sampled every 25 rounds: does it settle, or swing?")
SH = (3, 3, 16)
Lb = layout(SH, REST, REST, GRIP, 1, TD, clock="others")
nb_ = Lb.nb.shape[1]
centre = (1 * 3 + 1) * 16 + 8
far = (1 * 3 + 1) * 16 + 0
s_ = to_first(Lb, still(Lb, {}, {}))
s_.b[CLOCK, centre] = 10 * REST
st = s_
wells = []
means = []
for t in range(0, 1501):
    if t % 25 == 0:
        c = st.a[S00]
        wells.append(int(c[centre] - c[far]))
        means.append(int(c.sum()) // nb_)
    if t < 1500:
        st = tick_first(Lb, st, NOW, RATE)
say(f"  the well at rounds 0, 25, ..., 1500: {wells}")
for lo_r in (0, 500, 1000):
    seg = wells[lo_r // 25 : lo_r // 25 + 20]
    say(f"  rounds {lo_r}-{lo_r + 475}: the well's least {min(seg)}, greatest {max(seg)}, swing {max(seg) - min(seg)}; the mean c00 at the window's end {means[lo_r // 25 + 19]}")
Wl, Wf = REST + int(st.a[S00, centre]), REST + int(st.a[S00, far])
say(f"  at round 1500: W at the lump {Wl}, far {Wf}; the two clocks' N^2 ratio W_far / W_lump = {permille(Wf, Wl)} permille (1000 is no redshift); at round 500 it was {permille(REST + 3271, REST + 3298)} permille from the text's own numbers")
say("  the well swings about 0 with a width of tens and does not settle; the redshift between the two clocks fades as the mean grows: 'two clocks on one board keep their ratio' is not what the numbers say")

Path(HERE / "probe_term13.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
