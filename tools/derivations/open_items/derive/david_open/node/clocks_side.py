"""The clocks' side of the third click (the Boss's #2187 6539961086 item 2), on the click world as the loader lays it.
Whole numbers alone, every division Rule3's carry.

At every Node-clock and round the real act steps the board, and the probe books NOT_CLOSED 29's split at the rest as one
flow per pair of trains it joins (n = 0, as section 14 rules for writer D's world), each edge carried by its pair of
teeth at the dial K, the key times 3, born at its middle: the lower end's tooth t carries the flow x into the lower
train, t + x = q K + r, and the higher end clicks -q (section 14's pair carry). Between the carries a turn writes the
next tooth r + d at each edge, with no wrap dropped. Three turns are read:
- none: d = 0, the first click;
- along the circulation: d = C w, w for each triangle the centred remainder of the triangle's own circulating passing
  (the board's own number), C each edge's sign on the triangle's boundary, [j, k] - [i, k] + [i, j];
- per edge: d_e the centred remainder of the edge's own passing, edge by edge.
At every clock and round it checks the identity K x (the clock's booked total) = (its swept passing) + B (the teeth at
the birth less now) + B (every d so far), B each clock's sign on each edge (+1 at the lower end, -1 at the higher),
and it reports each clock's largest |K booked - swept| against its teeth's range.

With Big Pic's three_clicks folder given (bigpic-3clicks, mode 11 in circ.py), it also compares the clocks' lines of
his first click (mode 0) and his triangle's own tooth (mode 11), and of mode 11 with one hidden unit in the triangle's
twin at Node-clock 0, through his own code.

Usage: python3 -I clocks_side.py <src of node-live at 1794d474b> [rounds, 200 unless given] [Big Pic's three_clicks
folder]   (the example files are read from <src>/../examples/tensor24-click)
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
    """NOT_CLOSED 29's split as pair flows (split_d.py's own form): two-leg monomials at alpha 1/2, each tie group's
    excursion 1/3 to the held train and 2/3 to the tied one, at kappa 6; a train's own monomials pass nothing."""

    def __init__(self, terms, train_of, held_rows):
        self.train_of = train_of
        self.held_rows = tuple(held_rows)
        self.held_t = train_of[held_rows[0]]
        self.two, groups = [], {}
        for f, legs in terms:
            vals = [h for h in legs if h != UNIT]
            owners = {train_of[h] for h in vals}
            if len(owners) == 1:
                continue
            if len(vals) == 2:
                self.two.append((f, legs))
                continue
            held_legs = [h for h in vals if train_of[h] == self.held_t]
            tied = tuple(sorted(h for h in vals if train_of[h] != self.held_t))
            assert len(vals) == 4 and len(held_legs) == 2 and held_legs[0] == held_legs[1], legs
            groups.setdefault((f, tied), set()).add(held_legs[0])
        for key, rows in groups.items():
            assert rows == set(self.held_rows), key
        self.groups = sorted(groups)

    def flows(self, b, a, a1):
        out = {}
        half, third = carry(KAPPA, 2, 0)[0], carry(KAPPA, 3, 0)[0]
        for f, legs in self.two:
            w = {}
            for i, g in enumerate(legs):
                if g == UNIT:
                    continue
                j = -f * prod(value(h, a) for k, h in enumerate(legs) if k != i)
                w[self.train_of[g]] = w.get(self.train_of[g], 0) + j * (a1[g] - b[g])
            t1, t2 = sorted(w)
            out[(t1, t2)] = out.get((t1, t2), 0) + half * (w[t1] - w[t2])
        for c, tied in self.groups:
            p = prod(a[h] for h in tied)
            w_held = sum(-2 * c * p * a[r] * (a1[r] - b[r]) for r in self.held_rows)
            e = sum(a[r] * a[r] for r in self.held_rows)
            w_tied = sum(-c * prod(a[g] for k, g in enumerate(tied) if k != i) * e * (a1[h] - b[h])
                         for i, h in enumerate(tied))
            s_held = third * (2 * w_held - w_tied)
            t1, t2 = sorted((self.held_t, self.train_of[tied[0]]))
            out[(t1, t2)] = out.get((t1, t2), 0) + (s_held if t1 == self.held_t else -s_held)
        return out


src = Path(sys.argv[1])
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 200
ex = src.parent.joinpath("examples", "tensor24-click")
universe = json.loads(ex.joinpath("universe.json").read_text())
shape = json.loads(ex.joinpath("piece.json").read_text())["shape"]
setting = json.loads(ex.joinpath("setting.json").read_text())
held, found = loading.load(universe, setting, sites_of(shape), *main.made(loading.star(len(shape))))
assert found == [] and held is not None
lay = main.layout(universe, shape, held)
s0 = state_mod.State(*held.state)
rows, sites = s0.a.shape
tr = held.trains
firsts = [int(x) for x in tr.first] + [rows]
train_of = []
for t in range(len(tr.first)):
    train_of += [t] * (firsts[t + 1] - firsts[t])
