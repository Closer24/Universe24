"""Prepared execution of immutable local laws, with no cached physical inputs."""

from collections.abc import Callable
from threading import Lock

from event_universe.core.disturbance_state import CostMeter, Expression, Values, unpack
from event_universe.core.integer import checked_sum, checked_work, cross_product, dot_product

from .ratios import PROJECTIONS, evaluate_ratio, project

type Components = tuple[int, ...]
type Inputs = tuple[Values, Values, CostMeter, Values, tuple[Values, ...], tuple[Values, ...]]
type Execution = Callable[[Inputs], Components]
type Unary = Callable[[Components], Components]
type Binary = Callable[[Components, Components], Components]

# Host metadata only: roots keep identity keys alive; closures retain only law data.
# Eviction changes preparation work, never results, errors, or charged model work.
_PLAN_LIMIT = 1024
_plans: dict[int, tuple[Expression, Execution]] = {}
_plan_lock = Lock()


def _broadcast(left: Components, right: Components) -> tuple[Components, Components]:
    size = max(len(left), len(right))
    if len(left) not in (1, size) or len(right) not in (1, size):
        raise ValueError("incompatible expression component counts")
    return left * size if len(left) == 1 else left, right * size if len(right) == 1 else right


def _add(a: int, b: int) -> int:
    return checked_work(a + b)


def _sub(a: int, b: int) -> int:
    return checked_work(a - b)


def _mul(a: int, b: int) -> int:
    return checked_work(a * b)


def _exact_div(a: int, b: int) -> int:
    if b == 0 or a % b:
        raise ValueError("exact_div requires a nonzero divisor and an exact integer result")
    return checked_work(a // b)


def _negative(values: Components) -> Components:
    return tuple(checked_work(-value) for value in values)


def _absolute(values: Components) -> Components:
    return tuple(checked_work(abs(value)) for value in values)


def _sum(values: Components) -> Components:
    return (checked_sum(values),)


def _dot(left: Components, right: Components) -> Components:
    return (dot_product(left, right),)


def _equal(left: Components, right: Components) -> Components:
    return (int(left[0] == right[0]),)


def _greater(left: Components, right: Components) -> Components:
    return (1 if left[0] > right[0] else 0,)


def _all_arguments(
    arguments: tuple[Execution, ...], operation: Callable[[tuple[Components, ...]], Components]
) -> Execution:
    def execute(inputs: Inputs) -> Components:
        inputs[2].charge("evaluate")
        return operation(tuple(argument(inputs) for argument in arguments))

    return execute


def _unary(arguments: tuple[Execution, ...], operation: Unary) -> Execution:
    if len(arguments) != 1:
        return _all_arguments(arguments, lambda operands: operation(operands[0]))
    argument = arguments[0]

    def execute(inputs: Inputs) -> Components:
        inputs[2].charge("evaluate")
        return operation(argument(inputs))

    return execute


def _binary(arguments: tuple[Execution, ...], operation: Binary) -> Execution:
    if len(arguments) != 2:
        return _all_arguments(arguments, lambda operands: operation(operands[0], operands[1]))
    first, second = arguments

    def execute(inputs: Inputs) -> Components:
        inputs[2].charge("evaluate")
        return operation(first(inputs), second(inputs))

    return execute


def _componentwise(operation: Callable[[int, int], int]) -> Binary:
    def apply(left: Components, right: Components) -> Components:
        first, second = _broadcast(left, right)
        return tuple(operation(a, b) for a, b in zip(first, second, strict=True))

    return apply


def _prepare(expression: Expression) -> Execution:
    """Select operators once; every execution still charges before its children."""
    op = expression.op
    if op == "literal":
        literal = expression.literal

        def literal_value(inputs: Inputs) -> Components:
            inputs[2].charge("evaluate")
            return literal

        return literal_value
    if op == "field":
        side, field = expression.side, expression.field

        def field_value(inputs: Inputs) -> Components:
            inputs[2].charge("evaluate")
            return unpack((inputs[0] if side == 0 else inputs[1])[field])

        return field_value
    if op == "flux":
        field = expression.field

        def flux_value(inputs: Inputs) -> Components:
            inputs[2].charge("evaluate")
            if not inputs[3]:
                raise ValueError("spatial flux requires an explicitly supplied local sample")
            return unpack(inputs[3][field])

        return flux_value
    if op in ("received", "outgoing"):
        port, field = expression.port, expression.field

        def directional_value(inputs: Inputs) -> Components:
            inputs[2].charge("evaluate")
            channels = inputs[4] if op == "received" else inputs[5]
            if len(channels) != 6 or not 0 <= port < 6:
                raise ValueError(
                    "directional expressions require six explicitly supplied local channels"
                )
            return unpack(channels[port][field])

        return directional_value
    if op in PROJECTIONS:

        def rational_value(inputs: Inputs) -> Components:
            left, right, meter, fluxes, ports, outgoing = inputs
            meter.charge("evaluate")
            values = evaluate_ratio(
                expression.arguments[0], left, right, meter, fluxes, ports=ports, outgoing=outgoing
            )
            return project(op, values)

        return rational_value
    arguments = tuple(_prepare(arg) for arg in expression.arguments)
    if op in ("neg", "abs", "sum"):
        return _unary(arguments, {"neg": _negative, "abs": _absolute, "sum": _sum}[op])
    if op == "component":
        component = expression.component
        return _unary(arguments, lambda values: (values[component],))
    if op == "transform":
        matrix = expression.matrix
        return _unary(arguments, lambda values: tuple(dot_product(row, values) for row in matrix))
    if op == "vector":

        def vector_value(inputs: Inputs) -> Components:
            inputs[2].charge("evaluate")
            operands = tuple(argument(inputs) for argument in arguments)
            return tuple(operand[0] for operand in operands)

        return vector_value
    if op in ("dot", "cross", "eq", "gt"):
        binary: Binary = {"dot": _dot, "cross": cross_product, "eq": _equal, "gt": _greater}[op]
        return _binary(arguments, binary)
    components: dict[str, Callable[[int, int], int]] = {
        "add": _add,
        "sub": _sub,
        "mul": _mul,
        "min": min,
        "max": max,
        "exact_div": _exact_div,
    }
    if op in components:
        return _binary(arguments, _componentwise(components[op]))

    def unknown(inputs: Inputs) -> Components:
        inputs[2].charge("evaluate")
        operands = tuple(argument(inputs) for argument in arguments)
        first, second = _broadcast(operands[0], operands[1])
        for _ in zip(first, second, strict=True):
            raise ValueError(f"unknown expression operation: {op}")
        return ()

    return unknown


def evaluate(
    expression: Expression,
    left: Values,
    right: Values,
    meter: CostMeter,
    spatial_fluxes: Values = (),
    *,
    ports: tuple[Values, ...] = (),
    outgoing: tuple[Values, ...] = (),
) -> Components:
    """Evaluate a validated local law through its bounded, identity-keyed host plan."""
    key = id(expression)
    cached = _plans.get(key)
    if cached is None:
        execution = _prepare(expression)
        # Only insertion/eviction needs coordination; execution uses immutable plans.
        with _plan_lock:
            if key not in _plans and len(_plans) >= _PLAN_LIMIT:
                _plans.pop(next(iter(_plans)))
            _plans[key] = expression, execution
    else:
        execution = cached[1]
    return execution((left, right, meter, spatial_fluxes, ports, outgoing))
