"""The three clicks' laws read in one run on one world, for the handover (Big Pic, #2187): the first click (mode 0) and
the third click's two members from the structure, C C^T off its diagonal (mode 4) and its diagonal (road 3, mode 5).

- the books close at every place;
- R1: the record run twice, byte for byte;
- the run back to the lay: the carry's own inverse for the first click, the same act on the mirrored state for the third;
- the label rule, draw by draw, for every two trains alike in kinds: the run of the swapped lay is the original with the
  names swapped, each line's train exchanged and each edge read from its other end;
- R2 and its reach: one hidden unit in each edge's tooth at Node-clock 0 moves a later click side in the third click,
  every moved side at that Node-clock (in mode 11 the unit is laid in the twin of the edge's triangle);
- the split click's choice between the first and the third: an edge on no triangle, which C C^T leaves alone, carries
  in the third click exactly as in the first.
The exit status is 0 if every law reads as it should, and 1 if one does not, named.

Usage: python3 -I laws.py <src> <world> <rounds> [laid] [third-click modes, 45 unless given]
"""
import sys

src, world_dir, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
laid = len(sys.argv) > 4 and "laid" in sys.argv[4]
thirds = "45" if len(sys.argv) <= 5 else sys.argv[5]  # one digit per mode, or a comma list (edgeclick.modes_of)
sys.path.insert(0, src)
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
thirds = E.modes_of(thirds)
from tensor24.engine import step  # noqa: E402

universe, shape, held, lay, s0, world = E.load_world(src, world_dir)
if laid:
    s0 = E.board_lay(s0, shape, world)
kinds_of = [t["kinds"] for t in universe["trains"]]
rows = s0.a.shape[0]
failed = []


def swapped(s, p, q):
    rp = [r for r in range(rows) if world.train_of[r] == p]
    rq = [r for r in range(rows) if world.train_of[r] == q]
    out = []
    for arr in (s.a, s.b, s.r, s.rd):
        x = arr.copy()
        x[rp, :], x[rq, :] = arr[rq, :], arr[rp, :]
        out.append(x)
    k = s.k.copy()
    k[p, :], k[q, :] = s.k[q, :], s.k[p, :]
    return s._replace(a=out[0], b=out[1], r=out[2], rd=out[3], k=k)


def check(name, ok):
    print(f"   {name}: {ok}")
    if not ok:
        failed.append(name)


alike = [(p, q) for p in world.trains for q in world.trains if p < q and kinds_of[p] == kinds_of[q]]
alike = [(p, q) for p, q in alike if sum(1 for r in range(rows) if world.train_of[r] == p) == sum(1 for r in range(rows) if world.train_of[r] == q)]
ed = E.Edges(world, int(lay.click.key[0, 0]), s0.a.shape[1], kinds_of)
lone = [e for e in range(len(ed.pairs)) if not any(ed.cc[e])]
print(f"{world_dir}{', laid' if laid else ''}, {rounds} rounds: key {int(lay.click.key[0, 0])}, dial {ed.dial}; edges {ed.pairs},"
      f" triangles {ed.triangles}, edges on no triangle {[ed.pairs[e] for e in lone]}; trains alike {alike}")
first = None
for mode in [0] + thirds:
    a = E.run_from(lay, s0, world, rounds, mode, kinds_of=kinds_of)
    b = E.run_from(lay, s0, world, rounds, mode, kinds_of=kinds_of)
    print(f" {E.NAMES[mode]}: {a['places']} click places, {len(a['lines'])} click lines")
    check(f"mode {mode}: the books close at every place", a["books_open"] == 0)
    check(f"mode {mode}: R1, the record run twice byte for byte", a["digest"] == b["digest"])
    check(f"mode {mode}: the run back to the lay", bool(a["runback"]))
    for p, q in alike:
        sigma = {t: t for t in world.trains}
        sigma[p], sigma[q] = q, p
        c = E.run_from(lay, swapped(s0, p, q), world, rounds, mode, kinds_of=kinds_of)
        idx = {pr: i for i, pr in enumerate(a["pairs"])}

        def side(t, x, e, v):
            u, w = a["pairs"][e]
            su, sw = sigma[u], sigma[w]
            return (t, x, idx[(su, sw)], v) if su < sw else (t, x, idx[(sw, su)], -v)

        same = sorted(c["lines"]) == sorted((t, x, sigma[tr], v) for (t, x, tr, v) in a["lines"])
        same = same and sorted(c["sides"]) == sorted(side(*sd) for sd in a["sides"])
        check(f"mode {mode}: the label rule for trains {p} and {q}, draw by draw", same)
    if mode == 0:
        first = a
        continue
    for e in lone:
        mine = sorted(sd for sd in a["sides"] if sd[2] == e)
        theirs = sorted(sd for sd in first["sides"] if sd[2] == e)
        check(f"mode {mode}: edge {ed.pairs[e]}, on no triangle, carries as the first click", mine == theirs)
    for e in range(len(ed.pairs)):
        if e in lone:
            continue
        h = E.run_from(lay, s0, world, rounds, mode, hidden=(0, e), kinds_of=kinds_of)
        diff = set(map(tuple, a["sides"])) ^ set(map(tuple, h["sides"]))
        at = sorted({d[1] for d in diff})
        print(f"   mode {mode}: one hidden unit in edge {ed.pairs[e]}'s tooth at Node-clock 0 moves {len(diff)} click sides,"
              f" the first at round {min(d[0] for d in diff) if diff else None}, at Node-clocks {at}")
        check(f"mode {mode}: R2 for edge {ed.pairs[e]}, a later click moved, at Node-clock 0 alone", bool(diff) and at == [0])
print(f"every law holds: {not failed}" + (f"; failed: {failed}" if failed else ""))
sys.exit(1 if failed else 0)
