"""STOP1 copy of CONF1's kept.py (S/conf1/probes/kept.py), two changes and nothing else: dg covers a row held four
times (the stop's x^4 = (x x)(x x), held twice in each pair: 4 f x^2 in both dials, STOP1 section 3), and dg runs with
the stop (the board alone, as kept.py's stop runs). The window's read keeps kept.py's 12 f x^2.
CONF1 probe: the quantities the act keeps exactly, read round by round on a lay, on a tree's own loader and act.

The tree is an extracted tree (git archive) of node-live 1794d474b or node-edge 88b4d281c, read only. Modes:
- built: the tree's own step.act as shipped (on node-edge the edge teeth and the books on; on node-live its
  per-train click teeth);
- cut: the act with its passing and click carry cut out, the board alone, every click tooth left at its birth;
- dg: HAT2's energy-keeping step (both of a round's dials gain the row's curvature at the now slot), with the
  tree's own passing.
Per round, in exact integers:
- the board: the widest count, the held rows (A1, A2) and the tied rows' counts, and whether every row stays in the
  lay's invariant subspace (the held rows alike, every row the lay leaves at 0 still 0);
- the momentum books: M_out = M_in + 4 push, M = 2 D (a - b) + s the act's exact momentum on an edge, and push = J;
- the act's edge energy E' = SUM M_in^2 + 8 D V_e(a, b), V_e(z+, z) = SUM_m f_m e1_m(z+; z), e1(y; x) the sum over
  a monomial's value positions of its leg at y times its other legs at x. Its change per round is, exactly,
  8 D SUM_m R_m(a, b) + Theta, with R_m(a, b) = f_m (e1_m(b; a) - e1_m(a; b)) (David's -f (e1 - e3), NOT_CLOSED 29
  2.1, 0 on every two-leg monomial) and Theta = 4 SUM_rows J (s+ + s), the teeth's share; by monomial group (the
  held hand's own spring, the tie, the hands' tie), the groups read off the legs' trains;
- the circulations: L_k = k_A1 M_A2 - k_A2 M_A1 (the held hand's), L_gt = SUM_i (x_g,i M_t,i - x_t,i M_g,i) (the
  tied pair's);
- node-edge: every edge's two sides, q + q' = 0 and k + k' = key - 1; every side's key SUM q - SUM P = k(0) - k(n);
  each clock's click total; node-live: its books' miss, SUM over the trains of the passing, against the residual over
  the act's two windows;
- the 24: the lay's stabilizer among the 24 turns, and every round's state fixed by it;
- the board's chain digest, sha256 over (a, b, s, r_d) round after round, to set the modes side by side.
At the end: the run back from the end state alone (the last state within the width), by the tree's untick, against
the start seed, every field; and the first round whose state is the start seed again, if any. The run stops where a
count passes the width, named as the runner names it.
stop=1 (a candidate no file picks, CONF1 section 5, with the board alone, mode cut): G3's stop, lam c^2 on each tied
train's own square c (its kinds' tables with themselves onto A1), lam = hold f, the plans' one quartic factor.
Usage: python -I kept.py <tree> <files dir> <built|cut|dg> [rounds=N] [every=E] [table=<path>] [stop=1]
Whole numbers only; Rule3's carry the one division; no float, root, search or table.
"""

import hashlib
import json
import sys
from pathlib import Path

TREE, FILES, MODE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
opts = dict(x.split("=", 1) for x in sys.argv[4:] if "=" in x)
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds as kindsmod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import contract  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loadmod  # noqa: E402
from tensor24.runner import plans  # noqa: E402
from tensor24.runner.files import sites_of, star  # noqa: E402

