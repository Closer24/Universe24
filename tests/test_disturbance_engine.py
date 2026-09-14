"""Independent timing, locality and ownership contracts for generic disturbances."""

from dataclasses import FrozenInstanceError

import pytest

from event_universe.core.disturbance_engine import cycle_timing
from event_universe.core.disturbance_state import CostMeter, decode, unpack
from event_universe.disturbance_api import Simulation
from event_universe.fields.disturbances import evaluate
from event_universe.initialization import parse_initial_state

from .support.disturbances import document, field, kind


def resident_values(world, position):
    if position not in world.nodes:
        return []
    return [world.record_values(r) for r in world.nodes[position].records if r is not None]


def exchange_document(amount, denominator=1):
    kinds = [kind("left", values={"inventory": 0}), kind("right", values={"inventory": 0})]
    return document(
        kinds,
        [((2, 2, 2), "left"), ((2, 2, 2), "right")],
        couplings=[
            {
                "name": "local_exchange",
                "left_type": "left",
                "right_type": "right",
                "field": "inventory",
                "amount": amount,
                "denominator": denominator,
            }
        ],
    )


def meeting_document(capacity=4):
    return document(
        [
            kind("east", mode="move", weights=[1, 0, 0, 0, 0, 0]),
            kind("west", mode="move", weights=[0, 1, 0, 0, 0, 0]),
        ],
        [((0, 0, 0), "east"), ((2, 0, 0), "west")],
        capacity=capacity,
    )


@pytest.mark.parametrize(
    ("cost", "expected"),
    [(0, (0, 3)), (9, (0, 3)), (10, (0, 3)), (11, (3, 6)), (20, (3, 6)), (21, (6, 9))],
)
def test_normal_budget_boundary_adds_only_local_wait(cost, expected):
    assert cycle_timing(cost, 10, 3) == expected


@pytest.mark.parametrize(("budget", "first_arrival"), [(4, 3), (3, 6)])
def test_fixed_link_time_and_no_same_tick_relay(budget, first_arrival):
    events = []
    initial = parse_initial_state(
        document(
            [kind("traveler", mode="move", weights=[1, 0, 0, 0, 0, 0])],
            [((0, 0, 0), "traveler")],
            budget=budget,
            travel=3,
        )
    )
    world = Simulation(initial, observer=events.append)
    # One read, route, send and commit cost four units at the origin.
    for _ in range(first_arrival - 1):
        world.step()
        assert resident_values(world, (1, 0, 0)) == []
        assert world.totals() == {"inventory": (1,)}
    world.step()
    assert resident_values(world, (1, 0, 0)) == [{"inventory": (1,)}]
    assert resident_values(world, (2, 0, 0)) == []
    received = [e for e in events if e["event"] == "received"]
    assert len(received) == 1 and received[0]["tick"] == first_arrival
    for _ in range(2):
        world.step()
        assert resident_values(world, (2, 0, 0)) == []


def test_next_cycle_has_fresh_cost_without_carried_computation_debt():
    events = []
    world = Simulation(
        parse_initial_state(
            document(
                [
                    kind("moving", mode="move", weights=[1, 0, 0, 0, 0, 0]),
                    kind("resident"),
                ],
                [((0, 0, 0), "moving"), ((0, 0, 0), "resident")],
                budget=4,
            )
        ),
        observer=events.append,
    )
    for _ in range(3):
        world.step()
    starts = [e for e in events if e["event"] == "cycle_started" and e["position"] == (0, 0, 0)]
    assert [(e["tick"], e["cost"], e["ready_tick"], e["next_tick"]) for e in starts] == [
        (0, 6, 1, 2),
        (2, 3, 2, 3),
    ]
    assert world.totals() == {"inventory": (2,)}


def test_zero_state_still_activates_a_configured_local_coupling():
    world = Simulation(parse_initial_state(exchange_document(1)))
    world.step()
    assert resident_values(world, (2, 2, 2)) == [
        {"inventory": (-1,)},
        {"inventory": (1,)},
    ]
    assert world.totals() == {"inventory": (0,)}


def test_fractional_signed_exchange_is_mirrored_and_keeps_subunit_remainders():
    positive = Simulation(parse_initial_state(exchange_document(1, 4)))
    negative = Simulation(parse_initial_state(exchange_document(-1, 4)))
    for tick in range(1, 5):
        positive.step()
        negative.step()
        p = [item["inventory"][0] for item in resident_values(positive, (2, 2, 2))]
        n = [item["inventory"][0] for item in resident_values(negative, (2, 2, 2))]
        assert n == [-value for value in p]
        assert p == ([0, 0] if tick < 4 else [-1, 1])
        assert positive.totals() == negative.totals() == {"inventory": (0,)}


