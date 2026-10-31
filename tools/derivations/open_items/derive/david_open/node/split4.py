"""NOT_CLOSED 29, the third text: the split at the rest (Big Pic's road, #2187 6536112029 item 1), on the act
(node-live 575973a20), whole numbers alone.

The passing in the work form. For a monomial m and a train A: W_A = SUM over A's legs of the leg's push at the now
slot times its count's change over the window, J_g(a) (a+_g - b_g), with J_g = -f (the product of the other legs);
W = SUM over the trains; S_A = kappa (W_A - alpha_A W), alpha_A the train's share of the monomial's energy, SUM_A
alpha_A = 1. So the books close monomial by monomial, and S is odd under the window's reversal, since J(a) stands
and a+ - b changes sign.
- A two-leg monomial between two trains, alpha 1/2: S_A = (kappa / 2) (W_A - W_B), the act's own two-leg passing at
  kappa 2 (checked in (a)).
- A train's own monomial, alpha 1: nothing passes.
- The split at the rest. A tie group c P |k|^2, P the tied legs' product and |k|^2 the held rows' squares summed over
  every held row at one factor, is its value at the rest, c n P, the tied train's own (nothing passes), and the
  excursion c P (|k|^2 - n), shared with the excursion as one leg: alpha 2/3 to the tied train (its two legs), 1/3 to
  the held train. At kappa 6, one scale with the two-leg passing times 3: S_held = 4 W_held - 2 W_tied of the
  excursion, S_tied = -S_held.
- For reference, the page's forms: the act's (step.passing's X, four-leg monomials included), the background form
  (S_held = -2 c P(a) (Q(a+) - Q(b))), the middle form by halves at weight 4 / d, and the middle split in the work form
  (alpha 1/2 for the whole tie at kappa 6), which is the split with the excursion shared over the k rows instead.

Sections:
(a) the two-leg law: the work form at kappa 2 against the act's X, monomial by monomial, on the pair world;
(b) passing4's three lays (the text's probe): books, oddness, the held passing, for every form;
(c) B4's pair world through the real loader and act: n read from the frame, the books, the clicks per train at the
    key times 3 against the act's at the key, in the run test's 30 ticks, in the room (rounds 1 to 56) and past it;
(d) the energy each form books: the decay (the physicist's p5 lay), the free particle over a still vacuum (his r7),
    the same free tied train at n = 5^10 + 1, off every square (the eighth text), a train holding both a tie and a
    two-leg spring (his r2), and lays (A) and (C) over the held hand's own excursion (his r1), each in units 96 W E;
(e) the click tooth's run back under the split, on lay (B) and on the pair world: the tooth kept at the end, as the
    mirror keeps it, and carried back over the reversed windows returns to its birth.

Usage: python3 -I split4.py <src of node-live at 575973a20>
(B4's world is read from the run test, <src>/../tests/test_the_tensor24_run.py, at the same commit)
"""

import ast
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import contract, pushes  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402


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

UNIT = -1
KEY = 5**5
N = KEY * KEY
NONE_I = np.zeros(0, dtype=np.intp)
NONE_O = np.zeros(0, dtype=object)
UNREAD = Read(NONE_I, NONE_O, NONE_I)
NOPLAN = Plan(NONE_I, NONE_I, NONE_I, NONE_O, NONE_I)
KAPPA = 6


def value(row, x):
    return 1 if row == UNIT else x[row]


def prod(xs):
    p = 1
    for v in xs:
        p *= v
    return p


def ppm(num, den):
    return carry(1000 * num, den, 0)[0] if den else 0


