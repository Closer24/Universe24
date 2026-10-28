"""Tensor24's frame: its property tests on a trivial engine, each one failing on every mutant it must catch."""

import itertools

import numpy as np
import pytest

# a side of 5 or more: x + e, x - e, x + 2e and x - 2e are four sites, so no shift hides another
SHAPE = (5, 5, 5)
ASKEW = (3, 4, 5)  # a board the 24 do not keep: the images must fail on it


def board(shape):
    """The six neighbours of every site of the torus, the wrap by Rule3 on each coordinate."""
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def world(rng, shape, trains=2):
    """Both slots of every gear, whole numbers across 2**112, as Python integers in object arrays."""
    size = (trains, int(np.prod(shape)))
    return tuple(
        rng.integers(-(1 << 62), 1 << 62, size).astype(object) * (1 << 50)
        + rng.integers(-9, 9, size).astype(object)
        for _ in range(2)
    )


def same(xs, ys):
    """Equal at every gear, and Python integers throughout: no fixed width and no float."""
    return all(
        np.array_equal(x, y) and all(isinstance(v, int) for v in x.flat)
        for x, y in zip(xs, ys, strict=True)
    )


def trivial(nb, a, b):
    """Fredkin's second-order form on every train alike: a+ = (the six Meshes' sum of a) - a - b."""
    return a[:, nb].sum(axis=1) - a - b, a


def untrivial(nb, a, b):
    """The same form run back: the before slot from the now slot, a- = f(b) - a."""
    return b, b[:, nb].sum(axis=1) - b - a


def engine():
    """The trivial engine: its step and its own run back."""
    return trivial, untrivial


def local(make, shape, rng):
    """A site's two new slots read its seven sites alone: every gear beyond them changed, both slots, at every site."""
    (step, _), nb = make(), board(shape)
    a, b = world(rng, shape)
    out = step(nb, a, b)
    for site in range(nb.shape[1]):
        far = ~np.isin(np.arange(nb.shape[1]), [site, *nb[:, site]])
        moved = step(
            nb, *(np.where(far, new, old) for new, old in zip(world(rng, shape), (a, b), strict=True))
        )
        if not same([p[:, site] for p in moved], [p[:, site] for p in out]):
            return False
    return True


def pure(make, shape, rng):
    """Two worlds asked in turn of one engine, every input frozen, each answered as a fresh engine answers it."""
    nb, worlds = board(shape), [world(rng, shape) for _ in range(2)]
    for frozen in (nb, *worlds[0], *worlds[1]):
        frozen.flags.writeable = False
    fresh = [make()[0](nb, *w) for w in worlds]
    step = make()[0]
    return all(same(step(nb, *worlds[i % 2]), fresh[i % 2]) for i in range(4))


def renamed(make, shape, rng):
    """Every order of three trains orders the step's rows alike, and an inert fourth train leaves the three's bits."""
    (step, _), nb = make(), board(shape)
    a, b = world(rng, shape, 3)
    out, zero = step(nb, a, b), np.zeros((1, a.shape[1]), dtype=object)
    inert = step(nb, np.concatenate([a, zero]), np.concatenate([b, zero]))
    orders = [list(order) for order in itertools.permutations(range(3))]
    alike = all(same(step(nb, a[o], b[o]), [p[o] for p in out]) for o in orders)
    return alike and same([p[:3] for p in inert], out)


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
    """The board's moves, the 24 turns and the three unit translations that generate them all, move both slots alike."""
    (step, _), nb = make(), board(shape)
    a, b = world(rng, shape)
    out = step(nb, a, b)
    xyz, sides, e = np.indices(shape).reshape(3, -1), np.array(shape)[:, None], np.eye(3, dtype=int)
    for moved in [m @ xyz for m in turns()] + [xyz + e[:, [k]] for k in range(3)]:
        site = np.ravel_multi_index(tuple(moved % sides), shape)
        if np.unique(site).size < site.size:
            return False  # the move is no symmetry of this board
        a2, b2 = np.empty_like(a), np.empty_like(b)
        a2[:, site], b2[:, site] = a, b
        if not same([p[:, site] for p in step(nb, a2, b2)], out):
            return False
    return True


def naive(shape, a, b):
    """The same form site by site, with loops and neighbours found from the coordinates: the model the step is held to."""
    out = np.zeros_like(a)
    for g, x in itertools.product(range(len(a)), itertools.product(*map(range, shape))):
        near = [
            tuple((x[i] + d * (i == j)) % shape[i] for i in range(3)) for j in range(3) for d in (1, -1)
        ]
        here = np.ravel_multi_index(x, shape)
        out[g, here] = sum(a[g, np.ravel_multi_index(y, shape)] for y in near) - a[g, here] - b[g, here]
    return out, a


