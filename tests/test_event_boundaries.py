"""Independent per-axis topology cases from the published design 2b8153a.

On (3,2,1), periodic X/Z and open Y: +X at x=2 reaches x=0;
-X at x=0 reaches x=2; +/-Z retain separate Ports at the same Node.
Each transfer consumes one interval. A one-unit self-returning carrier
fills capacity two at ticks 1 and 2; tick 3 refuses without mutation.
"""

import json
from copy import deepcopy

import numpy as np
import pytest

from event_universe.core.lattice import adjacent_node
from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.transit import Transit
from event_universe.runner import run_initialization

MIXED = (True, False, True)
MIXED_JSON = {"x": "periodic", "y": "open", "z": "periodic"}
SHAPE = (3, 2, 1)


@pytest.mark.parametrize(
    "position,port,expected",
    [
        ((2, 1, 0), 0, (0, 1, 0)),
        ((0, 1, 0), 1, (2, 1, 0)),
        ((1, 0, 0), 2, (1, 1, 0)),
        ((1, 1, 0), 2, None),
        ((1, 0, 0), 3, None),
        ((1, 1, 0), 4, (1, 1, 0)),
        ((1, 1, 0), 5, (1, 1, 0)),
    ],
)
def test_adjacent_node_has_the_declared_signed_links(position, port, expected):
    assert adjacent_node(position, port, SHAPE, MIXED) == expected
    if expected is not None:
        assert adjacent_node(expected, port ^ 1, SHAPE, MIXED) == position


@pytest.mark.parametrize(
    "position,port,shape,periodic",
    [
        ((True, 0, 0), 0, SHAPE, MIXED),
        ((3, 0, 0), 0, SHAPE, MIXED),
        ((0, 0, 0), True, SHAPE, MIXED),
        ((0, 0, 0), 6, SHAPE, MIXED),
        ((0, 0, 0), 0, (3, 2, 0), MIXED),
        ((0, 0, 0), 0, (4097, 2, 1), MIXED),
        ((0, 0, 0), 0, SHAPE, (True, False, 1)),
    ],
)
def test_neighbor_provider_refuses_invalid_physical_indices(position, port, shape, periodic):
    with pytest.raises(ValueError):
        adjacent_node(position, port, shape, periodic)


@pytest.mark.parametrize(
    "position,port,momentum,target",
    [
        ((2, 1, 0), 0, (2, 0, 0), (0, 1, 0)),
        ((0, 1, 0), 1, (-2, 0, 0), (2, 1, 0)),
        ((1, 1, 0), 4, (0, 0, 2), (1, 1, 0)),
    ],
)
def test_one_transport_interval_retains_the_exact_wrapped_payload(position, port, momentum, target):
    transit = Transit(0, SHAPE, (7,), 32, 1024, periodic=MIXED, exact_transport=True)
    transit.place(position, 0, port, 2, 16, np.array(momentum, dtype=np.int64))
    assert int(transit.arr_amt.sum()) == 0
    assert int(transit.fly_amt[(*position, 0, port)]) == 2
    transit.walk()
    slot = (*target, transit.rank[7], port)
    assert int(transit.arr_amt[slot]) == 2 and int(transit.arr_amt.sum()) == 2
    assert int(transit.arr_ph[slot]) == 16 and transit.arr_mom[slot].tolist() == list(momentum)
    assert int(transit.fly_amt.sum()) == 0
    assert transit.escaped == 0 and transit.escaped_momentum.tolist() == [0, 0, 0]


@pytest.mark.parametrize("extent,target_z", [(1, 0), (2, 1)])
def test_opposite_ports_remain_separate_when_periodic_destinations_coincide(extent, target_z):
    transit = Transit(0, (1, 1, extent), (7,), 32, 1024, periodic=MIXED, exact_transport=True)
    transit.place((0, 0, 0), 0, 4, 2, 16, np.array([0, 0, 2], dtype=np.int64))
    transit.place((0, 0, 0), 0, 5, 3, 5, np.array([0, 0, -3], dtype=np.int64))
    transit.walk()
    for port, amount, phase, momentum in ((4, 2, 16, [0, 0, 2]), (5, 3, 5, [0, 0, -3])):
        slot = (0, 0, target_z, 0, port)
        assert int(transit.arr_amt[slot]) == amount
        assert int(transit.arr_ph[slot]) == phase
        assert transit.arr_mom[slot].tolist() == momentum
    assert int(transit.arr_amt.sum()) == 5 and transit.escaped == 0


