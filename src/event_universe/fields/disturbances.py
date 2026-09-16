"""Bounded local arithmetic for data-defined disturbance evolution and transport."""

from dataclasses import dataclass, replace

from event_universe.core.coupling_selectors import (
    matches_pair,
    participant_groups,
    selected_left_types,
    selected_right_types,
)
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
from event_universe.core.integer import (
    add_components,
    checked_sum,
    checked_work,
    cross_product,
    dot_product,
    signed_divrem,
)
from event_universe.core.validation import ValidationMeter

from .ratios import PROJECTIONS, evaluate_ratio, project
from .routing import balanced_port, rate_credit
from .spatial import split_weighted


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
    participants: tuple[Values, ...] = (),
    received_masks: tuple[int, ...] = (),
    node_cost: int | None = None,
) -> tuple[int, ...]:
    """Evaluate a validated, fixed-size integer AST without Python eval or imports."""
    meter.charge("evaluate")
    op = expression.op
    if op in PROJECTIONS:
        values = evaluate_ratio(
            expression.arguments[0],
            left,
            right,
            meter,
            spatial_fluxes,
            ports=ports,
            outgoing=outgoing,
            participants=participants,
            received_masks=received_masks,
            node_cost=node_cost,
        )
        return project(op, values)
    if op == "literal":
        return expression.literal
    if op == "node_cost":
        if node_cost is None or bounded(node_cost) < 0:
            raise ValueError("node cost requires an explicitly supplied committed local value")
        return (node_cost,)
    if op == "field":
        owners = participants or (left, right)
        if not 0 <= expression.side < len(owners):
            raise ValueError("field expression participant is unavailable")
        return unpack(owners[expression.side][expression.field])
    if op == "received_present":
        if not 0 <= expression.field < len(received_masks) or not 0 <= expression.port < 6:
            raise ValueError("received presence requires explicitly supplied local port masks")
        mask = received_masks[expression.field]
        if type(mask) is not int or not 0 <= mask < 64:
            raise ValueError("received mask requires six bounded port bits")
        return (int(bool(mask & (1 << expression.port))),)
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
        evaluate(
            arg,
            left,
            right,
            meter,
            spatial_fluxes,
            ports=ports,
            outgoing=outgoing,
            participants=participants,
            received_masks=received_masks,
            node_cost=node_cost,
        )
        for arg in expression.arguments
    )
    if op == "transform":
        return tuple(dot_product(row, operands[0]) for row in expression.matrix)
    if op == "dot":
        return (dot_product(operands[0], operands[1]),)
    if op == "cross":
        return cross_product(operands[0], operands[1])
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
            return (checked_sum(unary),)
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
    return pack(add_components(unpack(left), unpack(right)))


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