def formula(make, shape, rng):
    """The step equals the naive model at every gear of every site, both slots, as Python integers."""
    (step, _), nb = make(), board(shape)
    a, b = world(rng, shape)
    return same(step(nb, a, b), naive(shape, a, b))


def bijective(make, shape, rng):
    """The engine's own run back after the step, and the step after its run back, give the world back."""
    (step, unstep), nb = make(), board(shape)
    a, b = world(rng, shape)
    return same(unstep(nb, *step(nb, a, b)), (a, b)) and same(step(nb, *unstep(nb, a, b)), (a, b))


PROPERTIES = {"locality": local, "purity": pure, "rename": renamed, "images": turned}
PROPERTIES |= {"formula": formula, "bijectivity": bijective}


def broken(step):
    """An engine whose step is broken, its run back the trivial one."""
    return lambda: (step, untrivial)


def hidden(keep):
    """An engine holding a state between calls: what keep returns, given the worlds seen so far, is stepped."""

    def make():
        seen = []

        def step(nb, a, b):
            seen.append((a, b))
            return trivial(nb, *keep(seen))

        return step, untrivial

    return make


def two(nb):
    """The site one Mesh along +x and one along +y: two Meshes away, and no neighbour."""
    return nb[2][nb[0]]


def mark(n):
    """A column of n bits, 1 at row 0 alone."""
    return (np.arange(n) == 0).astype(object)[:, None]


def mutants():
    """Every broken engine with the property that must catch it: the frame's six and the hostile reader's ten."""
    return {
        "a Mesh read two away": ("locality", broken(lambda nb, a, b: trivial(nb, a[:, nb[0]], b))),
        "each Spoke taken twice": (
            "locality",
            broken(lambda nb, a, b: (a[:, np.stack([s[s] for s in nb])].sum(axis=1) - a - b, a)),
        ),
        "the before slot read two away": (
            "locality",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + b - b[:, two(nb)], a)),
        ),
        "the new before slot taken two away": (
            "locality",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0], a[:, two(nb)])),
        ),
        "a far site read through a carry": (
            "locality",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + (a[:, two(nb)] + 64) // 128, a)),
        ),
        "a counter": ("purity", hidden(lambda seen: (seen[-1][0] + len(seen) - 1, seen[-1][1]))),
        "the first call's world kept": ("purity", hidden(lambda seen: seen[0])),
        "the last call's world kept": ("purity", hidden(lambda seen: seen[max(len(seen) - 2, 0)])),
        "train 0 singled out": (
            "rename",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + mark(len(a)), a)),
        ),
        "the act scaled by the trains": (
            "rename",
            broken(lambda nb, a, b: ((a[:, nb].sum(axis=1) - a - b) * len(a) // 2, a)),
        ),
        "the +x Spoke weighted twice": (
            "images",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + a[:, nb[0]], a)),
        ),
        "site 0 marked": (
            "images",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + mark(a.shape[1]).T, a)),
        ),
        "a term dropped": ("formula", broken(lambda nb, a, b: (a[:, nb].sum(axis=1) - b, a))),
        "a clamp at 100": (
            "formula",
            broken(lambda nb, a, b: (np.minimum(trivial(nb, a, b)[0], 100), a)),
        ),
        "the width cut to 64 bits": (
            "formula",
            broken(lambda nb, a, b: tuple(x.astype(np.int64) for x in trivial(nb, a, b))),
        ),
        "the before slot dropped": (
            "bijectivity",
            broken(lambda nb, a, b: (a[:, nb].sum(axis=1) - a, a)),
        ),
    }


def holds(name, make, shape, seed):
    """Whether the property holds on the engine at one seed; an engine that overflows a fixed width does not."""
    try:
        return PROPERTIES[name](make, shape, np.random.default_rng(seed))
    except OverflowError:
        return False


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_property_holds_on_the_trivial_engine_and_fails_on_every_mutant_it_must_catch(mutant):
    name, make = mutants()[mutant]
    for seed in range(3):
        assert holds(name, engine, SHAPE, seed)
        assert not holds(name, make, SHAPE, seed)


def test_the_images_fail_on_a_board_the_24_do_not_keep():
    assert not holds("images", engine, ASKEW, 0)
