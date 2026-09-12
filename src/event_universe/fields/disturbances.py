"""Bounded local arithmetic for data-defined disturbance evolution and transport."""

from dataclasses import dataclass, replace

from event_universe.core.disturbance_state import (
    CostMeter,
    CouplingDefinition,
    Departure,
    DisturbanceDefinition,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    InteractionDefinition,
    LocalPlan,
    OperationCosts,
    Payload,
    Values,
    Weights,
    bounded,
    decode,
    encode,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work, signed_divrem

from .ratios import PROJECTIONS, evaluate_ratio, project
from .routing import balanced_port, rate_credit
from .spatial import split_weighted


def _dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    total = 0
    for a, b in zip(left, right, strict=True):
        total = checked_work(total + checked_work(a * b))
    return total


def _broadcast(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    size = max(len(left), len(right))
    if len(left) not in (1, size) or len(right) not in (1, size):
        raise ValueError("incompatible expression component counts")
    return left * size if len(left) == 1 else left, right * size if len(right) == 1 else right


def evaluate(
    expression: Expression,
    left: Values,
    right: Values,
    meter: CostMeter,
    spatial_fluxes: Values = (),
    *,
    ports: tuple[Values, ...] = (),
    outgoing: tuple[Values, ...] = (),
) -> tuple[int, ...]:
    """Evaluate a validated, fixed-size integer AST without Python eval or imports."""
    meter.charge("evaluate")
    op = expression.op
    if op in PROJECTIONS:
        values = evaluate_ratio(
            expression.arguments[0], left, right, meter, spatial_fluxes, ports=ports, outgoing=outgoing
        )
        return project(op, values)
    if op == "literal":
        return expression.literal
    if op == "field":
        return unpack((left if expression.side == 0 else right)[expression.field])
    if op == "flux":
        if not spatial_fluxes:
            raise ValueError("spatial flux requires an explicitly supplied local sample")
        return unpack(spatial_fluxes[expression.field])
    if op in ("received", "outgoing"):
        channels = ports if op == "received" else outgoing
        if len(channels) != 6 or not 0 <= expression.port < 6:
            raise ValueError("directional expressions require six explicitly supplied local channels")
        return unpack(channels[expression.port][expression.field])
    operands = tuple(
        evaluate(arg, left, right, meter, spatial_fluxes, ports=ports, outgoing=outgoing)
        for arg in expression.arguments
    )
    if op == "transform":
        return tuple(_dot(row, operands[0]) for row in expression.matrix)
    if op == "dot":
        return (_dot(operands[0], operands[1]),)
    if op == "cross":
        first, second = operands
        return tuple(
            checked_work(checked_work(first[a] * second[b]) - checked_work(first[b] * second[a]))
            for a, b in ((1, 2), (2, 0), (0, 1))
        )
    if op == "vector":
        return tuple(operand[0] for operand in operands)
    if op == "eq":
        return (int(operands[0][0] == operands[1][0]),)
    if op == "gt":
        return (1 if operands[0][0] > operands[1][0] else 0,)
    if op in ("neg", "abs", "sum", "component"):
        unary = operands[0]
        if op == "neg":
            return tuple(checked_work(-v) for v in unary)
        if op == "abs":
            return tuple(checked_work(abs(v)) for v in unary)
        if op == "sum":
            total = 0
            for value in unary:
                total = checked_work(total + value)
            return (total,)
        return (unary[expression.component],)
    first, second = _broadcast(operands[0], operands[1])
    result = []
    for a, b in zip(first, second, strict=True):
        if op == "add":
            value = checked_work(a + b)
        elif op == "sub":
            value = checked_work(a - b)
        elif op == "mul":
            value = checked_work(a * b)
        elif op == "min":
            value = min(a, b)
        elif op == "max":
            value = max(a, b)
        elif op == "exact_div":
            if b == 0 or a % b:
                raise ValueError("exact_div requires a nonzero divisor and an exact integer result")
            value = checked_work(a // b)
        else:
            raise ValueError(f"unknown expression operation: {op}")
        result.append(value)
    return tuple(result)


def add_values(left: Payload, right: Payload) -> Payload:
    if len(left) != len(right):
        raise ValueError("field component mismatch")
    return pack(tuple(checked_work(a + b) for a, b in zip(unpack(left), unpack(right), strict=True)))


def _sum_records(
    records: tuple[DisturbanceRecord | None, ...], fields: tuple[FieldDefinition, ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            checked_work(
                sum(decode(record.values[index][c]) for record in records if record is not None)
            )
            for c in range(field.components)
        )
        for index, field in enumerate(fields)
    )


def _shares(amount: int, weights: Weights, phase: int) -> tuple[tuple[int, ...], int]:
    """Count weighted cyclic intervals in fixed work, including signed amounts."""
    return split_weighted(amount, weights, phase)


def _with_value(record: DisturbanceRecord, index: int, value: Payload) -> DisturbanceRecord:
    values = list(record.values)
    values[index] = value
    return replace(record, values=tuple(values))


@dataclass(frozen=True, slots=True)
class DisturbanceLaw:
    """Pure local proposal: immutable definitions, fixed records and carried phases."""

    fields: tuple[FieldDefinition, ...]
    definitions: tuple[DisturbanceDefinition, ...]
    couplings: tuple[CouplingDefinition, ...]
    operation_costs: OperationCosts
    interactions: tuple[InteractionDefinition, ...] = ()

    def _interact(
        self,
        rule: InteractionDefinition,
        left: DisturbanceRecord,
        right: DisturbanceRecord,
        meter: CostMeter,
    ) -> tuple[DisturbanceRecord, DisturbanceRecord]:
        if rule.when is not None and evaluate(rule.when, left.values, right.values, meter)[0] <= 0:
            return left, right
        meter.charge("couple")
        before = tuple(evaluate(i.expression, left.values, right.values, meter) for i in rule.invariants)
        candidate = [left, right]
        for assignment in rule.assignments:
            meter.charge("update")
            # Every right-hand side reads the same frozen pair, not earlier assignments.
            value = evaluate(assignment.expression, left.values, right.values, meter)
            candidate[assignment.side] = _with_value(
                candidate[assignment.side], assignment.field, pack(value)
            )
        for record in candidate:
            self._validate(record, meter)
        first, second = candidate
        original_totals = _sum_records((left, right), self.fields)
        candidate_totals = _sum_records((first, second), self.fields)
        for index, field in enumerate(self.fields):
            if field.conserved and original_totals[index] != candidate_totals[index]:
                raise ValueError(f"interaction {rule.name} violates conservation of {field.name}")
        for invariant, expected in zip(rule.invariants, before, strict=True):
            if evaluate(invariant.expression, first.values, second.values, meter) != expected:
                raise ValueError(f"interaction {rule.name} violates invariant {invariant.name}")
        return first, second

    def _validate(self, record: DisturbanceRecord, meter: CostMeter) -> None:
        definition = self.definitions[record.type_index]
        if len(record.values) != len(self.fields):
            raise ValueError("record field count differs from the configured schema")
        for index, field in enumerate(self.fields):
            field.validate(record.values[index])
            if index not in definition.fields and any(unpack(record.values[index])):
                raise ValueError("record carries a field absent from its disturbance type")
        for check in definition.checks:
            if evaluate(check.expression, record.values, record.values, meter)[0] <= 0:
                raise ValueError(f"local check {check.name} failed")
        if record.exchange_remainders:
            if len(record.exchange_remainders) != len(self.couplings):
                raise ValueError("carried exchange state must match the fixed coupling rules")
            for coupling, payload in zip(self.couplings, record.exchange_remainders, strict=True):
                if len(payload) != self.fields[coupling.field].components:
                    raise ValueError("carried exchange component count differs from the field")
                residuals = unpack(payload)
                if any(abs(value) >= coupling.denominator for value in residuals):
                    raise ValueError("carried exchange residual must be below its denominator")
                if (
                    coupling.remainder_owner != "left" or record.type_index != coupling.left_type
                ) and any(residuals):
                    raise ValueError("record does not own this coupling's exchange remainder")

    def _route(
        self, record: DisturbanceRecord, meter: CostMeter
    ) -> tuple[DisturbanceRecord | None, tuple[Departure, ...]]:
        rule = self.definitions[record.type_index].transport
        meter.charge("route")
        if rule.mode == "hold":
            return record, ()
        if rule.mode == "split":
            channels = [[list(v) for v in record.values] for _ in range(6)]
            phases: list[Payload] = []
            for index, value in enumerate(record.values):
                updated = []
                for component, amount in enumerate(unpack(value)):
                    meter.charge("split")
                    shares, phase = _shares(
                        amount, rule.weights, record.phase_codes[index][component] - 1
                    )
                    updated.append(phase + 1)
                    for port, share in enumerate(shares):
                        channels[port][index][component] = encode(share)
                phases.append(tuple(updated))
            zero = tuple((1,) * field.components for field in self.fields)
            departures = []
            for port, channel in enumerate(channels):
                values = tuple(tuple(v) for v in channel)
                if any(any(unpack(v)) for v in values):
                    meter.charge("send")
                    departures.append(
                        Departure(
                            port,
                            DisturbanceRecord(record.type_index, values, zero, channel_code=port + 2),
                        )
                    )
            # Allocation phases belong to the local directional channel.
            return replace(record, values=zero, phase_codes=tuple(phases)), tuple(departures)
        weights = rule.weights
        if rule.direction_field is not None or rule.direction is not None:
            direction = (
                evaluate(rule.direction, record.values, record.values, meter)
                if rule.direction is not None
                else unpack(
                    record.values[rule.direction_field if rule.direction_field is not None else 0]
                )
            )
            weights = (
                max(0, direction[0]),
                max(0, -direction[0]),
                max(0, direction[1]),
                max(0, -direction[1]),
                max(0, direction[2]),
                max(0, -direction[2]),
            )
        rate = 1 if rule.rate is None else evaluate(rule.rate, record.values, record.values, meter)[0]
        divisor = rule.rate_denominator
        if rule.rate_divisor is not None:
            divisor = checked_work(
                divisor * evaluate(rule.rate_divisor, record.values, record.values, meter)[0]
            )
        if not 0 <= rate <= divisor or divisor <= 0:
            raise ValueError("movement rate must be between zero and one hop per base interval")
        if not any(weights):
            return record, ()
        if rule.rate_divisor is not None:
            move, credit, credit_den = rate_credit(
                record.rate_remainder_code - 1, record.rate_credit_denominator, rate, divisor, meter
            )
        else:
            budget = checked_work(record.rate_remainder_code - 1 + rate)
            move, credit, credit_den = budget >= divisor, budget % divisor, 1
        if not move:
            return replace(
                record, rate_remainder_code=credit + 1, rate_credit_denominator=credit_den
            ), ()
        counts, previous = (
            tuple(v - 1 for v in record.route_count_codes),
            tuple(v - 1 for v in record.route_weight_codes),
        )
        if rule.routing == "balanced":
            selected, counts, previous = balanced_port(weights, counts, previous, meter)
            phase_code = record.route_phase_code
        else:
            denominator = bounded(sum(weights))
            phase = (record.route_phase_code - 1) % denominator
            offset, selected = 0, 0
            for port, weight in enumerate(weights):
                if offset <= phase < offset + weight:
                    selected = port
                offset += weight
            phase_code = (phase + 1) % denominator + 1
        moved = replace(
            record,
            route_phase_code=phase_code,
            rate_remainder_code=credit + 1,
            rate_credit_denominator=credit_den,
            route_count_codes=tuple(v + 1 for v in counts),
            route_weight_codes=tuple(v + 1 for v in previous),
            channel_code=selected + 2,
        )
        meter.charge("send")
        return None, (Departure(selected, moved),)

    def __call__(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        coupling_remainders: tuple[int, ...],
        received_count: int,
    ) -> LocalPlan:
        meter = CostMeter(self.operation_costs)
        meter.charge("receive", received_count)
        original = _sum_records(records, self.fields)
        updated = list(records)
        source_delta = [[0] * f.components for f in self.fields]
        for slot, record in enumerate(records):
            if record is None:
                continue
            self._validate(record, meter)
            definition = self.definitions[record.type_index]
            meter.charge("read", len(definition.fields))
            for rule in definition.updates:
                meter.charge("update")
                before = unpack(record.values[rule.field])
                value = evaluate(rule.expression, record.values, record.values, meter)
                payload = pack(value)
                self.fields[rule.field].validate(payload)
                if rule.source:
                    for c, (new, old) in enumerate(zip(value, before, strict=True)):
                        source_delta[rule.field][c] = checked_work(
                            source_delta[rule.field][c] + new - old
                        )
                record = _with_value(record, rule.field, payload)
            updated[slot] = record

        remainders = list(coupling_remainders)
        slots = len(records)
        # Configured rule order, then fixed slot order, is the declared local law.
        for rule_index, coupling in enumerate(self.couplings):
            if coupling.remainder_owner not in ("pair", "left"):
                raise ValueError("coupling remainder owner must be pair or left")
            if coupling.remainder_owner == "left" and (
                coupling.left_type == coupling.right_type
                or self.definitions[coupling.left_type].transport.mode == "split"
            ):
                raise ValueError("left-owned exchange requires distinct types and a whole record")
            for left_slot in range(slots):
                for right_slot in range(slots):
                    left, right = updated[left_slot], updated[right_slot]
                    if (
                        left is None
                        or right is None
                        or left_slot == right_slot
                        or left.type_index != coupling.left_type
                        or right.type_index != coupling.right_type
                        or (coupling.left_type == coupling.right_type and right_slot < left_slot)
                    ):
                        continue
                    meter.charge("couple")
                    carried = []
                    if coupling.remainder_owner == "left":
                        carried = list(
                            left.exchange_remainders
                            or tuple(
                                pack((0,) * self.fields[r.field].components) for r in self.couplings
                            )
                        )
                    residuals = list(unpack(carried[rule_index])) if carried else []
                    proposed = evaluate(coupling.amount, left.values, right.values, meter)
                    first, second = (
                        unpack(left.values[coupling.field]),
                        unpack(right.values[coupling.field]),
                    )
                    new_left, new_right = [], []
                    for component, (a, b, delta) in enumerate(zip(first, second, proposed, strict=True)):
                        at = ((rule_index * slots + left_slot) * slots + right_slot) * 3 + component
                        old_remainder = residuals[component] if carried else decode(remainders[at])
                        quotient, remainder = signed_divrem(
                            checked_work(delta + old_remainder), coupling.denominator
                        )
                        new_left.append(checked_work(a - quotient))
                        new_right.append(checked_work(b + quotient))
                        if carried:
                            residuals[component] = remainder
                        else:
                            remainders[at] = encode(remainder)
                    left = _with_value(left, coupling.field, pack(tuple(new_left)))
                    right = _with_value(right, coupling.field, pack(tuple(new_right)))
                    if carried:
                        carried[rule_index] = pack(tuple(residuals))
                        left = replace(left, exchange_remainders=tuple(carried))
                    self._validate(left, meter)
                    self._validate(right, meter)
                    updated[left_slot], updated[right_slot] = left, right

        # Multi-field transactions follow exchanges and precede all routing.
        for interaction in self.interactions:
            for left_slot in range(slots):
                for right_slot in range(slots):
                    left, right = updated[left_slot], updated[right_slot]
                    if (
                        left is None
                        or right is None
                        or left_slot == right_slot
                        or left.type_index != interaction.left_type
                        or right.type_index != interaction.right_type
                        or (interaction.left_type == interaction.right_type and right_slot < left_slot)
                    ):
                        continue
                    updated[left_slot], updated[right_slot] = self._interact(
                        interaction, left, right, meter
                    )

        replacements: list[tuple[int, DisturbanceRecord | None]] = []
        departures: list[Departure] = []
        for slot, record in enumerate(updated):
            if record is None:
                continue
            retained, outgoing = self._route(record, meter)
            replacements.append((slot, retained))
            departures.extend(Departure(item.port, item.record, slot) for item in outgoing)
            if self.definitions[record.type_index].cost_field is not None:
                meter.charge("update")
        meter.charge("commit")
        # Subquantum exchange belongs to the current local pair, not to a later
        # occupant of its slot. It is rounding state, never conserved inventory.
        departed_slots = {slot for slot, record in replacements if record is None}
        for rule_index in range(len(self.couplings)):
            for left_slot in range(slots):
                for right_slot in range(slots):
                    if left_slot in departed_slots or right_slot in departed_slots:
                        at = ((rule_index * slots + left_slot) * slots + right_slot) * 3
                        remainders[at : at + 3] = [1, 1, 1]
        for item, (slot, record) in enumerate(replacements):
            if record is not None:
                target = self.definitions[record.type_index].cost_field
                if target is not None:
                    replacements[item] = (slot, _with_value(record, target, pack((meter.total,))))
        final_records = tuple(r for _, r in replacements) + tuple(d.record for d in departures)
        for record in final_records:
            if record is not None:
                self._validate(record, meter)
        final = _sum_records(final_records, self.fields)
        for index, field in enumerate(self.fields):
            if field.conserved:
                for c in range(field.components):
                    if final[index][c] != checked_work(original[index][c] + source_delta[index][c]):
                        raise ValueError(f"local rule violates conservation of {field.name}")
        return LocalPlan(
            tuple(replacements),
            tuple(departures),
            tuple(remainders),
            tuple(tuple(v) for v in source_delta),
            meter.total,
        )
