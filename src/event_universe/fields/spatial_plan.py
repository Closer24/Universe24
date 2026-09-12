"""Pure local emission and outward transport assembled from generic primitives."""

from dataclasses import dataclass, replace

from event_universe.core.disturbance_state import (
    CostMeter,
    DisturbanceRecord,
    FieldDefinition,
    OperationCosts,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    EmissionDefinition,
    SpatialFieldDefinition,
    SpatialPlan,
    SpatialPopulations,
    SpatialState,
)

from .disturbances import evaluate
from .spatial import add_populations, bounded_emission_amount, emission_amount, emit, split_outward


@dataclass(frozen=True, slots=True)
class SpatialLaw:
    fields: tuple[FieldDefinition, ...]
    definitions: tuple[SpatialFieldDefinition, ...]
    emissions: tuple[EmissionDefinition, ...]
    costs: OperationCosts

    def _emitter(self, record: DisturbanceRecord) -> DisturbanceRecord:
        """Validate fixed carried source metadata, or initialize an untouched emitter."""
        zero = tuple(
            pack((0,) * self.fields[self.definitions[rule.spatial_field].field].components)
            for rule in self.emissions
        )
        remainders, phases = record.emission_remainders, record.emission_phases
        budgets = tuple(
            rule.budget if rule.budget is not None and rule.type_index == record.type_index else blank
            for rule, blank in zip(self.emissions, zero, strict=True)
        )
        finite = any(rule.budget is not None for rule in self.emissions)
        if not remainders and not phases:
            if record.emission_remaining:
                raise ValueError("partial carried emission metadata cannot reset an allowance")
            return replace(
                record,
                emission_remainders=zero,
                emission_phases=zero,
                emission_remaining=budgets if finite else (),
            )
        if len(remainders) != len(zero) or len(phases) != len(zero):
            raise ValueError("carried emission state must match the fixed emission rules")
        for rule, remainder, phase, blank in zip(self.emissions, remainders, phases, zero, strict=True):
            if len(remainder) != len(blank) or len(phase) != len(blank):
                raise ValueError("carried emission component count differs from the field")
            residues, allocation = unpack(remainder), unpack(phase)
            if any(abs(value) >= rule.denominator for value in residues):
                raise ValueError("carried emission residual must be below its denominator")
            denominator = sum(self.definitions[rule.spatial_field].octant_weights)
            if any(not 0 <= value < denominator for value in allocation):
                raise ValueError("carried emission phase must be below the octant weight total")
            if rule.type_index != record.type_index and (any(residues) or any(allocation)):
                raise ValueError("an emitter cannot own another disturbance type's source residue")
        if finite:
            if len(record.emission_remaining) != len(budgets):
                raise ValueError("carried emission allowance count differs from its rules")
            for remaining, budget in zip(record.emission_remaining, budgets, strict=True):
                if len(remaining) != len(budget) or any(
                    not 0 <= value <= limit
                    for value, limit in zip(unpack(remaining), unpack(budget), strict=True)
                ):
                    raise ValueError("carried emission allowance exceeds its initial budget")
        elif record.emission_remaining:
            raise ValueError("unlimited emission cannot carry a finite allowance")
        return record

    def __call__(
        self,
        states: tuple[SpatialState, ...],
        records: tuple[DisturbanceRecord | None, ...],
        received_count: int = 0,
    ) -> SpatialPlan:
        if bounded(received_count) < 0:
            raise ValueError("received spatial packet count must be nonnegative")
        meter = CostMeter(self.costs)
        meter.charge("receive", received_count)
        meter.charge("read", received_count * 8 * len(self.definitions))
        received_components = sum(self.fields[d.field].components for d in self.definitions)
        # Each delivered component updates its population and directional sample.
        meter.charge("update", received_count * 16 * received_components)
        working = list(states)
        emitters = tuple(rule.type_index for rule in self.emissions)
        updated_records = [
            self._emitter(record) if record is not None and record.type_index in emitters else record
            for record in records
        ]
        source = [[0] * field.components for field in self.fields]
        for index, rule in enumerate(self.emissions):
            definition = self.definitions[rule.spatial_field]
            field = self.fields[definition.field]
            for slot, record in enumerate(updated_records):
                if record is None or record.type_index != rule.type_index:
                    continue
                meter.charge("read")
                if rule.budget is not None and not any(unpack(record.emission_remaining[index])):
                    continue
                proposed = evaluate(rule.amount, record.values, record.values, meter)
                residuals, allocation = list(record.emission_remainders), list(record.emission_phases)
                remaining = list(record.emission_remaining)
                if rule.budget is None:
                    amount, residuals[index] = emission_amount(
                        proposed, residuals[index], rule.denominator, field, meter
                    )
                else:
                    amount, residuals[index], remaining[index] = bounded_emission_amount(
                        proposed, residuals[index], rule.denominator, remaining[index], field, meter
                    )
                populations, allocation[index] = emit(
                    amount, allocation[index], definition, field, meter
                )
                old = working[rule.spatial_field]
                working[rule.spatial_field] = SpatialState(
                    add_populations(old.populations, populations, field, meter),
                    old.allocation_phases,
                    old.delivered,
                )
                updated_records[slot] = replace(
                    record,
                    emission_remainders=tuple(residuals),
                    emission_phases=tuple(allocation),
                    emission_remaining=tuple(remaining),
                )
                for component, value in enumerate(unpack(amount)):
                    source[definition.field][component] = checked_work(
                        source[definition.field][component] + value
                    )
        outgoing: list[list[SpatialPopulations]] = [[] for _ in range(6)]
        retained = []
        for index, definition in enumerate(self.definitions):
            field = self.fields[definition.field]
            channels, state = split_outward(working[index], definition, field, meter)
            retained.append(state)
            for port, payloads in enumerate(channels):
                outgoing[port].append(payloads)
            if field.conserved:
                for component in range(field.components):
                    before = source[definition.field][component]
                    for payload in states[index].populations:
                        before = checked_work(before + unpack(payload)[component])
                    after = 0
                    for channel in channels:
                        for payload in channel:
                            after = checked_work(after + unpack(payload)[component])
                    if before != after:
                        raise ValueError("outward transport violates declared conservation")
            # Validate the observable resident value before changing ownership.
            local = list(unpack(definition.baseline))
            for payload in working[index].populations:
                for component, value in enumerate(unpack(payload)):
                    local[component] = checked_work(local[component] + value)
            field.validate(pack(tuple(local)))
        meter.charge("commit")
        return SpatialPlan(
            tuple(retained),
            tuple(tuple(fields) for fields in outgoing),
            tuple(updated_records),
            tuple(tuple(v) for v in source),
            meter.total,
        )
