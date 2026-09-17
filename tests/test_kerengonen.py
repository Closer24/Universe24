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
    raw = two_lamps(4, 1)
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
    # Every ray is a wave ray (wave-ray-family-v1): a plain field admits an emission
    # phase below its declared width, and without a declared width only phase 0.
    raw = two_lamps(4, 1)
    del raw["spatial_fields"][0]["kerengonen"]
    raw["emissions"][1]["kerengonen_phase"] = 2
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


def single_quanta_document(steps, advance, absorber, phase_b=0):
    raw = two_lamps(steps, advance, absorber=absorber, phase_b=phase_b, ticks=12)
    for rule in raw["emissions"]:
        rule["amount"] = 2  # one quantum per ray, each way
    return raw


def absorber_of(world):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == 2
    )


def test_the_ticket_rule_is_bounded_and_no_absorber_draws_from_it():
    from event_universe.core.spatial_state import TICKET_MODULUS, next_ticket, ticket_draw

    # The bounded local draw stays for the Detector mark; an absorber never uses it.
    assert next_ticket(0, 0) == 1 and next_ticket(1, 5) == 48277
    assert ticket_draw(3) == 9 and 0 <= ticket_draw(TICKET_MODULUS - 1) < TICKET_MODULUS
    with pytest.raises(ValueError, match="ticket state"):
        next_ticket(TICKET_MODULUS, 0)
    # Single quanta at a quarter turn (x = 1 with eight steps): the share rule
    # truncates one quantum times one half to nothing, so only the two quanta
    # absorbed before the second lamp's rays arrive are taken, deterministically.
    share = Simulation(parse_initial_state(single_quanta_document(8, 1, 1)))
    for _ in range(12):
        share.step()
    report = share.conservation_report()
    assert report["status"] == "passed"
    assert share.totals()["quanta"][0] + report["escaped"]["energy"] == 800
    assert absorber_of(share)["quanta"] == (2,)


def test_the_capture_is_share_or_threshold_and_never_a_lottery():
    raw = single_quanta_document(4, 1, 0)
    raw["spatial_fields"][0]["kerengonen"]["capture"] = "dice"
    with pytest.raises(ValueError, match="share or threshold"):
        parse_initial_state(raw)
    raw = single_quanta_document(4, 1, 0)
    raw["spatial_fields"][0]["kerengonen"]["capture"] = "lottery"
    with pytest.raises(ValueError, match="lottery capture was deleted"):
        parse_initial_state(raw)
    raw = single_quanta_document(4, 1, 0)
    raw["spatial_fields"][0]["kerengonen"]["capture_seed"] = 7
    with pytest.raises(ValueError, match="unknown keys"):
        parse_initial_state(raw)


def huygens_document(lamp_b_phase=0, carried=True, ticks=12):
    """Lamp A -> slit -> Node (3, 0) <- lamp B from above: the slit re-emits what it absorbed.

    Headings +x and -y only, so nothing ever comes back to the slit.
    """
    raw = two_lamps(8, 1, ticks=ticks)
    del raw["conservation"]
    raw["spatial_fields"][0]["headings"] = [[1, 0, 0], [0, -1, 0]]
    raw["disturbance_types"].append(
        {
            "name": "slit",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }
    )
    for rule in raw["emissions"]:
        del rule["recoil_field"]
    raw["emissions"][0]["amount"] = 8
    raw["emissions"][1]["amount"] = 4
    if lamp_b_phase:
        raw["emissions"][1]["kerengonen_phase"] = lamp_b_phase
    slit_emission = {
        "type": "slit",
        "field": "quanta",
        "amount": {"field": "quanta"},
        "denominator": 1,
        "source": False,
    }
    if carried:
        slit_emission["kerengonen_phase"] = "carried"
    raw["emissions"].append(slit_emission)
    raw["spatial_couplings"].append(
        {"name": "slit_absorbs", "type": "slit", "field": "quanta", "mode": "absorb"}
    )
    raw["seeds"] = [
        {"position": [CENTER - 4, CENTER, CENTER], "type": "lamp_a"},
        {"position": [CENTER + 3, CENTER + 4, CENTER], "type": "lamp_b"},
        {"position": [CENTER, CENTER, CENTER], "type": "slit"},
    ]
    return raw


