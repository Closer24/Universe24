"""Local scheduling and ownership for initialization-defined disturbances."""

from collections.abc import Callable, Mapping
from dataclasses import replace
from types import MappingProxyType

from .conservation_state import InventoryNode, InventoryPacket, InventoryView
from .coupling_selectors import selected_type_set
from .disturbance_state import (
    DEFAULT_TOPOLOGY,
    Address3,
    DisturbanceNode,
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    NodeView,
    Packet,
    PendingCycle,
    bounded,
    decode,
    unpack,
)
from .event_resolution import EventResolver, LocalContext
from .event_space import CausalEventSpace
from .integer import ceil_div, checked_work
from .node_state import NodeSnapshot
from .record_policy import RecordPolicy
from .spatial_engine import SpatialCoupler, SpatialDecayer, SpatialEngine, SpatialPlanner
from .topology import (
    inverse_port,
    neighbor_address,
    validate_position,
    validate_topology_configuration,
)

Planner = Callable[[tuple[DisturbanceRecord | None, ...], tuple[int, ...], int], LocalPlan]
EventSink = Callable[[dict[str, object]], None]


def cycle_timing(cost: int, budget: int, link_ticks: int) -> tuple[int, int]:
    if min(budget, link_ticks) < 1 or cost < 0:
        raise ValueError("invalid cost, normal budget, or fixed link time")
    cycles = max(1, ceil_div(cost, budget))
    return bounded(checked_work((cycles - 1) * link_ticks)), bounded(checked_work(cycles * link_ticks))


