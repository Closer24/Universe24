"""Fixed local records for optional initialization-defined spatial fields."""

from dataclasses import dataclass, replace
from dataclasses import field as dataclass_field
from functools import lru_cache

from .disturbance_state import (
    MAX_COMPONENTS,
    MAX_RULES,
    MAX_SLOTS,
    Address3,
    Assignment,
    CostMeter,
    DisturbanceDefinition,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    InitialState,
    InteractionDefinition,
    Invariant,
    Payload,
    TransportDefinition,
    Values,
    any_negative,
    bounded,
    pack,
    unpack,
    validate_codes,
)
from .integer import checked_work, reduced_ratio

SpatialPopulations = tuple[Payload, ...]
SpatialOutgoing = tuple[SpatialPopulations, ...]
SpatialBundle = tuple[SpatialPopulations, ...]


DECAY_RESIDUES = ("localize", "dissipate")


@dataclass(frozen=True, slots=True)
class DecayDefinition:
    """Completed-link attenuation ratio and the fate of the removed fraction.

    ``localize`` (default) keeps the removed quantity as stationary stock owned
    by the receiving Node, so total signed inventory is preserved. ``dissipate`` is the
    explicit historical option that records it as loss instead.
    """

    retain_numerator: int
    retain_denominator: int
    residue: str = "localize"

    def __post_init__(self) -> None:
        if self.residue not in DECAY_RESIDUES:
            raise ValueError("decay residue must be dissipate or localize")

    @property
    def localizes(self) -> bool:
        return self.residue == "localize"


Heading = tuple[int, int, int]
MAX_HEADINGS = 65536
MAX_HEADING_COMPONENT = 4096
MAX_RAY_SLOTS = 4096


@dataclass(frozen=True, slots=True)
class Ray:
    """One straight-moving share of a ray field: heading index, DDA state and amount.

    The three accumulators travel with the ray, so every unit of one ray follows the
    same lattice line. They are bounded by the heading's Manhattan length.
    """

    heading: int
    accumulators: tuple[int, int, int]
    amount: int
    # Kerengonen fields only: the ray's phase step, advanced on every link, and
    # the ray's own advance per link when nonnegative (-1 uses the field's).
    phase: int = 0
    advance: int = -1
    # Euclidean pace only: how far the ray is toward its next link, below its
    # heading's pace denominator.
    wait: int = 0
    # Generic local coupling residence; independent of the pacing remainder.
    interaction_delay: int = 0


Rays = tuple[Ray, ...]

# Structural non-owning projections used by the ordinary indexed evaluator.
RAY_PROPERTIES = (
    FieldDefinition("amount", 1, "ray amount", False, True),
    FieldDefinition("heading", 3, "integer direction", True, False),
    FieldDefinition("phase", 1, "phase step", False, False),
    FieldDefinition("advance", 1, "phase step per interval", True, False),
    FieldDefinition("delay", 1, "local interval", False, False),
)


def ray_participant_definitions(
    fields: tuple[FieldDefinition, ...], definitions: tuple[SpatialFieldDefinition, ...]
) -> tuple[DisturbanceDefinition, ...]:
    """Describe non-owning ray views; no additional physical records are created."""
    defaults = tuple(pack((0,) * field.components) for field in RAY_PROPERTIES)
    return tuple(
        DisturbanceDefinition(
            fields[definition.field].name,
            tuple(range(len(RAY_PROPERTIES))) if definition.rays else (),
            defaults,
            TransportDefinition("hold"),
        )
        for definition in definitions
    )


