"""THIRD7's member on the board, written from C alone (a reading probe, never src): the triangle's own tooth pair.

Whole numbers only; every division is Rule3's carry (tensor24.algebra.carry.carry). The structure's numbers are read,
never typed:
- the Spokes, the senses and the axes from the star (runner.load.star): Spokes = len(star(axes)), senses = Spokes div
  axes; the split's half and third (Big Pic's KAPPA div 2 and KAPPA div 3) are Spokes div senses and Spokes div axes;
- the edge dial D = (Spokes div senses) x key and every birth (dial - 1) div senses;
- C, each triangle's boundary [j, k] - [i, k] + [i, j] on its sorted trains i < j < k (Big Pic's Edges order (ga, ab, gb):
  signs +1, +1, -1), and G = C^T C, each triangle's own Gram entry, the sum of its signs squared.

The member at one Node-clock, one round (y = C^T x the triangle's circulating passing):
- each edge e on a triangle t carries G x_e - c_e y at the dial G D with its own tooth, unturned;
  an edge on no triangle carries x_e at D (the first click);
- the triangle's tooth tau (kept by the mirror) carries y at the dial G D, its twin eta (flipped) beside it, turned by
  the palindrome at K = G: eta += G tau, tau += G eta; the carries; tau += G eta, eta += G tau (each shear a remainder
  about the birth, no quotient leaving it);
- each quantum w that tau lands is booked c_e w on every edge of its triangle in the same round.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def setup(src):
    sys.path.insert(0, str(src))
    sys.path.insert(0, str(HERE.joinpath("bp")))


def load_world(src, world_dir):
    """Big Pic's load_world (edgeclick.py), the world read from a folder given whole; the split's constants from the star."""
    from david_split import World
    from tensor24 import main
    from tensor24.algebra.carry import carry
    from tensor24.engine import state as state_mod
    from tensor24.runner import load as loading
    from tensor24.runner.files import sites_of

    ex = Path(world_dir)
    universe = json.loads(ex.joinpath("universe.json").read_text())
    shape = json.loads(ex.joinpath("piece.json").read_text())["shape"]
    setting = json.loads(ex.joinpath("setting.json").read_text())
    held, found = loading.load(universe, setting, sites_of(shape), *main.made(loading.star(len(shape))))
    assert found == [] and held is not None, found
    lay = main.layout(universe, shape, held)
    s = state_mod.State(*held.state)
    rows = s.a.shape[0]
    tr = held.trains
    firsts = [int(x) for x in tr.first] + [rows]
    train_of = []
    for t in range(len(tr.first)):
        train_of += [t] * (firsts[t + 1] - firsts[t])
    held_rows = [r for r in range(rows) if int(tr.held[train_of[r]])]
    factor, legs = held.potential
    terms = [(int(factor[i]), tuple(int(legs[j][i]) for j in range(4))) for i in range(len(factor))]
    axes = len(shape)
    spokes = len(loading.star(axes))
    senses, _ = carry(spokes, axes, 0)
    star = {"axes": axes, "spokes": spokes, "senses": senses, "half": carry(spokes, senses, 0)[0],
            "third": carry(spokes, axes, 0)[0]}
    return universe, shape, held, lay, s, StarWorld(terms, train_of, held_rows, star), star


def _star_world():
    from david_split import UNIT, World

    class StarWorld_(World):
        """David's split (NC29b, Big Pic's copy) with its KAPPA div 2 and KAPPA div 3 read from the star."""

        def __init__(self, terms, train_of, held_rows, star):
            super().__init__(terms, train_of, held_rows)
            self.star = star

        def split_flows(self, n, b, a, a1):
            out = {}
            half, third = self.star["half"], self.star["third"]
            for f, legs in self.two:
                w = self.work(legs, f, b, a, a1)
                t1, t2 = sorted({self.train_of[h] for h in legs if h != UNIT})
                out[(t1, t2)] = out.get((t1, t2), 0) + half * (w[t1] - w[t2])
            for c, tied in self.groups:
                w_held, w_tied = self.excursion_work(c, tied, n, b, a, a1)
                s_held = third * (2 * w_held - w_tied)  # David's own 2 (the square's), outside MINOR 4's list
                t1, t2 = sorted((self.held_t, self.train_of[tied[0]]))
                out[(t1, t2)] = out.get((t1, t2), 0) + (s_held if t1 == self.held_t else -s_held)
            return out

        def split_flows_david(self, n, b, a, a1):
            return World.split_flows(self, n, b, a, a1)

    return StarWorld_


class _Lazy:
    cls = None


def StarWorld(terms, train_of, held_rows, star):
    if _Lazy.cls is None:
        _Lazy.cls = _star_world()
    return _Lazy.cls(terms, train_of, held_rows, star)


def edge_set(world):
    """Big Pic's edge set and triangles (edgeclick.Edges), read without his dial."""
    from david_split import UNIT

    tr = world.train_of
    pairs = {tuple(sorted({tr[h] for h in lg if h != UNIT})) for _, lg in world.two}
    pairs |= {tuple(sorted((world.held_t, tr[td[0]]))) for _, td in world.groups}
    pairs = sorted(pairs)
    index = {p: i for i, p in enumerate(pairs)}
    ts = sorted({t for p in pairs for t in p})
    triangles = [(index[(i, j)], index[(j, k)], index[(i, k)])
                 for ai, i in enumerate(ts) for aj, j in enumerate(ts[ai + 1:], ai + 1) for k in ts[aj + 1:]
                 if (i, j) in index and (j, k) in index and (i, k) in index]
    return pairs, triangles