universe, piece, setting = (
    json.loads(FILES.joinpath(n + ".json").read_text(encoding="utf-8")) for n in ("universe", "piece", "setting")
)
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
assert found == [], found
STOP = "stop" in opts
if STOP:
    # a candidate no file picks (CONF1 section 5): G3's stop, one on each tied train's own square c = SUM C_yz x_y x_z
    # (the train's kinds' tables with themselves onto A1, plans.pairs_of), lam c^2 at the plans' one quartic factor,
    # lam = hold f with f = rest div Gamma (plans.holding's line), every pair of pairs once in order (c^2's terms)
    _, rest = loadmod.teeth(universe, star(len(shape)))
    f_tie, _ = carry(rest, universe["integers"]["full_rate"], 0)
    lam = universe["chosen"]["hold"] * f_tie
    one, two, entry, trn = plans.pairs_of(loaded.trains, c, loadmod.vocabulary(kinds, square)[2][0])
    tiedmask = np.array([int(loaded.trains.tied[int(x)]) for x in trn], dtype=object)
    sel = [i for i in range(len(entry)) if int(entry[i]) * int(tiedmask[i]) != 0]
    st_f, st_l = [], []
    for i in sel:
        for j in sel:
            if int(trn[i]) == int(trn[j]):
                st_f.append(lam * int(entry[i]) * int(entry[j]))
                st_l.append((int(one[i]), int(two[i]), int(one[j]), int(two[j])))
    f_old, l_old = loaded.potential
    newf = np.concatenate((np.asarray(f_old, dtype=object), np.array(st_f, dtype=object)))
    newl = tuple(np.concatenate((np.asarray(l_old[q]), np.array([x[q] for x in st_l], dtype=np.intp))) for q in range(4))
    N_OLD = len(f_old)
    loaded = loaded._replace(potential=(newf, newl))
    assert MODE in ("cut", "dg"), "the stop is laid on the board alone: the edge weights are the loader's, laid for its own potential"
layout = tmain.layout(universe, shape, loaded)
s0 = State(*loaded.state)
EDGE = "across" in type(layout.click)._fields
WIDTH = universe["integers"]["width"]
ROUNDS = int(opts.get("rounds", setting["ticks"]))
EVERY = int(opts.get("every", 50))

# ---- the live monomials, read off the loaded potential; each one's group by its value legs' trains
factor, legs = loaded.potential
legs = np.stack(legs, axis=1).astype(np.intp)
row, of, _, _, _ = plans.rows_of(loaded.trains)
rows = int(loaded.trains.size.sum())
train_of = np.zeros(rows, dtype=np.intp)
train_of[row] = of
held_t = [int(t) for t in range(len(loaded.trains)) if int(loaded.trains.held[t])]
live = [i for i in range(len(factor)) if int(factor[i]) != 0]
LG = legs[live]
F = np.array([int(factor[i]) for i in live], dtype=object)
VAL = (LG >= 0).astype(object)


def group_of(lg):
    ts = sorted(set(int(train_of[x]) for x in lg if x >= 0))
    if len(ts) == 1:
        return "own"
    if len(ts) == 2 and any(t in held_t for t in ts):
        return "tie"
    if len(ts) == 2:
        return "hands"
    return "more"


GROUP = [group_of(lg) for lg in LG]
if STOP:
    GROUP = [("stop" if i >= N_OLD else g) for i, g in zip(live, GROUP)]
NAMES = [g for g in ("own", "tie", "hands", "stop", "more") if g in GROUP]
MASK = {g: np.array([int(x == g) for x in GROUP], dtype=object) for g in NAMES}

# the monomials holding a row twice: the row's own curvature (HAT2's kappa), for dg and for the window's read; a row
# held four times (the stop's x^4) adds 12 f x^2 to the window's read, and dg's form does not cover it (HAT2 1)
RA, CA, A1_, A2_, PW = [], [], [], [], []
DG4_R, DG4_C = [], []
for f, lg in zip(F, LG):
    lg = [int(x) for x in lg]
    for r in sorted(set(x for x in lg if x >= 0)):
        if lg.count(r) == 2:
            o = list(lg)
            o.remove(r)
            o.remove(r)
            RA.append(r)
            CA.append(2 * int(f))
            A1_.append(o[0])
            A2_.append(o[1])
            PW.append(0)
        elif lg.count(r) == 4:
            RA.append(r)
            CA.append(12 * int(f))
            A1_.append(-1)
            A2_.append(-1)
            PW.append(2)
            DG4_R.append(r)
            DG4_C.append(4 * int(f))
        assert lg.count(r) in (1, 2, 4), lg
RA, A1_, A2_ = (np.array(x, dtype=np.intp) for x in (RA, A1_, A2_))
CA = np.array(CA, dtype=object)[:, None]
PW = np.array(PW, dtype=object)[:, None]


def kappa(a):
    v = step.valued(a)
    k = 0 * a
    np.add.at(k, RA, CA * v[A1_] * v[A2_] * v[RA] ** PW)
    return k


