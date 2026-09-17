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
    PORT_HEADINGS,
    RAY_PROPERTIES,
    RAY_VIEW_COMPONENTS,
    Heading,
    Layers,
    Ray,
    Rays,
    SpatialFieldDefinition,
    ray_layers,
    stamp_event,
    validate_ray_participants,
    validate_rays,
)

from .disturbances import convert_values, interact_values

Pushes = list[tuple[int, int, int]]


def _view(ray: Ray, definition: SpatialFieldDefinition, family: int) -> Values:
    """The RAY_PROPERTIES view of one ray: its family is the index of its spatial field
    and its charge per quantum is the family's (wave-ray-family-v1)."""
    return (
        pack((ray.amount,)),
        pack(definition.headings[ray.heading]),
        pack((ray.phase,)),
        pack((ray.advance,)),
        pack((ray.interaction_delay,)),
        pack((family,)),
        pack((definition.charge,)),
    )


def _replacement(ray: Ray, values: Values, definition: SpatialFieldDefinition, family: int) -> Ray:
    """One output of an interaction: the ray on its new line, before the event stamp."""
    if unpack(values[0]) != (ray.amount,) or unpack(values[3]) != (ray.advance,):
        raise ValueError("ray coupling amount and advance are read-only")
    if unpack(values[5]) != (family,) or unpack(values[6]) != (definition.charge,):
        raise ValueError("ray coupling family and charge are read-only")
    vector = unpack(values[1])
    if vector == definition.headings[ray.heading]:
        heading = ray.heading
    else:
        try:
            heading = definition.headings.index((vector[0], vector[1], vector[2]))
        except ValueError as error:
            raise ValueError("ray interaction heading is absent from its configured table") from error
    return replace(
        ray,
        heading=heading,
        accumulators=ray.accumulators if heading == ray.heading else (0, 0, 0),
        phase=unpack(values[2])[0],
        interaction_delay=unpack(values[4])[0],
    )


