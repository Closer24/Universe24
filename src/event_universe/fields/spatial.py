"""Pure bounded emission and monotonic transport for generic spatial fields."""

from dataclasses import replace

from event_universe.core.disturbance_state import (
    CostMeter,
    FieldDefinition,
    Payload,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import add_components, checked_work, signed_divrem
from event_universe.core.spatial_state import (
    SpatialFieldDefinition,
    SpatialOutgoing,
    SpatialPopulations,
    SpatialState,
    zero_spatial_state,
)

OCTANT_SIGNS: tuple[tuple[int, int, int], ...] = (
    (1, 1, 1),
    (1, 1, -1),
    (1, -1, 1),
    (1, -1, -1),
    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
)


def _weight_sum(weights: tuple[int, ...]) -> int:
    if not 1 <= len(weights) <= 8:
        raise ValueError("a spatial partition requires one through eight weights")
    for weight in weights:
        if bounded(weight) < 0:
            raise ValueError("spatial weights must be nonnegative")
    denominator = bounded(checked_work(sum(weights)))
    if denominator == 0:
        raise ValueError("spatial weights require a positive total")
    return denominator


def split_weighted(amount: int, weights: tuple[int, ...], phase: int) -> tuple[tuple[int, ...], int]:
    """Partition every signed unit; the phase only selects indivisible destinations."""
    bounded(amount)
    denominator = _weight_sum(weights)
    if not 0 <= bounded(phase) < denominator:
        raise ValueError("spatial allocation phase must be below the weight total")
    magnitude = abs(amount)
    sign = -1 if amount < 0 else 1
    start_whole, start_tail = divmod(phase, denominator)
    end_whole, end_tail = divmod(checked_work(phase + magnitude), denominator)
    offset = 0
    portions = []
    for weight in weights:
        before = checked_work(start_whole * weight + min(weight, max(0, start_tail - offset)))
        after = checked_work(end_whole * weight + min(weight, max(0, end_tail - offset)))
        portions.append(bounded(sign * (after - before)))
        offset += weight
    return tuple(portions), (phase + magnitude) % denominator


def _validate_definition(definition: SpatialFieldDefinition, field: FieldDefinition) -> None:
    if not field.extensive:
        raise ValueError("spatial transport requires an extensive field")
    field.validate(definition.baseline)
    if len(definition.axis_weights) != 3 or len(definition.octant_weights) != 8:
        raise ValueError("spatial definitions require three axis weights and eight octant weights")
    _weight_sum(definition.axis_weights)
    _weight_sum(definition.octant_weights)


def add_payloads(left: Payload, right: Payload, field: FieldDefinition, meter: CostMeter) -> Payload:
    """Validate each operand before combining it, so cancellation cannot hide invalid state."""
    field.validate(left)
    field.validate(right)
    meter.charge("read", 2)
    meter.charge("update", field.components)
    result = pack(add_components(unpack(left), unpack(right)))
    field.validate(result)
    return result


def add_populations(
    left: SpatialPopulations,
    right: SpatialPopulations,
    field: FieldDefinition,
    meter: CostMeter,
) -> SpatialPopulations:
    if len(left) != 8 or len(right) != 8:
        raise ValueError("spatial populations require exactly eight octants")
    return tuple(add_payloads(a, b, field, meter) for a, b in zip(left, right, strict=True))


def emission_amount(
    numerator: tuple[int, ...],
    residual: Payload,
    denominator: int,
    field: FieldDefinition,
    meter: CostMeter,
) -> tuple[Payload, Payload]:
    """Divide one local source numerator, retaining signed subunit emission residue."""
    if bounded(denominator) < 1:
        raise ValueError("emission denominator must be positive")
    if len(numerator) != field.components or len(residual) != field.components:
        raise ValueError("emission component count differs from the field")
    residues = unpack(residual)
    if any(abs(value) >= denominator for value in residues):
        raise ValueError("emission residual must be below its denominator")
    meter.charge("read")
    emitted, retained = [], []
    for value, old in zip(numerator, residues, strict=True):
        checked_work(value)
        meter.charge("update")
        quotient, remainder = signed_divrem(checked_work(value + old), denominator)
        emitted.append(quotient)
        retained.append(remainder)
    amount = pack(tuple(emitted))
    field.validate(amount)
    return amount, pack(tuple(retained))


def bounded_emission_amount(
    numerator: tuple[int, ...],
    residual: Payload,
    denominator: int,
    remaining: Payload,
    field: FieldDefinition,
    meter: CostMeter,
) -> tuple[Payload, Payload, Payload]:
    """Consume a finite absolute allowance; clipped demand creates no debt."""
    if bounded(denominator) < 1:
        raise ValueError("emission denominator must be positive")
    if any(len(value) != field.components for value in (numerator, residual, remaining)):
        raise ValueError("bounded emission component count differs from the field")
    residues, allowances = unpack(residual), unpack(remaining)
    if any(abs(value) >= denominator for value in residues):
        raise ValueError("emission residual must be below its denominator")
    if any(value < 0 for value in allowances):
        raise ValueError("emission allowance must be nonnegative")
    meter.charge("read", 2)
    emitted, retained, available = [], [], []
    for value, old, allowance in zip(numerator, residues, allowances, strict=True):
        checked_work(value)
        quotient, remainder = signed_divrem(checked_work(value + old), denominator)
        if not field.signed and quotient < 0:
            raise ValueError("unsigned field cannot emit a negative quantity")
        magnitude = min(abs(quotient), allowance)
        amount = -magnitude if quotient < 0 else magnitude
        left = allowance - magnitude
        emitted.append(amount)
        retained.append(remainder if left else 0)
        available.append(left)
        meter.charge("update", 3)
    result = pack(tuple(emitted))
    field.validate(result)
    return result, pack(tuple(retained)), pack(tuple(available))


def emit(
    amount: Payload,
    phases: Payload,
    definition: SpatialFieldDefinition,
    field: FieldDefinition,
    meter: CostMeter,
) -> tuple[SpatialPopulations, Payload]:
    """Distribute the explicit source amount over fixed octants without retaining stock."""
    _validate_definition(definition, field)
    field.validate(amount)
    if len(phases) != field.components:
        raise ValueError("emission phase component count differs from the field")
    meter.charge("read")
    buckets = [[0] * field.components for _ in range(8)]
    updated = []
    for component, (value, phase) in enumerate(zip(unpack(amount), unpack(phases), strict=True)):
        meter.charge("split")
        portions, next_phase = split_weighted(value, definition.octant_weights, phase)
        updated.append(next_phase)
        for octant, portion in enumerate(portions):
            buckets[octant][component] = portion
    return tuple(pack(tuple(bucket)) for bucket in buckets), pack(tuple(updated))


def split_outward(
    state: SpatialState,
    definition: SpatialFieldDefinition,
    field: FieldDefinition,
    meter: CostMeter,
) -> tuple[SpatialOutgoing, SpatialState]:
    """Send every population one octant-compatible edge, preserving its octant label.

    The caller schedules the fixed link time and owns all returned packets.
    Allocation phases stay local; delivered samples are unchanged projections.
    """
    _validate_definition(definition, field)
    state.validate(field.components)
    for payload in (*state.populations, *state.delivered):
        field.validate(payload)
    buckets = [[[0] * field.components for _ in range(8)] for _ in range(6)]
    updated = []
    for octant, payload in enumerate(state.populations):
        meter.charge("read")
        meter.charge("route")
        phases = []
        for component, (value, phase) in enumerate(
            zip(unpack(payload), unpack(state.allocation_phases[octant]), strict=True)
        ):
            meter.charge("split")
            portions, next_phase = split_weighted(value, definition.axis_weights, phase)
            phases.append(next_phase)
            for axis, portion in enumerate(portions):
                port = 2 * axis + (0 if OCTANT_SIGNS[octant][axis] > 0 else 1)
                buckets[port][octant][component] = portion
        updated.append(pack(tuple(phases)))
    outgoing = tuple(tuple(pack(tuple(payload)) for payload in port) for port in buckets)
    for port_values in buckets:
        if any(any(payload) for payload in port_values):
            meter.charge("send")
    cleared = zero_spatial_state(field.components)
    return outgoing, replace(state, populations=cleared.populations, allocation_phases=tuple(updated))
