"""Atomic common indexed operations over complete, locally owned ray bundles."""

from dataclasses import replace

from event_universe.core.coupling_selectors import participant_groups
from event_universe.core.disturbance_state import (
    MAX_SLOTS,
    CostMeter,
    DisturbanceRecord,
    FieldDefinition,
    InteractionDefinition,
    OperationCosts,
    Values,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    BIT_THING,
    MIXING_AMPLITUDE_SCALE,
    PORT_HEADINGS,
    RAY_PROPERTIES,
    RAY_VIEW_COMPONENTS,
    RAY_VIEW_COMPONENTS_UNPOLARIZED,
    Layers,
    Ray,
    RayPush,
    Rays,
    SpatialFieldDefinition,
    arrival_amplitude,
    push_of,
    pushed_ray,
    ray_layers,
    ray_momentum_vector,
    ray_vector,
    return_shadow,
    stamp_event,
    turn_receiver,
    validate_ray_participants,
    validate_rays,
)

from .disturbances import convert_values, evaluate, interact_values

Turns = list[RayPush]


def _view(ray: Ray, definition: SpatialFieldDefinition, family: int) -> Values:
    """The RAY_PROPERTIES view of one ray: its family is the index of its spatial field
    and its charge per quantum is the family's (wave-ray-family-v1); its bit is the
    one it carries, 1 a thing (bit-law-v1); its polarization is the step it
    carries, -1 for none (ray-polarization-v1)."""
    return (
        pack((ray.amount,)),
        pack(definition.headings[ray.heading]),
        pack((ray.phase,)),
        pack((ray.advance,)),
        pack((ray.interaction_delay,)),
        pack((family,)),
        pack((definition.charge,)),
        pack((ray.detector,)),
        pack((ray.polarization,)),
    )


def _replacement(ray: Ray, values: Values, definition: SpatialFieldDefinition, family: int) -> Ray:
    """One output of an interaction: the ray on its new line, before the event stamp."""
    if unpack(values[0]) != (ray.amount,) or unpack(values[3]) != (ray.advance,):
        raise ValueError("ray coupling amount and advance are read-only")
    if unpack(values[5]) != (family,) or unpack(values[6]) != (definition.charge,):
        raise ValueError("ray coupling family and charge are read-only")
    if unpack(values[7]) != (ray.detector,):
        raise ValueError("ray coupling detector is read-only: the bit never changes at a meeting")
    if unpack(values[8]) != (ray.polarization,):
        raise ValueError("ray coupling polarization is read-only")
    vector = unpack(values[1])
    if vector == definition.headings[ray.heading]:
        heading = ray.heading
    else:
        try:
            heading = definition.headings.index((vector[0], vector[1], vector[2]))
        except ValueError as error:
            raise ValueError("ray interaction heading is absent from its configured table") from error
    # A rule that puts the ray on a new line clears its momentum register: the new
    # line is what the rule said (ray-momentum-turn-v1); on the same line it stays.
    return replace(
        ray,
        heading=heading,
        accumulators=ray.accumulators if heading == ray.heading else (0, 0, 0),
        momentum=ray.momentum if heading == ray.heading else None,
        phase=unpack(values[2])[0],
        interaction_delay=unpack(values[4])[0],
    )


def _events(group: tuple[tuple[Ray, SpatialFieldDefinition], ...]) -> Rays:
    """The events of one interaction: its outputs stamped together with the mask of the
    Ports they leave through and the amount per Port, each a fresh trajectory, a
    thing of its input's identity (bit-law-v1)."""
    return stamp_event(
        tuple(ray for ray, _ in group),
        tuple(ray_vector(ray, definition) for ray, definition in group),
    )


def _output(values: Values, definition: SpatialFieldDefinition) -> Ray:
    """One declared output of a meeting (ray-meeting-conversion-v1): a new ray of the
    output's field on its declared line, before the event stamp. Its phase is read
    modulo the field's phase steps; an amount of zero is no ray."""
    vector = unpack(values[1])
    try:
        heading = definition.headings.index((vector[0], vector[1], vector[2]))
    except ValueError as error:
        raise ValueError("ray meeting output heading is absent from its field's table") from error
    return Ray(
        heading,
        (0, 0, 0),
        unpack(values[0])[0],
        phase=unpack(values[2])[0] & definition.phase_mask,
        advance=unpack(values[3])[0],
        interaction_delay=unpack(values[4])[0],
    )


