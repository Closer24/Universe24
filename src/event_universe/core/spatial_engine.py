"""Spatial ownership with fixed or shared computation cycle scheduling."""

from collections.abc import Callable, Mapping, Set
from dataclasses import dataclass, replace
from typing import Protocol

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
from .event_space import CausalEventSpace
from .integer import add_components, checked_work, subtract_components
from .node_execution import NodeExecution, SpatialPlanningInput
from .spatial_state import (
    FieldInteractionGuard,
    SpatialBundle,
    SpatialCouplingResult,
    SpatialNodeState,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
)
from .topology import neighbor_address

SpatialPlanner = Callable[
    [tuple[SpatialState, ...], tuple[DisturbanceRecord | None, ...], int], SpatialPlan
]
SpatialDecayer = Callable[[SpatialBundle], tuple[SpatialBundle, Values, int]]
EventSink = Callable[[dict[str, object]], None]
RecordCommit = Callable[[Address3, tuple[DisturbanceRecord | None, ...]], None]
RecordCause = Callable[[Address3], int | None]
CauseCommit = Callable[[Address3, int], None]


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
class _PreparedSpatialCycle:
    position: Address3
    node: SpatialNodeState
    states: tuple[SpatialState, ...]
    records: tuple[DisturbanceRecord | None, ...]
    sample_values: Values
    sample_fluxes: Values
    sample_ports: tuple[Values, ...]
    sample_cause: int | None


