"""NOT_CLOSED 29: the split at the rest on writer D's click world (node-live 36fbfbbde: the held rows' own spring
CHOSEN in the universe file, K = 2 W gone), whole numbers alone, every division Rule3's carry.

The world is examples/tensor24-click as the loader lays it from its three files; nothing is typed. Each round the
real act steps the whole board; at every Node-clock the probe books, per train, the act's own clicks and, beside them,
the split at the rest (the work form of NOT_CLOSED 29's sections 2 and 12: two-leg monomials at alpha 1/2, own
monomials nothing, each tie group's value at the rest c n P the tied train's own and its excursion c P (|k|^2 - n)
shared 1/3 to the held train and 2/3 to the tied one, at kappa 6), carried by each train's own click tooth at the key
times 3, born at its middle. It reads the books two ways at every place (Node-clock, round): the passing summed over
the trains (S), and the clicks summed over the trains (q), the decoder's reading. Beside them, Big Pic's check
(#2187 6538018966 item 4): the held pair's charge sigma = a_1 b_2 - a_2 b_1 over its two held rows, and the rounds
where it moves. Third, the same split with its clicks carried pair by pair: one tooth per pair of trains the split
joins (a click is two clocks connecting), each pair's two trains clicking opposite quotients. Why the clicks balance
where they do: two trains whose passings are opposite and whose teeth sum to the
key times 3 less 1 (each born at the middle of an odd key, (3 key - 1) div 2) click opposite quotients and keep their
teeth so; so the probe counts the trains clicking at each click place and the places where the teeth's sum leaves its
birth sum (the clicks summed are 0 at a place exactly when the teeth's sum stands there, the passings summing to 0).

n: writer D's world lays no hat. Two values are read: n = 0, where the world's own spring and tie are least, and n
the held hand's |k|^2 as the setting lays it at each Node-clock's first round, read from the state.

Usage: python3 -I split_d.py <src of node-live at 36fbfbbde> [rounds, the setting's ticks unless given] [world folder,
tensor24-click unless given]   (the example files are read from <src>/../examples/<world>)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
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


class World:
    """One Node-clock's value-leg monomials sorted by the trains their legs lie in: own, two-leg between two trains,
    and tie groups (four value legs joining the held train to one other, the held legs one row squared, one group per
    tied legs and factor covering every held row); the split at the rest and the act's own X on them."""

    def __init__(self, terms, train_of, held_rows):
        self.terms = [(f, tuple(legs)) for f, legs in terms if f != 0]
        self.train_of = train_of
        self.trains = sorted(set(train_of))
        self.held_rows = tuple(held_rows)
        held = {train_of[r] for r in held_rows}
        assert len(held) == 1
        self.held_t = next(iter(held))
        self.own, self.two, groups = [], [], {}
        for f, legs in self.terms:
            vals = [h for h in legs if h != UNIT]
            owners = {train_of[h] for h in vals}
            if len(owners) == 1:
                self.own.append((f, legs))
            elif len(vals) == 2:
                self.two.append((f, legs))
            else:
                held_legs = [h for h in vals if train_of[h] == self.held_t]
                tied_legs = tuple(sorted(h for h in vals if train_of[h] != self.held_t))
                assert len(vals) == 4 and len(owners) == 2 and self.held_t in owners, legs
                assert len(held_legs) == 2 and held_legs[0] == held_legs[1], legs
                groups.setdefault((f, tied_legs), set()).add(held_legs[0])
        for key, rows in groups.items():
            assert rows == set(self.held_rows), (key, rows)
        self.groups = sorted(groups)

    def work(self, legs, f, b, a, a1):
        out = {t: 0 for t in self.trains}
        for i, g in enumerate(legs):
            if g == UNIT:
                continue
            j = -f * prod(value(h, a) for k, h in enumerate(legs) if k != i)
            out[self.train_of[g]] += j * (a1[g] - b[g])
        return out

    def excursion_work(self, c, tied, n, b, a, a1):
        p = prod(a[h] for h in tied)
        w_held = 0
        for r in self.held_rows:
            w_held += -2 * c * p * a[r] * (a1[r] - b[r])
        e = sum(a[r] * a[r] for r in self.held_rows) - n
        w_tied = 0
        for i, h in enumerate(tied):
            other = prod(a[g] for k, g in enumerate(tied) if k != i)
            w_tied += -c * other * e * (a1[h] - b[h])
        return w_held, w_tied

    def split_s(self, n, b, a, a1):
        out = {t: 0 for t in self.trains}
        half = carry(KAPPA, 2, 0)[0]
        for f, legs in self.two:
            w = self.work(legs, f, b, a, a1)
            t1, t2 = sorted({self.train_of[h] for h in legs if h != UNIT})
            out[t1] += half * (w[t1] - w[t2])
            out[t2] += half * (w[t2] - w[t1])
        third = carry(KAPPA, 3, 0)[0]
        for c, tied in self.groups:
            w_held, w_tied = self.excursion_work(c, tied, n, b, a, a1)
            s_held = third * (2 * w_held - w_tied)
            out[self.held_t] += s_held
            out[self.train_of[tied[0]]] -= s_held
        return out

    def split_flows(self, n, b, a, a1):
        """The same split as pair flows: per pair of trains (t1 < t2), what passes into t1 (t2 takes its negative)."""
        out = {}
        half = carry(KAPPA, 2, 0)[0]
        for f, legs in self.two:
            w = self.work(legs, f, b, a, a1)
            t1, t2 = sorted({self.train_of[h] for h in legs if h != UNIT})
            out[(t1, t2)] = out.get((t1, t2), 0) + half * (w[t1] - w[t2])
        third = carry(KAPPA, 3, 0)[0]
        for c, tied in self.groups:
            w_held, w_tied = self.excursion_work(c, tied, n, b, a, a1)
            s_held = third * (2 * w_held - w_tied)
            t1, t2 = sorted((self.held_t, self.train_of[tied[0]]))
            out[(t1, t2)] = out.get((t1, t2), 0) + (s_held if t1 == self.held_t else -s_held)
        return out

    def act_x(self, x, y, terms):
        out = {t: 0 for t in self.trains}
        for f, legs in terms:
            for i, g in enumerate(legs):
                if g == UNIT:
                    continue
                oy = prod(value(h, y) for k, h in enumerate(legs) if k != i)
                ox = prod(value(h, x) for k, h in enumerate(legs) if k != i)
                out[self.train_of[g]] += -f * (x[g] * oy - y[g] * ox)
        return out


