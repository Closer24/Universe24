"""Fixed local records for optional initialization-defined spatial fields."""

from dataclasses import dataclass, replace
from dataclasses import field as dataclass_field
from functools import lru_cache

from .disturbance_state import (
    MAX_COMPONENTS,
    MAX_RULES,
    MAX_SLOTS,
    MAX_VALUE,
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
# that drew 0 or 1. Every created ray carries 0; a marked Node sets 1 or 2 on
# arrival (detector_draw) and no rule reads it.
DETECTOR_NONE, DETECTOR_BIT_0, DETECTOR_BIT_1 = 0, 1, 2
# Layers of event spacetime (Highlights 5.1): a layer is a set of families that
# couple, and a meeting exists only inside a layer. Layers are derived, never
# declared: the connected components of the ray fields over the participants
# of the declared ray interactions, a field no rule selects being its own layer.
RAY_LAYERS = "ray-layers-v1"
Layers = tuple[tuple[int, ...], ...]
# The meeting of rays with N-to-M outputs (Highlights 3.17, 3.26 and 5.1): a rule
# with declared outputs replaces its participants by new event rays at the
# meeting Node, an amount may be split by a declared table indexed by the phase
# difference of two inputs, and every family's stock is exact across the event.
RAY_MEETING = "ray-meeting-conversion-v1"
# The field as the ray's information (Highlights 3.5, 3.14, 3.15 and 3.28): a ray
# field declared with field_of is the field of that family, released at every
# Node a ray of the family crosses as one ray per heading, booked as a source;
# a meeting of a field ray is an ordinary declared rule whose outputs return it
# reversed as the recoil. A field has no field.
RELEASED_FIELD = "released-field-v1"
# Binding and gravity by delay (Highlights 3.4 and 3.28, ray-binding-v1): a rule
# without outputs whose assignment sets delay 1 binds its participants as a bound
# group that stays at the Node, ticks every interval and releases its field on all
# six headings; an earlier outputs rule that names a bound participant and an
# arriving ray unbinds it; a binding rule may declare the Node's output-clock
# delay (ray_delay); a meeting output may carry a delay by a declared table per
# the Port the field ray came through, a lag of the output's face clock in phase
# steps that turns the ray toward the lagging side one Link per phase modulus.
RAY_BINDING = "ray-binding-v1"
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
PORT_HEADINGS: tuple[Heading, ...] = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)
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
# The Detector mark (Highlights 3.19, 3.20 and 5.4, detector-mark-v1): a Node's
# bit with its setting and ticket seed. A marked Node draws one bit per arriving
# ray from its own ticket stream, reading nothing from the ray, and is otherwise
# an ordinary Node. In this slice the ray continues unchanged on both outcomes.
DETECTOR_MARK = "detector-mark-v1"
MAX_DETECTORS = 4096
# A draw of 0 returns the arriving ray on its own line (detector-return-v1): the
# same wave ray reversed, unchanged, walking its steps back to its event Node.
DETECTOR_RETURN = "detector-return-v1"
# At its event Node a returned ray performs the inverse split of its own share
# (inverse-split-v1, Highlights 3.20 "Return modes"): by the world's return_mode
# it transmits its amount, phase and bit to the sibling lines of its event
# (siblings), continues straight on the one line opposite its own (straight) or
# ends there into an explicitly accounted sink (annul).
INVERSE_SPLIT = "inverse-split-v1"
RETURN_MODES = ("siblings", "straight", "annul")
# The external body (Highlights 3.19, external-body-v1): the second declared
# element of a world beside the Detector mark, a Node declared to hold a family
# with an amount of any width, a charge and a momentum. It radiates the field of
# its family on all six headings once per interval, booked as a source; it never
# spreads; whatever arrives is met by its declared coupling, the sink by default;
# only field rays named by its momentum table move it, one Link per axis when a
# whole amount has accumulated.
EXTERNAL_BODY = "external-body-v1"
MAX_EXTERNAL_BODIES = 4096
BODY_SINK = -1
# Field spreading (Highlights 3.5, 3.17, 3.20 and 3.23, model owner 2026-09-17;
# field-spreading-v1): light is the field, and the field spreads. A family that
# declares `spread`, six weights in Port order relative to the arriving heading
# (forward, backward, the four transverse in Port order), releases again at
# every Node its content reaches: the outbound content that arrived is taken
# off the Node, amounts add per arriving heading, the phase is the phase of the
# coherent sum, each heading's content is shared by the table in whole quanta
# and the remainder leaves whole through the entry the phase selects; the
# departures are fresh field rays with no event. Huygens' principle in the
# lattice's language: one catalog entry of the family, not an engine mechanism.
FIELD_SPREADING = "field-spreading-v1"
SPREAD_ENTRIES = 6
SPREAD_BACKWARD = 1


@dataclass(frozen=True, slots=True)
class DetectorMark:
    """A Node's Detector bit with its setting and ticket seed: bounded Node metadata.

    The setting is the pass share of the draw range, an explicit rational with no
    default; the seed starts the mark's own ticket stream. Nothing here is a
    record, stock or a reading of any ray.
    """

    position: Address3
    pass_numerator: int
    pass_denominator: int
    seed: int

    def __post_init__(self) -> None:
        if type(self.position) is not tuple or len(self.position) != 3:
            raise ValueError("a Detector mark requires a three-integer position")
        if any(type(c) is not int or bounded(c) < 0 for c in self.position):
            raise ValueError("a Detector mark position must be nonnegative bounded integers")
        if bounded(self.pass_denominator) < 1:
            raise ValueError("a Detector setting requires a positive denominator")
        if not 0 <= bounded(self.pass_numerator) <= self.pass_denominator:
            raise ValueError("a Detector setting must be a rational from 0 through 1")
        if type(self.seed) is not int or not 0 <= self.seed < TICKET_MODULUS:
            raise ValueError("a Detector seed must stay below the ticket modulus")


