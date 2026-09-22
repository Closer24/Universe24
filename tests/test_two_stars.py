"""Series O, two stars moving toward each other, each the detector of the
other (`examples/events/two_stars/`, docs/designs/two_stars/DESIGN.md). The
expected values of docs/TEST_EXPECTATIONS.md ("Two stars, each the detector
of the other"), written down first:

(a) the shipped worlds equal `make_worlds.worlds()` document for document,
    parse under the law and run ten intervals with the books balanced; star
    A (`s_px1`, number 3) at x = 70 with the momentum +p and star B
    (`s_mx1`, number 4) at x = 130 with -p in `symmetric`, B at rest and A
    at the momentum of 0.4 c in `rest_frame`; the speed of the momentum
    by the drive's rule is 0.2 c within 1e-6 (0.4 c for the mover of
    `rest_frame`); since the law's line drive (2026-09-22, record 972) the
    momenta are the line rule's, 41021779276297 at 0.2 c and 109391411403460
    at 0.4 c (the per-axis drive of history's 37139059427100 and
    85543046832089 reproducible by `worlds(AXIS_DRIVE)`); `expectations.json`
    declares the generator's format, the drive, the two windows and the
    three worlds;
(b) the derivation's algebra, no world's numbers: under the law as built a
    reader moving at v_r toward a lamp moving at v_s toward it reads
    1 + z = (1 - v_s / c) / (1 + v_r / c); with v_s = v_r = 0.2 c that is
    2 / 3 exactly, equal to nature's sqrt((1 - beta) / (1 + beta)) at the
    relativistic sum beta = 0.4 / 1.04 (the identity of the symmetric
    frame); with v_s = 0 and v_r = 0.4 c it is 1 / 1.4 and with v_s = 0.4 c
    and v_r = 0 it is 0.6, against nature's 0.6547 for both (the rest
    frame tells the two readers apart);
(c) the expectation pins the first contact of `symmetric_pass` at tick 254
    (the stars 60 Links apart closing at 0.4 c = 0.2327 Links per interval
    to one Link: 59 / 0.2327 = 253.5) and earlier under gravity (`symmetric`
    240, `rest_frame` 238 under the line drive, whose push factor (1 - v
    T_D / Q)^2 is smaller than the per-axis (1 - v)^2; 237 and 236 under the
    per-axis drive of history), and every star's speed at the contact above
    its initial speed under gravity and equal to it without.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events import NatureBeamSimulation
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "two_stars"


def load_generator():
    path = WORLDS / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("two_stars_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["two_stars_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


def test_the_shipped_worlds_are_the_generators_and_run_balanced():
    """(a)."""
    generator = load_generator()
    generated = generator.worlds()
    assert set(generated) == {"symmetric", "rest_frame", "symmetric_pass"}
    for name, document in generated.items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        loaded = load_world(path.read_bytes(), base_dir=path.parent, root=WORLDS.parent)
        world = loaded.world
        stars = [entry for entry in world.measured if not entry.fixed]
        assert len(stars) == 2 and len(world.measured) == 4
        a, b = stars
        assert tuple(a.position) == (70, 1, 1) and tuple(b.position) == (130, 1, 1)
        v_a, v_b = generator.WORLDS[name][0], generator.WORLDS[name][1]
        for entry, v in ((a, v_a), (b, v_b)):
            p = entry.momentum[0]
            assert (p > 0) == (v > 0) and (p == 0) == (v == 0)
            assert abs(generator.speed(abs(p), generator.CONTENT) / generator.C - abs(v)) < 1e-6
        # The line rule's momenta, and the drive of history's reproducible.
        assert sorted(abs(entry.momentum[0]) for entry in stars) == sorted(
            abs(v) for v in generator.expectations()["momenta"][name].values()
        )
        simulation = NatureBeamSimulation(world)
        for tick in range(1, 11):
            simulation.step()
            assert simulation.books()["balanced"], (name, tick)
    assert generator.momentum(0.2 * generator.C, generator.CONTENT) == 41021779276297
    assert generator.momentum(0.4 * generator.C, generator.CONTENT) == 109391411403460
    assert (
        generator.momentum(0.2 * generator.C, generator.CONTENT, generator.AXIS_DRIVE) == 37139059427100
    )
    assert (
        generator.momentum(0.4 * generator.C, generator.CONTENT, generator.AXIS_DRIVE) == 85543046832089
    )
    history = generator.worlds(generator.AXIS_DRIVE)["symmetric"]["measured"][2]["momentum"]
    assert history == [37139059427100, 0, 0]
    expectations = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expectations["format"] == generator.EXPECTATIONS_FORMAT
    assert expectations["drive"] == generator.LINE_DRIVE
    assert expectations["windows"] == [[50, 150], [150, 250]]
    assert set(expectations["worlds"]) == set(generated)
    assert {k: v for k, v in expectations.items() if k != "runs"} == generator.expectations()


def test_the_readings_algebra_of_the_two_frames():
    """(b)."""
    generator = load_generator()
    c = generator.C
    symmetric = generator.one_plus_z(0.2 * c, 0.2 * c)
    assert abs(symmetric - 2 / 3) < 1e-12
    beta = generator.relativistic_sum(0.2, 0.2)
    assert abs(beta - 0.4 / 1.04) < 1e-12
    assert abs(generator.natures_one_plus_z(beta) - 2 / 3) < 1e-12
    assert abs(generator.one_plus_z(0.0, 0.4 * c) - 1 / 1.4) < 1e-12
    assert abs(generator.one_plus_z(0.4 * c, 0.0) - 0.6) < 1e-12
    assert abs(generator.natures_one_plus_z(0.4) - (0.6 / 1.4) ** 0.5) < 1e-12


def test_the_expectation_pins_the_contact_and_the_speeds():
    """(c)."""
    generator = load_generator()
    expected = generator.expectations()["worlds"]
    assert expected["symmetric_pass"]["contact_tick"] == 254
    assert expected["symmetric"]["contact_tick"] == 240
    assert expected["rest_frame"]["contact_tick"] == 238
    history = generator.expectations(generator.AXIS_DRIVE)["worlds"]
    assert history["symmetric_pass"]["contact_tick"] == 254
    assert history["symmetric"]["contact_tick"] == 237
    assert history["rest_frame"]["contact_tick"] == 236
    assert abs(history["symmetric"]["windows"]["50-150"]["A_reads_B"] - 0.6497) < 5e-5
    assert abs(expected["symmetric"]["windows"]["50-150"]["A_reads_B"] - 0.6528) < 5e-5
    at_contact = expected["symmetric"]["speeds_at_contact"]
    assert at_contact["v_a_over_c"] > 0.2 and at_contact["v_b_over_c"] < -0.2
    free = expected["symmetric_pass"]["speeds_at_contact"]
    assert abs(free["v_a_over_c"] - 0.2) < 1e-9 and abs(free["v_b_over_c"] + 0.2) < 1e-9
    window = expected["symmetric_pass"]["windows"]["50-150"]
    assert abs(window["A_reads_B"] - 2 / 3) < 1e-9 and abs(window["B_reads_A"] - 2 / 3) < 1e-9
    rest = expected["rest_frame"]["windows"]["50-150"]
    assert rest["A_reads_B"] > rest["natures_mutual"] > rest["B_reads_A"]
