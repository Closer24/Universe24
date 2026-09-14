"""Kerengonen: phased rays that combine by phase at a Node, whole quanta on capture."""

import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    Ray,
    SpatialFieldDefinition,
    advance_ray,
    coherence,
    coherent_stock,
    merge_rays,
    phase_cosines,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

CENTER = 7


def phased(steps=4, advance=1):
    return SpatialFieldDefinition(
        0,
        (0,),
        transport="ray",
        headings=((1, 0, 0), (-1, 0, 0)),
        rays_per_tick=1,
        ray_slots=8,
        phase_steps=steps,
        phase_advance=advance,
    )


def test_phase_advances_on_every_link_and_wraps():
    ray = Ray(0, (0, 0, 0), 3, 2)
    port, moved = advance_ray(ray, (1, 0, 0), 4, 1)
    assert port == 0 and moved.phase == 3
    assert advance_ray(moved, (1, 0, 0), 4, 1)[1].phase == 0
    # A plain ray field never touches the phase.
    assert advance_ray(ray, (1, 0, 0))[1].phase == 2
    assert merge_rays((Ray(0, (0, 0, 0), 1, 1), Ray(0, (0, 0, 0), 2, 1), Ray(0, (0, 0, 0), 4, 2))) == (
        Ray(0, (0, 0, 0), 3, 1),
        Ray(0, (0, 0, 0), 4, 2),
    )


def test_coherence_is_exact_at_equal_and_opposite_phases():
    definition = phased(4, 1)
    assert phase_cosines(4) == (256, 0, -256, 0)
    same = (Ray(0, (0, 0, 0), 5, 1), Ray(1, (0, 0, 0), 7, 1))
    numerator, denominator = coherence(same, definition)
    assert numerator == denominator and coherent_stock(same, definition) == 12
    opposite = (Ray(0, (0, 0, 0), 5, 0), Ray(1, (0, 0, 0), 5, 2))
    assert coherence(opposite, definition)[0] == 0 and coherent_stock(opposite, definition) == 0
    quarter = (Ray(0, (0, 0, 0), 4, 0), Ray(1, (0, 0, 0), 4, 1))
    numerator, denominator = coherence(quarter, definition)
    assert numerator * 2 == denominator and coherent_stock(quarter, definition) == 4
    # Without the key every set is fully coherent and the stock is the plain sum.
    plain = SpatialFieldDefinition(
        0, (0,), transport="ray", headings=((1, 0, 0),), rays_per_tick=1, ray_slots=8
    )
    assert coherence(opposite, plain) == (1, 1) and coherent_stock(opposite, plain) == 10
    with pytest.raises(ValueError, match="phase_steps"):
        phase_cosines(1)