class World:
    """The monomials of a world sorted by the trains their value legs lie in: own, two-leg between two trains, and tie
    groups (four value legs joining the held train to one other, its held legs a row squared, one group per tied legs
    and factor covering every held row)."""

    def __init__(self, terms, train_of, held_rows, n):
        self.terms = [(f, tuple(legs)) for f, legs in terms if f != 0]
        self.train_of = train_of
        self.trains = sorted(set(train_of))
        self.held_rows = tuple(held_rows)
        self.held = {train_of[r] for r in held_rows}
        assert len(self.held) == 1
        self.held_t = next(iter(self.held))
        self.n = n
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
                assert len(vals) == 4 and len(owners) == 2 and self.held_t in owners
                assert len(held_legs) == 2 and held_legs[0] == held_legs[1], legs
                groups.setdefault((f, tied_legs), set()).add(held_legs[0])
        for key, rows in groups.items():
            assert rows == set(self.held_rows), (key, rows)
        self.groups = sorted(groups)  # (c, tied legs)

    def work(self, legs, f, b, a, a1):
        """Per train, W_A of one monomial: SUM over its value legs of J(a) (a+ - b)."""
        out = {t: 0 for t in self.trains}
        for i, g in enumerate(legs):
            if g == UNIT:
                continue
            j = -f * prod(value(h, a) for k, h in enumerate(legs) if k != i)
            out[self.train_of[g]] += j * (a1[g] - b[g])
        return out

    def excursion_work(self, c, tied, b, a, a1):
        """W_held and W_tied of the excursion c P (|k|^2 - n): the held rows' pushes are the tie's own, -2 c P(a) k_r;
        the tied legs' pushes carry |k|^2 - n at the now slot in place of |k|^2."""
        p = prod(a[h] for h in tied)
        w_held = 0
        for r in self.held_rows:
            w_held += -2 * c * p * a[r] * (a1[r] - b[r])
        e = sum(a[r] * a[r] for r in self.held_rows) - self.n
        w_tied = 0
        for i, h in enumerate(tied):
            other = prod(a[g] for k, g in enumerate(tied) if k != i)
            w_tied += -c * other * e * (a1[h] - b[h])
        return w_held, w_tied

    def split_s(self, b, a, a1, kappa=KAPPA):
        """The split at the rest, per train, at kappa (a multiple of 6 keeps it whole)."""
        out = {t: 0 for t in self.trains}
        for f, legs in self.two:
            w = self.work(legs, f, b, a, a1)
            t1, t2 = sorted({self.train_of[h] for h in legs if h != UNIT})
            half = carry(kappa, 2, 0)[0]
            out[t1] += half * (w[t1] - w[t2])
            out[t2] += half * (w[t2] - w[t1])
        third = carry(kappa, 3, 0)[0]
        for c, tied in self.groups:
            w_held, w_tied = self.excursion_work(c, tied, b, a, a1)
            s_held = third * (2 * w_held - w_tied)
            out[self.held_t] += s_held
            out[self.train_of[tied[0]]] -= s_held
        return out

    def work_middle_s(self, b, a, a1, kappa=KAPPA):
        """The middle split in the work form: each tie group shared 1/2 and 1/2 (the excursion shared over the k rows),
        two-leg as in the split."""
        out = {t: 0 for t in self.trains}
        half = carry(kappa, 2, 0)[0]
        for f, legs in self.two:
            w = self.work(legs, f, b, a, a1)
            t1, t2 = sorted({self.train_of[h] for h in legs if h != UNIT})
            out[t1] += half * (w[t1] - w[t2])
            out[t2] += half * (w[t2] - w[t1])
        for c, tied in self.groups:
            w = {t: 0 for t in self.trains}
            for r in self.held_rows:
                wr = self.work(tied + (r, r), c, b, a, a1)
                for t in self.trains:
                    w[t] += wr[t]
            th, tt = self.held_t, self.train_of[tied[0]]
            out[th] += half * (w[th] - w[tt])
            out[tt] += half * (w[tt] - w[th])
        return out

    def act_x(self, x, y, terms=None):
        """The act's X per train on (x, y), over the given monomials: SUM over positions of x_g J_g(y) - y_g J_g(x)."""
        out = {t: 0 for t in self.trains}
        for f, legs in (self.terms if terms is None else terms):
            for i, g in enumerate(legs):
                if g == UNIT:
                    continue
                oy = prod(value(h, y) for k, h in enumerate(legs) if k != i)
                ox = prod(value(h, x) for k, h in enumerate(legs) if k != i)
                out[self.train_of[g]] += -f * (x[g] * oy - y[g] * ox)
        return out

    def act_s(self, b, a, a1, terms=None):
        u, v = self.act_x(a, b, terms), self.act_x(a1, a, terms)
        return {t: u[t] + v[t] for t in self.trains}

    def background_s(self, b, a, a1):
        """The page's background form: two-leg as the act, own nothing; each tie monomial books
        S_held = -2 c P(a) (Q(a+) - Q(b))."""
        out = self.act_s(b, a, a1, self.two)
        for c, tied in self.groups:
            p = prod(a[h] for h in tied)
            sh = 0
            for r in self.held_rows:
                sh += -2 * c * p * (a1[r] * a1[r] - b[r] * b[r])
            out[self.held_t] += sh
            out[self.train_of[tied[0]]] -= sh
        return out

    def halves_middle_s(self, b, a, a1, terms=None):
        """The page's middle form by halves at weight 4 / d (twice the act's scale), every monomial or those given."""
        out = {t: 0 for t in self.trains}
        for f, legs in (self.terms if terms is None else terms):
            vals = [j for j, h in enumerate(legs) if h != UNIT]
            d = len(vals)
            half = carry(d, 2, 0)[0]
            weight = carry(4, d, 0)[0]
            subsets = [[]]
            for j in vals:
                subsets = subsets + [s + [j] for s in subsets]
            halves = [s for s in subsets if len(s) == half]
            for x, y in ((a, b), (a1, a)):
                for i in vals:
                    g = legs[i]
                    mxy = myx = 0
                    for s in halves:
                        if i not in s:
                            continue
                        pxy = pyx = 1
                        for j in vals:
                            if j == i:
                                continue
                            pxy *= x[legs[j]] if j in s else y[legs[j]]
                            pyx *= y[legs[j]] if j in s else x[legs[j]]
                        mxy += pxy
                        myx += pyx
                    out[self.train_of[g]] += -f * weight * (x[g] * mxy - y[g] * myx)
        return out

    def tie_terms(self):
        return [(c, tied + (r, r)) for c, tied in self.groups for r in self.held_rows]

    def middle_written_s(self, b, a, a1):
        """The second text's road as written: the act's two-leg passing, the ties by halves at weight 1."""
        out = self.act_s(b, a, a1, self.two)
        m = self.halves_middle_s(b, a, a1, self.tie_terms())
        return {t: out[t] + m[t] for t in self.trains}

    def potential12(self, x, mode):
        """12 V per train under a split: own whole; two-leg halved; each tie group by mode: 'bg' all to the tied train,
        'mid' halved, 'split' its value at the rest c n P to the tied train, the excursion 2/3 and 1/3."""
        out = {t: 0 for t in self.trains}
        for f, legs in self.own:
            out[self.train_of[next(h for h in legs if h != UNIT)]] += 12 * f * prod(value(h, x) for h in legs)
        for f, legs in self.two:
            p = f * prod(value(h, x) for h in legs)
            for t in {self.train_of[h] for h in legs if h != UNIT}:
                out[t] += 6 * p
        for c, tied in self.groups:
            p = c * prod(x[h] for h in tied)
            k2 = sum(x[r] * x[r] for r in self.held_rows)
            tt = self.train_of[tied[0]]
            if mode == "bg":
                out[tt] += 12 * p * k2
            elif mode == "mid":
                out[tt] += 6 * p * k2
                out[self.held_t] += 6 * p * k2
            else:
                exc = p * (k2 - self.n)
                out[tt] += 12 * p * self.n + 8 * exc
                out[self.held_t] += 4 * exc
        return out