class SpatialEngine:
    def __init__(
        self,
        initial: InitialState,
        planner: SpatialPlanner,
        observer: EventSink | None,
        coupler: SpatialCoupler | None = None,
        decayer: SpatialDecayer | None = None,
        *,
        event_space: CausalEventSpace | None = None,
    ) -> None:
        self.initial = initial
        self.planner = planner
        self.observer = observer
        self.coupler = coupler
        self.decayer = decayer
        self.event_space = event_space
        meter = CostMeter(initial.operation_costs)
        if initial.spatial_computation_delay:
            components = 8 * sum(initial.fields[d.field].components for d in initial.spatial_fields)
            meter.charge("read", 2 * components)
            meter.charge("evaluate", components)
            meter.charge("update", components)
        self.node_merge_cost = meter.total
        self.nodes: dict[Address3, SpatialNodeState] = {}
        # Host scheduling index only: retain physical registers in self.nodes.
        self._active: set[Address3] = set()
        self._field_tick = -1
        self.links: dict[Address3, tuple[SpatialPacket | None, ...]] = {}
        self.sources = [[0] * field.components for field in initial.fields]
        self.dissipation = [[0] * field.components for field in initial.fields]
        self.reactions = [[0] * field.components for field in initial.fields]
        self.transformations = [[0] * field.components for field in initial.fields]
        self.escaped = [[0] * field.components for field in initial.fields]
        for seed in initial.spatial_seeds:
            node = self._at(seed.position)
            states = list(node.states)
            states[seed.spatial_field] = replace(
                states[seed.spatial_field], populations=seed.populations
            )
            node.states = tuple(states)
            self.values(seed.position)
        self._initial_totals = self.totals()
        if self.event_space is not None:
            self.event_space.require_room(len(self.nodes))
            for position, node in sorted(self.nodes.items()):
                node.cause_id = self._event("spatial_source", 0, position)

    def _blank_states(self) -> tuple[SpatialState, ...]:
        result = []
        for definition in self.initial.spatial_fields:
            zero = pack((0,) * self.initial.fields[definition.field].components)
            result.append(SpatialState((zero,) * 8, (zero,) * 8, (zero,) * 6))
        return tuple(result)

    def _at(self, position: Address3) -> SpatialNodeState:
        if position not in self.nodes:
            self.nodes[position] = SpatialNodeState(self._blank_states())
            self._active.add(position)
        elif position not in self._active:
            # An idle known node completed the empty phase without a host visit.
            # New nodes stay active, so this cannot backdate their creation.
            self.nodes[position].last_begin_tick = self._field_tick
        return self.nodes[position]

    def _neighbor(self, position: Address3, port: int) -> Address3 | None:
        return neighbor_address(position, port, self.initial.shape, self.initial.boundary)

    def _event(
        self,
        event: str,
        tick: int,
        position: Address3,
        *,
        causes: tuple[int | None, ...] = (),
        notifications: list[dict[str, object]] | None = None,
        **details: object,
    ) -> int | None:
        identity = None
        if self.event_space is not None:
            entry = self.event_space.append(
                tick=tick,
                addresses=(position,),
                owner="spatial",
                kind=event,
                physical_parents=tuple(dict.fromkeys(c for c in causes if c is not None)),
            )
            identity = entry.id
            details = {**details, "event_id": identity, "parents": entry.parents}
        if self.observer is not None:
            data = {"event": event, "tick": tick, "position": position, **details}
            if notifications is None:
                self.observer(data)
            else:
                notifications.append(data)
        return identity

    def _notify(self, notifications: list[dict[str, object]]) -> None:
        if self.observer is not None:
            for event in notifications:
                self.observer(event)

    def begin(
        self,
        tick: int,
        residents: Mapping[Address3, tuple[DisturbanceRecord | None, ...]],
        commit_records: RecordCommit,
        *,
        record_cause: RecordCause | None = None,
        commit_cause: CauseCommit | None = None,
        execution: NodeExecution | None = None,
    ) -> None:
        if tick % self.initial.link_ticks:
            return
        self._field_tick = tick
        emitter_types = selected_type_set(self.initial.emissions)
        coupled_types = selected_type_set(
            self.initial.spatial_couplings, self.initial.spatial_interactions
        )
        positions = set(self._active)
        for position, records in residents.items():
            if any(
                record is not None and record.type_index in emitter_types | coupled_types
                for record in records
            ):
                positions.add(position)
        ordered = sorted(positions)
        if execution is not None and execution.parallel:
            prepared = tuple(
                cycle
                for position in ordered
                if (cycle := self._prepare_cycle(tick, position, residents, coupled_types)) is not None
            )
            plans = execution.plan_spatial(
                tuple(
                    SpatialPlanningInput(cycle.states, cycle.records, cycle.node.received_count)
                    for cycle in prepared
                )
            )
            for cycle, plan in zip(prepared, plans, strict=True):
                self._commit_cycle(tick, cycle, plan, commit_records, record_cause, commit_cause)
            return
        for position in ordered:
            cycle = self._prepare_cycle(tick, position, residents, coupled_types)
            if cycle is not None:
                self._commit_cycle(
                    tick,
                    cycle,
                    self.planner(cycle.states, cycle.records, cycle.node.received_count),
                    commit_records,
                    record_cause,
                    commit_cause,
                )

    def _prepare_cycle(
        self,
        tick: int,
        position: Address3,
        residents: Mapping[Address3, tuple[DisturbanceRecord | None, ...]],
        coupled_types: Set[int],
    ) -> _PreparedSpatialCycle | None:
        node = self._at(position)
        if any(packet is not None for packet in self.links.get(position, ())):
            raise ValueError("outgoing spatial links are occupied")
        records = residents.get(position, ())
        sample_values, sample_fluxes, sample_ports = (
            node.sample_values,
            node.sample_fluxes,
            node.sample_ports,
        )
        sample_cause = node.sample_cause_id
        if (
            self.coupler is not None
            and not self.initial.field_phase_first
            and any(record is not None and record.type_index in coupled_types for record in records)
        ):
            # Freeze only locally delivered input, before fresh source injection.
            sample_values = self.coupler.sample(node.states)
            sample_fluxes = self.coupler.sample_fluxes(node.states)
            sample_cause = node.cause_id
            if self.initial.arrival_port_blind:
                node.sample_delivered = tuple(state.delivered for state in node.states)
            if self.initial.spatial_interactions:
                sample_ports = self.coupler.sample_ports(node.states)
        # Samples describe only the preceding delivery interval, never a permanent trail.
        states = (
            node.states
            if self.initial.field_rules
            else tuple(
                replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6)
                for state in node.states
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
            for index, rule in enumerate(self.initial.emissions)
        )
        active_field = any(any(unpack(payload)) for state in states for payload in state.populations)
        if not active_source and not active_field and node.received_count == 0:
            node.states = tuple(
                replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6)
                for state in states
            )
            node.last_cost = 0
            node.cost_cause_id = None
            node.sample_values, node.sample_fluxes, node.sample_ports = (
                sample_values,
                sample_fluxes,
                sample_ports,
            )
            node.sample_cause_id = sample_cause
            node.last_begin_tick = tick
            self._active.discard(position)
            return None
        return _PreparedSpatialCycle(
            position,
            node,
            states,
            records,
            sample_values,
            sample_fluxes,
            sample_ports,
            sample_cause,
        )

    def _commit_cycle(
        self,
        tick: int,
        cycle: _PreparedSpatialCycle,
        plan: SpatialPlan,
        commit_records: RecordCommit,
        record_cause: RecordCause | None,
        commit_cause: CauseCommit | None,
    ) -> None:
        position, node = cycle.position, cycle.node
        cost = bounded(checked_work(plan.cost + node.received_decay_cost))
        packets: list[SpatialPacket | None] = [None] * 6
        # Field-phase-first packets complete their link inside the departure interval.
        arrival = bounded(tick + self.initial.link_ticks - int(self.initial.field_phase_first))
        for port, bundle in enumerate(plan.outgoing):
            if any(any(unpack(payload)) for field in bundle for payload in field):
                packets[port] = SpatialPacket(
                    arrival,
                    position,
                    port,
                    bundle,
                    phases=plan.outgoing_phases[port] if plan.outgoing_phases else (),
                )
        # Worker results are immutable proposals. Only this scheduler thread commits them.
        if self.event_space is not None:
            self.event_space.require_room(1 + sum(p is not None for p in packets))
        carrier_cause = None if record_cause is None else record_cause(position)
        commit_records(position, plan.emission_records)
        node.states = plan.states
        node.last_cost = cost
        node.received_count = 0
        node.received_decay_cost = 0
        node.last_begin_tick = tick
        node.sample_values, node.sample_fluxes, node.sample_ports = (
            cycle.sample_values,
            cycle.sample_fluxes,
            cycle.sample_ports,
        )
        node.sample_cause_id = cycle.sample_cause
        self.links[position] = tuple(packets)
        # One following phase clears the reported cost before becoming idle.
        self._active.add(position)
        for index, payload in enumerate(plan.source_delta):
            for component, value in enumerate(payload):
                self.sources[index][component] += value
        for index, payload in enumerate(plan.rule_delta):
            for component, value in enumerate(payload):
                self.transformations[index][component] += value
        notifications: list[dict[str, object]] = []
        cause = self._event(
            "spatial_cycle",
            tick,
            position,
            causes=(node.cause_id, carrier_cause),
            notifications=notifications,
            cost=cost,
            source_delta={
                field.name: plan.source_delta[i]
                for i, field in enumerate(self.initial.fields)
                if any(plan.source_delta[i])
            },
            **(
                {
                    "rule_delta": {
                        field.name: plan.rule_delta[i]
                        for i, field in enumerate(self.initial.fields)
                        if any(plan.rule_delta[i])
                    }
                }
                if plan.rule_delta
                else {}
            ),
        )
        node.cause_id = node.cost_cause_id = cause
        if cause is not None and commit_cause is not None and plan.emission_records != cycle.records:
            commit_cause(position, cause)
        for index, packet in enumerate(packets):
            if packet is not None:
                sent = self._event(
                    "spatial_sent",
                    tick,
                    position,
                    causes=(cause,),
                    notifications=notifications,
                    port=packet.port,
                    arrival_tick=packet.arrival_tick,
                )
                if sent is not None:
                    packets[index] = replace(packet, cause_id=sent)
        self.links[position] = tuple(packets)
        self._notify(notifications)

    def cycle_causes(self, position: Address3, tick: int, *, sampled: bool) -> tuple[int, ...]:
        """IDs of the exact frozen sample and current cost consumed by a carrier."""
        node = self.nodes.get(position)
        if node is None:
            return ()
        causes = (
            node.sample_cause_id if sampled else None,
            node.cost_cause_id if tick % self.initial.link_ticks == 0 else None,
        )
        return tuple(dict.fromkeys(c for c in causes if c is not None))

    def reaction_causes(self, position: Address3, *, outgoing: bool) -> tuple[int, ...]:
        """Bounded owners read by a joint commit, including departure amendments."""
        node = self.nodes.get(position)
        if node is None:
            return ()
        causes = (node.cause_id,) + (
            tuple(p.cause_id for p in self.links.get(position, ()) if p is not None) if outgoing else ()
        )
        return tuple(dict.fromkeys(c for c in causes if c is not None))

    def link_reaction(self, position: Address3, proposal: ReactionCommit | None, cause: int) -> None:
        """The joint event owns the new stock and any amended departure bundle."""
        if proposal is None:
            return
        self.nodes[position].cause_id = cause
        if proposal.links is not None:
            self.links[position] = tuple(
                None if p is None else replace(p, cause_id=cause) for p in proposal.links
            )

    def freeze_samples(self, residents: Mapping[Address3, tuple[DisturbanceRecord | None, ...]]) -> None:
        """Freeze coupled samples after this interval's field phase has delivered."""
        if self.coupler is None:
            return
        coupled_types = selected_type_set(
            self.initial.spatial_couplings, self.initial.spatial_interactions
        )
        for position, records in residents.items():
            if not any(record is not None and record.type_index in coupled_types for record in records):
                continue
            node = self._at(position)
            node.sample_values = self.coupler.sample(node.states)
            node.sample_fluxes = self.coupler.sample_fluxes(node.states)
            if self.initial.spatial_interactions:
                node.sample_ports = self.coupler.sample_ports(node.states)
            node.sample_cause_id = node.cause_id

    def couple(
        self,
        position: Address3,
        records: tuple[DisturbanceRecord | None, ...],
        blind_ports: Mapping[int, int] | None = None,
    ) -> SpatialCouplingResult:
        if self.coupler is None:
            raise ValueError("spatial coupling requires an explicitly composed law")
        node = self._at(position)
        slot_samples: dict[int, Values] = {}
        slot_fluxes: dict[int, Values] = {}
        for slot, port in (blind_ports or {}).items():
            if slot >= len(records) or records[slot] is None or not node.sample_delivered:
                continue
            values, fluxes = list(node.sample_values), list(node.sample_fluxes)
            for definition, delivered in zip(
                self.initial.spatial_fields, node.sample_delivered, strict=True
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
        return self.coupler(
            records,
            node.sample_values,
            node.sample_fluxes,
            node.sample_ports,
            slot_samples=slot_samples,
            slot_fluxes=slot_fluxes,
        )

    def node_plan(
        self, position: Address3, records: tuple[DisturbanceRecord | None, ...]
    ) -> SpatialPlan:
        """Prepare a bounded field proposal without changing any physical owner."""
        planning_input = self.node_planning_input(position, records)
        if planning_input is None:
            return self.idle_node_plan(position, records)
        plan = self.planner(
            planning_input.states,
            planning_input.records,
            planning_input.received,
        )
        return self.complete_node_plan(position, plan)

    def node_planning_input(
        self, position: Address3, records: tuple[DisturbanceRecord | None, ...]
    ) -> SpatialPlanningInput | None:
        """Freeze the local input consumed by a shared field/carrier cycle."""
        node = self._at(position)
        active_source = any(
            record is not None
            and matches_type(rule, record.type_index)
            and (
                rule.budget is None
                or not record.emission_remaining
                or any(unpack(record.emission_remaining[index]))
            )
            for record in records
            for index, rule in enumerate(self.initial.emissions)
        )
        active = (
            active_source
            or node.received_count
            or any(any(unpack(payload)) for state in node.states for payload in state.populations)
        )
        states = (
            node.states
            if self.initial.field_rules
            else tuple(
                replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6)
                for state in node.states
            )
        )
        return SpatialPlanningInput(states, records, node.received_count) if active else None

    def complete_node_plan(self, position: Address3, plan: SpatialPlan) -> SpatialPlan:
        """Add locally received decay work to an already computed field proposal."""
        node = self._at(position)
        return replace(plan, cost=bounded(checked_work(plan.cost + node.received_decay_cost)))

    def idle_node_plan(
        self, position: Address3, records: tuple[DisturbanceRecord | None, ...]
    ) -> SpatialPlan:
        """Return the formula-free proposal for a Node with no field work."""
        states = self._at(position).states
        if not self.initial.field_rules:
            states = tuple(
                replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6)
                for state in states
            )
        blank = tuple(state.populations for state in self._blank_states())
        zero = tuple((0,) * field.components for field in self.initial.fields)
        return SpatialPlan(states, (blank,) * 6, records, zero, 0)

    def node_coupling(
        self, position: Address3, records: tuple[DisturbanceRecord | None, ...]
    ) -> SpatialCouplingResult:
        """Sample only the owned pre-cycle field; no fresh emission or late input."""
        assert self.coupler is not None
        states = self._at(position).states
        return self.coupler(
            records,
            self.coupler.sample(states),
            self.coupler.sample_fluxes(states),
            self.coupler.sample_ports(states) if self.initial.spatial_interactions else (),
        )

    def packets(
        self, position: Address3, tick: int, outgoing: tuple[SpatialBundle, ...]
    ) -> tuple[SpatialPacket | None, ...]:
        if len(outgoing) != 6:
            raise ValueError("spatial output requires exactly six bounded ports")
        arrival = bounded(checked_work(tick + self.initial.link_ticks))
        return tuple(
            SpatialPacket(arrival, position, port, bundle)
            if any(any(unpack(payload)) for field in bundle for payload in field)
            else None
            for port, bundle in enumerate(outgoing)
        )

    def node_states(self, position: Address3, plan: SpatialPlan) -> tuple[SpatialState, ...]:
        """Merge completed later inputs only after the frozen transformation."""
        incoming = self._at(position).incoming or self._blank_states()
        states = []
        for definition, state, later in zip(
            self.initial.spatial_fields, plan.states, incoming, strict=True
        ):
            field = self.initial.fields[definition.field]
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
        position: Address3,
        tick: int,
        plan: SpatialPlan,
        states: tuple[SpatialState, ...],
        phases: Values,
        packets: tuple[SpatialPacket | None, ...],
        reaction: Values,
    ) -> None:
        """Install already validated field ownership together with its carrier owner."""
        node = self._at(position)
        node.states, node.reaction_phases = states, phases
        node.received_count, node.received_decay_cost = node.incoming_count, node.incoming_decay_cost
        node.incoming, node.incoming_count, node.incoming_decay_cost = (), 0, 0
        node.pending = 0
        node.last_cost, node.last_begin_tick = plan.cost, tick
        self.links[position] = packets
        self._active.add(position)
        for ledger, delta in (
            (self.sources, plan.source_delta),
            (self.transformations, plan.rule_delta),
            (self.reactions, reaction),
        ):
            for index, values in enumerate(delta):
                for component, amount in enumerate(values):
                    ledger[index][component] += amount

    def validate_guards(
        self, position: Address3, reaction: Values, guards: tuple[FieldInteractionGuard, ...]
    ) -> None:
        if guards:
            if self.coupler is None:
                raise ValueError("spatial interaction guards require a configured response law")
            self.coupler.validate_guards(self._at(position).states, reaction, guards)

    def prepare_reaction(
        self, position: Address3, tick: int, reaction: Values, *, plan: SpatialPlan | None = None
    ) -> ReactionCommit | None:
        if not reaction or not any(any(payload) for payload in reaction):
            return None
        if self.coupler is None:
            raise ValueError("a spatial reaction requires its configured coupling law")
        node = self._at(position)
        if plan is not None:
            node = replace(node, states=plan.states, last_begin_tick=tick)
        if node.last_begin_tick != tick:
            states, phases = self.coupler.deposit(node.states, node.reaction_phases, reaction)
            return ReactionCommit(states, phases, None)
        # Only this instant's departure buffers are still locally appendable.
        # Packets from an earlier departure are immutable while in transit.
        old_links = (
            self.links.get(position, (None,) * 6)
            if plan is None
            else self.packets(position, tick, plan.outgoing)
        )
        arrival = bounded(tick + self.initial.link_ticks)
        if any(packet is not None and packet.arrival_tick != arrival for packet in old_links):
            raise ValueError("reaction cannot alter a spatial packet already in transit")
        states, phases, outgoing = self.coupler.forward_reaction(
            node.states, node.reaction_phases, reaction
        )
        links: list[SpatialPacket | None] = []
        for port, (old, bundle) in enumerate(zip(old_links, outgoing, strict=True)):
            merged = []
            for index, (definition, populations) in enumerate(
                zip(self.initial.spatial_fields, bundle, strict=True)
            ):
                field = self.initial.fields[definition.field]
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
                SpatialPacket(arrival, position, port, values, phases=() if old is None else old.phases)
                if any(any(unpack(payload)) for field in values for payload in field)
                else None
            )
        return ReactionCommit(states, phases, tuple(links))

    def commit_reaction(
        self, position: Address3, proposal: ReactionCommit | None, reaction: Values = ()
    ) -> None:
        if proposal is None:
            return
        node = self._at(position)
        node.states = proposal.states
        node.reaction_phases = proposal.phases
        self._active.add(position)
        if proposal.links is not None:
            self.links[position] = proposal.links
        for index, values in enumerate(reaction):
            for component, value in enumerate(values):
                self.reactions[index][component] += value

    def _escape(self, packet: SpatialPacket, tick: int) -> None:
        """No receiving node exists outside; terminal stock escapes without exterior decay."""
        amounts = [[0] * field.components for field in self.initial.fields]
        if self.event_space is not None:
            self.event_space.require_room(1)
        for definition, populations in zip(self.initial.spatial_fields, packet.fields, strict=True):
            if len(populations) != 8:
                raise ValueError("a terminal spatial packet requires eight octants")
            field = self.initial.fields[definition.field]
            for payload in populations:
                field.validate(payload)
                for component, value in enumerate(unpack(payload)):
                    amounts[definition.field][component] = checked_work(
                        amounts[definition.field][component] + value
                    )
        for index, values in enumerate(amounts):
            for component, value in enumerate(values):
                self.escaped[index][component] += value
        links = list(self.links[packet.origin])
        links[packet.port] = None
        self.links[packet.origin] = tuple(links)
        self._event(
            "spatial_escaped",
            tick,
            packet.origin,
            causes=(packet.cause_id,),
            port=packet.port,
            escaped={
                field.name: tuple(amounts[i])
                for i, field in enumerate(self.initial.fields)
                if any(amounts[i])
            },
        )

    def deliver(self, tick: int) -> None:
        ready: dict[Address3, list[SpatialPacket]] = {}
        for packets in self.links.values():
            for packet in packets:
                if packet is not None and packet.arrival_tick == tick:
                    target = self._neighbor(packet.origin, packet.port)
                    if target is None:
                        self._escape(packet, tick)
                    else:
                        ready.setdefault(target, []).append(packet)
        for position, arrivals in sorted(ready.items()):
            if self.event_space is not None:
                self.event_space.require_room(1 + int(self.decayer is not None))
            node = self._at(position)
            losses = [[0] * field.components for field in self.initial.fields]
            receiving = (node.incoming or self._blank_states()) if node.pending else node.states
            decay_cost = node.incoming_decay_cost if node.pending else node.received_decay_cost
            arrival_cost = 0
            surviving = []
            for packet in arrivals:
                if self.decayer is None:
                    surviving.append(packet)
                    continue
                bundle, dissipated, cost = self.decayer(packet.fields)
                surviving.append(replace(packet, fields=bundle))
                decay_cost = bounded(checked_work(decay_cost + cost))
                arrival_cost = bounded(checked_work(arrival_cost + cost))
                for index, dissipated_values in enumerate(dissipated):
                    for component, value in enumerate(dissipated_values):
                        losses[index][component] = checked_work(losses[index][component] + value)
            states = []
            arrival_readings = []
            for index, definition in enumerate(self.initial.spatial_fields):
                field = self.initial.fields[definition.field]
                old = receiving[index]
                populations = [list(unpack(v)) for v in old.populations]
                phases = [list(unpack(v)) for v in old.allocation_phases]
                phase_denominator = sum(definition.axis_weights)
                directions = [[0] * field.components for _ in range(6)]
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
                delivered = tuple(
                    pack(add_components(tuple(v), unpack(old.delivered[port])))
                    if node.pending
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
                states.append(SpatialState(packed, merged_phases, delivered))
                arrival_readings.append(tuple(tuple(v) for v in directions))
            received_count = bounded(
                checked_work(
                    (node.incoming_count if node.pending else node.received_count) + len(arrivals)
                )
            )
            if node.pending:
                node.incoming, node.incoming_count, node.incoming_decay_cost = (
                    tuple(states),
                    received_count,
                    decay_cost,
                )
            else:
                node.states, node.received_count, node.received_decay_cost = (
                    tuple(states),
                    received_count,
                    decay_cost,
                )
            self._active.add(position)
            for index, lost_values in enumerate(losses):
                for component, value in enumerate(lost_values):
                    self.dissipation[index][component] += value
            for packet in arrivals:
                links = list(self.links[packet.origin])
                links[packet.port] = None
                self.links[packet.origin] = tuple(links)
            # Read-only, post-commit summaries. State.delivered uses travel ports;
            # a receiver sees the opposite side. Retain zero readings on used
            # ports so cancellation is distinct from no completed reception.
            received_fields = [
                {
                    self.initial.fields[definition.field].name: readings[port ^ 1]
                    for definition, readings in zip(
                        self.initial.spatial_fields, arrival_readings, strict=True
                    )
                }
                if any(packet.port == port ^ 1 for packet in arrivals)
                else {}
                for port in range(6)
            ]
            notifications: list[dict[str, object]] = []
            node.cause_id = self._event(
                "spatial_received",
                tick,
                position,
                causes=(node.cause_id, *(p.cause_id for p in arrivals)),
                notifications=notifications,
                packets=len(arrivals),
                received_fields=received_fields,
            )
            if self.decayer is not None:
                node.cause_id = self._event(
                    "spatial_decayed",
                    tick,
                    position,
                    causes=(node.cause_id,),
                    notifications=notifications,
                    dissipated={
                        field.name: tuple(losses[i])
                        for i, field in enumerate(self.initial.fields)
                        if any(losses[i])
                    },
                    cost=arrival_cost,
                )
            self._notify(notifications)

    def cost(self, position: Address3, tick: int) -> int:
        node = self.nodes.get(position)
        return 0 if node is None or tick % self.initial.link_ticks else node.last_cost

    def totals(self) -> list[list[int]]:
        result = [[0] * field.components for field in self.initial.fields]
        volume = self.initial.shape[0] * self.initial.shape[1] * self.initial.shape[2]
        for index, definition in enumerate(self.initial.spatial_fields):
            for component, value in enumerate(unpack(definition.baseline)):
                result[definition.field][component] += volume * value
            inventories = [self.nodes[position].states[index].populations for position in self._active]
            inventories.extend(
                self.nodes[position].incoming[index].populations
                for position in self._active
                if self.nodes[position].incoming
            )
            inventories.extend(
                packet.fields[index]
                for packets in self.links.values()
                for packet in packets
                if packet is not None
            )
            for populations in inventories:
                for payload in populations:
                    for component, value in enumerate(unpack(payload)):
                        result[definition.field][component] += value
        return result

    def values(self, position: Address3) -> dict[str, dict[str, object]]:
        states = self.nodes[position].states if position in self.nodes else self._blank_states()
        result: dict[str, dict[str, object]] = {}
        for definition, state in zip(self.initial.spatial_fields, states, strict=True):
            field = self.initial.fields[definition.field]
            local = list(unpack(definition.baseline))
            for payload in state.populations:
                for component, value in enumerate(unpack(payload)):
                    local[component] = checked_work(local[component] + value)
            field.validate(pack(tuple(local)))
            result[field.name] = {
                "baseline": unpack(definition.baseline),
                "value": tuple(local),
                "directions": tuple(unpack(v) for v in state.delivered),
                "populations": tuple(unpack(v) for v in state.populations),
            }
        return result

    def accounting(self) -> dict[str, dict[str, object]]:
        """Diagnose every spatial owner, including fields without a conservation flag."""
        totals = self.totals()
        result = {}
        for definition in self.initial.spatial_fields:
            index = definition.field
            expected = tuple(
                start + source + reaction + transformed - loss - escaped
                for start, source, reaction, transformed, loss, escaped in zip(
                    self._initial_totals[index],
                    self.sources[index],
                    self.reactions[index],
                    self.transformations[index],
                    self.dissipation[index],
                    self.escaped[index],
                    strict=True,
                )
            )
            result[self.initial.fields[index].name] = {
                "initial": tuple(self._initial_totals[index]),
                "current": tuple(totals[index]),
                "sources": tuple(self.sources[index]),
                "reactions": tuple(self.reactions[index]),
                "dissipated": tuple(self.dissipation[index]),
                "escaped": tuple(self.escaped[index]),
                "balanced": tuple(totals[index]) == expected,
                **(
                    {"transformations": tuple(self.transformations[index])}
                    if self.initial.field_rules
                    else {}
                ),
            }
        return result

    def snapshot(self) -> dict[str, object]:
        return {
            "spatial_fields": [
                {
                    "position": position,
                    "fields": self.values(position),
                    "cost": node.last_cost,
                    **(
                        {
                            "pending": node.pending,
                            "incoming": {
                                self.initial.fields[d.field].name: tuple(
                                    unpack(p) for p in state.populations
                                )
                                for d, state in zip(
                                    self.initial.spatial_fields, node.incoming, strict=False
                                )
                            },
                        }
                        if self.initial.spatial_computation_delay
                        else {}
                    ),
                }
                for position, node in sorted(self.nodes.items())
            ],
            "spatial_baselines": {
                self.initial.fields[d.field].name: unpack(d.baseline)
                for d in self.initial.spatial_fields
            },
            "spatial_transfers": [
                {
                    "origin": p.origin,
                    "target": self._neighbor(p.origin, p.port),
                    "port": p.port,
                    "arrival_tick": p.arrival_tick,
                    "fields": {
                        self.initial.fields[d.field].name: tuple(unpack(v) for v in p.fields[i])
                        for i, d in enumerate(self.initial.spatial_fields)
                    },
                }
                for packets in self.links.values()
                for p in packets
                if p is not None
            ],
        }
