"""Pure local emission and outward transport assembled from generic primitives."""

from dataclasses import dataclass, replace

from event_universe.core.coupling_selectors import matches_type, selected_types
from event_universe.core.disturbance_state import (
    CostMeter,
    DisturbanceRecord,
    FieldDefinition,
    InteractionDefinition,
    OperationCosts,
    Values,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work, reduced_ratio
from event_universe.core.sampling_contract import DETECTOR_ONLY, validate_spatial_sampling
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    BIT_THING,
    PORT_HEADINGS,
    REMAINDER_SLOTS,
    RETURN_MODES,
    EmissionDefinition,
    FieldRuleGuard,
    FieldSpread,
    InverseSplit,
    Layers,
    NodeFieldRuleDefinition,
    Ray,
    Rays,
    ShadowHome,
    SpatialCouplingDefinition,
    SpatialFieldDefinition,
    SpatialOutgoing,
    SpatialPlan,
    SpatialPopulations,
    SpatialState,
    advance_ray,
    coherence,
    leave_trace,
    merge_rays,
    park_shares,
    parked_shares,
    parked_unit,
    phase_of_sum,
    port_heading,
    pushed_ray,
    ray_layers,
    ray_line,
    ray_momentum,
    ray_momentum_share,
    ray_stock,
    remainder_stock,
    rerelease_shadow,
    spread_content,
    stamp_event,
    trace_of,
    transmit,
    validate_ray_participants,
    validate_rays,
    validate_released_fields,
    validate_spread_fields,
)

from .disturbances import evaluate
from .local_field_rules import apply_field_rules, validate_field_guards
from .ray_interactions import Draws, Turns, apply_ray_interactions
from .rays import emit_rays, forward_rays, hold_rays, validate_ray_definition
from .spatial import (
    add_populations,
    bounded_emission_amount,
    emission_amount,
    emit,
    split_outward,
    split_outward_carried,
)


