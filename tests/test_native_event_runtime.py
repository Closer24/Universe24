"""Native event integration, classical endpoints and priced causal paths."""

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe.core.event_space import CausalEventSpace
from event_universe.quantum import Amplitude, DeferredQuantum, EventNetworkConfig, LocalUnitary
from event_universe.reference_api import ReferenceSimulation as Simulation
from event_universe.reference_api import parse_reference_state as parse_initial_state

BASE = Path(__file__).resolve().parents[1] / "examples/quantum/contact.json"
POSITION = [[[1, 0], [0, 0]], [[0, 0], [0, 1]]]


def configuration(r=3, t=4, n=5):
    data = json.loads(BASE.read_text())
    data["model_id"] = "native-quantum-contact-v1"
    data["event_program"] = {
        "model": "local-quantum-events-v1",
        "capacity": 10000,
        "addresses": [[6, 2, 1], [6, 3, 1]],
        "occupied": [0],
        "layers": [
            {
                "tick": 1,
                "operations": [
                    {
                        "sites": [0, 1],
                        "matrix": [
                            [n, 0, 0, 0],
                            [0, r, -t, 0],
                            [0, t, r, 0],
                            [0, 0, 0, n],
                        ],
                    }
                ],
            }
        ],
        "bindings": [
            {
                "address": [6, 2, 1],
                "types": ["Body A", "Body B"],
                "field": "decision",
                "codes": [1, 2],
                "instrument": POSITION,
            }
        ],
        "seed": 17,
    }
    return data


def run(data, names=("mass", "momentum")):
    trace = []
    world = Simulation(parse_initial_state(data), observer=trace.append)
    frames = [world.snapshot()]
    for _ in range(data["ticks"]):
        world.step()
        assert world.totals()[names[0]] == (2,)
        assert world.totals()[names[1]] == (0, 0, 0)
        state = world.snapshot()
        values = [r["values"] for c in state["cells"] for r in c["disturbances"]]
        values += [r["values"] for r in state["transfers"]]
        assert sum(sum(p * p for p in v[names[1]]) for v in values) == 2
        frames.append(world.snapshot())
    return world, trace, frames


def physical(frames):
    """Compare physical payload, place and transit, not diagnostic control codes."""
    frames = copy.deepcopy(frames)
    for frame in frames:
        for cell in frame["cells"]:
            cell.pop("cost")
            for record in cell["disturbances"]:
                record["values"].pop("decision", None)
        for packet in frame["transfers"]:
            packet["values"].pop("decision", None)
    return frames


@pytest.mark.parametrize("r,t,n", [(0, 1, 1), (5, 12, 13), (3, 4, 5), (12, 5, 13), (1, 0, 1)])
def test_all_parameter_tickets_produce_expected_native_outputs(r, t, n):
    counts = [0, 0]
    for ticket in range(n * n):
        data = configuration(r, t, n)
        data["event_program"]["tickets"] = [ticket]
        world, trace, _ = run(data)
        report = world.computation_report()
        record = report["resolver"]["records"][0]
        counts[record["outcome"]] += 1
        assert record["decision"]["weights"] == (t * t, r * r)
        assert report["resolver"]["oracle_calls"] == 1
        assert report["resolver"]["random_draws"] == int(bool(r and t))
        assert report["resolver"]["oracle_direct_world_ticks"] == 0
        assert report["model_operations_cost"] == sum(
            e["cost"] for e in trace if e["event"] == "cycle_started"
        )
        assert report["model_operations_cost"] == report["event_ledger_cost"] > 0
        sends = [e for e in trace if e["event"] == "sent" and e["tick"] == 4]
        assert len(sends) == 2
        assert sends[0]["arrival_tick"] == sends[1]["arrival_tick"] == 5
        for sent in sends:
            assert record["event_id"] in world.event_space.ancestors(sent["event_id"])
        assert {e["disturbance"]: e["port"] for e in sends} == (
            {"Body A": 1, "Body B": 0} if record["outcome"] else {"Body A": 0, "Body B": 1}
        )
    assert counts == [t * t, r * r]


def test_classical_endpoint_matches_ordinary_native_engine_every_tick():
    data = configuration(0, 1, 1)
    _, _, unified = run(data)
    data.pop("event_program")
    _, _, ordinary = run(data)
    assert physical(unified) == physical(ordinary)


