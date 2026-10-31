"""The miracle's clicks (the owner's word of about 09:05 UTC; the Boss's 6541517655 item 2.1): road B's round (MIRACLE_B,
frozen 0e034a76, and MIRACLE_B2 33345ba9: the tied family first by the engine's own act, then every held row on its
edges' own dials W(a) + W(a') + g_e, g_e = SUM f o(start) o(end) over the monomials holding it twice, its push
-(g_in + g_out) a) on node-all 9d75a4904's act, with term 11 reading the step's own exchange (VARY5's physicist, B2:
"removed" needs the step exact and term 11 reading that step's own exchange):
  - on every monomial holding a held row twice beside a tied row twice, (f; o, o, h, h), the exact exchange
    P = f h^2 o (o+ - o-) at the now slot over the window (b, a, a+), taken by the held side and given by the tied
    (MIRACLE_B 4.4), in the sides' units: kappa / two times four, as the act's own two-leg passing is;
  - every other term the act's own passing, the work form J_i(a) (a+ - b) by David's weights, exact for the two-leg
    monomials under the tied leapfrog; the Mesh edges the act's own crossing.
Every side carries its passing at the edge key by Rule3's carry into its own click tooth, as the act does.
Readings, each round:
  - the identity: E32 = 32 W E changes by exactly the teeth's share (a check by construction, MIRACLE_B2 4.1);
  - the sides' books, a check by construction read through the teeth (the MIRACLE pair's B1; first named "the books in
    the clicks"): each clock's (train's) change of E32 times kappa / two equals 8 W times what its sides carried (the
    key times its clicks plus its click teeth's change) plus its teeth's share times kappa / two, at every clock and
    round;
  - beside it, the act's own passing on the same window (the two-leg work form on every term): its running residual at
    one clock, in keys;
  - the whole clicks by train; the walk (the largest held square per window); the run back from the end state alone,
    board and click teeth (the engine's mirror, the same round, the mirror).
Usage: python3 -I clicks.py <node-all src> <universe> <piece> <setting> [rounds, 600 unless given] [every, 100]
       [engine: the present act instead, for its walk and run back beside road B's; the identity and the books are
       road B's and are not read then] [square: every two-leg form f x_r x_p read as its own square (f / 2)(x_r + x_p)^2,
       its own monomials (f / 2) x_r^2 and (f / 2) x_p^2 joined to J's potential (the breakthrough's check)]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Plan, State  # noqa: E402
from tensor24.runner import load as loadmod  # noqa: E402
from tensor24.runner import plans  # noqa: E402
from tensor24.runner.files import sites_of, star  # noqa: E402

universe, piece, setting = (json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[2:5])
ROUNDS = int(sys.argv[5]) if len(sys.argv) > 5 else 600
EVERY = int(sys.argv[6]) if len(sys.argv) > 6 else 100
ENGINE = "engine" in sys.argv[7:]
SQUARE = "square" in sys.argv[7:]  # every two-leg form read as its own square (the breakthrough's check)
shape = piece["shape"]
kinds, tables, square, lifted = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, tables, square, lifted)
assert found == [], found
if SQUARE:
    # each two-leg monomial f x_r x_p on two tied rows read as its own square, (f / 2)(x_r + x_p)^2: its own
    # monomials (f / 2) x_r^2 and (f / 2) x_p^2 join it, so every form of J's potential is a square of its legs' value
    _, row_of, _, _, _ = plans.rows_of(loaded.trains)
    held_rows = {r for r in range(len(row_of)) if int(loaded.trains.held[row_of[r]])}
    f0, legs0 = loaded.potential
    fs, ls = [int(x) for x in f0], [[int(x) for x in lg] for lg in legs0]
    for i in range(len(fs)):
        rows4 = [ls[j][i] for j in range(4)]
        two = [x for x in rows4 if x >= 0]
        if fs[i] == 0 or len(two) != 2 or two[0] == two[1] or set(two) & held_rows:
            continue
        half_f, odd = carry(fs[i], 2, 0)
        assert odd == 0, ("a two-leg form with an odd factor", fs[i])
        for r in two:
            fs.append(half_f)
            for j, x in enumerate((r, r, -1, -1)):
                ls[j].append(x)
    leg_type = np.asarray(legs0[0]).dtype
    squared = (np.array(fs, dtype=object), tuple(np.array(lg, dtype=leg_type) for lg in ls))
    # term 11 on the edges laid again from the squared potential by the loader's own edging (an own monomial joins
    # no two trains, so it weighs onto no side: its spring stays in its clock)
    loaded = loaded._replace(potential=squared,
                             click=loadmod.edging(loaded.trains, squared, universe["chosen"]["key"], star(len(shape))))
layout = tmain.layout(universe, shape, loaded)
nb, spokes, meshes, grip0, gearing, plan, clock, stretch, click, push, mesh = layout
held_t = [int(x) for x in loaded.trains.held].index(1)
_, of, _, _, _ = plans.rows_of(loaded.trains)
rows = len(of)
H = np.array([r for r in range(rows) if of[r] == held_t], dtype=np.intp)
inH = set(H.tolist())
factor, legs = loaded.potential
legs = np.stack(legs, axis=1).astype(np.intp)
GR, GF, GO, TF, TO1, TO2 = [], [], [], [], [], []
for f, lg in zip(factor, legs):
    if int(f) == 0:
        continue
    lg = [int(x) for x in lg]
    hl = [x for x in lg if x >= 0 and x in inH]
    tl = [x for x in lg if x >= 0 and x not in inH]
    assert len(tl) <= 2, ("a monomial with more than two legs off the held train", lg)
    if hl:
        assert len(hl) == 2 and hl[0] == hl[1], ("a held row not held exactly twice", lg)
        o = list(lg)
        o.remove(hl[0])
        o.remove(hl[0])
        assert o[0] == o[1], ("a held-twice monomial with two unlike other legs", lg)
        GR.append(hl[0])
        GF.append(int(f))
        GO.append(o[0])
    else:
        assert len(tl) == 2, ("a monomial on the tied family alone with a unit leg", lg)
        TF.append(int(f))
        TO1.append(tl[0])
        TO2.append(tl[1])
GR, GO, TO1, TO2 = (np.array(x, dtype=np.intp) for x in (GR, GO, TO1, TO2))
GF, TF = np.array(GF, dtype=object)[:, None], np.array(TF, dtype=object)[:, None]
rest, strch, kick, drive, parity = gearing
assert not np.asarray(push.factor).any(), "the metric's push is on: its read of the held rows is not covered"
assert not np.asarray(mesh.factor).any(), "the gradient vertex is on"
assert set(np.asarray(strch).ravel().tolist()) == {1} and set(np.asarray(kick).ravel().tolist()) == {1}
W = int(np.asarray(rest).ravel()[0])
assert set(np.asarray(rest).ravel().tolist()) == {W}, "the rest teeth differ between rows"
senses = step.halves(layout)
FOUR_W = senses * senses * W
KEY = int(universe["chosen"]["key"])
half_kappa, left = carry(int(np.asarray(click.key).ravel()[0]), KEY, 0)
assert left == 0
SCALE = senses * senses * half_kappa  # the exchange in E units to the sides' units: kappa / two times four
XG = [i for i in range(len(GR)) if int(GO[i]) >= 0]  # the four-leg ties: a held row twice beside a tied row twice
XR, XF, XO = GR[XG], GF[XG], GO[XG]
TR = np.array(of, dtype=np.intp)
NTR = len(loaded.trains)

# the plan's terms that touch no held row: the act's own passing for them (the two-leg monomials on the tied family)
legs_p, factor_p, target_p = plan
touch = np.zeros(len(target_p), dtype=bool)
for i in range(len(target_p)):
    touch[i] = int(target_p[i]) in inH or any(int(x) in inH for x in np.asarray(legs_p)[:, i] if int(x) >= 0)
PLAN_T = Plan(legs_p, np.array([0 if touch[i] else factor_p[i] for i in range(len(target_p))], dtype=object), target_p)


def gco(x, y):
    """g on every held row: SUM f o(x) o(y) over the monomials holding it twice, the unit read as 1; 0 elsewhere."""
    vx, vy = step.valued(x), step.valued(y)
    g = 0 * x
    np.add.at(g, GR, GF * vx[GO] * vy[GO])
    return g


def exchange(b, a, a1):
    """Every side's exact exchange of the four-leg ties over the window, in the sides' units, (trains x trains, sites):
    P = f h^2 o (o+ - o-) taken by the held side (h, t) and given by the tied side (t, h)."""
    p = SCALE * XF * a[XR] * a[XR] * a[XO] * (a1[XO] - b[XO])
    sides = np.zeros((NTR * NTR, a.shape[-1]), dtype=object)
    np.add.at(sides, TR[XR] * NTR + TR[XO], p)
    np.add.at(sides, TR[XO] * NTR + TR[XR], -p)
    return sides


def passed_by(b, a, a1, own):
    """Every side's passing at every reach: the four-leg ties' exact exchange beside the act's own passing on the rest
    (own=True), or the act's own passing on every term (own=False)."""
    if own:
        here = step.passing(click, PLAN_T, b, a, a1) + exchange(b, a, a1)
    else:
        here = step.passing(click, plan, b, a, a1)
    return np.concatenate((here, step.crossing(click, nb, b, a, a1)))


