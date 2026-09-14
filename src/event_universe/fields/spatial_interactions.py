"""Generic field/carrier transactions with rebased delayed-commit guards."""

from collections.abc import Mapping
from dataclasses import dataclass, replace

from event_universe.core.coupling_selectors import matches_type, participant_groups
from event_universe.core.disturbance_state import (
    MAX_RULES,
    MAX_SLOTS,
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
from event_universe.core.validation import ValidationMeter

from .disturbances import evaluate
from .local_field_rules import received_masks, received_values
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
        return received_values(self.fields, self.spatial_definitions, states)

    def sample_received_masks(self, states: tuple[SpatialState, ...]) -> tuple[int, ...]:
        return received_masks(self.fields, self.spatial_definitions, states)

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
        before: tuple[Values, ...],
        after: tuple[Values, ...],
        field_before: Values,
        field_after: Values,
        meter: CostMeter,
    ) -> None:
        meter = ValidationMeter(self.costs)
        original, candidate = (*before, field_before), (*after, field_after)
        for index, field in enumerate(self.fields):
            for payloads in (*original, *candidate):
                field.validate(payloads[index])
            meter.charge("read", len(original) + len(candidate))
            if field.conserved:
                totals = []
                for owners in (original, candidate):
                    total = (0,) * field.components
                    for owner in owners:
                        total = add_components(total, unpack(owner[index]))
                    totals.append(total)
                meter.charge("update", 2 * field.components)
                if totals[0] != totals[1]:
                    raise ValueError(
                        f"spatial interaction {rule.name} violates conservation of {field.name}"
                    )
        for invariant in rule.invariants:
            old = evaluate(invariant.expression, before[0], field_before, meter, participants=original)
            new = evaluate(invariant.expression, after[0], field_after, meter, participants=candidate)
            if old != new:
                raise ValueError(f"spatial interaction {rule.name} violates invariant {invariant.name}")

    def _proposal(
        self,
        rule: SpatialInteractionDefinition,
        before: tuple[Values, ...],
        field_values: Values,
        meter: CostMeter,
        fluxes: Values,
        ports: tuple[Values, ...],
        received_masks: tuple[int, ...],
    ) -> tuple[tuple[Values, ...], Values] | None:
        owners = (*before, field_values)
        for condition, condition_meter in (
            (rule.when, meter),
            (rule.commit_when, ValidationMeter(self.costs)),
        ):
            if (
                condition is not None
                and evaluate(
                    condition,
                    before[0],
                    field_values,
                    condition_meter,
                    fluxes,
                    ports=ports,
                    participants=owners,
                    received_masks=received_masks,
                )[0]
                <= 0
            ):
                return None
        meter.advance(rule.k)
        meter.charge("couple")
        candidate = [list(owner) for owner in owners]
        for assignment in rule.assignments:
            value = evaluate(
                assignment.expression,
                before[0],
                field_values,
                meter,
                fluxes,
                ports=ports,
                participants=owners,
                received_masks=received_masks,
            )
            payload = pack(value)
            self.fields[assignment.field].validate(payload)
            candidate[assignment.side][assignment.field] = payload
            meter.charge("update")
        after = tuple(tuple(owner) for owner in candidate[:-1])
        field_after = tuple(candidate[-1])
        self._check(rule, before, after, field_values, field_after, meter)
        return after, field_after

    def __call__(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        sample: Values,
        fluxes: Values = (),
        ports: tuple[Values, ...] = (),
        received_masks: tuple[int, ...] = (),
        *,
        slot_samples: Mapping[int, Values] | None = None,
        slot_fluxes: Mapping[int, Values] | None = None,
    ) -> SpatialCouplingResult:
        if slot_samples or slot_fluxes:
            raise ValueError("joint spatial interactions do not support per-slot samples")
        if len(records) > MAX_SLOTS or len(self.interactions) > MAX_RULES:
            raise ValueError("spatial interactions exceed fixed local capacity")
        legacy = SpatialCouplingLaw.__call__(self, records, sample, fluxes)
        meter = CostMeter(self.costs)
        meter.total = legacy.cost
        meter.interaction_ticks = legacy.interaction_ticks
        if not self.interactions:
            self._reserve_local_deposit(meter, legacy.reaction)
            return replace(legacy, cost=meter.total)
        if len(ports) != 6:
            raise ValueError("spatial interactions require six received port samples")
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
            groups = (
                participant_groups(rule, tuple(working))
                if rule.participants
                else tuple(
                    (slot,)
                    for slot, record in enumerate(working)
                    if record is not None and matches_type(rule, record.type_index)
                )
            )
            for slots in groups:
                selected = tuple(working[slot] for slot in slots)
                assert all(record is not None for record in selected)
                originals = tuple(record for record in selected if record is not None)
                before = tuple(record.values for record in originals)
                proposal = self._proposal(
                    rule, before, field_values, meter, fluxes, ports, received_masks
                )
                if proposal is None:
                    continue
                after, field_after = proposal
                delta = _difference(field_after, field_values, meter)
                _delta_cost(meter, delta)
                for field_index, change in enumerate(delta):
                    for component, amount in enumerate(change):
                        reaction[field_index][component] = bounded(
                            checked_work(reaction[field_index][component] + amount)
                        )
                guards.append(
                    FieldInteractionGuard(
                        index,
                        slots[0],
                        before[0],
                        after[0],
                        delta,
                        slots if rule.participants else (),
                        before if rule.participants else (),
                        after if rule.participants else (),
                    )
                )
                for slot, record, values in zip(slots, originals, after, strict=True):
                    working[slot] = replace(record, values=values)
                field_values = field_after
        self._reserve_local_deposit(meter, tuple(tuple(value) for value in reaction))
        return SpatialCouplingResult(
            tuple(working),
            tuple(tuple(value) for value in reaction),
            meter.total,
            tuple(guards),
            meter.interaction_ticks,
        )

    def validate_guards(
        self,
        states: tuple[SpatialState, ...],
        reaction: Values,
        guards: tuple[FieldInteractionGuard, ...],
    ) -> None:
        """Check each frozen transaction against currently owned field values."""
        if type(guards) is not tuple or len(guards) > MAX_RULES * MAX_SLOTS:
            raise ValueError("pending spatial interaction guards exceed fixed local capacity")
        if not guards:
            return
        meter = ValidationMeter(self.costs)
        remaining = [list(value) for value in reaction]
        for guard in guards:
            if type(guard) is not FieldInteractionGuard or type(guard.rule_index) is not int:
                raise ValueError("pending spatial interaction requires an immutable indexed guard")
            if not 0 <= guard.rule_index < len(self.interactions):
                raise ValueError("unknown pending spatial interaction guard")
            count = len(self.interactions[guard.rule_index].participants)
            if (
                type(guard.slots) is not tuple
                or len(guard.slots) != count
                or len(set(guard.slots)) != count
                or any(type(slot) is not int or not 0 <= slot < MAX_SLOTS for slot in guard.slots)
                or type(guard.participant_before) is not tuple
                or type(guard.participant_after) is not tuple
                or len(guard.participant_before) != count
                or len(guard.participant_after) != count
            ):
                raise ValueError("pending spatial interaction participant snapshots are invalid")
            _delta_cost(meter, guard.delta)
            for index, change in enumerate(guard.delta):
                for component, value in enumerate(change):
                    remaining[index][component] = checked_work(remaining[index][component] - value)
        sample = sample_values(states, self.spatial_definitions, self.fields, meter)
        current = _add_delta(sample, tuple(tuple(value) for value in remaining), meter)
        for guard in guards:
            if not 0 <= guard.rule_index < len(self.interactions):
                raise ValueError("unknown pending spatial interaction guard")
            after = _add_delta(current, guard.delta, meter)
            rule = self.interactions[guard.rule_index]
            before_owners = guard.participant_before or (guard.before,)
            after_owners = guard.participant_after or (guard.after,)
            if (
                rule.commit_when is not None
                and evaluate(
                    rule.commit_when,
                    before_owners[0],
                    current,
                    meter,
                    participants=(*before_owners, current),
                )[0]
                <= 0
            ):
                raise ValueError(f"spatial interaction {rule.name} commit_when is no longer satisfied")
            self._check(rule, before_owners, after_owners, current, after, meter)
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
            state.validate(field.components)
            values = list(reaction[definition.field])
            for payload in state.populations:
                field.validate(payload)
                for component, amount in enumerate(unpack(payload)):
                    values[component] = checked_work(values[component] + amount)
            packed = pack(tuple(values))
            field.validate(packed)
            blank = zero_spatial_state(field.components)
            updated[index] = replace(state, populations=(packed, *blank.populations[1:]))
        result = tuple(updated)
        sample_values(result, self.spatial_definitions, self.fields)
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
