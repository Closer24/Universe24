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
import pytest

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
        "per_axis_drive": True,  # the per-axis drive of history (2026-09-22): the integers as registered
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
                "lamp": {"wheel": [1, 64], "rate": [1, 1], "directions": [[-1, 0, 0]]},
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
    # The registered speed derived and compared (DERIVATIONS_BEAM 2.1, the
    # register's `derivations`): c = Q / T_D Links per interval on a heading,
    # T_D the heading's resolution of the flight rule (isqrt(3 Q^2) = 110),
    # the wall of the position's accumulator over its rate.
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    assert expectations["c"] == Q / int(table.resolution[HEADING_OFFSET])
    assert set(expectations["derivations"]) == set(expectations) - {
        "format",
        "derivations",
        "replicated",
    }
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
    # The nine worlds under the key `doppler` and their flux expectations
    # (the third run) left with the key on 2026-09-21 (the crossing rule,
    # MIGRATION): the generator writes no `doppler/` folder and a world
    # that declares the key is refused as an unknown key.
    assert not (WORLDS / "doppler").exists() and not hasattr(generator, "doppler_worlds")
    with pytest.raises(ValueError, match="unknown keys: doppler"):
        parse_nature_beam_world({**generator.record_worlds()["gravity_none"], "doppler": True})
    # The tool names a run by its folder.
    assert TOOL.Run.prefix.fget(SimpleNamespace(under_record=True)) == "record/"
    assert TOOL.Run.prefix.fget(SimpleNamespace(under_record=False)) == ""


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
    # The detector's own clock (2026-09-22): a fixed detector at
    # `suspension` 0 owes nothing, its rate 1 off its own state (DETECTOR).
    rate, kind = run.own_clock()
    assert rate == 1.0 and kind.startswith(TOOL.KIND_DETECTOR)


def test_the_detector_clock_restates_a_fit_by_one_closed_form():
    """(d) The detector's own clock (the model owner, 2026-09-22, records
    678 and 707): at the rate r every point reads 1 + z_d = r (1 + z) and
    its luminosity L_d = L / r, so L_d (1 + z_d) = L (1 + z) (the pin
    1 / (1 + z) clock-free) and the reading's formula keeps its ratio;
    the free fit's q is unchanged and its H_d = r H, every best-H rms r
    times the lattice's with the same nearest and farthest forms; at r =
    1 nothing moves. A property of the restatement, no world's numbers."""
    c = 32 / 55
    t0, throw_age = 350.0, 90.0
    design = [(f"s{i}", (3 + i) / throw_age, 3 + i) for i in range(24)]
    fit = TOOL.fit_points(TOOL.exact_points(design, t0, c, throw_age), t0)
    rate = 0.8
    restated = TOOL.in_detector_clock(fit, rate, TOOL.KIND_DETECTOR)
    assert restated.clock_rate == rate and restated.clock_kind == TOOL.KIND_DETECTOR
    for before, after in zip(fit.points, restated.points, strict=True):
        assert abs(after.z - (rate * (1.0 + before.z) - 1.0)) < 1e-12
        assert after.z_lattice == before.z and after.tau == before.tau
        assert abs(after.rate * (1.0 + after.z) - before.rate * (1.0 + before.z)) < 1e-12
        ratio_before = (1.0 + before.z) / (1.0 + before.predicted)
        ratio_after = (1.0 + after.z) / (1.0 + after.predicted)
        assert abs(ratio_after - ratio_before) < 1e-12
    assert restated.q_fit == fit.q_fit
    assert abs(restated.h_fit - rate * fit.h_fit) < 1e-15
    assert abs(restated.rms_fit - rate * fit.rms_fit) < 1e-12
    assert abs(restated.hubble_near - rate * fit.hubble_near) < 1e-15
    assert restated.nearest == fit.nearest == "q = 0" and restated.farthest == fit.farthest
    for label in fit.best:
        assert restated.best[label][0] == fit.best[label][0]
        assert abs(restated.best[label][1] - rate * fit.best[label][1]) < 1e-12
    unchanged = TOOL.in_detector_clock(fit, 1.0, TOOL.KIND_DETECTOR)
    assert unchanged.h_fit == fit.h_fit
    assert all(abs(a.z - b.z) < 1e-12 for a, b in zip(unchanged.points, fit.points, strict=True))


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


def test_the_generators_pins_under_the_two_drives():
    """(f) The generator's momenta and pins under the two drives (2026-09-22,
    docs/designs/drive_b/DEFAULT.md section (c)): the shipped
    `expectations.json` and `record/expectations.json` are the line drive's
    (`drive` "line", `centred` false, a derivation entry for each), the
    stars' momenta the line rule's p = Q S M v / (1 - v T_D / Q) at the
    declared speeds (s_px1 at v = 1 / 30 with M = 2^22 + 2^12:
    9962425798633, its speed 1 / 30 within the rounding), and the per-axis
    drive of history gives the registered integers (s_px1 9715512228193 by
    p = Q S M v / (1 - v)); the pushing crowds' derived q under the line
    drive within the shipped brackets and above the coasting crowd's."""
    generator = load("hubble_stars_make_worlds", WORLDS / "make_worlds.py")
    expectations = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    pinned = json.loads((WORLDS / "record" / "expectations.json").read_text(encoding="utf-8"))
    for register in (expectations, pinned):
        assert register["drive"] == generator.LINE_DRIVE and register["centred"] is False
        assert "drive" in register["derivations"] and "centred" in register["derivations"]
    content = generator.MASS + generator.LIGHT
    first = expectations["stars"][0]
    assert first["name"] == "s_px1" and first["momentum"] == 9962425798633
    assert first["momentum"] == round(64 * (1 << 20) * content * (1 / 30) / (1 - 110 / 64 / 30))
    assert abs(first["speed"] - 1 / 30) < 1e-9
    assert (
        abs(
            generator.speed(first["momentum"], content)
            - first["momentum"] * 64 / (64 * 64 * (1 << 20) * content + first["momentum"] * 110)
        )
        < 1e-15
    )
    history = generator.stars(generator.MASS, generator.AXIS_DRIVE)
    assert (
        history[0]["momentum"]
        == 9715512228193
        == round(64 * (1 << 20) * content * (1 / 30) / (1 - 1 / 30))
    )
    assert abs(history[0]["speed"] - 1 / 30) < 1e-9
    assert generator.push_factor(0.0) == 1.0 and generator.push_factor(0.1) == (1 - 0.1 * 110 / 64) ** 2
    assert generator.push_factor(0.1, generator.AXIS_DRIVE) == 0.9**2
    for crowd in ("gravity", "double"):
        entry = expectations["crowds"][crowd]
        q = entry["derived_fits"]["300-400"]["q_fit"]
        assert entry["q_bracket"][0] <= q <= entry["q_bracket"][1]
        assert q > expectations["crowds"]["coasting"]["derived_fits"]["300-400"]["q_fit"] + 0.1
    assert generator.momentum(1 / 30, content) == 9962425798633
    assert generator.momentum(1 / 30, content, generator.AXIS_DRIVE) == 9715512228193
