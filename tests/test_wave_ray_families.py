"""Every ray a wave ray; light (wave-ray-family-v1): family, charge, phase width, rest rate.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Wave-ray families")
before the first run. Every board is built inline under the shared admission
(schema 1, link_ticks 1, metric links, pace 1/1, no decay, the six unit-axial
headings in Port order, closed under negation).
"""

import json
import time
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
from event_universe.fields.rays import forward_rays
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
PLUS_X, MINUS_X = [1, 0, 0], [-1, 0, 0]
# The wide phase (owner's decision of 2026-09-17): 128 bits, a rest rate of 2^70
# steps per interval, and an emission phase three rates below the turn.
WIDE_RATE = 1 << 70
WIDE_MODULUS = 1 << 128
WIDE_PHASE = WIDE_MODULUS - 3 * WIDE_RATE
# The massive family of case (b): eight bits, rest rate 13, emitter phase 77.
MATTER_PHASES = [
    90,
    103,
    116,
    129,
    142,
    155,
    168,
    181,
    194,
    207,
    220,
    233,
    246,
    3,
    16,
    29,
    42,
    55,
    68,
    81,
]


def document(shape, families, lamps, ticks, ray_interactions=None):
    """One conserved scalar per family, one holding lamp type per lamp, one ray field per family."""
    return {
        "schema_version": 1,
        "model_id": "wave-ray-families-test-v1",
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
                "ray_slots": 8,
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
                "source": False,
                **lamp.get("emission", {}),
            }
            for lamp in lamps
        ],
        "seeds": [{"position": list(lamp["position"]), "type": lamp["type"]} for lamp in lamps],
        **({} if ray_interactions is None else {"ray_interactions": ray_interactions}),
    }