def round_(s):
    """Road B's round on node-all's act: the tied family by the act, then the held rows on their edges' own dials; the
    sides carry the step's own exchange at the edge key."""
    a, b, tooth, rd, k = s
    eng, _ = step.act(layout, s)
    g_in, g_out = gco(b, a), gco(a, eng.a)
    wa, wb = step.dials(layout, s)
    w1 = step.weight(gearing, clock, eng.a)
    h1, _, hs = step.gear(a, b, tooth, wa + wb + g_in, wa + w1 + g_out, -(g_in + g_out) * a, senses)
    a1, s1 = eng.a.copy(), eng.r.copy()
    a1[H], s1[H] = h1[H], hs[H]
    clicks, k1 = carry(passed_by(b, a, a1, True), click.key, k)
    return State(a1, a.copy(), s1, eng.rd, k1), clicks


if ENGINE:

    def round_(s):  # noqa: F811  the present act, for its walk and run back
        return step.act(layout, s)



def by_train(x):
    out = np.zeros((NTR, x.shape[1]), dtype=object)
    np.add.at(out, TR, x)
    return out


def e32_clocks(s):
    """E32 by clock: each row's kinetic, the held rows' whole edge energy, each two-leg monomial's polarized potential
    half to each leg; the Meshes' polarized energy must stand at 0 on the lay read (asserted)."""
    a, b = s.a, s.b
    d = a - b
    g = gco(b, a)
    per = 16 * W * W * d * d + 16 * W * g * (a * a + b * b) + 4 * g * g * (a + b) * (a + b)
    va, vb = step.valued(a), step.valued(b)
    half = 8 * W * TF * (vb[TO1] * va[TO2] + va[TO1] * vb[TO2])
    np.add.at(per, TO1, half)
    np.add.at(per, TO2, half)
    return by_train(per)


