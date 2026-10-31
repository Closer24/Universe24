"""The plan's property tests for any engine of Tensor24: locality, purity, rename, the 24's images and the run back;
the board, its Spokes and its Meshes they are read on, the half-open split on the edge's dial, and a test's lay of the
three files with no strength chosen, never a shipped world."""

import hashlib
import importlib
import itertools
import json
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

import numpy as np

from tensor24.engine import kinds
from tensor24.engine.state import Plan, Read, State
from tensor24.runner.files import NAMES

ROOT = Path(__file__).resolve().parents[1]


class Engine(NamedTuple):
    """An engine as the properties see it: its step and run back on a board, and its worlds."""

    step: Callable[..., Any]  # step(nb, s) -> s', s a tuple of arrays: a row per train, or one row
    unstep: Callable[..., Any]  # unstep(nb, s') -> s
    world: Callable[..., Any]  # world(rng, shape, trains) -> s


def board(shape):
    """The six neighbours of every site of the torus, the wrap by Rule3 on each coordinate."""
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def near(x, shape):
    """The six neighbours of the site x, found from its coordinates alone, in the board's order."""
    return [tuple((x[i] + d * (i == j)) % shape[i] for i in range(3)) for j in range(3) for d in (1, -1)]


def flat(state):
    """A step's new state as one row of arrays."""
    return [*state]


def wide(rng, size):
    """Whole numbers whose every bit is drawn, across 2**256 either side of 0, as Python integers."""
    # the second review (227cde2fe): a cut to 128 bits and a far read through a carry passed narrower worlds
    limbs = [rng.integers(0, 1 << 62, size).astype(object) << (62 * k) for k in range(5)]
    return sum(limbs) - (1 << 309)


def same(xs, ys):
    """Equal at every entry, and Python integers throughout: no fixed width, no float and no truth value."""
    return all(
        np.array_equal(x, y) and all(type(v) is int for v in x.flat) for x, y in zip(xs, ys, strict=True)
    )


def local(make, shape, rng):
    """A site's new state reads its seven sites alone: every entry beyond them changed, at every site."""
    e, nb = make(), board(shape)
    s = e.world(rng, shape, 2)
    out = flat(e.step(nb, s))
    for site in range(nb.shape[1]):
        far = ~np.isin(np.arange(nb.shape[1]), [site, *nb[:, site]])
        fresh = e.world(rng, shape, 2)
        moved = flat(
            e.step(nb, tuple(np.where(far, new, old) for new, old in zip(fresh, s, strict=True)))
        )
        if not same([p[:, site] for p in moved], [p[:, site] for p in out]):
            return False
    return True


def pure(make, shape, rng):
    """Two worlds asked in turn of one engine, every input frozen, each answered as a fresh engine answers it."""
    nb, worlds = board(shape), [make().world(rng, shape, 2) for _ in range(2)]
    for frozen in (nb, *worlds[0], *worlds[1]):
        frozen.flags.writeable = False
    fresh = [flat(make().step(nb, w)) for w in worlds]
    step = make().step
    return all(same(flat(step(nb, worlds[i % 2])), fresh[i % 2]) for i in range(4))


def renamed(make, shape, rng):
    """Every order of three trains orders the trains' rows alike, and three inert trains more leave the rest's bits."""
    e, nb = make(), board(shape)
    s = e.world(rng, shape, 3)
    out = flat(e.step(nb, s))

    def ordered(xs, o):
        return [x[o] if len(x) == 3 else x for x in xs]

    orders = map(list, itertools.permutations(range(3)))
    alike = all(same(flat(e.step(nb, tuple(ordered(s, o)))), ordered(out, o)) for o in orders)
    inert = tuple(np.concatenate([x, 0 * x]) if len(x) == 3 else x for x in s)
    return alike and same([p[:3] for p in flat(e.step(nb, inert))], [p[:3] for p in out])


def turns():
    """The 24 turns of the cube: the signed permutations of the axes with determinant +1."""
    for order, signs in itertools.product(
        itertools.permutations(range(3)), itertools.product((1, -1), repeat=3)
    ):
        m = np.zeros((3, 3), dtype=int)
        m[range(3), order] = signs
        if np.dot(m[0], np.cross(m[1], m[2])) == 1:
            yield m


def turned(make, shape, rng, trains=2):
    """The board's moves, the 24 turns and the three unit translations that generate them all, move the step alike."""
    e, nb = make(), board(shape)
    s = e.world(rng, shape, trains)
    out = flat(e.step(nb, s))
    xyz, sides, unit = np.indices(shape).reshape(3, -1), np.array(shape)[:, None], np.eye(3, dtype=int)
    for moved in [m @ xyz for m in turns()] + [xyz + unit[:, [k]] for k in range(3)]:
        site = np.ravel_multi_index(tuple(moved % sides), shape)
        if np.unique(site).size < site.size:
            return False  # the move is no symmetry of this board
        there = tuple(np.empty_like(x) for x in s)
        for x, y in zip(there, s, strict=True):
            x[:, site] = y
        if not same([p[:, site] for p in flat(e.step(nb, there))], out):
            return False
    return True