def rays_of(world):
    """Every Node holding a ray, with its bundles per spatial field, for exact comparison."""
    return {node.position: node.rays for node in world.inventory_view().nodes if any(node.rays)}


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
    plain = Simulation(
        parse_initial_state(document((7, 7, 7), {"quanta": {"phase_bits": 3}}, [lamp], 4))
    )
    phased = Simulation(
        parse_initial_state(
            document(
                (7, 7, 7),
                {"quanta": {"kerengonen": {"phase_steps": 8, "phase_advance": 0}}},
                [lamp],
                4,
            )
        )
    )
    for world, kerengonen, coherent in ((plain, False, False), (phased, True, True)):
        definition = world.initial.spatial_fields[0]
        assert (definition.phase_bits, definition.phase_modulus, definition.phase_advance) == (
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
        ({}, {"kerengonen_phase": 5}, "kerengonen_phase requires"),
        ({"phase_bits": 4, "kerengonen": {"phase_steps": 8, "phase_advance": 0}}, {}, "2 to the power"),
        ({"kerengonen": {"phase_steps": 12, "phase_advance": 0}}, {}, "power of two"),
        ({"phase_bits": 3, "kerengonen": {"phase_advance": 8}}, {}, "phase_advance requires"),
        (
            {"phase_bits": 3, "kerengonen": {"phase_advance": 1, "capture": "threshold"}},
            {},
            "capture requires",
        ),
        (
            {"phase_bits": 3, "kerengonen": {"phase_advance": 1}},
            {"kerengonen_phase": "carried"},
            "coherence table",
        ),
        ({"phase_bits": -1}, {}, "phase_bits"),
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
                    "light": {"phase_bits": 8},
                    "matter": {"kerengonen": {"phase_steps": 256, "phase_advance": 13}},
                },
                [light, matter],
                20,
            )
        )
    )
    light_field, matter_field = world.initial.spatial_fields
    assert (light_field.phase_bits, light_field.phase_advance, light_field.kerengonen) == (8, 0, False)
    assert (matter_field.phase_bits, matter_field.phase_advance, matter_field.coherent) == (8, 13, True)
    for tick in range(1, 21):
        world.step()
        stamp = {"steps": tick, "outbound": 1, "event_ports": 1, "event_shares": (4, 0, 0, 0, 0, 0)}
        assert rays_of(world) == {
            (2 + tick, 2, 2): ((Ray(0, (0, 0, 0), 4, phase=77, **stamp),), ()),
            (2 + tick, 3, 3): ((), (Ray(0, (0, 0, 0), 4, phase=MATTER_PHASES[tick - 1], **stamp),)),
        }
        assert MATTER_PHASES[tick - 1] == (77 + 13 * tick) % 256
        assert world.totals() == {"light": (4,), "matter": (4,)}

    # (c) Charge: rays of charge +1 and -1 with amounts 3 and 5 read -2 at every
    # tick, through a meeting that reverses both headings; charge x amount is an
    # invariant of the declared interaction, and an interaction that would change
    # the total charge is rejected at validation.
    assert [field.name for field in RAY_PROPERTIES] == [
        "amount",
        "heading",
        "phase",
        "advance",
        "delay",
        "family",
        "charge",
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
    ) == (-2,)
    assert ray_charge((Ray(0, (0, 0, 0), 3), Ray(1, (0, 0, 0), 4)), initial.spatial_fields[1]) == -7
    world = Simulation(initial)
    assert world.charge_totals() == {"plus": 0, "minus": 0}
    for _tick in range(1, 7):
        world.step()
        assert world.charge_totals() == {"plus": 3, "minus": -5}
        assert sum(world.charge_totals().values()) == -2
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

    # (d) The wide phase: 128 bits, rest rate 2^70 per interval, emission phase
    # 2^128 - 3 x 2^70. A ray walks 100 Links out and 100 back and returns with the
    # phase it left with, exactly; totals exact; about one second.
    wide = {
        "type": "lamp",
        "field": "matter",
        "stock": 2,
        "position": (2, 2, 2),
        "emission": {"heading": PLUS_X, "kerengonen_phase": WIDE_PHASE},
    }
    wide_families = {"matter": {"phase_bits": 128, "kerengonen": {"phase_advance": WIDE_RATE}}}
    raw = document((7, 5, 5), wide_families, [wide], 100)
    initial = parse_initial_state(raw)
    definition = initial.spatial_fields[0]
    assert (definition.phase_bits, definition.phase_modulus, definition.phase_mask) == (
        128,
        WIDE_MODULUS,
        WIDE_MODULUS - 1,
    )
    assert (definition.phase_advance, definition.coherent, definition.kerengonen) == (
        WIDE_RATE,
        False,
        True,
    )
    started = time.perf_counter()
    world = Simulation(initial)
    outbound = {}
    for tick in range(1, 101):
        world.step()
        assert world.totals() == {"matter": (2,)}
        ((ray,), *_) = rays_of(world)[((2 + tick) % 7, 2, 2)]
        assert (ray.steps, ray.outbound, ray.amount) == (tick, 1, 2)
        assert ray.phase == (WIDE_PHASE + tick * WIDE_RATE) % WIDE_MODULUS
        outbound[tick] = ray.phase
    assert outbound[1] == WIDE_MODULUS - (1 << 71) == 340282366920938461102191365996945604608
    assert outbound[2] == WIDE_MODULUS - WIDE_RATE
    assert outbound[3] == 0 and outbound[4] == WIDE_RATE
    assert outbound[100] == 97 * WIDE_RATE == 114517387209588896432128
    assert all(item["balanced"] for item in world.spatial_accounting().values())
    # The walk back (feature 3's return is not on main): the ray reversed on its
    # line with outbound 0 counts its steps and its phase down, one Link at a time.
    returning = replace(ray, outbound=0)
    meter = CostMeter(initial.operation_costs)
    for back in range(1, 101):
        ports, kept = forward_rays((returning,), definition, meter)
        assert kept == () and [len(port) for port in ports] == [1, 0, 0, 0, 0, 0]
        (returning,) = ports[0]
        assert (returning.steps, returning.phase) == (100 - back, outbound.get(100 - back, WIDE_PHASE))
    assert (returning.steps, returning.phase) == (0, WIDE_PHASE)
    with pytest.raises(ValueError, match="event Node"):
        forward_rays((returning,), definition, meter)
    elapsed = time.perf_counter() - started
    assert elapsed < 20, f"the wide-phase case took {elapsed:.2f} s"
    with pytest.raises(ValueError, match="power of two"):
        advance_ray(ray, (1, 0, 0), 12, 1)
    for patch, message in (
        ({"matter": {**wide_families["matter"], "self_exclusion": True}}, "phase_bits at most 30"),
        (
            {"matter": {"phase_bits": 128, "kerengonen": {"phase_steps": 8, "phase_advance": 1}}},
            "2 to the power",
        ),
    ):
        with pytest.raises(ValueError, match=message):
            parse_initial_state(document((7, 5, 5), patch, [wide], 1))
    with pytest.raises(ValueError, match="kerengonen_phase requires"):
        parse_initial_state(
            document(
                (7, 5, 5),
                wide_families,
                [{**wide, "emission": {"heading": PLUS_X, "kerengonen_phase": WIDE_MODULUS}}],
                1,
            )
        )
    meeting = reflect()
    meeting[0]["participants"] = [{"type": "matter"}, {"type": "matter"}]
    with pytest.raises(ValueError, match="phase_bits at most 30"):
        parse_initial_state(document((7, 5, 5), wide_families, [wide], 1, meeting))
    # The runner records the identity beside the ray state and runs the wide world.
    path = tmp_path / "wide.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=100)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["wave_ray"] == WAVE_RAY_FAMILY == "wave-ray-family-v1"
    assert metadata["ray_state"] == "ray-event-state-v1"
    assert metadata["spatial_policy"] == "kerengonen-ray-field-v1"
    assert metadata["conserved_at_every_completed_tick"] and metadata["final_totals"]["matter"] == [2]
    assert metadata["completed_ticks"] == 100
