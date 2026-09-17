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
    RAY_PROPERTIES,
    RAY_VIEW_COMPONENTS,
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
    produced = tuple(
        (kind, _output(values, definitions[kind]))
        for kind, values in zip(rule.outputs, converted[0], strict=True)
    )
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


def _meet(
    layer: tuple[int, ...],
    rules: tuple[InteractionDefinition, ...],
    rays: tuple[Rays, ...],
    candidate: list[list[Ray | None]],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
) -> None:
    """The meeting inside one layer: its rules fire over its rays alone, in declared
    order, each group once; the events are written to the candidate bundles. A rule
    with outputs removes its participants and appends its new event rays."""
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


def apply_ray_interactions(
    rays: tuple[Rays, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
    layers: Layers | None = None,
) -> tuple[Rays, ...]:
    """Build one complete proposal; no physical owner changes before all guards pass.

    The resident rays are met layer by layer (ray-layers-v1, Highlights 5.1): a
    layer is a connected set of fields that the declared rules couple, its rules
    fire over its rays alone, and a ray of a layer without a firing rule crosses
    unchanged. The layers are derived once by the caller or here from the rules.
    A rule with declared outputs (ray-meeting-conversion-v1) replaces its
    participants by its outputs, new event rays at this Node, with every family's
    stock exact; nothing is left at the Node.
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
        _meet(layer, layer_rules, rays, candidate, definitions, fields, meter, costs)
    result = tuple(tuple(ray for ray in bundle if ray is not None) for bundle in candidate)
    for index, bundle in enumerate(result):
        if len(bundle) > definitions[index].ray_slots:
            raise ValueError("ray meeting outputs exceed the field's ray slots")
    return result
