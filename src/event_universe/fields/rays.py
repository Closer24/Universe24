"""Pure emission and forwarding for straight-moving ray fields."""

from dataclasses import replace

from event_universe.core.disturbance_state import CostMeter, FieldDefinition, bounded
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    MAX_HEADINGS,
    MAX_RAY_SLOTS,
    Ray,
    Rays,
    SpatialFieldDefinition,
    advance_ray,
    heading_pace,
    merge_rays,
    validate_heading,
)


def validate_ray_definition(definition: SpatialFieldDefinition, field: FieldDefinition) -> None:
    if not definition.rays:
        raise ValueError("ray arithmetic requires ray transport")
    if field.components != 1:
        raise ValueError("ray transport requires a scalar field")
    if not 1 <= len(definition.headings) <= MAX_HEADINGS:
        raise ValueError("ray transport requires one to 65536 headings")
    for heading in definition.headings:
        validate_heading(heading)
    if not 1 <= definition.ray_slots <= MAX_RAY_SLOTS:
        raise ValueError("ray_slots must be between 1 and 4096")
    if not 1 <= definition.rays_per_tick <= definition.ray_slots:
        raise ValueError("rays_per_tick must be between 1 and ray_slots")
    if definition.kerengonen:
        if len(definition.cosine_table) != definition.phase_steps:
            raise ValueError("ray phase law must be prepared before transport")
        if not 0 <= definition.phase_advance < definition.phase_steps:
            raise ValueError("kerengonen phase_advance must be below phase_steps")


def emit_rays(
    amount: int,
    cursor: int,
    definition: SpatialFieldDefinition,
    meter: CostMeter,
    phase: int = 0,
    advance: int = -1,
    heading: int | None = None,
) -> tuple[Rays, int]:
    """Share one emitted amount over the next rays_per_tick headings of the sequence."""
    count = definition.rays_per_tick
    headings = len(definition.headings)
    if not 0 <= bounded(cursor) < headings:
        raise ValueError("ray emission cursor must index the heading sequence")
    if not 0 <= phase < max(definition.phase_steps, 1):
        raise ValueError("ray emission phase must index the field's phase steps")
    if not -1 <= advance < max(definition.phase_steps, 1):
        raise ValueError("ray emission advance must be -1 or index the field's phase steps")
    magnitude, sign = abs(bounded(amount)), -1 if amount < 0 else 1
    if heading is not None:
        if type(heading) is not int or not 0 <= heading < headings:
            raise ValueError("directed emission must index the heading sequence")
        if not amount:
            return (), cursor
        meter.charge("route")
        return (Ray(heading, (0, 0, 0), amount, phase, advance),), cursor
    base, extra = divmod(magnitude, count)
    meter.charge("read")
    meter.charge("split", count)
    rays = []
    for offset in range(count):
        share = base + int(offset < extra)
        if share:
            rays.append(Ray((cursor + offset) % headings, (0, 0, 0), sign * share, phase, advance))
    # An amount below the sweep count fills only `extra` headings; the cursor then
    # moves on by those, so a small stock still sweeps the whole sequence in turn.
    return tuple(rays), (cursor + (count if base else extra)) % headings


def forward_rays(
    rays: Rays, definition: SpatialFieldDefinition, meter: CostMeter
) -> tuple[tuple[Rays, ...], Rays]:
    """Move every ray that is due one link along its own line; return the ports and the kept.

    On the links metric every ray is due every tick and the Node keeps none. On
    the Euclidean metric a ray hops when its wait passes its heading's pace; a
    ray that waits stays resident, and its phase still advances with the tick.
    """
    outgoing: list[list[Ray]] = [[] for _ in range(6)]
    kept: list[Ray] = []
    for ray in rays:
        meter.charge("read")
        meter.charge("route")
        if ray.interaction_delay:
            if bounded(ray.interaction_delay) < 0:
                raise ValueError("ray interaction delay must be nonnegative")
            step = ray.advance if ray.advance >= 0 else definition.phase_advance
            phase = (ray.phase + step) % definition.phase_steps if definition.phase_steps else ray.phase
            kept.append(replace(ray, interaction_delay=ray.interaction_delay - 1, phase=phase))
            meter.charge("update", 2)
            continue
        numerator, denominator = heading_pace(definition, ray.heading)
        wait = checked_work(ray.wait + numerator)
        if wait < denominator:
            step = ray.advance if ray.advance >= 0 else definition.phase_advance
            phase = (ray.phase + step) % definition.phase_steps if definition.phase_steps else ray.phase
            kept.append(replace(ray, wait=bounded(wait), phase=phase))
            continue
        port, moved = advance_ray(
            replace(ray, wait=wait - denominator),
            definition.headings[ray.heading],
            definition.phase_steps,
            definition.phase_advance,
        )
        outgoing[port].append(moved)
    result = tuple(merge_rays(tuple(port_rays)) for port_rays in outgoing)
    meter.charge("send", sum(1 for port_rays in result if port_rays))
    return result, merge_rays(tuple(kept))


def hold_rays(
    rays: Rays, definition: SpatialFieldDefinition, meter: CostMeter, *, advance_phase: bool
) -> Rays:
    """Retain the post-interaction rays during one configured local delay interval."""
    meter.charge("read", len(rays))
    if not advance_phase or not definition.phase_steps:
        return rays
    meter.charge("update", len(rays))
    return merge_rays(
        tuple(
            replace(
                ray,
                phase=(ray.phase + (ray.advance if ray.advance >= 0 else definition.phase_advance))
                % definition.phase_steps,
            )
            for ray in rays
        )
    )
