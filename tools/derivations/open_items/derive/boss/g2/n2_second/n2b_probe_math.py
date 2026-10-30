"""N2's second text, the mathematician's five items and the moving-W finding, measured on the engine's act.

Clock: the metric's push read from the matter's strides, and the round run back, on a clock that moves.
Algebra: whole numbers only; the first-order form (p) and the head's staged form (r), their mirrors, the cube's 24.
Board: 3 x 4 x 5 for the run backs, 3 x 3 x 3 for the 24, lays from an integer recurrence.
Clicks: n/a.

Run: <t24b>/.venv/bin/python -I n2b_probe_math.py; the output is n2b_results_math.txt.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from n2b_lib import (  # noqa: E402
    A1ROWS,
    EROWS,
    FAMILIES,
    GRAD,
    MATTER,
    METRIC,
    ROWS,
    S0I,
    S00,
    SA,
    SB,
    SII,
    SJK,
    T1ROWS,
    TURNS,
    UNIT,
    VALUE,
    Carry,
    State,
    at,
    carry,
    eye_family,
    gradient_part,
    join,
    lay,
    layout,
    metric_source,
    mirror_first,
    mirror_head,
    notch,
    potential,
    rate_part,
    run,
    same,
    sign_free,
    spring,
    step,
    term_parity_ok,
    terms,
    tick_first,
    tick_head,
    to_first,
    turn_rows,
    turn_sites,
    turned_first,
    turned_head,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line, flush=True)
    OUT.append(line)


SHAPE, ROUNDS = (3, 4, 5), 300
REST, GRIP, DRIVE_M, DRIVE_G = 3000, 500, 7, 100
NOW = join(terms(spring(210, FAMILIES)), terms(notch(5000)), terms(potential(1)), terms(gradient_part(1)))
RATE = terms(rate_part(1))
NONE = terms([])


def board_(clock="others", **kw):
    return layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock=clock, **kw)


def teeth_course(L_, states, rows=MATTER):
    """W's range, and the site-rounds where a matter clock rose and fell, over a run's states."""
    ws = [step.weight(L_.gearing, L_.clock, st.a)[rows[0]] for st in states]
    rises = sum(int((ws[t + 1] > ws[t]).sum()) for t in range(len(ws) - 1))
    falls = sum(int((ws[t + 1] < ws[t]).sum()) for t in range(len(ws) - 1))
    return min(min(x) for x in ws), max(max(x) for x in ws), rises, falls


# ------------------------------------------------------------------------------------------------ 0. the harness
say("== 0. the harness")
L = board_("every")
s = lay(Carry(1), L)
say(
    "  the staged head's form with no stride read == step.tick (the head's act, the loader's clock read):",
    same(tick_head(L, s, NOW, NONE), step.tick(L._replace(plan=NOW._replace(**{
        f: np.where(getattr(NOW, f) == UNIT, 5 * ROWS, getattr(NOW, f)).astype(np.intp)
        for f in ("first", "second", "third")})), s)),
)
Ls = board_("none")
s, t = lay(Carry(21), Ls), lay(Carry(21), Ls, first=True)
agree = True
for _ in range(ROUNDS):
    s, t = tick_head(Ls, s, NOW, RATE), tick_first(Ls, t, NOW, RATE)
    agree &= same([s.a, to_first(Ls, s).b, s.rd], [t.a, t.b, t.rd])
say(f"  standing clock: the first-order form equals the staged head's form for {ROUNDS} rounds: {agree}")

# ------------------------------------------------------------------- 5 (M5). the theorem as restated, measured
say("\n== M5. the run back of the first-order form, the clock moving (every row but the 00 row reads the 00 slot)")
Lf = board_("others")
for seed in (22, 23, 24, 25):
    states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(seed), Lf, first=True), ROUNDS, NOW, RATE)
    lo, hi, rises, falls = teeth_course(Lf, states)
    rd_ok = all(bool(((st.rd >= 0) & (st.rd < Lf.gearing.drive)).all()) for st in states)
    say(
        f"  lay {seed}: W in [{lo}, {hi}], {rises} site-rounds rising and {falls} falling; every r_d within "
        f"[0, T_d): {rd_ok}; {ROUNDS} rounds forth and back bit for bit: {k is None}; moved: {not same(states[-1], states[0])}"
    )

# ------------------------------------------------------------------- 1 (M1). the four hypotheses, each broken
say("\n== M1. the four hypotheses, each broken case")
# (a) every r_d within [0, T_d)
s0 = lay(Carry(31), Lf, first=True)
bad = State(s0.a, s0.b, s0.r, s0.rd.copy())
bad.rd[S00, 0] = Lf.gearing.drive[S00, 0] + 3
bad.rd[A1ROWS[0], 5] = Lf.gearing.drive[A1ROWS[0], 0] + 2
states, k, rows = run(tick_first, mirror_first, Lf, bad, 20, NOW, RATE)
say(f"  (a) two drive teeth laid at T_d + 3 and T_d + 2: 20 rounds; departs at round back {k} (the start's own round), rows {rows}")
sh = lay(Carry(31), Ls)
badh = State(sh.a, sh.b, sh.r.copy(), sh.rd)
badh.r[A1ROWS[0], 5] = step.weight(Ls.gearing, Ls.clock, sh.b)[A1ROWS[0], 5] + 4
states, k, rows = run(tick_head, mirror_head, Ls, badh, 20, NOW, RATE)
say(f"      the head's form, one fine tooth laid at W + 4: departs at round back {k}, rows {rows}")
# (b) the parity of every monomial
cases = [
    ("00 <- sigma_b(T1 x) D_x(T1 x): one odd leg onto an even row", [(at(SB, 0), at(GRAD, 0), UNIT, 1, S00)]),
    ("0x <- sigma_b(A1) sigma_a(A1): two odd legs onto an odd row", [(at(SB, 5), at(SA, 5), UNIT, 1, S0I[0])]),
    ("00 <- value(0x) value(T1 x): the 0x row's count, odd, onto an even row", [(at(VALUE, S0I[0]), at(VALUE, 0), UNIT, 1, S00)]),
    ("0x <- value(0y) value(T1 x) value(T1 y): one odd leg onto an odd row (holds)", [(at(VALUE, S0I[1]), at(VALUE, 0), at(VALUE, 1), 1, S0I[0])]),
    ("yz <- value(0y) value(0z): two odd legs onto an even row (holds)", [(at(VALUE, S0I[1]), at(VALUE, S0I[2]), UNIT, 1, SJK[0])]),
]
for name, extra in cases:
    where = "pass 2" if any(idx // ROWS in (SB, SA) for tm in extra for idx in tm[:3] if idx != UNIT) else "pass 1"
    plan_now, plan_rate = (NOW, join(RATE, terms(extra))) if where == "pass 2" else (join(NOW, terms(extra)), RATE)
    states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(32), Lf, first=True), 60, plan_now, plan_rate)
    say(f"  (b) {name}: parity rule says {'holds' if all(term_parity_ok(x) for x in extra) else 'breaks'}; departs at round back {k}, rows {rows}")
# (c) the clock and the grips read even rows only
Lodd = board_([(S00, r) for r in range(ROWS) if r != S00] + [(S0I[0], r) for r in MATTER])
states, k, rows = run(tick_first, mirror_first, Lodd, lay(Carry(33), Lodd, first=True), 60, NOW, RATE)
say(f"  (c) the matter's teeth read the 0x row too (odd): departs at round back {k}, rows {rows}")
Lgo = board_("others", grip_rows=[S0I[0], SII[1], SII[2]])
states, k, rows = run(tick_first, mirror_first, Lgo, lay(Carry(34), Lgo, first=True), 60, NOW, RATE)
say(f"      the x grips read the 0x row (odd): departs at round back {k}, rows {rows}")
Leven = board_([(S00, r) for r in range(ROWS) if r != S00] + [(SII[0], r) for r in MATTER])
states, k, rows = run(tick_first, mirror_first, Leven, lay(Carry(35), Leven, first=True), 60, NOW, RATE, depth=2)
say(f"      control, the matter's teeth read the xx row too (even; xx reads 00, so a read of depth 2, three carries): departs at round back {k}")
states, k, rows = run(tick_first, mirror_first, Leven, lay(Carry(35), Leven, first=True), 60, NOW, RATE, depth=1)
say(f"      the same with two carries (one too few for the depth): departs at round back {k}")
# (d) pass 2 reads only the strides of rows it does not push
own = terms([(at(SB, S00), at(SB, S00), UNIT, 1, S00), (at(SA, S00), at(SA, S00), UNIT, 1, S00)])
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(36), Lf, first=True), 60, NOW, join(RATE, own))
say(f"  (d) the 00 row's own strides squared onto the 00 slot: departs at round back {k}, rows {rows}")
fric = terms([(at(SB, 5), at(SB, 5), UNIT, 1, 5), (at(SA, 5), at(SA, 5), UNIT, 1, 5)])
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(37), Lf, first=True), 60, NOW, join(RATE, fric))
say(f"      the A1 row pushed in pass 2 by its own strides squared (parity even, as its row): departs at round back {k}, rows {rows}")
fric1 = terms([(at(VALUE, 5), at(VALUE, 5), UNIT, 1, 5)])
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(37), Lf, first=True), 60, join(NOW, fric1), RATE)
say(f"      control, the same row pushed in pass 1 by its count squared: departs at round back {k}")

# ------------------------------------------------------------------- 2 (M2). the metric's own rows as sources
say("\n== M2. the metric's own rows as sources of the 00 and 0i slots")
spatial = terms(rate_part(1, families=[eye_family(SII + SJK)]))
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(41), Lf, first=True), ROUNDS, NOW, join(RATE, spatial))
lo, hi, rises, falls = teeth_course(Lf, states)
say(f"  the ii and jk rows' strides onto 00 (squares) and 0i (times their gradients), the clock moving (W in [{lo}, {hi}]): {ROUNDS} rounds exact: {k is None}")
shift = terms(rate_part(1, families=[eye_family(S0I)], slot0i=False))
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(42), Lf, first=True), 60, NOW, join(RATE, shift))
say(f"  the 0i rows' own strides squared onto 00 (parity even, but pass 2 pushes the 0i rows): departs at round back {k}, rows {rows}")
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(43), Lf, first=True), 60, NOW, join(RATE, own))
say(f"  the 00 row's own strides squared onto 00: departs at round back {k}, rows {rows}")

# ------------------------------------------------------------------- 3 (M3). rho and the pressure from J
say("\n== M3. 4 rho = J00 + sum J_ii and 4 pr = J00 - (sum J_ii) / 3, read from the probe's own J (strength 1 per slot)")
L0 = board_("none")
n = L0.nb.shape[1]
T5 = join(terms(gradient_part(1)), terms(potential(1)))
T5KIN = join(terms(gradient_part(1)), terms(potential(0)))


def read_j(s_, first=False, now=T5):
    j = metric_source(L0, s_, now, RATE, first=first)
    j00 = int(j[S00][0])
    jii = [int(j[x][0]) for x in SII]
    uniform = all(len(set(j[x].tolist())) == 1 for x in METRIC)
    return j00, jii, uniform


a = np.zeros((ROWS, n), dtype=object)
a[A1ROWS] = 77
b = a.copy()
b[A1ROWS] = 70
j00, jii, uni = read_j(State(a, b, 0 * a, 0 * a), now=T5KIN)
say(f"  the uniform swing, stride 7, no spring, no potential: J00 = {j00}, J_ii = {jii}, uniform over the board: {uni}; 4 rho = {j00 + sum(jii)}, 4 pr = {j00} - {sum(jii)} / 3 = {3 * j00 - sum(jii)} / 3: rho = pr = {j00 + sum(jii)} / 4 (stiff, P = rho)")
a = np.zeros((ROWS, n), dtype=object)
a[A1ROWS] = 5
j00, jii, uni = read_j(State(a, a.copy(), 0 * a, 0 * a))
say(f"  a count held still at 5, the potential 2V = x^2 (kv = 1): J00 = {j00} (below 0: S00 = 0, 2 eta_00 V = -2V), J_ii = {jii}; 4 rho = {j00 + sum(jii)} = 4V, 4 pr = {3 * j00 - sum(jii)} / 3 = -4V: rho = V, pr = -V")
a = np.zeros((ROWS, n), dtype=object)
z = (np.arange(n) % 5)
a[A1ROWS[0]] = np.array([(2, 1, -1, -2, 0)[k] for k in z], dtype=object) * 3  # a profile along z (the fastest axis, side 5)
j = metric_source(L0, State(a, a.copy(), 0 * a, 0 * a), T5, RATE)
tot = [int(j[x].sum()) for x in (S00, *SII, *S0I)]
say(f"  a count held still with a gradient along z: board sums J00 = {tot[0]}, J_xx, J_yy, J_zz = {tot[1:4]}, J_0i = {tot[4:]}: 4 rho = {tot[0] + sum(tot[1:4])}, 4 pr = {3 * tot[0] - sum(tot[1:4])} / 3 (the gradient's pressure is anisotropic: the trace, not 3 J_ii)")

# ------------------------------------------------------------------- 4 (M4). the clock's reads acyclic
say("\n== M4. the drift D inverts only where the clock's reads are acyclic")
R0, P = 2, 10
coll = [(x, x + carry(P, R0 + x, 0)[0]) for x in (1, 2)]
say(f"  the 00 row reading itself, x -> x + p div (R + x) at R = {R0}, p = {P}: {coll[0]} and {coll[1]}: two counts, one image")
Lm = board_("every")
states, k, rows = run(tick_first, mirror_first, Lm, lay(Carry(51), Lm, first=True), 20, NOW, RATE)
say(f"      the loader's lay (every row reads the 00 slot, the 00 row too): departs at round back {k}, rows {rows}")
# a cycle among even rows: the 00 row's teeth read the xx slot, the xx row's teeth read the 00 slot
cyc = [(S00, r) for r in range(ROWS) if r not in (S00, SII[0])] + [(SII[0], S00), (S00, SII[0])]
Lc = board_(cyc)
images = set()
grid = [(x, y) for x in range(0, 40) for y in range(0, 40)]
px, py = 30 * REST + 7, 20 * REST + 11
for x, y in grid:
    images.add((x + carry(px, REST + y, 0)[0], y + carry(py, REST + x, 0)[0]))
say(f"      a cycle (00 reads xx, xx reads 00): the drift on a 40 x 40 grid of (c00, cxx) at fixed rates has {len(images)} images for {len(grid)} states: not a bijection")
states, k, rows = run(tick_first, mirror_first, Lc, lay(Carry(52), Lc, first=True), 60, NOW, RATE, depth=1)
say(f"      its run back with the two-carry mirror: departs at round back {k}, rows {rows}")
states, k, rows = run(tick_first, mirror_first, Lc, lay(Carry(52), Lc, first=True), 60, NOW, RATE, depth=5)
say(f"      with six carries: departs at round back {k}, rows {rows}")
# an acyclic chain of depth 2: xx reads 00; every other row reads xx
chain = [(S00, SII[0])] + [(SII[0], r) for r in range(ROWS) if r not in (S00, SII[0])]
Lch = board_(chain)
states, k, rows = run(tick_first, mirror_first, Lch, lay(Carry(53), Lch, first=True), ROUNDS, NOW, RATE, depth=2)
lo, hi, rises, falls = teeth_course(Lch, states)
say(f"      an acyclic chain of depth 2 (xx reads 00, every other row reads xx; W in [{lo}, {hi}]): three carries, {ROUNDS} rounds exact: {k is None}")
states, k, rows = run(tick_first, mirror_first, Lch, lay(Carry(53), Lch, first=True), 60, NOW, RATE, depth=1)
say(f"      the same with two carries: departs at round back {k}, rows {rows}")

# ------------------------------------------------------------------- 6. the moving-W finding, in both forms
say("\n== F. the moving-W finding (the 24's readers, 2026-10-30): the forward drift and the 24, in both forms")
CUBE = (3, 3, 3)


def cube_layout(clock="others"):
    return layout(CUBE, 10, 10, 1, 1, 1, clock=clock)


def cube_lay(L_, seed, a00, b00, first):
    """T1 and A1 rows drawn in [-40, 40] with strides in [-5, 5], E rows 0, the 00 slot at (a00, b00) everywhere,
    the other metric slots 0, teeth drawn within W(b), drive teeth 0 (T_d = 1)."""
    seq = Carry(seed)
    n = L_.nb.shape[1]
    a = np.zeros((ROWS, n), dtype=object)
    b = np.zeros((ROWS, n), dtype=object)
    for row in T1ROWS + A1ROWS:
        a[row] = seq.draw(-40, 41, (n,))
        b[row] = a[row] - seq.draw(-5, 6, (n,))
    a[S00], b[S00] = a00, b00
    wb = step.weight(L_.gearing, L_.clock, b)
    _, r = carry(seq.draw(0, 1 << 40, (ROWS, n)), wb, 0)
    r[S00] = 0
    rd = 0 * a
    s_ = State(a, b, r, rd)
    return to_first(L_, s_) if first else s_


def sums_of_strides(L_, st, first):
    """Each active row's board sum of its stride (a - b in the r-form; p div W, the stride out, in the p-form), and
    of p itself in the p-form."""
    if first:
        w = step.weight(L_.gearing, L_.clock, st.a)
        q, _ = carry(st.b, w, 0)
        return q.sum(axis=1), st.b.sum(axis=1)
    return (st.a - st.b).sum(axis=1), None


Lcube = cube_layout()
FREE = terms([])
for form, tick, first in (("the head's r-form", tick_head, False), ("the first-order p-form", tick_first, True)):
    for label, a00, b00 in (("rising by 1 a round from W = 14", 4, 3), ("standing at W = 14 (control)", 4, 4)):
        st = cube_lay(Lcube, 11, a00, b00, first)
        start, p_start = sums_of_strides(Lcube, st, first)
        for _ in range(40):
            st = tick(Lcube, st, FREE, FREE)
        end, p_end = sums_of_strides(Lcube, st, first)
        w = step.weight(Lcube.gearing, Lcube.clock, st.a)
        t1 = [int(end[r] - start[r]) for r in T1ROWS]
        say(f"  {form}, no source (J = 0), the 00 slot {label}: after 40 rounds W = {int(w[0, 0])}; the change of each T1 row's board sum of strides: {t1}, the A1 row's: {int(end[5] - start[5])}")
        if first:
            say(f"      the board sum of p per T1 row at round 0 and 40: {[int(p_start[r]) for r in T1ROWS]} -> {[int(p_end[r]) for r in T1ROWS]} (exactly kept: {bool((p_start[T1ROWS + A1ROWS] == p_end[T1ROWS + A1ROWS]).all())})")


def the_24(L_, s_, tick, first, rounds, now_plan, rate_plan):
    """Per round: how many of the 24 turns give tick^n (turned s) = turned (tick^n s), the whole state and the counts
    a alone, and the largest |delta a| over the 21 sign-flipping turns; the image's tooth (r, or the rate p) flipped
    in the teeth of the round that made it."""
    g = L_.gearing
    states = [s_]
    for _ in range(rounds):
        states.append(tick(L_, states[-1], now_plan, rate_plan))
    held, held_a, worst = [0] * rounds, [0] * rounds, [0] * rounds
    for gi in TURNS:
        p = turn_rows(gi)
        site = turn_sites(gi, CUBE)
        turned = turned_first if first else turned_head
        t = turned(s_, p, site, step.weight(g, L_.clock, s_.a), g.drive)
        for k in range(rounds):
            t = tick(L_, t, now_plan, rate_plan)
            image = turned(states[k + 1], p, site, step.weight(g, L_.clock, states[k].a), g.drive)
            held[k] += same(t, image)
            held_a[k] += bool(np.array_equal(t.a, image.a))
            if not sign_free(p):
                worst[k] = max(worst[k], int(abs(t.a - image.a).max()))
    return held, held_a, worst


for form, tick, first in (("the head's r-form", tick_head, False), ("the first-order p-form", tick_first, True)):
    for label, a00, b00 in (("standing at W = 14", 4, 4), ("rising by 1 a round from W = 14", 4, 3)):
        st = cube_lay(Lcube, 12, a00, b00, first)
        held, held_a, worst = the_24(Lcube, st, tick, first, 6, FREE, FREE)
        say(f"  {form}, J = 0, the 00 slot {label}: turned run = run turned, rounds 1..6: {held} (the counts a alone: {held_a}); largest |delta a| over the flipping turns: {worst}")

Path(__file__).resolve().parent.joinpath("n2b_results_math.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