def test_departed_pair_remainder_is_not_inherited_by_the_next_slot_occupant():
    raw = exchange_document(1, 3)
    raw["disturbance_types"][0]["defaults"]["inventory"] = 10
    moving = raw["disturbance_types"][1]
    moving["defaults"]["inventory"] = 1
    moving["transport"] = {
        "mode": "move",
        "weights": [1, 0, 0, 0, 0, 0],
        "rate": 1,
        "rate_denominator": 2,
    }
    raw["seeds"].append({"position": [1, 2, 2], "type": "right"})
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert sum(decode(code) for code in world.nodes[(2, 2, 2)].coupling_remainders) == 1
    world.step()
    # The old right participant leaves; a distinct one enters the vacated slot.
    assert all(code == 1 for code in world.nodes[(2, 2, 2)].coupling_remainders)
    world.step()
    assert resident_values(world, (2, 2, 2)) == [{"inventory": (10,)}, {"inventory": (1,)}]
    assert world.totals() == {"inventory": (12,)}


def test_coupling_overflow_rejects_both_sides_before_mutating_records():
    from event_universe.core.disturbance_state import MAX_VALUE

    raw = exchange_document(1)
    raw["disturbance_types"][1]["defaults"]["inventory"] = MAX_VALUE
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert world.snapshot() == before
    assert world.totals() == {"inventory": (MAX_VALUE,)}
    assert world.faulted


def test_expression_sum_checks_intermediate_overflow_before_cancellation():
    expression = {
        "op": "sum",
        "args": [
            {
                "op": "mul",
                "args": [
                    {
                        "op": "mul",
                        "args": [[1000000000, 1000000000, -1000000000], 1000000000],
                    },
                    9,
                ],
            }
        ],
    }
    initial = parse_initial_state(exchange_document(expression))
    # Final sum fits 64 bits, but the first two components total 18e18.
    with pytest.raises(OverflowError):
        evaluate(
            initial.couplings[0].amount,
            initial.seeds[0].record.values,
            initial.seeds[1].record.values,
            CostMeter(initial.operation_costs),
        )


def test_signed_stream_payload_uses_same_faces_for_both_signs():
    worlds = []
    for value in (1, -1):
        world = Simulation(
            parse_initial_state(
                document(
                    [
                        kind(
                            "stream",
                            mode="split",
                            values={"inventory": value},
                            weights=[1, 1, 0, 0, 0, 0],
                        )
                    ],
                    [((2, 2, 2), "stream")],
                )
            )
        )
        world.step()
        worlds.append(world)
    assert resident_values(worlds[0], (3, 2, 2)) == [{"inventory": (1,)}]
    assert resident_values(worlds[1], (3, 2, 2)) == [{"inventory": (-1,)}]
    assert resident_values(worlds[0], (1, 2, 2)) == []
    assert resident_values(worlds[1], (1, 2, 2)) == []


def test_opposite_stream_channels_remain_distinct_at_a_shared_neighbor():
    raw = document(
        [
            kind(
                "stream",
                mode="split",
                values={"inventory": 2},
                weights=[1, 1, 0, 0, 0, 0],
            )
        ],
        [((0, 0, 0), "stream")],
    )
    raw["shape"] = [2, 1, 1]
    world = Simulation(parse_initial_state(raw))
    world.step()
    records = [r for r in world.nodes[(1, 0, 0)].records if r is not None]
    assert len(records) == 2
    assert {r.channel_code for r in records} == {2, 3}
    assert [world.record_values(r) for r in records] == [{"inventory": (1,)}, {"inventory": (1,)}]
    assert world.totals() == {"inventory": (2,)}


def test_signed_scalar_and_vector_inventory_survive_waits_splits_and_transit():
    world = Simulation(
        parse_initial_state(
            document(
                [
                    kind(
                        "stream",
                        mode="split",
                        values={"inventory": -5, "components": [3, -2, 1]},
                        weights=[2, 0, 1, 0, 0, 0],
                    )
                ],
                [((2, 2, 2), "stream")],
                fields=[field(), field("components", 3)],
                budget=3,
                travel=2,
            )
        )
    )
    waiting_seen = transit_seen = False
    for _ in range(40):
        world.step()
        assert world.totals() == {"inventory": (-5,), "components": (3, -2, 1)}
        assert world.source_totals() == {"inventory": (0,), "components": (0, 0, 0)}
        waiting_seen |= any(node.pending is not None for node in world.nodes.values())
        transit_seen |= any(p is not None for packets in world.links.values() for p in packets)
    assert waiting_seen and transit_seen