def test_generic_ledger_does_not_change_classical_physics_or_cost():
    data = configuration()
    data.pop("event_program")
    before, _, frames = run(data)
    data["event_program"] = {"model": "causal-events-v1", "capacity": 10000}
    after, _, traced = run(data)
    assert frames == traced
    assert (
        before.computation_report()["model_operations_cost"]
        == after.computation_report()["model_operations_cost"]
    )
    for event in after.event_space.events:
        assert all(parent < event.id for parent in event.parents)
        assert event.parents == event.physical_parents


def test_path_work_is_cumulative_not_free_and_waits_are_not_recharged():
    data = configuration(0, 1, 1)
    data["normal_budget"] = 2
    data["ticks"] = 40
    world, trace, frames = run(data)
    starts = [e for e in trace if e["event"] == "cycle_started"]
    commits = [e for e in trace if e["event"] == "cycle_committed"]
    assert len(starts) > 2
    for start in starts:
        extra = (start["cost"] + 1) // 2 - 1
        assert start["ready_tick"] == start["tick"] + extra
    assert any(e["ready_tick"] > e["tick"] for e in starts)
    assert world.computation_report()["model_operations_cost"] == sum(e["cost"] for e in starts)
    assert world.computation_report()["local_cycles_started"] == len(starts)
    for sent in (e for e in trace if e["event"] == "sent"):
        assert sent["arrival_tick"] == sent["tick"] + 1
    record = world.computation_report()["resolver"]["records"][0]
    tick = record["decision"]["tick"]
    assert tick > 4
    contact_cycle = next(e for e in starts if e["position"] == (6, 2, 1) and e["tick"] == tick)
    assert any(e["position"] == (6, 2, 1) and e["tick"] == contact_cycle["ready_tick"] for e in commits)
    assert world.computation_report()["resolver"]["oracle_calls"] == 1
    # More completed physical links necessarily involve more charged cycles.
    assert (
        sum(e["cost"] for e in starts if e["tick"] < 20)
        < world.computation_report()["model_operations_cost"]
    )


def test_periodic_repeated_contacts_get_distinct_records_and_causal_hops():
    data = configuration()
    data.update(shape=[8, 5, 3], boundary="periodic", ticks=14)
    data["seeds"][0]["position"] = [1, 2, 1]
    data["seeds"][1]["position"] = [5, 2, 1]
    p = data["event_program"]
    p["addresses"] = [[3, 2, 1], [7, 2, 1]]
    p["occupied"] = []
    p["layers"] = []
    template = p["bindings"][0]
    p["bindings"] = [{**template, "address": a} for a in p["addresses"]]
    world, trace, _ = run(data)
    records = world.computation_report()["resolver"]["records"]
    assert [r["decision"]["tick"] for r in records] == [2, 6, 10]
    assert len({r["event_id"] for r in records}) == 3
    assert world.computation_report()["resolver"]["random_draws"] == 0
    assert len([e for e in trace if e["event"] == "received"]) == 28


def test_local_hold_does_not_measure_again_without_new_arrival():
    data = configuration()
    data["seeds"][0]["position"] = [6, 2, 1]
    data["seeds"][1]["position"] = [6, 2, 1]
    for kind in data["disturbance_types"]:
        kind["transport"] = {"mode": "hold"}
    data["event_program"]["layers"] = []
    world, _, _ = run(data)
    assert world.computation_report()["resolver"]["oracle_calls"] == 1


def test_failures_do_not_create_silent_no_event_or_allow_resume():
    data = configuration()
    data["event_program"]["bounds"] = {"max_terms": 1}
    world = Simulation(parse_initial_state(data))
    with pytest.raises(OverflowError):
        for _ in range(8):
            world.step()
    assert world.faulted
    assert world.computation_report()["resolver"]["records"] == []
    with pytest.raises(RuntimeError):
        world.step()


@pytest.mark.parametrize(
    "key,value", [("capacity", 0), ("model", "unknown"), ("seed", True), ("addresses", [[99, 0, 0]])]
)
def test_invalid_program_rejected_during_initialization(key, value):
    data = configuration()
    data["event_program"][key] = value
    with pytest.raises((ValueError, TypeError)):
        parse_initial_state(data)


def test_invalid_local_instrument_or_conserved_control_is_rejected():
    for field in ("mass", "momentum"):
        data = configuration()
        data["event_program"]["bindings"][0]["field"] = field
        with pytest.raises(ValueError):
            parse_initial_state(data)
    data = configuration()
    data["event_program"]["bindings"][0]["instrument"] = [[[1, 0], [0, 0]]]
    with pytest.raises(ValueError):
        parse_initial_state(data)


