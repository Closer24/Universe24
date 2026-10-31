"""MIRACLE_B probe: road B, each edge's own dial, in the gears as they are (a gear's now, its before and one tooth per
edge: no third count, no second tooth). Families from the structure: H the held train's rows (its character, the
loader's flag), T every other row.
The round ("bedge"): T steps first by the engine's own act, unchanged (dial W(a) + W(a+), push at the now slot); then
every H row steps by the gear's own split on dials that are its edges' own,
  d = W(a) + W(a') + g_e,   g_e = SUM over the live monomials holding the row twice of f o1(start) o2(end),
the coefficient of the row's own square in V with its two other legs (T's rows or the unit) read at the edge's two
ends: the in-edge (b, a) at T's before and now, the out-edge (a, a+) at T's now and T's next count, given since T
stepped first; and the push -(g_in + g_out) a, the two edges' coefficients summed (the difference quotient's).
"engine": the engine's own act, for the same readings.
Readings: E32 = 32 W E, the whole polynomial the step's equation keeps when nothing rounds, and its change each round
against the exact whole-number identity dE32 = SUM (s - s+)(4 W (a+ - b) + 2 g_out (a + a+) - 2 g_in (a + b)) (g = 0 on
T rows); the widest count; T's curvature (its explicit window) and H's g in permille of 4W; the clicks; the run back
from the end state alone (the engine's mirror, the same act N times, the mirror); the 24 over a prefix (the run test's
own turned()); the hidden twin (one click tooth one unit apart at one clock: the board alike, the clicks apart only
there). Whole numbers only; Rule3's carry the one division.
Usage: python3 -I b_edge.py <universe> <piece> <setting> [rounds=N] [mode=bedge|engine] [every=N] [turns=N]
       [twin=N] [noback]"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("tree")))
sys.path.insert(0, str(HERE.joinpath("tree", "src")))
sys.set_int_max_str_digits(0)
import numpy as np
from tensor24 import main as tmain
from tensor24.algebra.carry import carry
from tensor24.engine import step
from tensor24.engine.contract import contract
from tensor24.engine.mesh import held as grips_at, stretches
from tensor24.engine.state import State
from tensor24.runner import load as loadmod, plans
from tensor24.runner.files import sites_of, star

opts = dict(x.split("=") for x in sys.argv[4:] if "=" in x)
MODE = opts.get("mode", "bedge")
paths = [Path(p) for p in sys.argv[1:4]]
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
assert found == [], found
layout = tmain.layout(universe, shape, loaded)
nb, spokes, meshes, grip0, gearing, plan, clock, stretch, click, push, mesh = layout
heldflag = [int(x) for x in loaded.trains.held]
assert sum(heldflag) == 1, ("one held train by its character", heldflag)
held_t = heldflag.index(1)
_, of, _, _, _ = plans.rows_of(loaded.trains)
rows = len(of)
H = np.array([r for r in range(rows) if of[r] == held_t], dtype=np.intp)
T = np.array([r for r in range(rows) if of[r] != held_t], dtype=np.intp)
inH = set(H.tolist())
# the live monomials, read by the structure
factor, legs = loaded.potential
legs = np.stack(legs, axis=1).astype(np.intp)
GR, GF, GO1, GO2, TF, TO1, TO2 = [], [], [], [], [], [], []
for f, lg in zip(factor, legs):
    if int(f) == 0:
        continue
    lg = [int(x) for x in lg]
    hl = [x for x in lg if x >= 0 and x in inH]
    tl = [x for x in lg if x >= 0 and x not in inH]
    assert len(tl) <= 2, ("a monomial with more than two legs off the held train: T's potential not quadratic", lg)
    if hl:
        assert len(hl) == 2 and hl[0] == hl[1], ("a held row not held exactly twice", lg)
        o = list(lg); o.remove(hl[0]); o.remove(hl[0])
        GR.append(hl[0]); GF.append(int(f)); GO1.append(o[0]); GO2.append(o[1])
    else:
        o = tl + [-1] * (2 - len(tl))
        TF.append(int(f)); TO1.append(o[0]); TO2.append(o[1])
GR, GO1, GO2, TO1, TO2 = (np.array(x, dtype=np.intp) for x in (GR, GO1, GO2, TO1, TO2))
assert all(x == y for x, y in zip(GO1, GO2)), "a monomial holding a held row twice with two unlike other legs: g not symmetric per monomial"
GF, TF = np.array(GF, dtype=object)[:, None], np.array(TF, dtype=object)[:, None]
rest, strch, kick, drive, parity = gearing
assert not np.asarray(push.factor).any(), "the metric's push is not at factor 0: its read of the held rows' momenta is not covered"
assert not np.asarray(mesh.factor).any(), "the gradient vertex is not at factor 0"
assert set(np.asarray(strch).ravel().tolist()) == {1} and set(np.asarray(kick).ravel().tolist()) == {1}
pushed = sorted(set(GR.tolist()) | set(x for x in np.concatenate((TO1, TO2)).tolist() if x >= 0) | set(GO1.tolist()) | set(GO2.tolist()))
assert all(int(np.broadcast_to(drive, (rows, 1))[r, 0]) == 1 for r in pushed if r >= 0), "a pushed row off the force's path"
W = int(np.asarray(rest).ravel()[0])
assert set(np.asarray(rest).ravel().tolist()) == {W}
senses = step.halves(layout)
FOUR_W = senses * senses * W


def gco(x, y):
    """g on every held row: SUM f o1(x) o2(y) over the monomials holding it twice (the unit read as 1); 0 elsewhere."""
    vx, vy = step.valued(x), step.valued(y)
    g = 0 * x
    np.add.at(g, GR, GF * vx[GO1] * vy[GO2])
    return g


ORIG_ACT = step.act
# the plan of the held-twice monomials' pushes landing on their held legs (laid once, as the loader lays a plan)
from tensor24.engine.contract import pushes
_gl = [lg for f, lg in zip(factor, legs) if int(f) != 0 and any(int(x) in inH for x in lg if int(x) >= 0)]
_gf = [int(f) for f, lg in zip(factor, legs) if int(f) != 0 and any(int(x) in inH for x in lg if int(x) >= 0)]
_gp = pushes(np.array(_gf, dtype=object), tuple(np.array([int(lg[i]) for lg in _gl], dtype=np.intp) for i in range(4)))
_keep = np.array([int(x) in inH for x in _gp.target], dtype=bool)
from tensor24.engine.state import Plan
GPLAN = Plan(_gp.first[_keep], _gp.second[_keep], _gp.third[_keep], _gp.factor[_keep], _gp.target[_keep])


def bedge(layout, s):
    a, b, tooth, rd, k = s
    eng, _ = ORIG_ACT(layout, s)  # T's step, the engine's own; its held rows are discarded below
    _, _, _, _, gear_, plan_, clock_, _, click_, _, _ = layout
    g_in, g_out = gco(b, a), gco(a, eng.a)
    wa, wb = step.dials(layout, s)
    w1 = step.weight(gear_, clock_, eng.a)  # the 00 row's next count is T's, given
    h1, _, hs = step.gear(a, b, tooth, wa + wb + g_in, wa + w1 + g_out, -(g_in + g_out) * a, senses)
    a1, s1 = eng.a.copy(), eng.r.copy()
    a1[H], s1[H] = h1[H], hs[H]
    jb, ja, ja1 = (contract(plan_, step.valued(v), v) for v in (b, a, a1))
    moved = step.passing(click_, a, b, ja, jb) + step.passing(click_, a1, a, ja1, ja)
    clicks, k1 = carry(moved, click_.key, k)
    return State(a1, a.copy(), s1, eng.rd, k1), clicks


def uniform(layout, s):
    """The same round with no row selected: every row's edge gains g (0 off the held rows, whose plan holds no other
    row twice beside held legs) and every row's push gains (2 g(a, a) - g(b, a) - g(a, a')) a, a' the count the split
    gives at the engine's own dials, exact for every row whose dial reads no held row (as the engine's own 00 row)."""
    a, b, tooth, rd, k = s
    _, _, _, _, gear_, plan_, clock_, _, click_, _, _ = layout
    force, j1 = step.sources(layout, a)
    _, _, _, teeth, _ = gear_
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(layout, s, step.driven(gear_, force, step.kick(gear_, first)))
    q, kept = step.drive(j, teeth, rd)
    push_ = step.driven(gear_, force, step.kick(gear_, q))
    wa, wb = step.dials(layout, s)
    first, _, _ = step.gear(a, b, tooth, wa + wb, wa + wb, push_, senses)
    w1 = step.weight(gear_, clock_, first)
    given, _, _ = step.gear(a, b, tooth, wa + wb, wa + w1, push_, senses)  # the engine's own next count
    g_in, g_out = gco(b, a), gco(a, given)
    # the held-twice monomials' pushes on their held legs, by the vertex law, taken out of J and read on the two edges
    held_legs = contract(GPLAN, step.valued(a), a)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb + g_in, wa + w1 + g_out, push_ - held_legs - (g_in + g_out) * a, senses)
    jb, ja, ja1 = (contract(plan_, step.valued(v), v) for v in (b, a, a1))
    moved = step.passing(click_, a, b, ja, jb) + step.passing(click_, a1, a, ja1, ja)
    clicks, k1 = carry(moved, click_.key, k)
    return State(a1, b1, s1, kept, k1), clicks


if MODE == "bedge":
    step.act = bedge
if MODE == "uniform":
    step.act = uniform
    MODE = "bedge"  # the same readings and the same identity


def E32(s):
    """32 W E: SUM over H rows of 16 W^2 (a - b)^2 + 16 W g (a^2 + b^2) + 4 g^2 (a + b)^2, g on the edge (b, a); over T rows
    16 W^2 (a - b)^2; T's own monomials polarized, 16 W f (o1(b) o2(a) + o1(a) o2(b)); the Meshes polarized,
    8 W SUM grip stretch(b) stretch(a). Returns (total, H part, T part)."""
    a, b = s.a, s.b
    d = a - b
    g = gco(b, a)
    kin = 16 * W * W * d * d
    eh = (kin[H] + 16 * W * g[H] * (a[H] * a[H] + b[H] * b[H]) + 4 * g[H] * g[H] * (a[H] + b[H]) * (a[H] + b[H])).sum()
    va, vb = step.valued(a), step.valued(b)
    et = kin[T].sum() + (16 * W * TF * (vb[TO1] * va[TO2] + va[TO1] * vb[TO2])).sum()
    gr = grips_at(layout, a)
    assert np.array_equal(gr, grips_at(layout, b)), "a grip moved: the Meshes' polarized energy is not covered"
    et = et + (8 * W * gr * stretches(layout, b) * stretches(layout, a)).sum()
    return int(eh + et), int(eh), int(et)


def predicted(s, s1):
    """The exact whole-number change of E32 over the round s -> s1: SUM (s - s+)(4W (a+ - b) + 2 g_out (a + a+) - 2 g_in (a + b))."""
    a, b, a1 = s.a, s.b, s1.a
    g_in, g_out = gco(b, a), gco(a, a1)
    return int(((s.r - s1.r) * (FOUR_W * (a1 - b) + 2 * g_out * (a + a1) - 2 * g_in * (a + b))).sum())


def shares(s, s1):
    """The teeth's share split by family: (on the held rows, on the others)."""
    a, b, a1 = s.a, s.b, s1.a
    g_in, g_out = gco(b, a), gco(a, a1)
    w = (s.r - s1.r) * (FOUR_W * (a1 - b) + 2 * g_out * (a + a1) - 2 * g_in * (a + b))
    return int(w[H].sum()), int(w[T].sum())