class Member:
    """The member's teeth at one Node-clock: each edge's tooth, each triangle's tooth tau and twin eta."""

    def __init__(self, n_edges, triangles, D, senses):
        from tensor24.algebra.carry import carry

        self.carry = carry
        self.n = n_edges
        # C: per triangle (ga, ab, gb), the boundary [j, k] - [i, k] + [i, j]: ga and ab with +1, gb with -1
        self.C = [((ga, 1), (ab, 1), (gb, -1)) for ga, ab, gb in triangles]
        self.G = [sum(sg * sg for _, sg in col) for col in self.C]  # C^T C, per triangle: its edges counted by C
        self.on = [[(t, sg) for t, col in enumerate(self.C) for e2, sg in col if e2 == e] for e in range(n_edges)]
        self.g = []
        for e in range(n_edges):
            p = 1
            for t, _ in self.on[e]:
                p *= self.G[t]
            self.g.append(p)  # an edge's factor: its triangle's G, 1 on no triangle (an edge on two is OPEN)
        self.D = D
        self.senses = senses
        self.dial = [gi * D for gi in self.g]
        self.born = [carry(d - 1, senses, 0)[0] for d in self.dial]
        self.tdial = [Gt * D for Gt in self.G]
        self.tborn = [carry(d - 1, senses, 0)[0] for d in self.tdial]

    def birth(self):
        return list(self.born), list(self.tborn), list(self.tborn)

    def cen(self, v, t):
        _, r = self.carry(v + self.tborn[t], self.tdial[t], 0)
        return r - self.tborn[t]

    def shear(self, dst, src, t):
        b = self.tborn[t]
        return b + self.cen(dst - b + self.G[t] * (src - b), t)

    def flip(self, eta):
        return [self.tborn[t] + self.cen(-(v - self.tborn[t]), t) for t, v in enumerate(eta)]

    def step(self, x, f, tau, eta, turned=True):
        """One round for the passings x (one per edge), the teeth in place; returns (sides per edge, landings per
        triangle). turned False leaves tau's twin out (the member unturned, a reading's control)."""
        carry = self.carry
        y = [sum(sg * x[e] for e, sg in col) for col in self.C]
        p = [self.g[e] * x[e] - sum(sg * y[t] for t, sg in self.on[e]) for e in range(self.n)]
        if turned:
            for t in range(len(self.C)):
                eta[t] = self.shear(eta[t], tau[t], t)
                tau[t] = self.shear(tau[t], eta[t], t)
        q = [0] * self.n
        for e in range(self.n):
            q[e], f[e] = carry(p[e], self.dial[e], f[e])
        w = []
        for t, col in enumerate(self.C):
            wt, tau[t] = carry(y[t], self.tdial[t], tau[t])
            w.append(wt)
            for e, sg in col:
                q[e] += sg * wt
        if turned:
            for t in range(len(self.C)):
                tau[t] = self.shear(tau[t], eta[t], t)
                eta[t] = self.shear(eta[t], tau[t], t)
        return q, w


class First:
    """The first click: each edge carries its passing at D with its own tooth."""

    def __init__(self, n_edges, D, senses):
        from tensor24.algebra.carry import carry

        self.carry = carry
        self.n = n_edges
        self.D = D
        self.born = carry(D - 1, senses, 0)[0]

    def birth(self):
        return [self.born] * self.n

    def step(self, x, f):
        q = [0] * self.n
        for e in range(self.n):
            q[e], f[e] = self.carry(x[e], self.D, f[e])
        return q


def lines_of(pairs, trains, t, x, q):
    out = {tr: 0 for tr in trains}
    for e, pr in enumerate(pairs):
        out[pr[0]] += q[e]
        out[pr[1]] -= q[e]
    return [(t, x, tr, v) for tr, v in out.items() if v]


def digest(obj):
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def board_digest(s):
    return hashlib.sha256(repr([z.tolist() for z in s]).encode()).hexdigest()
