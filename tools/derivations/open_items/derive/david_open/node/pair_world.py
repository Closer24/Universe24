"""NOT_CLOSED 29 on B4's pair world (tests/test_the_tensor24_run.py's own files): the act's passing against the background
form, summed over the trains, round by round, through the real loader and act of node-live 575973a20.

The world: one Node-clock; the held hand (A1, A2) at part 1 laid (1, 0) turning, a (T1, T2) giver at rest at 32, a
(T1, T2) taker gliding a count a round; hold 1, the hands' tie 1200, the key 76801. The plan's monomials are read back
from the plan as contract.pushes lays them (four entries per monomial, the first block's target the first leg). The
act's passing per train is step.passing's own form on the value legs' plan, X(a, b) + X(a+, a). The background form:
each monomial joining the held train to one other train books S_held = -2 c P(a) (Q(a+) - Q(b)) and S_other = -S_held;
two-leg monomials keep the act's form, and a train's own monomials book nothing (here they are the held hand's own
two-leg springs, on which the act's form gives 0 at every window). Printed: the rounds whose passings over the trains
do not sum to 0, for each form, and the held hand's |k|^2 over the run. The third text's split at the rest is
measured on this world by split4.py beside it.

Usage: python3 -I pair_world.py <src of node-live at 575973a20> [rounds, 400 unless given]
(B4's world is read from the run test, <src>/../tests/test_the_tensor24_run.py, at the same commit)
"""

import ast
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state, step  # noqa: E402
from tensor24.engine.contract import contract  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402


def b4_world(src):
    """B4's pair world as the engine's run test lays it (tests/test_the_tensor24_run.py beside the src), read from the
    test's own statements from its den to its gears, so this probe types no train: the test's world and its gears."""
    tree = ast.parse(Path(src).parent.joinpath("tests", "test_the_tensor24_run.py").read_text(encoding="utf-8"))

    def named(node, name):
        return isinstance(node, ast.Assign) and [getattr(t, "id", None) for t in node.targets] == [name]

    laying = [f for f in ast.walk(tree) if isinstance(f, ast.FunctionDef) and any(named(a, "hand") for a in f.body)]
    if len(laying) != 1:
        raise ValueError(f"the run test lays the held hand in {len(laying)} functions, not one")
    body = laying[0].body
    at = next(i for i, a in enumerate(body) if named(a, "hand"))
    start = max(i for i in range(at) if named(body[i], "den"))
    end = next(i for i in range(at, len(body)) if named(body[i], "gears"))
    names = {}

    def value(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return names[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -value(node.operand)
        if isinstance(node, ast.List):
            return [value(e) for e in node.elts]
        if isinstance(node, ast.Dict):
            out = {}
            for k, v in zip(node.keys, node.values, strict=True):
                out.update(value(v) if k is None else {value(k): value(v)})
            return out
        raise ValueError(f"not a plain value in the test's world: {ast.dump(node)}")

    for a in body[start : end + 1]:
        if not (isinstance(a, ast.Assign) and len(a.targets) == 1 and isinstance(a.targets[0], ast.Name)):
            raise ValueError(f"not a plain assignment in the test's world: {ast.unparse(a)}")
        names[a.targets[0].id] = value(a.value)
    return names["world"], names["gears"]

ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 400
universe, gears = b4_world(sys.argv[1])  # B4's world and gears, read from the run test that lays them
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
four = [(f, legs) for f, legs in monomials if all(x >= 0 for x in legs)]
joining = [(f, legs) for f, legs in four
           if len({train_of[g] for g in legs}) == 2 and {train_of[g] for g in legs} & set(held_t)]
live_four = [(f, legs) for f, legs in four if f != 0]
live_joining = [(f, legs) for f, legs in joining if f != 0]
print(f"monomials: {m}; four value legs: {len(four)}; of them joining the held train to one other: {len(joining)}")
print(f"  their factors: four-leg monomials live (factor not 0) {len(live_four)}, joining and live {len(live_joining)}"
      f" at the factors {sorted({f for f, _ in live_joining})}; every live four-leg monomial joins the held train to"
      f" one other: {len(live_four) == len(live_joining)}")


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