TR = np.array(of, dtype=np.intp)
NTR = len(loaded.trains)
XG = [i for i in range(len(GR)) if int(GO1[i]) >= 0]  # the four-leg ties: a held row twice beside a tied row twice
XR, XF, XO = GR[XG], GF[XG], GO1[XG]
assert all(int(x) >= 0 and int(y) >= 0 for x, y in zip(TO1, TO2)), "a monomial on T alone with a unit leg: not booked here"


def by_train(x):
    out = np.zeros((NTR, x.shape[1]), dtype=object)
    np.add.at(out, TR, x)
    return out


def E32_clocks(s):
    """E32 by clock (train, Node-clock): each row's kinetic, the held rows' whole edge energy (the four-leg tie's
    potential inside it), each two-leg monomial's polarized potential half to each leg, each Mesh half to each end."""
    a, b = s.a, s.b
    d = a - b
    g = gco(b, a)
    per = 16 * W * W * d * d + 16 * W * g * (a * a + b * b) + 4 * g * g * (a + b) * (a + b)
    va, vb = step.valued(a), step.valued(b)
    half = 8 * W * TF * (vb[TO1] * va[TO2] + va[TO1] * vb[TO2])
    np.add.at(per, TO1, half)
    np.add.at(per, TO2, half)
    per = per + (8 * W * grips_at(layout, a) * stretches(layout, b) * stretches(layout, a)).sum(axis=1)
    return by_train(per)


