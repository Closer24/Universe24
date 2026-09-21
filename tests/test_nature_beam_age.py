"""The age of a ray kept whole and read by a measured event (docs/BEAM_LAW.md,
section 2 the age and its bound, section 3 steps 2 and 5, section 10 note
24; the model owner, 2026-09-19, Highlights 5.4, "the clock beside a mass
... go for it"): the age is the count of intervals since the measured event
that created the ray (a birth or a re-emission; a collision keeps it), kept
whole on the record; the flight reads it modulo the direction's period and
the collision never reads it; a measured event, the external thing, reads
it whole as the age moment of the one reading (sum amount x age, `reads:
"age"`), which its clock counts; since clock-age-v1 (2026-09-21) by default
on every entry, the presence on an entry that reads `presence`. The GameBoard's step
is unchanged by the whole age. The expected integers of
docs/TEST_EXPECTATIONS.md ("The age"), written down first:

(a) the age whole: a ray on +x from x = 0 of an open 301 x 1 x 1 bar
    carries the age 200 after 200 intervals (200 mod 55 = 35 until
    2026-09-20) at x = m(200) = 116; a head-on pair at the ages 59 on an
    open 9 x 1 x 1 bar (x = 3 on +x, x = 5 on -x) meets at x = 4 at the
    first interval with the ages 60, parks in the rest slots with the ages
    kept (60, 60), turns onto +z and -z at the second interval still at 60
    (the rest pair leaves on z), ages to 61 at the third without a step
    (m(61) = m(60) = 35) and, still meeting, turns onto +y and -y (the
    class cycle +z-z -> +y-y), then steps at the fourth (m(62) = 36) and
    clicks on the y faces of the open bar (the bar declares `age_bound` 128
    for the declared ages); a ray of age 59 met by a `rerelease` Node is
    created again at age 0; a release is born at age 0;
(b) the age moment: three rays of amounts 1, 2, 4 at the ages 3, 5, 7 read
    the age moment 3 + 10 + 28 = 41 and the scalar 7; with a ray that did
    not step (amount 2, age 10) the here part is 20 and the whole 61; the
    48 signed axis permutations fix it; the keyed form over Nodes equals
    the readings Node by Node; without ages the moment is 0; an amount x
    age beyond 2^62 - 1 is refused before any product is formed;
    `count_component` selects `age` for every key but `presence`, which
    selects `scalar` (clock-age-v1, 2026-09-21; until then `age` for `age`
    and `scalar` for every other key);
(c) the clock: a source of `m` (content 1) at x = 0 of an open 5 x 1 x 1
    bar at `release` [1, 1] and a fixed reader of `light` (content 1) at
    x = 3 whose entry reads `age` at `suspension` [1, 4]: a ray born at
    tick b is at x = 3 at the ages 5 and 6 (ticks b + 5 and b + 6), so
    from tick 7 the reader counts the age moment 5 + 6 = 11 over a
    presence of 2 (5 over 1 at tick 6) and owes the count its owed
    accumulator gains (the fraction-free law, 2026-09-20; `count_owed`):
    the moment 5 at the age 5 gives 1 (the remainder 1), then 11 per
    self-creation gives 3, 2, 3, 3, 3 at the ages 6 through 10 (the
    accumulator 12, 11, 14, 13, 12 before the count; exact over the
    history: 5 + 5 x 11 = 60 = 15 x 4 owed in all): its age after the
    intervals 1 to 24 is 1, 2, 3, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9,
    9, 9, 10, 10, 10, 10, 11, 11 (until the fraction-free law the whole
    part off the clock at the current moment, `by_clock(age, 11, 4)` = 3,
    3, 2, 3, 3, put the 2 one self-creation later: 1, 2, 3, 4, 5, 6, 6, 7,
    7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 10, 11, 11); since
    clock-age-v1 (2026-09-21) a reader without the key counts the age
    moment too, with the same ages, its `read` record carrying the flow;
    a reader whose entry reads `presence` (until clock-age-v1 every reader
    without the key) counts the presence 2 and owes 0 at the presence 1 (the
    accumulator 1), 0 (3), 1 (5 -> 1), then 0, 1 alternately: 1, 2, 3, 4,
    5, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18,
    18 (the same ages as `by_clock(age, 2, 4)` off the clock); the `read`
    records of the age reader carry the reading 5 (the arrival's age
    moment);
(d) the parsing: `flight_bound` of an open 11^3 GameBoard over the six
    headings is 54 (D = 31 Links, ceil(31 x 110 / 64)) and 111 with the
    direction (1, 0, 64) declared (T 7095, one period, ceil(7095 / 64));
    `age_bound` defaults to twice it (108, 222) and parses as declared
    (100); 0, -1, a string and a fraction are refused naming `age_bound`;
    a GameBoard periodic on every axis without it is refused naming
    `age_bound`, and accepted with it; a declared ray's age beyond it is
    refused; the runner's record carries it; a ray on the z stub of an
    open 3 x 1 x 1 bar with z periodic (default 12) is refused with
    `OverflowError` naming `age_bound` at its 13th interval, not before;
(e) the GameBoard is unchanged by the whole age: 324 fixed rays on the
    periodic 8 x 8 x 4 GameBoard (head-on pairs among them) run 40 intervals with the
    ages whole, and again with every moving ray's age reduced modulo its
    direction's period after each interval from outside the law: the
    Nodes, directions, phases, amounts and contents are identical at every
    interval while the ages differ, and collisions moved rays on the way.
"""