def validate_ray_participants(
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
) -> frozenset[int]:
    """Enforce the same native participant limits for parsed and direct callers."""
    if type(rules) is not tuple or len(rules) > MAX_RULES:
        raise ValueError("ray interaction rules exceed their fixed capacity")
    selected: set[int] = set()
    for rule in rules:
        if (
            not 2 <= len(rule.participants) <= 6
            or rule.k
            or rule.output_types is not None
            or rule.outputs
        ):
            raise ValueError("ray interactions require two to six indexed roles without k or conversion")
        for role in rule.participants:
            if not role or any(
                type(index) is not int or not 0 <= index < len(definitions) for index in role
            ):
                raise ValueError("ray participant role refers to an unavailable spatial field")
            selected.update(role)
        if any(assignment.field not in (1, 2, 4) for assignment in rule.assignments):
            raise ValueError("ray interaction amount and advance are read-only")
    if sum(definitions[index].ray_slots for index in selected) > MAX_SLOTS:
        raise ValueError("ray interactions require at most 32 selected ray slots")
    for index in selected:
        definition = definitions[index]
        field = fields[definition.field]
        if (
            not definition.rays
            or field.signed
            or not field.conserved
            or any(unpack(definition.baseline))
            or definition.euclidean
            or definition.pace_numerator != definition.pace_denominator
            or definition.self_exclusion
            or definition.decay is not None
            or any(sum(abs(component) for component in heading) != 1 for heading in definition.headings)
        ):
            raise ValueError("ray coupling requires positive unit-axial unpaced ray fields")
    return frozenset(selected)


def validate_ray_coupling(initial: InitialState) -> None:
    if not initial.ray_interactions:
        return
    if (
        initial.schema_version != 1
        or initial.link_ticks != 1
        or initial.node_execution
        or initial.spatial_computation_delay
        or initial.field_phase_first
        or initial.arrival_port_blind
        or initial.ray_delay
        or initial.ray_phase_per_tick
        or initial.delay_direction is not None
        or initial.field_rules
        or initial.spatial_interactions
    ):
        raise ValueError("ray interactions require the default fixed H=1 spatial clock")
    selected = validate_ray_participants(
        initial.spatial_fields, initial.fields, initial.ray_interactions
    )
    if any(
        rule.field == initial.spatial_fields[index].field
        for index in selected
        for rule in initial.spatial_couplings
    ):
        raise ValueError("ray interactions do not support coupled responses or absorption")


@dataclass(frozen=True, slots=True)
class SpatialFieldDefinition:
    field: int
    baseline: Payload
    axis_weights: tuple[int, int, int] = (1, 1, 1)
    octant_weights: tuple[int, ...] = (1, 1, 1, 1, 1, 1, 1, 1)
    decay: DecayDefinition | None = None
    transport: str = "outward"
    # Ray transport only: the fixed heading sequence, rays emitted per source per
    # tick, and the resident ray capacity of one Node.
    headings: tuple[Heading, ...] = ()
    rays_per_tick: int = 0
    ray_slots: int = 0
    # Ray transport only: an emitting record that departs subtracts its own rays
    # from the flux it samples at the next Node, using only its own bookkeeping.
    self_exclusion: bool = False
    # Kerengonen (phased rays) only: the number of phase steps in one cycle and
    # the steps a ray advances on every link. Zero steps is the plain ray field.
    phase_steps: int = 0
    phase_advance: int = 0
    # Kerengonen only: how an absorber takes a ray. "share" takes the coherent
    # share of its amount; "threshold" takes the whole ray when that share reaches
    # one half and leaves it otherwise. Neither draws: the only draw in the model
    # is at a Node whose Detector bit is set.
    capture: str = "share"
    # Declared carrier-vector association for read-only ray inventory accounting.
    momentum_field: int | None = None
    # Ray transport only: "links" moves every ray one link per tick; "euclidean"
    # paces each heading so that every ray covers the same Euclidean distance
    # per tick, the slowest lattice direction setting the speed.
    metric: str = "links"
    # Ray transport only: the fastest heading hops pace_numerator links every
    # pace_denominator ticks (1 / 1 is link speed); a slower matter wave is
    # never faster than the signals that chase it.
    pace_numerator: int = 1
    pace_denominator: int = 1
    # Scalar response readout: last-hop Port channels or complete resident ray headings.
    flux_projection: str = "ports"
    cosine_table: tuple[int, ...] = dataclass_field(default=(), init=False, repr=False)
    sine_table: tuple[int, ...] = dataclass_field(default=(), init=False, repr=False)
    pace_table: tuple[tuple[int, int], ...] = dataclass_field(default=(), init=False, repr=False)

    def __post_init__(self) -> None:
        if self.flux_projection not in ("ports", "carried_heading"):
            raise ValueError("flux_projection must be ports or carried_heading")
        if self.flux_projection == "carried_heading" and not self.rays:
            raise ValueError("carried_heading flux_projection requires ray transport")
        if self.rays:
            object.__setattr__(self, "pace_table", prepare_heading_paces(self))
        if self.phase_steps:
            # Immutable law preparation precedes every physical event.
            object.__setattr__(self, "cosine_table", phase_cosines(self.phase_steps))
            object.__setattr__(self, "sine_table", phase_sines(self.phase_steps))

    @property
    def rays(self) -> bool:
        return self.transport == "ray"

    @property
    def euclidean(self) -> bool:
        return self.metric == "euclidean"

    @property
    def kerengonen(self) -> bool:
        return self.phase_steps > 0


