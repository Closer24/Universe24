"""The active input boundary permits fixed local operations, never supplied formulas."""

from .disturbance_state import (
    MAX_FIELDS,
    MAX_RULES,
    MAX_SLOTS,
    MAX_TYPES,
    MAX_VALUE,
    OPERATIONS,
    Address3,
    DisturbanceRecord,
    InitialState,
    Values,
    bounded,
    pack,
    unpack,
)
from .integer import checked_work


def _unique_names(names: tuple[str, ...]) -> None:
    if any(not isinstance(name, str) or not name.strip() or len(name) > 128 for name in names):
        raise ValueError("elementary names must be nonempty strings of at most 128 characters")
    if len(set(names)) != len(names):
        raise ValueError("duplicate elementary declaration name")


def _indices(indices: tuple[int, ...], size: int) -> None:
    if not 1 <= len(indices) <= size or len(set(indices)) != len(indices):
        raise ValueError("invalid elementary owned field count")
    if any(type(index) is not int or not 0 <= index < size for index in indices):
        raise ValueError("invalid elementary owned field index")


def _values(initial: InitialState, values: Values, owned: tuple[int, ...]) -> None:
    if len(values) != len(initial.fields):
        raise ValueError("elementary values must match the fixed field count")
    for index, (field, value) in enumerate(zip(initial.fields, values, strict=True)):
        field.validate(value)
        if index not in owned and any(unpack(value)):
            raise ValueError("an elementary carrier cannot store an unowned field")


def _position(position: Address3, shape: Address3) -> None:
    if len(position) != 3 or any(not 0 <= bounded(v) < n for v, n in zip(position, shape, strict=True)):
        raise ValueError("elementary seed must be inside the world")


def _structure(initial: InitialState) -> None:
    """Match JSON declaration limits before allocating any physical cell state."""
    limits = (
        (initial.fields, MAX_FIELDS, 1),
        (initial.disturbances, MAX_TYPES, 1),
        (initial.spatial_fields, MAX_FIELDS, 0),
        (initial.field_groups, MAX_FIELDS, 0),
        (initial.emissions, MAX_RULES, 0),
        (initial.elementary_exchanges, MAX_RULES, 0),
    )
    if any(not minimum <= len(items) <= maximum for items, maximum, minimum in limits):
        raise ValueError("elementary schema exceeds its fixed local capacity")
    _unique_names((initial.model_id,))
    if len(initial.shape) != 3 or any(bounded(v) < 1 for v in initial.shape):
        raise ValueError("elementary shape requires three positive dimensions")
    if not 1 <= bounded(initial.slots_per_cell) <= MAX_SLOTS:
        raise ValueError("elementary resident capacity exceeded")
    if (
        bounded(initial.link_ticks) < 1
        or bounded(initial.normal_budget) < 1
        or bounded(initial.ticks) < 0
    ):
        raise ValueError("invalid elementary clock or duration")
    if initial.boundary not in ("periodic", "open"):
        raise ValueError("invalid elementary boundary")
    if len(initial.operation_costs.prices) != len(OPERATIONS) or any(
        bounded(v) < 1 for v in initial.operation_costs.prices
    ):
        raise ValueError("elementary operation tariffs must be positive and fixed size")
    _unique_names(tuple(field.name for field in initial.fields))
    for field in initial.fields:
        _unique_names((field.units,))
        if (
            type(field.components) is not int
            or field.components not in (1, 3)
            or bounded(field.scale) < 1
        ):
            raise ValueError("invalid elementary field shape or scale")
        if any(type(flag) is not bool for flag in (field.signed, field.conserved, field.extensive)) or (
            field.conserved and not field.extensive
        ):
            raise ValueError("invalid elementary field flags")
    _unique_names(tuple(kind.name for kind in initial.disturbances))
    for kind in initial.disturbances:
        _indices(kind.fields, len(initial.fields))
        _values(initial, kind.defaults, kind.fields)
        transport = kind.transport
        if transport.mode not in ("hold", "move", "split") or transport.routing not in (
            "cyclic",
            "balanced",
        ):
            raise ValueError("invalid elementary transport mode or routing")
        if len(transport.weights) != 6 or any(bounded(v) < 0 for v in transport.weights):
            raise ValueError("invalid elementary transport weights")
        total = checked_work(sum(transport.weights))
        if (
            total < 1
            or (transport.routing == "cyclic" and total > MAX_VALUE)
            or bounded(transport.rate_denominator) < 1
        ):
            raise ValueError("invalid elementary transport sum or denominator")
        if transport.mode != "move" and (
            transport.direction_field is not None
            or transport.rate is not None
            or transport.rate_denominator != 1
            or transport.routing != "cyclic"
        ):
            raise ValueError("elementary movement settings require move transport")
        if transport.mode == "hold" and transport.weights != (1,) * 6:
            raise ValueError("held elementary carriers cannot select routing weights")
        if transport.mode == "split" and any(not initial.fields[i].extensive for i in kind.fields):
            raise ValueError("elementary split accepts only extensive fields")
        if transport.direction_field is not None:
            direction = transport.direction_field
            if (
                type(direction) is not int
                or direction not in kind.fields
                or initial.fields[direction].components != 3
                or transport.weights != (1,) * 6
            ):
                raise ValueError("elementary direction requires an owned vector and one provider")
        if kind.cost_field is not None:
            index = kind.cost_field
            if (
                type(index) is not int
                or index not in kind.fields
                or initial.fields[index].components != 1
                or initial.fields[index].conserved
                or transport.mode != "hold"
            ):
                raise ValueError("elementary cost reporter requires an owned nonconserved held scalar")
    spatial_indices = tuple(d.field for d in initial.spatial_fields)
    if spatial_indices:
        _indices(spatial_indices, len(initial.fields))
    _unique_names(tuple(group.name for group in initial.field_groups))
    for group in initial.field_groups:
        _indices(group.fields, len(initial.fields))