def kin32(m, w):
    """32 W T(M), T(M) = R (M - 2 W R) / 4 with R = round(M / 4 W): the act's drift integrated over the momentum."""
    r = carry(m + 2 * w, 4 * w, 0)[0]
    return 8 * w * r * (m - 2 * w * r)


def hat_terms(rows, hat, n):
    terms = []
    for i, a in enumerate(rows):
        terms.append((hat, (a, a, a, a)))
        for b in rows[i + 1:]:
            terms.append((2 * hat, (a, a, b, b)))
        terms.append((-2 * hat * n, (a, a, UNIT, UNIT)))
    return terms


def layout(terms, rows, sites, teeth):
    nb = board((sites, 1, 1))
    n_sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    ones = np.ones((rows, 1), dtype=object)
    gearing = Gearing(teeth * ones, ones, ones.copy(), ones.copy(), ones.copy())
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    factor = np.array([f for f, _ in terms], dtype=object)
    legs = tuple(np.array([leg[i] for _, leg in terms], dtype=np.intp) for i in range(4))
    parts = [nb, spokes, meshes, np.zeros((rows, 3 * n_sites), dtype=object), gearing, pushes(factor, legs), UNREAD,
             UNREAD, click, NOPLAN]
    parts += [NOPLAN] * (len(Layout._fields) - len(parts))
    return Layout(*parts), n_sites