src = Path(sys.argv[1])
world_dir = sys.argv[3] if len(sys.argv) > 3 else "tensor24-click"
ex = src.parent.joinpath("examples", world_dir)
universe = json.loads(ex.joinpath("universe.json").read_text())
shape = json.loads(ex.joinpath("piece.json").read_text())["shape"]
setting = json.loads(ex.joinpath("setting.json").read_text())
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else int(setting["ticks"])
held, found = loading.load(universe, setting, sites_of(shape), *main.made(loading.star(len(shape))))
assert found == [] and held is not None
lay = main.layout(universe, shape, held)
s = state_mod.State(*held.state)
rows, sites = s.a.shape
tr = held.trains
firsts = [int(x) for x in tr.first] + [rows]
train_of = []
for t in range(len(tr.first)):
    train_of += [t] * (firsts[t + 1] - firsts[t])
held_rows = [r for r in range(rows) if int(tr.held[train_of[r]])]
factor, legs = held.potential
terms = [(int(factor[i]), tuple(int(legs[j][i]) for j in range(4))) for i in range(len(factor))]
world = World(terms, train_of, held_rows)
ntr = len(world.trains)
key = int(lay.click.key[0, 0])
key3 = 3 * key
chosen = universe["chosen"]
print(f"{world_dir} on the src given: shape {shape}, {sites} Node-clocks, trains {world.trains} (held train"
      f" {world.held_t}, held rows {held_rows}), the CHOSEN key {key}, spring {chosen.get('spring')}, tie"
      f" {chosen.get('tie')}, hold {chosen.get('hold')}; value-leg monomials: own {len(world.own)}, two-leg between"
      f" trains {len(world.two)}, tie groups {len(world.groups)} (factors {sorted({c for c, _ in world.groups})});"
      f" {rounds} rounds")
n_lay = [sum(int(s.a[r, x]) ** 2 for r in held_rows) for x in range(sites)]
print(f"  the held hand's |k|^2 as laid, per Node-clock: from {min(n_lay)} to {max(n_lay)}")
forms = {"n = 0": [0] * sites, "n as laid": n_lay}
teeth = {k: [[carry(key3 - 1, 2, 0)[0]] * sites for _ in range(ntr)] for k in forms}
act_places = act_open = 0
born3 = carry(key3 - 1, 2, 0)[0]
pairs = sorted({tuple(sorted({train_of[h] for h in lg if h != UNIT})) for _, lg in world.two}
               | {tuple(sorted((world.held_t, train_of[td[0]]))) for _, td in world.groups})