def _convert(
    rule: InteractionDefinition,
    inputs: tuple[tuple[int, Ray], ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
) -> tuple[tuple[int, Ray], ...] | None:
    """The outputs of a meeting with declared outputs, as (field, ray) pairs stamped as
    the events of the meeting, or None when the guard is false. The stock of every
    family is exact across the event: the sum over the inputs of one field equals the
    sum over its outputs, beside the rule's own declared invariants; a decaying rule
    (decay-draw-v1) is the one exception, its outputs may change family with the
    total amount exact. The outputs are things (bit-law-v1), each carrying the
    identity of its source input (the `input` of the output, input 0 by default)."""
    before = tuple(_view(ray, definitions[kind], kind) for kind, ray in inputs)
    converted = convert_values(rule, before, RAY_PROPERTIES, meter, costs)
    if converted is None:
        return None
    for kind, values in zip(rule.outputs, converted[0], strict=True):
        # wave-ray-family-v1: an output is a ray of its field, with its field's charge.
        if unpack(values[5]) != (kind,) or unpack(values[6]) != (definitions[kind].charge,):
            raise ValueError("ray meeting outputs carry the family and charge of their field")
    produced = [
        (kind, _output(values, definitions[kind]))
        for kind, values in zip(rule.outputs, converted[0], strict=True)
    ]
    # ray-polarization-v1: each output carries its source input's polarization
    # unless it declares its own, input i's or a value; a rule that declares one
    # is charged one update per output for it.
    for position, (by_input, value) in enumerate(rule.output_polarization):
        polarization = inputs[value][1].polarization if by_input == 0 else value
        kind, ray = produced[position]
        produced[position] = (kind, replace(ray, polarization=polarization))
        if rule.polarization_declared:
            meter.charge("update")
    # bit-law-v1: each output is the thing its source input is, the owner of the
    # input the output reads; it carries that input's clock remainder and push
    # remainder on (clock-readings-v1: the corner table reproduces the thing that
    # entered, clock and all) and its passages, 0 when this rule is the group
    # breaking (point 20: the outputs of a decay are fresh things).
    for position, origin in enumerate(rule.output_sources):
        kind, ray = produced[position]
        source = inputs[origin][1]
        produced[position] = (
            kind,
            replace(
                ray,
                owner=source.owner,
                remainder=source.remainder if definitions[kind].clock else 0,
                push_remainder=source.push_remainder,
                periods=0 if rule.decay is not None else source.periods,
            ),
        )
    stock: dict[int, int] = {}
    for kind, ray in inputs:
        stock[kind] = checked_work(stock.get(kind, 0) + ray.amount)
    for kind, ray in produced:
        stock[kind] = checked_work(stock.get(kind, 0) - ray.amount)
    if any(stock.values()) and rule.decay is None:
        # A decay (Highlights 5.4 point 20 and 3.26: the weak interaction is a
        # change of family) may move content between families; the total
        # amount, the declared invariants and the appended charge invariant were
        # checked above, and the caller books what each family lost or gained.
        raise ValueError(f"ray meeting {rule.name} changes the stock of a family")
    # An output carries the source sign of the first input of its own family (the
    # recoil keeps its field's sign, field-spreading-v1); a family the inputs do
    # not hold starts at 0.
    signs: dict[int, int] = {}
    for kind, ray in inputs:
        signs.setdefault(kind, ray.source_sign)
    produced = [(kind, replace(ray, source_sign=signs.get(kind, 0))) for kind, ray in produced]
    products = tuple((kind, ray) for kind, ray in produced if ray.amount)
    stamped = stamp_event(
        tuple(ray for _, ray in products),
        tuple(definitions[kind].headings[ray.heading] for kind, ray in products),
    )
    return tuple((kind, ray) for (kind, _), ray in zip(products, stamped, strict=True))


def rides_with(
    shadow: Ray,
    thing: Ray,
    shadow_definition: SpatialFieldDefinition,
    thing_definition: SpatialFieldDefinition,
) -> bool:
    """One meeting, one push (return-field-v1; the orchestrator's reading of the
    definition of a meeting, two rays at one Node in one interval, to be
    confirmed by the model owner): a shadow that arrived at the Node through
    the Port the thing itself arrived by, this interval, left the previous
    Node together with the thing on the same lane (lanes-v1: one shadow per
    owner per lane), and is the meeting that already happened continuing, not
    a new one; it pushes nothing here and mixes on as any share. The Port a ray
    came in by is its in-lane, the one behind its heading (`lane_of`), read by
    the heading vector so that two families' heading tables compare; a ray off
    the Port headings never rides. Both must have walked a Link (steps at
    least 1): a share fresh at this Node (turned back or re-released here, steps
    0), a body's token and a thing at its event Node never ride, so a returning
    share meets a body at rest as a new meeting every time."""
    if not shadow.steps or not thing.steps:
        return False
    shadow_heading = shadow_definition.headings[shadow.heading]
    thing_heading = thing_definition.headings[thing.heading]
    if shadow_heading not in PORT_HEADINGS or thing_heading not in PORT_HEADINGS:
        return False
    return shadow_heading == thing_heading


def _turn(
    rule: InteractionDefinition,
    receiver_slot: int,
    owners: tuple[tuple[int, int], ...],
    views: tuple[DisturbanceRecord | None, ...],
    used: set[int],
    taken: dict[int, int],
    rays: tuple[Rays, ...],
    candidate: list[list[Ray | None]],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    turns: Turns | None,
) -> None:
    """A thing turns by momentum (ray-momentum-turn-v3 under clock-readings-v1,
    Highlights 5.4 points 3, 15, 16 and 18): the coupling's one unnamed
    participant, a thing, is pushed by every resident outbound shadow of a family
    the table names that is not its own, the group's shadow among them, each
    push the rule's reading of the shadow's message (`push_of`: the table's sign
    x amount x heading x the thing's content, or x the owner's charge over its
    content x the thing's charge, the latter accumulated exactly on the thing's
    push remainder; a returning share pushes with the opposite sign), and each
    shadow turned back with the opposite sign carrying -push (return-field-v1).
    The same shadows are read once per momentum rule of the thing (point 18,
    gravity and electricity the same shadows read twice): a shadow an earlier
    rule turned back for this thing pushes it again under this rule's reading
    and carries the sum home; a shadow another thing took is left to it. The
    thing keeps its amount, phase, bit, heading and event record; no event is
    stamped and the bit never changes. One record per push, in slot order,
    reports the momentum before and after."""
    index, slot = owners[receiver_slot]
    ray = candidate[index][slot]
    assert ray is not None
    definition = definitions[index]
    taken[receiver_slot] = receiver_slot
    # The groups whose amplitude this rule's wait has read for this thing
    # (wait-reads-v1): once per group of shadows arriving; and the thing's
    # remainder of amplitude below a whole unit, carried across the groups.
    amplitudes_read: set[tuple[int, int, int, int]] = set()
    wait_remainder = ray.wait_remainder
    for shadow_slot, (kind, ray_slot) in enumerate(owners):
        sign = rule.momentum_table[kind] if kind < len(rule.momentum_table) else 0
        if not sign or shadow_slot in used or views[shadow_slot] is None:
            continue
        shadow = rays[kind][ray_slot]
        if shadow.detector != BIT_SHADOW or shadow.owner in (ray.owner, *ray.owners):
            continue
        if taken.get(shadow_slot, receiver_slot) != receiver_slot:
            continue
        if rides_with(shadow, ray, definitions[kind], definition):
            continue
        meter.charge("evaluate")
        heading = definitions[kind].headings[shadow.heading]
        push, remainder = push_of(
            sign,
            shadow,
            definitions[kind],
            rule.reads,
            ray.amount,
            definition.charge,
            ray.push_remainder,
        )
        before = ray_momentum_vector(ray, definition)
        wait_quanta: int | None = None
        if definition.wait_reads == "amplitude":
            # The wait reads the amplitude (wait-reads-v1, a declared coupling
            # option): once per group of the shadows arriving at this Node (the
            # mixing's group: owner, sign, polarization, flow), the size of their
            # coherent sum in whole units of amplitude (32 at the engine's scale
            # is one quantum's), read as the push reads the amount (point 16);
            # the push itself reads the amount as before.
            group = (shadow.owner, shadow.source_sign, shadow.polarization, shadow.outbound)
            wait_quanta = 0
            if group not in amplitudes_read:
                amplitudes_read.add(group)
                members = tuple(
                    member
                    for member in rays[kind]
                    if member.detector == BIT_SHADOW
                    and not member.parked
                    and member.steps >= 1
                    and (member.owner, member.source_sign, member.polarization, member.outbound) == group
                )
                meter.charge("evaluate", len(members))
                # The remainder (feature 16f part 2): the size joins what the
                # thing holds below a whole unit, the whole units are read now
                # and the rest stays on the thing, exact, as `push_remainder`.
                size = checked_work(wait_remainder + arrival_amplitude(members, definitions[kind]))
                units, wait_remainder = divmod(size, MIXING_AMPLITUDE_SCALE)
                if units:
                    unit_push, _ = push_of(
                        sign,
                        replace(shadow, amount=units),
                        definitions[kind],
                        rule.reads,
                        ray.amount,
                        definition.charge,
                    )
                    wait_quanta = abs(unit_push[0]) + abs(unit_push[1]) + abs(unit_push[2])
        ray = replace(
            pushed_ray(ray, push, definition, wait_quanta),
            push_remainder=remainder,
            wait_remainder=wait_remainder,
        )
        meter.charge("update", 4)
        carried = (-push[0], -push[1], -push[2])
        earlier = candidate[kind][ray_slot] if shadow_slot in taken else None
        if earlier is not None and earlier.outbound != shadow.outbound:
            # Read twice: the shadow already turned back this cycle carries the
            # sum of its pushes (return-field-v1).
            home = earlier.momentum if earlier.momentum is not None else (0, 0, 0)
            summed = (
                checked_work(home[0] + carried[0]),
                checked_work(home[1] + carried[1]),
                checked_work(home[2] + carried[2]),
            )
            returned = replace(earlier, momentum=summed if any(summed) else None)
        else:
            returned = return_shadow(shadow, definitions[kind], carried)
        if definitions[kind].shadow_wait_reads == "thing":
            # The shadow's wait, the thing reading (shadow-wait-v1): the share read
            # by a thing owes n / d intervals per whole quantum of the push it
            # gave, before it leaves this Node; read twice, the sum.
            quanta = abs(push[0]) + abs(push[1]) + abs(push[2])
            returned = replace(
                returned,
                owed=checked_work(
                    returned.owed + checked_work(quanta * definitions[kind].shadow_wait_numerator)
                ),
            )
        validate_rays((returned,), definitions[kind], fields[definitions[kind].field])
        candidate[kind][ray_slot] = returned
        taken[shadow_slot] = receiver_slot
        meter.charge("update", 5)
        if turns is not None:
            turns.append(
                RayPush(
                    index,
                    ray.amount,
                    before,
                    ray_momentum_vector(ray, definition),
                    kind,
                    shadow.amount,
                    heading,
                )
            )
    validate_rays((ray,), definition, fields[definition.field])
    candidate[index][slot] = ray


def _decay_passes(rule: InteractionDefinition, inputs: tuple[tuple[int, Ray], ...]) -> bool:
    """Whether the group breaks at this meeting under the rule's declared decay
    condition (Highlights 5.4 point 20, clock-readings-v1): `after_periods` n,
    the group breaks at its n-th meeting under the rule (its passages counted on
    its rays, `periods`); `content_at_most` c, it breaks when the content of the
    rays met is at most c. Deterministic: the state of the group, nothing else."""
    kind, value = rule.decay if rule.decay is not None else ("", 0)
    if kind == "after_periods":
        return max(ray.periods for _, ray in inputs) + 1 >= value
    if kind == "content_at_most":
        return sum(ray.amount for _, ray in inputs) <= value
    raise ValueError("a decay is after_periods or content_at_most (clock-readings-v1, point 20)")


def _meet(
    layer: tuple[int, ...],
    rules: tuple[InteractionDefinition, ...],
    rays: tuple[Rays, ...],
    candidate: list[list[Ray | None]],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
    turns: Turns | None = None,
) -> None:
    """The meeting inside one layer: its rules fire over its rays alone, in declared
    order, each group once; the events are written to the candidate bundles. A rule
    with outputs removes its participants and appends its new event rays; a
    coupling of free rays whose table names a participant family pushes its
    unnamed participant and reports each push through `turns`
    (ray-momentum-turn-v3). A rule meets only the rays that arrived at the Node
    (loop-binding-v1, Highlights 3.4: a ray never stops): a ray at its event Node,
    the output of a rule waiting its declared delay there, is met by nothing and
    leaves, so no rule can hold its participants by meeting them again. A rule
    with outputs that declares `decay` is a group breaking by a table
    (clock-readings-v1, Highlights 5.4 point 20): when its participants meet, the
    declared condition on their state decides; met, the rule fires and its
    outputs are fresh things; not met, the meeting counts as one passage on the
    rays (`periods`, read by `after_periods`) and continues to the next rule in
    declared order, whose outputs carry the count on. A false guard is no
    meeting under the rule and counts nothing. Nothing is drawn."""
    owners = tuple((index, slot) for index in layer for slot in range(len(rays[index])))
    if len(owners) > MAX_SLOTS:
        raise ValueError("ray coupling exceeds the bounded participant capacity")
    # ray-polarization-v1: the polarization component is read when a rule of the
    # layer names it; a layer whose rules do not reads the view it read before.
    components = (
        RAY_VIEW_COMPONENTS
        if any(rule.polarization_declared for rule in rules)
        else RAY_VIEW_COMPONENTS_UNPOLARIZED
    )
    meter.charge("read", components * len(owners))
    for index in layer:
        validate_rays(rays[index], definitions[index], fields[definitions[index].field])
        if any(ray.amount <= 0 for ray in rays[index]):
            raise ValueError("ray coupling requires positive amounts")
    # Projection records only borrow values for the shared selector and evaluator.
    # Their stable owner references below are the only commit destinations. A
    # returning ray takes part in no group (detector-return-v1), and neither does
    # an event ray still at its event Node (steps 0 with an event stamp): the
    # output of a rule waiting its delay here arrived nowhere (loop-binding-v1),
    # nor a shadow at steps 0, a re-release departing (bit-law-v1). A thing with
    # no event, an external body's token or a direct caller's ray, is met as it
    # always was. A shadow is met by a momentum table alone (bit-law-v1, points 3
    # and 4): the declared tables with outputs or assignments are meetings of
    # things, and a shadow among their participants is not there for them; a
    # table never pushes with a thing of a named family, which crosses.
    views: tuple[DisturbanceRecord | None, ...] = tuple(
        None
        if rays[index][slot].interaction_delay
        or (not rays[index][slot].outbound and rays[index][slot].detector == BIT_THING)
        or (rays[index][slot].steps == 0 and rays[index][slot].event_ports)
        or (rays[index][slot].steps == 0 and rays[index][slot].detector == BIT_SHADOW)
        else DisturbanceRecord(index, _view(rays[index][slot], definitions[index], index), ())
        for index, slot in owners
    )
    used: set[int] = set()
    # The shadows turned back this cycle and the thing each pushed, and the
    # things pushed, each its own entry (point 18: the same shadows read by every
    # momentum rule of that thing, once each; a pushed thing is met by no rule
    # with outputs or assignments this cycle, as before).
    taken: dict[int, int] = {}
    # The rays as the rules see them: a passage under a decay rule is counted
    # here before the next rule reads its inputs.
    current: list[list[Ray]] = [list(bundle) for bundle in rays]
    for rule in rules:
        receiver = turn_receiver(rule)
        if receiver is not None:
            # A coupling with a momentum table (ray-momentum-turn-v2 under
            # bit-law-v1, point 3): the thing met, a resident thing of the
            # receiver role's families, is pushed by every resident outbound
            # shadow of a family the table names that is not its own, whatever
            # role that shadow's family is written in; the shadows of its own
            # family push it too, when their owner is another thing. One push
            # per receiver in slot order; the guard is read over the receiver's
            # view and the first shadow's, in role order.
            if receiver < 0:
                continue
            receiver_kinds = set(rule.participants[receiver])
            for slot, ((index, ray_slot), view) in enumerate(zip(owners, views, strict=True)):
                if view is None or slot in used or index not in receiver_kinds:
                    continue
                thing = rays[index][ray_slot]
                if thing.detector != BIT_THING:
                    continue
                shadows = [
                    other
                    for other, ((kind, kind_slot), other_view) in enumerate(
                        zip(owners, views, strict=True)
                    )
                    if other_view is not None
                    and other not in used
                    and kind < len(rule.momentum_table)
                    and rule.momentum_table[kind]
                    and rays[kind][kind_slot].detector == BIT_SHADOW
                    and rays[kind][kind_slot].owner not in (thing.owner, *thing.owners)
                    and taken.get(other, slot) == slot
                    and not rides_with(
                        rays[kind][kind_slot], thing, definitions[kind], definitions[index]
                    )
                ]
                if not shadows:
                    continue
                if rule.when is not None:
                    ordered = [views[shadows[0]]] * len(rule.participants)
                    ordered[receiver] = view
                    before = tuple(item.values for item in ordered if item is not None)
                    if evaluate(rule.when, (), (), meter, participants=before)[0] <= 0:
                        continue
                meter.charge("couple")
                _turn(
                    rule,
                    slot,
                    owners,
                    views,
                    used,
                    taken,
                    rays,
                    candidate,
                    definitions,
                    fields,
                    meter,
                    turns,
                )
            continue
        available = tuple(
            None
            if slot in used or slot in taken or rays[index][ray_slot].detector == BIT_SHADOW
            else view
            for slot, ((index, ray_slot), view) in enumerate(zip(owners, views, strict=True))
        )
        for group in participant_groups(rule, available):
            group_views = tuple(views[slot] for slot in group)
            assert all(view is not None for view in group_views)
            if rule.outputs:
                inputs = tuple((owners[o][0], current[owners[o][0]][owners[o][1]]) for o in group)
                if rule.decay is not None:
                    # The decay table (clock-readings-v1, point 20): the group meets
                    # under the rule (its guard read over the views) and its own
                    # state decides; not met, this meeting is one passage of the
                    # group and the rays stay available to the next rule in
                    # declared order, their count carried on.
                    before = tuple(view.values for view in group_views if view is not None)
                    if (
                        rule.when is not None
                        and evaluate(rule.when, (), (), meter, participants=before)[0] <= 0
                    ):
                        continue
                    meter.charge("evaluate")
                    if not _decay_passes(rule, inputs):
                        for owner in group:
                            index, slot = owners[owner]
                            passed = replace(
                                current[index][slot], periods=current[index][slot].periods + 1
                            )
                            current[index][slot] = passed
                            if candidate[index][slot] is not None:
                                candidate[index][slot] = passed
                            meter.charge("update")
                        continue
                products = _convert(rule, inputs, definitions, meter, costs)
                if products is None:
                    continue
                for owner in group:
                    index, slot = owners[owner]
                    candidate[index][slot] = None
                    meter.charge("update")
                for kind, product in products:
                    validate_rays((product,), definitions[kind], fields[definitions[kind].field])
                    candidate[kind].append(product)
                    meter.charge("update", 5)
                used.update(group)
                continue
            before = tuple(view.values for view in group_views if view is not None)
            after = interact_values(rule, before, RAY_PROPERTIES, meter, costs)
            if after is before:
                continue
            outputs = tuple(
                (_replacement(rays[index][slot], values, definitions[index], index), definitions[index])
                for (index, slot), values in zip((owners[o] for o in group), after, strict=True)
            )
            for owner, replacement in zip(group, _events(outputs), strict=True):
                index, slot = owners[owner]
                validate_rays((replacement,), definitions[index], fields[definitions[index].field])
                candidate[index][slot] = replacement
                meter.charge("update", 5)
            used.update(group)


def apply_ray_interactions(
    rays: tuple[Rays, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
    layers: Layers | None = None,
    turns: Turns | None = None,
) -> tuple[Rays, ...]:
    """Build one complete proposal; no physical owner changes before all guards pass.

    The resident rays are met layer by layer (ray-layers-v1, Highlights 5.1): a
    layer is a connected set of fields that the declared rules couple, its rules
    fire over its rays alone, and a ray of a layer without a firing rule crosses
    unchanged. The layers are derived once by the caller or here from the rules.
    A rule with declared outputs (ray-meeting-conversion-v1) replaces its
    participants by its outputs, new event rays at this Node, with every family's
    stock exact; nothing is left at the Node. The outputs of every group that
    fires are things (bit-law-v1). `turns`, when given, collects the record of
    every push a coupling's table gave its thing (ray-momentum-turn-v3); a rule
    with `decay` breaks its group by its declared condition (clock-readings-v1,
    point 20), nothing is drawn.
    """
    if not rules:
        return rays
    if len(rays) != len(definitions):
        raise ValueError("ray coupling requires one bundle per spatial field")
    selected = validate_ray_participants(definitions, fields, rules)
    if layers is None:
        layers = ray_layers(definitions, rules)
    candidate: list[list[Ray | None]] = [list(bundle) for bundle in rays]
    for layer in layers:
        if not selected.intersection(layer):
            continue
        # A rule belongs to the layer that holds every field its roles select.
        layer_rules = tuple(
            rule for rule in rules if all(kind in layer for role in rule.participants for kind in role)
        )
        _meet(
            layer,
            layer_rules,
            rays,
            candidate,
            definitions,
            fields,
            meter,
            costs,
            turns,
        )
    result = tuple(tuple(ray for ray in bundle if ray is not None) for bundle in candidate)
    for index, bundle in enumerate(result):
        if len(bundle) > definitions[index].ray_slots:
            raise ValueError("ray meeting outputs exceed the field's ray slots")
    return result
