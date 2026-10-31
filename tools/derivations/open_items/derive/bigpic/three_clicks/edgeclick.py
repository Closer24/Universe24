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

Usage: python3 -I edgeclick.py <src> <world> <rounds> <mode 0 to 5> [laid] [hidden unit: site edge-index]
"""

import hashlib
import json
import sys
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

    def __init__(self, world, key, sites, kinds_of=None):
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
        # each edge's twin, of the other class under the reversal (flipped, as the drive's tooth is), born alike
        self.twins = [[self.born] * len(self.pairs) for _ in range(sites)]
        # the palindrome's shears around every triangle (the THIRD deriver's four-tooth form, carried around three):
        # (destination, source, sign), each between a kept tooth (an edge's) and a flipped one (a twin's)
        self.shears = []
        for ga, ab, gb in self.triangles:
            g1, g2, g3 = ("g", ga), ("g", ab), ("g", gb)
            h1, h2, h3 = ("h", ga), ("h", ab), ("h", gb)
            self.shears += [(h1, g1, 1), (g1, h1, -1), (h2, g2, 1), (g2, h1, 1), (h3, g3, 1), (g3, h2, 1), (g1, h3, 1)]
        # SPLIT3 (the SPLIT deriver, #2187 6539135332 item 3): at a triangle whose one vertex differs in kinds from the
        # other two (its apex, read from the structure), the apex's two edges g1, g2 and their twins t1, t2 turn in
        # blocks the swap of the two alike vertices exchanges; the alike vertices' own edge carries unturned
        self.split3 = []
        self.apexes = []
        for ga, ab, gb in self.triangles:
            tri = sorted(set(self.pairs[ga]) | set(self.pairs[ab]) | set(self.pairs[gb]))
            if kinds_of is None:
                continue
            odd = [v for v in tri if sum(1 for w in tri if kinds_of[w] == kinds_of[v]) == 1]
            if len(odd) != 1 or len({tuple(kinds_of[v]) for v in tri}) != 2:
                continue  # no apex the structure names: this triangle stays unturned in mode 3 (named open)
            apex = odd[0]
            b1, b2 = [v for v in tri if v != apex]
            e1, e2 = self.index[tuple(sorted((apex, b1)))], self.index[tuple(sorted((apex, b2)))]
            self.apexes.append((apex, b1, b2))
            G1, G2, T1, T2 = ("g", e1), ("g", e2), ("h", e1), ("h", e2)
            self.split3 += [(T1, G1, 1), (T2, G2, 1), (G1, T1, -1), (G2, T2, -1), (T1, G1, -1), (T2, G2, -1),
                            (G1, T2, 1), (G2, T1, 1)]

        # the triangle's own coupling (mode 4): K, the off-diagonal of C C^T, C each edge's sign on the boundary of
        # every triangle it lies on (the boundary of [i, j, k] is [j, k] - [i, k] + [i, j]); two edges of one triangle
        # couple by the product of their signs, an edge never to itself, and a lone edge, on no triangle, to nothing.
        # Each twin gains K of the edge teeth, then each edge tooth K of the twins: two blocks of kept-flipped shears
        # that the palindrome runs before the carries and in reverse after them. K is the structure's own: every
        # relabelling of the trains moves it with the edges' signs, so the turn keeps the label rule; per eigenvalue
        # kappa of K the round's linear turn has trace 2 + 4 kappa^2, and the triangle's K has 2, -1, -1, so all
        # three edges mix (traces 18, 6, 6), the alike pair's own edge with them.
        n = len(self.pairs)
        cc = [[0] * n for _ in range(n)]
        for ga, ab, gb in self.triangles:
            sign = {ga: 1, ab: 1, gb: -1}
            for e, se in sign.items():
                for f, sf in sign.items():
                    cc[e][f] += se * sf
        # Road 3 (the THIRD deriver's, #2187 6539223290, mode 5) is the same palindrome on the diagonal of C C^T: each
        # triangle edge with its own twin, h += g, g += h, the carries, g += h, h += g, weighted by the number of
        # triangles the edge lies on (1 here); per edge trace 6. The two parts of C C^T are the structure's two members;
        # their sum, C C^T itself, keeps the two directions across the boundary unturned (its eigenvalues 3, 0, 0).
        self.cc = cc
        self.kcoup = [[cc[e][f] * (e != f) for f in range(n)] for e in range(n)]
        self.kdiag = [[cc[e][f] * (e == f) for f in range(n)] for e in range(n)]
        self.tri_k = self.blocks(self.kcoup)
        self.road3 = self.blocks(self.kdiag)
        # the circulation's members (THIRD6's OPEN 3, #2187 6539589459 item 3): the edge teeth gain only along each
        # triangle's circulation, g += C C^T h, so every train's booked total keeps to its swept flow (the boundary of
        # a circulation is 0); the twins gain C C^T off its diagonal of the edge teeth (mode 7) or C C^T itself (8)
        self.circ_k = self.blocks(self.kcoup, cc)
        self.circ_cc = self.blocks(cc, cc)

    @staticmethod
    def blocks(k, kg=None):
        """Two blocks of kept-flipped shears: each twin gains k of the edge teeth, then each edge tooth kg (k unless
        given) of the twins. Within a block every shear writes one class and reads the other, so its order is free."""
        n = len(k)
        kg = k if kg is None else kg
        return ([(("h", e), ("g", f), k[e][f]) for e in range(n) for f in range(n)]
                + [(("g", e), ("h", f), kg[e][f]) for e in range(n) for f in range(n)])

    def forward(self, mode):
        return {2: self.shears, 3: self.split3, 4: self.tri_k, 5: self.road3, 7: self.circ_k, 8: self.circ_cc}[mode]

    def backward(self, mode):
        return list(reversed(self.forward(mode)))

    def shear_all(self, u, w, order):
        for (dk, di), (sk, si), sign in order:
            src = (u if sk == "g" else w)[si] - self.born
            dst = u if dk == "g" else w
            dst[di] = self.born + self.cen(dst[di] - self.born + sign * src)

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


def board_lay(s, shape, world):
    """VARY1's stand-in, labelled so: each Node-clock's hands set apart below the key by the board's own coordinates
    (x, y, z), the loader's order unravelled: the giver's first row one count up per x, and the taker, laid at rest at
    0 in the world file, laid at the bare unit 1 (as the held hand is) one count up per y; now and before alike, so
    every hand starts at rest. No number is picked beyond the bare unit; no random."""
    rows, sites = s.a.shape
    first = {}
    for r in range(rows):
        first.setdefault(world.train_of[r], r)
    giver, taker = first[world.trains[3]], first[world.trains[4]]
    a, b = s.a.copy(), s.b.copy()
    for n in range(sites):
        rest, x = carry(n, shape[0], 0)
        _, y = carry(rest, shape[1], 0)
        a[giver, n] = a[giver, n] + x
        a[taker, n] = 1 + y
        b[giver, n], b[taker, n] = a[giver, n], a[taker, n]
    return s._replace(a=a, b=b)


def run(src, world_dir, rounds, turned, hidden=None, laid=False):
    universe, shape, held, lay, s, world = load_world(src, world_dir)
    if laid:
        s = board_lay(s, shape, world)
    out = run_from(lay, s, world, rounds, turned, hidden, [t["kinds"] for t in universe["trains"]])
    out.update({"world": world_dir, "shape": shape})
    return out


def run_from(lay, s, world, rounds, turned, hidden=None, kinds_of=None):
    rows, sites = s.a.shape
    key = int(lay.click.key[0, 0])
    edges = Edges(world, key, sites, kinds_of)
    if hidden is not None:
        site, e = hidden
        edges.teeth[site][e] = edges.born + edges.cen(edges.teeth[site][e] - edges.born + 1)
    lay_teeth = [list(u) for u in edges.teeth]
    lay_twins_saved = [list(w) for w in edges.twins]
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
            w = edges.twins[x]
            if turned >= 2:
                edges.shear_all(u, w, edges.forward(turned))
            elif turned:
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
            if turned >= 2:
                edges.shear_all(u, w, edges.backward(turned))
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
    lay_twins = lay_twins_saved
    mirror_ok = None
    if turned >= 2:
        # the board's own law: the same act on the mirrored state, the twins flipped and the edge teeth kept, every
        # passing negated, the rounds in reverse; then the mirror again; it must reach the lay
        u_all = [list(u) for u in edges.teeth]
        w_all = [[edges.born + edges.cen(-(v - edges.born)) for v in w] for w in edges.twins]
        for t in range(rounds - 1, -1, -1):
            for x in range(sites):
                u, w = u_all[x], w_all[x]
                edges.shear_all(u, w, edges.forward(turned))
                for e in range(len(edges.pairs)):
                    _, u[e] = carry(-flows[t][x][e], edges.dial, u[e])
                edges.shear_all(u, w, edges.backward(turned))
        w_all = [[edges.born + edges.cen(-(v - edges.born)) for v in w] for w in w_all]
        mirror_ok = u_all == lay_teeth and w_all == lay_twins
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
            if turned == 1:
                edges.unturn(u)
    runback = (back == lay_teeth and sorted(recovered) == sorted(sides)) if turned < 2 else mirror_ok
    digest = hashlib.sha256(repr((lines, sides)).encode()).hexdigest()
    return {
        "sites": sites, "trains": world.trains, "pairs": edges.pairs,
        "triangles": edges.triangles, "key": key, "dial": edges.dial, "born": edges.born, "rounds": rounds,
        "turned": turned, "lines": lines, "sides": sides, "flows": flows, "places": places,
        "books_open": books_open, "runback": runback, "digest": digest, "mirror": mirror_ok,
    }


NAMES = ["carried (first click)", "turned by the triangle M (third click)", "the 3+3 palindrome (third click)",
         "SPLIT3 (third click, the apex's edges)", "the triangle's coupling, C C^T off its diagonal (third click)",
         "road 3, C C^T's diagonal: each triangle edge with its own twin (third click)",
         "the THIRD deriver's five blocks (third click)",
         "the circulation: g += C C^T h, h += C C^T off its diagonal of g (third click)",
         "the circulation: g += C C^T h, h += C C^T g (third click)"]

if __name__ == "__main__":
    src, world_dir, rounds, turned = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    laid = len(sys.argv) > 5 and "laid" in sys.argv[5]
    hidden = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else None
    out = run(src, world_dir, rounds, turned, hidden, laid)
    per_edge = [sum(abs(c) for (_, _, e, c) in out["sides"] if e == i) for i in range(len(out["pairs"]))]
    print(f"{world_dir}: {out['sites']} Node-clocks, trains {out['trains']}, edges {out['pairs']},"
          f" triangles {out['triangles']}, key {out['key']}, dial {out['dial']} born {out['born']};"
          f" {rounds} rounds, {NAMES[turned]}{', the hands laid apart below the key (VARY1 stand-in)' if laid else ''}")
    print(f"  click places {out['places']}, the books open at {out['books_open']}; click lines {len(out['lines'])},"
          f" sides {len(out['sides'])}; quanta booked per edge {per_edge}")
    print(f"  the click teeth run back to the lay ({'by the same act on the mirrored state' if turned >= 2 else 'and every side recovered'}): {out['runback']}; record digest"
          f" {out['digest']}")
