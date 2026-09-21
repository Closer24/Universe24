"""The Hubble-stars readings tool (series G2, `tools/hubble_stars_readings.py`)
reads the engine's own functions (the experimenter skill: a readings tool
reads the engine, never replays a rule of it), and the worlds of
`examples/events/hubble_stars/` are the ones their generator writes. The
expected values of docs/TEST_EXPECTATIONS.md ("The tools read the engine"),
written down first:

(a) the shipped worlds equal `make_worlds.worlds()` document for document,
    and `expectations.json` declares the generator's format (a world
    declares `law`, never `format`);
(b) `read_run` on a run of a bar of 61 x 1 x 1 (y and z periodic) written
    by the runner, 60 intervals, N 64, `release` [1, 2^16], `width` 2^20,
    no suspension: a fixed measured event of the paid family `detector` at
    x = 20 declared as the detector `centre` reading `wave` with the entry
    `{"rule": "measure", "reads": "age"}` for the star family `s_px1`; a
    star `s_px1` at x = 25, a lamp of the paid family (`amount` 4096, `rate`
    [1, 1] on (-1, 0, 0)) holding `mass` 2^22 (the free family, `charge` 0,
    no phase circle), K = the content 2^22 + 4096 (the turn 1 per
    self-creation), with the momentum [Q S M, 0, 0] (the speed p / (Q S M +
    p) = 1 / 2 Link per self-creation: a step at every second
    self-creation), releasing its mass rows on the two headings of x. The
    reading: the crowd `gravity` and the clock `scalar` off the model name,
    rho = 1, c = 32 / 55, the star's declared speed 1 / 2, its initial
    distance 5 and its content 2^22 + 4096, its `record` lines the engine's
    detector set's (one per interval with a click, the phase the pointer's
    step), its clicks' age moments the engine's (amount 1, the reading the
    age), its steps the engine's `step` records (30 in 60 intervals), its
    homes the engine's `home` records (its outward rows taken home when it
    stepped in the release interval), completed and balanced; the window
    [20, 60): the pointer's turn reads 1 + z = 1 + v / c with v = 1 / 2
    within the grain of the digital step (0.05 in z), k = 0 (no
    suspension), the reading's formula within 2 % and the luminosity
    (clicks per interval) 1 / (1 + z) within 5 %;
(c) the fits on the exact coasting throw from one point (`exact_points`)
    read q = 0 and H (t_0 + T_0) = 1 to 1e-6 with the power-law family
    free in H and q, q = 0 the nearest of the three forms with rms 0, and
    on the exact Einstein-de Sitter form (q = +0.5) read q = +0.5 to 1e-3:
    a property of the fits, no world's numbers.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import HEADING_OFFSET, Q
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "hubble_stars"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


TOOL = load("hubble_stars_readings_tool", ROOT / "tools" / "hubble_stars_readings.py")

TICKS = 60
WIDTH = 1 << 20
MASS = 1 << 22
LIGHT = 1 << 12
CONTENT = MASS + LIGHT
MOMENTUM = Q * WIDTH * CONTENT  # v = p / (Q S M + p) = 1 / 2


def bar_world() -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "rays-hubble-stars-gravity-scalar-space-v1",
        "shape": [61, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": TICKS,
        "K": CONTENT,
        "N": 64,
        "release": [1, 1 << 16],
        "suspension": 0,
        "width": WIDTH,
        "families": [
            {"name": "detector", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "s_px1", "quantum": 1},
        ],
        "measured": [
            {
                "position": [20, 0, 0],
                "family": "detector",
                "amount": 1,
                "fixed": True,
                "table": {"s_px1": {"rule": "measure", "reads": "age"}},
            },
            {
                "position": [25, 0, 0],
                "family": "s_px1",
                "amount": LIGHT,
                "phase": 0,
                "momentum": [MOMENTUM, 0, 0],
                "held": {"mass": MASS},
                "directions": [[1, 0, 0], [-1, 0, 0]],
                "lamp": {"rate": [1, 1], "directions": [[-1, 0, 0]]},
            },
        ],
        "detectors": [{"name": "centre", "positions": [[20, 0, 0]], "threshold": 1, "reading": "wave"}],
    }


def expand(name: str) -> dict:
    """A shipped world as the loader expands it (its families from the
    definitions it references, `examples/events/entities/families.json`)."""
    path = WORLDS / f"{name}.json"
    return json.loads(
        load_world(path.read_bytes(), base_dir=path.parent, root=WORLDS.parent).expanded_source
    )


def test_the_shipped_worlds_are_the_generators_and_the_expectations_declare_a_format():
    """(a)."""
    generator = load("hubble_stars_make_worlds", WORLDS / "make_worlds.py")
    generated = generator.worlds()
    assert set(generated) == {
        f"{crowd}_{clock}"
        for crowd in ("coasting", "gravity", "double")
        for clock in ("none", "scalar", "age")
    }
    for name, document in generated.items():
        assert json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8")) == document, name
        # The stars are one instance of the definition `hubble_stars`
        # (record 113); the loader expands the world to its inline form.
        assert [e["definition"] for e in document["entities"]] == [
            "detector_material",
            "mass",
            "hubble_stars",
        ]
        expanded = expand(name)
        assert [f["name"] for f in expanded["families"]][:2] == ["detector", "mass"]
        assert len(expanded["families"]) == 26
        parse_nature_beam_world(expanded)
    expectations = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expectations["format"] == generator.EXPECTATIONS_FORMAT
    assert expectations["throw_age"] == generator.THROW_AGE
    assert {s["name"] for s in expectations["stars"]} == {
        m["family"] for m in generated["gravity_scalar"]["measured"] if "momentum" in m
    }
    assert set(expectations["crowds"]) == set(generator.CROWDS)
    assert expectations["reading_rule"] == "acoustic"
    # The record-click worlds (reading `sum` at the centre; the key
    # `amplitude` deleted by the one click of stage (vii), MIGRATION
    # (vii-4): every lamp births records) and the expectations pinned for
    # the second run under the step drive (the reading rule `source`, the
    # burst of the step rule at most 1).
    for name, document in generator.record_worlds().items():
        assert json.loads((WORLDS / "record" / f"{name}.json").read_text(encoding="utf-8")) == document
        assert "amplitude" not in document and document["detectors"][0]["reading"] == "sum"
        # Inline (a reference climbs one level only; the worlds of the
        # record click are deferred, record 113).
        assert "entity_definitions" not in document
        parse_nature_beam_world(document)
    pinned = json.loads((WORLDS / "record" / "expectations.json").read_text(encoding="utf-8"))
    assert pinned["format"] == generator.EXPECTATIONS_FORMAT and pinned["reading_rule"] == "source"
    assert pinned["step_burst_max"] == 1
    assert pinned["crowds"]["coasting"]["q_bracket"] == expectations["crowds"]["coasting"]["q_bracket"]
    gravity = pinned["crowds"]["gravity"]
    # The registered fit against the register's own bracket (since
    # 2026-09-21 no literal of a world's number here).
    assert (
        gravity["q_bracket"][0] <= gravity["derived_fits"]["300-400"]["q_fit"] <= gravity["q_bracket"][1]
    )
    assert (
        gravity["q_bracket"][0] > expectations["crowds"]["gravity"]["derived_fits"]["300-400"]["q_fit"]
    )
    # The worlds under the key `doppler` as well (doppler-v1, on main since
    # PR #379) and the expectations pinned for the third run (the reading
    # rule `flux`: the acoustic rule with the reader's speed at the grain
    # G = 2^12, docs/designs/hubble_stars/EXPECTATION_2.md): the record
    # worlds with the key added and nothing else changed.
    for name, document in generator.doppler_worlds().items():
        assert json.loads((WORLDS / "doppler" / f"{name}.json").read_text(encoding="utf-8")) == document
        assert "amplitude" not in document and document["doppler"] is True
        without = {k: v for k, v in document.items() if k not in ("doppler", "model_id")}
        record = generator.record_worlds()[name]
        assert without == {k: v for k, v in record.items() if k != "model_id"}
        parse_nature_beam_world(document)
    flux = json.loads((WORLDS / "doppler" / "expectations.json").read_text(encoding="utf-8"))
    assert flux["format"] == generator.EXPECTATIONS_FORMAT and flux["reading_rule"] == "flux"
    assert flux["step_burst_max"] == 1
    acoustic_q = expectations["crowds"]["gravity"]["derived_fits"]["300-400"]["q_fit"]
    flux_gravity = flux["crowds"]["gravity"]
    flux_q = flux_gravity["derived_fits"]["300-400"]["q_fit"]
    assert abs(flux_q - acoustic_q) < 0.002
    assert flux_gravity["q_bracket"][0] <= flux_q <= flux_gravity["q_bracket"][1]
    assert generator.quantised(26 / 90) == 1183 / 4096 and generator.quantised(-26 / 90) == -1183 / 4096
    # The tool names a run under the key by its folder.
    assert TOOL.Run.prefix.fget(SimpleNamespace(under_doppler=True, under_record=True)) == "doppler/"
    assert TOOL.Run.prefix.fget(SimpleNamespace(under_doppler=False, under_record=True)) == "record/"
    assert TOOL.Run.prefix.fget(SimpleNamespace(under_doppler=False, under_record=False)) == ""


def test_read_run_reads_the_record_and_the_engines_world(tmp_path):
    """(b)."""
    document = bar_world()
    world = parse_nature_beam_world(document)
    folder = tmp_path / "gravity_scalar"
    folder.mkdir()
    execute_nature_beam_run(world, json.dumps(document).encode("utf-8"), folder, "test", TICKS)
    run = TOOL.read_run(folder)
    assert (run.crowd, run.clock, run.rho, run.modulus) == ("gravity", "scalar", 1.0, 64)
    assert run.c == 32 / 55 == TOOL.beam_speed()
    assert run.completed and run.balanced and run.ticks == TICKS
    assert list(run.stars) == ["s_px1"]
    star = run.stars["s_px1"]
    assert (star.number, star.content, star.momentum) == (2, CONTENT, MOMENTUM)
    assert star.declared_speed == 0.5 and star.initial_distance == 5
    assert by_clock(0, MOMENTUM, Q * WIDTH * CONTENT + MOMENTUM) == 0
    assert by_clock(1, MOMENTUM, Q * WIDTH * CONTENT + MOMENTUM) == 1
    simulation = NatureBeamSimulation(world)
    steps: list[int] = []
    turns: list[tuple[int, int]] = []
    detector_set = simulation.detector_sets[0]
    family = 2
    for tick in range(1, TICKS + 1):
        before = simulation.measured[2].position
        record_before = detector_set.record[family]
        simulation.step()
        assert simulation.books()["balanced"]
        if simulation.measured[2].position != before:
            steps.append(tick)
        if detector_set.record[family] != record_before:
            assert detector_set.phase[family] is not None
            turns.append((tick, detector_set.phase[family]))
    assert star.steps == steps and len(steps) == 30
    assert star.turns == turns and len(turns) > 20
    ages = {}
    for tick, rows in star.clicks.items():
        assert len(rows) == 1 and rows[0][0] == 1
        ages[tick] = rows[0][1]
    # The first light row leaves x = 25 (r = 5) at tick 1 and arrives at
    # tick 1 + 8 = 9 with the age 8 (the least age with m(age) >= 5).
    assert ages[9] == 8 and min(ages) == 9
    # The star's own outward rows come home when it steps in the interval
    # of their release: the engine's `home` records, counted.
    assert star.homes > 0 and star.homes * (MASS >> 16) == simulation.measured[2].taken[1]["home"]
    assert star.final_momentum == max(abs(v) for v in simulation.measured[2].momentum)
    assert [r.name for r in TOOL.find_runs(tmp_path)] == ["gravity_scalar"]
    point = TOOL.window_point(run, star, (20, TICKS))
    assert point is not None and point.k == 0.0
    # Re-run under the one click (stage (vii) step 4); the verdict to be
    # re-read: the star's rows are records born at u with the path phase,
    # so the `wave` set's phase never turns and the acoustic rule's z (the
    # slope of the record's phase) is undefined; the record form's reading
    # of series G2 is the `source` rule of the record worlds' expectations
    # (until that step z within 0.05 of 0.5 / c, the formula and the
    # luminosity within their tolerances).
    assert math.isnan(point.z)
    assert point.declared == 0.5 / run.c


def test_the_fits_read_the_exact_forms():
    """(c)."""
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    assert int(table.period[HEADING_OFFSET]) == 55
    assert int(table.manhattan_steps(heading, np.array([55]))[0]) == 32
    assert TOOL.links([17.0, 34.0]).tolist() == [10, 20]
    c = 32 / 55
    t0, throw_age = 350.0, 90.0
    design = [(f"s{i}", (3 + i) / throw_age, 3 + i) for i in range(24)]
    exact = TOOL.exact_points(design, t0, c, throw_age)
    fit = TOOL.fit_points(exact, t0)
    assert abs(fit.q_fit) < 1e-3
    assert abs(fit.h_fit * (t0 + throw_age) - 1.0) < 1e-6
    assert fit.nearest == "q = 0" and fit.best["q = 0"][1] < 1e-9
    for p in exact:
        assert abs(p.z - p.tau / (t0 + throw_age - p.tau)) < 1e-12
    h = 1.0 / (t0 + throw_age)
    decelerating = [
        TOOL.Point(p.name, 0, TOOL.einstein_de_sitter(h * p.tau), 0.0, 0.0, p.tau, p.d, 1.0, 0.0)
        for p in exact
    ]
    fit_eds = TOOL.fit_points(decelerating, t0)
    assert abs(fit_eds.q_fit - 0.5) < 1e-3
    assert fit_eds.nearest == "q = +0.5"
