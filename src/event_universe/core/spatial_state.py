"""Fixed local records for optional initialization-defined spatial fields."""

from dataclasses import dataclass, replace
from dataclasses import field as dataclass_field
from functools import lru_cache

from .disturbance_state import (
    MAX_COMPONENTS,
    Address3,
    Assignment,
    CostMeter,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    Invariant,
    Payload,
    Values,
    bounded,
    pack,
    unpack,
)
from .integer import checked_work

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
    # Claim and gather only: the train (particle) this ray belongs to, zero for
    # a ray no claim can gather, and whether a claim has turned it homeward.
    train: int = 0
    homing: int = 0
    # Bonded pairs only: the bond this ray shares with the ray emitted with it,
    # zero for an unbonded ray.
    bond: int = 0


Rays = tuple[Ray, ...]


@dataclass(frozen=True, slots=True)
class Claim:
    """One Node's knowledge that a train has been captured: gather it homeward.

    The parent port leads one link toward the capturing Node (-1 at that Node
    itself); since is the tick the claim was opened; sent records that this
    Node has already passed the claim to its neighbors.
    """

    train: int
    parent: int
    since: int
    sent: int = 0
    # The Node that opened the claim, stamped by that Node when it commits; the
    # earlier opening tick wins where two claims for one train meet, then the
    # lower address, so every Node ends up pointing at one root.
    origin: Address3 = (-1, -1, -1)

    @property
    def priority(self) -> tuple[int, Address3]:
        return (self.since, self.origin)


Claims = tuple[Claim, ...]
MAX_CLAIM_SLOTS = 64


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
    # share of its amount; "lottery" takes the whole ray or nothing, decided by a
    # local ticket whose probability is that share.
    capture: str = "share"
    capture_seed: int = 0
    # Declared carrier-vector association for read-only ray inventory accounting.
    momentum_field: int | None = None
    # Ray transport only: "links" moves every ray one link per tick; "euclidean"
    # paces each heading so that every ray covers the same Euclidean distance
    # per tick, the slowest lattice direction setting the speed.
    metric: str = "links"
    # Ray transport only: the fastest heading hops pace_numerator links every
    # pace_denominator ticks (1 / 1 is link speed); a slower matter wave lets a
    # claim, traveling at link speed, overtake it.
    pace_numerator: int = 1
    pace_denominator: int = 1
    # Claim and gather only: a Node keeps a claim for claim_ticks ticks after it
    # was opened, at most claim_slots claims at once. Zero ticks disables claims.
    claim_ticks: int = 0
    claim_slots: int = 0
    # Bonded pairs only: the seed of the world's bond registry, -1 for none.
    bond_seed: int = -1
    cosine_table: tuple[int, ...] = dataclass_field(default=(), init=False, repr=False)
    sine_table: tuple[int, ...] = dataclass_field(default=(), init=False, repr=False)

    def __post_init__(self) -> None:
        if self.phase_steps:
            # Immutable law preparation precedes every physical event.
            object.__setattr__(self, "cosine_table", phase_cosines(self.phase_steps))
            object.__setattr__(self, "sine_table", phase_sines(self.phase_steps))

    @property
    def rays(self) -> bool:
        return self.transport == "ray"

    @property
    def bonded(self) -> bool:
        return self.bond_seed >= 0

    @property
    def euclidean(self) -> bool:
        return self.metric == "euclidean"

    @property
    def claims(self) -> bool:
        return self.claim_ticks > 0

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
    # Claim and gather (ray fields with claims only): the owned scalar field whose
    # value stamps every emitted ray with its train, so a claim can gather it; or,
    # when carried, the train of what the record last absorbed (a Huygens slit).
    train_field: int | None = None
    train_carried: bool = False
    # Ray fields only: emit every ray on this one heading of the sequence instead
    # of sweeping the sequence (a directed emitter). None sweeps.
    heading: int | None = None
    # Bonded fields only: the owned scalar whose value bonds every emitted ray,
    # or, with bond_origin, the birth Node and tick themselves: the origin
    # travels with the ray until its next interaction.
    bond_field: int | None = None
    bond_origin: bool = False


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
    # Absorb mode on a claim field only: taking any share of a train's ray opens
    # a claim at this Node, and the record gathers that train's homing rays whole.
    claim: bool = False
    # Absorb mode with the lottery only: added to the field's capture seed for
    # this rule's ticket, so two detectors draw their own sequences.
    capture_salt: int = 0
    # Absorb mode on a bonded field only: the owned scalar holding this
    # detector's setting; a bonded ray is taken or left by the bond registry.
    bond_setting: int | None = None


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
                unpack(value)
        if any(value < 0 for payload in self.allocation_phases for value in unpack(payload)):
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
    # Fixed host provenance references; never inputs to a physical field law.
    cause_id: int | None = None
    sample_cause_id: int | None = None
    cost_cause_id: int | None = None
    # Later arrivals have destination ownership but cannot enter a frozen cycle.
    shared_pending: int = 0
    # Stationary stock per spatial field, deposited by localizing decay. It is
    # owned inventory at a known Node: never transported, decayed or sampled.
    localized: tuple[Payload, ...] = ()
    # Resident rays per spatial field (empty for non-ray fields). They arrived on
    # the previous link and leave on the next cycle along their own lines.
    rays: tuple[Rays, ...] = ()
    # Claims held per spatial field (empty for fields without claims): which
    # trains are gathered through this Node and toward which port.
    claims: tuple[Claims, ...] = ()
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
    # Claim and gather: the Node's claims after this cycle, one tuple per field,
    # and the claims passed to each port, one tuple per field per port.
    claims: tuple[Claims, ...] = ()
    outgoing_claims: tuple[tuple[Claims, ...], ...] = ()


