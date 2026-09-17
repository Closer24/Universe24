"""Validate declarative initial conditions without importing physical model laws."""

from dataclasses import replace
from pathlib import Path
from typing import cast

from .core.conservation_state import CarrierMeasurement, ConservationDefinition, QuantityExpressions
from .core.coupling_selectors import (
    selected_left_types,
    selected_right_types,
    selected_type_set,
    selected_types,
)
from .core.disturbance_state import (
    AGGREGATIONS,
    MAX_COMPONENTS,
    MAX_CONVERSION_ARITY,
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
    CAPTURE_MODES,
    CHARGE_INVARIANT,
    DECAY_RESIDUES,
    MAX_HEADINGS,
    MAX_PHASE_STEPS,
    MAX_RAY_SLOTS,
    MAX_STORED_PHASE_BITS,
    RAY_PROPERTIES,
    RAY_WRITABLE,
    DecayDefinition,
    EmissionDefinition,
    FieldAssignment,
    FieldGroupDefinition,
    NodeFieldRuleDefinition,
    SpatialCouplingDefinition,
    SpatialFieldDefinition,
    SpatialInteractionDefinition,
    SpatialSeed,
    charge_invariant,
    ray_participant_definitions,
    validate_heading,
)
from .json_documents import parse_json_document as parse_json_document
from .observer_configuration import ObserverDefinition


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


def _phase_value(value: object, label: str, phase_bits: int) -> int:
    """A phase or a rate of the declared width: an integer from 0 below 2^phase_bits.

    The phase is the one value with its own declared width (issue #169, 2026-09-17),
    so it is not bounded by MAX_VALUE; Python integers are unbounded.
    """
    if type(value) is not int or not 0 <= value < (1 << phase_bits):
        raise ValueError(
            f"{label} requires an integer from 0 below 2^{phase_bits}, the field's phase width"
        )
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


def _fields(value: object, *, node_execution: bool = False) -> tuple[FieldDefinition, ...]:
    result: list[FieldDefinition] = []
    required = {"name", "components", "units", "signed", "conserved"}
    for raw in _array(value, "fields", MAX_FIELDS, 1):
        obj = _object(raw, "field", required | {"scale", "extensive", "aggregation"}, required)
        components = _integer(obj["components"], "field.components", 1)
        if node_execution and components > MAX_COMPONENTS:
            raise ValueError(f"field.components exceeds {MAX_COMPONENTS}")
        if not node_execution and components not in (1, 3):
            raise ValueError("field.components must be 1 or 3")
        aggregation = _text(obj["aggregation"], "field.aggregation") if "aggregation" in obj else None
        if node_execution and aggregation is None:
            raise ValueError("node_execution requires an explicit aggregation for every field")
        if aggregation is not None and aggregation not in AGGREGATIONS:
            raise ValueError("unsupported field aggregation")
        if aggregation in ("sum", "phase_bins") and components != 1:
            raise ValueError("sum and phase_bins require scalar fields")
        if aggregation == "vector_sum" and components == 1:
            raise ValueError("vector_sum requires a vector field")
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
                aggregation=aggregation,
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
        items = _array(value, f"value for {field.name}", field.components, field.components)
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
        participants: tuple[tuple[int, ...], ...] = (),
        node_cost: bool = False,
    ) -> None:
        self.fields = fields
        self.names = _names(fields)
        self.owned = (left, right)
        self.nodes = 0
        self.flux_fields = flux_fields
        self.received_fields = received_fields
        self.outgoing_fields = outgoing_fields
        self.participants = participants
        self.node_cost = node_cost
        self.max_components = max(field.components for field in fields)

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
            items = _array(value, "expression literal", max(3, self.max_components), 1)
            if len(items) not in {1, 3, *(field.components for field in self.fields)}:
                raise ValueError("expression literal has an unsupported vector shape")
            literal = tuple(_integer(item, "expression literal component") for item in items)
            return Expression("literal", literal=literal), len(literal)
        obj = _object(
            value,
            "expression",
            {
                "field",
                "side",
                "participant",
                "op",
                "args",
                "index",
                "flux",
                "matrix",
                "received",
                "outgoing",
                "received_present",
                "port",
                "node",
            },
            set(),
        )
        if "node" in obj:
            _object(obj, "node expression", {"node"}, {"node"})
            if not self.node_cost or obj["node"] != "committed_cost":
                raise ValueError("node.committed_cost is available only to emission expressions")
            return Expression("node_cost"), 1
        if {"received", "outgoing", "received_present"}.intersection(obj):
            operation = (
                "received_present"
                if "received_present" in obj
                else "received"
                if "received" in obj
                else "outgoing"
            )
            obj = _object(obj, "directional expression", {operation, "port"}, {operation, "port"})
            owned = (
                self.received_fields
                if operation in ("received", "received_present")
                else self.outgoing_fields
            )
            names = {self.fields[index].name: index for index in owned}
            index = _index(obj[operation], names, f"{operation} spatial field")
            port = _integer(obj["port"], "expression.port", 0)
            if port >= 6:
                raise ValueError("expression.port must be from 0 through 5")
            return Expression(
                operation, field=index, port=port
            ), 1 if operation == "received_present" else self.fields[index].components
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
        if operation == "cross" and sizes != (3, 3):
            raise ValueError("cross requires two three-component vectors")
        if operation == "dot" and (sizes[0] < 2 or sizes[0] != sizes[1]):
            raise ValueError("dot requires two vectors of equal size")
        if len(sizes) == 2 and operation not in ("dot", "cross"):
            if min(sizes) != 1 and sizes[0] != sizes[1]:
                raise ValueError("incompatible expression component counts")
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
        obj = _object(obj, "field expression", {"field", "side", "participant"}, {"field"})
        if "participant" in obj:
            if "side" in obj or not self.participants:
                raise ValueError("participant references require an indexed interaction context")
            side = _integer(obj["participant"], "expression.participant", 0)
            if side >= len(self.participants):
                raise ValueError("expression participant exceeds the declared roles")
            index = _index(obj["field"], self.names, "expression.field")
            if index not in self.participants[side]:
                raise ValueError("expression references a field not owned by its participant")
            return Expression("field", field=index, side=side), self.fields[index].components
        if self.participants:
            if obj.get("side") != "right" or self.owned[1] is None:
                raise ValueError("indexed interactions require an explicit participant reference")
            index = _index(obj["field"], self.names, "expression.field")
            if index not in self.owned[1]:
                raise ValueError("expression references a field not owned by the local spatial state")
            return Expression("field", field=index, side=len(self.participants)), self.fields[
                index
            ].components
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
    if mode == "split" and any(
        fields[index].aggregation not in (None, "sum", "vector_sum") for index in owned
    ):
        raise ValueError("split transport requires additive aggregation for every carried field")
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