DG4_R = np.array(DG4_R, dtype=np.intp)
DG4_C = np.array(DG4_C, dtype=object)[:, None]
TWICE = np.array([[int(int(p[0]) == 0)] for p in PW], dtype=object)  # the rows held twice: kappa's own terms


def kappa_dg(a):
    """dg's dial: every pair holding a row twice adds 2 f times the other pair at the now slot; a row held four times
    is held twice in each of its two pairs, 4 f x^2 (STOP1 section 3)."""
    v = step.valued(a)
    k = 0 * a
    np.add.at(k, RA, TWICE * CA * v[A1_] * v[A2_])
    if len(DG4_R):
        np.add.at(k, DG4_R, DG4_C * v[DG4_R] * v[DG4_R])
    return k


def others(g):
    """Each position's product over the other positions, (M, P, S): the prefix times the suffix, no division."""
    one = np.ones_like(g[:, :1])
    pre = np.concatenate((one, np.multiply.accumulate(g[:, :-1], axis=1)), axis=1)
    suf = np.concatenate((np.multiply.accumulate(g[:, :0:-1], axis=1)[:, ::-1], one), axis=1)
    return pre * suf


def e1(y, x):
    """(M,): per monomial, summed over the sites, its value positions' leg at y times its other legs at x."""
    Y, X = step.valued(y)[LG], step.valued(x)[LG]
    return (VAL[:, :, None] * Y * others(X)).sum(axis=(1, 2))


def by_group(per):
    return {g: int((MASK[g] * per).sum()) for g in NAMES}


# ---- the act's own push, its lines replicated (pure functions of the layout and the state)
def pushed(s):
    _, _, _, _, gearing, _, _, _, _, _, _ = layout
    a, b, tooth, rd, k = s
    force, j1 = step.sources(layout, a)
    _, _, _, teeth, _ = gearing
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(layout, s, step.driven(gearing, force, step.kick(gearing, first)))
    q, kept = step.drive(j, teeth, rd)
    return step.driven(gearing, force, step.kick(gearing, q)), kept, j1


def passed(s, a1):
    """The tree's own passing of the round's window, and its carry at the key: (P, clicks, k+)."""
    nb, _, _, _, _, plan, _, _, click, _, _ = layout
    a, b, _, _, k = s
    if EDGE:
        _, _, key, _, _ = click
        p = np.concatenate((step.passing(click, plan, b, a, a1), step.crossing(click, nb, b, a, a1)))
    else:
        _, _, _, _, key = click
        jb, ja, ja1 = (contract(plan, step.valued(v), v) for v in (b, a, a1))
        p = step.passing(click, a, b, ja, jb) + step.passing(click, a1, a, ja1, ja)
    q, k1 = carry(p, key, k)
    return p, q, k1


BUILT = step.act


def act_cut(lay, s):
    _, _, _, _, gearing, _, clock, _, _, _, _ = lay
    a, b, tooth, rd, k = s
    push, kept, _ = pushed(s)
    senses = step.halves(lay)
    wa, wb = step.dials(lay, s)
    first, _, _ = step.gear(a, b, tooth, wa + wb, wa + wb, push, senses)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb, wa + step.weight(gearing, clock, first), push, senses)
    return State(a1, b1, s1, kept, k), 0 * k


def act_dg(lay, s):
    _, _, _, _, gearing, _, clock, _, _, _, _ = lay
    a, b, tooth, rd, k = s
    push, kept, _ = pushed(s)
    senses = step.halves(lay)
    wa, wb = step.dials(lay, s)
    kap = kappa_dg(a)
    first, _, _ = step.gear(a, b, tooth, wa + wb + kap, wa + wb + kap, push, senses)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb + kap, wa + step.weight(gearing, clock, first) + kap, push, senses)
    if STOP:
        return State(a1, b1, s1, kept, k), 0 * k
    _, q, k1 = passed(s, a1)
    return State(a1, b1, s1, kept, k1), q


if MODE == "cut":
    step.act = act_cut
elif MODE == "dg":
    step.act = act_dg
else:
    assert MODE == "built", MODE