def booked(s, s1):
    """Each clock's exchanges over the round (b, a, a+), in E32 units, and the same in the passing's units (E32 = 8 W S):
    the four-leg tie, P = f k(a)^2 o(a)(o(a+) - o(b)), to the held leg's clock, -P from the tied leg's; each two-leg
    monomial, f (C(b, a) + C(a, a+)), C(u, v) = x(u) y(v) - x(v) y(u), to its first leg's clock, its negative from its
    second's. Returns (E32 units, passing units), both (trains, sites)."""
    a, b, a1 = s.a, s.b, s1.a
    p4 = XF * a[XR] * a[XR] * a[XO] * (a1[XO] - b[XO])
    x0, x1, xp, y0, y1, yp = b[TO1], a[TO1], a1[TO1], b[TO2], a[TO2], a1[TO2]
    p2 = TF * ((x0 * y1 - x1 * y0) + (x1 * yp - xp * y1))
    rows_s = 0 * a
    np.add.at(rows_s, XR, 4 * p4)
    np.add.at(rows_s, XO, -4 * p4)
    np.add.at(rows_s, TO1, p2)
    np.add.at(rows_s, TO2, -p2)
    sS = by_train(rows_s)
    return 8 * W * sS, sS


def share_clocks(s, s1):
    a, b, a1 = s.a, s.b, s1.a
    g_in, g_out = gco(b, a), gco(a, a1)
    return by_train((s.r - s1.r) * (FOUR_W * (a1 - b) + 2 * g_out * (a + a1) - 2 * g_in * (a + b)))


