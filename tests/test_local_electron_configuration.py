"""Independent values for the published displacement operation and source table."""

import importlib.util
import json
import sys
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe.core.disturbance_state import pack, unpack
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization


def load(name):
    location = Path(__file__).resolve().parents[1] / "examples/local-nucleus-electron" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, location)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


electron = load("electron_configuration")
calibration = load("electron_calibration")
strong = load("strong_configuration")


def configured(**parameters):
    defaults = {
        "force_numerator": 0,
        "force_denominator": 1,
        "source_enabled": 0,
        "mass": 1,
        "speed_scale": 10,
        "px": 3,
        "py": 4,
        "pz": 0,
        "launch_age": 0,
    }
    defaults.update(parameters)
    return electron.add_electron(
        strong.build_strong_document(parameters={"emission": 0}, shape=(41, 41, 41), ticks=6),
        parameters=defaults,
    )


def local_sequence(momenta, *, remainder=(0, 0, 0), launch_age=0):
    initial = parse_initial_state(configured(launch_age=launch_age))
    law = DisturbanceLaw(
        initial.fields,
        initial.disturbances,
        initial.couplings,
        initial.operation_costs,
        initial.interactions,
    )
    record = initial.seeds[-1].record
    names = {item.name: index for index, item in enumerate(initial.fields)}
    values = list(record.values)
    values[names["motion_remainder"]] = pack(remainder)
    record = replace(record, values=tuple(values))
    result = []
    for momentum in momenta:
        values = list(record.values)
        values[names["momentum"]] = pack(momentum)
        record = replace(record, values=tuple(values))
        plan = law((record,), (), 0)
        departure = plan.departures[0] if plan.departures else None
        record = departure.record if departure else dict(plan.replacements)[0]
        result.append(
            (
                departure.port if departure else None,
                unpack(record.values[names["motion_remainder"]]),
                unpack(record.values[names["age"]])[0],
            )
        )
    return result


def test_five_step_drift_has_independently_specified_displacement():
    sequence = local_sequence([(3, 4, 0)] * 5)
    assert [entry[0] for entry in sequence] == [None, None, 2, 0, 2]
    assert sequence[-1][1] == (5, 0, 0)
    assert tuple(
        10 * hop + remainder for hop, remainder in zip((1, 2, 0), sequence[-1][1], strict=True)
    ) == (15, 20, 0)


def test_changed_momentum_preserves_remainder_and_axis_tie_is_explicit():
    assert local_sequence([(6, 0, 0), (0, 6, 0), (4, 0, 0)])[-1][:2] == (0, (0, 6, 0))
    assert [entry[:2] for entry in local_sequence([(4, 4, 0), (0, 0, 0)], remainder=(6, 6, 0))] == [
        (0, (0, 10, 0)),
        (2, (0, 0, 0)),
    ]


def test_sign_reversal_and_rest():
    positive = local_sequence([(3, 4, 0)] * 5)
    negative = local_sequence([(-3, -4, 0)] * 5)
    assert [entry[0] for entry in negative] == [None, None, 3, 1, 3]
    assert all(a[1] == tuple(-value for value in b[1]) for a, b in zip(positive, negative, strict=True))
    assert all(entry[:2] == (None, (0, 0, 0)) for entry in local_sequence([(0, 0, 0)] * 8))


def test_release_age_reads_previous_age_and_speed_overflow_rejects():
    entries = local_sequence([(3, 4, 0)] * 4, launch_age=2)
    assert [entry[1] for entry in entries] == [(0, 0, 0), (0, 0, 0), (3, 4, 0), (6, 8, 0)]
    with pytest.raises(ValueError, match="one-hop"):
        configured(px=11, py=0)
    with pytest.raises(ValueError, match="admissible_one_hop_momentum"):
        local_sequence([(11, 0, 0)])


def test_builder_preserves_nuclear_operations_and_rejects_shared_conflict():
    original = strong.build_strong_document(parameters={}, shape=(41, 41, 41), ticks=832)
    before = deepcopy(original)
    combined = electron.add_electron(
        original, parameters={"force_numerator": 128, "force_denominator": 1}
    )
    assert original == before
    assert len(combined["fields"]) == 16
    assert combined["interactions"] == original["interactions"]
    assert combined["seeds"][:-1] == original["seeds"]
    assert combined["emissions"][:-1] == original["emissions"]
    assert "conservation" not in combined and "conservation" in original
    original["fields"][1]["signed"] = False
    with pytest.raises(ValueError, match="shared field charge"):
        electron.add_electron(original, parameters={"force_numerator": 0, "force_denominator": 1})


def test_source_table_and_passive_face_projection():
    heads = electron.source_headings()
    assert len(heads) == 2930 and len({tuple(h) for h in heads}) == 2930
    assert [sum(h[axis] for h in heads) for axis in range(3)] == [0, 0, 0]
    assert calibration.delivered_flux(
        [
            {"charge_field": [2]},
            {"charge_field": [7]},
            {},
            {"charge_field": [3]},
            {"charge_field": [4]},
            {},
        ]
    ) == (5, 3, -4)
    initial = parse_initial_state(calibration.calibration_document())
    assert not initial.spatial_couplings and initial.ticks == 84


@pytest.mark.parametrize(("age", "arrived", "expected"), [(63, 1, 0), (64, 0, 0), (64, 1, -128)])
def test_electron_response_requires_release_and_arrival_and_has_opposite_owner(age, arrived, expected):
    initial = parse_initial_state(
        configured(mass=512, speed_scale=16, px=0, py=2048, launch_age=64, force_numerator=128)
    )
    law = SpatialCouplingLaw(
        initial.fields, initial.spatial_couplings, initial.operation_costs, initial.spatial_fields
    )
    names = {item.name: index for index, item in enumerate(initial.fields)}
    record = initial.seeds[-1].record
    values = list(record.values)
    values[names["age"]] = pack((age,))
    record = replace(record, values=tuple(values))
    sample = tuple(pack((0,) * item.components) for item in initial.fields)
    flux = [pack((0, 0, 0)) for item in initial.fields]
    flux[names["charge_field"]] = pack((arrived, 0, 0))
    result = law((record,), sample, tuple(flux))
    assert unpack(result.records[0].values[names["momentum"]]) == (expected, 2048, 0)
    assert result.reaction[names["momentum"]] == (-expected, 0, 0)


def test_free_world_has_actual_canonical_artifact(tmp_path):
    document = configured()
    # This world is a free electron control, with no external source or nuclear records.
    document["seeds"] = document["seeds"][-1:]
    initial = tmp_path / "free-initialization.json"
    initial.write_text(json.dumps(document))
    run_initialization(initial, tmp_path / "run", visualize=True)
    metadata = json.loads((tmp_path / "run/run.json").read_text())
    assert metadata["status"] == "completed" and metadata["completed_ticks"] == 6
    assert metadata["accounting_balanced_at_every_completed_tick"]
    assert (tmp_path / "run/run.html").stat().st_size > 0
    events = [json.loads(line) for line in (tmp_path / "run/events.jsonl").read_text().splitlines()]
    departures = [event for event in events if event["event"] == "sent"]
    assert [event["port"] for event in departures[:3]] == [2, 0, 2]
