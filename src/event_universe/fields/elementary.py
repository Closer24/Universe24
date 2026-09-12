"""Fixed local component exchange and finite routing; no supplied force expressions."""

from dataclasses import dataclass, replace

from event_universe.core.disturbance_state import (
    Assignment,
    CostMeter,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    Invariant,
    Values,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    ElementaryExchange,
    SpatialInteractionDefinition,
    SpatialState,
)

from .spatial import split_weighted
from .spatial_interactions import JointSpatialCouplingLaw


def remaining(record: DisturbanceRecord, rules: tuple[ElementaryExchange, ...]) -> Values:
    limits = tuple(
        rule.budget if rule.type_index == record.type_index else pack((0,) * len(rule.budget))
        for rule in rules
    )
    values = record.interaction_remaining or limits
    if len(values) != len(limits):
        raise ValueError("elementary exchange allowance has the wrong fixed size")
    for value, limit in zip(values, limits, strict=True):
        if len(value) != len(limit) or any(
            not 0 <= a <= b for a, b in zip(unpack(value), unpack(limit), strict=True)
        ):
            raise ValueError("elementary exchange allowance exceeds its initial bound")
    return values


def exchange_spend(
    record: DisturbanceRecord,
    values: Values,
    rules: tuple[ElementaryExchange, ...],
    index: int,
    meter: CostMeter,
) -> tuple[int, ...] | None:
    rule = rules[index]
    if record.type_index != rule.type_index:
        return None
    budgets = remaining(record, rules)
    local, carried = unpack(values[rule.field]), unpack(record.values[rule.field])
    meter.charge("read", 3 + len(rules))
    meter.charge("evaluate", 3 * len(local))
    if not any(local):
        return None
    spend = tuple(
        abs(checked_work(a - b)) if c in rule.components else 0
        for c, (a, b) in enumerate(zip(local, carried, strict=True))
    )
    if not any(spend) or any(a > b for a, b in zip(spend, unpack(budgets[index]), strict=True)):
        return None
    return tuple(bounded(value) for value in spend)


def exchange_rules(
    rules: tuple[ElementaryExchange, ...], fields: tuple[FieldDefinition, ...]
) -> tuple[SpatialInteractionDefinition, ...]:
    """Build the one fixed operation and its independent sum/norm guards once."""
    result = []
    for rule in rules:
        size = fields[rule.field].components
        left, right = (Expression("field", field=rule.field, side=side) for side in (0, 1))
        assigned = []
        for side in (0, 1):
            if size == 1:
                expression = right if side == 0 else left
            else:
                expression = Expression(
                    "vector",
                    tuple(
                        Expression(
                            "component",
                            (
                                Expression(
                                    "field",
                                    field=rule.field,
                                    side=1 - side if c in rule.components else side,
                                ),
                            ),
                            component=c,
                        )
                        for c in range(size)
                    ),
                )
            assigned.append(Assignment(side, rule.field, expression))
        square_left = Expression("dot" if size == 3 else "mul", (left, left))
        square_right = Expression("dot" if size == 3 else "mul", (right, right))
        result.append(
            SpatialInteractionDefinition(
                rule.name,
                rule.type_index,
                tuple(assigned),
                (
                    Invariant("combined_components", Expression("add", (left, right))),
                    Invariant("combined_squared_norm", Expression("add", (square_left, square_right))),
                ),
            )
        )
    return tuple(result)


@dataclass(frozen=True, slots=True)
class ElementarySpatialCouplingLaw(JointSpatialCouplingLaw):
    exchanges: tuple[ElementaryExchange, ...] = ()

    def _activate(
        self, index: int, record: DisturbanceRecord, values: Values, meter: CostMeter
    ) -> DisturbanceRecord | None:
        spend = exchange_spend(record, values, self.exchanges, index, meter)
        if spend is None:
            return None
        budgets = list(remaining(record, self.exchanges))
        budgets[index] = pack(tuple(b - a for a, b in zip(spend, unpack(budgets[index]), strict=True)))
        meter.charge("update", len(spend))
        return replace(record, interaction_remaining=tuple(budgets))


def route_stock(
    state: SpatialState, field: FieldDefinition, weights: tuple[int, ...], meter: CostMeter
) -> tuple[SpatialState, tuple[tuple[tuple[int, ...], ...], ...]]:
    """Partition local stock with bounded carried allocation remainders."""
    total = [0] * field.components
    for payload in state.populations:
        field.validate(payload)
        meter.charge("read")
        for component, amount in enumerate(unpack(payload)):
            total[component] = checked_work(total[component] + amount)
            meter.charge("evaluate")
    total = [bounded(value) for value in total]
    channels = [[0] * field.components for _ in range(6)]
    phases = []
    for component, amount in enumerate(total):
        portions, phase = split_weighted(amount, weights, unpack(state.allocation_phases[0])[component])
        phases.append(phase)
        for port, value in enumerate(portions):
            channels[port][component] = value
        meter.charge("split", 6)
    blank = pack((0,) * field.components)
    next_state = replace(
        state,
        populations=(blank,) * 8,
        allocation_phases=(pack(tuple(phases)),) + (blank,) * 7,
        delivered=(blank,) * 6,
    )
    outgoing = tuple((pack(tuple(channel)),) + (blank,) * 7 for channel in channels)
    meter.charge("route")
    meter.charge("send", sum(any(channel) for channel in channels))
    return next_state, outgoing
