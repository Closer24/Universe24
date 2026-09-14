"""Contact configurations and inventory checks without importing test modules."""

import json
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.integration.contact_runtime import ContactEventResolver

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/quantum/localized_charge.json"


ROTATION = [[5, 0, 0, 0], [0, 3, -4, 0], [0, 4, 3, 0], [0, 0, 0, 5]]


INVERSE = [[5, 0, 0, 0], [0, 3, 4, 0], [0, -4, 3, 0], [0, 0, 0, 5]]


def configuration(fields=True):
    raw = json.loads(EXAMPLE.read_text())
    if not fields:
        raw.pop("spatial_fields")
        raw.pop("emissions")
    return raw


def world_for(raw, *, observer=None):
    world = Simulation(parse_initial_state(raw), observer=observer)
    assert isinstance(world._resolver, ContactEventResolver)
    return world, world._resolver


def step(world, count):
    for _ in range(count):
        world.step()
        assert world.totals()["charge"] == (-1,)
        assert world.totals()["mass"] == (1,)


def localized(world):
    return [
        (address, r.type_index)
        for address, node in world.nodes.items()
        for r in node.records
        if r is not None and r.type_index in (0, 1)
    ]