# ---- HAT2/HAT4's polarized energy (dg's own): 4E = SUM 2 D (a - b)^2 + 4 V_d(a, b)
P1, P2 = [], []
for lg in LG:
    lg = [int(x) for x in lg]
    if lg[0] == lg[1]:
        P1.append((lg[0], lg[1]))
        P2.append((lg[2], lg[3]))
    elif lg[2] == lg[3] and lg[2] >= 0:
        P1.append((lg[2], lg[3]))
        P2.append((lg[0], lg[1]))
    else:
        P1.append((lg[0], lg[2]))
        P2.append((lg[1], lg[3]))
P1, P2 = np.array(P1, dtype=np.intp), np.array(P2, dtype=np.intp)


def vd_groups(s):
    """4 V_d(a, b) by monomial group: HAT2/HAT4's polarized potential on the state's two slots."""
    vp, v = step.valued(s.a), step.valued(s.b)
    per = (F[:, None] * (vp[P1[:, 0]] * vp[P1[:, 1]] * v[P2[:, 0]] * v[P2[:, 1]]
                         + v[P1[:, 0]] * v[P1[:, 1]] * vp[P2[:, 0]] * vp[P2[:, 1]])).sum(axis=1)
    return {g: 4 * x for g, x in by_group(per).items()}


def e4_dg(s):
    wa, wb = step.dials(layout, s)
    vp, v = step.valued(s.a), step.valued(s.b)
    vd = (F[:, None] * (vp[P1[:, 0]] * vp[P1[:, 1]] * v[P2[:, 0]] * v[P2[:, 1]]
                        + v[P1[:, 0]] * v[P1[:, 1]] * vp[P2[:, 0]] * vp[P2[:, 1]])).sum()
    return int((2 * (wa + wb) * (s.a - s.b) * (s.a - s.b)).sum() + 4 * vd)


# ---- the 24 on a 1 x 1 x 1 board's rows (every site its own image), the tooth halved by Rule3's carry
def turned(m, s):
    acting = kindsmod.kinds(m[None, :, :])
    turn = np.eye(rows, dtype=object)
    for t in range(len(loaded.trains)):
        train = loaded.trains[t]
        blocks, before = ([kindsmod.square(acting)[0]] if train.square else [acting[k][0] for k in train.kinds]), 0
        for matrix in blocks:
            at = train.first + (before + np.arange(len(matrix))) * train.part
            before += len(matrix)
            for part in range(train.part):
                turn[np.ix_(at + part, at + part)] = matrix
    half, _ = carry(turn @ (s.r + s.r + 1) - 1, 2, 0)
    return State(turn @ s.a, turn @ s.b, half, s.rd, s.k)


def same(x, y):
    return all(np.array_equal(p, q) for p, q in zip(x, y))


import itertools  # noqa: E402

TURNS = []
for order, signs in itertools.product(itertools.permutations(range(3)), itertools.product((1, -1), repeat=3)):
    m = np.zeros((3, 3), dtype=int)
    m[range(3), order] = signs
    if int(np.dot(m[0], np.cross(m[1], m[2]))) == 1:
        TURNS.append(m)
assert len(TURNS) == 24
STAB = [m for m in TURNS if same(turned(m, s0), s0)]  # the lay's stabilizer, every field (the teeth too)
STAB_AB = [m for m in TURNS if same(turned(m, s0)[:2], s0[:2])]  # the counts' stabilizer (a and b alone)

# ---- the lay's subspace: rows alike at the lay with alike rows' equations stay alike; rows at 0 that nothing drives
held_rows = [r for r in range(rows) if int(train_of[r]) in held_t]
# the lay's closure: the rows the lay moves, and every row a live monomial drives from them (a position whose other
# value legs all lie in the set), until nothing is added; every other row is 0 with a zero push, by the structure
moving = set(r for r in range(rows) if int(s0.a[r, 0]) != 0 or int(s0.b[r, 0]) != 0 or int(s0.r[r, 0]) != 0)
grown = True
while grown:
    grown = False
    for lg in LG:
        vs = [int(x) for x in lg if x >= 0]
        for i, x in enumerate(vs):
            if x not in moving and all(y in moving for j, y in enumerate(vs) if j != i):
                moving.add(x)
                grown = True
moving = sorted(moving)
tied_moving = [r for r in moving if r not in held_rows]

