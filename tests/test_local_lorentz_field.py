"""Configured field pulses act only after local arrival, with paired momentum."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/local_lorentz_field.json"


def document():
    return json.loads(EXAMPLE.read_text())


def record(world, position):
    return next(world.record_values(r) for r in world.cells[position].records if r is not None)


def test_local_pulse_applies_opposite_charge_impulses_after_four_links():
    world = Simulation(parse_initial_state(document()))
    totals = world.totals()
    initial = {y: record(world, (5, y, 1))["momentum"] for y in (1, 3, 5)}
    for tick in range(1, 21):
        world.step()
        for y, impulse in ((1, 100000), (3, -100000), (5, 0)):
            expected = impulse if tick >= 5 else 0
            assert record(world, (5, y, 1))["momentum"] == (initial[y][0], expected, 0)
            assert world.spatial_values((5, y, 1))["momentum"]["value"] == (0, -expected, 0)
        assert world.totals() == totals
        assert all(item["balanced"] for item in world.spatial_accounting().values())


def test_field_continues_autonomously_without_any_carrier():
    raw = document()
    raw["seeds"] = []
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    for _ in range(20):
        world.step()
        assert world.totals() == initial
        assert all(item["sources"] == (0, 0, 0) for item in world.spatial_accounting().values())
    assert world.spatial_accounting()["electric"]["current"] == (0, 600000, 0)


@pytest.mark.parametrize("remove", ["electric", "magnetic"])
def test_electric_and_magnetic_response_have_independent_expected_directions(remove):
    raw = document()
    raw["spatial_seeds"] = [seed for seed in raw["spatial_seeds"] if seed["field"] != remove]
    world = Simulation(parse_initial_state(raw))
    for _ in range(5):
        world.step()
    # v=(1,0,0), E=(0,200000,0), B=(0,0,300000), electron q=-1.
    expected = 300000 if remove == "electric" else -200000
    assert record(world, (5, 1, 1))["momentum"] == (100000, expected, 0)


def test_law_and_field_names_do_not_select_physics():
    raw = document()
    names = {entry["name"]: f"property_{i}" for i, entry in enumerate(raw["fields"])}
    names.update({entry["name"]: f"kind_{i}" for i, entry in enumerate(raw["disturbance_types"])})

    def rename(value):
        if isinstance(value, dict):
            return {names.get(k, k): rename(v) for k, v in value.items()}
        if isinstance(value, list):
            return [rename(v) for v in value]
        return names.get(value, value) if isinstance(value, str) else value

    changed = rename(deepcopy(raw))
    changed["fields"].reverse()
    changed["spatial_fields"].reverse()
    a = Simulation(parse_initial_state(raw))
    b = Simulation(parse_initial_state(changed))
    for _ in range(20):
        a.step()
        b.step()
        for y in (1, 3, 5):
            assert record(a, (5, y, 1))["momentum"] == record(b, (5, y, 1))[names["momentum"]]


def test_nonexact_velocity_is_rejected_without_partial_impulse():
    raw = document()
    raw["disturbance_types"][0]["defaults"]["momentum"] = [100001, 0, 0]
    world = Simulation(parse_initial_state(raw))
    for _ in range(4):
        world.step()
    with pytest.raises(ValueError):
        world.step()
    assert record(world, (5, 1, 1))["momentum"] == (100001, 0, 0)
    assert world.spatial_values((5, 1, 1))["momentum"]["value"] == (0, 0, 0)


def test_delayed_impulse_and_field_reaction_commit_together():
    raw = document()
    raw["normal_budget"] = 100
    world = Simulation(parse_initial_state(raw))
    changed = None
    for _ in range(32):
        world.step()
        py = record(world, (5, 1, 1))["momentum"][1]
        reaction = world.spatial_values((5, 1, 1))["momentum"]["value"][1]
        assert py + reaction == 0
        if py and changed is None:
            changed = world.tick
    assert changed is not None and changed > 5


def test_excessive_impulse_faults_without_partial_reaction():
    raw = document()
    raw["disturbance_types"][0]["defaults"]["charge"] = 100000000
    world = Simulation(parse_initial_state(raw))
    for _ in range(4):
        world.step()
    with pytest.raises(ValueError):
        world.step()
    assert record(world, (5, 1, 1))["momentum"] == (100000, 0, 0)
    assert world.spatial_values((5, 1, 1))["momentum"]["value"] == (0, 0, 0)


@pytest.mark.parametrize("link_ticks", [1, 2])
@pytest.mark.parametrize(
    "velocity,electric,magnetic,impulse_per_charge",
    [
        ((0, 0, 0), (0, 2, 0), (0, 0, 3), (0, 2, 0)),
        ((1, 2, -1), (0, 0, 0), (0, 0, 0), (0, 0, 0)),
        ((0, 0, 1), (0, 0, 0), (0, 0, 3), (0, 0, 0)),
        ((0, 0, 0), (2, -3, 4), (0, 0, 0), (2, -3, 4)),
        ((1, 0, 0), (0, 0, 0), (0, 0, 3), (0, -3, 0)),
        ((-1, 0, 0), (0, 0, 0), (0, 0, 3), (0, 3, 0)),
        ((0, 1, 0), (0, 0, 0), (3, 0, 0), (0, 0, -3)),
        ((0, -1, 0), (0, 0, 0), (3, 0, 0), (0, 0, 3)),
        ((0, 0, 1), (0, 0, 0), (0, 3, 0), (-3, 0, 0)),
        ((0, 0, -1), (0, 0, 0), (0, 3, 0), (3, 0, 0)),
        ((1, 2, -1), (1, -2, 0), (2, -1, 3), (6, -7, -5)),
    ],
    ids=["rest", "no-field", "parallel", "electric", "px", "mx", "py", "my", "pz", "mz", "oblique"],
)
def test_signed_three_species_impulses_wait_for_causal_field_delivery(
    link_ticks, velocity, electric, magnetic, impulse_per_charge
):
    """Tabulated impulses are independent of the configured expression evaluator."""
    raw = document()
    raw["link_ticks"] = link_ticks
    for kind in raw["disturbance_types"]:
        mass = kind["defaults"]["mass"]
        kind["defaults"]["momentum"] = [mass * v for v in velocity]
    for seed in raw["spatial_seeds"]:
        vector = electric if seed["field"] == "electric" else magnetic
        seed["populations"][0] = [100000 * v for v in vector]
    world = Simulation(parse_initial_state(raw))
    initial = {y: record(world, (5, y, 1)) for y in (1, 3, 5)}
    totals = world.totals()
    for tick in range(1, 4 * link_ticks + 4):
        world.step()
        for y in initial:
            values = initial[y]
            impulse = tuple(
                values["charge"][0] * 100000 * v if tick >= 4 * link_ticks + 1 else 0
                for v in impulse_per_charge
            )
            assert record(world, (5, y, 1))["momentum"] == tuple(
                p + dp for p, dp in zip(values["momentum"], impulse, strict=True)
            )
            assert world.spatial_values((5, y, 1))["momentum"]["value"] == tuple(-v for v in impulse)
        assert world.totals() == totals
        assert all(item["balanced"] for item in world.spatial_accounting().values())


def test_known_magnetic_impulse_energy_gap_remains_visible():
    """A transverse one-shot impulse is not an energy-preserving magnetic orbit."""
    raw = document()
    raw["spatial_seeds"] = [s for s in raw["spatial_seeds"] if s["field"] == "magnetic"]
    world = Simulation(parse_initial_state(raw))
    before = record(world, (5, 1, 1))
    for _ in range(5):
        world.step()
    after = record(world, (5, 1, 1))
    assert before["momentum"] == (100000, 0, 0)
    assert after["momentum"] == (100000, 300000, 0)
    # Classical kinetic energy p^2/(2m) grows despite exact paired momentum.
    assert sum(p * p for p in before["momentum"]) // (2 * before["mass"][0]) == 50000
    assert sum(p * p for p in after["momentum"]) // (2 * after["mass"][0]) == 500000
    assert world.totals()["momentum"] == (367583633, 0, 0)
