"""The Hubble readings tool reads the engine's own functions (the
experimenter skill: a readings tool reads the engine, never replays a rule
of it). Each reading of `tools/hubble_readings.py` is checked against the
engine on a minimal GameBoard; the expected values of docs/TEST_EXPECTATIONS.md
("The tools read the engine"), written down first:

(a) the ray's speed and the distance off the flight table: on a heading
    the period is 55 intervals and m(55) = 32 Links, so c = 32 / 55 =
    0.58182 per interval; m(17) = 10 and m(34) = 20 Links (the least ages
    with 10 and 20 Links are 17 and 34: `test_nature_beam_flight`'s table);
(b) `read_run` on a run of a bar of 61 x 1 x 1 (y and z periodic) written
    by the runner, 60 intervals, K 64, N 64, `release` [1, 64], `width`
    2^20, no suspension: a fixed measured event of the paid family
    `detector` at x = 20 declared as the detector `centre` reading `wave`
    with the entry `{"rule": "measure", "reads": "age"}` for the source
    family `px1`; a free source `px1` of content 64 at x = 25 with the
    momentum [2^32, 0, 0] (since the directional drive of 2026-09-21,
    BEAM_LAW note 49, the speed |p| Q / (Q S M Q + |p| T_D) = 64 / 174 =
    0.3678 Links per self-creation on the heading, read off the engine's
    `drive_rate_and_wall` by the tool's `declared_speed`; until then p /
    (Q S M + p) = 1 / 2, `by_clock(age, p, 2^32 + p)`, a step at every
    second self-creation) releasing one row per self-creation on (-1, 0,
    0) with its clock's phase (the turn `by_clock(age, 64, 64)` = 1). The
    reading: the crowd `coasting` and the clock `scalar` off the model
    name, rho = 1, c = 32 / 55, the source's declared speed 64 / 174 and
    its initial distance 5, its `record` lines the engine's detector set's
    (one per interval with a click, the phase the pointer's step), its
    clicks' age moments the engine's (amount 1, the reading the age), its
    steps the engine's `step` records (22 in 60 intervals, floor(60 x 64 /
    174); 30 until 2026-09-21), completed and balanced; the window [20,
    60): the pointer's turn reads 1 + z = 1 + v / c with v = 64 / 174
    within the grain of the digital step (0.05 in z; v = 1 / 2 until
    2026-09-21), k = 0 (no suspension) and the reading's formula within
    2 %.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import HEADING_OFFSET, Q, drive_rate_and_wall

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "hubble_readings_tool", ROOT / "tools" / "hubble_readings.py"
)
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["hubble_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)

TICKS = 60
WIDTH = 1 << 20
CONTENT = 64
MOMENTUM = Q * WIDTH * CONTENT  # v = p Q / (Q S M Q + p T_D) = 64 / 174 (1 / 2 until 2026-09-21)


def bar_world() -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "rays-hubble-coasting-scalar-space-v1",
        "shape": [61, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": TICKS,
        "K": CONTENT,
        "N": 64,
        "release": [1, 64],
        "suspension": 0,
        "width": WIDTH,
        "families": [{"name": "detector", "quantum": 1}, {"name": "px1", "quantum": 0}],
        "measured": [
            {
                "position": [20, 0, 0],
                "family": "detector",
                "amount": 1,
                "fixed": True,
                "table": {"px1": {"rule": "measure", "reads": "age"}},
            },
            {
                "position": [25, 0, 0],
                "family": "px1",
                "amount": CONTENT,
                "phase": 0,
                "momentum": [MOMENTUM, 0, 0],
                "directions": [[-1, 0, 0]],
            },
        ],
        "detectors": [{"name": "centre", "positions": [[20, 0, 0]], "threshold": 1, "reading": "wave"}],
    }


def test_the_speed_and_the_distance_are_the_flight_tables():
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    assert int(table.period[HEADING_OFFSET]) == 55
    assert int(table.manhattan_steps(heading, np.array([55]))[0]) == 32
    assert TOOL.HEADINGS_FLIGHT.period[HEADING_OFFSET] == 55
    assert TOOL.links([17.0, 34.0]).tolist() == [10, 20]
    assert TOOL.links([16.0, 33.0]).tolist() == [9, 19]


def test_read_run_reads_the_record_and_the_engines_world(tmp_path):
    document = bar_world()
    world = parse_nature_beam_world(document)
    folder = tmp_path / "coasting_scalar"
    folder.mkdir()
    execute_nature_beam_run(world, json.dumps(document).encode("utf-8"), folder, "test", TICKS)
    run = TOOL.read_run(folder)
    assert (run.crowd, run.clock, run.rho, run.modulus) == ("coasting", "scalar", 1.0, 64)
    assert run.c == 32 / 55
    assert run.completed and run.balanced and run.ticks == TICKS
    assert list(run.sources) == ["px1"]
    source = run.sources["px1"]
    assert (source.number, source.content, source.momentum) == (2, CONTENT, MOMENTUM)
    assert source.declared_speed == 64 / 174 and source.initial_distance == 5
    rate, wall = drive_rate_and_wall([MOMENTUM, 0, 0], CONTENT, WIDTH, 1, 110)
    assert (rate, wall) == (MOMENTUM * 64, MOMENTUM * 174) and source.declared_speed == rate / wall
    assert [by_clock(age, rate, wall) for age in range(3)] == [0, 0, 1]
    simulation = NatureBeamSimulation(world)
    steps: list[int] = []
    turns: list[tuple[int, int]] = []
    ages: dict[int, int] = {}
    detector_set = simulation.detector_sets[0]
    for tick in range(1, TICKS + 1):
        before = simulation.measured[2].position
        record_before = detector_set.record[1]
        simulation.step()
        assert simulation.books()["balanced"]
        if simulation.measured[2].position != before:
            steps.append(tick)
        if detector_set.record[1] != record_before:
            assert detector_set.phase[1] is not None
            turns.append((tick, detector_set.phase[1]))
    assert source.steps == steps and len(steps) == 22 == TICKS * 64 // 174
    assert source.turns == turns and len(turns) > 20
    for tick, rows in source.clicks.items():
        assert len(rows) == 1 and rows[0][0] == 1
        ages[tick] = rows[0][1]
    # The age of a row at its click is its flight time: a row released at
    # the tick t from the distance r arrives at t + f(r), f the least age
    # with m(age) >= r; the first row leaves x = 25 (r = 5) at tick 1 and
    # arrives at tick 1 + 8 = 9 with the age 8.
    assert ages[9] == 8 and min(ages) == 9
    assert [r.name for r in TOOL.find_runs(tmp_path)] == ["coasting_scalar"]
    point = TOOL.window_point(run, source, (20, TICKS))
    assert point is not None and point.k == 0.0
    assert abs(point.z - (64 / 174) / run.c) < 0.05
    assert abs((1.0 + point.z) / (1.0 + point.predicted) - 1.0) <= TOOL.FORMULA_TOLERANCE
    assert point.declared == (64 / 174) / run.c
    assert point.initial_distance == 5.0


def test_from_one_point_collapses_a_coasting_throw_onto_the_milne_form():
    """The throw from one point (`--from-one-point`): exact coasting sources
    thrown from r_0 = 3, 5, 7, 9 at t_0 = 350 read z = v / c at tau = (r_0 +
    v t_0) / (c + v); with every tau reduced by (r_0 / c) / (1 + z) they lie
    on the Milne form z = H tau / (1 - H tau) with H = 1 / t_0 exactly (the
    best-H rms of q = 0 zero, its H t_0 one), while as thrown they do not;
    and the near fit through the origin on z <= 0.2 reads an exact coasting
    throw from one point as H t_0 > 1 (the Milne curvature read as a larger
    H), so the far part of that exact form lies below the coasting form at
    the near fit's H (the accelerating form's signature from a coasting
    throw). A property of the fits, no world's numbers."""
    c = 32 / 55
    t0 = 350.0
    points = []
    for rank, fraction in enumerate(
        (0.05, 0.15, 0.25, 0.35, 0.45, 0.6, 0.086, 0.257, 0.429, 0.6), start=1
    ):
        r0 = 1 + 2 * (1 + (rank - 1) % 4)
        v = fraction * c
        tau = (r0 + v * t0) / (c + v)
        points.append(
            TOOL.Point(
                f"s{rank}", 20, v / c, 0.0, v / c, tau, tau * c, None, None, None, None, v / c, tau, r0
            )
        )
    fit = TOOL.fit_points(points, t0)
    assert fit.best["q = 0"][1] > 0.003
    shifted = TOOL.from_one_point(fit, c)
    assert shifted.best["q = 0"][1] < 1e-9
    assert abs(shifted.best["q = 0"][0] * t0 - 1.0) < 1e-6
    for p in shifted.points:
        assert abs(p.z - p.tau / (t0 - p.tau)) < 1e-12
    bias = TOOL.near_fit_of_the_coasting_form(shifted)
    assert bias > 1.0
    assert shifted.rms_far["q = -0.55"] < shifted.rms_far["q = 0"] < shifted.rms_far["q = +0.5"]
