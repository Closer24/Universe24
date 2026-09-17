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

# Ray-event state (Highlights 3.3, 3.19, 3.20 and 5.1): every ray carries the
# number of Links it has walked since its event and the information of that
# event. The fields are hidden variables in this slice: no rule reads them.
RAY_EVENT_STATE = "ray-event-state-v1"
EventShares = tuple[int, int, int, int, int, int]
NO_EVENT_SHARES: EventShares = (0, 0, 0, 0, 0, 0)
# The Detector bit carried by a ray: no Detector event, or a Detector event
# that drew 0 or 1. No Detector exists yet, so every ray carries 0.
DETECTOR_NONE, DETECTOR_BIT_0, DETECTOR_BIT_1 = 0, 1, 2
# Every ray is a wave ray (Highlights 3.3 and 5.1, wave-ray-family-v1): the phase
# every ray carries has the width its family declares, `phase_bits`, and every
# phase advance or difference is a mask over 2^phase_bits, never a division. A
# plain family is the special case with rest rate 0. The width has no bound in
# the model; two host limits follow from what else stores a phase: the coherence
# table of a Kerengonen field has one entry per phase step (at most 4096, twelve
# bits), and a ray interaction view or a self-exclusion row stores the phase as
# a bounded value (MAX_VALUE = 2^30 - 1, thirty bits).
WAVE_RAY_FAMILY = "wave-ray-family-v1"
MAX_TABLE_BITS = 12
MAX_STORED_PHASE_BITS = 30


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
    # Ray-event state, carried and never read by a rule (ray-event-state-v1):
    # Links walked since the ray's event, counted up while outbound and down on
    # the walk back; 1 while the ray travels on its event's heading, 0 once it
    # is reversed on its line; the six-bit mask of the Ports the event sent to
    # and the amount it sent through each (six fixed entries, port order, zero
    # where the mask bit is zero); the Detector bit of the event, 0 for none.
    steps: int = 0
    outbound: int = 1
    event_ports: int = 0
    event_shares: EventShares = NO_EVENT_SHARES
    detector: int = DETECTOR_NONE


Rays = tuple[Ray, ...]

# Structural non-owning projections used by the ordinary indexed evaluator.
RAY_PROPERTIES = (
    FieldDefinition("amount", 1, "ray amount", False, True),
    FieldDefinition("heading", 3, "integer direction", True, False),
    FieldDefinition("phase", 1, "phase step", False, False),
    FieldDefinition("advance", 1, "phase step per interval", True, False),
    FieldDefinition("delay", 1, "local interval", False, False),
    # wave-ray-family-v1: the ray's family (the index of its spatial field) and
    # that family's charge per quantum, read-only views for a coupling at a meeting.
    FieldDefinition("family", 1, "spatial field index", False, False),
    FieldDefinition("charge", 1, "charge per quantum", True, False),
)
RAY_AMOUNT, RAY_HEADING, RAY_PHASE, RAY_ADVANCE, RAY_DELAY, RAY_FAMILY, RAY_CHARGE = range(7)
# A ray interaction may assign heading, phase and delay; the rest is read-only.
RAY_WRITABLE = frozenset((RAY_HEADING, RAY_PHASE, RAY_DELAY))
RAY_VIEW_COMPONENTS = sum(field.components for field in RAY_PROPERTIES)
CHARGE_INVARIANT = "charge"


