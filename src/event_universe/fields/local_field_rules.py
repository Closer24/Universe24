"""Atomic local field proposals using retained stock and six causal input channels."""

from dataclasses import replace

from event_universe.core.disturbance_state import (
    MAX_EXPRESSION_NODES,
    MAX_RULES,
    CostMeter,
    Expression,
    FieldDefinition,
    OperationCosts,
    Values,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    FieldRuleGuard,
    NodeFieldRuleDefinition,
    SpatialFieldDefinition,
    SpatialPlan,
    SpatialState,
)
from event_universe.core.validation import ValidationMeter

from .disturbances import evaluate


def received_values(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    states: tuple[SpatialState, ...],
) -> tuple[Values, ...]:
    """Project existing delivered samples by travel port, without creating inventory."""
    zero = tuple(pack((0,) * field.components) for field in fields)
    channels = [list(zero) for _ in range(6)]
    for definition, state in zip(definitions, states, strict=True):
        for port, payload in enumerate(state.delivered):
            channels[port][definition.field] = payload
    return tuple(tuple(channel) for channel in channels)


def received_masks(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    states: tuple[SpatialState, ...],
) -> tuple[int, ...]:
    """Project per-field port presence, including delivered zero-valued packets."""
    result = [0] * len(fields)
    for definition, state in zip(definitions, states, strict=True):
        state.validate(fields[definition.field].components)
        result[definition.field] = state.received_mask
    return tuple(result)


def _stock(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    states: tuple[SpatialState, ...],
    meter: CostMeter,
) -> Values:
    # Signed work integers permit a baseline to offset a larger octant total.
    values = [(0,) * field.components for field in fields]
    for definition, state in zip(definitions, states, strict=True):
        field = fields[definition.field]
        state.validate(field.components)
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


def _validate_guard_expression(expression: Expression, *, persistent: bool) -> None:
    pending = [expression]
    visited = 0
    forbidden = {"received", "received_present", "flux"}
    if persistent:
        forbidden.add("outgoing")
    while pending:
        current = pending.pop()
        visited += 1
        if type(current) is not Expression or type(current.arguments) is not tuple:
            raise ValueError("field guard requires immutable expression metadata")
        if visited + len(pending) + len(current.arguments) > MAX_EXPRESSION_NODES:
            raise ValueError("field guard expression exceeds the bounded expression size")
        if current.op in forbidden:
            raise ValueError("field guard cannot read transient inputs or unavailable outputs")
        pending.extend(current.arguments)


def _check_invariants(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    rule: NodeFieldRuleDefinition,
    stock: Values,
    outgoing: tuple[Values, ...],
    next_stock: Values,
    next_outgoing: tuple[Values, ...],
    meter: CostMeter,
) -> None:
    zero = tuple(pack((0,) * field.components) for field in fields)
    right = _observable(fields, definitions, stock, meter)
    next_right = _observable(fields, definitions, next_stock, meter)
    for index, field in enumerate(fields):
        if field.conserved and _total(stock, outgoing, index) != _total(
            next_stock, next_outgoing, index
        ):
            raise ValueError(f"field rule {rule.name} violates conservation of {field.name}")
    for invariant in rule.invariants:
        _validate_guard_expression(invariant.expression, persistent=False)
        expected = evaluate(invariant.expression, zero, right, meter, outgoing=outgoing)
        actual = evaluate(invariant.expression, zero, next_right, meter, outgoing=next_outgoing)
        if actual != expected:
            raise ValueError(f"field rule {rule.name} violates invariant {invariant.name}")


def _commit_allowed(rule: NodeFieldRuleDefinition, right: Values, meter: CostMeter) -> bool:
    if rule.commit_when is None:
        return True
    _validate_guard_expression(rule.commit_when, persistent=True)
    zero = tuple(pack((0,) * len(value)) for value in right)
    return evaluate(rule.commit_when, zero, right, meter)[0] > 0


