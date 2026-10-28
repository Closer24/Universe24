"""Tensor24's frame: its property tests on a trivial engine, each one failing on its own mutant."""

import itertools

import numpy as np
import pytest

SIDE = 3  # a side of 3 or more: on a side of 2, x + e is x - e and hides a sign error


def board():
    """The six neighbours of every site of the cubic torus, the wrap by Rule3 on the coordinates."""
    xyz = np.indices((SIDE,) * 3).reshape(3, -1)
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % SIDE), (SIDE,) * 3) for s in steps])


def trivial(nb, a, b):
    """Fredkin's second-order form on every train alike: a+ = (the six Meshes' sum of a) - a - b."""
    return a[:, nb].sum(axis=1) - a - b, a


def untrivial(nb, a, b):
    """The same form run back: the before slot from the now slot, a- = f(b) - a."""
    return b, b[:, nb].sum(axis=1) - b - a


def mutants():
    """One broken copy per property, each changing one thing the property must see."""
    calls = itertools.count()
    first = (np.arange(2) == 0)[:, None]
    return {
        "locality": lambda nb, a, b: trivial(nb, a[:, nb[0]], b),
        "purity": lambda nb, a, b: (trivial(nb, a, b)[0] + next(calls), a),
        "rename": lambda nb, a, b: (trivial(nb, a, b)[0] + first, a),
        "images": lambda nb, a, b: (trivial(nb, a, b)[0] + a[:, nb[0]], a),
        "formula": lambda nb, a, b: (a[:, nb].sum(axis=1) - b, a),
        "bijectivity": lambda nb, a, b: (a[:, nb].sum(axis=1) - a, a),
    }


def local(step, nb, a, b):
    """A change at one site reaches its six neighbours in one tick, and no site beyond them."""
    poked = a.copy()
    poked[:, 0] += 1
    moved = (step(nb, poked, b)[0] != step(nb, a, b)[0]).astype(bool).any(axis=0)
    return set(np.flatnonzero(moved)) <= {0, *nb[:, 0]}


def pure(step, nb, a, b):
    """With every input frozen, two calls give the same bits."""
    for frozen in (nb, a, b):
        frozen.flags.writeable = False
    return all((p == q).all() for p, q in zip(step(nb, a, b), step(nb, a, b), strict=True))


def renamed(step, nb, a, b):
    """Renaming the trains renames the step's rows alike."""
    order = np.roll(np.arange(len(a)), 1)
    alike = zip(step(nb, a, b), step(nb, a[order], b[order]), strict=True)
    return all((p[order] == q).all() for p, q in alike)


def turns():
    """The 24 turns of the cube: the signed permutations of the axes with determinant +1."""
    for order, signs in itertools.product(
        itertools.permutations(range(3)), itertools.product((1, -1), repeat=3)
    ):
        m = np.zeros((3, 3), dtype=int)
        m[range(3), order] = signs
        if np.dot(m[0], np.cross(m[1], m[2])) == 1:
            yield m


def turned(step, nb, a, b):
    """Each turn of the cube, applied to the board, commutes with the step."""
    xyz = np.indices((SIDE,) * 3).reshape(3, -1)
    for m in turns():
        site = np.ravel_multi_index(tuple((m @ xyz) % SIDE), (SIDE,) * 3)
        a2, b2 = np.empty_like(a), np.empty_like(b)
        a2[:, site], b2[:, site] = a, b
        if not (step(nb, a2, b2)[0][:, site] == step(nb, a, b)[0]).all():
            return False
    return True


def naive(nb, a, b):
    """The same form site by site, with loops: the model the vectorized step is held to."""
    out = np.zeros_like(a)
    for g, x in itertools.product(range(a.shape[0]), range(a.shape[1])):
        out[g, x] = sum(a[g, y] for y in nb[:, x]) - a[g, x] - b[g, x]
    return out, a


def formula(step, nb, a, b):
    """The step equals the naive model at every gear of every site."""
    return all((p == q).all() for p, q in zip(step(nb, a, b), naive(nb, a, b), strict=True))


def bijective(step, nb, a, b):
    """The step run back after the step, and the step after it is run back, are the identity."""
    back, forth = untrivial(nb, *step(nb, a, b)), step(nb, *untrivial(nb, a, b))
    return all((p == q).all() for p, q in zip(back + forth, (a, b, a, b), strict=True))


@pytest.mark.parametrize("name", ["locality", "purity", "rename", "images", "formula", "bijectivity"])
def test_each_property_holds_on_the_trivial_engine_and_fails_on_its_mutant(name):
    holds = {"locality": local, "purity": pure, "rename": renamed, "images": turned}
    holds = holds | {"formula": formula, "bijectivity": bijective}
    rng = np.random.default_rng(20261028)
    a, b = (rng.integers(-9, 9, size=(2, SIDE**3)).astype(object) for _ in range(2))
    assert holds[name](trivial, board(), a.copy(), b.copy())
    assert not holds[name](mutants()[name], board(), a.copy(), b.copy())
