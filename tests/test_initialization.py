"""Initialization contracts reject ambiguous physics before allocating a world."""

import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, unpack
from event_universe.initialization import load_initial_state, parse_initial_state

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def _document() -> dict[str, Any]:
    return json.loads((EXAMPLES / "basic.json").read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def test_defaults_and_owned_fields_use_one_fixed_global_schema() -> None:
    document = _document()
    document["seeds"][0]["values"] = {"charge": -7}
    initial = parse_initial_state(document)
    first = initial.seeds[0].record
    assert tuple(unpack(value) for value in first.values) == ((2,), (-7,), (2, 1, 0), (0,), (0,))
    assert first.phase_codes == ((1,), (1,), (1, 1, 1), (1,), (1,))
    assert initial.disturbances[0].transport.direction_field == 2
    assert initial.fields[2].extensive is False
    assert initial.operation_costs.price("receive") == 1


def test_arbitrary_field_and_type_names_do_not_select_physics() -> None:
    original = _document()
    names = {
        "mass": "alpha",
        "charge": "beta",
        "velocity": "gamma",
        "signal": "delta",
        "computation": "epsilon",
        "carrier": "first",
        "pulse": "second",
        "local_work": "third",
    }

    def rename(value: Any) -> Any:
        if isinstance(value, str):
            return names.get(value, value)
        if isinstance(value, list):
            return [rename(item) for item in value]
        if isinstance(value, dict):
            return {names.get(key, key): rename(item) for key, item in value.items()}
        return value

    before = parse_initial_state(original)
    after = parse_initial_state(rename(original))
    normalized = replace(
        after,
        fields=tuple(
            replace(new, name=old.name) for new, old in zip(after.fields, before.fields, strict=True)
        ),
        disturbances=tuple(
            replace(new, name=old.name)
            for new, old in zip(after.disturbances, before.disturbances, strict=True)
        ),
    )
    assert normalized == before


def test_coupling_references_are_resolved_to_owned_fields() -> None:
    initial = load_initial_state(EXAMPLES / "exchange.json")
    coupling = initial.couplings[0]
    assert (coupling.left_type, coupling.right_type, coupling.field, coupling.denominator) == (
        0,
        1,
        0,
        4,
    )
    assert coupling.amount.op == "sub"
    assert tuple(argument.side for argument in coupling.amount.arguments) == (0, 1)


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("schema_version",), 3, "schema_version"),
        (("ticks",), True, "must be an integer"),
        (("normal_budget",), 0, "must be an integer"),
        (("shape",), [7, 0, 7], "must be an integer"),
        (("slots_per_cell",), 33, "slots_per_cell"),
        (("operation_costs", "read"), 0, "cost of read"),
        (("operation_costs", "typo"), 2, "unknown keys"),
        (("fields", 0, "signed"), 1, "must be a boolean"),
        (("fields", 0, "scale"), MAX_VALUE + 1, "field.scale"),
        (("fields", 0, "extensive"), False, "must be extensive"),
        (("fields", 0, "components"), 2, "must be 1 or 3"),
        (("fields", 1, "name"), "mass", "duplicate name"),
        (("disturbance_types", 0, "defaults", "unknown"), 2, "unknown keys"),
        (("disturbance_types", 0, "defaults", "mass"), -1, "negative value forbidden"),
        (("disturbance_types", 0, "defaults", "velocity"), [1, 0], "length 3"),
        (("disturbance_types", 0, "transport", "direction_field"), "mass", "must be a vector"),
        (("disturbance_types", 0, "transport", "rate"), [1, 0, 0], "expected 1"),
        (("disturbance_types", 0, "transport", "weights"), [1, 0, 0, 0, 0, 0], "not both"),
        (("disturbance_types", 1, "transport", "weights"), [0] * 6, "positive bounded sum"),
        (("disturbance_types", 2, "transport", "rate"), 1, "unknown keys"),
        (("disturbance_types", 2, "cost_field"), "mass", "owned by the disturbance"),
        (("seeds", 0, "position"), [17, 0, 0], "within shape"),
        (("seeds", 0, "type"), "unknown", "unknown name"),
        (("seeds", 0, "values"), {"signal": 1}, "unknown keys"),
        (("seeds", 0, "velocity"), [1, 0, 0], "unknown keys"),
    ],
)
def test_invalid_schema_fails_before_running(
    path: tuple[str | int, ...], value: Any, message: str
) -> None:
    document = _document()
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError, match=message):
        parse_initial_state(document)


def test_split_cannot_divide_an_intensive_attribute() -> None:
    document = _document()
    document["disturbance_types"][0]["transport"] = {"mode": "split"}
    with pytest.raises(ValueError, match="only extensive fields"):
        parse_initial_state(document)


def test_initial_capacity_and_required_operation_prices() -> None:
    document = _document()
    document["slots_per_cell"] = 2
    with pytest.raises(ValueError, match="exceed slots_per_cell"):
        parse_initial_state(document)
    document["slots_per_cell"] = 3
    assert len(parse_initial_state(document).seeds) == 3
    del document["operation_costs"]["commit"]
    with pytest.raises(ValueError, match="missing keys: commit"):
        parse_initial_state(document)


@pytest.mark.parametrize(
    ("expression", "message"),
    [
        ({"op": "eval", "args": ["anything"]}, "unsupported expression operation"),
        ({"field": "signal"}, "not owned"),
        ({"field": "mass", "side": "right"}, "not owned"),
        ({"field": "mass", "op": "neg"}, "unknown keys"),
        ({"op": "component", "args": [{"field": "velocity"}], "index": 3}, "exceeds"),
        ({"op": "add", "args": [1]}, "length 2"),
        ({"op": "exact_div", "args": [1, [1, 2, 3]]}, "scalar denominator"),
        (False, "must be an object"),
        (1.5, "must be an object"),
    ],
)
def test_expression_language_has_no_execution_escape(expression: Any, message: str) -> None:
    document = _document()
    document["disturbance_types"][0]["transport"]["rate"] = expression
    with pytest.raises(ValueError, match=message):
        parse_initial_state(document)


def test_expression_depth_and_total_nodes_are_bounded() -> None:
    document = _document()
    expression: Any = 1
    for _ in range(16):
        expression = {"op": "abs", "args": [expression]}
    document["disturbance_types"][0]["transport"]["rate"] = expression
    with pytest.raises(ValueError, match="node or depth limit"):
        parse_initial_state(document)
    expression = 1
    for _ in range(6):
        expression = {"op": "add", "args": [expression, deepcopy(expression)]}
    document["disturbance_types"][0]["transport"]["rate"] = expression
    with pytest.raises(ValueError, match="node or depth limit"):
        parse_initial_state(document)


def test_conserved_updates_require_explicit_sources() -> None:
    document = _document()
    update = {"field": "mass", "expression": {"op": "add", "args": [{"field": "mass"}, 1]}}
    document["disturbance_types"][0]["updates"] = [update]
    with pytest.raises(ValueError, match="explicit source"):
        parse_initial_state(document)
    update["source"] = True
    assert parse_initial_state(document).disturbances[0].updates[0].source


def test_loader_rejects_duplicate_json_keys(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"schema_version": 1, "schema_version": 2}', encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate JSON key"):
        load_initial_state(path)
