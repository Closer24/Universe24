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


def closed_axis_world(mass: int, ticks: int = 8, stock: int | None = None, audit: bool = False):
    small_world()
    raw = PROBE.closed_document(ticks, 6, audit=audit)
    raw["spatial_fields"][0]["headings"] = axis_headings()
    raw["disturbance_types"].append(PROBE.closed_body("held_body", {"mode": "hold"}))
    raw["spatial_couplings"].append(PROBE.closed_attraction("held_body"))
    quanta = mass * PROBE.CLOSED_STOCK if stock is None else stock
    for k in (2, 4):
        raw["seeds"].append(
            {
                "position": [PROBE.CENTER + k, PROBE.CENTER, PROBE.CENTER],
                "type": "held_body",
                "values": {"mass": mass, "quanta": quanta},
            }
        )
    world = Simulation(parse_initial_state(raw))
    for _ in range(ticks):
        world.step()
    found = {position[0] - PROBE.CENTER: values for position, values in PROBE.bodies(world, 1)}
    return world, found, 2 * quanta


def test_signed_quanta_pull_bodies_toward_the_source_and_they_pay_their_own_stock():
    pulled = {}
    for mass in (1, 2):
        world, found, initial = closed_axis_world(mass)
        near, far = found[2], found[4]
        # Each -x-bound quantum share moves momentum toward the source by share x (1,0,0),
        # and the body pays exactly that share from its stock: nothing else changes.
        assert near["momentum"][0] < 0 and near["momentum"][1:] == (0, 0)
        assert mass * PROBE.CLOSED_STOCK - near["quanta"][0] == -near["momentum"][0]
        # The far body takes its share of what the near one left on the same ray.
        assert 0 < -far["momentum"][0] <= -near["momentum"][0]
        # The source is credited with every quantum it emits and recoils by nothing:
        # the six axis rays cancel exactly. Credited quanta are bounded integers
        # like any other stock; a source that emits forever eventually fails loudly.
        (_, source), *_ = PROBE.bodies(world, 0)
        assert source["quanta"] == (8 * 6 * PROBE.CLOSED_PER_RAY,)
        assert source["momentum"] == (0, 0, 0)
        assert PROBE.closure(world, initial)["quanta_closed"]
        pulled[mass] = -near["momentum"][0]
    # The share is proportional to mass: the same acceleration up to one unit per hit.
    assert abs(pulled[2] - 2 * pulled[1]) <= 8


def test_a_body_with_no_stock_left_is_not_pulled_and_the_audit_stays_closed():
    world, found, initial = closed_axis_world(1, ticks=8, stock=50, audit=True)
    assert found[2]["quanta"] == (0,) and found[2]["momentum"] == (-50, 0, 0)
    report = world.conservation_report()
    assert report["status"] == "passed" and report["checked_node_events"] > 0
    assert report["current"]["energy"] + report["escaped"]["energy"] == initial
    current, escaped = report["current"]["momentum"], report["escaped"]["momentum"]
    assert tuple(a + b for a, b in zip(current, escaped, strict=True)) == (0, 0, 0)
