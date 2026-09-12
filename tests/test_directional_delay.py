"""Independent schedules, ownership and uniform compatibility for six-port waits."""

from copy import deepcopy
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, DirectionalDelayDefinition
from event_universe.core.timing import directional_timing
from event_universe.diagnostics.cell_contract import cell_state_violations
from event_universe.initialization import parse_initial_state
from tests.test_disturbance_engine import document, kind, resident_values
from tests.test_local_field_rules import document as field_document
from tests.test_local_field_rules import field, invariant, local, operation, seed

ORIGIN = (2, 2, 2)


def pair_document():
    return document(
        [
            kind("positive_x", mode="move", weights=[1, 0, 0, 0, 0, 0]),
            kind("negative_x", mode="move", weights=[0, 1, 0, 0, 0, 0]),
        ],
        [(ORIGIN, "positive_x"), (ORIGIN, "negative_x")],
        budget=4,
        capacity=2,
    )


def wave_document(*, travel=1):
    raw = field_document([field("stock", conserved=True)], [seed("stock", 8)])
    raw["link_ticks"] = travel
    half = operation("exact_div", local("stock"), 2)
    raw["field_rules"] = [
        {
            "name": "two_outputs",
            "assignments": [
                {"field": "stock", "expression": 0},
                {"field": "stock", "port": 0, "expression": half},
                {"field": "stock", "port": 2, "expression": half},
            ],
            "invariants": [
                invariant(
                    "stock",
                    operation(
                        "add",
                        local("stock"),
                        operation(
                            "add", {"outgoing": "stock", "port": 0}, {"outgoing": "stock", "port": 2}
                        ),
                    ),
                )
            ],
        }
    ]
    return raw


@pytest.mark.parametrize("weights", [1, [1] * 6, [2] * 6])
def test_uniform_input_reproduces_the_complete_default_run(weights):
    original = pair_document()
    changed = deepcopy(original)
    changed["directional_delay"] = {"weights": weights, "denominator": 2 if weights == [2] * 6 else 1}
    sinks = [[], []]
    worlds = [
        Simulation(parse_initial_state(raw), observer=sink.append)
        for raw, sink in zip((original, changed), sinks, strict=True)
    ]
    for _ in range(12):
        for world in worlds:
            world.step()
        assert worlds[0].snapshot() == worlds[1].snapshot()
        assert worlds[0].computation_report() == worlds[1].computation_report()
    assert sinks[0] == sinks[1]


def test_unequal_outputs_release_independently_and_keep_one_owner():
    raw = pair_document()
    raw["directional_delay"] = {"weights": [1, 3, 1, 1, 1, 1]}
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()  # cost 7, B4: base wait 1; common atomic commit at 1.
    assert world.cells[ORIGIN].pending is None
    assert resident_values(world, ORIGIN) == []
    pending = [p for p in world.links[ORIGIN] if p is not None]
    assert [(p.release_tick, p.arrival_tick) for p in pending] == [(None, 2), (3, 4)]
    assert sum(e["event"] == "cycle_committed" for e in events) == 1
    assert [(e["port"], e["tick"]) for e in events if e["event"] == "sent"] == [(0, 1)]
    assert world.snapshot()["transfers"][1]["owner"] == "cell"
    for _ in range(3):
        world.step()
        assert world.totals() == {"inventory": (2,)}
        assert not cell_state_violations(tuple(world.links.values()))
    arrivals = [e for e in events if e["event"] == "received" and e["disturbance"] == "negative_x"]
    assert arrivals[0]["tick"] == 4
    assert arrivals[0]["position"] == (1, 2, 2)
    assert all(e["arrival_tick"] - e["tick"] == 1 for e in events if e["event"] == "sent")


@pytest.mark.parametrize("travel", [1, 3])
def test_spatial_cost_policy_delays_outputs_instead_of_stretching_links(travel):
    raw = wave_document(travel=travel)
    # Obtain the priced structural cost; expected timing below is independent arithmetic.
    control_events = []
    control = Simulation(parse_initial_state(raw), observer=control_events.append)
    control.step()
    cost = next(e["cost"] for e in control_events if e["event"] == "spatial_cycle")
    raw["normal_budget"] = cost - 1
    raw["directional_delay"] = {"weights": [1, 1, 3, 1, 1, 1], "spatial_mode": "cost"}
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    # Both outputs left retained stock together, but one still waits three base intervals.
    assert world.spatial_values(ORIGIN)["stock"]["value"] == (0,)
    assert world.totals()["stock"] == (8,)
    while world.tick < 4 * travel:
        world.step()
        assert world.totals()["stock"] == (8,)
        assert world.spatial_accounting()["stock"]["balanced"]
    sent = [
        (e["port"], e["tick"], e["arrival_tick"])
        for e in events
        if e["event"] == "spatial_sent" and e["position"] == ORIGIN
    ]
    assert sent == [(0, travel, 2 * travel), (2, 3 * travel, 4 * travel)]
    assert all(e["arrival_tick"] - e["tick"] == travel for e in events if e["event"] == "spatial_sent")