@dataclass(frozen=True, slots=True)
class SpatialLaw:
    fields: tuple[FieldDefinition, ...]
    definitions: tuple[SpatialFieldDefinition, ...]
    emissions: tuple[EmissionDefinition, ...]
    costs: OperationCosts
    field_rules: tuple[NodeFieldRuleDefinition, ...] = ()
    absorptions: tuple[SpatialCouplingDefinition, ...] = ()
    # "straight": a portion keeps its axis; "rotate": it continues the weight cycle;
    # "node": legacy node-owned phase.
    allocation_phase: str = "straight"
    computation_field: int | None = None
    # When set, indivisible portions prefer the axis whose port carries the least
    # computation load travelling along ("along") or against it ("against").
    least_delay_direction: str | None = None
    ray_interactions: tuple[InteractionDefinition, ...] = ()
    sampling_profile: str = DETECTOR_ONLY
    # What a returned ray does at its event Node (inverse-split-v1).
    return_mode: str = "siblings"
    # The layers of event spacetime (ray-layers-v1): derived here from the declared
    # ray interactions, never declared; every meeting reads them.
    layers: Layers = ()
    # Per spatial field, the families a declared ray interaction couples it with
    # (field-spreading-v1): the content a returned field quantum is absorbed by.
    coupled: tuple[tuple[int, ...], ...] = ()
    # The thing id per disturbance type (bit-law-v1): the owner of what a record
    # of that type emits and of the shadows its field is made of.
    things: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        validate_spatial_sampling(self.sampling_profile, self.definitions)
        if self.return_mode not in RETURN_MODES:
            raise ValueError("return_mode must be siblings, straight or annul")
        validate_released_fields(self.definitions, self.fields)
        validate_spread_fields(self.definitions, self.fields)
        coupled: list[tuple[int, ...]] = []
        for index in range(len(self.definitions)):
            partners: set[int] = set()
            for rule in self.ray_interactions:
                roles = {kind for role in rule.participants for kind in role}
                if index in roles:
                    partners |= roles - {index}
            coupled.append(tuple(sorted(partners)))
        object.__setattr__(self, "coupled", tuple(coupled))
        if self.ray_interactions:
            selected = validate_ray_participants(self.definitions, self.fields, self.ray_interactions)
            object.__setattr__(self, "layers", ray_layers(self.definitions, self.ray_interactions))
            if (
                self.field_rules
                or self.least_delay_direction is not None
                or any(
                    rule.field == self.definitions[index].field
                    for index in selected
                    for rule in self.absorptions
                )
            ):
                raise ValueError("ray interactions do not support another coupled field program")

    def _own_departed_keys(self, record: DisturbanceRecord, index: int, meter: CostMeter) -> set[Ray]:
        """Complete keys of the record's own rays that arrived here with it."""
        definition = self.definitions[index]
        if not definition.self_exclusion or not record.emission_departed or record.channel_code < 2:
            return set()
        port = record.channel_code - 2
        keys: set[Ray] = set()
        # The record's rays carry its identity (bit-law-v1), part of the key.
        owner = self.things[record.type_index] if record.type_index < len(self.things) else 0
        for rule_index, rule in enumerate(self.emissions):
            if rule.spatial_field != index or not matches_type(rule, record.type_index):
                continue
            if rule_index >= len(record.emission_departed):
                continue
            amount, cursor, phase, advance = unpack(record.emission_departed[rule_index])
            if not amount:
                continue
            for ray in emit_rays(
                amount, cursor, definition, meter, phase, advance, rule.heading, rule.polarization
            )[0]:
                first_port, moved = advance_ray(
                    ray,
                    definition.headings[ray.heading],
                    definition.phase_modulus,
                    definition.phase_advance,
                )
                meter.charge("evaluate")
                if first_port == port:
                    keys.add(replace(moved, amount=1, owner=owner))
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
                    return (stored + step) & definition.phase_mask, advance, heading
                return 0, -1, -1
        raise ValueError("a carried emission phase requires an absorb rule on the same field")

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
        that arrived with it are left alone. Nothing here draws: the capture is
        the coherent share or the deterministic threshold. A returning ray
        (outbound 0) enters no absorption and gates no coherence: it crosses the
        Node as if alone (detector-return-v1). Returns the total amount absorbed.
        """
        definition = self.definitions[index]
        absorbed_total = 0
        returning = [ray for ray in resident if not ray.outbound]
        resident[:] = [ray for ray in resident if ray.outbound]
        # Kerengonen: the coherence of everything that arrived gates every share.
        coherent_numerator, coherent_denominator = coherence(tuple(resident), definition)
        if definition.coherent:
            meter.charge("evaluate", len(resident))
        for rule_index, rule in enumerate(self.absorptions):
            if rule.field != definition.field:
                continue
            for slot, record in enumerate(records):
                if record is None or not matches_type(rule, record.type_index) or not resident:
                    continue
                own = self._own_departed_keys(record, index, meter)
                if all(replace(ray, amount=1) in own for ray in resident):
                    continue
                absorbed_terms: list[tuple[int, int]] = []
                carried_share, carried_advance, carried_heading = 0, -1, -1
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
                    if replace(ray, amount=1) in own:
                        remaining.append(ray)
                        continue
                    meter.charge("read")
                    meter.charge("couple")
                    share = ray.amount
                    fractional = numerator is not None and numerator < rule.fraction_denominator
                    share_numerator, share_denominator = reduced_ratio(
                        coherent_numerator, coherent_denominator
                    )
                    if fractional:
                        assert numerator is not None
                        left, right_denominator = reduced_ratio(
                            share_numerator, rule.fraction_denominator
                        )
                        right, left_denominator = reduced_ratio(numerator, share_denominator)
                        share_numerator = checked_work(left * right)
                        share_denominator = checked_work(left_denominator * right_denominator)
                    if definition.capture == "threshold":
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
                        available = max(stock, 0)
                        share = (
                            (0 if -share > available else share)
                            if definition.capture != "share"
                            else max(share, -available)
                        )
                    stock = checked_work(stock + share)
                    absorbed_total = checked_work(absorbed_total + share)
                    if share and definition.coherent:
                        absorbed_terms.append((abs(share), ray.phase))
                        if abs(share) > carried_share:
                            carried_share, carried_advance = abs(share), ray.advance
                            carried_heading = ray.heading
                    if momentum is not None:
                        for axis, value in enumerate(ray_momentum_share(ray, share, definition)):
                            momentum[axis] = checked_work(momentum[axis] + value)
                    if ray.amount != share:
                        remaining.append(replace(ray, amount=checked_work(ray.amount - share)))
                resident[:] = remaining
                values[definition.field] = pack((stock,))
                self.fields[definition.field].validate(values[definition.field])
                if momentum is not None and rule.momentum_field is not None:
                    values[rule.momentum_field] = pack(tuple(momentum))
                    self.fields[rule.momentum_field].validate(values[rule.momentum_field])
                meter.charge("update", 1 + (3 if momentum is not None else 0))
                phases = list(record.absorbed_phases)
                if definition.coherent:
                    if len(phases) != len(self.absorptions):
                        phases = [pack((0, -1, -1)) for _ in self.absorptions]
                    if absorbed_terms:
                        # The phase of the coherent sum; the advance and heading of the
                        # largest share.
                        meter.charge("evaluate", definition.phase_steps)
                        phases[rule_index] = pack(
                            (
                                phase_of_sum(tuple(absorbed_terms), definition),
                                carried_advance,
                                carried_heading,
                            )
                        )
                records[slot] = replace(
                    record,
                    values=tuple(values),
                    absorbed_phases=tuple(phases) if definition.coherent else record.absorbed_phases,
                )
        resident.extend(returning)
        return absorbed_total

    def _input_slot(self, index: int, records: list[DisturbanceRecord | None]) -> int | None:
        """The slot of the event's input when it is still at the Node: the first record
        with a funded emission rule into this field (the resident emitting record)."""
        for slot, record in enumerate(records):
            if record is None:
                continue
            for rule in self.emissions:
                if rule.spatial_field == index and rule.funded and matches_type(rule, record.type_index):
                    return slot
        return None

    def _refund(
        self,
        index: int,
        record: DisturbanceRecord,
        returned: Ray,
        transmitted: Rays,
        annulled: list[list[int]],
        meter: CostMeter,
    ) -> DisturbanceRecord:
        """Restore the returned share to the event's input exactly, the inverse of the
        funded-emission bookkeeping, then fund the transmission from it in the same
        interval: stock back by the share and out by the amounts transmitted or
        annulled; the recoil back by share x event heading and out by amount x
        heading per transmission or by the annulled momentum. A stock or recoil the
        field cannot hold fails closed."""
        definition = self.definitions[index]
        field = self.fields[definition.field]
        values = list(record.values)
        stock = unpack(values[definition.field])[0]
        restored = checked_work(stock + returned.amount)
        values[definition.field] = pack((restored,))
        try:
            field.validate(values[definition.field])
        except ValueError as error:
            raise ValueError(
                f"the inverse split cannot restore the returned share to its input: {error}"
            ) from error
        funded = checked_work(restored - annulled[definition.field][0])
        for ray in transmitted:
            funded = checked_work(funded - ray.amount)
        values[definition.field] = pack((funded,))
        field.validate(values[definition.field])
        meter.charge("update", 2)
        recoil_field = next(
            (
                rule.recoil_field
                for rule in self.emissions
                if rule.spatial_field == index and rule.funded and matches_type(rule, record.type_index)
            ),
            None,
        )
        if recoil_field is not None:
            recoil = list(unpack(values[recoil_field]))
            for axis, value in enumerate(ray_momentum((returned,), definition)):
                recoil[axis] = checked_work(recoil[axis] + value)
            for axis, value in enumerate(ray_momentum(transmitted, definition)):
                recoil[axis] = checked_work(recoil[axis] - value)
            if definition.momentum_field is not None:
                for axis, value in enumerate(annulled[definition.momentum_field]):
                    recoil[axis] = checked_work(recoil[axis] - value)
            values[recoil_field] = pack(tuple(recoil))
            self.fields[recoil_field].validate(values[recoil_field])
            meter.charge("update", 3)
        return replace(record, values=tuple(values))

    def _inverse_split(
        self,
        index: int,
        resident: list[Ray],
        records: list[DisturbanceRecord | None],
        meter: CostMeter,
        source: list[list[int]],
        funded: list[int],
        absorbed: list[int],
        annulled: list[list[int]],
    ) -> tuple[list[InverseSplit], Rays]:
        """Every returned thing resident at its event Node performs the inverse split
        of its own share by the world's return mode (inverse-split-v1).

        After the meeting by the declared couplings (absorption, ray interactions:
        in this slice a returning ray enters none) and before forwarding, so the
        transmission leaves on this cycle like an emission. Returns the records to
        publish and the transmitted rays, which join this cycle's emitted rays.
        """
        definition = self.definitions[index]
        # A shadow has no event Node and no inverse split: it walks home (bit-law-v1).
        due = [
            ray for ray in resident if not ray.outbound and ray.steps == 0 and ray.detector == BIT_THING
        ]
        if not due:
            return [], ()
        resident[:] = [ray for ray in resident if ray not in due]
        splits: list[InverseSplit] = []
        transmitted: list[Ray] = []
        slot = self._input_slot(index, records)
        for ray in due:
            meter.charge("read")
            meter.charge("route")
            rays, ports = transmit(ray, definition, self.return_mode)
            meter.charge("split", max(len(ports), 1))
            amounts = tuple(r.amount for r in rays)
            annulled_now = [[0] * f.components for f in self.fields]
            if self.return_mode == "annul":
                annulled_now[definition.field][0] = ray.amount
                if definition.momentum_field is not None:
                    for axis, value in enumerate(ray_momentum((ray,), definition)):
                        annulled_now[definition.momentum_field][axis] = value
            elif not rays:
                if slot is None:
                    raise ValueError(
                        "the inverse split of a one-line event with no input at its Node "
                        "has no sibling line to transmit to; use return_mode straight or annul"
                    )
            if slot is not None:
                record = records[slot]
                assert record is not None
                records[slot] = self._refund(index, record, ray, rays, annulled_now, meter)
                # The restore is booked as stock moving from the field to the record;
                # the transmission or the annulled content as funded from it.
                absorbed[definition.field] = checked_work(absorbed[definition.field] + ray.amount)
                paid = annulled_now[definition.field][0]
                for transmission in rays:
                    paid = checked_work(paid + transmission.amount)
                funded[definition.field] = checked_work(funded[definition.field] + paid)
            elif definition.momentum_field is not None and rays:
                # No input at the Node: the transmission is booked as a sourced
                # emission books its rays, the returned share read out of the source
                # ledger and the transmission's momentum into it.
                for axis, value in enumerate(ray_momentum((ray,), definition)):
                    source[definition.momentum_field][axis] = checked_work(
                        source[definition.momentum_field][axis] - value
                    )
                for axis, value in enumerate(ray_momentum(rays, definition)):
                    source[definition.momentum_field][axis] = checked_work(
                        source[definition.momentum_field][axis] + value
                    )
            for field_index, values in enumerate(annulled_now):
                for component, value in enumerate(values):
                    annulled[field_index][component] = checked_work(
                        annulled[field_index][component] + value
                    )
            transmitted.extend(rays)
            splits.append(
                InverseSplit(
                    index,
                    RETURN_MODES.index(self.return_mode),
                    ports,
                    amounts,
                    ray.amount,
                    int(slot is not None),
                    tuple(tuple(v) for v in annulled_now) if self.return_mode == "annul" else (),
                )
            )
        return splits, tuple(transmitted)

    def _spread(
        self,
        index: int,
        resident: list[Ray],
        emitted: list[Ray],
        source: list[list[int]],
        meter: CostMeter,
        registers: tuple[int, ...],
        register_phases: tuple[int, ...],
        blocks: list[tuple[int, ...]],
        block_phases: list[tuple[int, ...]],
    ) -> FieldSpread | None:
        """Field spreading (field-spreading-v1, Highlights 3.5): every Node that
        content of a spreading family reaches releases it again by the declared
        table. After the marks and the meetings and before the departures, the
        outbound content that arrived this interval and is due to leave (at least
        one Link walked, no delay or wait pending) is taken off the Node; a fresh
        ray at its event Node and a fresh release depart on their line and spread
        from the next Node, a returning ray walks back, a held ray is not due. The
        departures join this interval's emitted rays. The total is exact, so no
        amount is sourced, and a shadow carries no momentum on the ledger while
        outbound (bit-law-v1), so nothing is booked on the momentum field."""
        definition = self.definitions[index]
        # A thing moves whole on its line; a shadow spreads (bit-law-v1, point 2).
        due = tuple(
            ray
            for ray in resident
            if ray.outbound
            and ray.steps
            and ray.detector == BIT_SHADOW
            and not ray.interaction_delay
            and not ray.wait
        )
        if not due:
            return None
        resident[:] = [ray for ray in resident if ray not in due]
        meter.charge("read", len(due) + REMAINDER_SLOTS)
        if definition.coherent:
            meter.charge("evaluate", len(due) + definition.phase_steps)
        departures, record, after, after_phases = spread_content(
            index, due, definition, registers, register_phases
        )
        blocks[index], block_phases[index] = after, after_phases
        meter.charge("split", len(departures))
        meter.charge("update", REMAINDER_SLOTS)
        # A shadow carries no momentum on the ledger while outbound (bit-law-v1):
        # the spread moves content, and books nothing on the momentum field.
        emitted.extend(departures)
        return record

    def _homecoming(
        self,
        index: int,
        residents: list[list[Ray]],
        records: list[DisturbanceRecord | None],
        emitted: list[Ray],
        source: list[list[int]],
        returned: list[list[int]],
        meter: CostMeter,
    ) -> list[ShadowHome]:
        """A shadow that meets the thing that released it is home (bit-law-v1,
        point 3 of the law and the model owner's amendment): at a Node holding a
        thing of the shadow's owner, a resident thing ray that arrived (a pushed
        one among them) or a record of a type with that identity, every shadow of
        the family with that owner, outbound (it met its own thing: never a push)
        or on its walk back (it carries -dp of the push it gave), is absorbed
        back: the momentum it carries goes into the thing's register (a thing
        ray: `pushed_ray`; a record: its recoil field, or the `returned` line of
        the momentum field when its type has none), and it leaves again from
        where the thing is, back out along its line. A shadow is initial content,
        never sourced, and its homecoming is no crossing of the border (the model
        owner, 2026-09-18, point 7): its amount stays on the current line, nothing
        is booked. One record per shadow."""
        definition = self.definitions[index]
        resident = residents[index]
        # A shadow that arrived, or one waiting at rest for a thing of its owner
        # to pass (node-is-ports-v1, settled rule (ii)).
        due = [
            ray
            for ray in resident
            if ray.detector == BIT_SHADOW and not ray.parked and (ray.steps >= 1 or not ray.outbound)
        ]
        if not due:
            return []
        owners_here: dict[int, tuple[str, int, int]] = {}
        for kind, bundle in enumerate(residents):
            if not self.definitions[kind].rays:
                continue
            for slot, ray in enumerate(bundle):
                if ray.detector == BIT_THING and ray.outbound and ray.steps >= 1:
                    owners_here.setdefault(ray.owner, ("ray", kind, slot))
        for slot, record in enumerate(records):
            if record is None or record.type_index >= len(self.things):
                continue
            if any(unpack(value) != (0,) * len(unpack(value)) for value in record.values):
                owners_here.setdefault(self.things[record.type_index], ("record", slot, 0))
        taken: list[ShadowHome] = []
        ended: list[Ray] = []
        field = self.fields[definition.field]
        for ray in due:
            home = owners_here.get(ray.owner)
            if home is None:
                continue
            meter.charge("read")
            kind_of, at, slot = home
            if kind_of == "ray" and definition.headings[ray.heading] == ray_line(
                residents[at][slot], self.definitions[at]
            ):
                # A shadow on the line of a moving thing, walking with it, has not
                # come to it: what left a thing again leaves with it, and is home
                # again only when it meets the thing from another heading.
                continue
            momentum = ray.momentum if (ray.momentum is not None and not ray.outbound) else (0, 0, 0)
            outside = 0
            if kind_of == "ray":
                thing = residents[at][slot]
                if any(momentum):
                    thing = pushed_ray(thing, momentum, self.definitions[at])
                    validate_rays(
                        (thing,), self.definitions[at], self.fields[self.definitions[at].field]
                    )
                    residents[at][slot] = thing
                    meter.charge("update", 4)
                to = 0
            else:
                record = records[at]
                assert record is not None
                recoil_field = next(
                    (
                        rule.recoil_field
                        for rule in self.emissions
                        if matches_type(rule, record.type_index) and rule.recoil_field is not None
                    ),
                    None,
                )
                if any(momentum):
                    if recoil_field is not None:
                        values = list(record.values)
                        recoil = list(unpack(values[recoil_field]))
                        for axis in range(3):
                            recoil[axis] = checked_work(recoil[axis] + momentum[axis])
                        values[recoil_field] = pack(tuple(recoil))
                        self.fields[recoil_field].validate(values[recoil_field])
                        records[at] = replace(record, values=tuple(values))
                        meter.charge("update", 3)
                    elif definition.momentum_field is not None:
                        # No register to hold it: the momentum leaves the identity on
                        # the returned line, as a body's does.
                        outside = 1
                        for axis in range(3):
                            returned[definition.momentum_field][axis] = checked_work(
                                returned[definition.momentum_field][axis] + momentum[axis]
                            )
                to = 1
            port = PORT_HEADINGS.index(definition.headings[ray.heading])
            again = rerelease_shadow(ray, definition)
            validate_rays((again,), definition, field)
            emitted.append(again)
            meter.charge("update", 2)
            ended.append(ray)
            taken.append(
                ShadowHome(
                    index,
                    ray.amount,
                    ray.owner,
                    port,
                    (momentum[0], momentum[1], momentum[2]),
                    to,
                    PORT_HEADINGS.index(definition.headings[again.heading]),
                    outside,
                )
            )
        if ended:
            resident[:] = [ray for ray in resident if ray not in ended]
        return taken

    def _follow_traces(
        self, index: int, resident: list[Ray], parked: Rays, meter: CostMeter
    ) -> list[Ray]:
        """A shadow walking home whose steps are spent follows the trace of its owner
        (bit-law-v1, point 3; settled rule (ii) of node-is-ports-v1): where a
        zero-amount parked shadow of that owner says which Port the last thing of
        it left by, the shadow takes that line; where none does, the shadow waits
        at the Node, a zero-step shadow at rest, until a thing of its owner passes
        (and is then home). Returns the shadows that wait, taken off `resident`."""
        definition = self.definitions[index]
        waiting: list[Ray] = []
        for slot, ray in enumerate(resident):
            if ray.detector != BIT_SHADOW or ray.outbound or ray.steps:
                continue
            port = trace_of(parked, ray.owner, definition)
            if not 0 <= port < 6:
                waiting.append(ray)
                continue
            heading = port_heading(port, definition)
            if heading != ray.heading:
                resident[slot] = replace(ray, heading=heading, accumulators=(0, 0, 0))
                meter.charge("update")
        if waiting:
            resident[:] = [ray for ray in resident if ray not in waiting]
        return waiting

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
        blank_last = tuple(pack((0, 0, 0, 0)) for _ in self.emissions)
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
                for index, row in enumerate(rows):
                    if len(row) != 4:
                        raise ValueError(
                            "carried self-exclusion rows hold amount, cursor, wave phase and advance"
                        )
                    _amount, cursor, wave_phase, wave_advance = unpack(row)
                    definition = self.definitions[self.emissions[index].spatial_field]
                    if not 0 <= cursor < max(len(definition.headings), 1):
                        raise ValueError("carried self-exclusion cursor is outside its heading sequence")
                    if not 0 <= wave_phase < definition.phase_modulus:
                        raise ValueError("carried self-exclusion phase is outside its phase width")
                    if not -1 <= wave_advance < definition.phase_modulus:
                        raise ValueError("carried self-exclusion advance is outside its phase width")
        elif record.emission_last or record.emission_departed:
            raise ValueError("self-exclusion state requires a self-excluding ray field")
        return replace(record, emission_last=blank_last) if excluding else record

    def _port_loads(self, states: tuple[SpatialState, ...]) -> tuple[int, ...] | None:
        """Computation load pricing a departure through each port, read from local channels only."""
        if self.least_delay_direction is None or self.computation_field is None:
            return None
        index = next(i for i, d in enumerate(self.definitions) if d.field == self.computation_field)
        delivered = tuple(unpack(payload)[0] for payload in states[index].delivered)
        if self.least_delay_direction == "along":
            return delivered
        return tuple(delivered[port ^ 1] for port in range(6))

    def __call__(
        self,
        states: tuple[SpatialState, ...],
        records: tuple[DisturbanceRecord | None, ...],
        received_count: int = 0,
        node_cost: int | None = None,
        rays: tuple[Rays, ...] = (),
        ray_hold: int = 0,
        detector_ticket: int = 0,
    ) -> SpatialPlan:
        """One Node's spatial plan from its local input alone: the law reads no clock
        (the Node checks its tick before planning), so equal inputs give equal plans
        at any tick, which is what the plan-reuse key relies on. The parked
        shadows among `rays` (node-is-ports-v1) are the shares below one quantum
        the spread reads and writes and the traces the shadows walking home read
        and the things that leave write."""
        if type(ray_hold) is not int or ray_hold not in (0, 1, 2):
            raise ValueError("ray hold must be a bounded local delay mode")
        if type(detector_ticket) is not int or bounded(detector_ticket) < 0:
            raise ValueError("the Node's ticket state must be a nonnegative bounded integer")
        if self.ray_interactions and ray_hold:
            raise ValueError("ray interactions do not support a second ray hold clock")
        if bounded(received_count) < 0:
            raise ValueError("received spatial packet count must be nonnegative")
        has_rays = any(definition.rays for definition in self.definitions)
        # Rays that arrived on the previous link; this cycle's emission joins them
        # only after absorption, so a record never swallows its own fresh rays.
        # The parked shadows stay aside: the shares below one quantum as the block
        # the spread step reads (field-remainder-v1), the traces as they are.
        resident_rays: list[list[Ray]] = [
            [ray for ray in rays[index] if not ray.parked] if rays and index < len(rays) else []
            for index in range(len(self.definitions))
        ]
        parked_rays: list[Rays] = [
            tuple(ray for ray in rays[index] if ray.parked) if rays and index < len(rays) else ()
            for index in range(len(self.definitions))
        ]
        registers_held: list[tuple[int, ...]] = []
        register_phases_held: list[tuple[int, ...]] = []
        for index, definition in enumerate(self.definitions):
            block, block_phases = parked_shares(parked_rays[index], definition)
            registers_held.append(block)
            register_phases_held.append(block_phases)
        emitted_rays: list[list[Ray]] = [[] for _ in self.definitions]
        meter = CostMeter(self.costs)
        # The momentum a meeting moves between lines (ray-meeting-conversion-v1): a
        # split by a table steers content between two Ports, and the recoil owner,
        # the field ray of feature 7, does not exist yet, so the change is booked as
        # an explicitly accounted source of the momentum field (Highlights 3.15).
        meeting_momentum: list[tuple[int, tuple[int, int, int]]] = []
        # The pushes of free rays (ray-momentum-turn-v1): each moves its ray's
        # register, which the momentum readout below reads, so the push and the
        # recoil's reversal are booked together as the meeting's momentum change.
        turns: Turns = []
        # The draws of the decaying rules (decay-draw-v1): the Node's ticket state
        # enters as input and leaves with the last draw, never hidden in the law;
        # the content their conversions moved between families, per field.
        draws: Draws = []
        converted: list[tuple[int, int]] = []
        if self.ray_interactions:
            met = apply_ray_interactions(
                tuple(tuple(bundle) for bundle in resident_rays),
                self.definitions,
                self.fields,
                self.ray_interactions,
                meter,
                self.costs,
                self.layers,
                turns,
                draws,
                detector_ticket,
            )
            for index, definition in enumerate(self.definitions):
                if definition.rays and definition.momentum_field is not None:
                    before_momentum = ray_momentum(tuple(resident_rays[index]), definition)
                    after_momentum = ray_momentum(met[index], definition)
                    delta = tuple(
                        checked_work(after - before)
                        for after, before in zip(after_momentum, before_momentum, strict=True)
                    )
                    if any(delta):
                        meeting_momentum.append(
                            (definition.momentum_field, (delta[0], delta[1], delta[2]))
                        )
                if definition.rays:
                    # The content a decaying conversion moved between families
                    # (decay-draw-v1): what a family lost or gained at this meeting
                    # is booked as that family's source, the families summing to
                    # zero since the total amount is exact; a rule without `draw`
                    # keeps every family's stock, so this is zero for it.
                    moved = checked_work(ray_stock(met[index]) - ray_stock(tuple(resident_rays[index])))
                    if moved:
                        converted.append((definition.field, moved))
            resident_rays = [list(bundle) for bundle in met]
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
        for momentum_field, delta in meeting_momentum:
            for axis, value in enumerate(delta):
                source[momentum_field][axis] = checked_work(source[momentum_field][axis] + value)
        for field_index, moved in converted:
            source[field_index][0] = checked_work(source[field_index][0] + moved)
        funded = [0] * len(self.fields)
        absorbed_by_field = [0] * len(self.fields)
        annulled = [[0] * field.components for field in self.fields]
        # What came home this cycle (bit-law-v1): the amounts absorbed back and
        # re-released, and the momentum delivered outside the identity.
        returned = [[0] * field.components for field in self.fields]
        inverse_splits: list[InverseSplit] = []
        spreads: list[FieldSpread] = []
        homecomings: list[ShadowHome] = []
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
                        advance = (raw_advance // rule.advance_denominator) & definition.phase_mask
                    if rule.mirror is not None:
                        # A mirror: the whole amount back along the image of the absorbed
                        # heading, or nothing until something has been absorbed.
                        cursor = cursor_before
                        new_rays: Rays = ()
                        if absorbed_heading >= 0 and unpack(amount)[0]:
                            meter.charge("route")
                            image = self._mirrored_heading(absorbed_heading, rule.mirror, definition)
                            # The reflection is one event on the image's first Port.
                            new_rays = stamp_event(
                                (
                                    Ray(
                                        image,
                                        (0, 0, 0),
                                        unpack(amount)[0],
                                        phase,
                                        advance,
                                        polarization=rule.polarization,
                                    ),
                                ),
                                (definition.headings[image],),
                            )
                    else:
                        new_rays, cursor = emit_rays(
                            unpack(amount)[0],
                            cursor_before,
                            definition,
                            meter,
                            phase,
                            advance,
                            rule.heading,
                            rule.polarization,
                        )
                    allocation[index] = pack((cursor,))
                    if last and definition.self_exclusion:
                        last[index] = pack((unpack(amount)[0], cursor_before, phase, advance))
                    # bit-law-v1: what a record emits is a thing of the record's identity.
                    if record.type_index < len(self.things):
                        new_rays = tuple(
                            replace(ray, owner=self.things[record.type_index]) for ray in new_rays
                        )
                    emitted_rays[rule.spatial_field].extend(new_rays)
                    if not rule.funded and definition.momentum_field is not None:
                        for axis, value in enumerate(ray_momentum(new_rays, definition)):
                            source[definition.momentum_field][axis] = checked_work(
                                source[definition.momentum_field][axis] + value
                            )
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
        outgoing_phases: list[list[SpatialPopulations]] = [[] for _ in range(6)]
        outgoing_rays: list[list[Rays]] = [[] for _ in range(6)]
        kept_rays: list[Rays] = [() for _ in self.definitions]
        retained = []
        rule_delta = [[0] * field.components for field in self.fields]
        for index, definition in enumerate(self.definitions):
            field = self.fields[definition.field]
            channels: SpatialOutgoing
            blank = pack((0,) * field.components)
            channel_phases: SpatialOutgoing = ((blank,) * 8,) * 6
            if definition.rays:
                # Ray fields keep no octant stock; every resident ray moves one link.
                if any(any(unpack(payload)) for payload in working[index].populations):
                    raise ValueError("ray transport does not own octant populations")
                absorbed = self._absorb(index, resident_rays[index], updated_records, meter)
                absorbed_by_field[definition.field] = checked_work(
                    absorbed_by_field[definition.field] + absorbed
                )
                splits, transmitted = self._inverse_split(
                    index,
                    resident_rays[index],
                    updated_records,
                    meter,
                    source,
                    funded,
                    absorbed_by_field,
                    annulled,
                )
                inverse_splits.extend(splits)
                emitted_rays[index].extend(transmitted)
                # What the splits took out of the resident rays without sending it:
                # the shares restored to an input and the content annulled.
                for split in splits:
                    if split.restored:
                        absorbed = checked_work(absorbed + split.amount)
                    if RETURN_MODES[split.mode] == "annul":
                        absorbed = checked_work(absorbed + split.amount)
                registers_before = (
                    remainder_stock(registers_held[index], parked_unit(definition))
                    if definition.spread
                    else 0
                )
                # The shadows home at this Node come in and leave again (bit-law-v1),
                # before the spread; those whose steps are spent follow the trace
                # or wait for their owner (node-is-ports-v1, settled rule (ii)).
                homecomings.extend(
                    self._homecoming(
                        index,
                        resident_rays,
                        updated_records,
                        emitted_rays[index],
                        source,
                        returned,
                        meter,
                    )
                )
                waiting = self._follow_traces(index, resident_rays[index], parked_rays[index], meter)
                if definition.spread:
                    spread = self._spread(
                        index,
                        resident_rays[index],
                        emitted_rays[index],
                        source,
                        meter,
                        registers_held[index],
                        register_phases_held[index],
                        registers_held,
                        register_phases_held,
                    )
                    if spread is not None:
                        spreads.append(spread)
                if ray_hold:
                    ports, fresh_kept = forward_rays(tuple(emitted_rays[index]), definition, meter)
                    kept = merge_rays(
                        hold_rays(
                            tuple(resident_rays[index]), definition, meter, advance_phase=ray_hold == 2
                        )
                        + fresh_kept
                    )
                else:
                    ports, kept = forward_rays(
                        tuple(resident_rays[index]) + tuple(emitted_rays[index]), definition, meter
                    )
                # What stays at the Node beside the kept rays (node-is-ports-v1): the
                # shares below one quantum after the spread, parked again; the traces,
                # the Port the largest thing of each owner leaves this Node by (ties
                # to the lowest Port) replacing the owner's; the shadows waiting.
                parked_after: Rays = tuple(ray for ray in parked_rays[index] if not ray.amount)
                if definition.spread:
                    parked_after += park_shares(
                        registers_held[index], register_phases_held[index], definition
                    )
                departures: dict[int, tuple[int, int]] = {}
                for port, port_rays in enumerate(ports):
                    for ray in port_rays:
                        if ray.detector == BIT_THING and ray.outbound:
                            best = departures.get(ray.owner)
                            if best is None or ray.amount > best[0]:
                                departures[ray.owner] = (ray.amount, port)
                if all(heading in definition.headings for heading in PORT_HEADINGS):
                    # A family whose lines are not the six Port headings has no
                    # heading to park a trace on, and no shadow of its own to read it.
                    for owner, (_, port) in sorted(departures.items()):
                        parked_after = leave_trace(parked_after, owner, port, definition)
                kept = merge_rays(kept + parked_after + tuple(waiting))
                validate_rays(kept, definition, field)
                kept_rays[index] = kept
                before_rays = (
                    ray_stock(tuple(ray for ray in rays[index] if not ray.parked))
                    if rays and index < len(rays)
                    else 0
                )
                before_rays = checked_work(
                    before_rays
                    + source[definition.field][0]
                    + funded[definition.field]
                    + registers_before
                )
                # What came home this cycle left the residents and leaves again
                # among the kept rays, nothing booked (bit-law-v1, point 7); the
                # parked shares are whole quanta in total (field-remainder-v1).
                after_rays = checked_work(
                    absorbed + ray_stock(tuple(ray for ray in kept if not ray.parked))
                )
                if definition.spread:
                    after_rays = checked_work(
                        after_rays + remainder_stock(registers_held[index], parked_unit(definition))
                    )
                for port_rays in ports:
                    after_rays = checked_work(after_rays + ray_stock(port_rays))
                if field.conserved and before_rays != after_rays:
                    raise ValueError("ray transport violates declared conservation")
                channels = tuple((blank,) * 8 for _ in range(6))
                for port, port_rays in enumerate(ports):
                    outgoing_rays[port].append(port_rays)
                retained.append(working[index])
                for port, payloads in enumerate(channels):
                    outgoing[port].append(payloads)
                    outgoing_phases[port].append(channel_phases[port])
                continue
            for port in range(6):
                outgoing_rays[port].append(())
            if definition.transport == "local":
                channels = tuple(
                    (channel[definition.field],) + (blank,) * 7 for channel in local_outgoing
                )
                state = working[index]
                meter.charge("route")
                meter.charge("send", sum(any(unpack(channel[0])) for channel in channels))
            elif self.allocation_phase != "node":
                channels, state, channel_phases = split_outward_carried(
                    working[index],
                    definition,
                    field,
                    meter,
                    self._port_loads(states),
                    straight=self.allocation_phase == "straight",
                )
            else:
                channels, state = split_outward(working[index], definition, field, meter)
            if has_local:
                state = replace(state, delivered=(pack((0,) * field.components),) * 6, received_mask=0)
            retained.append(state)
            for port, payloads in enumerate(channels):
                outgoing[port].append(payloads)
                outgoing_phases[port].append(channel_phases[port])
            for component in range(field.components):
                before = source[definition.field][component]
                if component == 0:
                    # A funded octant emission entered the populations paid by the record.
                    before = checked_work(before + funded[definition.field])
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
            transfer_delta=tuple(
                (checked_work(funded[i] - absorbed_by_field[i]),) + (0,) * (f.components - 1)
                for i, f in enumerate(self.fields)
            )
            if any(funded) or any(absorbed_by_field)
            else (),
            outgoing_phases=tuple(tuple(fields) for fields in outgoing_phases)
            if self.allocation_phase != "node"
            else (),
            kept_rays=tuple(kept_rays) if has_rays and any(kept_rays) else (),
            inverse_splits=tuple(inverse_splits),
            annulled=tuple(tuple(v) for v in annulled) if any(any(v) for v in annulled) else (),
            spreads=tuple(spreads),
            homecomings=tuple(homecomings),
            returned_delta=tuple(tuple(v) for v in returned) if any(any(v) for v in returned) else (),
            ray_pushes=tuple(turns),
            decay_draws=tuple(draws),
        )
