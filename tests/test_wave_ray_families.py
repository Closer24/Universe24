"""Every ray a wave ray; light (wave-ray-family-v1): family, charge, phase width, rest rate.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Wave-ray families")
before the first run. Every board is built inline under the shared admission
(schema 1, link_ticks 1, metric links, pace 1/1, no decay, the six unit-axial
headings in Port order, closed under negation).
"""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter, pack
from event_universe.core.spatial_state import (
    CHARGE_INVARIANT,
    RAY_PROPERTIES,
    WAVE_RAY_FAMILY,
    Ray,
    advance_ray,
    ray_charge,
)
from event_universe.fields.disturbances import evaluate
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
PLUS_X, MINUS_X = [1, 0, 0], [-1, 0, 0]
# The wide phase (owner's decision of 2026-09-17): 128 bits, and an emission
# phase three steps of the clock below the turn. Since clock-readings-v1
# (2026-09-18) the clock is the content: the wide ray of 2 advances 2 steps per
# interval at K 1 (the rest rate 2^70 of the first pin is no family's to
# declare, and a content of 2^70 is beyond the bounded values).
WIDE_RATE = 2
# The massive family of case (b): eight bits, a ray of 4 at K 1 (four steps per
# interval since clock-readings-v1; 13 before), emitter phase 77.
MATTER_PHASES = [(77 + 4 * tick) % 256 for tick in range(1, 21)]


def document(shape, families, lamps, ticks, ray_interactions=None, n=8):
    """One conserved scalar per family, one holding lamp type per lamp, one ray field per family;
    `n` the world's one phase circle (the cleanup of 2026-09-18: one N for the world)."""
    return {
        "schema_version": 1,
        "N": n,
        "model_id": "wave-ray-families-test-v1",
        # K 1 (clock-readings-v1): a family that declares `clock` advances its
        # things' phase by their content per interval; the others ignore it.
        "K": 1,
        "shape": list(shape),
        "boundary": "periodic",
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
                "name": name,
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            }
            for name in families
        ],
        "disturbance_types": [
            {
                "name": lamp["type"],
                "fields": [lamp["field"]],
                "defaults": {lamp["field"]: lamp["stock"]},
                "transport": {"mode": "hold"},
            }
            for lamp in lamps
        ],
        "spatial_fields": [
            {
                "field": name,
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 6,
                "metric": "links",
                "pace": [1, 1],
                **extra,
            }
            for name, extra in families.items()
        ],
        "emissions": [
            {
                "type": lamp["type"],
                "field": lamp["field"],
                "amount": lamp["stock"],
                "denominator": 1,
                **lamp.get("emission", {}),
            }
            for lamp in lamps
        ],
        "seeds": [{"position": list(lamp["position"]), "type": lamp["type"]} for lamp in lamps],
        **({} if ray_interactions is None else {"ray_interactions": ray_interactions}),
    }