def bijective(make, shape, rng):
    """A fresh engine runs back another's steps of two worlds, in their order, and a step undoes its run back."""
    nb, (s, t) = board(shape), [make().world(rng, shape, 2) for _ in range(2)]
    e = make()
    s1, t1 = e.step(nb, s), e.step(nb, t)
    back = make().unstep
    undone = same(back(nb, s1), s) and same(back(nb, t1), t)
    # a now slot doubled and halved back passes the rewind alone, and fails forth
    forth = same(flat(make().step(nb, make().unstep(nb, s))), [*s])
    return undone and forth


PROPERTIES = {
    "locality": local,
    "purity": pure,
    "rename": renamed,
    "images": turned,
    "bijectivity": bijective,
}


def digest(xs):
    """One hash of a row of arrays, entry by entry."""
    return hashlib.sha256(repr([x.tolist() for x in xs]).encode()).hexdigest()


def answer(module, factory, shape, seeds):
    """The digest of the step of the last seed's world, by the engine the factory names, after the earlier seeds'."""
    e, nb = getattr(importlib.import_module(module), factory)(), board(shape)
    return digest(
        [flat(e.step(nb, e.world(np.random.default_rng(seed), shape, 2))) for seed in seeds][-1]
    )


def fresh(code, args, hash_seed=0, given=""):
    """What a fresh interpreter prints, the tests and src on its path, at a hash seed."""
    paths = os.pathsep.join([str(ROOT), str(ROOT / "src")])
    env = {**os.environ, "PYTHONHASHSEED": str(hash_seed), "PYTHONPATH": paths}
    run = subprocess.run(
        [sys.executable, "-c", code, *args],
        cwd=ROOT,
        env=env,
        input=given,
        capture_output=True,
        text=True,
    )
    return run.stdout.strip() or run.stderr


def unseeded(module, factory, shape):
    """Purity across interpreters: a world answered here after another, and in fresh ones at three hash seeds, alike."""
    here = answer(module, factory, shape, [1, 0])
    code = "import json, sys; from tests.frame import answer; print(answer(*sys.argv[1:3], *map(json.loads, sys.argv[3:])))"
    args = [module, factory, json.dumps(shape), json.dumps([0])]
    return all(fresh(code, args, hash_seed) == here for hash_seed in (1, 2, 3))


def undone_elsewhere(module, factory, shape, seed):
    """The run back in a fresh interpreter that never stepped, from the stepped state alone."""
    e, nb = getattr(importlib.import_module(module), factory)(), board(shape)
    s = e.world(np.random.default_rng(seed), shape, 2)
    rows = [x.tolist() for x in e.step(nb, s)]
    code = (
        "import importlib, json, sys; import numpy as np; from tests.frame import board, digest; "
        "d = json.loads(sys.stdin.read()); e = getattr(importlib.import_module(d['module']), d['factory'])(); "
        "rows = [np.array(x, dtype=object) for x in d['rows']]; "
        "print(digest(e.unstep(board(tuple(d['shape'])), tuple(rows))))"
    )
    given = json.dumps({"module": module, "factory": factory, "shape": shape, "rows": rows})
    return fresh(code, [], 0, given) == digest(s)


def turned_by(m, laid, held, s, shape):
    """The state turned by m: sites moved, each train's rows by its kinds' matrices block by block, its parts alike, a negated
    row's tooth flipped on its dial, -1 - s, as the mirror flips it, every click tooth moved with its site."""
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    site = np.ravel_multi_index(tuple((m @ xyz) % sides), shape)
    acting = kinds.kinds(m[None, :, :])
    turn = np.eye(len(laid.gearing.rest), dtype=object)
    for train in held.trains:
        blocks, before = (
            [kinds.square(acting)[0]] if train.square else [acting[k][0] for k in train.kinds],
            0,
        )
        for matrix in blocks:
            at, before = (
                train.first + (before + np.arange(len(matrix))) * train.part,
                before + len(matrix),
            )
            for part in range(train.part):
                turn[np.ix_(at + part, at + part)] = matrix
    there = State(*(np.empty_like(x) for x in s))
    for x, y in zip(there, s, strict=True):
        x[:, site] = y
    there.a[:, site], there.b[:, site] = turn @ s.a, turn @ s.b
    there.r[:, site] = (turn @ (s.r + s.r + 1) - 1) // 2  # s on a kept row, -1 - s on a negated one
    return there