@dataclass(frozen=True, slots=True)
class SpatialPacket:
    arrival_tick: int
    origin: Address3
    port: int
    fields: SpatialBundle
    cause_id: int | None = None
    rays: tuple[Rays, ...] = ()
    phases: SpatialBundle = ()
    claims: tuple[Claims, ...] = ()


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
        if type(ray.wait) is not int or not 0 <= ray.wait < pace[1]:
            raise ValueError("ray wait must stay below its heading's pace denominator")
        if type(ray.train) is not int or bounded(ray.train) < 0:
            raise ValueError("ray train must be a nonnegative bounded integer")
        if type(ray.homing) is not int or ray.homing not in (0, 1):
            raise ValueError("ray homing must be 0 or 1")
        if ray.homing and not (definition.claims and ray.train):
            raise ValueError("a homing ray requires a claim field and a train")
        if type(ray.bond) is not int or bounded(ray.bond) < 0:
            raise ValueError("ray bond must be a nonnegative bounded integer")
        if ray.bond and not definition.bonded:
            raise ValueError("a bonded ray requires a bonded field")


def validate_claims(claims: Claims, definition: SpatialFieldDefinition) -> None:
    if type(claims) is not tuple or len(claims) > definition.claim_slots:
        raise ValueError("claim slot budget exceeded")
    if claims and not definition.claims:
        raise ValueError("claims require a claim field")
    trains = set()
    for claim in claims:
        if type(claim) is not Claim:
            raise ValueError("claims require immutable Claim entries")
        if type(claim.train) is not int or bounded(claim.train) < 1:
            raise ValueError("a claim requires a positive bounded train")
        if type(claim.parent) is not int or not -1 <= claim.parent < 6:
            raise ValueError("a claim's parent must be -1 or a port")
        if type(claim.since) is not int or bounded(claim.since) < 0:
            raise ValueError("a claim's opening tick must be nonnegative")
        if type(claim.sent) is not int or claim.sent not in (0, 1):
            raise ValueError("a claim's sent flag must be 0 or 1")
        if (
            type(claim.origin) is not tuple
            or len(claim.origin) != 3
            or any(type(c) is not int or bounded(c) < -1 for c in claim.origin)
        ):
            raise ValueError("a claim's origin must be a lattice address")
        if claim.train in trains:
            raise ValueError("a Node holds one claim per train")
        trains.add(claim.train)


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
    combined: dict[tuple[int, tuple[int, int, int], int, int, int, int, int, int], int] = {}
    for ray in rays:
        key = (
            ray.heading,
            ray.accumulators,
            ray.phase,
            ray.advance,
            ray.wait,
            ray.train,
            ray.homing,
            ray.bond,
        )
        combined[key] = checked_work(combined.get(key, 0) + ray.amount)
    return tuple(
        Ray(heading, accumulators, bounded(amount), phase, advance, wait, train, homing, bond)
        for (heading, accumulators, phase, advance, wait, train, homing, bond), amount in sorted(
            combined.items()
        )
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


CAPTURE_MODES = ("share", "lottery", "threshold")
TICKET_MODULUS = 1073741789  # the largest prime below the field register bound


def next_ticket(state: int, salt: int) -> int:
    """Advance a local ticket state: a multiplicative congruence salted by the ray met."""
    if not 0 <= state < TICKET_MODULUS:
        raise ValueError("absorb ticket state must stay below the ticket modulus")
    return (state * 48271 + salt + 1) % TICKET_MODULUS


# A ray bonded to its origin leaves the planner with this mark; the Node that
# emits it replaces the mark with the code of its own address and the tick.
BOND_ORIGIN_MARK = TICKET_MODULUS


def origin_bond(position: Address3, shape: Address3, tick: int) -> int:
    """The bond of everything born at one Node on one tick: a positive bounded code."""
    index = (position[0] * shape[1] + position[1]) * shape[2] + position[2]
    return checked_work(index * 1048573 + bounded(tick)) % TICKET_MODULUS + 1


def ticket_draw(state: int) -> int:
    """The number a ticket state draws: its square modulo the ticket modulus.

    The state itself is affine in its salts, so two records that met the same
    rays would draw numbers a fixed distance apart; the square breaks that, so
    two detectors with their own seeds draw independently for every ray.
    """
    return checked_work(state * state) % TICKET_MODULUS


def ray_salt(ray: Ray) -> int:
    """A bounded integer that differs between rays of different line, phase or amount."""
    return (
        ray.heading * 7919
        + ray.accumulators[0] * 104729
        + ray.accumulators[1] * 1299709
        + ray.accumulators[2] * 15485863
        + ray.phase * 32452843
        + abs(ray.amount)
    ) % TICKET_MODULUS


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
_PACE_TABLES: dict[tuple[tuple[Heading, ...], bool, int, int], tuple[tuple[int, int], ...]] = {}


def integer_sqrt(value: int) -> int:
    """The floor of the square root, by Newton's method on integers."""
    if value < 0:
        raise ValueError("square root of a negative integer")
    if value < 2:
        return value
    guess = value
    better = (guess + value // guess) // 2
    while better < guess:
        guess, better = better, (better + value // better) // 2
    return guess


def heading_paces(definition: SpatialFieldDefinition) -> tuple[tuple[int, int], ...]:
    """(numerator, denominator) hops per tick for every heading.

    (1, 1) for every heading on the links metric at link speed; the configured
    pace scales every heading alike, and the Euclidean metric slows each heading
    to the slowest lattice direction on top of it.
    """
    key = (
        definition.headings,
        definition.euclidean,
        definition.pace_numerator,
        definition.pace_denominator,
    )
    table = _PACE_TABLES.get(key)
    if table is None:
        numerator, denominator = definition.pace_numerator, definition.pace_denominator
        if not definition.euclidean:
            table = tuple((numerator, denominator) for _ in definition.headings)
        else:
            ratios = []
            for heading in definition.headings:
                manhattan = sum(abs(c) for c in heading)
                squared = sum(c * c for c in heading)
                # E / L scaled: the Euclidean length in units of 1 / PACE_SCALE per link.
                ratios.append(integer_sqrt(squared * PACE_SCALE * PACE_SCALE) // manhattan)
            slowest = min(ratios)
            table = tuple(
                (checked_work(slowest * numerator), checked_work(ratio * denominator))
                for ratio in ratios
            )
        _PACE_TABLES[key] = table
    return table


def heading_pace(definition: SpatialFieldDefinition, heading: int) -> tuple[int, int]:
    return heading_paces(definition)[heading]
