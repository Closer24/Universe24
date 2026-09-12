"""Compile catalog particle facts into a bounded local two-to-two reaction probe.

This host-side adapter does not add species dispatch to the engine. Particle
identity supplies data only. The compiled initialization uses the existing local
conversion transaction and marks electric charge, configured energy and momentum
as conserved physical fields so the runtime rejects an imbalanced proposal.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from event_universe.core.disturbance_state import OPERATIONS
from event_universe.core.state import checked, checked_work
from event_universe.initialization import parse_initial_state, parse_json_document

JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class ParticleFact:
    """Integer catalog identity needed by the generic reaction authoring layer."""

    identity: str
    antiparticle_id: str
    electric_charge_thirds: int
    twice_spin: int
    conjugacy_status: str
    rest_mass_relation: str
    physical_status: str

    @property
    def statistics_class(self) -> str:
        """Classify the catalog spin using the established spin-statistics pairing."""
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
    momentum = (
        _integer(momentum_raw[0], f"{label}.momentum"),
        _integer(momentum_raw[1], f"{label}.momentum"),
        _integer(momentum_raw[2], f"{label}.momentum"),
    )
    return ReactionLeg(entity, energy, momentum)


def _sum_scalar(values: tuple[int, ...]) -> int:
    if len(values) != 2:
        raise ValueError("reaction scalar sum requires exactly two values")
    return checked(checked_work(values[0] + values[1]))


def _sum_vector(values: tuple[tuple[int, int, int], ...]) -> tuple[int, int, int]:
    if len(values) != 2:
        raise ValueError("reaction vector sum requires exactly two values")
    left, right = values
    return (
        checked(checked_work(left[0] + right[0])),
        checked(checked_work(left[1] + right[1])),
        checked(checked_work(left[2] + right[2])),
    )


def _reaction_document(
    catalog: object, reaction: object
) -> tuple[
    JsonObject, dict[str, JsonObject], tuple[ReactionLeg, ReactionLeg], tuple[ReactionLeg, ReactionLeg]
]:
    indexed = _particle_index(catalog)
    raw = _object(reaction, "reaction")
    required = {"reaction_version", "model_id", "inputs", "outputs"}
    optional = {"shape", "position", "ticks", "link_ticks", "move_outputs"}
    if not required <= set(raw) or not set(raw) <= required | optional:
        raise ValueError("reaction has missing or unsupported keys")
    if raw["reaction_version"] != 1 or type(raw["reaction_version"]) is not int:
        raise ValueError("unsupported reaction_version")
    if not isinstance(raw["model_id"], str) or not raw["model_id"]:
        raise ValueError("reaction.model_id must be a nonempty string")
    input_rows = _array(raw["inputs"], "inputs", 2)
    output_rows = _array(raw["outputs"], "outputs", 2)
    inputs = (
        _leg(input_rows[0], "inputs[0]", indexed),
        _leg(input_rows[1], "inputs[1]", indexed),
    )
    outputs = (
        _leg(output_rows[0], "outputs[0]", indexed),
        _leg(output_rows[1], "outputs[1]", indexed),
    )
    return raw, indexed, inputs, outputs


def reaction_manifest(catalog: object, reaction: object) -> JsonObject:
    """Validate known particle facts and exact additive reaction balances."""
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

    def facts(legs: tuple[ReactionLeg, ReactionLeg]) -> list[JsonObject]:
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
        "reaction_version": 1,
        "model_id": raw["model_id"],
        "inputs": facts(inputs),
        "outputs": facts(outputs),
        "conservation": {
            "electric_charge_thirds": {"before": charge_before, "after": charge_after},
            "configured_energy": {"before": energy_before, "after": energy_after},
            "configured_momentum": {
                "before": list(momentum_before),
                "after": list(momentum_after),
            },
        },
        "runtime_enforcement": ["charge", "energy", "momentum"],
        "limits": [
            "The current runtime conversion contract is exactly two input records to two output records.",
            "Configured energy is an explicit integer inventory; this adapter does not derive a relativistic dispersion relation.",
            "Spin statistics are identity metadata here; exchange antisymmetry and bosonic symmetrization remain quantum-dynamics work.",
            "Baryon and lepton numbers are not promoted to universal exact invariants by this adapter.",
        ],
    }


def _total_expression(field: str) -> JsonObject:
    return {
        "op": "add",
        "args": [
            {"field": field, "side": "left"},
            {"field": field, "side": "right"},
        ],
    }


def compile_particle_reaction(catalog: object, reaction: object) -> tuple[JsonObject, JsonObject]:
    """Compile a validated two-to-two particle reaction through the generic engine."""
    raw, indexed, inputs, outputs = _reaction_document(catalog, reaction)
    manifest = reaction_manifest(catalog, reaction)
    shape_raw = raw.get("shape", [9, 9, 9])
    shape = tuple(_integer(v, "shape", minimum=5) for v in _array(shape_raw, "shape", 3))
    position_raw = raw.get("position", [value // 2 for value in shape])
    position = tuple(_integer(v, "position", minimum=0) for v in _array(position_raw, "position", 3))
    if any(v >= size for v, size in zip(position, shape, strict=True)):
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
    type_names = (
        "reaction input left",
        "reaction input right",
        "reaction output left",
        "reaction output right",
    )
    types: list[JsonObject] = []
    for index, (leg, fact) in enumerate(
        zip((*inputs, *outputs), (*input_facts, *output_facts), strict=True)
    ):
        output = index >= 2
        transport: JsonObject = {"mode": "hold"}
        if output and move_outputs:
            transport = {
                "mode": "move",
                "direction_field": "momentum",
                "rate": 1,
                "rate_denominator": 1,
            }
        types.append(
            {
                "name": type_names[index],
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
    for side, leg, fact in zip(("left", "right"), outputs, output_facts, strict=True):
        assignments.extend(
            [
                {"side": side, "field": "charge", "expression": fact.electric_charge_thirds},
                {"side": side, "field": "energy", "expression": leg.energy},
                {"side": side, "field": "momentum", "expression": list(leg.momentum)},
            ]
        )
    initial: JsonObject = {
        "schema_version": 1,
        "model_id": raw["model_id"],
        "shape": list(shape),
        "boundary": "open",
        "slots_per_cell": 2,
        "link_ticks": link_ticks,
        "normal_budget": 10000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": fields,
        "disturbance_types": types,
        "interactions": [
            {
                "name": "configured particle reaction",
                "left_type": type_names[0],
                "right_type": type_names[1],
                "output_types": {"left": type_names[2], "right": type_names[3]},
                "assignments": assignments,
                "invariants": [
                    {"name": "electric charge", "expression": _total_expression("charge")},
                    {"name": "configured energy", "expression": _total_expression("energy")},
                    {"name": "momentum", "expression": _total_expression("momentum")},
                ],
            }
        ],
        "seeds": [
            {
                "position": list(position),
                "type": type_names[index],
                "values": {
                    "charge": input_facts[index].electric_charge_thirds,
                    "energy": inputs[index].energy,
                    "momentum": list(inputs[index].momentum),
                },
            }
            for index in range(2)
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