def engine_passing(s, s1):
    """The act's term 11 passing on the same window, X(a, b) + X(a+, a), the two-leg form on every monomial."""
    jb, ja, ja1 = (contract(plan, step.valued(v), v) for v in (s.b, s.a, s1.a))
    return step.passing(click, s.a, s.b, ja, jb) + step.passing(click, s1.a, s.a, ja1, ja)


# T's curvature from the monomials holding a T row twice (2 f times the other legs at a), and H's 2 g_out, in permille
# of 4W (the explicit step's window is T's; H's dial holds its own)
TK_R, TK_C, TK_O1, TK_O2 = [], [], [], []
for f, lg in zip(factor, legs):
    if int(f) == 0:
        continue
    lg = [int(x) for x in lg]
    for r in sorted(set(x for x in lg if x >= 0 and x not in inH)):
        if lg.count(r) == 2:
            o = list(lg); o.remove(r); o.remove(r)
            TK_R.append(r); TK_C.append(2 * int(f)); TK_O1.append(o[0]); TK_O2.append(o[1])
TK_R, TK_O1, TK_O2 = (np.array(x, dtype=np.intp) for x in (TK_R, TK_O1, TK_O2))
TK_C = np.array(TK_C, dtype=object)[:, None]


def permilles(s, s1):
    v = step.valued(s.a)
    kt = 0 * s.a
    if len(TK_R):
        np.add.at(kt, TK_R, TK_C * v[TK_O1] * v[TK_O2])
    pt, _ = carry(1000 * kt, FOUR_W, 0)
    ph, _ = carry(1000 * 2 * gco(s.a, s1.a), FOUR_W, 0)
    return int(pt[T].max()), int(ph[H].max())


