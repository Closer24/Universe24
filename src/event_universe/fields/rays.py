"""Pure emission and forwarding for straight-moving ray fields."""

from event_universe.core.disturbance_state import CostMeter, FieldDefinition, bounded
from event_universe.core.spatial_state import (
    MAX_HEADINGS,
    MAX_RAY_SLOTS,
    Ray,
    Rays,
    SpatialFieldDefinition,
    advance_ray,
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
    amount: int, cursor: int, definition: SpatialFieldDefinition, meter: CostMeter, phase: int = 0
) -> tuple[Rays, int]:
    """Share one emitted amount over the next rays_per_tick headings of the sequence."""
    count = definition.rays_per_tick
    headings = len(definition.headings)
    if not 0 <= bounded(cursor) < headings:
        raise ValueError("ray emission cursor must index the heading sequence")
    if not 0 <= phase < max(definition.phase_steps, 1):
        raise ValueError("ray emission phase must index the field's phase steps")
    magnitude, sign = abs(bounded(amount)), -1 if amount < 0 else 1
    base, extra = divmod(magnitude, count)
    meter.charge("read")
    meter.charge("split", count)
    rays = []
    for offset in range(count):
        share = base + int(offset < extra)
        if share:
            rays.append(Ray((cursor + offset) % headings, (0, 0, 0), sign * share, phase))
    return tuple(rays), (cursor + count) % headings


def forward_rays(rays: Rays, definition: SpatialFieldDefinition, meter: CostMeter) -> tuple[Rays, ...]:
    """Move every resident ray one link along its own line; the Node keeps none."""
    outgoing: list[list[Ray]] = [[] for _ in range(6)]
    for ray in rays:
        meter.charge("read")
        meter.charge("route")
        port, moved = advance_ray(
            ray,
            definition.headings[ray.heading],
            definition.phase_steps,
            definition.phase_advance,
        )
        outgoing[port].append(moved)
    result = tuple(merge_rays(tuple(port_rays)) for port_rays in outgoing)
    meter.charge("send", sum(1 for port_rays in result if port_rays))
    return result
