"""Prepare an excitation in its field's existing finite quantum registers.

This host-side authoring adapter adds frequency/energy preparation metadata, not
transport, a phase generator or an observer measurement. The ordinary runtime
input is unchanged in shape. No separate particle registers or classical carrier
are created. The Planck relation is a selected readout, not an emergence result.
"""

import argparse
import hashlib
import json
from math import gcd
from pathlib import Path
from typing import Any

from event_universe.configuration_validation import prepare_initialization
from event_universe.core.integer import checked_work
from event_universe.entities import compile_entities
from event_universe.entity_catalog import validate_catalog
from event_universe.initialization import parse_json_document

MODEL = "field-excitation-frequency-preparation-v1"


def _object(value: object, label: str, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} must contain exactly {sorted(keys)}")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f"{label} must be a nonempty trimmed string")
    return value


def _integer(value: object, label: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer of at least {minimum}")
    return checked_work(value)


def _ratio(numerator: int, denominator: int) -> dict[str, int]:
    divisor = gcd(numerator, denominator)
    return {"numerator": numerator // divisor, "denominator": denominator // divisor}


def prepare(
    definition: object, catalog: object, profiles: object
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return validated runtime input and a bound, read-only preparation manifest.

    Both polarizations share the selected frequency in the named preparation
    frame. Its time unit is not calibrated to a lattice tick or a local clock.
    Energy is above vacuum in units h/time_unit; normalized h is exactly one.
    """
    raw = _object(
        definition,
        "definition",
        {
            "definition_version",
            "representation",
            "entity_id",
            "field_id",
            "frequency",
            "occupations",
            "shape",
            "link_ticks",
            "ticks",
        },
    )
    if type(raw["definition_version"]) is not int or raw["definition_version"] != 1:
        raise ValueError("unsupported definition_version")
    if raw["representation"] != "finite_quantum_field_preparation":
        raise ValueError("unsupported excitation representation")
    frequency = _object(
        raw["frequency"], "frequency", {"numerator", "denominator", "reference_frame", "time_unit"}
    )
    numerator = _integer(frequency["numerator"], "frequency numerator", 1)
    denominator = _integer(frequency["denominator"], "frequency denominator", 1)
    frame = _text(frequency["reference_frame"], "reference_frame")
    time_unit = _text(frequency["time_unit"], "time_unit")
    entity_id = _text(raw["entity_id"], "entity_id")
    field_id = _text(raw["field_id"], "field_id")
    # Catalog references authorize an association, never infer an executable law.
    validate_catalog(catalog)
    assert isinstance(catalog, dict)
    particles = {item["id"]: item for item in catalog["particle_entities"]}
    fields = {item["id"]: item for item in catalog["field_entities"]}
    if (
        entity_id not in particles
        or field_id not in fields
        or field_id not in particles[entity_id].get("field_ids", [])
        or entity_id not in fields[field_id].get("excitation_ids", [])
    ):
        raise ValueError("excitation must reference its reciprocal catalog field")
    shape = raw["shape"]
    if not isinstance(shape, list) or len(shape) != 3:
        raise ValueError("shape must contain three integer dimensions")
    dimensions = tuple(_integer(size, "shape dimension", 5) for size in shape)
    ticks = _integer(raw["ticks"], "ticks")
    link_ticks = _integer(raw["link_ticks"], "link_ticks", 1)
    # Compile the field alone: selecting the particle too would duplicate modes.
    initial = compile_entities(
        catalog,
        [field_id],
        profiles=profiles,
        shape=dimensions,
        ticks=ticks,
        link_ticks=link_ticks,
        representation="quantum",
    )
    assert isinstance(profiles, dict)
    selected = next(row for row in profiles["profiles"] if row["entity_id"] == field_id)
    registers = selected["quantum_profile"]["registers"]
    names = {register["name"] for register in registers}
    occupations = _object(raw["occupations"], "occupations", names)
    levels = []
    for register in registers:
        basis = register["basis"]
        if basis != [f"n={index}" for index in range(len(basis))]:
            raise ValueError("field profile must declare ordered number-occupation bases")
        level = _integer(occupations[register["name"]], "occupation")
        if level >= len(basis):
            raise ValueError("occupation exceeds the explicitly truncated field basis")
        levels.append(level)
    initial["model_id"] = MODEL
    initial["event_program"]["initial_levels"] = levels
    prepare_initialization(initial)
    reduced = _ratio(numerator, denominator)
    count = sum(levels)
    energy = _ratio(checked_work(count * reduced["numerator"]), reduced["denominator"])
    manifest = {
        "preparation_version": 1,
        "model_id": MODEL,
        "entity_id": entity_id,
        "field_id": field_id,
        "state_owner": "event_program quantum field registers",
        "register_names": initial["event_program"]["register_names"].copy(),
        "occupations": dict(zip((r["name"] for r in registers), levels, strict=True)),
        "quantum_count": count,
        "frequency": {
            **reduced,
            "reference_frame": frame,
            "time_unit": time_unit,
            "unit": "cycles per time_unit",
            "status": "declared_preparation",
        },
        "energy": {
            "per_quantum": reduced.copy(),
            "total_above_vacuum": energy,
            "unit": "h per time_unit",
            "reference_frame": frame,
            "time_unit": time_unit,
            "status": "derived_preparation_readout_not_runtime_stock",
            "relation": "E_per_quantum = h*f; E_total_above_vacuum = N*h*f",
        },
        "limitations": [
            "One selected frequency for all declared polarization modes; no spectral bandwidth.",
            "No frequency-dependent phase evolution, propagation, emission or detection law.",
            "Register addresses are preparation support, not a resolved photon wave packet.",
            "No measured observer frequency, clock calibration or spatial-field composition.",
            "The old classical carrier proxy and its transport policy remain unchanged.",
        ],
    }
    return initial, manifest


def write_preparation(
    definition_path: Path, catalog_path: Path, profiles_path: Path, output: Path
) -> dict[str, Any]:
    """Read each input once, validate before writing, and never replace existing output."""
    sources = {"definition": definition_path, "catalog": catalog_path, "profiles": profiles_path}
    contents = {key: path.read_bytes() for key, path in sources.items()}
    documents = {key: parse_json_document(data) for key, data in contents.items()}
    initial, manifest = prepare(**documents)
    encoded = (json.dumps(initial, indent=2) + "\n").encode("utf-8")
    manifest["initialization_sha256"] = hashlib.sha256(encoded).hexdigest()
    manifest["source_sha256"] = {key: hashlib.sha256(data).hexdigest() for key, data in contents.items()}
    output.mkdir(parents=True, exist_ok=False)
    (output / "definition.json").write_bytes(contents["definition"])
    (output / "initialization.json").write_bytes(encoded)
    (output / "preparation.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definition", type=Path, default=Path(__file__).with_name("definition.json"))
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = write_preparation(args.definition, args.catalog, args.profiles, args.output)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