from __future__ import annotations

import itertools
import json

import numpy as np
import pytest

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import count_owed
from event_universe.events.measured import count_component
from event_universe.events.nature_beam import Q, read_arrivals
from event_universe.events.world import READS, flight_bound
from event_universe.runner import run_initialization

PLUS_X, MINUS_X = [1, 0, 0], [-1, 0, 0]
HEADINGS = tuple((0, 0, 0) if k < 2 else PORT_HEADINGS[k - 2] for k in range(8))
DIRECTIONS = [*[list(h) for h in PORT_HEADINGS], 0, 1, [1, 1, 0], [2, -1, 1]]


def crowd() -> list[dict[str, object]]:
    """324 fixed rays on the periodic 8 x 8 x 4 GameBoard: every heading, both
    rest slots, two fan directions, amounts 1 and 2, ages up to 22, and
    twelve head-on pairs that meet at the Node between them."""
    beams: list[dict[str, object]] = [
        {
            "position": [(k * 5) % 8, (k * 3) % 8, (k * 11) % 4],
            "family": "light",
            "number": 1,
            "direction": DIRECTIONS[(k * 7) % len(DIRECTIONS)],
            "amount": 1 + (k % 5 == 0),
            "phase": (k * 13) % 64,
            "age": (k * 17) % 23,
        }
        for k in range(300)
    ]
    for k in range(12):
        beams.append({**light([1, k % 8, k % 4], PLUS_X, phase=k), "age": 0})
        beams.append({**light([3, k % 8, k % 4], MINUS_X, phase=32 + k), "age": 0})
    return beams


def torus() -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "ray-age-test",
        "shape": [8, 8, 4],
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "ticks": 40,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "age_bound": 128,
        "directions": [[1, 1, 0], [2, -1, 1]],
        "families": [{"name": "light", "quantum": 1, "phase_per_link": 5}],
        "measured": [],
        "in_transit": crowd(),
    }


def bar(shape: list[int], **keys: object) -> dict[str, object]:
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "ray-age-test",
        "shape": shape,
        "boundary": "open",
        "ticks": 4,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}],
        "measured": [],
    }
    world.update(keys)
    return world