def run_meshless(terms, rows, a0, b0, rounds, teeth):
    """The act on Mesh-less Node-clocks; per round and site the window (b, a, a+) and the next momenta M."""
    sites = a0.shape[1]
    lay_, n_sites = layout(terms, rows, sites, teeth)
    s = State(a0.copy(), b0.copy(), np.zeros((rows, n_sites), dtype=object), np.zeros((rows, n_sites), dtype=object),
              np.zeros((1, n_sites), dtype=object))
    hist = []
    for _ in range(rounds):
        s1 = step.tick(lay_, s)
        rec = []
        for site in range(n_sites):
            b = [int(s.b[r, site]) for r in range(rows)]
            a = [int(s.a[r, site]) for r in range(rows)]
            a1 = [int(s1.a[r, site]) for r in range(rows)]
            m = [4 * teeth * (a1[r] - a[r]) + int(s1.r[r, site]) for r in range(rows)]
            rec.append((b, a, a1, m))
        hist.append(rec)
        s = s1
    return hist


def forms_of(world, b, a, a1):
    return {"act": world.act_s(b, a, a1), "middle": world.halves_middle_s(b, a, a1), "work middle":
            world.work_middle_s(b, a, a1), "background": world.background_s(b, a, a1), "split": world.split_s(b, a, a1)}


FORMS = ("act", "middle", "work middle", "background", "split")

# (b) passing4's three lays ---------------------------------------------------------------------------------------
HELD = (0, 1)
TIE = 3


def p4_terms(hat):
    return hat_terms(HELD, hat, N) + [(TIE, (2, 2, r, r)) for r in HELD] + [(N, (2, 2, UNIT, UNIT))]


print("(b) passing4's three lays: the held hand (k1, k2) under the hat at n = 5^10, the tie 3 to a tied train with its"
      " own spring n, four Mesh-less Node-clocks, 400 rounds; per form the windows whose books open, whose held"
      " passing is not 0, and that are odd under the window's reversal, of 1,600")
sites = 4
a0 = np.zeros((3, sites), dtype=object)
b0 = np.zeros((3, sites), dtype=object)
for i in range(sites):
    a0[0, i] = b0[0, i] = KEY
    a0[2, i] = 1000 * (i + 1)
    b0[2, i] = 1000 * (i + 1) - 7 * (i + 1)
a1_ = a0.copy()
b1_ = b0.copy()
for i in range(sites):
    a1_[0, i] = b1_[0, i] = KEY + 40 * (i + 1)
lays = [("(A) the hand at its rest (KEY, 0), the tied train swinging", 1, 2000 * N, a0, b0),
        ("(B) the hand's size laid off its rest", 1, 2000 * N, a1_, b1_),
        ("(C) a stiff hat 10^4, teeth 10^6 n, the hand at its rest", 10**4, 10**6 * N, a0, b0)]
p4_hist = {}
for label, hat, teeth, la, lb in lays:
    terms = p4_terms(hat)
    world = World(terms, [0, 0, 1], HELD, N)
    hist = run_meshless(terms, 3, la, lb, 400, teeth)
    p4_hist[label[:3]] = (world, hist, teeth, terms)
    books = {k: 0 for k in FORMS}
    heldnz = {k: 0 for k in FORMS}
    odd = {k: 0 for k in FORMS}
    same_mid = 0
    win = 0
    for rec in hist:
        for b, a, a1, _ in rec:
            fw = forms_of(world, b, a, a1)
            bw = forms_of(world, a1, a, b)
            win += 1
            for k in FORMS:
                books[k] += int(sum(fw[k].values()) != 0)
                heldnz[k] += int(fw[k][0] != 0)
                odd[k] += int(all(fw[k][t] == -bw[k][t] for t in world.trains))
            # the halves middle at kappa 4 against the work middle at kappa 6: 3 (halves) = 2 (work) where they agree
            same_mid += int(all(3 * fw["middle"][t] == 2 * fw["work middle"][t] for t in world.trains))
    print(f"  {label}:")
    for k in FORMS:
        print(f"    {k}: books open in {books[k]}; held passing not 0 in {heldnz[k]}; odd in {odd[k]} of {win}")
    print(f"    the middle form by halves equals the middle split in the work form (at one scale) in {same_mid} of"
          f" {win} windows")

# (a) and (c) B4's pair world ---------------------------------------------------------------------------------------
universe, gears = b4_world(sys.argv[1])  # B4's world and gears, read from the run test that lays them
setting = {"version": 1, "ticks": 400, "gears": gears}
held, found = loading.load(universe, setting, sites_of([1, 1, 1]), *main.made(loading.star(3)))
assert found == [] and held is not None
lay = main.layout(universe, [1, 1, 1], held)
s = state_mod.State(*held.state)
rows = len(s.a)
tr = held.trains
firsts = [int(x) for x in tr.first] + [rows]
train_of = []
for t in range(len(tr.first)):
    train_of += [t] * (firsts[t + 1] - firsts[t])
