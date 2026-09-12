"""Exact host-side calibration, authoring conversion and dimensional validation.

Fractions exist only during preparation and validation. Physical expressions and
their stored values are not converted, rewritten or evaluated by this module.
"""

from fractions import Fraction
from typing import cast

from .core.disturbance_state import (
    MAX_VALUE,
    Expression,
    FieldDefinition,
    InitialState,
    InteractionDefinition,
)
from .core.spatial_state import NodeFieldRuleDefinition, SpatialInteractionDefinition
from .core.unit_state import UnitDefinition, UnitSystem

DIMENSION_ORDER = ("length", "mass", "time", "current", "temperature", "amount", "luminous_intensity")
DIMENSIONLESS = (0,) * 7
MAX_UNITS = 64
MAX_RATIO_BITS = 256
MAX_DIMENSION_EXPONENT = 16
Dimension = tuple[int, ...]
ExactValue = int | Fraction


def _object(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} requires exactly these keys: {', '.join(sorted(keys))}")
    return cast(dict[str, object], value)


def _ratio(value: object, label: str, *, immutable: bool = False) -> tuple[int, int]:
    expected = tuple if immutable else list
    if type(value) is not expected or len(cast(list[object], value)) != 2:
        raise ValueError(f"{label} requires a numerator/denominator pair")
    pair = cast(tuple[int, int], value)
    if any(type(n) is not int or n <= 0 or n.bit_length() > MAX_RATIO_BITS for n in pair):
        raise ValueError(f"{label} requires positive integers of at most {MAX_RATIO_BITS} bits")
    result = Fraction(*pair)
    return result.numerator, result.denominator


def _dimension(value: object, *, immutable: bool = False) -> Dimension:
    expected = tuple if immutable else list
    if type(value) is not expected or len(cast(list[object], value)) != 7:
        raise ValueError("unit dimensions require seven integer exponents")
    items = cast(tuple[int, ...], value)
    if any(type(n) is not int or abs(n) > MAX_DIMENSION_EXPONENT for n in items):
        raise ValueError("unit dimension exponents must be integers from -16 through 16")
    return tuple(items)


def parse_unit_system(raw: object) -> UnitSystem:
    """Parse explicit rational SI calibration without any implicit named units."""
    obj = _object(raw, {"model_id", "base_scales", "units"}, "unit_system")
    if obj["model_id"] != "si-rational-v1":
        raise ValueError("unit_system requires model_id si-rational-v1")
    bases = obj["base_scales"]
    if not isinstance(bases, list) or len(bases) != 7:
        raise ValueError("unit_system.base_scales requires seven SI ratio pairs")
    definitions = obj["units"]
    if not isinstance(definitions, list) or not 1 <= len(definitions) <= MAX_UNITS:
        raise ValueError("unit_system.units requires 1 through 64 definitions")
    units = []
    for raw_unit in definitions:
        item = _object(raw_unit, {"name", "dimensions", "si_scale"}, "unit definition")
        name = item["name"]
        if not isinstance(name, str) or not name.strip() or len(name) > 128:
            raise ValueError("unit name must be a nonempty string of at most 128 characters")
        units.append(
            UnitDefinition(name, _dimension(item["dimensions"]), _ratio(item["si_scale"], name))
        )
    result = UnitSystem(tuple(_ratio(v, "base scale") for v in bases), tuple(units))
    _registry(result)
    return result


def _registry(system: UnitSystem) -> dict[str, UnitDefinition]:
    """Revalidate typed API/checkpoint objects, not only their JSON origin."""
    if not isinstance(system, UnitSystem) or system.model_id != "si-rational-v1":
        raise ValueError("unsupported immutable unit system")
    if type(system.base_scales) is not tuple or len(system.base_scales) != 7:
        raise ValueError("unit system requires seven immutable base scales")
    for scale in system.base_scales:
        _ratio(scale, "base scale", immutable=True)
    if type(system.units) is not tuple or not 1 <= len(system.units) <= MAX_UNITS:
        raise ValueError("unit system requires 1 through 64 immutable units")
    result = {}
    for unit in system.units:
        if not isinstance(unit, UnitDefinition):
            raise ValueError("unit registry contains an invalid definition")
        if not isinstance(unit.name, str) or not unit.name.strip() or len(unit.name) > 128:
            raise ValueError("unit name must be a nonempty string of at most 128 characters")
        if unit.name in result:
            raise ValueError(f"duplicate unit name {unit.name!r}")
        _dimension(unit.dimensions, immutable=True)
        _ratio(unit.si_scale, unit.name, immutable=True)
        result[unit.name] = unit
    return result


