"""Local reception, causal withholding, exact prefixes and passive recording."""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.diagnostics.local_observer import LocalObserver, ObserverDefinition
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization
from examples.observer.configuration import build_configuration, observer_position
from tests.test_spatial_engine import document

NODE = (0, 2, 2)


def test_configured_demo_receives_three_signals_while_local_clock_waits():
    probe = LocalObserver(ObserverDefinition(observer_position(9)))
    world = Simulation(parse_initial_state(build_configuration()), observer=probe.receive)
    counts, clocks = [], []
    for _ in range(8):
        world.step()
        counts.append(len(probe.receipts))
        clocks.append(probe.clock)
    assert counts == [0, 0, 0, 1, 1, 2, 2, 3]
    assert clocks == [1, 1, 2, 2, 2, 2, 2, 2]
    assert [r["port"] for r in probe.receipts] == [1, 2, 4]
    assert probe.receipts[0]["values"]["pulse_inventory"] == (7,)
    assert probe.receipts[1]["values"]["pulse_vector"] == (3, -2, 1)
    assert probe.receipts[2]["values"] == {"message_inventory": (11,), "message_vector": (2, -3, 1)}


def pulse_document():
    raw = document(components=3, baseline=[0, 0, 0], travel=2)
    raw.update(schema_version=2, shape=[5, 5, 5], ticks=3)
    raw["spatial_fields"][0].update(
        axis_weights=[1, 0, 0], decay={"retain_numerator": 1, "retain_denominator": 2}
    )
    raw["spatial_seeds"] = [
        {"position": [4, 2, 2], "field": "radiation", "populations": [[8, -4, 12], *([[0, 0, 0]] * 7)]}
    ]
    return raw


def test_clock_whitelist_ignores_global_information_and_preserves_capture_prefix():
    probe = LocalObserver(ObserverDefinition(NODE))
    probe.capture(0)
    probe.receive({"event": "cycle_committed", "position": NODE, "tick": 0})
    probe.receive({"event": "sent", "position": NODE, "values": {"secret": [99]}})
    probe.receive({"event": "cycle_committed", "position": (1, 2, 2)})
    probe.receive({"event": "received", "position": (1, 2, 2), "values": {"secret": [99]}})
    event = {
        "event": "received",
        "position": NODE,
        "port": 4,
        "disturbance": "__proto__",
        "values": {"charge": [-3]},
        "tick": 999,
        "origin": [9, 9, 9],
        "arrival_tick": 1000,
        "parents": [17],
    }
    probe.receive(event)
    event["values"]["charge"][0] = 99
    probe.capture(0)
    assert probe.samples == [
        {"audit_tick": 0, "clock": 0, "received_count": 0},
        {"audit_tick": 0, "clock": 1, "received_count": 1},
    ]
    assert probe.receipts == [
        {
            "sequence": 1,
            "clock": 1,
            "kind": "disturbance",
            "port": 4,
            "label": "__proto__",
            "values": {"charge": (-3,)},
        }
    ]
    second = LocalObserver(ObserverDefinition(NODE))
    second.receive({"event": "cycle_committed", "position": NODE, "tick": 100000})
    second.receive({**event, "tick": 0, "values": {"charge": [-3]}})
    assert second.receipts == probe.receipts


def test_zero_and_simultaneous_ports_are_retained_and_capacity_failure_is_atomic():
    event = {
        "event": "spatial_received",
        "position": NODE,
        "received_fields": [{"s": [0], "v": [2, -3, 0]}, {}, {}, {"s": [4]}, {}, {}],
    }
    too_small = LocalObserver(ObserverDefinition(NODE, max_receipts=1))
    with pytest.raises(ValueError, match="capacity exceeded"):
        too_small.receive(event)
    assert too_small.receipts == []
    probe = LocalObserver(ObserverDefinition(NODE, max_receipts=2))
    probe.receive(event)
    assert [(r["port"], r["clock"]) for r in probe.receipts] == [(0, 0), (3, 0)]
    assert probe.receipts[0]["values"] == {"s": (0,), "v": (2, -3, 0)}


