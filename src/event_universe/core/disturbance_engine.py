"""Local scheduling and ownership for initialization-defined disturbances."""

from collections.abc import Callable, Mapping
from dataclasses import replace
from functools import wraps
from threading import Lock
from types import MappingProxyType
from typing import Concatenate, Self

from .conservation_state import InventoryNode, InventoryPacket, InventoryView
from .coupling_selectors import selected_type_set
from .disturbance_node import DisturbanceNode
from .disturbance_state import (
    Address3,
    DisturbanceRecord,
    InitialState,
    NodeView,
    Packet,
    bounded,
    decode,
    unpack,
)
from .event_resolution import CausalSourceResolver, CommitResolver, EventResolver, Planner
from .event_space import CausalEventSpace
from .node_boundary import validate_record
from .node_conservation import NodeConservationGuard
from .node_execution import NodeExecution
from .node_ports import PortTable
from .node_services import NodeAccounting, NodeEvents, NodeServices, WorkLedger
from .node_services import cycle_timing as cycle_timing
from .record_policy import RecordPolicy
from .spatial_engine import (
    SpatialCoupler,
    SpatialDecayer,
    SpatialEngine,
    SpatialFieldGuard,
    SpatialPlanner,
)
from .spatial_node import SpatialNode
from .topology import neighbor_address


def _consistent_read[**P, T](
    method: Callable[Concatenate[DisturbanceEngine, P], T],
) -> Callable[Concatenate[DisturbanceEngine, P], T]:
    @wraps(method)
    def read(self: DisturbanceEngine, /, *args: P.args, **kwargs: P.kwargs) -> T:
        if self.event_space is None:
            return method(self, *args, **kwargs)
        with self.event_space.transaction():
            return method(self, *args, **kwargs)

    return read