def wide(s):
    return max(int(abs(int(x))).bit_length() for x in np.concatenate((s.a.ravel(), s.b.ravel())))


def same(x, y):
    return all(np.array_equal(p, q) for p, q in zip(x, y))


s0 = State(*loaded.state)
ticks = int(opts.get("rounds", setting["ticks"]))
every = int(opts.get("every", 250))
assert all(np.array_equal(w, rest + 0 * s0.a) for w in step.dials(layout, s0)), "the teeth are not at rest"
force0, j0 = step.sources(layout, s0.a)
assert np.array_equal(j0[H], -2 * gco(s0.a, s0.a)[H] * s0.a[H]) and not np.asarray(force0[H]).any(), "the held rows' push is not -2 g a"
e0, eh0, et0 = E32(s0)
print(f"{MODE}: rows {rows} (held {H.tolist()}), sites {s0.a.shape[1]}, W {W}, live monomials: {len(GR)} holding a held row twice, {len(TF)} on T alone", flush=True)
print(f"E32 at the lay {e0} (held {eh0}, other {et0})", flush=True)
s, ok_id, first_off, emin, emax, wmax, ptop, htop = s0, 0, None, e0, e0, wide(s0), (0, 0), (0, 0)
clicks_abs = [0] * len(loaded.trains)
twin_n = int(opts.get("twin", 0))
if twin_n:
    k2 = s0.k.copy()
    k2[held_t, 0] = k2[held_t, 0] + 1  # one hidden unit in one click tooth at one clock
    twin, twin_board, twin_clicks_apart, twin_elsewhere = State(s0.a, s0.b, s0.r, s0.rd, k2), 0, 0, 0
at = 0
SHARES, cum_h, cum_t = "shares" in sys.argv, 0, 0
BOOKS = "books" in sys.argv
DIAL, dial_min = "dial" in sys.argv, (None, 0)
bk_miss, bk_places, bk_legs, bk_run, bk_top, bk_englegs, bk_exact_top = 0, 0, 0, 0, 0, 0, 0
for at in range(1, ticks + 1):
    s1, cl = step.act(layout, s)
    for t in range(len(loaded.trains)):
        clicks_abs[t] += int(np.abs(np.asarray(cl[t], dtype=object)).sum())
    if twin_n and at <= twin_n:
        tw1, cl2 = step.act(layout, twin)
        twin_board += int(same(tw1[:4], s1[:4]))
        apart = np.asarray(cl2 != cl)
        twin_clicks_apart += int(apart.any())
        mask = apart.copy(); mask[held_t, 0] = False
        twin_elsewhere += int(mask.any())
        twin = tw1
    e, eh, et = E32(s1)
    if BOOKS:
        bk32, bkS = booked(s, s1)
        miss = E32_clocks(s1) - E32_clocks(s) - bk32 - share_clocks(s, s1)
        bk_miss += int(np.count_nonzero(np.asarray(miss != 0)))
        bk_places += miss.size
        sumlegs = bkS.sum(axis=0)
        bk_legs += int(np.count_nonzero(np.asarray(sumlegs != 0)))
        engS = engine_passing(s, s1)
        resid = engS - bkS
        bk_run = bk_run + resid
        bk_top = max(bk_top, max(abs(int(v)) for v in bk_run.ravel()))
        eng_legs = engS.sum(axis=0)
        bk_englegs = max(bk_englegs, max(abs(int(v)) for v in eng_legs.ravel()))
        bk_exact_top = max(bk_exact_top, max(abs(int(v)) for v in bkS.ravel()))
    if SHARES:
        sh, st_ = shares(s, s1)
        cum_h, cum_t = cum_h + sh, cum_t + st_
    if MODE == "bedge":
        if e - E32(s)[0] == predicted(s, s1):
            ok_id += 1
        elif first_off is None:
            first_off = at
    pt, ph = permilles(s, s1)
    if DIAL:
        dmin_now = min(int(v) for v in (2 * W + gco(s.a, s1.a))[H].ravel())
        dial_min = (dmin_now, at) if dial_min[0] is None else min(dial_min, (dmin_now, at))
    ptop, htop = max(ptop, (pt, at)), max(htop, (ph, at))
    s = s1
    w = wide(s)
    wmax = max(wmax, w)
    emin, emax = min(emin, e), max(emax, e)
    if at % every == 0 or w > 128:
        rel, _ = carry(1000000 * abs(e - e0), e0, 0)
        print(f"round {at}: widest {w} bits; E32 {e} ({int(rel)} ppm from the lay; held {eh}, other {et}); T's curvature {pt}, H's 2g {ph} permille of 4W", flush=True)
        if SHARES:
            print(f"  the teeth's share summed to round {at}: on the held rows {cum_h}, on the others {cum_t}", flush=True)
    if w > 128:
        print(f"a count past the width {universe['integers']['width']} after round {at}", flush=True)
        break
