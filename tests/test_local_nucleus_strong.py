"""Independent contact-energy and localization checks for the declared pilot."""

import importlib.util
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

SPEC = importlib.util.spec_from_file_location(
    "strong_configuration",
    Path(__file__).resolve().parents[1] / "examples/local-nucleus-electron/strong_configuration.py",
)
STRONG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STRONG)


def residents(snapshot):
    return [
        (tuple(node["position"]), record)
        for node in snapshot["nodes"]
        for record in node["disturbances"]
    ]


def test_capture_funds_one_radiation_batch_and_keeps_two_movable_records():
    raw = STRONG.build_strong_document(parameters={}, shape=(9, 9, 9), ticks=24)
    events = []
    with Simulation(parse_initial_state(raw), observer=events.append) as world:
        world.step()
        assert len(residents(world.snapshot())) == 2
        for position, record in residents(world.snapshot()):
            assert position == (4, 4, 4)
            assert record["values"]["momentum"] == (0, 0, 0)
            assert record["values"]["bound"] == (1,)
            assert record["values"]["radiation"] == (335414598,)
        for _ in range(23):
            world.step()
        assert len(residents(world.snapshot())) == 2
        assert {row[1]["type"] for row in residents(world.snapshot())} == {"proton", "neutron"}
        assert all(row[1]["values"]["radiation"] == (0,) for row in residents(world.snapshot()))
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert report["initial"] == {"energy": 940032, "momentum": (0, 0, 0)}
        assert report["current"]["energy"] + report["escaped"]["energy"] == 940032
        assert report["current"]["momentum"] == report["escaped"]["momentum"] == (0, 0, 0)
        assert all(kind.transport.mode == "move" for kind in world.initial.disturbances)
    emissions = [
        event for event in events if event["event"] == "spatial_sent" and event["position"] == (4, 4, 4)
    ]
    assert len(emissions) == 6
    assert {event["tick"] for event in emissions} == {1}


@pytest.mark.parametrize("axis", range(3))
@pytest.mark.parametrize("boost", [0, 1])
def test_disabled_pair_separates_and_boosted_capture_translates(axis, boost):
    raw = STRONG.build_strong_document(
        parameters={"coupling": boost, "boost": boost, "emission": 0, "axis": axis},
        shape=(9, 9, 9),
        ticks=32,
    )
    with Simulation(parse_initial_state(raw)) as world:
        for _ in range(32):
            world.step()
        rows = residents(world.snapshot())
        assert len(rows) == 2
        offsets = [position[axis] - 4 for position, _ in rows]
        assert sorted(offsets) == ([2, 2] if boost else [-2, 2])
        assert all(record["values"]["bound"] == (boost,) for _, record in rows)
        assert world.conservation_report()["status"] == "passed"
        assert world.conservation_report()["current"]["momentum"][axis] == 1880064 * boost


@pytest.mark.parametrize(
    "left,right,kick,expected_sector,expected_offsets",
    [
        (334944581, 334944582, 0, 1, [0, 0]),
        (334944582, 334944582, 0, 2, [0, 0]),
        (335414598, 335414598, 940032, 2, [-2, 2]),
    ],
)
def test_breakup_requires_actual_funding_and_outgoing_pair_does_not_recapture(
    left, right, kick, expected_sector, expected_offsets
):
    raw = STRONG.build_strong_document(
        parameters={
            "initial_bound": 1,
            "excitation_left": left,
            "excitation_right": right,
            "release_kick": kick,
            "emission": 0,
        },
        shape=(9, 9, 9),
        ticks=32,
    )
    with Simulation(parse_initial_state(raw)) as world:
        for _ in range(32):
            world.step()
        rows = residents(world.snapshot())
        assert len(rows) == 2
        assert sorted(position[0] - 4 for position, _ in rows) == expected_offsets
        assert all(record["values"]["sector"] == (expected_sector,) for _, record in rows)
        remaining = sorted(record["values"]["excitation"][0] for _, record in rows)
        assert remaining == ([left, right] if expected_sector == 1 else [0, 0])
        assert world.conservation_report()["status"] == "passed"
        assert world.conservation_report()["current"]["energy"] == left + right - 669889164


def test_nonexact_capture_rejects_without_partial_binding_or_radiation():
    raw = STRONG.build_strong_document(parameters={"emission": 0}, shape=(9, 9, 9), ticks=1)
    # Disable only the optional passive energy audit so transaction exactness is tested.
    raw.pop("conservation")
    raw["disturbance_types"][0]["defaults"]["momentum"][0] += 1
    with Simulation(parse_initial_state(raw)) as world:
        before = residents(world.snapshot())
        with pytest.raises(ValueError, match="exact"):
            world.step()
        assert residents(world.snapshot()) == before


@pytest.mark.parametrize("parameters", [{"release_kick": 1}, {"boost": 1}, {"coupling": 2}])
def test_unsupported_candidate_compositions_reject_before_world(parameters):
    with pytest.raises(ValueError):
        STRONG.build_strong_document(parameters=parameters, shape=(9, 9, 9), ticks=1)
