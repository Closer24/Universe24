"""The hostile mathematician's checks on N2's second text, section 4 (the theorem): whole numbers only.

Clock: the first-order form's run back, attacked at its hypotheses.
Algebra: n2b_lib's tick_first and mirror_first, unchanged; the plans varied.
Board: 3 x 4 x 5 as the text's; a small-teeth board where W reaches 1.
Clicks: n/a.

Run: <t24b>/.venv/bin/python -I probe_theorem.py; the output is probe_theorem.txt.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "g2" / "n2_second"))

import numpy as np  # noqa: E402
from n2b_lib import (  # noqa: E402
    A1ROWS,
    FAMILIES,
    GRAD,
    MATTER,
    ROWS,
    S0I,
    S00,
    SA,
    SB,
    SII,
    UNIT,
    VALUE,
    Carry,
    State,
    at,
    carry,
    gradient_part,
    join,
    lay,
    layout,
    mirror_first,
    notch,
    potential,
    rate_part,
    run,
    spring,
    step,
    term_parity_ok,
    terms,
    tick_first,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line, flush=True)
    OUT.append(line)


SHAPE, ROUNDS = (3, 4, 5), 60
REST, GRIP, DRIVE_M, DRIVE_G = 3000, 500, 7, 100
NOW = join(terms(spring(210, FAMILIES)), terms(notch(5000)), terms(potential(1)), terms(gradient_part(1)))
RATE = terms(rate_part(1))
Lf = layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock="others")

# ---------------------------------------------------------------- 1. hypothesis (b) is not enough: the swap of the strides
say("== 1. the swap of the two stride planes: monomials that pass the text's parity rule (b) and still depart")
cases = [
    ("00 <- sigma_b(A1)^2 alone (no sigma_a partner)", [(at(SB, 5), at(SB, 5), UNIT, 1, S00)]),
    ("00 <- sigma_a(A1)^2 alone", [(at(SA, 5), at(SA, 5), UNIT, 1, S00)]),
    ("00 <- sigma_b(T1 x) sigma_a(T1 y) alone (x != y, one ordering)", [(at(SB, 0), at(SA, 1), UNIT, 1, S00)]),
    ("0x <- sigma_b(A1) D_x(A1) alone (no sigma_a partner)", [(at(SB, 5), at(GRAD, 5), UNIT, 1, S0I[0])]),
    ("control: 00 <- sigma_b(A1)^2 + sigma_a(A1)^2 (the pair)", [(at(SB, 5), at(SB, 5), UNIT, 1, S00), (at(SA, 5), at(SA, 5), UNIT, 1, S00)]),
    ("control: 00 <- sigma_b(T1 x) sigma_a(T1 y) + sigma_b(T1 y) sigma_a(T1 x)", [(at(SB, 0), at(SA, 1), UNIT, 1, S00), (at(SB, 1), at(SA, 0), UNIT, 1, S00)]),
    ("control: 00 <- sigma_b(A1) sigma_a(A1) alone (its own swap image)", [(at(SB, 5), at(SA, 5), UNIT, 1, S00)]),
]
for name, extra in cases:
    ok = all(term_parity_ok(x) for x in extra)
    states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(61), Lf, first=True), ROUNDS, NOW, join(RATE, terms(extra)))
    # how often the two strides differ on the A1 row over the run (the swap is not the identity)
    differ = 0
    for st in states[:-1]:
        a, p, _, rd = st
        w = step.weight(Lf.gearing, Lf.clock, a)
        sb, _ = carry(p, w, 0)
        j1 = 0  # not needed: count only where the stride in differs from the stride out of the actual round
    say(f"  {name}: parity rule (b) says {'holds' if ok else 'breaks'}; departs at round back {k}, rows {rows}")
a, p, _, _ = states[0]
w = step.weight(Lf.gearing, Lf.clock, a)
sb0, _ = carry(p, w, 0)
a1 = states[1].a
say(f"  (at the first round the stride in and the stride out differ at {int((sb0[MATTER] != (a1 - a)[MATTER]).sum())} of {sb0[MATTER].size} matter gears: the swap is not the identity)")

# ---------------------------------------------------------------- 2. hypothesis (c): read, not landed
say("\n== 2. hypothesis (c) as written says the reads 'land' on even rows; what matters is which rows are read")
Lodd_target = layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock=[(S00, r) for r in range(ROWS) if r != S00])
odd_targets = [r for r in range(ROWS) if r in S0I]
states, k, rows = run(tick_first, mirror_first, Lodd_target, lay(Carry(62), Lodd_target, first=True), ROUNDS, NOW, RATE)
say(f"  the 00 slot (even) read into every other row, the odd 0i rows {odd_targets} among the targets (the text's own M5 lay): departs at round back {k}")
Lodd_source = layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock=[(S00, r) for r in range(ROWS) if r != S00] + [(S0I[1], 5)])
states, k, rows = run(tick_first, mirror_first, Lodd_source, lay(Carry(63), Lodd_source, first=True), ROUNDS, NOW, RATE)
say(f"  the odd 0y row read into the even A1 row's teeth (one read, factor 1): departs at round back {k}, rows {rows}")
Leven_source = layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock=[(S00, r) for r in range(ROWS) if r != S00] + [(SII[1], S0I[0])])
states, k, rows = run(tick_first, mirror_first, Leven_source, lay(Carry(64), Leven_source, first=True), ROUNDS, NOW, RATE, depth=2)
say(f"  the even yy row read into the odd 0x row's teeth (depth 2, three carries): departs at round back {k}")

# ---------------------------------------------------------------- 3. W of at least 1: the theorem near its edge
say("\n== 3. the run back where W reaches 1 (small teeth; the text measured W in [2816, 3208] only)")
for rest_m, seed in ((4, 71), (4, 72), (3, 73)):
    TDG = 1000
    # grip 0: at W near 1 any whole grip breaks the wave's stability (grip / W above 1 / 3), so the Meshes pull nothing
    # here; the plan still reads the neighbours through the gradients
    Ls = layout(SHAPE, rest_m, 50, 0, 1, TDG, clock="others")
    # a lay whose 00 slot swings so that W = rest_m + c00 visits 1: counts of the 00 row within [-(rest_m - 1), 6]
    seq = Carry(seed)
    n = Ls.nb.shape[1]
    a0 = np.zeros((ROWS, n), dtype=object)
    p0 = np.zeros((ROWS, n), dtype=object)
    for row in MATTER:
        a0[row] = seq.draw(-6, 7, (n,))
    a0[S00] = seq.draw(-(rest_m - 1), rest_m, (n,))  # W = rest_m + c00 within [1, 2 rest_m - 1]
    w0 = step.weight(Ls.gearing, Ls.clock, a0)
    for row in MATTER:
        p0[row] = seq.draw(-3, 4, (n,)) * w0[row] + carry(seq.draw(0, 1 << 20, (n,)), w0[row], 0)[1]
    _, rd0 = carry(seq.draw(0, 1 << 20, (ROWS, n)), Ls.gearing.drive, 0)
    s0 = State(a0, p0, 0 * a0, rd0)
    # the 00 slot swings on a notch of strength T_d (q = -c00 exactly), so W wanders between 1 and about 2 rest;
    # the matter's spring at 1, its potential and gradient onto the slots at strength 1 through T_d = 1000
    plan_now = join(terms(spring(1, FAMILIES)), terms(notch(TDG, rows=[S00])), terms(potential(1)), terms(gradient_part(1)))
    # forward while the promise W >= 1 holds at the now slot (the runner's read from outside), at most 40 rounds
    states = [s0]
    while len(states) <= 40:
        w = step.weight(Ls.gearing, Ls.clock, states[-1].a)
        if int(w.min()) < 1:
            break
        states.append(tick_first(Ls, states[-1], plan_now, RATE))
    held = len(states) - 1
    if int(step.weight(Ls.gearing, Ls.clock, states[-1].a).min()) < 1:
        states.pop()  # the last state stands below the promise: its round is not run
        held -= 1
    t = states[-1]
    first_bad = None
    for k in range(held):
        t = mirror_first(Ls, tick_first(Ls, mirror_first(Ls, t), plan_now, RATE))
        want = states[held - 1 - k]
        if not all(np.array_equal(x, y) for x, y in zip(t, want, strict=True)):
            first_bad = k + 1
            break
    ws = [step.weight(Ls.gearing, Ls.clock, st.a) for st in states]
    wmin = min(int(w[MATTER].min()) for w in ws)
    wmax = max(int(w[MATTER].max()) for w in ws)
    ones = sum(int((w[MATTER] == 1).sum()) for w in ws)
    say(f"  rest {rest_m}: {held} rounds within the promise (W of the matter rows in [{wmin}, {wmax}], {ones} matter site-rounds at W = 1); those rounds forth and back bit for bit: {first_bad is None}{'' if first_bad is None else f' (departs at round back {first_bad})'}")

# ---------------------------------------------------------------- 4. the sign law of the carry on the dividend, stated for all p
say("\n== 4. (W - 1 - p) div W = -(p div W) for every whole p at every W >= 1, and fails at W <= 0 (the text's load-bearing line)")
misses = {}
for W in range(-3, 8):
    if W == 0:
        continue
    miss = 0
    for p in range(-50, 51):
        if (W - 1 - p) // W != -(p // W):
            miss += 1
    misses[W] = miss
say(f"  misses per W over p in [-50, 50]: {misses}")

Path(HERE / "probe_theorem.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