def test_an_open_axis_keeps_default_escape_accounting_with_other_axes_periodic():
    transit = Transit(0, SHAPE, (7,), 32, 1024, periodic=MIXED, exact_transport=True)
    transit.place((1, 1, 0), 0, 2, 2, 16, np.array([0, 2, 0], dtype=np.int64))
    transit.walk()
    assert int(transit.arr_amt.sum()) == 0 and int(transit.fly_amt.sum()) == 0
    assert transit.escaped == 2 and transit.escaped_momentum.tolist() == [0, 2, 0]


def candidate_world(*, heading=None, position=None, capacity=7):
    return {
        "law": "events",
        "dynamics": "reversible-detector-v1",
        "model_id": "boundary-rule-test",
        "shape": list(SHAPE),
        "boundary": MIXED_JSON.copy(),
        "ticks": 2,
        "K": 1024,
        "N": 8,
        "release": 0,
        "suspension": 0,
        "max_active_owners": 1,
        "families": [{"name": "carrier", "kind": "paid"}],
        "measured": [
            {
                "position": [1, 1, 0],
                "family": "carrier",
                "amount": 1,
                "fixed": True,
                "table": {"carrier": "transduce"},
                "port_map": list(range(6)),
            }
        ],
        "in_transit": [
            {
                "position": [1, 1, 0] if position is None else position,
                "family": "carrier",
                "number": 1,
                "amount": 1,
                "phase": 3,
                "heading": [0, 0, 1] if heading is None else heading,
            }
        ],
        "detectors": [
            {
                "name": "counter",
                "positions": [[1, 1, 0]],
                "groups": [
                    {
                        "name": "shared",
                        "positions": [[1, 1, 0]],
                        "output": [1, 1, 0],
                        "threshold": 1,
                        "capacity": capacity,
                        "reference_phase": 0,
                    }
                ],
            }
        ],
    }


@pytest.mark.parametrize(
    "start,heading,target,port",
    [([2, 0, 0], [1, 0, 0], (0, 0, 0), 0), ([0, 0, 0], [-1, 0, 0], (2, 0, 0), 1)],
)
def test_candidate_periodic_transfer_preserves_owner_phase_and_signed_momentum(
    start, heading, target, port
):
    simulation = EventSimulation(parse_event_world(candidate_world(position=start, heading=heading)))
    simulation.step()
    transit = simulation.transits[0]
    assert int(transit.fly_amt[(*start, transit.rank[1], port)]) == 1
    simulation.step()
    slot = (*target, transit.rank[1], port)
    assert int(transit.fly_amt[slot]) == 1 and int(transit.fly_ph[slot]) == 3
    assert transit.fly_mom[slot].tolist() == heading
    assert transit.escaped == 0
    assert simulation.detector_readouts()[0]["groups"][0]["value"] == 0


def test_candidate_self_return_has_one_contact_per_interval_and_finite_capacity():
    records = []
    simulation = EventSimulation(parse_event_world(candidate_world(capacity=2)), records.append)
    for tick in (1, 2):
        simulation.step()
        assert simulation.tick == tick
        assert simulation.detector_readouts()[0]["groups"][0]["value"] == tick
        transit = simulation.transits[0]
        slot = (1, 1, 0, transit.rank[1], 4)
        assert int(transit.fly_amt[slot]) == 1 and int(transit.fly_ph[slot]) == 3
        assert transit.fly_mom[slot].tolist() == [0, 0, 1]
        assert transit.escaped == 0 and simulation.measured[1].momentum == [0, 0, 0]
        assert len(records) == tick
    before, previous_records = deepcopy(simulation.snapshot()), deepcopy(records)
    with pytest.raises(ValueError):
        simulation.step()
    assert simulation.snapshot() == before and records == previous_records


