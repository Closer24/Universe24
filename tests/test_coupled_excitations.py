"""Independent state and causal checks for the configured unit-excitation candidate."""

import json
import runpy
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration as validate_canonical
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.initialization import parse_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/coupled-excitations"
PREPARE = runpy.run_path(str(EXAMPLE / "prepare.py"))
ZERO = (0, 0, 0)
X = (1, 0, 0)
Y = (0, 1, 0)
Z = (0, 0, 1)


def configuration(case="incoming_positive"):
    return PREPARE["configuration"](case)


def carrier(world, names=None):
    names = names or {}
    records = [
        (tuple(cell["position"]), record["values"])
        for cell in world.snapshot()["cells"]
        for record in cell["disturbances"]
    ]
    assert len(records) == 1
    position, values = records[0]
    return position, {
        name: tuple(values[names.get(name, name)]) for name in ("internal", "recoil", "coupling")
    }


def owned_amplitudes(world, name="amplitude"):
    """Count resident fields and actual packets, excluding pending plans and views."""
    snapshot = world.snapshot()
    result = []
    for node in snapshot["spatial_fields"]:
        value = tuple(node["fields"][name]["value"])
        if any(value):
            result.append(("node", tuple(node["position"]), value))
    for packet in snapshot["spatial_transfers"]:
        populations = packet["fields"].get(name, [])
        value = tuple(sum(population[axis] for population in populations) for axis in range(3))
        if any(value):
            result.append(("packet", tuple(packet["target"]), value))
    return result


def ledger(world, names=None):
    names = names or {}
    field_energy = sum(
        sum(component * component for component in value)
        for _, _, value in owned_amplitudes(world, names.get("amplitude", "amplitude"))
    )
    internal_energy = 0
    momentum = [field_energy, 0, 0]
    for cell in world.snapshot()["cells"]:
        for record in cell["disturbances"]:
            values = record["values"]
            internal_energy += sum(value * value for value in values[names.get("internal", "internal")])
            for axis, value in enumerate(values[names.get("recoil", "recoil")]):
                momentum[axis] += value
    return internal_energy + field_energy, tuple(momentum)


def gate(world, position, name="gate"):
    return world.spatial_values(position)[name]["value"]


def checked_steps(world, count, expected, names=None):
    assert ledger(world, names) == expected
    for _ in range(count):
        world.step()
        assert ledger(world, names) == expected
        assert all(row["balanced"] for row in world.spatial_accounting().values())


def amplitude_seed(raw):
    return next(seed for seed in raw["spatial_seeds"] if seed["field"] == "amplitude")


def gate_seed(raw):
    return next(seed for seed in raw["spatial_seeds"] if seed["field"] == "gate")


def carrier_values(raw):
    return raw["seeds"][0].setdefault("values", {})


@pytest.mark.parametrize(
    ("case", "internal", "recoil", "remaining"),
    [
        ("incoming_positive", Y, X, []),
        ("incoming_negative", (0, -1, 0), X, []),
        ("incoming_zero", ZERO, ZERO, [Y]),
    ],
)
def test_signed_absorption_and_zero_coupling_preserve_owned_occupancy_and_momentum(
    case,
    internal,
    recoil,
    remaining,
):
    raw = configuration(case)
    world = Simulation(parse_initial_state(raw))
    position, initial = carrier(world)
    assert initial["internal"] == initial["recoil"] == ZERO
    checked_steps(world, 5 * raw["link_ticks"], (1, X))
    assert carrier(world)[0] == position
    assert carrier(world)[1]["internal"] == internal
    assert carrier(world)[1]["recoil"] == recoil
    assert [value for _, _, value in owned_amplitudes(world)] == remaining
    assert gate(world, position) == (0,)


def test_explicit_emission_moves_one_owned_unit_into_the_field_with_opposite_recoil():
    raw = configuration("emission")
    world = Simulation(parse_initial_state(raw))
    position, values = carrier(world)
    assert values["internal"] == Y and values["recoil"] == ZERO
    assert owned_amplitudes(world) == []
    checked_steps(world, 4 * raw["link_ticks"], (1, ZERO))
    assert carrier(world)[1]["internal"] == ZERO
    assert carrier(world)[1]["recoil"] == (-1, 0, 0)
    assert [value for _, _, value in owned_amplitudes(world)] == [(0, -1, 0)]
    assert gate(world, position) == (0,)


