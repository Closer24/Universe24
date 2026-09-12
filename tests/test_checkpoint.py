"""Exact continued trajectories and safe state IO across ownership boundaries."""

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.checkpoint import load_checkpoint, save_checkpoint
from event_universe.checkpoint_codec import canonical, decode, encode
from event_universe.checkpoint_quantum import capture_events, capture_quantum
from event_universe.checkpoint_validation import SPATIAL_FIELDS, WORLD_FIELDS
from event_universe.core.disturbance_state import pack
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease
from tests.test_disturbance_engine import document, kind
from tests.test_finite_spatial_engine import finite_document
from tests.test_native_event_runtime import configuration
from tests.test_native_quantum_channels import POSITION, config
from tests.test_spatial_coupling import document as spatial_document
from tests.test_units import example as calibrated_document

ROOT = Path(__file__).resolve().parents[1]


def scenario(name):
    if name == "delayed":
        return document(
            [kind("traveler", mode="move", weights=[1, 0, 0, 0, 0, 0])],
            [((2, 2, 2), "traveler")],
            budget=3,
            travel=3,
        )
    if name == "finite-open":
        raw = finite_document(moving=True, source=True, travel=2, budget=8)
        raw.update(boundary="open", shape=[3, 4, 5])
        raw["seeds"][0]["position"] = [2, 2, 2]
        raw["emissions"][0]["budget"] = 145
        return raw
    if name == "spatial-coupling":
        return spatial_document()
    if name == "native-delayed":
        raw = configuration()
        raw["normal_budget"] = 2
        return raw
    if name == "native":
        return configuration()
    if name == "mixed":
        return config({"channel": POSITION})
    if name == "grouped":
        raw = config()
        raw["event_program"]["layers"] = raw["event_program"]["layers"][:1]
        binding = raw["event_program"]["bindings"][0]
        binding.pop("instrument")
        binding["grouped_instrument"] = [POSITION]
        binding["codes"] = [1]
        raw["event_program"]["tickets"] = []
        return raw
    if name == "units":
        raw = calibrated_document()
        raw["unit_system"]["units"].append(
            {"name": "tiny_unused", "dimensions": [0] * 7, "si_scale": [1, 10**60]}
        )
        return raw
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def data_state(world):
    fresh = Simulation(world.initial)
    return encode(
        {
            "world": {name: getattr(world, name) for name in WORLD_FIELDS},
            "spatial": {name: getattr(world._spatial, name) for name in SPATIAL_FIELDS}
            if world._spatial
            else None,
            "events": capture_events(world),
            "quantum": capture_quantum(world, fresh),
        }
    )


@pytest.mark.parametrize(
    "name,cut,end",
    [
        ("basic.json", 3, 12),
        ("03-spreading-pulse.json", 2, 7),
        ("topology/bcc_vectors.json", 3, 10),
        ("delayed", 1, 18),
        ("finite-open", 3, 16),
        ("spatial-coupling", 2, 8),
        ("native", 0, 9),
        ("native", 3, 9),
        ("native", 5, 9),
        ("native-delayed", 3, 52),
        ("mixed", 2, 9),
        ("mixed", 5, 9),
        ("grouped", 5, 9),
        ("units", 1, 4),
        ("particle-contracts/electron-proton.json", 2, 18),
    ],
)
def test_restore_preserves_every_future_event_payload_phase_cost_and_total(tmp_path, name, cut, end):
    events = []
    world = Simulation(parse_initial_state(scenario(name)), observer=events.append)
    for _ in range(cut):
        world.step()
    before = data_state(world)
    path = save_checkpoint(world, tmp_path / "state.json")
    assert data_state(world) == before  # Saving is read-only, including query caches/counters.
    resumed_events = []
    resumed = load_checkpoint(path, observer=resumed_events.append)
    assert resumed_events == []  # Loading does not announce or replay seed events.
    assert data_state(resumed) == before
    assert resumed.snapshot() == world.snapshot()
    start = len(events)
    for _ in range(cut, end):
        world.step()
        resumed.step()
        assert resumed.snapshot() == world.snapshot()
        assert resumed.totals() == world.totals()
        assert resumed.source_totals() == world.source_totals()
        assert resumed.dissipation_totals() == world.dissipation_totals()
        assert resumed.escaped_totals() == world.escaped_totals()
        assert resumed.spatial_accounting() == world.spatial_accounting()
        assert resumed.computation_report() == world.computation_report()
    assert resumed_events == events[start:]
    assert data_state(resumed) == data_state(world)


def rewrite(path, update):
    envelope = json.loads(path.read_text())
    update(envelope["payload"])
    envelope["sha256"] = hashlib.sha256(canonical(envelope["payload"])).hexdigest()
    path.write_bytes(canonical(envelope))