def sci(n):
    """A whole number shown as d.ddd e N by its digits alone (no float)."""
    n = int(n)
    d = str(abs(n))
    return ("-" if n < 0 else "") + (d if len(d) < 5 else d[0] + "." + d[1:4] + "e" + str(len(d) - 1))


def bits(s):
    return max(max(int(abs(int(x))).bit_length() for x in s.a.ravel()), max(int(abs(int(x))).bit_length() for x in s.b.ravel()))


def board_text(s):
    return json.dumps([s.a.tolist(), s.b.tolist(), s.r.tolist(), s.rd.tolist()])


# ---- the run
D_rows = None
table = open(opts["table"], "w", encoding="utf-8") if "table" in opts else None
chain = hashlib.sha256(board_text(s0).encode("utf-8")).hexdigest()
s = s0
wa0, wb0 = step.dials(layout, s0)
D0 = wa0 + wb0
uniform = int(all(int(x) == int(D0.ravel()[0]) for x in D0.ravel()))
D = int(D0.ravel()[0])
W4 = 2 * D  # 4 W, the explicit step's window on a row's curvature
tot = {"dK": 0, "Theta": 0, **{"R_" + g: 0 for g in NAMES}, **{"dVe_" + g: 0 for g in NAMES}}
checks = {"momentum books": 0, "push = J": 0, "energy ledger": 0, "work = e1 form": 0, "subspace": 0,
          "stabilizer": 0, "edge q + q' = 0": 0, "edge k + k' = key - 1": 0, "carry law": 0, "live miss = residual": 0}
side_sum_q, side_sum_p = None, None
e4_first, e4_lo, e4_hi = None, None, None
e4_0 = e4_dg(s0)
named, stopped_at, first_return = None, 0, None
first_wide = {}
key = int((layout.click.key if EDGE else layout.click.key).ravel()[0])
k_birth = s0.k.copy()
clock_total = None
print(f"tree {TREE.name}, mode {MODE}, edges {'on (node-edge term 11 on the edges)' if EDGE else 'off (per-train click teeth)'}; "
      f"rows {rows}, live monomials {len(F)} by group {dict((g, int(MASK[g].sum())) for g in NAMES)}; "
      f"dial 2D uniform {bool(uniform)} at D = {D}; key {key}; the lay's stabilizer {len(STAB)} of 24 turns (every field), "
      f"{len(STAB_AB)} of 24 (the counts alone); the lay's closure, rows {moving}", flush=True)
