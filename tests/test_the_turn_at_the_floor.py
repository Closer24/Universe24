"""The turn at the top and at the floor (ALGEBRA.md, The swap at the top, the law's fifth act, and The floor, its second trigger): the act reads the gapped time line of the holder of the volume, whose rest is the Node's clock's one level, the pair (den - den div Gamma, den) (loader/universe.volume_pair; ALGEBRA.md, The volume holder's rest is the clock's one level); a Node whose three levels show a weak maximum turns, and a Node whose output would fall below the floor X_f = volume_of(Gamma, -Gamma), the least volume with a reading, turns the same way: the interval ends at the state it started from with every line's two levels exchanged and every remainder complemented at its wall (swap.at_top, swap.at_floor, swap.acted); the inverse is the same reading on the undone interval and restores the pre-state bit for bit. Both are driven on the bare 3-cube torus of the tests' small universe by hand: the light emptied so that nothing sources the held row, its time line set at every Node at a top or falling toward the floor."""

from pathlib import Path

import numpy as np
import pytest

from event_universe import records, swap, world_files
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import CUBE, GAMMA, bare_torus


def turning(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, now: int, before: int) -> None:
    """The bare 3-cube with the light emptied and the held row's time line at (now, before) on every Node, the remainder as laid: one interval forward turns every Node, the pre-state with the two levels exchanged, the time line's remainder complemented at its wall w, the swap logged at the interval 1 for the 27 Nodes; one interval back restores the pre-state bit for bit."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path, CUBE)))
    held, light = board.held[0], board.world.seed
    den = board.families[held].pair[1]
    assert light is not None and board.families[held].pair == (
        den - den // GAMMA,
        den,
    )  # the clock's level
    full, states = lambda level: records.full(board.shape, level, board.kind), board.states  # noqa: E731
    states[light].lines[0] = records.Record(full(0), full(0), states[light].lines[0].remainder)
    remainder = np.asarray(states[held].lines[0].remainder, dtype=object).copy()
    states[held].lines[0] = records.Record(full(now), full(before), states[held].lines[0].remainder)
    kept = board_state(board)
    board.step()
    time, wall = board.states[held].lines[0], wall_of(den, GAMMA, board.unit)
    assert (time.now == before).all() and (time.before == now).all()
    assert (np.asarray(time.remainder, dtype=object) == wall - 1 - remainder).all()
    assert board.swaps == [(1, 1, CUBE**3)]
    board.step_inverse()
    assert board.interval == 0 and same_state(board_state(board), kept)


def test_a_top_turns_every_node(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The time line at Gamma + 2 now and Gamma + 1 before with no source: the free step gives 2 X1 - X0 less Rule3's own mass on the volume, 2 X1 / Gamma at the vacuum's paces, below X1, so the top's trigger fires on the triple at every Node; the turn and its inverse."""
    assert swap.at_top(GAMMA + 1, GAMMA + 2, GAMMA + 1).all()
    turning(tmp_path, monkeypatch, GAMMA + 2, GAMMA + 1)


def test_the_floor_turns_as_the_top_does(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The floor X_f is swap.floor_of(Gamma); the time line at X_f + 1 now and X_f + 3 before with no source steps to X_f - 1, below the floor, so the floor's trigger fires on the triple at every Node where the top's does not; the turn and its inverse."""
    floor = swap.floor_of(GAMMA)
    triple = (floor + 3, floor + 1, floor - 1)  # X0, X1 and the output X2 the free step gives, 2 X1 - X0
    assert not swap.at_top(*triple).any() and swap.at_floor(triple[0], triple[2], floor).all()
    turning(tmp_path, monkeypatch, floor + 1, floor + 3)