def _seeds(initial: InitialState) -> None:
    """Typed initialization has the same fresh-seed vocabulary as ordinary JSON."""
    occupied: dict[Address3, int] = {}
    phases = tuple(pack((0,) * field.components) for field in initial.fields)
    for seed in initial.seeds:
        _position(seed.position, initial.shape)
        occupied[seed.position] = occupied.get(seed.position, 0) + 1
        if occupied[seed.position] > initial.slots_per_cell:
            raise ValueError("initial elementary seeds exceed resident capacity")
        record = seed.record
        if type(record.type_index) is not int or not 0 <= record.type_index < len(initial.disturbances):
            raise ValueError("invalid elementary seed type")
        _values(initial, record.values, initial.disturbances[record.type_index].fields)
        if record != DisturbanceRecord(record.type_index, record.values, phases):
            raise ValueError("elementary initialization requires fresh bounded seed bookkeeping")
    spatial_occupied = set()
    for spatial_seed in initial.spatial_seeds:
        _position(spatial_seed.position, initial.shape)
        index = spatial_seed.spatial_field
        if (
            type(index) is not int
            or not 0 <= index < len(initial.spatial_fields)
            or len(spatial_seed.populations) != 8
        ):
            raise ValueError("invalid elementary spatial seed owner or population count")
        key = (spatial_seed.position, index)
        if key in spatial_occupied:
            raise ValueError("duplicate elementary spatial seed")
        spatial_occupied.add(key)
        definition = initial.spatial_fields[index]
        field = initial.fields[definition.field]
        total = list(unpack(definition.baseline))
        for payload in spatial_seed.populations:
            field.validate(payload)
            for component, value in enumerate(unpack(payload)):
                total[component] = checked_work(total[component] + value)
        field.validate(pack(tuple(total)))


