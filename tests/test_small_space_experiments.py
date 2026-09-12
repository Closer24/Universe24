"""Acceptance for new finite-reservoir and zero-total-momentum candidates."""

import importlib.util
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "small_space_experiments", ROOT / "examples/small-space/experiments.py"
)
EXPERIMENTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPERIMENTS)


def owned(world):
    frame = world.snapshot()
    return [row["values"] for cell in frame["cells"] for row in cell["disturbances"]] + [
        row["values"] for row in frame["transfers"]
    ]


def test_zero_total_unequal_mass_candidate_reflects_and_declines_nonzero_total():
    raw = EXPERIMENTS.candidates()["unequal-zero-total-candidate"]
    world = Simulation(parse_initial_state(raw))
    for tick in range(1, 9):
        world.step()
        assert world.totals() == {"mass": (3,), "charge": (0,), "momentum": (0, 0, 0)}
        assert sorted(value["mass"][0] for value in owned(world)) == [1, 2]
        assert all(sum(v * v for v in value["momentum"]) == 1 for value in owned(world))
        if tick == 4:
            # Independent classical unit check from measured displacement.
            initial_x = {1: 2, 2: 5}
            for cell in world.snapshot()["cells"]:
                for record in cell["disturbances"]:
                    mass = record["values"]["mass"][0]
                    displacement = cell["position"][0] - initial_x[mass]
                    assert (
                        displacement * mass * raw["fields"][2]["scale"]
                        == record["values"]["momentum"][0] * tick
                    )
    assert {v["mass"][0]: v["momentum"] for v in owned(world)} == {1: (-1, 0, 0), 2: (1, 0, 0)}
    # The same rule must not apply its simple swap to a general unequal pair.
    raw["seeds"][0]["position"] = raw["seeds"][1]["position"] = [4, 4, 4]
    raw["disturbance_types"][0]["defaults"]["momentum"] = [2, 0, 0]
    world = Simulation(parse_initial_state(raw))
    before = sorted((v["mass"], v["momentum"]) for v in owned(world))
    world.step()
    assert sorted((v["mass"], v["momentum"]) for v in owned(world)) == before


def test_finite_reservoir_debits_real_stock_and_stops_without_a_source():
    raw = EXPERIMENTS.candidates()["closed-reservoir"]
    name = raw["fields"][0]["name"]
    world = Simulation(parse_initial_state(raw))
    for expected in (2, 1, 0, 0, 0):
        world.step()
        assert owned(world)[0][name] == (expected,)
        assert world.totals()[name] == (3,)
        assert world.source_totals()[name] == (0,)
        balance = world.spatial_accounting()[name]
        assert balance["balanced"]
        assert balance["current"][0] + balance["escaped"][0] == 3 - expected


def test_source_receiver_waits_for_delivery_and_records_opposite_reaction():
    raw = EXPERIMENTS.candidates()["source-response-9"]
    world = Simulation(parse_initial_state(raw))
    for expected in (0, 36, 72):
        world.step()
        receiver = next(value for value in owned(world) if value.get("polarity") == (1,))
        assert receiver["momentum"] == (expected, 0, 0)
        assert world.totals()["momentum"] == (0, 0, 0)
        assert world.spatial_accounting()["momentum"]["current"] == (-expected, 0, 0)
