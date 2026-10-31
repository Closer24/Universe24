"""ALG2: the homology of the laid complex, from the structure alone, on node-all 9d75a4904.

Args: <tree> <world dir> <unit-strengths world dir>
The complex is cochain2.py's: the clocks (every train at every Node-clock), the own edges (a structural coupling's
trains at one Node-clock), the Mesh edges (the gradient vertex's structural couplings across a + Spoke, joining
(x, t) to (x + s, u)), and the triangles (three clocks of one Node-clock pairwise joined). Read:
  - |V|, |E|, |F|; rank B = |V| - (connected parts), by a union of parts; rank C over the rationals, by exact row
    reduction with whole numbers (each row divided by the gcd of its entries, Euclid by Rule3's carry);
  - H_1 = |E| - rank B - rank C and H_2 = |F| - rank C, on the whole board and on each Node-clock's own part;
  - the triangles across one Mesh (two clocks of one Node-clock joined by an own edge, each joined by a Mesh edge to
    one clock at a neighbour): their count, and H_1 once they are filled too.
Whole numbers only; Rule3's carry the one division."""
import json
import sys
from pathlib import Path

tree, world, unit_world = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(tree.joinpath("src")))
import numpy as np  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner import files  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
from tensor24.runner.plans import rows_of  # noqa: E402


def loaded(wdir):
    paths = [wdir.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
    assert not files.departures(*paths)
    universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
    shape = piece["shape"]
    kinds, tables, square, lifted = main.ENGINE.made(files.star(len(shape)))
    ld, found = L.load(universe, setting, files.sites_of(shape), kinds, tables, square, lifted)
    assert not found, found
    return ld, main.ENGINE.layout(universe, shape, ld)


ld, lay = loaded(world)
ldu, layu = loaded(unit_world)
T = len(ld.trains)
rows, sites = ld.state[0].shape
nb = lay.nb
row_train = np.full(rows + 1, T, dtype=np.intp)
r_, of, _, _, _ = rows_of(ld.trains)
row_train[r_] = of
facu, legsu = ldu.potential
legs4 = np.stack(legsu)
pairs = set()
for m in range(len(facu)):
    if facu[m] != 0:
        ts = sorted({int(row_train[x]) for x in legs4[:, m] if x != -1})
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                pairs.add((ts[i], ts[j]))
own = sorted(pairs)
mesh = sorted({(int(s), int(row_train[r]), int(row_train[p])) for s, r, p in
               np.argwhere(np.asarray(layu.click.across != 0, dtype=bool)) if s % 2 == 0})
tri = [(i, j, k) for i in range(T) for j in range(i + 1, T) for k in range(j + 1, T)
       if (i, j) in pairs and (i, k) in pairs and (j, k) in pairs]


def vid(x, t):
    return x * T + t


edges = []  # (v1, v2), v1 the first end
for x in range(sites):
    for t, u in own:
        edges.append((vid(x, t), vid(x, u)))
for x in range(sites):
    for s, t, u in mesh:
        edges.append((vid(x, t), vid(int(nb[s][x]), u)))
eix = {}
for i, (p_, q_) in enumerate(edges):
    eix.setdefault((p_, q_), i)
nV, nE = sites * T, len(edges)


def parts(nv, es):
    up = list(range(nv))

    def root(v):
        while up[v] != v:
            up[v] = up[up[v]]
            v = up[v]
        return v
    for p_, q_ in es:
        a_, b_ = root(p_), root(q_)
        if a_ != b_:
            up[a_] = b_
    return len({root(v) for v in range(nv)})


def gcd(a_, b_):
    a_, b_ = abs(a_), abs(b_)
    while b_:
        _, r = carry(a_, b_, 0)
        a_, b_ = b_, r
    return a_


def rank(rows_):
    """Rank over the rationals of sparse whole-number rows (dicts column -> entry), by exact row reduction."""
    rows_ = [dict(r) for r in rows_ if r]
    rk = 0
    while rows_:
        piv_row = rows_.pop()
        if not piv_row:
            continue
        col = min(piv_row)
        pv = piv_row[col]
        rk += 1
        nxt = []
        for r in rows_:
            if col in r:
                f = r[col]
                new = {}
                for c, v in r.items():
                    new[c] = v * pv
                for c, v in piv_row.items():
                    new[c] = new.get(c, 0) - f * v
                new = {c: v for c, v in new.items() if v != 0}
                if new:
                    g = 0
                    for v in new.values():
                        g = gcd(g, v)
                    new = {c: carry(v, g, 0)[0] for c, v in new.items()}
                    nxt.append(new)
            else:
                nxt.append(r)
        rows_ = nxt
    return rk


def boundary(tris_):
    """Each triangle's boundary as a row over the edges: [j, k] - [i, k] + [i, j], each edge read with its held
    orientation."""
    out = []
    for (a_, b_, c_) in tris_:
        row = {}
        for (p_, q_), sg in (((b_, c_), 1), ((a_, c_), -1), ((a_, b_), 1)):
            if (p_, q_) in eix:
                row[eix[(p_, q_)]] = row.get(eix[(p_, q_)], 0) + sg
            else:
                row[eix[(q_, p_)]] = row.get(eix[(q_, p_)], 0) - sg
        out.append(row)
    return out


site_tris = [(vid(x, i), vid(x, j), vid(x, k)) for x in range(sites) for i, j, k in tri]
c_parts = parts(nV, edges)
rB = nV - c_parts
rC = rank(boundary(site_tris))
print("WORLD", world.name, "; trains", T, "; sites", sites, "; own edge pairs", own, "; Mesh edges (+ end)", mesh,
      "; triangles at a Node-clock", tri)
print("BOARD: |V|", nV, "|E|", nE, "|F|", len(site_tris), "; connected parts", c_parts, "; rank B", rB, "; rank C", rC,
      "; H_1", nE - rB - rC, "; H_2", len(site_tris) - rC)
joined = {v for e in edges for v in e}
print("  clocks on some edge", len(joined), "of", nV, "; the parts among them", parts(nV, edges) - (nV - len(joined)))
# each Node-clock's own part: its own edges and its triangles
own_e = [(vid(0, t), vid(0, u)) for t, u in own]
print("A NODE-CLOCK'S OWN PART: |V|", T, "|E|", len(own_e), "|F|", len(tri), "; H_1",
      len(own_e) - (T - parts(T, own_e)) - (rank(boundary([(vid(0, i), vid(0, j), vid(0, k)) for i, j, k in tri]))
                                           if tri else 0))
# the triangles across one Mesh
adj = {}
for p_, q_ in edges:
    adj.setdefault(p_, set()).add(q_)
    adj.setdefault(q_, set()).add(p_)
cross = set()
for p_, q_ in edges:
    for w in adj[p_] & adj[q_]:
        tri3 = tuple(sorted((p_, q_, w)))
        xs = {v // T for v in tri3}
        if len(xs) > 1:
            cross.add(tri3)
cross = sorted(cross)
print("TRIANGLES ACROSS ONE MESH:", len(cross), "; e.g.", [[(v // T, v % T) for v in c3] for c3 in cross[:2]])
if cross:
    rC2 = rank(boundary(site_tris + cross))
    print("  with them filled too: rank C", rC2, "; H_1", nE - rB - rC2, "; H_2", len(site_tris) + len(cross) - rC2)
print("END")