@dataclass(frozen=True, slots=True)
class ExternalBody:
    """The external body mark of a Node (external-body-v1): bounded Node metadata.

    The declaration (position, family as a spatial field index, amount of any
    width, charge, the released field's index or -1, the coupling as a ray
    interaction index or BODY_SINK, the released phase, the momentum table as one
    sign per spatial field), the momentum with its three exact accumulators, and
    one exact sink counter per spatial field. No rays, no history.
    """

    index: int
    position: Address3
    family: int
    amount: int
    charge: int = 0
    field: int = -1
    coupling: int = BODY_SINK
    phase: int = 0
    signs: tuple[int, ...] = ()
    momentum: tuple[int, int, int] = (0, 0, 0)
    accumulators: tuple[int, int, int] = (0, 0, 0)
    sink: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if type(self.index) is not int or not 0 <= self.index < MAX_EXTERNAL_BODIES:
            raise ValueError("an external body index must stay below the body capacity")
        if type(self.position) is not tuple or len(self.position) != 3:
            raise ValueError("an external body requires a three-integer position")
        if any(type(c) is not int or bounded(c) < 0 for c in self.position):
            raise ValueError("an external body position must be nonnegative bounded integers")
        if type(self.amount) is not int or self.amount < 1:
            raise ValueError("an external body amount must be a positive integer")
        if type(self.family) is not int or self.family < 0:
            raise ValueError("an external body family must be a spatial field index")
        if type(self.field) is not int or self.field < -1:
            raise ValueError("an external body field must be a spatial field index or -1")
        if type(self.coupling) is not int or self.coupling < BODY_SINK:
            raise ValueError("an external body coupling must be a rule index or the sink")
        if type(self.phase) is not int or self.phase < 0:
            raise ValueError("an external body phase must be a nonnegative integer")
        bounded(self.charge)
        for vector in (self.momentum, self.accumulators):
            if type(vector) is not tuple or len(vector) != 3:
                raise ValueError("an external body momentum requires three integers")
            for value in vector:
                checked_work(value)
        if any(abs(value) >= self.amount for value in self.accumulators):
            raise ValueError("an external body accumulator stays below its amount")
        if type(self.signs) is not tuple or any(sign not in (-1, 0, 1) for sign in self.signs):
            raise ValueError("an external body momentum table holds signs -1, 0 or 1")
        if type(self.sink) is not tuple or any(type(v) is not int or v < 0 for v in self.sink):
            raise ValueError("an external body sink holds nonnegative counters")


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
    # Bending by delay (ray-binding-v1, Highlights 3.28): the lag of the ray's
    # output-face clocks in phase steps, one signed integer per axis, positive
    # toward the +axis Port. A transverse lag that reaches the phase modulus is
    # spent as one Link toward the lagging side at the next departure; a lag on
    # the ray's own axis as one interval of wait. Zero on every created ray.
    lag: tuple[int, int, int] = (0, 0, 0)


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
        if not 2 <= len(rule.participants) <= 6 or rule.k or rule.output_types is not None:
            raise ValueError("ray interactions require two to six indexed roles without k or conversion")
        for role in rule.participants:
            if not role or any(
                type(index) is not int or not 0 <= index < len(definitions) for index in role
            ):
                raise ValueError("ray participant role refers to an unavailable spatial field")
            selected.update(role)
        if rule.outputs:
            # A meeting with outputs (ray-meeting-conversion-v1): one to six new event
            # rays of ray fields, assigned from the frozen inputs, in the same layer.
            if not 1 <= len(rule.outputs) <= 6 or any(
                type(kind) is not int or not 0 <= kind < len(definitions) for kind in rule.outputs
            ):
                raise ValueError("ray meeting outputs require one to six ray fields")
            selected.update(rule.outputs)
            if any(
                not 0 <= assignment.side < len(rule.outputs)
                or not 0 <= assignment.field < len(RAY_PROPERTIES)
                for assignment in rule.assignments
            ):
                raise ValueError("ray meeting assignments address its declared outputs")
            if any(
                not 0 <= split.first < len(rule.outputs)
                or not 0 <= split.second < len(rule.outputs)
                or split.first == split.second
                or split.field != 0
                or split.phase_field != 2
                or not 1 <= len(split.table) <= MAX_PHASE_STEPS
                or any(
                    type(weight) is not int or not 0 <= weight <= len(split.table)
                    for weight in split.table
                )
                or any(not 0 <= index < len(rule.participants) for index in split.between)
                or split.between[0] == split.between[1]
                or not -1 <= split.source < len(rule.participants)
                or any(len(split.table) != definitions[kind].phase_modulus for kind in rule.outputs)
                for split in rule.splits
            ):
                raise ValueError("ray meeting table split requires two outputs and the phase modulus")
            if bounded(rule.ray_delay):
                raise ValueError("ray_delay is declared by a binding rule, one without outputs")
            for lag in rule.lags:
                # ray-binding-v1: a delay by a table per Port on one output, read from
                # the amount and the Port of one input.
                if (
                    not 0 <= lag.output < len(rule.outputs)
                    or not 0 <= lag.source < len(rule.participants)
                    or len(lag.table) != 6
                    or any(type(v) is not int or bounded(v) < 0 for v in lag.table)
                    or type(lag.per) is not int
                    or not 1 <= lag.per <= MAX_VALUE
                ):
                    raise ValueError(
                        "a delay table names an output and an input, six Port entries and a unit"
                    )
        elif rule.splits:
            raise ValueError("a table split requires a meeting with outputs")
        elif rule.lags:
            raise ValueError("a delay table requires a meeting with outputs")
        elif any(assignment.field not in RAY_WRITABLE for assignment in rule.assignments):
            raise ValueError("ray interaction amount, advance, family and charge are read-only")
        elif type(rule.ray_delay) is not int or bounded(rule.ray_delay) < 0:
            raise ValueError("a binding rule's ray_delay is a nonnegative bounded integer")
    for layer in ray_layers(definitions, rules):
        # The indexed selector's capacity bounds one meeting, and a meeting exists
        # only inside a layer: fields of different layers never share it.
        if selected.intersection(layer) and (
            sum(definitions[index].ray_slots for index in layer) > MAX_SLOTS
        ):
            raise ValueError("ray interactions require at most 32 selected ray slots in one layer")
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