held_rows = [r for r in range(rows) if int(tr.held[train_of[r]])]
factor, legs = held.potential
pw_terms = [(int(factor[i]), tuple(int(legs[j][i]) for j in range(4))) for i in range(len(factor))]
key = int(lay.click.key[0, 0])
# n: the frame's held hand, laid (1, 0) and turning a quarter a round under its own spring; its |k|^2 is read below
k2_lay = sum(int(s.a[r, 0]) ** 2 for r in held_rows)
pw = World(pw_terms, train_of, held_rows, k2_lay)
print(f"(c) B4's pair world (the run test's files), the real loader and act: trains {sorted(set(train_of))}, held rows"
      f" {held_rows}, key {key}; monomials: own {len(pw.own)}, two-leg between trains {len(pw.two)}, tie groups"
      f" {len(pw.groups)} (factors {sorted({c for c, _ in pw.groups})}, each over held rows {held_rows});"
      f" n = the held hand's |k|^2 as laid, {k2_lay}")
KEY3 = 3 * key
teeth_split = [carry(KEY3 - 1, 2, 0)[0]] * 3
teeth_ref = {"background": [carry(key - 1, 2, 0)[0]] * 3, "middle as written": [carry(key - 1, 2, 0)[0]] * 3}
ref_books = {k: 0 for k in teeth_ref}
ref_room = {k: [0, 0, 0] for k in teeth_ref}
ref_room_max = {k: [0, 0, 0] for k in teeth_ref}
ref_lines = {k: [] for k in teeth_ref}
ref_past_max = {k: [0, 0, 0] for k in teeth_ref}
ref_same = {k: 0 for k in teeth_ref}
ref_held_fires = {k: 0 for k in teeth_ref}
birth_split = list(teeth_split)
two_ok = 0
two_n = 0
books = 0
k2s = []
first_off = 0
lines_act, lines_split = [], []
same_room = 0
room = {"act": [0, 0, 0], "split": [0, 0, 0]}
room_max = {"act": [0, 0, 0], "split": [0, 0, 0]}
past = {"act": [0, 0, 0], "split": [0, 0, 0]}
past_max = {"act": [0, 0, 0], "split": [0, 0, 0]}
pw_windows = []
for t in range(1, 401):
    s1, act_clicks = step.act(lay, s)
    b = [int(s.b[r, 0]) for r in range(rows)]
    a = [int(s.a[r, 0]) for r in range(rows)]
    a1 = [int(s1.a[r, 0]) for r in range(rows)]
    pw_windows.append((b, a, a1))
    k2s.append(sum(a1[r] * a1[r] for r in held_rows))
    if first_off == 0 and k2s[-1] != k2_lay:
        first_off = t
    # (a) the work form at kappa 2 against the act's X, two-leg monomial by monomial
    for f, lg in pw.two:
        w = pw.work(lg, f, b, a, a1)
        x = pw.act_s(b, a, a1, [(f, lg)])
        t1, t2 = sorted({train_of[h] for h in lg if h != UNIT})
        two_n += 1
        two_ok += int(x[t1] == w[t1] - w[t2] and x[t2] == w[t2] - w[t1])
    sp = pw.split_s(b, a, a1)
    books += int(sum(sp.values()) != 0)
    q = []
    for i in range(3):
        c_, teeth_split[i] = carry(sp[i], KEY3, teeth_split[i])
        q.append(c_)
    qa = [int(act_clicks[i, 0]) for i in range(3)]
    if t <= 30:
        lines_act.append(tuple(qa))
        lines_split.append(tuple(q))
    for name, qq in (("act", qa), ("split", q)):
        box, top = (room[name], room_max[name]) if t <= 56 else (past[name], past_max[name])
        for i in range(3):
            box[i] += abs(qq[i])
            top[i] = max(top[i], abs(qq[i]))
    if t <= 56:
        same_room += int(q == qa)
    for k, sv in (("background", pw.background_s(b, a, a1)), ("middle as written", pw.middle_written_s(b, a, a1))):
        ref_books[k] += int(sum(sv.values()) != 0)
        qq = []
        for i in range(3):
            c_, teeth_ref[k][i] = carry(sv[i], key, teeth_ref[k][i])
            qq.append(c_)
        if t <= 30:
            ref_lines[k].append(tuple(qq))
        if t <= 56:
            ref_same[k] += int(qq == qa)
            ref_held_fires[k] += int(qq[0] != 0)
        for i in range(3):
            if t <= 56:
                ref_room[k][i] += abs(qq[i])
                ref_room_max[k][i] = max(ref_room_max[k][i], abs(qq[i]))
            else:
                ref_past_max[k][i] = max(ref_past_max[k][i], abs(qq[i]))
    s = s1
