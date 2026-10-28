"""Tensor24's frame: its property tests on a trivial engine, each one failing on every mutant it must catch."""

import itertools

import numpy as np
import pytest

from tests.frame import STORED, Engine, digest, holds, near, turned, undone_elsewhere, unseeded, wide

# a side of 5 or more: x + e, x - e, x + 2e and x - 2e are four sites, so no shift hides another
SHAPE = (5, 5, 5)
ASKEW = (3, 4, 5)  # a board the 24 do not keep: the images must fail on it


def world(rng, shape, trains):
    """Both slots of every gear, every bit drawn across 2**256, as Python integers in object arrays."""
    return tuple(wide(rng, (trains, int(np.prod(shape)))) for _ in range(2))


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


def logged():
    """An engine that loses half its act and whose run back reads the log its step hid."""
    log = []

    def step(nb, s):
        log.append(s)
        a, b = trivial(nb, *s)
        return (a // 2, b), ()

    return Engine(step, lambda nb, s, out: log.pop(0) if log else s, world, naive)


HELD = {}  # the module-level state a cached, a fifo or a memo engine keeps, which a fresh interpreter has not


def engine():
    """The trivial engine, named for a fresh interpreter."""
    return broken(trivial)()


def cached():
    """An engine whose step answers every world of a shape as it answered the first: state held in the module."""
    return broken(lambda nb, a, b: HELD.setdefault(a.shape, trivial(nb, a, b)))()


def salted():
    """An engine whose step reads the interpreter's hash seed."""
    return broken(lambda nb, a, b: (trivial(nb, a, b)[0] + (hash("tensor24") & 1), a))()


def fifo():
    """An engine whose run back pops the worlds its steps queued in the module, the state and the out unread."""
    queue = HELD.setdefault("queue", [])

    def step(nb, s):
        queue.append(s)
        return trivial(nb, *s), (0 * s[0][:1],)

    return Engine(step, lambda nb, s, out: queue.pop(0) if queue else s, world, naive)


def memo():
    """An engine whose run back looks the stepped state up among the worlds its steps kept in the module."""
    kept = HELD.setdefault("memo", {})

    def step(nb, s):
        new = trivial(nb, *s)
        kept[digest(new)] = s
        return new, (0 * s[0][:1],)

    return Engine(step, lambda nb, s, out: kept.get(digest(s), s), world, naive)


def two(nb):
    """The site one Mesh along +x and one along +y: two Meshes away, and no neighbour."""
    return nb[2][nb[0]]


def fed(a, into, by):
    """Row by added into row into, where the world holds both: a step that mixes two components at every site alike."""
    out = 0 * a
    if len(a) > max(into, by):
        out[into] = a[by]
    return out


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
        "both x Spokes weighted twice": (
            "images",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + a[:, nb[0]] + a[:, nb[1]], a)),
        ),
        "A2 fed into A1": ("kinds", broken(lambda nb, a, b: (trivial(nb, a, b)[0] + fed(a, 0, 1), a))),
        "T1's second component fed into its first": (
            "kinds",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + fed(a, 1 + 1, 3), a)),
        ),
        "a tension fed by T1": (
            "kinds",
            broken(lambda nb, a, b: (trivial(nb, a, b)[0] + fed(a, 8, 1 + 1), a)),
        ),
        "the before slot dropped": (
            "bijectivity",
            broken(lambda nb, a, b: (a[:, nb].sum(axis=1) - a, a)),
        ),
        "a hidden log": ("bijectivity", logged),
    }


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_property_holds_on_the_trivial_engine_and_fails_on_every_mutant_it_must_catch(mutant):
    name, make = mutants()[mutant]
    for seed in range(3):
        assert holds(name, broken(trivial), SHAPE, seed)
        assert not holds(name, make, SHAPE, seed)


def test_the_images_fail_on_a_board_the_24_do_not_keep():
    assert not holds("images", broken(trivial), ASKEW, 0)
    assert not holds("kinds", broken(trivial), ASKEW, 0)


def test_the_mixing_mutants_pass_the_images_of_the_sites_alone_on_every_stored_kind():
    for name in ("A2 fed into A1", "T1's second component fed into its first", "a tension fed by T1"):
        assert turned(mutants()[name][1], SHAPE, np.random.default_rng(0), STORED)


@pytest.mark.parametrize("factory, pure", [("engine", True), ("cached", False), ("salted", False)])
def test_a_world_is_answered_alike_in_fresh_interpreters_at_other_hash_seeds(factory, pure):
    assert unseeded(__name__, factory, SHAPE) == pure


@pytest.mark.parametrize("factory, honest", [("engine", True), ("fifo", False), ("memo", False)])
def test_a_world_is_run_back_in_a_fresh_interpreter_that_never_stepped(factory, honest):
    HELD.clear()
    for seed in range(3):
        assert holds("bijectivity", globals()[factory], SHAPE, seed)
    assert undone_elsewhere(__name__, factory, SHAPE, 0) == honest
