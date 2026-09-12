"""Validate descriptive physical reference data without selecting simulation laws.

Measurements, identity relations and possible channels are host-side references.
This module never computes a physical update or loads a representation profile.
"""

import argparse
import re
from decimal import Decimal
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from event_universe.initialization import parse_json_document

JsonObject = dict[str, Any]
ENTITY_SECTIONS = ("field_entities", "particle_entities", "disturbance_families")
PROPERTY_STATUSES = {
    "established",
    "measured",
    "theoretical",
    "reference",
    "unknown",
    "not_applicable",
    "context_dependent",
    "hypothetical",
    "observationally_inferred",
    "project_hypothesis",
    "upper_limit",
}
PROPERTY_KEYS = {
    "status",
    "sources",
    "value",
    "value_decimal",
    "unit",
    "context",
    "description",
    "precision",
    "uncertainty_decimal",
    "uncertainty_kind",
    "lower_bound_decimal",
    "upper_bound_decimal",
    "entity_id",
    "metadata_key",
    "constituent_ids",
    "reference",
    "confidence_level_percent",
}
EXECUTION_KEYS = {
    "op",
    "args",
    "expression",
    "expressions",
    "formula",
    "formulas",
    "updates",
    "assignments",
    "field_rules",
    "couplings",
    "transport",
    "hamiltonian",
    "rates",
    "executable_profile",
    "quantum_profile",
    "disturbance_types",
    "spatial_fields",
    "operation_costs",
    "seed_values",
    "output_types",
}
DECIMAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z")


def _object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    return value


def _strings(value: object, label: str, *, unique: bool = True) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    result = [_text(item, label) for item in value]
    if unique and len(result) != len(set(result)):
        raise ValueError(f"{label} must not contain duplicates")
    return result


def _index(value: object, label: str) -> dict[str, JsonObject]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    result = {}
    for item in value:
        row = _object(item, label)
        identity = _text(row.get("id"), f"{label} id")
        if identity in result:
            raise ValueError(f"duplicate {label} id: {identity}")
        result[identity] = row
    return result


def _references(value: object, valid: object, label: str, *, unique: bool = True) -> list[str]:
    names = _strings(value, label, unique=unique)
    if not isinstance(valid, (dict, set)) or any(name not in valid for name in names):
        raise ValueError(f"{label} contains an unknown reference")
    return names


def _sources(row: JsonObject, sources: JsonObject, label: str) -> None:
    if not _references(row.get("sources"), sources, f"{label} sources"):
        raise ValueError(f"{label} must cite at least one source")


def _no_execution(value: object) -> None:
    if isinstance(value, dict):
        if EXECUTION_KEYS.intersection(value):
            raise ValueError("physical catalog must not contain executable rules or formulas")
        for item in value.values():
            _no_execution(item)
    elif isinstance(value, list):
        for item in value:
            _no_execution(item)


def _decimal(value: object, label: str) -> Decimal:
    if not isinstance(value, str) or not DECIMAL.fullmatch(value):
        raise ValueError(f"{label} must be a finite decimal string")
    return Decimal(value)


