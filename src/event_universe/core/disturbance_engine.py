"""Local scheduling and ownership for initialization-defined disturbances."""

from collections.abc import Callable, Mapping
from dataclasses import replace
from types import MappingProxyType

from .conservation_state import InventoryNode, InventoryPacket, InventoryView
from .coupling_selectors import selected_type_set
from .disturbance_state import (
    Address3,
    CellView,
    DisturbanceCell,
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    Packet,
    PendingCycle,
    bounded,
    decode,
    unpack,
)
from .event_resolution import EventResolver, LocalContext
from .event_space import CausalEventSpace
from .integer import ceil_div, checked_work
from .record_policy import RecordPolicy
from .spatial_engine import SpatialCoupler, SpatialDecayer, SpatialEngine, SpatialPlanner
from .spatial_state import SpatialPacket, SpatialState
from .topology import neighbor_address

Planner = Callable[[tuple[DisturbanceRecord | None, ...], tuple[int, ...], int], LocalPlan]
EventSink = Callable[[dict[str, object]], None]


def cycle_timing(cost: int, budget: int, link_ticks: int) -> tuple[int, int]:
    if min(budget, link_ticks) < 1 or cost < 0:
        raise ValueError("invalid cost, normal budget, or fixed link time")
    cycles = max(1, ceil_div(cost, budget))
    return bounded(checked_work((cycles - 1) * link_ticks)), bounded(checked_work(cycles * link_ticks))


