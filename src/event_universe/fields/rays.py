"""Pure emission and forwarding for straight-moving ray fields."""

from dataclasses import dataclass, replace

from event_universe.core.disturbance_state import CostMeter, FieldDefinition, bounded
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    BIT_THING,
    MAX_HEADINGS,
    MAX_RAY_SLOTS,
    POLARIZATION_NONE,
    PORT_HEADINGS,
    Ray,
    RayMergeKey,
    Rays,
    SpatialFieldDefinition,
    advance_ray,
    clock_step,
    heading_pace,
    ledger_momentum,
    merge_rays,
    phase_of_sum,
    ray_merge_key,
    ray_vector,
    stamp_event,
    step_thing,
    tick_clock,
    validate_heading,
)


@dataclass(frozen=True, slots=True)
class Departures:
    """The account of one Node's departures (clock-readings-v1): the phase steps
    the things made this interval (point 11, the computation) and the momentum
    they spent on their steps (the settled rule (i)), content x the new heading
    per step."""

    phase_steps: int = 0
    spent: tuple[int, int, int] = (0, 0, 0)


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


def emit_rays(
    amount: int,
    cursor: int,
    definition: SpatialFieldDefinition,
    meter: CostMeter,
    phase: int = 0,
    advance: int = -1,
    heading: int | None = None,
    polarization: int = POLARIZATION_NONE,
) -> tuple[Rays, int]:
    """Share one emitted amount over the next rays_per_tick headings of the sequence.

    One emission is one event: every ray it creates is stamped with the mask of
    the Ports the emission sends to and the amount sent through each, and carries
    the emission's declared polarization, none by default (ray-polarization-v1).
    """
    count = definition.rays_per_tick
    headings = len(definition.headings)
    if not 0 <= bounded(cursor) < headings:
        raise ValueError("ray emission cursor must index the heading sequence")
    if type(phase) is not int or not 0 <= phase < definition.phase_modulus:
        raise ValueError("ray emission phase must be below the field's phase width")
    if type(advance) is not int or not -1 <= advance < definition.phase_modulus:
        raise ValueError("ray emission advance must be -1 or below the field's phase width")
    if type(polarization) is not int or not (
        polarization == POLARIZATION_NONE or 0 <= polarization < definition.polarization_modulus
    ):
        raise ValueError(
            "ray emission polarization must be none (-1) or a step below the family's "
            "polarization circle"
        )
    magnitude, sign = abs(bounded(amount)), -1 if amount < 0 else 1
    if heading is not None:
        if type(heading) is not int or not 0 <= heading < headings:
            raise ValueError("directed emission must index the heading sequence")
        if not amount:
            return (), cursor
        meter.charge("route")
        directed = (Ray(heading, (0, 0, 0), amount, phase, advance, polarization=polarization),)
        return stamp_event(directed, (definition.headings[heading],)), cursor
    base, extra = divmod(magnitude, count)
    meter.charge("read")
    meter.charge("split", count)
    rays = []
    for offset in range(count):
        share = base + int(offset < extra)
        if share:
            rays.append(
                Ray(
                    (cursor + offset) % headings,
                    (0, 0, 0),
                    sign * share,
                    phase,
                    advance,
                    polarization=polarization,
                )
            )
    stamped = stamp_event(tuple(rays), tuple(definition.headings[ray.heading] for ray in rays))
    # An amount below the sweep count fills only `extra` headings; the cursor then
    # moves on by those, so a small stock still sweeps the whole sequence in turn.
    return stamped, (cursor + (count if base else extra)) % headings


class LaneClaims:
    """The real slots of a Node's six out-lanes in one interval (lanes-v1,
    Highlights 5.4 point 25), shared by every family of the Node's cycle: the
    family and the merge key of the one real ray leaving through each Port, or
    None while the lane is free. Rays of one key merge into one ray, so they
    hold one slot; a second real of another key on a taken lane is refused, as
    no Port ever sends two."""

    __slots__ = ("taken",)

    def __init__(self) -> None:
        self.taken: list[tuple[int, RayMergeKey] | None] = [None] * 6

    def free(self, port: int) -> bool:
        return self.taken[port] is None

    def claim(self, port: int, family: int, ray: Ray) -> None:
        """Take the lane for a real ray. A second real of the same family given
        the lane in this interval joins the first: the two are one real ray
        (`merge_lane`; the model owner, 2026-09-18), and the first keeps the
        slot. A real of another family is a meeting the table of the pair
        decides, which a departure cannot hold: refused."""
        held = (family, ray_merge_key(ray))
        taken = self.taken[port]
        if taken is None:
            self.taken[port] = held
        elif taken[0] != family:
            raise ValueError(
                "two real rays of different families on one lane are a meeting the table of "
                "the pair decides, not a departure (Highlights 5.4, point 25)"
            )

    def release(self, port: int, family: int, ray: Ray) -> None:
        if self.taken[port] == (family, ray_merge_key(ray)):
            self.taken[port] = None