def _properties(entities: dict[str, JsonObject], sources: JsonObject) -> None:
    aliases = {}
    for identity, entity in entities.items():
        properties = _object(entity.get("physical_properties"), f"{identity} physical_properties")
        if not properties:
            raise ValueError(f"{identity} must declare physical properties")
        for name, raw in properties.items():
            prop = _object(raw, f"{identity}.{name}")
            if (
                set(prop) - PROPERTY_KEYS
                or not isinstance(prop.get("status"), str)
                or prop["status"] not in PROPERTY_STATUSES
            ):
                raise ValueError(f"unsupported property descriptor: {identity}.{name}")
            _sources(prop, sources, f"{identity}.{name}")
            if not any(
                key in prop
                for key in (
                    "value",
                    "value_decimal",
                    "context",
                    "description",
                    "entity_id",
                    "metadata_key",
                    "upper_bound_decimal",
                    "lower_bound_decimal",
                )
            ):
                raise ValueError(f"{identity}.{name} needs a value or an explicit explanation")
            if "value" in prop:
                value = prop["value"]
                if not (
                    isinstance(value, str)
                    or type(value) is int
                    or (
                        isinstance(value, list)
                        and all(isinstance(item, str) or type(item) is int for item in value)
                    )
                ):
                    raise ValueError("property values must be descriptive primitives")
            for key in ("context", "description", "precision", "unit", "reference", "uncertainty_kind"):
                if key in prop:
                    _text(prop[key], key)
            numeric = {
                key: _decimal(value, key) for key, value in prop.items() if key.endswith("_decimal")
            }
            if numeric:
                _text(prop.get("unit"), "measurement unit")
                _text(prop.get("context"), "measurement context")
                if name in {"mass", "mass_upper_limit", "lifetime", "width", "decay_width"} and any(
                    value < 0 for value in numeric.values()
                ):
                    raise ValueError(f"{name} measurements and bounds must be nonnegative")
                if prop["status"] in {"unknown", "not_applicable", "reference"}:
                    raise ValueError("unknown or referenced properties cannot invent numerical values")
                if "uncertainty_decimal" in numeric and (
                    numeric["uncertainty_decimal"] < 0 or "value_decimal" not in numeric
                ):
                    raise ValueError("measurement uncertainty needs a value and must be nonnegative")
                if "uncertainty_decimal" in numeric:
                    _text(prop.get("uncertainty_kind"), "measurement uncertainty_kind")
                if (
                    "lower_bound_decimal" in numeric
                    and "upper_bound_decimal" in numeric
                    and numeric["lower_bound_decimal"] > numeric["upper_bound_decimal"]
                ):
                    raise ValueError("measurement bounds are reversed")
            if "confidence_level_percent" in prop:
                confidence = prop["confidence_level_percent"]
                if type(confidence) is not int or not 0 < confidence < 100 or not numeric:
                    raise ValueError(
                        "measurement confidence_level_percent must be an integer between 0 and 100"
                    )
            if "metadata_key" in prop:
                key = _text(prop["metadata_key"], "metadata_key")
                if (
                    key not in {"electric_charge_thirds", "twice_spin"}
                    or type(entity.get(key)) is not int
                ):
                    raise ValueError(
                        "property metadata_key must reference an intrinsic integer attribute"
                    )
                if "value" in prop or numeric:
                    raise ValueError("referenced intrinsic attributes must have one canonical value")
            if "constituent_ids" in prop:
                _references(prop["constituent_ids"], entities, "constituents", unique=False)
            if prop["status"] == "reference":
                target = _text(prop.get("entity_id"), "property reference entity_id")
                if target not in entities or name not in _object(
                    entities[target].get("physical_properties"), "reference properties"
                ):
                    raise ValueError("property reference must resolve to the same property")
                if "value" in prop or "metadata_key" in prop:
                    raise ValueError("property references cannot override their target")
                aliases[(identity, name)] = (target, name)
            elif "entity_id" in prop:
                raise ValueError("entity_id property aliases require reference status")
    for start in aliases:
        seen = set()
        cursor = start
        while cursor in aliases:
            if cursor in seen:
                raise ValueError("cyclic physical property reference")
            seen.add(cursor)
            cursor = aliases[cursor]


