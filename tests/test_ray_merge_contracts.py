"""Counterexamples at the ownership boundaries shared by the integrated ray policies."""

from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter, bounded, pack, unpack
from event_universe.core.node_boundary import validate_spatial_plan
from event_universe.core.spatial_state import Ray, SpatialPacket, zero_spatial_state
from event_universe.initialization import parse_initial_state

from .test_energy_audit import absorbing_document, document
from .test_kerengonen import two_lamps
from .test_ray_delay import document as delay_document
from .test_ray_integration_guards import _law, _record


@pytest.mark.parametrize("screen_here", [False, True])
def test_load_delay_keeps_funded_slow_emissions_and_allows_resident_absorption(screen_here):
    raw = delay_document(ray_delay=True, emission=0)
    raw["spatial_fields"][0]["pace"] = [1, 4]
    raw["spatial_fields"][1]["baseline"] = 6000
    raw["emissions"][0]["amount"] = 1
    if screen_here:
        raw["seeds"][1]["position"] = raw["seeds"][0]["position"]
    world = Simulation(parse_initial_state(raw))
    for tick in range(1, 4):
        world.step()
        assert world.totals()["quanta"] == (16,)
        if screen_here:
            assert unpack(_record(world, 1).values[0]) == (tick - 1,)


@pytest.mark.parametrize(
    "kept",
    [((Ray(999999, (0, 0, 0), 1),),), ((Ray(0, (0, 0, 0), 1),) * 65,), ((), ())],
)
def test_retained_ray_proposals_are_validated_before_adoption(kept):
    initial = parse_initial_state(document(headings=[[1, 0, 0]], rays_per_tick=1))
    states = (zero_spatial_state(1),)
    plan = _law(initial)(states, (), 0)
    with pytest.raises(ValueError):
        validate_spatial_plan(initial, replace(plan, kept_rays=kept), 0)


def test_maximum_equivalent_euclidean_pace_keeps_wait_in_the_physical_register():
    raw = document(headings=[[1, 0, 0], [1, 1, 1]], rays_per_tick=1, amount=1)
    raw["spatial_fields"][0].update(metric="euclidean", pace=[1073741823, 1073741823])
    world = Simulation(parse_initial_state(raw))
    for _ in range(4):
        world.step()
        for node in world.inventory_view().nodes:
            for rays in node.rays:
                for ray in rays:
                    assert bounded(ray.wait) == ray.wait
    assert world.conservation_report()["status"] == "passed"


def test_pace_is_prepared_before_steps_and_irreducible_overflow_fails_preflight(monkeypatch):
    from event_universe.core import spatial_state

    raw = document(headings=[[1, 0, 0], [1, 1, 1]], rays_per_tick=1, amount=1)
    raw["spatial_fields"][0].update(metric="euclidean", pace=[1073741822, 1073741823])
    with pytest.raises(ValueError, match="integer bound"):
        parse_initial_state(raw)
    raw["spatial_fields"][0]["pace"] = [1, 1]
    world = Simulation(parse_initial_state(raw))

    def reject_preparation(*args):
        pytest.fail("physical stepping prepared a pace law")

    monkeypatch.setattr(spatial_state, "prepare_heading_paces", reject_preparation)
    monkeypatch.setattr(spatial_state, "integer_sqrt", reject_preparation)
    for _ in range(4):
        world.step()


def test_observer_failure_cannot_interrupt_installation_of_held_ray_inventory():
    raw = delay_document(ray_delay=True, emission=0)
    raw["spatial_fields"][0]["pace"] = [1, 4]
    raw["spatial_fields"][1]["baseline"] = 6000
    raw["emissions"][0]["amount"] = 1
    world = Simulation(parse_initial_state(raw))
    world.step()

    def fail_after_commit(event):
        if event["event"] == "spatial_cycle":
            raise RuntimeError("observer failed after commit")

    world._spatial.observer = fail_after_commit
    with pytest.raises(RuntimeError, match="observer failed"):
        world.step()
    assert world.faulted and world.totals()["quanta"] == (16,)


def test_absorbing_the_last_waiting_ray_releases_its_local_delay_counter():
    raw = delay_document(ray_delay=True, emission=0)
    raw["seeds"][1]["position"] = raw["seeds"][0]["position"]
    raw["emissions"][0]["amount"] = 0
    world = Simulation(parse_initial_state(raw))
    position = tuple(raw["seeds"][0]["position"])
    spatial = world._spatial
    node = spatial._at(position)
    node.rays = ((Ray(0, (0, 0, 0), 1),), ())
    node.ray_wait = 3
    node.advance(0, world._nodes[position], spatial._services)
    assert not any(node.rays)
    assert node.ray_wait == 0
    assert unpack(_record(world, 1).values[0]) == (1,)


