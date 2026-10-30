"""The hostile mathematician's checks on N2's second text, the physics probes P3, P4 and M3: whole numbers only.

Clock: a travelling pulse's stress ratios against its width; the 'held gradient' of M3 taken apart.
Algebra: n2b_lib's metric_source on the engine's act, unchanged.
Board: a line along z (96 to 384 sites); 3 x 4 x 5 for M3.
Clicks: n/a.

Run: <t24b>/.venv/bin/python -I probe_phys.py; the output is probe_phys.txt.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "g2" / "n2_second"))

import numpy as np  # noqa: E402
from n2b_lib import (  # noqa: E402
    A1ROWS,
    ROWS,
    S0I,
    S00,
    SII,
    SJK,
    T1ROWS,
    State,
    carry,
    engine_plan,
    gradient_part,
    join,
    layout,
    metric_source,
    potential,
    rate_part,
    step,
    terms,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line, flush=True)
    OUT.append(line)


REST, GRIP = 3000, 500
LIGHT = T1ROWS[0]
T5 = join(terms(gradient_part(1)), terms(potential(0)))
RATE = terms(rate_part(1))


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


def still(L_, rows_values, metric_values):
    n = L_.nb.shape[1]
    a = np.zeros((ROWS, n), dtype=object)
    for row, values in rows_values.items():
        a[row] = values
    for slot, value in metric_values.items():
        a[slot] = value
    return State(a, a.copy(), 0 * a, 0 * a)


# ------------------------------------------------------------------- 1. P4's ratios against the pulse's width
say("== 1. P4's travelling pulse: Szz / S00 (24 in the continuum) and -S0z / S00 (4.9) against the pulse's half width h")
say("  (the bump (h^2 - u^2)^2 for |u| < h, split into two pulses; the line long enough that the pulses do not meet)")
for h, NZ, rounds in ((8, 96, 60), (16, 192, 120), (32, 384, 240), (64, 768, 480)):
    L = layout((1, 1, NZ), REST, REST, GRIP, 1, 1, clock="others")
    z = np.arange(NZ)
    u = z - NZ // 2
    bump = np.where(abs(u) < h, (h * h - u * u) ** 2, 0).astype(object)
    s_ = still(L, {LIGHT: bump}, {})
    Le = L._replace(plan=engine_plan(terms([])))
    for _ in range(rounds):
        s_ = step.tick(Le, s_)
    j = metric_source(L, s_, T5, RATE)
    right = z >= NZ // 2
    s00, s0z, szz = int(j[S00][right].sum()), int(j[S0I[2]][right].sum()), int(j[SII[2]][right].sum())
    say(f"  h = {h:2d}, {NZ} sites, {rounds} rounds: Szz / S00 = {permille(szz, s00)} permille of 1 (24000 in the continuum), -S0z / S00 = {permille(-s0z, s00)} (4899), null S0z^2 / (S00 Szz) = {permille(s0z * s0z, s00 * szz)}")
say("  the ratios climb toward 24 and 4.9 as the pulse widens: the text's 23.1 and 4.7 are the lattice's at h = 8, stated there without this check")

# ------------------------------------------------------------------- 2. M3's 'held gradient', taken apart
say("\n== 2. M3's third case, 'a count held still with a gradient along z': its J's by source")
L0 = layout((3, 4, 5), REST, REST, GRIP, 1, 1, clock="none")
n = L0.nb.shape[1]
a = np.zeros((ROWS, n), dtype=object)
zz = np.arange(n) % 5
a[A1ROWS[0]] = np.array([(2, 1, -1, -2, 0)[k] for k in zz], dtype=object) * 3
s_ = State(a, a.copy(), 0 * a, 0 * a)
for name, now in (("gradient part and the potential (the text's)", join(terms(gradient_part(1)), terms(potential(1)))), ("the gradient part alone", terms(gradient_part(1))), ("the potential alone", terms(potential(1)))):
    j = metric_source(L0, s_, now, RATE)
    tot = [int(j[x].sum()) for x in (S00, *SII, *S0I)]
    say(f"  {name}: J00 = {tot[0]}, J_xx, J_yy, J_zz = {tot[1:4]}, J_0i = {tot[4:]}")
j = metric_source(L0, s_, terms(gradient_part(1)), terms([]))
say(f"  the gradient part with no stride read at all: J00 = {int(j[S00].sum())}, J_zz = {int(j[SII[2]].sum())}")
# is the profile held? the stride out of pass 1 under the pull
force = step.sources(L0._replace(plan=engine_plan(terms([]))), a)[0]
a1, _, _ = step.gear(a, a.copy(), 0 * a, step.weight(L0.gearing, L0.clock, a), step.driven(L0.gearing, force, 0 * a))
moved = int((a1[A1ROWS[0]] != a[A1ROWS[0]]).sum())
say(f"  the profile is not held: the Meshes' pull moves it at {moved} of {n} sites in the round (sigma_a != 0), which is where the 72 on J_0z and the +72 on J00 come from")
say("  so J_xx = J_yy = 1080 are the potential's (2V = x^2 summed), not the gradient's; the gradient alone gives J00 = J_xx = J_yy = 0 up to the pass-1 motion, as the continuum has it")

Path(HERE / "probe_phys.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