def rays_of(world):
    """Every Node holding a ray, with its bundles per spatial field, for exact comparison."""
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`); this module pins lines and events, not identities (test_bit_law does).
    return {
        node.position: tuple(tuple(replace(ray, owner=0) for ray in bundle) for bundle in node.rays)
        for node in world.inventory_view().nodes
        if any(node.rays)
    }


def reflect(charge_assignment=None, invariant_name="amount"):
    """Two families meet and each reverses its heading; amounts are declared invariant."""
    negated = [
        {
            "participant": side,
            "field": "heading",
            "expression": {"op": "neg", "args": [{"participant": side, "field": "heading"}]},
        }
        for side in range(2)
    ]
    return [
        {
            "name": "reflect",
            "participants": [{"type": "plus"}, {"type": "minus"}],
            "assignments": negated + ([] if charge_assignment is None else [charge_assignment]),
            "invariants": [
                {
                    "name": invariant_name,
                    "expression": {
                        "op": "add",
                        "args": [
                            {"participant": 0, "field": "amount"},
                            {"participant": 1, "field": "amount"},
                        ],
                    },
                }
            ],
        }
    ]


def test_every_ray_is_a_wave_ray(tmp_path):
    # (a) A plain family with a declared width and the same family declared with the
    # kerengonen key at rest rate 0 are one rule: each world is held to the same
    # pinned integers (no world is compared with another), the emitter's phase 5
    # carried unchanged by every ray.
    lamp = {
        "type": "lamp",
        "field": "quanta",
        "stock": 30,
        "position": (3, 3, 3),
        "emission": {"amount": 15, "kerengonen_phase": 5},
    }
    plain = Simulation(parse_initial_state(document((7, 7, 7), {"quanta": {}}, [lamp], 4)))
    phased = Simulation(
        parse_initial_state(
            document(
                (7, 7, 7),
                {"quanta": {"kerengonen": {"phase_steps": 8}}},
                [lamp],
                4,
            )
        )
    )
    for world, kerengonen, coherent in ((plain, False, False), (phased, True, True)):
        definition = world.initial.spatial_fields[0]
        assert (definition.phase_bits, definition.phase_modulus, definition.clock) == (
            8 - 5,
            8,
            0,
        )
        assert (definition.kerengonen, definition.coherent, definition.charge) == (
            kerengonen,
            coherent,
            0,
        )
    for tick in range(1, 5):
        for world in (plain, phased):
            world.step()
            # The first emission's six rays, one per Port, t Links from the lamp on
            # the 7-ring; after tick 4 each of those Nodes also holds the second
            # emission's ray coming the opposite way (steps 3), the two meeting
            # around the ring.
            held = rays_of(world)
            for port, (unit, amount) in enumerate(zip(HEADINGS, (3, 3, 3, 2, 2, 2), strict=True)):
                position = tuple((c + tick * u) % 7 for c, u in zip((3, 3, 3), unit, strict=True))
                (bundle,) = held[position]
                assert (
                    Ray(
                        port,
                        (0, 0, 0),
                        amount,
                        phase=5,
                        steps=tick,
                        event_ports=63,
                        event_shares=(3, 3, 3, 2, 2, 2),
                    )
                    in bundle
                )
                assert len(bundle) == (2 if tick == 4 else 1)
            rays = [ray for bundles in held.values() for bundle in bundles for ray in bundle]
            assert len(rays) == 6 * min(tick, 2)
            assert {ray.phase for ray in rays} == {5} and {ray.advance for ray in rays} == {-1}
            assert {ray.steps for ray in rays} == ({1} if tick == 1 else {tick, tick - 1})
            assert world.totals() == {"quanta": (30,)}
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            # One Link from the lamp along +X: the newest emission's ray of amount 3
            # after ticks 1 and 2, nothing after ticks 3 and 4.
            assert world.spatial_values((4, 3, 3))["quanta"]["value"] == ((3,) if tick <= 2 else (0,))
    for extra, emission, message in (
        # Every family is on the world's circle of N steps (the cleanup of
        # 2026-09-18): a phase at N or above is refused, one below it admitted.
        ({}, {"kerengonen_phase": 8}, "kerengonen_phase requires"),
        ({"kerengonen": {"phase_steps": 16}}, {}, "must equal N"),
        ({"kerengonen": {"phase_steps": 12}}, {}, "power of two"),
        ({"kerengonen": {"phase_advance": 8}}, {}, "clock-readings-v1"),
        # The record-as-owner field program is retired (the settled rule (v), the
        # cleanup of 2026-09-18): its keys are refused naming the rule.
        ({"kerengonen": {"capture": "threshold"}}, {}, "settled rule"),
        ({"self_exclusion": True}, {}, "settled rule"),
        ({}, {"kerengonen_mirror": "x"}, "settled rule"),
        ({"clock": True}, {"kerengonen_phase": "carried"}, "coherence table"),
        # One N for the world (the cleanup of 2026-09-18): a width on a family is
        # refused naming the definitions of the law.
        ({"phase_bits": 3}, {}, "definitions of the law"),
    ):
        raw = document(
            (7, 7, 7), {"quanta": extra}, [{**lamp, "emission": {"amount": 15, **emission}}], 1
        )
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
    raw = document((7, 7, 7), {"quanta": {"charge": 1}}, [lamp], 1)
    raw["spatial_fields"][0] = {"field": "quanta", "transport": "outward", "charge": 1}
    with pytest.raises(ValueError, match="require ray transport"):
        parse_initial_state(raw)
    for bad in (1, 12, 8192):
        raw = document((7, 7, 7), {"quanta": {}}, [lamp], 1, n=bad)
        with pytest.raises(ValueError, match="power of two from 2 through 4096"):
            parse_initial_state(raw)

    # (b) Light, a family with rest rate 0, keeps the emitter's phase 77 over 20
    # Links; a massive family of rest rate 13 advances by 13 per interval, masked
    # to eight bits.
    light = {
        "type": "lamp_light",
        "field": "light",
        "stock": 4,
        "position": (2, 2, 2),
        "emission": {"heading": PLUS_X, "kerengonen_phase": 77},
    }
    matter = {
        "type": "lamp_matter",
        "field": "matter",
        "stock": 4,
        "position": (2, 3, 3),
        "emission": {"heading": PLUS_X, "kerengonen_phase": 77},
    }
    world = Simulation(
        parse_initial_state(
            document(
                (25, 5, 5),
                {
                    "light": {},
                    "matter": {"kerengonen": {"phase_steps": 256}, "clock": True},
                },
                [light, matter],
                20,
                n=256,
            )
        )
    )
    light_field, matter_field = world.initial.spatial_fields
    assert (light_field.phase_bits, light_field.clock, light_field.kerengonen) == (8, 0, False)
    assert (matter_field.phase_bits, matter_field.clock, matter_field.coherent) == (8, 1, True)
    for tick in range(1, 21):
        world.step()
        stamp = {"steps": tick, "outbound": 1, "event_ports": 1, "event_shares": (4, 0, 0, 0, 0, 0)}
        assert rays_of(world) == {
            (2 + tick, 2, 2): ((Ray(0, (0, 0, 0), 4, phase=77, **stamp),), ()),
            (2 + tick, 3, 3): ((), (Ray(0, (0, 0, 0), 4, phase=MATTER_PHASES[tick - 1], **stamp),)),
        }
        assert MATTER_PHASES[tick - 1] == (77 + 4 * tick) % 256
        assert world.totals() == {"light": (4,), "matter": (4,)}

    # (c) Charge: two things, of charge +1 and -1 and contents 3 and 5, read 0 at
    # every tick, through a meeting that reverses both headings; the charge of
    # the things is an invariant of the declared interaction, and an interaction
    # that would change the total charge is rejected at validation. Re-pinned
    # 2026-09-18 (charge-per-thing-v1, Highlights 5.4 point 16 as amended): a
    # family's charge is the charge of one of its things, whole, whatever its
    # content, and the readouts count things, not quanta (3 - 5 = -2 before).
    # `detector` joined the view on 2026-09-17 (detector-bit-property-v1, feature
    # 2b): the Detector bit a ray carries, read-only like family and charge; and
    # `polarization` on 2026-09-17 (ray-polarization-v1, feature 11), read-only in
    # a guard, declared on a meeting's output.
    assert [field.name for field in RAY_PROPERTIES] == [
        "amount",
        "heading",
        "phase",
        "advance",
        "delay",
        "family",
        "charge",
        "detector",
        "polarization",
    ]
    plus = {
        "type": "lamp_plus",
        "field": "plus",
        "stock": 3,
        "position": (2, 2, 2),
        "emission": {"heading": PLUS_X},
    }
    minus = {
        "type": "lamp_minus",
        "field": "minus",
        "stock": 5,
        "position": (6, 2, 2),
        "emission": {"heading": MINUS_X},
    }
    families = {"plus": {"charge": 1}, "minus": {"charge": -1}}
    initial = parse_initial_state(document((9, 5, 5), families, [plus, minus], 6, reflect()))
    (rule,) = initial.ray_interactions
    assert [invariant.name for invariant in rule.invariants] == ["amount", CHARGE_INVARIANT]
    views = (
        (pack((3,)), pack((1, 0, 0)), pack((0,)), pack((-1,)), pack((0,)), pack((0,)), pack((1,))),
        (pack((5,)), pack((-1, 0, 0)), pack((0,)), pack((-1,)), pack((0,)), pack((1,)), pack((-1,))),
    )
    charge = next(invariant for invariant in rule.invariants if invariant.name == CHARGE_INVARIANT)
    assert evaluate(
        charge.expression, (), (), CostMeter(initial.operation_costs), participants=views
    ) == (0,)
    # Two things of the minus family read two charges, whatever their contents.
    assert ray_charge((Ray(0, (0, 0, 0), 3), Ray(1, (0, 0, 0), 4)), initial.spatial_fields[1]) == -2
    world = Simulation(initial)
    # Since ray-event-audit-v1 (2026-09-17) the readout counts the stock a record
    # holds of a charged family, the owners totals() reads (one thing not yet
    # emitted since charge-per-thing-v1); it read 0 and 0 before the first tick
    # before feature 10, over rays alone.
    assert world.charge_totals() == {"plus": 1, "minus": -1}
    for _tick in range(1, 7):
        world.step()
        assert world.charge_totals() == {"plus": 1, "minus": -1}
        assert sum(world.charge_totals().values()) == 0
        assert world.totals() == {"plus": (3,), "minus": (5,)}
    # After the meeting at (4, 2, 2) in tick 3 both rays are events of that one
    # interaction (Ports +X and -X, shares 5 and 3) walking apart, four Links on.
    stamp = {"steps": 4, "event_ports": 0b000011, "event_shares": (5, 3, 0, 0, 0, 0)}
    assert rays_of(world) == {
        (0, 2, 2): ((Ray(1, (0, 0, 0), 3, **stamp),), ()),
        (8, 2, 2): ((), (Ray(0, (0, 0, 0), 5, **stamp),)),
    }
    for rules, message in (
        (reflect({"participant": 0, "field": "charge", "expression": 0}), "read-only"),
        (reflect({"participant": 1, "field": "family", "expression": 0}), "read-only"),
        (reflect(invariant_name="charge"), "declared for every ray interaction"),
    ):
        with pytest.raises(ValueError, match=message):
            parse_initial_state(document((9, 5, 5), families, [plus, minus], 6, rules))

    # (d) The wide phase of the first pin (128 bits) is deleted with the per-family
    # width (the cleanup of 2026-09-18): N is one for the world, a power of two
    # up to 4096, and a wider circle adds no measured precision (Highlights 5.4,
    # the definitions of the law). A ray interaction still stores the phase as a
    # bounded value, so a world of 4096 steps parses and one whose rule reads a
    # phase over 30 bits cannot exist.
    wide = {
        "type": "lamp",
        "field": "matter",
        "stock": 2,
        "position": (2, 2, 2),
        "emission": {"heading": PLUS_X, "kerengonen_phase": 4093},
    }
    wide_families = {"matter": {"clock": True}}
    raw = document((7, 5, 5), wide_families, [wide], 100, n=4096)
    initial = parse_initial_state(raw)
    definition = initial.spatial_fields[0]
    assert (definition.phase_bits, definition.phase_modulus, definition.phase_mask) == (12, 4096, 4095)
    assert (definition.clock, definition.coherent, definition.kerengonen) == (1, False, True)
    world = Simulation(initial)
    for tick in range(1, 101):
        world.step()
        assert world.totals() == {"matter": (2,)}
        ((ray,), *_) = rays_of(world)[((2 + tick) % 7, 2, 2)]
        assert (ray.steps, ray.outbound, ray.amount) == (tick, 1, 2)
        assert ray.phase == (4093 + tick * WIDE_RATE) % 4096
    with pytest.raises(ValueError, match="power of two"):
        advance_ray(ray, (1, 0, 0), 12, 1)
    with pytest.raises(ValueError, match="kerengonen_phase requires"):
        parse_initial_state(
            document(
                (7, 5, 5),
                wide_families,
                [{**wide, "emission": {"heading": PLUS_X, "kerengonen_phase": 4096}}],
                1,
                n=4096,
            )
        )
    # The runner records the identity and N beside the ray state and runs the world.
    path = tmp_path / "wide.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=100)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["wave_ray"] == WAVE_RAY_FAMILY == "wave-ray-family-v1"
    assert metadata["ray_state"] == "ray-event-state-v1"
    assert metadata["spatial_policy"] == "kerengonen-ray-field-v1"
    assert metadata["conserved_at_every_completed_tick"] and metadata["final_totals"]["matter"] == [2]
    assert metadata["completed_ticks"] == 100