def _events(
    group: tuple[tuple[Ray, SpatialFieldDefinition], ...],
) -> Rays:
    """The events of one interaction: its outputs stamped together with the mask of the
    Ports they leave through and the amount per Port, each a fresh trajectory."""
    return stamp_event(
        tuple(ray for ray, _ in group),
        tuple(definition.headings[ray.heading] for ray, definition in group),
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
    sum over its outputs, beside the rule's own declared invariants."""
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
    if any(stock.values()):
        raise ValueError(f"ray meeting {rule.name} changes the stock of a family")
    products = tuple((kind, ray) for kind, ray in produced if ray.amount)
    stamped = stamp_event(
        tuple(ray for _, ray in products),
        tuple(definitions[kind].headings[ray.heading] for kind, ray in products),
    )
    return tuple((kind, ray) for (kind, _), ray in zip(products, stamped, strict=True))


def _recoil(ray: Ray, definition: SpatialFieldDefinition) -> tuple[Ray, Heading]:
    """A field ray returned reversed by the group it pushed (bound-group-motion-v1):
    a new event ray on the negated heading with the ray's amount, phase and advance,
    stamped as one event on its Port, as the recoil of released-field-v1."""
    heading = definition.headings[ray.heading]
    negated = (-heading[0], -heading[1], -heading[2])
    if negated not in definition.headings:
        raise ValueError("a recoil requires the negated heading in the field's sequence")
    reversed_ray = Ray(
        definition.headings.index(negated), (0, 0, 0), ray.amount, phase=ray.phase, advance=ray.advance
    )
    (stamped,) = stamp_event((reversed_ray,), (negated,))
    return stamped, heading


def _push(
    rule: InteractionDefinition,
    owners: tuple[tuple[int, int], ...],
    views: tuple[DisturbanceRecord | None, ...],
    used: set[int],
    rays: tuple[Rays, ...],
    candidate: list[list[Ray | None]],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    pushes: Pushes,
) -> None:
    """The momentum table of a binding rule that fired (bound-group-motion-v1): every
    resident outbound ray of a named family that no earlier rule met is met by the
    group, the register moved by sign x amount x heading (-1 toward the source,
    which lies opposite the arriving heading) and the field ray returned reversed."""
    for slot, (index, ray_slot) in enumerate(owners):
        sign = rule.momentum_table[index] if index < len(rule.momentum_table) else 0
        if not sign or slot in used or views[slot] is None:
            continue
        ray = rays[index][ray_slot]
        meter.charge("evaluate")
        recoil, heading = _recoil(ray, definitions[index])
        validate_rays((recoil,), definitions[index], fields[definitions[index].field])
        candidate[index][ray_slot] = recoil
        used.add(slot)
        pushes.append(
            (
                checked_work(sign * ray.amount * heading[0]),
                checked_work(sign * ray.amount * heading[1]),
                checked_work(sign * ray.amount * heading[2]),
            )
        )
        meter.charge("update", 5)


def _meet(
    layer: tuple[int, ...],
    rules: tuple[InteractionDefinition, ...],
    rays: tuple[Rays, ...],
    candidate: list[list[Ray | None]],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
    bound: list[int] | None = None,
    pushes: Pushes | None = None,
) -> None:
    """The meeting inside one layer: its rules fire over its rays alone, in declared
    order, each group once; the events are written to the candidate bundles. A rule
    with outputs removes its participants and appends its new event rays. A rule
    without outputs that fires and declares `ray_delay` reports it through `bound`
    (ray-binding-v1): the Node's output-clock delay while its group is held; one
    that declares a `momentum_table` meets the field rays the table names and
    reports each push through `pushes` (bound-group-motion-v1)."""
    owners = tuple((index, slot) for index in layer for slot in range(len(rays[index])))
    if len(owners) > MAX_SLOTS:
        raise ValueError("ray coupling exceeds the bounded participant capacity")
    meter.charge("read", RAY_VIEW_COMPONENTS * len(owners))
    for index in layer:
        validate_rays(rays[index], definitions[index], fields[definitions[index].field])
        if any(ray.amount <= 0 for ray in rays[index]):
            raise ValueError("ray coupling requires positive amounts")
    # Projection records only borrow values for the shared selector and evaluator.
    # Their stable owner references below are the only commit destinations. A
    # returning ray takes part in no group (detector-return-v1).
    views: tuple[DisturbanceRecord | None, ...] = tuple(
        None
        if rays[index][slot].interaction_delay or not rays[index][slot].outbound
        else DisturbanceRecord(index, _view(rays[index][slot], definitions[index], index), ())
        for index, slot in owners
    )
    used: set[int] = set()
    for rule in rules:
        available = tuple(None if slot in used else view for slot, view in enumerate(views))
        for group in participant_groups(rule, available):
            group_views = tuple(views[slot] for slot in group)
            assert all(view is not None for view in group_views)
            if rule.outputs:
                inputs = tuple((owners[o][0], rays[owners[o][0]][owners[o][1]]) for o in group)
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
            if bound is not None and rule.ray_delay:
                bound.append(rule.ray_delay)
            if pushes is not None and rule.momentum_table:
                _push(rule, owners, views, used, rays, candidate, definitions, fields, meter, pushes)


def apply_ray_interactions(
    rays: tuple[Rays, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
    layers: Layers | None = None,
    bound: list[int] | None = None,
    pushes: Pushes | None = None,
) -> tuple[Rays, ...]:
    """Build one complete proposal; no physical owner changes before all guards pass.

    The resident rays are met layer by layer (ray-layers-v1, Highlights 5.1): a
    layer is a connected set of fields that the declared rules couple, its rules
    fire over its rays alone, and a ray of a layer without a firing rule crosses
    unchanged. The layers are derived once by the caller or here from the rules.
    A rule with declared outputs (ray-meeting-conversion-v1) replaces its
    participants by its outputs, new event rays at this Node, with every family's
    stock exact; nothing is left at the Node. `bound`, when given, collects the
    `ray_delay` of every binding rule that fired (ray-binding-v1), and `pushes`
    the momentum every field ray a binding rule's table met gave the group
    (bound-group-motion-v1).
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
        _meet(layer, layer_rules, rays, candidate, definitions, fields, meter, costs, bound, pushes)
    result = tuple(tuple(ray for ray in bundle if ray is not None) for bundle in candidate)
    for index, bundle in enumerate(result):
        if len(bundle) > definitions[index].ray_slots:
            raise ValueError("ray meeting outputs exceed the field's ray slots")
    return result