class DisturbanceEngine:
    """One bounded record schema, one local planner, and configured equal-time links.

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
        validate_topology_configuration(initial)
        if event_space is not None and initial.topology != DEFAULT_TOPOLOGY:
            raise ValueError("causal event_space currently requires cardinal-six-v1 topology")
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
        self._nodes: dict[Address3, DisturbanceNode] = {}
        self._links: dict[Address3, tuple[Packet | None, ...]] = {}
        self._empty_links: tuple[Packet | None, ...] = (None,) * (
            len(initial.topology.offsets) * initial.slots_per_node
        )
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
        self._spatial = (
            None
            if spatial_planner is None or not initial.spatial_fields
            else SpatialEngine(initial, spatial_planner, observer, spatial_coupler, spatial_decayer)
        )
        for seed in initial.seeds:
            node = self._at(seed.position)
            records = list(node.records)
            try:
                slot = records.index(None)
            except ValueError as error:
                raise ValueError("initial disturbance capacity exceeded") from error
            records[slot] = seed.record
            node.records = tuple(records)
        if self.event_space is not None:
            self.event_space.require_room(len(self._nodes))
            for position in sorted(self._nodes):
                self._emit("source", position)

    @property
    def nodes(self) -> Mapping[Address3, NodeView]:
        return MappingProxyType(
            {
                position: NodeView(
                    node.records,
                    node.coupling_remainders,
                    node.pending,
                    node.available_tick,
                    node.received_count,
                    node.last_cost,
                    node.cause_id,
                )
                for position, node in self._nodes.items()
            }
        )

    @property
    def cells(self) -> Mapping[Address3, NodeView]:
        """Legacy read alias for nodes; no second state store."""
        return self.nodes

    def node_view(self, position: Address3) -> NodeSnapshot:
        """Read one node without creating it or scanning any other node.

        Immutable references remain readable after a failed transition.
        Physical validation belongs to commits, not this passive accessor.
        """
        validate_position(position, self.initial.shape, self.initial.topology)
        node = self._nodes.get(position)
        carrier = (
            None
            if node is None
            else NodeView(
                node.records,
                node.coupling_remainders,
                node.pending,
                node.available_tick,
                node.received_count,
                node.last_cost,
                node.cause_id,
            )
        )
        spatial = self._spatial
        return NodeSnapshot(
            position,
            self.tick,
            carrier,
            None if spatial is None else spatial.node_view(position),
            self._links.get(position, self._empty_links),
            () if spatial is None else spatial.links.get(position, spatial.empty_links),
        )

    def inventory_view(self) -> InventoryView:
        """Expose immutable actual owners for host audits, excluding proposal views."""
        spatial = self._spatial
        positions = self._nodes.keys() | ({} if spatial is None else spatial.nodes).keys()
        blank = () if spatial is None else spatial._blank_states()
        nodes = tuple(
            InventoryNode(
                position,
                () if position not in self._nodes else self._nodes[position].records,
                blank
                if spatial is None or position not in spatial.nodes
                else spatial.nodes[position].states,
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

    def _at(self, position: Address3) -> DisturbanceNode:
        if position not in self._nodes:
            validate_position(position, self.initial.shape, self.initial.topology)
            capacity = self.initial.slots_per_node
            self._nodes[position] = DisturbanceNode(
                (None,) * capacity,
                (1,) * (len(self.initial.couplings) * capacity * capacity * 3),
            )
        return self._nodes[position]

    def neighbor(self, origin: Address3, port: int) -> Address3 | None:
        return neighbor_address(
            origin, port, self.initial.shape, self.initial.boundary, self.initial.topology
        )

    def _emit(
        self,
        event: str,
        position: Address3,
        *,
        causes: tuple[int, ...] = (),
        event_cost: int = 0,
        **data: object,
    ) -> int | None:
        identity = None
        if self.event_space is not None:
            node = self._at(position)
            parents = causes if node.cause_id is None else (*causes, node.cause_id)
            entry = self.event_space.append(
                tick=self.tick,
                addresses=(position,),
                owner="disturbance",
                kind=event,
                physical_parents=parents,
                model_cost=event_cost,
            )
            identity = node.cause_id = entry.id
            data = {**data, "event_id": identity, "parents": entry.parents}
        if self._observer is not None:
            self._observer({"event": event, "tick": self.tick, "position": position, **data})
        return identity

    def computation_report(self) -> dict[str, object]:
        """Every begun local cycle is charged once, even while waiting or in flight."""
        report: dict[str, object] = {
            "model_operations_cost": self._model_work,
            "local_cycles_started": self._local_cycles,
        }
        if self.event_space is not None:
            report["causal_events"] = self.event_space.next_id
            report["event_ledger_cost"] = self.event_space.model_cost
        if self._resolver is not None:
            report["resolver"] = self._resolver.report()
        return report

    def _begin(self, position: Address3, node: DisturbanceNode) -> None:
        if node.pending is not None or node.available_tick > self.tick:
            return
        if not self._record_policy.has_work(node.records) and not (
            self._resolver is not None
            and self._resolver.has_work(
                LocalContext(
                    self.tick,
                    position,
                    node.records,
                    node.coupling_remainders,
                    node.received_count,
                    node.cause_id,
                )
            )
        ):
            return
        coupled = (
            self._spatial.couple(position, node.records)
            if self._spatial is not None
            and any(r is not None and r.type_index in self._coupled_types for r in node.records)
            else None
        )
        if self.event_space is not None:
            self.event_space.require_room(1)
        context = LocalContext(
            self.tick,
            position,
            node.records if coupled is None else coupled.records,
            node.coupling_remainders,
            node.received_count,
            node.cause_id,
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
        if len(plan.departures) > self.initial.slots_per_node * self.initial.topology.degree:
            raise ValueError("local rule exceeds fixed outgoing capacity")
        for departure in plan.departures:
            if not 0 <= bounded(departure.port) < self.initial.topology.degree:
                raise ValueError("departure port exceeds configured topology")
        extra, duration = cycle_timing(plan.cost, self.initial.normal_budget, self.initial.link_ticks)
        work = checked_work(self._model_work + plan.cost)
        cycles = checked_work(self._local_cycles + 1)
        pending = PendingCycle(bounded(self.tick + extra), bounded(self.tick + duration), plan)
        # Originals remain in their occupied slots throughout the local wait.
        node.pending = pending
        node.received_count = 0
        node.last_cost = plan.cost
        self._model_work, self._local_cycles = work, cycles
        cause = self._emit(
            "cycle_started",
            position,
            causes=() if plan.cause_id is None else (plan.cause_id,),
            event_cost=plan.cost,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
        )
        node.pending = replace(pending, cause_id=cause)

    def _commit(self, position: Address3, node: DisturbanceNode) -> None:
        pending = node.pending
        if pending is None or pending.ready_tick > self.tick:
            return
        if self.event_space is not None:
            self.event_space.require_room(2 + len(pending.plan.departures))
        old_links = self._links.get(
            position, (None,) * (self.initial.topology.degree * self.initial.slots_per_node)
        )
        if any(packet is not None for packet in old_links):
            raise ValueError("outgoing links still occupied; no implicit packet queue is allowed")
        records = list(node.records)
        for slot, record in pending.plan.replacements:
            records[slot] = self._current_emission_state(record, node.records[slot])
        departure_tick = bounded(self.tick + self.initial.link_ticks)
        links: list[Packet | None] = [None] * len(old_links)
        for index, departure in enumerate(pending.plan.departures):
            record = departure.record
            if departure.origin_slot != -1:
                if not 0 <= departure.origin_slot < len(node.records):
                    raise ValueError("departure origin slot exceeds local capacity")
                current = node.records[departure.origin_slot]
                merged = self._current_emission_state(record, current)
                assert merged is not None
                record = merged
            links[index] = Packet(departure_tick, position, departure.port, record)
        if self._spatial is not None:
            self._spatial.validate_guards(
                position, pending.plan.spatial_reaction, pending.plan.spatial_guards
            )
        reaction = (
            None
            if self._spatial is None
            else self._spatial.prepare_reaction(position, self.tick, pending.plan.spatial_reaction)
        )
        # All proposal validation has succeeded; commit coupled records together.
        node.records = tuple(records)
        node.coupling_remainders = pending.plan.coupling_remainders
        node.available_tick = pending.next_tick
        node.pending = None
        self._links[position] = tuple(links)
        if self._spatial is not None:
            self._spatial.commit_reaction(position, reaction, pending.plan.spatial_reaction)
        for index, values in enumerate(pending.plan.source_delta):
            for component, delta in enumerate(values):
                self._source_totals[index][component] += delta
        self._emit(
            "cycle_committed",
            position,
            causes=() if pending.cause_id is None else (pending.cause_id,),
            cost=pending.plan.cost,
            transfers=len(pending.plan.departures),
        )
        if pending.plan.spatial_reaction:
            self._emit(
                "spatial_coupled",
                position,
                reaction={
                    field.name: values
                    for field, values in zip(
                        self.initial.fields, pending.plan.spatial_reaction, strict=True
                    )
                    if any(values)
                },
            )
        for index, departure in enumerate(pending.plan.departures):
            cause = self._emit(
                "sent",
                position,
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
        node = self._nodes.get(position)
        if node is None:
            if records:
                raise ValueError("spatial emission cannot create disturbance records")
            return
        if len(records) != len(node.records):
            raise ValueError("spatial emission cannot change disturbance capacity")
        for before, after in zip(node.records, records, strict=True):
            if before is None or after is None:
                if before is not after:
                    raise ValueError("spatial emission cannot change disturbance occupancy")
            elif self._current_emission_state(before, after) != after:
                raise ValueError("spatial emission cannot change a disturbance's physical values")
        node.records = records

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
            node = self._at(position)
            locked = (
                frozenset()
                if node.pending is None
                else frozenset(slot for slot, _ in node.pending.plan.replacements)
            )
            records = self._record_policy.receive(
                node.records, tuple(packet.record for _, _, packet in deliveries), locked
            )
            if len(records) != len(node.records):
                raise ValueError("record policy cannot change local capacity")
            received = bounded(node.received_count + len(deliveries))
            # Validate the whole local arrival event before clearing any packet.
            node.records = records
            node.received_count = received
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
                    port=inverse_port(packet.port, self.initial.topology),
                    disturbance=self.initial.disturbances[packet.record.type_index].name,
                    values=self.record_values(packet.record),
                )

    def step(self) -> None:
        if self.faulted:
            raise RuntimeError("a failed disturbance simulation cannot continue")
        try:
            if self._spatial is not None:
                self._spatial.begin(
                    self.tick,
                    {p: node.records for p, node in self._nodes.items()},
                    self._commit_emission_records,
                )
            for position in sorted(self._nodes):
                node = self._nodes[position]
                self._begin(position, node)
                self._commit(position, node)
            self.tick = bounded(self.tick + 1)
            if self._spatial is not None:
                self._spatial.deliver(self.tick)
            self._deliver()
            for position in sorted(self._nodes):
                self._commit(position, self._nodes[position])
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
        records = [r for node in self._nodes.values() for r in node.records if r is not None]
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
        validate_position(position, self.initial.shape, self.initial.topology)
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
                    "cost": node.last_cost,
                    "available_tick": node.available_tick,
                    "waiting_until": None if node.pending is None else node.pending.ready_tick,
                    "disturbances": [
                        {
                            "type": self.initial.disturbances[r.type_index].name,
                            "values": self.record_values(r),
                            "channel": r.channel_code - 1,
                            **self._bookkeeping(r),
                        }
                        for r in node.records
                        if r is not None
                    ],
                }
                for position, node in sorted(self._nodes.items())
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
