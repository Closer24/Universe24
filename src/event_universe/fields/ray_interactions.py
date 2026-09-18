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
    PORT_HEADINGS,
    RAY_PROPERTIES,
    RAY_VIEW_COMPONENTS,
    RAY_VIEW_COMPONENTS_UNPOLARIZED,
    DecayDraw,
    Heading,
    Layers,
    Ray,
    RayPush,
    Rays,
    SpatialFieldDefinition,
    push_of,
    pushed_ray,
    ray_layers,
    ray_momentum_vector,
    ray_vector,
    return_shadow,
    stamp_event,
    ticket_bit,
    turn_receiver,
    validate_ray_participants,
    validate_rays,
)

from .disturbances import convert_values, evaluate, interact_values

Turns = list[RayPush]
# The draws of the decaying rules at one Node in one cycle (decay-draw-v1), in
# the order they were taken from the Node's ticket stream; the last one carries
# the stream's state after the cycle, and the caller's `ticket` its state before.
Draws = list[DecayDraw]


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
    # input the output reads.
    for position, origin in enumerate(rule.output_sources):
        kind, ray = produced[position]
        produced[position] = (kind, replace(ray, owner=inputs[origin][1].owner))
    for lag in rule.lags:
        # ray-binding-v1, Highlights 3.28: the delay by the declared table, per the
        # Port the source input came through, the whole quanta of amount x entry /
        # unit in phase steps, laid on the output's face clock on that side.
        kind, source = inputs[lag.source]
        port = PORT_HEADINGS.index(definitions[kind].headings[source.heading]) ^ 1
        delay = checked_work(source.amount * lag.table[port]) // lag.per
        meter.charge("evaluate")
        axis, negative = divmod(port, 2)
        target, ray = produced[lag.output]
        clocks = list(ray.lag)
        clocks[axis] = checked_work(clocks[axis] + (-delay if negative else delay))
        produced[lag.output] = (target, replace(ray, lag=(clocks[0], clocks[1], clocks[2])))
        meter.charge("update")
    stock: dict[int, int] = {}
    for kind, ray in inputs:
        stock[kind] = checked_work(stock.get(kind, 0) + ray.amount)
    for kind, ray in produced:
        stock[kind] = checked_work(stock.get(kind, 0) - ray.amount)
    if any(stock.values()) and rule.draw is None:
        # A decaying rule (decay-draw-v1, Highlights 3.26: the weak interaction is
        # a change of family) may move content between families; the total
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


def _table_pushes(
    rule: InteractionDefinition,
    owners: tuple[tuple[int, int], ...],
    views: tuple[DisturbanceRecord | None, ...],
    used: set[int],
    rays: tuple[Rays, ...],
    candidate: list[list[Ray | None]],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    receiver_owner: int,
    receiver: Ray,
    receiver_definition: SpatialFieldDefinition,
) -> list[tuple[int, Ray, Heading, tuple[int, int, int]]]:
    """The shadows a momentum table meets and the push each gives (bit-law-v1,
    point 3): every resident outbound shadow of a named family that no earlier
    rule met, in slot order, whose owner is not the pushed thing's (a thing is
    never pushed by its own shadow: that shadow is home, and the planner absorbs
    it back). Each is turned back on its own steps carrying -push
    (`return_shadow`): its spatial field, the shadow, its heading and the push,
    sign x amount x heading read times the thing's content or charge as the
    rule's `reads` declares (point 16), -1 toward the source, which lies
    opposite the arriving heading. The meeting creates no momentum."""
    met = []
    for slot, (index, ray_slot) in enumerate(owners):
        sign = rule.momentum_table[index] if index < len(rule.momentum_table) else 0
        if not sign or slot in used or views[slot] is None:
            continue
        ray = rays[index][ray_slot]
        if ray.detector != BIT_SHADOW or ray.owner == receiver_owner:
            continue
        meter.charge("evaluate")
        heading = definitions[index].headings[ray.heading]
        push = push_of(
            sign, ray, definitions[index], rule.reads, receiver.amount, receiver_definition.charge
        )
        returned = return_shadow(ray, definitions[index], (-push[0], -push[1], -push[2]))
        validate_rays((returned,), definitions[index], fields[definitions[index].field])
        candidate[index][ray_slot] = returned
        used.add(slot)
        met.append((index, ray, heading, push))
        meter.charge("update", 5)
    return met


