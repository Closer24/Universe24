"""Validate declarative initial conditions without importing physical model laws."""

import json
from pathlib import Path
from typing import cast

from .core.disturbance_state import (
    MAX_EXPRESSION_NODES,
    MAX_FIELDS,
    MAX_RULES,
    MAX_SLOTS,
    MAX_TYPES,
    MAX_VALUE,
    OPERATIONS,
    Address3,
    CouplingDefinition,
    DisturbanceDefinition,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    InitialState,
    OperationCosts,
    Payload,
    Seed,
    TransportDefinition,
    UpdateRule,
    Values,
    Weights,
    pack,
)


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    result = cast(dict[str, object], value)
    unknown = result.keys() - allowed
    missing = required - result.keys()
    if unknown:
        raise ValueError(f"{label} has unknown keys: {', '.join(sorted(unknown))}")
    if missing:
        raise ValueError(f"{label} is missing keys: {', '.join(sorted(missing))}")
    return result


def _array(value: object, label: str, limit: int, minimum: int = 0) -> list[object]:
    if not isinstance(value, list) or not minimum <= len(value) <= limit:
        raise ValueError(f"{label} must be an array of length {minimum} through {limit}")
    return cast(list[object], value)


def _integer(value: object, label: str, minimum: int = -MAX_VALUE) -> int:
    if type(value) is not int or not minimum <= value <= MAX_VALUE:
        raise ValueError(f"{label} must be an integer from {minimum} through {MAX_VALUE}")
    return value