def _selection(
    obj: dict[str, object],
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    type_key: str,
    requires_key: str,
    label: str,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Resolve property layouts once and expose only guaranteed carrier properties."""
    if (type_key in obj) == (requires_key in obj):
        raise ValueError(f"{label} requires exactly one of {type_key} or {requires_key}")
    if type_key in obj:
        kind = _index(obj[type_key], _names(disturbances), f"{label}.{type_key}")
        return (kind,), disturbances[kind].fields
    required = tuple(
        _index(item, _names(fields), f"{label}.{requires_key}")
        for item in _array(obj[requires_key], requires_key, MAX_FIELDS, 1)
    )
    if len(set(required)) != len(required):
        raise ValueError(f"{label}.{requires_key} contains duplicate properties")
    kinds = tuple(i for i, kind in enumerate(disturbances) if set(required) <= set(kind.fields))
    if not kinds:
        raise ValueError(f"{label}.{requires_key} has no compatible disturbance layout")
    return kinds, required


def _couplings(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
) -> tuple[CouplingDefinition, ...]:
    result: list[CouplingDefinition] = []
    field_names = _names(fields)
    required = {"name", "field", "amount"}
    selectors = {"left_type", "right_type", "left_requires", "right_requires"}
    for raw in _array(value, "couplings", MAX_RULES):
        obj = _object(
            raw, "coupling", required | selectors | {"denominator", "remainder_owner"}, required
        )
        name = _text(obj["name"], "coupling.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate coupling name")
        left, left_fields = _selection(
            obj, fields, disturbances, "left_type", "left_requires", "coupling"
        )
        right, right_fields = _selection(
            obj, fields, disturbances, "right_type", "right_requires", "coupling"
        )
        field = _index(obj["field"], field_names, "coupling.field")
        if field not in left_fields or field not in right_fields:
            raise ValueError("coupling field must be owned by both participants")
        if any(field == disturbances[kind].cost_field for kind in (*left, *right)):
            raise ValueError("cost_field cannot also be a coupling target")
        amount = _Expressions(fields, left_fields, right_fields).parse(
            obj["amount"], fields[field].components
        )
        denominator = _integer(obj.get("denominator", 1), "coupling.denominator", 1)
        owner = _text(obj.get("remainder_owner", "pair"), "coupling.remainder_owner")
        if owner not in ("pair", "left"):
            raise ValueError("coupling.remainder_owner must be pair or left")
        if owner == "left":
            if set(left) & set(right):
                raise ValueError(
                    "left-owned exchange remainders require distinct participant types or disjoint property selections"
                )
            if any(disturbances[kind].transport.mode == "split" for kind in left):
                raise ValueError("left-owned exchange remainders require whole-record hold or move")
        result.append(
            CouplingDefinition(
                name,
                left[0],
                right[0],
                field,
                amount,
                denominator,
                owner,
                left if "left_requires" in obj else (),
                right if "right_requires" in obj else (),
            )
        )
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
    *,
    node_execution: bool = False,
) -> tuple[InteractionDefinition, ...]:
    result: list[InteractionDefinition] = []
    type_names, field_names = _names(disturbances), _names(fields)
    required = {"name", "assignments", "invariants"}
    selectors = {"left_type", "right_type", "left_requires", "right_requires"}
    for raw in _array(value, "interactions", MAX_RULES):
        obj = _object(
            raw,
            "interaction",
            required | selectors | {"when", "output_types", "k", "participants", "outputs"},
            required,
        )
        name = _text(obj["name"], "interaction.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate interaction name")
        k = _rule_ticks(obj, node_execution)
        if "outputs" in obj:
            if selectors.intersection(obj) or "output_types" in obj:
                raise ValueError("a family conversion selects its inputs with participants only")
            if "participants" not in obj:
                raise ValueError("conversion outputs require indexed participants")
            result.append(_conversion_interaction(obj, fields, disturbances, k))
            continue
        if "participants" in obj:
            if not node_execution:
                raise ValueError("indexed interactions require node_execution")
            if selectors.intersection(obj) or "output_types" in obj:
                raise ValueError("indexed interactions cannot combine pair selectors or conversions")
            result.append(_indexed_interaction(obj, fields, disturbances, k))
            continue
        left, left_fields = _selection(
            obj, fields, disturbances, "left_type", "left_requires", "interaction"
        )
        right, right_fields = _selection(
            obj, fields, disturbances, "right_type", "right_requires", "interaction"
        )
        participants = (disturbances[left[0]], disturbances[right[0]])

        def expression(
            raw: object,
            expected: int | None = None,
            left_fields: tuple[int, ...] = left_fields,
            right_fields: tuple[int, ...] = right_fields,
        ) -> Expression:
            return _Expressions(fields, left_fields, right_fields).parse(raw, expected)

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
            if field not in (left_fields, right_fields)[side] or any(
                field == disturbances[kind].cost_field for kind in (left, right)[side]
            ):
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
                    _Expressions(fields, left_fields, right_fields).parse(
                        item["expression"], invariant=True
                    ),
                )
            )
        when = expression(obj["when"], 1) if "when" in obj else None
        output_types = None
        if "output_types" in obj:
            if "left_requires" in obj or "right_requires" in obj:
                raise ValueError("conversion requires explicit type selectors")
            outputs = _object(obj["output_types"], "output_types", {"left", "right"}, {"left", "right"})
            output_types = (
                _index(outputs["left"], type_names, "output_types.left"),
                _index(outputs["right"], type_names, "output_types.right"),
            )
            if set(output_types) & {left[0], right[0]}:
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
                name,
                left[0],
                right[0],
                tuple(assignments),
                tuple(invariants),
                when,
                output_types,
                left if "left_requires" in obj else (),
                right if "right_requires" in obj else (),
                k,
            )
        )
    return tuple(result)


def _rule_ticks(obj: dict[str, object], required: bool) -> int:
    if "k" not in obj:
        if required:
            raise ValueError("node_execution requires explicit positive k for every local rule")
        return 0
    return _integer(obj["k"], "rule.k", 1)


def _participant_selections(
    obj: dict[str, object],
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    *,
    minimum: int = 2,
    maximum: int = MAX_SLOTS,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    """Compile the same bounded role selection for carrier and field transactions."""
    selections, owned = [], []
    for raw in _array(obj["participants"], "interaction.participants", maximum, minimum):
        role = _object(raw, "participant", {"type", "requires"}, set())
        kinds, properties = _selection(role, fields, disturbances, "type", "requires", "participant")
        selections.append(kinds)
        owned.append(properties)
    return tuple(selections), tuple(owned)


def _indexed_interaction(
    obj: dict[str, object],
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    k: int,
) -> InteractionDefinition:
    """Compile fixed participant roles, preserving their declared selection order."""
    selections, layouts = _participant_selections(obj, fields, disturbances)

    def expression(value: object, size: int | None = None, *, invariant: bool = False) -> Expression:
        return _Expressions(fields, (), participants=layouts).parse(value, size, invariant=invariant)

    assignments: list[Assignment] = []
    for raw in _array(obj["assignments"], "assignments", MAX_FIELDS * MAX_SLOTS, 1):
        item = _object(
            raw,
            "assignment",
            {"participant", "field", "expression"},
            {"participant", "field", "expression"},
        )
        participant = _integer(item["participant"], "assignment.participant", 0)
        if participant >= len(layouts):
            raise ValueError("assignment participant exceeds the declared roles")
        field = _index(item["field"], _names(fields), "assignment.field")
        if field not in layouts[participant] or any(
            disturbances[index].cost_field == field for index in selections[participant]
        ):
            raise ValueError("assignment requires an owned field other than cost_field")
        if any(a.side == participant and a.field == field for a in assignments):
            raise ValueError("duplicate assignment target")
        assignments.append(
            Assignment(participant, field, expression(item["expression"], fields[field].components))
        )
    invariants: list[Invariant] = []
    for raw in _array(obj["invariants"], "invariants", MAX_FIELDS, 1):
        item = _object(raw, "invariant", {"name", "expression"}, {"name", "expression"})
        name = _text(item["name"], "invariant.name")
        if any(invariant.name == name for invariant in invariants):
            raise ValueError("duplicate invariant name")
        invariants.append(Invariant(name, expression(item["expression"], invariant=True)))
    return InteractionDefinition(
        name=_text(obj["name"], "interaction.name"),
        left_type=selections[0][0],
        right_type=selections[1][0],
        assignments=tuple(assignments),
        invariants=tuple(invariants),
        when=expression(obj["when"], 1) if "when" in obj else None,
        k=k,
        participants=tuple(selections),
    )


def _conversion_interaction(
    obj: dict[str, object],
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    k: int,
) -> InteractionDefinition:
    """Compile an N-to-M family conversion: indexed inputs, declared output families.

    Every output payload is assigned from the frozen inputs. Invariants are
    per-record readouts whose sums over all inputs and all outputs must agree.
    """
    selections, layouts = _participant_selections(
        obj, fields, disturbances, minimum=1, maximum=MAX_CONVERSION_ARITY
    )
    type_names = _names(disturbances)
    outputs = []
    for raw in _array(obj["outputs"], "interaction.outputs", MAX_CONVERSION_ARITY, 1):
        item = _object(raw, "conversion output", {"type"}, {"type"})
        outputs.append(_index(item["type"], type_names, "output.type"))
    involved = {kind for role in selections for kind in role} | set(outputs)
    if any(
        disturbances[kind].transport.mode == "split" or disturbances[kind].cost_field is not None
        for kind in involved
    ):
        raise ValueError("conversion requires whole records without cost_field")

    def expression(value: object, size: int | None = None) -> Expression:
        return _Expressions(fields, (), participants=layouts).parse(value, size)

    field_names = _names(fields)
    assignments: list[Assignment] = []
    for raw in _array(obj["assignments"], "assignments", MAX_FIELDS * MAX_CONVERSION_ARITY, 1):
        item = _object(
            raw, "assignment", {"output", "field", "expression"}, {"output", "field", "expression"}
        )
        output = _integer(item["output"], "assignment.output", 0)
        if output >= len(outputs):
            raise ValueError("assignment output exceeds the declared outputs")
        field = _index(item["field"], field_names, "assignment.field")
        if field not in disturbances[outputs[output]].fields:
            raise ValueError("assignment requires a field owned by its output family")
        if any(a.side == output and a.field == field for a in assignments):
            raise ValueError("duplicate assignment target")
        assignments.append(
            Assignment(output, field, expression(item["expression"], fields[field].components))
        )
    expected = {(j, field) for j, kind in enumerate(outputs) for field in disturbances[kind].fields}
    if {(a.side, a.field) for a in assignments} != expected:
        raise ValueError("conversion requires explicit assignments for every output field")
    every_field = tuple(range(len(fields)))
    invariants: list[Invariant] = []
    for raw in _array(obj["invariants"], "invariants", MAX_FIELDS, 1):
        item = _object(raw, "invariant", {"name", "expression"}, {"name", "expression"})
        name = _text(item["name"], "invariant.name")
        if any(invariant.name == name for invariant in invariants):
            raise ValueError("duplicate invariant name")
        # A readout of one record; absent fields read as zero for that family.
        invariants.append(Invariant(name, _Expressions(fields, every_field).parse(item["expression"])))
    return InteractionDefinition(
        name=_text(obj["name"], "interaction.name"),
        left_type=selections[0][0],
        right_type=selections[-1][0],
        assignments=tuple(assignments),
        invariants=tuple(invariants),
        when=expression(obj["when"], 1) if "when" in obj else None,
        k=k,
        participants=tuple(selections),
        outputs=tuple(outputs),
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
            raise ValueError("initial seeds exceed slots_per_node")
        type_index = _index(obj["type"], names, "seed.type")
        definition = disturbances[type_index]
        values = _values(obj.get("values", {}), fields, definition.fields, definition.defaults)
        result.append(Seed(position, DisturbanceRecord(type_index, values, phases)))
    return tuple(result)


def _decay(value: object) -> DecayDefinition:
    keys = {"retain_numerator", "retain_denominator"}
    obj = _object(value, "spatial decay", keys | {"residue"}, keys)
    numerator = _integer(obj["retain_numerator"], "decay.retain_numerator", 0)
    denominator = _integer(obj["retain_denominator"], "decay.retain_denominator", 1)
    if numerator >= denominator:
        raise ValueError("decay requires retain_numerator < retain_denominator")
    residue = _text(obj.get("residue", "localize"), "decay.residue")
    if residue not in DECAY_RESIDUES:
        raise ValueError("decay.residue must be dissipate or localize")
    return DecayDefinition(numerator, denominator, residue)


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
            | {
                "headings",
                "rays_per_tick",
                "ray_slots",
                "self_exclusion",
                "kerengonen",
                "metric",
                "pace",
                "flux_projection",
                "phase_bits",
                "charge",
            }
            | ({"decay"} if schema_version == 2 else set()),
            {"field", "transport"} | ({"decay"} if schema_version == 2 else set()),
        )
        index = _index(obj["field"], names, "spatial field")
        if any(item.field == index for item in result):
            raise ValueError("duplicate spatial field")
        field = fields[index]
        if not field.extensive:
            raise ValueError("spatial transport requires extensive field components")
        if field.aggregation not in (None, "sum", "vector_sum"):
            raise ValueError("spatial ownership requires additive field aggregation")
        transport = _text(obj["transport"], "spatial transport")
        if transport not in ("outward", "local", "ray"):
            raise ValueError("spatial transport must be outward, local or ray")
        if transport == "local" and schema_version != 1:
            raise ValueError("local spatial transport requires schema_version 1")
        ray_keys = {"headings", "rays_per_tick", "ray_slots"}
        self_exclusion = False
        phase_steps, phase_advance = 0, 0
        phase_bits, charge = 0, 0
        capture = "share"
        metric = "links"
        pace_numerator, pace_denominator = 1, 1
        flux_projection = "ports"
        if transport == "ray":
            flux_projection = _text(obj.get("flux_projection", "ports"), "flux_projection")
            self_exclusion = _boolean(obj.get("self_exclusion", False), "self_exclusion")
            # Every ray is a wave ray (wave-ray-family-v1): the family declares the
            # width of its phase, 2^phase_bits values, and its charge per quantum.
            if "phase_bits" in obj:
                phase_bits = _integer(obj["phase_bits"], "phase_bits", 0)
            charge = _integer(obj.get("charge", 0), "spatial field charge")
            if self_exclusion and phase_bits > MAX_STORED_PHASE_BITS:
                raise ValueError(
                    "self_exclusion stores the departure phase as a bounded value: it requires "
                    "phase_bits at most 30"
                )
            metric = _text(obj.get("metric", "links"), "spatial field metric")
            if metric not in ("links", "euclidean"):
                raise ValueError("spatial field metric must be links or euclidean")
            if "pace" in obj:
                # Slower than link speed: the fastest heading hops numerator links
                # every denominator ticks. Never faster: the causal bound stands.
                pace = tuple(_integer(v, "pace term", 1) for v in _array(obj["pace"], "pace", 2, 2))
                pace_numerator, pace_denominator = pace
                if pace_numerator > pace_denominator:
                    raise ValueError("pace must not exceed one link per tick")
            if "kerengonen" in obj:
                # Kerengonen: phased rays. phase_advance, the family's rest rate, is
                # required and explicit; phase_steps declares the coherence table, one
                # entry per phase step of one turn, and fixes the width (2^phase_bits =
                # phase_steps) unless phase_bits declares the same width; a family
                # without a table has a rate and no coherence coupling.
                phased = _object(
                    obj["kerengonen"],
                    "kerengonen",
                    {"phase_steps", "phase_advance", "capture"},
                    {"phase_advance"},
                )
                if "phase_steps" in phased:
                    phase_steps = _integer(phased["phase_steps"], "kerengonen.phase_steps", 2)
                    if phase_steps > MAX_PHASE_STEPS or phase_steps & (phase_steps - 1):
                        raise ValueError(
                            "kerengonen phase_steps must be a power of two between 2 and 4096"
                        )
                    table_bits = phase_steps.bit_length() - 1
                    if "phase_bits" in obj and phase_bits != table_bits:
                        raise ValueError("kerengonen phase_steps must equal 2 to the power phase_bits")
                    phase_bits = table_bits
                elif "capture" in phased:
                    raise ValueError("kerengonen.capture requires phase_steps, the coherence table")
                capture = _text(phased.get("capture", "share"), "kerengonen.capture")
                if capture not in CAPTURE_MODES:
                    raise ValueError(
                        "kerengonen.capture must be share or threshold: the lottery capture was "
                        "deleted on 2026-09-17, only a Node whose Detector bit is set may draw"
                    )
                phase_advance = _phase_value(
                    phased["phase_advance"], "kerengonen.phase_advance", phase_bits
                )
            missing = ray_keys - obj.keys()
            if missing:
                raise ValueError(f"ray transport requires keys: {', '.join(sorted(missing))}")
            if field.components != 1:
                raise ValueError("ray transport requires a scalar field")
            if "axis_weights" in obj or "octant_weights" in obj:
                raise ValueError("ray transport does not use axis or octant weights")
            headings = tuple(
                cast(
                    tuple[int, int, int],
                    tuple(_integer(v, "ray heading component") for v in _array(h, "ray heading", 3, 3)),
                )
                for h in _array(obj["headings"], "headings", MAX_HEADINGS, 1)
            )
            for heading in headings:
                validate_heading(heading)
            ray_slots = _integer(obj["ray_slots"], "ray_slots", 1)
            rays_per_tick = _integer(obj["rays_per_tick"], "rays_per_tick", 1)
            if ray_slots > MAX_RAY_SLOTS or rays_per_tick > ray_slots:
                raise ValueError("rays_per_tick must not exceed ray_slots, at most 4096")
        elif (
            ray_keys
            | {"self_exclusion", "kerengonen", "metric", "pace", "flux_projection"}
            | {"phase_bits", "charge"}
        ) & obj.keys():
            raise ValueError(
                "headings, rays_per_tick, ray_slots, self_exclusion, kerengonen, metric, pace, "
                "flux_projection, phase_bits and charge require ray transport"
            )
        else:
            headings, rays_per_tick, ray_slots = (), 0, 0
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
                headings,
                rays_per_tick,
                ray_slots,
                self_exclusion,
                phase_steps,
                phase_advance,
                capture,
                metric=metric,
                pace_numerator=pace_numerator,
                pace_denominator=pace_denominator,
                flux_projection=flux_projection,
                phase_bits=phase_bits,
                charge=charge,
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
            {
                "type",
                "requires",
                "field",
                "amount",
                "denominator",
                "source",
                "recoil_field",
                "kerengonen_phase",
                "kerengonen_advance",
                "kerengonen_mirror",
                "dissolve",
                "heading",
            }
            | ({"budget"} if schema_version == 2 else set()),
            {"field", "source"} | ({"budget"} if schema_version == 2 else set()),
        )
        if "amount" not in obj and "dissolve" not in obj:
            raise ValueError("emission requires an amount unless it dissolves")
        source = _boolean(obj["source"], "emission.source")
        kinds, owned = _selection(obj, fields, disturbances, "type", "requires", "emission")
        kind = kinds[0]
        index = _index(obj["field"], names, "emission.field")
        recoil: int | None = None
        if not source:
            # Funded emission: the record pays from its own field of the same name.
            if spatial[index].field not in owned:
                raise ValueError("funded emission requires the emitting type to own the emitted field")
            if spatial[index].rays and schema_version == 2:
                raise ValueError("funded ray emission requires schema_version 1")
        if "recoil_field" in obj:
            if source:
                raise ValueError("recoil_field requires a funded emission (source: false)")
            recoil = _index(obj["recoil_field"], _names(fields), "emission.recoil_field")
            if recoil not in owned or fields[recoil].components != 3 or not fields[recoil].signed:
                raise ValueError("recoil_field must be a signed vector owned by the emitting type")
        phase, carried = 0, False
        if "kerengonen_phase" in obj:
            # Every ray is a wave ray: an emission stamps a phase on any ray field of
            # the declared width, a plain field included (its rate is 0, so the ray
            # carries the emitter's phase unchanged, as light does).
            if not spatial[index].rays:
                raise ValueError("kerengonen_phase requires a ray field")
            if obj["kerengonen_phase"] == "carried":
                # The phase of what the emitter last absorbed; checked against the
                # absorb rules once every spatial coupling is parsed.
                if not spatial[index].coherent:
                    raise ValueError(
                        "a carried kerengonen_phase requires the field's kerengonen coherence table"
                    )
                carried = True
            else:
                phase = _phase_value(
                    obj["kerengonen_phase"], "emission.kerengonen_phase", spatial[index].phase_bits
                )
        advance: Expression | None = None
        advance_denominator = 1
        if "kerengonen_advance" in obj:
            if not spatial[index].kerengonen:
                raise ValueError("kerengonen_advance requires a kerengonen ray field")
            advance_object = _object(
                obj["kerengonen_advance"],
                "emission.kerengonen_advance",
                {"amount", "denominator"},
                {"amount"},
            )
            advance = _Expressions(fields, owned).parse(advance_object["amount"], 1)
            advance_denominator = _integer(
                advance_object.get("denominator", 1), "emission.kerengonen_advance.denominator", 1
            )
        dissolve_after, dissolve_over = 0, 0
        if "dissolve" in obj:
            if source or not spatial[index].rays:
                raise ValueError("dissolve requires a funded emission on a ray field")
            schedule = _object(
                obj["dissolve"],
                "emission.dissolve",
                {"after_ticks", "over_ticks"},
                {"after_ticks", "over_ticks"},
            )
            dissolve_after = _integer(schedule["after_ticks"], "emission.dissolve.after_ticks", 0)
            dissolve_over = _integer(schedule["over_ticks"], "emission.dissolve.over_ticks", 1)
        mirror: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] | None = None
        if "kerengonen_mirror" in obj:
            if not spatial[index].coherent:
                raise ValueError(
                    "kerengonen_mirror requires a kerengonen ray field with a coherence table"
                )
            axis = _text(obj["kerengonen_mirror"], "emission.kerengonen_mirror")
            if axis in ("x", "y", "z"):
                # A mirror across the plane normal to one axis: that component flips.
                mirror = cast(
                    tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                    tuple((i, -1 if "xyz"[i] == axis else 1) for i in range(3)),
                )
            elif axis in ("xy", "xz", "yz"):
                # A mirror across the diagonal plane of two axes: they swap.
                first, second = "xyz".index(axis[0]), "xyz".index(axis[1])
                order = [0, 1, 2]
                order[first], order[second] = second, first
                mirror = cast(
                    tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                    tuple((order[i], 1) for i in range(3)),
                )
            else:
                raise ValueError("kerengonen_mirror must be x, y, z, xy, xz or yz")
            for heading in spatial[index].headings:
                image = tuple(heading[source] * sign for source, sign in mirror)
                if image not in spatial[index].headings:
                    raise ValueError(
                        "kerengonen_mirror requires the heading sequence to contain every mirror image"
                    )
            if "recoil_field" not in obj:
                raise ValueError(
                    "kerengonen_mirror requires a recoil_field: a mirror takes the momentum it reverses"
                )
        fixed_heading: int | None = None
        if "heading" in obj:
            if not spatial[index].rays:
                raise ValueError("emission.heading requires a ray field")
            if mirror is not None:
                raise ValueError("emission.heading cannot be combined with kerengonen_mirror")
            fixed = cast(
                tuple[int, int, int],
                tuple(
                    _integer(v, "emission.heading component")
                    for v in _array(obj["heading"], "emission.heading", 3, 3)
                ),
            )
            if fixed not in spatial[index].headings:
                raise ValueError("emission.heading must be one of the field's headings")
            fixed_heading = spatial[index].headings.index(fixed)
        if any(disturbances[index].transport.mode == "split" for index in kinds):
            raise ValueError("an emitting disturbance must hold or move as a whole record")
        if any(
            set(selected_types(item)) & set(kinds) and item.spatial_field == index for item in result
        ):
            raise ValueError("duplicate emission for the same disturbance type and field")
        amount = _Expressions(fields, owned, node_cost=True).parse(
            obj.get("amount", 0), fields[spatial[index].field].components
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
                kinds if "requires" in obj else (),
                not source,
                recoil,
                phase,
                carried,
                advance,
                advance_denominator,
                mirror,
                dissolve_after,
                dissolve_over,
                fixed_heading,
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
        if spatial[index].rays:
            raise ValueError("ray transport fields take no octant seeds; use an emitting source")
        if (position, index) in occupied:
            raise ValueError("duplicate spatial seed at the same node and field")
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
    field_names = _names(fields)
    spatial_fields = tuple(definition.field for definition in spatial)
    flux_fields = tuple(index for index in spatial_fields if fields[index].components == 1)
    required = {"name", "field", "mode"} | ({"budget"} if schema_version == 2 else set())
    for raw in _array(value, "spatial_couplings", MAX_RULES):
        obj = _object(
            raw,
            "spatial coupling",
            required
            | {
                "type",
                "requires",
                "amount",
                "rotation",
                "denominator",
                "axis_order",
                "momentum_field",
                "fraction",
                "fraction_denominator",
            },
            required,
        )
        name = _text(obj["name"], "spatial coupling.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate spatial coupling name")
        kinds, owned = _selection(obj, fields, disturbances, "type", "requires", "spatial coupling")
        kind = kinds[0]
        target = _index(obj["field"], field_names, "spatial coupling.field")
        mode = _text(obj["mode"], "spatial coupling.mode")
        if mode not in ("exchange", "rotation", "absorb"):
            raise ValueError("spatial coupling.mode must be exchange, rotation or absorb")
        if mode == "absorb":
            obj = _object(
                obj,
                "spatial coupling",
                required
                | {
                    "type",
                    "requires",
                    "momentum_field",
                    "fraction",
                    "fraction_denominator",
                },
                required,
            )
            definition = next((d for d in spatial if d.field == target), None)
            if definition is None or not definition.rays or target not in owned:
                raise ValueError("absorb requires a ray field that the absorbing type also carries")
            if schema_version != 1:
                raise ValueError("absorb requires schema_version 1")
            if any(disturbances[index].transport.mode == "split" for index in kinds):
                raise ValueError("absorb requires a whole-record hold or move type")
            momentum: int | None = None
            if "momentum_field" in obj:
                momentum = _index(obj["momentum_field"], field_names, "spatial coupling.momentum_field")
                if (
                    momentum not in owned
                    or fields[momentum].components != 3
                    or not fields[momentum].signed
                ):
                    raise ValueError(
                        "momentum_field must be a signed vector owned by the absorbing type"
                    )
            fraction: Expression | None = None
            fraction_denominator = 1
            if "fraction" in obj:
                fraction = _Expressions(fields, owned).parse(obj["fraction"], 1)
                if "fraction_denominator" in obj:
                    fraction_denominator = _integer(
                        obj["fraction_denominator"], "spatial coupling.fraction_denominator", 1
                    )
            elif "fraction_denominator" in obj:
                raise ValueError("fraction_denominator requires an absorb fraction")
            result.append(
                SpatialCouplingDefinition(
                    name,
                    kind,
                    target,
                    mode,
                    _Expressions(fields, owned).parse(1, 1),
                    1,
                    (0, 1, 2),
                    None,
                    kinds if "requires" in obj else (),
                    momentum,
                    fraction,
                    fraction_denominator,
                )
            )
            continue
        parameter = "amount" if mode == "exchange" else "rotation"
        allowed = (
            required
            | {"type", "requires", parameter, "denominator"}
            | ({"axis_order"} if mode == "rotation" else set())
        )
        obj = _object(obj, "spatial coupling", allowed, required | {parameter})
        if target not in owned or target not in spatial_fields:
            raise ValueError("spatial coupling target must be both carried and spatial")
        field = fields[target]
        if not field.signed or not field.extensive:
            raise ValueError("spatial coupling target must be signed and extensive")
        if any(disturbances[index].transport.mode == "split" for index in kinds):
            raise ValueError("spatial coupling requires a whole-record hold or move type")
        if any(disturbances[index].cost_field == target for index in kinds):
            raise ValueError("cost_field cannot also be a spatial coupling target")
        if mode == "rotation" and field.components != 3:
            raise ValueError("spatial rotation requires a three-component target")
        expression = _Expressions(fields, owned, spatial_fields, flux_fields).parse(
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
                kinds if "requires" in obj else (),
            )
        )
    absorbed = {rule.field for rule in result if rule.mode == "absorb"}
    if any(rule.mode != "absorb" and rule.field in absorbed for rule in result):
        raise ValueError("a ray field cannot be both absorbed and exchanged or rotated")
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
    *,
    node_execution: bool = False,
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
        obj = _object(raw, "field rule", required | {"when", "commit_when", "k"}, required)
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
        result.append(
            NodeFieldRuleDefinition(
                name,
                tuple(assignments),
                tuple(invariants),
                when,
                _rule_ticks(obj, node_execution),
                commit_when=(
                    _Expressions(fields, (), spatial_fields).parse(obj["commit_when"], 1)
                    if "commit_when" in obj
                    else None
                ),
            )
        )
    return tuple(result)


def _spatial_interactions(
    value: object,
    fields: tuple[FieldDefinition, ...],
    disturbances: tuple[DisturbanceDefinition, ...],
    spatial: tuple[SpatialFieldDefinition, ...],
    *,
    node_execution: bool = False,
) -> tuple[SpatialInteractionDefinition, ...]:
    result: list[SpatialInteractionDefinition] = []
    field_names = _names(fields)
    spatial_fields = tuple(definition.field for definition in spatial)
    local_fields = tuple(definition.field for definition in spatial if definition.transport == "local")
    required = {"name", "assignments", "invariants"}
    for raw in _array(value, "spatial_interactions", MAX_RULES):
        if not spatial:
            raise ValueError("spatial interactions require at least one spatial field")
        obj = _object(
            raw,
            "spatial interaction",
            required | {"type", "requires", "participants", "when", "commit_when", "k"},
            required,
        )
        name = _text(obj["name"], "spatial interaction.name")
        if any(rule.name == name for rule in result):
            raise ValueError("duplicate spatial interaction name")
        indexed = "participants" in obj
        if indexed:
            if {"type", "requires"}.intersection(obj):
                raise ValueError("spatial interactions cannot mix participants with type or requires")
            selections, layouts = _participant_selections(obj, fields, disturbances)
        else:
            kinds, carrier_fields = _selection(
                obj, fields, disturbances, "type", "requires", "spatial interaction"
            )
            selections, layouts = (kinds,), (carrier_fields,)
        if any(disturbances[index].transport.mode == "split" for kinds in selections for index in kinds):
            raise ValueError("spatial interaction requires a whole-record hold or move type")
        spatial_side = len(layouts)

        def expression(
            value: object,
            size: int | None = None,
            *,
            invariant: bool = False,
            received: bool = False,
            owned: tuple[tuple[int, ...], ...] = layouts,
            indexed_roles: bool = indexed,
        ) -> Expression:
            return _Expressions(
                fields,
                owned[0],
                spatial_fields,
                received_fields=spatial_fields if received else (),
                participants=owned if indexed_roles else (),
            ).parse(value, size, invariant=invariant)

        assignments: list[Assignment] = []
        for raw_assignment in _array(
            obj["assignments"], "spatial assignments", MAX_FIELDS * (spatial_side + 1), 1
        ):
            item = _object(
                raw_assignment,
                "spatial assignment",
                {"side", "participant", "field", "expression"},
                {"field", "expression"},
            )
            if indexed and "participant" in item:
                if "side" in item:
                    raise ValueError("spatial assignment cannot mix participant and side")
                side = _integer(item["participant"], "assignment.participant", 0)
                if side >= spatial_side:
                    raise ValueError("assignment participant exceeds the declared roles")
            elif indexed:
                if item.get("side") != "right":
                    raise ValueError("indexed assignments require an explicit participant or right side")
                side = spatial_side
            else:
                if "participant" in item or item.get("side") not in ("left", "right"):
                    raise ValueError("assignment.side must be left or right")
                side = 0 if item["side"] == "left" else 1
            field = _index(item["field"], field_names, "spatial assignment.field")
            owned = local_fields if side == spatial_side else layouts[side]
            if field not in owned or (
                side != spatial_side
                and any(field == disturbances[index].cost_field for index in selections[side])
            ):
                raise ValueError("spatial assignment requires an owned non-cost or local spatial field")
            if any(a.side == side and a.field == field for a in assignments):
                raise ValueError("duplicate spatial assignment target")
            assignments.append(
                Assignment(
                    side, field, expression(item["expression"], fields[field].components, received=True)
                )
            )
        invariants: list[Invariant] = []
        for raw_invariant in _array(obj["invariants"], "spatial invariants", MAX_FIELDS, 1):
            item = _object(raw_invariant, "invariant", {"name", "expression"}, {"name", "expression"})
            invariant_name = _text(item["name"], "invariant.name")
            if any(invariant.name == invariant_name for invariant in invariants):
                raise ValueError("duplicate invariant name")
            invariants.append(Invariant(invariant_name, expression(item["expression"], invariant=True)))
        result.append(
            SpatialInteractionDefinition(
                name,
                selections[0][0],
                tuple(assignments),
                tuple(invariants),
                expression(obj["when"], 1, received=True) if "when" in obj else None,
                selections[0] if "requires" in obj else (),
                _rule_ticks(obj, node_execution),
                participants=selections if indexed else (),
                commit_when=expression(obj["commit_when"], 1) if "commit_when" in obj else None,
            )
        )
    return tuple(result)


def _ray_interactions(
    value: object,
    fields: tuple[FieldDefinition, ...],
    spatial: tuple[SpatialFieldDefinition, ...],
) -> tuple[InteractionDefinition, ...]:
    """Compile the existing indexed syntax against structural complete-ray views."""
    definitions = ray_participant_definitions(fields, spatial)
    required = {"name", "participants", "assignments", "invariants"}
    rules: list[InteractionDefinition] = []
    for raw in _array(value, "ray_interactions", MAX_RULES):
        obj = _object(raw, "ray interaction", required | {"when"}, required)
        rule = _indexed_interaction(obj, RAY_PROPERTIES, definitions, 0)
        if len(rule.participants) > 6:
            raise ValueError("ray interactions admit at most six participants")
        if any(assignment.field not in RAY_WRITABLE for assignment in rule.assignments):
            raise ValueError("ray interaction amount, advance, family and charge are read-only")
        if any(existing.name == rule.name for existing in rules):
            raise ValueError("duplicate ray interaction name")
        if any(invariant.name == CHARGE_INVARIANT for invariant in rule.invariants):
            raise ValueError(
                "the charge invariant is declared for every ray interaction; "
                "do not declare another invariant named charge"
            )
        # wave-ray-family-v1: charge x amount summed over the participants is an
        # invariant of every declared ray interaction, checked like the declared ones.
        rule = replace(rule, invariants=(*rule.invariants, charge_invariant(len(rule.participants))))
        rules.append(rule)
    return tuple(rules)


def parse_initial_state(document: object) -> InitialState:
    """Reject malformed, ambiguous or unbounded initialization data before a run."""
    required = {
        "schema_version",
        "model_id",
        "shape",
        "slots_per_node",
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
            "ray_interactions",
            "observer",
            "conservation",
            "node_execution",
            "conservation_contract",
            "spatial_computation_delay",
            "field_phase_first",
            "arrival_port_blind",
            "allocation_phase",
            "computation_field",
            "delay_direction",
            "least_delay_routing",
            "ray_delay",
            "focus",
            "ray_phase_per_tick",
            "sampling_profile",
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
    if "observer" in obj:
        ObserverDefinition.parse(obj["observer"], shape)
    capacity = _integer(obj["slots_per_node"], "slots_per_node", 1)
    if capacity > MAX_SLOTS:
        raise ValueError(f"slots_per_node exceeds {MAX_SLOTS}")
    costs = _object(obj["operation_costs"], "operation_costs", set(OPERATIONS), set(OPERATIONS))
    node_execution = _boolean(obj.get("node_execution", False), "node_execution")
    fields = _fields(obj["fields"], node_execution=node_execution)
    disturbances = _disturbances(obj["disturbance_types"], fields)
    spatial = _spatial_fields(obj.get("spatial_fields", []), fields, schema_version)
    initial = InitialState(
        model_id=_text(obj["model_id"], "model_id"),
        sampling_profile=_text(obj.get("sampling_profile", "detector-only-v1"), "sampling_profile"),
        shape=shape,
        slots_per_node=capacity,
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
        interactions=_interactions(
            obj.get("interactions", []), fields, disturbances, node_execution=node_execution
        ),
        field_groups=_field_groups(obj.get("field_groups", []), fields),
        field_rules=_field_rules(
            obj.get("field_rules", []), fields, spatial, node_execution=node_execution
        ),
        spatial_interactions=_spatial_interactions(
            obj.get("spatial_interactions", []),
            fields,
            disturbances,
            spatial,
            node_execution=node_execution,
        ),
        ray_interactions=_ray_interactions(obj.get("ray_interactions", []), fields, spatial),
        node_execution=node_execution,
        spatial_computation_delay=_boolean(
            obj.get("spatial_computation_delay", False), "spatial_computation_delay"
        ),
        field_phase_first=_boolean(obj.get("field_phase_first", False), "field_phase_first"),
        arrival_port_blind=_boolean(obj.get("arrival_port_blind", False), "arrival_port_blind"),
        allocation_phase=_text(obj.get("allocation_phase", "straight"), "allocation_phase"),
        computation_field=(
            None
            if "computation_field" not in obj
            else _index(obj["computation_field"], _names(fields), "computation_field")
        ),
        delay_direction=(
            None if "delay_direction" not in obj else _text(obj["delay_direction"], "delay_direction")
        ),
        least_delay_routing=_boolean(obj.get("least_delay_routing", False), "least_delay_routing"),
        ray_delay=_boolean(obj.get("ray_delay", False), "ray_delay"),
        focus=_boolean(obj.get("focus", True), "focus"),
        ray_phase_per_tick=_boolean(obj.get("ray_phase_per_tick", False), "ray_phase_per_tick"),
    )
    if any(len(rule.participants) > capacity for rule in initial.spatial_interactions):
        raise ValueError("spatial interaction participant count exceeds slots_per_node")
    if any(definition.rays for definition in initial.spatial_fields):
        if node_execution or initial.spatial_computation_delay:
            raise ValueError("ray transport requires the fixed field clock without node_execution")
        if initial.spatial_interactions or initial.field_rules:
            raise ValueError("ray transport does not support field rules or spatial interactions")
        bindings: dict[int, int] = {}
        for emission in initial.emissions:
            if emission.recoil_field is not None:
                bindings[emission.spatial_field] = emission.recoil_field
        for index, definition in enumerate(initial.spatial_fields):
            targets = {
                rule.recoil_field
                for rule in initial.emissions
                if rule.spatial_field == index and rule.recoil_field is not None
            } | {
                rule.momentum_field
                for rule in initial.spatial_couplings
                if rule.field == definition.field
                and rule.mode == "absorb"
                and rule.momentum_field is not None
            }
            if len(targets) > 1:
                raise ValueError("a ray field requires one consistent momentum field binding")
            if targets:
                target = next(iter(targets))
                if any(item.field == target for item in initial.spatial_fields):
                    raise ValueError("ray momentum field cannot also own spatial populations")
                bindings[index] = target
            if (
                (definition.kerengonen or definition.decay is not None)
                and definition.self_exclusion
                and any(rule.mode != "absorb" for rule in initial.spatial_couplings)
            ):
                raise ValueError(
                    "phased or decaying self-exclusion supports absorption only, not response sampling"
                )
        initial = replace(
            initial,
            spatial_fields=tuple(
                replace(definition, momentum_field=bindings.get(index))
                for index, definition in enumerate(initial.spatial_fields)
            ),
        )
    if node_execution:
        if "conservation_contract" not in obj:
            raise ValueError("node_execution requires an explicit conservation_contract")
        if initial.schema_version != 1 or initial.link_ticks != 1:
            raise ValueError("node_execution requires schema_version 1 and link_ticks 1")
        if (
            initial.couplings
            or initial.emissions
            or initial.spatial_couplings
            or any(kind.updates for kind in initial.disturbances)
        ):
            raise ValueError("node_execution requires explicit k rules instead of unpriced legacy rules")
        if any(len(rule.participants) > capacity for rule in initial.interactions):
            raise ValueError("interaction participant count exceeds slots_per_node")
    for rule in initial.emissions:
        if (rule.phase_carried or rule.mirror is not None) and not any(
            coupling.mode == "absorb"
            and coupling.field == initial.spatial_fields[rule.spatial_field].field
            and set(selected_types(coupling)) & set(selected_types(rule))
            for coupling in initial.spatial_couplings
        ):
            raise ValueError(
                "a carried kerengonen_phase or kerengonen_mirror requires an absorb rule on the same field"
            )
    _validate_conversions(initial)
    if "conservation" in obj:
        initial = replace(initial, conservation=_conservation(obj["conservation"], initial))
        from .diagnostics.local_conservation import validate_empty_measurement

        validate_empty_measurement(initial)
    if "conservation_contract" in obj:
        from .node_conservation_configuration import parse_node_conservation

        initial = replace(
            initial, conservation_contract=parse_node_conservation(obj["conservation_contract"], initial)
        )
    return initial


def _conservation(value: object, initial: InitialState) -> ConservationDefinition:
    """Parse explicit measurement expressions without executing a law or world."""
    required = {"name", "energy_units", "momentum_units", "carriers"}
    obj = _object(value, "conservation", required | {"spatial"}, required)
    if any(not rule.funded for rule in initial.emissions) or any(
        update.source for kind in initial.disturbances for update in kind.updates
    ):
        raise ValueError("conservation audit requires closed internal transfers, not explicit sources")
    if any(any(unpack(field.baseline)) for field in initial.spatial_fields):
        raise ValueError("conservation audit requires zero spatial baselines")
    if any(
        field.decay is not None and field.decay.retain_numerator != field.decay.retain_denominator
        for field in initial.spatial_fields
    ):
        raise ValueError("conservation audit requires lossless transport or an owned reservoir")
    field_names = {field.name: index for index, field in enumerate(initial.fields)}
    measurements: list[CarrierMeasurement] = []
    covered: set[int] = set()
    for value in _array(obj["carriers"], "conservation.carriers", MAX_TYPES):
        row = _object(
            value,
            "carrier measurement",
            {"requires", "energy", "momentum"},
            {"requires", "energy", "momentum"},
        )
        names = _array(row["requires"], "conservation requires", MAX_FIELDS, 1)
        owned = tuple(_index(name, field_names, "conservation property") for name in names)
        if len(set(owned)) != len(owned):
            raise ValueError("duplicate conservation property")
        kinds = tuple(i for i, kind in enumerate(initial.disturbances) if set(owned) <= set(kind.fields))
        if not kinds or covered.intersection(kinds):
            raise ValueError("each disturbance layout must match exactly one conservation measurement")
        if any(initial.disturbances[i].cost_field in owned for i in kinds):
            raise ValueError("conservation measurements cannot depend on a computation cost reporter")
        quantities = QuantityExpressions(
            _Expressions(initial.fields, owned, ()).parse(row["energy"], 1),
            _Expressions(initial.fields, owned, ()).parse(row["momentum"], 3),
        )
        covered.update(kinds)
        measurements.append(CarrierMeasurement(kinds, quantities))
    if covered != set(range(len(initial.disturbances))):
        raise ValueError("conservation measurements must cover every disturbance layout")
    if bool(initial.spatial_fields) != ("spatial" in obj):
        raise ValueError("conservation spatial measurement must match spatial field presence")
    spatial = None
    if "spatial" in obj:
        row = _object(
            obj["spatial"], "spatial measurement", {"energy", "momentum"}, {"energy", "momentum"}
        )
        owned = tuple(field.field for field in initial.spatial_fields)
        spatial = QuantityExpressions(
            _Expressions(initial.fields, (), owned).parse(row["energy"], 1),
            _Expressions(initial.fields, (), owned).parse(row["momentum"], 3),
        )
    return ConservationDefinition(
        _text(obj["name"], "conservation.name"),
        _text(obj["energy_units"], "energy_units"),
        _text(obj["momentum_units"], "momentum_units"),
        tuple(measurements),
        spatial,
    )


def _validate_conversions(initial: InitialState) -> None:
    for rule in initial.interactions:
        if rule.output_types is None and not rule.outputs:
            continue
        if initial.schema_version != 1:
            raise ValueError("conversion requires schema_version 1")
        kinds = (
            {rule.left_type, rule.right_type, *rule.output_types}
            if rule.output_types is not None
            else {kind for role in rule.participants for kind in role} | set(rule.outputs)
        )
        if any(
            set((*selected_left_types(c), *selected_right_types(c))) & kinds for c in initial.couplings
        ):
            raise ValueError("conversion types cannot participate in exchange couplings")
        spatial_types = selected_type_set(
            initial.emissions, initial.spatial_couplings, initial.spatial_interactions
        )
        if spatial_types & kinds:
            raise ValueError("conversion types cannot participate in spatial responses or emission")


def load_initial_state(path: Path) -> InitialState:
    """Read a strict JSON initialization file and parse its generic definitions."""
    return parse_initial_json(path.read_bytes())


def parse_initial_json(source: str | bytes) -> InitialState:
    """Parse strict JSON and validate its generic initialization definitions."""
    return parse_initial_state(parse_json_document(source))
