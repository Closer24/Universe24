"""Port ownership, frozen joint commits and failed admission remain local."""

from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import Packet, unpack
from event_universe.core.register_contracts import PortState, ReadyBatch, WakeIntent
from event_universe.core.register_node import PortExecutionNode
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.initialization import parse_initial_state


def joint_document():
    return {
        "schema_version": 1,
        "node_execution": True,
        "model_id": "register-atomic-exchange-control-v1",
        "shape": [6, 6, 6],
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 10000,
        "ticks": 4,
        "operation_costs": dict.fromkeys(
            ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit"),
            1,
        ),
        "fields": [
            {
                "name": "amount",
                "components": 1,
                "units": "unit",
                "signed": False,
                "conserved": True,
                "aggregation": "sum",
            }
        ],
        "disturbance_types": [
            {
                "name": name,
                "fields": ["amount"],
                "defaults": {"amount": amount},
                "transport": {"mode": "hold"},
            }
            for name, amount in (("first", 2), ("second", 5))
        ],
        "seeds": [{"position": [0, 1, 1], "type": "first"}, {"position": [1, 0, 1], "type": "second"}],
        "interactions": [
            {
                "name": "one_local_swap",
                "left_type": "first",
                "right_type": "second",
                "k": 2,
                "when": {
                    "op": "gt",
                    "args": [{"field": "amount", "side": "right"}, {"field": "amount", "side": "left"}],
                },
                "assignments": [
                    {
                        "side": "left",
                        "field": "amount",
                        "expression": {"field": "amount", "side": "right"},
                    },
                    {
                        "side": "right",
                        "field": "amount",
                        "expression": {"field": "amount", "side": "left"},
                    },
                ],
                "invariants": [
                    {
                        "name": "sum",
                        "expression": {
                            "op": "add",
                            "args": [
                                {"field": "amount", "side": "left"},
                                {"field": "amount", "side": "right"},
                            ],
                        },
                    }
                ],
            }
        ],
        "conservation_contract": {
            "name": "quantity",
            "quantities": [
                {
                    "name": "amount",
                    "components": 1,
                    "units": "unit",
                    "carriers": [{"requires": ["amount"], "value": {"field": "amount"}}],
                }
            ],
        },
    }


def test_two_register_inputs_freeze_and_commit_one_joint_transaction(tmp_path):
    initial = parse_initial_state(joint_document())
    events = []
    with Simulation(replace(initial, seeds=()), observer=events.append) as world:
        node = world._at((1, 1, 1))
        local = PortExecutionNode(node, world._services)
        assert len(local.ports) == 6
        assert local.bootstrap().wakes == ()
        packets = tuple(
            Packet(1, seed.position, port, seed.record)
            for seed, port in zip(initial.seeds, (0, 2), strict=True)
        )
        admitted = local.receive(
            (ReadyBatch(1, "arrival", packets[:1]), ReadyBatch(3, "arrival", packets[1:])), 1
        )
        local.acknowledge_receipt(admitted, 1)
        assert local.ports[1].slots == (0,)
        assert local.ports[3].slots == (1,)
        frames = [world.snapshot()]
        result = local.ready((ReadyBatch(1, "compute"), ReadyBatch(3, "compute")), 1)
        assert result.wakes == (WakeIntent(1, "commit", 3),)
        assert [unpack(record.values[0]) for record in node.records] == [(2,), (5,)]
        assert local.ports[1].locked_slots == (0,)
        assert local.ports[3].locked_slots == (1,)
        assert [event["event"] for event in events].count("cycle_started") == 1
        frames.append(world.snapshot())
        # No owner changes while the two-tick local transaction waits.
        assert node.pending.ready_tick == 3
        with pytest.raises(ValueError, match="only one grouped"):
            local.ready((ReadyBatch(1, "compute"),), 1)
        result = local.ready((ReadyBatch(1, "commit"),), 3)
        assert result.committed
        assert [unpack(record.values[0]) for record in node.records] == [(5,), (2,)]
        assert all(not register.locked_slots for register in local.ports)
        assert [event["event"] for event in events].count("cycle_committed") == 1
        assert sum(unpack(record.values[0])[0] for record in node.records) == 7
        frames.append(world.snapshot())
        render_disturbances(
            frames,
            tmp_path / "joint-register-transaction.html",
            {"scope": "isolated local owner calls", "clock": [1, 1, 3]},
        )


def test_failed_admission_keeps_both_owners_and_register_metadata(tmp_path):
    initial = parse_initial_state(joint_document())
    with Simulation(replace(initial, seeds=())) as world:
        node = world._at((1, 1, 1))
        local = PortExecutionNode(node, world._services)
        first = Packet(1, (0, 1, 1), 0, initial.seeds[0].record)
        wrong = Packet(1, (5, 5, 5), 2, initial.seeds[1].record)
        before = node.records, local.ports
        with pytest.raises(ValueError, match="addressed to another Node"):
            local.receive((ReadyBatch(1, "arrival", (first,)), ReadyBatch(3, "arrival", (wrong,))), 1)
        assert (node.records, local.ports) == before
        assert first.record is initial.seeds[0].record and wrong.record is initial.seeds[1].record
        render_disturbances(
            [world.snapshot()],
            tmp_path / "rejected-register-admission.html",
            {"scope": "rejected isolated admission"},
        )


