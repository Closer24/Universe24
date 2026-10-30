"""NOT_CLOSED 29 on B4's pair world (tests/test_the_tensor24_run.py's own files): the act's passing against the background
form, summed over the trains, round by round, through the real loader and act of node-live 575973a20.

The world: one Node-clock; the held hand (A1, A2) at part 1 laid (1, 0) turning, a (T1, T2) giver at rest at 32, a
(T1, T2) taker gliding a count a round; hold 1, the hands' tie 1200, the key 76801. The plan's monomials are read back
from the plan as contract.pushes lays them (four entries per monomial, the first block's target the first leg). The
act's passing per train is step.passing's own form on the value legs' plan, X(a, b) + X(a+, a). The background form:
each monomial joining the held train to one other train books S_held = -2 c P(a) (Q(a+) - Q(b)) and S_other = -S_held;
a train's own monomials and two-leg monomials keep the act's form. Printed: per window of the run, the rounds whose
passings over the trains do not sum to 0, for each form, and |k|^2 per round.

Usage: python3 -I pair_world.py <src of node-live at 575973a20> [rounds, 400 unless given]
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state, step  # noqa: E402
from tensor24.engine.contract import contract  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 400
den = 1
hand = {"name": "held", "kinds": ["A1", "A2"], "part": 1, "pinion": den}
pair = {"kinds": ["T1", "T2"], "part": 1, "pinion": den}
trains_f = [hand, {"name": "giver", **pair}, {"name": "taker", **pair}]
chosen = {"key": 76801, "push": 0, "notch": 0, "hold": 1, "tie": 1200, "mesh": 0}
integers = {"den": den, "full_rate": 10000, "width": 128}
universe = {"version": 1, "integers": integers, "chosen": chosen, "trains": trains_f}
gears = [[0, 0, 0, 1, 0, 0], [0, 1, 0, 0, -1, 0], [1, 0, 0, 32, 32, 0], [2, 0, 0, 0, -1, 0]]
setting = {"version": 1, "ticks": ROUNDS, "gears": gears}
shape = [1, 1, 1]

held, found = loading.load(universe, setting, sites_of(shape), *main.made(loading.star(len(shape))))
assert found == [] and held is not None
lay = main.layout(universe, shape, held)
s = state.State(*held.state)
tr = held.trains
rows = len(s.a)
firsts = [int(x) for x in tr.first] + [rows]
train_of = [None] * rows
for t in range(len(tr.first)):
    for r in range(firsts[t], firsts[t + 1]):
        train_of[r] = t
assert None not in train_of
held_t = [t for t in range(len(tr.first)) if int(tr.held[t])]
print(f"trains: firsts {list(map(int, tr.first))}, rows per train {[firsts[t + 1] - firsts[t] for t in range(len(tr.first))]},"
      f" held {list(map(int, tr.held))},"
      f" tied {list(map(int, tr.tied))}; rows {rows}")

plan = lay.plan
m = carry(len(plan.factor), 4, 0)[0]
monomials = [(-int(plan.factor[i]), (int(plan.target[i]), int(plan.first[i]), int(plan.second[i]), int(plan.third[i])))
             for i in range(m)]
four = [legs for _, legs in monomials if all(x >= 0 for x in legs)]
joining = [legs for legs in four if len({train_of[g] for g in legs}) == 2 and {train_of[g] for g in legs} & {0}]
print(f"monomials: {m}; four value legs: {len(four)}; of them joining the held train to one other: {len(joining)}")


def valued(x):
    return np.concatenate((x, np.ones_like(x[:1], dtype=object)))


def act_passing(b, a, a1):
    """step.passing's own form, on one Node-clock, per train: SUM over the click's terms, as step.act does."""
    jb, ja, ja1 = (contract(plan, valued(x), x) for x in (b, a, a1))
    moved = step.passing(lay.click, a, b, ja, jb) + step.passing(lay.click, a1, a, ja1, ja)
    return [int(x) for x in moved[:, 0]]


def background(b, a, a1, act):
    """The act's passing with each held-joining four-leg monomial's share replaced by the background form."""
    out = list(act)
    for f, legs in monomials:
        values = [g for g in legs if g >= 0]
        owners = {train_of[g] for g in values}
        if len(values) != 4 or len(owners) != 2 or not owners & set(held_t):
            continue
        # remove this monomial's act share (X over the window on its legs) and add the background share
        share = [0] * len(out)
        for i, g in enumerate(legs):
            others = [legs[j] for j in range(4) if j != i]

            def prod(x, ls):
                p = 1
                for h in ls:
                    p *= int(x[h, 0]) if h >= 0 else 1
                return p
            # x_g J_g(y) - y_g J_g(x) with J_g = -f (product of the other legs), on (a, b) and on (a1, a)
            share[train_of[g]] += -f * (int(a[g, 0]) * prod(b, others) - int(b[g, 0]) * prod(a, others))
            share[train_of[g]] += -f * (int(a1[g, 0]) * prod(a, others) - int(a[g, 0]) * prod(a1, others))
        for t in range(len(out)):
            out[t] -= share[t]
        held_side = [g for g in values if train_of[g] in held_t]
        other_side = [g for g in values if train_of[g] not in held_t]
        p = 1
        for g in other_side:
            p *= int(a[g, 0])
        q1 = q0 = 1
        for g in held_side:
            q1 *= int(a1[g, 0])
            q0 *= int(b[g, 0])
        s_held = -2 * f * p * (q1 - q0)
        out[train_of[held_side[0]]] += s_held
        out[train_of[other_side[0]]] -= s_held
    return out


open_act = open_bg = 0
first_act = first_bg = None
norms = []
for t in range(1, ROUNDS + 1):
    s1 = step.tick(lay, s)
    act = act_passing(s.b, s.a, s1.a)
    bg = background(s.b, s.a, s1.a, act)
    if sum(act) != 0:
        open_act += 1
        first_act = t if first_act is None else first_act
    if sum(bg) != 0:
        open_bg += 1
        first_bg = t if first_bg is None else first_bg
    hr = [r for r in range(rows) if train_of[r] in held_t]
    norms.append(sum(int(s1.a[r, 0]) ** 2 for r in hr))
    s = s1
print(f"{ROUNDS} rounds: the act's passing opens the books in {open_act} (first at round {first_act}); the background form"
      f" in {open_bg} (first at {first_bg}); the held hand's |k|^2 from {min(norms)} to {max(norms)}")
