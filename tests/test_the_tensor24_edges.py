"""Tensor24's Mesh edges, term 6's gradient vertex split by the Spoke it reads across (onelaw sections 1 and 3), on the mesh
world's own files at a test's key: the split the Mesh contraction itself, one coupling at both ends, every edge's books
closed, the run back exact with the teeth carried, the line's 8 turns and a cube's 24; each with its no."""

import json
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.engine import mesh, step
from tensor24.engine.contract import contract
from tensor24.engine.state import State
from tensor24.runner import load as loading
from tensor24.runner import run
from tensor24.runner.files import NAMES, sites_of
from tensor24.runner.rewind import rewind
from tests import frame

ROOT = Path(__file__).resolve().parents[1]
# odd and above 1, so the teeth move (the readers' B2 and B3), unlike the mesh world's key 3, which divides every passing
# there (their gcd 30000, AUDIT2's C): no Mesh tooth of a shipped world moves, but the click world's own-edge teeth do
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
            for c in range(held.trains[tied].dims[0])  # the tied train's first kind's components
        ]
        held, _ = loading.load(universe, setting, sites_of(shape), *made)
    return held, main.layout(universe, shape, held), State(*held.state), shape


def faces(laid, held):
    """The Mesh sides' view, (Spoke, t, u, site), of the sides after every train's own Node-clock's; each Spoke's opposite."""
    trains, spokes = len(held.trains), laid.spokes.tolist()
    opposite = [spokes.index([-x for x in e]) for e in spokes]
    return (lambda x: x[trains * trains :].reshape(len(spokes), trains, trains, -1)), opposite


def back(laid, s, far=None):
    """The state with every side read back at every Spoke, as the record's writer reads it (run.sided; D1 holds each Mesh edge at its + end), or by far."""
    return s._replace(k=run.faced(laid, s.k, far)) if far else run.sided(laid, s)


def closed(laid, held, q, s, far=None):
    """Every Mesh edge's two ends read back, (Spoke, t, u) at a site and (its opposite, u, t) across it: q negated, the teeth summing to key - 1."""
    (view, opposite), q, k = faces(laid, held), run.faced(laid, q, np.negative), back(laid, s, far).k
    far = np.take_along_axis(view(q)[opposite].swapaxes(1, 2), laid.nb[:, None, None, :], axis=-1)
    teeth = np.take_along_axis(view(k)[opposite].swapaxes(1, 2), laid.nb[:, None, None, :], axis=-1)
    return not (view(q) + far).any() and not (view(k) + teeth + 1 - laid.click.key[0, 0]).any()


def spun(m, laid, held, s, shape, far=None):
    """The state turned by m (frame.turned_by), every Mesh tooth read back, moved on to the turned Spoke with its site and held again at the
    + Spoke of each axis (D1: where m sends a + Spoke to a - one, the trains swapped and the tooth flipped, or a click negated by far)."""
    there, (view, _) = frame.turned_by(m, laid, held, back(laid, s, far), shape), faces(laid, held)
    to = [laid.spokes.tolist().index((m @ np.array(e)).tolist()) for e in laid.spokes.tolist()]
    moved, own = there.k.copy(), len(held.trains) ** 2
    view(moved)[to] = view(there.k)
    return there._replace(k=np.concatenate((moved[:own], view(moved)[::2].reshape(-1, moved.shape[-1]))))


def test_the_mesh_edges_are_the_mesh_contraction_one_coupling_at_both_ends_with_every_edges_books_closed():
    """Yes: across every Spoke the edges sum to the engine's Mesh contraction, 0 entries missed, kappa / two times it; each edge's two
    ends hold one coupling; every edge's books close in every round; the rounds run back exact, the teeth carried. No: a run back
    restarted at the teeth's birth misses, and the far end read back unflipped (D1's mutant) opens the books."""
    held, laid, start, _ = world()
    _, _, key, across, _ = laid.click
    scale, own, s, moved, nb = key[0, 0] // KEY, len(held.trains) ** 2, start, False, laid.nb
    assert across.any()
    for _ in range(ROUNDS):
        _, flat = step.readings(laid, s.a, mesh.stretches(laid, s.a))
        # each edge laid at its + end (D1), its far end the same coupling transposed across the opposite Spoke
        split = sum(c @ s.a[:, nb[x + x]] + c.T @ s.a[:, nb[x + x + 1]] for x, c in enumerate(across))
        assert frame.same([split], [scale * contract(laid.mesh, flat, s.a)])
        out, q = step.act(laid, s)
        assert closed(laid, held, q, out)
        s, moved = out, moved or q[own:].any()
    assert moved and frame.same(rewind(step.untick, laid, s, ROUNDS), start)
    assert not frame.same(rewind(step.untick, laid, s._replace(k=start.k), ROUNDS), start)
    assert not closed(laid, held, q, out, lambda k: k)  # the far end read back unflipped, D1's mutant


def test_the_mesh_edges_turn_with_the_lines_8_turns_and_a_cubes_24():
    """Yes: the mesh world's line past its first Mesh click, turned by each of the 8 turns that keep it, and a cube in memory of its
    lay's gears, turned by each of the 24, step to the round turned, the state, every Mesh tooth on its turned Spoke and every click.
    No: the Mesh teeth left on their Spokes under a turn that moves the axes miss."""
    for shape, kept in ((None, lambda m: abs(m[0, 0]) == 1), (CUBE, lambda m: True)):
        held, laid, s, shape = world(shape)
        for _ in range(ROUNDS):
            s, q = step.act(laid, s)
        out, q = step.act(laid, s)
        own = len(held.trains) * len(held.trains)
        assert q[own:].any()  # the Mesh edges carry in the turned round
        for m in [m for m in frame.turns() if kept(m)]:
            moved, p = step.act(laid, spun(m, laid, held, s, shape))
            assert frame.same(moved, spun(m, laid, held, out, shape))
            assert frame.same([p], [spun(m, laid, held, s._replace(k=q), shape, np.negative).k])
    m = next(m for m in frame.turns() if abs(m[0, 0]) != 1)
    assert not frame.same(frame.turned_by(m, laid, held, out, shape), spun(m, laid, held, out, shape))
