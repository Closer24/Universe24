"""Formal offline schemas cover every active runtime branch and reject malformed shapes."""

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from event_universe.experiment import load_experiment
from event_universe.initialization import parse_initial_json, parse_initial_state
from event_universe.schemas import SCHEMA_NAMES, schema_document

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def validators():
    documents = [schema_document(name) for name in SCHEMA_NAMES]
    registry = Registry().with_resources((doc["$id"], Resource.from_contents(doc)) for doc in documents)
    return {
        name: Draft202012Validator(doc, registry=registry)
        for name, doc in zip(SCHEMA_NAMES, documents, strict=True)
    }


def test_every_packaged_schema_is_draft_2020_12_and_self_consistent(validators):
    for validator in validators.values():
        Draft202012Validator.check_schema(validator.schema)
        assert validator.schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_all_runtime_examples_and_skill_template_conform(validators):
    count = 0
    versions = set()
    for path in [
        *sorted((ROOT / "examples").rglob("*.json")),
        ROOT / "skills/simulation-configuration/assets/two-streams.json",
    ]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if (
            not isinstance(raw, dict)
            or not {"schema_version", "fields", "disturbance_types"} <= raw.keys()
        ):
            continue
        parse_initial_json(path.read_bytes())
        try:
            validators["runtime"].validate(raw)
        except ValidationError as error:
            pytest.fail(f"{path.relative_to(ROOT)}: {error.message} at {list(error.absolute_path)}")
        count += 1
        versions.add(raw["schema_version"])
    assert count >= 20
    assert versions == {1, 2}


def test_manifest_parts_and_resolved_runtime_validate_offline(validators):
    folder = ROOT / "examples/experiment-package"
    for path in sorted(folder.rglob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        kind = "experiment" if "experiment_version" in raw else raw["part_kind"]
        validators[kind].validate(raw)
    package = load_experiment(folder / "experiment.json")
    validators["runtime"].validate(json.loads(package.runtime_json))


@pytest.mark.parametrize(
    "mutation",
    [
        lambda raw: raw.update(unknown=True),
        lambda raw: raw["fields"][0].update(unknown=1),
        lambda raw: raw["fields"][0].update(components=2),
        lambda raw: raw["seeds"][0].update(name="unsupported"),
        lambda raw: raw["seeds"][0].update(position=[1, 2]),
        lambda raw: raw["disturbance_types"][0]["transport"].update(camera=1),
        lambda raw: raw["disturbance_types"][0].update(
            updates=[{"field": "heading", "expression": {"op": "add", "args": [1]}}]
        ),
        lambda raw: raw["disturbance_types"][0].update(
            updates=[{"field": "heading", "expression": {"op": "component", "args": [[1, 2, 3]]}}]
        ),
        lambda raw: raw["disturbance_types"][0].update(
            updates=[{"field": "heading", "expression": {"op": "custom", "args": [1, 2]}}]
        ),
        lambda raw: raw["disturbance_types"][0].update(
            updates=[{"field": "heading", "expression": {"op": "ratio", "args": [1, 2]}}]
        ),
        lambda raw: raw["disturbance_types"][0].update(
            updates=[{"field": "heading", "expression": {"field": "heading", "args": []}}]
        ),
        lambda raw: raw["operation_costs"].update(route=True),
    ],
)
def test_unknown_keys_and_recursive_expression_shapes_fail(validators, mutation):
    raw = json.loads(load_experiment(ROOT / "examples/experiment-package/experiment.json").runtime_json)
    mutation(raw)
    with pytest.raises(ValidationError):
        validators["runtime"].validate(raw)


def test_schema_version_specific_fields_and_semantic_parser_remain_distinct(validators):
    raw = json.loads(load_experiment(ROOT / "examples/experiment-package/experiment.json").runtime_json)
    malformed = copy.deepcopy(raw)
    malformed.update(schema_version=2, field_rules=[])
    with pytest.raises(ValidationError):
        validators["runtime"].validate(malformed)
    # JSON Schema treats mathematically integral numbers as integers; the engine
    # additionally requires integer JSON tokens and valid references/ownership.
    raw["seeds"][0]["type"] = "missing"
    validators["runtime"].validate(raw)
    with pytest.raises(ValueError, match="unknown name"):
        parse_initial_state(raw)


def test_schema_api_returns_fresh_documents_and_rejects_unknown_names():
    document = schema_document()
    document["additionalProperties"] = True
    assert schema_document()["additionalProperties"] is False
    with pytest.raises(ValueError, match="unknown schema"):
        schema_document("../secret")