print(f"  (a) the two-leg law: the work form at kappa 2 equals the act's X in {two_ok} of {two_n} (monomial, round)"
      f" pairs over 400 rounds")
print(f"  the held hand's |k|^2 at each round's next count, rounds 1 to 56: {sorted(set(k2s[:56]))}; past the room"
      f" {sorted(set(k2s[56:]))}; first not {k2_lay} at round {first_off}, where it is {k2s[first_off - 1]}")
print(f"  the split at kappa 6, the key times 3 ({KEY3}): books open in {books} of 400 rounds")
print(f"  the run test's 30 ticks: the act's (held, giver, taker) per round {sorted(set(lines_act))}; the split's"
      f" {sorted(set(lines_split))}")
print(f"  inside the room (rounds 1 to 56) the split's clicks equal the act's in {same_room} of 56 rounds; summed size"
      f" per train, the act {room['act']}, the split {room['split']}; largest in a round, the act {room_max['act']},"
      f" the split {room_max['split']}")
print(f"  past it (rounds 57 to 400): summed size per train, the act {past['act']}, the split {past['split']};"
      f" largest in a round, the act {past_max['act']}, the split {past_max['split']}")
for k in teeth_ref:
    print(f"  for reference, the {k} form at the key {key}: books open in {ref_books[k]}; the run test's 30 ticks"
          f" {sorted(set(ref_lines[k]))[:3]}{' ...' if len(set(ref_lines[k])) > 3 else ''}; in the room summed size"
          f" {ref_room[k]}, largest in a round {ref_room_max[k]}, the clicks equal the act's in {ref_same[k]} of 56"
          f" rounds, the held train firing in {ref_held_fires[k]}; past it largest in a round {ref_past_max[k]}")

# (d) the energy each form books ------------------------------------------------------------------------------------
BOOK = {"background": 24, "middle": 12, "split": 8, "work middle": 8}  # 96 W E per unit passing, times W


def energies(world, rec, teeth, mode):
    b, a, a1, m = rec
    kin = {t: 0 for t in world.trains}
    for r, mm in enumerate(m):
        kin[world.train_of[r]] += 3 * kin32(mm, teeth)
    va, va1 = world.potential12(a, mode), world.potential12(a1, mode)
    return {t: kin[t] + 4 * teeth * (va[t] + va1[t]) for t in world.trains}


def start_energy(world, b, a, teeth, mode):
    m = [4 * teeth * (a[r] - b[r]) for r in range(len(a))]
    return energies(world, (b, b, a, m), teeth, mode)


def held_misses(world, hist, teeth, site, b0l, a0l):
    """Per form, the worst |96 W dE_held - book W SUM S_held| over the run, and the held hand's own excursion."""
    modes = {"background": "bg", "middle": "mid", "work middle": "mid", "split": "split"}
    e0 = {k: start_energy(world, b0l, a0l, teeth, modes[k])[world.held_t] for k in modes}
    own0 = e0["background"]
    cum = {k: 0 for k in modes}
    miss = {k: 0 for k in modes}
    own_exc = 0
    for rnd in hist:
        rec = rnd[site]
        b, a, a1, _ = rec
        fw = forms_of(world, b, a, a1)
        e = {k: energies(world, rec, teeth, modes[k])[world.held_t] for k in modes}
        for k in modes:
            cum[k] += fw[k][world.held_t]
            miss[k] = max(miss[k], abs((e[k] - e0[k]) - BOOK[k] * teeth * cum[k]))
        own_exc = max(own_exc, abs(e["background"] - own0))
    return miss, own_exc


print("(d) the energy each form books, units 96 W E; a form's miss is its cumulative held passing against the held"
      " train's energy under its own split, in permille of the held hand's own excursion")
for tag in ("(A)", "(C)"):
    world, hist, teeth, terms = p4_hist[tag]
    for site in range(4):
        b0l = [KEY, 0, 1000 * (site + 1) - 7 * (site + 1)]
        a0l = [KEY, 0, 1000 * (site + 1)]
        miss, own = held_misses(world, hist, teeth, site, b0l, a0l)
        print(f"  lay {tag} site {site}: " + "; ".join(f"{k} {ppm(miss[k], own)}" for k in miss)
              + f" (the hand's own excursion {own})")