def light(position: list[int], direction: list[int], age: int = 0, phase: int = 0) -> dict[str, object]:
    return {
        "position": position,
        "family": "light",
        "number": 1,
        "direction": direction,
        "amount": 1,
        "phase": phase,
        "age": age,
    }


def rows_of(simulation: NatureBeamSimulation, family: int) -> list[tuple[int, int, int]]:
    store = simulation.stores[family]
    return sorted(
        (int(store.node[i]), int(store.direction[i]), int(store.age[i])) for i in range(store.size)
    )


def test_the_age_is_kept_whole_and_a_collision_keeps_it():
    """(a)."""
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([301, 1, 1], in_transit=[light([0, 0, 0], PLUS_X)]))
    )
    for _ in range(200):
        simulation.step()
    store = simulation.stores[1]
    assert store.size == 1 and int(store.age[0]) == 200
    assert int(store.node[0]) == store.flat((116, 0, 0))
    # A head-on pair: the collision parks the pair and keeps the ages.
    pair = [light([3, 0, 0], PLUS_X, age=59), light([5, 0, 0], MINUS_X, age=59, phase=9)]
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([9, 1, 1], in_transit=pair, age_bound=128)), records.append
    )
    store = simulation.stores[1]
    node = store.flat((4, 0, 0))
    simulation.step()
    assert rows_of(simulation, 1) == [(node, 0, 60), (node, 1, 60)]
    simulation.step()
    assert rows_of(simulation, 1) == [(node, 6, 60), (node, 7, 60)]
    simulation.step()
    assert rows_of(simulation, 1) == [(node, 4, 61), (node, 5, 61)] and records == []
    simulation.step()
    assert store.size == 0 and sorted(r["detector"] for r in records) == ["face:+y", "face:-y"]
    assert simulation.books()["balanced"]
    # A re-emission is a birth: age 0, the arriving phase, the re-emitter's
    # number (2; the ray's number 1 is the lamp's, so it is not home).
    lamp = {"position": [0, 0, 0], "family": "light", "amount": 1, "fixed": True}
    mirror = {
        "position": [4, 0, 0],
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "rerelease"},
        "directions": [PLUS_X],
    }
    old = light([3, 0, 0], PLUS_X, age=59, phase=20)
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([9, 1, 1], measured=[lamp, mirror], in_transit=[old], age_bound=128))
    )
    store = simulation.stores[1]
    simulation.step()
    assert rows_of(simulation, 1) == [(store.flat((4, 0, 0)), 2, 0)]
    assert int(store.phase[0]) == 20 and int(store.number[0]) == 2
    # A release is born at age 0.
    source = {"position": [4, 0, 0], "family": "m", "amount": 1, "fixed": True}
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([9, 1, 1], measured=[source], release=[1, 1]))
    )
    simulation.step()
    store = simulation.stores[0]
    assert store.size == 6 and (store.age == 0).all()


def cube_group() -> list[np.ndarray]:
    matrices = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            matrix = np.zeros((3, 3), dtype=np.int64)
            for axis in range(3):
                matrix[perm[axis], axis] = signs[axis]
            matrices.append(matrix)
    return matrices