def _unit(name: str, registry: dict[str, UnitDefinition]) -> UnitDefinition:
    if name not in registry:
        raise ValueError(f"unknown unit label {name!r}")
    return registry[name]


def _exact(value: ExactValue) -> Fraction:
    if type(value) is not int and type(value) is not Fraction:
        raise ValueError("authoring values require exact integers or Fraction values")
    return Fraction(value)


def convert_value(value: ExactValue, from_unit: str, to_unit: str, system: UnitSystem) -> Fraction:
    """Convert a scalar exactly; registry unit names have no built-in meanings."""
    registry = _registry(system)
    source, target = _unit(from_unit, registry), _unit(to_unit, registry)
    if source.dimensions != target.dimensions:
        raise ValueError("cannot convert values between different dimensions")
    return _exact(value) * Fraction(*source.si_scale) / Fraction(*target.si_scale)


def encode_field_value(
    value: ExactValue, from_unit: str, field: FieldDefinition, system: UnitSystem
) -> int:
    """Return one external JSON component, rejecting rounding and register overflow."""
    _field_dimensions((field,), system)
    converted = convert_value(value, from_unit, field.units, system) * field.scale
    if converted.denominator != 1:
        raise ValueError("converted value is not an exact integer field quantum")
    result = converted.numerator
    if abs(result) > MAX_VALUE or (result < 0 and not field.signed):
        raise ValueError("converted value exceeds the field register or sign bound")
    return result


def _field_dimensions(fields: tuple[FieldDefinition, ...], system: UnitSystem) -> tuple[Dimension, ...]:
    registry = _registry(system)
    dimensions = []
    for field in fields:
        unit = _unit(field.units, registry)
        if type(field.scale) is not int or not 1 <= field.scale <= MAX_VALUE:
            raise ValueError(f"invalid scale for field {field.name}")
        quantum = Fraction(1)
        for base, exponent in zip(system.base_scales, unit.dimensions, strict=True):
            quantum *= Fraction(*base) ** exponent
        if Fraction(*unit.si_scale) / field.scale != quantum:
            raise ValueError(f"field {field.name} does not use the coherent quantum for its dimensions")
        dimensions.append(unit.dimensions)
    return tuple(dimensions)


def _same(first: Dimension | None, second: Dimension | None, context: str) -> Dimension | None:
    if first is None:
        return second
    if second is None:
        return first
    if first != second:
        raise ValueError(f"dimension mismatch in {context}: {first} versus {second}")
    return first


class _Dimensions:
    def __init__(self, fields: tuple[Dimension, ...], port_count: int) -> None:
        self.fields = fields
        self.limit = max(64, 8 * port_count + 16)
        self.nodes = 0

    def infer(self, expression: Expression, *, invariant: bool = False) -> Dimension | None:
        self.nodes = 0
        return self._node(expression, 1, invariant)

    def _node(self, expression: Expression, depth: int, key_allowed: bool = False) -> Dimension | None:
        self.nodes += 1
        if not isinstance(expression, Expression) or self.nodes > self.limit or depth > 16:
            raise ValueError("dimensional expression exceeds its fixed syntax bounds")
        op = expression.op
        if op in ("field", "received", "outgoing", "flux"):
            if type(expression.field) is not int or not 0 <= expression.field < len(self.fields):
                raise ValueError("dimensional expression references an unknown field")
            return self.fields[expression.field]
        if op == "literal":
            if not expression.literal or any(type(v) is not int for v in expression.literal):
                raise ValueError("dimensional literals require integer components")
            return DIMENSIONLESS if any(expression.literal) else None
        arities = {
            **dict.fromkeys(
                ("add", "sub", "mul", "dot", "cross", "exact_div", "ratio", "min", "max", "gt", "eq"), 2
            ),
            **dict.fromkeys(
                (
                    "neg",
                    "abs",
                    "sum",
                    "component",
                    "transform",
                    "rational_whole",
                    "rational_remainder",
                    "rational_numerator",
                    "rational_denominator",
                    "rational_direction",
                    "rational_key",
                    "rational_floor",
                ),
                1,
            ),
            "vector": 3,
        }
        if op not in arities or len(expression.arguments) != arities[op]:
            raise ValueError(f"dimensional validation does not support operation {op!r}")
        if op == "rational_key" and not key_allowed:
            raise ValueError("rational_key is only dimensionally valid as an invariant root")
        args = tuple(self._node(arg, depth + 1) for arg in expression.arguments)
        if op in ("add", "sub", "min", "max", "gt", "eq"):
            result = _same(args[0], args[1], op)
            return DIMENSIONLESS if op in ("gt", "eq") else result
        if op == "vector":
            return _same(_same(args[0], args[1], op), args[2], op)
        if op in ("mul", "dot", "cross"):
            if args[0] is None or args[1] is None:
                return None
            return tuple(a + b for a, b in zip(args[0], args[1], strict=True))
        if op in ("exact_div", "ratio"):
            if args[1] is None:
                raise ValueError("dimensional expression has an identically zero denominator")
            if args[0] is None:
                return None
            return tuple(a - b for a, b in zip(args[0], args[1], strict=True))
        if op in ("rational_direction", "rational_denominator"):
            return DIMENSIONLESS
        return args[0]

    def require(self, expression: Expression, expected: Dimension, context: str) -> None:
        _same(self.infer(expression), expected, context)