def ray_layers(
    definitions: tuple[SpatialFieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
) -> Layers:
    """The layers over the ray fields (ray-layers-v1): the connected components of the
    fields that the roles of one rule can select, and one layer for every ray field
    that no rule selects. Each layer lists its spatial-field indices in field order
    and the layers are in the order of their first field. Bounded by the number of
    spatial fields and the fixed rule capacity; nothing is declared."""
    if type(rules) is not tuple or len(rules) > MAX_RULES:
        raise ValueError("ray interaction rules exceed their fixed capacity")
    parent = list(range(len(definitions)))

    def root(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for rule in rules:
        # The fields a rule's roles select and the fields of its outputs couple.
        selected = {kind for role in rule.participants for kind in role} | set(rule.outputs)
        if any(type(kind) is not int or not 0 <= kind < len(definitions) for kind in selected):
            raise ValueError("ray participant role refers to an unavailable spatial field")
        kinds = sorted(selected)
        for kind in kinds[1:]:
            parent[root(kind)] = root(kinds[0])
    members: dict[int, list[int]] = {}
    for index, definition in enumerate(definitions):
        if definition.rays:
            members.setdefault(root(index), []).append(index)
    return tuple(tuple(layer) for layer in sorted(members.values()))


def ray_layer_names(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
) -> tuple[tuple[str, ...], ...]:
    """The derived layers as family names for the run record, sorted within each layer
    and between layers."""
    return tuple(
        sorted(
            tuple(sorted(fields[definitions[index].field].name for index in layer))
            for layer in ray_layers(definitions, rules)
        )
    )


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


def validate_released_fields(
    definitions: tuple[SpatialFieldDefinition, ...], fields: tuple[FieldDefinition, ...]
) -> None:
    """The admission of a released field (released-field-v1): a positive, conserved,
    unpaced unit-axial ray field on the links metric with the six Port headings,
    the field of another such ray field with the same phase steps, which is not
    itself a field of anything, released as a rational at most 1."""
    for definition in definitions:
        if definition.field_of is None:
            if definition.release_numerator or definition.release_denominator != 1:
                raise ValueError("a release ratio requires field_of")
            continue
        if type(definition.field_of) is not int or not 0 <= definition.field_of < len(definitions):
            raise ValueError("field_of refers to an unavailable spatial field")
        origin = definitions[definition.field_of]
        if origin is definition or origin.field == definition.field:
            raise ValueError("a family is not its own field")
        if origin.field_of is not None:
            raise ValueError("a field has no field")
        numerator, denominator = definition.release_numerator, definition.release_denominator
        if not 1 <= bounded(numerator) <= bounded(denominator):
            raise ValueError("release must be a rational from 1 / d through 1")
        for member in (definition, origin):
            field = fields[member.field]
            if (
                not member.rays
                or field.signed
                or not field.conserved
                or any(unpack(member.baseline))
                or member.euclidean
                or member.pace_numerator != member.pace_denominator
                or member.self_exclusion
                or member.decay is not None
                or any(sum(abs(c) for c in heading) != 1 for heading in member.headings)
            ):
                raise ValueError("a released field requires positive unit-axial unpaced ray fields")
        if any(heading not in definition.headings for heading in PORT_HEADINGS):
            raise ValueError("a released field requires the six Port headings")
        if definition.phase_modulus != origin.phase_modulus:
            raise ValueError("a released field carries its source's phase steps: one phase width")


def validate_released_field_admission(initial: InitialState) -> None:
    """A world with a released field runs under the shared Detector admission."""
    if not any(definition.field_of is not None for definition in initial.spatial_fields):
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
        raise ValueError("a released field requires the default fixed H=1 spatial clock")
    validate_released_fields(initial.spatial_fields, initial.fields)
    involved = {
        definition.field for definition in initial.spatial_fields if definition.field_of is not None
    } | {
        initial.spatial_fields[definition.field_of].field
        for definition in initial.spatial_fields
        if definition.field_of is not None
    }
    if any(rule.field in involved for rule in initial.spatial_couplings):
        raise ValueError("a released field does not support coupled responses or absorption")


def release_amount(amount: int, definition: SpatialFieldDefinition) -> int:
    """The amount of one released ray: the whole quanta of amount x n / d. The
    fraction the floor leaves is not released: the field is a description booked
    as a source, so nothing owned is lost (Highlights 3.17)."""
    return checked_work(amount * definition.release_numerator) // definition.release_denominator


def _released(amount: int, phase: int, definition: SpatialFieldDefinition, skip: Heading | None) -> Rays:
    return tuple(
        Ray(definition.headings.index(heading), (0, 0, 0), amount, phase=phase)
        for heading in PORT_HEADINGS
        if heading != skip
    )


def release_field(
    rays: Rays, definition: SpatialFieldDefinition, origin: SpatialFieldDefinition
) -> Rays:
    """The field rays a bundle of source rays releases at the Node they depart from
    (released-field-v1): one ray per Port heading except the source ray's own,
    each with the released amount and the source's phase, no event (mask 0,
    steps 0). The heading the source travels on is the source's own line ahead of
    it, which at link speed the source itself occupies, so it releases nothing
    there and a straight ray never shares a Node with its own field. A ray held
    at the Node by its interaction delay (a bound group, ray-binding-v1) occupies
    no line ahead of it and releases on all six headings, once per interval."""
    released: list[Ray] = []
    for ray in rays:
        amount = release_amount(ray.amount, definition)
        if amount <= 0:
            continue
        skip = None if ray.interaction_delay else origin.headings[ray.heading]
        released.extend(_released(amount, ray.phase, definition, skip))
    return tuple(released)


def bound_group(rays: tuple[Rays, ...]) -> tuple[tuple[int, Ray], ...]:
    """The bound group resident at a Node (ray-binding-v1, Highlights 3.4): the
    outbound rays at their event Node with no delay or wait pending, as (spatial
    field, ray) pairs in field and merge-key order. A ray is at its event Node with
    `steps` 0 only while a rule holds it there and ticks again; every other resident
    ray has walked a Link, is waiting, or is returned. The Node keeps nothing else."""
    return tuple(
        (index, ray)
        for index, bundle in enumerate(rays)
        for ray in sorted(bundle, key=ray_merge_key)
        if ray.outbound and ray.steps == 0 and not ray.interaction_delay and not ray.wait
    )


def release_stock(stock: int, definition: SpatialFieldDefinition) -> Rays:
    """The field rays resident content releases once per interval: one ray per Port
    heading, all six, from the stock a record holds, with phase 0 (a record has no
    phase of its own in this slice)."""
    amount = release_amount(stock, definition)
    return _released(amount, 0, definition, None) if amount > 0 else ()


def holds_source_stock(
    record: DisturbanceRecord | None, definitions: tuple[SpatialFieldDefinition, ...]
) -> bool:
    """Whether a resident record holds stock of a family that has a released field."""
    if record is None:
        return False
    for definition in definitions:
        if definition.field_of is None:
            continue
        field = definitions[definition.field_of].field
        if field < len(record.values) and unpack(record.values[field])[0] > 0:
            return True
    return False


def released_field_names(
    fields: tuple[FieldDefinition, ...], definitions: tuple[SpatialFieldDefinition, ...]
) -> list[dict[str, object]]:
    """The released fields for the run record: each field ray family with the family
    it is the field of and its release ratio, in field order."""
    return [
        {
            "field": fields[definition.field].name,
            "field_of": fields[definitions[definition.field_of].field].name,
            "release": [definition.release_numerator, definition.release_denominator],
        }
        for definition in definitions
        if definition.field_of is not None
    ]


# Field spreading (field-spreading-v1). Every rule here reads the content that
# arrived at one Node and the family's declared table; nothing reads another Node.


@dataclass(frozen=True, slots=True)
class FieldSpread:
    """The record of one spread for the Node to publish (field-spreading-v1): plain
    bounded integers, as the Node state contract requires. The spatial field, the
    amount taken off the Node, the amount that arrived per heading (six entries by
    the heading's Port index), the departure per Port, the remainder quanta placed
    per Port, the combined phase and the reduced coherence of the arrivals."""

    field: int
    amount: int
    arrived: tuple[int, ...]
    amounts: tuple[int, ...]
    remainders: tuple[int, ...]
    phase: int
    coherence: tuple[int, int]


def validate_spread_table(table: tuple[int, ...]) -> int:
    """The split table of a spreading family: six nonnegative bounded weights in Port
    order relative to the arriving heading, the backward weight positive (a
    forward-only split piles the field on the diagonals and empties the axes,
    Highlights 3.5) and the four transverse weights equal (the lattice has no
    preferred transverse direction, Highlights 3.23). Returns the total, the
    table's denominator."""
    if (
        type(table) is not tuple
        or len(table) != SPREAD_ENTRIES
        or any(type(weight) is not int or bounded(weight) < 0 for weight in table)
    ):
        raise ValueError(
            "a spread table holds six nonnegative integer weights in Port order relative to "
            "the arriving heading"
        )
    if table[SPREAD_BACKWARD] <= 0:
        raise ValueError("a spread table must give the backward heading a positive weight")
    if len(set(table[2:])) != 1:
        raise ValueError("a spread table gives the four transverse headings one weight")
    return bounded(sum(table))


def validate_spread_fields(
    definitions: tuple[SpatialFieldDefinition, ...], fields: tuple[FieldDefinition, ...]
) -> None:
    """The admission of a spreading family (field-spreading-v1): the geometry of a
    released field (a positive, conserved, unpaced unit-axial ray field on the
    links metric with the six Port headings, zero baseline, no decay, no
    self-exclusion) and, with a phase width, the coherence table, since the phase
    of the content is the phase of the coherent sum."""
    for definition in definitions:
        if not definition.spread:
            continue
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
            or any(sum(abs(c) for c in heading) != 1 for heading in definition.headings)
        ):
            raise ValueError("a spreading family requires a positive unit-axial unpaced ray field")
        if any(heading not in definition.headings for heading in PORT_HEADINGS):
            raise ValueError("a spreading family requires the six Port headings")
        if definition.phase_bits and not definition.coherent:
            raise ValueError(
                "a spreading family with a phase width declares the coherence table: the phase "
                "of the content is the phase of the coherent sum"
            )


def validate_spread_admission(initial: InitialState) -> None:
    """A world with a spreading family runs under the shared Detector admission."""
    if not any(definition.spread for definition in initial.spatial_fields):
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
        raise ValueError("a spreading family requires the default fixed H=1 spatial clock")
    validate_spread_fields(initial.spatial_fields, initial.fields)
    spreading = {definition.field for definition in initial.spatial_fields if definition.spread}
    if any(rule.field in spreading for rule in initial.spatial_couplings):
        raise ValueError("a spreading family does not support coupled responses or absorption")


def relative_ports(port: int) -> tuple[int, ...]:
    """The six Ports in the order of a spread table for content arriving on the
    heading of Port `port`: forward, that Port; backward, its opposite; then the
    four transverse Ports in Port order."""
    if type(port) is not int or not 0 <= port < 6:
        raise ValueError("a relative Port order requires a Port index")
    return (port, port ^ 1, *(other for other in range(6) if other >> 1 != port >> 1))


def spread_remainder_entry(phase: int, phase_modulus: int, table: tuple[int, ...]) -> int:
    """The entry of the table the phase selects for the remainder (Highlights 3.17
    and 3.20, the steering table's rule for a whole quantum): the phase, as a
    share of the turn, laid against the weights end to end; the smallest entry i
    with modulus x (w_0 + ... + w_i) > phase x total. At phase 0 the first entry
    with a weight; over all phases the remainders follow the table."""
    total = sum(table)
    target = checked_work(phase * total)
    cumulative = 0
    for entry, weight in enumerate(table):
        cumulative = checked_work(cumulative + weight)
        if checked_work(phase_modulus * cumulative) > target:
            return entry
    raise ValueError("a spread phase must be below the family's phase width")


def spread_phase(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The one phase of the content a Node spreads: the phase step nearest the
    direction of the coherent sum over every taken ray (the coherence rule of
    Highlights 3.20; a cancelled sum gives step 0), 0 for a family without a
    phase width."""
    if not definition.coherent:
        return 0
    return phase_of_sum(tuple((abs(ray.amount), ray.phase) for ray in rays), definition)


def spread_content(
    index: int, rays: Rays, definition: SpatialFieldDefinition
) -> tuple[Rays, FieldSpread]:
    """The spread of one family's content at a Node (field-spreading-v1): the
    departures, one fresh field ray per Port with content in Port order, and the
    record. The rays are the outbound content that arrived (at least one Link
    walked). Amounts add per arriving heading; the phase of the whole is the
    phase of the coherent sum and its Detector bit the catalog default, 1
    outranks 0 outranks none; each heading's content is shared over the six
    relative headings in whole quanta, floor(content x weight / total), and the
    quanta the floors leave, at most five, leave whole through the entry the
    phase selects. Each departure carries the Port's heading, accumulators
    (0, 0, 0), the combined phase, the family's rate, no wait, delay or lag,
    steps 0, outbound 1 and no event. The total is exact."""
    table = definition.spread
    total = validate_spread_table(table)
    arrived = [0] * 6
    for ray in rays:
        if not ray.outbound or ray.steps < 1 or ray.amount <= 0:
            raise ValueError("a spread takes the outbound content that arrived at the Node")
        heading = definition.headings[ray.heading]
        if heading not in PORT_HEADINGS:
            raise ValueError("a spread requires content on a Port heading")
        port = PORT_HEADINGS.index(heading)
        arrived[port] = checked_work(arrived[port] + ray.amount)
    phase = spread_phase(rays, definition)
    entry = spread_remainder_entry(phase, definition.phase_modulus, table)
    amounts, remainders = [0] * 6, [0] * 6
    for port, content in enumerate(arrived):
        if not content:
            continue
        ports = relative_ports(port)
        placed = 0
        for weight, target in zip(table, ports, strict=True):
            share = checked_work(content * weight) // total
            amounts[target] = checked_work(amounts[target] + share)
            placed = checked_work(placed + share)
        rest = content - placed
        amounts[ports[entry]] = checked_work(amounts[ports[entry]] + rest)
        remainders[ports[entry]] = checked_work(remainders[ports[entry]] + rest)
    bit = max(ray.detector for ray in rays)
    departures = tuple(
        Ray(
            definition.headings.index(PORT_HEADINGS[port]),
            (0, 0, 0),
            bounded(amount),
            phase=phase,
            detector=bit,
        )
        for port, amount in enumerate(amounts)
        if amount
    )
    numerator, denominator = coherence(rays, definition)
    record = FieldSpread(
        index,
        bounded(sum(arrived)),
        tuple(arrived),
        tuple(amounts),
        tuple(remainders),
        phase,
        reduced_ratio(numerator, denominator),
    )
    return departures, record


def spreading_field_names(
    fields: tuple[FieldDefinition, ...], definitions: tuple[SpatialFieldDefinition, ...]
) -> list[dict[str, object]]:
    """The spreading families for the run record: each with its table, in field order."""
    return [
        {"field": fields[definition.field].name, "spread": list(definition.spread)}
        for definition in definitions
        if definition.spread
    ]


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
    # Released field (released-field-v1): the spatial-field index of the family
    # whose field this ray field is, and the release ratio, the share of the
    # source's amount each released ray carries per Node crossed.
    field_of: int | None = None
    release_numerator: int = 0
    release_denominator: int = 1
    # Field spreading (field-spreading-v1): the split table, six weights in Port
    # order relative to the arriving heading; empty for a family that does not
    # spread, the behaviour of every existing world.
    spread: tuple[int, ...] = ()
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
        if self.spread:
            if not self.rays:
                raise ValueError("spread requires ray transport")
            validate_spread_table(self.spread)

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
    # The Detector mark of this Node when its bit is set, and the mark's own ticket
    # state: seeded from the mark, advanced by one unsalted step per arriving ray.
    detector: DetectorMark | None = None
    detector_ticket: int = 0
    # The external body this Node holds, whole, when one is declared or has
    # stepped here (external-body-v1); None at every other Node.
    body: ExternalBody | None = None
    # The output-clock delay of the bound group held here (ray-binding-v1): the
    # intervals every arriving ray waits before it meets or departs; 0 without.
    bound_delay: int = 0


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
    # The output-clock delay declared by the binding rule that fired this cycle.
    bound_delay: int = 0
    # The inverse splits of this cycle, one per returned ray at its event Node,
    # and the content they annulled per field (inverse-split-v1).
    inverse_splits: tuple[InverseSplit, ...] = ()
    annulled: Values = ()
    # The external body after this cycle and the Port it steps through, or -1
    # when it stays (external-body-v1); None at a Node without a body.
    body: ExternalBody | None = None
    body_port: int = -1
    # The spreads of this cycle, one per spreading family whose content arrived
    # (field-spreading-v1).
    spreads: tuple[FieldSpread, ...] = ()


@dataclass(frozen=True, slots=True)
class InverseSplit:
    """The record of one inverse split for the Node to publish (inverse-split-v1).

    Plain bounded integers, as the Node state contract requires: the spatial
    field, the mode as its index in RETURN_MODES, the Ports transmitted to with
    the amount per Port, the returned share, the ray's Detector bit (0 or 1, or -1
    for none), 1 when the share was first restored to the event's input at the
    Node, and, in annul mode, the per-field content that left the world.
    """

    field: int
    mode: int
    ports: tuple[int, ...]
    amounts: tuple[int, ...]
    amount: int
    bit: int
    restored: int
    annulled: Values = ()


@dataclass(frozen=True, slots=True)
class SpatialPacket:
    arrival_tick: int
    origin: Address3
    port: int
    fields: SpatialBundle
    rays: tuple[Rays, ...] = ()
    phases: SpatialBundle = ()
    # An external body stepping one Link through this Port (external-body-v1).
    body: ExternalBody | None = None


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
        if type(ray.lag) is not tuple or len(ray.lag) != 3 or any(type(v) is not int for v in ray.lag):
            raise ValueError("a ray requires three integer face-clock lags")
        for value in ray.lag:
            bounded(value)
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
    with no steps walked, each carrying the mask and shares of that interaction. A
    fresh event carries no Detector bit; a marked Node sets it on arrival."""
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


def return_ray(ray: Ray, definition: SpatialFieldDefinition) -> Ray:
    """The same wave ray reversed on its line (detector-return-v1).

    The heading index becomes the index of the negated heading, outbound becomes 0
    and the transport accumulators (DDA, pace wait, interaction delay, face-clock
    lag) are reset;
    amount, phase, steps, event Ports, event shares and Detector bit are exactly
    what arrived. The Detector admission guarantees the negated heading is in the
    sequence; a field where it is not fails closed.
    """
    heading = definition.headings[ray.heading]
    negated = (-heading[0], -heading[1], -heading[2])
    if negated not in definition.headings:
        raise ValueError("a return requires the negated heading in the field's sequence")
    return replace(
        ray,
        heading=definition.headings.index(negated),
        accumulators=(0, 0, 0),
        wait=0,
        interaction_delay=0,
        lag=(0, 0, 0),
        outbound=0,
    )


def event_port(ray: Ray, definition: SpatialFieldDefinition) -> int:
    """The Port the ray's event sent it through: the first DDA step of its event heading
    from the event Node. A returning ray's event heading is its own heading negated."""
    heading = definition.headings[ray.heading]
    if not ray.outbound:
        heading = (-heading[0], -heading[1], -heading[2])
    port, _ = dda_step((0, 0, 0), heading)
    return port


def port_heading(port: int, definition: SpatialFieldDefinition) -> int:
    """The index of the unit-axial heading that leaves through the given Port; a field
    without that line fails closed."""
    axis, negative = divmod(port, 2)
    unit = tuple(0 if i != axis else (-1 if negative else 1) for i in range(3))
    if unit not in definition.headings:
        raise ValueError("a transmission requires the line of its Port in the field's sequence")
    return definition.headings.index(unit)


def split_ports(ray: Ray, definition: SpatialFieldDefinition, mode: str) -> tuple[int, ...]:
    """The Ports a returned ray transmits to at its event Node, in Port order.

    siblings: every Port of its event's mask except its own; straight: the one Port
    opposite its own; annul: none.
    """
    if mode not in RETURN_MODES:
        raise ValueError("return_mode must be siblings, straight or annul")
    own = event_port(ray, definition)
    if mode == "annul":
        return ()
    if mode == "straight":
        return (own ^ 1,)
    return tuple(port for port in range(6) if ray.event_ports >> port & 1 and port != own)


def split_amounts(amount: int, count: int) -> tuple[int, ...]:
    """Share one amount exactly over `count` lines, the remainder to the first lines
    in Port order (Highlights 3.17): nothing is dropped and nothing stays."""
    if count <= 0:
        return ()
    magnitude, sign = abs(bounded(amount)), -1 if amount < 0 else 1
    base, extra = divmod(magnitude, count)
    return tuple(sign * (base + int(offset < extra)) for offset in range(count))


def transmit(ray: Ray, definition: SpatialFieldDefinition, mode: str) -> tuple[Rays, tuple[int, ...]]:
    """The inverse split of a returned ray at its event Node (inverse-split-v1).

    The ray must be resident at its event Node (`outbound` 0, `steps` 0). The
    transmission is a set of new event rays at this Node: outbound, no steps
    walked, the returned ray's phase, advance and Detector bit, the mask of the
    lines transmitted to and the amount per line as their event record. Returns the
    rays and the Ports, in Port order; annul transmits nothing.
    """
    if ray.outbound or ray.steps:
        raise ValueError("the inverse split requires a returned ray at its event Node")
    ports = split_ports(ray, definition, mode)
    amounts = split_amounts(ray.amount, len(ports))
    rays = tuple(
        Ray(port_heading(port, definition), (0, 0, 0), amount, ray.phase, ray.advance)
        for port, amount in zip(ports, amounts, strict=True)
        if amount
    )
    stamped = stamp_event(rays, tuple(definition.headings[r.heading] for r in rays))
    return tuple(replace(r, detector=ray.detector) for r in stamped), ports


RayMergeKey = tuple[
    int, tuple[int, int, int], int, int, int, int, int, int, int, EventShares, int, tuple[int, int, int]
]


def ray_merge_key(ray: Ray) -> RayMergeKey:
    """The identity of a ray's line and event: everything but its amount, in a fixed order."""
    return (
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
        ray.lag,
    )


def merge_rays(rays: Rays) -> Rays:
    """Combine rays that share heading, lattice phase, wave phase and event: one line, so exact.

    Rays of different events never merge, whatever their heading and phase: the
    event state is part of the identity, so each ray keeps the information of
    its own event.
    """
    combined: dict[RayMergeKey, int] = {}
    for ray in rays:
        key = ray_merge_key(ray)
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
            lag=lag,
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
            lag,
        ), amount in sorted(combined.items())
        if amount
    )