def validate_catalog(catalog: object) -> None:
    """Reject invalid references, measurements or executable catalog content.

    This checks the declared metadata contract, not the truth or completeness of
    physics. The shipped inventory has separate independent coverage tests.
    """
    data = _object(catalog, "catalog")
    required = {
        "catalog_version",
        "purpose",
        "scope",
        "notes",
        "sources",
        *ENTITY_SECTIONS,
        "interaction_families",
        "representative_channels",
        "examples",
    }
    if (
        set(data) != required
        or type(data.get("catalog_version")) is not int
        or data["catalog_version"] != 2
        or data.get("purpose") != "physical_reference"
    ):
        raise ValueError("expected a complete physical_reference catalog_version 2")
    _no_execution(data)
    if not _object(data["scope"], "catalog scope") or not _strings(
        data["notes"], "catalog notes", unique=False
    ):
        raise ValueError("catalog needs explicit scope and notes")
    sources = _object(data["sources"], "catalog sources")
    for name, raw in sources.items():
        row = _object(raw, f"source {name}")
        _text(row.get("title"), "source title")
        url = urlsplit(_text(row.get("url"), "source URL"))
        if url.scheme != "https" or not url.netloc:
            raise ValueError("source URL must be an absolute HTTPS reference")
    sections = {key: _index(data[key], key) for key in ENTITY_SECTIONS}
    entities: dict[str, JsonObject] = {}
    for section in sections.values():
        if entities.keys() & section.keys():
            raise ValueError("entity IDs must be unique across catalog sections")
        entities.update(section)
    interactions = _index(data["interaction_families"], "interaction families")
    for identity, row in entities.items():
        _text(row.get("label"), f"{identity} label")
        _text(row.get("physical_status"), f"{identity} physical_status")
        _sources(row, sources, identity)
        _references(row.get("interaction_ids"), interactions, f"{identity} interaction_ids")
    fields, particles, families = (sections[name] for name in ENTITY_SECTIONS)
    for identity, row in fields.items():
        for excitation in _references(
            row.get("excitation_ids"), particles, f"{identity} excitation_ids"
        ):
            if identity not in _strings(particles[excitation].get("field_ids"), "field_ids"):
                raise ValueError("field/excitation links must be reciprocal")
    for identity, row in (particles | families).items():
        for field in _references(row.get("field_ids"), fields, f"{identity} field_ids"):
            if identity in particles and identity not in fields[field]["excitation_ids"]:
                raise ValueError("particle/field links must be reciprocal")
    for identity, row in particles.items():
        partner = particles.get(_text(row.get("antiparticle_id"), "antiparticle_id"))
        if partner is None or partner.get("antiparticle_id") != identity:
            raise ValueError("antiparticle links must be reciprocal")
        for key in ("electric_charge_thirds", "twice_spin"):
            if type(row.get(key)) is not int:
                raise ValueError(f"{key} must be an integer")
        if (
            row["twice_spin"] < 0
            or partner.get("twice_spin") != row["twice_spin"]
            or partner.get("electric_charge_thirds") != -row["electric_charge_thirds"]
        ):
            raise ValueError("conjugate charge or spin attributes disagree")
        if partner.get("rest_mass_relation") != row.get("rest_mass_relation"):
            raise ValueError("conjugate mass relations disagree")
    _properties(entities, sources)
    for identity, row in interactions.items():
        _text(row.get("label"), "interaction label")
        _text(row.get("physical_status"), "interaction physical_status")
        if row.get("claim_level") != "descriptive_only" or not _strings(
            row.get("conditions"), "interaction conditions", unique=False
        ):
            raise ValueError("interaction families need descriptive_only status and conditions")
        participants = _references(row.get("participant_ids"), entities, "interaction participants")
        _references(row.get("mediator_ids"), entities, "interaction mediators")
        if not participants:
            raise ValueError("interaction needs declared participants")
        for participant in participants:
            if identity not in entities[participant]["interaction_ids"]:
                raise ValueError("interaction/participant links must be reciprocal")
        _sources(row, sources, identity)
    for identity, entity in entities.items():
        for interaction in entity["interaction_ids"]:
            if identity not in interactions[interaction]["participant_ids"]:
                raise ValueError("entity/interaction links must be reciprocal")
    for identity, row in _index(data["representative_channels"], "channels").items():
        family = interactions.get(_text(row.get("interaction_id"), "channel interaction_id"))
        if family is None:
            raise ValueError("channel interaction_id must resolve")
        if row.get("claim_level") != "descriptive_only" or not _strings(
            row.get("conditions"), "channel conditions", unique=False
        ):
            raise ValueError("channels need descriptive_only status and conditions")
        _text(row.get("physical_status"), "channel physical_status")
        incoming = _references(row.get("incoming_ids"), entities, "channel incoming_ids", unique=False)
        outgoing = _references(row.get("outgoing_ids"), entities, "channel outgoing_ids", unique=False)
        if not incoming or not outgoing:
            raise ValueError("channel must identify incoming and outgoing entities")
        if any(item not in family["participant_ids"] for item in incoming + outgoing):
            raise ValueError("channel entity is outside its interaction family")
        if all(
            type(entities[item].get("electric_charge_thirds")) is int for item in incoming + outgoing
        ):
            if sum(entities[item]["electric_charge_thirds"] for item in incoming) != sum(
                entities[item]["electric_charge_thirds"] for item in outgoing
            ):
                raise ValueError("channel electric charge is not balanced")
        _sources(row, sources, identity)
    if not isinstance(data["examples"], list):
        raise ValueError("examples must be an array")
    for raw in data["examples"]:
        example = _object(raw, "example")
        _text(example.get("path"), "example path")
        _references(example.get("entity_ids"), entities, "example entity_ids")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    validate_catalog(parse_json_document(args.catalog.read_bytes()))
    print("Physical reference catalog validated; no simulation laws were loaded.")


if __name__ == "__main__":
    main()
