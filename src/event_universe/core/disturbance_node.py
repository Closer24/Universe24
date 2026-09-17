"""A bounded Node owns carrier transitions and its local outgoing port bank."""

from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

from .coupling_selectors import matches_type
from .disturbance_state import (
    Address3,
    DisturbanceNodeState,
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    Packet,
    PendingCycle,
    bounded,
    pack,
    unpack,
)
from .event_resolution import CommitResolver, LocalContext
from .integer import checked_work
from .node_boundary import validate_local_plan, validate_record, validate_records
from .node_conservation import LocalInventory
from .node_execution import DisturbancePlanningInput, PlanningCycle, PlanningResult, finish_local_cycle
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

    def can_sleep(self, services: NodeServices) -> bool:
        """Certify a no-op carrier visit from this Node's own bounded state.

        A resolver or a shared field clock may own autonomous work; those paths
        retain their ordinary scheduler. Nonempty records and pending cycles
        stay awake even when their next completion is several ticks away.
        """
        return (
            services.resolver is None
            and not services.initial.spatial_computation_delay
            and self.pending is None
            and all(record is None for record in self.records)
            and not (services.initial.node_execution and any(self.delay_counts))
            and not services.record_policy.has_work(self.records)
        )

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
        notifications: list[dict[str, object]] | None = None,
        **data: object,
    ) -> None:
        message = services.events.message(event, tick, self.position, **data)
        if notifications is None:
            services.events.publish(message)
        else:
            notifications.append(message)

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
        arrivals = tuple(packet.record for packet in packets)
        records = services.record_policy.receive(self.records, arrivals, locked)
        if len(records) != len(self.records):
            raise ValueError("record policy cannot change local capacity")
        # Every arrival was validated above; a policy may place that same immutable
        # object into a free slot. Any other new record, such as a merge, is checked.
        validate_records(initial, records, len(self.records), self.records, arrivals)
        if any(records[slot] != self.records[slot] for slot in locked):
            raise ValueError("record policy cannot change a pending local slot")
        if initial.arrival_port_blind:
            codes = list(self.arrival_port_codes) or [0] * len(records)
            for packet in packets:
                for slot, record in enumerate(records):
                    if record is packet.record:
                        codes[slot] = packet.port + 1
            self.arrival_port_codes = tuple(codes)
        received = bounded(self.received_count + len(packets))
        if services.balance_guard is not None:
            fields = () if spatial is None else tuple(state.populations for state in spatial.states)
            services.balance_guard.check(
                LocalInventory(records=self.records, spatial=fields, carrier_packets=arrivals),
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
        finish_local_cycle(
            self.plan_cycle(tick, services, spatial, spatial_services),
            services.planner,
            None if spatial_services is None else spatial_services.planner,
        )

    def parallel_cycle(
        self,
        tick: int,
        services: NodeServices,
        spatial: SpatialNode | None,
        spatial_services: SpatialServices | None,
    ) -> PlanningCycle:
        """Keep the start/commit event order after each common planning barrier."""
        child = self.plan_cycle(tick, services, spatial, spatial_services)
        result: PlanningResult = None
        completed = False
        try:
            for _ in range(2 if services.initial.spatial_computation_delay else 1):
                try:
                    request = None if completed else child.send(result)
                except StopIteration:
                    completed, request = True, None
                result = yield request
            if not completed:
                try:
                    child.send(result)
                except StopIteration:
                    pass
                else:
                    raise RuntimeError("local planning exceeded its fixed phase count")
            self.advance(
                tick, services, window_closed=True, spatial=spatial, spatial_services=spatial_services
            )
        finally:
            child.close()

    def plan_cycle(
        self,
        tick: int,
        services: NodeServices,
        spatial: SpatialNode | None,
        spatial_services: SpatialServices | None,
    ) -> PlanningCycle:
        """Own the transition and expose only frozen local planning inputs to workers."""
        if spatial is not None and spatial.position != self.position:
            raise ValueError("carrier and spatial components must belong to the same Node")
        if self.pending is not None or self.available_tick > tick:
            return
        if services.initial.spatial_computation_delay:
            assert spatial is not None and spatial_services is not None
            yield from self._begin_shared(tick, services, spatial, spatial_services)
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
                )
            )
        ):
            return
        coupled = (
            spatial.couple(
                self.records,
                spatial_services,
                tick,
                {slot: code - 1 for slot, code in enumerate(self.arrival_port_codes) if code}
                if services.initial.arrival_port_blind
                else None,
            )
            if spatial is not None
            and spatial_services is not None
            and any(r is not None and r.type_index in services.coupled_types for r in self.records)
            else None
        )
        port_loads: tuple[int, ...] = (0, 0, 0, 0, 0, 0)
        if services.initial.least_delay_routing and spatial is not None and spatial_services is not None:
            port_loads = tuple(spatial.directional_load(port, spatial_services) for port in range(6))
        context = LocalContext(
            tick,
            self.position,
            self.records if coupled is None else coupled.records,
            self.coupling_remainders,
            self.received_count,
            port_loads,
        )
        if services.resolver is None:
            plan = yield DisturbancePlanningInput(
                context.records, context.residuals, context.received, port_loads
            )
            if not isinstance(plan, LocalPlan):
                raise ValueError("carrier planning requires a LocalPlan")
        else:
            plan = services.resolver.resolve(context, services.planner)
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
        if (
            extra
            and spatial_services is not None
            and any(
                self._ray_owned_fields(record, spatial_services.initial)
                for record in self.records
                if record is not None
            )
        ):
            raise ValueError(
                "funded ray emission or absorption does not support a delayed carrier cycle"
            )
        delays: tuple[int, ...] = ()
        if (
            services.initial.delay_direction is not None
            and spatial is not None
            and spatial_services is not None
        ):
            # Each departure prices the computation load travelling along or against it;
            # the extra wait beyond the local cycle is spent before its arrival.
            delays = tuple(
                max(
                    0,
                    cycle_timing(
                        bounded(
                            checked_work(
                                plan.cost + spatial.directional_load(departure.port, spatial_services)
                            )
                        ),
                        services.initial.normal_budget,
                        services.initial.link_ticks,
                    )[0]
                    - extra,
                )
                for departure in plan.departures
            )
            duration = bounded(checked_work(duration + max(delays, default=0)))
        services.accounting.charge_cycle(plan.cost)
        pending = PendingCycle(
            bounded(tick + extra), bounded(tick + duration), plan, departure_delays=delays
        )
        if services.initial.node_execution and coupled is not None and spatial is not None:
            spatial.consume_sample()
        # Originals remain in their occupied slots throughout the local wait.
        self.pending = pending
        self.received_count = 0
        self.last_cost = plan.cost
        self.arrival_mask = (0,) * port_count(services.initial)
        self.delay_counts = (extra // services.initial.link_ticks,) * port_count(services.initial)
        self.notify(
            "cycle_started",
            tick,
            services,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
        )

    def _begin_shared(
        self, tick: int, services: NodeServices, spatial: SpatialNode, spatial_services: SpatialServices
    ) -> PlanningCycle:
        """Freeze one field/carrier transaction and charge its combined work once."""
        field_plan = yield from spatial.plan_shared_fields(
            self.records, spatial_services, self.committed_cost
        )
        has_carriers = services.record_policy.has_work(self.records)
        if not has_carriers and field_plan.cost == 0:
            spatial.last_cost = 0
            spatial_services.activity.mark(self.position, False)
            return
        # Under the shared clock the computation load delays field forwarding too.
        load = spatial.refresh_load(spatial_services)
        field_plan = replace(
            field_plan,
            cost=bounded(checked_work(field_plan.cost + spatial_services.node_merge_cost + load)),
        )
        self._validate_emission_records(
            self.records,
            field_plan.emission_records,
            initial=spatial_services.initial,
        )
        records = field_plan.emission_records
        coupled = (
            spatial.node_coupling(records, spatial_services)
            if any(
                record is not None and record.type_index in services.coupled_types for record in records
            )
            else None
        )
        zero = tuple((0,) * field.components for field in services.initial.fields)
        request = (
            DisturbancePlanningInput(
                records if coupled is None else coupled.records,
                self.coupling_remainders,
                self.received_count,
            )
            if has_carriers
            else None
        )
        proposed = yield request
        if has_carriers:
            if not isinstance(proposed, LocalPlan):
                raise ValueError("carrier planning requires a LocalPlan")
            plan = proposed
        else:
            plan = LocalPlan((), (), self.coupling_remainders, zero, 0)
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
        services.accounting.charge_cycle(plan.cost)
        self.pending, self.received_count, self.last_cost = pending, 0, plan.cost
        spatial.shared_pending = 1
        spatial.last_cost = field_plan.cost
        self.arrival_mask = (0,) * port_count(services.initial)
        self.delay_counts = (extra // services.initial.link_ticks,) * port_count(services.initial)
        self.notify(
            "cycle_started",
            tick,
            services,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
            spatial_cost=field_plan.cost,
        )

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
            spatial.require_free_links()
            field_states = spatial.node_states(field_plan, spatial_services)
            if pending.spatial_guard_states and spatial.incoming:
                assert spatial_services.coupler is not None
                guarded = spatial.node_states(
                    replace(field_plan, states=pending.spatial_guard_states), spatial_services
                )
                spatial_services.coupler.validate_guards(
                    guarded, pending.plan.spatial_reaction, pending.plan.spatial_guards
                )
            field_packets = spatial.packets(tick, field_plan.outgoing, spatial_services, field_plan.rays)
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
        records = [self._staying(record) for record in records]
        alternatives: list[tuple[DisturbanceRecord | None, ...]] = []
        resolver = services.resolver
        context = LocalContext(tick, self.position, tuple(records), self.coupling_remainders, 0)
        if pending.plan.resolution_token is not None:
            if not isinstance(resolver, CommitResolver):
                raise ValueError("pending resolution requires a commit resolver")
            if pending.plan.departures:
                raise ValueError("deferred alternatives require a local replacement-only cycle")
            options = resolver.alternatives(context, pending.plan.resolution_token)
            if not 1 <= len(options) <= 6:
                raise ValueError("one to six local commit alternatives required")
            reserved = {slot for slot, _ in pending.plan.replacements}
            for option in options:
                if {slot for slot, _ in option} != reserved:
                    raise ValueError("commit alternatives must use exactly the reserved local slots")
                validate_local_plan(
                    services.initial,
                    replace(pending.plan, replacements=option),
                    len(self.coupling_remainders),
                    tuple(source_records),
                )
                proposed = list(source_records)
                for slot, record in option:
                    proposed[slot] = self._current_emission_state(record, source_records[slot])
                validate_records(services.initial, tuple(proposed), len(self.records))
                alternatives.append(tuple(self._staying(record) for record in proposed))
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
            delay = pending.departure_delays[index] if pending.departure_delays else 0
            links[index] = Packet(
                bounded(checked_work(departure_tick + delay)),
                self.position,
                departure.port,
                self._departing(record),
            )
        if spatial is not None and spatial_services is not None and field_plan is None:
            spatial.validate_guards(
                spatial_services, pending.plan.spatial_reaction, pending.plan.spatial_guards
            )
        reaction = (
            None
            if spatial is None or spatial_services is None or field_plan is not None
            else spatial.prepare_reaction(tick, pending.plan.spatial_reaction, spatial_services)
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
        if alternatives:
            assert isinstance(resolver, CommitResolver)
            assert pending.plan.resolution_token is not None
            choice, _ = resolver.commit_choice(
                context, pending.plan.resolution_token, 1 + int(bool(pending.plan.spatial_reaction))
            )
            records = list(alternatives[choice])
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
        self.notify(
            "cycle_committed",
            tick,
            services,
            notifications=notifications,
            cost=pending.plan.cost,
            transfers=len(pending.plan.departures),
        )
        if field_plan is not None:
            assert spatial is not None and spatial_services is not None
            spatial._event(
                "spatial_cycle",
                tick,
                spatial_services,
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
        if pending.plan.spatial_reaction:
            self.notify(
                "spatial_coupled",
                tick,
                services,
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
        if field_plan is not None:
            assert spatial is not None and spatial_services is not None
            for field_packet in spatial.output.packets:
                if field_packet is not None:
                    spatial._event(
                        "spatial_sent",
                        tick,
                        spatial_services,
                        notifications=notifications,
                        port=field_packet.port,
                        arrival_tick=field_packet.arrival_tick,
                    )
        for index, departure in enumerate(pending.plan.departures):
            self.notify(
                "sent",
                tick,
                services,
                notifications=notifications,
                port=departure.port,
                disturbance=services.initial.disturbances[departure.record.type_index].name,
                values=record_values(services.initial, departure.record),
                arrival_tick=bounded(
                    checked_work(
                        departure_tick
                        + (pending.departure_delays[index] if pending.departure_delays else 0)
                    )
                ),
            )
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
            emission_last=current.emission_last,
            emission_departed=current.emission_departed,
            absorbed_phases=current.absorbed_phases,
            dissolve_clocks=current.dissolve_clocks,
        )

    @staticmethod
    def _staying(record: DisturbanceRecord | None) -> DisturbanceRecord | None:
        """A record that stays meets none of its own rays on the next cycle."""
        if record is None or not record.emission_last:
            return record
        return replace(record, emission_departed=tuple(pack((0, 0, 0, 0)) for _ in record.emission_last))

    @staticmethod
    def _departing(record: DisturbanceRecord) -> DisturbanceRecord:
        """A departing record carries this cycle's emission to subtract on arrival."""
        if not record.emission_last:
            return record
        return replace(record, emission_departed=record.emission_last)

    def accept_emission(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        *,
        funded: bool = False,
        initial: InitialState | None = None,
    ) -> None:
        self._validate_emission_records(self.records, records, funded=funded, initial=initial)
        self.records = records

    @staticmethod
    def _ray_owned_fields(record: DisturbanceRecord, initial: InitialState) -> set[int]:
        """Fields explicitly writable by this record's funded emission or absorption."""
        allowed: set[int] = set()
        for rule in initial.emissions:
            if rule.funded and matches_type(rule, record.type_index):
                allowed.add(initial.spatial_fields[rule.spatial_field].field)
                if rule.recoil_field is not None:
                    allowed.add(rule.recoil_field)
        for coupling in initial.spatial_couplings:
            if coupling.mode == "absorb" and matches_type(coupling, record.type_index):
                allowed.add(coupling.field)
                if coupling.momentum_field is not None:
                    allowed.add(coupling.momentum_field)
        return allowed

    @staticmethod
    def _validate_emission_records(
        originals: tuple[DisturbanceRecord | None, ...],
        records: tuple[DisturbanceRecord | None, ...],
        *,
        funded: bool = False,
        initial: InitialState | None = None,
    ) -> None:
        if funded and initial is None:
            raise ValueError("funded emission updates require explicit owned field definitions")
        if len(records) != len(originals):
            raise ValueError("spatial emission cannot change disturbance capacity")
        for before, after in zip(originals, records, strict=True):
            if before is None or after is None:
                if before is not after:
                    raise ValueError("spatial emission cannot change disturbance occupancy")
            else:
                allowed = (
                    set() if initial is None else DisturbanceNode._ray_owned_fields(before, initial)
                )
                values = tuple(
                    after.values[index] if index in allowed and index < len(after.values) else value
                    for index, value in enumerate(before.values)
                )
                expected = DisturbanceNode._current_emission_state(replace(before, values=values), after)
                if expected != after:
                    raise ValueError(
                        "spatial emission cannot change unowned values or transport metadata"
                    )
