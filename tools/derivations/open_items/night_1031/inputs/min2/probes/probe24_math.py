"""MIN1 math reader's probe: the 24 on MIN1's reduced teeth (D1 + D2 + D3), on the edges test's own cube world
(tests/test_the_tensor24_edges.world(CUBE): the mesh world's files at the test's key 1000003, a 3x3x3 cube, Mesh edges
carrying at once). The full turn is the test's own spun (sites, rows by the kinds' matrices, every Mesh tooth moved to
its turned Spoke, a pure permutation of the teeth). The reduced turn is g_R = reduce . spun . expand. Measured, for
each of the 24: (1) the turned full state stays on the pair law (expand(reduce(t)) == t); (2) on the held Mesh teeth
g_R is the transport where the + Spoke goes to a + Spoke and key - 1 - k (trains swapped, the other end) where it goes
to a - Spoke; (3) act_R . g_R == g_R . act_R on the state, and the clicks read back turn as the engine's.
Whole numbers only; argv: tree rounds."""
import sys
from pathlib import Path

tree, rounds = Path(sys.argv[1]), int(sys.argv[2])
sys.path.insert(0, str(tree.joinpath("src")))
sys.path.insert(0, str(tree))
import numpy as np  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import run as R  # noqa: E402
from tests import test_the_tensor24_edges as E  # noqa: E402

held, lay, s0, shape = E.world(E.CUBE)
T = len(held.trains)
rows, sites = s0.a.shape
n = lay.nb.shape[0]
K = int(lay.click.key[0, 0])
birth = int(s0.k[0, 0])
spokes = lay.spokes.tolist()
opp = [spokes.index([-x for x in e]) for e in spokes]
plus = [sp for sp, e in enumerate(spokes) if sum(e) == 1]
nb = lay.nb
partners = R.joined(lay.click, T)
edges = R.crossed(lay.click, T)
own_pairs = sorted({(min(t, v), max(t, v)) for t, ps in enumerate(partners) for v in ps})
mesh_sides = [(sp, t, v) for sp, t, v in edges if sp in plus]
two = np.flatnonzero(lay.gearing.drive.reshape(-1) != 1)
own_at = [t * T + v for t, v in own_pairs]
mesh_at = [(sp * T + t) * T + v for sp, t, v in mesh_sides]
print("cube world: edge key", K, "birth", birth, "+ Spokes", plus, "opp", opp, "own held", own_pairs,
      "Mesh held", mesh_sides, "rd held", two.tolist())


def reduce(s):
    a, b, r, rd, k = s
    return (a, b, r, rd[two], k[own_at], k[T * T:][mesh_at])


def expand_k(ko, km, fill, negate):
    k = np.full(((1 + n) * T * T, sites), fill, dtype=object)
    kk = k.reshape(1 + n, T, T, sites)
    for i, (t, v) in enumerate(own_pairs):
        kk[0, t, v] = ko[i]
        kk[0, v, t] = negate(ko[i])
    for j, (sp, t, v) in enumerate(mesh_sides):
        kk[1 + sp, t, v] = km[j]
        far = np.full(sites, fill, dtype=object)
        far[nb[sp]] = negate(km[j])
        kk[1 + opp[sp], v, t] = far
    return k


def expand(sr):
    rd = np.zeros((rows, sites), dtype=object)
    rd[two] = sr[3]
    return State(sr[0], sr[1], sr[2], rd, expand_k(sr[4], sr[5], birth, lambda x: K - 1 - x))


def act_reduced(sr):
    nb_, _, _, _, gearing, plan, clock, _, click, _, _ = lay
    a, b, tooth, rdh, ko, km = sr
    rd = np.zeros((rows, sites), dtype=object)
    rd[two] = rdh
    board = State(a, b, tooth, rd, None)
    force, j1 = step.sources(lay, a)
    teeth = gearing.drive
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(lay, board, step.driven(gearing, force, step.kick(gearing, first)))
    q, kept = step.drive(j, teeth, rd)
    kicks = step.kick(gearing, q)
    senses, push = step.halves(lay), step.driven(gearing, force, kicks)
    wa, wb = step.dials(lay, board)
    first, _, _ = step.gear(a, b, tooth, wa + wb, wa + wb, push, senses)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb, wa + step.weight(gearing, clock, first), push, senses)
    po = step.passing(click, plan, b, a, a1)[own_at]
    pm = step.crossing(click, nb_, b, a, a1)[mesh_at]
    qo, ko1 = carry(po, K, ko)
    qm, km1 = carry(pm, K, km)
    return (a1, b1, s1, kept[two], ko1, km1), expand_k(qo, qm, 0, lambda x: -x)


def same(x, y):
    return all(np.array_equal(np.asarray(p, dtype=object), np.asarray(q, dtype=object)) for p, q in zip(x, y))


# the run on the full act, then its reduced image; both on the pair law
s = s0
for _ in range(rounds):
    s, _ = step.act(lay, s)
sr = reduce(s)
assert same(expand(sr), s), "the full state left the pair law"
moved_mesh = int((sr[5] != birth).sum())
print("after", rounds, "rounds: held Mesh teeth entries off birth", moved_mesh, "of", sr[5].size,
      "; held own teeth off birth", int((sr[4] != birth).sum()), "of", sr[4].size)
out_r, c_r = act_reduced(sr)
out_f, c_f = step.act(lay, s)
assert same(expand(out_r), out_f) and same([c_r], [c_f]), "reduced act off the engine's"
stats = {"turns": 0, "reversing": 0, "law kept": 0, "flip seen": 0, "transport seen": 0, "commute state": 0,
         "commute clicks": 0}
for m in E.frame.turns():
    stats["turns"] += 1
    to = [spokes.index((m @ np.array(e, dtype=object)).tolist()) for e in spokes]
    t_full = E.spun(m, lay, held, s, shape)
    stats["law kept"] += int(same(expand(reduce(t_full)), t_full))
    g = reduce(t_full)
    # (2) on the held Mesh teeth: the image under the turn, by the pure transport of the held tooth or by its flip
    xyz, sides_ = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    site = np.ravel_multi_index(tuple((m @ xyz) % sides_), shape)
    rev = any(to[sp] not in plus for sp in plus)
    stats["reversing"] += int(rev)
    for j, (sp, t, v) in enumerate(mesh_sides):
        image = to[sp]
        if image in plus:
            jj = mesh_sides.index((image, t, v))
            stats["transport seen"] += int(np.array_equal(g[5][jj][site], sr[5][j]))
        else:
            jj = mesh_sides.index((opp[image], v, t))
            far_site = nb[image][site]  # the image edge's + end, across the - Spoke from the turned site
            stats["flip seen"] += int(np.array_equal(g[5][jj][far_site], K - 1 - sr[5][j]))
    # (3) the reduced act commutes with the reduced turn
    a_then_g = reduce(E.spun(m, lay, held, expand(out_r), shape))
    g_then_a, c_g = act_reduced(g)
    stats["commute state"] += int(same(a_then_g, g_then_a))
    turned_clicks = E.spun(m, lay, held, expand(out_r)._replace(k=c_r), shape).k
    stats["commute clicks"] += int(np.array_equal(turned_clicks, c_g))
print("24 on the reduced form:", stats)
print("END")