def _rule_dimensions(
    rule: InteractionDefinition | NodeFieldRuleDefinition | SpatialInteractionDefinition,
    analyzer: _Dimensions,
) -> None:
    if rule.when is not None:
        analyzer.require(rule.when, DIMENSIONLESS, f"condition of {rule.name}")
    for assignment in rule.assignments:
        analyzer.require(
            assignment.expression, analyzer.fields[assignment.field], f"assignment in {rule.name}"
        )
    for invariant in rule.invariants:
        analyzer.infer(invariant.expression, invariant=True)


def validate_units(initial: InitialState) -> None:
    """Validate all active parsed law contexts when calibration is explicitly enabled."""
    system = initial.unit_system
    if system is None:
        return
    dimensions = _field_dimensions(initial.fields, system)
    analyzer = _Dimensions(dimensions, initial.topology.degree)
    if initial.event_program is not None:
        from .integration.event_program import parse_event_program

        program = parse_event_program(initial)
        if any(dimensions[binding.field] != DIMENSIONLESS for binding in program.bindings):
            raise ValueError("native event outcome fields must be dimensionless control codes")
    for kind in initial.disturbances:
        for update in kind.updates:
            analyzer.require(update.expression, dimensions[update.field], f"update of {kind.name}")
        for check in kind.checks:
            analyzer.require(check.expression, DIMENSIONLESS, f"check {check.name}")
        if kind.cost_field is not None and dimensions[kind.cost_field] != DIMENSIONLESS:
            raise ValueError("modeled cost fields must be dimensionless in strict unit mode")
        movement = kind.transport
        if movement.direction is not None:
            analyzer.infer(movement.direction)
        if movement.rate is not None:
            rate = analyzer.infer(movement.rate)
            divisor = (
                DIMENSIONLESS if movement.rate_divisor is None else analyzer.infer(movement.rate_divisor)
            )
            if divisor is None:
                raise ValueError("unit-checked movement divisor cannot be identically zero")
            _same(rate, divisor, f"dimensionless movement rate of {kind.name}")
        elif movement.rate_divisor is not None:
            raise ValueError("unit-checked movement divisor requires a rate")
    for coupling in initial.couplings:
        analyzer.require(coupling.amount, dimensions[coupling.field], f"coupling {coupling.name}")
    for emission in initial.emissions:
        target = initial.spatial_fields[emission.spatial_field].field
        analyzer.require(emission.amount, dimensions[target], "emission amount")
    for spatial_coupling in initial.spatial_couplings:
        expected = (
            DIMENSIONLESS if spatial_coupling.mode == "rotation" else dimensions[spatial_coupling.field]
        )
        analyzer.require(
            spatial_coupling.expression, expected, f"spatial coupling {spatial_coupling.name}"
        )
    rules: tuple[InteractionDefinition | NodeFieldRuleDefinition | SpatialInteractionDefinition, ...] = (
        *initial.interactions,
        *initial.field_rules,
        *initial.spatial_interactions,
    )
    for rule in rules:
        _rule_dimensions(rule, analyzer)
