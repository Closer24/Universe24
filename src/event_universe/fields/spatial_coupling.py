"""Bounded local field exchange and exact lattice rotations with opposite reaction."""

from collections.abc import Mapping
from dataclasses import dataclass, replace

from event_universe.core.coupling_selectors import matches_type
from event_universe.core.disturbance_state import (
    MAX_RULES,
    MAX_SLOTS,
    CostMeter,
    DisturbanceRecord,
    FieldDefinition,
    OperationCosts,
    Payload,
    Values,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work, dot_product, signed_divrem, subtract_components
from event_universe.core.spatial_state import (
    FieldInteractionGuard,
    SpatialCouplingDefinition,
    SpatialCouplingResult,
    SpatialFieldDefinition,
    SpatialState,
    zero_spatial_state,
)

from .disturbances import evaluate
from .spatial import add_populations, emission_amount, emit, split_outward


def sample_values(
    states: tuple[SpatialState, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter | None = None,
) -> Values:
    """Read only the resident spatial inventory and immutable local background."""
    if len(states) != len(definitions):
        raise ValueError("spatial sample state count differs from its definitions")
    result = [pack((0,) * field.components) for field in fields]
    for state, definition in zip(states, definitions, strict=True):
        field = fields[definition.field]
        state.validate(field.components)
        field.validate(definition.baseline)
        local = list(unpack(definition.baseline))
        for payload in state.populations:
            field.validate(payload)
            for component, value in enumerate(unpack(payload)):
                local[component] = checked_work(local[component] + value)
        result[definition.field] = pack(tuple(local))
        field.validate(result[definition.field])
        if meter is not None:
            meter.charge("read", 9)
            meter.charge("update", 8 * field.components)
    return tuple(result)


def sample_fluxes(
    states: tuple[SpatialState, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter | None = None,
) -> Values:
    """Project scalar delivered channels into a signed three-component travel vector."""
    if len(states) != len(definitions):
        raise ValueError("spatial flux state count differs from its definitions")
    result = [pack((0, 0, 0)) for _ in fields]
    for state, definition in zip(states, definitions, strict=True):
        field = fields[definition.field]
        if field.components != 1:
            continue
        state.validate(1)
        for payload in state.delivered:
            field.validate(payload)
        delivered = tuple(unpack(payload)[0] for payload in state.delivered)
        result[definition.field] = pack(
            tuple(checked_work(delivered[2 * axis] - delivered[2 * axis + 1]) for axis in range(3))
        )
        if meter is not None:
            meter.charge("read", 6)
            meter.charge("update", 3)
    return tuple(result)


def _reaction_phases(
    phases: Values,
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
) -> list[Payload]:
    if not phases:
        return [pack((0,) * fields[d.field].components) for d in definitions]
    if len(phases) != len(definitions):
        raise ValueError("reaction phase count differs from spatial definitions")
    for phase, definition in zip(phases, definitions, strict=True):
        if len(phase) != fields[definition.field].components:
            raise ValueError("reaction phase component count differs from the field")
        if any(not 0 <= value < sum(definition.octant_weights) for value in unpack(phase)):
            raise ValueError("reaction phase must be below its octant weight total")
    return list(phases)


def _validate_reaction(reaction: Values, fields: tuple[FieldDefinition, ...]) -> None:
    if len(reaction) != len(fields):
        raise ValueError("reaction field count differs from the configured schema")
    for values, field in zip(reaction, fields, strict=True):
        field.validate(pack(values))


def deposit_reaction(
    states: tuple[SpatialState, ...],
    phases: Values,
    reaction: Values,
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    *,
    validate_local: bool = True,
) -> tuple[tuple[SpatialState, ...], Values]:
    """Add opposite reaction to owned populations without declaring an external source."""
    if len(states) != len(definitions):
        raise ValueError("reaction state count differs from spatial definitions")
    _validate_reaction(reaction, fields)
    allowed = {definition.field for definition in definitions}
    if any(any(values) and index not in allowed for index, values in enumerate(reaction)):
        raise ValueError("reaction requires a declared spatial owner")
    updated, allocation = list(states), _reaction_phases(phases, definitions, fields)
    for index, definition in enumerate(definitions):
        if not any(reaction[definition.field]):
            continue
        field = fields[definition.field]
        if not field.signed or not field.extensive:
            raise ValueError("spatial reaction requires a signed extensive field")
        state = states[index]
        state.validate(field.components)
        populations, allocation[index] = emit(
            pack(reaction[definition.field]), allocation[index], definition, field, meter
        )
        combined = add_populations(state.populations, populations, field, meter)
        updated[index] = replace(state, populations=combined)
        if validate_local:
            sample_values((updated[index],), (definition,), fields)
    return tuple(updated), tuple(allocation)


def _rotate(
    value: tuple[int, ...],
    request: tuple[int, ...],
    residual: Payload,
    denominator: int,
    axes: tuple[int, int, int],
    meter: CostMeter,
) -> tuple[tuple[int, ...], Payload]:
    """Apply ordered quarter turns; an invariant axis leaves its counter unchanged."""
    if len(value) != 3 or len(request) != 3 or len(residual) != 3 or sorted(axes) != [0, 1, 2]:
        raise ValueError("lattice rotation requires three components and a valid axis order")
    if bounded(denominator) < 1:
        raise ValueError("rotation denominator must be positive")
    rotated = list(value)
    remainders = list(unpack(residual))
    planes = ((1, 2), (2, 0), (0, 1))
    for axis in axes:
        meter.charge("route")
        meter.charge("read", 2)
        first, second = planes[axis]
        a, b = rotated[first], rotated[second]
        if a == 0 and b == 0:
            continue
        quarter, remainders[axis] = signed_divrem(
            checked_work(request[axis] + remainders[axis]), denominator
        )
        meter.charge("update")
        turns = bounded(quarter) % 4
        if turns == 1:
            rotated[first], rotated[second] = -b, a
        elif turns == 2:
            rotated[first], rotated[second] = -a, -b
        elif turns == 3:
            rotated[first], rotated[second] = b, -a
        if turns:
            meter.charge("update", 2)
    before = dot_product(value, value)
    after = dot_product(tuple(rotated), tuple(rotated))
    if before != after:
        raise ValueError("lattice rotation changed the squared vector norm")
    return tuple(rotated), pack(tuple(remainders))


def _debit_allowance(remaining: Payload, change: tuple[int, ...], meter: CostMeter) -> Payload | None:
    """Reserve every absolute component together, without refunds for sign reversals."""
    available = unpack(remaining)
    if len(available) != len(change):
        raise ValueError("spatial coupling allowance component count differs from its change")
    meter.charge("read", len(change))
    meter.charge("update", len(change))
    spent = tuple(abs(checked_work(value)) for value in change)
    if any(amount > limit for amount, limit in zip(spent, available, strict=True)):
        return None
    meter.charge("update", len(change))
    return pack(tuple(limit - amount for amount, limit in zip(spent, available, strict=True)))


def _exchange_candidate(
    before: tuple[int, ...],
    request: tuple[int, ...],
    residual: Payload,
    denominator: int,
    meter: CostMeter,
) -> tuple[tuple[int, ...], Payload]:
    """Keep a finite candidate in work registers until its allowance is checked."""
    if bounded(denominator) < 1:
        raise ValueError("exchange denominator must be positive")
    if len(before) != len(request) or len(before) != len(residual):
        raise ValueError("exchange component count differs from its field")
    residues = unpack(residual)
    if any(abs(value) >= denominator for value in residues):
        raise ValueError("exchange residual must be below its denominator")
    meter.charge("read")
    proposed, remainders = [], []
    for value, numerator, remainder in zip(before, request, residues, strict=True):
        meter.charge("update")
        quotient, retained = signed_divrem(checked_work(numerator + remainder), denominator)
        proposed.append(checked_work(value - quotient))
        remainders.append(retained)
    return tuple(proposed), pack(tuple(remainders))


@dataclass(frozen=True, slots=True)
class SpatialCouplingLaw:
    fields: tuple[FieldDefinition, ...]
    definitions: tuple[SpatialCouplingDefinition, ...]
    costs: OperationCosts
    spatial_definitions: tuple[SpatialFieldDefinition, ...] = ()

    def sample(self, states: tuple[SpatialState, ...]) -> Values:
        return sample_values(states, self.spatial_definitions, self.fields)

    def sample_fluxes(self, states: tuple[SpatialState, ...]) -> Values:
        return sample_fluxes(states, self.spatial_definitions, self.fields)

    def sample_ports(self, states: tuple[SpatialState, ...]) -> tuple[Values, ...]:
        raise ValueError("port-aware interactions require a configured joint law")

    def sample_received_masks(self, states: tuple[SpatialState, ...]) -> tuple[int, ...]:
        from .local_field_rules import received_masks

        return received_masks(self.fields, self.spatial_definitions, states)

    def validate_guards(
        self,
        states: tuple[SpatialState, ...],
        reaction: Values,
        guards: tuple[FieldInteractionGuard, ...],
    ) -> None:
        if guards:
            raise ValueError("spatial interaction guards require a configured joint law")

    def deposit(
        self,
        states: tuple[SpatialState, ...],
        phases: Values,
        reaction: Values,
    ) -> tuple[tuple[SpatialState, ...], Values]:
        return deposit_reaction(
            states, phases, reaction, self.spatial_definitions, self.fields, CostMeter(self.costs)
        )

    def forward_reaction(
        self,
        states: tuple[SpatialState, ...],
        phases: Values,
        reaction: Values,
    ) -> tuple[tuple[SpatialState, ...], Values, tuple[tuple[tuple[Payload, ...], ...], ...]]:
        """Route reaction alone for a same-tick link append; preserve unrelated inventory."""
        blank = tuple(
            replace(state, populations=zero_spatial_state(self.fields[d.field].components).populations)
            for state, d in zip(states, self.spatial_definitions, strict=True)
        )
        meter = CostMeter(self.costs)
        deposited, next_phases = deposit_reaction(
            blank, phases, reaction, self.spatial_definitions, self.fields, meter, validate_local=False
        )
        updated = list(states)
        outgoing: list[list[tuple[Payload, ...]]] = [[] for _ in range(6)]
        for index, definition in enumerate(self.spatial_definitions):
            field = self.fields[definition.field]
            if any(reaction[definition.field]):
                channels, cleared = split_outward(deposited[index], definition, field, meter)
                updated[index] = replace(states[index], allocation_phases=cleared.allocation_phases)
            else:
                channels = (zero_spatial_state(field.components).populations,) * 6
            for port, populations in enumerate(channels):
                outgoing[port].append(populations)
        return tuple(updated), next_phases, tuple(tuple(bundle) for bundle in outgoing)

    def _remainders(self, record: DisturbanceRecord) -> Values:
        if not record.spatial_remainders:
            return tuple(pack((0,) * self.fields[d.field].components) for d in self.definitions)
        if len(record.spatial_remainders) != len(self.definitions):
            raise ValueError("spatial coupling remainder count differs from its rules")
        for payload, definition in zip(record.spatial_remainders, self.definitions, strict=True):
            if len(payload) != self.fields[definition.field].components:
                raise ValueError("spatial coupling remainder component count differs from its field")
            residuals = unpack(payload)
            if any(abs(value) >= definition.denominator for value in residuals):
                raise ValueError("spatial coupling residual must be below its denominator")
            if not matches_type(definition, record.type_index) and any(residuals):
                raise ValueError("record does not own another type's spatial coupling remainder")
        return record.spatial_remainders

    def _remaining(self, record: DisturbanceRecord) -> Values:
        limits = []
        for definition in self.definitions:
            field = self.fields[definition.field]
            limit = pack((0,) * field.components)
            if definition.budget is not None:
                field.validate(definition.budget)
                if any(value < 0 for value in unpack(definition.budget)):
                    raise ValueError("spatial coupling budget must be nonnegative")
                if matches_type(definition, record.type_index):
                    limit = definition.budget
            limits.append(limit)
        if not record.spatial_remaining:
            return tuple(limits)
        if len(record.spatial_remaining) != len(self.definitions):
            raise ValueError("spatial coupling allowance count differs from its rules")
        for remaining, limit in zip(record.spatial_remaining, limits, strict=True):
            if len(remaining) != len(limit):
                raise ValueError("spatial coupling allowance component count differs from its field")
            if any(
                not 0 <= value <= initial
                for value, initial in zip(unpack(remaining), unpack(limit), strict=True)
            ):
                raise ValueError("spatial coupling allowance exceeds its owned initial budget")
        return record.spatial_remaining

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
        if len(records) > MAX_SLOTS or len(self.definitions) > MAX_RULES:
            raise ValueError("spatial coupling exceeds the fixed local capacity")
        if len(sample) != len(self.fields):
            raise ValueError("spatial sample field count differs from its schema")
        for field, payload in zip(self.fields, sample, strict=True):
            field.validate(payload)
        if fluxes:
            if len(fluxes) != len(self.fields) or any(len(payload) != 3 for payload in fluxes):
                raise ValueError("spatial flux samples require one vector per configured field")
            for payload in fluxes:
                unpack(payload)
        meter = CostMeter(self.costs)
        for spatial_definition in self.spatial_definitions:
            components = self.fields[spatial_definition.field].components
            meter.charge("read", 9 + (6 if components == 1 else 0))
            meter.charge("update", 8 * components + (3 if components == 1 else 0))
        updated = list(records)
        reaction = [[0] * field.components for field in self.fields]
        for index, definition in enumerate(self.definitions):
            field = self.fields[definition.field]
            if (
                not field.signed
                or not field.extensive
                or definition.mode not in ("exchange", "rotation")
            ):
                raise ValueError(
                    "spatial coupling requires a signed extensive field and a supported mode"
                )
            if definition.mode == "rotation" and field.components != 3:
                raise ValueError("spatial rotation requires a three-component target")
            for slot, record in enumerate(updated):
                if record is None or not matches_type(definition, record.type_index):
                    continue
                if len(record.values) != len(self.fields):
                    raise ValueError("record field count differs from spatial coupling schema")
                for owned_field, payload in zip(self.fields, record.values, strict=True):
                    owned_field.validate(payload)
                residuals = list(self._remainders(record))
                meter.charge("read")
                meter.charge("couple")
                remaining = record.spatial_remaining
                if remaining or definition.budget is not None:
                    remaining = self._remaining(record)
                if definition.budget is not None:
                    record = replace(record, spatial_remaining=remaining)
                    updated[slot] = record
                    meter.charge("read", field.components)
                    if not any(unpack(remaining[index])):
                        continue
                local_sample = sample if not slot_samples else slot_samples.get(slot, sample)
                local_fluxes = fluxes if not slot_fluxes else slot_fluxes.get(slot, fluxes)
                request = evaluate(
                    definition.expression, record.values, local_sample, meter, local_fluxes
                )
                before = unpack(record.values[definition.field])
                if definition.mode == "rotation":
                    after, residuals[index] = _rotate(
                        before,
                        request,
                        residuals[index],
                        definition.denominator,
                        definition.axis_order,
                        meter,
                    )
                elif definition.budget is not None:
                    after, residuals[index] = _exchange_candidate(
                        before, request, residuals[index], definition.denominator, meter
                    )
                else:
                    fraction, residuals[index] = emission_amount(
                        request, residuals[index], definition.denominator, field, meter
                    )
                    after = subtract_components(before, unpack(fraction))
                if definition.budget is not None:
                    change = subtract_components(before, after)
                    reserved = _debit_allowance(remaining[index], change, meter)
                    if reserved is None:
                        continue
                    allowances = list(remaining)
                    allowances[index] = reserved
                    remaining = tuple(allowances)
                value = pack(after)
                field.validate(value)
                meter.charge("update", field.components)
                for component, (old, new) in enumerate(zip(before, after, strict=True)):
                    delta = bounded(checked_work(old - new))
                    reaction[definition.field][component] = bounded(
                        checked_work(reaction[definition.field][component] + delta)
                    )
                    meter.charge("update")
                values = list(record.values)
                values[definition.field] = value
                updated[slot] = replace(
                    record,
                    values=tuple(values),
                    spatial_remainders=tuple(residuals),
                    spatial_remaining=remaining,
                )
        # This fixed six-face preparation tariff is a model reservation, not an
        # exact count of the later commit branch or host instructions. Ordinary
        # later field forwarding is priced in its own stage without changing this
        # frozen response cost; see docs/SPATIAL_COUPLINGS.md.
        for field, amount in zip(self.fields, reaction, strict=True):
            if any(amount):
                meter.charge("read", 121)
                meter.charge("split", 9 * field.components)
                meter.charge("update", 56 * field.components)
                meter.charge("route", 8)
                meter.charge("send", 6)
        return SpatialCouplingResult(tuple(updated), tuple(tuple(v) for v in reaction), meter.total)