# the decay: the hand displaced 400 counts radially, the tied train seeded at 30, hat 1, tie 1, no own spring
W2 = 2000 * N
dterms = hat_terms(HELD, 1, N) + [(1, (2, 2, r, r)) for r in HELD]
dworld = World(dterms, [0, 0, 1], HELD, N)
da = np.array([[KEY + 400], [0], [30]], dtype=object)
dhist = run_meshless(dterms, 3, da, da.copy(), 3000, W2)
v_rest = dworld.potential12([KEY, 0, 0], "bg")[0]
v_start = dworld.potential12([KEY + 400, 0, 30], "bg")[0]
excess = 4 * W2 * 2 * (v_start - v_rest)  # 96 W times the hand's starting excess
cum = {"background": 0, "middle": 0, "split": 0}
worst_split_bg = 0
worst_at = 0
worst_mid_bg = 0
win_diff = 0
win_n = 0
for nr, rnd in enumerate(dhist):
    b, a, a1, _ = rnd[0]
    fw = forms_of(dworld, b, a, a1)
    for k in cum:
        cum[k] += fw[k][0]
    booked = {k: BOOK[k] * W2 * cum[k] for k in cum}
    d_sb = booked["split"] - booked["background"]
    if abs(d_sb) > worst_split_bg:
        worst_split_bg, worst_at = abs(d_sb), nr + 1
    worst_mid_bg = max(worst_mid_bg, abs(booked["middle"] - booked["background"]))
    if 1800 <= nr + 1 <= 2200:
        win_n += 1
        win_diff += d_sb
final = {k: ppm(BOOK[k] * W2 * cum[k], excess) for k in cum}
print(f"  the decay, 3,000 rounds: the held train's booked transfer at the end, permille of its starting excess:"
      f" background {final['background']}, middle {final['middle']}, split {final['split']}; the split against the"
      f" background differs by at most {ppm(worst_split_bg, excess)} (round {worst_at}), by"
      f" {ppm(win_diff, excess * win_n)} on the mean over rounds 1,800 to 2,200; the middle against the background by"
      f" at most {ppm(worst_mid_bg, excess)}")

# the free particle over a nearly still vacuum: hat 400, tie 1, no own spring, x0 2,000, 1,200 rounds
fterms = hat_terms(HELD, 400, N) + [(1, (2, 2, r, r)) for r in HELD]
fworld = World(fterms, [0, 0, 1], HELD, N)
fa = np.array([[KEY], [0], [2000]], dtype=object)
fhist = run_meshless(fterms, 3, fa, fa.copy(), 1200, W2)
energy = 96 * W2 * (1 * N * 2000 * 2000)
cum = {"background": 0, "middle": 0, "split": 0}
tot = {k: 0 for k in cum}
lo = {k: 0 for k in cum}
hi = {k: 0 for k in cum}
cnt = 0
kmax = 0
for nr, rnd in enumerate(fhist):
    b, a, a1, _ = rnd[0]
    fw = forms_of(fworld, b, a, a1)
    kmax = max(kmax, abs(a1[0] * a1[0] + a1[1] * a1[1] - N))
    for k in cum:
        cum[k] += fw[k][0]
        booked = BOOK[k] * W2 * cum[k]
        lo[k] = min(lo[k], booked)
        hi[k] = max(hi[k], booked)
        if nr + 1 > 200:
            tot[k] += booked
    if nr + 1 > 200:
        cnt += 1
print(f"  the free particle at x0 2,000 over a nearly still vacuum (|k|^2 - n at most {kmax}): the vacuum's booked"
      f" energy, permille of the particle's c n x0^2, its mean over rounds 201 to 1,200 and its range: "
      + "; ".join(f"{k} {ppm(tot[k], energy * cnt)} ({ppm(lo[k], energy)} to {ppm(hi[k], energy)})" for k in cum))

# the same free tied train with n off every square, n = 5^10 + 1, the hand still laid at (5^5, 0), |k|^2 one below n,
# so the reading does not rest on an exact aim (the end mathematician's free_offroot, the eighth text)
N1 = N + 1
W21 = 2000 * N1
f1terms = hat_terms(HELD, 400, N1) + [(1, (2, 2, r, r)) for r in HELD]
f1world = World(f1terms, [0, 0, 1], HELD, N1)
f1hist = run_meshless(f1terms, 3, fa, fa.copy(), 1200, W21)
energy1 = 96 * W21 * (1 * N1 * 2000 * 2000)
cum = {"background": 0, "middle": 0, "split": 0}
tot = {k: 0 for k in cum}
lo = {k: 0 for k in cum}
hi = {k: 0 for k in cum}
cnt = 0
for nr, rnd in enumerate(f1hist):
    b, a, a1, _ = rnd[0]
    fw = forms_of(f1world, b, a, a1)
    for k in cum:
        cum[k] += fw[k][0]
        booked = BOOK[k] * W21 * cum[k]
        lo[k] = min(lo[k], booked)
        hi[k] = max(hi[k], booked)
        if nr + 1 > 200:
            tot[k] += booked
    if nr + 1 > 200:
        cnt += 1