def test_a_slit_re_emits_the_phase_it_absorbed_so_the_wave_continues_through_it():
    # Lamp A's +x rays (4 quanta) reach the slit after four links, phase 4. The slit
    # absorbs them, stores that phase, and next cycle re-emits its stock over both
    # headings (2 quanta each way) at phase 5: the slit's own tick counts as one
    # advance. Three more links to (3, 0) make phase 0. Lamp B's -y rays (2 quanta)
    # reach (3, 0) after four links at phase 4: opposite, and the Node reads zero
    # although 4 quanta are resident. Offsetting lamp B by four steps makes them
    # equal: the Node reads 4. A slit that re-emits at a fixed phase 0 instead
    # arrives at phase 3, a partial 4 x |2 e^0 + 2 e^(i pi/4)|^2 / 16 = 3.
    readings = {}
    for name, raw in (
        ("carried", huygens_document()),
        ("offset", huygens_document(lamp_b_phase=4)),
        ("fixed", huygens_document(carried=False)),
    ):
        world = Simulation(parse_initial_state(raw))
        initial = world.totals()["quanta"][0]
        for _ in range(12):
            world.step()
        readings[name] = value_at(world, 3)
        assert world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == initial
        slit = next(
            world.record_values(r)
            for node in world.nodes.values()
            for r in node.records
            if r is not None and r.type_index == 3
        )
        assert slit["quanta"] == (4,)  # this cycle's absorption, re-emitted next cycle
    assert readings == {"carried": 0, "offset": 4, "fixed": 3}
    # A carried phase needs an absorb rule for the emitter on that field.
    raw = huygens_document()
    raw["spatial_couplings"] = raw["spatial_couplings"][:1]
    with pytest.raises(ValueError, match="requires an absorb rule on the same field"):
        parse_initial_state(raw)


def test_a_ray_carries_its_own_advance_and_an_emitter_sets_it_from_its_momentum():
    # A ray with its own advance ignores the field's; -1 means the field's.
    own = Ray(0, (0, 0, 0), 3, 0, 4)
    assert advance_ray(own, (1, 0, 0), 64, 1)[1].phase == 4
    assert advance_ray(Ray(0, (0, 0, 0), 3, 0), (1, 0, 0), 64, 1)[1].phase == 1
    assert merge_rays((Ray(0, (0, 0, 0), 1, 0, 4), Ray(0, (0, 0, 0), 1, 0, 8))) == (
        Ray(0, (0, 0, 0), 1, 0, 4),
        Ray(0, (0, 0, 0), 1, 0, 8),
    )
    # Two beams of momentum 16 and 32 on one 64-step field, advance = |p| / 4:
    # after three links their rays sit at phases 12 and 24.
    raw = two_lamps(64, 1, ticks=6)
    del raw["conservation"]
    raw["spatial_fields"][0]["headings"] = [[1, 0, 0]]
    raw["spatial_fields"][0]["rays_per_tick"] = 1
    momentum = {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]}
    for rule in raw["emissions"]:
        del rule["recoil_field"]
        rule["amount"] = 2
        rule["kerengonen_advance"] = {"amount": momentum, "denominator": 4}
    raw["disturbance_types"][0]["defaults"]["momentum"] = [16, 0, 0]
    raw["disturbance_types"][1]["defaults"]["momentum"] = [32, 0, 0]
    raw["seeds"] = [
        {"position": [CENTER - 6, CENTER, CENTER], "type": "lamp_a"},
        {"position": [CENTER - 6, CENTER + 2, CENTER], "type": "lamp_b"},
    ]
    world = Simulation(parse_initial_state(raw))
    for _ in range(4):
        world.step()
    rays = {
        node.position[1] - CENTER: node.rays[0]
        for node in world.inventory_view().nodes
        if node.rays and node.rays[0]
    }
    assert {r.advance for r in rays[0]} == {4} and {r.advance for r in rays[2]} == {8}
    # Same links traveled, twice the phase: the fast beam's wavelength is half.
    slow = sorted(r.phase for r in rays[0])
    fast = sorted(r.phase for r in rays[2])
    assert slow and fast == [2 * phase for phase in slow] and all(phase % 4 == 0 for phase in slow)
    # A negative or non-kerengonen advance is rejected.
    raw["emissions"][0]["kerengonen_advance"] = {"amount": -4}
    with pytest.raises(ValueError, match="must not be negative"):
        Simulation(parse_initial_state(raw)).step()
    del raw["spatial_fields"][0]["kerengonen"]
    with pytest.raises(ValueError, match="kerengonen_advance requires"):
        parse_initial_state(raw)


