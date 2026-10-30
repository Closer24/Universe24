"""N2 probe: the metric's push reading the matter's four-vector, and the run back. Whole numbers only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from n2_lib import (  # noqa: E402
    A1ROWS,
    EROWS,
    FAMILIES,
    GRAD,
    KINDS,
    MATTER,
    METRIC,
    ODD,
    PLANES,
    ROWS,
    S0I,
    S00,
    SA,
    SB,
    SII,
    SJK,
    SQUARE,
    T1ROWS,
    UNIT,
    VALUE,
    Carry,
    State,
    at,
    carry,
    contract,
    gradient_part,
    join,
    lay,
    layout,
    metric_gradient_selfpush,
    mirror_first,
    mirror_head,
    notch,
    potential,
    rate_part,
    readings,
    run,
    same,
    spring,
    step,
    terms,
    tick_first,
    tick_head,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line)
    OUT.append(line)


SHAPE, ROUNDS = (3, 4, 5), 300
REST, GRIP, DRIVE_M, DRIVE_G = 3000, 500, 7, 100
NOW = join(
    terms(spring(210, FAMILIES)), terms(notch(5000)), terms(potential(1)), terms(gradient_part(1))
)
RATE = terms(rate_part(1))
NONE = terms([])


def board_(clock):
    return layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock=clock)


# ------------------------------------------------------------------------------------------------ 0. the harness
say("== 0. the harness is the head's act where no stride is read")
L = board_("every")
engine_plan = NOW._replace(
    **{
        f: np.where(getattr(NOW, f) == UNIT, 5 * ROWS, getattr(NOW, f)).astype(np.intp)
        for f in ("first", "second", "third")
    }
)
s = lay(Carry(1), L)
say(
    "tick_head(now plan, no rate plan) == step.tick(head):",
    same(tick_head(L, s, NOW, NONE), step.tick(L._replace(plan=engine_plan), s)),
)

# ------------------------------------------------------------------------------------------------ 1. N3's numbers


def metric_source(L_, s_, now_plan, rate_plan):
    """J on the metric's rows (before the drive): pass 1's strides out, then pass 2's terms."""
    a, b, r, rd = s_
    g = L_.gearing
    w = step.weight(g, L_.clock, a)
    force, flat = readings(L_, a, a - b, 0 * a)
    j1 = contract.contract(now_plan, flat, a)
    q1d, _ = step.drive(j1, g.drive, rd)
    a1, _, _ = step.gear(a, b, r, w, step.driven(g, force, q1d))
    _, flat = readings(L_, a, a - b, a1 - a)
    return j1 + contract.contract(rate_plan, flat, a)


say("\n== 1. N3: a uniform swing, no spring, stride 7 (strength 1 per slot)")
L0 = board_("none")
n = L0.nb.shape[1]
T5 = join(terms(gradient_part(1)), terms(potential(0)))
for name, rows in (("A1 gear", A1ROWS), ("T1 gear x", T1ROWS[:1])):
    a = np.zeros((ROWS, n), dtype=object)
    a[rows] = 7 * 11  # any count, the same at every site
    s = State(a, a - 7 * (np.isin(np.arange(ROWS), rows)[:, None].astype(object)), 0 * a, 0 * a)
    j = metric_source(L0, s, T5, RATE)
    j00, jii, j0i, jjk = j[S00], j[SII], j[S0I], j[SJK]
    uniform = all(len(set(x.tolist())) == 1 for x in (j00, *jii, *j0i, *jjk))
    say(
        f"  {name}: 00 slot {j00[0]}, diagonal {[x[0] for x in jii]}, 0i {[x[0] for x in j0i]}, "
        f"jk {[x[0] for x in jjk]}, the same at every site: {uniform};  4 rho = {j00[0] + 3 * jii[0][0]}, "
        f"4 p = {j00[0] - jii[0][0]}"
    )
