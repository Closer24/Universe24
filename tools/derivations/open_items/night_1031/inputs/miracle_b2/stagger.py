"""MIRACLE_B probe, way (i): the true stagger, the held family H and every other row T on alternate half rounds, in the
gears as they are. The state holds H at (n-1, n) and T at (n-1/2, n+1/2). The round is Q after P:
  P: H's step; its in-edge's dial reads T's before slot (the in-edge's midpoint), its out-edge's T's now slot (the
     out-edge's midpoint): d = W(a) + W(a+) + g(T at the midpoint), g the coefficient of the row's square in V; the
     push -(g_in + g_out) a;
  Q: T's step; its in-edge's dial reads H's before slot after P (its midpoint n), its out-edge's H's now slot (n + 1):
     d = W(a) + W(a+) + g_T, g_T the coefficient of the T row's square in the monomials with held legs; the push
     -(g_in + g_out) a plus T's own monomials and the Meshes at T's now slot.
Every read is acyclic and every edge's dial is its own. Measured: the run back by the engine's mirror (M, the same act
N times, M), and by the stagger's own mirror M_s = M after P (an involution, since M P M = P^-1).
Usage: python3 -I stagger.py <universe> <piece> <setting> [rounds=N]"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("tree")))
sys.path.insert(0, str(HERE.joinpath("tree", "src")))
sys.set_int_max_str_digits(0)
import numpy as np
from tensor24 import main as tmain
from tensor24.engine import step
from tensor24.engine.contract import contract
from tensor24.engine.mesh import pull
from tensor24.engine.state import State
from tensor24.runner import load as loadmod, plans
from tensor24.runner.files import sites_of, star

opts = dict(x.split("=") for x in sys.argv[4:] if "=" in x)
paths = [Path(p) for p in sys.argv[1:4]]
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
assert found == [], found
layout = tmain.layout(universe, shape, loaded)
_, _, _, _, gearing, plan, clock, _, click, push, mesh = layout
heldflag = [int(x) for x in loaded.trains.held]
assert sum(heldflag) == 1
held_t = heldflag.index(1)
_, of, _, _, _ = plans.rows_of(loaded.trains)
rows = len(of)
H = np.array([r for r in range(rows) if of[r] == held_t], dtype=np.intp)
T = np.array([r for r in range(rows) if of[r] != held_t], dtype=np.intp)
inH = set(H.tolist())
factor, legs = loaded.potential
legs = np.stack(legs, axis=1).astype(np.intp)
HR, HF, HO1, HO2, QR, QF, QO1, QO2, LF, LL = [], [], [], [], [], [], [], [], [], []
for f, lg in zip(factor, legs):
    if int(f) == 0:
        continue
    lg = [int(x) for x in lg]
    hl = [x for x in lg if x >= 0 and x in inH]
    tl = [x for x in lg if x >= 0 and x not in inH]
    if hl:
        assert len(hl) == 2 and hl[0] == hl[1], lg
        o = list(lg); o.remove(hl[0]); o.remove(hl[0])
        HR.append(hl[0]); HF.append(int(f)); HO1.append(o[0]); HO2.append(o[1])
        assert all(x < 0 or x not in inH for x in o), lg
        for r in sorted(set(tl)):
            assert tl.count(r) == 2, ("a tied row held once beside held legs", lg)
            QR.append(r); QF.append(int(f)); QO1.append(hl[0]); QO2.append(hl[0])
    else:
        assert len(tl) <= 2, lg
        LF.append(int(f)); LL.append(lg)
HR, HO1, HO2, QR, QO1, QO2 = (np.array(x, dtype=np.intp) for x in (HR, HO1, HO2, QR, QO1, QO2))
HF, QF = np.array(HF, dtype=object)[:, None], np.array(QF, dtype=object)[:, None]
assert not np.asarray(push.factor).any() and not np.asarray(mesh.factor).any()
senses = step.halves(layout)
# T's own monomials as a plan of their own (the vertex law), read at T's now slot
from tensor24.engine.contract import pushes
if LF:
    LLa = np.array(LL, dtype=np.intp)
    tplan = pushes(np.array(LF, dtype=object), (LLa[:, 0], LLa[:, 1], LLa[:, 2], LLa[:, 3]))


def coef(R, F, O1, O2, x, y):
    vx, vy = step.valued(x), step.valued(y)
    g = 0 * x
    np.add.at(g, R, F * vx[O1] * vy[O2])
    return g


def P(s):
    """H's step, T frozen: its in-edge at T's before slot, its out-edge at T's now slot."""
    a, b, tooth, rd, k = s
    wa, wb = step.dials(layout, s)
    g_in, g_out = coef(HR, HF, HO1, HO2, b, b), coef(HR, HF, HO1, HO2, a, a)
    # T's before and now slots stand in rows T of b and a; the held legs never enter g
    h1, _, hs = step.gear(a, b, tooth, wa + wb + g_in, wa + wa + g_out, -(g_in + g_out) * a, senses)
    a1, b1, s1 = a.copy(), b.copy(), tooth.copy()
    a1[H], b1[H], s1[H] = h1[H], a[H], hs[H]
    return State(a1, b1, s1, rd, k)


def Q(s):
    """T's step, H frozen: its in-edge at H's before slot, its out-edge at H's now slot; T's own monomials and the
    Meshes at T's now slot."""
    a, b, tooth, rd, k = s
    wa, wb = step.dials(layout, s)
    g_in, g_out = coef(QR, QF, QO1, QO2, b, b), coef(QR, QF, QO1, QO2, a, a)
    lin = pull(layout, a)
    if LF:
        lin = lin + contract(tplan, step.valued(a), a)
    t1, _, ts = step.gear(a, b, tooth, wa + wb + g_in, wa + wa + g_out, lin - (g_in + g_out) * a, senses)
    a1, b1, s1 = a.copy(), b.copy(), tooth.copy()
    a1[T], b1[T], s1[T] = t1[T], a[T], ts[T]
    return State(a1, b1, s1, rd, k)


def round_(s):
    return Q(P(s))


def M(s):
    return step.mirror(layout, s)


def same(x, y):
    return all(np.array_equal(p, q) for p, q in zip(x, y))


s0 = State(*loaded.state)
assert all(np.array_equal(w, gearing.rest + 0 * s0.a) for w in step.dials(layout, s0))
ticks = int(opts.get("rounds", setting["ticks"]))
traj = [s0]
for _ in range(ticks):
    traj.append(round_(traj[-1]))
end = traj[-1]
wmax = max(max(int(abs(int(v))).bit_length() for v in np.concatenate((x.a.ravel(), x.b.ravel()))) for x in traj)
print(f"stagger: {ticks} rounds forward, widest count {wmax} bits", flush=True)
for n in (1, 2, 5, ticks):
    e = traj[n]
    x = M(e)
    for _ in range(n):
        x = round_(x)
    plain = same(M(x), s0)
    y = M(P(e))
    for _ in range(n):
        y = round_(y)
    own_ = same(M(P(y)), s0)
    print(f"over {n} rounds: run back by the engine's mirror exact {plain}; by the stagger's mirror M after P exact {own_}", flush=True)
x = s0
print("M_s an involution on the lay and the end:", same(M(P(M(P(s0)))), s0), same(M(P(M(P(end)))), end), flush=True)