def test_a_slit_carries_the_absorbed_advance_with_the_phase():
    # The Huygens test again, on a 64-step field whose lamps advance 4 per link
    # from momentum 16 while the field's own advance is 1: the slit must re-emit
    # at the lamps' advance, or the wave changes wavelength at the slit.
    raw = huygens_document(ticks=12)
    raw["spatial_fields"][0]["kerengonen"] = {"phase_steps": 64, "phase_advance": 1}
    momentum = {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]}
    for rule in raw["emissions"][:2]:
        rule["kerengonen_advance"] = {"amount": momentum, "denominator": 4}
    for kind in raw["disturbance_types"][:2]:
        kind["defaults"]["momentum"] = [16, 0, 0]
    # Lamp A -> slit: 4 links at 4 = 16; the slit's tick adds 4 and three links add
    # 12: phase 32. Lamp B -> (3, 0): 4 links at 4 = 16. A quarter turn apart,
    # reading 2; with lamp B offset 16 steps equal, reading 4; offset 48, opposite,
    # reading 0. Had the slit used the field's advance 1 the readings would differ.
    readings = []
    for offset in (0, 16, 48):
        doc = json.loads(json.dumps(raw))
        if offset:
            doc["emissions"][1]["kerengonen_phase"] = offset
        world = Simulation(parse_initial_state(doc))
        for _ in range(12):
            world.step()
        readings.append(value_at(world, 3))
    assert readings == [2, 4, 0]


def mirror_document(advance=4, mirror_x=6, ticks=24, phase_b=0):
    """Lamp A at x = -6 fires +x; a mirror at x = mirror_x sends the wave back along -x."""
    raw = two_lamps(64, 1, ticks=ticks)
    del raw["conservation"]
    raw["spatial_fields"][0]["headings"] = [[1, 0, 0], [-1, 0, 0]]
    raw["spatial_fields"][0]["kerengonen"] = {"phase_steps": 64, "phase_advance": advance}
    raw["disturbance_types"].append(
        {
            "name": "mirror",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }
    )
    raw["emissions"] = [
        {
            "type": "lamp_a",
            "field": "quanta",
            "amount": 8,
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
        },
        {
            "type": "mirror",
            "field": "quanta",
            "amount": {"field": "quanta"},
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
            "kerengonen_phase": "carried",
            "kerengonen_mirror": "x",
        },
    ]
    raw["spatial_couplings"].append(
        {
            "name": "mirror_absorbs",
            "type": "mirror",
            "field": "quanta",
            "mode": "absorb",
            "momentum_field": "momentum",
        }
    )
    raw["seeds"] = [
        {"position": [CENTER - 6, CENTER, CENTER], "type": "lamp_a"},
        {"position": [CENTER + mirror_x, CENTER, CENTER], "type": "mirror"},
    ]
    return raw