@dataclass(frozen=True, slots=True)
class FieldGroupDefinition:
    name: str
    fields: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class FieldAssignment:
    field: int
    expression: Expression
    port: int = -1


@dataclass(frozen=True, slots=True)
class NodeFieldRuleDefinition:
    name: str
    assignments: tuple[FieldAssignment, ...]
    invariants: tuple[Invariant, ...]
    when: Expression | None = None
    k: int = 0
    commit_when: Expression | None = None


@dataclass(frozen=True, slots=True)
class FieldRuleGuard:
    rule_index: int
    delta: Values
    outgoing: tuple[Values, ...]


@dataclass(frozen=True, slots=True)
class SpatialInteractionDefinition:
    name: str
    type_index: int
    assignments: tuple[Assignment, ...]
    invariants: tuple[Invariant, ...]
    when: Expression | None = None
    types: tuple[int, ...] = ()
    k: int = 0
    participants: tuple[tuple[int, ...], ...] = ()
    commit_when: Expression | None = None


@dataclass(frozen=True, slots=True)
class FieldInteractionGuard:
    rule_index: int
    slot: int
    before: Values
    after: Values
    delta: Values
    slots: tuple[int, ...] = ()
    participant_before: tuple[Values, ...] = ()
    participant_after: tuple[Values, ...] = ()


@dataclass(frozen=True, slots=True)
class EmissionDefinition:
    type_index: int
    spatial_field: int
    amount: Expression
    denominator: int = 1
    budget: Payload | None = None
    types: tuple[int, ...] = ()
    # Ray fields only: pay the emitted amount from the record's own field of the
    # same name (clipped to its stock) instead of declaring an external source,
    # and subtract the emitted rays' amount x heading from an owned vector field.
    funded: bool = False
    recoil_field: int | None = None
    # Kerengonen fields only: the phase step every emitted ray starts with, or,
    # when carried, the phase of what the record last absorbed plus one advance.
    phase: int = 0
    phase_carried: bool = False
    # Kerengonen fields only: the emitted rays' own advance per link, an owned-field
    # expression over advance_denominator, taken modulo the phase steps.
    advance: Expression | None = None
    advance_denominator: int = 1
    # Kerengonen fields only: re-emit the whole amount along the mirror image of the
    # heading last absorbed: for each output component, the source component and
    # its sign (a mirror across an axis plane or a diagonal plane).
    mirror: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] | None = None
    # Dissolution (funded ray fields only): emit nothing for dissolve_after cycles,
    # then the record's initial stock over dissolve_over cycles, never more than
    # is left. Zero dissolve_over means no dissolution.
    dissolve_after: int = 0
    dissolve_over: int = 0
    # Ray fields only: emit every ray on this one heading of the sequence instead
    # of sweeping the sequence (a directed emitter). None sweeps.
    heading: int | None = None


