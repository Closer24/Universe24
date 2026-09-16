"""Independent ownership and local exchange expectations for the configured probe."""

import importlib.util
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "property_packet_benchmark", ROOT / "examples/property_packet/run_benchmark.py"
)
benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(benchmark)


@pytest.mark.parametrize("case", benchmark.CASES)
def test_transport_and_atomic_exchange(case, tmp_path):
    result = benchmark.run_case(case, tmp_path / case)
    changed = case not in ("zero_coupling", "missing_property")
    assert result["status"] == "completed"
    assert result["conserved_at_every_completed_tick"]
    observations = result["observations"]
    assert len(observations) == 19
    seen_owners = set()
    seen_positions = set()
    for sample in observations:
        carrier, reservoir = sample["carrier"], sample["reservoir"]
        seen_owners.add(sample["ownership"])
        seen_positions.add(tuple(sample["position"]))
        assert carrier["inventory"] == [1]
        assert carrier["charge"] == [-1]
        assert carrier["phase"] == [3]
        assert carrier["heading"] == [1, 0, 0]
        assert carrier["energy_ledger"][0] + reservoir["energy_ledger"][0] == 7
        assert [a + b for a, b in zip(carrier["momentum"], reservoir["momentum"], strict=True)] == [
            1,
            0,
            0,
        ]
        # An accepted joint transition changes both owners at the same commit.
        allowed = [(2, 5, [1, 0, 0], [0, 0, 0])]
        if changed:
            allowed.append((3, 4, [1, 2, 0], [0, -2, 0]))
        assert (
            carrier["energy_ledger"][0],
            reservoir["energy_ledger"][0],
            carrier["momentum"],
            reservoir["momentum"],
        ) in allowed
    assert seen_positions == {(x, 2, 2) for x in range(6)}
    assert "resident" in seen_owners
    final = observations[-1]
    assert final["carrier"]["energy_ledger"] == ([3] if changed else [2])
    assert final["reservoir"]["energy_ledger"] == ([4] if changed else [5])
    assert (tmp_path / case / "run/run.html").is_file()


def test_actual_in_flight_packet_has_no_resident_duplicate(tmp_path):
    raw, _ = benchmark.configuration("exchange")
    frames = []

    def observe(event):
        if event["event"] != "sent":
            return
        # Observe the actual committed Link owner before the subsequent receipt.
        inventory = world.inventory_view()
        resident = [record for node in inventory.nodes for record in node.records if record is not None]
        in_flight = [packet for packet in inventory.packets if packet.kind == "carrier"]
        assert resident == []
        assert len(in_flight) == 1
        assert in_flight[0].arrival_tick == event["tick"] + 1
        frames.append(world.snapshot())

    with Simulation(parse_initial_state(raw), observer=observe) as world:
        for _ in range(raw["ticks"]):
            world.step()
    assert len(frames) == 17
    assert all(len(frame["transfers"]) == 1 for frame in frames)
    render_disturbances(
        frames,
        tmp_path / "in_flight_ownership.html",
        {"scope": "actual committed packet owners before receipt", "model": raw["model_id"]},
    )