def validate_field_guards(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    rules: tuple[NodeFieldRuleDefinition, ...],
    states: tuple[SpatialState, ...],
    plan: SpatialPlan,
    costs: OperationCosts,
) -> None:
    """Check frozen substeps on current local stock without rerunning assignments."""
    if type(plan.field_guards) is not tuple or len(plan.field_guards) > MAX_RULES:
        raise ValueError("field guard metadata exceeds the fixed rule capacity")
    if type(plan.outgoing) is not tuple or len(plan.outgoing) != 6:
        raise ValueError("field guard proposal requires six immutable outgoing channels")
    for bundle in plan.outgoing:
        if type(bundle) is not tuple or len(bundle) != len(definitions):
            raise ValueError("field guard proposal has an incompatible spatial layout")
        for definition, populations in zip(definitions, bundle, strict=True):
            if type(populations) is not tuple or len(populations) != 8:
                raise ValueError("field guard proposal requires eight immutable populations")
            for payload in populations:
                fields[definition.field].validate(payload)
    checks = ValidationMeter(costs)
    zero = tuple(pack((0,) * field.components) for field in fields)
    outgoing: tuple[Values, ...] = (zero,) * 6
    stock = _stock(fields, definitions, states, checks)
    local_fields = {d.field for d in definitions if d.transport == "local"}
    previous = -1
    duration = 0
    for guard in plan.field_guards:
        if (
            type(guard) is not FieldRuleGuard
            or type(guard.rule_index) is not int
            or not previous < guard.rule_index < len(rules)
        ):
            raise ValueError("field guards require ordered distinct configured rule indices")
        previous = guard.rule_index
        rule = rules[guard.rule_index]
        duration = checked_work(duration + rule.k)
        if type(guard.delta) is not tuple or len(guard.delta) != len(fields):
            raise ValueError("field guard delta has an incompatible field layout")
        next_stock = []
        for index, (field, current, delta) in enumerate(zip(fields, stock, guard.delta, strict=True)):
            if type(delta) is not tuple or len(delta) != field.components:
                raise ValueError("field guard delta has an incompatible component layout")
            for amount in delta:
                checked_work(amount)
            if index not in local_fields and any(delta):
                raise ValueError("field guard delta can change only local spatial fields")
            next_stock.append(tuple(checked_work(a + b) for a, b in zip(current, delta, strict=True)))
        if type(guard.outgoing) is not tuple or len(guard.outgoing) != 6:
            raise ValueError("field guard requires six immutable outgoing channels")
        for channel in guard.outgoing:
            if type(channel) is not tuple or len(channel) != len(fields):
                raise ValueError("field guard outgoing has an incompatible field layout")
            for index, (field, payload) in enumerate(zip(fields, channel, strict=True)):
                if type(payload) is not tuple:
                    raise ValueError("field guard requires immutable outgoing components")
                field.validate(payload)
                if index not in local_fields and any(unpack(payload)):
                    raise ValueError("field guards can output only local spatial fields")
        right = _observable(fields, definitions, stock, checks)
        if not _commit_allowed(rule, right, checks):
            raise ValueError(f"field rule {rule.name} violates commit_when")
        _check_invariants(
            fields, definitions, rule, stock, outgoing, tuple(next_stock), guard.outgoing, checks
        )
        stock, outgoing = tuple(next_stock), guard.outgoing
    if duration != plan.interaction_ticks:
        raise ValueError("field guard duration differs from the frozen proposal")
    proposed = _stock(fields, definitions, plan.states, checks)
    for spatial_index, definition in enumerate(definitions):
        if definition.transport != "local":
            continue
        index = definition.field
        if stock[index] != proposed[index]:
            raise ValueError("field guard deltas differ from the proposed local stock")
        for port, bundle in enumerate(plan.outgoing):
            amounts = [0] * fields[index].components
            for payload in bundle[spatial_index]:
                for component, value in enumerate(unpack(payload)):
                    amounts[component] = checked_work(amounts[component] + value)
            if tuple(amounts) != unpack(outgoing[port][index]):
                raise ValueError("field guard outputs differ from the proposed outgoing stock")


def apply_field_rules(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    rules: tuple[NodeFieldRuleDefinition, ...],
    states: tuple[SpatialState, ...],
    meter: CostMeter,
    *,
    guards: list[FieldRuleGuard] | None = None,
) -> tuple[tuple[SpatialState, ...], tuple[Values, ...]]:
    """Replace local retained stock and outgoing buffers from frozen rule inputs.

    Field references read baseline plus retained stock. A retained assignment
    writes dynamic stock only; it never replaces or spends the immutable baseline.
    Each incoming channel is a readonly projection of already received inventory.
    """
    checks = ValidationMeter(meter.definitions)
    zero = tuple(pack((0,) * field.components) for field in fields)
    outgoing: tuple[Values, ...] = (zero,) * 6
    stock = _stock(fields, definitions, states, meter)
    ports = received_values(fields, definitions, states)
    masks = received_masks(fields, definitions, states)
    local_fields = tuple(d.field for d in definitions if d.transport == "local")
    active = (
        any(masks)
        or any(any(stock[index]) for index in local_fields)
        or any(any(unpack(payload)) for channel in ports for payload in channel)
    )
    # Baseline alone does not activate empty space or create undeclared sources.
    if active:
        for rule_index, rule in enumerate(rules):
            right = _observable(fields, definitions, stock, meter)
            meter.charge("read", 6 * len(definitions))
            if (
                rule.when is not None
                and evaluate(
                    rule.when, zero, right, meter, ports=ports, outgoing=outgoing, received_masks=masks
                )[0]
                <= 0
            ):
                continue
            if not _commit_allowed(rule, right, checks):
                continue
            meter.advance(rule.k)
            proposed_stock = list(stock)
            proposed_outgoing = [list(channel) for channel in outgoing]
            for assignment in rule.assignments:
                if assignment.field not in local_fields or not -1 <= assignment.port < 6:
                    raise ValueError(
                        "field rules can write only local stock or its six outgoing buffers"
                    )
                value = pack(
                    evaluate(
                        assignment.expression,
                        zero,
                        right,
                        meter,
                        ports=ports,
                        outgoing=outgoing,
                        received_masks=masks,
                    )
                )
                fields[assignment.field].validate(value)
                meter.charge("update", fields[assignment.field].components)
                if assignment.port == -1:
                    proposed_stock[assignment.field] = unpack(value)
                else:
                    proposed_outgoing[assignment.port][assignment.field] = value
            next_stock = tuple(proposed_stock)
            next_outgoing = tuple(tuple(channel) for channel in proposed_outgoing)
            _observable(fields, definitions, next_stock, meter)
            _check_invariants(
                fields, definitions, rule, stock, outgoing, next_stock, next_outgoing, checks
            )
            if guards is not None:
                guards.append(
                    FieldRuleGuard(
                        rule_index,
                        tuple(
                            tuple(checked_work(b - a) for a, b in zip(old, new, strict=True))
                            for old, new in zip(stock, next_stock, strict=True)
                        ),
                        next_outgoing,
                    )
                )
            stock, outgoing = next_stock, next_outgoing
    result = []
    for definition, state in zip(definitions, states, strict=True):
        if definition.transport == "local":
            blank = zero[definition.field]
            state = replace(state, populations=(pack(stock[definition.field]),) + (blank,) * 7)
            meter.charge("update", fields[definition.field].components)
        result.append(state)
    return tuple(result), outgoing