print(f"rounds {at}; widest {wmax} bits; E32 from {emin} to {emax} (lay {e0})", flush=True)
if MODE == "bedge":
    print(f"the exact identity dE32 = SUM (s - s+)(...) held in {ok_id} of {at} rounds; first off: {first_off}", flush=True)
print(f"T's largest curvature {ptop[0]} permille of 4W at round {ptop[1]}; H's largest 2g {htop[0]} at round {htop[1]}", flush=True)
if DIAL:
    pd, _ = carry(1000 * dial_min[0], FOUR_W, 0)
    print(f"the held rows' smallest out-dial W(a) + W(a') + g_out over the run: {dial_min[0]} ({int(pd)} permille of 4W) at round {dial_min[1]}", flush=True)
if BOOKS:
    keyv = int(np.asarray(click.key).ravel()[0])
    kt, _ = carry(bk_top, keyv, 0)
    print(f"books: each clock's energy change = its booked exchanges + its teeth's share, missed at {bk_miss} of {bk_places} clock-rounds", flush=True)
    print(f"books: the exact exchanges summed over each monomial's legs, not 0 at {bk_legs} Node-clock-rounds", flush=True)
    print(f"books: the act's two-leg passing beside the exact exchange: its running residual at one clock reaches {bk_top} ({int(kt)} keys of {keyv}); its sum over the trains at one Node-clock in one round reaches {bk_englegs}; the exact exchange at one clock in one round reaches {bk_exact_top}", flush=True)
print("whole clicks |q| summed over the run, by train:", clicks_abs, flush=True)
if twin_n:
    print(f"hidden twin over {min(twin_n, at)} rounds: board alike in {twin_board}; clicks apart in {twin_clicks_apart} rounds; apart at another clock in {twin_elsewhere}", flush=True)
force1, j1 = step.sources(layout, s.a)
assert np.array_equal(j1[H], -2 * gco(s.a, s.a)[H] * s.a[H])
if "noback" not in sys.argv:
    x = step.mirror(layout, s)
    for _ in range(at):
        x = step.tick(layout, x)
    x = step.mirror(layout, x)
    print(f"run back from the end state alone ({at} rounds, the engine's mirror, the same act, the mirror): exact {same(x, s0)}", flush=True)
nt = int(opts.get("turns", 0))
if nt:
    from tests import frame
    from tests.test_the_tensor24_run import turned
    plain = [s0]
    for _ in range(nt):
        plain.append(step.tick(layout, plain[-1]))
    alike = 0
    for m in frame.turns():
        x, good = turned(m, layout, loaded, s0, shape), True
        for r in range(1, nt + 1):
            x = step.tick(layout, x)
            if not same(x, turned(m, layout, loaded, plain[r], shape)):
                good = False
                break
        alike += int(good)
    print(f"the 24: alike in {alike} of 24 turns over {nt} rounds", flush=True)
