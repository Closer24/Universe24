"""Native program startup capacity is checked before any world is constructed."""

import pytest

from event_universe import Simulation
from event_universe.core.event_space import CausalEventSpace
from event_universe.initialization import parse_initial_state
from event_universe.integration.event_program import parse_event_program
from event_universe.quantum.event_network import EventNetwork


@pytest.fixture(autouse=True)
def no_runtime_construction(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Static validation must not construct or step runtime state")

    for owner in (Simulation, CausalEventSpace, EventNetwork):
        monkeypatch.setattr(owner, "__init__", forbidden)
    monkeypatch.setattr(Simulation, "step", forbidden)


def configuration(positions, *, capacity=1, addresses=None, model="causal-events-v1", max_nodes=10000):
    program = {"model": model, "capacity": capacity}
    if addresses is not None:
        program["addresses"] = addresses
        program["bounds"] = {"max_nodes": max_nodes}
        if model == "local-quantum-events-v2":
            program["register_names"] = [f"register {index}" for index in range(len(addresses))]
            program["dimensions"] = [2] * len(addresses)
    return {
        "schema_version": 1,
        "model_id": "static-native-validation-fixture",
        "shape": [5, 5, 5],
        "boundary": "open",
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 10000,
        "ticks": 10,
        "operation_costs": {
            "receive": 1,
            "read": 1,
            "evaluate": 1,
            "update": 1,
            "couple": 1,
            "route": 1,
            "split": 1,
            "send": 1,
            "commit": 1,
        },
        "fields": [
            {
                "name": "stock",
                "components": 1,
                "units": "fixture unit",
                "signed": False,
                "conserved": True,
            }
        ],
        "disturbance_types": [
            {
                "name": "held record",
                "fields": ["stock"],
                "defaults": {"stock": 1},
                "transport": {"mode": "hold"},
            }
        ],
        "seeds": [{"position": list(position), "type": "held record"} for position in positions],
        "event_program": program,
    }


def test_empty_causal_program_needs_no_initial_source_event():
    initial = parse_initial_state(configuration([]))
    assert parse_event_program(initial).capacity == 1


def test_classical_sources_count_distinct_nodes_and_accept_exact_capacity():
    initial = parse_initial_state(configuration([(0, 0, 0), (0, 0, 0), (1, 0, 0)], capacity=2))
    assert len(initial.seeds) == 3
    assert parse_event_program(initial).capacity == 2
    parse_initial_state(configuration([(0, 0, 0)] * 3, capacity=1))


def test_classical_initial_sources_exceeding_capacity_fail_before_startup():
    with pytest.raises(ValueError, match="initial sources.*2.*capacity.*1"):
        parse_initial_state(configuration([(0, 0, 0), (1, 0, 0)], capacity=1))


@pytest.mark.parametrize("model", ["local-quantum-events-v1", "local-quantum-events-v2"])
def test_quantum_register_sources_accept_exact_capacity_and_reject_one_less(model):
    addresses = [[0, 0, 0], [1, 0, 0]]
    initial = parse_initial_state(configuration([], capacity=2, addresses=addresses, model=model))
    assert len(parse_event_program(initial).network.addresses) == 2
    with pytest.raises(ValueError, match="initial sources.*2.*capacity.*1"):
        parse_initial_state(configuration([], capacity=1, addresses=addresses, model=model))


@pytest.mark.parametrize("model", ["local-quantum-events-v1", "local-quantum-events-v2"])
def test_classical_and_quantum_initial_sources_share_the_event_capacity(model):
    positions = [(0, 0, 0), (0, 0, 0), (1, 0, 0)]
    addresses = [[0, 0, 0], [1, 0, 0]]
    parse_initial_state(configuration(positions, capacity=4, addresses=addresses, model=model))
    with pytest.raises(ValueError, match="initial sources.*4.*capacity.*3"):
        parse_initial_state(configuration(positions, capacity=3, addresses=addresses, model=model))


def test_colocated_quantum_registers_keep_separate_source_events():
    positions = [(0, 0, 0), (0, 0, 0)]
    addresses = [[0, 0, 0], [0, 0, 0]]
    options = {"addresses": addresses, "model": "local-quantum-events-v2"}
    parse_initial_state(configuration(positions, capacity=3, **options))
    with pytest.raises(ValueError, match="initial sources.*3.*capacity.*2"):
        parse_initial_state(configuration(positions, capacity=2, **options))


def test_quantum_node_budget_remains_separate_from_shared_event_capacity():
    positions = [(0, 0, 0), (1, 0, 0)]
    options = {"addresses": [[0, 0, 0], [0, 0, 0]], "model": "local-quantum-events-v2"}
    parse_initial_state(configuration(positions, capacity=4, max_nodes=2, **options))
    with pytest.raises(ValueError, match="node budget cannot hold initial sources"):
        parse_initial_state(configuration(positions, capacity=4, max_nodes=1, **options))


def test_startup_validation_does_not_reserve_capacity_for_future_events():
    raw = configuration([], capacity=1, addresses=[[0, 0, 0]], model="local-quantum-events-v1")
    raw["event_program"]["layers"] = [
        {"tick": 1, "operations": [{"register_indices": [0], "matrix": [[0, 1], [1, 0]]}]}
    ]
    initial = parse_initial_state(raw)
    assert parse_event_program(initial).capacity == 1


def test_classical_spatial_sources_count_each_owner_without_expanding_baselines():
    raw = configuration([(0, 0, 0)], capacity=3)
    raw["shape"] = [1000, 1000, 1000]
    raw["spatial_fields"] = [{"field": "stock", "baseline": 7, "transport": "outward"}]
    raw["spatial_seeds"] = [
        {"position": p, "field": "stock", "populations": [1] * 8} for p in ([0, 0, 0], [1, 0, 0])
    ]
    assert parse_event_program(parse_initial_state(raw)).network is None
    raw["event_program"]["capacity"] = 2
    with pytest.raises(ValueError, match="initial sources.*3.*capacity.*2"):
        parse_initial_state(raw)
    raw["spatial_seeds"] = []
    raw["event_program"]["capacity"] = 1
    parse_initial_state(raw)


@pytest.mark.parametrize("model", ["local-quantum-events-v1", "local-quantum-events-v2"])
def test_quantum_spatial_composition_remains_explicitly_unsupported(model):
    raw = configuration([], addresses=[[0, 0, 0]], model=model)
    raw["spatial_fields"] = [{"field": "stock", "baseline": 0, "transport": "outward"}]
    with pytest.raises(ValueError, match="quantum.*spatial-field clocks"):
        parse_initial_state(raw)
