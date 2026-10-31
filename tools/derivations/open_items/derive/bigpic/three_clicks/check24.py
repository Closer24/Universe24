"""The 24 on the edge clicks: the lay turned by each of the cube's 24 turns (sites moved, each train's rows by its
kind's matrix, a negated row's tooth flipped, as tests/test_the_tensor24_run.py's turned does) runs to the same
clicks, each moved to its turned Node-clock, in the first click and in the third."""
import itertools, sys
import numpy as np
src = sys.argv[1]; rounds = int(sys.argv[2]); world_dir = sys.argv[3] if len(sys.argv) > 3 else "tensor24-click"
sys.path.insert(0, src); sys.path.insert(0, ".")
import edgeclick as E
from tensor24.engine import kinds, state

def turns():
    for order, signs in itertools.product(itertools.permutations(range(3)), itertools.product((1, -1), repeat=3)):
        m = np.zeros((3, 3), dtype=int); m[range(3), order] = signs
        if np.dot(m[0], np.cross(m[1], m[2])) == 1:
            yield m

def turned(m, laid, held, s, shape):
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    site = np.ravel_multi_index(tuple((m @ xyz) % sides), shape)
    acting = kinds.kinds(m[None, :, :])
    turn = np.eye(len(laid.gearing.rest), dtype=object)
    for train in held.trains:
        matrix = kinds.square(acting)[0] if train.square else acting[train.kinds[0]][0]
        at = train.first + np.arange(len(matrix)) * train.part
        for part in range(train.part):
            turn[np.ix_(at + part, at + part)] = matrix
    there = state.State(*(np.empty_like(x) for x in s))
    for x, y in zip(there, s, strict=True):
        x[:, site] = y
    there.a[:, site], there.b[:, site] = turn @ s.a, turn @ s.b
    there.r[:, site] = (turn @ (s.r + s.r + 1) - 1) // 2
    return there, site

universe, shape, held, lay, s0, world = E.load_world(src, world_dir)
for mode in (0, 1):
    base = E.run_from(lay, s0, world, rounds, mode)
    want = sorted(base["lines"])
    ok = 0; ms = []
    for m in turns():
        xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
        if np.unique(np.ravel_multi_index(tuple((m @ xyz) % sides), shape)).size == xyz.shape[1]:
            ms.append(m)  # the turns that are symmetries of this board
    for m in ms:
        s1, site = turned(m, lay, held, s0, shape)
        got = E.run_from(lay, s1, world, rounds, mode)
        moved = sorted((t, int(site[x]), tr, q) for (t, x, tr, q) in base["lines"])
        ok += sorted(got["lines"]) == moved
    print(f"{world_dir}, {'third click (turned)' if mode else 'first click (carried)'}: {ok} of {len(ms)} turns give the"
          f" same clicks at the turned Node-clocks over {rounds} rounds ({len(want)} click lines)")
