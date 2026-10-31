"""Tensor24's Mesh edges, term 6's gradient vertex split by the Spoke it reads across (onelaw sections 1 and 3), on the mesh
world's own files at a test's key: the split the Mesh contraction itself, one coupling at both ends, every edge's books
closed, the run back exact with the teeth carried, the line's 8 turns and a cube's 24; each with its no."""

import json
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.engine import step
from tensor24.engine.contract import contract
from tensor24.engine.state import State
from tensor24.runner import load as loading
from tensor24.runner.files import NAMES, sites_of
from tensor24.runner.rewind import rewind
from tests import frame

ROOT = Path(__file__).resolve().parents[1]
# odd and above 1, so the teeth move (the readers' B2 and B3); never a world's: the mesh world's key 3 divides every
# passing there (their gcd 30000, AUDIT2's C), so no tooth of a shipped world moves; a finer key is the owner's batch
KEY = 1000003
ROUNDS = 25  # the mesh world's rounds past its first Mesh click, round 20 on its lay
CUBE = [3, 3, 3]  # a cube in memory


def world(cube=None):
    """The mesh world's files at the test's key, on its line, or on a cube in memory with its lay's gears at the cube's sites and,
    the test's lay, the tied hand's components at the held hand's counts where the wave is laid, so its Mesh edges carry at once."""
    folder = ROOT / "examples" / "tensor24-mesh"
    universe, piece, setting = (json.loads((folder / f"{n}.json").read_text("utf-8")) for n in NAMES)
    universe["chosen"]["key"], shape = KEY, cube or piece["shape"]
    setting["gears"] = [g for g in setting["gears"] if g[2] < sites_of(shape)]
    made = main.made(loading.star(len(shape)))
    held, _ = loading.load(universe, setting, sites_of(shape), *made)
    if cube:
        (tied,) = [n for n in range(len(held.trains)) if held.trains.tied[n]]
        hand, wave = (g for g in setting["gears"] if held.trains.held[g[0]]), list(setting["gears"])
        counts = next(hand)[3:]  # the held hand's now, before and tooth
        setting["gears"] += [
            [tied, c, g[2], *counts]
            for g in wave
            if not held.trains.held[g[0]]
            for c in range(len(cube))
        ]
        held, _ = loading.load(universe, setting, sites_of(shape), *made)
    return held, main.layout(universe, shape, held), State(*held.state), shape


def faces(laid, held):
    """The Mesh sides' view, (Spoke, t, u, site), of the sides after every train's own Node-clock's; each Spoke's opposite."""
    trains, spokes = len(held.trains), laid.spokes.tolist()
    opposite = [spokes.index([-x for x in e]) for e in spokes]
    return (lambda x: x[trains * trains :].reshape(len(spokes), trains, trains, -1)), opposite


def closed(laid, held, q, k):
    """Every Mesh edge's two ends, (Spoke, t, u) at a site and (its opposite, u, t) across it: q negated, the teeth summing to key - 1."""
    view, opposite = faces(laid, held)
    far = np.take_along_axis(view(q)[opposite].swapaxes(1, 2), laid.nb[:, None, None, :], axis=-1)
    teeth = np.take_along_axis(view(k)[opposite].swapaxes(1, 2), laid.nb[:, None, None, :], axis=-1)
    return not (view(q) + far).any() and not (view(k) + teeth + 1 - laid.click.key[0, 0]).any()


def spun(m, laid, held, s, shape):
    """The state turned by m (frame.turned_by), every Mesh tooth moved on to the turned Spoke with its site."""
    there, (view, _) = frame.turned_by(m, laid, held, s, shape), faces(laid, held)
    to = [
        laid.spokes.tolist().index((m @ np.array(e, dtype=object)).tolist())
        for e in laid.spokes.tolist()
    ]
    moved = there.k.copy()
    view(moved)[to] = view(there.k)
    return there._replace(k=moved)


def test_the_mesh_edges_are_the_mesh_contraction_one_coupling_at_both_ends_with_every_edges_books_closed():
    """Yes: across every Spoke the edges sum to the engine's Mesh contraction, 0 entries missed, kappa / two times it; each edge's two
    ends hold one coupling; every edge's books close in every round; the rounds run back exact, the teeth carried. No: a run back
    restarted at the teeth's birth misses, and one tooth born one past its complement opens the books."""
    held, laid, start, _ = world()
    _, _, key, across, _ = laid.click
    scale, (_, opposite) = key[0, 0] // KEY, faces(laid, held)
    assert frame.same([across], [np.stack([across[x].T for x in opposite])]) and across.any()
    s, moved = start, False
    for _ in range(ROUNDS):
        _, flat = step.readings(laid, s.a)
        split = sum(across[x] @ s.a[:, laid.nb[x]] for x in range(len(across)))
        assert frame.same([split], [scale * contract(laid.mesh, flat, s.a)])
        out, q = step.act(laid, s)
        assert closed(laid, held, q, out.k)
        s, moved = out, moved or faces(laid, held)[0](q).any()
    assert moved and frame.same(rewind(step.untick, laid, s, ROUNDS), start)
    assert not frame.same(rewind(step.untick, laid, s._replace(k=start.k), ROUNDS), start)
    off = start.k.copy()
    faces(laid, held)[0](off)[0] += (
        1  # every Mesh side across the first Spoke born one past its complement
    )
    out, q = step.act(laid, s._replace(k=off))
    assert not closed(laid, held, q, out.k)


def test_the_mesh_edges_turn_with_the_lines_8_turns_and_a_cubes_24():
    """Yes: the mesh world's line past its first Mesh click, turned by each of the 8 turns that keep it, and a cube in memory of its
    lay's gears, turned by each of the 24, step to the round turned, the state, every Mesh tooth on its turned Spoke and every click.
    No: the Mesh teeth left on their Spokes under a turn that moves the axes miss."""
    for shape, kept in ((None, lambda m: abs(m[0, 0]) == 1), (CUBE, lambda m: True)):
        held, laid, s, shape = world(shape)
        for _ in range(ROUNDS):
            s, q = step.act(laid, s)
        out, q = step.act(laid, s)
        assert faces(laid, held)[0](q).any()  # the Mesh edges carry in the turned round
        for m in [m for m in frame.turns() if kept(m)]:
            moved, p = step.act(laid, spun(m, laid, held, s, shape))
            assert frame.same(moved, spun(m, laid, held, out, shape))
            assert frame.same([p], [spun(m, laid, held, s._replace(k=q), shape).k])
    stayed = frame.turned_by(next(m for m in frame.turns() if abs(m[0, 0]) != 1), laid, held, out, shape)
    assert not frame.same(
        stayed, spun(next(m for m in frame.turns() if abs(m[0, 0]) != 1), laid, held, out, shape)
    )