def test_the_age_moment_is_the_amount_weighted_age_and_the_symmetries_fix_it():
    """(b)."""
    vectors = np.array([[1, 0, 0], [2, -1, 0], [1, 1, 1]], dtype=np.int64)
    amounts = np.array([1, 2, 4], dtype=np.int64)
    ages = np.array([3, 5, 7], dtype=np.int64)
    reading = read_arrivals(vectors, amounts, ages=ages)
    assert int(reading.age) == 41 and int(reading.presence) == 7
    assert int(reading.age_outside) == 41 and int(reading.age_here) == 0
    assert int(reading.component("age")) == 41
    with_here = read_arrivals(
        np.concatenate([vectors, np.zeros((1, 3), dtype=np.int64)]),
        np.append(amounts, 2),
        ages=np.append(ages, 10),
    )
    assert int(with_here.age_here) == 20 and int(with_here.age_outside) == 41
    assert int(with_here.age) == 61 and int(with_here.here) == 2
    for matrix in cube_group():
        rotated = read_arrivals(vectors @ matrix.T, amounts, ages=ages)
        assert int(rotated.age) == 41 and rotated.flow.tolist() == (matrix @ reading.flow).tolist()
    keyed = read_arrivals(
        np.concatenate([vectors, vectors]),
        np.concatenate([amounts, amounts * 2]),
        np.array([1, 1, 1, 0, 0, 0]),
        2,
        ages=np.concatenate([ages, ages]),
    )
    assert keyed.age.tolist() == [82, 41] and keyed.presence.tolist() == [14, 7]
    assert int(read_arrivals(vectors, amounts).age) == 0
    with pytest.raises(OverflowError, match="moments of a reading"):
        read_arrivals(np.array([[1, 0, 0]]), np.array([1 << 40]), ages=np.array([1 << 23]))
    read_arrivals(np.array([[1, 0, 0]]), np.array([1 << 40]), ages=np.array([(1 << 22) - 1]))
    # clock-age-v1 (2026-09-21): the age moment on every entry but the one
    # that reads `presence`, the clock's word for the count before the word.
    assert count_component("age") == "age" and count_component("presence") == "scalar"
    assert [count_component(key) for key in READS if key not in ("age", "presence")] == ["age"] * 5


def clock_world(reader_table: dict[str, object]) -> dict[str, object]:
    source = {"position": [0, 0, 0], "family": "m", "amount": 1, "fixed": True}
    reader = {
        "position": [3, 0, 0],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": reader_table,
    }
    return bar([5, 1, 1], measured=[source, reader], release=[1, 1], suspension=[1, 4], ticks=24)


def ages_of_the_reader(
    world: dict[str, object],
) -> tuple[list[int], list[tuple[int, int, int]], list[object]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), records.append)
    reader = simulation.measured[2]
    ages, readings = [], []
    for tick in range(1, 25):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert reader.age + reader.waited == tick
        ages.append(reader.age)
        if reader.creating:
            readings.append((tick, reader.presence, reader.counted))
    read = [r["reading"] for r in records if r["event"] == "read" and r["measured"] == 2]
    return ages, readings, read


def test_the_clock_counts_the_age_moment_on_an_entry_that_reads_age():
    """(c)."""
    # The owed counts by the accumulator over the moments 5, 11, 11, ...
    owed, accumulator = [], 0
    for moment in (0, 0, 0, 0, 0, 5, 11, 11, 11, 11, 11):
        count, accumulator = count_owed(accumulator, moment, (1, 4))
        owed.append(count)
    assert owed == [0, 0, 0, 0, 0, 1, 3, 2, 3, 3, 3] and accumulator == 0
    # The whole part off the clock at the current moment, the form until
    # the fraction-free law: 3, 3, 2, 3, 3 (history).
    assert by_clock(5, 5, 4) == 1 and [by_clock(age, 11, 4) for age in range(6, 11)] == [3, 3, 2, 3, 3]
    ages, readings, read = ages_of_the_reader(clock_world({"m": {"reads": "age"}}))
    expected = [1, 2, 3, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11]
    assert ages == expected
    assert readings[5] == (6, 1, 5) and readings[6] == (8, 2, 11)
    assert all((presence, counted) == (2, 11) for tick, presence, counted in readings if tick >= 7)
    assert read == [5] * 19
    # clock-age-v1 (the model owner's word of 2026-09-21, record 394): a
    # reader without the key counts the age moment too (the same ages as
    # the `age` reader) while its `read` record still carries the flow; the
    # presence is the clock's count only on an entry that reads `presence`.
    ages, readings, read = ages_of_the_reader(clock_world({"m": "read"}))
    assert ages == expected
    assert all((presence, counted) == (2, 11) for tick, presence, counted in readings if tick >= 7)
    assert read == [[Q, 0, 0]] * len(read)
    ages, readings, read = ages_of_the_reader(clock_world({"m": {"rule": "read", "reads": "presence"}}))
    assert ages == [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 18]
    assert all(presence == counted for _, presence, counted in readings)
    # the presence reader's record carries the presence, the zeroth moment
    assert read == [1] * len(read)


