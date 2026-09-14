"""A bounded Node owns spatial transitions and its own field output bank."""

from collections.abc import Callable, Generator, Mapping
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Protocol

from .coupling_selectors import matches_type, selected_type_set
from .disturbance_state import (
    Address3,
    CostMeter,
    DisturbanceRecord,
    InitialState,
    Values,
    bounded,
    pack,
    unpack,
)
from .integer import add_components, checked_work, subtract_components
from .node_boundary import (
    validate_decay,
    validate_reaction_state,
    validate_samples,
    validate_spatial_bundle,
    validate_spatial_outgoing,
    validate_spatial_plan,
)
from .node_conservation import LocalInventory, NodeConservationGuard
from .node_execution import (
    PlanningCycle,
    PlanningRequest,
    PlanningResult,
    SpatialPlanningInput,
    finish_local_cycle,
)
from .node_ports import PortBank
from .node_services import NodeEvents, add_audit_delta, port_count
from .spatial_state import (
    FieldInteractionGuard,
    Rays,
    SpatialBundle,
    SpatialCouplingResult,
    SpatialNodeState,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
    attenuate_rays,
    merge_rays,
    ray_stock,
    validate_rays,
    zero_spatial_state,
)
from .topology import neighbor_address

if TYPE_CHECKING:
    from .disturbance_node import DisturbanceNode

SpatialPlanner = Callable[
    [
        tuple[SpatialState, ...],
        tuple[DisturbanceRecord | None, ...],
        int,
        int,
        tuple[Rays, ...],
    ],
    SpatialPlan,
]
SpatialDecayer = Callable[[SpatialBundle], tuple[SpatialBundle, Values, int]]
SpatialFieldGuard = Callable[[tuple[SpatialState, ...], SpatialPlan], None]


class SpatialCoupler(Protocol):
    def sample(self, states: tuple[SpatialState, ...]) -> Values: ...

    def sample_fluxes(self, states: tuple[SpatialState, ...]) -> Values: ...

    def sample_ports(self, states: tuple[SpatialState, ...]) -> tuple[Values, ...]: ...

    def sample_received_masks(self, states: tuple[SpatialState, ...]) -> tuple[int, ...]: ...

    def __call__(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        sample: Values,
        fluxes: Values = (),
        ports: tuple[Values, ...] = (),
        received_masks: tuple[int, ...] = (),
        *,
        slot_samples: Mapping[int, Values] | None = None,
        slot_fluxes: Mapping[int, Values] | None = None,
    ) -> SpatialCouplingResult: ...

    def validate_guards(
        self,
        states: tuple[SpatialState, ...],
        reaction: Values,
        guards: tuple[FieldInteractionGuard, ...],
    ) -> None: ...

    def deposit(
        self, states: tuple[SpatialState, ...], phases: Values, reaction: Values
    ) -> tuple[tuple[SpatialState, ...], Values]: ...

    def forward_reaction(
        self, states: tuple[SpatialState, ...], phases: Values, reaction: Values
    ) -> tuple[tuple[SpatialState, ...], Values, tuple[SpatialBundle, ...]]: ...


@dataclass(frozen=True, slots=True)
class ReactionCommit:
    states: tuple[SpatialState, ...]
    phases: Values
    links: tuple[SpatialPacket | None, ...] | None


@dataclass(frozen=True, slots=True)
class PendingSpatialCycle:
    """Frozen proposal; its originals remain in the Node's actual inventory."""

    ready_tick: int
    before: tuple[SpatialState, ...]
    plan: SpatialPlan
    cost: int
    cause_id: int | None = None


class NodeActivity:
    """Write-only scheduling notice; no physical state can be retrieved here."""

    def __init__(self, active: set[Address3]) -> None:
        self.__active = active

    def mark(self, position: Address3, active: bool) -> None:
        if active:
            self.__active.add(position)
        else:
            self.__active.discard(position)


@dataclass(frozen=True, slots=True)
class SpatialServices:
    initial: InitialState
    planner: SpatialPlanner
    events: NodeEvents
    coupler: SpatialCoupler | None
    decayer: SpatialDecayer | None
    activity: NodeActivity
    accounting: SpatialAccounting
    balance_guard: NodeConservationGuard | None = None
    field_guard: SpatialFieldGuard | None = None
    node_merge_cost: int = 0

    def __post_init__(self) -> None:
        if self.initial.node_execution and (
            self.initial.conservation_contract is None or self.balance_guard is None
        ):
            raise ValueError("node_execution requires a conservation contract and balance guard")
        if self.initial.node_execution and self.initial.field_rules and self.field_guard is None:
            raise ValueError("node_execution field rules require a field commit guard")

    def validate_field_guards(self, states: tuple[SpatialState, ...], plan: SpatialPlan) -> None:
        if not self.initial.node_execution:
            return
        if self.field_guard is None:
            if plan.field_guards:
                raise ValueError("field rule metadata requires a field commit guard")
            return
        self.field_guard(states, plan)