EventSink = Callable[[dict[str, object]], None]


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
        node_workers: int = 1,
        balance_guard: NodeConservationGuard | None = None,
        field_guard: SpatialFieldGuard | None = None,
    ) -> None:
        if initial.node_execution and (initial.conservation_contract is None or balance_guard is None):
            raise ValueError("node_execution requires a conservation contract and balance guard")
        self.initial = initial
        self._execution = NodeExecution(node_workers, planner, spatial_planner)
        self._step_lock = Lock()
        if self._execution.parallel and resolver is not None:
            raise ValueError("parallel Node execution does not support an event program")
        if resolver is not None and event_space is None:
            raise ValueError("an event resolver requires a shared event space")
        self.event_space = event_space
        if event_space is not None:
            event_space.seal_streams()
        self._resolver = resolver
        self._work = WorkLedger()
        self._planner = planner
        self._record_policy = record_policy
        self._observer = observer
        self._nodes: dict[Address3, DisturbanceNode] = {}
        self._links: PortTable[Packet] = PortTable((None,) * (6 * initial.slots_per_node))
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
                balance_guard=balance_guard,
                field_guard=field_guard,
            )
        )
        self._services = NodeServices(
            replace(initial, seeds=(), spatial_seeds=()),
            planner,
            record_policy,
            NodeEvents(event_space, observer),
            NodeAccounting(self._work, self._source_totals),
            self._coupled_types,
            (0,) * 6,
            resolver,
            balance_guard,
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
                self._emit("source", position)
            # Quantum-only Nodes own the same bounded local handles, without
            # inventing carrier source events or activating ordinary cycles.
            for position in self.event_space.stream_addresses:
                self._at(position)
        if isinstance(resolver, CausalSourceResolver):
            for position, source_node in resolver.source_nodes().items():
                self._at(position).source_envelope = source_node

    @property
    def _observer(self) -> EventSink | None:
        return self._event_observer

    @_observer.setter
    def _observer(self, observer: EventSink | None) -> None:
        self._event_observer = observer
        if hasattr(self, "_services"):
            self._services.events.set_observer(observer)

    @property
    @_consistent_read
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
                    node.arrival_mask,
                    node.delay_counts,
                    node.committed_cost,
                    tuple((cursor.stream_id, cursor.head) for cursor in node.event_cursors),
                    () if node.event_references is None else node.event_references.origins,
                )
                for position, node in self._nodes.items()
            }
        )

    @_consistent_read
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
                ()
                if spatial is None or position not in spatial.nodes
                else spatial.nodes[position].incoming,
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
            capacity = self.initial.slots_per_node
            self._nodes[position] = DisturbanceNode(
                (None,) * capacity,
                (1,) * (len(self.initial.couplings) * capacity * capacity * 3),
                position=position,
                output=self._links.bank(position),
                arrival_mask=(0,) * 6,
                delay_counts=(0,) * 6,
                event_cursors=() if self.event_space is None else self.event_space.cursors_at(position),
                event_references=None
                if self.event_space is None
                else self.event_space.references_at(position),
            )
        return self._nodes[position]

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
            message = {"event": event, "tick": self.tick, "position": position, **data}
            if notifications is None:
                self._observer(message)
            else:
                notifications.append(message)
        return identity

    def _record_cause(self, position: Address3) -> int | None:
        node = self._nodes.get(position)
        return None if node is None else node.cause_id

    def _commit_emission_cause(self, position: Address3, cause: int) -> None:
        self._nodes[position].cause_id = cause

    @_consistent_read
    def computation_report(self) -> dict[str, object]:
        """Every begun local cycle is charged once, even while waiting or in flight."""
        report: dict[str, object] = {
            "model_operations_cost": self._work.work,
            "local_cycles_started": self._work.cycles,
        }
        if self.event_space is not None:
            report["carrier_model_operations_cost"] = self._work.work
            report["model_operations_cost"] = self.event_space.model_cost
            report["causal_events"] = self.event_space.next_id
            report["causal_event_capacity"] = self.event_space.capacity
            report["event_ledger_cost"] = self.event_space.model_cost
        if self._resolver is not None:
            report["resolver"] = self._resolver.report()
        return report

    def execution_report(self) -> dict[str, object]:
        """Report host scheduling separately from modeled local computation cost."""
        return self._execution.report()

    def close(self) -> None:
        """Release host worker interpreters without changing simulation state."""
        if not self._step_lock.acquire(blocking=False):
            raise RuntimeError("cannot close a simulation while a tick is running")
        try:
            self._execution.close()
        finally:
            self._step_lock.release()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, _type: object, _value: object, _traceback: object) -> None:
        self.close()

    def _local_spatial(self, position: Address3, node: DisturbanceNode) -> SpatialNode | None:
        spatial = None if self._spatial is None else self._spatial.nodes.get(position)
        if (
            self._spatial is not None
            and spatial is None
            and (
                self.initial.spatial_computation_delay
                or any(
                    record is not None and record.type_index in self._coupled_types
                    for record in node.records
                )
            )
        ):
            spatial = self._spatial._at(position)
        return spatial

    def _begin(self, position: Address3, node: DisturbanceNode) -> None:
        spatial = self._local_spatial(position, node)
        services = None if self._spatial is None else self._spatial._services
        node._begin(self.tick, self._services, spatial, services)

    def _commit(self, position: Address3, node: DisturbanceNode) -> None:
        spatial = None if self._spatial is None else self._spatial.nodes.get(position)
        services = None if self._spatial is None else self._spatial._services
        node.advance(
            self.tick, self._services, window_closed=True, spatial=spatial, spatial_services=services
        )

    _current_emission_state = staticmethod(DisturbanceNode._current_emission_state)

    def _commit_emission_records(
        self, position: Address3, records: tuple[DisturbanceRecord | None, ...]
    ) -> None:
        node = self._nodes.get(position)
        if node is None:
            if records:
                raise ValueError("spatial emission cannot create disturbance records")
            return
        node.accept_emission(records)

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
                    if packet.origin != origin:
                        raise ValueError("carrier packet origin differs from its link owner")
                    validate_record(self.initial, packet.record)
                    target = self.neighbor(origin, packet.port)
                    if target is None:
                        self._escape(origin, slot, packet)
                    else:
                        ready.setdefault(target, []).append((origin, slot, packet))
        for position, deliveries in sorted(ready.items()):
            if self.event_space is not None:
                self.event_space.require_room(len(deliveries))
            node = self._at(position)
            batch = tuple(packet for _, _, packet in deliveries)
            node.receive(
                batch,
                self.tick,
                self._services,
                spatial=None if self._spatial is None else self._spatial.nodes.get(position),
            )
            for origin, slot, _packet in deliveries:
                links = list(self._links[origin])
                links[slot] = None
                self._links[origin] = tuple(links)
            # Transport releases the complete batch before diagnostic callbacks.
            node.acknowledge_receipt(batch, self.tick, self._services)

    def step(self) -> None:
        if not self._step_lock.acquire(blocking=False):
            raise RuntimeError("only one caller may advance a simulation tick")
        try:
            if self.event_space is None:
                self._step()
            else:
                with self.event_space.transaction():
                    self._step()
        finally:
            self._step_lock.release()

    def _step(self) -> None:
        if self.faulted:
            raise RuntimeError("a failed disturbance simulation cannot continue")
        try:
            readings: dict[Address3, dict[str, dict[str, object]]] | None = None
            if isinstance(self._resolver, CausalSourceResolver):
                if self._spatial is None:
                    raise ValueError("causal source owner requires spatial fields")
                # The local field values present at the start of this cycle;
                # a field-dependent gate scheduled this tick reads only these.
                readings = {
                    position: self._spatial.values(position)
                    for position in self._resolver.source_nodes()
                }
                for position in self._resolver.source_nodes():
                    spatial_node = self._spatial._at(position)
                    proposal = self._resolver.prepare_source(
                        position, self.tick, spatial_node.states, self._nodes[position].last_cost
                    )
                    if proposal is not None:
                        notifications = self._spatial.commit_source(position, self.tick, proposal)
                        self._resolver.commit_source(position, self.tick)
                        self._spatial._notify(notifications)
            if self._spatial is not None and not self.initial.spatial_computation_delay:
                self._spatial.begin(
                    self.tick,
                    self._nodes,
                    execution=self._execution,
                )
                if self.initial.field_phase_first:
                    # The field phase completes its links before any carrier samples them.
                    self._spatial.deliver(self.tick, self._nodes)
                    self._spatial.freeze_samples(self._nodes)
            positions = set(self._nodes)
            if self._spatial is not None and self.initial.spatial_computation_delay:
                positions.update(self._spatial._active)
            ordered = tuple(sorted(positions))
            if self._execution.parallel:
                cycles = []
                for position in ordered:
                    node = self._at(position)
                    spatial = self._local_spatial(position, node)
                    cycles.append(
                        node.parallel_cycle(
                            self.tick,
                            self._services,
                            spatial,
                            None if self._spatial is None else self._spatial._services,
                        )
                    )
                self._execution.finish_cycles(tuple(cycles))
            else:
                for position in ordered:
                    node = self._at(position)
                    self._begin(position, node)
                    self._commit(position, node)
            if isinstance(self._resolver, CausalSourceResolver):
                self._resolver.start_sources(
                    self.tick, None if readings is None else readings.__getitem__
                )
            if self.initial.arrival_port_blind:
                # The entry-port exclusion applies only to the arrival interval's sample.
                for node in self._nodes.values():
                    node.arrival_port_codes = ()
            self.tick = bounded(self.tick + 1)
            if self._spatial is not None:
                # Under field_phase_first only carrier reactions still arrive here.
                self._spatial.deliver(self.tick, self._nodes)
            self._deliver()
            if self._spatial is not None:
                self._spatial.close(self.tick, self._nodes)
            if isinstance(self._resolver, CommitResolver):
                self._resolver.begin_tick(self.tick)
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

    @_consistent_read
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
        if isinstance(self._resolver, CommitResolver):
            for i, components in enumerate(self._resolver.inventory()):
                for c, value in enumerate(components):
                    values[i][c] += value
        return {
            field.name: tuple(values[i])
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    @_consistent_read
    def source_totals(self) -> dict[str, tuple[int, ...]]:
        return {
            field.name: tuple(
                value + (0 if self._spatial is None else self._spatial.sources[i][c])
                for c, value in enumerate(self._source_totals[i])
            )
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    @_consistent_read
    def spatial_values(self, position: Address3) -> dict[str, dict[str, object]]:
        """Read the independent spatial state without inferring source identity."""
        if any(not 0 <= v < n for v, n in zip(position, self.initial.shape, strict=True)):
            raise ValueError("spatial sample position must be within shape")
        return {} if self._spatial is None else self._spatial.values(position)

    @_consistent_read
    def dissipation_totals(self) -> dict[str, tuple[int, ...]]:
        """Signed loss from tracked fields; this diagnostic is not physical inventory."""
        return {
            field.name: (
                (0,) * field.components if self._spatial is None else tuple(self._spatial.dissipation[i])
            )
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    @_consistent_read
    def localized_totals(self) -> dict[str, tuple[int, ...]]:
        """Stationary stock deposited by localizing decay; it is counted in totals()."""
        return {
            field.name: (
                (0,) * field.components if self._spatial is None else tuple(self._spatial.localized[i])
            )
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    @_consistent_read
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

    @_consistent_read
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

    @_consistent_read
    def snapshot(self) -> dict[str, object]:
        """Plain data for headless reports or an explicitly requested renderer."""
        return {
            **({} if self._spatial is None else self._spatial.snapshot()),
            "tick": self.tick,
            "boundary": self.initial.boundary,
            "escaped_totals": self.escaped_totals(),
            "nodes": [
                {
                    "position": position,
                    "cost": node.last_cost,
                    "committed_cost": node.committed_cost,
                    "arrival_mask": node.arrival_mask,
                    "delay_counts": node.delay_counts,
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
                if not node.event_cursors or node.cause_id is not None
            ],
            **(
                {
                    "event_support": [
                        {"position": position, "origins": origins}
                        for position, node in sorted(self._nodes.items())
                        if node.event_references is not None
                        and (
                            origins := tuple(
                                origin
                                for origin in node.event_references.origins
                                if self.event_space.resolution(origin) is None
                            )
                        )
                    ]
                }
                if self.event_space is not None
                and any(node.event_references is not None for node in self._nodes.values())
                else {}
            ),
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
