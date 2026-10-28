"""Tensor24's frame: its property tests on a trivial engine, each one failing on every mutant it must catch."""

import itertools

import numpy as np
import pytest

from tests.frame import Engine, holds, near

# a side of 5 or more: x + e, x - e, x + 2e and x - 2e are four sites, so no shift hides another
SHAPE = (5, 5, 5)
ASKEW = (3, 4, 5)  # a board the 24 do not keep: the images must fail on it


def world(rng, shape, trains):
    """Both slots of every gear, whole numbers across 2**112, as Python integers in object arrays."""
    size = (trains, int(np.prod(shape)))
    return tuple(
        rng.integers(-(1 << 62), 1 << 62, size).astype(object) * (1 << 50)
        + rng.integers(-9, 9, size).astype(object)
        for _ in range(2)
    )


def trivial(nb, a, b):
    """Fredkin's second-order form on every train alike: a+ = (the six Meshes' sum of a) - a - b."""
    return a[:, nb].sum(axis=1) - a - b, a


def untrivial(nb, a, b):
    """The same form run back: the before slot from the now slot, a- = f(b) - a."""
    return b, b[:, nb].sum(axis=1) - b - a


def naive(shape, s):
    """The same form site by site, with loops and neighbours found from the coordinates."""
    a, b = s
    out = np.zeros_like(a)
    for g, x in itertools.product(range(len(a)), itertools.product(*map(range, shape))):
        here = np.ravel_multi_index(x, shape)
        around = sum(a[g, np.ravel_multi_index(y, shape)] for y in near(x, shape))
        out[g, here] = around - a[g, here] - b[g, here]
    return (out, a), ()


def broken(step):
    """An engine of the form step(nb, a, b), its out empty and its run back the trivial one."""
    return lambda: Engine(
        lambda nb, s: (step(nb, *s), ()), lambda nb, s, out: untrivial(nb, *s), world, naive
    )


def hidden(keep):
    """An engine holding a state between calls: what keep returns, given the worlds seen so far, is stepped."""

    def make():
        seen = []

        def step(nb, a, b):
            seen.append((a, b))
            return trivial(nb, *keep(seen))

        return broken(step)()

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


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_property_holds_on_the_trivial_engine_and_fails_on_every_mutant_it_must_catch(mutant):
    name, make = mutants()[mutant]
    for seed in range(3):
        assert holds(name, broken(trivial), SHAPE, seed)
        assert not holds(name, make, SHAPE, seed)


def test_the_images_fail_on_a_board_the_24_do_not_keep():
    assert not holds("images", broken(trivial), ASKEW, 0)
