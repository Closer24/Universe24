"""Independent finite expectations for contact-triggered quantum feedback."""

import json
from pathlib import Path

import pytest

from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_json
from event_universe.integration.quantum_contact_trial import (
    CONTACT,
    ContactPlanner,
    mechanics,
    quantum_rules,
    run_trial,
)
from event_universe.quantum import DeferredQuantum, EventNetworkConfig

FIXTURE = Path(__file__).resolve().parents[1] / "examples/quantum/contact.json"


@pytest.mark.parametrize("ticket", range(25))
def test_all_tickets_select_physical_outcome(ticket):
    result = run_trial(FIXTURE, ticket)
    reflected = ticket >= 16
    assert result["outcome"] == int(reflected)
    assert result["weights_transmission_reflection"] == (16, 9)
    assert result["physical_tick"] == result["quantum_tick"] == 8
    assert result["extra_world_ticks"] == 0
    assert result["contact_tick"] == 4
    assert result["query_counts_after_each_tick"] == [0, 0, 0, 0, 0, 1, 1, 1, 1]
    last = result["balances"][-1]
    assert last["momentum"] == (0, 0, 0)
    assert last["twice_kinetic_energy"] == 2
    assert last["body_momenta"]["Body A"] == ((-1, 0, 0) if reflected else (1, 0, 0))
    sends = [e for e in result["events"] if e["event"] == "sent" and e["tick"] == 4]
    assert len(sends) == 2
    assert all(e["position"] == CONTACT and e["arrival_tick"] == 5 for e in sends)
    ports = {e["disturbance"]: e["port"] for e in sends}
    assert ports == ({"Body A": 1, "Body B": 0} if reflected else {"Body A": 0, "Body B": 1})
    assert result["final_quantum_state"] == (((4 if reflected else 1), (1, 0)),)


def test_no_contact_means_no_oracle_call():
    initial = parse_initial_json(FIXTURE.read_bytes())
    owner = DeferredQuantum()
    space = owner.bind_event_network(EventNetworkConfig((CONTACT,), (0,)))
    planner = ContactPlanner(initial, space, 24)
    planner((initial.seeds[0].record, None), (), 0)
    assert planner.record is None
    assert owner.query_stats.successful_queries == 0


@pytest.mark.parametrize("ticket", [-1, 25, True])
def test_invalid_ticket_is_rejected(ticket):
    with pytest.raises(ValueError, match="ticket"):
        run_trial(FIXTURE, ticket)


def test_render_capture_has_no_physical_feedback():
    plain, captured = run_trial(FIXTURE, 24), run_trial(FIXTURE, 24, visualize=True)
    assert plain["frames"] == []
    assert len(captured["frames"]) == 9
    for key in (
        "events", "balances", "final_state", "final_quantum_state", "query_counts_after_each_tick"
    ):
        assert plain[key] == captured[key]


def test_unmeasured_transmission_matches_ordinary_engine():
    events = []
    world = Simulation(parse_initial_json(FIXTURE.read_bytes()), observer=events.append)
    for _ in range(8):
        world.step()
        mechanics(world)
    measured = run_trial(FIXTURE, 0)
    assert mechanics(world) == measured["balances"][-1]

    def routing(trace):
        return [
            (e["tick"], e["position"], e["port"], e["arrival_tick"], e["disturbance"])
            for e in trace if e["event"] == "sent"
        ]

    assert routing(events) == routing(measured["events"])


def test_quantum_capacity_error_is_not_no_event():
    initial = parse_initial_json(FIXTURE.read_bytes())
    owner = DeferredQuantum()
    space = owner.bind_event_network(EventNetworkConfig((CONTACT, (6, 3, 1)), (0,), max_nodes=3))
    space.step(((quantum_rules()[0], (0, 1)),))
    planner = ContactPlanner(initial, space, 24)
    with pytest.raises(OverflowError):
        planner(tuple(s.record for s in initial.seeds), (), 0)
    assert space.records == ()
    assert planner.record is None


def test_outside_fixture_geometry_fails_before_running(tmp_path):
    data = json.loads(FIXTURE.read_text())
    data["shape"] = [14, 5, 3]
    changed = tmp_path / "contact.json"
    changed.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="fixture"):
        run_trial(changed, 0)