def validate_elementary(initial: InitialState) -> None:
    """Also enforce the boundary for typed callers that bypass the JSON parser."""
    if type(initial.schema_version) is not int or initial.schema_version != 3:
        raise ValueError(
            "ordinary simulation requires elementary schema 3; use the explicit reference API for supplied laws"
        )
    if any(
        (
            initial.couplings,
            initial.interactions,
            initial.spatial_couplings,
            initial.field_rules,
            initial.spatial_interactions,
            initial.event_program,
        )
    ):
        raise ValueError("elementary initialization cannot contain expression rules or event programs")
    _structure(initial)
    for kind in initial.disturbances:
        if kind.updates or kind.checks:
            raise ValueError("elementary disturbances cannot contain update or check expressions")
        transport = kind.transport
        if transport.direction is not None or transport.rate_divisor is not None:
            raise ValueError("elementary transport cannot evaluate a supplied expression")
        if transport.rate is not None and (
            transport.rate.op != "literal"
            or transport.rate.arguments
            or len(transport.rate.literal) != 1
        ):
            raise ValueError("elementary movement rate must be a constant integer")
        if transport.rate is not None:
            if bounded(transport.rate.literal[0]) < 0:
                raise ValueError("elementary movement rate cannot be negative")
        if kind.cost_field is not None:
            if any(kind.cost_field == rule.field for rule in initial.elementary_exchanges):
                raise ValueError("a cost reporter cannot participate in an exchange")
            if transport.direction_field == kind.cost_field:
                raise ValueError("a cost reporter cannot control routing")
    spatial = {item.field: item for item in initial.spatial_fields}
    for definition in initial.spatial_fields:
        field = initial.fields[definition.field]
        field.validate(definition.baseline)
        if definition.axis_weights != (1, 1, 1) or definition.octant_weights != (1,) * 8:
            raise ValueError("elementary fields cannot select reference propagation parameters")
        if definition.transport != "local" or not field.extensive:
            raise ValueError("elementary spatial fields require local extensive stock")
        if type(definition.computation_delay) is not bool:
            raise ValueError("computation_delay must be a boolean")
        weights = definition.routing_weights
        if len(weights) != 6 or any(bounded(v) < 0 for v in weights) or bounded(sum(weights)) < 1:
            raise ValueError(
                "elementary fields require six nonnegative routing weights with a positive bounded sum"
            )
        decay = definition.decay
        if decay is None or not 0 <= bounded(decay.retain_numerator) < bounded(decay.retain_denominator):
            raise ValueError("every elementary spatial field requires finite decay")
    emission_owners = set()
    for emission in initial.emissions:
        if (
            type(emission.type_index) is not int
            or type(emission.spatial_field) is not int
            or not 0 <= emission.type_index < len(initial.disturbances)
            or not 0 <= emission.spatial_field < len(initial.spatial_fields)
        ):
            raise ValueError("invalid elementary emission owner")
        kind = initial.disturbances[emission.type_index]
        owner = (emission.type_index, emission.spatial_field)
        if (
            owner in emission_owners
            or kind.transport.mode == "split"
            or bounded(emission.denominator) < 1
        ):
            raise ValueError("duplicate emission or invalid elementary emission transport/denominator")
        emission_owners.add(owner)
        field = initial.fields[initial.spatial_fields[emission.spatial_field].field]
        amount = emission.amount
        if amount.arguments or amount.op not in ("literal", "field") or amount.side != 0:
            raise ValueError("elementary emission accepts only a literal or a carried field value")
        if amount.op == "field" and (
            type(amount.field) is not int
            or amount.field not in kind.fields
            or amount.field == kind.cost_field
        ):
            raise ValueError("elementary emission requires an owned physical field")
        if amount.op == "literal":
            field.validate(pack(amount.literal))
        elif initial.fields[amount.field].components != field.components:
            raise ValueError("elementary emission field shapes must agree")
        if (
            emission.budget is None
            or len(emission.budget) != field.components
            or any(value < 0 for value in unpack(emission.budget))
        ):
            raise ValueError("elementary emission requires a finite nonnegative allowance")
    names = set()
    owners = set()
    for rule in initial.elementary_exchanges:
        _unique_names((rule.name,))
        if rule.name in names or (rule.type_index, rule.field) in owners:
            raise ValueError("duplicate elementary exchange")
        names.add(rule.name)
        owners.add((rule.type_index, rule.field))
        if (
            type(rule.type_index) is not int
            or type(rule.field) is not int
            or not 0 <= rule.type_index < len(initial.disturbances)
            or rule.field not in spatial
        ):
            raise ValueError("elementary exchange requires a carrier and a local field")
        kind = initial.disturbances[rule.type_index]
        field = initial.fields[rule.field]
        if rule.field not in kind.fields or kind.transport.mode == "split":
            raise ValueError("elementary exchange requires an owned whole-record field")
        if any(unpack(spatial[rule.field].baseline)) or not field.signed:
            raise ValueError("elementary exchange requires signed stock with zero baseline")
        if (
            not rule.components
            or len(set(rule.components)) != len(rule.components)
            or any(type(c) is not int or not 0 <= c < field.components for c in rule.components)
        ):
            raise ValueError("invalid elementary exchange components")
        if len(rule.budget) != field.components or any(v < 0 for v in unpack(rule.budget)):
            raise ValueError("elementary exchange requires one finite allowance per component")
    _seeds(initial)