def test_occupied_exchange_and_negative_inverse_restore_the_two_local_polarizations():
    raw = configuration("occupied_exchange")
    world = Simulation(parse_initial_state(raw))
    position, _ = carrier(world)
    checked_steps(world, 4 * raw["link_ticks"], (2, X))
    assert carrier(world)[1]["internal"] == Z
    assert carrier(world)[1]["recoil"] == ZERO
    assert [value for _, _, value in owned_amplitudes(world)] == [(0, -1, 0)]
    inverse = deepcopy(raw)
    carrier_values(inverse).update(internal=list(Z), recoil=list(ZERO), coupling=-1)
    amplitude_seed(inverse)["position"] = list(position)
    amplitude_seed(inverse)["populations"][0] = [0, -1, 0]
    reverse = Simulation(parse_initial_state(inverse))
    checked_steps(reverse, 2, (2, X))
    assert carrier(reverse)[1]["internal"] == Y
    assert carrier(reverse)[1]["recoil"] == ZERO
    assert [value for _, _, value in owned_amplitudes(reverse)] == [Z]
    assert gate(reverse, position) == (0,)


@pytest.mark.parametrize("link_ticks", [1, 3])
def test_receiver_cannot_absorb_before_two_causal_links_have_arrived(link_ticks):
    raw = configuration()
    raw["link_ticks"] = link_ticks
    world = Simulation(parse_initial_state(raw))
    position, before = carrier(world)
    changes = []
    saw_in_flight_owner = False
    for _ in range(2 * link_ticks + 3):
        checked_steps(world, 1, (1, X))
        owners = owned_amplitudes(world)
        saw_in_flight_owner |= any(kind == "packet" for kind, _, _ in owners)
        if world.tick < 2 * link_ticks:
            assert carrier(world)[1] == before
            assert gate(world, position) == (1,)
        if carrier(world)[1]["internal"] != before["internal"]:
            changes.append(world.tick)
    assert saw_in_flight_owner or link_ticks == 1
    assert changes and changes[0] >= 2 * link_ticks
    assert carrier(world)[1]["internal"] == Y


def test_waiting_gate_does_not_emit_without_an_explicit_emission_request():
    raw = configuration("emission")
    gate_seed(raw)["populations"][0] = 1
    world = Simulation(parse_initial_state(raw))
    position, before = carrier(world)
    checked_steps(world, 5, (1, ZERO))
    assert carrier(world)[1] == before
    assert gate(world, position) == (1,)
    assert owned_amplitudes(world) == []


def test_field_can_travel_independently_and_an_absent_receiver_does_not_release_its_gate():
    free = Simulation(parse_initial_state(configuration("free")))
    held = Simulation(parse_initial_state(configuration("absent_carrier")))
    checked_steps(free, 5, (1, X))
    checked_steps(held, 5, (1, X))
    assert all(not node["disturbances"] for node in free.snapshot()["cells"])
    assert all(not node["disturbances"] for node in held.snapshot()["cells"])
    assert owned_amplitudes(free) != owned_amplitudes(held)
    assert owned_amplitudes(held) == [("node", (4, 2, 2), Y)]
    assert gate(held, (4, 2, 2)) == (1,)


def test_low_budget_preserves_owned_state_until_the_frozen_exchange_commits():
    raw = configuration("delayed")
    world = Simulation(parse_initial_state(raw))
    position, before = carrier(world)
    # By tick four the two-link pulse has arrived and the exchange has been planned.
    checked_steps(world, 4, (1, X))
    pending = world.cells[position].pending
    assert pending is not None and pending.ready_tick > world.tick
    assert pending.plan.spatial_guards
    ready = pending.ready_tick
    while world.tick < ready:
        assert carrier(world)[1] == before
        assert gate(world, position) == (1,)
        assert owned_amplitudes(world) == [("node", position, Y)]
        checked_steps(world, 1, (1, X))
    assert carrier(world)[1]["internal"] == Y
    assert carrier(world)[1]["recoil"] == X
    assert gate(world, position) == (0,)
    assert owned_amplitudes(world) == []