def share_clocks(s, s1):
    """Each clock's teeth's share: SUM over its rows (s - s+)(4 W (a+ - b) + 2 g_out (a + a+) - 2 g_in (a + b))."""
    a, b, a1 = s.a, s.b, s1.a
    g_in, g_out = gco(b, a), gco(a, a1)
    return by_train((s.r - s1.r) * (FOUR_W * (a1 - b) + 2 * g_out * (a + a1) - 2 * g_in * (a + b)))


def own_sides(x):
    """A side array's sum per clock at its own Node-clock and across every Spoke: (trains, sites)."""
    per = x.reshape(-1, NTR, NTR, x.shape[-1]).sum(axis=0)
    return per.sum(axis=1)


def same(x, y):
    return all(np.array_equal(p, q) for p, q in zip(x, y))


s0 = State(*loaded.state)
s = s0
e_lay = e32_clocks(s)
assert int(abs(step.crossing(click, nb, s.b, s.a, s.a)).sum()) == 0
misses_identity, misses_books, widest, run_res, worst_res = 0, 0, 0, 0 * e_lay, 0
sum_share, sum_carried = 0 * e_lay, 0 * e_lay  # each clock's running teeth's share and running booked exchange
clicks_by = np.zeros(NTR, dtype=object)
walk, window_max, past32 = [], 0, 0  # past32: the first round a count passes 32 bits
print(f"{'the present act' if ENGINE else 'road B'} on node-all"
      f"{'' if ENGINE else ', the sides reading the step' + chr(39) + 's own exchange'}"
      f"{', every two-leg form its own square' if SQUARE else ''}:"
      f" rows {rows} (held {H.tolist()}), sites"
      f" {s.a.shape[-1]}, W {W}, the sides' key {KEY} x {half_kappa}, four-leg ties {len(XG)}", flush=True)