def test_delayed_periodic_receipt_is_post_decay_and_observation_changes_no_state():
    initial = parse_initial_state(pulse_document())
    probe = LocalObserver(ObserverDefinition(NODE))
    observed, plain = Simulation(initial, observer=probe.receive), Simulation(initial)
    for tick in (1, 2, 3):
        observed.step()
        plain.step()
        assert observed.snapshot() == plain.snapshot()
        assert observed.computation_report() == plain.computation_report()
        assert len(probe.receipts) == (0 if tick == 1 else 1)
    assert probe.receipts[0]["port"] == 1
    assert probe.receipts[0]["values"] == {"radiation": (4, -2, 6)}
    assert probe.clock == 0
    assert observed.dissipation_totals()["radiation"] == (4, -2, 6)


def test_runner_archive_exhaustion_preserves_completed_delivery_and_failed_evidence(tmp_path):
    raw = pulse_document()
    raw["spatial_seeds"].append(
        {
            "position": [1, 2, 2],
            "field": "radiation",
            "populations": [[0, 0, 0]] * 4 + [[8, -4, 12]] + [[0, 0, 0]] * 3,
        }
    )
    initialization, placement = tmp_path / "input.json", tmp_path / "probe.json"
    initialization.write_text(json.dumps(raw))
    placement.write_text(json.dumps({"position": NODE, "max_receipts": 1}))
    output = tmp_path / "failed"
    with pytest.raises(ValueError, match="capacity exceeded"):
        run_initialization(initialization, output, observer=placement)
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["status"] == "failed" and metadata["completed_ticks"] == 1
    events = [json.loads(line) for line in (output / "events.jsonl").read_text().splitlines()]
    completed = next(
        e for e in events if e["event"] == "spatial_received" and e["position"] == list(NODE)
    )
    assert completed["packets"] == 2
    assert completed["received_fields"][0]["radiation"] == [4, -2, 6]
    assert completed["received_fields"][1]["radiation"] == [4, -2, 6]
    assert json.loads((output / "observations.json").read_text())["receipts"] == []
    assert metadata["final_totals"]["radiation"] == [8, -4, 12]


def test_remote_change_is_hidden_until_delivery_and_runner_stride_keeps_receipts(tmp_path):
    raw = pulse_document()
    changed = deepcopy(raw)
    changed["spatial_seeds"][0]["populations"][0] = [16, -8, 24]
    probes = [LocalObserver(ObserverDefinition(NODE)) for _ in range(2)]
    worlds = [
        Simulation(parse_initial_state(r), observer=p.receive)
        for r, p in zip((raw, changed), probes, strict=True)
    ]
    for world in worlds:
        world.step()
    assert probes[0].receipts == probes[1].receipts == []
    for world in worlds:
        world.step()
    assert probes[0].receipts[0]["values"] != probes[1].receipts[0]["values"]
    initialization, placement = tmp_path / "input.json", tmp_path / "probe.json"
    initialization.write_text(json.dumps(raw))
    placement.write_text(json.dumps({"position": NODE}))
    for name, stride, observer in (
        ("dense", 1, placement),
        ("sparse", 3, placement),
        ("plain", 1, None),
    ):
        run_initialization(initialization, tmp_path / name, frame_stride=stride, observer=observer)
    dense = json.loads((tmp_path / "dense/observations.json").read_text())
    sparse = json.loads((tmp_path / "sparse/observations.json").read_text())
    assert dense["receipts"] == sparse["receipts"]
    assert [s["received_count"] for s in dense["samples"]] == [0, 0, 1, 1]
    assert [s["received_count"] for s in sparse["samples"]] == [0, 1]
    for filename in ("state.json", "events.jsonl"):
        assert (tmp_path / "dense" / filename).read_bytes() == (
            tmp_path / "plain" / filename
        ).read_bytes()
    assert not (tmp_path / "dense/run.html").exists()


@pytest.mark.parametrize(
    "raw",
    [
        {"position": [True, 0, 0]},
        {"position": [5, 0, 0]},
        {"position": [0, 0, 0], "formula": "c*t"},
        {"position": [0, 0, 0], "max_receipts": 0},
    ],
)
def test_invalid_configuration_is_rejected_before_running(tmp_path, raw):
    path = tmp_path / "observer.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match="observer"):
        ObserverDefinition.load(path, (5, 5, 5))
