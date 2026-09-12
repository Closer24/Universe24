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
    Assignment,
    CouplingDefinition,
    DisturbanceDefinition,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    InitialState,
    InteractionDefinition,
    Invariant,
    OperationCosts,
    Payload,
    Seed,
    TransportDefinition,
    UpdateRule,
    Values,
    Weights,
    pack,
    unpack,
)
from .core.integer import checked_work
from .core.spatial_state import (
    DecayDefinition,
    EmissionDefinition,
    FieldAssignment,
    FieldGroupDefinition,
    NodeFieldRuleDefinition,
    SpatialCouplingDefinition,
    SpatialFieldDefinition,
    SpatialInteractionDefinition,
    SpatialSeed,
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
    """Parse a bounded, typed expression tree from JSON data only."""

    def __init__(
        self,
        fields: tuple[FieldDefinition, ...],
        left: tuple[int, ...],
        right: tuple[int, ...] | None = None,
        flux_fields: tuple[int, ...] = (),
        received_fields: tuple[int, ...] = (),
        outgoing_fields: tuple[int, ...] = (),
    ) -> None:
        self.fields = fields
        self.names = _names(fields)
        self.owned = (left, right)
        self.nodes = 0
        self.flux_fields = flux_fields
        self.received_fields = received_fields
        self.outgoing_fields = outgoing_fields

    def parse(
        self, value: object, expected: int | None = None, *, invariant: bool = False
    ) -> Expression:
        expression, components = self._node(value, 1, allow_key=invariant)
        if expected is not None and components != expected:
            raise ValueError(f"expression has {components} components; expected {expected}")
        return expression

    def _node(
        self, value: object, depth: int, rational: bool = False, *, allow_key: bool = False
    ) -> tuple[Expression, int]:
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
        obj = _object(
            value,
            "expression",
            {"field", "side", "op", "args", "index", "flux", "matrix", "received", "outgoing", "port"},
            set(),
        )
        if "received" in obj or "outgoing" in obj:
            operation = "received" if "received" in obj else "outgoing"
            obj = _object(obj, "directional expression", {operation, "port"}, {operation, "port"})
            owned = self.received_fields if operation == "received" else self.outgoing_fields
            names = {self.fields[index].name: index for index in owned}
            index = _index(obj[operation], names, f"{operation} spatial field")
            port = _integer(obj["port"], "expression.port", 0)
            if port >= 6:
                raise ValueError("expression.port must be from 0 through 5")
            return Expression(operation, field=index, port=port), self.fields[index].components
        if "flux" in obj:
            obj = _object(obj, "flux expression", {"flux"}, {"flux"})
            names = {self.fields[index].name: index for index in self.flux_fields}
            index = _index(obj["flux"], names, "scalar spatial flux")
            return Expression("flux", field=index), 3
        if "field" in obj:
            return self._reference(obj)
        obj = _object(obj, "operation expression", {"op", "args", "index", "matrix"}, {"op", "args"})
        operation = _text(obj["op"], "expression.op")
        if operation == "rational_key" and not allow_key:
            raise ValueError("rational_key is only allowed as a top-level invariant")
        projections = {
            "rational_whole",
            "rational_remainder",
            "rational_denominator",
            "rational_numerator",
            "rational_direction",
            "rational_key",
            "rational_floor",
        }
        if operation == "ratio" and not rational:
            raise ValueError("ratio requires an explicit rational projection")
        arities = {
            **dict.fromkeys(projections, 1),
            "ratio": 2,
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
            "transform": 1,
            "dot": 2,
            "gt": 2,
            "eq": 2,
            "cross": 2,
            "vector": 3,
        }
        if operation not in arities:
            raise ValueError(f"unsupported expression operation {operation!r}")
        if operation != "component" and "index" in obj:
            raise ValueError("only component expressions accept index")
        if operation != "transform" and "matrix" in obj:
            raise ValueError("only transform expressions accept matrix")
        count = arities[operation]
        arguments = tuple(
            self._node(item, depth + 1, rational or operation in projections)
            for item in _array(obj["args"], "expression.args", count, count)
        )
        sizes = tuple(item[1] for item in arguments)
        if operation == "transform":
            if sizes != (3,) or "matrix" not in obj:
                raise ValueError("transform requires a vector and a 3 by 3 integer matrix")
            matrix = tuple(
                tuple(_integer(item, "matrix coefficient") for item in _array(row, "matrix row", 3, 3))
                for row in _array(obj["matrix"], "matrix", 3, 3)
            )
            return Expression(operation, tuple(item[0] for item in arguments), matrix=matrix), 3
        if operation in ("dot", "cross") and sizes != (3, 3):
            raise ValueError(f"{operation} requires two vectors")
        if operation == "vector" and sizes != (1, 1, 1):
            raise ValueError("vector requires three scalars")
        if operation in ("gt", "eq") and sizes != (1, 1):
            raise ValueError("gt requires two scalars")
        component = 0
        if operation == "component":
            if "index" not in obj:
                raise ValueError("component expression requires index")
            component = _integer(obj["index"], "expression.index", 0)
            if component >= sizes[0]:
                raise ValueError("expression.index exceeds the input component count")
        if operation in ("exact_div", "ratio") and sizes[1] != 1:
            raise ValueError("exact_div requires a scalar denominator")
        size = 1 if operation in ("sum", "component", "dot", "gt", "eq") else max(sizes)
        if operation == "rational_denominator":
            size = 1
        elif operation == "rational_key":
            size = 2 * sizes[0]
        elif operation == "rational_direction" and sizes[0] != 3:
            raise ValueError("rational_direction requires a vector")
        if operation == "vector":
            size = 3
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
        value,
        "transport",
        {
            "mode",
            "weights",
            "direction_field",
            "rate",
            "rate_denominator",
            "routing",
            "direction",
            "rate_divisor",
        },
        {"mode"},
    )
    mode = _text(obj["mode"], "transport.mode")
    allowed = {
        "hold": {"mode"},
        "split": {"mode", "weights"},
        "move": {
            "mode",
            "weights",
            "direction_field",
            "rate",
            "rate_denominator",
            "routing",
            "direction",
            "rate_divisor",
        },
    }
    if mode not in allowed:
        raise ValueError("transport.mode must be hold, move or split")
    _object(obj, f"{mode} transport", allowed[mode], {"mode"})
    weights_raw = _array(obj.get("weights", [1, 1, 1, 1, 1, 1]), "transport.weights", 6, 6)
    weights = cast(Weights, tuple(_integer(item, "transport weight", 0) for item in weights_raw))
    if not 1 <= sum(weights) or (obj.get("routing", "cyclic") == "cyclic" and sum(weights) > MAX_VALUE):
        raise ValueError("transport weights must have a positive bounded sum")
    routing = _text(obj.get("routing", "cyclic"), "transport.routing")
    if routing not in ("cyclic", "balanced"):
        raise ValueError("routing must be cyclic or balanced")
    direction_expression = (
        _Expressions(fields, owned).parse(obj["direction"], 3) if "direction" in obj else None
    )
    if direction_expression is not None and ("weights" in obj or "direction_field" in obj):
        raise ValueError("select exactly one direction provider")
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
    divisor = (
        _Expressions(fields, owned).parse(obj["rate_divisor"], 1) if "rate_divisor" in obj else None
    )
    return TransportDefinition(
        mode, weights, direction, rate, denominator, routing, direction_expression, divisor
    )


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
    allowed = {"name", "fields", "defaults", "transport", "updates", "cost_field", "checks"}
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
        checks: list[Invariant] = []
        for raw_check in _array(obj.get("checks", []), "local checks", MAX_RULES):
            check = _object(raw_check, "local check", {"name", "expression"}, {"name", "expression"})
            name = _text(check["name"], "check.name")
            if any(item.name == name for item in checks):
                raise ValueError("duplicate local check name")
            checks.append(Invariant(name, _Expressions(fields, owned).parse(check["expression"], 1)))
        result.append(
            DisturbanceDefinition(
                name=_text(obj["name"], "disturbance name"),
                fields=owned,
                defaults=_values(obj.get("defaults", {}), fields, owned, zero),
                transport=transport,
                updates=updates,
                cost_field=cost_field,
                checks=tuple(checks),
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
        obj = _object(raw, "coupling", required | {"denominator", "remainder_owner"}, required)
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
        owner = _text(obj.get("remainder_owner", "pair"), "coupling.remainder_owner")
        if owner not in ("pair", "left"):
            raise ValueError("coupling.remainder_owner must be pair or left")
        if owner == "left":
            if left == right:
                raise ValueError("left-owned exchange remainders require distinct participant types")
            if disturbances[left].transport.mode == "split":
                raise ValueError("left-owned exchange remainders require whole-record hold or move")
        result.append(CouplingDefinition(name, left, right, field, amount, denominator, owner))
    return tuple(result)


def _address(value: object, label: str, minimum: int) -> Address3:
    return cast(
        Address3,
        tuple(_integer(item, label, minimum) for item in _array(value, label, 3, 3)),
    )


def _interactions(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
) -> tuple[InteractionDefinition, ...]:
    result: list[InteractionDefinition] = []
    type_names, field_names = _names(disturbances), _names(fields)
    required = {"name", "left_type", "right_type", "assignments", "invariants"}
    for raw in _array(value, "interactions", MAX_RULES):
        obj = _object(raw, "interaction", required | {"when", "output_types"}, required)
        name = _text(obj["name"], "interaction.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate interaction name")
        left = _index(obj["left_type"], type_names, "interaction.left_type")
        right = _index(obj["right_type"], type_names, "interaction.right_type")
        participants = (disturbances[left], disturbances[right])

        def expression(
            raw: object,
            expected: int | None = None,
            participants: tuple[DisturbanceDefinition, DisturbanceDefinition] = participants,
        ) -> Expression:
            return _Expressions(fields, participants[0].fields, participants[1].fields).parse(
                raw, expected
            )

        assignments: list[Assignment] = []
        for raw_assignment in _array(obj["assignments"], "assignments", MAX_FIELDS * 2, 1):
            item = _object(
                raw_assignment,
                "assignment",
                {"side", "field", "expression"},
                {"side", "field", "expression"},
            )
            if item["side"] not in ("left", "right"):
                raise ValueError("assignment.side must be left or right")
            side = 0 if item["side"] == "left" else 1
            field = _index(item["field"], field_names, "assignment.field")
            if field not in participants[side].fields or field == participants[side].cost_field:
                raise ValueError("assignment requires an owned field other than cost_field")
            if any(a.side == side and a.field == field for a in assignments):
                raise ValueError("duplicate assignment target")
            assignments.append(
                Assignment(side, field, expression(item["expression"], fields[field].components))
            )
        invariants: list[Invariant] = []
        for raw_invariant in _array(obj["invariants"], "invariants", MAX_FIELDS, 1):
            item = _object(raw_invariant, "invariant", {"name", "expression"}, {"name", "expression"})
            invariant_name = _text(item["name"], "invariant.name")
            if any(i.name == invariant_name for i in invariants):
                raise ValueError("duplicate invariant name")
            invariants.append(
                Invariant(
                    invariant_name,
                    _Expressions(fields, participants[0].fields, participants[1].fields).parse(
                        item["expression"], invariant=True
                    ),
                )
            )
        when = expression(obj["when"], 1) if "when" in obj else None
        output_types = None
        if "output_types" in obj:
            outputs = _object(obj["output_types"], "output_types", {"left", "right"}, {"left", "right"})
            output_types = (
                _index(outputs["left"], type_names, "output_types.left"),
                _index(outputs["right"], type_names, "output_types.right"),
            )
            if set(output_types) & {left, right}:
                raise ValueError("conversion output types must differ from both input types")
            involved = (*participants, *(disturbances[index] for index in output_types))
            if any(set(kind.fields) != set(participants[0].fields) for kind in involved):
                raise ValueError("conversion types must own the same fields")
            if any(kind.transport.mode == "split" or kind.cost_field is not None for kind in involved):
                raise ValueError("conversion requires whole records without cost_field")
            expected = {(side, field) for side in (0, 1) for field in participants[side].fields}
            if {(a.side, a.field) for a in assignments} != expected:
                raise ValueError("conversion requires explicit assignments for every output field")
        result.append(
            InteractionDefinition(
                name, left, right, tuple(assignments), tuple(invariants), when, output_types
            )
        )
    return tuple(result)


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


def _decay(value: object) -> DecayDefinition:
    keys = {"retain_numerator", "retain_denominator"}
    obj = _object(value, "spatial decay", keys, keys)
    numerator = _integer(obj["retain_numerator"], "decay.retain_numerator", 0)
    denominator = _integer(obj["retain_denominator"], "decay.retain_denominator", 1)
    if numerator >= denominator:
        raise ValueError("decay requires retain_numerator < retain_denominator")
    return DecayDefinition(numerator, denominator)


def _allowance(value: object, field: FieldDefinition, label: str) -> Payload:
    amounts: tuple[int, ...]
    if field.components == 1:
        amounts = (_integer(value, label, 0),)
    else:
        amounts = tuple(
            _integer(component, label, 0)
            for component in _array(value, label, field.components, field.components)
        )
    return pack(amounts)


def _spatial_fields(
    value: object,
    fields: tuple[FieldDefinition, ...],
    schema_version: int = 1,
) -> tuple[SpatialFieldDefinition, ...]:
    result: list[SpatialFieldDefinition] = []
    names = _names(fields)
    for raw in _array(value, "spatial_fields", MAX_FIELDS):
        obj = _object(
            raw,
            "spatial field",
            {"field", "baseline", "transport", "axis_weights", "octant_weights"}
            | ({"decay"} if schema_version == 2 else set()),
            {"field", "transport"} | ({"decay"} if schema_version == 2 else set()),
        )
        index = _index(obj["field"], names, "spatial field")
        if any(item.field == index for item in result):
            raise ValueError("duplicate spatial field")
        field = fields[index]
        if not field.extensive:
            raise ValueError("spatial transport requires extensive field components")
        transport = _text(obj["transport"], "spatial transport")
        if transport not in ("outward", "local"):
            raise ValueError("spatial transport must be outward or local")
        if transport == "local" and schema_version != 1:
            raise ValueError("local spatial transport requires schema_version 1")
        axis = tuple(
            _integer(v, "axis weight", 0)
            for v in _array(obj.get("axis_weights", [1, 1, 1]), "axis_weights", 3, 3)
        )
        octants = tuple(
            _integer(v, "octant weight", 0)
            for v in _array(obj.get("octant_weights", [1] * 8), "octant_weights", 8, 8)
        )
        if not 1 <= sum(axis) <= MAX_VALUE or not 1 <= sum(octants) <= MAX_VALUE:
            raise ValueError("spatial weights must have positive bounded totals")
        baseline = (
            _payload(obj["baseline"], field) if "baseline" in obj else pack((0,) * field.components)
        )
        result.append(
            SpatialFieldDefinition(
                index,
                baseline,
                cast(tuple[int, int, int], axis),
                octants,
                _decay(obj["decay"]) if schema_version == 2 else None,
                transport,
            )
        )
    return tuple(result)


def _emissions(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    spatial: tuple[SpatialFieldDefinition, ...],
    schema_version: int = 1,
) -> tuple[EmissionDefinition, ...]:
    result: list[EmissionDefinition] = []
    names = {fields[item.field].name: i for i, item in enumerate(spatial)}
    for raw in _array(value, "emissions", MAX_RULES):
        obj = _object(
            raw,
            "emission",
            {"type", "field", "amount", "denominator", "source"}
            | ({"budget"} if schema_version == 2 else set()),
            {"type", "field", "amount", "source"} | ({"budget"} if schema_version == 2 else set()),
        )
        if not _boolean(obj["source"], "emission.source"):
            raise ValueError("emission requires explicit source: true")
        kind = _index(obj["type"], _names(disturbances), "emission.type")
        index = _index(obj["field"], names, "emission.field")
        if disturbances[kind].transport.mode == "split":
            raise ValueError("an emitting disturbance must hold or move as a whole record")
        if any(item.type_index == kind and item.spatial_field == index for item in result):
            raise ValueError("duplicate emission for the same disturbance type and field")
        amount = _Expressions(fields, disturbances[kind].fields).parse(
            obj["amount"], fields[spatial[index].field].components
        )
        result.append(
            EmissionDefinition(
                kind,
                index,
                amount,
                _integer(obj.get("denominator", 1), "emission.denominator", 1),
                _allowance(obj["budget"], fields[spatial[index].field], "emission.budget")
                if schema_version == 2
                else None,
            )
        )
    return tuple(result)


def _spatial_seeds(
    value: object,
    fields: tuple[FieldDefinition, ...],
    spatial: tuple[SpatialFieldDefinition, ...],
    shape: Address3,
) -> tuple[SpatialSeed, ...]:
    if not isinstance(value, list):
        raise ValueError("spatial_seeds must be an array")
    result: list[SpatialSeed] = []
    occupied: set[tuple[Address3, int]] = set()
    names = {fields[item.field].name: i for i, item in enumerate(spatial)}
    for raw in value:
        obj = _object(
            raw,
            "spatial seed",
            {"position", "field", "populations"},
            {"position", "field", "populations"},
        )
        position = _address(obj["position"], "spatial seed position", 0)
        if any(v >= n for v, n in zip(position, shape, strict=True)):
            raise ValueError("spatial seed position must be within shape")
        index = _index(obj["field"], names, "spatial seed field")
        if (position, index) in occupied:
            raise ValueError("duplicate spatial seed at the same cell and field")
        occupied.add((position, index))
        payloads = tuple(
            _payload(v, fields[spatial[index].field])
            for v in _array(obj["populations"], "spatial populations", 8, 8)
        )
        local = list(unpack(spatial[index].baseline))
        for payload in payloads:
            for component, amount in enumerate(unpack(payload)):
                local[component] = checked_work(local[component] + amount)
        fields[spatial[index].field].validate(pack(tuple(local)))
        result.append(SpatialSeed(position, index, payloads))
    return tuple(result)


def _spatial_couplings(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    spatial: tuple[SpatialFieldDefinition, ...],
    schema_version: int = 1,
) -> tuple[SpatialCouplingDefinition, ...]:
    result: list[SpatialCouplingDefinition] = []
    field_names, type_names = _names(fields), _names(disturbances)
    spatial_fields = tuple(definition.field for definition in spatial)
    flux_fields = tuple(index for index in spatial_fields if fields[index].components == 1)
    required = {"name", "type", "field", "mode"} | ({"budget"} if schema_version == 2 else set())
    for raw in _array(value, "spatial_couplings", MAX_RULES):
        obj = _object(
            raw,
            "spatial coupling",
            required | {"amount", "rotation", "denominator", "axis_order"},
            required,
        )
        name = _text(obj["name"], "spatial coupling.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate spatial coupling name")
        kind = _index(obj["type"], type_names, "spatial coupling.type")
        target = _index(obj["field"], field_names, "spatial coupling.field")
        mode = _text(obj["mode"], "spatial coupling.mode")
        if mode not in ("exchange", "rotation"):
            raise ValueError("spatial coupling.mode must be exchange or rotation")
        parameter = "amount" if mode == "exchange" else "rotation"
        allowed = (
            required | {parameter, "denominator"} | ({"axis_order"} if mode == "rotation" else set())
        )
        obj = _object(obj, "spatial coupling", allowed, required | {parameter})
        if target not in disturbances[kind].fields or target not in spatial_fields:
            raise ValueError("spatial coupling target must be both carried and spatial")
        field = fields[target]
        if not field.signed or not field.extensive:
            raise ValueError("spatial coupling target must be signed and extensive")
        if disturbances[kind].transport.mode == "split":
            raise ValueError("spatial coupling requires a whole-record hold or move type")
        if disturbances[kind].cost_field == target:
            raise ValueError("cost_field cannot also be a spatial coupling target")
        if mode == "rotation" and field.components != 3:
            raise ValueError("spatial rotation requires a three-component target")
        expression = _Expressions(fields, disturbances[kind].fields, spatial_fields, flux_fields).parse(
            obj[parameter], field.components
        )
        axes = tuple(
            _integer(axis, "spatial coupling.axis_order", 0)
            for axis in _array(obj.get("axis_order", [0, 1, 2]), "spatial coupling.axis_order", 3, 3)
        )
        if sorted(axes) != [0, 1, 2]:
            raise ValueError("spatial coupling.axis_order must be a permutation of 0, 1, 2")
        result.append(
            SpatialCouplingDefinition(
                name,
                kind,
                target,
                mode,
                expression,
                _integer(obj.get("denominator", 1), "spatial coupling.denominator", 1),
                cast(tuple[int, int, int], axes),
                _allowance(obj["budget"], field, "spatial coupling.budget")
                if schema_version == 2
                else None,
            )
        )
    return tuple(result)


def _field_groups(
    value: object, fields: tuple[FieldDefinition, ...]
) -> tuple[FieldGroupDefinition, ...]:
    result: list[FieldGroupDefinition] = []
    names = _names(fields)
    for raw in _array(value, "field_groups", MAX_FIELDS):
        obj = _object(raw, "field group", {"name", "fields"}, {"name", "fields"})
        name = _text(obj["name"], "field group.name")
        if any(group.name == name for group in result):
            raise ValueError("duplicate field group name")
        members = tuple(
            _index(item, names, "field group member")
            for item in _array(obj["fields"], "field group.fields", MAX_FIELDS, 1)
        )
        if len(set(members)) != len(members):
            raise ValueError("duplicate field group member")
        result.append(FieldGroupDefinition(name, members))
    return tuple(result)


def _field_rules(
    value: object,
    fields: tuple[FieldDefinition, ...],
    spatial: tuple[SpatialFieldDefinition, ...],
) -> tuple[NodeFieldRuleDefinition, ...]:
    result: list[NodeFieldRuleDefinition] = []
    spatial_fields = tuple(definition.field for definition in spatial)
    local_fields = tuple(definition.field for definition in spatial if definition.transport == "local")
    names = {fields[index].name: index for index in local_fields}

    def expression(raw: object, expected: int | None = None) -> Expression:
        return _Expressions(
            fields, (), spatial_fields, received_fields=spatial_fields, outgoing_fields=local_fields
        ).parse(raw, expected)

    required = {"name", "assignments", "invariants"}
    for raw in _array(value, "field_rules", MAX_RULES):
        obj = _object(raw, "field rule", required | {"when"}, required)
        name = _text(obj["name"], "field rule.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate field rule name")
        assignments: list[FieldAssignment] = []
        for raw_assignment in _array(obj["assignments"], "field assignments", MAX_RULES, 1):
            item = _object(
                raw_assignment,
                "field assignment",
                {"field", "expression", "port"},
                {"field", "expression"},
            )
            field = _index(item["field"], names, "local spatial assignment field")
            port = _integer(item["port"], "field assignment.port", 0) if "port" in item else -1
            if port >= 6:
                raise ValueError("field assignment.port must be from 0 through 5")
            if any(a.field == field and a.port == port for a in assignments):
                raise ValueError("duplicate field assignment target")
            assignments.append(
                FieldAssignment(field, expression(item["expression"], fields[field].components), port)
            )
        invariants: list[Invariant] = []
        for raw_invariant in _array(obj["invariants"], "field invariants", MAX_FIELDS, 1):
            item = _object(raw_invariant, "invariant", {"name", "expression"}, {"name", "expression"})
            invariant_name = _text(item["name"], "invariant.name")
            if any(invariant.name == invariant_name for invariant in invariants):
                raise ValueError("duplicate invariant name")
            invariant_expression = _Expressions(
                fields, (), spatial_fields, outgoing_fields=local_fields
            ).parse(item["expression"], invariant=True)
            invariants.append(Invariant(invariant_name, invariant_expression))
        when = expression(obj["when"], 1) if "when" in obj else None
        result.append(NodeFieldRuleDefinition(name, tuple(assignments), tuple(invariants), when))
    return tuple(result)


def _spatial_interactions(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    spatial: tuple[SpatialFieldDefinition, ...],
) -> tuple[SpatialInteractionDefinition, ...]:
    result: list[SpatialInteractionDefinition] = []
    type_names, field_names = _names(disturbances), _names(fields)
    spatial_fields = tuple(definition.field for definition in spatial)
    local_fields = tuple(definition.field for definition in spatial if definition.transport == "local")
    required = {"name", "type", "assignments", "invariants"}
    for raw in _array(value, "spatial_interactions", MAX_RULES):
        if not spatial:
            raise ValueError("spatial interactions require at least one spatial field")
        obj = _object(raw, "spatial interaction", required | {"when"}, required)
        name = _text(obj["name"], "spatial interaction.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate spatial interaction name")
        kind = _index(obj["type"], type_names, "spatial interaction.type")
        participant = disturbances[kind]
        if participant.transport.mode == "split":
            raise ValueError("spatial interaction requires a whole-record hold or move type")
        assignments: list[Assignment] = []
        for raw_assignment in _array(obj["assignments"], "spatial assignments", MAX_FIELDS * 2, 1):
            item = _object(
                raw_assignment,
                "spatial assignment",
                {"side", "field", "expression"},
                {"side", "field", "expression"},
            )
            if item["side"] not in ("left", "right"):
                raise ValueError("assignment.side must be left or right")
            side = 0 if item["side"] == "left" else 1
            field = _index(item["field"], field_names, "spatial assignment.field")
            owned = participant.fields if side == 0 else local_fields
            if field not in owned or (side == 0 and field == participant.cost_field):
                raise ValueError("spatial assignment requires an owned non-cost or local spatial field")
            if any(a.side == side and a.field == field for a in assignments):
                raise ValueError("duplicate spatial assignment target")
            expression = _Expressions(
                fields, participant.fields, spatial_fields, received_fields=spatial_fields
            ).parse(item["expression"], fields[field].components)
            assignments.append(Assignment(side, field, expression))
        invariants: list[Invariant] = []
        for raw_invariant in _array(obj["invariants"], "spatial invariants", MAX_FIELDS, 1):
            item = _object(raw_invariant, "invariant", {"name", "expression"}, {"name", "expression"})
            invariant_name = _text(item["name"], "invariant.name")
            if any(invariant.name == invariant_name for invariant in invariants):
                raise ValueError("duplicate invariant name")
            expression = _Expressions(fields, participant.fields, spatial_fields).parse(
                item["expression"], invariant=True
            )
            invariants.append(Invariant(invariant_name, expression))
        when = (
            _Expressions(
                fields, participant.fields, spatial_fields, received_fields=spatial_fields
            ).parse(obj["when"], 1)
            if "when" in obj
            else None
        )
        result.append(
            SpatialInteractionDefinition(name, kind, tuple(assignments), tuple(invariants), when)
        )
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
    obj = _object(
        document,
        "initial state",
        required
        | {
            "couplings",
            "interactions",
            "spatial_fields",
            "emissions",
            "spatial_seeds",
            "spatial_couplings",
            "boundary",
            "field_groups",
            "field_rules",
            "spatial_interactions",
            "event_program",
        },
        required,
    )
    schema_version = _integer(obj["schema_version"], "schema_version", 1)
    if schema_version not in (1, 2):
        raise ValueError("unsupported schema_version; expected 1 or 2")
    if schema_version != 1 and ({"field_rules", "spatial_interactions"} & obj.keys()):
        raise ValueError("field rules and spatial interactions require schema_version 1")
    boundary = _text(obj.get("boundary", "periodic"), "boundary")
    if boundary not in ("periodic", "open"):
        raise ValueError("boundary must be periodic or open")
    shape = _address(obj["shape"], "shape", 1)
    capacity = _integer(obj["slots_per_cell"], "slots_per_cell", 1)
    if capacity > MAX_SLOTS:
        raise ValueError(f"slots_per_cell exceeds {MAX_SLOTS}")
    costs = _object(obj["operation_costs"], "operation_costs", set(OPERATIONS), set(OPERATIONS))
    fields = _fields(obj["fields"])
    disturbances = _disturbances(obj["disturbance_types"], fields)
    spatial = _spatial_fields(obj.get("spatial_fields", []), fields, schema_version)
    initial = InitialState(
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
        spatial_fields=spatial,
        emissions=_emissions(obj.get("emissions", []), fields, disturbances, spatial, schema_version),
        spatial_seeds=_spatial_seeds(obj.get("spatial_seeds", []), fields, spatial, shape),
        spatial_couplings=_spatial_couplings(
            obj.get("spatial_couplings", []), fields, disturbances, spatial, schema_version
        ),
        schema_version=schema_version,
        boundary=boundary,
        interactions=_interactions(obj.get("interactions", []), fields, disturbances),
        field_groups=_field_groups(obj.get("field_groups", []), fields),
        field_rules=_field_rules(obj.get("field_rules", []), fields, spatial),
        spatial_interactions=_spatial_interactions(
            obj.get("spatial_interactions", []), fields, disturbances, spatial
        ),
        event_program=None if "event_program" not in obj else json.dumps(obj["event_program"]),
    )
    if initial.event_program is not None:
        from .integration.event_program import parse_event_program

        parse_event_program(initial)
    _validate_conversions(initial)
    return initial


def _validate_conversions(initial: InitialState) -> None:
    for rule in initial.interactions:
        if rule.output_types is None:
            continue
        if initial.schema_version != 1:
            raise ValueError("conversion requires schema_version 1")
        kinds = {rule.left_type, rule.right_type, *rule.output_types}
        if any(c.left_type in kinds or c.right_type in kinds for c in initial.couplings):
            raise ValueError("conversion types cannot participate in exchange couplings")
        spatial_types = (
            {r.type_index for r in initial.emissions}
            | {r.type_index for r in initial.spatial_couplings}
            | {r.type_index for r in initial.spatial_interactions}
        )
        if spatial_types & kinds:
            raise ValueError("conversion types cannot participate in spatial responses or emission")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_initial_state(path: Path) -> InitialState:
    """Read a strict JSON initialization file and parse its generic definitions."""
    return parse_initial_json(path.read_bytes())


def parse_initial_json(source: str | bytes) -> InitialState:
    """Parse one immutable JSON payload, rejecting duplicate keys."""
    return parse_initial_state(parse_json_document(source))


def parse_json_document(source: str | bytes) -> object:
    """Read data with the same duplicate-key policy for full inputs and editor fragments."""
    document: object = json.loads(source, object_pairs_hook=_unique_object)
    return document
