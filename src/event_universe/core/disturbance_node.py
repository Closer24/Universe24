"""A bounded carrier node owns its local transitions and outgoing port bank."""

from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

from .disturbance_state import (
    Address3,
    DisturbanceRecord,
    InitialState,
    Packet,
    PendingCycle,
    bounded,
    unpack,
)
from .disturbance_state import (
    DisturbanceNode as NodeState,
)
from .event_resolution import LocalContext
from .integer import checked_work
from .node_boundary import validate_local_plan, validate_record, validate_records
from .node_ports import PortBank
from .node_services import NodeServices, cycle_timing
from .topology import inverse_port, neighbor_address

if TYPE_CHECKING:
    from .spatial_node import SpatialNode, SpatialServices


def record_values(initial: InitialState, record: DisturbanceRecord) -> dict[str, tuple[int, ...]]:
    return {
        initial.fields[i].name: unpack(record.values[i])
        for i in initial.disturbances[record.type_index].fields
    }


@dataclass(slots=True)
class DisturbanceNode(NodeState):
    """Only this address's records and ports; services contain no world lookup."""

    position: Address3 = (0, 0, 0)
    output: PortBank[Packet] = field(default_factory=lambda: PortBank(()))

    def advance(
        self,
        tick: int,
        services: NodeServices,
        *,
        window_closed: bool = False,
        spatial: SpatialNode | None = None,
        spatial_services: SpatialServices | None = None,
    ) -> None:
        """A closing clock notice completes waiting work even with no arrivals."""
        bounded(tick)
        if tick < 0:
            raise ValueError("node clock must be nonnegative")
        if spatial is not None and spatial.position != self.position:
            raise ValueError("carrier and spatial components must belong to the same node")
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
        **data: object,
    ) -> int | None:
        identity, message = services.events.record(
            event,
            tick,
            self.position,
            self.cause_id,
            causes=causes,
            event_cost=event_cost,
            **data,
        )
        if identity is not None:
            self.cause_id = identity
        services.events.publish(message)
        return identity

    def receive(
        self,
        packets: tuple[Packet, ...],
        tick: int,
        services: NodeServices,
    ) -> None:
        """Validate and accept a transport batch without invoking event services."""
        bounded(tick)
        if tick < 0:
            raise ValueError("node clock must be nonnegative")
        if (
            type(packets) is not tuple
            or len(packets) > len(self.output.packets) * services.initial.topology.degree
        ):
            raise ValueError("node arrival batch exceeds fixed port capacity")
        initial = services.initial
        for packet in packets:
            if type(packet) is not Packet or packet.arrival_tick != tick:
                raise ValueError("node received a packet outside its arrival tick")
            bounded(packet.arrival_tick)
            if (
                neighbor_address(
                    packet.origin, packet.port, initial.shape, initial.boundary, initial.topology
                )
                != self.position
            ):
                raise ValueError("node received a packet addressed to another node")
            validate_record(initial, packet.record)
        services.events.require_room(len(packets))
        locked = (
            frozenset()
            if self.pending is None
            else frozenset(slot for slot, _ in self.pending.plan.replacements)
        )
        records = services.record_policy.receive(
            self.records, tuple(packet.record for packet in packets), locked
        )
        if len(records) != len(self.records):
            raise ValueError("record policy cannot change local capacity")
        validate_records(services.initial, records, len(self.records), self.records)
        if any(records[slot] != self.records[slot] for slot in locked):
            raise ValueError("record policy cannot change a pending local slot")
        received = bounded(self.received_count + len(packets))
        # Validate the whole local arrival event before clearing any packet.
        self.records = records
        self.received_count = received

    def acknowledge_receipt(
        self,
        packets: tuple[Packet, ...],
        tick: int,
        services: NodeServices,
    ) -> None:
        """The transport has released its batch; causal recording may now fail safely."""
        for packet in packets:
            self.notify(
                "received",
                tick,
                services,
                causes=() if packet.cause_id is None else (packet.cause_id,),
                port=inverse_port(packet.port, services.initial.topology),
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
            spatial.couple(self.records, spatial_services)
            if spatial is not None
            and spatial_services is not None
            and any(r is not None and r.type_index in services.coupled_types for r in self.records)
            else None
        )
        if coupled is not None:
            validate_records(services.initial, coupled.records, len(self.records), self.records)
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
            plan = replace(
                plan,
                spatial_reaction=coupled.reaction,
                spatial_guards=coupled.guards,
                cost=bounded(checked_work(plan.cost + coupled.cost)),
            )
        if spatial_services is not None:
            plan = replace(
                plan,
                cost=bounded(
                    checked_work(
                        plan.cost + (0 if spatial is None else spatial.cost(tick, spatial_services))
                    )
                ),
            )
            plan = services.record_policy.report_cost(plan)
        validate_local_plan(services.initial, plan, len(self.coupling_remainders), self.records)
        extra, duration = cycle_timing(
            plan.cost, services.initial.normal_budget, services.initial.link_ticks
        )
        pending = PendingCycle(bounded(tick + extra), bounded(tick + duration), plan)
        delays = (extra,) * services.initial.topology.degree if extra else services.zero_delays
        services.accounting.charge_cycle(plan.cost)
        # Originals remain in their occupied slots throughout the local wait.
        self.pending = pending
        self.received_count = 0
        self.last_cost = plan.cost
        self.h = delays
        cause = self.notify(
            "cycle_started",
            tick,
            services,
            causes=() if plan.cause_id is None else (plan.cause_id,),
            event_cost=plan.cost,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
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
        services.events.require_room(2 + len(pending.plan.departures))
        old_links = self.output.packets
        if any(packet is not None for packet in old_links):
            raise ValueError("outgoing links still occupied; no implicit packet queue is allowed")
        records = list(self.records)
        for slot, record in pending.plan.replacements:
            records[slot] = self._current_emission_state(record, self.records[slot])
        departure_tick = bounded(tick + services.initial.link_ticks)
        links: list[Packet | None] = [None] * len(old_links)
        for index, departure in enumerate(pending.plan.departures):
            record = departure.record
            if departure.origin_slot != -1:
                if not 0 <= departure.origin_slot < len(self.records):
                    raise ValueError("departure origin slot exceeds local capacity")
                current = self.records[departure.origin_slot]
                merged = self._current_emission_state(record, current)
                assert merged is not None
                record = merged
            links[index] = Packet(departure_tick, self.position, departure.port, record)
        if spatial is not None and spatial_services is not None:
            spatial.validate_guards(
                spatial_services, pending.plan.spatial_reaction, pending.plan.spatial_guards
            )
        reaction = (
            None
            if spatial is None or spatial_services is None
            else spatial.prepare_reaction(tick, pending.plan.spatial_reaction, spatial_services)
        )
        # All proposal validation has succeeded; commit coupled records together.
        self.records = tuple(records)
        self.coupling_remainders = pending.plan.coupling_remainders
        self.available_tick = pending.next_tick
        self.pending = None
        self.output.publish(tuple(links))
        if spatial is not None and spatial_services is not None:
            spatial.commit_reaction(reaction, pending.plan.spatial_reaction, spatial_services)
        services.accounting.record_sources(pending.plan.source_delta)
        self.notify(
            "cycle_committed",
            tick,
            services,
            causes=() if pending.cause_id is None else (pending.cause_id,),
            cost=pending.plan.cost,
            transfers=len(pending.plan.departures),
        )
        if pending.plan.spatial_reaction:
            self.notify(
                "spatial_coupled",
                tick,
                services,
                reaction={
                    field.name: values
                    for field, values in zip(
                        services.initial.fields, pending.plan.spatial_reaction, strict=True
                    )
                    if any(values)
                },
            )
        for index, departure in enumerate(pending.plan.departures):
            cause = self.notify(
                "sent",
                tick,
                services,
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
        if len(records) != len(self.records):
            raise ValueError("spatial emission cannot change disturbance capacity")
        for before, after in zip(self.records, records, strict=True):
            if before is None or after is None:
                if before is not after:
                    raise ValueError("spatial emission cannot change disturbance occupancy")
            elif self._current_emission_state(before, after) != after:
                raise ValueError("spatial emission cannot change a disturbance's physical values")
        self.records = records