print(f"at the lay: K' {int((((2 * D0 * (s0.a - s0.b) + s0.r) ** 2)).sum())}, 8D V_e {dict((g, 8 * D * v) for g, v in by_group(F * e1(s0.a, s0.b)).items())}, 4E_dg {e4_0}", flush=True)
for at in range(1, ROUNDS + 1):
    a, b, r = s.a, s.b, s.r
    push, kept, j1 = pushed(s)
    s1, q = step.act(layout, s)
    a1 = s1.a
    wa, wb = step.dials(layout, s)
    wa1, wb1 = step.dials(layout, s1)
    m_in = 2 * (wa + wb) * (a - b) + r
    m_out = 2 * (wa1 + wb1) * (a1 - a) + s1.r
    if MODE != "dg":
        checks["momentum books"] += int(not (m_out - m_in - 4 * push).any())
    checks["push = J"] += int(not (push - j1).any())
    # the work and the ledger (exact)
    e_ab, e_ba, e_a1a = e1(a, b), e1(b, a), e1(a1, a)
    work = int((j1 * (a1 - b)).sum())
    checks["work = e1 form"] += int(work == -int((F * (e_a1a - e_ba)).sum()))
    R = by_group(F * (e_ba - e_ab))
    dVe = {g: v1 - v0 for (g, v1), v0 in zip(by_group(F * e_a1a).items(), by_group(F * e_ab).values())}
    theta = int((4 * j1 * (s1.r + r)).sum())
    theta_t = [int((4 * j1 * (s1.r + r))[[x for x in range(rows) if int(train_of[x]) == tt]].sum()) for tt in range(len(loaded.trains))]
    kin_t = [int((m_out * m_out)[[x for x in range(rows) if int(train_of[x]) == tt]].sum()) for tt in range(len(loaded.trains))]
    dK = int((m_out * m_out).sum() - (m_in * m_in).sum())
    if MODE != "dg":
        ledger = 8 * D * (sum(R.values()) - sum(dVe.values())) + theta
        checks["energy ledger"] += int(uniform and dK == ledger)
    tot["dK"] += dK
    tot["Theta"] += theta
    for g in NAMES:
        tot["R_" + g] += 8 * D * R[g]
        tot["dVe_" + g] += 8 * D * dVe[g]
    # the books
    if MODE != "cut" and not STOP:
        p, qq, k1 = passed(s, a1)
        checks["carry law"] += int(same([qq, k1], [q, s1.k]) and not (p + s.k - q * key - s1.k).any())
        if EDGE:
            T = len(loaded.trains)
            qv = q.reshape(-1, T, T, q.shape[-1])
            kv = s1.k.reshape(-1, T, T, q.shape[-1])
            checks["edge q + q' = 0"] += int(not (qv + qv.swapaxes(1, 2)).any())
            checks["edge k + k' = key - 1"] += int(not (kv + kv.swapaxes(1, 2) + 1 - key).any())
            side_sum_q = q.copy() if side_sum_q is None else side_sum_q + q
            side_sum_p = p.copy() if side_sum_p is None else side_sum_p + p
        else:
            miss = int(p.sum())
            checks["live miss = residual"] += int(miss == sum(R.values()) + sum(by_group(F * (e1(a, a1) - e1(a1, a))).values()))
            side_sum_q = q.copy() if side_sum_q is None else side_sum_q + q
            side_sum_p = p.copy() if side_sum_p is None else side_sum_p + p
    # the subspace and the 24
    checks["stabilizer"] += int(all(same(turned(m, s1), s1) for m in STAB) and all(same(turned(m, s1)[:2], s1[:2]) for m in STAB_AB))
    alike = all(int(s1.a[x, 0]) == int(s1.a[held_rows[0], 0]) and int(s1.b[x, 0]) == int(s1.b[held_rows[0], 0])
                and int(s1.r[x, 0]) == int(s1.r[held_rows[0], 0]) for x in held_rows)
    still = all(int(s1.a[x, 0]) == 0 and int(s1.b[x, 0]) == 0 and int(s1.r[x, 0]) == 0 for x in range(rows) if x not in moving)
    checks["subspace"] += int(alike and still)
    # dg's own energy, read on the counts
    e4 = e4_dg(s1)
    e4_lo = e4 if e4_lo is None else min(e4_lo, e4)
    e4_hi = e4 if e4_hi is None else max(e4_hi, e4)
    if e4_first is None and e4 != e4_0:
        e4_first = at
    # the circulations
    hk = held_rows
    L_k = int(s1.a[hk[0], 0] * m_out[hk[1], 0] - s1.a[hk[1], 0] * m_out[hk[0], 0]) if len(hk) == 2 else 0
    tg = sorted(set(int(train_of[x]) for x in range(rows)) - set(held_t))
    xg = [x for x in range(rows) if int(train_of[x]) == tg[0]]
    xt = [x for x in range(rows) if int(train_of[x]) == tg[1]]
    L_gt = int(sum(s1.a[i, 0] * m_out[j, 0] - s1.a[j, 0] * m_out[i, 0] for i, j in zip(xg, xt)))
    w = bits(s1)
    for mark in (8, 16, 32, 64, 96):
        if w > mark and mark not in first_wide:
            first_wide[mark] = at
    kap = kappa(a1)
    ph = max(int(carry(1000 * kap[x, 0], W4, 0)[0]) for x in hk)
    pt = max(int(carry(1000 * kap[x, 0], W4, 0)[0]) for x in tied_moving)
    E_edge = int((m_out * m_out).sum()) + 8 * D * int((F * e_a1a).sum())
    chain = hashlib.sha256((chain + board_text(s1)).encode("utf-8")).hexdigest()
    if table is not None:
        table.write(json.dumps({"round": at, "bits": w, "k": [int(s1.a[x, 0]) for x in hk],
                                "tied": [int(s1.a[x, 0]) for x in tied_moving], "K'": int((m_out * m_out).sum()),
                                "8D Ve": {g: 8 * D * v for g, v in by_group(F * e_a1a).items()},
                                "8D R": {g: 8 * D * v for g, v in R.items()}, "Theta": theta, "Theta by train": theta_t, "K' by train": kin_t, "E'": E_edge,
                                "4E_dg": e4, "4Vd": vd_groups(s1), "4W(a-b)^2 x2": int((2 * (wa1 + wb1) * (s1.a - s1.b) * (s1.a - s1.b)).sum()), "L_k": L_k, "L_gt": L_gt, "held permille of 4W": ph,
                                "tied permille of 4W": pt}) + "\n")
    if carry(at, EVERY, 0)[1] == 0 or at == ROUNDS or w > WIDTH:
        print(f"round {at}: widest {w} bits; held {[int(s1.a[x, 0]) for x in hk][0]} tied {[int(s1.a[x, 0]) for x in tied_moving]}; "
              f"curvature permille of 4W held {ph} tied {pt}; K' {sci((m_out * m_out).sum())}; E' {sci(E_edge)}; "
              f"cum 8D R {dict((g, sci(tot['R_' + g])) for g in NAMES)}; cum Theta {sci(tot['Theta'])}; "
              f"cum -8D dVe {dict((g, sci(-tot['dVe_' + g])) for g in NAMES)}; L_k {L_k}; L_gt {sci(L_gt)}; 4E_dg {sci(e4)}; chain {chain[:16]}", flush=True)
    stopped_at = at
    if first_return is None and same(s1, s0):
        first_return = at
    s_prev, s = s, s1
    if w > WIDTH:
        named = f"round {at + 1}: a count takes more bits than the width, {WIDTH} (the state after round {at})"
        break

