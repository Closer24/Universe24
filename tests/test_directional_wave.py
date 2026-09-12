"""Independent checks for the configured transverse directional-wave candidate."""

import copy
import itertools
import json
import runpy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/directional-wave"
PREPARE = runpy.run_path(str(EXAMPLE / "prepare.py"))
OBSERVE = runpy.run_path(str(EXAMPLE / "observe.py"))
CHANNELS = json.loads((EXAMPLE / "definition.json").read_text(encoding="utf-8"))["channels"]
NAMES = [channel["field"] for channel in CHANNELS]
PORTS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def configuration(case="approach_unequal"):
    return PREPARE["configuration"](case)


def measure(world):
    return OBSERVE["measure"](world.snapshot(), CHANNELS)


def run(raw, ticks=None):
    world = Simulation(parse_initial_state(raw))
    initial = measure(world)
    for _ in range(raw["ticks"] if ticks is None else ticks):
        world.step()
        current = measure(world)
        assert (current["energy"], current["momentum"]) == (initial["energy"], initial["momentum"])
        assert all(item["balanced"] for item in world.spatial_accounting().values())
    return world


def test_unequal_encounter_rotates_polarization_with_exact_energy_and_momentum():
    world = Simulation(parse_initial_state(configuration()))
    assert (measure(world)["energy"], measure(world)["momentum"]) == (13, (5, 0, 0))
    world.step()
    overlap = measure(world)["nodes"]
    assert len(overlap) == 1
    assert overlap[0]["electric"] == (0, 5, 0)
    assert overlap[0]["magnetic"] == (0, 0, 1)
    world.step()
    assert world.spatial_values((5, 4, 4))["a_px"]["value"] == (0, 0, 3)
    assert world.spatial_values((3, 4, 4))["a_mx"]["value"] == (0, 0, -2)
    assert (measure(world)["energy"], measure(world)["momentum"]) == (13, (5, 0, 0))


@pytest.mark.parametrize(
    "case",
    [
        "approach_unequal",
        "free_unequal",
        "coincident_electric",
        "coincident_magnetic",
        "six_way",
        "periodic_seam",
    ],
)
def test_saved_cases_preserve_declared_quantities_and_packet_direction(case):
    run(configuration(case))


@pytest.mark.parametrize(
    "case,expected_e,expected_b",
    [("coincident_electric", (0, 6, 0), (0, 0, 0)), ("coincident_magnetic", (0, 0, 0), (0, 0, 6))],
)
def test_coincident_modes_remain_real_when_one_aggregate_readout_vanishes(case, expected_e, expected_b):
    world = Simulation(parse_initial_state(configuration(case)))
    initial = measure(world)
    assert initial["nodes"][0]["electric"] == expected_e
    assert initial["nodes"][0]["magnetic"] == expected_b
    assert (initial["energy"], initial["momentum"]) == (18, (0, 0, 0))
    world.step()
    assert len(measure(world)["nodes"]) == 2
    assert measure(world)["energy"] == 18


def test_single_mode_propagates_without_collision_or_polarization_change():
    raw = configuration()
    raw["spatial_seeds"] = raw["spatial_seeds"][:1]
    world = run(raw, 27)
    assert world.spatial_values((3, 4, 4))["a_px"]["value"] == (0, 3, 0)
    assert (measure(world)["energy"], measure(world)["momentum"]) == (9, (9, 0, 0))


def test_nonparallel_polarizations_keep_unequal_mode_energies():
    raw = configuration("coincident_electric")
    raw["spatial_seeds"][0]["populations"][0] = [0, 3, 4]
    raw["spatial_seeds"][1]["populations"][0] = [0, -2, 1]
    world = run(raw, 1)
    assert world.spatial_values((5, 4, 4))["a_px"]["value"] == (0, -4, 3)
    assert world.spatial_values((3, 4, 4))["a_mx"]["value"] == (0, 1, 2)
    assert (measure(world)["energy"], measure(world)["momentum"]) == (30, (20, 0, 0))


def test_field_names_do_not_select_the_candidate_behavior():
    raw = configuration()
    channels = copy.deepcopy(CHANNELS)
    encoded = json.dumps(raw)
    for i, name in enumerate(NAMES):
        encoded = encoded.replace(json.dumps(name), json.dumps(f"mode_{i}"))
        channels[i]["field"] = f"mode_{i}"
    world = Simulation(parse_initial_state(json.loads(encoded)))
    for _ in range(20):
        world.step()
        observed = OBSERVE["measure"](world.snapshot(), channels)
        assert (observed["energy"], observed["momentum"]) == (13, (5, 0, 0))
    assert world.spatial_values((5, 4, 4))["mode_0"]["value"] == (0, 0, -3)


