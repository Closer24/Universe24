"""The 24 on THIRD7's member itself (tri7.Member), after check24gen.py and Big Pic's check24.py: every turn of the cube
that is a symmetry of the board turns the lay (sites moved, each train's rows by its kind's matrix, a negated row's tooth
flipped), the board steps by step.act unchanged, David's split gives each edge's flow, and the member books the clicks;
the record must be the lay's record moved to the turned Node-clocks: the lines, the sides and the triangle's landings.
Whole numbers only (numpy holds the board's integers, as in check24.py). argv: src, rounds, world folder name."""
import itertools
import sys
from pathlib import Path

import numpy as np

SRC, ROUNDS = sys.argv[1], int(sys.argv[2])
WNAME = sys.argv[3] if len(sys.argv) > 3 else "tensor24-click"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds, state, step  # noqa: E402


def turns():
    for order, signs in itertools.product(itertools.permutations(range(3)), itertools.product((1, -1), repeat=3)):
        m = np.zeros((3, 3), dtype=int)
        m[range(3), order] = signs
        if np.dot(m[0], np.cross(m[1], m[2])) == 1:
            yield m


def turned(m, laid, held, s, shape):
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    site = np.ravel_multi_index(tuple(carry(m @ xyz, sides, 0)[1]), shape)
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
    there.r[:, site] = carry(turn @ (s.r + s.r + 1) - 1, 2, 0)[0]
    return there, site


universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", WNAME))
LAID = len(sys.argv) > 4 and sys.argv[4] == "laid"
if LAID:  # Big Pic's laid stand-in (edgeclick.board_lay, VARY1's, labelled so): the Node-clocks set apart
    sys.path.insert(0, str(HERE.joinpath("bp")))
    import edgeclick as E

    s0 = E.board_lay(s0, shape, world)
    WNAME = WNAME + ", the laid stand-in"
rows, sites = s0.a.shape
key = int(lay.click.key[0, 0])
pairs, triangles = tri7.edge_set(world)
D = star["half"] * key
member = tri7.Member(len(pairs), triangles, D, star["senses"])


def record(s):
    teeth = [member.birth() for _ in range(sites)]
    lines, sides, paths = [], [], []
    for t in range(ROUNDS):
        s1, _ = step.act(lay, s)
        for x in range(sites):
            b = [int(s.b[r, x]) for r in range(rows)]
            a = [int(s.a[r, x]) for r in range(rows)]
            a1 = [int(s1.a[r, x]) for r in range(rows)]
            fl = world.split_flows(0, b, a, a1)
            q, w = member.step([fl.get(pr, 0) for pr in pairs], *teeth[x])
            sides += [(t, x, e, c) for e, c in enumerate(q) if c]
            lines += tri7.lines_of(pairs, world.trains, t, x, q)
            paths += [(t, x, i, v) for i, v in enumerate(w) if v]
        s = s1
    return lines, sides, paths


base = record(s0)
ms = []
for m in turns():
    xyz, sd = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    if np.unique(np.ravel_multi_index(tuple(carry(m @ xyz, sd, 0)[1]), shape)).size == xyz.shape[1]:
        ms.append(m)
ok = [0, 0, 0]
for m in ms:
    s1, site = turned(m, lay, held, s0, shape)
    got = record(s1)
    for k in range(3):
        moved = sorted((z[0], int(site[z[1]])) + tuple(z[2:]) for z in base[k])
        ok[k] += sorted(got[k]) == moved
print(f"{WNAME}, the member (the triangle's own tooth pair), {ROUNDS} rounds: of {len(ms)} turns, {ok[0]} give the same"
      f" lines at the turned Node-clocks ({len(base[0])} lines), {ok[1]} the same sides ({len(base[1])}), {ok[2]} the"
      f" same landings ({len(base[2])})")
