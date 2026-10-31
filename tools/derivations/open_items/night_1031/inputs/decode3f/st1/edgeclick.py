"""Big Pic's three clicks on the real act (the owner's words of 04:0x and 04:1x UTC; #2187 6538866082), whole numbers,
every division Rule3's carry.

The board steps by step.act as it stands; the click pushes nothing into the gears. At every Node-clock, every round:
- the first click: David's split gives one flow per pair of trains it joins (an edge); each edge carries its flow with
  its own tooth at the dial 3 key, born at its middle (3 key - 1) div 2, and the far end clicks the opposite quotient
  (the owner's shared pair of teeth, NC29b); a train's click is the sum of its edges;
- the split click: where three trains are pairwise joined, the flows split over a triangle of edges;
- the third click: there the triangle's three teeth turn between carries, the takers' edge gaining the first edge,
  the second losing the takers' edge, the first losing the second, each a remainder on the dial about the birth;
  a lone edge has no triangle, so nothing turns it and it carries as the first click.
No line asks how many trains meet: the turn is the product over the triangles the edge set holds.

Usage: python3 -I edgeclick.py <src> <world> <rounds> <turn: 1 or 0> [hidden unit: site edge-index]
"""

import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, str(Path(__file__).resolve().parent))
from david_split import UNIT, World  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402


def load_world(src, world_dir):
    ex = Path(src).parent / "examples" / world_dir
    universe = json.loads((ex / "universe.json").read_text())
    shape = json.loads((ex / "piece.json").read_text())["shape"]
    setting = json.loads((ex / "setting.json").read_text())
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
    return universe, shape, held, lay, s, World(terms, train_of, held_rows)


class Edges:
    """The edge set from the structure: every pair of trains a two-leg monomial or a tie group joins, and every
    triangle of three trains pairwise joined; per Node-clock one tooth per edge at the dial 3 key."""

    def __init__(self, world, key, sites):
        tr = world.train_of
        pairs = {tuple(sorted({tr[h] for h in lg if h != UNIT})) for _, lg in world.two}
        pairs |= {tuple(sorted((world.held_t, tr[td[0]]))) for _, td in world.groups}
        self.pairs = sorted(pairs)
        self.index = {p: i for i, p in enumerate(self.pairs)}
        ts = sorted({t for p in self.pairs for t in p})
        self.triangles = [
            (self.index[(i, j)], self.index[(j, k)], self.index[(i, k)])
            for ai, i in enumerate(ts) for aj, j in enumerate(ts[ai + 1:], ai + 1) for k in ts[aj + 1:]
            if (i, j) in self.index and (j, k) in self.index and (i, k) in self.index
        ]
        self.dial = carry(world_kappa_half(), 1, 0)[0] * key  # the key times 3, the split's own scale (kappa 6 / 2)
        self.born, _ = carry(self.dial - 1, 2, 0)
        self.teeth = [[self.born] * len(self.pairs) for _ in range(sites)]

    def cen(self, v):
        _, r = carry(v + self.born, self.dial, 0)
        return r - self.born

    def turn(self, u):
        for ga, ab, gb in self.triangles:
            x, y, z = u[ga] - self.born, u[ab] - self.born, u[gb] - self.born
            y = self.cen(y + x)
            z = self.cen(z - y)
            x = self.cen(x - z)
            u[ga], u[ab], u[gb] = x + self.born, y + self.born, z + self.born

    def unturn(self, u):
        for ga, ab, gb in reversed(self.triangles):
            x, y, z = u[ga] - self.born, u[ab] - self.born, u[gb] - self.born
            x = self.cen(x + z)
            z = self.cen(z + y)
            y = self.cen(y - x)
            u[ga], u[ab], u[gb] = x + self.born, y + self.born, z + self.born


def world_kappa_half():
    from david_split import KAPPA

    half, _ = carry(KAPPA, 2, 0)
    return half