def charge_invariant(participants: int) -> Invariant:
    """The charge readout, charge x amount summed over the participants, declared as an
    invariant of a ray interaction: exact before and after, checked like every
    declared invariant (wave-ray-family-v1)."""
    if type(participants) is not int or not 1 <= participants <= 6:
        raise ValueError("the charge invariant covers one to six participants")
    total: Expression | None = None
    for side in range(participants):
        term = Expression(
            "mul",
            (
                Expression("field", field=RAY_CHARGE, side=side),
                Expression("field", field=RAY_AMOUNT, side=side),
            ),
        )
        total = term if total is None else Expression("add", (total, term))
    assert total is not None
    return Invariant(CHARGE_INVARIANT, total)


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
        if any(assignment.field not in RAY_WRITABLE for assignment in rule.assignments):
            raise ValueError("ray interaction amount, advance, family and charge are read-only")
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
        if definition.phase_bits > MAX_STORED_PHASE_BITS:
            raise ValueError(
                "ray interactions view the phase as a stored value: they require phase_bits at most 30"
            )
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
    # Kerengonen (phased rays): the coherence table, one entry per phase step of
    # one turn (2^phase_bits entries, a power of two up to 4096; 0 is no table),
    # and the family's rest rate, the steps its phase advances every interval
    # (0 for light and for the plain field). A ray's own advance overrides the
    # rest rate (kerengonen_advance); every advance is a mask over the width.
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
    # Every ray is a wave ray (wave-ray-family-v1): the width of the phase every
    # ray of this family carries, the modulus being 2^phase_bits; 0 (one phase
    # value, the plain field of existing worlds) unless declared, and log2 of
    # phase_steps when a coherence table is declared without a width.
    phase_bits: int = 0
    # The family's charge per quantum, a bounded signed integer read by couplings
    # at a meeting and summed as charge x amount by the charge readout.
    charge: int = 0
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
        if type(self.phase_bits) is not int or self.phase_bits < 0:
            raise ValueError("phase_bits must be a nonnegative integer")
        if self.phase_steps:
            if (
                type(self.phase_steps) is not int
                or not 2 <= self.phase_steps <= MAX_PHASE_STEPS
                or self.phase_steps & (self.phase_steps - 1)
            ):
                raise ValueError("kerengonen phase_steps must be a power of two between 2 and 4096")
            bits = self.phase_steps.bit_length() - 1
            if self.phase_bits == 0:
                object.__setattr__(self, "phase_bits", bits)
            elif self.phase_bits != bits:
                raise ValueError("kerengonen phase_steps must equal 2 to the power phase_bits")
            # Immutable law preparation precedes every physical event.
            object.__setattr__(self, "cosine_table", phase_cosines(self.phase_steps))
            object.__setattr__(self, "sine_table", phase_sines(self.phase_steps))
        bounded(self.charge)

    @property
    def rays(self) -> bool:
        return self.transport == "ray"

    @property
    def coherent(self) -> bool:
        """The family declares the Kerengonen coherence table."""
        return self.phase_steps > 0

    @property
    def phase_modulus(self) -> int:
        """The phase turns over at 2^phase_bits; 1 for a family without a declared width."""
        return 1 << self.phase_bits

    @property
    def phase_mask(self) -> int:
        return (1 << self.phase_bits) - 1

    @property
    def euclidean(self) -> bool:
        return self.metric == "euclidean"

    @property
    def kerengonen(self) -> bool:
        """The family declares a phase rule: a coherence table or a nonzero rest rate."""
        return self.phase_steps > 0 or self.phase_advance > 0


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
        if type(ray.phase) is not int or not 0 <= ray.phase < definition.phase_modulus:
            raise ValueError("ray phase must be below the field's phase width")
        if type(ray.advance) is not int or not -1 <= ray.advance < definition.phase_modulus:
            raise ValueError("ray advance must be -1 or below the field's phase width")
        pace = heading_pace(definition, ray.heading)
        if type(ray.wait) is not int or not 0 <= bounded(ray.wait) < pace[1]:
            raise ValueError("ray wait must stay below its heading's pace denominator")
        if bounded(ray.interaction_delay) < 0:
            raise ValueError("ray interaction delay must be nonnegative")
        validate_ray_event_state(ray)


def validate_ray_event_state(ray: Ray) -> None:
    """The carried event state is bounded: a count, a bit, a Port mask, six shares, a bit pair."""
    if bounded(ray.steps) < 0:
        raise ValueError("ray steps since its event must be nonnegative")
    if type(ray.outbound) is not int or ray.outbound not in (0, 1):
        raise ValueError("ray outbound must be 1 on the event's heading or 0 reversed")
    if type(ray.event_ports) is not int or not 0 <= ray.event_ports < 64:
        raise ValueError("ray event ports must be a six-bit port mask")
    if type(ray.event_shares) is not tuple or len(ray.event_shares) != 6:
        raise ValueError("ray event shares require one bounded entry per port")
    for port, share in enumerate(ray.event_shares):
        if bounded(share) and not ray.event_ports >> port & 1:
            raise ValueError("ray event shares must be zero where the event sent nothing")
    if ray.detector not in (DETECTOR_NONE, DETECTOR_BIT_0, DETECTOR_BIT_1):
        raise ValueError("ray detector must be 0 (none), 1 (bit 0) or 2 (bit 1)")


def dda_step(accumulators: tuple[int, int, int], heading: Heading) -> tuple[int, tuple[int, int, int]]:
    """One Link along the axis furthest behind the heading; ties take the lowest axis."""
    length = validate_heading(heading)
    advanced = [a + abs(h) for a, h in zip(accumulators, heading, strict=True)]
    axis = max(range(3), key=lambda i: (advanced[i], -i))
    advanced[axis] -= length
    port = 2 * axis + (0 if heading[axis] > 0 else 1)
    return port, (advanced[0], advanced[1], advanced[2])


def ray_phase_step(ray: Ray, phase_advance: int) -> int:
    """The signed phase step of one Link: the ray's own advance or the field's, forward
    while outbound and backward on the walk back, so a returned ray reaches its event
    Node with the phase it left with."""
    step = ray.advance if ray.advance >= 0 else phase_advance
    return step if ray.outbound else -step


