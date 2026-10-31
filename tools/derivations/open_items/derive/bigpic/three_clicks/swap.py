"""The label rule (#2187 6539135332 item 1) on the real act: swap the two trains alike in kinds (the giver and the
taker, T1 + T2 each), their rows with them, and the record must be the original with the two names swapped, draw by
draw: each line's train exchanged, the apex's two edges exchanged, the alike pair's own edge read from its other end
(its quotient negated). The teeth are born alike, so they swap with the trains."""
import sys
src, world_dir, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
laid = len(sys.argv) > 4 and "laid" in sys.argv[4]
sys.path.insert(0, src); sys.path.insert(0, ".")
import edgeclick as E
universe, shape, held, lay, s0, world = E.load_world(src, world_dir)
if laid:
    s0 = E.board_lay(s0, shape, world)
kinds_of = [t["kinds"] for t in universe["trains"]]
alike = [t for t in world.trains if kinds_of[t] == ["T1", "T2"]]
assert len(alike) == 2
p, q = alike
rows = s0.a.shape[0]
rp = [r for r in range(rows) if world.train_of[r] == p]
rq = [r for r in range(rows) if world.train_of[r] == q]
assert len(rp) == len(rq)
def swapped_state(s):
    out = []
    for arr in (s.a, s.b, s.r, s.rd):
        x = arr.copy()
        x[rp, :], x[rq, :] = arr[rq, :], arr[rp, :]
        out.append(x)
    k = s.k.copy()
    k[p, :], k[q, :] = s.k[q, :], s.k[p, :]
    return s._replace(a=out[0], b=out[1], r=out[2], rd=out[3], k=k)
sigma = {t: t for t in world.trains}
sigma[p], sigma[q] = q, p
names = E.NAMES
from tensor24.engine import step
s1, s2 = s0, swapped_state(s0)
board_ok = True
for t in range(rounds):
    s1, _ = step.act(lay, s1)
    s2, _ = step.act(lay, s2)
    w = swapped_state(s1)
    board_ok = board_ok and all((x == y).all() for x, y in zip((w.a, w.b), (s2.a, s2.b)))
print(f"{world_dir}{', laid' if laid else ''}: key {int(lay.click.key[0, 0])}; the trains alike {alike}; the board itself swap-covariant over {rounds} rounds: {board_ok}")
for mode in [int(m) for m in (sys.argv[5] if len(sys.argv) > 5 else '01234')]:
    a = E.run_from(lay, s0, world, rounds, mode, kinds_of=kinds_of)
    b = E.run_from(lay, swapped_state(s0), world, rounds, mode, kinds_of=kinds_of)
    pairs = a["pairs"]
    idx = {pr: i for i, pr in enumerate(pairs)}
    def map_side(t, x, e, c):
        u, v = pairs[e]
        su, sv = sigma[u], sigma[v]
        if su < sv:
            return (t, x, idx[(su, sv)], c)
        return (t, x, idx[(sv, su)], -c)
    want_lines = sorted((t, x, sigma[tr], qq) for (t, x, tr, qq) in a["lines"])
    want_sides = sorted(map_side(*sd) for sd in a["sides"])
    got_lines, got_sides = sorted(b["lines"]), sorted(b["sides"])
    rounds_bad = len({ln[0] for ln in set(map(tuple, want_lines)) ^ set(map(tuple, got_lines))})
    print(f"   {names[mode]}: the swapped run is the original with the names swapped, draw by draw: lines {got_lines == want_lines}, sides {got_sides == want_sides}; rounds that differ {rounds_bad} of {rounds}")