held_rows = [r for r in range(rows) if int(tr.held[train_of[r]])]
factor, legs = held.potential
terms = [(int(factor[i]), tuple(int(legs[j][i]) for j in range(4))) for i in range(len(factor)) if int(factor[i]) != 0]
world = World(terms, train_of, held_rows)
pairs = sorted({tuple(sorted({train_of[h] for h in lg if h != UNIT})) for _, lg in world.two}
               | {tuple(sorted((world.held_t, train_of[td[0]]))) for _, td in world.groups})
clocks = sorted({v for pr in pairs for v in pr})
index = {pr: e for e, pr in enumerate(pairs)}
triangles = [(i, j, k) for i in clocks for j in clocks for k in clocks if i < j < k
             and (i, j) in index and (i, k) in index and (j, k) in index]
C = [{index[(j, k)]: 1, index[(i, k)]: -1, index[(i, j)]: 1} for i, j, k in triangles]
B = {v: {e: (1 if pr[0] == v else -1) for e, pr in enumerate(pairs) if v in pr} for v in clocks}
key = int(lay.click.key[0, 0])
K = 3 * key
born, _ = carry(K - 1, 2, 0)
bc = [[sum(B[v].get(e, 0) * C[f].get(e, 0) for e in range(len(pairs))) for f in range(len(triangles))] for v in clocks]
print(f"tensor24-click on the src given: {sites} Node-clocks, {rounds} rounds; edges {pairs}; triangles {triangles};"
      f" the dial K = 3 x key = {K}, the birth {born}; B C at every clock and triangle: {bc}")


def centred(v):
    _, r = carry(v + born, K, 0)
    return r - born


for mode in ("none", "circulation", "per edge"):
    s = s0
    teeth = [[born] * len(pairs) for _ in range(sites)]
    booked = [{v: 0 for v in clocks} for _ in range(sites)]
    swept = [{v: 0 for v in clocks} for _ in range(sites)]
    moved = [{v: 0 for v in clocks} for _ in range(sites)]
    off = widest = 0
    for _ in range(rounds):
        s1, _ = step.act(lay, s)
        for x in range(sites):
            b = [int(s.b[r, x]) for r in range(rows)]
            a = [int(s.a[r, x]) for r in range(rows)]
            a1 = [int(s1.a[r, x]) for r in range(rows)]
            fl = world.flows(b, a, a1)
            xs = [fl.get(pr, 0) for pr in pairs]
            t = teeth[x]
            for e, pr in enumerate(pairs):
                q, t[e] = carry(xs[e], K, t[e])
                booked[x][pr[0]] += q
                booked[x][pr[1]] -= q
                swept[x][pr[0]] += xs[e]
                swept[x][pr[1]] -= xs[e]
            if mode == "circulation":
                d = [0] * len(pairs)
                for f in range(len(triangles)):
                    w = centred(sum(sg * xs[e] for e, sg in C[f].items()))
                    for e, sg in C[f].items():
                        d[e] += sg * w
            elif mode == "per edge":
                d = [centred(v) for v in xs]
            else:
                d = [0] * len(pairs)
            for e in range(len(pairs)):
                t[e] += d[e]
            for v in clocks:
                moved[x][v] += sum(B[v][e] * d[e] for e in B[v])
                left = K * booked[x][v] - swept[x][v]
                right = sum(B[v][e] * (born - t[e]) for e in B[v]) + moved[x][v]
                off += int(left != right)
                widest = max(widest, abs(left))
        s = s1
    end = {v: max(abs(moved[x][v]) for x in range(sites)) for v in clocks}
    print(f"  turn {mode}: the identity off at {off} of {rounds * sites * len(clocks)} (clock, Node-clock, round) places;"
          f" each clock's largest |K booked - swept| {widest}, against two teeth's range {2 * (K - 1)}; each clock's"
          f" largest |B (every d)| at the end {end}")

if len(sys.argv) > 3:
    sys.path.insert(0, sys.argv[3])
    import edgeclick  # noqa: E402

    def per(lines):
        return {(t, x, v): q for t, x, v, q in lines}

    first = edgeclick.run(str(src), "tensor24-click", rounds, 0)
    third = edgeclick.run(str(src), "tensor24-click", rounds, 11)
    hidden = edgeclick.run(str(src), "tensor24-click", rounds, 11, hidden=(0, 0))
    a, b, c = per(first["lines"]), per(third["lines"]), per(hidden["lines"])
    differ = sum(1 for k in set(a) | set(b) if a.get(k, 0) != b.get(k, 0))
    hid = sum(1 for k in set(b) | set(c) if b.get(k, 0) != c.get(k, 0))
    totals = {}
    for (t, x, v), q in a.items():
        totals[(x, v)] = totals.get((x, v), 0) + q
    for (t, x, v), q in b.items():
        totals[(x, v)] = totals.get((x, v), 0) - q
    print(f"  Big Pic's code, {rounds} rounds: clock lines (round, Node-clock, train), the first click {len(a)}, mode 11"
          f" {len(b)}; differing round by round {differ}; each clock's total, the first click less mode 11, from"
          f" {min(totals.values())} to {max(totals.values())}; mode 11 with one hidden unit in the triangle's twin at"
          f" Node-clock 0: lines differing {hid}, sides differing {len(set(third['sides']) ^ set(hidden['sides']))};"
          f" books open {first['books_open']}, {third['books_open']}, {hidden['books_open']}; run back"
          f" {first['runback']}, {third['runback']}, {hidden['runback']}")
