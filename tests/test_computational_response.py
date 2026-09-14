"""Real one-link arrivals select opposite integer impulses in the example law."""

import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/computational-response/moving-pair.json"
DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
CENTER = (5, 5, 5)


def setup(port, response=1):
    raw = json.loads(EXAMPLE.read_text())
    raw["normal_budget"] = 1000000
    raw["emissions"] = []
    body = raw["disturbance_types"][0]
    body["transport"] = {"mode": "hold"}
    body["defaults"]["momentum"] = [0, 0, 0]
    body["defaults"]["response"] = response
    raw["seeds"] = [{"type": "mass_body", "position": list(CENTER)}]
    spatial = raw["spatial_fields"][0]
    spatial["axis_weights"] = [int(i == port // 2) for i in range(3)]
    # Outward populations carry their travel direction. A received port is the
    # travel direction of the last hop, not a bearing to a remote source.
    octant = (4, 2, 1)[port // 2] if port % 2 else 0
    populations = [[0, 0, 0] for _ in range(8)]
    populations[octant] = [64, 0, 0]
    origin = [a - b for a, b in zip(CENTER, DIRECTIONS[port], strict=True)]
    raw["spatial_seeds"] = [
        {"position": origin, "field": "computational_load", "populations": populations}
    ]
    return raw


def momentum(world):
    return next(world.record_values(r)["momentum"] for r in world.nodes[CENTER].records if r is not None)


@pytest.mark.parametrize("port", range(6))
def test_each_last_hop_selects_an_opposite_impulse_only_after_delivery(port):
    world = Simulation(parse_initial_state(setup(port)))
    world.step()
    assert momentum(world) == (0, 0, 0)
    world.step()
    expected = tuple(-v for v in DIRECTIONS[port])
    assert momentum(world) == expected
    assert world.spatial_values(CENTER)["momentum"]["value"] == DIRECTIONS[port]
    assert world.totals()["momentum"] == (0, 0, 0)
    world.step()
    assert momentum(world) == expected  # Delivered trigger does not persist.


def test_zero_response_property_disables_impulse_without_disabling_delivery():
    world = Simulation(parse_initial_state(setup(2, response=0)))
    world.step()
    assert world.spatial_values(CENTER)["computational_load"]["value"] == (64, 0, 0)
    world.step()
    assert momentum(world) == (0, 0, 0)
    assert world.totals()["momentum"] == (0, 0, 0)


def test_opposite_port_inputs_cancel_and_field_keeps_zero_net_reaction():
    raw = setup(0)
    raw["spatial_seeds"] += setup(1)["spatial_seeds"]
    world = Simulation(parse_initial_state(raw))
    world.step()
    world.step()
    assert momentum(world) == (0, 0, 0)
    assert world.spatial_values(CENTER)["momentum"]["value"] == (0, 0, 0)


def test_response_change_is_explicit_configuration_not_particle_name():
    raw = setup(4, response=-2)
    raw["disturbance_types"][0]["name"] = "unrelated_label"
    raw["seeds"][0]["type"] = "unrelated_label"
    world = Simulation(parse_initial_state(raw))
    world.step()
    world.step()
    assert momentum(world) == (0, 0, 2)
    assert world.totals()["momentum"] == (0, 0, 0)
