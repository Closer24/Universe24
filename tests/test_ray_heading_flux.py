"""Independent carried-heading sampling, causal response and self-exclusion checks."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import (
    MAX_VALUE,
    OPERATIONS,
    CostMeter,
    FieldDefinition,
    OperationCosts,
    pack,
    unpack,
)
from event_universe.core.spatial_state import Ray, SpatialFieldDefinition, zero_spatial_state
from event_universe.fields.spatial_coupling import SpatialCouplingLaw, sample_fluxes
from event_universe.initialization import parse_initial_state


def document(projection="carried_heading"):
    fixture = Path(__file__).resolve().parents[1] / "examples/generic-ray-coupling/field-sampling.json"
    raw = json.loads(fixture.read_text(encoding="utf-8"))
    raw["spatial_fields"][0]["flux_projection"] = projection
    return raw


def projection_input(projection="carried_heading"):
    field = FieldDefinition("radiation", 1, "ray", True, True)
    definition = SpatialFieldDefinition(
        0,
        pack((11,)),
        transport="ray",
        headings=((2, 1, 0), (-2, -1, 0)),
        rays_per_tick=1,
        ray_slots=4,
        flux_projection=projection,
    )
    delivered = (pack((3,)),) + (pack((0,)),) * 5
    state = replace(zero_spatial_state(1), delivered=delivered)
    return field, definition, state


def test_diagonal_heading_survives_a_single_axis_last_hop_and_baseline_has_no_heading():
    field, definition, state = projection_input()
    rays = ((Ray(0, (-1, 1, 0), 3),),)
    assert unpack(sample_fluxes((state,), (definition,), (field,), rays=rays)[0]) == (6, 3, 0)
    ports = replace(definition, flux_projection="ports")
    assert unpack(sample_fluxes((state,), (ports,), (field,), rays=rays)[0]) == (3, 0, 0)
    assert unpack(sample_fluxes((state,), (definition,), (field,), rays=((),))[0]) == (0, 0, 0)


def test_opposite_local_headings_cancel_and_signed_amount_reverses_the_projection():
    field, definition, state = projection_input()
    rays = ((Ray(0, (0, 0, 0), 3), Ray(1, (0, 0, 0), 3)),)
    assert unpack(sample_fluxes((state,), (definition,), (field,), rays=rays)[0]) == (0, 0, 0)
    negative = ((Ray(0, (0, 0, 0), -3),),)
    assert unpack(sample_fluxes((state,), (definition,), (field,), rays=negative)[0]) == (-6, -3, 0)


def test_heading_sampling_rejects_missing_ray_owners_capacity_and_overflow():
    field, definition, state = projection_input()
    with pytest.raises(ValueError, match="ray.*sample|ray.*count"):
        sample_fluxes((state,), (definition,), (field,))
    with pytest.raises(ValueError, match="slot budget"):
        sample_fluxes((state,), (definition,), (field,), rays=((Ray(0, (0, 0, 0), 1),) * 5,))
    with pytest.raises(ValueError, match="integer bound"):
        sample_fluxes((state,), (definition,), (field,), rays=((Ray(0, (0, 0, 0), MAX_VALUE),),))


def test_overflow_rejects_before_changing_the_receiving_ray_or_carrier():
    raw = document()
    raw["emissions"][0]["amount"] = MAX_VALUE // 2 + 1
    world = Simulation(parse_initial_state(raw))
    world.step()
    node = world._spatial.nodes[(5, 4, 4)]
    rays_before = node.rays
    records_before = world.nodes[(5, 4, 4)].records
    with pytest.raises(ValueError, match="integer bound"):
        node.freeze_sample(world._spatial._services)
    assert node.rays == rays_before
    assert world.nodes[(5, 4, 4)].records == records_before


@pytest.mark.parametrize(
    ("projection", "expected"), [("ports", (3, 0, 0)), ("carried_heading", (6, 3, 0))]
)
def test_causal_carrier_response_uses_selected_projection_and_balances_reaction(projection, expected):
    world = Simulation(parse_initial_state(document(projection)))

    def momentum():
        record = next(record for record in world.nodes[(5, 4, 4)].records if record is not None)
        return world.record_values(record)["momentum"]

    world.step()
    assert momentum() == (0, 0, 0)
    world.step()
    assert momentum() == expected
    assert world.spatial_values((5, 4, 4))["momentum"]["value"] == tuple(-value for value in expected)
    assert world.totals()["momentum"] == (0, 0, 0)


def test_same_heading_projection_removes_only_the_departed_local_self_contribution():
    raw = document()
    raw["spatial_fields"][0]["self_exclusion"] = True
    raw["emissions"][0]["type"] = "receiver"
    initial = parse_initial_state(raw)
    world = Simulation(initial)
    record = next(record for record in world.nodes[(5, 4, 4)].records if record is not None)
    record = replace(record, channel_code=2, emission_departed=(pack((3, 0, 0, -1)),))
    law = SpatialCouplingLaw(
        initial.fields,
        initial.spatial_couplings,
        initial.operation_costs,
        initial.spatial_fields,
        emissions=initial.emissions,
    )
    sample = (pack((7,)), pack((0, 0, 0)))
    flux = (pack((14, 7, 0)), pack((0, 0, 0)))
    corrected, projected = law._without_own_rays(
        record, sample, flux, CostMeter(initial.operation_costs)
    )
    assert unpack(corrected[0]) == (4,)
    assert unpack(projected[0]) == (8, 4, 0)
    isolated, zero = law._without_own_rays(
        record,
        (pack((3,)), pack((0, 0, 0))),
        (pack((6, 3, 0)), pack((0, 0, 0))),
        CostMeter(initial.operation_costs),
    )
    assert unpack(isolated[0]) == (0,) and unpack(zero[0]) == (0, 0, 0)


def test_projection_tariff_is_declared_fixed_capacity_work():
    field, definition, state = projection_input()
    costs = OperationCosts((1,) * len(OPERATIONS))
    ports = SpatialCouplingLaw((field,), (), costs, (replace(definition, flux_projection="ports"),))
    headings = SpatialCouplingLaw((field,), (), costs, (definition,))
    sample = (pack((0,)),)
    flux = (pack((0, 0, 0)),)
    assert headings((), sample, flux).cost - ports((), sample, flux).cost == 10 * definition.ray_slots


def test_free_moving_emitter_has_no_response_to_its_coarriving_diagonal_ray():
    raw = document()
    raw["spatial_fields"][0]["self_exclusion"] = True
    raw["emissions"][0]["type"] = "receiver"
    raw["disturbance_types"][1]["transport"] = {"mode": "move", "direction_field": "momentum"}
    raw["seeds"] = [{"position": [2, 4, 4], "type": "receiver", "values": {"momentum": [1, 0, 0]}}]
    world = Simulation(parse_initial_state(raw))
    for _ in range(3):
        world.step()
        records = [
            record for node in world.nodes.values() for record in node.records if record is not None
        ]
        assert len(records) == 1
        assert world.record_values(records[0])["momentum"] == (1, 0, 0)
        assert world.totals()["momentum"] == (1, 0, 0)


@pytest.mark.parametrize("mode", ["unknown", 1])
def test_invalid_projection_is_rejected_at_preflight(mode):
    with pytest.raises((TypeError, ValueError), match="flux_projection"):
        parse_initial_state(document(mode))


def test_projection_requires_ray_transport_and_rejects_port_blind_sampling():
    raw = document()
    raw["spatial_fields"][1]["flux_projection"] = "carried_heading"
    with pytest.raises(ValueError, match="ray transport"):
        parse_initial_state(raw)
    raw = document()
    raw["arrival_port_blind"] = True
    with pytest.raises(ValueError, match="outward spatial fields"):
        parse_initial_state(raw)