class SpatialAccounting:
    """Only local deltas can be submitted; global stock cannot be read by a node."""

    def __init__(
        self,
        sources: list[list[int]],
        dissipation: list[list[int]],
        reactions: list[list[int]],
        transformations: list[list[int]],
        localized: list[list[int]] | None = None,
    ) -> None:
        self.__sources, self.__dissipation = sources, dissipation
        self.__reactions, self.__transformations = reactions, transformations
        self.__localized = [] if localized is None else localized

    def record_sources(self, values: Values) -> None:
        add_audit_delta(self.__sources, values)

    def record_dissipation(self, values: Values) -> None:
        add_audit_delta(self.__dissipation, values)

    def record_localized(self, values: Values) -> None:
        """Deposits stay owned stock; this ledger only avoids scanning idle Nodes."""
        add_audit_delta(self.__localized, values)

    def record_reactions(self, values: Values) -> None:
        add_audit_delta(self.__reactions, values)

    def record_transformations(self, values: Values) -> None:
        add_audit_delta(self.__transformations, values)


@dataclass(slots=True)
class SpatialNode(SpatialNodeState):
    """A local field lane with no access to another Node's physical state."""

    position: Address3 = (0, 0, 0)
    output: PortBank[SpatialPacket] = field(default_factory=lambda: PortBank(()), compare=False)
    arrival_mask: tuple[int, ...] = ()
    delay_counts: tuple[int, ...] = ()
    pending: PendingSpatialCycle | None = None
    completed_tick: int = -1

    def _event(
        self,
        event: str,
        tick: int,
        services: SpatialServices,
        *,
        causes: tuple[int | None, ...] = (),
        notifications: list[dict[str, object]] | None = None,
        **details: object,
    ) -> int | None:
        identity, message = services.events.record(
            event,
            tick,
            self.position,
            None,
            causes=tuple(dict.fromkeys(c for c in causes if c is not None)),
            owner="spatial",
            event_cost=0,
            **details,
        )
        if notifications is None:
            services.events.publish(message)
        else:
            notifications.append(message)
        return identity

    def catch_up_idle(self, tick: int) -> None:
        self.last_begin_tick = tick

    def _sampled_states(self, services: SpatialServices) -> tuple[SpatialState, ...]:
        """Resident ray stock is local value for a carrier reading a ray field."""
        if not any(self.rays):
            return self.states
        result = []
        for index, (definition, state) in enumerate(
            zip(services.initial.spatial_fields, self.states, strict=True)
        ):
            if definition.rays and index < len(self.rays) and self.rays[index]:
                populations = (pack((ray_stock(self.rays[index]),)),) + state.populations[1:]
                result.append(replace(state, populations=populations))
            else:
                result.append(state)
        return tuple(result)

    def advance(self, tick: int, carrier: DisturbanceNode | None, services: SpatialServices) -> None:
        finish_local_cycle(self.plan_cycle(tick, carrier, services), None, services.planner)

    def plan_cycle(
        self, tick: int, carrier: DisturbanceNode | None, services: SpatialServices
    ) -> PlanningCycle:
        if bounded(tick) < 0:
            raise ValueError("node clock must be nonnegative")
        if carrier is not None and carrier.position != self.position:
            raise ValueError("carrier and spatial components must belong to the same Node")
        if services.initial.node_execution:
            if self.pending is not None:
                yield None
                self.commit_ready(tick, carrier, services)
                return
            # A completed field cycle gives the colocated carrier one turn before
            # another field cycle can reserve those local inputs.
            if self.completed_tick == tick or (carrier is not None and carrier.pending is not None):
                return
        if tick % services.initial.link_ticks:
            return
        coupled_types = selected_type_set(
            services.initial.spatial_couplings, services.initial.spatial_interactions
        )
        if any(packet is not None for packet in self.output.packets):
            raise ValueError("outgoing spatial links are occupied")
        records = () if carrier is None else carrier.records
        if services.initial.computation_field is not None:
            # Stock present before forwarding is this interval's local computation load;
            # for a ray field that stock is the resident rays, delivered per travel port.
            index = self._computation_index(services)
            self.load = self._resident_load(index)
            self.load_channels = tuple(unpack(payload)[0] for payload in self.states[index].delivered)
        sample_values, sample_fluxes, sample_ports = (
            self.sample_values,
            self.sample_fluxes,
            self.sample_ports,
        )
        sample_cause = self.sample_cause_id
        sample_received_masks = self.sample_received_masks
        if (
            services.coupler is not None
            and not services.initial.field_phase_first
            and any(record is not None and record.type_index in coupled_types for record in records)
        ):
            # Freeze only locally delivered input, before fresh source injection.
            sample_values = services.coupler.sample(self._sampled_states(services))
            sample_fluxes = services.coupler.sample_fluxes(self.states)
            sample_cause = self.cause_id
            if services.initial.arrival_port_blind:
                self.sample_delivered = tuple(state.delivered for state in self.states)
            if services.initial.spatial_interactions:
                sample_ports = services.coupler.sample_ports(self.states)
                sample_received_masks = services.coupler.sample_received_masks(self.states)
            validate_samples(services.initial, sample_values, sample_fluxes, sample_ports)
        # Samples describe only the preceding delivery interval, never a permanent trail.
        states = (
            self.states
            if services.initial.field_rules
            else tuple(
                replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6, received_mask=0)
                for state in self.states
            )
        )
        active_source = any(
            record is not None
            and matches_type(rule, record.type_index)
            and (
                rule.budget is None
                or not record.emission_remaining
                or any(unpack(record.emission_remaining[index]))
            )
            for record in records
            for index, rule in enumerate(services.initial.emissions)
        )
        active_field = any(
            any(unpack(payload)) for state in states for payload in state.populations
        ) or any(self.rays)
        if not active_source and not active_field and self.received_count == 0:
            self.states = tuple(
                replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6, received_mask=0)
                for state in states
            )
            self.last_cost = 0
            self.cost_cause_id = None
            self.sample_values, self.sample_fluxes, self.sample_ports = (
                sample_values,
                sample_fluxes,
                sample_ports,
            )
            self.sample_cause_id = sample_cause
            self.sample_received_masks = sample_received_masks
            self.last_begin_tick = tick
            services.activity.mark(self.position, False)
            return
        # This is the previous completed colocated carrier cycle, never pending
        # work or a register carried here from another Node.
        node_cost = 0 if carrier is None else carrier.committed_cost
        plan = yield SpatialPlanningInput(states, records, self.received_count, node_cost, self.rays)
        if not isinstance(plan, SpatialPlan):
            raise ValueError("spatial planning requires a SpatialPlan")
        validate_spatial_plan(services.initial, plan, len(records), records)
        services.validate_field_guards(self.states, plan)
        cost = bounded(checked_work(plan.cost + self.received_decay_cost))
        if services.initial.node_execution and plan.interaction_ticks:
            ready_tick = bounded(tick + plan.interaction_ticks)
            services.events.require_room(1)
            self.pending = PendingSpatialCycle(ready_tick, self.states, plan, cost)
            # Samples received during the wait have an independent fixed window.
            # Clearing these views does not remove any owned physical inventory.
            self.states = tuple(
                replace(
                    state,
                    delivered=(pack((0,) * len(state.populations[0])),) * port_count(services.initial),
                    received_mask=0,
                )
                for state in self.states
            )
            self.arrival_mask = (0,) * port_count(services.initial)
            self.received_count = 0
            self.received_decay_cost = 0
            self.last_cost = cost
            self.delay_counts = (plan.interaction_ticks,) * port_count(services.initial)
            cause = self._event(
                "spatial_cycle_started",
                tick,
                services,
                causes=(self.cause_id, None if carrier is None else carrier.cause_id),
                ready_tick=ready_tick,
                interaction_ticks=plan.interaction_ticks,
                cost=cost,
            )
            self.pending = replace(self.pending, cause_id=cause)
            services.activity.mark(self.position, True)
            return
        self.sample_values, self.sample_fluxes, self.sample_ports = (
            sample_values,
            sample_fluxes,
            sample_ports,
        )
        self.sample_cause_id = sample_cause
        self.sample_received_masks = sample_received_masks
        self._commit_plan(tick, carrier, services, plan, cost)

    def commit_ready(
        self, tick: int, carrier: DisturbanceNode | None, services: SpatialServices
    ) -> None:
        """Finish only due work; a clock notice cannot begin another local cycle."""
        pending = self.pending
        remaining = 0 if pending is None else max(0, pending.ready_tick - tick)
        self.delay_counts = (remaining // services.initial.link_ticks,) * port_count(services.initial)
        if pending is None or pending.ready_tick > tick:
            return
        states = []
        for current, original, proposed in zip(
            self.states, pending.before, pending.plan.states, strict=True
        ):
            populations = tuple(
                pack(
                    tuple(
                        checked_work(now + checked_work(new - old))
                        for now, old, new in zip(
                            unpack(live), unpack(before), unpack(after), strict=True
                        )
                    )
                )
                for live, before, after in zip(
                    current.populations, original.populations, proposed.populations, strict=True
                )
            )
            states.append(
                replace(current, populations=populations, allocation_phases=proposed.allocation_phases)
            )
        records = () if carrier is None else carrier.records
        plan = replace(pending.plan, states=tuple(states), emission_records=records)
        validate_spatial_plan(services.initial, plan, len(records), records)
        services.validate_field_guards(self.states, plan)
        self._commit_plan(tick, carrier, services, plan, pending.cost, pending_cause=pending.cause_id)

    def _commit_plan(
        self,
        tick: int,
        carrier: DisturbanceNode | None,
        services: SpatialServices,
        plan: SpatialPlan,
        cost: int,
        *,
        pending_cause: int | None = None,
    ) -> None:
        """Commit all proposed local owners before publishing any observation."""
        records = () if carrier is None else carrier.records
        packets: list[SpatialPacket | None] = [None] * 6
        # Field-phase-first packets complete their link inside the departure interval.
        arrival = bounded(tick + services.initial.link_ticks - int(services.initial.field_phase_first))
        for port, bundle in enumerate(plan.outgoing):
            port_rays = plan.rays[port] if plan.rays else ()
            if any(any(unpack(payload)) for field in bundle for payload in field) or any(port_rays):
                packets[port] = SpatialPacket(
                    arrival,
                    self.position,
                    port,
                    bundle,
                    rays=port_rays if any(port_rays) else (),
                    phases=plan.outgoing_phases[port] if plan.outgoing_phases else (),
                )
        # All physical calculations and validation precede the local commit.
        if services.balance_guard is not None:
            services.balance_guard.check(
                LocalInventory(
                    records=records, spatial=tuple(state.populations for state in self.states)
                ),
                LocalInventory(
                    records=plan.emission_records,
                    spatial=tuple(state.populations for state in plan.states),
                    spatial_packets=tuple(packet.fields for packet in packets if packet is not None),
                ),
                "spatial interaction commit",
            )
        if services.events.enabled:
            services.events.require_room(1 + sum(p is not None for p in packets))
        carrier_cause = None if carrier is None else carrier.cause_id
        if carrier is None:
            if plan.emission_records:
                raise ValueError("spatial emission cannot create disturbance records")
        else:
            carrier.accept_emission(plan.emission_records)
        self.states = plan.states
        if self.rays:
            # Every resident ray left on this cycle along its own line.
            self.rays = tuple(() for _ in self.rays)
        self.last_cost = cost
        if self.pending is None:
            self.arrival_mask = (0,) * port_count(services.initial)
            self.received_count = 0
            self.received_decay_cost = 0
            self.delay_counts = (0,) * port_count(services.initial)
        else:
            self.pending = None
            self.completed_tick = tick
            self.delay_counts = (0,) * port_count(services.initial)
        self.last_begin_tick = tick
        self.output.publish(tuple(packets))
        # One following phase clears the reported cost before becoming idle.
        services.activity.mark(self.position, True)
        services.accounting.record_sources(plan.source_delta)
        services.accounting.record_transformations(plan.rule_delta)
        notifications: list[dict[str, object]] = []
        cause = self._event(
            "spatial_cycle",
            tick,
            services,
            causes=(self.cause_id, carrier_cause, pending_cause),
            notifications=notifications,
            cost=cost,
            source_delta={
                field.name: plan.source_delta[i]
                for i, field in enumerate(services.initial.fields)
                if any(plan.source_delta[i])
            },
            **(
                {
                    "rule_delta": {
                        field.name: plan.rule_delta[i]
                        for i, field in enumerate(services.initial.fields)
                        if any(plan.rule_delta[i])
                    }
                }
                if plan.rule_delta
                else {}
            ),
        )
        self.cause_id = self.cost_cause_id = cause
        if cause is not None and carrier is not None and plan.emission_records != records:
            carrier.cause_id = cause
        for index, packet in enumerate(packets):
            if packet is not None:
                sent = self._event(
                    "spatial_sent",
                    tick,
                    services,
                    causes=(cause,),
                    notifications=notifications,
                    port=packet.port,
                    arrival_tick=packet.arrival_tick,
                )
                if sent is not None:
                    packets[index] = replace(packet, cause_id=sent)
        self.output.publish(tuple(packets))
        for message in notifications:
            services.events.publish(message)

    def cycle_causes(self, tick: int, services: SpatialServices, *, sampled: bool) -> tuple[int, ...]:
        """IDs of the exact frozen sample and current cost consumed by a carrier."""
        causes = (
            self.sample_cause_id if sampled else None,
            self.cost_cause_id if tick % services.initial.link_ticks == 0 else None,
        )
        return tuple(dict.fromkeys(c for c in causes if c is not None))

    def reaction_causes(self, *, outgoing: bool) -> tuple[int, ...]:
        """Bounded owners read by a joint commit, including departure amendments."""
        causes = (self.cause_id,) + (
            tuple(p.cause_id for p in self.output.packets if p is not None) if outgoing else ()
        )
        return tuple(dict.fromkeys(c for c in causes if c is not None))

    def link_reaction(self, proposal: ReactionCommit | None, cause: int) -> None:
        """The joint event owns the new stock and any amended departure bundle."""
        if proposal is None:
            return
        self.cause_id = cause
        if proposal.links is not None:
            self.output.publish(
                tuple(None if p is None else replace(p, cause_id=cause) for p in proposal.links)
            )

    def couple(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        services: SpatialServices,
        tick: int,
        blind_ports: Mapping[int, int] | None = None,
    ) -> SpatialCouplingResult:
        if services.coupler is None:
            raise ValueError("spatial coupling requires an explicitly composed law")
        if blind_ports:
            slot_samples, slot_fluxes = self.blind_samples(records, blind_ports, services)
            return services.coupler(
                records,
                self.sample_values,
                self.sample_fluxes,
                self.sample_ports,
                self.sample_received_masks,
                slot_samples=slot_samples,
                slot_fluxes=slot_fluxes,
            )
        if services.initial.node_execution:
            if self.pending is not None:
                raise ValueError("pending field inputs are reserved by their local interaction")
            if self.last_begin_tick != tick or self.completed_tick == tick:
                self.sample_values = services.coupler.sample(self.states)
                self.sample_fluxes = services.coupler.sample_fluxes(self.states)
                self.sample_ports = services.coupler.sample_ports(self.states)
                self.sample_received_masks = services.coupler.sample_received_masks(self.states)
                self.sample_cause_id = self.cause_id
            validate_samples(services.initial, self.sample_values, self.sample_fluxes, self.sample_ports)
        return services.coupler(
            records,
            self.sample_values,
            self.sample_fluxes,
            self.sample_ports,
            self.sample_received_masks,
        )

    def consume_sample(self) -> None:
        """Consume causal input views after their carrier proposal has been accepted."""
        self.states = tuple(
            replace(
                state,
                delivered=(pack((0,) * len(state.populations[0])),) * len(state.delivered),
                received_mask=0,
            )
            for state in self.states
        )
        self.sample_received_masks = (0,) * len(self.sample_received_masks)
        self.arrival_mask = (0,) * len(self.arrival_mask)

    def plan_shared_fields(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        services: SpatialServices,
        node_cost: int = 0,
    ) -> Generator[PlanningRequest, PlanningResult, SpatialPlan]:
        """Prepare a bounded field proposal without changing any physical owner."""
        active_source = any(
            record is not None
            and matches_type(rule, record.type_index)
            and (
                rule.budget is None
                or not record.emission_remaining
                or any(unpack(record.emission_remaining[index]))
            )
            for record in records
            for index, rule in enumerate(services.initial.emissions)
        )
        active = (
            active_source
            or self.received_count
            or any(any(unpack(payload)) for state in self.states for payload in state.populations)
        )
        states = (
            self.states
            if services.initial.field_rules
            else tuple(
                replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6)
                for state in self.states
            )
        )
        if active:
            plan = yield SpatialPlanningInput(states, records, self.received_count, node_cost)
            if not isinstance(plan, SpatialPlan):
                raise ValueError("spatial planning requires a SpatialPlan")
            validate_spatial_plan(services.initial, plan, len(records), records)
            return replace(plan, cost=bounded(checked_work(plan.cost + self.received_decay_cost)))
        blank = tuple(
            state.populations
            for state in tuple(
                zero_spatial_state(services.initial.fields[d.field].components)
                for d in services.initial.spatial_fields
            )
        )
        zero = tuple((0,) * field.components for field in services.initial.fields)
        yield None
        return SpatialPlan(states, (blank,) * 6, records, zero, 0)

    def node_coupling(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        services: SpatialServices,
    ) -> SpatialCouplingResult:
        """Sample only the owned pre-cycle field; no fresh emission or late input."""
        assert services.coupler is not None
        states = self.states
        return services.coupler(
            records,
            services.coupler.sample(states),
            services.coupler.sample_fluxes(states),
            services.coupler.sample_ports(states) if services.initial.spatial_interactions else (),
        )

    def packets(
        self,
        tick: int,
        outgoing: tuple[SpatialBundle, ...],
        services: SpatialServices,
        outgoing_phases: tuple[SpatialBundle, ...] = (),
    ) -> tuple[SpatialPacket | None, ...]:
        if len(outgoing) != 6:
            raise ValueError("spatial output requires exactly six bounded ports")
        arrival = bounded(checked_work(tick + services.initial.link_ticks))
        return tuple(
            SpatialPacket(
                arrival,
                self.position,
                port,
                bundle,
                phases=outgoing_phases[port] if outgoing_phases else (),
            )
            if any(any(unpack(payload)) for field in bundle for payload in field)
            else None
            for port, bundle in enumerate(outgoing)
        )

    def node_states(self, plan: SpatialPlan, services: SpatialServices) -> tuple[SpatialState, ...]:
        """Merge completed later inputs only after the frozen transformation."""
        incoming = self.incoming or tuple(
            zero_spatial_state(services.initial.fields[d.field].components)
            for d in services.initial.spatial_fields
        )
        states = []
        for definition, state, later in zip(
            services.initial.spatial_fields, plan.states, incoming, strict=True
        ):
            field = services.initial.fields[definition.field]
            populations = tuple(
                pack(add_components(unpack(before), unpack(added)))
                for before, added in zip(state.populations, later.populations, strict=True)
            )
            for payload in populations:
                field.validate(payload)
            value = list(unpack(definition.baseline))
            for payload in populations:
                for index, component in enumerate(unpack(payload)):
                    value[index] = checked_work(value[index] + component)
            field.validate(pack(tuple(value)))
            states.append(SpatialState(populations, state.allocation_phases, later.delivered))
        return tuple(states)

    def commit_node(
        self,
        tick: int,
        plan: SpatialPlan,
        states: tuple[SpatialState, ...],
        phases: Values,
        packets: tuple[SpatialPacket | None, ...],
        reaction: Values,
        services: SpatialServices,
    ) -> None:
        """Install already validated field ownership together with its carrier owner."""
        self.states, self.reaction_phases = states, phases
        self.received_count, self.received_decay_cost = self.incoming_count, self.incoming_decay_cost
        self.incoming, self.incoming_count, self.incoming_decay_cost = (), 0, 0
        self.shared_pending = 0
        self.last_cost, self.last_begin_tick = plan.cost, tick
        self.output.publish(packets)
        services.activity.mark(self.position, True)
        services.accounting.record_sources(plan.source_delta)
        services.accounting.record_transformations(plan.rule_delta)
        services.accounting.record_reactions(reaction)

    def validate_guards(
        self, services: SpatialServices, reaction: Values, guards: tuple[FieldInteractionGuard, ...]
    ) -> None:
        if guards:
            if services.coupler is None:
                raise ValueError("spatial interaction guards require a configured response law")
            services.coupler.validate_guards(self.states, reaction, guards)

    def prepare_reaction(
        self, tick: int, reaction: Values, services: SpatialServices, *, plan: SpatialPlan | None = None
    ) -> ReactionCommit | None:
        if not reaction or not any(any(payload) for payload in reaction):
            return None
        if services.coupler is None:
            raise ValueError("a spatial reaction requires its configured coupling law")
        if plan is None and self.last_begin_tick != tick:
            states, phases = services.coupler.deposit(self.states, self.reaction_phases, reaction)
            validate_reaction_state(services.initial, states, phases)
            return ReactionCommit(states, phases, None)
        # Only this instant's departure buffers are still locally appendable.
        # Packets from an earlier departure are immutable while in transit.
        old_links = (
            self.output.packets
            if plan is None
            else self.packets(tick, plan.outgoing, services, plan.outgoing_phases)
        )
        arrival = bounded(tick + services.initial.link_ticks)
        if any(packet is not None and packet.arrival_tick != arrival for packet in old_links):
            raise ValueError("reaction cannot alter a spatial packet already in transit")
        states, phases, outgoing = services.coupler.forward_reaction(
            self.states if plan is None else plan.states, self.reaction_phases, reaction
        )
        validate_reaction_state(services.initial, states, phases)
        validate_spatial_outgoing(services.initial, outgoing)
        links: list[SpatialPacket | None] = []
        for port, (old, bundle) in enumerate(zip(old_links, outgoing, strict=True)):
            merged = []
            for index, (definition, populations) in enumerate(
                zip(services.initial.spatial_fields, bundle, strict=True)
            ):
                field = services.initial.fields[definition.field]
                previous = (pack((0,) * field.components),) * 8 if old is None else old.fields[index]
                if not any(reaction[definition.field]):
                    merged.append(previous)
                    continue
                combined = []
                for before, added in zip(previous, populations, strict=True):
                    payload = pack(add_components(unpack(before), unpack(added)))
                    field.validate(payload)
                    combined.append(payload)
                merged.append(tuple(combined))
            values = tuple(merged)
            links.append(
                # A reaction appended to a departing packet keeps that packet's carried phases.
                SpatialPacket(
                    arrival, self.position, port, values, phases=() if old is None else old.phases
                )
                if any(any(unpack(payload)) for field in values for payload in field)
                else None
            )
        return ReactionCommit(states, phases, tuple(links))

    def commit_reaction(
        self, proposal: ReactionCommit | None, reaction: Values, services: SpatialServices
    ) -> None:
        if proposal is None:
            return
        self.states = proposal.states
        self.reaction_phases = proposal.phases
        services.activity.mark(self.position, True)
        if proposal.links is not None:
            self.output.publish(proposal.links)
        services.accounting.record_reactions(reaction)

    def cost(self, tick: int, services: SpatialServices) -> int:
        # Under a directional delay the load prices departures, not the whole cycle.
        load = 0 if services.initial.delay_direction is not None else self.load_value(services)
        if tick % services.initial.link_ticks:
            return load
        return bounded(checked_work(self.last_cost + load))

    @staticmethod
    def _computation_index(services: SpatialServices) -> int:
        index = services.initial.computation_field
        return next(i for i, d in enumerate(services.initial.spatial_fields) if d.field == index)

    @staticmethod
    def _baseline_load(services: SpatialServices) -> int:
        if services.initial.computation_field is None:
            return 0
        definition = services.initial.spatial_fields[SpatialNode._computation_index(services)]
        return unpack(definition.baseline)[0]

    def load_value(self, services: SpatialServices) -> int:
        """Local value of the configured computation field: baseline plus stock present this interval."""
        if services.initial.computation_field is None:
            return 0
        return bounded(checked_work(self._baseline_load(services) + self.load))

    def _resident_load(self, index: int) -> int:
        stock = sum(unpack(payload)[0] for payload in self.states[index].populations)
        if self.rays and index < len(self.rays) and self.rays[index]:
            stock = checked_work(stock + ray_stock(self.rays[index]))
        return stock

    def refresh_load(self, services: SpatialServices) -> int:
        """Read the computation stock owned now, for the shared clock's field forwarding."""
        if services.initial.computation_field is None:
            return 0
        self.load = self._resident_load(self._computation_index(services))
        return self.load_value(services)

    def directional_load(self, port: int, services: SpatialServices) -> int:
        """Load pricing a departure through `port`: field travelling along it, or against it."""
        if services.initial.computation_field is None or services.initial.delay_direction is None:
            return 0
        channel = port if services.initial.delay_direction == "along" else port ^ 1
        return bounded(checked_work(self._baseline_load(services) + self.load_channels[channel]))

    def freeze_sample(self, services: SpatialServices) -> None:
        """Freeze coupled samples after this interval's field phase has delivered."""
        assert services.coupler is not None
        self.sample_values = services.coupler.sample(self._sampled_states(services))
        self.sample_fluxes = services.coupler.sample_fluxes(self.states)
        if services.initial.spatial_interactions:
            self.sample_ports = services.coupler.sample_ports(self.states)
            self.sample_received_masks = services.coupler.sample_received_masks(self.states)
        self.sample_cause_id = self.cause_id

    def blind_samples(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        blind_ports: Mapping[int, int],
        services: SpatialServices,
    ) -> tuple[dict[int, Values], dict[int, Values]]:
        """Per-slot samples that exclude what arrived through each record's own entry port."""
        slot_samples: dict[int, Values] = {}
        slot_fluxes: dict[int, Values] = {}
        for slot, port in blind_ports.items():
            if slot >= len(records) or records[slot] is None or not self.sample_delivered:
                continue
            values, fluxes = list(self.sample_values), list(self.sample_fluxes)
            for definition, delivered in zip(
                services.initial.spatial_fields, self.sample_delivered, strict=True
            ):
                through = unpack(delivered[port])
                if not any(through):
                    continue
                index = definition.field
                values[index] = pack(subtract_components(unpack(values[index]), through))
                if len(through) == 1:
                    flux = list(unpack(fluxes[index]))
                    axis, opposite = divmod(port, 2)
                    flux[axis] = checked_work(
                        flux[axis] + through[0] if opposite else flux[axis] - through[0]
                    )
                    fluxes[index] = pack(tuple(flux))
            slot_samples[slot] = tuple(values)
            slot_fluxes[slot] = tuple(fluxes)
        return slot_samples, slot_fluxes

    def receive(
        self,
        arrivals: tuple[SpatialPacket, ...],
        tick: int,
        services: SpatialServices,
        *,
        carrier: DisturbanceNode | None = None,
    ) -> list[dict[str, object]]:
        """Validate and accept a local batch; transport releases it before publication."""
        if bounded(tick) < 0:
            raise ValueError("node clock must be nonnegative")
        if carrier is not None and carrier.position != self.position:
            raise ValueError("carrier and spatial components must belong to the same Node")
        if type(arrivals) is not tuple or len(arrivals) > port_count(services.initial):
            raise ValueError("spatial arrival batch exceeds fixed port capacity")
        for packet in arrivals:
            if type(packet) is not SpatialPacket or bounded(packet.arrival_tick) != tick:
                raise ValueError("node received a spatial packet outside its arrival tick")
            if (
                neighbor_address(
                    packet.origin, packet.port, services.initial.shape, services.initial.boundary
                )
                != self.position
            ):
                raise ValueError("node received a spatial packet addressed to another Node")
            validate_spatial_bundle(services.initial, packet.fields)
        if services.events.enabled:
            services.events.require_room(1 + int(services.decayer is not None))
        losses = [[0] * field.components for field in services.initial.fields]
        receiving = (
            (
                self.incoming
                or tuple(
                    zero_spatial_state(services.initial.fields[d.field].components)
                    for d in services.initial.spatial_fields
                )
            )
            if self.shared_pending
            else self.states
        )
        decay_cost = self.incoming_decay_cost if self.shared_pending else self.received_decay_cost
        arrival_cost = 0
        surviving = []
        for packet in arrivals:
            if services.decayer is None:
                surviving.append(packet)
                continue
            bundle, dissipated, cost = services.decayer(packet.fields)
            validate_decay(services.initial, bundle, dissipated, cost)
            surviving.append(replace(packet, fields=bundle))
            decay_cost = bounded(checked_work(decay_cost + cost))
            arrival_cost = bounded(checked_work(arrival_cost + cost))
            for index, dissipated_values in enumerate(dissipated):
                for component, value in enumerate(dissipated_values):
                    losses[index][component] = checked_work(losses[index][component] + value)
        resident_rays = list(self.rays) or [() for _ in services.initial.spatial_fields]
        ray_arrivals = [[0] * 6 for _ in services.initial.spatial_fields]
        for packet in arrivals:
            for index, packet_rays in enumerate(packet.rays):
                if not packet_rays:
                    continue
                definition = services.initial.spatial_fields[index]
                field = services.initial.fields[definition.field]
                if not definition.rays:
                    raise ValueError("rays delivered to a field without ray transport")
                incoming_rays = packet_rays
                if services.decayer is not None and definition.decay is not None:
                    meter = CostMeter(services.initial.operation_costs)
                    incoming_rays, removed = attenuate_rays(packet_rays, definition.decay, meter)
                    losses[definition.field][0] = checked_work(losses[definition.field][0] + removed)
                    decay_cost = bounded(checked_work(decay_cost + meter.total))
                    arrival_cost = bounded(checked_work(arrival_cost + meter.total))
                ray_arrivals[index][packet.port] = checked_work(
                    ray_arrivals[index][packet.port] + ray_stock(incoming_rays)
                )
                resident_rays[index] = merge_rays(tuple(resident_rays[index]) + incoming_rays)
                validate_rays(resident_rays[index], definition, field)
        localized = list(self.localized) or [
            pack((0,) * services.initial.fields[d.field].components)
            for d in services.initial.spatial_fields
        ]
        deposited = [[0] * field.components for field in services.initial.fields]
        for index, definition in enumerate(services.initial.spatial_fields):
            if definition.decay is None or not definition.decay.localizes:
                continue
            field = services.initial.fields[definition.field]
            # The removed fraction stays owned here as stationary stock, not loss.
            deposited[definition.field] = losses[definition.field]
            losses[definition.field] = [0] * field.components
            localized[index] = pack(
                add_components(unpack(localized[index]), tuple(deposited[definition.field]))
            )
            field.validate(localized[index])
        states = []
        arrival_readings = []
        for index, definition in enumerate(services.initial.spatial_fields):
            field = services.initial.fields[definition.field]
            old = receiving[index]
            populations = [list(unpack(v)) for v in old.populations]
            phases = [list(unpack(v)) for v in old.allocation_phases]
            phase_denominator = sum(definition.axis_weights) if definition.axis_weights else 1
            directions = (
                [list(unpack(payload)) for payload in old.delivered]
                if services.initial.node_execution
                else [[0] * field.components for _ in range(6)]
            )
            for port, stock in enumerate(ray_arrivals[index]):
                if stock:
                    directions[port][0] = checked_work(directions[port][0] + stock)
            for packet in surviving:
                for octant, payload in enumerate(packet.fields[index]):
                    field.validate(payload)
                    for component, value in enumerate(unpack(payload)):
                        populations[octant][component] = checked_work(
                            populations[octant][component] + value
                        )
                        directions[packet.port][component] = checked_work(
                            directions[packet.port][component] + value
                        )
                if packet.phases:
                    # Carried remainders merge by addition modulo the axis cycle.
                    for octant, payload in enumerate(packet.phases[index]):
                        for component, value in enumerate(unpack(payload)):
                            phases[octant][component] = (
                                phases[octant][component] + value
                            ) % phase_denominator
            packed = tuple(pack(tuple(v)) for v in populations)
            merged_phases = tuple(pack(tuple(v)) for v in phases)
            arrival_readings.append(tuple(tuple(v) for v in directions))
            delivered = tuple(
                pack(add_components(tuple(v), unpack(old.delivered[port])))
                if self.shared_pending
                else pack(tuple(v))
                for port, v in enumerate(directions)
            )
            for payload in (*packed, *delivered):
                field.validate(payload)
            local = list(unpack(definition.baseline))
            for population_values in populations:
                for component, value in enumerate(population_values):
                    local[component] = checked_work(local[component] + value)
            field.validate(pack(tuple(local)))
            received_mask = old.received_mask if services.initial.node_execution else 0
            for packet in arrivals:
                received_mask |= 1 << packet.port
            states.append(SpatialState(packed, merged_phases, delivered, received_mask))
        received_count = bounded(
            checked_work(
                (self.incoming_count if self.shared_pending else self.received_count) + len(arrivals)
            )
        )
        if services.balance_guard is not None:
            records = () if carrier is None else carrier.records
            services.balance_guard.check(
                LocalInventory(
                    records=records,
                    spatial=tuple(state.populations for state in self.states),
                    spatial_packets=tuple(packet.fields for packet in arrivals),
                ),
                LocalInventory(records=records, spatial=tuple(state.populations for state in states)),
                "spatial receipt",
            )
        self.arrival_mask = tuple(
            int(any(packet.port == port ^ 1 for packet in arrivals)) or old
            for port, old in enumerate(self.arrival_mask)
        )
        if self.shared_pending:
            self.incoming, self.incoming_count, self.incoming_decay_cost = (
                tuple(states),
                received_count,
                decay_cost,
            )
        else:
            self.states, self.received_count, self.received_decay_cost = (
                tuple(states),
                received_count,
                decay_cost,
            )
        self.localized = tuple(localized)
        if any(definition.rays for definition in services.initial.spatial_fields):
            self.rays = tuple(tuple(rays) for rays in resident_rays)
        services.activity.mark(self.position, True)
        services.accounting.record_dissipation(tuple(tuple(values) for values in losses))
        if any(any(values) for values in deposited):
            services.accounting.record_localized(tuple(tuple(values) for values in deposited))
        # Read-only, post-commit summaries. State.delivered uses travel ports;
        # a receiver sees the opposite side. Retain zero readings on used
        # ports so cancellation is distinct from no completed reception.
        received_fields = [
            {
                services.initial.fields[definition.field].name: readings[port ^ 1]
                for definition, readings in zip(
                    services.initial.spatial_fields, arrival_readings, strict=True
                )
            }
            if any(packet.port == port ^ 1 for packet in arrivals)
            else {}
            for port in range(6)
        ]
        notifications: list[dict[str, object]] = []
        self.cause_id = self._event(
            "spatial_received",
            tick,
            services,
            causes=(self.cause_id, *(p.cause_id for p in arrivals)),
            notifications=notifications,
            packets=len(arrivals),
            received_fields=received_fields,
        )
        if services.decayer is not None:
            self.cause_id = self._event(
                "spatial_decayed",
                tick,
                services,
                causes=(self.cause_id,),
                notifications=notifications,
                dissipated={
                    field.name: tuple(losses[i])
                    for i, field in enumerate(services.initial.fields)
                    if any(losses[i])
                },
                localized={
                    field.name: tuple(deposited[i])
                    for i, field in enumerate(services.initial.fields)
                    if any(deposited[i])
                },
                cost=arrival_cost,
            )
        return notifications
