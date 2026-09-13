"""Fixed, domain-neutral schemas for initialization-defined disturbances."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, NamedTuple

from .event_links import EventCursor, EventReferences

if TYPE_CHECKING:
    from .conservation_state import ConservationDefinition
    from .node_conservation import NodeConservationDefinition
    from .spatial_state import (
        EmissionDefinition,
        FieldGroupDefinition,
        FieldInteractionGuard,
        NodeFieldRuleDefinition,
        SpatialCouplingDefinition,
        SpatialFieldDefinition,
        SpatialInteractionDefinition,
        SpatialPlan,
        SpatialSeed,
        SpatialState,
    )

from .integer import checked_work

MAX_VALUE = 1_073_741_823
MAX_FIELDS = 16
MAX_TYPES = 16
MAX_SLOTS = 32
MAX_RULES = 32
MAX_EXPRESSION_NODES = 64
MAX_COMPONENTS = 32
AGGREGATIONS = frozenset(
    {"sum", "vector_sum", "keep_equal", "phase_bins", "interaction_state", "nonmergeable"}
)
OPERATIONS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
Payload = tuple[int, ...]
Values = tuple[Payload, ...]
Weights = tuple[int, int, int, int, int, int]
Address3 = tuple[int, int, int]


def bounded(value: int) -> int:
    if type(value) is not int or abs(value) > MAX_VALUE:
        raise ValueError("value exceeds the disturbance integer bound")
    return value


def encode(value: int) -> int:
    bounded(value)
    return 2 * value + 1 if value >= 0 else -2 * value


def decode(code: int) -> int:
    if type(code) is not int or not 1 <= code <= 2 * MAX_VALUE + 1:
        raise ValueError("invalid positive integer component code")
    return code // 2 if code % 2 else -(code // 2)


def pack(values: tuple[int, ...]) -> Payload:
    return tuple(encode(v) for v in values)


def unpack(values: Payload) -> tuple[int, ...]:
    return tuple(decode(v) for v in values)


@dataclass(frozen=True, slots=True)
class FieldDefinition:
    name: str
    components: int
    units: str
    signed: bool
    conserved: bool
    scale: int = 1
    extensive: bool = True
    aggregation: str | None = None

    def validate(self, values: Payload) -> None:
        if len(values) != self.components:
            raise ValueError(f"invalid component count for field {self.name}")
        decoded = unpack(values)
        if not self.signed and any(v < 0 for v in decoded):
            raise ValueError(f"negative value forbidden for field {self.name}")


@dataclass(frozen=True, slots=True)
class Expression:
    op: str
    arguments: tuple[Expression, ...] = ()
    literal: tuple[int, ...] = ()
    field: int = 0
    side: int = 0
    component: int = 0
    matrix: tuple[tuple[int, ...], ...] = ()
    port: int = 0


@dataclass(frozen=True, slots=True)
class UpdateRule:
    field: int
    expression: Expression
    source: bool = False


@dataclass(frozen=True, slots=True)
class TransportDefinition:
    mode: str
    weights: Weights = (1, 1, 1, 1, 1, 1)
    direction_field: int | None = None
    rate: Expression | None = None
    rate_denominator: int = 1
    routing: str = "cyclic"
    direction: Expression | None = None
    rate_divisor: Expression | None = None


@dataclass(frozen=True, slots=True)
class DisturbanceDefinition:
    name: str
    fields: tuple[int, ...]
    defaults: Values
    transport: TransportDefinition
    updates: tuple[UpdateRule, ...] = ()
    cost_field: int | None = None
    checks: tuple[Invariant, ...] = ()


@dataclass(frozen=True, slots=True)
class CouplingDefinition:
    name: str
    left_type: int
    right_type: int
    field: int
    amount: Expression
    denominator: int = 1
    remainder_owner: str = "pair"
    left_types: tuple[int, ...] = ()
    right_types: tuple[int, ...] = ()


@dataclass(frozen=True, slots=True)
class Assignment:
    side: int
    field: int
    expression: Expression


@dataclass(frozen=True, slots=True)
class Invariant:
    name: str
    expression: Expression


@dataclass(frozen=True, slots=True)
class InteractionDefinition:
    name: str
    left_type: int
    right_type: int
    assignments: tuple[Assignment, ...]
    invariants: tuple[Invariant, ...]
    when: Expression | None = None
    output_types: tuple[int, int] | None = None
    left_types: tuple[int, ...] = ()
    right_types: tuple[int, ...] = ()
    k: int = 0
    participants: tuple[tuple[int, ...], ...] = ()


@dataclass(frozen=True, slots=True)
class OperationCosts:
    prices: tuple[int, ...]

    def price(self, operation: str) -> int:
        return self.prices[OPERATIONS.index(operation)]


class CostMeter:
    """Count declared bounded model primitives, excluding accounting and host work."""

    def __init__(self, definitions: OperationCosts) -> None:
        self.definitions = definitions
        self.total = 0
        self.interaction_ticks = 0

    def charge(self, operation: str, count: int = 1) -> None:
        self.total = bounded(checked_work(self.total + self.definitions.price(operation) * count))

    def advance(self, ticks: int) -> None:
        """Reserve configured sequential rule duration independently of tariffs."""
        if bounded(ticks) < 0:
            raise ValueError("interaction duration must be nonnegative")
        self.interaction_ticks = bounded(checked_work(self.interaction_ticks + ticks))


@dataclass(frozen=True, slots=True)
class DisturbanceRecord:
    type_index: int
    values: Values
    phase_codes: Values
    route_phase_code: int = 1
    rate_remainder_code: int = 1
    channel_code: int = 1
    emission_remainders: Values = ()
    emission_phases: Values = ()
    exchange_remainders: Values = ()
    spatial_remainders: Values = ()
    emission_remaining: Values = ()
    spatial_remaining: Values = ()
    route_count_codes: tuple[int, ...] = (1, 1, 1, 1, 1, 1)
    route_weight_codes: tuple[int, ...] = (1, 1, 1, 1, 1, 1)
    rate_credit_denominator: int = 1


@dataclass(frozen=True, slots=True)
class Seed:
    position: Address3
    record: DisturbanceRecord


@dataclass(frozen=True, slots=True)
class InitialState:
    model_id: str
    shape: Address3
    slots_per_node: int
    link_ticks: int
    normal_budget: int
    ticks: int
    fields: tuple[FieldDefinition, ...]
    disturbances: tuple[DisturbanceDefinition, ...]
    couplings: tuple[CouplingDefinition, ...]
    operation_costs: OperationCosts
    seeds: tuple[Seed, ...]
    spatial_fields: tuple[SpatialFieldDefinition, ...] = ()
    emissions: tuple[EmissionDefinition, ...] = ()
    spatial_seeds: tuple[SpatialSeed, ...] = ()
    spatial_couplings: tuple[SpatialCouplingDefinition, ...] = ()
    schema_version: int = 1
    boundary: str = "periodic"
    interactions: tuple[InteractionDefinition, ...] = ()
    field_groups: tuple[FieldGroupDefinition, ...] = ()
    field_rules: tuple[NodeFieldRuleDefinition, ...] = ()
    spatial_interactions: tuple[SpatialInteractionDefinition, ...] = ()
    event_program: str | None = None
    conservation: ConservationDefinition | None = None
    node_execution: bool = False
    conservation_contract: NodeConservationDefinition | None = None

    spatial_computation_delay: bool = False

    def __post_init__(self) -> None:
        if self.node_execution and self.spatial_computation_delay:
            raise ValueError("node_execution and spatial_computation_delay select different clocks")
        if type(self.spatial_computation_delay) is not bool:
            raise ValueError("spatial_computation_delay must be boolean")
        if self.spatial_computation_delay and not self.spatial_fields:
            raise ValueError("spatial_computation_delay requires spatial fields")


class Departure(NamedTuple):
    port: int
    record: DisturbanceRecord
    origin_slot: int = -1


@dataclass(frozen=True, slots=True)
class LocalPlan:
    replacements: tuple[tuple[int, DisturbanceRecord | None], ...]
    departures: tuple[Departure, ...]
    coupling_remainders: tuple[int, ...]
    source_delta: Values
    cost: int
    spatial_reaction: Values = ()
    spatial_guards: tuple[FieldInteractionGuard, ...] = ()
    cause_id: int | None = None
    interaction_ticks: int = 0


@dataclass(frozen=True, slots=True)
class PendingCycle:
    ready_tick: int
    next_tick: int
    plan: LocalPlan
    cause_id: int | None = None
    spatial_plan: SpatialPlan | None = None
    spatial_phases: Values = ()
    spatial_guard_states: tuple[SpatialState, ...] = ()


@dataclass(frozen=True, slots=True)
class Packet:
    arrival_tick: int
    origin: Address3
    port: int
    record: DisturbanceRecord
    cause_id: int | None = None


@dataclass(slots=True)
class DisturbanceNodeState:
    """Mutable disturbance-owned state at one Node."""

    records: tuple[DisturbanceRecord | None, ...]
    coupling_remainders: tuple[int, ...]
    pending: PendingCycle | None = None
    available_tick: int = 0
    received_count: int = 0
    last_cost: int = 0
    cause_id: int | None = None
    event_cursors: tuple[EventCursor, ...] = ()
    event_references: EventReferences | None = None


@dataclass(frozen=True, slots=True)
class NodeView:
    """Immutable public view of one Node's disturbance-owned state."""

    records: tuple[DisturbanceRecord | None, ...]
    coupling_remainders: tuple[int, ...]
    pending: PendingCycle | None
    available_tick: int
    received_count: int
    last_cost: int
    arrival_mask: tuple[int, ...] = ()
    delay_counts: tuple[int, ...] = ()
    committed_cost: int = 0
    event_heads: tuple[tuple[int, int | None], ...] = ()
    event_origins: tuple[int, ...] = ()