if EDGE:
    checks.pop("live miss = residual")
else:
    checks.pop("edge q + q' = 0")
    checks.pop("edge k + k' = key - 1")
if MODE == "cut" or STOP:
    for x in ("carry law", "live miss = residual", "edge q + q' = 0", "edge k + k' = key - 1"):
        checks.pop(x, None)
if MODE == "dg":
    checks.pop("momentum books")
    checks.pop("energy ledger")
print("checks, rounds of", stopped_at, ":", json.dumps(checks), flush=True)
print("first round past 8/16/32/64/96 bits:", json.dumps(first_wide), flush=True)
print("named:", named, "; the first round whose state is the start seed again, every field:", first_return, flush=True)
print(f"totals over the run: K'(end) - K'(lay) {tot['dK']}, of which cum 8D R {dict((g, tot['R_' + g]) for g in NAMES)}, "
      f"cum Theta {tot['Theta']}, cum -8D dVe {dict((g, -tot['dVe_' + g]) for g in NAMES)}", flush=True)
print(f"4E_dg at the lay {e4_0}; first change at round {e4_first}; range {e4_lo} to {e4_hi}", flush=True)
if side_sum_q is not None:
    if EDGE:
        T = len(loaded.trains)
        sq = side_sum_q[: T * T].reshape(T, T)
        sp = side_sum_p[: T * T].reshape(T, T)
        teeth = (k_birth - s.k)[: T * T].reshape(T, T)
        print("each side's clicks summed, (t, u) own Node-clock:", sq.tolist(), flush=True)
        print("each side's key SUM q - SUM P = k(0) - k(n):", bool(not (key * sq - sp - teeth).any()),
              "; each side's |key SUM q - SUM P| below key:", bool(all(abs(int(x)) < key for x in (key * sq - sp).ravel())), flush=True)
        print("each side's passing summed, (t, u):", sp.tolist(), flush=True)
        print("each clock's click total:", [int(x) for x in sq.sum(axis=1)], "summed over the clocks:", int(sq.sum()),
              "; the Mesh edges' sides all 0:", bool(not side_sum_q[T * T:].any()), flush=True)
    else:
        print("each train's clicks summed:", [int(x) for x in side_sum_q.ravel()], "summed:", int(side_sum_q.sum()),
              "; each train's passing summed:", [int(x) for x in side_sum_p.ravel()], "; the books' miss summed:", int(side_sum_p.sum()), flush=True)
print("board chain digest:", chain, flush=True)
# the run back from the end state alone: from the last state within the width
end, n = (s, stopped_at) if named is None else (s_prev, stopped_at - 1)
back = end
for _ in range(n):
    back = step.untick(layout, back)
print(f"run back from the end state alone over {n} rounds: board and every tooth at the start seed: {same(back, s0)}", flush=True)
if table is not None:
    table.close()