def test_a_mirror_sends_the_wave_back_along_the_reflected_heading_as_a_standing_wave():
    # The lamp fires 4 quanta each way every tick; the +x rays reach the mirror at
    # x = 6 after 12 links, phase 48 at advance 4. The mirror re-emits its stock along
    # -x only, at the carried phase plus one advance. Between them incident and
    # reflected rays meet with equal amounts: the reading is 8 cos^2 of half their
    # phase difference, which changes by 2 x advance per link, so the standing wave
    # repeats every 64 / (2 x advance) links: 8 at advance 4, 4 at advance 8.
    world = Simulation(parse_initial_state(mirror_document(advance=4)))
    for _ in range(24):
        world.step()
    rays = {
        node.position[0] - CENTER: node.rays[0]
        for node in world.inventory_view().nodes
        if node.rays and node.rays[0]
    }
    # Reflected rays exist, travel -x, and carry the field's advance and the mirror's phase.
    backward = [ray for x in rays for ray in rays[x] if ray.heading == 1 and x < 6]
    assert backward and all(ray.advance == -1 for ray in backward)
    mirror = next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == 3
    )
    # The mirror holds what it absorbed this cycle and has taken the reversed momentum.
    assert mirror["quanta"] == (4,) and mirror["momentum"][0] > 0
    assert world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == 400
    readings = [value_at(world, x) for x in range(-5, 6)]
    assert readings == [0, 2, 5, 7, 7, 5, 2, 0, 0, 2, 5]
    assert readings[:3] == readings[8:11]
    faster = Simulation(parse_initial_state(mirror_document(advance=8)))
    for _ in range(24):
        faster.step()
    readings = [value_at(faster, x) for x in range(-5, 6)]
    assert readings[:3] == readings[4:7] == readings[8:11]
    assert readings == [6, 1, 1, 6, 6, 1, 1, 6, 6, 1, 1]  # period 4, no exact node on this grid


def test_the_mirror_emission_is_validated():
    raw = mirror_document()
    raw["spatial_fields"][0]["headings"] = [[1, 0, 0], [0, 1, 0]]
    with pytest.raises(ValueError, match="mirror image"):
        parse_initial_state(raw)
    raw = mirror_document()
    del raw["emissions"][1]["recoil_field"]
    with pytest.raises(ValueError, match="recoil_field"):
        parse_initial_state(raw)
    raw = mirror_document()
    raw["emissions"][1]["kerengonen_mirror"] = "w"
    with pytest.raises(ValueError, match="xy, xz or yz"):
        parse_initial_state(raw)
    raw = mirror_document()
    raw["spatial_couplings"] = raw["spatial_couplings"][:1]
    with pytest.raises(ValueError, match="requires an absorb rule"):
        parse_initial_state(raw)


def test_a_directed_emitter_fires_one_heading_and_is_validated():
    raw = mirror_document()
    raw["emissions"][0]["heading"] = [-1, 0, 0]
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(6):
        world.step()
    headings = {
        ray.heading
        for node in world.inventory_view().nodes
        for ray in (node.rays[0] if node.rays else ())
    }
    # Every ray of the lamp went along -x (heading index 1); nothing swept +x.
    assert headings == {1}
    assert world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == initial
    raw = mirror_document()
    raw["emissions"][0]["heading"] = [0, 1, 0]
    with pytest.raises(ValueError, match="one of the field's headings"):
        parse_initial_state(raw)
    raw = mirror_document()
    raw["emissions"][1]["heading"] = [1, 0, 0]
    with pytest.raises(ValueError, match="kerengonen_mirror"):
        parse_initial_state(raw)