def _boolean(value: object, label: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{label} must be a boolean")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise ValueError(f"{label} must be a nonempty string of at most 128 characters")
    return value


def _index(value: object, names: dict[str, int], label: str) -> int:
    name = _text(value, label)
    if name not in names:
        raise ValueError(f"{label} refers to unknown name {name!r}")
    return names[name]


def _names(values: tuple[FieldDefinition | DisturbanceDefinition, ...]) -> dict[str, int]:
    result: dict[str, int] = {}
    for index, value in enumerate(values):
        if value.name in result:
            raise ValueError(f"duplicate name {value.name!r}")
        result[value.name] = index
    return result


def _fields(value: object) -> tuple[FieldDefinition, ...]:
    result: list[FieldDefinition] = []
    required = {"name", "components", "units", "signed", "conserved"}
    for raw in _array(value, "fields", MAX_FIELDS, 1):
        obj = _object(raw, "field", required | {"scale", "extensive"}, required)
        components = _integer(obj["components"], "field.components", 1)
        if components not in (1, 3):
            raise ValueError("field.components must be 1 or 3")
        conserved = _boolean(obj["conserved"], "field.conserved")
        extensive = _boolean(obj.get("extensive", True), "field.extensive")
        if conserved and not extensive:
            raise ValueError("conserved fields must be extensive")
        result.append(
            FieldDefinition(
                name=_text(obj["name"], "field.name"),
                components=components,
                units=_text(obj["units"], "field.units"),
                signed=_boolean(obj["signed"], "field.signed"),
                conserved=conserved,
                scale=_integer(obj.get("scale", 1), "field.scale", 1),
                extensive=extensive,
            )
        )
    fields = tuple(result)
    _names(fields)
    return fields


def _payload(value: object, field: FieldDefinition) -> Payload:
    components: tuple[int, ...]
    if field.components == 1:
        components = (_integer(value, f"value for {field.name}"),)
    else:
        items = _array(value, f"value for {field.name}", 3, 3)
        components = tuple(_integer(item, f"component of {field.name}") for item in items)
    result = pack(components)
    field.validate(result)
    return result


def _values(
    value: object,
    fields: tuple[FieldDefinition, ...],
    owned: tuple[int, ...],
    defaults: Values,
) -> Values:
    names = {fields[index].name: index for index in owned}
    obj = _object(value, "values", set(names), set())
    result = list(defaults)
    for name, raw in obj.items():
        index = names[name]
        result[index] = _payload(raw, fields[index])
    return tuple(result)


class _Expressions:
    """Compile a bounded, typed expression tree from JSON data only."""

    def __init__(
        self,
        fields: tuple[FieldDefinition, ...],
        left: tuple[int, ...],
        right: tuple[int, ...] | None = None,
    ) -> None:
        self.fields = fields
        self.names = _names(fields)
        self.owned = (left, right)
        self.nodes = 0

    def parse(self, value: object, expected: int) -> Expression:
        expression, components = self._node(value, 1)
        if components != expected:
            raise ValueError(f"expression has {components} components; expected {expected}")
        return expression

    def _node(self, value: object, depth: int) -> tuple[Expression, int]:
        self.nodes += 1
        if self.nodes > MAX_EXPRESSION_NODES or depth > 16:
            raise ValueError("expression exceeds the node or depth limit")
        if type(value) is int:
            return Expression("literal", literal=(_integer(value, "expression literal"),)), 1
        if isinstance(value, list):
            items = _array(value, "expression literal", 3, 1)
            if len(items) not in (1, 3):
                raise ValueError("expression literal must contain 1 or 3 components")
            literal = tuple(_integer(item, "expression literal component") for item in items)
            return Expression("literal", literal=literal), len(literal)
        obj = _object(value, "expression", {"field", "side", "op", "args", "index"}, set())
        if "field" in obj:
            return self._reference(obj)
        obj = _object(obj, "operation expression", {"op", "args", "index"}, {"op", "args"})
        operation = _text(obj["op"], "expression.op")
        arities = {
            "add": 2,
            "sub": 2,
            "mul": 2,
            "exact_div": 2,
            "min": 2,
            "max": 2,
            "neg": 1,
            "abs": 1,
            "sum": 1,
            "component": 1,
        }
        if operation not in arities:
            raise ValueError(f"unsupported expression operation {operation!r}")
        if operation != "component" and "index" in obj:
            raise ValueError("only component expressions accept index")
        count = arities[operation]
        arguments = tuple(
            self._node(item, depth + 1) for item in _array(obj["args"], "expression.args", count, count)
        )
        sizes = tuple(item[1] for item in arguments)
        component = 0
        if operation == "component":
            if "index" not in obj:
                raise ValueError("component expression requires index")
            component = _integer(obj["index"], "expression.index", 0)
            if component >= sizes[0]:
                raise ValueError("expression.index exceeds the input component count")
        if operation == "exact_div" and sizes[1] != 1:
            raise ValueError("exact_div requires a scalar denominator")
        size = 1 if operation in ("sum", "component") else max(sizes)
        return Expression(operation, tuple(item[0] for item in arguments), component=component), size

    def _reference(self, obj: dict[str, object]) -> tuple[Expression, int]:
        obj = _object(obj, "field expression", {"field", "side"}, {"field"})
        side_name = obj.get("side", "left")
        if side_name not in ("left", "right"):
            raise ValueError("expression.side must be left or right")
        side = 1 if side_name == "right" else 0
        index = _index(obj["field"], self.names, "expression.field")
        owned = self.owned[side]
        if owned is None or index not in owned:
            raise ValueError("expression references a field not owned by its participant")
        return Expression("field", field=index, side=side), self.fields[index].components


def _transport(
    value: object, fields: tuple[FieldDefinition, ...], owned: tuple[int, ...]
) -> TransportDefinition:
    obj = _object(
        value, "transport", {"mode", "weights", "direction_field", "rate", "rate_denominator"}, {"mode"}
    )
    mode = _text(obj["mode"], "transport.mode")
    allowed = {
        "hold": {"mode"},
        "split": {"mode", "weights"},
        "move": {"mode", "weights", "direction_field", "rate", "rate_denominator"},
    }
    if mode not in allowed:
        raise ValueError("transport.mode must be hold, move or split")
    _object(obj, f"{mode} transport", allowed[mode], {"mode"})
    weights_raw = _array(obj.get("weights", [1, 1, 1, 1, 1, 1]), "transport.weights", 6, 6)
    weights = cast(Weights, tuple(_integer(item, "transport weight", 0) for item in weights_raw))
    if not 1 <= sum(weights) <= MAX_VALUE:
        raise ValueError("transport weights must have a positive bounded sum")
    direction: int | None = None
    if "direction_field" in obj:
        if "weights" in obj:
            raise ValueError("move transport must select weights or direction_field, not both")
        direction = _index(obj["direction_field"], _names(fields), "transport.direction_field")
        if direction not in owned or fields[direction].components != 3:
            raise ValueError("direction_field must be a vector owned by the disturbance")
    if mode == "split" and any(not fields[index].extensive for index in owned):
        raise ValueError("split transport accepts only extensive fields")
    rate = _Expressions(fields, owned).parse(obj["rate"], 1) if "rate" in obj else None
    denominator = _integer(obj.get("rate_denominator", 1), "transport.rate_denominator", 1)
    return TransportDefinition(mode, weights, direction, rate, denominator)


def _updates(
    value: object, fields: tuple[FieldDefinition, ...], owned: tuple[int, ...]
) -> tuple[UpdateRule, ...]:
    result: list[UpdateRule] = []
    names = _names(fields)
    for raw in _array(value, "updates", MAX_RULES):
        obj = _object(raw, "update", {"field", "expression", "source"}, {"field", "expression"})
        index = _index(obj["field"], names, "update.field")
        if index not in owned:
            raise ValueError("update field must be owned by its disturbance")
        source = _boolean(obj.get("source", False), "update.source")
        if fields[index].conserved and not source:
            raise ValueError("updating a conserved field requires explicit source: true")
        if any(rule.field == index for rule in result):
            raise ValueError("a disturbance cannot update the same field more than once")
        expression = _Expressions(fields, owned).parse(obj["expression"], fields[index].components)
        result.append(UpdateRule(index, expression, source))
    return tuple(result)


def _disturbances(
    value: object, fields: tuple[FieldDefinition, ...]
) -> tuple[DisturbanceDefinition, ...]:
    result: list[DisturbanceDefinition] = []
    names = _names(fields)
    zero = tuple(pack((0,) * field.components) for field in fields)
    allowed = {"name", "fields", "defaults", "transport", "updates", "cost_field"}
    for raw in _array(value, "disturbance_types", MAX_TYPES, 1):
        obj = _object(raw, "disturbance type", allowed, {"name", "fields", "transport"})
        owned = tuple(
            _index(item, names, "disturbance field")
            for item in _array(obj["fields"], "disturbance fields", MAX_FIELDS, 1)
        )
        if len(set(owned)) != len(owned):
            raise ValueError("duplicate disturbance field")
        transport = _transport(obj["transport"], fields, owned)
        updates = _updates(obj.get("updates", []), fields, owned)
        cost_field: int | None = None
        if "cost_field" in obj:
            cost_field = _index(obj["cost_field"], names, "cost_field")
            if cost_field not in owned or fields[cost_field].components != 1:
                raise ValueError("cost_field must be a scalar owned by the disturbance")
            if fields[cost_field].conserved or transport.mode != "hold":
                raise ValueError("cost_field must be nonconserved and use hold transport")
            if any(rule.field == cost_field for rule in updates):
                raise ValueError("cost_field cannot also be an update target")
        result.append(
            DisturbanceDefinition(
                name=_text(obj["name"], "disturbance name"),
                fields=owned,
                defaults=_values(obj.get("defaults", {}), fields, owned, zero),
                transport=transport,
                updates=updates,
                cost_field=cost_field,
            )
        )
    disturbances = tuple(result)
    _names(disturbances)
    if sum(len(item.updates) for item in disturbances) > MAX_RULES:
        raise ValueError("initial state exceeds the total update rule limit")
    return disturbances


def _couplings(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
) -> tuple[CouplingDefinition, ...]:
    result: list[CouplingDefinition] = []
    type_names = _names(disturbances)
    field_names = _names(fields)
    required = {"name", "left_type", "right_type", "field", "amount"}
    for raw in _array(value, "couplings", MAX_RULES):
        obj = _object(raw, "coupling", required | {"denominator"}, required)
        name = _text(obj["name"], "coupling.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate coupling name")
        left = _index(obj["left_type"], type_names, "coupling.left_type")
        right = _index(obj["right_type"], type_names, "coupling.right_type")
        field = _index(obj["field"], field_names, "coupling.field")
        participants = (disturbances[left], disturbances[right])
        if any(field not in participant.fields for participant in participants):
            raise ValueError("coupling field must be owned by both participants")
        if any(field == participant.cost_field for participant in participants):
            raise ValueError("cost_field cannot also be a coupling target")
        amount = _Expressions(fields, participants[0].fields, participants[1].fields).parse(
            obj["amount"], fields[field].components
        )
        denominator = _integer(obj.get("denominator", 1), "coupling.denominator", 1)
        result.append(CouplingDefinition(name, left, right, field, amount, denominator))
    return tuple(result)


def _address(value: object, label: str, minimum: int) -> Address3:
    return cast(
        Address3,
        tuple(_integer(item, label, minimum) for item in _array(value, label, 3, 3)),
    )


def _seeds(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    shape: Address3,
    capacity: int,
) -> tuple[Seed, ...]:
    if not isinstance(value, list):
        raise ValueError("seeds must be an array")
    result: list[Seed] = []
    occupied: dict[Address3, int] = {}
    names = _names(disturbances)
    phases = tuple(pack((0,) * field.components) for field in fields)
    for raw in value:
        obj = _object(raw, "seed", {"position", "type", "values"}, {"position", "type"})
        position = _address(obj["position"], "seed.position", 0)
        if any(coordinate >= length for coordinate, length in zip(position, shape, strict=True)):
            raise ValueError("seed.position must be within shape")
        occupied[position] = occupied.get(position, 0) + 1
        if occupied[position] > capacity:
            raise ValueError("initial seeds exceed slots_per_cell")
        type_index = _index(obj["type"], names, "seed.type")
        definition = disturbances[type_index]
        values = _values(obj.get("values", {}), fields, definition.fields, definition.defaults)
        result.append(Seed(position, DisturbanceRecord(type_index, values, phases)))
    return tuple(result)


def parse_initial_state(document: object) -> InitialState:
    """Reject malformed, ambiguous or unbounded initialization data before a run."""
    required = {
        "schema_version",
        "model_id",
        "shape",
        "slots_per_cell",
        "link_ticks",
        "normal_budget",
        "ticks",
        "operation_costs",
        "fields",
        "disturbance_types",
        "seeds",
    }
    obj = _object(document, "initial state", required | {"couplings"}, required)
    if _integer(obj["schema_version"], "schema_version", 1) != 1:
        raise ValueError("unsupported schema_version; expected 1")
    shape = _address(obj["shape"], "shape", 1)
    capacity = _integer(obj["slots_per_cell"], "slots_per_cell", 1)
    if capacity > MAX_SLOTS:
        raise ValueError(f"slots_per_cell exceeds {MAX_SLOTS}")
    costs = _object(obj["operation_costs"], "operation_costs", set(OPERATIONS), set(OPERATIONS))
    fields = _fields(obj["fields"])
    disturbances = _disturbances(obj["disturbance_types"], fields)
    return InitialState(
        model_id=_text(obj["model_id"], "model_id"),
        shape=shape,
        slots_per_cell=capacity,
        link_ticks=_integer(obj["link_ticks"], "link_ticks", 1),
        normal_budget=_integer(obj["normal_budget"], "normal_budget", 1),
        ticks=_integer(obj["ticks"], "ticks", 0),
        fields=fields,
        disturbances=disturbances,
        couplings=_couplings(obj.get("couplings", []), fields, disturbances),
        operation_costs=OperationCosts(
            tuple(_integer(costs[name], f"cost of {name}", 1) for name in OPERATIONS)
        ),
        seeds=_seeds(obj["seeds"], fields, disturbances, shape, capacity),
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_initial_state(path: Path) -> InitialState:
    """Read a strict JSON initialization file and compile its generic definitions."""
    return parse_initial_json(path.read_bytes())


def parse_initial_json(source: str | bytes) -> InitialState:
    """Compile one immutable JSON payload, rejecting duplicate keys."""
    document: object = json.loads(source, object_pairs_hook=_unique_object)
    return parse_initial_state(document)