# the turning round: the stride in +1, the stride out -1; and a speeding swing 6 then 8
for sb, sa in ((1, -1), (6, 8)):
    a = np.zeros((ROWS, n), dtype=object)
    a[A1ROWS] = 50
    b = a.copy()
    b[A1ROWS] = 50 - sb
    s = State(a, b, 0 * a, 0 * a)
    # the stride out is the one the gear takes; lay it by a push of the A1 gear's own: a spring-free source on it
    kick = terms([(UNIT, UNIT, UNIT, (sa - sb) * REST * DRIVE_M, A1ROWS[0])])
    j = metric_source(L0, s, join(T5, kick), RATE)
    say(
        f"  strides in {sb}, out {sa}: 00 slot {j[S00][0]} (sigma_b^2 + sigma_a^2; the product form 2 sb sa would be "
        f"{2 * sb * sa}), diagonal {j[SII[0]][0]}"
    )

# ------------------------------------------------------------------------------- 2. the 24 and the reversal on S
say(
    "\n== 2. S = sum C (v_b (x) v_b + v_a (x) v_a) under the 24 and under the reversal (one site, varied readings)"
)


def site_source(plan, R):
    J = [0] * ROWS
    for f, s_, t, c, g in zip(*(x.tolist() for x in plan), strict=True):
        J[g] += c * R[f] * R[s_] * R[t]
    return J


def site_readings(vals):
    """vals: per matter row (value, sigma_b, sigma_a, (D_x, D_y, D_z))."""
    R = [0] * (PLANES * ROWS + 1)
    R[UNIT] = 1
    for x, (v, sb, sa, d) in vals.items():
        R[at(VALUE, x)], R[at(SB, x)], R[at(SA, x)] = v, sb, sa
        for i in range(3):
            R[at(GRAD + i, x)] = d[i]
    return R


seq = Carry(7)
draw = lambda: int(seq.draw(-9, 10, (1,))[0])  # noqa: E731
vals = {x: (draw(), draw(), draw(), (draw(), draw(), draw())) for x in MATTER}
P5 = join(RATE, terms(gradient_part(1)), terms(potential(3)))
S = site_source(P5, site_readings(vals))
turns = [g for g in range(KINDS.t1.shape[0]) if (KINDS.t1[g] != 0).any()]
ok_turns = 0
for g in turns:
    m, rt, re = KINDS.t1[g], KINDS.t1[g], KINDS.e[g]
    turned = {}
    for rows, mat in ((T1ROWS, rt), (EROWS, re), (A1ROWS, np.ones((1, 1), dtype=object))):
        v = np.array([vals[x][0] for x in rows], dtype=object)
        sb = np.array([vals[x][1] for x in rows], dtype=object)
        sa = np.array([vals[x][2] for x in rows], dtype=object)
        d = np.array([vals[x][3] for x in rows], dtype=object)  # (components, axes)
        v2, sb2, sa2 = mat @ v, mat @ sb, mat @ sa
        d2 = mat @ d @ m.T  # components by the kind's matrix, axes by the turn
        for k, x in enumerate(rows):
            turned[x] = (v2[k], sb2[k], sa2[k], tuple(d2[k]))
    S2 = site_source(P5, site_readings(turned))
    want = (SQUARE[g] @ np.array(S[S00:], dtype=object)).tolist()
    ok_turns += S2[S00:] == want
say(f"  S on the turned readings = square(g) S on all {ok_turns} of {len(turns)} turns of the 24")
rev = {x: (v, -sa, -sb, d) for x, (v, sb, sa, d) in vals.items()}
S3 = site_source(P5, site_readings(rev))
tau = [1 - o - o for o in ODD]
say(
    f"  under the reversal (sigma_b, sigma_a) -> (-sigma_a, -sigma_b): S -> tau S with tau = {tau}:",
    S3[S00:] == [t * x for t, x in zip(tau, S[S00:], strict=True)],
)
say(
    f"  (rows' parity laid from the four-vector's reversal: odd slots {[METRIC[i] for i, o in enumerate(ODD) if o]})"
)

# ------------------------------------------------------------------- 3. candidate (ii): T even in the stride, unstaged
say(
    "\n== 3. candidate (ii): the metric reads the matter's stride at the now slot squared, unstaged (head's form)"
)
Ls = board_("none")
RATE_II = terms(rate_part(1, before=SB, after=SB))  # both slots read a - b: 2 sigma^2 and 2 sigma D
for parity in (False, True):
    states, k, rows = run(
        tick_head, mirror_head, Ls, lay(Carry(11), Ls), ROUNDS, NOW, RATE_II, parity=parity
    )
    say(f"  parity mirror {parity}: first round back that departs: {k}, rows departing there: {rows}")