def ray_stock(rays: Rays) -> int:
    total = 0
    for ray in rays:
        total = checked_work(total + ray.amount)
    return bounded(total)


def ray_momentum(rays: Rays, definition: SpatialFieldDefinition) -> tuple[int, int, int]:
    """Read the candidate's amount-times-heading inventory from actual ray owners.

    A returning ray (outbound 0) reads as its share on the event's heading, its
    own heading negated: the Detector takes no recoil on a return and the audit
    stays exact (detector-return-v1, issue #169).
    """
    result = [0, 0, 0]
    for ray in rays:
        sign = 1 if ray.outbound else -1
        for axis, component in enumerate(definition.headings[ray.heading]):
            result[axis] = checked_work(result[axis] + sign * checked_work(ray.amount * component))
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
# an absorber never draws. The ticket sequence below is the bounded local draw
# the Detector mark owns (detector_draw); no other owner calls it.
CAPTURE_MODES = ("share", "threshold")
TICKET_MODULUS = 1073741789  # the largest prime below the field register bound


def next_ticket(state: int, salt: int) -> int:
    """Advance a local ticket state: a multiplicative congruence plus a salt.

    The Detector mark draws unsalted (salt 0): its stream depends on its seed and
    the order of its arrivals alone, never on what arrives.
    """
    if not 0 <= state < TICKET_MODULUS:
        raise ValueError("ticket state must stay below the ticket modulus")
    return (state * 48271 + salt + 1) % TICKET_MODULUS