def phase_mask(phase_modulus: int) -> int:
    """The mask of a phase modulus: 2^phase_bits - 1. The modulus is a power of two, so
    every phase advance and difference is a mask, never a division; 0 means that no
    width was given and the phase is left as it is."""
    if type(phase_modulus) is not int or phase_modulus < 0 or phase_modulus & (phase_modulus - 1):
        raise ValueError("the phase modulus must be a power of two")
    return phase_modulus - 1 if phase_modulus else 0


def advance_ray(
    ray: Ray, heading: Heading, phase_modulus: int = 0, phase_advance: int = 0
) -> tuple[int, Ray]:
    """Walk one Link: the DDA port, the step count and the phase.

    An outbound ray counts its steps up and its phase forward by its rate; a
    returning ray counts both down. The phase is masked by the modulus, a power of
    two (2^phase_bits); a plain family has rate 0 and its phase stays. A returning
    ray with no steps left is at its event Node, and what it does there is not
    defined in this slice, so walking it further is refused.
    """
    port, accumulators = dda_step(ray.accumulators, heading)
    if ray.outbound:
        steps = bounded(checked_work(ray.steps + 1))
    elif ray.steps > 0:
        steps = ray.steps - 1
    else:
        raise ValueError("a returning ray with no steps left is at its event Node")
    phase = ray.phase
    if phase_modulus:
        phase = (ray.phase + ray_phase_step(ray, phase_advance)) & phase_mask(phase_modulus)
    return port, replace(ray, accumulators=accumulators, phase=phase, steps=steps)


def event_stamp(rays: Rays, headings: tuple[Heading, ...]) -> tuple[int, EventShares]:
    """The mask of Ports one event sends to and the amount per Port, read from its rays.

    Each ray leaves through the Port of its first DDA step. Rays on different
    headings that share a first Port are one event on that Port, so their amounts
    add; a share is bounded like any stored value.
    """
    mask, shares = 0, [0] * 6
    for ray, heading in zip(rays, headings, strict=True):
        port, _ = dda_step(ray.accumulators, heading)
        mask |= 1 << port
        shares[port] = checked_work(shares[port] + ray.amount)
    return mask, (
        bounded(shares[0]),
        bounded(shares[1]),
        bounded(shares[2]),
        bounded(shares[3]),
        bounded(shares[4]),
        bounded(shares[5]),
    )


def stamp_event(rays: Rays, headings: tuple[Heading, ...]) -> Rays:
    """Make the given rays the events of one interaction: fresh outbound trajectories
    with no steps walked, each carrying the mask and shares of that interaction. No
    Detector exists in this slice, so the Detector bit is none."""
    mask, shares = event_stamp(rays, headings)
    return tuple(
        replace(
            ray,
            steps=0,
            outbound=1,
            event_ports=mask,
            event_shares=shares,
            detector=DETECTOR_NONE,
        )
        for ray in rays
    )


def merge_rays(rays: Rays) -> Rays:
    """Combine rays that share heading, lattice phase, wave phase and event: one line, so exact.

    Rays of different events never merge, whatever their heading and phase: the
    event state is part of the identity, so each ray keeps the information of
    its own event.
    """
    combined: dict[
        tuple[int, tuple[int, int, int], int, int, int, int, int, int, int, EventShares, int], int
    ] = {}
    for ray in rays:
        key = (
            ray.heading,
            ray.accumulators,
            ray.phase,
            ray.advance,
            ray.wait,
            ray.interaction_delay,
            ray.steps,
            ray.outbound,
            ray.event_ports,
            ray.event_shares,
            ray.detector,
        )
        combined[key] = checked_work(combined.get(key, 0) + ray.amount)
    return tuple(
        Ray(
            heading,
            accumulators,
            bounded(amount),
            phase,
            advance,
            wait,
            delay,
            steps=steps,
            outbound=outbound,
            event_ports=ports,
            event_shares=shares,
            detector=detector,
        )
        for (
            heading,
            accumulators,
            phase,
            advance,
            wait,
            delay,
            steps,
            outbound,
            ports,
            shares,
            detector,
        ), amount in sorted(combined.items())
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


def ray_charge(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The charge readout of one bundle: the family's charge per quantum times the amount,
    summed over its rays as a 64-bit intermediate (wave-ray-family-v1)."""
    total = 0
    for ray in rays:
        total = checked_work(total + checked_work(ray.amount * definition.charge))
    return total


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
    phase_steps, mask = definition.phase_steps, definition.phase_mask
    cosines, sines = definition.cosine_table, definition.sine_table
    x = y = 0
    for amount, phase in terms:
        x = checked_work(x + amount * cosines[phase & mask])
        y = checked_work(y + amount * sines[phase & mask])
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
    if not definition.coherent or not rays:
        return (1, 1)
    mask = definition.phase_mask
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
                numerator + checked_work(amount * other_amount) * cosines[(phase - other) & mask]
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
