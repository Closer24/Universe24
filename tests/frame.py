"""The plan's property tests for any engine of Tensor24: locality, purity, rename, the 24's images, the formula, the run back."""

import itertools
from collections.abc import Callable
from typing import Any, NamedTuple

import numpy as np


class Engine(NamedTuple):
    """An engine as the properties see it: its step and run back on a board, its worlds, and its naive model."""

    step: Callable[
        ..., Any
    ]  # step(nb, s) -> (s', out), s a tuple of arrays: a row per train, or one row
    unstep: Callable[..., Any]  # unstep(nb, s', out) -> s
    world: Callable[..., Any]  # world(rng, shape, trains) -> s
    naive: Callable[..., Any]  # naive(shape, s) -> (s', out), site by site with loops


def board(shape):
    """The six neighbours of every site of the torus, the wrap by Rule3 on each coordinate."""
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def near(x, shape):
    """The six neighbours of the site x, found from its coordinates alone, in the board's order."""
    return [tuple((x[i] + d * (i == j)) % shape[i] for i in range(3)) for j in range(3) for d in (1, -1)]


def flat(result):
    """A step's new state and its out as one row of arrays."""
    state, out = result
    return [*state, *out]


def same(xs, ys):
    """Equal at every entry, and Python integers throughout: no fixed width and no float."""
    return all(
        np.array_equal(x, y) and all(isinstance(v, int) for v in x.flat)
        for x, y in zip(xs, ys, strict=True)
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
    """Every order of three trains orders the trains' rows alike, and an inert fourth train leaves the rest's bits."""
    e, nb = make(), board(shape)
    s = e.world(rng, shape, 3)
    out = flat(e.step(nb, s))

    def ordered(xs, o):
        return [x[o] if len(x) == 3 else x for x in xs]

    orders = map(list, itertools.permutations(range(3)))
    alike = all(same(flat(e.step(nb, tuple(ordered(s, o)))), ordered(out, o)) for o in orders)
    inert = tuple(np.concatenate([x, 0 * x[:1]]) if len(x) == 3 else x for x in s)
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


def turned(make, shape, rng):
    """The board's moves, the 24 turns and the three unit translations that generate them all, move the step alike."""
    e, nb = make(), board(shape)
    s = e.world(rng, shape, 2)
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


def formula(make, shape, rng):
    """The step equals the engine's naive model at every entry of every site, as Python integers."""
    e, nb = make(), board(shape)
    s = e.world(rng, shape, 2)
    return same(flat(e.step(nb, s)), flat(e.naive(shape, s)))


def bijective(make, shape, rng):
    """The engine's own run back undoes the step; where the step puts out nothing, the step undoes the run back."""
    e, nb = make(), board(shape)
    s, x = e.world(rng, shape, 2), e.world(rng, shape, 2)
    state, out = e.step(nb, s)
    forth = bool(out) or same(flat(e.step(nb, e.unstep(nb, x, out))), [*x])
    return same(e.unstep(nb, state, out), s) and forth


PROPERTIES = {"locality": local, "purity": pure, "rename": renamed, "images": turned}
PROPERTIES |= {"formula": formula, "bijectivity": bijective}


def holds(name, make, shape, seed):
    """Whether the property holds on the engine at one seed; an engine that overflows a fixed width does not."""
    try:
        return PROPERTIES[name](make, shape, np.random.default_rng(seed))
    except OverflowError:
        return False
