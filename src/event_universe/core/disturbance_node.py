"""A bounded Node owns carrier transitions and its local outgoing port bank."""

from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

from .disturbance_state import (
    Address3,
    DisturbanceNodeState,
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    Packet,
    PendingCycle,
    bounded,
    unpack,
)
from .event_resolution import LocalContext
from .integer import checked_work
from .node_boundary import validate_local_plan, validate_record, validate_records
from .node_conservation import LocalInventory
from .node_ports import PortBank
from .node_services import NodeServices, cycle_timing, port_count
from .spatial_state import SpatialPacket, SpatialState, zero_spatial_state
from .topology import neighbor_address

if TYPE_CHECKING:
    from .spatial_node import SpatialNode, SpatialServices


def record_values(initial: InitialState, record: DisturbanceRecord) -> dict[str, tuple[int, ...]]:
    return {
        initial.fields[i].name: unpack(record.values[i])
        for i in initial.disturbances[record.type_index].fields
    }


@dataclass(slots=True)
class DisturbanceNode(DisturbanceNodeState):
    """Local state and transitions; no world, neighbor inventory or history access."""

    position: Address3 = (0, 0, 0)
    output: PortBank[Packet] = field(default_factory=lambda: PortBank(()), compare=False)
    arrival_mask: tuple[int, ...] = ()
    delay_counts: tuple[int, ...] = ()
    committed_cost: int = 0

    def advance(
        self,
        tick: int,
        services: NodeServices,
        *,
        window_closed: bool = False,
        spatial: SpatialNode | None = None,
        spatial_services: SpatialServices | None = None,
    ) -> None:
        if bounded(tick) < 0:
            raise ValueError("node clock must be nonnegative")
        if spatial is not None and spatial.position != self.position:
            raise ValueError("carrier and spatial components must belong to the same Node")
        if services.initial.node_execution:
            remaining = 0 if self.pending is None else max(0, self.pending.ready_tick - tick)
            self.delay_counts = (remaining,) * port_count(services.initial)
        if not window_closed:
            self._begin(tick, services, spatial, spatial_services)
        self._commit(tick, services, spatial, spatial_services)

    def notify(
        self,
        event: str,
        tick: int,
        services: NodeServices,
        *,
        causes: tuple[int, ...] = (),
        event_cost: int = 0,
        notifications: list[dict[str, object]] | None = None,
        **data: object,
    ) -> int | None:
        identity, message = services.events.record(
            event,
            tick,
            self.position,
            self.cause_id,
            causes=causes,
            event_cost=event_cost,
            owner="disturbance",
            **data,
        )
        if identity is not None:
            self.cause_id = identity
        if notifications is None:
            services.events.publish(message)
        else:
            notifications.append(message)
        return identity

    def receive(
        self,
        packets: tuple[Packet, ...],
        tick: int,
        services: NodeServices,
        *,
        spatial: SpatialNode | None = None,
    ) -> None:
        """Accept a complete, bounded delivery batch before transport releases its packets."""
        if bounded(tick) < 0:
            raise ValueError("node clock must be nonnegative")
        if spatial is not None and spatial.position != self.position:
            raise ValueError("carrier and spatial components must belong to the same Node")
        initial = services.initial
        degree = port_count(initial)
        if type(packets) is not tuple or len(packets) > degree * len(self.output.packets):
            raise ValueError("node arrival batch exceeds fixed port capacity")
        mask = list(self.arrival_mask or (0,) * degree)
        for packet in packets:
            if type(packet) is not Packet or bounded(packet.arrival_tick) != tick:
                raise ValueError("node received a packet outside its arrival tick")
            if (
                neighbor_address(packet.origin, packet.port, initial.shape, initial.boundary)
                != self.position
            ):
                raise ValueError("node received a packet addressed to another Node")
            validate_record(initial, packet.record)
            mask[packet.port ^ 1] = 1
        services.events.require_room(len(packets))
        locked = (
            frozenset()
            if self.pending is None
            else frozenset(slot for slot, _ in self.pending.plan.replacements)
        )
        if self.pending is not None and self.pending.spatial_plan is not None:
            locked |= frozenset(
                slot
                for slot, record in enumerate(self.pending.spatial_plan.emission_records)
                if record is not None
            )
        records = services.record_policy.receive(
            self.records, tuple(packet.record for packet in packets), locked
        )
        if len(records) != len(self.records):
            raise ValueError("record policy cannot change local capacity")
        validate_records(initial, records, len(self.records), self.records)
        if any(records[slot] != self.records[slot] for slot in locked):
            raise ValueError("record policy cannot change a pending local slot")
        received = bounded(self.received_count + len(packets))
        if services.balance_guard is not None:
            fields = () if spatial is None else tuple(state.populations for state in spatial.states)
            services.balance_guard.check(
                LocalInventory(
                    records=self.records,
                    spatial=fields,
                    carrier_packets=tuple(p.record for p in packets),
                ),
                LocalInventory(records=records, spatial=fields),
                "carrier receipt",
            )
        self.records, self.received_count, self.arrival_mask = records, received, tuple(mask)

    def acknowledge_receipt(
        self, packets: tuple[Packet, ...], tick: int, services: NodeServices
    ) -> None:
        for packet in packets:
            self.notify(
                "received",
                tick,
                services,
                causes=() if packet.cause_id is None else (packet.cause_id,),
                port=packet.port ^ 1,
                disturbance=services.initial.disturbances[packet.record.type_index].name,
                values=record_values(services.initial, packet.record),
            )

    def _begin(
        self,
        tick: int,
        services: NodeServices,
        spatial: SpatialNode | None,
        spatial_services: SpatialServices | None,
    ) -> None:
        if self.pending is not None or self.available_tick > tick:
            return
        if services.initial.spatial_computation_delay:
            assert spatial is not None and spatial_services is not None
            self._begin_shared(tick, services, spatial, spatial_services)
            return
        if services.initial.node_execution and spatial is not None and spatial.pending is not None:
            return
        if not services.record_policy.has_work(self.records) and not (
            services.resolver is not None
            and services.resolver.has_work(
                LocalContext(
                    tick,
                    self.position,
                    self.records,
                    self.coupling_remainders,
                    self.received_count,
                    self.cause_id,
                )
            )
        ):
            return
        coupled = (
            spatial.couple(self.records, spatial_services, tick)
            if spatial is not None
            and spatial_services is not None
            and any(r is not None and r.type_index in services.coupled_types for r in self.records)
            else None
        )
        if services.events.enabled:
            services.events.require_room(1)
        context = LocalContext(
            tick,
            self.position,
            self.records if coupled is None else coupled.records,
            self.coupling_remainders,
            self.received_count,
            self.cause_id,
        )
        plan = (
            services.planner(context.records, context.residuals, context.received)
            if services.resolver is None
            else services.resolver.resolve(context, services.planner)
        )
        if coupled is not None:
            validate_records(services.initial, coupled.records, len(self.records), self.records)
            plan = replace(
                plan,
                spatial_reaction=coupled.reaction,
                spatial_guards=coupled.guards,
                cost=bounded(checked_work(plan.cost + coupled.cost)),
                interaction_ticks=bounded(
                    checked_work(plan.interaction_ticks + coupled.interaction_ticks)
                ),
            )
        if spatial is not None and spatial_services is not None:
            plan = replace(
                plan, cost=bounded(checked_work(plan.cost + spatial.cost(tick, spatial_services)))
            )
            plan = services.record_policy.report_cost(plan)
        validate_local_plan(services.initial, plan, len(self.coupling_remainders), self.records)
        if services.initial.node_execution:
            extra = plan.interaction_ticks
            duration = bounded(extra + services.initial.link_ticks)
        else:
            extra, duration = cycle_timing(
                plan.cost, services.initial.normal_budget, services.initial.link_ticks
            )
        services.accounting.charge_cycle(plan.cost)
        pending = PendingCycle(bounded(tick + extra), bounded(tick + duration), plan)
        if services.initial.node_execution and coupled is not None and spatial is not None:
            spatial.consume_sample()
        # Originals remain in their occupied slots throughout the local wait.
        self.pending = pending
        self.received_count = 0
        self.last_cost = plan.cost
        self.arrival_mask = (0,) * port_count(services.initial)
        self.delay_counts = (extra // services.initial.link_ticks,) * port_count(services.initial)
        cause = self.notify(
            "cycle_started",
            tick,
            services,
            causes=(
                (() if plan.cause_id is None else (plan.cause_id,))
                + (
                    spatial.cycle_causes(tick, spatial_services, sampled=coupled is not None)
                    if services.events.enabled and spatial is not None and spatial_services is not None
                    else ()
                )
            ),
            event_cost=plan.cost,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
        )
        self.pending = replace(pending, cause_id=cause)

    def _begin_shared(
        self, tick: int, services: NodeServices, spatial: SpatialNode, spatial_services: SpatialServices
    ) -> None:
        """Freeze one field/carrier transaction and charge its combined work once."""
        field_plan = spatial.node_plan(self.records, spatial_services, self.committed_cost)
        has_carriers = services.record_policy.has_work(self.records)
        if not has_carriers and field_plan.cost == 0:
            spatial.last_cost = 0
            spatial.cost_cause_id = None
            spatial_services.activity.mark(self.position, False)
            return
        field_plan = replace(
            field_plan, cost=bounded(checked_work(field_plan.cost + spatial_services.node_merge_cost))
        )
        self._validate_emission_records(self.records, field_plan.emission_records)
        records = field_plan.emission_records
        coupled = (
            spatial.node_coupling(records, spatial_services)
            if any(
                record is not None and record.type_index in services.coupled_types for record in records
            )
            else None
        )
        zero = tuple((0,) * field.components for field in services.initial.fields)
        plan = (
            services.planner(
                records if coupled is None else coupled.records,
                self.coupling_remainders,
                self.received_count,
            )
            if has_carriers
            else LocalPlan((), (), self.coupling_remainders, zero, 0)
        )
        if coupled is not None:
            plan = replace(
                plan,
                spatial_reaction=coupled.reaction,
                spatial_guards=coupled.guards,
                cost=bounded(checked_work(plan.cost + coupled.cost)),
            )
        plan = services.record_policy.report_cost(
            replace(plan, cost=bounded(checked_work(plan.cost + field_plan.cost)))
        )
        validate_local_plan(services.initial, plan, len(self.coupling_remainders), self.records)
        if plan.spatial_guards:
            assert spatial_services.coupler is not None
            spatial_services.coupler.validate_guards(
                field_plan.states, plan.spatial_reaction, plan.spatial_guards
            )
        guard_states = field_plan.states if plan.spatial_guards else ()
        reaction = spatial.prepare_reaction(
            tick, plan.spatial_reaction, spatial_services, plan=field_plan
        )
        phases = spatial.reaction_phases
        if reaction is not None:
            assert reaction.links is not None
            blank = tuple(
                zero_spatial_state(services.initial.fields[d.field].components).populations
                for d in services.initial.spatial_fields
            )
            field_plan = replace(
                field_plan,
                states=reaction.states,
                outgoing=tuple(blank if p is None else p.fields for p in reaction.links),
            )
            phases = reaction.phases
        extra, duration = cycle_timing(
            plan.cost, services.initial.normal_budget, services.initial.link_ticks
        )
        pending = PendingCycle(
            bounded(tick + extra),
            bounded(tick + duration),
            plan,
            spatial_plan=field_plan,
            spatial_phases=phases,
            spatial_guard_states=guard_states,
        )
        if services.events.enabled:
            services.events.require_room(1)
        field_cause = spatial.cause_id
        services.accounting.charge_cycle(plan.cost)
        self.pending, self.received_count, self.last_cost = pending, 0, plan.cost
        spatial.shared_pending = 1
        spatial.last_cost = field_plan.cost
        self.arrival_mask = (0,) * port_count(services.initial)
        self.delay_counts = (extra // services.initial.link_ticks,) * port_count(services.initial)
        cause = self.notify(
            "cycle_started",
            tick,
            services,
            causes=() if field_cause is None else (field_cause,),
            event_cost=plan.cost,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
            spatial_cost=field_plan.cost,
        )
        self.pending = replace(pending, cause_id=cause)

    def _commit(
        self,
        tick: int,
        services: NodeServices,
        spatial: SpatialNode | None,
        spatial_services: SpatialServices | None,
    ) -> None:
        pending = self.pending
        if pending is None or pending.ready_tick > tick:
            return
        field_plan = pending.spatial_plan
        field_states: tuple[SpatialState, ...] = ()
        field_packets: tuple[SpatialPacket | None, ...] = ()
        if field_plan is not None:
            assert spatial is not None and spatial_services is not None
            if any(packet is not None for packet in spatial.output.packets):
                raise ValueError("outgoing spatial links are occupied")
            field_states = spatial.node_states(field_plan, spatial_services)
            if pending.spatial_guard_states and spatial.incoming:
                assert spatial_services.coupler is not None
                guarded = spatial.node_states(
                    replace(field_plan, states=pending.spatial_guard_states), spatial_services
                )
                spatial_services.coupler.validate_guards(
                    guarded, pending.plan.spatial_reaction, pending.plan.spatial_guards
                )
            field_packets = spatial.packets(tick, field_plan.outgoing, spatial_services)
        if services.events.enabled:
            services.events.require_room(
                1
                + int(bool(pending.plan.spatial_reaction))
                + len(pending.plan.departures)
                + int(field_plan is not None)
                + sum(p is not None for p in field_packets)
            )
        old_links = self.output.packets
        if any(packet is not None for packet in old_links):
            raise ValueError("outgoing links still occupied; no implicit packet queue is allowed")
        source_records = list(self.records)
        if field_plan is not None:
            for slot, emitted in enumerate(field_plan.emission_records):
                if emitted is not None:
                    source_records[slot] = self._current_emission_state(source_records[slot], emitted)
        records = list(source_records)
        for slot, record in pending.plan.replacements:
            records[slot] = self._current_emission_state(record, source_records[slot])
        departure_tick = bounded(tick + services.initial.link_ticks)
        links: list[Packet | None] = [None] * len(old_links)
        for index, departure in enumerate(pending.plan.departures):
            record = departure.record
            if departure.origin_slot != -1:
                if not 0 <= departure.origin_slot < len(self.records):
                    raise ValueError("departure origin slot exceeds local capacity")
                current = source_records[departure.origin_slot]
                merged = self._current_emission_state(record, current)
                assert merged is not None
                record = merged
            links[index] = Packet(departure_tick, self.position, departure.port, record)
        if spatial is not None and spatial_services is not None and field_plan is None:
            spatial.validate_guards(
                spatial_services, pending.plan.spatial_reaction, pending.plan.spatial_guards
            )
        reaction = (
            None
            if spatial is None or spatial_services is None or field_plan is not None
            else spatial.prepare_reaction(tick, pending.plan.spatial_reaction, spatial_services)
        )
        field_causes = (
            spatial.reaction_causes(outgoing=reaction is not None and reaction.links is not None)
            if services.events.enabled
            and spatial is not None
            and spatial_services is not None
            and (field_plan is not None or pending.plan.spatial_reaction or pending.plan.spatial_guards)
            else ()
        )
        if services.balance_guard is not None:
            before_fields = (
                () if spatial is None else tuple(state.populations for state in spatial.states)
            )
            after_fields = (
                before_fields
                if reaction is None
                else tuple(state.populations for state in reaction.states)
            )
            before_packets = (
                ()
                if spatial is None
                else tuple(packet.fields for packet in spatial.output.packets if packet is not None)
            )
            after_packets = (
                before_packets
                if reaction is None or reaction.links is None
                else tuple(packet.fields for packet in reaction.links if packet is not None)
            )
            services.balance_guard.check(
                LocalInventory(
                    records=self.records, spatial=before_fields, spatial_packets=before_packets
                ),
                LocalInventory(
                    records=tuple(records),
                    spatial=after_fields,
                    carrier_packets=tuple(packet.record for packet in links if packet is not None),
                    spatial_packets=after_packets,
                ),
                "carrier interaction commit",
            )
        # All proposal validation has succeeded; commit coupled records together.
        self.records = tuple(records)
        self.committed_cost = pending.plan.cost
        self.coupling_remainders = pending.plan.coupling_remainders
        self.available_tick = pending.next_tick
        self.pending = None
        if services.initial.node_execution:
            self.delay_counts = services.zero_delays
        self.output.publish(tuple(links))
        if field_plan is not None:
            assert spatial is not None and spatial_services is not None
            spatial.commit_node(
                tick,
                field_plan,
                field_states,
                pending.spatial_phases,
                field_packets,
                pending.plan.spatial_reaction,
                spatial_services,
            )
        elif spatial is not None and spatial_services is not None:
            spatial.commit_reaction(reaction, pending.plan.spatial_reaction, spatial_services)
        services.accounting.record_sources(pending.plan.source_delta)
        notifications: list[dict[str, object]] = []
        committed = self.notify(
            "cycle_committed",
            tick,
            services,
            causes=(() if pending.cause_id is None else (pending.cause_id,)) + field_causes,
            notifications=notifications,
            cost=pending.plan.cost,
            transfers=len(pending.plan.departures),
        )
        if field_plan is not None:
            assert spatial is not None and spatial_services is not None
            cause = spatial._event(
                "spatial_cycle",
                tick,
                spatial_services,
                causes=(committed,),
                notifications=notifications,
                cost=field_plan.cost,
                source_delta={
                    f.name: field_plan.source_delta[i]
                    for i, f in enumerate(services.initial.fields)
                    if any(field_plan.source_delta[i])
                },
                rule_delta={
                    f.name: field_plan.rule_delta[i]
                    for i, f in enumerate(services.initial.fields)
                    if field_plan.rule_delta and any(field_plan.rule_delta[i])
                },
            )
            spatial.cause_id = spatial.cost_cause_id = cause
        if pending.plan.spatial_reaction:
            cause = self.notify(
                "spatial_coupled",
                tick,
                services,
                causes=(),
                event_cost=0,
                notifications=notifications,
                reaction={
                    field.name: values
                    for field, values in zip(
                        services.initial.fields, pending.plan.spatial_reaction, strict=True
                    )
                    if any(values)
                },
                **(
                    {
                        "spatial_departures": tuple(
                            {"port": p.port, "arrival_tick": p.arrival_tick}
                            for p in reaction.links
                            if p is not None
                        )
                    }
                    if reaction is not None and reaction.links is not None
                    else {}
                ),
            )
            if cause is not None and spatial is not None and spatial_services is not None:
                if field_plan is not None:
                    spatial.cause_id = cause
                else:
                    spatial.link_reaction(reaction, cause)
        if field_plan is not None:
            assert spatial is not None and spatial_services is not None
            linked_fields = list(spatial.output.packets)
            for index, field_packet in enumerate(linked_fields):
                if field_packet is not None:
                    cause = spatial._event(
                        "spatial_sent",
                        tick,
                        spatial_services,
                        causes=(spatial.cause_id,),
                        notifications=notifications,
                        port=field_packet.port,
                        arrival_tick=field_packet.arrival_tick,
                    )
                    linked_fields[index] = replace(field_packet, cause_id=cause)
            spatial.output.publish(tuple(linked_fields))
        for index, departure in enumerate(pending.plan.departures):
            cause = self.notify(
                "sent",
                tick,
                services,
                notifications=notifications,
                port=departure.port,
                disturbance=services.initial.disturbances[departure.record.type_index].name,
                values=record_values(services.initial, departure.record),
                arrival_tick=departure_tick,
            )
            if cause is not None:
                linked = list(self.output.packets)
                packet = linked[index]
                assert packet is not None
                linked[index] = replace(packet, cause_id=cause)
                self.output.publish(tuple(linked))
        for event in notifications:
            services.events.publish(event)

    @staticmethod
    def _current_emission_state(
        proposed: DisturbanceRecord | None,
        current: DisturbanceRecord | None,
    ) -> DisturbanceRecord | None:
        """Refresh only independent source bookkeeping in an otherwise frozen proposal."""
        if proposed is None or current is None:
            return proposed
        return replace(
            proposed,
            emission_remainders=current.emission_remainders,
            emission_phases=current.emission_phases,
            emission_remaining=current.emission_remaining,
        )

    def accept_emission(
        self,
        records: tuple[DisturbanceRecord | None, ...],
    ) -> None:
        self._validate_emission_records(self.records, records)
        self.records = records

    @staticmethod
    def _validate_emission_records(
        originals: tuple[DisturbanceRecord | None, ...], records: tuple[DisturbanceRecord | None, ...]
    ) -> None:
        if len(records) != len(originals):
            raise ValueError("spatial emission cannot change disturbance capacity")
        for before, after in zip(originals, records, strict=True):
            if before is None or after is None:
                if before is not after:
                    raise ValueError("spatial emission cannot change disturbance occupancy")
            elif DisturbanceNode._current_emission_state(before, after) != after:
                raise ValueError("spatial emission cannot change a disturbance's physical values")
