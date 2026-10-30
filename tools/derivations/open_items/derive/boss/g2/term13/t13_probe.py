"""Term 13, the frozen clock: where the teeth W grow without bound on the slot form, with no hold and no restore,
measured on the engine's act in the first-order form of term 5 (N2's second text).

Clock: a clock's beat goes as the root of its spring over its teeth, so it stops only where W grows without bound;
light's speed goes as the root of the grip over the teeth, so light stops where the grip vanishes.
Algebra: whole numbers only; the first-order form's tick and mirror (../n2_second/n2b_lib.py), the head's act where
the metric stands still.
Board: one Node-clock for the uniform swing, 3 x 3 x 16 for the lump, a ring of 12 for the grip's regimes, a cube of
3 for the 24.
Clicks: a horizon in the clicks is a rate N = sqrt(rest / W) that falls to 0.

Run: <t24b>/.venv/bin/python -I t13_probe.py; the output is t13_results.txt.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "n2_second"))

import numpy as np  # noqa: E402
from n2b_lib import (  # noqa: E402
    A1ROWS,
    FAMILIES,
    METRIC,
    ROWS,
    S0I,
    S00,
    SII,
    SJK,
    T1ROWS,
    TURNS,
    Carry,
    State,
    carry,
    engine_plan,
    gradient_part,
    join,
    layout,
    mirror_first,
    potential,
    rate_part,
    run,
    same,
    sign_free,
    spring,
    step,
    table,
    terms,
    tick_first,
    to_first,
    turn_rows,
    turn_sites,
    turned_first,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line, flush=True)
    OUT.append(line)


REST, GRIP, G = 3000, 500, 210
CLOCK, LIGHT = A1ROWS[0], T1ROWS[0]
SPRING = terms(spring(G, [(A1ROWS, table("A1"))]))
UNIT = 7 * ROWS


def at(plane, row):
    return plane * ROWS + row


def energy_source(families=FAMILIES):
    """Term 5 in the act's own energy units (the gear's energy E = (W / 2) sigma^2 + (g / 2) a^2, the Mesh's
    (grip / 2) (delta a)^2), twice over so that every strength is whole: the 00 slot by 2 W (sigma_b^2 + sigma_a^2)
    - 2 g a^2 (4K - 2V = rho + 3 pr), W = rest + c00 read as a leg; each 0i slot by W (sigma_b + sigma_a) D_i; each
    ii slot by grip_rest D_i^2 + 2 g a^2 and each jk by grip_rest D_j D_k. The 0i slots' unit is OPEN (G4) and the
    grip is read at rest here; the overall scale is the coupling's (G3), the drive's teeth stand in for it."""
    now, rate = [], []
    for rows, c in families:
        for x, y, cxy in pairs_(c, rows):
            now.append((at(0, x), at(0, y), UNIT, -2 * G * cxy, S00))
            now += [(at(0, x), at(0, y), UNIT, 2 * G * cxy, s) for s in SII]
            for i in range(3):
                now.append((at(1 + i, x), at(1 + i, y), UNIT, GRIP * cxy, SII[i]))
            for k in range(3):
                i, j = (k + 1) % 3, (k + 2) % 3
                now.append((at(1 + i, x), at(1 + j, y), UNIT, GRIP * cxy, SJK[k]))
            for plane in (5, 6):
                rate.append((at(plane, x), at(plane, y), at(0, S00), 2 * cxy, S00))
                rate.append((at(plane, x), at(plane, y), UNIT, 2 * REST * cxy, S00))
                for i in range(3):
                    rate.append((at(plane, x), at(1 + i, y), at(0, S00), cxy, S0I[i]))
                    rate.append((at(plane, x), at(1 + i, y), UNIT, REST * cxy, S0I[i]))
    return terms(now), terms(rate)


def pairs_(c, rows):
    return [(rows[i], rows[j], int(c[i, j])) for i in range(len(rows)) for j in range(len(rows)) if c[i, j]]


T5, RATE = energy_source()
NOW = join(SPRING, T5)  # the matter's spring and term 5, no notch: nothing restores the metric
TD = 1000  # the metric rows' drive teeth: the probe's stand-in for the coupling's scale (G3), a carry, no bound


def promise_holds(L_, st):
    return bool((step.weight(L_.gearing, L_.clock, st.a) >= 1).all())


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
        if rounds > 200000:
            return None
    return rounds


def teeth(L_, st):
    return step.weight(L_.gearing, L_.clock, st.a)


# ------------------------------------------------------------------------------ 1. the beat against W
say("== 1. the clock's beat against its teeth (the engine's act, the metric standing): period^2 goes as W")
L6 = layout((1, 1, 6), REST, REST, GRIP, 1, 1, clock="others")
base = None
for mult in (1, 2, 4, 8, 16):
    c00 = (mult - 1) * REST
    t = crossings(L6, still(L6, {CLOCK: 10**6}, {S00: c00}), SPRING, CLOCK, 0, 40)
    base = base or t
    say(f"  W = {mult} rest: 40 sign changes in {t} rounds; period^2 / period_rest^2 = {carry(1000 * t * t, base * base, 0)[0]} permille against W / rest = {1000 * mult}")
say("  N = sqrt(rest / W): the clock stops only where W grows without bound; at every finite W it beats")

# ------------------------------------------------------------------------------ 2. the uniform swing winds W without bound
say(f"\n== 2. the uniform swing with term 5 in energy units, no notch, the metric's drive at T_d = {TD}: W over the rounds")
L1 = layout((1, 1, 1), REST, REST, GRIP, 1, TD, clock="others")
s_ = still(L1, {}, {})
s_ = to_first(L1, s_)
s_.b[CLOCK, 0] = 10 * REST  # the clock's gear swinging at stride 10 through the origin
course = []
T = 3000
st = s_
broke = None
for t in range(T + 1):
    if not promise_holds(L1, st):
        broke = t
        break
    if t % 500 == 0:
        w = int(teeth(L1, st)[CLOCK, 0])
        course.append((t, w, int(st.b[S00, 0]), int(st.b[CLOCK, 0]), int(st.a[CLOCK, 0])))
    if t < T:
        st = tick_first(L1, st, NOW, RATE)
for t, w, p00, pc, ac in course:
    say(f"  round {t:5d}: W = {w:9d}, the 00 row's rate p00 = {p00:10d}, the clock gear's p = {pc:10d} (its stride {carry(pc, w, 0)[0]:4d}), count {ac:6d}")
say(f"  the promise W >= 1 held through every round: {broke is None}")
states, k, rows = run(tick_first, mirror_first, L1, s_, T, NOW, RATE)
say(f"  {T} rounds forth and back bit for bit: {k is None}")
say("  4K - 2V averages to the swing's energy, above 0, so the 00 slot is pushed up round after round; as W grows the swing slows and its energy drains into the clock's rate; nothing holds or restores W: it grows without bound, the clock slowing as 1 / sqrt(W), frozen at no finite round")

# ------------------------------------------------------------------------------ 3. a lump: the well is bounded, the mean is not
say("\n== 3. a lump on a board: the well against the board's mean")
SH = (3, 3, 16)
Lb = layout(SH, REST, REST, GRIP, 1, TD, clock="others")
nb_ = Lb.nb.shape[1]
centre = (1 * 3 + 1) * 16 + 8
far = (1 * 3 + 1) * 16 + 0
s_ = to_first(Lb, still(Lb, {}, {}))
s_.b[CLOCK, centre] = 10 * REST
T = 1500
st = s_
broke = None
for t in range(T + 1):
    if not promise_holds(Lb, st):
        broke = t
        break
    if t % 250 == 0:
        c = st.a[S00]
        mean, _ = carry(int(c.sum()), nb_, 0)
        say(f"  round {t:5d}: c00 at the lump {int(c[centre]):7d}, at the far site {int(c[far]):7d}, the board's mean {int(mean):7d}; the well (lump - far) {int(c[centre] - c[far]):6d}; the xx slot at the lump {int(st.a[SII[0], centre]):6d}, the clock gear's stride {int(carry(st.b[CLOCK, centre], teeth(Lb, st)[CLOCK, centre], 0)[0]):4d}")
    if t < T:
        st = tick_first(Lb, st, NOW, RATE)
say(f"  the promise held through every round: {broke is None}")
states, k, rows = run(tick_first, mirror_first, Lb, s_, 300, NOW, RATE)
say(f"  300 rounds forth and back bit for bit on this board: {k is None}")
say("  the well settles (the 00 wave carries the push away at light's speed) while the mean grows: on the slot form W grows without bound through the board's mean alone, every clock alike; a horizon at one Node-clock does not follow")

# ------------------------------------------------------------------------------ 4. where the grip vanishes, light stops
say("\n== 4. the grip's three regimes at the chosen ratio ii = -c00 / 12 (gamma = 1): the metric laid still")
L12 = layout((1, 1, 12), REST, REST, GRIP, 1, 1, clock="others")
for c00, ii, name in ((0, 0, "grip 500, W = rest"), (3000, -250, "grip 0, W = 2 rest: light's horizon"), (3600, -300, "grip -100, W = 2.2 rest: beyond it")):
    metric = {S00: c00, SII[0]: ii, SII[1]: ii, SII[2]: ii}
    s_light = still(L12, {LIGHT: mode6(12, 10**3)}, metric)
    L12e = L12._replace(plan=engine_plan(SPRING))
    st = s_light
    peak = []
    for t in range(1, 61):
        st = step.tick(L12e, st)
        if t % 20 == 0:
            peak.append(int(abs(st.a[LIGHT]).max()))
    moved = int(abs(st.a[LIGHT] - s_light.a[LIGHT]).max())
    tl = crossings(L12, s_light, SPRING, LIGHT, 0, 20) if ii == 0 else None
    tc = crossings(L12, still(L12, {CLOCK: 10**6}, metric), SPRING, CLOCK, 0, 40)
    back = step.untick(L12e, st)
    for _ in range(59):
        back = step.untick(L12e, back)
    say(f"  {name}: light's wave peak at rounds 20, 40, 60: {peak} (laid 2000); moved at all after 60 rounds: {moved != 0}; light's 20 sign changes in {tl} rounds; the clock's 40 in {tc} rounds; 60 rounds run back exact: {same(back, s_light)}")
say("  at grip 0 light stands (the pull vanishes) while the clock beats at N^2 = 1 / 2; beyond, the Mesh pushes the neighbours apart and the strides grow without bound: the slot form's edge is light's, not the clock's")

# ------------------------------------------------------------------------------ 5. the other edge: W falls to 1
say("\n== 5. the potential's push (eta_00 = -1) with no hold: W falls to the act's edge")
s_ = to_first(L1, still(L1, {CLOCK: 40}, {}))
st = s_
FREE_POT = T5  # a count held still, no spring: J00 = -2V = -2 g a^2 every round, through the drive at T_d
t, broke = 0, None
while t < 4000:
    w = teeth(L1, st)
    if int(w.min()) < 1:
        broke = t
        break
    if t % 50 == 0:
        say(f"  round {t:4d}: W = {int(w[CLOCK, 0]):6d}, p00 = {int(st.b[S00, 0]):8d}, the xx slot {int(st.a[SII[0], 0]):6d} (the grips rise)")
    st = tick_first(L1, st, FREE_POT, RATE)
    t += 1
say(f"  the promise W >= 1 breaks before round {broke}: the runner names it from outside; the act holds nothing")
say("  where rho + 3 pr < 0 persists (a potential held still) the slot form runs W down to 1: the clock races (N^2 = rest / W grows) and light with it; this edge is the carry's own, and no term restores it (term 9, OPEN)")

# ------------------------------------------------------------------------------ 6. the 24 on a clock that moves by term 5
say("\n== 6. the cube's 24 on a clock moved by term 5 (the p-form), and on a clock rising fast")
CUBE = (3, 3, 3)
Lc = layout(CUBE, REST, REST, GRIP, 1, TD, clock="others")


def cube_lay(seed, p00):
    seq = Carry(seed)
    n = Lc.nb.shape[1]
    a = np.zeros((ROWS, n), dtype=object)
    b = np.zeros((ROWS, n), dtype=object)
    for row in T1ROWS + A1ROWS:
        a[row] = seq.draw(-40, 41, (n,))
        b[row] = a[row] - seq.draw(-30, 31, (n,))
    st = to_first(Lc, State(a, b, 0 * a, 0 * a))
    st.b[S00] = p00
    return st


def the_24(s_, rounds, now_plan, rate_plan):
    g = Lc.gearing
    states = [s_]
    for _ in range(rounds):
        states.append(tick_first(Lc, states[-1], now_plan, rate_plan))
    held, held_a, worst = [0] * rounds, [0] * rounds, [0] * rounds
    for gi in TURNS:
        p = turn_rows(gi)
        site = turn_sites(gi, CUBE)
        t = turned_first(s_, p, site, teeth(Lc, s_), g.drive)
        for k in range(rounds):
            t = tick_first(Lc, t, now_plan, rate_plan)
            image = turned_first(states[k + 1], p, site, teeth(Lc, states[k]), g.drive)
            held[k] += same(t, image)
            held_a[k] += bool(np.array_equal(t.a, image.a))
            if not sign_free(p):
                worst[k] = max(worst[k], int(abs(t.a - image.a).max()))
    w0, w1 = teeth(Lc, states[0])[CLOCK], teeth(Lc, states[-1])[CLOCK]
    return held, held_a, worst, int(w0.min()), int(w1.max())


held, held_a, worst, w0, w1 = the_24(cube_lay(3, 0), 6, SPRING, terms([]))
say(f"  the clock standing (no term 5), W = {w0}: turned run = run turned, rounds 1..6: {held}; largest |delta a| {worst}")
held, held_a, worst, w0, w1 = the_24(cube_lay(3, 0), 6, NOW, RATE)
say(f"  term 5 on, the clock moved by the matter, W from {w0} to {w1}: {held} (the counts a alone {held_a}); largest |delta a| over the flipping turns {worst}")
held, held_a, worst, w0, w1 = the_24(cube_lay(3, 20 * REST), 6, SPRING, terms([]))
say(f"  the 00 slot laid rising by 20 a round (no term 5), W from {w0} to {w1}: {held} (a alone {held_a}); largest |delta a| {worst}")
held, held_a, worst, w0, w1 = the_24(cube_lay(3, 3000 * REST), 6, SPRING, terms([]))
say(f"  the 00 slot laid rising by 3000 a round (W doubling at the first round), W from {w0} to {w1}: {held} (a alone {held_a}); largest |delta a| {worst}")
say("  the flip of a rate in its teeth, W - 1 - p, moves with W: the 21 sign-flipping turns depart from the second round wherever W moved, by whole notches where the shifted dividend crosses a carry; where W grows fast the departure is many notches a round")

HERE.joinpath("t13_results.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