def ticket_draw(state: int) -> int:
    """The number a ticket state draws: its square modulo the ticket modulus.

    The state itself is affine in its salts, so two marks that met the same
    arrivals would draw numbers a fixed distance apart; the square breaks that,
    so two Detectors with their own seeds draw independently for every arrival.
    """
    return checked_work(state * state) % TICKET_MODULUS


def detector_draw(ticket: int, mark: DetectorMark) -> tuple[int, int]:
    """One unsalted draw of a marked Node: the next ticket state and the bit, 1 = PASS.

    The bit is 1 when the drawn number times the setting's denominator is below
    the numerator times the ticket modulus, so the setting is the pass share of
    the draw range: 1 / 1 always passes and 0 / 1 never does. The product is a
    64-bit intermediate. The draw reads nothing from the ray it is drawn for.
    """
    state = next_ticket(ticket, 0)
    number = ticket_draw(state)
    passes = checked_work(number * mark.pass_denominator) < checked_work(
        mark.pass_numerator * TICKET_MODULUS
    )
    return state, int(passes)


def validate_detector_marks(initial: InitialState) -> None:
    """Marks are admitted under the shared Detector admission, one mark per Node."""
    if type(initial.detectors) is not tuple or len(initial.detectors) > MAX_DETECTORS:
        raise ValueError("detectors exceed their fixed capacity")
    if not initial.detectors:
        return
    positions: set[Address3] = set()
    for mark in initial.detectors:
        if type(mark) is not DetectorMark:
            raise ValueError("detectors require DetectorMark entries")
        if any(c >= length for c, length in zip(mark.position, initial.shape, strict=True)):
            raise ValueError("a Detector mark position must be within shape")
        if mark.position in positions:
            raise ValueError("a Node carries one Detector mark")
        positions.add(mark.position)
    ray_fields = [definition for definition in initial.spatial_fields if definition.rays]
    if (
        initial.schema_version != 1
        or initial.link_ticks != 1
        or initial.node_execution
        or initial.spatial_computation_delay
        or not ray_fields
    ):
        raise ValueError(
            "Detector marks require schema 1, link_ticks 1, the default clock and a ray field"
        )
    for definition in ray_fields:
        headings = set(definition.headings)
        if (
            definition.euclidean
            or definition.pace_numerator != definition.pace_denominator
            or definition.decay is not None
            or any(sum(abs(c) for c in heading) != 1 for heading in definition.headings)
            or any(tuple(-c for c in heading) not in headings for heading in definition.headings)
        ):
            raise ValueError(
                "Detector marks require unpaced, undecayed ray fields with unit-axial "
                "headings closed under negation"
            )


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