@dataclass(frozen=True, slots=True)
class SpatialCouplingDefinition:
    name: str
    type_index: int
    field: int
    mode: str
    expression: Expression
    denominator: int = 1
    axis_order: tuple[int, int, int] = (0, 1, 2)
    budget: Payload | None = None
    types: tuple[int, ...] = ()
    # Absorb mode only: the owned vector field that receives amount x heading.
    momentum_field: int | None = None
    # Absorb mode only: the share of each arriving ray that is absorbed, as a
    # nonnegative owned-field expression over fraction_denominator; the rest of
    # the ray is forwarded. None absorbs whole rays.
    fraction: Expression | None = None
    fraction_denominator: int = 1


@dataclass(frozen=True, slots=True)
class SpatialCouplingResult:
    records: tuple[DisturbanceRecord | None, ...]
    reaction: Values
    cost: int
    guards: tuple[FieldInteractionGuard, ...] = ()
    interaction_ticks: int = 0


@dataclass(frozen=True, slots=True)
class SpatialSeed:
    position: Address3
    spatial_field: int
    populations: SpatialPopulations


@dataclass(frozen=True, slots=True)
class SpatialState:
    """Eight owned populations, eight allocation phases, and six delivered samples.

    All entries use the ordinary positive payload coding, including phases.
    Delivered samples project already owned inventory and are never extra stock.
    """

    populations: SpatialPopulations
    allocation_phases: SpatialPopulations
    delivered: tuple[Payload, ...]
    received_mask: int = 0

    def validate(self, components: int) -> None:
        if type(components) is not int or not 1 <= components <= MAX_COMPONENTS:
            raise ValueError("spatial fields require one to thirty-two components")
        if type(self.received_mask) is not int or not 0 <= self.received_mask < 64:
            raise ValueError("received mask requires six bounded port bits")
        for values, size in (
            (self.populations, 8),
            (self.allocation_phases, 8),
            (self.delivered, 6),
        ):
            if len(values) != size:
                raise ValueError("spatial state requires eight octants and six delivered channels")
            for value in values:
                if len(value) != components:
                    raise ValueError("spatial state component count differs from the field")
                validate_codes(value)
        if any(any_negative(payload) for payload in self.allocation_phases):
            raise ValueError("spatial allocation phases must be nonnegative")


@dataclass(slots=True)
class SpatialNodeState:
    """Mutable spatial-field state owned by one Node."""

    states: tuple[SpatialState, ...]
    last_cost: int = 0
    received_count: int = 0
    reaction_phases: Values = ()
    sample_values: Values = ()
    sample_fluxes: Values = ()
    last_begin_tick: int = -1
    received_decay_cost: int = 0
    sample_ports: tuple[Values, ...] = ()
    sample_received_masks: tuple[int, ...] = ()
    # Frozen six delivered channels per spatial field, for arrival-port-blind samples.
    sample_delivered: tuple[tuple[Payload, ...], ...] = ()
    # Computation-field stock present at this node before its last forwarding.
    load: int = 0
    # The same stock split by the six travel channels it was delivered through.
    load_channels: tuple[int, ...] = (0, 0, 0, 0, 0, 0)
    # Later arrivals have destination ownership but cannot enter a frozen cycle.
    shared_pending: int = 0
    # Stationary stock per spatial field, deposited by localizing decay. It is
    # owned inventory at a known Node: never transported, decayed or sampled.
    localized: tuple[Payload, ...] = ()
    # Resident rays per spatial field (empty for non-ray fields). They arrived on
    # the previous link and leave on the next cycle along their own lines.
    rays: tuple[Rays, ...] = ()
    incoming: tuple[SpatialState, ...] = ()
    incoming_count: int = 0
    incoming_decay_cost: int = 0
    # Intervals the resident rays still wait under ray_delay before forwarding.
    ray_wait: int = 0