def test_renamed_fields_types_and_reordered_declarations_still_run():
    data = configuration(0, 1, 1)
    before, _, frames = run(data)
    # Reordering is handled by name resolution, not hard-coded field indices.
    data["fields"].reverse()
    data["disturbance_types"].reverse()
    after, _, other = run(data)
    assert physical(frames) == physical(other)
    assert (
        before.computation_report()["model_operations_cost"]
        == after.computation_report()["model_operations_cost"]
    )


def test_shared_identity_namespace_retains_quantum_inverse_and_checkpoint():
    events = CausalEventSpace()
    root = events.append(tick=0, addresses=((0, 0, 0),), owner="other", kind="source")
    owner = DeferredQuantum()
    space = owner.bind_event_network(EventNetworkConfig(((0, 0, 0),)), event_space=events)
    h = LocalUnitary(tuple(tuple(Amplitude(x, 0) for x in row) for row in ((1, 1), (1, -1))))
    space.step(((h, (0,)),))
    space.checkpoint(0)
    space.step(((h, (0,)),))
    assert space.query(0).weights == (1, 0)
    assert events.event(root.id) is root
    assert not space.records


def test_dependency_is_not_a_physical_link_and_capacity_is_atomic():
    events = CausalEventSpace(3)
    a = events.append(tick=0, addresses=((0, 0, 0),), owner="a", kind="source")
    with pytest.raises(ValueError, match="link"):
        events.append(
            tick=0, addresses=((9, 0, 0),), owner="b", kind="receive", physical_parents=(a.id,)
        )
    assert events.next_id == 1
    b = events.append(tick=0, addresses=((9, 0, 0),), owner="b", kind="calculation", parents=(a.id,))
    events.append(tick=0, addresses=((9, 0, 0),), owner="b", kind="result", parents=(b.id,))
    with pytest.raises(OverflowError):
        events.append(tick=0, addresses=((9, 0, 0),), owner="b", kind="overflow")
    assert events.next_id == 3


def test_selected_mechanical_branch_pays_its_own_work():
    straight, _, _ = run(configuration(0, 1, 1))
    reflected, _, _ = run(configuration(1, 0, 1))
    assert straight.computation_report()["model_operations_cost"] == 116
    assert reflected.computation_report()["model_operations_cost"] == 135
    for world in (straight, reflected):
        report = world.computation_report()["resolver"]
        assert report["controller_overhead_cost"] == 4
        assert report["oracle_calls"] == 1
        assert report["random_draws"] == 0


def test_regular_runner_writes_shared_graph_and_costs_without_rendering(tmp_path):
    from event_universe.reference_runner import run_reference_initialization as run_initialization

    initial = tmp_path / "initial.json"
    initial.write_text(json.dumps(configuration(0, 1, 1)))
    output = tmp_path / "run"
    result = run_initialization(initial, output)
    assert result == output / "run.json"
    metadata = json.loads(result.read_text())
    assert metadata["status"] == "completed"
    assert metadata["computation"]["model_operations_cost"] == 116
    assert metadata["computation"]["resolver"]["random_draws"] == 0
    events = [json.loads(line) for line in (output / "causal-events.jsonl").read_text().splitlines()]
    assert {e["owner"] for e in events} == {"quantum", "disturbance", "resolver"}
    assert not (output / "run.html").exists()


def test_invalid_ticket_fails_without_record_and_faults_native_world():
    data = configuration()
    data["event_program"]["tickets"] = [25]
    world = Simulation(parse_initial_state(data))
    with pytest.raises(ValueError, match="ticket"):
        for _ in range(8):
            world.step()
    assert world.faulted
    assert world.computation_report()["resolver"]["records"] == []


def test_retired_quantum_payload_does_not_delete_a_physical_descendant():
    data = configuration(0, 1, 1)
    world, trace, _ = run(data)
    events = world.event_space
    before = events.events
    resolver = world._resolver
    resolver.space.checkpoint(0)
    assert events.events[: len(before)] == before
    sent = next(e for e in trace if e["event"] == "sent" and e["tick"] == 4)
    assert events.ancestors(sent["event_id"])


