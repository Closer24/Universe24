"""Local spatial state execution; transport owns the address index."""

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Protocol

from .coupling_selectors import matches_type, selected_type_set
from .disturbance_state import Address3, DisturbanceRecord, InitialState, Values, bounded, pack, unpack
from .integer import add_components, checked_work
from .node_boundary import (
    validate_decay,
    validate_reaction_state,
    validate_samples,
    validate_spatial_bundle,
    validate_spatial_outgoing,
    validate_spatial_plan,
)
from .node_ports import PortBank
from .node_services import add_audit_delta
from .spatial_state import (
    FieldInteractionGuard,
    SpatialBundle,
    SpatialCouplingResult,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
)
from .spatial_state import (
    SpatialNode as NodeState,
)
from .topology import inverse_port, neighbor_address

if TYPE_CHECKING:
    from .disturbance_node import DisturbanceNode

SpatialPlanner = Callable[
    [tuple[SpatialState, ...], tuple[DisturbanceRecord | None, ...], int], SpatialPlan
]
SpatialDecayer = Callable[[SpatialBundle], tuple[SpatialBundle, Values, int]]
EventSink = Callable[[dict[str, object]], None]


class SpatialCoupler(Protocol):
    def sample(self, states: tuple[SpatialState, ...]) -> Values: ...

    def sample_fluxes(self, states: tuple[SpatialState, ...]) -> Values: ...

    def sample_ports(self, states: tuple[SpatialState, ...]) -> tuple[Values, ...]: ...

    def __call__(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        sample: Values,
        fluxes: Values = (),
        ports: tuple[Values, ...] = (),
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
    observer: EventSink | None
    coupler: SpatialCoupler | None
    decayer: SpatialDecayer | None
    activity: NodeActivity
    accounting: SpatialAccounting


class SpatialAccounting:
    """Only local deltas can be submitted; global stock cannot be read by a node."""

    def __init__(
        self,
        sources: list[list[int]],
        dissipation: list[list[int]],
        reactions: list[list[int]],
        transformations: list[list[int]],
    ) -> None:
        self.__sources, self.__dissipation = sources, dissipation
        self.__reactions, self.__transformations = reactions, transformations

    def record_sources(self, values: Values) -> None:
        add_audit_delta(self.__sources, values)

    def record_dissipation(self, values: Values) -> None:
        add_audit_delta(self.__dissipation, values)

    def record_reactions(self, values: Values) -> None:
        add_audit_delta(self.__reactions, values)

    def record_transformations(self, values: Values) -> None:
        add_audit_delta(self.__transformations, values)


@dataclass(slots=True)
class SpatialNode(NodeState):
    position: Address3 = (0, 0, 0)
    output: PortBank[SpatialPacket] = field(default_factory=lambda: PortBank(()))

    def catch_up_idle(self, tick: int) -> None:
        """Record skipped empty phases without rerunning a physical rule."""
        self.last_begin_tick = tick

    def cost(self, tick: int, services: SpatialServices) -> int:
        return 0 if tick % services.initial.link_ticks else self.last_cost

    def _message(self, event: str, tick: int, **details: object) -> dict[str, object]:
        return {"event": event, "tick": tick, "position": self.position, **details}

    def _event(self, event: str, tick: int, services: SpatialServices, **details: object) -> None:
        if services.observer is not None:
            services.observer(self._message(event, tick, **details))

    def advance(self, tick: int, carrier: DisturbanceNode | None, services: SpatialServices) -> None:
        bounded(tick)
        if tick < 0:
            raise ValueError("node clock must be nonnegative")
        if carrier is not None and carrier.position != self.position:
            raise ValueError("carrier and spatial components must belong to the same node")
        if tick % services.initial.link_ticks:
            return
        coupled_types = selected_type_set(
            services.initial.spatial_couplings, services.initial.spatial_interactions
        )
        if any(packet is not None for packet in self.output.packets):
            raise ValueError("outgoing spatial links are occupied")
        records = () if carrier is None else carrier.records
        sample_values, sample_fluxes, sample_ports = (
            self.sample_values,
            self.sample_fluxes,
            self.sample_ports,
        )
        if services.coupler is not None and any(
            record is not None and record.type_index in coupled_types for record in records
        ):
            # Freeze only locally delivered input, before fresh source injection.
            sample_values = services.coupler.sample(self.states)
            sample_fluxes = services.coupler.sample_fluxes(self.states)
            if services.initial.spatial_interactions:
                sample_ports = services.coupler.sample_ports(self.states)
            validate_samples(services.initial, sample_values, sample_fluxes, sample_ports)
        # Samples describe only the preceding delivery interval, never a permanent trail.
        states = (
            self.states
            if services.initial.field_rules
            else tuple(
                replace(
                    state,
                    delivered=(pack((0,) * len(state.populations[0])),)
                    * services.initial.topology.degree,
                )
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
        active_field = any(any(unpack(payload)) for state in states for payload in state.populations)
        if not active_source and not active_field and self.received_count == 0:
            self.states = tuple(
                replace(
                    state,
                    delivered=(pack((0,) * len(state.populations[0])),)
                    * services.initial.topology.degree,
                )
                for state in states
            )
            self.last_cost = 0
            self.sample_values, self.sample_fluxes, self.sample_ports = (
                sample_values,
                sample_fluxes,
                sample_ports,
            )
            self.last_begin_tick = tick
            services.activity.mark(self.position, False)
            return
        plan = services.planner(states, records, self.received_count)
        validate_spatial_plan(services.initial, plan, len(records), records)
        cost = bounded(checked_work(plan.cost + self.received_decay_cost))
        packets: list[SpatialPacket | None] = [None] * services.initial.topology.degree
        for port, bundle in enumerate(plan.outgoing):
            if any(any(unpack(payload)) for field in bundle for payload in field):
                packets[port] = SpatialPacket(
                    bounded(tick + services.initial.link_ticks), self.position, port, bundle
                )
        # All physical calculations and validation precede the local commit.
        if carrier is None:
            if plan.emission_records:
                raise ValueError("spatial emission cannot create disturbance records")
        else:
            carrier.accept_emission(plan.emission_records)
        self.sample_values, self.sample_fluxes, self.sample_ports = (
            sample_values,
            sample_fluxes,
            sample_ports,
        )
        self.states = plan.states
        self.last_cost = cost
        self.received_count = 0
        self.received_decay_cost = 0
        self.last_begin_tick = tick
        self.output.publish(tuple(packets))
        # One following phase clears the reported cost before becoming idle.
        services.activity.mark(self.position, True)
        services.accounting.record_sources(plan.source_delta)
        services.accounting.record_transformations(plan.rule_delta)
        self._event(
            "spatial_cycle",
            tick,
            services,
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
        for packet in packets:
            if packet is not None:
                self._event(
                    "spatial_sent",
                    tick,
                    services,
                    port=packet.port,
                    arrival_tick=packet.arrival_tick,
                )

    def couple(
        self, records: tuple[DisturbanceRecord | None, ...], services: SpatialServices
    ) -> SpatialCouplingResult:
        if services.coupler is None:
            raise ValueError("spatial coupling requires an explicitly composed law")
        return services.coupler(records, self.sample_values, self.sample_fluxes, self.sample_ports)

    def validate_guards(
        self, services: SpatialServices, reaction: Values, guards: tuple[FieldInteractionGuard, ...]
    ) -> None:
        if guards:
            if services.coupler is None:
                raise ValueError("spatial interaction guards require a configured response law")
            services.coupler.validate_guards(self.states, reaction, guards)

    def prepare_reaction(
        self, tick: int, reaction: Values, services: SpatialServices
    ) -> ReactionCommit | None:
        if not reaction or not any(any(payload) for payload in reaction):
            return None
        if services.coupler is None:
            raise ValueError("a spatial reaction requires its configured coupling law")
        if self.last_begin_tick != tick:
            states, phases = services.coupler.deposit(self.states, self.reaction_phases, reaction)
            validate_reaction_state(services.initial, states, phases)
            return ReactionCommit(states, phases, None)
        # Only this instant's departure buffers are still locally appendable.
        # Packets from an earlier departure are immutable while in transit.
        old_links = self.output.packets
        arrival = bounded(tick + services.initial.link_ticks)
        if any(packet is not None and packet.arrival_tick != arrival for packet in old_links):
            raise ValueError("reaction cannot alter a spatial packet already in transit")
        states, phases, outgoing = services.coupler.forward_reaction(
            self.states, self.reaction_phases, reaction
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
                SpatialPacket(arrival, self.position, port, values)
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

    def receive(
        self, arrivals: tuple[SpatialPacket, ...], tick: int, services: SpatialServices
    ) -> tuple[dict[str, object], ...]:
        initial = services.initial
        bounded(tick)
        if tick < 0:
            raise ValueError("node clock must be nonnegative")
        if type(arrivals) is not tuple or len(arrivals) > initial.topology.degree:
            raise ValueError("spatial arrival batch exceeds fixed port capacity")
        for packet in arrivals:
            if type(packet) is not SpatialPacket or packet.arrival_tick != tick:
                raise ValueError("node received a spatial packet outside its arrival tick")
            bounded(packet.arrival_tick)
            if (
                neighbor_address(
                    packet.origin, packet.port, initial.shape, initial.boundary, initial.topology
                )
                != self.position
            ):
                raise ValueError("node received a spatial packet addressed to another node")
            validate_spatial_bundle(initial, packet.fields)
        messages: list[dict[str, object]] = []
        losses = [[0] * field.components for field in services.initial.fields]
        decay_cost = self.received_decay_cost
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
        states = []
        for index, definition in enumerate(services.initial.spatial_fields):
            field = services.initial.fields[definition.field]
            old = self.states[index]
            populations = [list(unpack(v)) for v in old.populations]
            directions = [[0] * field.components for _ in range(services.initial.topology.degree)]
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
            packed = tuple(pack(tuple(v)) for v in populations)
            delivered = tuple(pack(tuple(v)) for v in directions)
            for payload in (*packed, *delivered):
                field.validate(payload)
            local = list(unpack(definition.baseline))
            for population_values in populations:
                for component, value in enumerate(population_values):
                    local[component] = checked_work(local[component] + value)
            field.validate(pack(tuple(local)))
            states.append(SpatialState(packed, old.allocation_phases, delivered))
        received_count = bounded(checked_work(self.received_count + len(arrivals)))
        self.states = tuple(states)
        self.received_count = received_count
        self.received_decay_cost = decay_cost
        services.activity.mark(self.position, True)
        services.accounting.record_dissipation(tuple(tuple(values) for values in losses))
        # Read-only, post-commit summaries. State.delivered uses travel ports;
        # a receiver sees the opposite side. Retain zero readings on used
        # ports so cancellation is distinct from no completed reception.
        received_fields = [
            {
                services.initial.fields[definition.field].name: unpack(
                    state.delivered[inverse_port(port, services.initial.topology)]
                )
                for definition, state in zip(services.initial.spatial_fields, states, strict=True)
            }
            if any(packet.port == inverse_port(port, services.initial.topology) for packet in arrivals)
            else {}
            for port in range(services.initial.topology.degree)
        ]
        messages.append(
            self._message(
                "spatial_received",
                tick,
                packets=len(arrivals),
                received_fields=received_fields,
            )
        )
        if services.decayer is not None:
            messages.append(
                self._message(
                    "spatial_decayed",
                    tick,
                    dissipated={
                        field.name: tuple(losses[i])
                        for i, field in enumerate(services.initial.fields)
                        if any(losses[i])
                    },
                    cost=arrival_cost,
                )
            )

        return tuple(messages)
