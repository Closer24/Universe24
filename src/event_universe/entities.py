"""Compile explicit catalog representation profiles into ordinary initialization.

This host-side authoring adapter supplies no physical species dispatch or laws.
The ordinary validator, scheduler and local integer operations remain owners.
"""

import argparse
import copy
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_json_document
from event_universe.reference_api import parse_reference_state as parse_initial_state

JsonObject = dict[str, Any]


def _object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    return value


def _rows(value: object, label: str) -> list[JsonObject]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return [_object(row, label) for row in value]


def compile_entities(
    catalog: object,
    entity_ids: Sequence[str],
    *,
    shape: tuple[int, int, int] = (9, 9, 9),
    ticks: int = 4,
    link_ticks: int = 1,
    representation: str = "classical",
) -> JsonObject:
    """Select bounded explicit profiles; retain physical claims in the catalog.

    Carrier definitions and local-field operations are copied from profiles.
    The supplied field probes preserve retained-plus-outgoing component balances.
    Extending the domain is not a continuum-limit or physical-law claim.
    """
    source = _object(catalog, "catalog")
    if type(source.get("catalog_version")) is not int or source["catalog_version"] != 1:
        raise ValueError("unsupported catalog_version")
    entries = _rows(source.get("field_entities"), "field_entities") + _rows(
        source.get("particle_entities"), "particle_entities"
    )
    indexed: dict[str, JsonObject] = {}
    for entry in entries:
        identity = entry.get("id")
        if not isinstance(identity, str) or not identity or identity in indexed:
            raise ValueError("entity IDs must be unique nonempty strings")
        indexed[identity] = entry
    if (
        isinstance(entity_ids, str)
        or not entity_ids
        or any(not isinstance(identity, str) or not identity for identity in entity_ids)
        or len(set(entity_ids)) != len(entity_ids)
    ):
        raise ValueError("select at least one entity without duplicates")
    if len(shape) != 3 or any(type(size) is not int or size < 5 for size in shape):
        raise ValueError("representation probes require three integer dimensions of at least five")
    if representation not in ("classical", "quantum"):
        raise ValueError("representation must be classical or quantum")
    if representation == "quantum":
        from event_universe.integration.quantum_entities import compile_quantum_entities

        return compile_quantum_entities(
            indexed, entity_ids, shape=shape, ticks=ticks, link_ticks=link_ticks
        )
    fields: dict[str, JsonObject] = {}
    types: dict[str, JsonObject] = {}
    spatial_names: set[str] = set()
    result: JsonObject = {
        "schema_version": 1,
        "model_id": "catalog-representation-probes-v1",
        "shape": list(shape),
        "boundary": "open",
        "slots_per_cell": 16,
        "link_ticks": link_ticks,
        "normal_budget": 1000000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "seeds": [],
        "spatial_fields": [],
        "spatial_seeds": [],
        "field_groups": [],
        "field_rules": [],
    }
    position = [2, shape[1] // 2, shape[2] // 2]
    for identity in entity_ids:
        if identity not in indexed:
            raise ValueError(f"unknown entity: {identity}")
        profile = copy.deepcopy(_object(indexed[identity].get("executable_profile"), "profile"))
        if profile.get("claim_level") != "representation_probe":
            raise ValueError("profiles must explicitly declare representation_probe")
        kind = profile.get("kind")
        required = {"kind", "claim_level", "assumptions", "fields", "seed_values"}
        required |= (
            {"disturbance"} if kind == "carrier" else {"components", "spatial_fields", "field_rules"}
        )
        if kind not in ("carrier", "local_field") or set(profile) != required:
            raise ValueError("unsupported or incomplete executable profile")
        if (
            not isinstance(profile["assumptions"], list)
            or not profile["assumptions"]
            or any(not isinstance(item, str) or not item.strip() for item in profile["assumptions"])
        ):
            raise ValueError("profile assumptions must be explicit")
        definitions = _rows(profile["fields"], "profile fields")
        local: dict[str, JsonObject] = {}
        for field in definitions:
            name = field.get("name")
            if not isinstance(name, str) or not name or name in local:
                raise ValueError("profile field names must be unique nonempty strings")
            if name in fields and fields[name] != field:
                raise ValueError(f"incompatible shared field: {name}")
            local[name] = field
            fields[name] = field
        values = _object(profile["seed_values"], "seed_values")
        if set(values) != set(local):
            raise ValueError("seed_values must specify every profile field exactly once")
        if kind == "carrier":
            disturbance = _object(profile["disturbance"], "disturbance")
            name = disturbance.get("name")
            if not isinstance(name, str) or name in types:
                raise ValueError("selected disturbance names must be unique")
            owned = disturbance.get("fields")
            if (
                not isinstance(owned, list)
                or any(not isinstance(name, str) for name in owned)
                or len(set(owned)) != len(owned)
                or set(owned) != set(local)
            ):
                raise ValueError("carrier must own exactly its profile fields")
            types[name] = disturbance
            result["seeds"].append({"position": position.copy(), "type": name, "values": values})
        else:
            components = profile["components"]
            if not isinstance(components, list) or components != list(local):
                raise ValueError("components must list the profile fields in declaration order")
            result["field_groups"].append({"name": identity, "fields": components})
            spatial = _rows(profile["spatial_fields"], "spatial_fields")
            if [item.get("field") for item in spatial] != components:
                raise ValueError("spatial_fields must declare each component in order")
            result["spatial_fields"].extend(spatial)
            result["field_rules"].extend(_rows(profile["field_rules"], "field_rules"))
            for name, field in local.items():
                if name in spatial_names:
                    raise ValueError("selected spatial fields must have distinct ownership")
                spatial_names.add(name)
                zero: int | list[int] = 0 if field.get("components") == 1 else [0, 0, 0]
                result["spatial_seeds"].append(
                    {
                        "position": position.copy(),
                        "field": name,
                        "populations": [values[name]] + [zero] * 7,
                    }
                )
    if not types:
        # Initialization requires a type even for an unoccupied spatial world.
        types["unused carrier"] = {
            "name": "unused carrier",
            "fields": list(fields),
            "transport": {"mode": "hold"},
        }
    result["fields"] = list(fields.values())
    result["disturbance_types"] = list(types.values())
    parse_initial_state(result)
    return result


def main() -> None:
    """Write a validated input for the existing runner and configuration UI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--entity", action="append", required=True)
    parser.add_argument("--output-init", type=Path, required=True)
    parser.add_argument("--ticks", type=int, default=4)
    parser.add_argument("--representation", choices=("classical", "quantum"), default="classical")
    args = parser.parse_args()
    initial = compile_entities(
        parse_json_document(args.catalog.read_bytes()),
        args.entity,
        ticks=args.ticks,
        representation=args.representation,
    )
    args.output_init.parent.mkdir(parents=True, exist_ok=True)
    with args.output_init.open("x", encoding="utf-8") as output:
        output.write(json.dumps(initial, indent=2) + "\n")
    print(args.output_init)


if __name__ == "__main__":
    main()