def interact_values(
    rule: InteractionDefinition,
    before: tuple[Values, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
) -> tuple[Values, ...]:
    """Apply the same frozen indexed operation to any admitted complete owner view."""
    if rule.outputs or rule.output_types is not None:
        raise ValueError("indexed value updates do not support family conversion outputs")
    if rule.when is not None and evaluate(rule.when, (), (), meter, participants=before)[0] <= 0:
        return before
    meter.advance(rule.k)
    meter.charge("couple")
    candidate = [list(values) for values in before]
    for assignment in rule.assignments:
        value = evaluate(assignment.expression, (), (), meter, participants=before)
        candidate[assignment.side][assignment.field] = pack(value)
        meter.charge("update")
    after = tuple(tuple(values) for values in candidate)
    for values in after:
        for field, value in zip(fields, values, strict=True):
            field.validate(value)
    for index, field in enumerate(fields):
        if field.conserved:
            old = tuple(
                checked_sum(unpack(values[index])[c] for values in before)
                for c in range(field.components)
            )
            new = tuple(
                checked_sum(unpack(values[index])[c] for values in after)
                for c in range(field.components)
            )
            if old != new:
                raise ValueError(f"interaction {rule.name} violates conservation of {field.name}")
    checks = ValidationMeter(costs)
    for invariant in rule.invariants:
        if evaluate(invariant.expression, (), (), checks, participants=before) != evaluate(
            invariant.expression, (), (), checks, participants=after
        ):
            raise ValueError(f"interaction {rule.name} violates invariant {invariant.name}")
    return after


@dataclass(frozen=True, slots=True)
class DisturbanceLaw:
    """Pure local proposal: immutable definitions, fixed records and carried phases."""

    fields: tuple[FieldDefinition, ...]
    definitions: tuple[DisturbanceDefinition, ...]
    couplings: tuple[CouplingDefinition, ...]
    operation_costs: OperationCosts
    interactions: tuple[InteractionDefinition, ...] = ()
    least_delay: bool = False

    def _interact_group(
        self, rule: InteractionDefinition, records: tuple[DisturbanceRecord, ...], meter: CostMeter
    ) -> tuple[DisturbanceRecord, ...]:
        """Apply simultaneous assignments against one frozen indexed input group."""
        before = tuple(record.values for record in records)
        after = interact_values(rule, before, self.fields, meter, self.operation_costs)
        if after is before:
            return records
        candidate = tuple(
            replace(record, values=values) for record, values in zip(records, after, strict=True)
        )
        for record in candidate:
            self._validate(record, meter)
        return candidate

    def _interact(
        self,
        rule: InteractionDefinition,
        left: DisturbanceRecord,
        right: DisturbanceRecord,
        meter: CostMeter,
    ) -> tuple[DisturbanceRecord, DisturbanceRecord]:
        if rule.when is not None and evaluate(rule.when, left.values, right.values, meter)[0] <= 0:
            return left, right
        meter.advance(rule.k)
        meter.charge("couple")
        checks = ValidationMeter(self.operation_costs)
        before = tuple(
            evaluate(i.expression, left.values, right.values, checks) for i in rule.invariants
        )
        candidate = [left, right]
        for assignment in rule.assignments:
            meter.charge("update")
            # Every right-hand side reads the same frozen pair, not earlier assignments.
            value = evaluate(assignment.expression, left.values, right.values, meter)
            candidate[assignment.side] = _with_value(
                candidate[assignment.side], assignment.field, pack(value)
            )
        if rule.output_types is not None:
            for side, original in enumerate((left, right)):
                self._require_convertible(original)
                meter.charge("update")
                zero = tuple((1,) * field.components for field in self.fields)
                # Whole-record channel tags record arrival provenance, not fractional stock.
                candidate[side] = DisturbanceRecord(
                    rule.output_types[side],
                    candidate[side].values,
                    zero,
                    channel_code=original.channel_code,
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
            if evaluate(invariant.expression, first.values, second.values, checks) != expected:
                raise ValueError(f"interaction {rule.name} violates invariant {invariant.name}")
        return first, second

    @staticmethod
    def _require_convertible(original: DisturbanceRecord) -> None:
        """A different routing law cannot inherit or silently erase fractional progress."""
        carried = (
            *original.phase_codes,
            *original.emission_remainders,
            *original.emission_phases,
            *original.exchange_remainders,
            *original.spatial_remainders,
            *original.emission_remaining,
            *original.spatial_remaining,
        )
        if (
            original.route_phase_code != 1
            or original.rate_remainder_code != 1
            or original.rate_credit_denominator != 1
            or any(code != 1 for code in original.route_count_codes)
            or any(code != 1 for code in original.route_weight_codes)
            or any(code != 1 for payload in carried for code in payload)
        ):
            raise ValueError("conversion requires zero carried routing and allowance state")
        if not 1 <= original.channel_code <= 7:
            raise ValueError("conversion channel must identify the seed or a neighbor port")

    def _convert_group(
        self, rule: InteractionDefinition, records: tuple[DisturbanceRecord, ...], meter: CostMeter
    ) -> tuple[DisturbanceRecord, ...] | None:
        """Replace N frozen inputs by M declared output families, or None when the guard is false.

        Every output payload is built from the same frozen inputs. Conserved fields
        and every per-record readout invariant are compared as sums over all inputs
        against sums over all outputs before anything is returned.
        """
        before = tuple(record.values for record in records)
        if rule.when is not None and evaluate(rule.when, (), (), meter, participants=before)[0] <= 0:
            return None
        meter.advance(rule.k)
        meter.charge("couple")
        for original in records:
            self._require_convertible(original)
        zero_phases = tuple((1,) * field.components for field in self.fields)
        zero_values = tuple(pack((0,) * field.components) for field in self.fields)
        candidates = [
            DisturbanceRecord(
                kind,
                zero_values,
                zero_phases,
                # Outputs that reuse an input slot keep its arrival provenance; new ones are local.
                channel_code=records[index].channel_code if index < len(records) else 1,
            )
            for index, kind in enumerate(rule.outputs)
        ]
        for assignment in rule.assignments:
            value = evaluate(assignment.expression, (), (), meter, participants=before)
            candidates[assignment.side] = _with_value(
                candidates[assignment.side], assignment.field, pack(value)
            )
            meter.charge("update")
        for candidate in candidates:
            meter.charge("update")
            self._validate(candidate, meter)
        inputs, outputs = (
            _sum_records(records, self.fields),
            _sum_records(tuple(candidates), self.fields),
        )
        for index, field in enumerate(self.fields):
            if field.conserved and inputs[index] != outputs[index]:
                raise ValueError(f"interaction {rule.name} violates conservation of {field.name}")
        checks = ValidationMeter(self.operation_costs)
        for invariant in rule.invariants:
            sums = []
            for group in (records, tuple(candidates)):
                readouts = [evaluate(invariant.expression, r.values, r.values, checks) for r in group]
                width = len(readouts[0])
                if any(len(readout) != width for readout in readouts):
                    raise ValueError(f"invariant {invariant.name} readout shape differs across records")
                sums.append(tuple(checked_sum(readout[c] for readout in readouts) for c in range(width)))
            if sums[0] != sums[1]:
                raise ValueError(f"interaction {rule.name} violates invariant {invariant.name}")
        return tuple(candidates)

    def _validate(self, record: DisturbanceRecord, meter: CostMeter) -> None:
        definition = self.definitions[record.type_index]
        if len(record.values) != len(self.fields):
            raise ValueError("record field count differs from the configured schema")
        for index, field in enumerate(self.fields):
            field.validate(record.values[index])
            if index not in definition.fields and any(unpack(record.values[index])):
                raise ValueError("record carries a field absent from its disturbance type")
        for check in definition.checks:
            if (
                evaluate(
                    check.expression, record.values, record.values, ValidationMeter(self.operation_costs)
                )[0]
                <= 0
            ):
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
                    coupling.remainder_owner != "left"
                    or record.type_index not in selected_left_types(coupling)
                ) and any(residuals):
                    raise ValueError("record does not own this coupling's exchange remainder")

    def _route(
        self,
        record: DisturbanceRecord,
        meter: CostMeter,
        port_loads: tuple[int, ...] | None = None,
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
            selected, counts, previous = balanced_port(
                weights, counts, previous, meter, loads=port_loads if self.least_delay else None
            )
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
        *,
        port_loads: tuple[int, ...] = (0, 0, 0, 0, 0, 0),
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
                set(selected_left_types(coupling)) & set(selected_right_types(coupling))
                or any(
                    self.definitions[kind].transport.mode == "split"
                    for kind in selected_left_types(coupling)
                )
            ):
                raise ValueError("left-owned exchange requires distinct types and a whole record")
            for left_slot in range(slots):
                for right_slot in range(slots):
                    left, right = updated[left_slot], updated[right_slot]
                    if (
                        left is None
                        or right is None
                        or left_slot == right_slot
                        or not matches_pair(coupling, left.type_index, right.type_index)
                        or (
                            right_slot < left_slot
                            and matches_pair(coupling, right.type_index, left.type_index)
                        )
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
        consumed: set[int] = set()
        products: set[int] = set()
        for interaction in self.interactions:
            if interaction.participants:
                for group in participant_groups(interaction, tuple(updated)):
                    records_in_group = tuple(updated[slot] for slot in group)
                    assert all(record is not None for record in records_in_group)
                    participants = tuple(record for record in records_in_group if record is not None)
                    if not interaction.outputs:
                        outputs = self._interact_group(interaction, participants, meter)
                        for slot, output in zip(group, outputs, strict=True):
                            updated[slot] = output
                        continue
                    converted = self._convert_group(interaction, participants, meter)
                    if converted is None:
                        continue
                    for slot, output in zip(group, converted, strict=False):
                        updated[slot] = output
                        products.add(slot)
                    for slot in group[len(converted) :]:
                        updated[slot] = None
                        consumed.add(slot)
                        products.discard(slot)
                    for output in converted[len(group) :]:
                        free = next((s for s in range(slots) if updated[s] is None), None)
                        if free is None:
                            raise ValueError("conversion outputs exceed the free resident slots")
                        updated[free] = output
                        consumed.discard(free)
                        products.add(free)
                continue
            for left_slot in range(slots):
                for right_slot in range(slots):
                    left, right = updated[left_slot], updated[right_slot]
                    if (
                        left is None
                        or right is None
                        or left_slot == right_slot
                        or not matches_pair(interaction, left.type_index, right.type_index)
                        or (
                            right_slot < left_slot
                            and matches_pair(interaction, right.type_index, left.type_index)
                        )
                    ):
                        continue
                    updated[left_slot], updated[right_slot] = self._interact(
                        interaction, left, right, meter
                    )

        replacements: list[tuple[int, DisturbanceRecord | None]] = []
        departures: list[Departure] = []
        for slot, record in enumerate(updated):
            if record is None:
                if slot in consumed:
                    replacements.append((slot, None))
                continue
            retained, outgoing = self._route(record, meter, port_loads)
            replacements.append((slot, retained))
            departures.extend(Departure(item.port, item.record, slot) for item in outgoing)
            if self.definitions[record.type_index].cost_field is not None:
                meter.charge("update")
        # Products of this cycle's conversions leave on distinct Ports; other records
        # keep the ordinary transport, which admits several packets per Port.
        product_ports = [item.port for item in departures if item.origin_slot in products]
        if len(set(product_ports)) != len(product_ports):
            raise ValueError("conversion departures must use distinct Ports")
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
            interaction_ticks=meter.interaction_ticks,
        )
