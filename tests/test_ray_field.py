"""Straight-moving ray fields: lines, Gauss shells, receivers, decay, capacity and limits."""

import json
import math

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter, OperationCosts
from event_universe.core.spatial_state import Ray, SpatialFieldDefinition, advance_ray, merge_rays
from event_universe.fields.rays import emit_rays, forward_rays
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

CENTER = 7
SIZE = 15


def golden_headings(count: int, scale: int) -> list[list[int]]:
    """Integer headings spread evenly over the sphere by a golden spiral."""
    ratio = (1 + 5**0.5) / 2
    result = []
    for i in range(count):
        z = 1 - 2 * (i + 0.5) / count
        radius = math.sqrt(1 - z * z)
        angle = 2 * math.pi * i / ratio
        heading = [
            round(scale * radius * math.cos(angle)),
            round(scale * radius * math.sin(angle)),
            round(scale * z),
        ]
        result.append(heading if any(heading) else [scale, 0, 0])
    return result


def document(*, headings=None, rays_per_tick=8, ray_slots=64, strength=64, ticks=6, **extra):
    raw = {
        "schema_version": 1,
        "model_id": "ray-field-test-v1",
        "shape": [SIZE, SIZE, SIZE],
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
                "name": "strength",
                "components": 1,
                "units": "source units",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "radiation",
                "components": 1,
                "units": "ray unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "vector unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "polarity",
                "components": 1,
                "units": "multiplier",
                "signed": True,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "source",
                "fields": ["strength"],
                "defaults": {"strength": strength},
                "transport": {"mode": "hold"},
            },
            {
                "name": "receiver",
                "fields": ["momentum", "polarity"],
                "defaults": {"momentum": [0, 0, 0], "polarity": 1},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "radiation",
                "baseline": 0,
                "transport": "ray",
                "headings": headings if headings is not None else golden_headings(64, 6),
                "rays_per_tick": rays_per_tick,
                "ray_slots": ray_slots,
            },
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "local"},
        ],
        "emissions": [
            {
                "type": "source",
                "field": "radiation",
                "amount": {"field": "strength"},
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [
            {
                "name": "flux_exchange",
                "type": "receiver",
                "field": "momentum",
                "mode": "exchange",
                "amount": {
                    "op": "neg",
                    "args": [{"op": "mul", "args": [{"field": "polarity"}, {"flux": "radiation"}]}],
                },
                "denominator": 1,
            }
        ],
        "seeds": [{"position": [CENTER] * 3, "type": "source"}],
    }
    raw.update(extra)
    return raw


def shell_stock(world, radius):
    total = 0
    for a in range(-radius, radius + 1):
        for b in range(-radius + abs(a), radius - abs(a) + 1):
            for c in {radius - abs(a) - abs(b), -(radius - abs(a) - abs(b))}:
                total += world.spatial_values((CENTER + a, CENTER + b, CENTER + c))["radiation"][
                    "value"
                ][0]
    return total


def meter():
    return CostMeter(OperationCosts((1,) * 9))


@pytest.mark.parametrize("heading", [(2, 1, 0), (3, -1, 2), (0, 0, -4), (5, 5, 5)])
def test_dda_ray_returns_to_its_heading_after_one_period(heading):
    ray = Ray(0, (0, 0, 0), 3)
    position = [0, 0, 0]
    length = sum(abs(v) for v in heading)
    for _ in range(length):
        port, ray = advance_ray(ray, heading)
        position[port // 2] += 1 if port % 2 == 0 else -1
        assert all(-length < a <= length for a in ray.accumulators)
    assert tuple(position) == heading
    assert ray.accumulators == (0, 0, 0)


def test_emission_shares_amount_over_the_next_headings_and_cycles_the_cursor():
    definition = SpatialFieldDefinition(
        0,
        (1,),
        transport="ray",
        headings=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        rays_per_tick=2,
        ray_slots=4,
    )
    rays, cursor = emit_rays(5, 2, definition, meter())
    assert rays == (Ray(2, (0, 0, 0), 3), Ray(0, (0, 0, 0), 2)) and cursor == 1
    # Edge case: an amount smaller than the ray count skips empty rays and keeps the sum.
    rays, cursor = emit_rays(1, 1, definition, meter())
    assert rays == (Ray(1, (0, 0, 0), 1),) and cursor == 0
    ports = forward_rays(rays, definition, meter())
    assert [len(p) for p in ports] == [0, 0, 1, 0, 0, 0]
    assert merge_rays((Ray(1, (0, 0, 0), 1), Ray(1, (0, 0, 0), 2), Ray(1, (1, 0, 0), 1))) == (
        Ray(1, (0, 0, 0), 3),
        Ray(1, (1, 0, 0), 1),
    )


def test_ray_field_conserves_stock_and_puts_one_tick_of_emission_on_every_shell():
    world = Simulation(parse_initial_state(document()))
    initial = world.totals()
    for tick in range(1, 7):
        world.step()
        assert world.totals()["radiation"] == (64 * tick,)
        assert world.source_totals()["radiation"] == (64 * tick,)
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        for radius in range(1, tick + 1):
            assert shell_stock(world, radius) == 64
    values = world.spatial_values((CENTER + 1, CENTER, CENTER))["radiation"]
    assert values["ray_count"] >= 1 and values["value"][0] == sum(
        values["directions"][port][0] for port in range(6)
    )
    assert initial["radiation"] == (0,)


def test_receiver_momentum_follows_the_delivered_ray_flux():
    raw = document(headings=[[1, 0, 0]], rays_per_tick=1, strength=5)
    raw["seeds"].append({"position": [CENTER + 3, CENTER, CENTER], "type": "receiver"})
    world = Simulation(parse_initial_state(raw))
    for _ in range(6):
        world.step()
    record = next(
        r
        for r in world.nodes[(CENTER + 3, CENTER, CENTER)].records
        if r is not None and r.type_index == 1
    )
    # Rays arrive from tick 3; the receiver samples the previous delivery before each cycle.
    assert world.record_values(record)["momentum"] == (15, 0, 0)
    assert world.spatial_values((CENTER + 3, CENTER, CENTER))["radiation"]["value"] == (5,)
    assert world.spatial_values((CENTER + 2, CENTER, CENTER))["radiation"]["value"] == (5,)


@pytest.mark.parametrize("residue", ["localize", "dissipate"])
def test_ray_attenuation_on_completed_links_localizes_or_dissipates(residue):
    raw = document(headings=[[1, 0, 0]], rays_per_tick=1, strength=8, schema_version=2)
    raw["spatial_fields"][0]["decay"] = {
        "retain_numerator": 1,
        "retain_denominator": 2,
        "residue": residue,
    }
    raw["spatial_fields"][1] = {
        "field": "momentum",
        "baseline": [0, 0, 0],
        "transport": "outward",
        "decay": {"retain_numerator": 1, "retain_denominator": 2},
    }
    raw["emissions"][0]["budget"] = 8
    raw["spatial_couplings"] = []
    world = Simulation(parse_initial_state(raw))
    for _ in range(6):
        world.step()
    along = [world.spatial_values((CENTER + k, CENTER, CENTER))["radiation"] for k in range(1, 5)]
    assert [v["value"][0] for v in along] == [0, 0, 0, 0]
    if residue == "localize":
        assert [v["localized"][0] for v in along] == [4, 2, 1, 1]
        assert world.totals()["radiation"] == (8,) and world.dissipation_totals()["radiation"] == (0,)
    else:
        assert world.totals()["radiation"] == (0,) and world.dissipation_totals()["radiation"] == (8,)
    assert all(item["balanced"] for item in world.spatial_accounting().values())


def test_ray_slot_budget_is_an_explicit_failure():
    # Two headings with period three. Sources A and B hit the center every tick at
    # one phase each; source C's ray reaches it at tick 3 with a third phase.
    raw = document(headings=[[2, 1, 0], [1, 2, 0]], rays_per_tick=2, ray_slots=2, strength=2)
    raw["seeds"] = [
        {"position": [CENTER - 1, CENTER, CENTER], "type": "source"},
        {"position": [CENTER, CENTER - 1, CENTER], "type": "source"},
        {"position": [CENTER - 2, CENTER - 1, CENTER], "type": "source"},
    ]
    raw["spatial_couplings"] = []
    world = Simulation(parse_initial_state(raw))
    world.step()
    world.step()
    assert world.spatial_values((CENTER, CENTER, CENTER))["radiation"]["ray_count"] == 2
    with pytest.raises(ValueError, match="ray slot budget exceeded"):
        world.step()


def test_rays_escape_an_open_boundary_and_are_counted():
    raw = document(headings=[[1, 0, 0]], rays_per_tick=1, strength=3, boundary="open", ticks=12)
    raw["spatial_couplings"] = []
    world = Simulation(parse_initial_state(raw))
    for _ in range(12):
        world.step()
    # A ray emitted at tick t sits at distance t; the last interior node is 7 links out.
    assert world.escaped_totals()["radiation"] == (3 * (12 - CENTER),)
    assert world.totals()["radiation"] == (3 * CENTER,)
    assert all(item["balanced"] for item in world.spatial_accounting().values())


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda raw: raw["spatial_fields"][0].pop("headings"), "requires keys"),
        (lambda raw: raw["spatial_fields"][0].update(headings=[[0, 0, 0]]), "zero vector"),
        (lambda raw: raw["spatial_fields"][0].update(rays_per_tick=65), "rays_per_tick"),
        (lambda raw: raw["spatial_fields"][0].update(octant_weights=[1] * 8), "axis or octant"),
        (lambda raw: raw["spatial_fields"][1].update(headings=[[1, 0, 0]]), "require ray transport"),
        (
            lambda raw: raw.update(
                spatial_seeds=[
                    {"position": [1, 1, 1], "field": "radiation", "populations": [1] + [0] * 7}
                ]
            ),
            "no octant seeds",
        ),
        (lambda raw: raw.update(spatial_computation_delay=True), "fixed field clock"),
        (lambda raw: raw["spatial_fields"][0].update(field="momentum"), "scalar field"),
    ],
)
def test_ray_configuration_limits_are_rejected(change, message):
    raw = document()
    change(raw)
    with pytest.raises(ValueError, match=message):
        parse_initial_state(raw)


def test_runner_records_the_ray_identity(tmp_path):
    raw = document(ticks=4)
    path = tmp_path / "rays.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=4)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["spatial_policy"] == "isotropic-ray-field-v1"
    assert metadata["spatial_transport"] == "straight-rays"
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["final_totals"]["radiation"] == [256]