def test_equal_spatial_weights_preserve_fixed_mode_but_cost_mode_removes_timing_bypass():
    raw = wave_document()
    raw["normal_budget"] = 1
    sinks = [[], []]
    worlds = []
    for mode, sink in zip(("fixed", "cost"), sinks, strict=True):
        selected = deepcopy(raw)
        selected["directional_delay"] = {"weights": 1, "spatial_mode": mode}
        worlds.append(Simulation(parse_initial_state(selected), observer=sink.append))
    for world in worlds:
        world.step()
    assert any(e["event"] == "spatial_received" for e in sinks[0])
    assert not any(e["event"] == "spatial_sent" for e in sinks[1])
    assert all(p["owner"] == "cell" for p in worlds[1].snapshot()["spatial_transfers"])


@pytest.mark.parametrize(
    "delay",
    [
        {"weights": True},
        {"weights": 1.5},
        {"weights": [1] * 5},
        {"weights": [1] * 7},
        {"weights": [-1] * 6},
        {"weights": [True] * 6},
        {"weights": [1.0] * 6},
        {"weights": MAX_VALUE + 1},
        {"denominator": 0},
        {"denominator": False},
        {"spatial_mode": "automatic"},
        {"unexpected": 1},
        None,
    ],
)
def test_invalid_delay_definitions_fail_at_initialization(delay):
    raw = pair_document()
    raw["directional_delay"] = delay
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_rational_weights_round_only_the_declared_wait_and_unused_directions_do_not_block():
    law = DirectionalDelayDefinition((1, 3, 8, 1, 1, 1), 2)
    assert directional_timing(11, 10, 3, law, (0, 1)) == (2, 8, (2, 5, 12, 2, 2, 2))
    assert directional_timing(10, 10, 3, law, (0, 1)) == (0, 3, (0,) * 6)


def test_time_overflow_fails_before_the_transaction_changes_inventory():
    raw = pair_document()
    raw["directional_delay"] = {"weights": [MAX_VALUE] * 6}
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()
    with pytest.raises(ValueError):
        world.step()
    assert world.snapshot() == before
    assert world.faulted


@pytest.mark.parametrize("bad", [(True,) * 6, (-1,) * 6, (1,) * 3])
def test_direct_definition_does_not_bypass_bounds(bad):
    with pytest.raises(ValueError):
        replace(DirectionalDelayDefinition(), weights=bad)


def test_only_used_direction_sets_single_record_commit_time():
    raw = document([kind("slow", mode="move", weights=[0, 1, 0, 0, 0, 0])], [(ORIGIN, "slow")], budget=3)
    raw["directional_delay"] = {"weights": [0, 3, 0, 0, 0, 0]}
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.cells[ORIGIN].pending.ready_tick == 3
    assert resident_values(world, ORIGIN) == [{"inventory": (1,)}]
    assert world.snapshot()["transfers"] == []


def test_playback_keeps_waiting_output_on_its_node_until_actual_dispatch():
    from tests.test_observer_playback import player, recording

    data = recording()
    result = player(
        data,
        """
initializeWorldView();
const p={origin:[1,2,3],target:[2,2,3],port:0,arrival_tick:111,departure_tick:110};
console.log(JSON.stringify([transferView(p,{tick:107}),transferView(p,{tick:110})]));
""",
    )
    assert result[0]["position"] == [1, 2, 3]
    assert result[0]["transfer"] is False
    assert "Waiting at node" in result[0]["owner"]
    assert "Link" in result[1]["owner"]


def test_runner_preserves_directional_policy_and_failed_output_evidence(tmp_path):
    import json

    from event_universe.runner import run_initialization

    raw = pair_document()
    raw["ticks"] = 3
    raw["directional_delay"] = {"weights": [1, 3, 1, 1, 1, 1]}
    source = tmp_path / "initialization.json"
    source.write_text(json.dumps(raw))
    output = tmp_path / "run"
    run_initialization(source, output)
    meta = json.loads((output / "run.json").read_text())
    assert meta["accounting_balanced_at_every_completed_tick"]
    assert meta["directional_delay"]["weights"] == raw["directional_delay"]["weights"]
    assert meta["directional_delay"]["link_transit_ticks"] == 1
    assert not (output / "run.html").exists()