def test_arrival_during_pending_exchange_rejects_stale_commit_without_releasing_gate():
    raw = configuration("delayed")
    position = tuple(raw["seeds"][0]["position"])
    raw["normal_budget"] = 50
    amplitude_seed(raw)["position"] = list(position)
    late = deepcopy(amplitude_seed(raw))
    late["position"][0] -= 1
    late["populations"][0] = [0, -1, 0]
    raw["spatial_seeds"].append(late)
    with pytest.raises(ValueError, match="one initial amplitude packet"):
        PREPARE["validate_configuration"](raw)
    # This deliberately violates the one-pulse envelope to challenge atomic commit.
    # The cancelling arrival is not claimed to conserve the nonlinear global ledger.
    world = Simulation(parse_initial_state(raw))
    before = carrier(world)[1]
    world.step()
    pending = world.cells[position].pending
    assert pending is not None and pending.plan.spatial_guards
    ready = pending.ready_tick
    assert ready > world.tick
    while world.tick < ready - 1:
        assert carrier(world)[1] == before
        assert gate(world, position) == (1,)
        world.step()
    assert world.spatial_values(position)["amplitude"]["value"] == ZERO
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    assert world.faulted
    assert carrier(world)[1] == before
    assert gate(world, position) == (1,)
    assert world.spatial_values(position)["amplitude"]["value"] == ZERO
    assert world.spatial_accounting()["amplitude"]["reactions"] == ZERO


