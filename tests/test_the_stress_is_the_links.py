"""The stress is the Links' (ALGEBRA.md, a proposal under its own name, 2026-10-23; the builder's derivation M21): the tension's part of a record on each axis at a Node is the square of the Node's centred difference, weight x (now_(i+a) - now_(i-a))^2, read at the doubled wall 2 E_s W_c, in place of the former -weight x (now_(i-a) now_(i+a) - now_i^2) at E_s W_c. Tested: the board sums of the former reading and the new one equal to the bit on a wrapped board, for a plane wave, for a one-Node record and for random levels (the new over its doubled wall, the former over its wall); the reading invariant under the shift of every level by one number where the former gains m Delta_a a; even under the axis's inversion; a one-Node record's parts 0 at its Node and the level squared at each of its two neighbours on the axis; the loader's tension lines at the doubled wall, the shear lines' wall; and a wrapped world with a structured record stepped and run back bit for bit."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np

from event_universe import node, readings, world_files
from event_universe.core.ports import AXES, Wrap
from event_universe.features.read import link_tensions
from event_universe.lattice import Lattice
from event_universe.loader.derived import held_write_of
from event_universe.meeting_back import first_difference, snapshot
from event_universe.records import Record
from event_universe.world_files import load_world
from tests.laws import EVENTS, UNIVERSE

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
    """A -> a + m leaves every part as it stands where the former gains m Delta_a a; the board reflected along an axis reads the reflected parts; a one-Node record's part is 0 at the Node and its level squared at the two neighbours on each axis, the former's -a^2 at the Node and 0 beside it, the same sum."""
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
    """The loader: gravity's three tension lines at 2 E_s W_c = 2 x level_weight x 3 den T x the row's write wall, twice the former, the shear lines' wall where the shear is declared; a 5-cube torus with the matter record structured by hand stepped 6 intervals and run back 6, the snapshot bit for bit."""
    document = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    (tmp_path / "u.json").write_text(json.dumps(document), encoding="utf-8")
    world = dict(
        shape=[5, 5, 5], boundary={a: "periodic" for a in "xyz"}, intervals=10, universe="u.json"
    )
    world.update(bodies=[], node_detectors=[])
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


def test_the_three_clumps_edge_at_one_node_holds_the_tension_below_gamma_through_the_top_and_names_the_returns_growth() -> (
    None
):
    """The structured board's clause of The stress is the Links' (the owner's question of 2026-10-23, derived at one Node and read once): the three-clump 5-cube torus at Gamma 1,000 (examples/events/m20/m19_lay3_g1000.json, gravity gapped [999, 1000], the matter clumps 1,350 / 850 / 425 quanta on z), its extreme levels the clump's top 5,374 against the void's 0 one Link away; at the clump's edge Node [2, 2, 0] the act reads the z part num x 5,374^2 = 19,233,997,416 and the x and y parts 0, the traceless write per interval at the vacuum's paces (2 / 3 and -1 / 3 of it over the doubled wall 2 E_s W_c = 216,000,000, the time line's trace apart) 59 on z and -30 on x and y, the Link [2, 2, 0]-[2, 2, 1] read at 48 after the first interval (the mean of the two ends, 59 and 37), below Gamma; the static bound at the Node: Rule3's traceless Link term relaxes a line by R / (3 w) = num p^2 / (9 den Gamma^2), 1 / 9 per Link difference per interval at the vacuum's paces, so a source S per interval at one Node stands at 9 G_5(0) S with G_5(0) = 0.2081 the 5-cube torus's lattice Green's function at the source, 110 levels at S = 59, and the Link's mean of the source Node and its neighbour 9 (G_5(0) + G_5(1)) S / 2 = 67, every bound below Gamma 1,000 and falling as e^(-U) after the lay (the write's factor e^(-5 U) against the stiffness e^(-4 U)): the tension HOLDS below Gamma through the top. Through a return it does not follow from the reading: the step conserves the shear's momentum (X / Gamma) T', so a velocity at the top is amplified by X_top / X_return at the return (738 on this lay's first return by the record, 5,359,666 over 7,264), and 738 times the one-interval write 59 passes Gamma 1,000 by a factor 43: the returns' growth is the contraction's, bounded by the gap (which sets X_top and the return's depth) and the clump's amplitude (which sets the write), not by the stress's reading. The exact condition on a lay under which the course closes at the Node's bound: a gravity row without a gap (no return, the matter era alone) closes iff 9 G_5(0) k_w num (2 / 3) a_top^2 / (2 E_s W_c) < Gamma, a_top^2 < Gamma E_s W_c / (3 G_5(0) k_w num), the clump's top level below 16,100 on this lay's integers against its 5,374 (the margin 3.0 in the level, 9 in the write); a gapped row's returns add the contraction's growth, a course quantity named in FURTHER_RESEARCH.md."""
    world = load_world(EVENTS / "m20" / "m19_lay3_g1000.json")
    board = Lattice(world)
    names = [family.name for family in board.families]
    matter, gravity = names.index("matter"), names.index("gravity")
    record = board.states[matter].lines[0]
    levels = np.asarray(record.now, dtype=object)
    assert [int(levels[2, 2, k]) for k in range(5)] == [0, 5374, 4264, 3015, 0]
    num = board.families[matter].pair[0]
    parts = readings.stresses_of(num, [record], board.wrap)
    assert [int(part[2, 2, 0]) for part in parts] == [0, 0, num * 5374 * 5374]
    write = held_write_of(board.families, gravity, world.quantum_action, world.link_unit)
    assert write.walls[1] == 2 * 3 * 1000 * 36000 == 216_000_000
    board.step()
    lines = [np.asarray(board.states[gravity].lines[1 + a].now, dtype=object) for a in range(3)]
    assert [int(line[2, 2, 0]) for line in lines] == [-30, -30, 59]
    assert [int(line[2, 2, 1]) for line in lines] == [-19, -19, 37]
    _content, axes = node.read_lines(matter, board.families, board.states, 1, world.node_clock, 0)
    tensions = link_tensions(axes, board.wrap, world.node_clock)
    largest = max(int(np.asarray(t).max()) for t in tensions)
    assert largest == 48 < world.node_clock
    source = 59
    waves = [k for k in itertools.product(range(5), repeat=3) if k != (0, 0, 0)]
    denominators = [6 - 2 * sum(math.cos(2 * math.pi * ki / 5) for ki in k) for k in waves]
    green_0 = sum(1 / d for d in denominators) / 125
    green_1 = (
        sum(math.cos(2 * math.pi * k[2] / 5) / d for k, d in zip(waves, denominators, strict=True)) / 125
    )
    assert round(green_0, 4) == 0.2081 and 9 * green_0 * source < 111 < world.node_clock
    assert 9 * (green_0 + green_1) / 2 * source < 67 < world.node_clock  # the Link's static mean
    assert 5_359_666 // 7_264 == 737 and 737 * source > 43 * world.node_clock  # the return's growth
    edge = (
        world.node_clock * 108_000_000 * 10_000 // (3 * num * 2081)
    )  # a_top^2 below Gamma E_s W_c / (3 G_5(0) k_w num)
    assert 5374 * 5374 < edge and 16_100**2 < edge < 16_200**2
    assert (
        9 * green_0 * (2 * num * 16_200**2 // (3 * 216_000_000)) > world.node_clock
    )  # the edge of the condition