# ------------------------------------------------------------------- 4. candidate (i): staged, head's form
say(
    "\n== 4. candidate (i): staged (the matter steps first, the metric reads sigma_b = a - b and sigma_a = a+ - a)"
)
for parity in (False, True):
    states, k, rows = run(
        tick_head, mirror_head, Ls, lay(Carry(12), Ls), ROUNDS, NOW, RATE, parity=parity
    )
    say(f"  standing clock, parity mirror {parity}: departs at round back {k}, rows {rows}")
for seed in (13, 14, 15):
    states, k, rows = run(tick_head, mirror_head, Ls, lay(Carry(seed), Ls), ROUNDS, NOW, RATE)
    say(
        f"  standing clock, parity mirror, lay {seed}: {ROUNDS} rounds forth and back exact: {k is None}; "
        f"the state moved: {not same(states[-1], states[0])}"
    )

# the moving clock: every row's teeth read the 00 slot, as the loader lays it
Lm = board_("every")
for seed in (16, 17):
    breaks, falls, wmin, wmax = [], [0], [None], [None]

    def watch(st, _b=breaks, _f=falls, _lo=wmin, _hi=wmax):
        w = step.weight(Lm.gearing, Lm.clock, st.a)
        wb = step.weight(Lm.gearing, Lm.clock, st.b)
        _b.append(
            int((st.r >= w).sum())
        )  # a kept tooth at or above the teeth of the round that reads it
        _f[0] += int((w < wb)[S00].sum())
        lo, hi = min(w.flat), max(w.flat)
        _lo[0] = lo if _lo[0] is None else min(_lo[0], lo)
        _hi[0] = hi if _hi[0] is None else max(_hi[0], hi)

    states, k, rows = run(
        tick_head, mirror_head, Lm, lay(Carry(seed), Lm), ROUNDS, NOW, RATE, watch=watch
    )
    first = next((t for t, x in enumerate(breaks) if x), None)
    say(
        f"  moving clock, lay {seed}: W in [{wmin[0]}, {wmax[0]}], {falls[0]} site-rounds where the clock fell; "
        f"rounds whose promise breaks (r >= W(a)): {sum(1 for x in breaks if x)}, the first at round {first}; "
        f"the run back departs at round back {k} (round {None if k is None else ROUNDS - k + 1} forth)"
    )

# ------------------------------------------------------------------- 5. candidate (iii): the first-order form
say(
    "\n== 5. candidate (iii): the first-order form, each rate in its own slot (p), mirror R = R_P o D^-1"
)
# (a) at a standing clock it is the staged head's act bit for bit: p = W (a - b) + r
s = lay(Carry(21), Ls)
t = lay(Carry(21), Ls, first=True)
agree = True
for _ in range(ROUNDS):
    s, t = tick_head(Ls, s, NOW, RATE), tick_first(Ls, t, NOW, RATE)
    w = step.weight(Ls.gearing, Ls.clock, s.b)
    agree &= same([s.a, w * (s.a - s.b) + s.r, s.rd], [t.a, t.b, t.rd])
say(
    f"  (a) standing clock: the first-order form equals the staged head's form for {ROUNDS} rounds: {agree}"
)
# (b) the clock moving: every row but the 00 row reads the 00 slot
Lf = board_("others")
for seed in (22, 23, 24, 25):
    falls, wmin, wmax, stride00, last = [0], [None], [None], [0, 0], [None]

    def watch(st, _f=falls, _lo=wmin, _hi=wmax, _s=stride00, _last=last):
        w = step.weight(Lf.gearing, Lf.clock, st.a)
        if _last[0] is not None:
            _f[0] += int((w < _last[0])[MATTER[0]].sum())
        _last[0] = w
        lo, hi = min(w.flat), max(w.flat)
        _lo[0] = lo if _lo[0] is None else min(_lo[0], lo)
        _hi[0] = hi if _hi[0] is None else max(_hi[0], hi)

    states, k, rows = run(
        tick_first, mirror_first, Lf, lay(Carry(seed), Lf, first=True), ROUNDS, NOW, RATE, watch=watch
    )
    big = max(abs(v) for x in states[-1] for v in np.asarray(x).flat)
    say(
        f"  (b) moving clock, lay {seed}: W in [{wmin[0]}, {wmax[0]}], {falls[0]} site-rounds where a matter clock "
        f"fell; {ROUNDS} rounds forth and back bit for bit: {k is None}; moved: {not same(states[-1], states[0])}; "
        f"largest count {big}"
    )
