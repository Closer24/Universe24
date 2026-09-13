"""Carried allocation phases: an indivisible unit continues its own cycle at the next node.

Highlights 3.3.1 requires integer division remainders to be carried into later
updates. With node-owned phases every fresh node starts at the first axis, so
far-field singletons of a decay-free pulse all follow that axis. With carried
phases (the default) each portion leaves with the phase after its last
allocated slot, merged by addition modulo the axis cycle on arrival.
"""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, pack
from event_universe.fields.spatial import carried_phases, split_weighted
from event_universe.initialization import parse_initial_state

C = 12
TICKS = 11


def document(*, carried=None, components=1, populations=None):
    doc = {
        "schema_version": 1,
        "model_id": "carried-allocation-phase-contract-v1",
        "boundary": "open",
        "shape": [25, 25, 25],
        "slots_per_node": 1,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": TICKS,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "marker", "components": 1, "units": "unit", "signed": False, "conserved": False},
            {
                "name": "radiation",
                "components": components,
                "units": "unit",
                "signed": components == 3,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "probe",
                "fields": ["marker"],
                "defaults": {"marker": 0},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "radiation",
                "baseline": 0 if components == 1 else [0, 0, 0],
                "transport": "outward",
            }
        ],
        "spatial_seeds": [
            {
                "position": [C, C, C],
                "field": "radiation",
                "populations": populations if populations is not None else [27] * 8,
            }
        ],
        "seeds": [{"position": [C, C, C], "type": "probe"}],
    }
    if carried is not None:
        doc["carried_allocation_phase"] = carried
    return doc


def shell(doc):
    world = Simulation(parse_initial_state(doc))
    for _ in range(doc["ticks"]):
        world.step()
    cells = {}
    for node in world.snapshot()["spatial_fields"]:
        amounts = [
            sum(p[i] for p in node["fields"]["radiation"]["populations"])
            for i in range(len(node["fields"]["radiation"]["populations"][0]))
        ]
        if any(amounts):
            cells[tuple(node["position"])] = amounts
    return world, cells


def mean_axis_distances(cells):
    total = sum(abs(a[0]) for a in cells.values())
    return tuple(sum(abs(p[i] - C) * abs(a[0]) for p, a in cells.items()) / total for i in range(3))


def test_default_is_carried_and_boolean_is_enforced():
    assert parse_initial_state(document()).carried_allocation_phase is True
    assert parse_initial_state(document(carried=False)).carried_allocation_phase is False
    with pytest.raises(ValueError, match="boolean"):
        parse_initial_state(document(carried="yes"))


def test_carried_phases_keep_the_decay_free_shell_isotropic():
    world, cells = shell(document())
    assert world.totals()["radiation"] == (216,)
    assert all(sum(abs(p[i] - C) for i in range(3)) == TICKS for p in cells)
    dx, dy, dz = mean_axis_distances(cells)
    assert max(dx, dy, dz) < 1.3 * min(dx, dy, dz)


def test_node_owned_phases_document_the_first_axis_bias():
    world, cells = shell(document(carried=False))
    assert world.totals()["radiation"] == (216,)
    dx, dy, dz = mean_axis_distances(cells)
    assert dx > 2 * max(dy, dz)


def test_vector_field_components_are_conserved_under_carried_phases():
    populations = [[5, -3, 7]] * 8
    world, cells = shell(document(components=3, populations=populations))
    assert world.totals()["radiation"] == (40, -24, 56)
    assert world.snapshot()["spatial_transfers"] == []
    assert all(sum(abs(p[i] - C) for i in range(3)) == TICKS for p in cells)


@pytest.mark.parametrize(
    ("magnitude", "weights", "phase", "expected"),
    [
        (1, (1, 1, 1), 0, (1, 2, 0)),
        (1, (1, 1, 1), 1, (1, 2, 0)),
        (1, (1, 1, 1), 2, (1, 2, 0)),
        (3, (1, 1, 1), 0, (1, 2, 0)),
        (2, (1, 1, 1), 1, (1, 2, 0)),
        (4, (1, 1, 1), 2, (1, 2, 0)),
        (5, (2, 1, 0), 1, (2, 0, 0)),
        (0, (1, 1, 1), 2, (0, 0, 0)),
    ],
)
def test_carried_phase_of_each_portion_is_the_slot_after_its_last_unit(
    magnitude, weights, phase, expected
):
    assert carried_phases(magnitude, weights, phase) == expected
    portions, _ = split_weighted(magnitude, weights, phase)
    assert sum(portions) == magnitude


def test_singleton_cycles_through_all_axes_under_carried_phases():
    phase, visited = 0, []
    for _ in range(6):
        portions, _ = split_weighted(1, (1, 1, 1), phase)
        axis = portions.index(1)
        visited.append(axis)
        phase = carried_phases(1, (1, 1, 1), phase)[axis]
    assert visited == [0, 1, 2, 0, 1, 2]
    assert pack((phase,)) == pack((0,))
