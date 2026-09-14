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
    BOND_ORIGIN_MARK,
    TICKET_MODULUS,
    Claim,
    Claims,
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
    merge_rays,
    next_ticket,
    phase_of_sum,
    ray_salt,
    ray_stock,
    ticket_draw,
    validate_claims,
    validate_rays,
)

from .bonds import BondRegistry
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
    # The one shared object: the bond registry, the declared exception to the
    # causal bound. None when no field is bonded.
    bonds: BondRegistry | None = None

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

    def _carried_phase(
        self, record: DisturbanceRecord, definition: SpatialFieldDefinition
    ) -> tuple[int, int, int]:
        """Phase, advance and heading of the record's last absorption on this field, one link on."""
        for rule_index, rule in enumerate(self.absorptions):
            if rule.field == definition.field and matches_type(rule, record.type_index):
                if rule_index < len(record.absorbed_phases):
                    stored, advance, heading = unpack(record.absorbed_phases[rule_index])
                    step = advance if advance >= 0 else definition.phase_advance
                    return (stored + step) % definition.phase_steps, advance, heading
                return 0, -1, -1
        raise ValueError("a carried emission phase requires an absorb rule on the same field")

    def _carried_train(self, record: DisturbanceRecord, definition: SpatialFieldDefinition) -> int:
        """The train of the record's last absorption on this field, zero before any."""
        for rule_index, rule in enumerate(self.absorptions):
            if rule.field == definition.field and matches_type(rule, record.type_index):
                if rule_index < len(record.absorbed_trains):
                    return unpack(record.absorbed_trains[rule_index])[0]
                return 0
        raise ValueError("a carried train requires an absorb rule on the same field")

    def _mirrored_heading(
        self,
        heading: int,
        mirror: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
        definition: SpatialFieldDefinition,
    ) -> int:
        """The index of the absorbed heading's mirror image; the parser proved it exists."""
        source = definition.headings[heading]
        image = (
            source[mirror[0][0]] * mirror[0][1],
            source[mirror[1][0]] * mirror[1][1],
            source[mirror[2][0]] * mirror[2][1],
        )
        return definition.headings.index(image)

    def _gather(
        self,
        index: int,
        resident: list[Ray],
        claims: list[Claim],
        records: list[DisturbanceRecord | None],
        meter: CostMeter,
    ) -> int:
        """Claims turn their trains' rays homeward; at the claiming Node a record takes them whole.

        A free ray whose train this Node holds a claim for becomes homing: it no
        longer follows its line but the claim's parent ports back to the Node
        that opened the claim. There, a record with a claiming absorb rule takes
        every homing ray of its trains whole, amount to its field and amount x
        heading to its momentum field, with no coherence or lottery: the claim
        owns the train. Returns the amount gathered.
        """
        if not claims:
            return 0
        definition = self.definitions[index]
        claimed = {claim.train: claim for claim in claims}
        for position, ray in enumerate(resident):
            if ray.train and not ray.homing and ray.train in claimed:
                meter.charge("read")
                meter.charge("update")
                resident[position] = replace(ray, homing=1, wait=0)
        roots = {train for train, claim in claimed.items() if claim.parent < 0}
        gathered = 0
        if not roots:
            return 0
        for rule in self.absorptions:
            if rule.field != definition.field or not rule.claim:
                continue
            for slot, record in enumerate(records):
                if record is None or not matches_type(rule, record.type_index):
                    continue
                values = list(record.values)
                stock = unpack(values[definition.field])[0]
                momentum = (
                    list(unpack(values[rule.momentum_field]))
                    if rule.momentum_field is not None
                    else None
                )
                remaining: list[Ray] = []
                for ray in resident:
                    if not (ray.homing and ray.train in roots):
                        remaining.append(ray)
                        continue
                    meter.charge("read")
                    meter.charge("couple")
                    stock = checked_work(stock + ray.amount)
                    gathered = checked_work(gathered + ray.amount)
                    if momentum is not None:
                        heading = definition.headings[ray.heading]
                        for axis in range(3):
                            momentum[axis] = checked_work(momentum[axis] + ray.amount * heading[axis])
                if len(remaining) == len(resident):
                    continue
                resident[:] = remaining
                values[definition.field] = pack((stock,))
                self.fields[definition.field].validate(values[definition.field])
                if momentum is not None and rule.momentum_field is not None:
                    values[rule.momentum_field] = pack(tuple(momentum))
                    self.fields[rule.momentum_field].validate(values[rule.momentum_field])
                meter.charge("update", 1 + (3 if momentum is not None else 0))
                records[slot] = replace(record, values=tuple(values))
        return gathered

    def _absorb(
        self,
        index: int,
        resident: list[Ray],
        records: list[DisturbanceRecord | None],
        meter: CostMeter,
        claims: list[Claim] | None = None,
        tick: int = 0,
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
                    tickets = [
                        pack(((definition.capture_seed + item.capture_salt) % TICKET_MODULUS,))
                        for item in self.absorptions
                    ]
                ticket = unpack(tickets[rule_index])[0] if lottery else 0
                absorbed_terms: list[tuple[int, int]] = []
                carried_share, carried_advance, carried_heading = 0, -1, -1
                largest_share, carried_train = 0, 0
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
                    if (ray.heading, ray.accumulators) in own or ray.homing:
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
                    while share_denominator > TICKET_MODULUS:
                        # Keep the share at the ticket's resolution so the draw and the
                        # truncated share stay within the working register.
                        share_numerator //= 2
                        share_denominator //= 2
                    if rule.bond_setting is not None and ray.bond and self.bonds is not None:
                        # A bonded ray: the registry answers for both ends of the pair.
                        setting = unpack(record.values[rule.bond_setting])[0]
                        meter.charge("evaluate")
                        if self.bonds.draw(ray.bond, setting, ray_salt(ray)) < 0:
                            share = 0
                    elif lottery:
                        # Whole ray or nothing: the local ticket draws against the share.
                        ticket = next_ticket(ticket, ray_salt(ray))
                        meter.charge("evaluate")
                        if checked_work(ticket_draw(ticket) * share_denominator) >= checked_work(
                            share_numerator * TICKET_MODULUS
                        ):
                            share = 0
                    elif definition.capture == "threshold":
                        # Whole ray or nothing, decided by the hidden phases alone: taken
                        # when the coherent share reaches one half, left otherwise.
                        meter.charge("evaluate")
                        if checked_work(2 * share_numerator) < share_denominator:
                            share = 0
                    elif share_numerator < share_denominator:
                        magnitude = checked_work(abs(ray.amount) * share_numerator) // share_denominator
                        share = -magnitude if ray.amount < 0 else magnitude
                    if share < 0:
                        # A pull is paid from the record's own stock, never borrowed.
                        share = max(share, -max(stock, 0))
                    stock = checked_work(stock + share)
                    absorbed_total = checked_work(absorbed_total + share)
                    if (
                        share
                        and rule.claim
                        and ray.train
                        and claims is not None
                        and all(claim.train != ray.train for claim in claims)
                        and len(claims) < definition.claim_slots
                    ):
                        # Claim and gather: taking any of a train opens a claim here,
                        # the root that every neighbor's claim will lead back to.
                        meter.charge("update")
                        claims.append(Claim(ray.train, -1, tick))
                    if share and definition.claims and abs(share) > largest_share:
                        largest_share, carried_train = abs(share), ray.train
                    if share and definition.kerengonen:
                        absorbed_terms.append((abs(share), ray.phase))
                        if abs(share) > carried_share:
                            carried_share, carried_advance = abs(share), ray.advance
                            carried_heading = ray.heading
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
                        phases = [pack((0, -1, -1)) for _ in self.absorptions]
                    if absorbed_terms:
                        # The phase of the coherent sum; the advance and heading of the
                        # largest share.
                        meter.charge("evaluate", definition.phase_steps)
                        phases[rule_index] = pack(
                            (
                                phase_of_sum(tuple(absorbed_terms), definition.phase_steps),
                                carried_advance,
                                carried_heading,
                            )
                        )
                trains = list(record.absorbed_trains)
                if definition.claims:
                    if len(trains) != len(self.absorptions):
                        trains = [pack((0,)) for _ in self.absorptions]
                    if largest_share:
                        trains[rule_index] = pack((carried_train,))
                records[slot] = replace(
                    record,
                    values=tuple(values),
                    absorb_tickets=tuple(tickets) if lottery else record.absorb_tickets,
                    absorbed_phases=tuple(phases) if definition.kerengonen else record.absorbed_phases,
                    absorbed_trains=tuple(trains) if definition.claims else record.absorbed_trains,
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
        claims: tuple[Claims, ...] = (),
        tick: int = 0,
    ) -> SpatialPlan:
        if bounded(received_count) < 0:
            raise ValueError("received spatial packet count must be nonnegative")
        has_rays = any(definition.rays for definition in self.definitions)
        has_claims = any(definition.claims for definition in self.definitions)
        # Claims this Node still holds: a claim expires claim_ticks after it opened.
        claims_state: list[list[Claim]] = [
            [
                claim
                for claim in (claims[index] if claims and index < len(claims) else ())
                if checked_work(bounded(tick) - claim.since) <= definition.claim_ticks
            ]
            for index, definition in enumerate(self.definitions)
        ]
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
                clocks = list(record.dissolve_clocks)
                if rule.dissolve_over:
                    # A particle paying itself out: count this record's cycles, remember
                    # the stock it started with, and schedule the train from it.
                    if len(clocks) != len(self.emissions):
                        clocks = [pack((0, 0)) for _ in self.emissions]
                    elapsed, initial = unpack(clocks[index])
                    stock = unpack(record.values[definition.field])[0]
                    if initial == 0:
                        initial = stock
                    elapsed = checked_work(elapsed + 1)
                    clocks[index] = pack((min(elapsed, rule.dissolve_after + 1), initial))
                    share = (initial + rule.dissolve_over - 1) // rule.dissolve_over
                    proposed = (min(stock, share) if elapsed > rule.dissolve_after else 0,)
                    meter.charge("update")
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
                    phase, advance, absorbed_heading = rule.phase, -1, -1
                    if rule.phase_carried or rule.mirror is not None:
                        # Huygens: continue the wave absorbed last cycle, one advance on.
                        phase, advance, absorbed_heading = self._carried_phase(record, definition)
                        if not rule.phase_carried:
                            phase, advance = rule.phase, -1
                    if rule.advance is not None:
                        # De Broglie: the rays' own advance per link from the emitter's state.
                        raw_advance = evaluate(rule.advance, record.values, record.values, meter)[0]
                        if raw_advance < 0:
                            raise ValueError("kerengonen_advance must not be negative")
                        advance = (raw_advance // rule.advance_denominator) % definition.phase_steps
                    if rule.mirror is not None:
                        # A mirror: the whole amount back along the image of the absorbed
                        # heading, or nothing until something has been absorbed.
                        cursor = cursor_before
                        new_rays: Rays = ()
                        if absorbed_heading >= 0 and unpack(amount)[0]:
                            meter.charge("route")
                            image = self._mirrored_heading(absorbed_heading, rule.mirror, definition)
                            new_rays = (Ray(image, (0, 0, 0), unpack(amount)[0], phase, advance),)
                    elif rule.heading is not None:
                        # A directed emitter: the whole amount on one fixed heading.
                        cursor = cursor_before
                        new_rays = ()
                        if unpack(amount)[0]:
                            meter.charge("route")
                            new_rays = (Ray(rule.heading, (0, 0, 0), unpack(amount)[0], phase, advance),)
                    else:
                        new_rays, cursor = emit_rays(
                            unpack(amount)[0], cursor_before, definition, meter, phase, advance
                        )
                    allocation[index] = pack((cursor,))
                    if last and definition.self_exclusion:
                        last[index] = pack((unpack(amount)[0], cursor_before))
                    if (rule.train_field is not None or rule.train_carried) and new_rays:
                        # Claim and gather: every ray of this emission belongs to the
                        # record's train, or to the train it last absorbed, so a claim
                        # can gather it later.
                        train = (
                            self._carried_train(record, definition)
                            if rule.train_carried
                            else unpack(record_values[rule.train_field or 0])[0]
                        )
                        if train < 0:
                            raise ValueError("a train must not be negative")
                        new_rays = tuple(replace(ray, train=train) for ray in new_rays)
                        meter.charge("update", len(new_rays))
                    if (rule.bond_field is not None or rule.bond_origin) and new_rays:
                        # Bonded at birth: by the emitter's label, or by the birth Node
                        # and tick, which the Node stamps when it commits this plan.
                        bond = (
                            BOND_ORIGIN_MARK
                            if rule.bond_origin
                            else unpack(record_values[rule.bond_field or 0])[0]
                        )
                        if bond < 0:
                            raise ValueError("a bond must not be negative")
                        new_rays = tuple(replace(ray, bond=bond) for ray in new_rays)
                        meter.charge("update", len(new_rays))
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
                    dissolve_clocks=tuple(clocks),
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
        kept_rays: list[Rays] = [() for _ in self.definitions]
        outgoing_claims: list[list[Claims]] = [[() for _ in self.definitions] for _ in range(6)]
        retained = []
        rule_delta = [[0] * field.components for field in self.fields]
        for index, definition in enumerate(self.definitions):
            field = self.fields[definition.field]
            channels: SpatialOutgoing
            if definition.rays:
                # Ray fields keep no octant stock; every resident ray moves one link.
                if any(any(unpack(payload)) for payload in working[index].populations):
                    raise ValueError("ray transport does not own octant populations")
                absorbed = self._gather(
                    index, resident_rays[index], claims_state[index], updated_records, meter
                )
                absorbed = checked_work(
                    absorbed
                    + self._absorb(
                        index, resident_rays[index], updated_records, meter, claims_state[index], tick
                    )
                )
                absorbed = checked_work(
                    absorbed
                    + self._gather(
                        index, resident_rays[index], claims_state[index], updated_records, meter
                    )
                )
                absorbed_by_field[definition.field] = checked_work(
                    absorbed_by_field[definition.field] + absorbed
                )
                free = tuple(ray for ray in resident_rays[index] if not ray.homing)
                homing = tuple(ray for ray in resident_rays[index] if ray.homing)
                ports, kept = forward_rays(free + tuple(emitted_rays[index]), definition, meter)
                if homing:
                    # Homing rays follow the claim's parent port one link per tick;
                    # without a parent here (the root, or no claim) they wait.
                    port_lists = [list(port_rays) for port_rays in ports]
                    kept_list = list(kept)
                    claimed = {claim.train: claim for claim in claims_state[index]}
                    for ray in homing:
                        meter.charge("read")
                        meter.charge("route")
                        claim = claimed.get(ray.train)
                        if claim is None or claim.parent < 0:
                            kept_list.append(ray)
                        else:
                            meter.charge("send")
                            port_lists[claim.parent].append(ray)
                    ports = tuple(merge_rays(tuple(port_rays)) for port_rays in port_lists)
                    kept = merge_rays(tuple(kept_list))
                validate_rays(kept, definition, field)
                kept_rays[index] = kept
                if definition.claims:
                    # The flood: a claim not yet passed on goes to every port but the
                    # one it came from, then stays here as knowledge until it expires.
                    unsent = [claim for claim in claims_state[index] if not claim.sent]
                    for port in range(6):
                        outgoing_claims[port][index] = tuple(
                            Claim(claim.train, -1, claim.since, 0, claim.origin)
                            for claim in unsent
                            if claim.parent != port
                        )
                    meter.charge("send", sum(1 for _ in unsent) * 5)
                    claims_state[index] = [replace(claim, sent=1) for claim in claims_state[index]]
                    validate_claims(tuple(claims_state[index]), definition)
                before_rays = ray_stock(tuple(rays[index])) if rays and index < len(rays) else 0
                before_rays = checked_work(
                    before_rays + source[definition.field][0] + funded[definition.field]
                )
                after_rays = checked_work(absorbed + ray_stock(kept))
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
            tuple(kept_rays) if has_rays and any(kept_rays) else (),
            tuple(tuple(field_claims) for field_claims in claims_state) if has_claims else (),
            tuple(tuple(port_claims) for port_claims in outgoing_claims) if has_claims else (),
        )
