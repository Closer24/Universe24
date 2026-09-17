"""Local scheduling and ownership for initialization-defined disturbances."""

from collections.abc import Callable, Mapping
from dataclasses import replace
from threading import Lock
from types import MappingProxyType
from typing import Self

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
from .event_resolution import CommitResolver, EventResolver, Planner
from .integer import checked_work
from .node_boundary import validate_record
from .node_conservation import NodeConservationGuard
from .node_execution import NodeExecution
from .node_ports import PortTable
from .node_services import NodeAccounting, NodeEvents, NodeServices, WorkLedger
from .node_services import cycle_timing as cycle_timing
from .ray_event_audit import ledger_line, world_ledger
from .spatial_engine import (
    SpatialCoupler,
    SpatialDecayer,
    SpatialEngine,
    SpatialFieldGuard,
    SpatialPlanner,
)
from .spatial_node import SpatialNode
from .topology import neighbor_address

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
        resolver: EventResolver | None = None,
        node_workers: int = 1,
        balance_guard: NodeConservationGuard | None = None,
        field_guard: SpatialFieldGuard | None = None,
        reuse_carrier_plans: bool = False,
        reuse_spatial_plans: bool = False,
    ) -> None:
        if initial.node_execution and (initial.conservation_contract is None or balance_guard is None):
            raise ValueError("node_execution requires a conservation contract and balance guard")
        self.initial = initial
        self._execution = NodeExecution(
            node_workers,
            planner,
            spatial_planner,
            reuse_carriers=reuse_carrier_plans,
            reuse_fields=reuse_spatial_plans,
        )
        carrier_planner = self._execution.disturbance if reuse_carrier_plans else planner
        field_planner = self._execution.spatial if reuse_spatial_plans else spatial_planner
        self._step_lock = Lock()
        if self._execution.parallel and resolver is not None:
            raise ValueError("parallel Node execution does not support an event program")
        self._resolver = resolver
        self._work = WorkLedger()
        self._planner = planner
        self._observer = observer
        self._nodes: dict[Address3, DisturbanceNode] = {}
        self._focus_fallback = (
            "event resolver"
            if resolver is not None
            else "shared field clock"
            if initial.spatial_computation_delay
            else None
        )
        self._focus_enabled = initial.focus and self._focus_fallback is None
        self._awake_carriers: set[Address3] = set()
        self._carrier_phase_visits = 0
        self._links: PortTable[Packet] = PortTable((None,) * (6 * initial.slots_per_node))
        self.tick = 0
        self.faulted = False
        self._source_totals = [[0] * f.components for f in initial.fields]
        self._escaped_totals = [[0] * f.components for f in initial.fields]
        # Absorption runs inside the spatial plan; only response rules need the coupler.
        response_rules = tuple(rule for rule in initial.spatial_couplings if rule.mode != "absorb")
        self._coupled_types = selected_type_set(response_rules, initial.spatial_interactions)
        if initial.spatial_fields and spatial_planner is None:
            raise ValueError("spatial fields require an explicitly composed spatial planner")
        if (response_rules or initial.spatial_interactions) and spatial_coupler is None:
            raise ValueError("spatial couplings require an explicitly composed response law")
        if initial.schema_version == 2 and initial.spatial_fields and spatial_decayer is None:
            raise ValueError("schema 2 spatial fields require an explicitly composed decay law")
        self._spatial = (
            None
            if spatial_planner is None or not initial.spatial_fields
            else SpatialEngine(
                initial,
                spatial_planner,
                observer,
                spatial_coupler,
                spatial_decayer,
                balance_guard=balance_guard,
                field_guard=field_guard,
                execution_planner=field_planner,
            )
        )
        self._services = NodeServices(
            replace(initial, seeds=(), spatial_seeds=()),
            carrier_planner,
            selected_type_set(initial.spatial_couplings, initial.spatial_interactions),
            NodeEvents(observer),
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

        # The world ledger's initial lines (ray-event-audit-v1): what the world
        # holds before the first tick, per conserved field and per ray family.
        self._ledger_initial = (self.totals(), self.charge_totals())

    @property
    def _observer(self) -> EventSink | None:
        return self._event_observer

    @_observer.setter
    def _observer(self, observer: EventSink | None) -> None:
        self._event_observer = observer
        if hasattr(self, "_services"):
            self._services.events.set_observer(observer)

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
                    node.arrival_mask,
                    node.delay_counts,
                    node.committed_cost,
                )
                for position, node in self._nodes.items()
            }
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
                ()
                if spatial is None or position not in spatial.nodes
                else spatial.nodes[position].incoming,
                () if spatial is None or position not in spatial.nodes else spatial.nodes[position].rays,
                group=(
                    None
                    if spatial is None or position not in spatial.nodes
                    else spatial.nodes[position].bound_motion
                ),
                remainders=(
                    ()
                    if spatial is None or position not in spatial.nodes
                    else spatial.nodes[position].remainders
                ),
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
                    "spatial",
                    origin,
                    slot,
                    packet.port,
                    packet.arrival_tick,
                    spatial=packet.fields,
                    rays=packet.rays,
                    group=packet.group,
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
        if self._focus_enabled:
            # Actual creation/access, including completed Link delivery, wakes
            # the owner before this tick's commit phase. No future packet is read.
            self._awake_carriers.add(position)
        if position not in self._nodes:
            capacity = self.initial.slots_per_node
            self._nodes[position] = DisturbanceNode(
                (None,) * capacity,
                (1,) * (len(self.initial.couplings) * capacity * capacity * 3),
                position=position,
                output=self._links.bank(position),
                arrival_mask=(0,) * 6,
                delay_counts=(0,) * 6,
            )
        return self._nodes[position]

    def neighbor(self, origin: Address3, port: int) -> Address3 | None:
        return neighbor_address(origin, port, self.initial.shape, self.initial.boundary)

    def _emit(
        self,
        event: str,
        position: Address3,
        *,
        notifications: list[dict[str, object]] | None = None,
        **data: object,
    ) -> None:
        if self._observer is not None:
            message = {"event": event, "tick": self.tick, "position": position, **data}
            if notifications is None:
                self._observer(message)
            else:
                notifications.append(message)

    def computation_report(self) -> dict[str, object]:
        """Every begun local cycle is charged once, even while waiting or in flight."""
        report: dict[str, object] = {
            "model_operations_cost": self._work.work,
            "local_cycles_started": self._work.cycles,
        }
        if self._resolver is not None:
            report["resolver"] = self._resolver.report()
        return report

    def execution_report(self) -> dict[str, object]:
        """Report host scheduling separately from modeled local computation cost."""
        return {
            **self._execution.report(),
            "focus_requested": self.initial.focus,
            "focus_enabled": self._focus_enabled,
            "focus_fallback": self._focus_fallback if self.initial.focus else None,
            "carrier_phase_visits": self._carrier_phase_visits,
            "carrier_transport": self._links.execution_report(),
            "spatial_transport": None
            if self._spatial is None
            else self._spatial.links.execution_report(),
            "awake_carrier_nodes": len(self._awake_carriers)
            if self._focus_enabled
            else len(self._nodes),
        }

    def _sleep_carriers(self, positions: tuple[Address3, ...]) -> None:
        if self._focus_enabled:
            for position in positions:
                if self._nodes[position].can_sleep(self._services):
                    self._awake_carriers.discard(position)

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
        try:
            node.advance(
                self.tick, self._services, window_closed=True, spatial=spatial, spatial_services=services
            )
        finally:
            self._refresh_output(position)

    def _refresh_output(self, position: Address3) -> None:
        self._links.refresh(position)
        if self._spatial is not None:
            self._spatial.links.refresh(position)

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
        """Complete one already validated terminal link; unused allowances are not stock."""
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
            port=packet.port,
            disturbance=self.initial.disturbances[packet.record.type_index].name,
            values=values,
        )

    def _deliver(self) -> None:
        ready: dict[Address3, list[tuple[Address3, int, Packet]]] = {}
        for origin, packets in self._links.active_items():
            for slot, packet in enumerate(packets):
                if packet is not None and packet.arrival_tick == self.tick:
                    if packet.origin != origin:
                        raise ValueError("carrier packet origin differs from its link owner")
                    target = self.neighbor(origin, packet.port)
                    if target is None:
                        # The world boundary is the only receiver of an escaping record.
                        validate_record(self.initial, packet.record)
                        self._escape(origin, slot, packet)
                    else:
                        # The receiving Node validates each delivered record once.
                        ready.setdefault(target, []).append((origin, slot, packet))
        for position, deliveries in sorted(ready.items()):
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
            self._step()
        finally:
            self._step_lock.release()

    def _step(self) -> None:
        if self.faulted:
            raise RuntimeError("a failed disturbance simulation cannot continue")
        try:
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
            positions = set(self._awake_carriers if self._focus_enabled else self._nodes)
            if self._spatial is not None and self.initial.spatial_computation_delay:
                positions.update(self._spatial._active)
            ordered = tuple(sorted(positions))
            self._carrier_phase_visits += 2 * len(ordered)
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
                try:
                    self._execution.finish_cycles(tuple(cycles))
                finally:
                    for position in ordered:
                        self._refresh_output(position)
            else:
                for position in ordered:
                    node = self._at(position)
                    try:
                        self._begin(position, node)
                        self._commit(position, node)
                    except Exception:
                        self._refresh_output(position)
                        raise
            self._sleep_carriers(ordered)
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
            closing = tuple(sorted(self._awake_carriers if self._focus_enabled else self._nodes))
            self._carrier_phase_visits += len(closing)
            for position in closing:
                self._commit(position, self._nodes[position])
            self._sleep_carriers(closing)
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
        if isinstance(self._resolver, CommitResolver):
            for i, components in enumerate(self._resolver.inventory()):
                for c, value in enumerate(components):
                    values[i][c] += value
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

    def localized_totals(self) -> dict[str, tuple[int, ...]]:
        """Stationary stock deposited by localizing decay; it is counted in totals()."""
        return {
            field.name: (
                (0,) * field.components if self._spatial is None else tuple(self._spatial.localized[i])
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

    def annulled_totals(self) -> dict[str, tuple[int, ...]]:
        """Content that left the world at an inverse split in annul mode (inverse-split-v1):
        an explicitly accounted sink, initial = current + escaped + annulled."""
        return {
            field.name: (
                (0,) * field.components if self._spatial is None else tuple(self._spatial.annulled[i])
            )
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    def external_body_totals(self) -> dict[str, tuple[int, ...]]:
        """Content that ended in an external body's sink (external-body-v1), per family:
        an explicitly accounted sink, initial + sources = current + dissipated +
        escaped + annulled + absorbed_by_bodies, the sources holding what the bodies
        released."""
        return {
            field.name: (
                (0,) * field.components if self._spatial is None else tuple(self._spatial.absorbed[i])
            )
            for i, field in enumerate(self.initial.fields)
            if field.conserved
        }

    def external_bodies(self) -> list[dict[str, object]]:
        """Every external body with its Node, momentum, accumulators and sink."""
        return [] if self._spatial is None else self._spatial.external_bodies()

    def external_body_momentum(self) -> tuple[int, int, int]:
        """The bodies' momentum line of the audit."""
        return (0, 0, 0) if self._spatial is None else self._spatial.external_body_momentum()

    def spatial_accounting(self) -> dict[str, dict[str, object]]:
        return {} if self._spatial is None else self._spatial.accounting()

    def charge_totals(self) -> dict[str, int]:
        """The charge readout per ray field, charge x amount over the owners totals()
        reads: the rays resident at active Nodes and in flight on Links
        (wave-ray-family-v1) and, since ray-event-audit-v1, the stock of the
        family a record holds, resident or in transit; read-only, like the other
        totals."""
        if self._spatial is None:
            return {}
        result = self._spatial.charge_totals()
        records = [r for node in self._nodes.values() for r in node.records if r is not None]
        records.extend(p.record for packets in self._links.values() for p in packets if p is not None)
        for definition in self.initial.spatial_fields:
            if not definition.rays or definition.charge == 0:
                continue
            name = self.initial.fields[definition.field].name
            for record in records:
                stock = decode(record.values[definition.field][0])
                result[name] = checked_work(result[name] + checked_work(stock * definition.charge))
        return result

    def escaped_charge_totals(self) -> dict[str, int]:
        """The charge that left the world through an open boundary, per ray field:
        charge x amount of every escaped ray, and of the stock of the family a
        record carried out (ray-event-audit-v1)."""
        if self._spatial is None:
            return {}
        result = self._spatial.escaped_charge_totals()
        for definition in self.initial.spatial_fields:
            if definition.rays and definition.charge:
                name = self.initial.fields[definition.field].name
                stock = self._escaped_totals[definition.field][0]
                result[name] = checked_work(result[name] + checked_work(stock * definition.charge))
        return result

    def audit(self) -> dict[str, object]:
        """The world ledger at the current tick (ray-event-audit-v1): one line per
        conserved field (amount per family, momentum) and one per ray family
        (charge), each reading initial, sourced, current, escaped, annulled and
        absorbed with initial + sourced = current + escaped + annulled + absorbed
        exact, and the external bodies' own lines (count, momentum, charge, sinks).
        Read-only, like the totals it is built from."""
        initial_totals, initial_charge = self._ledger_initial
        totals, sources = self.totals(), self.source_totals()
        # The absorbed line is what the external bodies' sinks took (external-body-v1).
        escaped, annulled, absorbed = (
            self.escaped_totals(),
            self.annulled_totals(),
            self.external_body_totals(),
        )
        fields = {
            name: ledger_line(
                values, sources[name], totals[name], escaped[name], annulled[name], absorbed[name]
            )
            for name, values in initial_totals.items()
        }
        current_charge, escaped_charge = self.charge_totals(), self.escaped_charge_totals()
        charge = {}
        for definition in self.initial.spatial_fields:
            if not definition.rays:
                continue
            name = self.initial.fields[definition.field].name
            # Charge is per quantum, so what a family sourced, annulled or absorbed
            # reads as charge x that amount; the world's and the escaped charge are
            # read over their owners.
            per_quantum = definition.charge
            charge[name] = ledger_line(
                initial_charge[name],
                checked_work(sources.get(name, (0,))[0] * per_quantum),
                current_charge[name],
                escaped_charge[name],
                checked_work(annulled.get(name, (0,))[0] * per_quantum),
                checked_work(absorbed.get(name, (0,))[0] * per_quantum),
            )
        body_charge = 0
        for body in self.initial.external_bodies:
            body_charge = checked_work(body_charge + body.charge)
        bodies = {
            "count": len(self.initial.external_bodies),
            "momentum": self.external_body_momentum(),
            "charge": body_charge,
            "sink": absorbed,
        }
        return world_ledger(self.tick, fields, charge, bodies)

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