def test_the_age_bound_is_derived_declared_or_required(tmp_path):
    """(d)."""
    headings = HEADINGS
    assert flight_bound((11, 11, 11), headings) == 54
    assert flight_bound((11, 11, 11), (*headings, (1, 0, 64))) == 111
    cube = bar([11, 11, 11])
    assert parse_nature_beam_world(cube).age_bound == 108
    assert parse_nature_beam_world({**cube, "directions": [[1, 0, 64]]}).age_bound == 222
    assert parse_nature_beam_world({**cube, "age_bound": 100}).age_bound == 100
    for bad in (0, -1, "8", 1.5):
        with pytest.raises(ValueError, match="age_bound"):
            parse_nature_beam_world({**cube, "age_bound": bad})
    everywhere = {"x": "periodic", "y": "periodic", "z": "periodic"}
    with pytest.raises(ValueError, match="age_bound is required on a GameBoard periodic on every axis"):
        parse_nature_beam_world({**cube, "boundary": everywhere})
    assert parse_nature_beam_world({**cube, "boundary": everywhere, "age_bound": 7}).age_bound == 7
    with pytest.raises(ValueError, match=r"in_transit\[0\].age must be an integer from 0 through 108"):
        parse_nature_beam_world({**cube, "in_transit": [light([5, 5, 5], PLUS_X, age=109)]})
    parse_nature_beam_world({**cube, "in_transit": [light([5, 5, 5], PLUS_X, age=108)]})
    world_file = tmp_path / "world.json"
    world_file.write_text(json.dumps({**cube, "ticks": 2}), encoding="utf-8")
    run_initialization(world_file, tmp_path / "run")
    record = json.loads((tmp_path / "run" / "run.json").read_text(encoding="utf-8"))
    assert record["age_bound"] == 108 and record["status"] == "completed"
    # The stub: a ray on +z of a z-periodic bar never leaves; at the bound
    # the run is refused, nothing on the GameBoard changed.
    stub = bar([3, 1, 1], boundary={"z": "periodic"}, in_transit=[light([1, 0, 0], [0, 0, 1])])
    world = parse_nature_beam_world(stub)
    assert world.age_bound == 12
    simulation = NatureBeamSimulation(world)
    for _ in range(12):
        simulation.step()
    assert int(simulation.stores[1].age[0]) == 12
    with pytest.raises(OverflowError, match="age_bound 12"):
        simulation.step()


def game_board(simulation: NatureBeamSimulation) -> np.ndarray:
    store = simulation.stores[0]
    rows = np.stack([store.node, store.direction, store.phase, store.amount, store.content], axis=1)
    return rows[np.lexsort(rows.T[::-1])]


def test_the_game_board_is_unchanged_by_the_whole_age():
    """(e)."""
    whole = NatureBeamSimulation(parse_nature_beam_world(torus()))
    reduced = NatureBeamSimulation(parse_nature_beam_world(torus()))
    period = reduced.tables.flight.period
    collided = False
    ages_differed = False
    for _ in range(40):
        before = whole.stores[0].direction.copy()
        whole.step()
        reduced.step()
        store = reduced.stores[0]
        moving = store.direction >= 2
        store.age = np.where(moving, store.age % period[store.direction], store.age)
        store.merge()
        assert np.array_equal(game_board(whole), game_board(reduced))
        collided = collided or before.shape != whole.stores[0].direction.shape
        collided = collided or (before != whole.stores[0].direction).any()
        ages_differed = ages_differed or int(whole.stores[0].age.sum()) != int(store.age.sum())
    assert collided and ages_differed
