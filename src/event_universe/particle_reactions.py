"""Compile established catalog particle identities into bounded local reactions.

Particle names remain host-side data. The generated initialization uses the generic
n-to-m reaction owner and exact conserved charge, configured energy and momentum
fields. No species name selects a runtime law or reaction probability.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from event_universe.core.disturbance_state import (
    MAX_REACTION_INPUTS,
    MAX_REACTION_OUTPUTS,
    OPERATIONS,
)
from event_universe.core.state import checked, checked_work
from event_universe.initialization import parse_initial_state, parse_json_document

JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class ParticleFact:
    identity: str
    antiparticle_id: str
    electric_charge_thirds: int
    twice_spin: int
    conjugacy_status: str
    rest_mass_relation: str
    physical_status: str

    @property
    def statistics_class(self) -> str:
        return "fermion" if self.twice_spin % 2 else "boson"


@dataclass(frozen=True, slots=True)
class ReactionLeg:
    entity: str
    energy: int
    momentum: tuple[int, int, int]


def _object(value: object, label: str, allowed: set[str] | None = None) -> JsonObject:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    if allowed is not None and set(value) != allowed:
        raise ValueError(f"{label} must contain exactly {sorted(allowed)}")
    return value


def _array(value: object, label: str, size: int) -> list[object]:
    if not isinstance(value, list) or len(value) != size:
        raise ValueError(f"{label} must contain exactly {size} items")
    return value


def _array_range(value: object, label: str, maximum: int, minimum: int = 1) -> list[object]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError(f"{label} must contain {minimum} through {maximum} items")
    return value


def _integer(value: object, label: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise ValueError(f"{label} must be an integer")
    checked(value)
    if minimum is not None and value < minimum:
        raise ValueError(f"{label} must be at least {minimum}")
    return value


def _particle_index(catalog: object) -> dict[str, JsonObject]:
    source = _object(catalog, "catalog")
    if type(source.get("catalog_version")) is not int or source["catalog_version"] != 1:
        raise ValueError("unsupported catalog_version")
    rows = source.get("particle_entities")
    if not isinstance(rows, list):
        raise ValueError("catalog particle_entities must be an array")
    indexed: dict[str, JsonObject] = {}
    for raw in rows:
        row = _object(raw, "particle entity")
        identity = row.get("id")
        if not isinstance(identity, str) or not identity or identity in indexed:
            raise ValueError("particle IDs must be unique nonempty strings")
        indexed[identity] = row
    return indexed


def _particle_fact(indexed: dict[str, JsonObject], identity: str) -> ParticleFact:
    if identity not in indexed:
        raise ValueError(f"unknown particle entity: {identity}")
    row = indexed[identity]
    antiparticle = row.get("antiparticle_id")
    conjugacy = row.get("conjugacy_status")
    rest_mass = row.get("rest_mass_relation")
    status = row.get("physical_status")
    if (
        not isinstance(antiparticle, str)
        or not antiparticle
        or not isinstance(conjugacy, str)
        or not conjugacy
        or not isinstance(rest_mass, str)
        or not rest_mass
        or not isinstance(status, str)
        or not status
    ):
        raise ValueError(f"particle {identity} has incomplete identity metadata")
    charge = _integer(row.get("electric_charge_thirds"), f"{identity}.electric_charge_thirds")
    twice_spin = _integer(row.get("twice_spin"), f"{identity}.twice_spin", minimum=0)
    if status != "established":
        raise ValueError(f"particle reaction probes require established entities: {identity}")
    if antiparticle not in indexed:
        raise ValueError(f"particle {identity} has unknown antiparticle")
    partner = indexed[antiparticle]
    if partner.get("antiparticle_id") != identity:
        raise ValueError(f"particle {identity} has a nonreciprocal antiparticle relation")
    partner_charge = _integer(
        partner.get("electric_charge_thirds"), f"{antiparticle}.electric_charge_thirds"
    )
    partner_spin = _integer(partner.get("twice_spin"), f"{antiparticle}.twice_spin", minimum=0)
    if partner_charge != -charge or partner_spin != twice_spin:
        raise ValueError(f"particle {identity} disagrees with its antiparticle charge or spin")
    if partner.get("rest_mass_relation") != rest_mass:
        raise ValueError(f"particle {identity} disagrees with its antiparticle mass relation")
    if conjugacy == "self_conjugate" and antiparticle != identity:
        raise ValueError(f"self-conjugate particle {identity} must reference itself")
    if conjugacy == "distinct_antiparticle" and antiparticle == identity:
        raise ValueError(f"distinct-antiparticle particle {identity} cannot reference itself")
    return ParticleFact(identity, antiparticle, charge, twice_spin, conjugacy, rest_mass, status)


def _leg(value: object, label: str, indexed: dict[str, JsonObject]) -> ReactionLeg:
    obj = _object(value, label, {"entity", "energy", "momentum"})
    entity = obj["entity"]
    if not isinstance(entity, str) or not entity:
        raise ValueError(f"{label}.entity must be a nonempty string")
    _particle_fact(indexed, entity)
    energy = _integer(obj["energy"], f"{label}.energy", minimum=0)
    momentum_raw = _array(obj["momentum"], f"{label}.momentum", 3)
    momentum = tuple(_integer(value, f"{label}.momentum") for value in momentum_raw)
    return ReactionLeg(entity, energy, momentum)  # type: ignore[arg-type]


def _sum_scalar(values: tuple[int, ...]) -> int:
    total = 0
    for value in values:
        total = checked(checked_work(total + value))
    return total


def _sum_vector(values: tuple[tuple[int, int, int], ...]) -> tuple[int, int, int]:
    totals = [0, 0, 0]
    for value in values:
        for component in range(3):
            totals[component] = checked(checked_work(totals[component] + value[component]))
    return totals[0], totals[1], totals[2]


def _reaction_document(
    catalog: object, reaction: object
) -> tuple[JsonObject, dict[str, JsonObject], tuple[ReactionLeg, ...], tuple[ReactionLeg, ...]]:
    indexed = _particle_index(catalog)
    raw = _object(reaction, "reaction")
    required = {"reaction_version", "model_id", "inputs", "outputs"}
    optional = {"shape", "position", "ticks", "link_ticks", "move_outputs"}
    if not required <= set(raw) or not set(raw) <= required | optional:
        raise ValueError("reaction has missing or unsupported keys")
    version = raw["reaction_version"]
    if type(version) is not int or version not in (1, 2):
        raise ValueError("unsupported reaction_version")
    if not isinstance(raw["model_id"], str) or not raw["model_id"]:
        raise ValueError("reaction.model_id must be a nonempty string")
    if version == 1:
        input_rows = _array(raw["inputs"], "inputs", 2)
        output_rows = _array(raw["outputs"], "outputs", 2)
    else:
        input_rows = _array_range(raw["inputs"], "inputs", MAX_REACTION_INPUTS)
        output_rows = _array_range(raw["outputs"], "outputs", MAX_REACTION_OUTPUTS)
    inputs = tuple(_leg(item, f"inputs[{index}]", indexed) for index, item in enumerate(input_rows))
    outputs = tuple(_leg(item, f"outputs[{index}]", indexed) for index, item in enumerate(output_rows))
    return raw, indexed, inputs, outputs


def reaction_manifest(catalog: object, reaction: object) -> JsonObject:
    raw, indexed, inputs, outputs = _reaction_document(catalog, reaction)
    input_facts = tuple(_particle_fact(indexed, leg.entity) for leg in inputs)
    output_facts = tuple(_particle_fact(indexed, leg.entity) for leg in outputs)
    charge_before = _sum_scalar(tuple(fact.electric_charge_thirds for fact in input_facts))
    charge_after = _sum_scalar(tuple(fact.electric_charge_thirds for fact in output_facts))
    energy_before = _sum_scalar(tuple(leg.energy for leg in inputs))
    energy_after = _sum_scalar(tuple(leg.energy for leg in outputs))
    momentum_before = _sum_vector(tuple(leg.momentum for leg in inputs))
    momentum_after = _sum_vector(tuple(leg.momentum for leg in outputs))
    if charge_before != charge_after:
        raise ValueError("reaction violates electric charge conservation")
    if energy_before != energy_after:
        raise ValueError("reaction violates configured energy conservation")
    if momentum_before != momentum_after:
        raise ValueError("reaction violates configured momentum conservation")

    def facts(legs: tuple[ReactionLeg, ...]) -> list[JsonObject]:
        result: list[JsonObject] = []
        for leg in legs:
            fact = _particle_fact(indexed, leg.entity)
            result.append(
                {
                    "entity": fact.identity,
                    "antiparticle_id": fact.antiparticle_id,
                    "electric_charge_thirds": fact.electric_charge_thirds,
                    "twice_spin": fact.twice_spin,
                    "statistics_class": fact.statistics_class,
                    "conjugacy_status": fact.conjugacy_status,
                    "rest_mass_relation": fact.rest_mass_relation,
                    "energy": leg.energy,
                    "momentum": list(leg.momentum),
                }
            )
        return result

    return {
        "reaction_version": raw["reaction_version"],
        "model_id": raw["model_id"],
        "inputs": facts(inputs),
        "outputs": facts(outputs),
        "conservation": {
            "electric_charge_thirds": {"before": charge_before, "after": charge_after},
            "configured_energy": {"before": energy_before, "after": energy_after},
            "configured_momentum": {"before": list(momentum_before), "after": list(momentum_after)},
        },
        "runtime_enforcement": ["charge", "energy", "momentum"],
        "limits": [
            f"Reaction version 2 supports one through {MAX_REACTION_INPUTS} inputs and one through {MAX_REACTION_OUTPUTS} outputs; version 1 remains exactly two-to-two.",
            "Configured energy is an explicit integer inventory; this adapter does not derive a relativistic dispersion relation.",
            "Spin statistics are identity metadata here; exchange antisymmetry and bosonic symmetrization remain quantum-dynamics work.",
            "Baryon and lepton numbers are not promoted to universal exact invariants by this adapter.",
        ],
    }


def compile_particle_reaction(catalog: object, reaction: object) -> tuple[JsonObject, JsonObject]:
    raw, indexed, inputs, outputs = _reaction_document(catalog, reaction)
    manifest = reaction_manifest(catalog, reaction)
    shape_raw = raw.get("shape", [9, 9, 9])
    shape_items = _array(shape_raw, "shape", 3)
    shape = tuple(_integer(value, "shape", minimum=5) for value in shape_items)
    position_raw = raw.get("position", [value // 2 for value in shape])
    position_items = _array(position_raw, "position", 3)
    position = tuple(_integer(value, "position", minimum=0) for value in position_items)
    if any(value >= size for value, size in zip(position, shape, strict=True)):
        raise ValueError("reaction position must be within shape")
    ticks = _integer(raw.get("ticks", 4), "ticks", minimum=1)
    link_ticks = _integer(raw.get("link_ticks", 1), "link_ticks", minimum=1)
    move_outputs = raw.get("move_outputs", True)
    if type(move_outputs) is not bool:
        raise ValueError("move_outputs must be a boolean")

    input_facts = tuple(_particle_fact(indexed, leg.entity) for leg in inputs)
    output_facts = tuple(_particle_fact(indexed, leg.entity) for leg in outputs)
    fields: list[JsonObject] = [
        {
            "name": "charge",
            "components": 1,
            "units": "one third elementary charge",
            "signed": True,
            "conserved": True,
            "extensive": True,
        },
        {
            "name": "energy",
            "components": 1,
            "units": "configured reaction energy unit",
            "signed": False,
            "conserved": True,
            "extensive": True,
        },
        {
            "name": "momentum",
            "components": 3,
            "units": "configured reaction momentum unit",
            "signed": True,
            "conserved": True,
            "extensive": True,
        },
    ]
    input_names = tuple(f"reaction input {index}" for index in range(len(inputs)))
    output_names = tuple(f"reaction output {index}" for index in range(len(outputs)))
    types: list[JsonObject] = []
    for leg, fact in zip(inputs, input_facts, strict=True):
        types.append(
            {
                "name": input_names[len(types)],
                "fields": ["charge", "energy", "momentum"],
                "defaults": {
                    "charge": fact.electric_charge_thirds,
                    "energy": leg.energy,
                    "momentum": list(leg.momentum),
                },
                "transport": {"mode": "hold"},
            }
        )
    for index, (leg, fact) in enumerate(zip(outputs, output_facts, strict=True)):
        transport: JsonObject = {"mode": "hold"}
        if move_outputs:
            transport = {"mode": "move", "direction_field": "momentum", "rate": 1, "rate_denominator": 1}
        types.append(
            {
                "name": output_names[index],
                "fields": ["charge", "energy", "momentum"],
                "defaults": {
                    "charge": fact.electric_charge_thirds,
                    "energy": leg.energy,
                    "momentum": list(leg.momentum),
                },
                "transport": transport,
            }
        )

    assignments: list[JsonObject] = []
    for output, (leg, fact) in enumerate(zip(outputs, output_facts, strict=True)):
        assignments.extend(
            [
                {"output": output, "field": "charge", "expression": fact.electric_charge_thirds},
                {"output": output, "field": "energy", "expression": leg.energy},
                {"output": output, "field": "momentum", "expression": list(leg.momentum)},
            ]
        )
    initial: JsonObject = {
        "schema_version": 1,
        "model_id": raw["model_id"],
        "shape": list(shape),
        "boundary": "open",
        "slots_per_cell": max(len(inputs), len(outputs)),
        "link_ticks": link_ticks,
        "normal_budget": 10000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": fields,
        "disturbance_types": types,
        "reactions": [
            {
                "name": "configured particle reaction",
                "input_types": list(input_names),
                "output_types": list(output_names),
                "assignments": assignments,
            }
        ],
        "seeds": [
            {
                "position": list(position),
                "type": input_names[index],
                "values": {
                    "charge": input_facts[index].electric_charge_thirds,
                    "energy": inputs[index].energy,
                    "momentum": list(inputs[index].momentum),
                },
            }
            for index in range(len(inputs))
        ],
    }
    parse_initial_state(initial)
    return initial, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--reaction", type=Path, required=True)
    parser.add_argument("--output-init", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path)
    args = parser.parse_args()
    initial, manifest = compile_particle_reaction(
        parse_json_document(args.catalog.read_bytes()),
        parse_json_document(args.reaction.read_bytes()),
    )
    args.output_init.parent.mkdir(parents=True, exist_ok=True)
    with args.output_init.open("x", encoding="utf-8") as output:
        output.write(json.dumps(initial, indent=2) + "\n")
    if args.output_manifest is not None:
        args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
        with args.output_manifest.open("x", encoding="utf-8") as output:
            output.write(json.dumps(manifest, indent=2) + "\n")
    print(args.output_init)


if __name__ == "__main__":
    main()