pair_teeth = {k: {pr: [born3] * sites for pr in pairs} for k in forms}
pq_places = {k: 0 for k in forms}
pq_open = {k: 0 for k in forms}
pq_held = {k: 0 for k in forms}
pq_flow_off = {k: 0 for k in forms}
clicking = {k: {} for k in forms}
teeth_off = {k: 0 for k in forms}
s_open = {k: 0 for k in forms}
q_places = {k: 0 for k in forms}
q_open = {k: 0 for k in forms}
held_fires = {k: 0 for k in forms}
two_ok = two_n = 0
sigma_moves = 0
held_act_fires = 0
r1, r2 = held_rows[0], held_rows[1]
for t in range(1, rounds + 1):
    s1, act_clicks = step.act(lay, s)
    for x in range(sites):
        b = [int(s.b[r, x]) for r in range(rows)]
        a = [int(s.a[r, x]) for r in range(rows)]
        a1 = [int(s1.a[r, x]) for r in range(rows)]
        qa = [int(act_clicks[i, x]) for i in range(ntr)]
        if any(qa):
            act_places += 1
            act_open += int(sum(qa) != 0)
        held_act_fires += int(qa[world.held_t] != 0)
        if t <= 200:
            for f, lg in world.two:
                w = world.work(lg, f, b, a, a1)
                u = world.act_x(a, b, [(f, lg)])
                v = world.act_x(a1, a, [(f, lg)])
                t1, t2 = sorted({train_of[h] for h in lg if h != UNIT})
                two_n += 1
                two_ok += int(u[t1] + v[t1] == w[t1] - w[t2] and u[t2] + v[t2] == w[t2] - w[t1])
        sig0 = a[r1] * b[r2] - a[r2] * b[r1]
        sig1 = a1[r1] * a[r2] - a1[r2] * a[r1]
        sigma_moves += int(sig1 != sig0)
        for k, ns in forms.items():
            sp = world.split_s(ns[x], b, a, a1)
            s_open[k] += int(sum(sp.values()) != 0)
            q = []
            for i in range(ntr):
                c_, teeth[k][i][x] = carry(sp[world.trains[i]], key3, teeth[k][i][x])
                q.append(c_)
            if any(q):
                q_places[k] += 1
                q_open[k] += int(sum(q) != 0)
                m = sum(1 for v in q if v)
                clicking[k][m] = clicking[k].get(m, 0) + 1
            teeth_off[k] += int(sum(teeth[k][i][x] for i in range(ntr)) != ntr * born3)
            fl = world.split_flows(ns[x], b, a, a1)
            back = {t: 0 for t in world.trains}
            for pr, v in fl.items():
                back[pr[0]] += v
                back[pr[1]] -= v
            pq_flow_off[k] += int(back != sp)
            qp = {t: 0 for t in world.trains}
            for pr in pairs:
                c_, pair_teeth[k][pr][x] = carry(fl.get(pr, 0), key3, pair_teeth[k][pr][x])
                qp[pr[0]] += c_
                qp[pr[1]] -= c_
            if any(qp.values()):
                pq_places[k] += 1
                pq_open[k] += int(sum(qp.values()) != 0)
            pq_held[k] += int(qp[world.held_t] != 0)
            held_fires[k] += int(q[world.held_t] != 0)
    s = s1
total = rounds * sites
print(f"  the two-leg law: the work form at kappa 2 equals the act's X in {two_ok} of {two_n} (monomial, Node-clock,"
      f" round) cases over the first 200 rounds")
print(f"  the act as built (its own clicks at the key): places with a click {act_places} of {total}; the books open"
      f" (the clicks summed over the trains not 0) at {act_open} of them; the held train clicking at {held_act_fires}"
      f" places")
for k in forms:
    print(f"  the split at the rest, {k}, kappa 6, the key times 3: the passing summed over the trains not 0 at"
          f" {s_open[k]} of {total} places; places with a click {q_places[k]}, the books open (the clicks summed not"
          f" 0) at {q_open[k]} of them; the held train clicking at {held_fires[k]} places; trains clicking per click"
          f" place {dict(sorted(clicking[k].items()))}; places where the trains' teeth summed are off their birth sum"
          f" {teeth_off[k]}")
for k in forms:
    print(f"  the split at the rest, {k}, its clicks carried pair by pair (one tooth per pair of trains the split"
          f" joins, {pairs}, each born at the middle, the pair's two trains clicking opposite quotients): the flows"
          f" summed back per train differ from the split's passing at {pq_flow_off[k]} places; places with a click"
          f" {pq_places[k]}, the books open at {pq_open[k]} of them; the held train clicking at {pq_held[k]} places")
print(f"  Big Pic's check: the held pair's charge sigma = a_1 b_2 - a_2 b_1 moves at {sigma_moves} of {total} places")