def test_a_thick_screen_absorbs_what_a_thin_one_lets_pass():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "double_slit_probe_thick",
        Path(__file__).resolve().parents[1] / "examples/kerengonen-double-slit/run_experiments.py",
    )
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
    headings = probe.planar_headings(32, probe.HEADING_SCALE)
    thin = probe.run(probe.document(24, headings, screen_half=4))
    thick = probe.run(probe.document(24, headings, screen_half=4, layers=3))
    assert thin["quanta_closed"] and thick["quanta_closed"]
    assert thick["layer_totals"][0] == thin["absorbed_total"]
    assert thick["absorbed_total"] >= thin["absorbed_total"] and len(thick["layer_totals"]) == 3


def dissolving_document(after=3, over=4, stock=10, ticks=12, moving=False):
    """One particle of `stock` quanta on a one-heading field pays itself out on a schedule."""
    raw = two_lamps(8, 1, ticks=ticks)
    del raw["conservation"]
    raw["spatial_fields"][0]["headings"] = [[1, 0, 0]]
    raw["spatial_fields"][0]["rays_per_tick"] = 1
    raw["disturbance_types"] = [
        {
            "name": "particle",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": stock, "momentum": [4, 0, 0]},
            "transport": {"mode": "hold"}
            if not moving
            else {
                "mode": "move",
                "direction_field": "momentum",
                "rate": {"op": "min", "args": [1, {"field": "quanta"}]},
                "rate_denominator": 1,
            },
        }
    ]
    raw["emissions"] = [
        {
            "type": "particle",
            "field": "quanta",
            "source": False,
            "dissolve": {"after_ticks": after, "over_ticks": over},
        }
    ]
    raw["spatial_couplings"] = []
    raw["seeds"] = [{"position": [CENTER - 4, CENTER, CENTER], "type": "particle"}]
    return raw


def particle_stock(world):
    return [
        world.record_values(r)["quanta"][0]
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == 0
    ]


def test_a_dissolving_record_pays_its_initial_stock_out_on_the_schedule():
    world = Simulation(parse_initial_state(dissolving_document()))
    stocks = []
    for _ in range(9):
        world.step()
        stocks.append(particle_stock(world)[0])
    # Nothing for three cycles, then ceil(10 / 4) = 3 per cycle until the last quantum.
    assert stocks == [10, 10, 10, 7, 4, 1, 0, 0, 0]
    assert world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == 10
    # A moving particle keeps flying while it holds quanta and stops when empty; the
    # schedule counts its own cycles wherever it is.
    world = Simulation(parse_initial_state(dissolving_document(moving=True)))
    positions = []
    for _ in range(9):
        world.step()
        found = [
            position[0] - CENTER
            for position, node in world.nodes.items()
            for r in node.records
            if r is not None and r.type_index == 0
        ]
        positions.append(found[0] if found else None)
    assert positions[0] == -3 and positions[5] == 2 and positions[6] == positions[8] == 2
    assert world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == 10


def test_dissolution_is_validated():
    raw = dissolving_document()
    raw["emissions"][0]["source"] = True
    with pytest.raises(ValueError, match="funded emission on a ray field"):
        parse_initial_state(raw)
    raw = dissolving_document()
    del raw["emissions"][0]["dissolve"]
    with pytest.raises(ValueError, match="requires an amount"):
        parse_initial_state(raw)
    raw = dissolving_document()
    raw["emissions"][0]["dissolve"] = {"after_ticks": 0, "over_ticks": 0}
    with pytest.raises(ValueError, match="over_ticks"):
        parse_initial_state(raw)