def test_two_tick_physical_links_and_recipe_timing():
    data = configuration(0, 1, 1)
    data["link_ticks"] = 2
    data["ticks"] = 16
    data["event_program"]["layers"][0]["tick"] = 2
    world, trace, _ = run(data)
    assert world.computation_report()["resolver"]["records"][0]["decision"]["tick"] == 8
    assert all(e["arrival_tick"] - e["tick"] == 2 for e in trace if e["event"] == "sent")
    data["event_program"]["layers"][0]["tick"] = 1
    world = Simulation(parse_initial_state(data))
    with pytest.raises(ValueError, match="link time"):
        world.step()
    assert world.faulted


def test_renaming_labels_does_not_select_hidden_mechanics():
    mapping = {
        "mass": "inventory",
        "momentum": "travel",
        "decision": "choice",
        "Body A": "alpha",
        "Body B": "beta",
    }

    def translated(value, names):
        if isinstance(value, str):
            return names.get(value, value)
        if isinstance(value, dict):
            return {names.get(k, k): translated(v, names) for k, v in value.items()}
        if isinstance(value, (tuple, list)):
            return type(value)(translated(v, names) for v in value)
        return value

    data = configuration(0, 1, 1)
    reference, _, frames = run(data)
    other, _, renamed = run(translated(data, mapping), ("inventory", "travel"))
    assert physical(frames) == physical(translated(renamed, {v: k for k, v in mapping.items()}))
    assert (
        reference.computation_report()["model_operations_cost"]
        == other.computation_report()["model_operations_cost"]
    )


@pytest.mark.parametrize(
    "name,expected",
    [
        ("native_classical", 116),
        ("native_quantum", 135),
        ("native_reflection", 135),
        ("native_cost_delay", 130),
    ],
)
def test_shipped_examples_use_the_normal_simulation(name, expected):
    data = json.loads((BASE.parent / (name + ".json")).read_text())
    world, _, _ = run(data)
    assert world.computation_report()["model_operations_cost"] == expected


def test_zero_valued_local_record_still_activates_declared_instrument():
    data = configuration()
    data["seeds"] = [
        {"position": [6, 2, 1], "type": "Body A", "values": {"mass": 0, "momentum": [0, 0, 0]}}
    ]
    data["disturbance_types"][0]["transport"] = {"mode": "hold"}
    data["interactions"] = []
    data["event_program"]["bindings"][0]["types"] = ["Body A"]
    data["event_program"]["layers"] = []
    world = Simulation(parse_initial_state(data))
    world.step()
    assert world.computation_report()["resolver"]["oracle_calls"] == 1
    assert world.computation_report()["resolver"]["records"][0]["outcome"] == 1


@pytest.mark.parametrize("budget", [1, 2, 5, 10000])
def test_classical_control_with_same_operation_cost_matches_delayed_world(budget):
    from dataclasses import replace

    from event_universe.core.disturbance_engine import DisturbanceEngine
    from event_universe.core.disturbance_state import pack
    from event_universe.fields.disturbances import DisturbanceLaw
    from event_universe.fields.record_operations import RecordOperations

    data = configuration(0, 1, 1)
    data["normal_budget"] = budget
    quantum = Simulation(parse_initial_state(data))
    data.pop("event_program")
    initial = parse_initial_state(data)
    law = DisturbanceLaw(
        initial.fields,
        initial.disturbances,
        initial.couplings,
        initial.operation_costs,
        initial.interactions,
    )

    def classical_plan(records, residuals, received):
        if all(r is not None for r in records):
            local = tuple(replace(r, values=(*r.values[:2], pack((1,)))) for r in records)
            plan = law(local, residuals, received)
            # Same explicit local inspection, constant-result primitive and two writes.
            return replace(plan, cost=plan.cost + 4)
        return law(records, residuals, received)

    classical = DisturbanceEngine(
        initial,
        classical_plan,
        record_policy=RecordOperations(
            initial.fields, initial.disturbances, initial.couplings, initial.interactions
        ),
        reference=True,
    )
    for _ in range(40):
        quantum.step()
        classical.step()
        assert quantum.snapshot() == classical.snapshot()
        assert (
            quantum.computation_report()["model_operations_cost"]
            == classical.computation_report()["model_operations_cost"]
        )


def test_canonical_cli_actually_emits_native_results(tmp_path):
    output = tmp_path / "native-cli"
    source = BASE.parent / "native_classical.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "event_universe.reference_runner",
            "--init",
            str(source),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["computation"]["model_operations_cost"] == 116
    assert metadata["computation"]["resolver"]["oracle_calls"] == 1
    assert metadata["computation"]["resolver"]["random_draws"] == 0
    assert (output / "causal-events.jsonl").stat().st_size > 0
    assert (output / "state.json").stat().st_size > 0