def _turn(
    rule: InteractionDefinition,
    receiver_slot: int,
    owners: tuple[tuple[int, int], ...],
    views: tuple[DisturbanceRecord | None, ...],
    used: set[int],
    rays: tuple[Rays, ...],
    candidate: list[list[Ray | None]],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    turns: Turns | None,
) -> None:
    """A thing turns by momentum (ray-momentum-turn-v2 under bit-law-v1): the
    coupling's one unnamed participant, a thing, is pushed by every resident
    outbound shadow of a family the table names that no earlier rule met and
    that is not its own, the group's shadow among them, each push sign x amount x
    heading of the shadow, and each shadow turned back on its steps with -push.
    The thing keeps its amount, phase, bit, heading index and event record; no
    event is stamped and the bit never changes. One record per push, in slot
    order, reports the register before and after."""
    index, slot = owners[receiver_slot]
    ray = rays[index][slot]
    definition = definitions[index]
    used.add(receiver_slot)
    for pusher, field_ray, heading, push in _table_pushes(
        rule,
        owners,
        views,
        used,
        rays,
        candidate,
        definitions,
        fields,
        meter,
        ray.owner,
        ray,
        definition,
    ):
        before = ray_momentum_vector(ray, definition)
        ray = pushed_ray(ray, push, definition)
        meter.charge("update", 4)
        if turns is not None:
            turns.append(
                RayPush(
                    index,
                    ray.amount,
                    before,
                    ray_momentum_vector(ray, definition),
                    pusher,
                    field_ray.amount,
                    heading,
                )
            )
    validate_rays((ray,), definition, fields[definition.field])
    candidate[index][slot] = ray


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
    draws: Draws | None = None,
    ticket: int = 0,
    declared: tuple[InteractionDefinition, ...] = (),
) -> None:
    """The meeting inside one layer: its rules fire over its rays alone, in declared
    order, each group once; the events are written to the candidate bundles. A rule
    with outputs removes its participants and appends its new event rays; a
    coupling of free rays whose table names a participant family pushes its
    unnamed participant and reports each push through `turns`
    (ray-momentum-turn-v1). A rule meets only the rays that arrived at the Node
    (loop-binding-v1, Highlights 3.4: a ray never stops): a ray at its event Node,
    the output of a rule waiting its declared delay there, is met by nothing and
    leaves, so no rule can hold its participants by meeting them again. A rule
    with outputs that declares `draw` is a decaying conversion (decay-draw-v1,
    Highlights 3.26): when its participants meet, the meeting draws once, one draw
    per meeting and not per ray, from the Node's ticket stream (`ticket` its state
    before this cycle, the last of `draws` its state after) with the rule's
    setting; on 1 the rule fires, on 0 it does not and the meeting continues to
    the next rule in declared order. A false guard is no meeting under the rule
    and draws nothing."""
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
        or not rays[index][slot].outbound
        or (rays[index][slot].steps == 0 and rays[index][slot].event_ports)
        or (rays[index][slot].steps == 0 and rays[index][slot].detector == BIT_SHADOW)
        else DisturbanceRecord(index, _view(rays[index][slot], definitions[index], index), ())
        for index, slot in owners
    )
    used: set[int] = set()
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
                    and rays[kind][kind_slot].owner != thing.owner
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
                    rule, slot, owners, views, used, rays, candidate, definitions, fields, meter, turns
                )
            continue
        available = tuple(
            None if slot in used or rays[index][ray_slot].detector == BIT_SHADOW else view
            for slot, ((index, ray_slot), view) in enumerate(zip(owners, views, strict=True))
        )
        for group in participant_groups(rule, available):
            group_views = tuple(views[slot] for slot in group)
            assert all(view is not None for view in group_views)
            if rule.outputs:
                inputs = tuple((owners[o][0], rays[owners[o][0]][owners[o][1]]) for o in group)
                if rule.draw is not None:
                    # decay-draw-v1: the group meets under the rule (its guard read
                    # over the views) and the meeting draws once at the rule's
                    # setting from the Node's stream; the draw reads nothing from
                    # the rays. On 0 the rule does not fire and the rays stay
                    # available to the next rule in declared order.
                    before = tuple(view.values for view in group_views if view is not None)
                    if (
                        rule.when is not None
                        and evaluate(rule.when, (), (), meter, participants=before)[0] <= 0
                    ):
                        continue
                    if draws is None:
                        raise ValueError("a decaying rule draws from the Node's ticket stream")
                    state, bit = ticket_bit(draws[-1].ticket if draws else ticket, *rule.draw)
                    index = (declared or rules).index(rule)
                    draws.append(DecayDraw(index, rule.draw[0], rule.draw[1], state, bit))
                    if not bit:
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
    draws: Draws | None = None,
    ticket: int = 0,
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
    every push a coupling's table gave its thing (ray-momentum-turn-v2). `draws`, when given, collects the
    draw of every meeting of a rule that declares `draw` (decay-draw-v1), taken
    from the Node's ticket stream whose state before this cycle is `ticket`; a
    world without such a rule never touches either.
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
            draws,
            ticket,
            rules,
        )
    result = tuple(tuple(ray for ray in bundle if ray is not None) for bundle in candidate)
    for index, bundle in enumerate(result):
        if len(bundle) > definitions[index].ray_slots:
            raise ValueError("ray meeting outputs exceed the field's ray slots")
    return result
