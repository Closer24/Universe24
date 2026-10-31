"""MIRACLE_A, the board: the polarized step of the files' potential (HAT4's form, the coupled McMillan step) on the
engine's own worlds, in three forms, read round by round.
  exact:  the force read at the exact rational (the count and its tooth together): every gear's two slots exact
          rationals (qrat.R, reduced by Euclid's carries, the least an exact form holds), the engine's own sources,
          weights and plans run on them, the split replaced by the exact quotient,
            n = 2 (D_in + kappa(a)) (a - b) + 4 push(a),   a+ = a + n / (2 (D_out + kappa(a))),
          D_out = W(a) + W(first) as the engine reads its 00 row's next count first. The drive's teeth are 1 wherever
          the plan lands and the metric's push plan is all 0 on these worlds (read and asserted), so push = s F + J1.
          The click tooth is not stepped (its carry would read a rational passing).
  whole:  HAT4's act, the engine's act with both dials gaining kappa(a), the row's curvature at the middle count,
            2 (D_out + kappa(a)) (a+ - a) + s+ = 2 (D_in + kappa(a)) (a - b) + s + 4 J(a), split at the carry.
  engine: the engine's own act, unpatched.
kappa(a) = SUM over the live monomials holding the row twice of 2 f PROD the other legs at a. The polarized energy,
  4E = SUM_g 2 (W(a) + W(b)) (a - b)^2 + 4 V_d(a, b),  V_d(z', z) = SUM_m f [P1(z') P2(z) + P1(z) P2(z')]
(HAT4's pairing), read on the exact rationals (exact) or on the counts (whole, engine). The run back is the same act on
the mirrored end state alone (step.untick's mirror). The 24 by the run test's own turned(). Usage:
python -I board.py <exact|whole|engine> <universe> <piece> <setting> [rounds=N] [turns=N] [back] [every=N]"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import qrat  # noqa: E402,F401  (puts the tree on the path)
from qrat import R, bits, over  # noqa: E402

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loadmod  # noqa: E402
from tensor24.runner.files import sites_of, star  # noqa: E402

MODE = sys.argv[1]
opts = dict(x.split("=") for x in sys.argv[5:] if "=" in x)
universe, piece, setting = (json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[2:5])
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
assert found == [], found
layout = tmain.layout(universe, shape, loaded)
_, _, _, _, gearing, plan, clock, _, click, push_plan, mesh_plan = layout
factor, legs = loaded.potential
legs = np.stack(legs, axis=1).astype(np.intp)
R_, C_, O1, O2, PF, P1, P2 = [], [], [], [], [], [], []
for f, lg in zip(factor, legs):
    if int(f) == 0:
        continue
    lg = [int(x) for x in lg]
    for r in sorted(set(x for x in lg if x >= 0)):
        m = lg.count(r)
        assert m <= 2, ("a row more than twice: the polarized form here does not cover it", lg)
        if m == 2:
            o = list(lg)
            o.remove(r)
            o.remove(r)
            R_.append(r)
            C_.append(2 * int(f))
            O1.append(o[0])
            O2.append(o[1])
    PF.append(int(f))
    if lg[0] == lg[1]:
        P1.append((lg[0], lg[1]))
        P2.append((lg[2], lg[3]))
    elif lg[2] == lg[3] and lg[2] >= 0:
        P1.append((lg[2], lg[3]))
        P2.append((lg[0], lg[1]))
    else:
        P1.append((lg[0], lg[2]))
        P2.append((lg[1], lg[3]))
R_, O1, O2 = (np.array(x, dtype=np.intp) for x in (R_, O1, O2))
C_ = np.array(C_, dtype=object)[:, None]
PF = np.array(PF, dtype=object)[:, None]
P1, P2 = np.array(P1, dtype=np.intp), np.array(P2, dtype=np.intp)
senses = step.halves(layout)
width = universe["integers"]["width"]


def kappa(a):
    v = step.valued(a)
    k = np.zeros_like(a, dtype=object)
    np.add.at(k, R_, C_ * v[O1] * v[O2])
    return k


def Vd(zp, z):
    vp, v = step.valued(zp), step.valued(z)
    return (PF * (vp[P1[:, 0]] * vp[P1[:, 1]] * v[P2[:, 0]] * v[P2[:, 1]]
                  + v[P1[:, 0]] * v[P1[:, 1]] * vp[P2[:, 0]] * vp[P2[:, 1]])).sum()


def E4(s):
    wa, wb = step.weight(gearing, clock, s.a), step.weight(gearing, clock, s.b)
    return (senses * (wa + wb) * (s.a - s.b) * (s.a - s.b)).sum() + 4 * Vd(s.a, s.b)


ORIG_ACT = step.act


def act_whole(lay, s):
    """HAT4's act: the engine's own lines, both dials gaining kappa(a) at the middle count."""
    _, _, _, _, gearing_, plan_, clock_, _, click_, _, _ = lay
    a, b, tooth, rd, k = s
    force, j1 = step.sources(lay, a)
    _, _, _, teeth, _ = gearing_
    _, _, _, _, key = click_
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(lay, s, step.driven(gearing_, force, step.kick(gearing_, first)))
    q, kept = step.drive(j, teeth, rd)
    kicks = step.kick(gearing_, q)
    sns, push = step.halves(lay), step.driven(gearing_, force, kicks)
    wa, wb = step.dials(lay, s)
    kap = kappa(a)
    first, _, _ = step.gear(a, b, tooth, wa + wb + kap, wa + wb + kap, push, sns)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb + kap, wa + step.weight(gearing_, clock_, first) + kap, push, sns)
    jb, ja, ja1 = (step.contract(plan_, step.valued(v), v) for v in (b, a, a1))
    moved = step.passing(click_, a, b, ja, jb) + step.passing(click_, a1, a, ja1, ja)
    clicks, k1 = carry(moved, key, k)
    return State(a1, b1, s1, kept, k1), clicks


teeth_rows = np.asarray(gearing.drive, dtype=object)
assert all(int(x) == 0 for x in push_plan.factor), "the metric's push plan is not all 0: the exact form here does not cover it"


def tick_exact(s):
    a, b, tooth, rd, k = s
    force, j1 = step.sources(layout, a)
    # the drive: teeth 1 on every row the plan lands on (q = J1 exactly, no fine tooth); asserted, not assumed
    landed = [i for i in range(a.shape[0]) for x in range(a.shape[1]) if not (j1[i, x] == 0)]
    assert all(int(np.broadcast_to(teeth_rows, a.shape)[i, 0]) == 1 for i in landed)
    push = step.driven(gearing, force, step.kick(gearing, j1))
    kap = kappa(a)
    wa, wb = step.weight(gearing, clock, a), step.weight(gearing, clock, b)
    n = senses * ((wa + wb + kap) * (a - b) + senses * push)
    din = senses * (wa + wb + kap)
    first = a + np.vectorize(over, otypes=[object])(n, din)
    dout = senses * (wa + step.weight(gearing, clock, first) + kap)
    a1 = a + np.vectorize(over, otypes=[object])(n, dout)
    return State(a1, a.copy(), tooth, rd, k)


def mirror_exact(s):
    a, b, tooth, rd, k = s
    _, _, _, _, even = gearing
    tau = senses * np.broadcast_to(np.asarray(even, dtype=object), a.shape) - 1
    return State(tau * b, tau * a, tooth, rd, k)


if MODE == "whole":
    step.act = act_whole
if MODE == "exact":
    s0 = State(*loaded.state)
    s0 = State(np.vectorize(R, otypes=[object])(s0.a), np.vectorize(R, otypes=[object])(s0.b), s0.r, s0.rd, s0.k)
    assert not any(int(x) != 0 for x in np.asarray(s0.r).ravel()), "a laid tooth: the exact lay reads it as 0 here"
    tick, mirror = tick_exact, mirror_exact
else:
    s0 = State(*loaded.state)
    tick = lambda s: step.tick(layout, s)  # noqa: E731
    mirror = lambda s: step.mirror(layout, s)  # noqa: E731


def same(x, y):
    return all(np.array_equal(p, q) for p, q in zip(x, y))


def widest_count(s):
    if MODE == "exact":
        return max(int(abs(carry(v.n, v.d, 0)[0])).bit_length() for v in np.concatenate((s.a.ravel(), s.b.ravel())))
    return max(int(abs(int(v))).bit_length() for v in np.concatenate((s.a.ravel(), s.b.ravel())))


def widest_number(s):
    if MODE == "exact":
        return max(bits(v) for v in np.concatenate((s.a.ravel(), s.b.ravel())))
    return max(int(abs(int(v))).bit_length() for v in np.concatenate((s.a.ravel(), s.b.ravel(), s.r.ravel())))


def alike(s):
    return all(np.array_equal(np.repeat(x[:, :1], x.shape[1], axis=1), x) for x in (s.a, s.b, s.r))


def outside(s):
    """Wherever a tooth of the state stands outside the window of the round that reads it next (its edge's other end)."""
    if MODE == "exact":
        return False
    wa, wb = step.dials(layout, s)
    d = wa + wb + (kappa(s.a) if MODE == "whole" else 0)
    r = np.asarray(s.r, dtype=object)
    return bool(((r < -d) | (r >= d)).any())


ticks = int(opts.get("rounds", setting["ticks"]))
every = int(opts.get("every", 250))
s, e0 = s0, E4(s0)
print(f"{MODE}: rows {s0.a.shape[0]}, sites {s0.a.shape[1]}; 4E at the lay {e0}", flush=True)
lo = hi = e0
first_move, past, out_at, wide_c, wide_n, kept_all, apart = None, None, None, 0, 0, True, None
for at in range(1, ticks + 1):
    s = tick(s)
    e = E4(s)
    if MODE == "exact":
        kept_all = kept_all and (e == e0)
    else:
        lo, hi = min(lo, e), max(hi, e)
        first_move = first_move or ((at, e - e0) if e != e0 else None)
    wc, wn = widest_count(s), widest_number(s)
    wide_c, wide_n = max(wide_c, wc), max(wide_n, wn)
    past = past or (at if (wn if MODE == "exact" else wc) > width else None)
    out_at = out_at or (at if outside(s) else None)
    apart = apart or (None if alike(s) else at)
    if at % every == 0 or at == ticks or (MODE != "exact" and wc > width):
        tail = f"4E kept exactly {e == e0}; widest number {wn} bits" if MODE == "exact" else f"4E {e}"
        print(f"round {at}: widest count {wc} bits; {tail}", flush=True)
    if MODE != "exact" and wc > width:
        print(f"a count past the width {width} after round {at}", flush=True)
        break
if MODE == "exact":
    print(f"exact: 4E kept exactly in every round: {kept_all}; widest count {wide_c} bits; widest numerator or "
          f"denominator {wide_n} bits; the width {width} first passed by a number of the state at round {past}")
else:
    print(f"{MODE}: 4E at the lay {e0}; over {at} rounds from {lo} to {hi}; first change {first_move}; widest count "
          f"{wide_c} bits; first count past the width {past}; first tooth outside its other end's window: {out_at}")
print(f"the sites alike in every round: {apart is None} (first apart: {apart})", flush=True)
if "back" in sys.argv:
    def back_over(n_rounds, end):
        y = mirror(end)
        for _ in range(n_rounds):
            y = tick(y)
        return mirror(y)
    print(f"run back by the same act on the mirrored end state alone over {at} rounds:", same(back_over(at, s), s0),
          flush=True)
    if out_at and out_at < at:
        x = s0
        for _ in range(out_at):
            x = tick(x)
        y = tick(x)
        print(f"run back over {out_at} rounds: {same(back_over(out_at, x), s0)}; over {out_at + 1} rounds: "
              f"{same(back_over(out_at + 1, y), s0)}", flush=True)
nt = int(opts.get("turns", 0))
if nt:
    from tests import frame
    from tests.test_the_tensor24_run import turned
    plain = [s0]
    for _ in range(nt):
        plain.append(tick(plain[-1]))
    ok = 0
    for m in frame.turns():
        x, good = turned(m, layout, loaded, s0, shape), True
        for r in range(1, nt + 1):
            x = tick(x)
            good = good and same(x, turned(m, layout, loaded, plain[r], shape))
        ok += int(good)
    print(f"the 24: alike in {ok} of 24 turns over {nt} rounds", flush=True)
