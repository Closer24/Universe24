"""The stress is the Links' (ALGEBRA.md, a proposal under its own name, 2026-10-23; the builder's derivation M21): the tension's part of a record on each axis at a Node is the square of the Node's centred difference, weight x (now_(i+a) - now_(i-a))^2, read at the doubled wall 2 E_s W_c, in place of the former -weight x (now_(i-a) now_(i+a) - now_i^2) at E_s W_c. Tested: the board sums of the former reading and the new one equal to the bit on a wrapped board, for a plane wave, for a one-Node record and for random levels (the new over its doubled wall, the former over its wall); the reading invariant under the shift of every level by one number where the former gains m Delta_a a; even under the axis's inversion; a one-Node record's parts 0 at its Node and the level squared at each of its two neighbours on the axis; the loader's tension lines at the doubled wall, the shear lines' wall; and a wrapped world with a structured record stepped and run back bit for bit."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from event_universe import readings, world_files
from event_universe.core.ports import AXES, Wrap
from event_universe.lattice import Lattice
from event_universe.loader.derived import held_write_of
from event_universe.meeting_back import first_difference, snapshot
from event_universe.records import Record
from event_universe.world_files import load_world

WRAP = Wrap(True, True, True)


def former(weight: int, now: np.ndarray) -> list[np.ndarray]:
    """The former reading by hand, -weight x (now_(i-a) now_(i+a) - now_i^2) per axis, the wrapped neighbours."""
    return [-weight * (np.roll(now, 1, a) * np.roll(now, -1, a) - now * now) for a in range(AXES)]


def reading(weight: int, now: np.ndarray) -> list[np.ndarray]:
    return [np.asarray(part) for part in readings.stresses_of(weight, [Record(now, now, 0 * now)], WRAP)]


def test_the_board_sums_of_the_former_and_the_new_reading_are_equal_to_the_bit_on_a_wrapped_board() -> (
    None
):
    """The identity h_a = a Delta_a a - grad_+ grad_- and the torus sum of a Delta_a a = -SUM grad^2: the new reading's board sum over its doubled wall is the former's over its wall, 2 SUM(-h_a) = SUM (a_+ - a_-)^2, for a plane wave along an axis, a one-Node record and forty random integer boards, every axis."""
    draw = np.random.default_rng(2023)
    shape = (6, 4, 5)
    wave = np.take(np.array([2000, 1000, -1000, -2000, -1000, 1000]), np.indices(shape)[0])
    one = np.zeros(shape, dtype=np.int64)
    one[2, 1, 3] = 1353
    boards = [wave, one] + [draw.integers(-3000, 3000, shape) for _ in range(40)]
    for now in boards:
        old, new = former(7, now), reading(7, now)
        for a in range(AXES):
            assert 2 * int(old[a].sum(dtype=object)) == int(new[a].sum(dtype=object))
    assert all(int(part.sum()) == 2 * 6 * (3 * 2000 * 2000 // 4) * 20 for part in reading(1, wave)[:1])


def test_the_reading_is_invariant_under_the_shift_and_even_under_the_inversion_and_reads_a_one_node_record_at_its_neighbours() -> (
    None
):
    """A -> a + m leaves every part unchanged where the former gains m Delta_a a; the board reflected along an axis reads the reflected parts; a one-Node record's part is 0 at the Node and its level squared at the two neighbours on each axis, the former's -a^2 at the Node and 0 beside it, the same sum."""
    draw = np.random.default_rng(31)
    shape = (5, 5, 5)
    now = draw.integers(-500, 500, shape)
    for m in (1, -3, 75_000):
        shifted = reading(3, now + m)
        assert all(np.array_equal(s, p) for s, p in zip(shifted, reading(3, now), strict=True))
        gained = [f - g for f, g in zip(former(3, now + m), former(3, now), strict=True)]
        for a in range(AXES):
            delta = np.roll(now, -1, a) + np.roll(now, 1, a) - 2 * now
            assert np.array_equal(gained[a], -3 * m * delta)
    for a in range(AXES):
        mirrored = reading(3, np.flip(now, a))
        assert all(
            np.array_equal(np.flip(p, a), q) for p, q in zip(reading(3, now), mirrored, strict=True)
        )
    one = np.zeros(shape, dtype=np.int64)
    one[2, 2, 2] = 1353
    parts = reading(1, one)
    for a in range(AXES):
        at = [2, 2, 2]
        assert parts[a][2, 2, 2] == 0 and int(parts[a].sum()) == 2 * 1353 * 1353
        for side in (1, -1):
            at[a] = 2 + side
            assert parts[a][tuple(at)] == 1353 * 1353


def test_the_tension_lines_write_at_the_doubled_wall_and_a_wrapped_world_runs_back(
    tmp_path: Path,
) -> None:
    """The loader: gravity's three tension lines at 2 E_s W_c = 2 x level_weight x 3 den T x the row's write wall, twice the former, the shear lines' wall where the shear is declared; a 5-cube torus of the three-clump universe (no holder of the sign) with the matter record structured by hand stepped 6 intervals and run back 6, the snapshot bit for bit through the fifth act's fires at the void's pinned rest."""
    document = {  # the three-clump universe, examples/events/m20/universe_m19_lay3_g1000.json in the derived form (2026-10-24): gravity, dust and matter, no holder of the sign, so the reading's test is independent of the charge, and the fifth act refuses a holder under the rotation at a top by name; light the seed family, laid at one quantum on every Node
        "integers": {"node_clock": 1000, "quantum_action": 36000, "link_unit": 16},
        "families": [
            {"name": "gravity", "pair": [999, 1000]},
            {"name": "dust", "pair": [0, 1000], "dimension": 1},
            {"name": "matter", "pair": [666, 1000], "dimension": 1},
            {"name": "light", "pair": [1000, 1000], "dimension": 1},
        ],
    }
    (tmp_path / "u.json").write_text(json.dumps(document), encoding="utf-8")
    world = dict(shape=[5, 5, 5], intervals=10, universe="u.json")
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    world_files.REPOSITORY_ROOT = tmp_path
    loaded = load_world(path)
    board = Lattice(loaded)
    names = [family.name for family in board.families]
    matter, gravity = names.index("matter"), names.index("gravity")
    row, action = board.families[gravity], loaded.quantum_action
    write = held_write_of(board.families, gravity, action, loaded.link_unit)
    dens = {board.families[r].pair[1] for r in range(len(names)) if board.families[r].quanta}
    assert len(dens) == 1
    expected = 2 * row.level_weight * 3 * dens.pop() * action * row.write_wall
    assert (
        list(write.walls[1 : 1 + AXES]) == [expected] * AXES
        and write.walls[0] == row.level_weight * action * row.write_wall
    )
    draw = np.random.default_rng(7)
    line = board.states[matter].lines[0]
    blob = draw.integers(0, 400, (5, 5, 5)).astype(line.now.dtype)
    board.states[matter].lines[0] = Record(blob, blob, line.remainder)
    kept = snapshot(board)
    for _ in range(6):
        board.step()
    assert all(
        np.asarray(part).any()
        for part in readings.stresses_of(4000, [Record(blob, blob, 0 * blob)], WRAP)
    )
    for _ in range(6):
        board.step_inverse()
    assert first_difference(kept, snapshot(board)) is None
