"""Compose reusable model definitions with explicit world inputs before a run.

This authoring boundary owns document composition and field-coupling coverage.
Initialization remains the semantic owner of names, values and physical rules.
"""

import argparse
import copy
import json
from pathlib import Path
from typing import cast

from event_universe.core.disturbance_state import OPERATIONS, Expression, InitialState
from event_universe.initialization import parse_initial_state
from event_universe.json_documents import parse_json_document

_WORLD_KEYS = frozenset(
    {
        "shape",
        "boundary",
        "slots_per_cell",
        "link_ticks",
        "normal_budget",
        "ticks",
        "operation_costs",
        "seeds",
        "spatial_seeds",
        "observer",
        "event_program",
    }
)


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    return cast(dict[str, object], value)


def _body(document: object, version_key: str, body_key: str) -> dict[str, object]:
    outer = _object(document, version_key.removesuffix("_version"))
    if set(outer) != {version_key, body_key}:
        raise ValueError(f"document requires exactly {version_key} and {body_key}")
    if type(outer[version_key]) is not int or outer[version_key] != 1:
        raise ValueError(f"{version_key} must be integer 1")
    return _object(outer[body_key], body_key)


def _model(document: object) -> dict[str, object]:
    model = _body(document, "definitions_version", "model")
    misplaced = model.keys() & _WORLD_KEYS
    if misplaced:
        raise ValueError(f"model contains experiment-owned keys: {', '.join(sorted(misplaced))}")
    return model


def _reads_spatial(expression: Expression | None) -> bool:
    if expression is None:
        return False
    return (
        expression.op == "received"
        or (expression.op == "field" and expression.side == 1)
        or any(_reads_spatial(argument) for argument in expression.arguments)
    )


def _require_field_couplings(initial: InitialState) -> InitialState:
    """Require a declared field source/response, without inferring its effect.

    This authoring policy inspects already validated bounded rules. A joint
    interaction must write spatial state or read it in an assignment/condition;
    mentioning a spatial field only in an invariant is not a coupling.
    """
    coupled = {rule.type_index for rule in initial.emissions}
    coupled.update(rule.type_index for rule in initial.spatial_couplings)
    coupled.update(
        rule.type_index
        for rule in initial.spatial_interactions
        if _reads_spatial(rule.when)
        or any(
            assignment.side == 1 or _reads_spatial(assignment.expression)
            for assignment in rule.assignments
        )
    )
    missing = [kind.name for index, kind in enumerate(initial.disturbances) if index not in coupled]
    if missing:
        raise ValueError(
            "each disturbance requires an explicit field coupling; missing for: " + ", ".join(missing)
        )
    return initial


def validate_model_definitions(document: object) -> InitialState:
    """Validate the complete bounded model using an empty neutral world.

    Every declared type and rule is checked, including unplaced types. The
    returned state is validation context, not an authored experiment or a world
    execution. No input objects are changed and no files are read.
    """
    model = _model(document)
    neutral: dict[str, object] = {
        "shape": [1, 1, 1],
        "slots_per_cell": 1,
        "link_ticks": 1,
        "normal_budget": 1,
        "ticks": 0,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "seeds": [],
    }
    return _require_field_couplings(parse_initial_state({**model, **neutral}))


def prepare_experiment(
    definitions: object, experiment: object
) -> tuple[dict[str, object], InitialState]:
    """Validate model/world composition and return a detached ordinary input.

    Named definitions and rule order are retained exactly. Experiment data
    cannot replace model definitions, and the complete composed initialization
    is checked before making its independent snapshot.
    """
    model = _model(definitions)
    world = _body(experiment, "experiment_version", "world")
    unknown = world.keys() - _WORLD_KEYS
    if unknown:
        raise ValueError(f"experiment world has unsupported keys: {', '.join(sorted(unknown))}")
    composed = {**model, **world}
    initial = _require_field_couplings(parse_initial_state(composed))
    return copy.deepcopy(composed), initial


def compose_initialization(definitions: object, experiment: object) -> dict[str, object]:
    """Return a detached, validated initialization for the ordinary runner."""
    return prepare_experiment(definitions, experiment)[0]


def main(argv: list[str] | None = None) -> int:
    """Write a validated input exclusively; never run a simulation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definitions", type=Path, required=True)
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--output-init", type=Path, required=True)
    args = parser.parse_args(argv)
    initial = compose_initialization(
        parse_json_document(args.definitions.read_bytes()),
        parse_json_document(args.experiment.read_bytes()),
    )
    args.output_init.parent.mkdir(parents=True, exist_ok=True)
    with args.output_init.open("x", encoding="utf-8") as output:
        json.dump(initial, output, indent=2)
        output.write("\n")
    print(args.output_init)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
