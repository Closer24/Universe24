"""Fixed, domain-neutral schemas for initialization-defined disturbances."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, NamedTuple

from .sampling_contract import DETECTOR_ONLY, validate_spatial_sampling

if TYPE_CHECKING:
    from .conservation_state import ConservationDefinition
    from .node_conservation import NodeConservationDefinition
    from .source_emission_node import EmittingEnvelopeNode
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
# A declared bound of the N-to-M conversion contract: six input roles, six output
# families and one product departure per Port. The engine's transport itself
# admits several packets per Port; the bound is design, not a transport limit.
MAX_CONVERSION_ARITY = 6
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


def validate_codes(values: Payload) -> None:
    """Reject, in order, every component that decode would reject, without decoding."""
    for code in values:
        if type(code) is not int or not 1 <= code <= 2 * MAX_VALUE + 1:
            raise ValueError("invalid positive integer component code")


def any_negative(values: Payload) -> bool:
    """Among validated codes, an even code is a negative value; odd codes are not."""
    return any(code % 2 == 0 for code in values)


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
        validate_codes(values)
        if not self.signed and any_negative(values):
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
    # Declared output families of an N-to-M conversion, in output index order.
    outputs: tuple[int, ...] = ()


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
    # Self-excluding ray bookkeeping: (amount, cursor, wave phase, advance) per rule.
    # emission_last is this cycle's emission; emission_departed is the emission
    # of the cycle the record last left a Node, zero while it stays. After a move
    # the record subtracts the rays of that departure from the flux it samples.
    emission_last: Values = ()
    emission_departed: Values = ()
    # Kerengonen lottery capture: one local ticket state per absorb rule, advanced
    # on every draw from the record's own row and the ray it meets.
    absorb_tickets: Values = ()
    # Kerengonen carried phase: per absorb rule, the phase of the coherent sum of
    # what the record last absorbed, so a re-emission can continue the wave.
    absorbed_phases: Values = ()
    # Dissolution: per emission rule, the cycles this record has seen and the
    # stock it held when the rule first saw it, so a record can pay itself out
    # as rays on a schedule.
    dissolve_clocks: Values = ()
    # Claim and gather: per absorb rule, the train of the largest share the record
    # last absorbed, so a re-emission can keep the train a claim will gather.
    absorbed_trains: Values = ()
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
    ray_interactions: tuple[InteractionDefinition, ...] = ()
    conservation: ConservationDefinition | None = None
    node_execution: bool = False
    conservation_contract: NodeConservationDefinition | None = None

    spatial_computation_delay: bool = False
    field_phase_first: bool = False
    arrival_port_blind: bool = False
    allocation_phase: str = "straight"
    computation_field: int | None = None
    delay_direction: str | None = None
    least_delay_routing: bool = False
    # Rays resident at a Node wait the extra intervals its computation load alone
    # would add to a cycle (default clock); with ray_phase_per_tick a Kerengonen
    # ray's phase advances on every waiting interval as well as on every link.
    ray_delay: bool = False
    ray_phase_per_tick: bool = False
    # Host scheduling only; physical rules and their clocks do not read this flag.
    focus: bool = True
    sampling_profile: str = DETECTOR_ONLY

    def __post_init__(self) -> None:
        from .spatial_state import validate_ray_coupling

        validate_spatial_sampling(self.sampling_profile, self.spatial_fields)
        validate_ray_coupling(self)
        if self.node_execution and self.spatial_computation_delay:
            raise ValueError("node_execution and spatial_computation_delay select different clocks")
        for index, spatial_definition in enumerate(self.spatial_fields):
            if spatial_definition.self_exclusion and (
                self.ray_delay
                or spatial_definition.euclidean
                or spatial_definition.claims
                or spatial_definition.bonded
                or spatial_definition.pace_numerator != spatial_definition.pace_denominator
                or any(
                    rule.spatial_field == index and rule.mirror is not None for rule in self.emissions
                )
            ):
                raise ValueError(
                    "one-Link self-exclusion does not support paced, delayed, mirrored, claimed or bonded rays"
                )
        for name in ("ray_delay", "ray_phase_per_tick", "focus"):
            if type(getattr(self, name)) is not bool:
                raise ValueError(f"{name} must be boolean")
        if self.ray_delay:
            if self.computation_field is None:
                raise ValueError("ray_delay requires computation_field")
            if self.spatial_computation_delay or self.node_execution:
                raise ValueError("ray_delay requires the default clock")
            if not any(definition.rays for definition in self.spatial_fields):
                raise ValueError("ray_delay requires a ray spatial field")
        if self.ray_phase_per_tick:
            if not self.ray_delay:
                raise ValueError("ray_phase_per_tick requires ray_delay")
            if not any(definition.phase_steps for definition in self.spatial_fields):
                raise ValueError("ray_phase_per_tick requires a Kerengonen ray field")
        if type(self.least_delay_routing) is not bool:
            raise ValueError("least_delay_routing must be boolean")
        if self.least_delay_routing and self.delay_direction is None:
            raise ValueError("least_delay_routing requires delay_direction")
        if self.delay_direction is not None:
            if self.delay_direction not in ("along", "against"):
                raise ValueError("delay_direction must be along or against")
            if self.computation_field is None:
                raise ValueError("delay_direction requires computation_field")
            if self.spatial_computation_delay:
                raise ValueError("delay_direction requires the default clock")
        if type(self.spatial_computation_delay) is not bool:
            raise ValueError("spatial_computation_delay must be boolean")
        if self.allocation_phase not in ("straight", "rotate", "node"):
            raise ValueError("allocation_phase must be straight, rotate or node")
        if self.computation_field is not None:
            index = self.computation_field
            if type(index) is not int or not 0 <= index < len(self.fields):
                raise ValueError("computation_field must name a configured field")
            field = self.fields[index]
            definition = next((d for d in self.spatial_fields if d.field == index), None)
            if definition is None or definition.transport not in ("outward", "ray"):
                raise ValueError("computation_field must be an outward or ray spatial field")
            if field.components != 1 or field.signed or not field.conserved:
                raise ValueError("computation_field must be an unsigned conserved scalar field")
        if self.spatial_computation_delay and not self.spatial_fields:
            raise ValueError("spatial_computation_delay requires spatial fields")
        for name in ("field_phase_first", "arrival_port_blind"):
            if type(getattr(self, name)) is not bool:
                raise ValueError(f"{name} must be boolean")
            if not getattr(self, name):
                continue
            if not self.spatial_fields:
                raise ValueError(f"{name} requires spatial fields")
            if any(field.transport != "outward" for field in self.spatial_fields):
                raise ValueError(f"{name} requires outward spatial fields only")
            if self.spatial_computation_delay:
                raise ValueError(f"{name} cannot combine with spatial_computation_delay")
            if self.field_rules or self.spatial_interactions:
                raise ValueError(f"{name} cannot combine with field rules or spatial interactions")
        if self.field_phase_first and self.link_ticks != 1:
            raise ValueError("field_phase_first requires link_ticks 1")
        if self.field_phase_first and self.arrival_port_blind:
            raise ValueError(
                "field_phase_first and arrival_port_blind are alternative self-field policies"
            )


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
    interaction_ticks: int = 0
    resolution_token: int | None = None


@dataclass(frozen=True, slots=True)
class PendingCycle:
    ready_tick: int
    next_tick: int
    plan: LocalPlan
    # Extra ticks each departure spends before arrival under a directional delay.
    departure_delays: tuple[int, ...] = ()
    spatial_plan: SpatialPlan | None = None
    spatial_phases: Values = ()
    spatial_guard_states: tuple[SpatialState, ...] = ()


@dataclass(frozen=True, slots=True)
class Packet:
    arrival_tick: int
    origin: Address3
    port: int
    record: DisturbanceRecord


@dataclass(slots=True)
class DisturbanceNodeState:
    """Mutable disturbance-owned state at one Node."""

    records: tuple[DisturbanceRecord | None, ...]
    coupling_remainders: tuple[int, ...]
    pending: PendingCycle | None = None
    available_tick: int = 0
    received_count: int = 0
    last_cost: int = 0
    # Per slot: 0, or travel port + 1 of a record that arrived in the current interval.
    arrival_port_codes: tuple[int, ...] = ()
    source_envelope: EmittingEnvelopeNode | None = None


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
