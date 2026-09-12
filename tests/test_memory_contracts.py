"""Small permanent checks for bounded host storage and physical ownership."""

import json
from io import StringIO

import pytest

from event_universe import Simulation
from event_universe.archive import JsonArchive, write_json
from event_universe.core.disturbance_state import decode
from event_universe.diagnostics.local_observer import LocalObserver, ObserverDefinition
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_disturbance_engine import document, exchange_document, kind


def test_maximum_coupling_defaults_share_immutable_storage_before_and_after_work():
    raw = exchange_document(1, 3)
    rule = raw["couplings"][0]
    raw["couplings"] = [{**rule, "name": f"exchange_{i}"} for i in range(32)]
    raw["seeds"] = [{"position": [i, 0, 0], "type": "left"} for i in range(3)]
    raw["disturbance_types"][0]["defaults"]["inventory"] = 1
    with Simulation(parse_initial_state(raw)) as world:
        before = [cell.coupling_remainders for cell in world.cells.values()]
        assert len(before[0]) == 3 * 32 * 32 * 32
        assert all(item is before[0] for item in before)
        assert isinstance(before[0], tuple) and set(before[0]) == {1}
        world.step()
        assert world.computation_report()["local_cycles_started"] == 3
        assert all(cell.coupling_remainders is before[0] for cell in world.cells.values())
        assert world.totals() == {"inventory": (3,)}


def test_nonzero_pending_remainders_do_not_modify_other_cells_or_simulations():
    raw = exchange_document(1, 3)
    raw.update(slots_per_cell=2, normal_budget=1)
    raw["seeds"].append({"position": [3, 2, 2], "type": "left"})
    initial = parse_initial_state(raw)
    with Simulation(initial) as world, Simulation(initial) as untouched:
        original = world.cells[(2, 2, 2)].coupling_remainders
        world.step()
        pending = world.cells[(2, 2, 2)].pending
        assert pending is not None and pending.ready_tick > world.tick
        assert any(decode(value) == 1 for value in pending.plan.coupling_remainders)
        assert world.cells[(2, 2, 2)].coupling_remainders is original
        while world.tick < pending.ready_tick:
            world.step()
        assert world.cells[(2, 2, 2)].pending is None
        assert any(decode(value) == 1 for value in world.cells[(2, 2, 2)].coupling_remainders)
        assert set(original) == {1}
        assert world.cells[(3, 2, 2)].coupling_remainders is original
        assert all(set(cell.coupling_remainders) == {1} for cell in untouched.cells.values())
        assert world.totals() == untouched.totals() == {"inventory": (0,)}


def test_periodic_motion_retains_domain_history_with_shared_empty_packet_arrays():
    raw = document(
        [kind("traveler", mode="move", weights=[1, 0, 0, 0, 0, 0])],
        [((0, 0, 0), "traveler")],
        capacity=2,
    )
    raw["shape"] = [8, 1, 1]
    with Simulation(parse_initial_state(raw)) as world:
        for _ in range(16):
            world.step()
        retained = tuple(world.cells), tuple(world.links)
        for _ in range(64):
            world.step()
        assert retained == (tuple(world.cells), tuple(world.links))
        assert len(world.cells) == len(world.links) == 8
        assert len({id(slots) for slots in world.links.values()}) == 1
        assert all(packet is None for slots in world.links.values() for packet in slots)
        assert not world._links._due and not world._links._ticks
        assert not world._pending_due
        assert world.totals() == {"inventory": (1,)}


def test_disk_observer_preserves_same_tick_prefixes_and_atomic_capacity_failure(tmp_path):
    with JsonArchive(tmp_path) as receipts, JsonArchive(tmp_path) as samples:
        probe = LocalObserver(
            ObserverDefinition((0, 0, 0), max_receipts=2), receipts=receipts, samples=samples
        )
        probe.capture(0)
        probe.receive({"event": "cycle_committed", "position": (0, 0, 0)})
        probe.receive(
            {
                "event": "received",
                "position": (0, 0, 0),
                "port": 4,
                "disturbance": "__proto__",
                "values": {"inventory": [-3]},
            }
        )
        probe.capture(0)
        with pytest.raises(ValueError, match="capacity exceeded"):
            probe.receive(
                {
                    "event": "spatial_received",
                    "position": (0, 0, 0),
                    "received_fields": [{"inventory": [0]}, {"inventory": [2]}, {}, {}, {}, {}],
                }
            )
        probe.capture(1)
        output = StringIO()
        write_json(output, probe.recording())
        stored = json.loads(output.getvalue())
        assert stored["samples"] == [
            {"audit_tick": 0, "clock": 0, "received_count": 0},
            {"audit_tick": 0, "clock": 1, "received_count": 1},
            {"audit_tick": 1, "clock": 1, "received_count": 1},
        ]
        assert stored["receipts"] == [
            {
                "sequence": 1,
                "clock": 1,
                "kind": "disturbance",
                "port": 4,
                "label": "__proto__",
                "values": {"inventory": [-3]},
            }
        ]
    assert receipts.closed and samples.closed


def test_failed_runner_exports_every_observer_capture_without_retaining_archives(tmp_path):
    raw = document(
        [kind("traveler", mode="move", weights=[1, 0, 0, 0, 0, 0])],
        [((0, 0, 0), "traveler")],
        capacity=1,
    )
    raw.update(shape=[2, 1, 1], observer={"position": [1, 0, 0], "max_receipts": 1})
    source, output = tmp_path / "input.json", tmp_path / "run"
    source.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="capacity exceeded"):
        run_initialization(source, output, ticks=4)
    recording = json.loads((output / "observations.json").read_text(encoding="utf-8"))
    assert recording["samples"] == [
        {"audit_tick": 0, "clock": 0, "received_count": 0},
        {"audit_tick": 1, "clock": 0, "received_count": 1},
        {"audit_tick": 2, "clock": 1, "received_count": 1},
        {"audit_tick": 3, "clock": 1, "received_count": 1},
    ]
    assert len(recording["receipts"]) == 1
    metadata = json.loads((output / "run.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "failed" and metadata["completed_ticks"] == 2
    assert metadata["tick"] == 3 and metadata["execution"]["closed"]
    events = [json.loads(line) for line in (output / "events.jsonl").read_text().splitlines()]
    assert events[-1]["event"] == "received" and events[-1]["tick"] == 3


def test_archive_export_uses_bounded_chunks_without_materializing_history(tmp_path, monkeypatch):
    with JsonArchive(tmp_path) as archive:
        archive.append({"payload": "x" * 140_000})
        for tick in range(512):
            archive.append({"audit_tick": tick, "clock": 0, "received_count": 0})
        assert len(archive) == 513
        assert archive[-1] == {"audit_tick": 511, "clock": 0, "received_count": 0}

        def no_history_reads(self, index):
            pytest.fail("export decoded stored history instead of streaming bounded chunks")

        monkeypatch.setattr(JsonArchive, "__getitem__", no_history_reads)
        count = total = 0
        for chunk in archive.json_chunks():
            assert len(chunk) <= 65536
            total += len(chunk)
            count += 1
        assert total > 140_000 and count > 513
        assert not any(isinstance(value, (list, dict, set)) for value in vars(archive).values())
