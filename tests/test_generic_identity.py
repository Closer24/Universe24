"""Active semantic label and declaration-order equivalence with shared baselines."""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

from .support.identity import (
    assert_exercised,
    configured_example,
    normalize,
    observation,
    renamed_document,
    reorder_declarations,
)


@pytest.fixture(
    scope="module",
    params=[
        "basic",
        "exchange",
        "finite_fields",
        "open_world",
        "rotation",
        "flux",
        "property_fields",
    ],
)
def baseline(request):
    case = request.param
    original = configured_example(case)
    encoded = json.dumps(original)
    events = []
    world = Simulation(parse_initial_state(original), observer=events.append)
    initial = world.totals()
    trace = []
    for tick in range(7):
        trace.append(json.dumps(normalize(observation(world, events), {}, {}), sort_keys=True))
        for name, total in world.totals().items():
            assert tuple(
                value + loss + escaped
                for value, loss, escaped in zip(
                    total, world.dissipation_totals()[name], world.escaped_totals()[name], strict=True
                )
            ) == tuple(a + b for a, b in zip(initial[name], world.source_totals()[name], strict=True))
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        if tick < 6:
            world.step()
    assert_exercised(case, world, events)
    assert json.dumps(original) == encoded
    # Strings and tuples are immutable; no live world or mutable snapshot is shared.
    return case, encoded, tuple(trace)


@pytest.mark.parametrize("change", ["rename", "reorder", "both"])
def test_generic_runtime_uses_references_instead_of_names_or_declaration_indices(baseline, change):
    case, encoded, trace = baseline
    original = json.loads(encoded)
    changed, fields, types = renamed_document(original)
    if change == "reorder":
        changed, fields, types = deepcopy(original), {}, {}
    if change != "rename":
        reorder_declarations(changed)
    events = []
    world = Simulation(parse_initial_state(changed), observer=events.append)
    for tick, expected in enumerate(trace):
        actual = json.dumps(normalize(observation(world, events), fields, types), sort_keys=True)
        assert actual == expected, (case, change, tick)
        if tick < 6:
            world.step()
    assert json.dumps(original) == encoded