class DisturbanceEngine:
    """One bounded record schema, one local planner, and six equal-time links.

    Physical-name semantics are absent. Measurements may inspect totals but never
    drive the planner. A capacity failure stops the run without dropping records.
    Completed local events need not roll back when a later independent event fails.
    """

    def __init__(
        self,
        initial: InitialState,
        planner: Planner,
        observer: EventSink | None = None,
        spatial_planner: SpatialPlanner | None = None,
        spatial_coupler: SpatialCoupler | None = None,
        spatial_decayer: SpatialDecayer | None = None,
        *,
        record_policy: RecordPolicy,
        event_space: CausalEventSpace | None = None,
        resolver: EventResolver | None = None,
    ) -> None:
        self.initial = initial
        if resolver is not None and event_space is None:
            raise ValueError("an event resolver requires a shared event space")
        self.event_space = event_space
        self._resolver = resolver
        self._model_work = 0
        self._local_cycles = 0
        self._planner = planner
        self._record_policy = record_policy
        self._observer = observer
        self._cells: dict[Address3, DisturbanceCell] = {}
        self._links: dict[Address3, tuple[Packet | None, ...]] = {}
        self.tick = 0
        self.faulted = False
        self._source_totals = [[0] * f.components for f in initial.fields]
        self._escaped_totals = [[0] * f.components for f in initial.fields]
        self._coupled_types = selected_type_set(initial.spatial_couplings, initial.spatial_interactions)
        if initial.spatial_fields and spatial_planner is None:
            raise ValueError("spatial fields require an explicitly composed spatial planner")
        if (initial.spatial_couplings or initial.spatial_interactions) and spatial_coupler is None:
            raise ValueError("spatial couplings require an explicitly composed response law")
        if initial.schema_version == 2 and initial.spatial_fields and spatial_decayer is None:
            raise ValueError("schema 2 spatial fields require an explicitly composed decay law")
        if self.event_space is not None:
            self.event_space.require_room(
                len({s.position for s in initial.seeds})
                + len({s.position for s in initial.spatial_seeds})
            )
        self._spatial = (
            None
            if spatial_planner is None or not initial.spatial_fields
            else SpatialEngine(
                initial,
                spatial_planner,
                observer,
                spatial_coupler,
                spatial_decayer,
                event_space=event_space,
            )
        )
        for seed in initial.seeds:
            cell = self._at(seed.position)
            records = list(cell.records)
            try:
                slot = records.index(None)
            except ValueError as error:
                raise ValueError("initial disturbance capacity exceeded") from error
            records[slot] = seed.record
            cell.records = tuple(records)
        if self.event_space is not None:
            self.event_space.require_room(len(self._cells))
            for position in sorted(self._cells):
                self._emit("source", position)

    @property
    def cells(self) -> Mapping[Address3, CellView]:
        return MappingProxyType(
            {
                position: CellView(
                    cell.records,
                    cell.coupling_remainders,
                    cell.pending,
                    cell.available_tick,
                    cell.received_count,
                    cell.last_cost,
                )
                for position, cell in self._cells.items()
            }
        )

    def inventory_view(self) -> InventoryView:
        """Expose immutable actual owners for host audits, excluding proposal views."""
        spatial = self._spatial
        positions = self._cells.keys() | ({} if spatial is None else spatial.cells).keys()
        blank = () if spatial is None else spatial._blank_states()
        nodes = tuple(
            InventoryNode(
                position,
                () if position not in self._cells else self._cells[position].records,
                blank
                if spatial is None or position not in spatial.cells
                else spatial.cells[position].states,
                ()
                if spatial is None or position not in spatial.cells
                else spatial.cells[position].incoming,
            )
            for position in sorted(positions)
        )
        packets = [
            InventoryPacket(
                "carrier", origin, slot, packet.port, packet.arrival_tick, record=packet.record
            )
            for origin, links in self._links.items()
            for slot, packet in enumerate(links)
            if packet is not None
        ]
        if spatial is not None:
            packets.extend(
                InventoryPacket(
                    "spatial", origin, slot, packet.port, packet.arrival_tick, spatial=packet.fields
                )
                for origin, links in spatial.links.items()
                for slot, packet in enumerate(links)
                if packet is not None
            )
        return InventoryView(nodes, tuple(packets))

    @property
    def links(self) -> Mapping[Address3, tuple[Packet | None, ...]]:
        return MappingProxyType(self._links)

    def _at(self, position: Address3) -> DisturbanceCell:
        if position not in self._cells:
            capacity = self.initial.slots_per_cell
            self._cells[position] = DisturbanceCell(
                (None,) * capacity,
                (1,) * (len(self.initial.couplings) * capacity * capacity * 3),
            )
        return self._cells[position]

    def neighbor(self, origin: Address3, port: int) -> Address3 | None:
        return neighbor_address(origin, port, self.initial.shape, self.initial.boundary)

    def _emit(
        self,
        event: str,
        position: Address3,
        *,
        causes: tuple[int, ...] = (),
        event_cost: int = 0,
        notifications: list[dict[str, object]] | None = None,
        **data: object,
    ) -> int | None:
        identity = None
        if self.event_space is not None:
            cell = self._at(position)
            parents = causes if cell.cause_id is None else (*causes, cell.cause_id)
            entry = self.event_space.append(
                tick=self.tick,
                addresses=(position,),
                owner="disturbance",
                kind=event,
                physical_parents=parents,
                model_cost=event_cost,
            )
            identity = cell.cause_id = entry.id
            data = {**data, "event_id": identity, "parents": entry.parents}
        if self._observer is not None:
            message = {"event": event, "tick": self.tick, "position": position, **data}
            if notifications is None:
                self._observer(message)
            else:
                notifications.append(message)
        return identity

    def _record_cause(self, position: Address3) -> int | None:
        cell = self._cells.get(position)
        return None if cell is None else cell.cause_id

    def _commit_emission_cause(self, position: Address3, cause: int) -> None:
        self._cells[position].cause_id = cause

    def computation_report(self) -> dict[str, object]:
        """Every begun local cycle is charged once, even while waiting or in flight."""
        report: dict[str, object] = {
            "model_operations_cost": self._model_work,
            "local_cycles_started": self._local_cycles,
        }
        if self.event_space is not None:
            report["causal_events"] = self.event_space.next_id
            report["causal_event_capacity"] = self.event_space.capacity
            report["event_ledger_cost"] = self.event_space.model_cost
        if self._resolver is not None:
            report["resolver"] = self._resolver.report()
        return report

    def _begin(self, position: Address3, cell: DisturbanceCell) -> None:
        if cell.pending is not None or cell.available_tick > self.tick:
            return
        if self.initial.spatial_computation_delay:
            self._begin_node(position, cell)
            return
        if not self._record_policy.has_work(cell.records) and not (
            self._resolver is not None
            and self._resolver.has_work(
                LocalContext(
                    self.tick,
                    position,
                    cell.records,
                    cell.coupling_remainders,
                    cell.received_count,
                    cell.cause_id,
                )
            )
        ):
            return
        coupled = (
            self._spatial.couple(position, cell.records)
            if self._spatial is not None
            and any(r is not None and r.type_index in self._coupled_types for r in cell.records)
            else None
        )
        if self.event_space is not None:
            self.event_space.require_room(1)
        context = LocalContext(
            self.tick,
            position,
            cell.records if coupled is None else coupled.records,
            cell.coupling_remainders,
            cell.received_count,
            cell.cause_id,
        )
        plan = (
            self._planner(context.records, context.residuals, context.received)
            if self._resolver is None
            else self._resolver.resolve(context, self._planner)
        )
        if coupled is not None:
            plan = replace(
                plan,
                spatial_reaction=coupled.reaction,
                spatial_guards=coupled.guards,
                cost=bounded(checked_work(plan.cost + coupled.cost)),
            )
        if self._spatial is not None:
            plan = replace(
                plan, cost=bounded(checked_work(plan.cost + self._spatial.cost(position, self.tick)))
            )
            plan = self._record_policy.report_cost(plan)
        if len(plan.departures) > self.initial.slots_per_cell * 6:
            raise ValueError("local rule exceeds fixed outgoing capacity")
        extra, duration = cycle_timing(plan.cost, self.initial.normal_budget, self.initial.link_ticks)
        work = checked_work(self._model_work + plan.cost)
        cycles = checked_work(self._local_cycles + 1)
        pending = PendingCycle(bounded(self.tick + extra), bounded(self.tick + duration), plan)
        # Originals remain in their occupied slots throughout the local wait.
        cell.pending = pending
        cell.received_count = 0
        cell.last_cost = plan.cost
        self._model_work, self._local_cycles = work, cycles
        cause = self._emit(
            "cycle_started",
            position,
            causes=(
                (() if plan.cause_id is None else (plan.cause_id,))
                + (
                    self._spatial.cycle_causes(position, self.tick, sampled=coupled is not None)
                    if self.event_space is not None and self._spatial is not None
                    else ()
                )
            ),
            event_cost=plan.cost,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
        )
        cell.pending = replace(pending, cause_id=cause)

    def _begin_node(self, position: Address3, cell: DisturbanceCell) -> None:
        """Freeze one field/carrier transaction and charge its combined work once."""
        spatial = self._spatial
        assert spatial is not None
        field_plan = spatial.node_plan(position, cell.records)
        has_carriers = self._record_policy.has_work(cell.records)
        if not has_carriers and field_plan.cost == 0:
            spatial.cells[position].last_cost = 0
            spatial.cells[position].cost_cause_id = None
            spatial._active.discard(position)
            return
        field_plan = replace(
            field_plan, cost=bounded(checked_work(field_plan.cost + spatial.node_merge_cost))
        )
        self._validate_emission_records(cell.records, field_plan.emission_records)
        records = field_plan.emission_records
        coupled = (
            spatial.node_coupling(position, records)
            if any(record is not None and record.type_index in self._coupled_types for record in records)
            else None
        )
        zero = tuple((0,) * field.components for field in self.initial.fields)
        plan = (
            self._planner(
                records if coupled is None else coupled.records,
                cell.coupling_remainders,
                cell.received_count,
            )
            if has_carriers
            else LocalPlan((), (), cell.coupling_remainders, zero, 0)
        )
        if coupled is not None:
            plan = replace(
                plan,
                spatial_reaction=coupled.reaction,
                spatial_guards=coupled.guards,
                cost=bounded(checked_work(plan.cost + coupled.cost)),
            )
        plan = self._record_policy.report_cost(
            replace(plan, cost=bounded(checked_work(plan.cost + field_plan.cost)))
        )
        if len(plan.departures) > self.initial.slots_per_cell * 6:
            raise ValueError("local rule exceeds fixed outgoing capacity")
        if plan.spatial_guards:
            assert spatial.coupler is not None
            spatial.coupler.validate_guards(
                field_plan.states, plan.spatial_reaction, plan.spatial_guards
            )
        guard_states = field_plan.states if plan.spatial_guards else ()
        reaction = spatial.prepare_reaction(position, self.tick, plan.spatial_reaction, plan=field_plan)
        phases = spatial.cells[position].reaction_phases
        if reaction is not None:
            assert reaction.links is not None
            blank = tuple(s.populations for s in spatial._blank_states())
            field_plan = replace(
                field_plan,
                states=reaction.states,
                outgoing=tuple(blank if p is None else p.fields for p in reaction.links),
            )
            phases = reaction.phases
        extra, duration = cycle_timing(plan.cost, self.initial.normal_budget, self.initial.link_ticks)
        pending = PendingCycle(
            bounded(self.tick + extra),
            bounded(self.tick + duration),
            plan,
            spatial_plan=field_plan,
            spatial_phases=phases,
            spatial_guard_states=guard_states,
        )
        work, cycles = checked_work(self._model_work + plan.cost), checked_work(self._local_cycles + 1)
        if self.event_space is not None:
            self.event_space.require_room(1)
        field_cell = spatial.cells[position]
        field_cause = field_cell.cause_id
        cell.pending, cell.received_count, cell.last_cost = pending, 0, plan.cost
        field_cell.pending = 1
        field_cell.last_cost = field_plan.cost
        self._model_work, self._local_cycles = work, cycles
        cause = self._emit(
            "cycle_started",
            position,
            causes=() if field_cause is None else (field_cause,),
            event_cost=plan.cost,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
            spatial_cost=field_plan.cost,
        )
        cell.pending = replace(pending, cause_id=cause)

    def _commit(self, position: Address3, cell: DisturbanceCell) -> None:
        pending = cell.pending
        if pending is None or pending.ready_tick > self.tick:
            return
        spatial = self._spatial
        field_plan = pending.spatial_plan
        field_states: tuple[SpatialState, ...] = ()
        field_packets: tuple[SpatialPacket | None, ...] = ()
        if field_plan is not None:
            assert spatial is not None
            if any(packet is not None for packet in spatial.links.get(position, ())):
                raise ValueError("outgoing spatial links are occupied")
            field_states = spatial.node_states(position, field_plan)
            if pending.spatial_guard_states and spatial.cells[position].incoming:
                assert spatial.coupler is not None
                guarded = spatial.node_states(
                    position, replace(field_plan, states=pending.spatial_guard_states)
                )
                spatial.coupler.validate_guards(
                    guarded, pending.plan.spatial_reaction, pending.plan.spatial_guards
                )
            field_packets = spatial.packets(position, self.tick, field_plan.outgoing)
        if self.event_space is not None:
            self.event_space.require_room(
                1
                + int(bool(pending.plan.spatial_reaction))
                + len(pending.plan.departures)
                + int(field_plan is not None)
                + sum(p is not None for p in field_packets)
            )
        old_links = self._links.get(position, (None,) * (6 * self.initial.slots_per_cell))
        if any(packet is not None for packet in old_links):
            raise ValueError("outgoing links still occupied; no implicit packet queue is allowed")
        source_records = list(cell.records)
        if field_plan is not None:
            for slot, emitted in enumerate(field_plan.emission_records):
                if emitted is not None:
                    source_records[slot] = self._current_emission_state(source_records[slot], emitted)
        records = list(source_records)
        for slot, record in pending.plan.replacements:
            records[slot] = self._current_emission_state(record, source_records[slot])
        departure_tick = bounded(self.tick + self.initial.link_ticks)
        links: list[Packet | None] = [None] * len(old_links)
        for index, departure in enumerate(pending.plan.departures):
            record = departure.record
            if departure.origin_slot != -1:
                if not 0 <= departure.origin_slot < len(cell.records):
                    raise ValueError("departure origin slot exceeds local capacity")
                current = source_records[departure.origin_slot]
                merged = self._current_emission_state(record, current)
                assert merged is not None
                record = merged
            links[index] = Packet(departure_tick, position, departure.port, record)
        if self._spatial is not None and field_plan is None:
            self._spatial.validate_guards(
                position, pending.plan.spatial_reaction, pending.plan.spatial_guards
            )
        reaction = (
            None
            if self._spatial is None or field_plan is not None
            else self._spatial.prepare_reaction(position, self.tick, pending.plan.spatial_reaction)
        )
        field_causes = (
            self._spatial.reaction_causes(
                position, outgoing=reaction is not None and reaction.links is not None
            )
            if self.event_space is not None
            and self._spatial is not None
            and (field_plan is not None or pending.plan.spatial_reaction or pending.plan.spatial_guards)
            else ()
        )
        # All proposal validation has succeeded; commit coupled records together.
        cell.records = tuple(records)
        cell.coupling_remainders = pending.plan.coupling_remainders
        cell.available_tick = pending.next_tick
        cell.pending = None
        self._links[position] = tuple(links)
        if field_plan is not None:
            assert spatial is not None
            spatial.commit_node(
                position,
                self.tick,
                field_plan,
                field_states,
                pending.spatial_phases,
                field_packets,
                pending.plan.spatial_reaction,
            )
        elif self._spatial is not None:
            self._spatial.commit_reaction(position, reaction, pending.plan.spatial_reaction)
        for index, values in enumerate(pending.plan.source_delta):
            for component, delta in enumerate(values):
                self._source_totals[index][component] += delta
        notifications: list[dict[str, object]] = []
        committed = self._emit(
            "cycle_committed",
            position,
            causes=(() if pending.cause_id is None else (pending.cause_id,)) + field_causes,
            notifications=notifications,
            cost=pending.plan.cost,
            transfers=len(pending.plan.departures),
        )
        if field_plan is not None:
            assert spatial is not None
            cause = spatial._event(
                "spatial_cycle",
                self.tick,
                position,
                causes=(committed,),
                notifications=notifications,
                cost=field_plan.cost,
                source_delta={
                    f.name: field_plan.source_delta[i]
                    for i, f in enumerate(self.initial.fields)
                    if any(field_plan.source_delta[i])
                },
                rule_delta={
                    f.name: field_plan.rule_delta[i]
                    for i, f in enumerate(self.initial.fields)
                    if field_plan.rule_delta and any(field_plan.rule_delta[i])
                },
            )
            spatial.cells[position].cause_id = spatial.cells[position].cost_cause_id = cause
        if pending.plan.spatial_reaction:
            cause = self._emit(
                "spatial_coupled",
                position,
                causes=(),
                event_cost=0,
                notifications=notifications,
                reaction={
                    field.name: values
                    for field, values in zip(
                        self.initial.fields, pending.plan.spatial_reaction, strict=True
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
            if cause is not None and field_plan is not None:
                assert spatial is not None
                spatial.cells[position].cause_id = cause
            elif cause is not None and self._spatial is not None:
                self._spatial.link_reaction(position, reaction, cause)
        if field_plan is not None:
            assert spatial is not None
            linked_fields = list(spatial.links[position])
            for index, field_packet in enumerate(linked_fields):
                if field_packet is not None:
                    cause = spatial._event(
                        "spatial_sent",
                        self.tick,
                        position,
                        causes=(spatial.cells[position].cause_id,),
                        notifications=notifications,
                        port=field_packet.port,
                        arrival_tick=field_packet.arrival_tick,
                    )
                    linked_fields[index] = replace(field_packet, cause_id=cause)
            spatial.links[position] = tuple(linked_fields)
        for index, departure in enumerate(pending.plan.departures):
            cause = self._emit(
                "sent",
                position,
                notifications=notifications,
                port=departure.port,
                disturbance=self.initial.disturbances[departure.record.type_index].name,
                values=self.record_values(departure.record),
                arrival_tick=departure_tick,
            )
            if cause is not None:
                linked = list(self._links[position])
                packet = linked[index]
                assert packet is not None
                linked[index] = replace(packet, cause_id=cause)
                self._links[position] = tuple(linked)
        if self._observer is not None:
            for event in notifications:
                self._observer(event)

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

    def _commit_emission_records(
        self,
        position: Address3,
        records: tuple[DisturbanceRecord | None, ...],
    ) -> None:
        cell = self._cells.get(position)
        if cell is None:
            if records:
                raise ValueError("spatial emission cannot create disturbance records")
            return
        self._validate_emission_records(cell.records, records)
        cell.records = records

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
            elif DisturbanceEngine._current_emission_state(before, after) != after:
                raise ValueError("spatial emission cannot change a disturbance's physical values")

    def _escape(self, origin: Address3, slot: int, packet: Packet) -> None:
        """Complete one terminal link; unused allowances are not physical stock."""
        if self.event_space is not None:
            self.event_space.require_room(1)
        for field, payload in zip(self.initial.fields, packet.record.values, strict=True):
            field.validate(payload)
        values = self.record_values(packet.record)
        for index, payload in enumerate(packet.record.values):
            for component, value in enumerate(unpack(payload)):
                self._escaped_totals[index][component] += value
        links = list(self._links[origin])
        links[slot] = None
        self._links[origin] = tuple(links)
        self._emit(
            "escaped",
            origin,
            causes=() if packet.cause_id is None else (packet.cause_id,),
            port=packet.port,
            disturbance=self.initial.disturbances[packet.record.type_index].name,
            values=values,
        )

    def _deliver(self) -> None:
        ready: dict[Address3, list[tuple[Address3, int, Packet]]] = {}
        for origin, packets in self._links.items():
            for slot, packet in enumerate(packets):
                if packet is not None and packet.arrival_tick == self.tick:
                    target = self.neighbor(origin, packet.port)
                    if target is None:
                        self._escape(origin, slot, packet)
                    else:
                        ready.setdefault(target, []).append((origin, slot, packet))
        for position, deliveries in sorted(ready.items()):
            if self.event_space is not None:
                self.event_space.require_room(len(deliveries))
            cell = self._at(position)
            locked = (
                frozenset()
                if cell.pending is None
                else frozenset(slot for slot, _ in cell.pending.plan.replacements)
            )
            if cell.pending is not None and cell.pending.spatial_plan is not None:
                locked |= frozenset(
                    slot
                    for slot, record in enumerate(cell.pending.spatial_plan.emission_records)
                    if record is not None
                )
            records = self._record_policy.receive(
                cell.records, tuple(packet.record for _, _, packet in deliveries), locked
            )
            if len(records) != len(cell.records):
                raise ValueError("record policy cannot change local capacity")
            received = bounded(cell.received_count + len(deliveries))
            # Validate the whole local arrival event before clearing any packet.
            cell.records = records
            cell.received_count = received
            for origin, slot, _packet in deliveries:
                links = list(self._links[origin])
                links[slot] = None
                self._links[origin] = tuple(links)
            # Ownership is complete before an external observer can fail.
            for _, _, packet in deliveries:
                self._emit(
                    "received",
                    position,
                    causes=() if packet.cause_id is None else (packet.cause_id,),
                    port=packet.port ^ 1,
                    disturbance=self.initial.disturbances[packet.record.type_index].name,
                    values=self.record_values(packet.record),
                )

    def step(self) -> None:
        if self.faulted:
            raise RuntimeError("a failed disturbance simulation cannot continue")
        try:
            if self._spatial is not None and not self.initial.spatial_computation_delay:
                self._spatial.begin(
                    self.tick,
                    {p: cell.records for p, cell in self._cells.items()},
                    self._commit_emission_records,
                    record_cause=self._record_cause if self.event_space is not None else None,
                    commit_cause=self._commit_emission_cause if self.event_space is not None else None,
                )
            positions = set(self._cells)
            if self._spatial is not None and self.initial.spatial_computation_delay:
                positions.update(self._spatial._active)
            for position in sorted(positions):
                cell = self._at(position)
                self._begin(position, cell)
                self._commit(position, cell)
            self.tick = bounded(self.tick + 1)
            if self._spatial is not None:
                self._spatial.deliver(self.tick)
            self._deliver()
            for position in sorted(self._cells):
                self._commit(position, self._cells[position])
            if self._resolver is not None:
                self._resolver.advance(self.tick)
        except Exception:
            self.faulted = True
            raise

    def record_values(self, record: DisturbanceRecord) -> dict[str, tuple[int, ...]]:
        return {
            self.initial.fields[i].name: unpack(record.values[i])
            for i in self.initial.disturbances[record.type_index].fields
        }

    def totals(self) -> dict[str, tuple[int, ...]]:
        """Read-only totals include resident originals during waits and link-owned packets."""
        values = (
            [[0] * field.components for field in self.initial.fields]
            if self._spatial is None
            else self._spatial.totals()
        )
        records = [r for cell in self._cells.values() for r in cell.records if r is not None]
        records.extend(p.record for packets in self._links.values() for p in packets if p is not None)
        for record in records:
            for i, components in enumerate(record.values):
                for c, code in enumerate(components):
                    values[i][c] += decode(code)
        return {
            field.name: tuple(values[i])
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    def source_totals(self) -> dict[str, tuple[int, ...]]:
        return {
            field.name: tuple(
                value + (0 if self._spatial is None else self._spatial.sources[i][c])
                for c, value in enumerate(self._source_totals[i])
            )
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    def spatial_values(self, position: Address3) -> dict[str, dict[str, object]]:
        """Read the independent spatial state without inferring source identity."""
        if any(not 0 <= v < n for v, n in zip(position, self.initial.shape, strict=True)):
            raise ValueError("spatial sample position must be within shape")
        return {} if self._spatial is None else self._spatial.values(position)

    def dissipation_totals(self) -> dict[str, tuple[int, ...]]:
        """Signed loss from tracked fields; this diagnostic is not physical inventory."""
        return {
            field.name: (
                (0,) * field.components if self._spatial is None else tuple(self._spatial.dissipation[i])
            )
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    def escaped_totals(self) -> dict[str, tuple[int, ...]]:
        """Read quantities that completed an open exit, excluding internal bookkeeping."""
        return {
            field.name: tuple(
                value + (0 if self._spatial is None else self._spatial.escaped[index][component])
                for component, value in enumerate(self._escaped_totals[index])
            )
            for index, field in enumerate(self.initial.fields)
            if field.conserved
        }

    def spatial_accounting(self) -> dict[str, dict[str, object]]:
        return {} if self._spatial is None else self._spatial.accounting()

    @staticmethod
    def _bookkeeping(record: DisturbanceRecord) -> dict[str, object]:
        """Expose carried fractions separately from physical inventory for inspection."""
        values = {
            name: tuple(unpack(payload) for payload in payloads)
            for name, payloads in (
                ("emission_remainders", record.emission_remainders),
                ("emission_phases", record.emission_phases),
                ("exchange_remainders", record.exchange_remainders),
                ("spatial_remainders", record.spatial_remainders),
                ("emission_remaining", record.emission_remaining),
                ("spatial_remaining", record.spatial_remaining),
            )
            if payloads
        }
        extra: dict[str, object] = dict(values)
        if any(v != 1 for v in record.route_weight_codes):
            extra.update(
                route_counts=tuple(v - 1 for v in record.route_count_codes),
                route_weights=tuple(v - 1 for v in record.route_weight_codes),
            )
        if record.rate_credit_denominator != 1:
            extra["movement_credit"] = (record.rate_remainder_code - 1, record.rate_credit_denominator)
        return {"bookkeeping": extra} if extra else {}

    def snapshot(self) -> dict[str, object]:
        """Plain data for headless reports or an explicitly requested renderer."""
        return {
            **({} if self._spatial is None else self._spatial.snapshot()),
            "tick": self.tick,
            "boundary": self.initial.boundary,
            "escaped_totals": self.escaped_totals(),
            "cells": [
                {
                    "position": position,
                    "cost": cell.last_cost,
                    "available_tick": cell.available_tick,
                    "waiting_until": None if cell.pending is None else cell.pending.ready_tick,
                    "disturbances": [
                        {
                            "type": self.initial.disturbances[r.type_index].name,
                            "values": self.record_values(r),
                            "channel": r.channel_code - 1,
                            **self._bookkeeping(r),
                        }
                        for r in cell.records
                        if r is not None
                    ],
                }
                for position, cell in sorted(self._cells.items())
            ],
            "transfers": [
                {
                    "origin": p.origin,
                    "target": self.neighbor(p.origin, p.port),
                    "port": p.port,
                    "arrival_tick": p.arrival_tick,
                    "type": self.initial.disturbances[p.record.type_index].name,
                    "values": self.record_values(p.record),
                    **self._bookkeeping(p.record),
                }
                for packets in self._links.values()
                for p in packets
                if p is not None
            ],
        }