@pytest.mark.parametrize(
    "damage", ["version", "source", "config", "type", "integer", "capacity", "pending", "resident"]
)
def test_corruption_is_rejected_before_returning_a_world(tmp_path, damage):
    world = Simulation(parse_initial_state(scenario("delayed")))
    world.step()
    original = data_state(world)
    path = save_checkpoint(world, tmp_path / "state.json")

    def alter(body):
        if damage == "version":
            body["version"] += 1
        elif damage == "source":
            body["runtime"]["source_sha256"] = "0" * 64
        elif damage == "config":
            raw = json.loads(body["initialization"])
            raw["normal_budget"] = 0
            body["initialization"] = json.dumps(raw)
            body["config_sha256"] = hashlib.sha256(body["initialization"].encode()).hexdigest()
        elif damage == "type":
            body["state"] = {"kind": "record", "type": "os.system", "values": ["never execute"]}
        else:
            state = decode(body["state"])
            cell = next(iter(state["world"]["_cells"].values()))
            if damage == "integer":
                state["world"]["tick"] = 1 << 70
            elif damage == "capacity":
                cell.records += (None,)
            elif damage == "resident":
                cell.records = (replace(cell.records[0], values=(pack((2,)),)), *cell.records[1:])
            else:
                pending = cell.pending
                departure = pending.plan.departures[0]
                inflated = replace(departure.record, values=(pack((2,)),))
                plan = replace(pending.plan, departures=(departure._replace(record=inflated),))
                cell.pending = replace(pending, plan=plan)
            body["state"] = encode(state)

    rewrite(path, alter)
    seen = []
    with pytest.raises(ValueError):
        load_checkpoint(path, observer=seen.append)
    assert not seen and data_state(world) == original


def test_checksum_and_duplicate_json_keys_fail_closed(tmp_path):
    world = Simulation(parse_initial_state(scenario("basic.json")))
    path = save_checkpoint(world, tmp_path / "state.json")
    envelope = json.loads(path.read_text())
    envelope["payload"]["version"] = 2
    path.write_bytes(canonical(envelope))
    with pytest.raises(ValueError):
        load_checkpoint(path)
    path.write_text('{"payload":{},"payload":{},"sha256":""}')
    with pytest.raises(ValueError, match="duplicate"):
        load_checkpoint(path)


def test_custom_component_unknown_state_and_missing_provenance_are_explicit(tmp_path):
    raw = scenario("basic.json")
    world = Simulation(parse_initial_state(raw))
    world._planner = lambda *_: None
    with pytest.raises(ValueError, match="replaced"):
        save_checkpoint(world, tmp_path / "custom.json")
    world = Simulation(parse_initial_state(raw))
    world.hidden_callback = lambda: None
    with pytest.raises(ValueError, match="injected"):
        save_checkpoint(world, tmp_path / "custom.json")
    world = Simulation(replace(parse_initial_state(raw), source_json=None))
    with pytest.raises(ValueError, match="original"):
        save_checkpoint(world, tmp_path / "custom.json")
    save_checkpoint(world, tmp_path / "explicit.json", initialization=json.dumps(raw))


def test_atomic_replace_failure_keeps_previous_checkpoint(tmp_path, monkeypatch):
    import event_universe.checkpoint as checkpoint

    world = Simulation(parse_initial_state(scenario("basic.json")))
    path = save_checkpoint(world, tmp_path / "state.json")
    original = path.read_bytes()
    world.step()

    def fail_replace(source, target):
        if Path(target) == path:
            raise OSError("simulated interrupted atomic replacement")
        return real_replace(source, target)

    real_replace = checkpoint.os.replace
    monkeypatch.setattr(checkpoint.os, "replace", fail_replace)
    with pytest.raises(OSError, match="interrupted"):
        save_checkpoint(world, path)
    assert path.read_bytes() == original
    assert load_checkpoint(path).tick == 0
    assert not list(tmp_path.glob("*.tmp"))


def test_checkpoint_can_share_runner_directory_lease_and_rejects_wrong_lease(tmp_path):
    output = tmp_path / "run"
    output.mkdir()
    world = Simulation(parse_initial_state(scenario("basic.json")))
    with ArtifactLease(tmp_path, [output]) as lease:
        path = save_checkpoint(world, output / "checkpoint.json", lease=lease)
        world.step()
        save_checkpoint(world, path, lease=lease)
        assert load_checkpoint(path).tick == 1
        with pytest.raises(ValueError, match="outside"):
            save_checkpoint(world, tmp_path / "outside.json", lease=lease)
    assert not (output / ".event-universe-retention").exists()


