"""Passive local I/O validation; no world, graph, callbacks or physical laws.

Validate proposals before retaining them. Exact immutable containers prevent
accidental mutable aliases; this is not a sandbox for hostile Python code.
"""

from .disturbance_state import (
    MAX_COMPONENTS,
    MAX_RULES,
    MAX_VALUE,
    Departure,
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    Values,
    bounded,
)
from .node_services import port_count
from .spatial_state import FieldInteractionGuard, SpatialBundle, SpatialPlan, SpatialState


def _tuple(value: object, maximum: int, size: int | None = None) -> None:
    if type(value) is not tuple or len(value) > maximum or (size is not None and len(value) != size):
        raise ValueError("node I/O requires an immutable tuple of the configured size")


def _index(value: int, size: int) -> None:
    if type(value) is not int or not 0 <= value < size:
        raise ValueError("node I/O index exceeds local capacity")


def _codes(values: tuple[int, ...], maximum: int) -> None:
    _tuple(values, maximum)
    for value in values:
        if type(value) is not int or not 1 <= value <= 2 * MAX_VALUE + 1:
            raise ValueError("node I/O requires bounded positive integer codes")


def _values(initial: InitialState, values: Values, *, encoded: bool, optional: bool = False) -> None:
    _tuple(values, len(initial.fields))
    if optional and not values:
        return
    if len(values) != len(initial.fields):
        raise ValueError("node I/O field count differs from initialization")
    for field, payload in zip(initial.fields, values, strict=True):
        _tuple(payload, field.components, field.components)
        if encoded:
            field.validate(payload)
        else:
            for component in payload:
                bounded(component)


def validate_record(initial: InitialState, record: DisturbanceRecord) -> None:
    if type(record) is not DisturbanceRecord:
        raise ValueError("node I/O requires an immutable disturbance record")
    _index(record.type_index, len(initial.disturbances))
    _values(initial, record.values, encoded=True)
    _tuple(record.phase_codes, len(initial.fields), len(initial.fields))
    for field, codes in zip(initial.fields, record.phase_codes, strict=True):
        _tuple(codes, field.components, field.components)
    for rows in (
        record.phase_codes,
        record.emission_remainders,
        record.emission_phases,
        record.exchange_remainders,
        record.spatial_remainders,
        record.emission_remaining,
        record.spatial_remaining,
    ):
        _tuple(rows, max(len(initial.fields), MAX_RULES))
        for row in rows:
            _codes(row, MAX_COMPONENTS)
    for codes in (record.route_count_codes, record.route_weight_codes):
        _tuple(codes, port_count(initial), port_count(initial))
        _codes(codes, port_count(initial))
    _codes((record.route_phase_code, record.rate_remainder_code, record.channel_code), 3)
    _index(record.channel_code - 1, port_count(initial) + 1)
    if bounded(record.rate_credit_denominator) < 1:
        raise ValueError("node I/O rate denominator must be positive")


def validate_records(
    initial: InitialState,
    records: tuple[DisturbanceRecord | None, ...],
    capacity: int,
    trusted: tuple[DisturbanceRecord | None, ...] = (),
) -> None:
    _tuple(records, initial.slots_per_node, capacity)
    if records is trusted:
        return
    for slot, record in enumerate(records):
        if slot < len(trusted) and record is trusted[slot]:
            continue
        if record is not None:
            validate_record(initial, record)


def validate_local_plan(
    initial: InitialState,
    plan: LocalPlan,
    residual_count: int,
    trusted: tuple[DisturbanceRecord | None, ...] = (),
) -> None:
    if type(plan) is not LocalPlan:
        raise ValueError("node I/O requires an immutable local proposal")
    capacity = initial.slots_per_node
    _tuple(plan.replacements, capacity)
    replaced: set[int] = set()
    for replacement in plan.replacements:
        _tuple(replacement, 2, 2)
        slot, record = replacement
        _index(slot, capacity)
        if slot in replaced:
            raise ValueError("node I/O proposal replaces a local slot twice")
        replaced.add(slot)
        if record is not None and not (slot < len(trusted) and record is trusted[slot]):
            validate_record(initial, record)
    _tuple(plan.departures, capacity * port_count(initial))
    for departure in plan.departures:
        if type(departure) is not Departure:
            raise ValueError("node I/O departure must select a local port")
        _index(departure.port, port_count(initial))
        if type(departure.origin_slot) is not int or departure.origin_slot != -1:
            _index(departure.origin_slot, capacity)
        validate_record(initial, departure.record)
    _tuple(plan.coupling_remainders, residual_count, residual_count)
    _codes(plan.coupling_remainders, residual_count)
    _values(initial, plan.source_delta, encoded=False, optional=True)
    _values(initial, plan.spatial_reaction, encoded=False, optional=True)
    if bounded(plan.cost) < 0:
        raise ValueError("node I/O cost must be nonnegative")
    if bounded(plan.interaction_ticks) < 0:
        raise ValueError("node I/O interaction duration must be nonnegative")
    if plan.cause_id is not None and bounded(plan.cause_id) < 0:
        raise ValueError("node I/O cause must be nonnegative")
    _tuple(plan.spatial_guards, capacity * len(initial.spatial_interactions))
    for guard in plan.spatial_guards:
        if type(guard) is not FieldInteractionGuard:
            raise ValueError("node I/O requires an immutable field guard")
        _index(guard.slot, capacity)
        _index(guard.rule_index, len(initial.spatial_interactions))
        _values(initial, guard.before, encoded=True)
        _values(initial, guard.after, encoded=True)
        _values(initial, guard.delta, encoded=False)