def test_candidate_mixed_open_exit_refuses_the_entire_step_before_a_second_packet_wraps():
    document = candidate_world(heading=[0, 1, 0])
    second = deepcopy(document["in_transit"][0])
    second.update(position=[2, 0, 0], heading=[1, 0, 0])
    document["in_transit"].append(second)
    simulation = EventSimulation(parse_event_world(document))
    simulation.step()
    before = deepcopy(simulation.snapshot())
    with pytest.raises(ValueError):
        simulation.step()
    assert simulation.snapshot() == before and simulation.tick == 1


def moving_world(momentum, position):
    return {
        "law": "events",
        "model_id": "boundary-movement-rule-test",
        "shape": list(SHAPE),
        "boundary": MIXED_JSON.copy(),
        "ticks": 2,
        "K": 1024,
        "N": 32,
        "release": 0,
        "families": [{"name": "body", "kind": "paid"}],
        "measured": [{"position": position, "family": "body", "amount": 1, "momentum": momentum}],
    }


@pytest.mark.parametrize(
    "momentum,start,expected", [([1, 0, 0], [2, 1, 0], (0, 1, 0)), ([0, 0, 1], [1, 1, 0], (1, 1, 0))]
)
def test_default_material_wrap_and_self_loop_keep_one_inventory(momentum, start, expected):
    simulation = EventSimulation(parse_event_world(moving_world(momentum, start)))
    simulation.step()
    assert simulation.measured[1].position == tuple(start) and simulation.measured[1].steps == 0
    simulation.step()
    assert len(simulation.measured) == 1 and simulation.at == {expected: 1}
    entry = simulation.measured[1]
    assert entry.position == expected and entry.steps == 1
    assert entry.held == [1] and entry.momentum == momentum and entry.age == 2
    assert simulation.books()["balanced"] and simulation.held_escaped == [0]


def test_default_wrapped_movement_still_merges_with_a_different_resident():
    document = moving_world([1, 0, 0], [2, 1, 0])
    document["measured"].append({"position": [0, 1, 0], "family": "body", "amount": 1, "fixed": True})
    simulation = EventSimulation(parse_event_world(document))
    simulation.step()
    simulation.step()
    assert list(simulation.measured) == [2]
    assert simulation.measured[2].held == [2] and simulation.measured[2].momentum == [1, 0, 0]
    assert simulation.at == {(0, 1, 0): 2} and simulation.books()["balanced"]


def test_default_material_on_an_open_axis_still_escapes():
    simulation = EventSimulation(parse_event_world(moving_world([0, 1, 0], [1, 1, 0])))
    simulation.step()
    simulation.step()
    assert simulation.measured == {} and simulation.held_escaped == [1]
    assert simulation.momentum_escaped == [0, 1, 0] and simulation.books()["balanced"]


@pytest.mark.parametrize("boundary", [{"z": "periodic"}, "open"])
def test_snapshot_and_runner_record_the_actual_declared_topology(tmp_path, boundary):
    document = candidate_world()
    document["boundary"] = boundary
    document["in_transit"] = []
    simulation = EventSimulation(parse_event_world(document))
    assert simulation.snapshot()["boundary"] == boundary
    source = tmp_path / "world.json"
    source.write_text(json.dumps(document), encoding="utf-8")
    metadata_path = run_initialization(source, tmp_path / "run", ticks=1)
    assert json.loads(metadata_path.read_text())["boundary"] == boundary
    assert json.loads((metadata_path.parent / "state.json").read_text())["boundary"] == boundary


@pytest.mark.parametrize("candidate,boundary", [(True, "open"), (True, MIXED_JSON), (False, MIXED_JSON)])
def test_flux_refuses_periodic_geometry_and_the_unpopulated_candidate_cache(candidate, boundary):
    document = candidate_world() if candidate else moving_world([0, 0, 0], [1, 1, 0])
    document["boundary"] = boundary
    simulation = EventSimulation(parse_event_world(document))
    with pytest.raises(ValueError):
        simulation.cube_flux(0, (1, 1, 0), 1)


def test_default_all_open_flux_keeps_its_contract():
    document = moving_world([0, 0, 0], [1, 1, 0])
    document["boundary"] = "open"
    simulation = EventSimulation(parse_event_world(document))
    assert simulation.cube_flux(0, (1, 1, 0), 1) == 0
    assert adjacent_node((2, 1, 0), 0, SHAPE) is None