# the same with the uniform mirror: the 0i rows break it
states, k, rows = run(
    tick_first, mirror_first, Lf, lay(Carry(22), Lf, first=True), ROUNDS, NOW, RATE, parity=False
)
say(f"  (b') moving clock, the uniform mirror (no parity): departs at round back {k}, rows {rows}")
# (c) the 00 row reading its own count as teeth (the loader's lay) has no bijection in this form
R0, P = 2, 10
coll = [(x, x + carry(P, R0 + x, 0)[0]) for x in (1, 2)]
say(
    f"  (c) the 00 row's drift x -> x + p div (R + x) at R = {R0}, p = {P}: {coll[0][0]} -> {coll[0][1]} and "
    f"{coll[1][0]} -> {coll[1][1]}: two counts, one image"
)
states, k, rows = run(tick_first, mirror_first, Lm, lay(Carry(22), Lm, first=True), ROUNDS, NOW, RATE)
say(f"      run with the 00 row reading itself: departs at round back {k}, rows {rows}")

# ------------------------------------------------------------------- 6. the metric's self-push
say("\n== 6. the self-push: the metric reading its own rate, and its own gradient")
own_in = terms([(at(SB, m), at(SB, m), UNIT, 1, S00) for m in METRIC])
own_out = terms([(at(SA, m), at(SA, m), UNIT, 1, S00) for m in METRIC])
for name, extra in (
    ("its own stride into the now, squared", own_in),
    ("its own stride out (pass 1's)", own_out),
):
    states, k, rows = run(tick_head, mirror_head, Ls, lay(Carry(31), Ls), ROUNDS, NOW, join(RATE, extra))
    say(f"  head's form, {name}: departs at round back {k}, rows {rows}")
    states, k, rows = run(
        tick_first, mirror_first, Lf, lay(Carry(31), Lf, first=True), ROUNDS, NOW, join(RATE, extra)
    )
    say(f"  first-order form, {name}: departs at round back {k}, rows {rows}")
GSELF = join(NOW, terms(metric_gradient_selfpush(1)))
states, k, rows = run(tick_head, mirror_head, Ls, lay(Carry(32), Ls), ROUNDS, GSELF, RATE)
say(f"  head's form, its own gradient at the now slot (ii, jk): exact {ROUNDS} rounds: {k is None}")
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(32), Lf, first=True), ROUNDS, GSELF, RATE)
say(f"  first-order form, its own gradient, the clock moving: exact {ROUNDS} rounds: {k is None}")

# ------------------------------------------------------------------- 7. locality: one Mesh a round
say("\n== 7. locality: the staged act at a site reads its own gears and its six neighbours' alone")
for name, tick, first in (("head's form", tick_head, False), ("first-order form", tick_first, True)):
    Lx = Ls if not first else Lf
    base = lay(Carry(41), Lx, first=first)
    out = tick(Lx, base, NOW, RATE)
    nb = Lx.nb
    held = True
    for site in (0, 17, 59):
        near = set([site, *nb[:, site].tolist()])
        far = np.array([j not in near for j in range(nb.shape[1])])
        fresh = lay(Carry(42 + site), Lx, first=first)
        mixed = State(*(np.where(far[None, :], f, x) for f, x in zip(fresh, base, strict=True)))
        got = tick(Lx, mixed, NOW, RATE)
        held &= all(np.array_equal(g[:, site], o[:, site]) for g, o in zip(got, out, strict=True))
    say(f"  {name}: every site's new state unchanged by every count beyond its six neighbours: {held}")

(Path(__file__).resolve().parent / "n2_results.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
