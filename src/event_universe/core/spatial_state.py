"""Fixed local records for optional initialization-defined spatial fields."""

from dataclasses import dataclass

from .disturbance_state import (
    MAX_PORTS,
    Address3,
    Assignment,
    DisturbanceRecord,
    Expression,
    Invariant,
    Payload,
    Values,
    bounded,
    pack,
    unpack,
)

SpatialPopulations = tuple[Payload, ...]
SpatialOutgoing = tuple[SpatialPopulations, ...]
SpatialBundle = tuple[SpatialPopulations, ...]


def validate_port_count(port_count: int) -> None:
    """Reject invalid local channel capacity before allocating any port buffers."""
    if type(port_count) is not int or not 2 <= port_count <= MAX_PORTS:
        raise ValueError("spatial port count must be from 2 through 26")


@dataclass(frozen=True, slots=True)
class DecayDefinition:
    retain_numerator: int
    retain_denominator: int


@dataclass(frozen=True, slots=True)
class SpatialFieldDefinition:
    field: int
    baseline: Payload
    axis_weights: tuple[int, int, int] = (1, 1, 1)
    octant_weights: tuple[int, ...] = (1, 1, 1, 1, 1, 1, 1, 1)
    decay: DecayDefinition | None = None
    transport: str = "outward"


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


@dataclass(frozen=True, slots=True)
class SpatialInteractionDefinition:
    name: str
    type_index: int
    assignments: tuple[Assignment, ...]
    invariants: tuple[Invariant, ...]
    when: Expression | None = None
    types: tuple[int, ...] = ()


@dataclass(frozen=True, slots=True)
class FieldInteractionGuard:
    rule_index: int
    slot: int
    before: Values
    after: Values
    delta: Values


@dataclass(frozen=True, slots=True)
class EmissionDefinition:
    type_index: int
    spatial_field: int
    amount: Expression
    denominator: int = 1
    budget: Payload | None = None
    types: tuple[int, ...] = ()


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


@dataclass(frozen=True, slots=True)
class SpatialCouplingResult:
    records: tuple[DisturbanceRecord | None, ...]
    reaction: Values
    cost: int
    guards: tuple[FieldInteractionGuard, ...] = ()


@dataclass(frozen=True, slots=True)
class SpatialSeed:
    position: Address3
    spatial_field: int
    populations: SpatialPopulations


@dataclass(frozen=True, slots=True)
class SpatialState:
    """Eight owned populations/phases and a configured count of delivered samples.

    All entries use the ordinary positive payload coding, including phases.
    Delivered samples project already owned inventory and are never extra stock.
    """

    populations: SpatialPopulations
    allocation_phases: SpatialPopulations
    delivered: tuple[Payload, ...]

    def validate(self, components: int, port_count: int = 6) -> None:
        if components not in (1, 3):
            raise ValueError("spatial fields require one or three components")
        validate_port_count(port_count)
        for values, size in (
            (self.populations, 8),
            (self.allocation_phases, 8),
            (self.delivered, port_count),
        ):
            if len(values) != size:
                raise ValueError(
                    "spatial state requires eight octants and configured delivered channels"
                )
            for value in values:
                if len(value) != components:
                    raise ValueError("spatial state component count differs from the field")
                unpack(value)
        if any(value < 0 for payload in self.allocation_phases for value in unpack(payload)):
            raise ValueError("spatial allocation phases must be nonnegative")


@dataclass(slots=True)
class SpatialNode:
    states: tuple[SpatialState, ...]
    last_cost: int = 0
    received_count: int = 0
    reaction_phases: Values = ()
    sample_values: Values = ()
    sample_fluxes: Values = ()
    last_begin_tick: int = -1
    received_decay_cost: int = 0
    sample_ports: tuple[Values, ...] = ()


@dataclass(frozen=True, slots=True)
class SpatialPlan:
    states: tuple[SpatialState, ...]
    outgoing: tuple[SpatialBundle, ...]
    emission_records: tuple[DisturbanceRecord | None, ...]
    source_delta: Values
    cost: int
    rule_delta: Values = ()


@dataclass(frozen=True, slots=True)
class SpatialPacket:
    arrival_tick: int
    origin: Address3
    port: int
    fields: SpatialBundle


def zero_spatial_state(components: int, port_count: int = 6) -> SpatialState:
    bounded(components)
    if components not in (1, 3):
        raise ValueError("spatial fields require one or three components")
    validate_port_count(port_count)
    zero = pack((0,) * components)
    state = SpatialState((zero,) * 8, (zero,) * 8, (zero,) * port_count)
    state.validate(components, port_count)
    return state


# Historical import alias; spatial state has one node owner.
SpatialCell = SpatialNode
