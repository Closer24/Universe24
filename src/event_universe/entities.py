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
from event_universe.entity_catalog import ENTITY_SECTIONS, validate_catalog
from event_universe.initialization import parse_initial_state, parse_json_document

JsonObject = dict[str, Any]


def _object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    return value


def _rows(value: object, label: str) -> list[JsonObject]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return [_object(row, label) for row in value]


def _profile_index(
    indexed: dict[str, JsonObject], profiles: object, version: int
) -> dict[str, JsonObject]:
    """Bind explicit experiment data without interpreting physical metadata."""
    profile_keys = {"executable_profile", "quantum_profile"}
    embedded = any(profile_keys.intersection(entry) for entry in indexed.values())
    if embedded and (profiles is not None or version == 2):
        raise ValueError("embedded profiles cannot be combined with external profiles or catalog v2")
    if profiles is None:
        if version == 2:
            raise ValueError("catalog v2 requires explicit profiles")
        return copy.deepcopy(indexed)
    document = _object(profiles, "profiles document")
    if type(document.get("profile_version")) is not int or document["profile_version"] != 1:
        raise ValueError("unsupported profile_version")
    if set(document) != {"profile_version", "purpose", "profiles"}:
        raise ValueError("unsupported or incomplete profiles document")
    purpose = document["purpose"]
    if not isinstance(purpose, str) or not purpose.strip():
        raise ValueError("profiles purpose must be explicit")
    result: dict[str, JsonObject] = {}
    for row in _rows(document["profiles"], "profiles"):
        identity = row.get("entity_id")
        if not isinstance(identity, str) or not identity or identity in result:
            raise ValueError("profile entity IDs must be unique nonempty strings")
        if identity not in indexed:
            raise ValueError(f"orphan profile entity ID: {identity}")
        if set(row) - profile_keys != {"entity_id"} or not profile_keys.intersection(row):
            raise ValueError("unsupported or incomplete profile binding")
        result[identity] = {}
        for key in profile_keys.intersection(row):
            representation = "classical" if key == "executable_profile" else "quantum"
            result[identity][key] = copy.deepcopy(
                _object(row[key], f"{identity} {representation} profile")
            )
    return result


def compile_entities(
    catalog: object,
    entity_ids: Sequence[str],
    *,
    profiles: object = None,
    shape: tuple[int, int, int] = (9, 9, 9),
    ticks: int = 4,
    link_ticks: int = 1,
    representation: str = "classical",
) -> JsonObject:
    """Select explicit experiments separately from physical descriptors.

    Catalog v2 requires an external profiles document supplied by the caller.
    Legacy v1 authoring documents may still contain their explicit profiles.

    Carrier definitions and local-field operations are copied from profiles.
    The supplied field probes preserve retained-plus-outgoing component balances.
    Extending the domain is not a continuum-limit or physical-law claim.
    """
    source = _object(catalog, "catalog")
    version = source.get("catalog_version")
    if type(version) is not int or version not in (1, 2):
        raise ValueError("unsupported catalog_version")
    sections = ENTITY_SECTIONS if version == 2 else ENTITY_SECTIONS[:2]
    entries = [entry for section in sections for entry in _rows(source.get(section), section)]
    indexed: dict[str, JsonObject] = {}
    for entry in entries:
        identity = entry.get("id")
        if not isinstance(identity, str) or not identity or identity in indexed:
            raise ValueError("entity IDs must be unique nonempty strings")
        indexed[identity] = entry
    experiments = _profile_index(indexed, profiles, version)
    if version == 2:
        validate_catalog(source)
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
    profile_key = "executable_profile" if representation == "classical" else "quantum_profile"
    for identity in entity_ids:
        if identity not in indexed:
            raise ValueError(f"unknown entity: {identity}")
        if identity not in experiments or profile_key not in experiments[identity]:
            raise ValueError(f"unsupported {representation} representation: no profile for {identity}")
    if representation == "quantum":
        from event_universe.integration.quantum_entities import compile_quantum_entities

        return compile_quantum_entities(
            experiments, entity_ids, shape=shape, ticks=ticks, link_ticks=link_ticks
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
        profile = _object(experiments[identity]["executable_profile"], "profile")
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


def validate_profiles(catalog: object, profiles: object) -> dict[str, int]:
    """Validate each supplied experiment separately without constructing a world.

    The catalog must be a complete physical reference version 2. Bindings may
    cover any subset and contain either or both supported representations.
    Separate checks avoid imposing one world's capacity on the whole library.
    """
    source = _object(catalog, "catalog")
    validate_catalog(source)
    indexed = {
        entry["id"]: entry for section in ENTITY_SECTIONS for entry in _rows(source[section], section)
    }
    experiments = _profile_index(indexed, profiles, 2)
    summary = {"profiles": len(experiments), "classical": 0, "quantum": 0}
    for identity, experiment in experiments.items():
        for representation, key in (
            ("classical", "executable_profile"),
            ("quantum", "quantum_profile"),
        ):
            if key not in experiment:
                continue
            try:
                compile_entities(source, [identity], profiles=profiles, representation=representation)
            except (ValueError, OverflowError) as error:
                raise ValueError(f"{identity} {representation} profile: {error}") from error
            summary[representation] += 1
    return summary


def main() -> None:
    """Write a validated input for the existing runner and configuration UI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, help="explicit representation experiment document")
    parser.add_argument("--entity", action="append", required=True)
    parser.add_argument("--output-init", type=Path, required=True)
    parser.add_argument("--ticks", type=int, default=4)
    parser.add_argument("--representation", choices=("classical", "quantum"), default="classical")
    args = parser.parse_args()
    initial = compile_entities(
        parse_json_document(args.catalog.read_bytes()),
        args.entity,
        profiles=parse_json_document(args.profiles.read_bytes()) if args.profiles is not None else None,
        ticks=args.ticks,
        representation=args.representation,
    )
    args.output_init.parent.mkdir(parents=True, exist_ok=True)
    with args.output_init.open("x", encoding="utf-8") as output:
        output.write(json.dumps(initial, indent=2) + "\n")
    print(args.output_init)


if __name__ == "__main__":
    main()
