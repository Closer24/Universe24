"""Ordinary initialization data shared by the finite disturbance experiments."""

from event_universe.core.disturbance_state import OPERATIONS


def operation(name, *arguments):
    return {"op": name, "args": list(arguments)}


def reference(name, side="left"):
    return {"field": name, "side": side}


def field(name, components=1, *, conserved=False, extensive=True):
    return {
        "name": name,
        "components": components,
        "units": "candidate inventory unit",
        "signed": True,
        "conserved": conserved,
        "extensive": extensive,
    }


def base_configuration(model_id, ticks=12, shape=(9, 9, 3), slots=4):
    return {
        "schema_version": 1,
        "model_id": model_id,
        "shape": list(shape),
        "boundary": "open",
        "slots_per_node": slots,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": ticks,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [],
        "disturbance_types": [],
        "seeds": [],
    }


def additive_audit(energy="energy", momentum="momentum", *, spatial=False):
    result = {
        "name": "declared additive disturbance inventories",
        "energy_units": "candidate energy unit",
        "momentum_units": "candidate momentum unit",
        "carriers": [
            {
                "requires": [energy, momentum],
                "energy": reference(energy),
                "momentum": reference(momentum),
            }
        ],
    }
    if spatial:
        result["spatial"] = {
            "energy": reference(energy, "right"),
            "momentum": reference(momentum, "right"),
        }
    return result
