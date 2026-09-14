"""Pure local emission and outward transport assembled from generic primitives."""

from dataclasses import dataclass, replace

from event_universe.core.coupling_selectors import matches_type, selected_types
from event_universe.core.disturbance_state import (
    CostMeter,
    DisturbanceRecord,
    FieldDefinition,
    OperationCosts,
    Values,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    TICKET_MODULUS,
    EmissionDefinition,
    FieldRuleGuard,
    NodeFieldRuleDefinition,
    Ray,
    Rays,
    SpatialCouplingDefinition,
    SpatialFieldDefinition,
    SpatialOutgoing,
    SpatialPlan,
    SpatialPopulations,
    SpatialState,
    advance_ray,
    coherence,
    next_ticket,
    phase_of_sum,
    ray_salt,
    ray_stock,
)

from .disturbances import evaluate
from .local_field_rules import apply_field_rules, validate_field_guards
from .rays import emit_rays, forward_rays, validate_ray_definition
from .spatial import add_populations, bounded_emission_amount, emission_amount, emit, split_outward


@dataclass(frozen=True, slots=True)
class SpatialLaw:
    fields: tuple[FieldDefinition, ...]
    definitions: tuple[SpatialFieldDefinition, ...]
    emissions: tuple[EmissionDefinition, ...]
    costs: OperationCosts
    field_rules: tuple[NodeFieldRuleDefinition, ...] = ()
    absorptions: tuple[SpatialCouplingDefinition, ...] = ()

    def _own_departed_keys(
        self, record: DisturbanceRecord, index: int, meter: CostMeter
    ) -> set[tuple[int, tuple[int, int, int]]]:
        """Heading and phase of the record's own rays that arrived here with it."""
        definition = self.definitions[index]
        if not definition.self_exclusion or not record.emission_departed or record.channel_code < 2:
            return set()
        port = record.channel_code - 2
        keys: set[tuple[int, tuple[int, int, int]]] = set()
        for rule_index, rule in enumerate(self.emissions):
            if rule.spatial_field != index or not matches_type(rule, record.type_index):
                continue
            if rule_index >= len(record.emission_departed):
                continue
            amount, cursor = unpack(record.emission_departed[rule_index])
            if not amount:
                continue
            for ray in emit_rays(amount, cursor, definition, meter)[0]:
                first_port, moved = advance_ray(ray, definition.headings[ray.heading])
                meter.charge("evaluate")
                if first_port == port:
                    keys.add((moved.heading, moved.accumulators))
        return keys

    def _carried_phase(self, record: DisturbanceRecord, definition: SpatialFieldDefinition) -> int:
        """The phase of the record's last absorption on this field, plus one link's advance."""
        for rule_index, rule in enumerate(self.absorptions):
            if rule.field == definition.field and matches_type(rule, record.type_index):
                if rule_index < len(record.absorbed_phases):
                    stored = unpack(record.absorbed_phases[rule_index])[0]
                    return (stored + definition.phase_advance) % definition.phase_steps
                return 0
        raise ValueError("a carried emission phase requires an absorb rule on the same field")

    def _absorb(
        self,
        index: int,
        resident: list[Ray],
        records: list[DisturbanceRecord | None],
        meter: CostMeter,
    ) -> int:
        """Absorbing records take a share of the resident rays of one field, in slot order.

        The share of each ray is amount x fraction / fraction_denominator, truncated
        toward zero, or the whole ray without a fraction. A negative share is paid
        from the record's own stock and never beyond it. The share adds to the
        record's field of the same name and share x heading to its momentum field;
        the rest of the ray stays resident and is forwarded. A record's own rays
        that arrived with it are left alone. Returns the total amount absorbed.
        """
        definition = self.definitions[index]
        absorbed_total = 0
        # Kerengonen: the coherence of everything that arrived gates every share.
        coherent_numerator, coherent_denominator = coherence(tuple(resident), definition)
        if definition.kerengonen:
            meter.charge("evaluate", len(resident))
        lottery = definition.capture == "lottery"
        for rule_index, rule in enumerate(self.absorptions):
            if rule.field != definition.field:
                continue
            for slot, record in enumerate(records):
                if record is None or not matches_type(rule, record.type_index) or not resident:
                    continue
                own = self._own_departed_keys(record, index, meter)
                if all((ray.heading, ray.accumulators) in own for ray in resident):
                    continue
                tickets = list(record.absorb_tickets)
                if lottery and len(tickets) != len(self.absorptions):
                    tickets = [pack((definition.capture_seed,)) for _ in self.absorptions]
                ticket = unpack(tickets[rule_index])[0] if lottery else 0
                absorbed_terms: list[tuple[int, int]] = []
                values = list(record.values)
                stock = unpack(values[definition.field])[0]
                momentum = (
                    list(unpack(values[rule.momentum_field]))
                    if rule.momentum_field is not None
                    else None
                )
                numerator = None
                if rule.fraction is not None:
                    numerator = evaluate(rule.fraction, record.values, record.values, meter)[0]
                    if numerator < 0:
                        raise ValueError("absorb fraction must not be negative")
                remaining: list[Ray] = []
                for ray in resident:
                    if (ray.heading, ray.accumulators) in own:
                        remaining.append(ray)
                        continue
                    meter.charge("read")
                    meter.charge("couple")
                    share = ray.amount
                    fractional = numerator is not None and numerator < rule.fraction_denominator
                    share_numerator, share_denominator = coherent_numerator, coherent_denominator
                    if fractional:
                        assert numerator is not None
                        share_numerator = checked_work(share_numerator * numerator)
                        share_denominator = checked_work(share_denominator * rule.fraction_denominator)
                    if lottery:
                        # Whole ray or nothing: the local ticket draws against the share.
                        ticket = next_ticket(ticket, ray_salt(ray))
                        meter.charge("evaluate")
                        if checked_work(ticket * share_denominator) >= checked_work(
                            share_numerator * TICKET_MODULUS
                        ):
                            share = 0
                    elif share_numerator < share_denominator:
                        magnitude = checked_work(abs(ray.amount) * share_numerator) // share_denominator
                        share = -magnitude if ray.amount < 0 else magnitude
                    if share < 0:
                        # A pull is paid from the record's own stock, never borrowed.
                        share = max(share, -max(stock, 0))
                    stock = checked_work(stock + share)
                    absorbed_total = checked_work(absorbed_total + share)
                    if share and definition.kerengonen:
                        absorbed_terms.append((abs(share), ray.phase))
                    if momentum is not None:
                        heading = definition.headings[ray.heading]
                        for axis in range(3):
                            momentum[axis] = checked_work(momentum[axis] + share * heading[axis])
                    if ray.amount != share:
                        remaining.append(replace(ray, amount=checked_work(ray.amount - share)))
                resident[:] = remaining
                values[definition.field] = pack((stock,))
                self.fields[definition.field].validate(values[definition.field])
                if momentum is not None and rule.momentum_field is not None:
                    values[rule.momentum_field] = pack(tuple(momentum))
                    self.fields[rule.momentum_field].validate(values[rule.momentum_field])
                meter.charge("update", 1 + (3 if momentum is not None else 0))
                if lottery:
                    tickets[rule_index] = pack((ticket,))
                phases = list(record.absorbed_phases)
                if definition.kerengonen:
                    if len(phases) != len(self.absorptions):
                        phases = [pack((0,)) for _ in self.absorptions]
                    if absorbed_terms:
                        meter.charge("evaluate", definition.phase_steps)
                        phases[rule_index] = pack(
                            (phase_of_sum(tuple(absorbed_terms), definition.phase_steps),)
                        )
                records[slot] = replace(
                    record,
                    values=tuple(values),
                    absorb_tickets=tuple(tickets) if lottery else record.absorb_tickets,
                    absorbed_phases=tuple(phases) if definition.kerengonen else record.absorbed_phases,
                )
        return absorbed_total

    def validate_guards(self, states: tuple[SpatialState, ...], plan: SpatialPlan) -> None:
        validate_field_guards(self.fields, self.definitions, self.field_rules, states, plan, self.costs)

    def _emitter(self, record: DisturbanceRecord) -> DisturbanceRecord:
        """Validate fixed carried source metadata, or initialize an untouched emitter."""
        zero = tuple(
            pack((0,) * self.fields[self.definitions[rule.spatial_field].field].components)
            for rule in self.emissions
        )
        remainders, phases = record.emission_remainders, record.emission_phases
        budgets = tuple(
            rule.budget if rule.budget is not None and matches_type(rule, record.type_index) else blank
            for rule, blank in zip(self.emissions, zero, strict=True)
        )
        finite = any(rule.budget is not None for rule in self.emissions)
        excluding = any(self.definitions[rule.spatial_field].self_exclusion for rule in self.emissions)
        blank_last = tuple(pack((0, 0)) for _ in self.emissions)
        if not remainders and not phases:
            if record.emission_remaining:
                raise ValueError("partial carried emission metadata cannot reset an allowance")
            return replace(
                record,
                emission_remainders=zero,
                emission_phases=zero,
                emission_remaining=budgets if finite else (),
                emission_last=blank_last if excluding else (),
                emission_departed=blank_last if excluding else (),
            )
        if len(remainders) != len(zero) or len(phases) != len(zero):
            raise ValueError("carried emission state must match the fixed emission rules")
        for rule, remainder, phase, blank in zip(self.emissions, remainders, phases, zero, strict=True):
            if len(remainder) != len(blank) or len(phase) != len(blank):
                raise ValueError("carried emission component count differs from the field")
            residues, allocation = unpack(remainder), unpack(phase)
            if any(abs(value) >= rule.denominator for value in residues):
                raise ValueError("carried emission residual must be below its denominator")
            definition = self.definitions[rule.spatial_field]
            denominator = len(definition.headings) if definition.rays else sum(definition.octant_weights)
            if any(not 0 <= value < denominator for value in allocation):
                raise ValueError("carried emission phase must be below the octant weight total")
            if not matches_type(rule, record.type_index) and (any(residues) or any(allocation)):
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
        if excluding:
            for rows in (record.emission_last, record.emission_departed):
                if len(rows) != len(blank_last):
                    raise ValueError("carried self-exclusion state must match the fixed emission rules")
                for row in rows:
                    if len(row) != 2:
                        raise ValueError("carried self-exclusion rows hold an amount and a cursor")
                    unpack(row)
        elif record.emission_last or record.emission_departed:
            raise ValueError("self-exclusion state requires a self-excluding ray field")
        return record

    def __call__(
        self,
        states: tuple[SpatialState, ...],
        records: tuple[DisturbanceRecord | None, ...],
        received_count: int = 0,
        node_cost: int | None = None,
        rays: tuple[Rays, ...] = (),
    ) -> SpatialPlan:
        if bounded(received_count) < 0:
            raise ValueError("received spatial packet count must be nonnegative")
        has_rays = any(definition.rays for definition in self.definitions)
        # Rays that arrived on the previous link; this cycle's emission joins them
        # only after absorption, so a record never swallows its own fresh rays.
        resident_rays: list[list[Ray]] = [
            list(rays[index]) if rays and index < len(rays) else []
            for index in range(len(self.definitions))
        ]
        emitted_rays: list[list[Ray]] = [[] for _ in self.definitions]
        meter = CostMeter(self.costs)
        meter.charge("receive", received_count)
        meter.charge("read", received_count * 8 * len(self.definitions))
        received_components = sum(self.fields[d.field].components for d in self.definitions)
        # Each delivered component updates its population and directional sample.
        meter.charge("update", received_count * 16 * received_components)
        working = list(states)
        emitters = {kind for rule in self.emissions for kind in selected_types(rule)}
        updated_records = [
            self._emitter(record) if record is not None and record.type_index in emitters else record
            for record in records
        ]
        source = [[0] * field.components for field in self.fields]
        funded = [0] * len(self.fields)
        absorbed_by_field = [0] * len(self.fields)
        for index, rule in enumerate(self.emissions):
            definition = self.definitions[rule.spatial_field]
            field = self.fields[definition.field]
            for slot, record in enumerate(updated_records):
                if record is None or not matches_type(rule, record.type_index):
                    continue
                meter.charge("read")
                if rule.budget is not None and not any(unpack(record.emission_remaining[index])):
                    continue
                proposed = evaluate(
                    rule.amount, record.values, record.values, meter, node_cost=node_cost
                )
                residuals, allocation = list(record.emission_remainders), list(record.emission_phases)
                remaining = list(record.emission_remaining)
                last = list(record.emission_last)
                if rule.budget is None:
                    amount, residuals[index] = emission_amount(
                        proposed, residuals[index], rule.denominator, field, meter
                    )
                else:
                    amount, residuals[index], remaining[index] = bounded_emission_amount(
                        proposed, residuals[index], rule.denominator, remaining[index], field, meter
                    )
                record_values = record.values
                if rule.funded:
                    # The record pays from its own stock of the same field; a request
                    # beyond that stock is clipped, never borrowed.
                    # A negative amount is a signed quantum: the emitter is credited.
                    stock = unpack(record.values[definition.field])[0]
                    requested = unpack(amount)[0]
                    paid = requested if requested < 0 else min(requested, max(stock, 0))
                    amount = pack((paid,))
                    values = list(record.values)
                    values[definition.field] = pack((checked_work(stock - paid),))
                    field.validate(values[definition.field])
                    record_values = tuple(values)
                    meter.charge("update")
                if definition.rays:
                    # Straight rays: the amount is shared over the next headings of the
                    # sequence and leaves this Node on the same cycle with the residents.
                    validate_ray_definition(definition, field)
                    cursor_before = unpack(allocation[index])[0]
                    phase = rule.phase
                    if rule.phase_carried:
                        # Huygens: continue the wave absorbed last cycle, one advance on.
                        phase = self._carried_phase(record, definition)
                    new_rays, cursor = emit_rays(
                        unpack(amount)[0], cursor_before, definition, meter, phase
                    )
                    allocation[index] = pack((cursor,))
                    if last and definition.self_exclusion:
                        last[index] = pack((unpack(amount)[0], cursor_before))
                    emitted_rays[rule.spatial_field].extend(new_rays)
                    if rule.recoil_field is not None and new_rays:
                        # The emitter loses the momentum its rays carry: amount x heading.
                        values = list(record_values)
                        recoil = list(unpack(values[rule.recoil_field]))
                        for ray in new_rays:
                            heading = definition.headings[ray.heading]
                            for axis in range(3):
                                recoil[axis] = checked_work(recoil[axis] - ray.amount * heading[axis])
                        values[rule.recoil_field] = pack(tuple(recoil))
                        self.fields[rule.recoil_field].validate(values[rule.recoil_field])
                        record_values = tuple(values)
                        meter.charge("update", 3)
                else:
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
                    values=record_values,
                    emission_remainders=tuple(residuals),
                    emission_phases=tuple(allocation),
                    emission_remaining=tuple(remaining),
                    emission_last=tuple(last),
                )
                if rule.funded:
                    funded[definition.field] = checked_work(funded[definition.field] + unpack(amount)[0])
                    continue
                for component, value in enumerate(unpack(amount)):
                    source[definition.field][component] = checked_work(
                        source[definition.field][component] + value
                    )
        before_rules = tuple(working)
        has_local = any(definition.transport == "local" for definition in self.definitions)
        local_outgoing: tuple[Values, ...] = ()
        guards: list[FieldRuleGuard] = []
        if has_local:
            ruled_states, local_outgoing = apply_field_rules(
                self.fields, self.definitions, self.field_rules, tuple(working), meter, guards=guards
            )
            working = list(ruled_states)
        outgoing: list[list[SpatialPopulations]] = [[] for _ in range(6)]
        outgoing_rays: list[list[Rays]] = [[] for _ in range(6)]
        retained = []
        rule_delta = [[0] * field.components for field in self.fields]
        for index, definition in enumerate(self.definitions):
            field = self.fields[definition.field]
            channels: SpatialOutgoing
            if definition.rays:
                # Ray fields keep no octant stock; every resident ray moves one link.
                if any(any(unpack(payload)) for payload in working[index].populations):
                    raise ValueError("ray transport does not own octant populations")
                absorbed = self._absorb(index, resident_rays[index], updated_records, meter)
                absorbed_by_field[definition.field] = checked_work(
                    absorbed_by_field[definition.field] + absorbed
                )
                ports = forward_rays(
                    tuple(resident_rays[index]) + tuple(emitted_rays[index]), definition, meter
                )
                before_rays = ray_stock(tuple(rays[index])) if rays and index < len(rays) else 0
                before_rays = checked_work(
                    before_rays + source[definition.field][0] + funded[definition.field]
                )
                after_rays = absorbed
                for port_rays in ports:
                    after_rays = checked_work(after_rays + ray_stock(port_rays))
                if field.conserved and before_rays != after_rays:
                    raise ValueError("ray transport violates declared conservation")
                blank = pack((0,) * field.components)
                channels = tuple((blank,) * 8 for _ in range(6))
                for port, port_rays in enumerate(ports):
                    outgoing_rays[port].append(port_rays)
                retained.append(working[index])
                for port, payloads in enumerate(channels):
                    outgoing[port].append(payloads)
                continue
            for port in range(6):
                outgoing_rays[port].append(())
            if definition.transport == "local":
                blank = pack((0,) * field.components)
                channels = tuple(
                    (channel[definition.field],) + (blank,) * 7 for channel in local_outgoing
                )
                state = working[index]
                meter.charge("route")
                meter.charge("send", sum(any(unpack(channel[0])) for channel in channels))
            else:
                channels, state = split_outward(working[index], definition, field, meter)
            if has_local:
                state = replace(state, delivered=(pack((0,) * field.components),) * 6, received_mask=0)
            retained.append(state)
            for port, payloads in enumerate(channels):
                outgoing[port].append(payloads)
            for component in range(field.components):
                before = source[definition.field][component]
                for payload in states[index].populations:
                    before = checked_work(before + unpack(payload)[component])
                after = 0
                for payload in state.populations:
                    after = checked_work(after + unpack(payload)[component])
                for channel in channels:
                    for payload in channel:
                        after = checked_work(after + unpack(payload)[component])
                if field.conserved:
                    if before != after:
                        raise ValueError("spatial transport violates declared conservation")
                pre_rule = 0
                for payload in before_rules[index].populations:
                    pre_rule = checked_work(pre_rule + unpack(payload)[component])
                rule_delta[definition.field][component] = bounded(checked_work(after - pre_rule))
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
            tuple(tuple(v) for v in rule_delta) if has_local else (),
            meter.interaction_ticks,
            tuple(guards),
            tuple(tuple(port_rays) for port_rays in outgoing_rays) if has_rays else (),
            tuple(
                (checked_work(funded[i] - absorbed_by_field[i]),) + (0,) * (f.components - 1)
                for i, f in enumerate(self.fields)
            )
            if has_rays and any(funded) or any(absorbed_by_field)
            else (),
        )