def run(src, world_dir, rounds, turned, hidden=None):
    universe, shape, held, lay, s, world = load_world(src, world_dir)
    out = run_from(lay, s, world, rounds, turned, hidden)
    out.update({"world": world_dir, "shape": shape})
    return out


def run_from(lay, s, world, rounds, turned, hidden=None):
    rows, sites = s.a.shape
    key = int(lay.click.key[0, 0])
    edges = Edges(world, key, sites)
    if hidden is not None:
        site, e = hidden
        edges.teeth[site][e] = edges.born + edges.cen(edges.teeth[site][e] - edges.born + 1)
    lay_teeth = [list(u) for u in edges.teeth]
    lines, sides, flows = [], [], []
    books_open = places = 0
    for t in range(rounds):
        s1, _ = step.act(lay, s)
        round_flows = []
        for x in range(sites):
            b = [int(s.b[r, x]) for r in range(rows)]
            a = [int(s.a[r, x]) for r in range(rows)]
            a1 = [int(s1.a[r, x]) for r in range(rows)]
            fl = world.split_flows(0, b, a, a1)
            u = edges.teeth[x]
            if turned:
                edges.turn(u)
            q = {tr_: 0 for tr_ in world.trains}
            xs = []
            for e, pr in enumerate(edges.pairs):
                f = fl.get(pr, 0)
                xs.append(f)
                c, u[e] = carry(f, edges.dial, u[e])
                q[pr[0]] += c
                q[pr[1]] -= c
                if c:
                    sides.append((t, x, e, c))
            round_flows.append(xs)
            if any(q.values()):
                places += 1
                books_open += int(sum(q.values()) != 0)
            for tr_, v in q.items():
                if v:
                    lines.append((t, x, tr_, v))
        flows.append(round_flows)
        s = s1
    end_teeth = [list(u) for u in edges.teeth]
    # the run back of the click teeth: each edge's carry with its flow negated, then the turn undone
    back = [list(u) for u in end_teeth]
    recovered = []
    for t in range(rounds - 1, -1, -1):
        for x in range(sites):
            u = back[x]
            for e in range(len(edges.pairs)):
                c, u[e] = carry(-flows[t][x][e], edges.dial, u[e])
                if c:
                    recovered.append((t, x, e, -c))
            if turned:
                edges.unturn(u)
    runback = back == lay_teeth and sorted(recovered) == sorted(sides)
    digest = hashlib.sha256(repr((lines, sides)).encode()).hexdigest()
    return {
        "sites": sites, "trains": world.trains, "pairs": edges.pairs,
        "triangles": edges.triangles, "key": key, "dial": edges.dial, "born": edges.born, "rounds": rounds,
        "turned": turned, "lines": lines, "sides": sides, "flows": flows, "places": places,
        "books_open": books_open, "runback": runback, "digest": digest,
    }


if __name__ == "__main__":
    src, world_dir, rounds, turned = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    hidden = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else None
    t0 = time.time()
    out = run(src, world_dir, rounds, turned, hidden)
    per_edge = [sum(abs(c) for (_, _, e, c) in out["sides"] if e == i) for i in range(len(out["pairs"]))]
    print(f"{world_dir}: {out['sites']} Node-clocks, trains {out['trains']}, edges {out['pairs']},"
          f" triangles {out['triangles']}, key {out['key']}, dial {out['dial']} born {out['born']};"
          f" {rounds} rounds, {'turned (third click)' if turned else 'carried (first click)'}")
    print(f"  click places {out['places']}, the books open at {out['books_open']}; click lines {len(out['lines'])},"
          f" sides {len(out['sides'])}; quanta booked per edge {per_edge}")
    print(f"  the click teeth run back to the lay and every side recovered: {out['runback']}; record digest"
          f" {out['digest']}; {time.time() - t0:.0f} s")
    json.dump({k: out[k] for k in ("lines", "sides", "digest")}, open(f"edge_{world_dir}_{rounds}_{turned}.json", "w"))