def _on_lane(ray: Ray, definition: SpatialFieldDefinition) -> bool:
    """Whether a departing ray takes a real slot (lanes-v1): a thing on one of the
    six Port lines. The lane is one direction of a Port, so a ray of the old ray
    worlds on a line that is not a Port heading holds none."""
    return ray.detector == BIT_THING and definition.headings[ray.heading] in PORT_HEADINGS


def merge_lane(rays: Rays, port: int, claims: LaneClaims, definition: SpatialFieldDefinition) -> Rays:
    """The real rays of one family given one out-lane in one interval are one
    real ray (lanes-v1, Highlights 5.4 point 25, the model owner's decision of
    2026-09-18): a thing born at the Node by an emission, a mark's return or a
    table's output while another passes joins it. The amounts add (whole
    quanta of the family), the phase is the coherent sum's (rule 3.20, the
    amount never cancels), the momentum they carry adds exactly (the charge,
    per quantum, adds with the amount), and the owners are kept as a set so
    that a returning shadow of either is home at the merged ray; every other
    property is that of the ray that took the lane first, the one already on
    the heading. A content above the family's bound is the decay table's
    business (point 20). Rays of one merge key merged already."""
    reals = [ray for ray in rays if _on_lane(ray, definition)]
    if len(reals) <= 1:
        return rays
    held = claims.taken[port]
    # The ray already on its way on the heading keeps its record: the thing that
    # passes (outbound) before one born here or turned back, the first to take
    # the lane before the rest.
    base = next(
        (ray for ray in reals if held is not None and (definition.field, ray_merge_key(ray)) == held),
        reals[0],
    )
    if not base.outbound:
        base = next((ray for ray in reals if ray.outbound), base)
    amount = 0
    total = [0, 0, 0]
    owners: set[int] = set()
    for ray in reals:
        amount = checked_work(amount + ray.amount)
        owners.add(ray.owner)
        owners.update(ray.owners)
        for axis, value in enumerate(ledger_momentum(ray, definition)):
            total[axis] = checked_work(total[axis] + value)
    # The momentum adds exactly as the ledger reads it: the merged thing's own
    # motion is its amount on the lane, and what the sum holds beyond that is
    # the momentum it carries (a returned ray reads its event's momentum).
    heading = definition.headings[base.heading]
    momentum = tuple(
        bounded(checked_work(total[axis] - checked_work(amount * heading[axis]))) for axis in range(3)
    )
    phase = base.phase
    if definition.coherent and definition.cosine_table:
        phase = phase_of_sum(tuple((ray.amount, ray.phase) for ray in reals), definition)
    owners.discard(base.owner)
    merged = replace(
        base,
        amount=bounded(amount),
        phase=phase,
        momentum=(momentum[0], momentum[1], momentum[2]) if any(momentum) else None,
        outbound=1,
        owners=tuple(sorted(owners)),
    )
    return merge_rays(tuple(ray for ray in rays if ray not in reals) + (merged,))


