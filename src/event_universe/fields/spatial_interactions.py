"""Generic field/carrier transactions with rebased delayed-commit guards."""

from dataclasses import dataclass, replace

from event_universe.core.disturbance_state import (
    CostMeter,
    DisturbanceRecord,
    Values,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import add_components, checked_work, subtract_components
from event_universe.core.spatial_state import (
    FieldInteractionGuard,
    SpatialCouplingResult,
    SpatialInteractionDefinition,
    SpatialState,
    zero_spatial_state,
)

from .disturbances import evaluate
from .local_field_rules import received_values
from .spatial_coupling import SpatialCouplingLaw, sample_values


def _delta_cost(meter: CostMeter, values: Values, count: int = 1) -> None:
    """Price a bounded component-wise read/read/arithmetic pass."""
    components = sum(len(value) for value in values) * count
    meter.charge("read", 2 * components)
    meter.charge("update", components)


def _add_delta(values: Values, delta: Values, meter: CostMeter) -> Values:
    if len(values) != len(delta):
        raise ValueError("field transaction delta has the wrong schema")
    _delta_cost(meter, values)
    return tuple(
        pack(add_components(unpack(value), change)) for value, change in zip(values, delta, strict=True)
    )


def _difference(after: Values, before: Values, meter: CostMeter) -> Values:
    _delta_cost(meter, before)
    return tuple(
        tuple(bounded(value) for value in subtract_components(unpack(new), unpack(old)))
        for new, old in zip(after, before, strict=True)
    )


@dataclass(frozen=True, slots=True)
class JointSpatialCouplingLaw(SpatialCouplingLaw):
    """Reuse old response operations, then apply configured joint assignments."""

    interactions: tuple[SpatialInteractionDefinition, ...] = ()

    def sample_ports(self, states: tuple[SpatialState, ...]) -> tuple[Values, ...]:
        return received_values(self.fields, self.spatial_definitions, states, self.port_count)

    def _reserve_sample(self, meter: CostMeter) -> None:
        for definition in self.spatial_definitions:
            meter.charge("read", 9)
            meter.charge("update", 8 * self.fields[definition.field].components)

    def _reserve_local_deposit(self, meter: CostMeter, reaction: Values) -> None:
        changed = False
        for definition in self.spatial_definitions:
            if definition.transport == "local" and any(reaction[definition.field]):
                changed = True
                meter.charge("read", 9)
                meter.charge("update", 9 * self.fields[definition.field].components)
        if changed:
            self._reserve_sample(meter)

    def _check(
        self,
        rule: SpatialInteractionDefinition,
        before: Values,
        after: Values,
        field_before: Values,
        field_after: Values,
        meter: CostMeter,
    ) -> None:
        for index, field in enumerate(self.fields):
            for payloads in (before, after, field_before, field_after):
                field.validate(payloads[index])
            meter.charge("read", 4)
            if field.conserved:
                old = tuple(
                    checked_work(a + b)
                    for a, b in zip(unpack(before[index]), unpack(field_before[index]), strict=True)
                )
                new = tuple(
                    checked_work(a + b)
                    for a, b in zip(unpack(after[index]), unpack(field_after[index]), strict=True)
                )
                meter.charge("update", 2 * field.components)
                if old != new:
                    raise ValueError(
                        f"spatial interaction {rule.name} violates conservation of {field.name}"
                    )
        for invariant in rule.invariants:
            old = evaluate(invariant.expression, before, field_before, meter)
            new = evaluate(invariant.expression, after, field_after, meter)
            if old != new:
                raise ValueError(f"spatial interaction {rule.name} violates invariant {invariant.name}")

    def __call__(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        sample: Values,
        fluxes: Values = (),
        ports: tuple[Values, ...] = (),
    ) -> SpatialCouplingResult:
        legacy = SpatialCouplingLaw.__call__(self, records, sample, fluxes)
        meter = CostMeter(self.costs)
        meter.total = legacy.cost
        if not self.interactions:
            self._reserve_local_deposit(meter, legacy.reaction)
            return replace(legacy, cost=meter.total)
        if len(ports) != self.port_count:
            raise ValueError("spatial interactions require the configured received port samples")
        for channel in ports:
            if len(channel) != len(self.fields):
                raise ValueError("received port fields differ from the configured schema")
            for field, payload in zip(self.fields, channel, strict=True):
                field.validate(payload)
                meter.charge("read")
        working = list(legacy.records)
        field_values = _add_delta(sample, legacy.reaction, meter)
        reaction = [list(values) for values in legacy.reaction]
        guards = []
        for index, rule in enumerate(self.interactions):
            for slot, record in enumerate(working):
                if record is None or record.type_index != rule.type_index:
                    continue
                if (
                    rule.when is not None
                    and evaluate(rule.when, record.values, field_values, meter, fluxes, ports=ports)[0]
                    <= 0
                ):
                    continue
                meter.charge("couple")
                candidate = [list(record.values), list(field_values)]
                for assignment in rule.assignments:
                    value = evaluate(
                        assignment.expression, record.values, field_values, meter, fluxes, ports=ports
                    )
                    payload = pack(value)
                    self.fields[assignment.field].validate(payload)
                    candidate[assignment.side][assignment.field] = payload
                    meter.charge("update")
                after, field_after = tuple(candidate[0]), tuple(candidate[1])
                start = meter.total
                self._check(rule, record.values, after, field_values, field_after, meter)
                # Reserve the same bounded validation work for the actual delayed commit.
                meter.total = bounded(checked_work(meter.total + meter.total - start))
                delta = _difference(field_after, field_values, meter)
                _delta_cost(meter, delta)
                for field_index, change in enumerate(delta):
                    for component, amount in enumerate(change):
                        reaction[field_index][component] = bounded(
                            checked_work(reaction[field_index][component] + amount)
                        )
                guards.append(FieldInteractionGuard(index, slot, record.values, after, delta))
                working[slot] = replace(record, values=after)
                field_values = field_after
        if guards:
            # Commit resamples, subtracts every delta, adds the legacy remainder,
            # then replays each guard, even when the final reaction is zero.
            self._reserve_sample(meter)
            _delta_cost(meter, sample, 2 * len(guards) + 1)
        self._reserve_local_deposit(meter, tuple(tuple(value) for value in reaction))
        return SpatialCouplingResult(
            tuple(working), tuple(tuple(value) for value in reaction), meter.total, tuple(guards)
        )

    def validate_guards(
        self,
        states: tuple[SpatialState, ...],
        reaction: Values,
        guards: tuple[FieldInteractionGuard, ...],
    ) -> None:
        """Check each frozen transaction against currently owned field values."""
        if not guards:
            return
        meter = CostMeter(self.costs)
        remaining = [list(value) for value in reaction]
        for guard in guards:
            _delta_cost(meter, guard.delta)
            for index, change in enumerate(guard.delta):
                for component, value in enumerate(change):
                    remaining[index][component] = checked_work(remaining[index][component] - value)
        sample = sample_values(
            states, self.spatial_definitions, self.fields, meter, port_count=self.port_count
        )
        current = _add_delta(sample, tuple(tuple(value) for value in remaining), meter)
        for guard in guards:
            if not 0 <= guard.rule_index < len(self.interactions):
                raise ValueError("unknown pending spatial interaction guard")
            after = _add_delta(current, guard.delta, meter)
            self._check(
                self.interactions[guard.rule_index], guard.before, guard.after, current, after, meter
            )
            current = after

    def _partition_reaction(self, reaction: Values) -> tuple[Values, Values]:
        local_fields = {d.field for d in self.spatial_definitions if d.transport == "local"}
        zero = tuple((0,) * field.components for field in self.fields)
        return (
            tuple(value if i not in local_fields else zero[i] for i, value in enumerate(reaction)),
            tuple(value if i in local_fields else zero[i] for i, value in enumerate(reaction)),
        )

    def _deposit_local(
        self, states: tuple[SpatialState, ...], reaction: Values
    ) -> tuple[SpatialState, ...]:
        if not any(any(value) for value in reaction):
            return states
        updated = list(states)
        for index, definition in enumerate(self.spatial_definitions):
            if definition.transport != "local" or not any(reaction[definition.field]):
                continue
            field = self.fields[definition.field]
            state = states[index]
            state.validate(field.components, self.port_count)
            values = list(reaction[definition.field])
            for payload in state.populations:
                field.validate(payload)
                for component, amount in enumerate(unpack(payload)):
                    values[component] = checked_work(values[component] + amount)
            packed = pack(tuple(values))
            field.validate(packed)
            blank = zero_spatial_state(field.components, self.port_count)
            updated[index] = replace(state, populations=(packed, *blank.populations[1:]))
        result = tuple(updated)
        sample_values(result, self.spatial_definitions, self.fields, port_count=self.port_count)
        return result

    def deposit(
        self,
        states: tuple[SpatialState, ...],
        phases: Values,
        reaction: Values,
    ) -> tuple[tuple[SpatialState, ...], Values]:
        outward, local = self._partition_reaction(reaction)
        updated, next_phases = SpatialCouplingLaw.deposit(self, states, phases, outward)
        return self._deposit_local(updated, local), next_phases

    def forward_reaction(
        self,
        states: tuple[SpatialState, ...],
        phases: Values,
        reaction: Values,
    ) -> tuple[tuple[SpatialState, ...], Values, tuple[tuple[tuple[tuple[int, ...], ...], ...], ...]]:
        outward, local = self._partition_reaction(reaction)
        updated, next_phases, outgoing = SpatialCouplingLaw.forward_reaction(
            self, states, phases, outward
        )
        return self._deposit_local(updated, local), next_phases, outgoing