# The external body (external-body-v1). Every rule here reads the body's own mark
# and the rays that arrived at its Node; nothing reads another Node.


def body_release(body: ExternalBody, definition: SpatialFieldDefinition, port: int = -1) -> Rays:
    """The field rays a body releases once per interval: one per Port heading, each
    the whole quanta of amount x n / d, with the body's declared phase, no event;
    booked as a source by the Node. In an interval the body steps through a Port,
    that heading is its own line ahead of it, which its ray occupies, and it
    releases nothing there (no self-field, Highlights 3.5). The amount enters no
    sum: the product is a Python integer and only the released ray amount is bounded."""
    amount = (body.amount * definition.release_numerator) // definition.release_denominator
    if amount <= 0:
        return ()
    skip = PORT_HEADINGS[port] if port >= 0 else None
    return _released(bounded(amount), body.phase & definition.phase_mask, definition, skip)


def body_absorb(
    body: ExternalBody, index: int, rays: Rays, definition: SpatialFieldDefinition
) -> ExternalBody:
    """The sink: the arriving rays of one family end in the body's exact counter for
    that family, and a field ray of a family the momentum table names changes the
    momentum by sign x amount x heading (-1 is attraction toward the source, which
    lies opposite the arriving heading). The body's content never changes."""
    sink = list(body.sink)
    momentum = list(body.momentum)
    sign = body.signs[index] if index < len(body.signs) else 0
    for ray in rays:
        sink[index] = checked_work(sink[index] + ray.amount)
        if sign:
            heading = definition.headings[ray.heading]
            for axis in range(3):
                momentum[axis] = checked_work(momentum[axis] + sign * ray.amount * heading[axis])
    return replace(body, sink=tuple(sink), momentum=(momentum[0], momentum[1], momentum[2]))


