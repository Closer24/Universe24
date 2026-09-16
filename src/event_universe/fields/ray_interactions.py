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
from event_universe.core.spatial_state import (
    RAY_PROPERTIES,
    Ray,
    Rays,
    SpatialFieldDefinition,
    validate_ray_participants,
    validate_rays,
)

from .disturbances import interact_values


def _view(ray: Ray, definition: SpatialFieldDefinition) -> Values:
    return (
        pack((ray.amount,)),
        pack(definition.headings[ray.heading]),
        pack((ray.phase,)),
        pack((ray.advance,)),
        pack((ray.interaction_delay,)),
    )


def _replacement(ray: Ray, values: Values, definition: SpatialFieldDefinition) -> Ray:
    if unpack(values[0]) != (ray.amount,) or unpack(values[3]) != (ray.advance,):
        raise ValueError("ray coupling amount and advance are read-only")
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


def apply_ray_interactions(
    rays: tuple[Rays, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
    meter: CostMeter,
    costs: OperationCosts,
) -> tuple[Rays, ...]:
    """Build one complete proposal; no physical owner changes before all guards pass."""
    if not rules:
        return rays
    if len(rays) != len(definitions):
        raise ValueError("ray coupling requires one bundle per spatial field")
    selected = validate_ray_participants(definitions, fields, rules)
    owners = tuple(
        (index, slot)
        for index, bundle in enumerate(rays)
        if index in selected
        for slot in range(len(bundle))
    )
    if len(owners) > MAX_SLOTS:
        raise ValueError("ray coupling exceeds the bounded participant capacity")
    meter.charge("read", 7 * len(owners))
    for index in selected:
        validate_rays(rays[index], definitions[index], fields[definitions[index].field])
        if any(ray.amount <= 0 for ray in rays[index]):
            raise ValueError("ray coupling requires positive amounts")
    # Projection records only borrow values for the shared selector and evaluator.
    # Their stable owner references below are the only commit destinations.
    views: tuple[DisturbanceRecord | None, ...] = tuple(
        None
        if rays[index][slot].interaction_delay
        else DisturbanceRecord(index, _view(rays[index][slot], definitions[index]), ())
        for index, slot in owners
    )
    candidate = [list(bundle) for bundle in rays]
    used: set[int] = set()
    for rule in rules:
        available = tuple(None if slot in used else view for slot, view in enumerate(views))
        for group in participant_groups(rule, available):
            group_views = tuple(views[slot] for slot in group)
            assert all(view is not None for view in group_views)
            before = tuple(view.values for view in group_views if view is not None)
            after = interact_values(rule, before, RAY_PROPERTIES, meter, costs)
            if after is before:
                continue
            for owner, values in zip(group, after, strict=True):
                index, slot = owners[owner]
                replacement = _replacement(rays[index][slot], values, definitions[index])
                validate_rays((replacement,), definitions[index], fields[definitions[index].field])
                candidate[index][slot] = replacement
                meter.charge("update", 5)
            used.update(group)
    return tuple(tuple(bundle) for bundle in candidate)
