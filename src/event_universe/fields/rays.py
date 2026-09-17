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
    ray_phase_step,
    ray_vector,
    stamp_event,
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
    if definition.coherent and len(definition.cosine_table) != definition.phase_steps:
        raise ValueError("ray phase law must be prepared before transport")
    if not 0 <= definition.phase_advance < definition.phase_modulus:
        raise ValueError("kerengonen phase_advance must be below the field's phase width")


def emit_rays(
    amount: int,
    cursor: int,
    definition: SpatialFieldDefinition,
    meter: CostMeter,
    phase: int = 0,
    advance: int = -1,
    heading: int | None = None,
) -> tuple[Rays, int]:
    """Share one emitted amount over the next rays_per_tick headings of the sequence.

    One emission is one event: every ray it creates is stamped with the mask of
    the Ports the emission sends to and the amount sent through each.
    """
    count = definition.rays_per_tick
    headings = len(definition.headings)
    if not 0 <= bounded(cursor) < headings:
        raise ValueError("ray emission cursor must index the heading sequence")
    if type(phase) is not int or not 0 <= phase < definition.phase_modulus:
        raise ValueError("ray emission phase must be below the field's phase width")
    if type(advance) is not int or not -1 <= advance < definition.phase_modulus:
        raise ValueError("ray emission advance must be -1 or below the field's phase width")
    magnitude, sign = abs(bounded(amount)), -1 if amount < 0 else 1
    if heading is not None:
        if type(heading) is not int or not 0 <= heading < headings:
            raise ValueError("directed emission must index the heading sequence")
        if not amount:
            return (), cursor
        meter.charge("route")
        directed = (Ray(heading, (0, 0, 0), amount, phase, advance),)
        return stamp_event(directed, (definition.headings[heading],)), cursor
    base, extra = divmod(magnitude, count)
    meter.charge("read")
    meter.charge("split", count)
    rays = []
    for offset in range(count):
        share = base + int(offset < extra)
        if share:
            rays.append(Ray((cursor + offset) % headings, (0, 0, 0), sign * share, phase, advance))
    stamped = stamp_event(tuple(rays), tuple(definition.headings[ray.heading] for ray in rays))
    # An amount below the sweep count fills only `extra` headings; the cursor then
    # moves on by those, so a small stock still sweeps the whole sequence in turn.
    return stamped, (cursor + (count if base else extra)) % headings


def forward_rays(
    rays: Rays, definition: SpatialFieldDefinition, meter: CostMeter
) -> tuple[tuple[Rays, ...], Rays]:
    """Move every ray that is due one link along its own line; return the ports and the kept.

    On the links metric every ray is due every tick and the Node keeps none. On
    the Euclidean metric a ray hops when its wait passes its heading's pace; a
    ray that waits stays resident, and its phase still advances with the tick,
    forward while outbound and backward on the walk back. A returning ray with
    no steps left is at its event Node and stays resident, inert, with its phase
    unchanged, until the inverse split (detector-return-v1).
    """
    outgoing: list[list[Ray]] = [[] for _ in range(6)]
    kept: list[Ray] = []
    for ray in rays:
        meter.charge("read")
        meter.charge("route")
        if not ray.outbound and ray.steps == 0 and (ray.event_ports or not definition.spread):
            # At its event Node; a returned field quantum of a spreading family has
            # none and walks on along its line (field-spreading-v1, Highlights 5.5).
            kept.append(ray)
            continue
        if ray.interaction_delay:
            if bounded(ray.interaction_delay) < 0:
                raise ValueError("ray interaction delay must be nonnegative")
            kept.append(
                replace(
                    ray, interaction_delay=ray.interaction_delay - 1, phase=_held_phase(ray, definition)
                )
            )
            meter.charge("update", 2)
            continue
        numerator, denominator = heading_pace(definition, ray.heading)
        wait = checked_work(ray.wait + numerator)
        if wait < denominator:
            kept.append(replace(ray, wait=bounded(wait), phase=_held_phase(ray, definition)))
            continue
        lagged = _spend_lag(ray, definition, meter)
        if lagged is not None:
            port, moved = lagged
            if port < 0:
                kept.append(moved)
            else:
                outgoing[port].append(moved)
            continue
        # The DDA walks the ray's momentum register when a push set one, else the
        # heading of its line (ray-momentum-turn-v1): one Link per interval either way.
        port, moved = advance_ray(
            replace(ray, wait=wait - denominator),
            ray_vector(ray, definition),
            definition.phase_modulus,
            definition.phase_advance,
        )
        outgoing[port].append(moved)
    result = tuple(merge_rays(tuple(port_rays)) for port_rays in outgoing)
    meter.charge("send", sum(1 for port_rays in result if port_rays))
    return result, merge_rays(tuple(kept))


def _spend_lag(ray: Ray, definition: SpatialFieldDefinition, meter: CostMeter) -> tuple[int, Ray] | None:
    """Bending by delay (ray-binding-v1, Highlights 3.28): a face-clock lag that has
    reached the phase modulus, one full interval of delay on that side, is spent at
    this departure. On a transverse axis the ray steps one Link toward the lagging
    side (the Port returned), its steps up by one and its phase moved by its rate,
    its heading and event record unchanged: the turn of its line. On its own axis
    the ray waits one interval (Port -1). A ray at its event Node leaves through its
    event's Port first, so a lag is spent from the next Node on; the lowest lagging
    axis is spent first, one Link per interval. None when no lag is due."""
    if not ray.steps or not any(ray.lag):
        return None
    modulus = definition.phase_modulus
    axis = next((a for a in range(3) if abs(ray.lag[a]) >= modulus), None)
    if axis is None:
        return None
    sign = 1 if ray.lag[axis] > 0 else -1
    lag = list(ray.lag)
    lag[axis] = bounded(checked_work(lag[axis] - sign * modulus))
    meter.charge("update", 2)
    spent = replace(ray, lag=(lag[0], lag[1], lag[2]), phase=_held_phase(ray, definition))
    if ray_vector(ray, definition)[axis] != 0:
        return -1, spent
    return 2 * axis + (0 if sign > 0 else 1), replace(spent, steps=bounded(checked_work(ray.steps + 1)))


def hold_rays(
    rays: Rays, definition: SpatialFieldDefinition, meter: CostMeter, *, advance_phase: bool
) -> Rays:
    """Retain the post-interaction rays during one configured local delay interval."""
    meter.charge("read", len(rays))
    if not advance_phase or not definition.kerengonen:
        return rays
    meter.charge("update", len(rays))
    return merge_rays(tuple(replace(ray, phase=_held_phase(ray, definition)) for ray in rays))


def _held_phase(ray: Ray, definition: SpatialFieldDefinition) -> int:
    """The phase of a ray that spends this tick at its Node: one signed step of its rate,
    masked by the family's width; unchanged on a plain field, whose rate is 0."""
    return (ray.phase + ray_phase_step(ray, definition.phase_advance)) & definition.phase_mask
