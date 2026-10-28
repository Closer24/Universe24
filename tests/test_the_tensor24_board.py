"""Tensor24's board: the neighbours and the Meshes from the shape, each Mesh alike at its two ends, the cone both ways."""

from types import SimpleNamespace

import numpy as np
import pytest

from tensor24.algebra.carry import carry, choose, nonneg
from tensor24.engine import step
from tensor24.engine.state import Layout, State
from tensor24.runner import board
from tests.frame import board as modelled
from tests.frame import meshes_of

SHAPES = ((3, 3, 3), (4, 5, 6), (3, 4, 7), (1, 1, 1), (7, 7, 7))
SIDE, GAMMA, ROUNDS = 7, 9, 60  # the cone's board, its full rate and its rounds


def model(m):
    """The neighbours and the Meshes equal the frame's, found by numpy's own wrap, at every shape."""
    built = [m.board(shape) for shape in SHAPES]
    wanted = [(modelled(shape), meshes_of(modelled(shape))) for shape in SHAPES]
    return all(
        np.array_equal(x, y)
        for pair in zip(built, wanted, strict=True)
        for x, y in zip(*pair, strict=True)
    )


def alike(m):
    """Each Mesh is held alike at its two ends: a site's +axis Spoke and its +axis neighbour's -axis Spoke."""
    for shape in SHAPES:
        nb, meshes = m.board(shape)
        if not all(
            np.array_equal(meshes[axis + axis], meshes[axis + axis + 1][nb[axis + axis]])
            for axis in range(3)
        ):
            return False
    return True


def lin(layout, s):
    """derive/asynchronous_read's lin: the neighbour read on the line toward a slot written a count ahead."""
    nb, meshes, grip, _, _, _ = layout
    a, b, _, _, _, c, tb, tn = s
    line = (
        b[:, nb]
        + carry((a[:, nb] - b[:, nb]) * (c[:, None, :] - tb[:, nb]), tn[:, nb] - tb[:, nb], 0)[0]
    )
    seen = choose(nonneg(c[:, None, :] - tn[:, nb]), a[:, nb], line)
    return ((seen - a[:, None, :]) * grip[meshes]).sum(axis=1)


def row(rng, low, high):
    """One integer per site, drawn in [low, high)."""
    return rng.integers(low, high, size=(1, SIDE**3)).astype(object)


def world(seed, rate=None):
    """A board of side SIDE parted at every site and Mesh, with its first state; the rates drawn, or one for all."""
    rng = np.random.default_rng(seed)
    nb, meshes = board.board((SIDE,) * 3)
    w, grip = row(rng, 1, 20), rng.integers(1, 4, size=3 * SIDE**3).astype(object)
    rates = row(rng, 0, GAMMA + 1) if rate is None else 0 * w + rate
    a, b, r, go, ph, zero = (
        row(rng, *ends) for ends in ((-99, 99), (-99, 99), (0, 1 << 20), (0, 2), (0, GAMMA), (0, 1))
    )
    return (
        Layout(nb, meshes, grip, w, rates, GAMMA),
        State(a, b, r % w, go, ph, zero, zero - 1, zero),
        rng,
    )


def distance():
    """Each site's Mesh distance from site 0 on the board of side SIDE."""
    xyz = np.indices((SIDE,) * 3).reshape(3, -1)
    return np.minimum(xyz, SIDE - xyz).sum(axis=0)


def changed(u):
    """The state with its gear at site 0 moved far."""
    change = (np.arange(SIDE**3) == 0).astype(object) * (1 << 40)
    return u._replace(a=u.a + change, b=u.b + change)


def early(first, far):
    """Some site reached below its distance, or none reached at all."""
    return ((first < far) & (far > 0)).any() or (first == ROUNDS).all()


def cone(m):
    """A change at one site reaches a site at Mesh distance d at no count below d, under random masks (David's p3)."""
    far = distance()
    for seed in range(3):
        layout, u, rng = world(seed)
        v, first = changed(u), far * 0 + ROUNDS
        for _ in range(ROUNDS):
            mask = row(rng, 0, 2)
            (u, _), (v, _) = m.tick(layout, u, mask), m.tick(layout, v, mask)
            fresh = (u.a[0] != v.a[0]) & (first == ROUNDS)
            first[fresh] = u.tn[0][fresh]
        if early(first, far):
            return False
    return True


def back(m):
    """Run back at the full rate, every clock ticking each round, a change reaches distance d in no fewer than d rounds."""
    far = distance()
    for seed in range(3):
        layout, u, _ = world(seed, GAMMA)
        outs = []
        for _ in range(SIDE + SIDE):
            u, out = m.tick(layout, u, 1)
            outs = [out, *outs]
        v, first = changed(u), far * 0 + ROUNDS
        for rounds, out in enumerate(outs, start=1):
            u, v = m.untick(layout, u, out), m.untick(layout, v, out)
            moved = (u.a[0] != v.a[0]) | (u.b[0] != v.b[0]) | (u.r[0] != v.r[0])
            first[moved & (first == ROUNDS)] = rounds
        if early(first, far):
            return False
    return True


def mutants():
    """Broken copies, each with the law that must catch it: what it replaces, and with what."""

    def wrapped_once(shape):
        nb, meshes = board.board(shape)
        return nb, np.stack([meshes[0], meshes[0], *meshes[2:]])

    def one_short(shape):
        nb, meshes = board.board(shape)
        return np.stack([nb[0], nb[0], *nb[2:]]), meshes

    def read_by_line(layout, s, allowed):
        saved, step.pull = step.pull, lin
        try:
            return step.tick(layout, s, allowed)
        finally:
            step.pull = saved

    return {
        "the -x neighbour taken as the +x": ("model", board, {"board": one_short}),
        "the -x Spoke holding the site's own Mesh": ("alike", board, {"board": wrapped_once}),
        "the read on the line toward the slot ahead": ("cone", step, {"tick": read_by_line}),
        "the run back reading two Meshes away": (
            "back",
            step,
            {
                "untick": lambda layout, s, o: step.untick(
                    layout._replace(nb=layout.nb[:, layout.nb[0]]), s, o
                )
            },
        ),
    }


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_law_of_the_board_holds_and_fails_on_its_mutant(mutant):
    name, module, broken = mutants()[mutant]
    law = {"model": model, "alike": alike, "cone": cone, "back": back}[name]
    assert law(module)
    assert not law(SimpleNamespace(**{**vars(module), **broken}))
