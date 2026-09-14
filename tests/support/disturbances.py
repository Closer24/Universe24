"""Small generic initialization builders shared by independent contract tests."""

from event_universe.core.disturbance_state import OPERATIONS


def field(name="inventory", components=1, *, conserved=True, signed=True, extensive=True):
    return {
        "name": name,
        "components": components,
        "units": "configured unit",
        "signed": signed,
        "conserved": conserved,
        "extensive": extensive,
    }


def kind(name, *, mode="hold", values=None, weights=None, updates=None):
    values = {"inventory": 1} if values is None else values
    transport = {"mode": mode}
    if weights is not None:
        transport["weights"] = weights
    return {
        "name": name,
        "fields": list(values),
        "defaults": values,
        "transport": transport,
        "updates": [] if updates is None else updates,
    }


def document(kinds, seeds, *, fields=None, couplings=None, budget=10000, travel=1, capacity=32):
    return {
        "schema_version": 1,
        "model_id": "generic-contract-fixture-v1",
        "shape": [41, 41, 41],
        "slots_per_node": capacity,
        "link_ticks": travel,
        "normal_budget": budget,
        "ticks": 0,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [field()] if fields is None else fields,
        "disturbance_types": kinds,
        "couplings": [] if couplings is None else couplings,
        "seeds": [{"position": list(position), "type": name} for position, name in seeds],
    }
