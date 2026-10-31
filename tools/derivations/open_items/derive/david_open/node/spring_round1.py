"""NOT_CLOSED 29 on the head (node-live 1794d474b): where the click world's one-sided passing comes from, and what the
split at the rest books for it. Whole numbers alone, every division Rule3's carry.

The world is examples/tensor24-click as the loader lays it from its three files; nothing is typed. Each round the real
act steps the board, and at every Node-clock the probe reads each train's passing as the act books it (step.passing
on both windows, (a, b) and (a+, a), as step.act sums them), and splits it by the kind of value-leg monomial the
loader laid: own (every value leg in one train: the held rows' own springs), two-leg between two trains (the hands'
tie), and the tie groups (four value legs joining the held train to one tied train). Beside it, the split at the rest
(NOT_CLOSED 29's section 2.4 at kappa 6, n = 0: writer D's world lays no hat, and its own spring and tie are least at
k = 0), per train and as flows per pair of trains. Node-clocks reading alike are printed once, with their count.
Then, over a longer run, at every place: the act's passing summed over the trains (the books' miss) against each
kind's sum, and each Node-clock's running miss. With the word spring0 the universe's CHOSEN spring is read as 0
(plans.holding: 0 lays none), in memory only, to read the world with the held rows' own spring off.

Usage: python3 -I spring_round1.py <src of node-live at 1794d474b> [rounds read place by place, 2 unless given]
[rounds summed, 200 unless given] [spring0]   (the example files are read from <src>/../examples/tensor24-click)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import contract  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

UNIT = -1
KAPPA = 6


def value(row, x):
    return 1 if row == UNIT else x[row]


def prod(xs):
    p = 1
    for v in xs:
        p *= v
    return p


src = Path(sys.argv[1])
ex = src.parent.joinpath("examples", "tensor24-click")
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
summed = int(sys.argv[3]) if len(sys.argv) > 3 else 200
universe = json.loads(ex.joinpath("universe.json").read_text())
if "spring0" in sys.argv[4:]:
    universe["chosen"]["spring"] = 0
shape = json.loads(ex.joinpath("piece.json").read_text())["shape"]
setting = json.loads(ex.joinpath("setting.json").read_text())
held, found = loading.load(universe, setting, sites_of(shape), *main.made(loading.star(len(shape))))
assert found == [] and held is not None
lay = main.layout(universe, shape, held)
s = state_mod.State(*held.state)
rows, sites = s.a.shape
tr = held.trains
firsts = [int(x) for x in tr.first] + [rows]
ntr = len(tr.first)
train_of = []
for t in range(ntr):
    train_of += [t] * (firsts[t + 1] - firsts[t])
held_rows = [r for r in range(rows) if int(tr.held[train_of[r]])]
held_t = train_of[held_rows[0]]
factor, legs = held.potential
terms = [(int(factor[i]), tuple(int(legs[j][i]) for j in range(4))) for i in range(len(factor)) if int(factor[i]) != 0]
kinds = {"own": [], "two-leg": [], "tie": []}
groups = {}
for f, lg in terms:
    vals = [h for h in lg if h != UNIT]
    owners = {train_of[h] for h in vals}
    if len(owners) == 1:
        kinds["own"].append((f, lg))
    elif len(vals) == 2:
        kinds["two-leg"].append((f, lg))
    else:
        kinds["tie"].append((f, lg))
        hl = [h for h in vals if train_of[h] == held_t]
        tied = tuple(sorted(h for h in vals if train_of[h] != held_t))
        assert len(vals) == 4 and len(hl) == 2 and hl[0] == hl[1], lg
        groups.setdefault((f, tied), set()).add(hl[0])
chosen = universe["chosen"]
print(f"tensor24-click on the src given: {sites} Node-clocks, trains 0 to {ntr - 1}, rows per train"
      f" {[firsts[t + 1] - firsts[t] for t in range(ntr)]}, the held train {held_t} on rows {held_rows}; CHOSEN spring"
      f" {chosen.get('spring')}, tie {chosen.get('tie')}, hold {chosen.get('hold')}")
for k, v in kinds.items():
    joined = sorted({tuple(sorted({train_of[h] for h in lg if h != UNIT})) for _, lg in v})
    print(f"  {k} monomials: {len(v)}, factors {sorted({f for f, _ in v})}, trains joined {joined}")
for f, lg in kinds["own"]:
    print(f"    own: factor {f}, legs {lg}")


def act_x(x, y, tl):
    """The act's form x J(y) - y J(x) per train on the monomials tl, J the value legs' push."""
    out = [0] * ntr
    for f, lg in tl:
        for i, g in enumerate(lg):
            if g == UNIT:
                continue
            oy = prod(value(h, y) for k, h in enumerate(lg) if k != i)
            ox = prod(value(h, x) for k, h in enumerate(lg) if k != i)
            out[train_of[g]] += -f * (x[g] * oy - y[g] * ox)
    return out


def split(b, a, a1):
    """The split at the rest at kappa 6, n = 0: per train, and the flows into the first train of each pair."""
    out, flows = [0] * ntr, {}
    half, third = carry(KAPPA, 2, 0)[0], carry(KAPPA, 3, 0)[0]
    for f, lg in kinds["two-leg"]:
        w = [0] * ntr
        for i, g in enumerate(lg):
            if g == UNIT:
                continue
            w[train_of[g]] += -f * prod(value(h, a) for k, h in enumerate(lg) if k != i) * (a1[g] - b[g])
        t1, t2 = sorted({train_of[h] for h in lg if h != UNIT})
        out[t1] += half * (w[t1] - w[t2])
        out[t2] += half * (w[t2] - w[t1])
        flows[(t1, t2)] = flows.get((t1, t2), 0) + half * (w[t1] - w[t2])
    for (c, tied), hrows in sorted(groups.items()):
        assert hrows == set(held_rows)
        p = prod(a[h] for h in tied)
        w_held = sum(-2 * c * p * a[r] * (a1[r] - b[r]) for r in held_rows)
        e = sum(a[r] * a[r] for r in held_rows)
        w_tied = sum(-c * prod(a[g] for k, g in enumerate(tied) if k != i) * e * (a1[h] - b[h])
                     for i, h in enumerate(tied))
        s_held = third * (2 * w_held - w_tied)
        out[held_t] += s_held
        out[train_of[tied[0]]] -= s_held
        pr = (held_t, train_of[tied[0]])
        flows[pr] = flows.get(pr, 0) + s_held
    return out, flows


_, _, _, _, _, plan, _, _, click, _, _ = lay
for t in range(1, rounds + 1):
    s1, _ = step.act(lay, s)
    jb, ja, ja1 = (contract(plan, step.valued(s.b), s.b), contract(plan, step.valued(s.a), s.a),
                   contract(plan, step.valued(s1.a), s1.a))
    moved = step.passing(click, s.a, s.b, ja, jb) + step.passing(click, s1.a, s.a, ja1, ja)
    alike = {}
    for x in range(sites):
        b = [int(s.b[r, x]) for r in range(rows)]
        a = [int(s.a[r, x]) for r in range(rows)]
        a1 = [int(s1.a[r, x]) for r in range(rows)]
        mv = tuple(int(moved[i, x]) for i in range(ntr))
        parts = tuple((k, tuple(u + w for u, w in zip(act_x(a, b, v), act_x(a1, a, v)))) for k, v in kinds.items())
        assert tuple(sum(p[i] for _, p in parts) for i in range(ntr)) == mv
        sp, fl = split(b, a, a1)
        hand = (tuple(b[r] for r in held_rows), tuple(a[r] for r in held_rows), tuple(a1[r] for r in held_rows))
        giver = tuple(a[r] for r in range(firsts[3], firsts[4]))
        line = (mv, parts, tuple(sp), tuple(sorted(fl.items())), hand, giver)
        alike[line] = alike.get(line, 0) + 1
    for (mv, parts, sp, fl, hand, giver), count in sorted(alike.items()):
        print(f"round {t}, {count} Node-clocks alike: the act's passing per train {list(mv)} (summed {sum(mv)}),"
              f" by kind: " + "; ".join(f"{k} {list(p)}" for k, p in parts))
        print(f"    the held hand before, now, next {hand}; the giver's rows now {giver}")
        print(f"    the split at the rest (kappa 6, n = 0): per train {list(sp)} (summed {sum(sp)}); flows into the"
              f" first train of each pair {dict(fl)}")
    s = s1

s = state_mod.State(*held.state)
key = int(lay.click.key[0, 0])
miss_places = 0
kind_off = {k: 0 for k in kinds}
equal = 0
running = [0] * sites
widest = 0
for t in range(1, summed + 1):
    s1, _ = step.act(lay, s)
    jb, ja, ja1 = (contract(plan, step.valued(s.b), s.b), contract(plan, step.valued(s.a), s.a),
                   contract(plan, step.valued(s1.a), s1.a))
    moved = step.passing(click, s.a, s.b, ja, jb) + step.passing(click, s1.a, s.a, ja1, ja)
    for x in range(sites):
        b = [int(s.b[r, x]) for r in range(rows)]
        a = [int(s.a[r, x]) for r in range(rows)]
        a1 = [int(s1.a[r, x]) for r in range(rows)]
        miss = sum(int(moved[i, x]) for i in range(ntr))
        sums = {k: sum(act_x(a, b, v)) + sum(act_x(a1, a, v)) for k, v in kinds.items()}
        miss_places += int(miss != 0)
        for k in kinds:
            kind_off[k] += int(sums[k] != 0)
        equal += int(miss == sums["tie"])
        running[x] += miss
        widest = max(widest, abs(running[x]))
    s = s1
print(f"over {summed} rounds at {sites} Node-clocks: the act's passing summed over the trains (the books' miss) not 0 at"
      f" {miss_places} of {summed * sites} places; each kind's sum not 0 at: " + ", ".join(f"{k} {v}" for k, v in
      kind_off.items()) + f"; the miss equal to the tie groups' sum at {equal} of {summed * sites} places; a"
      f" Node-clock's running miss at most {widest}, against the key {key}")

