"""The turn at the floor (ALGEBRA.md, The floor, the law's fifth act's second trigger: a Node whose time line's output would fall below the floor X_f turns as it turns at the top, ending the interval at the state it started from with every line's two levels exchanged and every remainder complemented at its wall, X_f = volume_of(Gamma, -Gamma) the least volume with a reading; swap.at_floor, swap.floor_of, swap.acted). The one universe's course reaches no floor in 2,400 intervals (the record's legend reads 0 turns at the floor), so the act is driven on the bare 3-cube torus of the one universe file by hand: the light emptied so that nothing sources the held row, its time line set falling toward the floor, the step's output below it at every Node."""

from pathlib import Path

import numpy as np
import pytest

from event_universe import records, swap, world_files
from event_universe.core.rule3 import wall_of
from event_universe.features import volume
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import CUBE, bare_torus, flat


def test_a_node_whose_output_would_fall_below_the_floor_turns_as_at_the_top(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The floor X_f is volume_of(Gamma, -Gamma); the time line at X_f + 1 now and X_f + 3 before with no source steps to X_f - 1, below the floor, so the floor's trigger fires on the triple at every Node where the top's does not; after the interval every Node holds the pre-state with the two levels exchanged (X_f + 3 now, X_f + 1 before), the time line's remainder complemented at its wall w and every write remainder at its own wall, the swap logged at the interval 1 for the 27 Nodes; the inverse is the same reading on the undone interval and restores the pre-state bit for bit."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path, CUBE)))
    held, light, gamma = board.held[0], board.world.seed, board.world.node_clock
    assert light is not None
    floor = swap.floor_of(gamma)
    assert floor == int(
        np.asarray(volume.volume_of(gamma, np.array([-gamma], dtype=object))).reshape(-1)[0]
    )
    zeros = records.zeros(board.shape, board.kind)
    board.states[light].lines[0] = records.Record(
        zeros, zeros.copy(), board.states[light].lines[0].remainder
    )
    time = board.states[held].lines[0]
    now, before = (
        records.full(board.shape, floor + 1, board.kind),
        records.full(board.shape, floor + 3, board.kind),
    )
    board.states[held].lines[0] = records.Record(now, before, time.remainder)
    pre = board_state(board)
    remainder = np.asarray(time.remainder, dtype=object).copy()
    write_remainders = [np.asarray(r, dtype=object).copy() for r in board.states[held].write_remainders]
    triple = (floor + 3, floor + 1, floor - 1)  # X0, X1 and the output X2 the free step gives, 2 X1 - X0
    assert not swap.at_top(*triple).any() and swap.at_floor(*triple, floor).all()
    board.step()
    assert board.swaps == [(1, 1, CUBE**3)]
    turned = board.states[held].lines[0]
    assert flat(turned.now) == [floor + 3] * CUBE**3 and flat(turned.before) == [floor + 1] * CUBE**3
    wall = wall_of(board.families[held].pair[1], gamma, board.unit)
    assert np.array_equal(
        np.asarray(turned.remainder, dtype=object), records.complement(remainder, wall)
    )
    for kept, after, own in zip(
        write_remainders, board.states[held].write_remainders, board.write_walls[held], strict=True
    ):
        assert np.array_equal(
            np.asarray(after, dtype=object), records.complement(kept, np.asarray(own, dtype=object))
        )
    board.step_inverse()
    assert board.interval == 0 and same_state(board_state(board), pre)