@dataclass(frozen=True, slots=True)
class SpatialPlan:
    states: tuple[SpatialState, ...]
    outgoing: tuple[SpatialBundle, ...]
    emission_records: tuple[DisturbanceRecord | None, ...]
    source_delta: Values
    cost: int
    rule_delta: Values = ()
    interaction_ticks: int = 0
    field_guards: tuple[FieldRuleGuard, ...] = ()
    # Outgoing rays per port, each entry holding one tuple per spatial field.
    rays: tuple[tuple[Rays, ...], ...] = ()
    # Per port, per field, eight carried allocation phases; empty under node-owned phases.
    outgoing_phases: tuple[SpatialBundle, ...] = ()
    # Funded emission minus absorption per field: stock that moved between a
    # record and its field, booked as a reaction, never as a source.
    transfer_delta: Values = ()
    # Rays that stay resident this cycle (Euclidean pace), one tuple per field.
    kept_rays: tuple[Rays, ...] = ()


@dataclass(frozen=True, slots=True)
class SpatialPacket:
    arrival_tick: int
    origin: Address3
    port: int
    fields: SpatialBundle
    rays: tuple[Rays, ...] = ()
    phases: SpatialBundle = ()


def zero_spatial_state(components: int) -> SpatialState:
    bounded(components)
    if not 1 <= components <= MAX_COMPONENTS:
        raise ValueError("spatial fields require one to thirty-two components")
    zero = pack((0,) * components)
    return SpatialState((zero,) * 8, (zero,) * 8, (zero,) * 6)


# Ray state rules. A ray carries its heading index and three integer accumulators.
# On every link it steps along the axis that is furthest behind its heading (an
# integer digital differential analyzer), so all rays of one heading and phase
# trace the same lattice line. Nothing here reads another Node or a global value.


def validate_heading(heading: Heading) -> int:
    """Return the Manhattan length of a bounded nonzero integer heading."""
    if type(heading) is not tuple or len(heading) != 3:
        raise ValueError("a ray heading requires three integer components")
    length = 0
    for component in heading:
        if type(component) is not int or abs(component) > MAX_HEADING_COMPONENT:
            raise ValueError("ray heading components must be bounded integers")
        length += abs(component)
    if length == 0:
        raise ValueError("a ray heading must not be the zero vector")
    return length


def validate_rays(rays: Rays, definition: SpatialFieldDefinition, field: FieldDefinition) -> None:
    if type(rays) is not tuple or len(rays) > definition.ray_slots:
        raise ValueError("ray slot budget exceeded")
    for ray in rays:
        if type(ray) is not Ray:
            raise ValueError("ray transport requires immutable Ray entries")
        if type(ray.heading) is not int or not 0 <= ray.heading < len(definition.headings):
            raise ValueError("ray heading index is outside the configured sequence")
        length = validate_heading(definition.headings[ray.heading])
        if type(ray.accumulators) is not tuple or len(ray.accumulators) != 3:
            raise ValueError("a ray requires three integer accumulators")
        if any(type(a) is not int or not -length < a <= length for a in ray.accumulators):
            raise ValueError("ray accumulators must stay within the heading length")
        if bounded(ray.amount) == 0:
            raise ValueError("a resident ray must carry a nonzero amount")
        field.validate(pack((ray.amount,)))
        if type(ray.phase) is not int or not 0 <= ray.phase < max(definition.phase_steps, 1):
            raise ValueError("ray phase must index the field's phase steps")
        if type(ray.advance) is not int or not -1 <= ray.advance < max(definition.phase_steps, 1):
            raise ValueError("ray advance must be -1 or index the field's phase steps")
        pace = heading_pace(definition, ray.heading)
        if type(ray.wait) is not int or not 0 <= bounded(ray.wait) < pace[1]:
            raise ValueError("ray wait must stay below its heading's pace denominator")
        if bounded(ray.interaction_delay) < 0:
            raise ValueError("ray interaction delay must be nonnegative")