def forward_rays(
    rays: Rays,
    definition: SpatialFieldDefinition,
    meter: CostMeter,
    lanes: LaneClaims | None = None,
) -> tuple[tuple[Rays, ...], Rays, Departures]:
    """Move every ray that is due one link along its own line; return the ports, the
    kept, and the departures' account: the phase steps the things made and the
    momentum they spent on their steps.

    A Port is two lanes (lanes-v1, Highlights 5.4 point 25): an out-lane carries
    at most one real ray per interval, `lanes` holding the claims of every family
    of the Node's cycle (a fresh set when none is given). The lane is a condition
    on the step: every ray that leaves on its own heading takes its lane first,
    a thing that would step to a new heading holds its own lane until it is
    resolved, in the Node's ray order, and steps only if the new lane is free;
    otherwise it keeps its heading, its momentum stays accumulated, and it steps
    at the next Node. Two reals of different keys on one lane are refused.

    On the links metric every ray is due every tick and the Node keeps none. On
    the Euclidean metric a ray hops when its wait passes its heading's pace; a
    ray that waits stays resident, and its clock still runs with the tick,
    forward while outbound and backward on the walk back. A returning thing with
    no steps left is at its event Node and stays resident, inert, with its phase
    unchanged, until the inverse split (detector-return-v1). A shadow, outgoing
    or returning, walks one Link like any share (return-field-v1). A thing steps
    before it leaves (clock-readings-v1, `step_thing`): the first axis on which
    the momentum it carries has reached its content turns it to that axis and
    drops by the content, which is spent; every ray then walks one Link on its
    heading. The clock (point 19): a thing of a clock family advances its phase
    by content / K steps per interval with the remainder kept on it, and the
    steps are counted, the world's computation (point 11). A thing that owes an
    interval for a whole quantum it read (point 23) stays this interval, its
    clock still.
    """
    outgoing: list[list[Ray]] = [[] for _ in range(6)]
    kept: list[Ray] = []
    steps = 0
    spent = [0, 0, 0]
    modulus, clock = definition.phase_modulus, definition.clock
    claims = LaneClaims() if lanes is None else lanes
    family = definition.field
    # The things that would step to a new heading this interval, resolved after
    # every other departure has taken its lane (lanes-v1): the departure on the
    # thing's own heading and the departure on the new one.
    deferred: list[tuple[tuple[int, Ray], tuple[int, Ray], tuple[int, int, int]]] = []
    for ray in rays:
        meter.charge("read")
        meter.charge("route")
        if not ray.outbound and ray.steps == 0 and ray.detector == BIT_THING:
            # At its event Node (a thing).
            kept.append(ray)
            continue
        if ray.detector == BIT_SHADOW and ray.owed:
            # The shadow's wait, a declared option (shadow-wait-v1): a share that
            # owes stays this interval, d spent; it leaves owing nothing, a debt
            # below one interval paid by the interval (a share keeps no remainder
            # past its next mixing, unlike a thing).
            kept.append(replace(ray, owed=max(ray.owed - definition.shadow_wait_denominator, 0)))
            meter.charge("update")
            continue
        if ray.detector == BIT_THING and ray.owed >= definition.wait_denominator:
            # A thing pays a tick for every whole quantum it read (Highlights 5.4
            # point 23): this interval it neither moves, nor steps, nor advances
            # its phase; one interval of its debt is spent.
            kept.append(replace(ray, owed=ray.owed - definition.wait_denominator))
            meter.charge("update")
            continue
        if ray.interaction_delay:
            if bounded(ray.interaction_delay) < 0:
                raise ValueError("ray interaction delay must be nonnegative")
            steps += abs(clock_step(ray, clock)[0])
            kept.append(
                tick_clock(replace(ray, interaction_delay=ray.interaction_delay - 1), modulus, clock)
            )
            meter.charge("update", 2)
            continue
        numerator, denominator = heading_pace(definition, ray.heading)
        wait = checked_work(ray.wait + numerator)
        if wait < denominator:
            steps += abs(clock_step(ray, clock)[0])
            kept.append(tick_clock(replace(ray, wait=bounded(wait)), modulus, clock))
            continue
        stepped, dropped = step_thing(ray, definition)
        # Every ray walks one Link on its heading (clock-readings-v1, point 21).
        steps += abs(clock_step(stepped, clock)[0])
        own = advance_ray(
            replace(ray, wait=wait - denominator), ray_vector(ray, definition), modulus, clock
        )
        if stepped.heading != ray.heading:
            # The lane is a condition on the step (lanes-v1, point 25): the thing
            # holds its own heading's lane until it is resolved below.
            turned = advance_ray(
                replace(stepped, wait=wait - denominator),
                ray_vector(stepped, definition),
                modulus,
                clock,
            )
            if _on_lane(own[1], definition):
                claims.claim(own[0], family, own[1])
            deferred.append((own, turned, dropped))
            continue
        port, moved = own
        if _on_lane(moved, definition):
            claims.claim(port, family, moved)
        outgoing[port].append(moved)
    for own, turned, dropped in deferred:
        if claims.free(turned[0]):
            # The step: the lane is free, the thing turns and its momentum drops.
            claims.release(own[0], family, own[1])
            claims.claim(turned[0], family, turned[1])
            meter.charge("update", 2)
            for axis in range(3):
                spent[axis] = checked_work(spent[axis] + dropped[axis])
            outgoing[turned[0]].append(turned[1])
        else:
            # The lane is taken: the thing keeps its heading, its momentum stays
            # accumulated, and it steps at the next Node (Highlights 5.4, point 25).
            outgoing[own[0]].append(own[1])
    result = tuple(
        merge_lane(merge_rays(tuple(port_rays)), port, claims, definition)
        for port, port_rays in enumerate(outgoing)
    )
    meter.charge("send", sum(1 for port_rays in result if port_rays))
    return result, merge_rays(tuple(kept)), Departures(steps, (spent[0], spent[1], spent[2]))