def test_all_axis_collisions_commute_and_leave_per_mode_energy_unchanged():
    raw = configuration("six_way")
    reordered = copy.deepcopy(raw)
    reordered["field_rules"][1:-1] = reversed(reordered["field_rules"][1:-1])
    reordered["spatial_seeds"].reverse()
    first, second = run(raw), run(reordered)
    assert canonical(first.snapshot()) == canonical(second.snapshot())
    assert (measure(first)["energy"], measure(first)["momentum"]) == (28, (0, 0, 0))


def test_dark_aggregate_is_not_zero_mode_energy():
    raw = configuration("coincident_electric")
    raw["spatial_seeds"] = [
        {"field": field, "position": [4, 4, 4], "populations": [[0, sign, 0]] + [[0, 0, 0]] * 7}
        for field, sign in [("a_px", 1), ("a_mx", 1), ("a_pz", -1), ("a_mz", -1)]
    ]
    world = Simulation(parse_initial_state(raw))
    diagnostic = measure(world)
    assert diagnostic["nodes"][0]["electric"] == diagnostic["nodes"][0]["magnetic"] == (0, 0, 0)
    assert diagnostic["energy"] == 4
    assert len(diagnostic["nodes"][0]["modes"]) == 4
    run(raw)


@pytest.mark.parametrize("failure", ["longitudinal", "bound", "misroute", "amplify"])
def test_invalid_proposals_are_rejected_without_installing_a_partial_state(failure):
    raw = configuration("coincident_electric")
    if failure in ("longitudinal", "bound"):
        raw["spatial_seeds"] = raw["spatial_seeds"][:1]
        raw["spatial_seeds"][0]["populations"][0] = (
            [1, 3, 0] if failure == "longitudinal" else [0, MAX_VALUE // 2 + 1, 0]
        )
        expected = "a_px_unchanged"
    elif failure == "misroute":
        next(a for a in raw["field_rules"][-1]["assignments"] if a.get("port") == 0)["port"] = 2
        expected = "a_px_momentum"
    else:
        assignment = raw["field_rules"][1]["assignments"][0]
        assignment["expression"] = {"op": "mul", "args": [2, assignment["expression"]]}
        expected = "a_px_energy"
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()
    with pytest.raises(ValueError, match=expected):
        world.step()
    assert world.faulted
    assert world.snapshot() == before


def test_declared_amplitude_boundary_keeps_quarter_turn_deltas_bounded():
    limit = json.loads((EXAMPLE / "definition.json").read_text(encoding="utf-8"))["max_abs_component"]
    assert limit == MAX_VALUE // 2
    raw = configuration("six_way")
    for seed, direction in zip(raw["spatial_seeds"], PORTS, strict=True):
        seed["position"] = [4, 4, 4]
        seed["populations"][0] = [limit if n == 0 else 0 for n in direction]
    world = run(raw, 36)
    assert (measure(world)["energy"], measure(world)["momentum"]) == (12 * limit * limit, (0, 0, 0))


def rotations():
    for axes in itertools.permutations(range(3)):
        parity = (-1) ** sum(axes[i] > axes[j] for i in range(3) for j in range(i + 1, 3))
        for signs in itertools.product((1, -1), repeat=3):
            if parity * signs[0] * signs[1] * signs[2] == 1:
                yield axes, signs


IDENTITY = ((0, 1, 2), (1, 1, 1))


def rotate(vector, rotation=IDENTITY):
    axes, signs = rotation
    result = [0, 0, 0]
    for i in range(3):
        result[axes[i]] = signs[i] * vector[i]
    return tuple(result)


def transformed_input(raw, rotation=IDENTITY, shift=(0, 0, 0)):
    changed = copy.deepcopy(raw)
    n = raw["shape"][0]
    for seed in changed["spatial_seeds"]:
        p = rotate([v - n // 2 for v in seed["position"]], rotation)
        seed["position"] = [(v + n // 2 + d) % n for v, d in zip(p, shift, strict=True)]
        seed["field"] = NAMES[PORTS.index(rotate(PORTS[NAMES.index(seed["field"])], rotation))]
        seed["populations"] = [list(rotate(v, rotation)) for v in seed["populations"]]
    assert changed["field_rules"] == raw["field_rules"]
    return changed


def canonical(snapshot, n=9, rotation=IDENTITY, shift=(0, 0, 0)):
    axes, signs = rotation
    inv = (tuple(axes.index(i) for i in range(3)), tuple(signs[axes.index(i)] for i in range(3)))

    def position(p):
        return tuple(
            (v + n // 2) % n for v in rotate([(p[i] - shift[i] - n // 2) % n for i in range(3)], inv)
        )

    rows = []
    for node in snapshot["spatial_fields"]:
        for name in NAMES:
            state = node["fields"][name]
            if not any(state["value"]) and not any(any(v) for v in state["directions"]):
                continue
            port = PORTS.index(rotate(PORTS[NAMES.index(name)], inv))
            channels = sorted(
                (PORTS.index(rotate(PORTS[p], inv)), rotate(v, inv))
                for p, v in enumerate(state["directions"])
                if any(v)
            )
            rows.append(
                ("node", position(node["position"]), port, rotate(state["value"], inv), channels)
            )
    for packet in snapshot["spatial_transfers"]:
        for name in NAMES:
            value = tuple(sum(v[i] for v in packet["fields"][name]) for i in range(3))
            if any(value):
                rows.append(
                    (
                        "link",
                        position(packet["origin"]),
                        position(packet["target"]),
                        PORTS.index(rotate(PORTS[NAMES.index(name)], inv)),
                        PORTS.index(rotate(PORTS[packet["port"]], inv)),
                        packet["arrival_tick"] - snapshot["tick"],
                        rotate(value, inv),
                    )
                )
    return sorted(rows, key=repr)


@pytest.mark.parametrize("rotation", list(rotations()))
def test_same_law_is_covariant_under_proper_cubic_rotations(rotation):
    raw = configuration()
    first = Simulation(parse_initial_state(raw))
    second = Simulation(parse_initial_state(transformed_input(raw, rotation)))
    for _ in range(12):
        first.step()
        second.step()
        assert canonical(first.snapshot()) == canonical(second.snapshot(), rotation=rotation)
        assert measure(second)["momentum"] == rotate((5, 0, 0), rotation)
        assert measure(second)["energy"] == 13


def test_periodic_seam_translation_preserves_full_state():
    raw = configuration()
    first = Simulation(parse_initial_state(raw))
    shift = (5, 2, 1)
    second = Simulation(parse_initial_state(transformed_input(raw, shift=shift)))
    for _ in range(37):
        first.step()
        second.step()
        assert canonical(first.snapshot()) == canonical(second.snapshot(), shift=shift)


@pytest.mark.parametrize("link_ticks", [1, 2])
def test_four_encounters_restore_polarization_and_complete_field_phase(link_ticks):
    raw = configuration()
    raw["link_ticks"] = link_ticks
    world = Simulation(parse_initial_state(raw))
    for _ in range(link_ticks):
        world.step()
    first = canonical(world.snapshot())
    for _ in range(36 * link_ticks):
        world.step()
        assert (measure(world)["energy"], measure(world)["momentum"]) == (13, (5, 0, 0))
    assert canonical(world.snapshot()) == first


def test_even_lattice_and_double_link_keep_energy_momentum_and_causal_ports():
    raw = configuration()
    raw["shape"] = [8] * 3
    raw["link_ticks"] = 2
    run(raw, 64)


def test_in_flight_readouts_preserve_actual_modes_before_arrival():
    raw = configuration()
    raw["link_ticks"] = 2
    world = Simulation(parse_initial_state(raw))
    world.step()
    result = measure(world)
    assert not result["nodes"]
    assert len(result["transfers"]) == 2
    assert {p["arrival_tick"] for p in result["transfers"]} == {2}
    assert sorted(p["energy"] for p in result["transfers"]) == [4, 9]
    assert (result["energy"], result["momentum"]) == (13, (5, 0, 0))


def test_ordinary_runner_accepts_component_rotations_and_tracks_transformations(tmp_path):
    initial = tmp_path / "input.json"
    initial.write_text(json.dumps(configuration()), encoding="utf-8")
    path = run_initialization(initial, tmp_path / "run", ticks=3)
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["status"] == "completed"
    assert report["accounting_balanced_at_every_completed_tick"]
    assert report["spatial_accounting"]["a_px"]["transformations"] == [0, -3, 3]
    assert not (tmp_path / "run/run.html").exists()
