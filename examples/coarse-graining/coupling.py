"""Finite property-selected transfer followed by the existing momentum route."""

from copy import deepcopy

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

from .configuration import additive_audit, field, operation, reference
from .routing import build_configuration as routing_configuration

RESERVOIR = (3, 2, 1)


def build_configuration(coupling=1, *, link_ticks=1, normal_budget=1_000_000):
    """Supply a local candidate law; labels never select its response."""
    raw = routing_configuration(
        (1, 0, 0),
        ticks=4 * link_ticks,
        shape=(9, 9, 3),
        link_ticks=link_ticks,
        normal_budget=normal_budget,
    )
    raw["model_id"] = "property-transfer-routing-candidate-v1"
    raw["fields"] += [field("coupling", extensive=False), field("internal", extensive=False)]
    definition = raw["disturbance_types"][0]
    definition["fields"] += ["coupling", "internal"]
    definition["defaults"] = {
        "energy": 3,
        "momentum": [1, 0, 0],
        "coupling": coupling,
        "internal": 0,
    }
    raw["seeds"] = [{"position": [2, 2, 1], "type": definition["name"]}]
    raw["spatial_fields"] = [
        {"field": name, "transport": "local", "baseline": zero}
        for name, zero in (("energy", 0), ("momentum", [0, 0, 0]))
    ]
    raw["spatial_seeds"] = [
        {
            "position": list(RESERVOIR),
            "field": name,
            "populations": [value] + [zero] * 7,
        }
        for name, value, zero in (("energy", 4, 0), ("momentum", [-1, 1, 0], [0, 0, 0]))
    ]
    strength = reference("coupling")
    energy_delta = operation("mul", strength, operation("min", 1, reference("energy", "right")))
    momentum_delta = operation("mul", strength, reference("momentum", "right"))
    assignments = []
    for name, delta in (("energy", energy_delta), ("momentum", momentum_delta)):
        for side, op in (("left", "add"), ("right", "sub")):
            assignments.append(
                {"side": side, "field": name, "expression": operation(op, reference(name, side), delta)}
            )
    assignments.append(
        {
            "side": "left",
            "field": "internal",
            "expression": operation("add", reference("internal"), operation("abs", strength)),
        }
    )
    raw["spatial_interactions"] = [
        {
            "name": "exchange_with_local_reservoir",
            "requires": ["energy", "momentum", "coupling", "internal"],
            "when": operation(
                "gt", operation("dot", reference("momentum", "right"), reference("momentum", "right")), 0
            ),
            "assignments": assignments,
            "invariants": [
                {
                    "name": "joint_" + name,
                    "expression": operation("add", reference(name), reference(name, "right")),
                }
                for name in ("energy", "momentum")
            ],
        }
    ]
    raw["conservation"] = additive_audit(spatial=True)
    return raw


def run_configuration(raw=None, *, ticks=None):
    """Read actual owners/events; the audit never supplies a physical update."""
    raw = build_configuration() if raw is None else deepcopy(raw)
    count = raw["ticks"] if ticks is None else ticks
    if type(count) is not int or not 0 <= count <= 256:
        raise ValueError("candidate trace requires zero through 256 ticks")
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    snapshots = [world.snapshot()]
    for _ in range(count):
        world.step()
        snapshots.append(world.snapshot())
    return {
        "model_id": raw["model_id"],
        "snapshots": snapshots,
        "events": events,
        "conservation": world.conservation_report(),
        "spatial_accounting": world.spatial_accounting(),
        "computation": world.computation_report(),
    }
