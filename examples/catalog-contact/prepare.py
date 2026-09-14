"""Bind catalog properties to the existing causal contact example outside the engine."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

from event_universe.entity_catalog import resolve_property, validate_catalog
from event_universe.initialization import parse_initial_state
from event_universe.reference_units import encode_components

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = Path(__file__).with_name("experiment.json")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def prepare(entity_ids=None, experiment_path=EXPERIMENT):
    """Return a validated initialization and passive provenance; never run a world."""
    settings = load(experiment_path)
    catalog_path, units_path, template_path = (
        ROOT / settings[key] for key in ("catalog", "units", "template")
    )
    catalog, registry, raw = (load(path) for path in (catalog_path, units_path, template_path))
    validate_catalog(catalog)
    indexed = {row["id"]: row for row in catalog["particle_entities"]}
    allowed = settings["particle_ids"]
    if len(allowed) != len(set(allowed)) or any(
        identity not in indexed or indexed[identity]["physical_status"] != "established"
        for identity in allowed
    ):
        raise ValueError("particle_ids must uniquely select established catalog particles")
    selected = list(settings["default_entities"] if entity_ids is None else entity_ids)
    if not 1 <= len(selected) <= 10:
        raise ValueError("select 1 through 10 occurrences (three modes each)")
    if any(identity not in allowed for identity in selected):
        raise ValueError("selected particle is not enabled in particle_ids")
    if settings["missing_mass_policy"] != "marked_unassigned":
        raise ValueError("missing mass requires explicit marked_unassigned policy")

    template_domain = copy.deepcopy(raw["event_program"]["domains"][0])
    incoming, localized, probe = copy.deepcopy(raw["disturbance_types"])
    source_emission, output_emission = copy.deepcopy(raw["emissions"])
    carrier_fields = ["charge", "mass", "momentum_known", "mass_assigned", "spin_twice"]
    for role in (incoming, localized):
        role["fields"] = carrier_fields.copy()
        role["defaults"] = dict.fromkeys(carrier_fields, 0)
    for field in raw["fields"]:
        if field["name"] in ("charge", "mass"):
            field.update(settings[field["name"] + "_field"])
    raw["fields"].extend(
        {
            "name": name,
            "components": 1,
            "units": units,
            "signed": False,
            "conserved": False,
            "extensive": False,
        }
        for name, units in (
            ("mass_assigned", "0 unassigned; 1 catalog central value"),
            ("spin_twice", "doubled spin quantum number; passive metadata"),
        )
    )
    raw.update(model_id=settings["model_id"], ticks=settings["ticks"])
    raw["shape"] = [7, 2 * len(selected) + 1, 3]
    raw["disturbance_types"] = [localized, probe]
    output_emission["budget"] = settings["capture_budget"]
    raw["emissions"] = [output_emission]
    raw["seeds"] = []
    program = raw["event_program"]
    program["tickets"] = [settings["ticket"]] * (raw["ticks"] * len(selected))
    program["addresses"], program["domains"] = [], []
    bindings, occurrence_rows = {}, []
    for occurrence, identity in enumerate(selected):
        if identity not in bindings:
            entity = indexed[identity]
            charge = resolve_property(catalog, identity, "electric_charge")
            charge_encoding = encode_components(
                registry, charge["value_decimal"], charge["unit"], settings["charge_field"]
            )
            mass = resolve_property(catalog, identity, "mass")
            mass_encoding = None
            if "value_decimal" in mass:
                mass_encoding = encode_components(
                    registry,
                    mass["value_decimal"],
                    mass["unit"],
                    settings["mass_field"],
                    max_error=settings["mass_error_by_source_unit"][mass["unit"]],
                )
            values = {
                "charge": charge_encoding["value"],
                "mass": 0 if mass_encoding is None else mass_encoding["value"],
                "momentum_known": 0,
                "mass_assigned": int(mass_encoding is not None),
                "spin_twice": entity["twice_spin"],
            }
            source = copy.deepcopy(incoming)
            source["name"] = "source_" + identity
            source["defaults"] = values
            raw["disturbance_types"].append(source)
            emission = copy.deepcopy(source_emission)
            emission.update(type=source["name"], budget=settings["source_budget"])
            raw["emissions"].append(emission)
            bindings[identity] = {
                "source_type": source["name"],
                "values": values,
                "charge_encoding": charge_encoding,
                "mass_encoding": mass_encoding,
                "mass_reference": mass,
                "catalog_reference": entity,
            }
        binding = bindings[identity]
        offset = 3 * occurrence
        positions = [[x, 1 + 2 * occurrence, 1] for x in (1, 2, 3)]
        program["addresses"].extend(positions)
        domain = copy.deepcopy(template_domain)
        domain["name"] = "occurrence_" + str(occurrence)
        domain["register_indices"] = [offset + index for index in domain["register_indices"]]
        domain["source"]["register_index"] += offset
        domain["source"]["type"] = binding["source_type"]
        domain["capture"]["register_indices"] = [
            offset + index for index in domain["capture"]["register_indices"]
        ]
        domain["capture"]["output"]["values"] = copy.deepcopy(binding["values"])
        for phase in domain["phases"]:
            for gate in phase:
                gate["register_indices"] = [offset + index for index in gate["register_indices"]]
        program["domains"].append(domain)
        raw["seeds"].extend(
            [
                {"position": positions[0], "type": binding["source_type"]},
                {"position": positions[0], "type": probe["name"]},
                {"position": positions[2], "type": probe["name"]},
            ]
        )
        occurrence_rows.append({"entity_id": identity, "domain": domain["name"], "positions": positions})
    parse_initial_state(raw)
    report = {
        "model": program["model"],
        "bindings": bindings,
        "occurrences": occurrence_rows,
        "notes": settings["notes"],
        "dependencies_sha256": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (catalog_path, units_path, template_path)
        },
    }
    return raw, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", type=Path, default=EXPERIMENT)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--entity", action="append")
    selection.add_argument("--all", action="store_true", help="prepare one bounded world per particle")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    settings = load(args.experiment)
    selections = [[identity] for identity in settings["particle_ids"]] if args.all else [args.entity]
    prepared = [prepare(ids, args.experiment) for ids in selections]
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("output must be a new or empty directory")
    args.output.mkdir(parents=True, exist_ok=True)
    for (raw, report), ids in zip(prepared, selections, strict=True):
        name = ids[0] if args.all else "demo"
        for suffix, document in (("init", raw), ("bindings", report)):
            (args.output / f"{name}.{suffix}.json").write_text(
                json.dumps(document, indent=2) + "\n", encoding="utf-8"
            )
    print(f"Prepared and validated {len(prepared)} worlds; no simulation was run.")


if __name__ == "__main__":
    main()
