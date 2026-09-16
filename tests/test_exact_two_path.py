"""Independent finite-mode interference and atomic-failure expectations."""

import runpy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

EXAMPLE = Path(__file__).parents[1] / "examples/exact_two_path/run.py"
configuration = runpy.run_path(str(EXAMPLE))["configuration"]


@pytest.mark.parametrize(
    ("phase", "expected"),
    [
        ("zero", {"mode_a": (25, 0, 0), "mode_b": (0, 0, 0)}),
        ("quarter", {"mode_a": (9, 16, 0), "mode_b": (-12, 12, 0)}),
        ("half", {"mode_a": (-7, 0, 0), "mode_b": (-24, 0, 0)}),
    ],
)
def test_exact_modes_preserve_norm_and_causal_timing(phase, expected):
    events = []
    with Simulation(parse_initial_state(configuration(phase)), observer=events.append) as world:
        for _ in range(12):
            world.step()
            frame = world.snapshot()
            owners = [record for node in frame["nodes"] for record in node["disturbances"]]
            owners.extend(frame["transfers"])
            assert len(owners) == 2
            assert (
                sum(sum(value * value for value in owner["values"]["amplitude"]) for owner in owners)
                == 625
            )
            # Stored physical payloads use the engine's existing positive codec.
            assert all(
                code > 0
                for node in world.nodes.values()
                for record in node.records
                if record
                for value in record.values
                for code in value
            )
        receipts = [event for event in events if event["event"] == "received"]
        for mode, path in (
            ("mode_a", [(1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 2, 1)]),
            ("mode_b", [(0, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0), (2, 2, 1)]),
        ):
            selected = [event for event in receipts if event["disturbance"] == mode]
            assert [(event["tick"], tuple(event["position"])) for event in selected] == list(
                zip((2, 4, 6, 8, 10), path, strict=True)
            )
            assert tuple(selected[-1]["values"]["amplitude"]) == expected[mode]
        for event in events:
            if event["event"] == "sent":
                assert event["arrival_tick"] == event["tick"] + 1
            if event["event"] == "cycle_started":
                assert event["ready_tick"] == event["tick"] + 1
        assert world.tick == 12


def test_nonexact_division_rejects_before_local_commit():
    events = []
    with Simulation(parse_initial_state(configuration(amplitude=1)), observer=events.append) as world:
        before = world.snapshot()
        with pytest.raises(ValueError, match="exact_div"):
            world.step()
        assert world.snapshot() == before
        assert not events
        assert world.faulted