def test_share_capture_keeps_exact_rational_truncation():
    raw = absorbing_document(headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[1, 0, 0])
    raw["spatial_fields"][0]["kerengonen"] = {"phase_steps": 4, "phase_advance": 0}
    raw["spatial_couplings"][0].update(fraction=1, fraction_denominator=3)
    initial = parse_initial_state(raw)
    residents, records = [Ray(0, (0, 0, 0), 100005)], [_record(Simulation(initial), 1)]
    assert _law(initial)._absorb(0, residents, records, CostMeter(initial.operation_costs)) == 33335
    assert residents == [Ray(0, (0, 0, 0), 66670)]


def test_threshold_capture_cannot_partially_fund_a_negative_ray():
    raw = absorbing_document(
        headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[1, 0, 0], stock=1, signed=True
    )
    raw["spatial_fields"][0]["kerengonen"] = {
        "phase_steps": 4,
        "phase_advance": 0,
        "capture": "threshold",
    }
    initial = parse_initial_state(raw)
    residents, records = [Ray(0, (0, 0, 0), -2)], [_record(Simulation(initial), 1)]
    assert _law(initial)._absorb(0, residents, records, CostMeter(initial.operation_costs)) == 0
    assert residents == [Ray(0, (0, 0, 0), -2)]
    assert unpack(records[0].values[0]) == (1,)


def test_directed_self_exclusion_uses_the_emitted_heading_and_full_ray_identity():
    raw = two_lamps(4, 1)
    raw["spatial_fields"][0].update(self_exclusion=True, rays_per_tick=1)
    raw["emissions"][0]["heading"] = [-1, 0, 0]
    raw["spatial_couplings"][0]["type"] = "lamp_a"
    initial = parse_initial_state(raw)
    record = replace(
        _record(Simulation(initial), 0),
        channel_code=3,
        emission_departed=(pack((4, 0, 0, -1)), pack((0, 0, 0, 0))),
    )
    own = Ray(1, (0, 0, 0), 4, 1)
    foreign = replace(own, advance=2)
    residents, records = [own, foreign], [record]
    taken = _law(initial)._absorb(0, residents, records, CostMeter(initial.operation_costs))
    assert taken == 4 and residents == [own]


@pytest.mark.parametrize("option", ["pace", "metric", "mirror"])
def test_self_exclusion_refuses_compositions_without_a_complete_departure_record(option):
    raw = two_lamps(4, 1)
    raw["spatial_fields"][0]["self_exclusion"] = True
    if option == "mirror":
        raw["emissions"][0]["kerengonen_mirror"] = "x"
    else:
        raw["spatial_fields"][0][option] = {"pace": [1, 2], "metric": "euclidean"}[option]
    with pytest.raises(ValueError, match="self-exclusion"):
        parse_initial_state(raw)


def _ray_receiver():
    raw = document(headings=[[1, 0, 0]], rays_per_tick=1)
    raw["spatial_fields"][0]["ray_slots"] = 2
    world = Simulation(parse_initial_state(raw))
    spatial = world._spatial
    node = spatial._at((2, 2, 2))
    packet = SpatialPacket(10, (1, 2, 2), 0, ((pack((0,)),) * 8,), rays=((Ray(0, (0, 0, 0), 3),),))
    return spatial, node, packet


def test_receipt_validates_the_entire_ray_packet_before_merging_residents():
    spatial, node, packet = _ray_receiver()
    node.rays = ((Ray(0, (0, 0, 0), 2),),)
    before = node.rays
    invalid = replace(packet, rays=((Ray(0, (0, 0, 0), 3), Ray(0, (0, 0, 0), 4, wait=1)),))
    with pytest.raises(ValueError, match="ray wait"):
        node.receive((invalid,), 10, spatial._services)
    assert node.rays == before
    node.receive((packet,), 10, spatial._services)
    # Rays on one line merge on arrival; the slot budget bounds residency, and no
    # occupied-channel rule pushes a ray back or makes it wait for room.
    assert node.rays == ((Ray(0, (0, 0, 0), 5),),)