def opposed(clicks, teeth, key, trains):
    """Every edge's two sides at its own Node-clock, (t, u) at t trains + u and (u, t): their quotients summing to 0, their teeth to key - 1."""
    q, k = (x[: trains * trains].reshape(trains, trains, -1) for x in (clicks, teeth))
    return not (q + q.swapaxes(0, 1)).any() and not (k + k.swapaxes(0, 1) + 1 - key).any()


def meshes_of(nb):
    """Each Spoke's Mesh, one per axis and site: along +axis the site's own, along -axis its -axis neighbour's."""
    axes, n = np.arange(len(nb)) // 2, nb.shape[1]
    own, theirs = axes[:, None] * n + np.arange(n)[None, :], axes[:, None] * n + nb
    return np.where((np.arange(len(nb)) % 2 == 0)[:, None], own, theirs)


def spokes(axes=3):
    """Each Spoke's direction in the board's order, +axis then -axis for every axis: the steps board() takes."""
    return np.array([sign * axis for axis in np.eye(axes, dtype=int) for sign in (1, -1)], dtype=object)


def split(n, d):
    """The split of n at the dial 2 d from its half, with plain integers: n = q 2d + s, -d <= s < d."""
    q, r = divmod(n + d, d + d)
    return q, r - d


def unread():
    """The clocks' read of no term: every gear's teeth its rest."""
    none = np.zeros(0, dtype=np.intp)
    return Read(none, none.astype(object), none)


def unclocked():
    """The clocks' plan of no term: every gear's teeth its rest."""
    none = np.zeros(0, dtype=np.intp)
    return Plan(np.zeros((1, 0), dtype=np.intp), none.astype(object), none)


def dense(read, rows, landed):
    """A linear read, a Read or a plan of one-leg terms, as the matrix of its whole factors, per row it lands on and row it reads, the factors summed."""
    (first,) = read.legs if isinstance(read, Plan) else (read.first,)
    m = np.zeros((landed, rows), dtype=object)
    np.add.at(m, (read.target, first), read.factor)
    return m


def strengthless():
    """A test's lay, never a shipped world: the board's wave and the square on a 4 x 4 x 4 board, every strength 0 and the
    key 1, no monomial joining the two (no edge, so no click line), one wave gear moving at site 0, 10 ticks; by name."""
    den = 1  # every pinion den, the seed's
    trains = [{"name": "wave", "kinds": ["A1"], "part": 2, "pinion": den}]
    trains += [{"name": "square", "kinds": ["A1", "T1", "A1", "E", "T2"], "part": 1, "pinion": den}]
    chosen = {"key": 1, "push": 0, "notch": 0, "hold": 0, "spring": 0, "tie": 0, "mesh": 0}
    integers = {"den": den, "full_rate": 1000, "width": 128}
    universe = {"version": 1, "integers": integers, "chosen": chosen, "trains": trains}
    setting = {"version": 1, "ticks": 10, "gears": [[0, 0, 0, 1, 0, 0]]}
    return {"universe": universe, "piece": {"version": 1, "shape": [4, 4, 4]}, "setting": setting}


def pair_world():
    """A pair world of one Node-clock, NOT_CLOSED 37's (the first hostile code reader's M3; the seventh's rulings: the held hand at rest,
    and no assert that it runs away), its three files: the held hand (1, 0), its before its now, its spring CHOSEN at the grip at rest, den
    Gamma^2, the giver at its turning point at 14 and the taker at rest, at Gamma 1000, the hands' tie 9600 and the key 614401 odd."""
    den = 1  # every pinion den, the seed's
    hand = {"name": "held", "kinds": ["A1", "A2"], "part": 1, "pinion": den}
    pair = {"kinds": ["T1", "T2"], "part": 1, "pinion": den}
    trains = [hand, {"name": "giver", **pair}, {"name": "taker", **pair}]
    integers = {"den": den, "full_rate": 1000, "width": 128}
    grip = den * integers["full_rate"] * integers["full_rate"]  # the grip at rest, the spring's rule
    chosen = {"key": 614401, "push": 0, "notch": 0, "hold": 1, "spring": grip, "tie": 9600, "mesh": 0}
    world = {"version": 1, "integers": integers, "chosen": chosen, "trains": trains}
    gears = [[0, 0, 0, 1, 1, 0], [1, 0, 0, 14, 14, 0]]  # the held hand at rest, as every pulse
    laid_ = {"version": 1, "ticks": 1260, "gears": gears}
    return {"universe": world, "piece": {"version": 1, "shape": [1, 1, 1]}, "setting": laid_}


def written(folder, files):
    """The three files written as JSON in the folder under their names: their paths, in the files' order."""
    folder.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        folder.joinpath(f"{name}.json").write_text(json.dumps(files[name]), encoding="utf-8")
    return [folder / f"{name}.json" for name in NAMES]
