"""Local scheduling and ownership for initialization-defined disturbances."""

from collections.abc import Callable, Mapping
from dataclasses import replace
from types import MappingProxyType

from .conservation_state import InventoryNode, InventoryPacket, InventoryView
from .coupling_selectors import selected_type_set
from .disturbance_node import DisturbanceNode
from .disturbance_state import (
    DEFAULT_TOPOLOGY,
    Address3,
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    NodeView,
    Packet,
    bounded,
    decode,
    unpack,
)
from .event_resolution import EventResolver
from .event_space import CausalEventSpace
from .node_boundary import validate_record
from .node_ports import PortTable
from .node_services import NodeAccounting, NodeEvents, NodeServices, WorkLedger
from .node_services import cycle_timing as cycle_timing
from .node_state import NodeSnapshot
from .record_policy import RecordPolicy
from .spatial_engine import SpatialCoupler, SpatialDecayer, SpatialEngine, SpatialPlanner
from .spatial_node import SpatialNode
from .topology import (
    neighbor_address,
    validate_position,
    validate_topology_configuration,
)

Planner = Callable[[tuple[DisturbanceRecord | None, ...], tuple[int, ...], int], LocalPlan]
EventSink = Callable[[dict[str, object]], None]


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
        self._ledger = WorkLedger()
        self._observer = observer
        self._nodes: dict[Address3, DisturbanceNode] = {}
        self._empty_links: tuple[Packet | None, ...] = (None,) * (
            len(initial.topology.offsets) * initial.slots_per_node
        )
        self._links: PortTable[Packet] = PortTable(self._empty_links)
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
        self._services = NodeServices(
            replace(initial, seeds=(), spatial_seeds=(), event_program=None),
            planner,
            record_policy,
            NodeEvents(event_space, observer),
            NodeAccounting(self._ledger, self._source_totals),
            self._coupled_types,
            (0,) * initial.topology.degree,
            resolver,
        )
        for seed in initial.seeds:
            validate_record(initial, seed.record)
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
                self._at(position).notify("source", self.tick, self._services)

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
                    node.h,
                )
                for position, node in self._nodes.items()
            }
        )

    def set_observer(self, observer: EventSink | None) -> None:
        """Attach a passive sink consistently to both local execution lanes."""
        self._observer = observer
        self._services = replace(self._services, events=NodeEvents(self.event_space, observer))
        if self._spatial is not None:
            self._spatial.observer = observer
            self._spatial.services = replace(self._spatial.services, observer=observer)

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
                node.h,
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
                position=position,
                output=self._links.bank(position),
                h=self._services.zero_delays,
            )
        return self._nodes[position]

    def neighbor(self, origin: Address3, port: int) -> Address3 | None:
        return neighbor_address(
            origin, port, self.initial.shape, self.initial.boundary, self.initial.topology
        )

    def computation_report(self) -> dict[str, object]:
        """Every begun local cycle is charged once, even while waiting or in flight."""
        report: dict[str, object] = {
            "model_operations_cost": self._ledger.work,
            "local_cycles_started": self._ledger.cycles,
        }
        if self.event_space is not None:
            report["causal_events"] = self.event_space.next_id
            report["event_ledger_cost"] = self.event_space.model_cost
        if self._resolver is not None:
            report["resolver"] = self._resolver.report()
        return report

    def _local_spatial(self, position: Address3) -> SpatialNode | None:
        """Bind the local field component without exposing a world to the node."""
        if self._spatial is None:
            return None
        node = self._nodes[position]
        if any(r is not None and r.type_index in self._coupled_types for r in node.records) or (
            node.pending is not None
            and (node.pending.plan.spatial_reaction or node.pending.plan.spatial_guards)
        ):
            return self._spatial._at(position)
        return self._spatial.nodes.get(position)

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
        self._at(origin).notify(
            "escaped",
            self.tick,
            self._services,
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
                    if packet.origin != origin:
                        raise ValueError("carrier packet origin differs from its link owner")
                    target = self.neighbor(origin, packet.port)
                    if target is None:
                        validate_record(self.initial, packet.record)
                        self._escape(origin, slot, packet)
                    else:
                        ready.setdefault(target, []).append((origin, slot, packet))
        for position, deliveries in sorted(ready.items()):
            node = self._at(position)
            incoming_packets = tuple(packet for _, _, packet in deliveries)
            node.receive(incoming_packets, self.tick, self._services)
            for origin, slot, _packet in deliveries:
                links = list(self._links[origin])
                links[slot] = None
                self._links[origin] = tuple(links)
            # Ownership is complete before an external observer can fail.
            node.acknowledge_receipt(incoming_packets, self.tick, self._services)

    def step(self) -> None:
        if self.faulted:
            raise RuntimeError("a failed disturbance simulation cannot continue")
        try:
            if self._spatial is not None:
                self._spatial.begin(self.tick, self._nodes)
            for position in sorted(self._nodes):
                node = self._nodes[position]
                node.advance(
                    self.tick,
                    self._services,
                    spatial=self._local_spatial(position),
                    spatial_services=None if self._spatial is None else self._spatial.services,
                )
            self.tick = bounded(self.tick + 1)
            if self._spatial is not None:
                self._spatial.deliver(self.tick)
            self._deliver()
            for position in sorted(self._nodes):
                self._nodes[position].advance(
                    self.tick,
                    self._services,
                    window_closed=True,
                    spatial=self._local_spatial(position),
                    spatial_services=None if self._spatial is None else self._spatial.services,
                )
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
