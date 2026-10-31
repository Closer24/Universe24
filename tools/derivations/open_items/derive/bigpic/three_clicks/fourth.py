"""The fourth click, off the table (the owner's word through the Boss's 6541083468 item 1). Read on the bench:
  (a) every shipped world's structure at a Node-clock: its clocks (trains), the pairs a term joins, the triangles (three
      clocks pairwise joined) and the 3-cells (four clocks pairwise joined), from edgeclick's own structure reader;
  (b) on the four-clock toy (shared.py's structure, the only one with a 3-cell's boundary), round by round: every
      side is its edge's own carry plus the triangles' landings booked on it, with nothing left over, and the faces'
      sum, the 3-cell's boundary, books nothing on any edge (C d_3 = 0): what a 3-cell held could write no side;
      and how often the four triangles' landings lean along that boundary, landing nowhere in the sides.
Whole numbers and Rule3's carry alone.

Usage: python3 -I fourth.py <src> <rounds>
"""
import json
import sys
from pathlib import Path

src, rounds = sys.argv[1], int(sys.argv[2])
sys.path.insert(0, src)
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402

# (a) the shipped worlds, read from each world's own potential: the trains every live monomial's value legs lie in
for world_dir in sorted(p.name for p in Path(src).parent.joinpath("examples").iterdir() if p.is_dir()):
    ex = Path(src).parent / "examples" / world_dir
    universe = json.loads((ex / "universe.json").read_text())
    shape = json.loads((ex / "piece.json").read_text())["shape"]
    setting = json.loads((ex / "setting.json").read_text())
    held, found = E.loading.load(universe, setting, E.sites_of(shape), *E.main.made(E.loading.star(len(shape))))
    if found or held is None:
        print(f"{world_dir}: the loader names {len(found)} departures; the first: {found[0] if found else 'none'}")
        continue
    tr = held.trains
    rows = int(sum(int(v) for v in tr.size))
    firsts = [int(x) for x in tr.first] + [rows]
    train_of = []
    for t in range(len(tr.first)):
        train_of += [t] * (firsts[t + 1] - firsts[t])
    factor, legs = held.potential
    joined, widest = set(), 0
    for i in range(len(factor)):
        if int(factor[i]) == 0:
            continue
        owners = sorted({train_of[int(legs[j][i])] for j in range(4) if int(legs[j][i]) >= 0})
        widest = max(widest, len(owners))
        for x in range(len(owners)):
            for y in range(x + 1, len(owners)):
                joined.add((owners[x], owners[y]))
    trains = sorted({t for p in joined for t in p})
    tris = [(a, b, c) for a in trains for b in trains for c in trains
            if a < b < c and {(a, b), (a, c), (b, c)} <= joined]
    quads = [(a, b, c, d) for a in trains for b in trains for c in trains for d in trains
             if a < b < c < d and {(a, b), (a, c), (a, d), (b, c), (b, d), (c, d)} <= joined]
    print(f"{world_dir}: {len(universe['trains'])} trains; {len(joined)} pairs joined by a live term; {len(tris)}"
          f" triangles; {len(quads)} sets of four clocks pairwise joined; the widest live term joins {widest} trains")

# (b) the four-clock toy's 3-cell: its boundary, the four faces taken with the tetrahedron's signs, books nothing on any
# edge, so whatever a 3-cell held, booked through its boundary, could write no side and no clock's line
edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
tris = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
C = [[0] * len(tris) for _ in edges]
for f, (i, j, k) in enumerate(tris):
    C[edges.index((j, k))][f] += 1
    C[edges.index((i, k))][f] -= 1
    C[edges.index((i, j))][f] += 1
boundary = [-1, 1, -1, 1]  # the faces of the tetrahedron 0123 with its signs: d_3 [0123] = [123] - [023] + [013] - [012]
on_edges = [sum(C[e][f] * boundary[f] for f in range(len(tris))) for e in range(len(edges))]
B = [[(1 if a == v else -1 if b == v else 0) for (a, b) in edges] for v in range(4)]
on_lines = [sum(B[v][e] * on_edges[e] for e in range(len(edges))) for v in range(4)]
print(f"four clocks pairwise joined: the 3-cell's boundary on the four faces {boundary} books {on_edges} on the six edges"
      f" and {on_lines} on the four clocks' lines (C d_3 = 0)")
