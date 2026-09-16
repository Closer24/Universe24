"""Independent ownership and local exchange expectations for the configured probe."""

import importlib.util
from pathlib import Path

import pytest

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