def validate_spatial_states(initial: InitialState, states: tuple[SpatialState, ...]) -> None:
    count, degree = len(initial.spatial_fields), port_count(initial)
    _tuple(states, count, count)
    for definition, state in zip(initial.spatial_fields, states, strict=True):
        if type(state) is not SpatialState:
            raise ValueError("node I/O requires immutable spatial state")
        field = initial.fields[definition.field]
        for rows, size in (
            (state.populations, 8),
            (state.allocation_phases, 8),
            (state.delivered, degree),
        ):
            _tuple(rows, size, size)
            for payload in rows:
                _tuple(payload, field.components, field.components)
        state.validate(field.components)
        for payload in state.populations:
            field.validate(payload)


def validate_spatial_bundle(initial: InitialState, bundle: SpatialBundle) -> None:
    count = len(initial.spatial_fields)
    _tuple(bundle, count, count)
    for definition, populations in zip(initial.spatial_fields, bundle, strict=True):
        _tuple(populations, 8, 8)
        field = initial.fields[definition.field]
        for payload in populations:
            _tuple(payload, field.components, field.components)
            field.validate(payload)


def validate_spatial_outgoing(initial: InitialState, outgoing: tuple[SpatialBundle, ...]) -> None:
    _tuple(outgoing, port_count(initial), port_count(initial))
    for bundle in outgoing:
        validate_spatial_bundle(initial, bundle)


def validate_samples(
    initial: InitialState, values: Values, fluxes: Values, ports: tuple[Values, ...]
) -> None:
    _values(initial, values, encoded=True)
    _tuple(fluxes, len(initial.fields), len(initial.fields))
    for payload in fluxes:
        _tuple(payload, 3, 3)
        _codes(payload, 3)
    _tuple(ports, port_count(initial))
    if ports:
        _tuple(ports, port_count(initial), port_count(initial))
        for sample in ports:
            _values(initial, sample, encoded=True)


def validate_reaction_state(
    initial: InitialState, states: tuple[SpatialState, ...], phases: Values
) -> None:
    validate_spatial_states(initial, states)
    _tuple(phases, len(initial.spatial_fields), len(initial.spatial_fields))
    for definition, payload in zip(initial.spatial_fields, phases, strict=True):
        components = initial.fields[definition.field].components
        _tuple(payload, components, components)
        _codes(payload, components)


def validate_decay(initial: InitialState, bundle: SpatialBundle, loss: Values, cost: int) -> None:
    validate_spatial_bundle(initial, bundle)
    _values(initial, loss, encoded=False)
    if bounded(cost) < 0:
        raise ValueError("node I/O decay cost must be nonnegative")


def validate_spatial_plan(
    initial: InitialState,
    plan: SpatialPlan,
    resident_count: int,
    trusted: tuple[DisturbanceRecord | None, ...] = (),
) -> None:
    if type(plan) is not SpatialPlan:
        raise ValueError("node I/O requires an immutable spatial proposal")
    validate_spatial_states(initial, plan.states)
    validate_spatial_outgoing(initial, plan.outgoing)
    validate_records(initial, plan.emission_records, resident_count, trusted)
    _values(initial, plan.source_delta, encoded=False)
    _values(initial, plan.rule_delta, encoded=False, optional=True)
    if bounded(plan.cost) < 0:
        raise ValueError("node I/O cost must be nonnegative")
    if bounded(plan.interaction_ticks) < 0:
        raise ValueError("node I/O interaction duration must be nonnegative")