print("  the same free tied train at n = 5^10 + 1, off every square, the hand still at (5^5, 0), |k|^2 one below n:"
      " the held train's booked energy, permille of c n x0^2, its mean over rounds 201 to 1,200 and its range: "
      + "; ".join(f"{k} {ppm(tot[k], energy1 * cnt)} ({ppm(lo[k], energy1)} to {ppm(hi[k], energy1)})" for k in cum))

# a train holding both the tie and a two-leg spring: x (row 2) and y (row 3), each with the tie and its own spring n,
# and f x y between them; x's cumulative passing against its split energy
C = 1
F = N
tterms = (hat_terms(HELD, 1, N) + [(C, (2, 2, r, r)) for r in HELD] + [(C, (3, 3, r, r)) for r in HELD]
          + [(N, (2, 2, UNIT, UNIT)), (N, (3, 3, UNIT, UNIT)), (F, (2, 3, UNIT, UNIT))])
tworld = World(tterms, [0, 0, 1, 2], HELD, N)
for label, x0, y0 in (("x laid at 1,000, y at rest at 0", 1000, 0), ("x laid at 2,000, y at -500", 2000, -500)):
    ta = np.array([[KEY], [0], [x0], [y0]], dtype=object)
    thist = run_meshless(tterms, 4, ta, ta.copy(), 400, W2)
    e0 = start_energy(tworld, [KEY, 0, x0, y0], [KEY, 0, x0, y0], W2, "split")[1]
    cum_x = 0
    worst = 0
    exc = 0
    for rnd in thist:
        rec = rnd[0]
        b, a, a1, _ = rec
        cum_x += tworld.split_s(b, a, a1)[1]
        e = energies(tworld, rec, W2, "split")[1]
        exc = max(exc, abs(e - e0))
        worst = max(worst, abs((e - e0) - 8 * W2 * cum_x))
    print(f"  one scale, {label}, 400 rounds: x's split energy against its passing, worst miss {ppm(worst, exc)}"
          f" permille of its excursion")

# (e) the click tooth's run back under the split ---------------------------------------------------------------------
print("(e) the click tooth's run back under the split: carried forward over the windows, kept at the end as the mirror"
      " keeps it, and carried back over the reversed windows (b, a, a+) -> (a+, a, b) in reverse order")


def tooth_run_back(world, windows, kk):
    """The tooth kept under the mirror: carry(-S, K, r+) = (-q, r) wherever S is odd under the window's reversal."""
    tooth = {t: carry(kk - 1, 2, 0)[0] for t in world.trains}
    birth = dict(tooth)
    fwd = []
    for b, a, a1 in windows:
        sp = world.split_s(b, a, a1)
        q = {}
        for t in world.trains:
            q[t], tooth[t] = carry(sp[t], kk, tooth[t])
        fwd.append(q)
    ok_q = 0
    for (b, a, a1), q in zip(reversed(windows), reversed(fwd)):
        sp = world.split_s(a1, a, b)
        qb = {}
        for t in world.trains:
            qb[t], tooth[t] = carry(sp[t], kk, tooth[t])
        ok_q += int(all(qb[t] == -q[t] for t in world.trains))
    return tooth == birth, ok_q, len(windows)


world, hist, teeth, terms = p4_hist["(B)"]
for site in range(4):
    wins = [(rec[site][0], rec[site][1], rec[site][2]) for rec in hist]
    ok, okq, nn = tooth_run_back(world, wins, 3 * 7681)
    print(f"  lay (B) site {site}, key 3 x 7681: the tooth returned to its birth: {ok}; each back round's clicks the"
          f" forward's negated in {okq} of {nn}")
ok, okq, nn = tooth_run_back(pw, pw_windows, KEY3)
print(f"  the pair world, 400 rounds, key {KEY3}: the tooth returned to its birth: {ok}; each back round's clicks the"
      f" forward's negated in {okq} of {nn}")