@pytest.mark.parametrize("boundary", ["open", "periodic"])
@pytest.mark.parametrize("travel", [1, 2])
def test_delayed_finite_source_decay_and_escape_remain_balanced(boundary, travel):
    from tests.test_finite_spatial_engine import finite_document

    raw = finite_document(moving=True, source=True, travel=travel, budget=32)
    raw["boundary"] = boundary
    raw["shape"] = [5, 5, 5]
    raw["seeds"][0]["position"] = [2, 2, 2]
    raw["emissions"][0]["budget"] = 96
    raw["directional_delay"] = {"weights": [0, 2, 1, 3, 1, 1], "spatial_mode": "cost"}
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    initial = world.totals()
    for _ in range(28):
        world.step()
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        for name, expected in initial.items():
            assert tuple(
                a + b + c
                for a, b, c in zip(
                    world.totals()[name],
                    world.dissipation_totals()[name],
                    world.escaped_totals()[name],
                    strict=True,
                )
            ) == tuple(a + b for a, b in zip(expected, world.source_totals()[name], strict=True))
    assert all(e["arrival_tick"] - e["tick"] == travel for e in events if e["event"].endswith("sent"))


def test_joint_reaction_never_rewrites_waiting_or_inflight_spatial_outputs():
    from tests.test_spatial_coupling import document as coupled_document

    raw = coupled_document()
    raw["normal_budget"] = 64
    raw["shape"] = [5, 5, 5]
    for item in raw["seeds"]:
        item["position"] = list(ORIGIN)
    raw["directional_delay"] = {"weights": [1, 2, 1, 2, 1, 2], "spatial_mode": "cost"}
    world = Simulation(parse_initial_state(raw))
    for _ in range(24):
        world.step()
        assert world.spatial_accounting()["inventory"]["balanced"]
        for packets in world._spatial.links.values():
            assert not cell_state_violations(packets)
    assert world.totals()["inventory"] == (5, 0, 0)


def test_delayed_receiver_retains_all_directional_inputs_but_observer_reports_only_new_arrivals():
    from event_universe.core.disturbance_state import pack
    from event_universe.core.spatial_state import SpatialPacket

    raw = wave_document()
    raw["directional_delay"] = {"weights": 1, "spatial_mode": "cost"}
    raw["spatial_seeds"] = []
    world = Simulation(parse_initial_state(raw))
    engine = world._spatial
    events = []
    engine.observer = events.append
    engine._at(ORIGIN).available_tick = 10
    # Two already-dispatched finite inputs arrive at different ticks during one wait.
    for tick, amount in ((1, 3), (2, 5)):
        origin = (1, 2, 2)
        packet = SpatialPacket(tick, origin, 0, (((pack((amount,)),) + (pack((0,)),) * 7),))
        engine.links[origin] = (packet, None, None, None, None, None)
        engine.deliver(tick)
    state = engine.cells[ORIGIN]
    from event_universe.core.disturbance_state import unpack

    assert unpack(state.states[0].delivered[0]) == (8,)
    receipts = [event for event in events if event["event"] == "spatial_received"]
    assert [event["received_fields"][1]["stock"] for event in receipts] == [(3,), (5,)]
    assert state.received_count == 2
    assert engine.cost(ORIGIN, 2) == 0


def test_source_keeps_emitting_while_its_output_waits_at_the_origin():
    from tests.test_spatial_engine import document as source_document

    raw = source_document(moving=True, source=True)
    raw["shape"] = [9, 9, 9]
    raw["seeds"][0]["position"] = [4, 4, 4]
    raw["disturbance_types"].append(
        {
            "name": "fast_partner",
            "fields": ["heading"],
            "defaults": {"heading": [0, 1, 0]},
            "transport": {"mode": "move", "direction_field": "heading"},
        }
    )
    raw["seeds"].append({"position": [4, 4, 4], "type": "fast_partner"})
    baseline_events = []
    baseline = Simulation(parse_initial_state(raw), observer=baseline_events.append)
    baseline.step()
    cost = next(e["cost"] for e in baseline_events if e["event"] == "cycle_started")
    raw["normal_budget"] = cost - 1
    raw["directional_delay"] = {"weights": [3, 1, 1, 1, 1, 1]}
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(4):
        world.step()
        assert world.totals()["strength"] == (72,)
        assert world.spatial_accounting()["radiation"]["balanced"]
    emissions = [
        e["tick"]
        for e in events
        if e["event"] == "spatial_cycle" and e["position"] == (4, 4, 4) and e["source_delta"]
    ]
    assert emissions == [0, 1, 2]
    sends = [e for e in events if e["event"] == "sent" and e["disturbance"] == "carrier"]
    assert sends[0]["tick"] == 3 and sends[0]["arrival_tick"] == 4
    assert world.source_totals()["radiation"] == (216,)


def test_fixed_spatial_no_output_does_not_reserve_an_unused_future_link():
    raw = field_document([field("stock", conserved=True)], [seed("stock", 8)])
    raw["link_ticks"] = 2
    world = Simulation(parse_initial_state(raw))
    world.tick = MAX_VALUE - 1
    world.step()
    assert world.tick == MAX_VALUE
    assert world.totals() == {"stock": (8,)}
    assert world.snapshot()["spatial_transfers"] == []
