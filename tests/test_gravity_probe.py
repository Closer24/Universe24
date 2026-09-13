"""Gravity probe: attraction toward a ray source is mass proportional and conserving."""

import importlib.util
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "gravity_probe", ROOT / "examples/gravity-probe/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def small_world():
    PROBE.SIZE, PROBE.CENTER = 15, 7
    PROBE.HEADINGS, PROBE.RAYS_PER_TICK = 6, 6
    PROBE.STEPS = {"axis": (2, 4), "face_diagonal": (), "body_diagonal": ()}


def axis_headings():
    """Six axis rays per tick: every axis Node receives one sixth of the emission each tick."""
    return [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]


def test_held_bodies_gain_momentum_toward_the_source_in_proportion_to_mass():
    small_world()
    raw = PROBE.held_document(6)
    raw["spatial_fields"][0]["headings"] = axis_headings()
    raw["seeds"].append(
        {
            "position": [PROBE.CENTER - 2, PROBE.CENTER, PROBE.CENTER],
            "type": "held_body",
            "values": {"mass": 3},
        }
    )
    world = Simulation(parse_initial_state(raw))
    for _ in range(6):
        world.step()
    gained = {}
    for position, values in PROBE.bodies(world, 1):
        gained[(position[0] - PROBE.CENTER, values["mass"][0])] = values["momentum"]
    # Each axis Node receives 4096 / 6 = 682 or 683 units per tick from tick k onward;
    # momentum moves toward the source, scaled by mass, over four response ticks at +2.
    assert gained[(2, 1)][0] < 0 and gained[(2, 1)][1:] == (0, 0)
    assert gained[(-2, 3)][0] > 0
    # Proportional to mass up to the carried integer remainder of one unit per tick.
    assert abs(gained[(2, 2)][0] - 2 * gained[(2, 1)][0]) <= 6
    assert abs(gained[(2, 4)][0] - 4 * gained[(2, 1)][0]) <= 6
    assert abs(gained[(4, 1)][0]) < abs(gained[(2, 1)][0])
    # The reaction stays in the local momentum field: combined momentum is conserved.
    assert world.totals()["momentum"] == (0, 0, 0)
    assert world.spatial_values((PROBE.CENTER + 2,) + (PROBE.CENTER,) * 2)["momentum"]["value"][0] > 0


def test_falling_body_oscillates_through_the_source():
    small_world()
    raw = PROBE.falling_document(62, 1, 5)
    raw["spatial_fields"][0]["headings"] = axis_headings()
    world = Simulation(parse_initial_state(raw))
    offsets, momenta = [], []
    for _ in range(62):
        world.step()
        position, values = PROBE.bodies(world, 1)[0]
        offsets.append(position[0] - PROBE.CENTER)
        momenta.append(values["momentum"][0])
    first_crossing = offsets.index(0)
    inward = list(zip(offsets[:first_crossing], momenta[:first_crossing], strict=True))
    # Outside the source the body only moves inward and its inward momentum only grows.
    assert inward[0] == (5, 0)
    assert [o for o, _ in inward] == sorted((o for o, _ in inward), reverse=True)
    assert [-m for _, m in inward] == sorted(-m for _, m in inward) and inward[-1][1] < 0
    # Past the source the same rule decelerates it; it turns near the mirror distance,
    # its momentum changes sign, and it comes back through the source: a bound orbit.
    turning = momenta.index(0, first_crossing)
    assert -7 <= offsets[turning] <= -5 and momenta[turning + 1] > 0
    assert 0 in offsets[turning:] and max(offsets[turning:]) >= 5
    second_turn = momenta.index(0, turning + 1)
    assert offsets[second_turn] >= 5 and momenta[second_turn + 1] < 0
    # Edge case: no momentum leaks; carrier plus local field momentum stays zero.
    assert world.totals()["momentum"] == (0, 0, 0)