def advance_ray(
    ray: Ray, heading: Heading, phase_steps: int = 0, phase_advance: int = 0
) -> tuple[int, Ray]:
    """Choose the port of the axis furthest behind the heading; ties take the lowest axis.

    A Kerengonen ray also advances its phase by the field's steps per link.
    """
    length = validate_heading(heading)
    accumulators = [a + abs(h) for a, h in zip(ray.accumulators, heading, strict=True)]
    axis = max(range(3), key=lambda i: (accumulators[i], -i))
    accumulators[axis] -= length
    port = 2 * axis + (0 if heading[axis] > 0 else 1)
    step = ray.advance if ray.advance >= 0 else phase_advance
    phase = (ray.phase + step) % phase_steps if phase_steps else ray.phase
    return port, replace(
        ray, accumulators=(accumulators[0], accumulators[1], accumulators[2]), phase=phase
    )


def merge_rays(rays: Rays) -> Rays:
    """Combine rays that share heading, lattice phase and wave phase: one line, so exact."""
    combined: dict[tuple[int, tuple[int, int, int], int, int, int, int], int] = {}
    for ray in rays:
        key = (
            ray.heading,
            ray.accumulators,
            ray.phase,
            ray.advance,
            ray.wait,
            ray.interaction_delay,
        )
        combined[key] = checked_work(combined.get(key, 0) + ray.amount)
    return tuple(
        Ray(heading, accumulators, bounded(amount), phase, advance, wait, delay)
        for (heading, accumulators, phase, advance, wait, delay), amount in sorted(combined.items())
        if amount
    )


def ray_stock(rays: Rays) -> int:
    total = 0
    for ray in rays:
        total = checked_work(total + ray.amount)
    return bounded(total)


def ray_momentum(rays: Rays, definition: SpatialFieldDefinition) -> tuple[int, int, int]:
    """Read the candidate's amount-times-heading inventory from actual ray owners."""
    result = [0, 0, 0]
    for ray in rays:
        for axis, component in enumerate(definition.headings[ray.heading]):
            result[axis] = checked_work(result[axis] + checked_work(ray.amount * component))
    return result[0], result[1], result[2]


def attenuate_rays(rays: Rays, decay: DecayDefinition, meter: CostMeter) -> tuple[Rays, int]:
    """Apply the completed-link ratio to each ray; return survivors and the removed total."""
    numerator, denominator = decay.retain_numerator, decay.retain_denominator
    survivors, removed = [], 0
    for ray in rays:
        meter.charge("read")
        magnitude = checked_work(abs(ray.amount) * numerator) // denominator
        kept = -magnitude if ray.amount < 0 else magnitude
        removed = checked_work(removed + ray.amount - kept)
        meter.charge("update", 3)
        if kept:
            survivors.append(replace(ray, amount=kept))
    return tuple(survivors), bounded(removed)


# Kerengonen rules. A ray carries a phase step; rays that meet at a Node combine
# by phase. Coherence is |sum a e^(i phi)|^2 / (sum |a|)^2 in bounded integers:
# a fixed cosine table over phase differences, scaled by PHASE_COSINE_SCALE, so
# equal phases give exactly one and opposite phases of equal amounts exactly zero.

MAX_PHASE_STEPS = 4096
PHASE_COSINE_SCALE = 256
# pi in fixed point: integer arithmetic only, as every physical module requires.
_PI_FIXED = 3141592654
_FIXED = 1000000000


def _fixed_cosine(angle: int) -> int:
    """cos of a fixed-point angle in [0, pi/2], scaled by _FIXED, by its series."""
    if not 0 <= angle <= _PI_FIXED // 2:
        raise ValueError("phase table angle is outside the first quadrant")
    magnitude, total, sign = _FIXED, 0, 1
    for k in range(2, 66, 2):
        total = checked_work(total + sign * magnitude)
        magnitude = checked_work(magnitude * angle) // _FIXED
        magnitude = checked_work(magnitude * angle) // _FIXED // ((k - 1) * k)
        if not magnitude:
            return total
        sign = -sign
    raise OverflowError("phase table cosine did not converge within its fixed bound")


