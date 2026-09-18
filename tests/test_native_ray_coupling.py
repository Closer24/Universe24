"""Independent ownership, timing and error controls for the complete-ray adapter."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import (
    CostMeter,
    DisturbanceRecord,
    Expression,
    Invariant,
    pack,
)
from event_universe.core.spatial_state import Ray, SpatialCouplingDefinition, merge_rays, validate_rays
from event_universe.fields.disturbances import DisturbanceLaw, interact_values
from event_universe.fields.ray_interactions import apply_ray_interactions
from event_universe.fields.spatial_plan import SpatialLaw
from event_universe.initialization import parse_initial_state

FIXTURE = Path(__file__).resolve().parents[1] / "examples/generic-ray-coupling/finite-residence.json"
CENTER = (5, 3, 3)


def document():
    return json.loads(FIXTURE.read_text())


def apply(initial, rays, rules=None):
    meter = CostMeter(initial.operation_costs)
    return apply_ray_interactions(
        (rays,),
        initial.spatial_fields,
        initial.fields,
        initial.ray_interactions if rules is None else rules,
        meter,
        initial.operation_costs,
    )[0]


def residents(world):
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`); this module pins lines and events, not identities (test_bit_law does).
    return tuple(
        (position, replace(ray, owner=0))
        for position, node in sorted(world._spatial.nodes.items())
        for bundle in node.rays
        for ray in bundle
    )


def test_funded_actual_rays_reside_two_intervals_then_release_with_fixed_h():
    world = Simulation(parse_initial_state(document()))
    for tick, phase, delay in ((1, 0, 0), (2, 1, 1), (3, 2, 0)):
        world.step()
        actual = residents(world)
        assert world.tick == tick
        assert len(actual) == 2
        assert {position for position, _ in actual} == {CENTER}
        assert {(ray.phase, ray.interaction_delay) for _, ray in actual} == {(phase, delay)}
        assert world.totals() == {"wave": (10,), "momentum": (0, 0, 0)}
        assert world.conservation_report()["status"] == "passed"
        assert all(
            world.record_values(record)["momentum"] == (0, 0, 0)
            for node in world.nodes.values()
            for record in node.records
            if record is not None
        )
        assert CENTER in world._spatial._active
    world.step()
    assert {(p, r.phase, r.interaction_delay) for p, r in residents(world)} == {
        ((4, 3, 3), 3, 0),
        ((6, 3, 3), 3, 0),
    }
    assert world.totals() == {"wave": (10,), "momentum": (0, 0, 0)}
    for _ in range(8):
        world.step()
    assert not residents(world)


@pytest.mark.parametrize("control", ["absent", "phase", "unequal", "missing"])
def test_no_admitted_coupling_does_not_hold_rays(control):
    doc = document()
    if control == "absent":
        doc["ray_interactions"] = []
    elif control == "phase":
        for emission in doc["emissions"]:
            emission["kerengonen_phase"] = 0
    elif control == "unequal":
        doc["disturbance_types"][1]["defaults"]["wave"] = 3
    else:
        doc["seeds"].pop()
    world = Simulation(parse_initial_state(doc))
    world.step()
    world.step()
    actual = residents(world)
    assert actual
    assert all(position != CENTER and ray.interaction_delay == 0 for position, ray in actual)


def test_common_swap_preserves_complete_metadata_and_resets_changed_line():
    initial = parse_initial_state(document())
    rays = (Ray(0, (1, 0, 0), 5, advance=3), Ray(1, (0, 1, 0), 5, advance=5))
    updated = apply(initial, rays)
    # The interaction is one event on -X and one on +X: both outputs carry that
    # mask and the amount per Port, as fresh trajectories (ray-event-state-v1).
    event = {"event_ports": 0b000011, "event_shares": (5, 5, 0, 0, 0, 0)}
    assert updated == (
        replace(rays[0], heading=1, accumulators=(0, 0, 0), interaction_delay=2, **event),
        replace(rays[1], heading=0, accumulators=(0, 0, 0), interaction_delay=2, **event),
    )
    assert rays[0].heading == 0 and rays[1].heading == 1


def test_later_group_invariant_failure_produces_no_partial_ray_proposal():
    initial = parse_initial_state(document())
    rule = replace(initial.ray_interactions[0], when=Expression("literal", literal=(1,)))
    rays = (
        Ray(0, (0, 0, 0), 5, advance=1),
        Ray(1, (0, 0, 0), 5, advance=2),
        Ray(0, (0, 0, 0), 5, advance=3),
        Ray(1, (0, 0, 0), 3, advance=4),
    )
    frozen = tuple(rays)
    with pytest.raises(ValueError, match="invariant momentum"):
        apply(initial, rays, (rule,))
    assert rays == frozen
    assert all(ray.interaction_delay == 0 for ray in rays)


def test_invalid_native_phase_rejects_complete_proposal():
    doc = document()
    doc["ray_interactions"][0]["assignments"].append(
        {"participant": 1, "field": "phase", "expression": 8}
    )
    initial = parse_initial_state(doc)
    rays = (Ray(0, (0, 0, 0), 5), Ray(1, (0, 0, 0), 5))
    with pytest.raises(ValueError, match="ray phase"):
        apply(initial, rays)
    assert all(ray.phase == 0 and ray.interaction_delay == 0 for ray in rays)


def test_delay_is_part_of_merge_identity_and_has_bounded_integer_validation():
    initial = parse_initial_state(document())
    ray = Ray(0, (0, 0, 0), 5)
    delayed = replace(ray, interaction_delay=1)
    assert merge_rays((ray, delayed)) == (ray, delayed)
    assert merge_rays((delayed, delayed)) == (replace(delayed, amount=10),)
    for invalid in (-1, True, 1_073_741_824):
        with pytest.raises(ValueError):
            validate_rays(
                (replace(ray, interaction_delay=invalid),), initial.spatial_fields[0], initial.fields[0]
            )


def test_delayed_owner_is_not_reselected_and_each_owner_fires_once():
    initial = parse_initial_state(document())
    delayed = Ray(0, (0, 0, 0), 5, interaction_delay=1)
    partner = Ray(1, (0, 0, 0), 5)
    assert apply(initial, (delayed, partner)) == (delayed, partner)
    first = initial.ray_interactions[0]
    second = replace(first, name="second", when=Expression("literal", literal=(1,)))
    rays = (replace(delayed, interaction_delay=0), partner)
    assert apply(initial, rays, (first, second)) == apply(initial, rays, (first,))


def test_unchanged_vector_preserves_duplicate_heading_index_and_dda():
    doc = document()
    doc["spatial_fields"][0]["headings"].insert(1, [1, 0, 0])
    rule = doc["ray_interactions"][0]
    rule["assignments"] = [item for item in rule["assignments"] if item["field"] == "delay"]
    initial = parse_initial_state(doc)
    rays = (Ray(1, (1, 0, 0), 5), Ray(2, (0, 1, 0), 5))
    assert apply(initial, rays) == tuple(
        replace(ray, interaction_delay=2, event_ports=0b000011, event_shares=(5, 5, 0, 0, 0, 0))
        for ray in rays
    )


@pytest.mark.parametrize("unsupported", ["absorb", "routing"])
def test_direct_spatial_law_keeps_native_coupling_admission(unsupported):
    initial = parse_initial_state(document())
    options = {"ray_interactions": initial.ray_interactions}
    definitions = initial.spatial_fields
    if unsupported == "absorb":
        options["absorptions"] = (
            SpatialCouplingDefinition("capture", 0, 0, "absorb", Expression("literal", literal=(1,))),
        )
    elif unsupported == "routing":
        options["least_delay_direction"] = "along"
    with pytest.raises(ValueError, match="ray interactions"):
        SpatialLaw(initial.fields, definitions, initial.emissions, initial.operation_costs, **options)


@pytest.mark.parametrize(
    "change",
    [
        {"link_ticks": 2},
        {"node_execution": True},
        {"spatial_computation_delay": True},
    ],
)
def test_typed_and_json_callers_reject_unsupported_clock_compositions(change):
    initial = parse_initial_state(document())
    with pytest.raises(ValueError):
        replace(initial, **change)
    doc = document()
    doc.update(change)
    with pytest.raises(ValueError):
        parse_initial_state(doc)


def test_local_direct_caller_rejects_unsupported_heading_domain():
    initial = parse_initial_state(document())
    definitions = (replace(initial.spatial_fields[0], headings=((2, 0, 0), (-2, 0, 0))),)
    with pytest.raises(ValueError, match="unit-axial"):
        apply_ray_interactions(
            ((Ray(0, (0, 0, 0), 5),),),
            definitions,
            initial.fields,
            initial.ray_interactions,
            CostMeter(initial.operation_costs),
            initial.operation_costs,
        )


@pytest.mark.parametrize(
    "key,value", [("ray_slots", 33), ("self_exclusion", True), ("metric", "euclidean")]
)
def test_unsupported_ray_domains_reject_before_run(key, value):
    doc = document()
    doc["spatial_fields"][0][key] = value
    with pytest.raises(ValueError):
        parse_initial_state(doc)


def test_labels_select_properties_without_changing_the_active_trace():
    plain = document()
    renamed = json.loads(
        json.dumps(plain)
        .replace('"wave"', '"__proto__"')
        .replace('"left_source"', '"heading"')
        .replace('"right_source"', '"phase"')
    )
    renamed["disturbance_types"].reverse()
    worlds = [Simulation(parse_initial_state(doc)) for doc in (plain, renamed)]
    for _ in range(5):
        for world in worlds:
            world.step()
        assert residents(worlds[0]) == residents(worlds[1])
        assert tuple(node.last_cost for _, node in sorted(worlds[0].nodes.items())) == tuple(
            node.last_cost for _, node in sorted(worlds[1].nodes.items())
        )


def test_existing_carrier_false_guard_remains_the_original_noop():
    initial = parse_initial_state(document())
    kind = replace(
        initial.disturbances[0], checks=(Invariant("unselected", Expression("literal", literal=(0,))),)
    )
    rule = replace(initial.ray_interactions[0], when=Expression("literal", literal=(0,)))
    records = (DisturbanceRecord(0, (pack((5,)),), (pack((0,)),)),) * 2
    law = DisturbanceLaw(initial.fields, (kind,), (), initial.operation_costs)
    meter = CostMeter(initial.operation_costs)
    assert law._interact_group(rule, records, meter) is records
    assert meter.total == 1 and meter.interaction_ticks == 0


def test_native_ray_json_does_not_admit_the_carrier_conversion_output_form():
    # A meeting with outputs (ray-meeting-conversion-v1) assigns through its
    # outputs, each a ray field with an amount and a heading, never a carrier type.
    doc = document()
    doc["ray_interactions"][0]["outputs"] = [{"type": "wave"}]
    with pytest.raises(ValueError, match="assigns through its outputs"):
        parse_initial_state(doc)
    del doc["ray_interactions"][0]["assignments"]
    with pytest.raises(ValueError, match="ray meeting output has unknown keys: type"):
        parse_initial_state(doc)


@pytest.mark.parametrize("entry", ["initial_state", "local_law", "local_apply"])
def test_native_ray_typed_entries_reject_malformed_meeting_outputs(entry):
    initial = parse_initial_state(document())
    # One declared output while the assignments address two participants.
    rule = replace(initial.ray_interactions[0], outputs=(0,))
    rays = (Ray(0, (0, 0, 0), 5), Ray(1, (0, 0, 0), 5))
    with pytest.raises(ValueError, match="address its declared outputs"):
        if entry == "initial_state":
            replace(initial, ray_interactions=(rule,))
        elif entry == "local_law":
            SpatialLaw(
                initial.fields,
                initial.spatial_fields,
                initial.emissions,
                initial.operation_costs,
                ray_interactions=(rule,),
            )
        else:
            apply(initial, rays, (rule,))
    assert all(ray.interaction_delay == 0 for ray in rays)


@pytest.mark.parametrize("conversion", [{"outputs": (0,)}, {"output_types": (0, 0)}])
def test_shared_same_owner_evaluator_rejects_conversion_before_work(conversion):
    initial = parse_initial_state(document())
    rule = replace(initial.ray_interactions[0], **conversion)
    before = ((pack((5,)), pack((0, 0, 0))),) * 2
    meter = CostMeter(initial.operation_costs)
    with pytest.raises(ValueError, match="family conversion outputs"):
        interact_values(rule, before, initial.fields, meter, initial.operation_costs)
    assert meter.total == 0 and meter.interaction_ticks == 0
    assert before == ((pack((5,)), pack((0, 0, 0))),) * 2