def test_checkpoint_refuses_to_overwrite_an_original_configuration(tmp_path):
    world = Simulation(parse_initial_state(scenario("basic.json")))
    path = tmp_path / "original.json"
    path.write_text(world.initial.source_json)
    original = path.read_bytes()
    with pytest.raises(ValueError):
        save_checkpoint(world, path)
    assert path.read_bytes() == original


@pytest.mark.parametrize("damage", ["active", "unsigned"])
def test_spatial_corruption_cannot_hide_stock_or_cancel_invalid_unsigned_bins(tmp_path, damage):
    raw = document([kind("unused")], [])
    raw["fields"][0]["signed"] = damage == "active"
    raw["spatial_fields"] = [{"field": "inventory", "transport": "local", "baseline": 0}]
    raw["spatial_seeds"] = [
        {"field": "inventory", "position": [2, 2, 2], "populations": [5, 0, 0, 0, 0, 0, 0, 0]}
    ]
    world = Simulation(parse_initial_state(raw))
    path = save_checkpoint(world, tmp_path / "state.json")

    def alter(body):
        state = decode(body["state"])
        spatial = state["spatial"]
        if damage == "active":
            spatial["_active"].clear()
        else:
            cell = next(iter(spatial["cells"].values()))
            values = cell.states[0]
            cell.states = (
                replace(values, populations=(pack((-1,)), pack((6,)), *values.populations[2:])),
            )
        body["state"] = encode(state)

    rewrite(path, alter)
    with pytest.raises(ValueError):
        load_checkpoint(path)


@pytest.mark.parametrize("damage", ["sites", "kind", "dimension", "outcome"])
def test_quantum_payload_must_match_saved_event_and_outcome_metadata(tmp_path, damage):
    world = Simulation(parse_initial_state(scenario("native")))
    for _ in range(5):
        world.step()
    path = save_checkpoint(world, tmp_path / "state.json")

    def alter(body):
        state = decode(body["state"])
        network = state["quantum"]["network"]
        identity = next(iter(network["_records"].values())).event_id
        value = network["_payloads"][identity]
        if damage == "sites":
            value = replace(value, sites=(1 - value.sites[0],))
        elif damage == "kind":
            value = replace(value, outcome=-1)
        elif damage == "dimension":
            value = replace(value, matrix=tuple(row[:1] for row in value.matrix[:1]))
        else:
            value = replace(value, outcome=1 - value.outcome)
        network["_payloads"][identity] = value
        body["state"] = encode(state)

    rewrite(path, alter)
    with pytest.raises(ValueError):
        load_checkpoint(path)


def test_saved_quantum_decisions_retain_identity_before_commit_and_after_compaction(tmp_path):
    world = Simulation(parse_initial_state(scenario("native")))
    world.step()
    resolver = world._resolver
    instrument = next(iter(resolver.bindings.values())).instrument
    prepared = resolver.space.prepare(901, 0, instrument)
    path = save_checkpoint(world, tmp_path / "pending.json")
    resumed = load_checkpoint(path)
    restored = resumed._resolver.space._prepared[901]
    assert restored == prepared
    first = resolver.space.commit(prepared, 0)
    second = resumed._resolver.space.commit(restored, 0)
    assert first == second
    assert resumed._resolver.space.commit(restored, 0) is second
    resolver.space.checkpoint(0)
    path = save_checkpoint(world, tmp_path / "compacted.json")
    compacted = load_checkpoint(path)
    assert data_state(compacted) == data_state(world)
    for _ in range(7):
        compacted.step()
        world.step()
        assert compacted.snapshot() == world.snapshot()
        assert compacted.computation_report() == world.computation_report()


@pytest.mark.parametrize("dynamic", [False, True])
def test_invalid_fractional_credit_is_rejected_before_the_next_step(tmp_path, dynamic):
    raw = document(
        [kind("traveler", mode="move", weights=[1, 0, 0, 0, 0, 0])],
        [((2, 2, 2), "traveler")],
        budget=1_000_000,
    )
    transport = raw["disturbance_types"][0]["transport"]
    transport.update(rate=3)
    transport["rate_divisor" if dynamic else "rate_denominator"] = 5
    world = Simulation(parse_initial_state(raw))
    world.step()
    path = save_checkpoint(world, tmp_path / "credit.json")

    def alter(body):
        state = decode(body["state"])
        cell = next(iter(state["world"]["_cells"].values()))
        assert cell.records[0].rate_remainder_code == 4
        cell.records = (replace(cell.records[0], rate_remainder_code=6), *cell.records[1:])
        body["state"] = encode(state)

    rewrite(path, alter)
    with pytest.raises(ValueError, match="credit"):
        load_checkpoint(path)