def test_failed_local_arithmetic_does_not_commit_one_side(tmp_path):
    raw = joint_document()
    raw["interactions"][0]["assignments"][0]["expression"] = {
        "op": "add",
        "args": [{"field": "amount", "side": "left"}, 1073741823],
    }
    initial = parse_initial_state(raw)
    with Simulation(replace(initial, seeds=())) as world:
        local = PortExecutionNode(world._at((1, 1, 1)), world._services)
        packets = tuple(
            Packet(1, seed.position, port, seed.record)
            for seed, port in zip(initial.seeds, (0, 2), strict=True)
        )
        local.receive(
            (ReadyBatch(1, "arrival", packets[:1]), ReadyBatch(3, "arrival", packets[1:])),
            1,
        )
        before = local.node.records, local.ports
        with pytest.raises(ValueError, match="integer bound"):
            local.ready((ReadyBatch(1, "compute"), ReadyBatch(3, "compute")), 1)
        assert (local.node.records, local.ports) == before
        assert local.node.pending is None
        assert all(packet is None for packet in local.node.output.packets)
        render_disturbances(
            [world.snapshot()],
            tmp_path / "rejected-local-arithmetic.html",
            {"scope": "rejected local overflow preserves both input owners"},
        )


def test_seed_port_and_portbank_are_single_owners(tmp_path):
    raw = joint_document()
    raw.pop("interactions")
    raw["disturbance_types"][0]["transport"] = {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]}
    raw["seeds"] = raw["seeds"][:1]
    with Simulation(parse_initial_state(raw)) as world:
        node = world._nodes[(0, 1, 1)]
        local = PortExecutionNode(node, world._services)
        assert local.ports[0].slots == (0,)
        frames = [world.snapshot()]
        result = local.ready((ReadyBatch(0, "compute"),), 0)
        assert len(result.outgoing) == 1
        intent = result.outgoing[0]
        assert (intent.port, intent.arrival_tick) == (0, 1)
        assert all(record is None for record in node.records)
        assert all(not register.slots for register in local.ports)
        assert node.output.packets[intent.slot] is world._links.bank(node.position).packets[intent.slot]
        assert result.wakes == ()
        frames.append(world.snapshot())
        render_disturbances(
            frames, tmp_path / "register-bank-ownership.html", {"scope": "isolated local owner calls"}
        )


def test_zero_valued_cross_register_pair_remains_active(tmp_path):
    raw = joint_document()
    for kind in raw["disturbance_types"]:
        kind["defaults"]["amount"] = 0
    raw["interactions"][0].pop("when")
    initial = parse_initial_state(raw)
    with Simulation(replace(initial, seeds=())) as world:
        local = PortExecutionNode(world._at((1, 1, 1)), world._services)
        packets = tuple(
            Packet(1, seed.position, port, seed.record)
            for seed, port in zip(initial.seeds, (0, 2), strict=True)
        )
        local.receive((ReadyBatch(1, "arrival", packets[:1]), ReadyBatch(3, "arrival", packets[1:])), 1)
        assert local.bootstrap(1).wakes == (WakeIntent(1, "compute", 1), WakeIntent(3, "compute", 1))
        local.ready((ReadyBatch(1, "compute"), ReadyBatch(3, "compute")), 1)
        assert local.node.pending.ready_tick == 3
        render_disturbances(
            [world.snapshot()], tmp_path / "zero-pair.html", {"scope": "zero-valued local joint inputs"}
        )


def test_repeated_arrival_port_preserves_original_packet_order(tmp_path):
    initial = parse_initial_state(joint_document())
    with Simulation(replace(initial, seeds=(), slots_per_node=3)) as world:
        local = PortExecutionNode(world._at((1, 1, 1)), world._services)
        first, second = (seed.record for seed in initial.seeds)
        packets = (
            Packet(1, (0, 1, 1), 0, first),
            Packet(1, (1, 0, 1), 2, second),
            Packet(1, (0, 1, 1), 0, first),
        )
        local.receive(tuple(ReadyBatch(packet.port ^ 1, "arrival", (packet,)) for packet in packets), 1)
        assert tuple(local.node.records) == (first, second, first)
        assert local.ports[1].slots == (0, 2)
        assert local.ports[3].slots == (1,)
        render_disturbances(
            [world.snapshot()],
            tmp_path / "ordered-arrivals.html",
            {"scope": "ordered admission from three packet slots"},
        )


@pytest.mark.parametrize("port", [-1, 6, True])
def test_register_ports_are_exactly_six(port):
    with pytest.raises(ValueError, match="Register port"):
        PortState(port)


def test_register_profile_rejects_unsupported_spatial_owner():
    raw = joint_document()
    raw["spatial_fields"] = [{"field": "amount", "baseline": 0, "transport": "local"}]
    raw["conservation_contract"]["quantities"][0]["spatial"] = {
        "field": "amount",
        "side": "right",
    }
    with Simulation(parse_initial_state(raw)) as world:
        with pytest.raises(ValueError, match="carrier-only"):
            PortExecutionNode(world._nodes[(0, 1, 1)], world._services)