def two_lamps(steps, advance, separation=6, ticks=8, absorber=None, phase_b=0):
    """Two funded lamps on the x axis fire at each other; a body between them may absorb."""
    raw = {
        "schema_version": 1,
        "model_id": "kerengonen-two-lamp-test-v1",
        "shape": [15, 15, 15],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "lamp_a",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 400, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "lamp_b",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 400, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "body",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0], [-1, 0, 0]],
                "rays_per_tick": 2,
                "ray_slots": 8,
                "kerengonen": {"phase_steps": steps, "phase_advance": advance},
            }
        ],
        "emissions": [
            {
                "type": "lamp_a",
                "field": "quanta",
                "amount": 4,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            },
            {
                "type": "lamp_b",
                "field": "quanta",
                "amount": 4,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": phase_b,
            },
        ],
        "spatial_couplings": [
            {
                "name": "body_absorbs",
                "type": "body",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        ],
        "seeds": [
            {"position": [CENTER - separation // 2, CENTER, CENTER], "type": "lamp_a"},
            {"position": [CENTER + separation // 2, CENTER, CENTER], "type": "lamp_b"},
        ],
        "conservation": {
            "name": "quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["quanta", "momentum"],
                    "energy": {"field": "quanta"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "quanta", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }
    if absorber is not None:
        raw["seeds"].append({"position": [CENTER + absorber, CENTER, CENTER], "type": "body"})
    return raw


def value_at(world, x):
    return world.spatial_values((CENTER + x, CENTER, CENTER))["quanta"]["value"][0]


def test_rays_from_two_lamps_combine_by_phase_where_they_meet():
    # Lamps at x = -3 and +3 fire a 2-quantum ray each way every tick; the +x ray of
    # lamp_a and the -x ray of lamp_b cross between them. With four phase steps and
    # one step per link the phase difference at x is 2x steps: rays meeting at even
    # x are in phase (value 4), at odd x opposite (value 0), while every ray still
    # carries its quanta onward. With eight steps, x = 1 is a quarter turn: value 2.
    world = Simulation(parse_initial_state(two_lamps(4, 1)))
    for _ in range(7):
        world.step()
    assert [value_at(world, x) for x in (-2, -1, 0, 1, 2)] == [4, 0, 4, 0, 4]
    report = world.conservation_report()
    assert report["status"] == "passed"
    assert world.totals()["quanta"][0] + report["escaped"]["energy"] == 800
    eighth = Simulation(parse_initial_state(two_lamps(8, 1)))
    for _ in range(7):
        eighth.step()
    assert [value_at(eighth, x) for x in (0, 1, 2)] == [4, 2, 0]
    # The same world without phase advance is the plain ray field: values add.
    plain = Simulation(parse_initial_state(two_lamps(4, 0)))
    for _ in range(7):
        plain.step()
    assert [value_at(plain, x) for x in (-2, -1, 0, 1, 2)] == [4, 4, 4, 4, 4]


def test_an_absorber_takes_whole_quanta_gated_by_coherence():
    # At x = 1 the crossing rays are opposite: the body absorbs nothing and both rays
    # pass. At x = 0 they are in phase: it absorbs everything. A lamp_b phase offset of
    # two steps makes x = 1 bright instead.
    dark = Simulation(parse_initial_state(two_lamps(4, 1, absorber=1)))
    bright = Simulation(parse_initial_state(two_lamps(4, 1, absorber=0)))
    shifted = Simulation(parse_initial_state(two_lamps(4, 1, absorber=1, phase_b=2)))
    for world in (dark, bright, shifted):
        for _ in range(8):
            world.step()
    bodies = {}
    for name, world in (("dark", dark), ("bright", bright), ("shifted", shifted)):
        bodies[name] = next(
            world.record_values(r)
            for node in world.nodes.values()
            for r in node.records
            if r is not None and r.type_index == 2
        )
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert world.totals()["quanta"][0] + report["escaped"]["energy"] == 800
    # Before lamp_a's ray arrives at x = 1 (tick 5) lamp_b's rays are alone there and
    # fully coherent: two of them are absorbed, 2 quanta and heading (-1, 0, 0) each.
    # From tick 5 the crossing pair is opposite and nothing more is absorbed.
    assert bodies["dark"]["quanta"] == (4,) and bodies["dark"]["momentum"] == (-4, 0, 0)
    # The crossing pair is absorbed at x = 0 on five cycles: 2 + 2 quanta each,
    # momentum +2 and -2 that cancel.
    assert bodies["bright"]["quanta"] == (20,) and bodies["bright"]["momentum"] == (0, 0, 0)
    assert bodies["shifted"]["quanta"] == (20,)


def test_kerengonen_is_validated_and_identified(tmp_path):
    # The runner's per-tick accounting counts record momentum only, so the identity
    # run keeps the lamps recoil-free; the event audit covers recoil in the tests above.
    raw = two_lamps(4, 1)
    for rule in raw["emissions"]:
        del rule["recoil_field"]
    path = tmp_path / "two_lamps.json"
    path.write_text(json.dumps(raw))
    run_initialization(path, tmp_path / "out", ticks=2)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["spatial_policy"] == "kerengonen-ray-field-v1"
    assert metadata["spatial_transport"] == "straight-rays"
    for patch, message in (
        ({"phase_steps": 1, "phase_advance": 0}, "phase_steps"),
        ({"phase_steps": 4, "phase_advance": 4}, "phase_advance"),
        ({"phase_steps": 4}, "kerengonen"),
    ):
        raw = two_lamps(4, 1)
        raw["spatial_fields"][0]["kerengonen"] = patch
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
    raw = two_lamps(4, 1)
    raw["emissions"][1]["kerengonen_phase"] = 4
    with pytest.raises(ValueError, match="kerengonen_phase"):
        parse_initial_state(raw)
    raw = two_lamps(4, 1)
    del raw["spatial_fields"][0]["kerengonen"]
    with pytest.raises(ValueError, match="kerengonen_phase requires"):
        parse_initial_state(raw)
    raw = two_lamps(4, 1)
    raw["spatial_fields"][0]["transport"] = "outward"
    for key in ("headings", "rays_per_tick", "ray_slots"):
        del raw["spatial_fields"][0][key]
    with pytest.raises(ValueError, match="require ray transport"):
        parse_initial_state(raw)


def test_double_slit_probe_composes_and_closes():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "double_slit_probe",
        Path(__file__).resolve().parents[1] / "examples/kerengonen-double-slit/run_experiments.py",
    )
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
    headings = probe.planar_headings(16, probe.HEADING_SCALE)
    assert all(h[0] > 0 and h[2] == 0 for h in headings) and len({tuple(h) for h in headings}) == len(
        headings
    )
    assert [probe.path_difference(y) for y in (-3, -1, 0, 1, 3)] == [-6, -2, 0, 2, 6]
    phased = probe.run(probe.document(8, headings, screen_half=2))
    plain = probe.run(probe.document(8, headings, phase_steps=0, screen_half=2))
    assert phased["quanta_closed"] and plain["quanta_closed"]
    assert parse_initial_state(probe.document(4, headings, phase_b=4, screen_half=1))