def test_whole_record_movement_preserves_extensive_and_intensive_values_together():
    world = Simulation(
        parse_initial_state(
            document(
                [
                    kind(
                        "bundle",
                        mode="move",
                        values={"inventory": 5, "signed_inventory": -2, "direction": [2, -1, 3]},
                        weights=[1, 0, 0, 0, 0, 0],
                    )
                ],
                [((2, 2, 2), "bundle")],
                fields=[
                    field(signed=False),
                    field("signed_inventory"),
                    field("direction", 3, conserved=False, extensive=False),
                ],
                travel=2,
            )
        )
    )
    expected = {"inventory": (5,), "signed_inventory": (-2,), "direction": (2, -1, 3)}
    world.step()
    assert resident_values(world, (2, 2, 2)) == []
    packets = [p for group in world.links.values() for p in group if p is not None]
    assert len(packets) == 1 and world.record_values(packets[0].record) == expected
    world.step()
    assert resident_values(world, (3, 2, 2)) == [expected]
    assert world.totals() == {"inventory": (5,), "signed_inventory": (-2,)}


def test_incoming_records_wait_without_rewriting_a_frozen_local_proposal():
    update = {
        "field": "inventory",
        "source": True,
        "expression": {
            "op": "add",
            "args": [{"op": "add", "args": [{"field": "inventory"}, 1]}, 0],
        },
    }
    world = Simulation(
        parse_initial_state(
            document(
                [
                    kind("busy", values={"inventory": 10}, updates=[update]),
                    kind(
                        "incoming",
                        mode="move",
                        values={"inventory": 5},
                        weights=[1, 0, 0, 0, 0, 0],
                    ),
                ],
                [((2, 2, 2), "busy"), ((1, 2, 2), "incoming")],
                budget=4,
                capacity=2,
            )
        )
    )
    world.step()
    assert resident_values(world, (2, 2, 2)) == [{"inventory": (10,)}, {"inventory": (5,)}]
    assert world.nodes[(2, 2, 2)].pending.ready_tick == 2
    assert world.totals() == {"inventory": (15,)}
    world.step()
    assert resident_values(world, (2, 2, 2)) == [{"inventory": (11,)}, {"inventory": (5,)}]
    assert world.totals() == {"inventory": (16,)}
    assert world.source_totals() == {"inventory": (1,)}


def test_receiver_capacity_failure_keeps_every_undelivered_packet_owned_once():
    world = Simulation(parse_initial_state(meeting_document(capacity=1)))
    with pytest.raises(ValueError, match="receiving capacity"):
        world.step()
    assert world.faulted
    assert resident_values(world, (1, 0, 0)) == []
    assert world.totals() == {"inventory": (2,)}
    assert sum(p is not None for packets in world.links.values() for p in packets) == 2
    with pytest.raises(RuntimeError, match="cannot continue"):
        world.step()


def test_observer_failure_cannot_split_one_local_arrival_ownership_commit():
    def fail_on_receive(event):
        if event["event"] == "received":
            raise RuntimeError("diagnostic output failed")

    world = Simulation(parse_initial_state(meeting_document()), observer=fail_on_receive)
    with pytest.raises(RuntimeError, match="diagnostic output failed"):
        world.step()
    assert world.faulted
    assert world.totals() == {"inventory": (2,)}
    assert resident_values(world, (1, 0, 0)) == [{"inventory": (1,)}, {"inventory": (1,)}]
    assert all(p is None for packets in world.links.values() for p in packets)


def test_public_nodes_and_nested_records_cannot_mutate_physical_state():
    world = Simulation(parse_initial_state(exchange_document(1)))
    nodes = world.nodes
    node = nodes[(2, 2, 2)]
    with pytest.raises(TypeError):
        nodes[(2, 2, 2)] = node
    with pytest.raises((FrozenInstanceError, AttributeError)):
        node.available_tick = 100
    with pytest.raises((FrozenInstanceError, AttributeError)):
        node.records = (None,) * len(node.records)
    with pytest.raises((FrozenInstanceError, AttributeError)):
        node.records[0].values = ()
    world.step()
    assert unpack(node.records[0].values[0]) == (0,)
    assert resident_values(world, (2, 2, 2))[0] == {"inventory": (-1,)}


def test_diagnostic_snapshot_is_detached_from_engine_state():
    world = Simulation(parse_initial_state(exchange_document(1)))
    snapshot = world.snapshot()
    snapshot["nodes"][0]["disturbances"][0]["values"]["inventory"] = (123,)
    snapshot["nodes"].clear()
    assert resident_values(world, (2, 2, 2)) == [{"inventory": (0,)}, {"inventory": (0,)}]
    world.step()
    assert world.totals() == {"inventory": (0,)}