def body_step(body: ExternalBody) -> tuple[int, ExternalBody]:
    """One interval of the body's motion: each axis accumulator adds the momentum
    component, and the body steps one Link through the Port of the first axis
    (x before y before z) whose accumulator has reached a whole amount, subtracting
    the amount; at most one Link per interval, never faster than a ray. Returns
    the Port, or -1 when it stays, and the body with its new accumulators."""
    accumulators = [a + m for a, m in zip(body.accumulators, body.momentum, strict=True)]
    port = -1
    for axis in range(3):
        if accumulators[axis] >= body.amount:
            accumulators[axis] -= body.amount
            port = 2 * axis
            break
        if accumulators[axis] <= -body.amount:
            accumulators[axis] += body.amount
            port = 2 * axis + 1
            break
    for axis in range(3):
        # An accumulator only grows past the amount while the body waits its turn
        # on another axis; it is capped so the mark stays bounded metadata.
        if accumulators[axis] > 2 * body.amount:
            raise ValueError("an external body momentum exceeds its amount: faster than a ray")
        if accumulators[axis] < -2 * body.amount:
            raise ValueError("an external body momentum exceeds its amount: faster than a ray")
    return port, replace(body, accumulators=(accumulators[0], accumulators[1], accumulators[2]))


def body_coupled_families(body: ExternalBody, initial: InitialState) -> frozenset[int]:
    """The spatial fields the body's declared coupling rule meets: every role of the
    rule that does not select the body's family; empty for the sink."""
    if body.coupling == BODY_SINK:
        return frozenset()
    rule = initial.ray_interactions[body.coupling]
    return frozenset(kind for role in rule.participants for kind in role if kind != body.family)