def _fixed_sine(angle: int) -> int:
    """sin of a fixed-point angle in [0, pi/2], scaled by _FIXED, by its series."""
    if not 0 <= angle <= _PI_FIXED // 2:
        raise ValueError("phase table angle is outside the first quadrant")
    magnitude, total, sign = angle, 0, 1
    for k in range(3, 67, 2):
        total = checked_work(total + sign * magnitude)
        magnitude = checked_work(magnitude * angle) // _FIXED
        magnitude = checked_work(magnitude * angle) // _FIXED // ((k - 1) * k)
        if not magnitude:
            return total
        sign = -sign
    raise OverflowError("phase table sine did not converge within its fixed bound")


@lru_cache(maxsize=16)
def phase_sines(phase_steps: int) -> tuple[int, ...]:
    """Scaled sine of every phase step, the companion of phase_cosines."""
    phase_cosines(phase_steps)
    entries = []
    for step in range(phase_steps):
        reduced = step if 2 * step <= phase_steps else phase_steps - step
        angle = checked_work(2 * _PI_FIXED * reduced) // phase_steps
        if 4 * reduced > phase_steps:
            angle = _PI_FIXED - angle
        scaled = checked_work(_fixed_sine(angle) * PHASE_COSINE_SCALE + _FIXED // 2) // _FIXED
        entries.append(scaled if 2 * step <= phase_steps else -scaled)
    return tuple(entries)


def phase_of_sum(terms: tuple[tuple[int, int], ...], definition: SpatialFieldDefinition) -> int:
    """The phase step nearest the direction of sum a e^(i phi): the best projection.

    Ties and an empty or cancelled sum give step zero. Bounded by phase_steps.
    """
    phase_steps = definition.phase_steps
    cosines, sines = definition.cosine_table, definition.sine_table
    x = y = 0
    for amount, phase in terms:
        x = checked_work(x + amount * cosines[phase % phase_steps])
        y = checked_work(y + amount * sines[phase % phase_steps])
    best, best_projection = 0, None
    for step in range(phase_steps):
        projection = checked_work(x * cosines[step] + y * sines[step])
        if best_projection is None or projection > best_projection:
            best, best_projection = step, projection
    return best


@lru_cache(maxsize=16)
def phase_cosines(phase_steps: int) -> tuple[int, ...]:
    """Scaled cosine of every phase difference; immutable law data, computed once.

    cos(2 pi d / P) x 256, rounded to the nearest integer. The only rational
    values on that circle are 0, +-1/2 and +-1, so no entry is a half-integer.
    """
    if type(phase_steps) is not int or not 2 <= phase_steps <= MAX_PHASE_STEPS:
        raise ValueError("kerengonen phase_steps must be between 2 and 4096")
    entries = []
    for difference in range(phase_steps):
        reduced = min(difference, phase_steps - difference)
        angle = checked_work(2 * _PI_FIXED * reduced) // phase_steps
        flip = 4 * reduced > phase_steps
        if flip:
            angle = _PI_FIXED - angle
        cosine = _fixed_cosine(angle)
        scaled = checked_work(cosine * PHASE_COSINE_SCALE + _FIXED // 2) // _FIXED
        entries.append(-scaled if flip else scaled)
    return tuple(entries)


def coherence(rays: Rays, definition: SpatialFieldDefinition) -> tuple[int, int]:
    """Numerator and denominator of the coherent fraction of one Node's rays, in [0, 1]."""
    if not definition.kerengonen or not rays:
        return (1, 1)
    steps = definition.phase_steps
    cosines = definition.cosine_table
    by_phase: dict[int, int] = {}
    magnitude = 0
    for ray in rays:
        by_phase[ray.phase] = checked_work(by_phase.get(ray.phase, 0) + ray.amount)
        magnitude = checked_work(magnitude + abs(ray.amount))
    numerator = 0
    for phase, amount in by_phase.items():
        for other, other_amount in by_phase.items():
            numerator = checked_work(
                numerator + checked_work(amount * other_amount) * cosines[(phase - other) % steps]
            )
    denominator = checked_work(checked_work(magnitude * magnitude) * PHASE_COSINE_SCALE)
    return (min(max(numerator, 0), denominator), denominator)


# The two captures are deterministic. The ordinary lottery capture and the bond
# registry were deleted on 2026-09-17 (Highlights 3.18 deleted, 3.19, 3.20, 5.4):
# an absorber never draws. The ticket sequence below stays as the bounded local
# draw that a Node whose Detector bit is set will own.
CAPTURE_MODES = ("share", "threshold")
TICKET_MODULUS = 1073741789  # the largest prime below the field register bound


def next_ticket(state: int, salt: int) -> int:
    """Advance a local ticket state: a multiplicative congruence salted by the arrival."""
    if not 0 <= state < TICKET_MODULUS:
        raise ValueError("absorb ticket state must stay below the ticket modulus")
    return (state * 48271 + salt + 1) % TICKET_MODULUS


def ticket_draw(state: int) -> int:
    """The number a ticket state draws: its square modulo the ticket modulus.

    The state itself is affine in its salts, so two marks that met the same
    arrivals would draw numbers a fixed distance apart; the square breaks that,
    so two Detectors with their own seeds draw independently for every arrival.
    """
    return checked_work(state * state) % TICKET_MODULUS


def coherent_stock(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The stock a reader sees: the ray total scaled by the Node's coherence, toward zero."""
    total = ray_stock(rays)
    numerator, denominator = coherence(rays, definition)
    if numerator == denominator:
        return total
    magnitude = checked_work(abs(total) * numerator) // denominator
    return bounded(-magnitude if total < 0 else magnitude)


# Euclidean pace. A heading of Manhattan length L and Euclidean length E covers
# E / L of a Euclidean unit per link. Pacing every ray to the slowest direction
# makes the wave front round: a ray hops when its wait passes its denominator.

PACE_SCALE = 4096


def integer_sqrt(value: int) -> int:
    """The floor of the square root, by Newton's method on integers."""
    if checked_work(value) < 0:
        raise ValueError("square root of a negative integer")
    if value < 2:
        return value
    guess = value
    better = (guess + value // guess) // 2
    for _ in range(64):
        if better >= guess:
            return guess
        guess, better = better, (better + value // better) // 2
    raise OverflowError("integer square root exceeded its fixed iteration bound")


def prepare_heading_paces(definition: SpatialFieldDefinition) -> tuple[tuple[int, int], ...]:
    """(numerator, denominator) hops per tick for every heading.

    (1, 1) for every heading on the links metric at link speed; the configured
    pace scales every heading alike, and the Euclidean metric slows each heading
    to the slowest lattice direction on top of it.
    """
    numerator, denominator = bounded(definition.pace_numerator), bounded(definition.pace_denominator)
    if not 1 <= numerator <= denominator:
        raise ValueError("pace must be positive and not exceed one link per tick")
    if not 1 <= len(definition.headings) <= MAX_HEADINGS:
        raise ValueError("ray transport requires one to 65536 headings")
    if not definition.euclidean:
        return tuple((numerator, denominator) for _ in definition.headings)
    ratios = []
    for heading in definition.headings:
        manhattan = validate_heading(heading)
        squared = sum(c * c for c in heading)
        ratios.append(integer_sqrt(checked_work(squared * PACE_SCALE * PACE_SCALE)) // manhattan)
    slowest = min(ratios)
    table = []
    for ratio in ratios:
        terms = reduced_ratio(checked_work(slowest * numerator), checked_work(ratio * denominator))
        table.append((bounded(terms[0]), bounded(terms[1])))
    return tuple(table)


def heading_paces(definition: SpatialFieldDefinition) -> tuple[tuple[int, int], ...]:
    """Read immutable configured pace data; physical stepping never prepares a table."""
    return definition.pace_table


def heading_pace(definition: SpatialFieldDefinition, heading: int) -> tuple[int, int]:
    return heading_paces(definition)[heading]