def test_a_euclidean_pace_makes_the_wave_front_round_and_keeps_waiting_rays():
    from event_universe.core.spatial_state import heading_paces, integer_sqrt

    assert [integer_sqrt(v) for v in (0, 1, 2, 3, 4, 15, 16, 17, 1000000)] == [
        0,
        1,
        1,
        1,
        2,
        3,
        4,
        4,
        1000,
    ]
    raw = two_lamps(64, 1, ticks=12)
    del raw["conservation"]
    raw["spatial_fields"][0]["headings"] = [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
    raw["spatial_fields"][0]["rays_per_tick"] = 3
    raw["spatial_fields"][0]["metric"] = "euclidean"
    definition = parse_initial_state(raw).spatial_fields[0]
    paces = heading_paces(definition)
    # Manhattan 1, 2, 3 against Euclidean 1, sqrt 2, sqrt 3: the body diagonal hops
    # every tick and the axis ray once in sqrt 3 ticks.
    # Reducing the integer ratios must preserve the same physical schedule.
    assert paces[2][0] == paces[2][1]
    assert paces[0][0] * 4096 == paces[0][1] * 2364
    assert paces[1][0] * 2896 == paces[1][1] * 2364
    raw["emissions"] = raw["emissions"][:1]
    raw["emissions"][0]["amount"] = 3
    raw["seeds"] = raw["seeds"][:1]
    world = Simulation(parse_initial_state(raw))
    lamp = raw["seeds"][0]["position"][0]
    reach = []
    for _ in range(12):
        world.step()
        far = {}
        for node in world.inventory_view().nodes:
            for ray in node.rays[0] if node.rays else ():
                offset = (node.position[0] - lamp, node.position[1] - CENTER, node.position[2] - CENTER)
                far[ray.heading] = max(far.get(ray.heading, 0), sum(abs(o) for o in offset))
        reach.append(far)
    # The body diagonal hops every tick, so every heading moves 0.577 link-lengths of
    # Euclidean distance per tick: after twelve ticks the first axis ray has made
    # about 6.9 links, the first face diagonal 9.8 links along its staircase, the
    # body diagonal 12; measured from the lamp, which keeps emitting behind them.
    assert reach[-1][0] in (6, 7) and reach[-1][1] in (9, 10) and reach[-1][2] == 12
    assert reach[3][0] == 2 and reach[3][2] == 4
    assert world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == 400
    raw["spatial_fields"][0]["metric"] = "hops"
    with pytest.raises(ValueError, match="links or euclidean"):
        parse_initial_state(raw)


def test_a_diagonal_mirror_swaps_the_heading_axes_and_a_fraction_makes_it_partial():
    raw = mirror_document(advance=4)
    raw["spatial_fields"][0]["headings"] = [[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]]
    raw["spatial_fields"][0]["rays_per_tick"] = 4
    raw["emissions"][0]["amount"] = 8
    raw["emissions"][1]["kerengonen_mirror"] = "xy"
    world = Simulation(parse_initial_state(raw))
    for _ in range(16):
        world.step()
    # The +x ray reaching the mirror at x = 6 comes back along +y: the mirror's Node
    # column above it holds rays of heading index 1 and nothing returns along -x.
    rays = {
        tuple(p - CENTER for p in node.position): [r.heading for r in node.rays[0]]
        for node in world.inventory_view().nodes
        if node.rays and node.rays[0]
    }
    above = [h for (x, y, z), hs in rays.items() if x == 6 and y > 0 for h in hs]
    assert above and set(above) == {1}
    assert not [h for (x, y, z), hs in rays.items() if 0 < x < 6 and y == 0 for h in hs if h == 2]
    # A partial mirror: absorb a quarter, let the rest pass; the quarter comes back.
    raw = mirror_document(advance=4)
    raw["spatial_couplings"][-1].update({"fraction": 1, "fraction_denominator": 4})
    world = Simulation(parse_initial_state(raw))
    for _ in range(20):
        world.step()
    rays = {
        node.position[0] - CENTER: [(r.heading, r.amount) for r in node.rays[0]]
        for node in world.inventory_view().nodes
        if node.rays and node.rays[0]
    }
    passed = [amount for x, rs in rays.items() if x > 6 for h, amount in rs if h == 0]
    reflected = [amount for x, rs in rays.items() if 0 < x < 6 for h, amount in rs if h == 1]
    assert passed and set(passed) == {3} and reflected and set(reflected) == {1}
    assert world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == 400
