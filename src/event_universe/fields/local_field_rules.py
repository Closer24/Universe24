"""Atomic local field proposals using retained stock and configured causal channels."""

from dataclasses import replace

from event_universe.core.disturbance_state import CostMeter, FieldDefinition, Values, pack, unpack
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    NodeFieldRuleDefinition,
    SpatialFieldDefinition,
    SpatialState,
    validate_port_count,
)
from event_universe.core.validation import ValidationMeter

from .disturbances import evaluate


def received_values(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    states: tuple[SpatialState, ...],
    port_count: int = 6,
) -> tuple[Values, ...]:
    """Project existing delivered samples by travel port, without creating inventory."""
    validate_port_count(port_count)
    zero = tuple(pack((0,) * field.components) for field in fields)
    channels = [list(zero) for _ in range(port_count)]
    for definition, state in zip(definitions, states, strict=True):
        state.validate(fields[definition.field].components, port_count)
        for port, payload in enumerate(state.delivered):
            channels[port][definition.field] = payload
    return tuple(tuple(channel) for channel in channels)


def _stock(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    states: tuple[SpatialState, ...],
    meter: CostMeter,
    port_count: int,
) -> Values:
    # Signed work integers permit a baseline to offset a larger octant total.
    values = [(0,) * field.components for field in fields]
    for definition, state in zip(definitions, states, strict=True):
        field = fields[definition.field]
        state.validate(field.components, port_count)
        total = [0] * field.components
        for payload in state.populations:
            meter.charge("read")
            field.validate(payload)
            for component, amount in enumerate(unpack(payload)):
                total[component] = checked_work(total[component] + amount)
                meter.charge("evaluate")
        values[definition.field] = tuple(total)
    return tuple(values)


def _observable(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    stock: Values,
    meter: CostMeter,
) -> Values:
    values = [pack((0,) * field.components) for field in fields]
    for definition in definitions:
        field = fields[definition.field]
        values[definition.field] = pack(
            tuple(
                checked_work(baseline + amount)
                for baseline, amount in zip(
                    unpack(definition.baseline), stock[definition.field], strict=True
                )
            )
        )
        meter.charge("read")
        meter.charge("evaluate", field.components)
        field.validate(values[definition.field])
    return tuple(values)


def _total(stock: Values, outgoing: tuple[Values, ...], index: int) -> tuple[int, ...]:
    result = list(stock[index])
    for channel in outgoing:
        for component, amount in enumerate(unpack(channel[index])):
            result[component] = checked_work(result[component] + amount)
    return tuple(result)


def apply_field_rules(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    rules: tuple[NodeFieldRuleDefinition, ...],
    states: tuple[SpatialState, ...],
    meter: CostMeter,
    port_count: int = 6,
) -> tuple[tuple[SpatialState, ...], tuple[Values, ...]]:
    """Replace local retained stock and outgoing buffers from frozen rule inputs.

    Field references read baseline plus retained stock. A retained assignment
    writes dynamic stock only; it never replaces or spends the immutable baseline.
    Each incoming channel is a readonly projection of already received inventory.
    """
    validate_port_count(port_count)
    checks = ValidationMeter(meter.definitions)
    zero = tuple(pack((0,) * field.components) for field in fields)
    outgoing: tuple[Values, ...] = (zero,) * port_count
    stock = _stock(fields, definitions, states, meter, port_count)
    ports = received_values(fields, definitions, states, port_count)
    local_fields = tuple(d.field for d in definitions if d.transport == "local")
    active = any(any(stock[index]) for index in local_fields) or any(
        any(unpack(payload)) for channel in ports for payload in channel
    )
    # Baseline alone does not activate empty space or create undeclared sources.
    if active:
        for rule in rules:
            right = _observable(fields, definitions, stock, meter)
            meter.charge("read", port_count * len(definitions))
            if (
                rule.when is not None
                and evaluate(rule.when, zero, right, meter, ports=ports, outgoing=outgoing)[0] <= 0
            ):
                continue
            before = tuple(
                evaluate(invariant.expression, zero, right, checks, ports=ports, outgoing=outgoing)
                for invariant in rule.invariants
            )
            proposed_stock = list(stock)
            proposed_outgoing = [list(channel) for channel in outgoing]
            for assignment in rule.assignments:
                if assignment.field not in local_fields or not -1 <= assignment.port < port_count:
                    raise ValueError(
                        "field rules can write only local stock or configured outgoing buffers"
                    )
                value = pack(
                    evaluate(assignment.expression, zero, right, meter, ports=ports, outgoing=outgoing)
                )
                fields[assignment.field].validate(value)
                meter.charge("update", fields[assignment.field].components)
                if assignment.port == -1:
                    proposed_stock[assignment.field] = unpack(value)
                else:
                    proposed_outgoing[assignment.port][assignment.field] = value
            next_stock = tuple(proposed_stock)
            next_outgoing = tuple(tuple(channel) for channel in proposed_outgoing)
            next_right = _observable(fields, definitions, next_stock, meter)
            for index, field in enumerate(fields):
                if field.conserved:
                    if _total(stock, outgoing, index) != _total(next_stock, next_outgoing, index):
                        raise ValueError(f"field rule {rule.name} violates conservation of {field.name}")
            for invariant, expected in zip(rule.invariants, before, strict=True):
                actual = evaluate(
                    invariant.expression, zero, next_right, checks, ports=ports, outgoing=next_outgoing
                )
                if actual != expected:
                    raise ValueError(f"field rule {rule.name} violates invariant {invariant.name}")
            stock, outgoing = next_stock, next_outgoing
    result = []
    for definition, state in zip(definitions, states, strict=True):
        if definition.transport == "local":
            blank = zero[definition.field]
            state = replace(state, populations=(pack(stock[definition.field]),) + (blank,) * 7)
            meter.charge("update", fields[definition.field].components)
        result.append(state)
    return tuple(result), outgoing
