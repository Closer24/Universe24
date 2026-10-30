"""Hostile physicist, check B: gamma as the clicks would read it, (1) on the metric term 5's written push makes
(the 00 and ii slots of check A's uniform swing at the depth P2 used, c00 about 600), and (2) at a small depth
with the ii slots laid at the chosen -c00 / 12, against the slot form's own law.

Clock: a held hand's beat and light's standing wave on a ring of six, each counted in rounds, the metric laid still.
Algebra: whole numbers; the engine's own act (step.tick); the periods' squares as permille ratios by one carry.
Board: one Node-clock to make the pushed metric, a ring of 6 along z to read it, as n2b_probe_phys P2 does.
Clicks: light's slowing over the clock's at one depth is 1 + gamma at first order; the slot form's own law is
light's period^2 ratio (1 + u) / (1 - u) and the clock's 1 + u, u = c00 / rest, so the ratio is 2 / (1 - u).

Run: <t24b>/.venv/bin/python -I b_gamma_pushed.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "copy" / "n2_second"))
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
from n2b_lib import A1ROWS, ROWS, S00, SII, T1ROWS, State, carry, engine_plan, layout, spring, step, table, terms  # noqa: E402

REST, GRIP, G, TD = 3000, 500, 210, 1000
CLOCK, LIGHT = A1ROWS[0], T1ROWS[0]
SPRING = terms(spring(G, [(A1ROWS, table("A1"))]))
L6 = layout((1, 1, 6), REST, REST, GRIP, 1, 1, clock="others")


def mode6(n, amplitude):
    seq = [2 * amplitude, amplitude]
    while len(seq) < n:
        seq.append(seq[-1] - seq[-2])
    return np.array(seq[:n], dtype=object)


def still(L_, rows_values, metric_values):
    n = L_.nb.shape[1]
    a = np.zeros((ROWS, n), dtype=object)
    for row, values in rows_values.items():
        a[row] = values
    for slot, value in metric_values.items():
        a[slot] = value
    return State(a, a.copy(), 0 * a, 0 * a)


def crossings(L_, s_, plan, row, site, wanted):
    L_ = L_._replace(plan=engine_plan(plan))
    rounds, count, sign = 0, 0, None
    while count < wanted:
        s_ = step.tick(L_, s_)
        rounds += 1
        v = int(s_.a[row, site])
        if v != 0:
            new = 1 if v > 0 else -1
            if sign is not None and new != sign:
                count += 1
            sign = new
        if rounds > 2000000:
            return None
    return rounds


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


def ratio2(t1, t0):
    return permille(t1 * t1, t0 * t0)


def read(c00, ii, n_changes):
    metric = {S00: c00, SII[0]: ii, SII[1]: ii, SII[2]: ii}
    tc0 = crossings(L6, still(L6, {CLOCK: 10**6}, {}), SPRING, CLOCK, 0, n_changes)
    tl0 = crossings(L6, still(L6, {LIGHT: mode6(6, 10**6)}, {}), SPRING, LIGHT, 0, n_changes)
    tc = crossings(L6, still(L6, {CLOCK: 10**6}, metric), SPRING, CLOCK, 0, n_changes)
    tl = crossings(L6, still(L6, {LIGHT: mode6(6, 10**6)}, metric), SPRING, LIGHT, 0, n_changes)
    rc, rl = ratio2(tc, tc0), ratio2(tl, tl0)
    one_plus_gamma = permille(rl - 1000, rc - 1000) if rc != 1000 else None
    return tc0, tl0, tc, tl, rc, rl, one_plus_gamma


# (1) the metric the written push makes: check A's one-site replica run until c00 reaches P2's 600
from a_source_and_energy_lib import tick1  # noqa: E402

x = (0, 10 * REST, 0, 0, 0, 0, 0, 0)
t = 0
while x[2] < 600:
    x, _ = tick1(x)
    t += 1
c00, ii = x[2], x[5]
print("== B1. gamma read on the metric term 5's written push makes (the uniform swing of t13 probe 2 / check A)")
print(f"  at round {t} the push has made c00 = {c00}, each ii slot = {ii} (grip {GRIP + 2 * ii}); the chosen -c00 / 12 would be {-carry(c00, 12, 0)[0]}")
tc0, tl0, tc, tl, rc, rl, opg = read(c00, ii, 60)
print(f"  laid still on the ring of 6: the clock {tc0} -> {tc} rounds for 60 sign changes (period^2 ratio {rc} permille), light {tl0} -> {tl} ({rl} permille); light's slowing over the clock's, 1 + gamma = {opg} permille (P2's laid -c00/12 gave 2490, 0 gave 1000, +c00/12 gave about 0)")
print("  reading: on the metric the act's own push makes, light speeds up where the clock slows: gamma well below -1; the gamma = 1 of P2 is on slots laid by hand with the opposite sign")

print("\n== B2. the laid -c00 / 12 at a small depth against P2's c00 = 600, with 600 sign changes: the slot form's own law 2 / (1 - u)")
for c00_, n in ((60, 600), (600, 60)):
    ii_ = -carry(c00_, 12, 0)[0]
    tc0, tl0, tc, tl, rc, rl, opg = read(c00_, ii_, n)
    u_permille = permille(c00_, REST)
    law = permille(2000, 1000 - u_permille)
    print(f"  c00 = {c00_} (u = {u_permille} permille), ii = {ii_}: clock period^2 ratio {rc} permille (law 1 + u = {1000 + u_permille}), light {rl} (law (1 + u) / (1 - u) = {permille(1000 + u_permille, 1000 - u_permille)}); 1 + gamma read {opg} permille, the slot form's 2 / (1 - u) = {law}")
print("  reading: P2's 2.49 at c00 = 600 is not 'about 2' but the slot form's own 2 / (1 - u) at u = 0.2; the first-order gamma = 1 shows only at small u")