def body_token(body: ExternalBody) -> Ray:
    """The body as the participant of its coupling rule that never changes: one
    quantum of its family at the Node, heading 0, no event; the Node strips the
    rule's unchanged output of it before anything leaves."""
    return Ray(0, (0, 0, 0), 1, phase=body.phase)


def validate_external_bodies(initial: InitialState) -> None:
    """The admission of external bodies (external-body-v1): the shared Detector
    admission, one body per Node, never on a Detector, a unit-axial links-metric
    ray family at pace 1, the family's released field when one is declared, a
    coupling that is the sink or a declared meeting with outputs in which one role
    selects the body's family alone and the body is returned unchanged."""
    if type(initial.external_bodies) is not tuple or len(initial.external_bodies) > MAX_EXTERNAL_BODIES:
        raise ValueError("external bodies exceed their fixed capacity")
    if not initial.external_bodies:
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
        or initial.spatial_couplings
    ):
        raise ValueError("an external body requires the default fixed H=1 spatial clock")
    positions = {mark.position for mark in initial.detectors}
    for expected, body in enumerate(initial.external_bodies):
        if type(body) is not ExternalBody:
            raise ValueError("external_bodies require ExternalBody entries")
        if body.index != expected:
            raise ValueError("external bodies are indexed in declaration order")
        if any(c >= length for c, length in zip(body.position, initial.shape, strict=True)):
            raise ValueError("an external body position must be within shape")
        if body.position in positions:
            raise ValueError("a Node carries one external body and no Detector mark beside it")
        positions.add(body.position)
        if body.family >= len(initial.spatial_fields) or body.field >= len(initial.spatial_fields):
            raise ValueError("an external body family must name a ray spatial field")
        family = initial.spatial_fields[body.family]
        if family.field_of is not None:
            raise ValueError("an external body holds a family, not a field")
        if (
            not family.rays
            or family.euclidean
            or family.pace_numerator != family.pace_denominator
            or family.decay is not None
            or any(sum(abs(c) for c in heading) != 1 for heading in family.headings)
            or any(heading not in family.headings for heading in PORT_HEADINGS)
        ):
            raise ValueError("an external body requires a unit-axial unpaced ray family")
        released = [i for i, d in enumerate(initial.spatial_fields) if d.field_of == body.family]
        if body.field != (released[0] if released else -1):
            raise ValueError("an external body radiates the released field of its family")
        if body.phase >= family.phase_modulus:
            raise ValueError("an external body phase must be below its family's phase width")
        if len(body.signs) != len(initial.spatial_fields) or len(body.sink) != len(
            initial.spatial_fields
        ):
            raise ValueError("an external body holds one sign and one sink counter per spatial field")
        if any(sign and not initial.spatial_fields[i].rays for i, sign in enumerate(body.signs)):
            raise ValueError("an external body momentum table names ray families")
        if body.coupling == BODY_SINK:
            continue
        if body.coupling >= len(initial.ray_interactions):
            raise ValueError("an external body coupling names a declared ray interaction")
        rule = initial.ray_interactions[body.coupling]
        own = [role for role in rule.participants if role == (body.family,)]
        if (
            not rule.outputs
            or len(own) != 1
            or any(body.family in role for role in rule.participants if role != (body.family,))
        ):
            raise ValueError(
                "an external body coupling is a meeting with outputs in which one role is the body"
            )
        if rule.outputs.count(body.family) != 1:
            raise ValueError("an external body coupling returns the body once, unchanged")


def external_body_names(initial: InitialState) -> list[dict[str, object]]:
    """The declared bodies for the run record, in declaration order."""
    return [
        {
            "index": body.index,
            "family": initial.fields[initial.spatial_fields[body.family].field].name,
            "amount": body.amount,
            "charge": body.charge,
            "field": (
                None if body.field < 0 else initial.fields[initial.spatial_fields[body.field].field].name
            ),
            "coupling": (
                "sink" if body.coupling == BODY_SINK else initial.ray_interactions[body.coupling].name
            ),
            "initial_position": list(body.position),
            "initial_momentum": list(body.momentum),
        }
        for body in initial.external_bodies
    ]
