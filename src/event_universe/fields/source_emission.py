"""Local finite source emission from a causally retained complex envelope."""

from dataclasses import dataclass

from event_universe.core.coupling_selectors import matches_type
from event_universe.core.disturbance_state import (
    CostMeter,
    DisturbanceRecord,
    FieldDefinition,
    OperationCosts,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.source_emission import EnvelopeEmissionState, PendingEnvelopeEmission
from event_universe.core.source_envelope_state import (
    EnvelopeAmplitude,
    EnvelopeRemainder,
    EnvelopeScale,
)
from event_universe.core.spatial_state import (
    EmissionDefinition,
    SpatialBundle,
    SpatialFieldDefinition,
    SpatialPopulations,
    SpatialState,
)

from .disturbances import evaluate
from .source_envelope import weighted_emission
from .spatial import add_populations, emit


@dataclass(frozen=True, slots=True)
class SourceEmissionLaw:
    fields: tuple[FieldDefinition, ...]
    spatial_fields: tuple[SpatialFieldDefinition, ...]
    emissions: tuple[EmissionDefinition, ...]
    operation_costs: OperationCosts


def initial_emission_state(
    initial: SourceEmissionLaw, record: DisturbanceRecord
) -> EnvelopeEmissionState:
    residuals, phases, remaining = [], [], []
    for rule in initial.emissions:
        field = initial.fields[initial.spatial_fields[rule.spatial_field].field]
        zero = pack((0,) * field.components)
        selected = matches_type(rule, record.type_index)
        if selected and rule.budget is None:
            raise ValueError("causal envelope sources require finite per-mode emission allowances")
        residuals.append((EnvelopeRemainder(),) * field.components)
        phases.append(zero)
        remaining.append(rule.budget if selected and rule.budget is not None else zero)
    return EnvelopeEmissionState(tuple(residuals), tuple(phases), tuple(remaining))


def prepare_emission(
    initial: SourceEmissionLaw,
    record: DisturbanceRecord,
    amplitude: EnvelopeAmplitude,
    state: EnvelopeEmissionState,
    node_cost: int,
    source_id: int,
    cause_id: int | None,
    scale: EnvelopeScale | None = None,
) -> PendingEnvelopeEmission:
    """Freeze one local source cycle; the caller supplies its commit clock."""
    meter = CostMeter(initial.operation_costs)
    meter.charge("read")
    residuals, phases, remaining = list(state.remainders), list(state.phases), list(state.remaining)
    populations: list[SpatialPopulations] = [
        (pack((0,) * initial.fields[definition.field].components),) * 8
        for definition in initial.spatial_fields
    ]
    source = [[0] * field.components for field in initial.fields]
    funded = [[0] * field.components for field in initial.fields]
    for index, rule in enumerate(initial.emissions):
        if not matches_type(rule, record.type_index):
            continue
        definition = initial.spatial_fields[rule.spatial_field]
        if definition.rays:
            raise ValueError("causal envelope emission currently requires octant spatial transport")
        field = initial.fields[definition.field]
        meter.charge("read")
        if not any(unpack(remaining[index])):
            continue
        proposed = evaluate(rule.amount, record.values, record.values, meter, node_cost=node_cost)
        amount, residuals[index], remaining[index] = weighted_emission(
            proposed,
            rule.denominator,
            amplitude,
            residuals[index],
            remaining[index],
            field,
            meter,
            scale,
        )
        emitted, phases[index] = emit(amount, phases[index], definition, field, meter)
        populations[rule.spatial_field] = add_populations(
            populations[rule.spatial_field], emitted, field, meter
        )
        for component, value in enumerate(unpack(amount)):
            source[definition.field][component] = checked_work(
                source[definition.field][component] + value
            )
            if rule.funded:
                funded[definition.field][component] = checked_work(
                    funded[definition.field][component] + value
                )
    # Reserve the final addition against current local stock now, before the
    # caller computes the delay. Its tariff is fixed by the field layout.
    for definition in initial.spatial_fields:
        field = initial.fields[definition.field]
        zero = (pack((0,) * field.components),) * 8
        add_populations(zero, zero, field, meter)
    meter.charge("commit")
    return PendingEnvelopeEmission(
        0,
        0,
        source_id,
        tuple(populations),
        tuple(tuple(values) for values in source),
        EnvelopeEmissionState(tuple(residuals), tuple(phases), tuple(remaining)),
        meter.total,
        cause_id,
        tuple(tuple(values) for values in funded),
    )


def deposit_populations(
    initial: SourceEmissionLaw, states: tuple[SpatialState, ...], populations: SpatialBundle
) -> tuple[SpatialState, ...]:
    """Add a committed local source to current local stock, retaining received input."""
    meter = CostMeter(initial.operation_costs)
    return tuple(
        SpatialState(
            add_populations(old.populations, added, initial.fields[definition.field], meter),
            old.allocation_phases,
            old.delivered,
            old.received_mask,
        )
        for old, added, definition in zip(states, populations, initial.spatial_fields, strict=True)
    )
