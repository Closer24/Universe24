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
from .spatial_state import (
    BIT_THING,
    PORT_HEADINGS,
    FieldInteractionGuard,
    Rays,
    SpatialBundle,
    SpatialPlan,
    SpatialState,
)


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
        record.emission_last,
        record.emission_departed,
        record.absorbed_phases,
        record.dissolve_clocks,
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
    verified: tuple[DisturbanceRecord, ...] = (),
) -> None:
    """Validate each record once per boundary crossing.

    ``trusted`` holds the current slot contents: an unchanged slot needs no
    second pass. ``verified`` holds immutable record objects the caller already
    validated during this same crossing, such as delivered packets that a record
    policy places into free slots. Object identity certifies them; an equal but
    distinct record, including a merged one, is still validated.
    """
    _tuple(records, initial.slots_per_node, capacity)
    if records is trusted:
        return
    verified_ids = {id(record) for record in verified}
    for slot, record in enumerate(records):
        if record is None or (slot < len(trusted) and record is trusted[slot]):
            continue
        if id(record) in verified_ids:
            continue
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
    if plan.resolution_token is not None and bounded(plan.resolution_token) < 0:
        raise ValueError("node I/O resolution token must be nonnegative")
    _tuple(plan.spatial_guards, capacity * len(initial.spatial_interactions))
    for guard in plan.spatial_guards:
        if type(guard) is not FieldInteractionGuard:
            raise ValueError("node I/O requires an immutable field guard")
        _index(guard.slot, capacity)
        _index(guard.rule_index, len(initial.spatial_interactions))
        _values(initial, guard.before, encoded=True)
        _values(initial, guard.after, encoded=True)
        _values(initial, guard.delta, encoded=False)
        rule = initial.spatial_interactions[guard.rule_index]
        count = len(rule.participants)
        _tuple(guard.slots, capacity, count)
        _tuple(guard.participant_before, capacity, count)
        _tuple(guard.participant_after, capacity, count)
        slots = guard.slots or (guard.slot,)
        if len(set(slots)) != len(slots) or not set(slots) <= replaced:
            raise ValueError("pending spatial interaction must lock every distinct participant")
        if count:
            if guard.slot != slots[0]:
                raise ValueError("pending spatial interaction first slot differs from its group")
            if guard.before != guard.participant_before[0] or guard.after != guard.participant_after[0]:
                raise ValueError("pending spatial interaction first snapshot differs from its group")
            for slot, before, after in zip(
                slots, guard.participant_before, guard.participant_after, strict=True
            ):
                _index(slot, capacity)
                _values(initial, before, encoded=True)
                _values(initial, after, encoded=True)


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
    validate_plan_rays(initial, plan)


def validate_plan_rays(initial: InitialState, plan: SpatialPlan) -> None:
    """Outgoing rays: six ports, one tuple per spatial field, each validated."""
    has_rays = any(definition.rays for definition in initial.spatial_fields)
    validate_ray_bundle(initial, plan.kept_rays, optional=True)
    _tuple(plan.rays, port_count(initial))
    if not plan.rays:
        if has_rays:
            raise ValueError("ray transport requires outgoing rays for every port")
        return
    if not has_rays:
        raise ValueError("outgoing rays require a ray transport field")
    degree = port_count(initial)
    _tuple(plan.rays, degree, degree)
    for port_rays in plan.rays:
        validate_ray_bundle(initial, port_rays)
        # A Port is two lanes (lanes-v1, Highlights 5.4 point 25): an out-lane
        # carries at most one real ray per interval, whatever its family; the
        # lane is one direction of a Port, so a ray on one of the six Port lines.
        reals = sum(
            1
            for definition, family_rays in zip(initial.spatial_fields, port_rays, strict=True)
            for ray in family_rays
            if ray.detector == BIT_THING and definition.headings[ray.heading] in PORT_HEADINGS
        )
        if reals > 1:
            raise ValueError("two real rays on one lane (Highlights 5.4, point 25)")


def validate_ray_bundle(
    initial: InitialState, bundle: tuple[Rays, ...], *, optional: bool = False
) -> None:
    """Validate a complete incoming, retained or outgoing owner before filtering it."""
    from .spatial_state import validate_rays

    count = len(initial.spatial_fields)
    _tuple(bundle, count)
    if optional and not bundle:
        return
    _tuple(bundle, count, count)
    for definition, rays in zip(initial.spatial_fields, bundle, strict=True):
        if rays and not definition.rays:
            raise ValueError("rays on a field without ray transport")
        validate_rays(rays, definition, initial.fields[definition.field])