def test_matched_interior_experiments_agree_in_nine_and_fifteen_node_cubes():
    worlds = []
    positions = []
    for size in (9, 15):
        raw = configuration("occupied_exchange")
        original = raw["seeds"][0]["position"]
        shift = [size // 2 - component for component in original]
        raw["shape"] = [size] * 3
        for seed in raw["seeds"] + raw["spatial_seeds"]:
            seed["position"] = [
                value + offset for value, offset in zip(seed["position"], shift, strict=True)
            ]
        PREPARE["validate_configuration"](raw)
        worlds.append(Simulation(parse_initial_state(raw)))
        positions.append((size // 2,) * 3)
    for _ in range(5):
        observations = []
        for world, center in zip(worlds, positions, strict=True):
            checked_steps(world, 1, (2, X))
            relative = [
                (
                    kind,
                    tuple(value - origin for value, origin in zip(location, center, strict=True)),
                    amplitude,
                )
                for kind, location, amplitude in owned_amplitudes(world)
            ]
            observations.append((carrier(world)[1], gate(world, center), relative))
        assert observations[0] == observations[1]


def test_field_type_and_rule_names_do_not_select_the_coupled_behavior():
    raw = configuration("occupied_exchange")
    names = {
        name: f"payload_{index}"
        for index, name in enumerate(
            ("internal", "amplitude", "recoil", "coupling", "gate", "excitation")
        )
    }
    names.update(
        {
            rule["name"]: f"configured_rule_{index}"
            for index, rule in enumerate(raw["field_rules"] + raw["spatial_interactions"])
        }
    )

    def rename(item):
        if isinstance(item, dict):
            return {names.get(key, key): rename(value) for key, value in item.items()}
        if isinstance(item, list):
            return [rename(value) for value in item]
        return names.get(item, item) if isinstance(item, str) else item

    changed = rename(raw)
    changed["fields"].reverse()
    changed["spatial_fields"].reverse()
    changed["disturbance_types"][0]["fields"].reverse()
    changed["model_id"] = "renamed-unit-exchange-test"
    world = Simulation(parse_initial_state(changed))
    checked_steps(world, 5, (2, X), names)
    position, state = carrier(world, names)
    assert state["internal"] == Z and state["recoil"] == ZERO
    assert gate(world, position, names["gate"]) == (0,)
    assert [value for _, _, value in owned_amplitudes(world, names["amplitude"])] == [(0, -1, 0)]


@pytest.mark.parametrize(
    "failure",
    [
        "coupling",
        "longitudinal_internal",
        "longitudinal_amplitude",
        "oversized_amplitude",
        "two_components",
        "gate",
        "baseline",
        "two_packets",
        "two_carriers",
        "remote_gate",
        "open",
    ],
)
def test_candidate_preflight_rejects_inputs_outside_its_explicit_envelope(failure):
    raw = configuration()
    if failure == "coupling":
        carrier_values(raw)["coupling"] = 2
    elif failure == "longitudinal_internal":
        carrier_values(raw)["internal"] = [1, 0, 0]
    elif failure == "longitudinal_amplitude":
        amplitude_seed(raw)["populations"][0] = [1, 0, 0]
    elif failure == "oversized_amplitude":
        amplitude_seed(raw)["populations"][0] = [0, 2, 0]
    elif failure == "two_components":
        amplitude_seed(raw)["populations"][0] = [0, 1, 1]
    elif failure == "gate":
        gate_seed(raw)["populations"][0] = 3
    elif failure == "baseline":
        next(field for field in raw["spatial_fields"] if field["field"] == "amplitude")["baseline"] = [
            0,
            1,
            0,
        ]
    elif failure == "two_packets":
        extra = deepcopy(amplitude_seed(raw))
        extra["position"][0] -= 1
        raw["spatial_seeds"].append(extra)
    elif failure == "two_carriers":
        extra = deepcopy(raw["seeds"][0])
        extra["position"][0] += 1
        raw["seeds"].append(extra)
    elif failure == "remote_gate":
        gate_seed(raw)["position"][0] += 1
    else:
        raw["boundary"] = "open"
    with pytest.raises((ValueError, OverflowError)):
        PREPARE["validate_configuration"](raw)


@pytest.mark.parametrize("failure", ["coupling", "internal", "amplitude", "gate"])
def test_runtime_guards_fault_without_repairing_invalid_state_or_releasing_the_gate(failure):
    raw = configuration()
    position = tuple(raw["seeds"][0]["position"])
    amplitude_seed(raw)["position"] = list(position)
    if failure == "coupling":
        carrier_values(raw)["coupling"] = 2
    elif failure == "internal":
        carrier_values(raw)["internal"] = [1, 0, 0]
    elif failure == "amplitude":
        amplitude_seed(raw)["populations"][0] = [0, 2, 0]
    else:
        gate_seed(raw)["populations"][0] = 3
    world = Simulation(parse_initial_state(raw))
    before = carrier(world)[1]
    initial_gate = gate(world, position)
    initial_amplitude = world.spatial_values(position)["amplitude"]["value"]
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert world.faulted
    assert carrier(world)[1] == before
    assert gate(world, position) == initial_gate
    assert world.spatial_values(position)["amplitude"]["value"] == initial_amplitude


def test_negative_transverse_z_unit_is_absorbed_without_changing_its_axis():
    raw = configuration()
    amplitude_seed(raw)["populations"][0] = [0, 0, -1]
    PREPARE["validate_configuration"](raw)
    world = Simulation(parse_initial_state(raw))
    checked_steps(world, 5, (1, X))
    assert carrier(world)[1]["internal"] == (0, 0, -1)
    assert carrier(world)[1]["recoil"] == X
    assert owned_amplitudes(world) == []


def test_candidate_rejects_a_schema_valid_ongoing_source():
    raw = configuration()
    raw["emissions"] = [
        {"type": "excitation", "field": "amplitude", "amount": [0, 1, 0], "source": True}
    ]
    parse_initial_state(raw)
    with pytest.raises(ValueError, match="ongoing sources"):
        PREPARE["validate_configuration"](raw)


@pytest.mark.parametrize("colocated", [False, True])
def test_emission_trigger_rejects_an_initial_pulse_even_before_it_can_arrive(colocated):
    raw = configuration()
    gate_seed(raw)["populations"][0] = 2
    if colocated:
        amplitude_seed(raw)["position"] = list(raw["seeds"][0]["position"])
    parse_initial_state(raw)
    with pytest.raises(ValueError, match="emission trigger.*initial amplitude packet"):
        PREPARE["validate_configuration"](raw)


def test_recoil_overflow_cannot_partially_absorb_a_unit_or_release_its_gate():
    raw = configuration()
    position = tuple(raw["seeds"][0]["position"])
    amplitude_seed(raw)["position"] = list(position)
    carrier_values(raw)["recoil"] = [MAX_VALUE, 0, 0]
    PREPARE["validate_configuration"](raw)
    world = Simulation(parse_initial_state(raw))
    before = carrier(world)[1]
    with pytest.raises(ValueError, match="integer bound"):
        world.step()
    assert world.faulted
    assert carrier(world)[1] == before
    assert gate(world, position) == (1,)
    assert owned_amplitudes(world) == [("node", position, Y)]
    assert world.spatial_accounting()["amplitude"]["reactions"] == ZERO


def test_zero_gate_forwards_the_pulse_past_a_present_coupled_carrier():
    raw = configuration()
    gate_seed(raw)["populations"][0] = 0
    PREPARE["validate_configuration"](raw)
    world = Simulation(parse_initial_state(raw))
    position, before = carrier(world)
    checked_steps(world, 5, (1, X))
    assert carrier(world)[1] == before
    assert gate(world, position) == (0,)
    owners = owned_amplitudes(world)
    assert [value for _, _, value in owners] == [Y]
    assert all(location != position for _, location, _ in owners)


def test_negative_emission_reverses_the_known_positive_absorption_state():
    raw = configuration("emission")
    carrier_values(raw).update(coupling=-1, recoil=list(X))
    PREPARE["validate_configuration"](raw)
    world = Simulation(parse_initial_state(raw))
    position, _ = carrier(world)
    checked_steps(world, 4, (1, X))
    assert carrier(world)[1]["internal"] == ZERO
    assert carrier(world)[1]["recoil"] == ZERO
    assert gate(world, position) == (0,)
    assert [value for _, _, value in owned_amplitudes(world)] == [Y]


def test_delayed_emission_commits_before_send_and_obeys_the_configured_link_delay():
    raw = configuration("emission")
    raw.update(normal_budget=200, link_ticks=3)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    position, before = carrier(world)
    checked_steps(world, 1, (1, ZERO))
    pending = world.cells[position].pending
    assert pending is not None and pending.ready_tick > world.tick
    ready = pending.ready_tick
    while world.tick < ready:
        assert carrier(world)[1] == before
        assert gate(world, position) == (2,)
        assert owned_amplitudes(world) == []
        assert not any(event["event"] == "spatial_sent" for event in events)
        checked_steps(world, 1, (1, ZERO))
    assert carrier(world)[1]["internal"] == ZERO
    assert carrier(world)[1]["recoil"] == (-1, 0, 0)
    assert gate(world, position) == (0,)
    checked_steps(world, raw["link_ticks"] + 2, (1, ZERO))
    commits = [event for event in events if event["event"] == "cycle_committed"]
    sends = [event for event in events if event["event"] == "spatial_sent"]
    receives = [event for event in events if event["event"] == "spatial_received"]
    assert commits[0]["tick"] == ready
    assert sends and receives
    first_send = sends[0]
    assert first_send["tick"] >= commits[0]["tick"]
    assert first_send["arrival_tick"] - first_send["tick"] == raw["link_ticks"]
    assert receives[0]["tick"] == first_send["arrival_tick"]
    assert tuple(receives[0]["position"]) == (position[0] + 1, position[1], position[2])


def test_prepare_cli_writes_a_standalone_valid_configuration_and_preserves_existing_output(tmp_path):
    output = tmp_path / "prepared.json"
    command = [
        sys.executable,
        str(EXAMPLE / "prepare.py"),
        "--case",
        "occupied_exchange",
        "--output",
        str(output),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr
    written = output.read_bytes()
    assert json.loads(written) == configuration("occupied_exchange")
    assert validate_canonical(written).valid
    protected = b"existing user-owned output\n"
    output.write_bytes(protected)
    refused = subprocess.run(command, capture_output=True, text=True, check=False)
    assert refused.returncode != 0
    assert output.read_bytes() == protected


def test_prepare_rejects_unknown_cases_and_unsupported_experiment_overrides(tmp_path, monkeypatch):
    with pytest.raises(ValueError, match="unknown experiment"):
        configuration("not_an_experiment")
    for name in ("law.json", "definition.json"):
        (tmp_path / name).write_bytes((EXAMPLE / name).read_bytes())
    (tmp_path / "experiments.json").write_text(
        json.dumps({"unsupported": {"boundary": "periodic"}}), encoding="utf-8"
    )
    monkeypatch.setitem(PREPARE["configuration"].__globals__, "HERE", tmp_path)
    with pytest.raises(ValueError, match="unsupported experiment option"):
        configuration("unsupported")