for n in range(1, ROUNDS + 1):
    s1, q = round_(s)
    if ENGINE:
        widest = max(widest, max(int(abs(x)).bit_length() for x in s1.a.ravel()))
        window_max = max(window_max, int((s1.a[H] * s1.a[H]).sum(axis=0).max()))
        if carry(n, EVERY, 0)[1] == 0:
            walk.append((n, window_max))
            window_max = 0
        s = s1
        continue
    e0, e1 = e32_clocks(s), e32_clocks(s1)
    sh = share_clocks(s, s1)
    if int((e1 - e0).sum()) != int(sh.sum()):
        misses_identity += 1
    carried = own_sides(click.key * q + s1.k - s.k)  # what each clock's sides carried: key x clicks + teeth's change
    lhs = half_kappa * (e1 - e0)
    rhs = 8 * W * carried + half_kappa * sh
    misses_books += int((lhs != rhs).sum())
    sum_share, sum_carried = sum_share + half_kappa * sh, sum_carried + 8 * W * carried
    act_sides = own_sides(passed_by(s.b, s.a, s1.a, False))
    run_res = run_res + (8 * W * own_sides(passed_by(s.b, s.a, s1.a, True)) - 8 * W * act_sides)
    worst_res = max(worst_res, int(abs(run_res).max()))
    per_train = abs(q).reshape(-1, NTR, NTR, q.shape[-1]).sum(axis=(0, 2, 3))
    clicks_by = clicks_by + per_train
    widest = max(widest, max(int(abs(x)).bit_length() for x in s1.a.ravel()))
    past32 = past32 or (n if widest > 32 else 0)
    window_max = max(window_max, int((s1.a[H] * s1.a[H]).sum(axis=0).max()))
    if carry(n, EVERY, 0)[1] == 0:
        walk.append((n, window_max))
        window_max = 0
    s = s1
key_e32 = 8 * W * KEY * half_kappa  # one key at a side in E32 units times kappa / two
kres, _ = carry(worst_res, key_e32, 0)
print(f"rounds {ROUNDS} ({'the present act' if ENGINE else 'road B'}); widest count {widest} bits; a count first past"
      f" 32 bits at round {past32 or 'none'}", flush=True)
if ENGINE:
    print("the identity, the sides' books and the clicks by train: not read under the present act (road B's)",
          flush=True)
else:
    print(f"the identity (E32's change = the teeth's share) missed in {misses_identity} of {ROUNDS} rounds", flush=True)
    print(f"the sides' books, by construction (each clock's change = its sides' key x clicks + click teeth's change"
          f" + its teeth's"
          f" share) missed at {misses_books} of {ROUNDS * NTR * s.a.shape[-1]} clock-rounds", flush=True)
    print(f"the act's own passing beside the step's exchange: its running residual at one clock reaches {kres} keys",
          flush=True)
    print(f"whole clicks |q| by train: {clicks_by.tolist()}", flush=True)
if not ENGINE:
    # what each clock's energy gained over the run, split by the identity: the booked exchanges (the clicks) and the
    # teeth's share (no click), in the clock's own energy at the lay (permille), per Node-clock 0
    for t in range(NTR):
        lay_t = int(half_kappa * e_lay[t, 0])
        if lay_t:
            got_b, _ = carry(1000 * int(sum_carried[t, 0]), lay_t, 0)
            got_s, _ = carry(1000 * int(sum_share[t, 0]), lay_t, 0)
            print(f"  train {t}: over the run its energy gained {got_b + got_s} permille of its own at the lay:"
                  f" {got_b} by its booked exchanges (the clicks), {got_s} by its teeth's share", flush=True)
print(f"the walk, the largest held square per {EVERY} rounds: {walk}", flush=True)
# the run back from the end state alone: the engine's mirror, the same round, the mirror; board and click teeth
back = step.mirror(layout, s)
for _ in range(ROUNDS):
    back, _ = round_(back)
back = step.mirror(layout, back)
print(f"the run back from the end state alone over {ROUNDS} rounds, board and click teeth: {same(back, s0)}", flush=True)
# the 24 (node-all's own tests/frame.py, as its run test reads them): each turn of the lay, run TURNS rounds, against
# the run turned, board and clicks
sys.path.insert(0, str(Path(sys.argv[1]).resolve().parent))
from tests import frame  # noqa: E402

TURNS, alike, turned = 8, 0, 0
for m in frame.turns():
    turned += 1
    u, v, ok = frame.turned_by(m, layout, loaded, s0, shape), s0, True
    for _ in range(TURNS):
        u1, qu = round_(u)
        v1, qv = round_(v)
        ok = ok and frame.same(u1, frame.turned_by(m, layout, loaded, v1, shape))
        ok = ok and frame.same([qu], [frame.turned_by(m, layout, loaded, v1._replace(k=qv), shape).k])
        u, v = u1, v1
    alike += 1 if ok else 0
print(f"the 24: the round and its clicks turned alike in {alike} of {turned} turns over {TURNS} rounds", flush=True)
