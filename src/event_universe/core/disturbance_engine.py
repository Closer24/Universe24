"""Local scheduling and ownership for initialization-defined disturbances."""

from collections.abc import Callable, Mapping
from dataclasses import replace
from types import MappingProxyType

from .disturbance_state import (
    Address3,
    CellView,
    CouplingDefinition,
    DisturbanceCell,
    DisturbanceRecord,
    InitialState,
    InteractionDefinition,
    LocalPlan,
    Packet,
    PendingCycle,
    bounded,
    decode,
    pack,
    unpack,
)
from .integer import checked_work
from .spatial_engine import SpatialCoupler, SpatialDecayer, SpatialEngine, SpatialPlanner
from .topology import neighbor_address

Planner = Callable[[tuple[DisturbanceRecord | None, ...], tuple[int, ...], int], LocalPlan]
EventSink = Callable[[dict[str, object]], None]


def cycle_timing(cost: int, budget: int, link_ticks: int) -> tuple[int, int]:
    if min(budget, link_ticks) < 1 or cost < 0:
        raise ValueError("invalid cost, normal budget, or fixed link time")
    cycles = max(1, checked_work(cost + budget - 1) // budget)
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
    ) -> None:
        self.initial = initial
        self._planner = planner
        self._observer = observer
        self._cells: dict[Address3, DisturbanceCell] = {}
        self._links: dict[Address3, tuple[Packet | None, ...]] = {}
        self.tick = 0
        self.faulted = False
        self._source_totals = [[0] * f.components for f in initial.fields]
        self._escaped_totals = [[0] * f.components for f in initial.fields]
        self._coupled_types = {rule.type_index for rule in initial.spatial_couplings} | {
            rule.type_index for rule in initial.spatial_interactions
        }
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
            cell = self._at(seed.position)
            records = list(cell.records)
            try:
                slot = records.index(None)
            except ValueError as error:
                raise ValueError("initial disturbance capacity exceeded") from error
            records[slot] = seed.record
            cell.records = tuple(records)

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

    def _emit(self, event: str, position: Address3, **data: object) -> None:
        if self._observer is not None:
            self._observer({"event": event, "tick": self.tick, "position": position, **data})

    def _has_work(self, cell: DisturbanceCell) -> bool:
        present = [record.type_index for record in cell.records if record is not None]
        if self._coupled_types.intersection(present):
            return True
        rules: tuple[CouplingDefinition | InteractionDefinition, ...] = (
            *self.initial.couplings,
            *self.initial.interactions,
        )
        for coupling in rules:
            if coupling.left_type in present and coupling.right_type in present:
                if coupling.left_type != coupling.right_type or present.count(coupling.left_type) > 1:
                    return True
        for record in cell.records:
            if record is not None:
                definition = self.initial.disturbances[record.type_index]
                if definition.transport.mode == "move" and definition.transport.direction_field is None:
                    return True
                if definition.updates or definition.checks or definition.cost_field is not None:
                    return True
                if any(any(unpack(v)) for v in record.values):
                    return True
        return False

    def _begin(self, position: Address3, cell: DisturbanceCell) -> None:
        if cell.pending is not None or cell.available_tick > self.tick or not self._has_work(cell):
            return
        coupled = (
            self._spatial.couple(position, cell.records)
            if self._spatial is not None
            and any(r is not None and r.type_index in self._coupled_types for r in cell.records)
            else None
        )
        plan = self._planner(
            cell.records if coupled is None else coupled.records,
            cell.coupling_remainders,
            cell.received_count,
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
            replacements = []
            for slot, record in plan.replacements:
                if record is not None:
                    cost_field = self.initial.disturbances[record.type_index].cost_field
                    if cost_field is not None:
                        values = list(record.values)
                        # This reporter assignment was already metered by the local planner.
                        values[cost_field] = pack((plan.cost,))
                        record = replace(record, values=tuple(values))
                replacements.append((slot, record))
            plan = replace(plan, replacements=tuple(replacements))
        if len(plan.departures) > self.initial.slots_per_cell * 6:
            raise ValueError("local rule exceeds fixed outgoing capacity")
        extra, duration = cycle_timing(plan.cost, self.initial.normal_budget, self.initial.link_ticks)
        pending = PendingCycle(bounded(self.tick + extra), bounded(self.tick + duration), plan)
        # Originals remain in their occupied slots throughout the local wait.
        cell.pending = pending
        cell.received_count = 0
        cell.last_cost = plan.cost
        self._emit(
            "cycle_started",
            position,
            cost=plan.cost,
            ready_tick=pending.ready_tick,
            next_tick=pending.next_tick,
        )

    def _commit(self, position: Address3, cell: DisturbanceCell) -> None:
        pending = cell.pending
        if pending is None or pending.ready_tick > self.tick:
            return
        old_links = self._links.get(position, (None,) * (6 * self.initial.slots_per_cell))
        if any(packet is not None for packet in old_links):
            raise ValueError("outgoing links still occupied; no implicit packet queue is allowed")
        records = list(cell.records)
        for slot, record in pending.plan.replacements:
            records[slot] = self._current_emission_state(record, cell.records[slot])
        departure_tick = bounded(self.tick + self.initial.link_ticks)
        links: list[Packet | None] = [None] * len(old_links)
        for index, departure in enumerate(pending.plan.departures):
            record = departure.record
            if departure.origin_slot != -1:
                if not 0 <= departure.origin_slot < len(cell.records):
                    raise ValueError("departure origin slot exceeds local capacity")
                current = cell.records[departure.origin_slot]
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
        cell.records = tuple(records)
        cell.coupling_remainders = pending.plan.coupling_remainders
        cell.available_tick = pending.next_tick
        cell.pending = None
        self._links[position] = tuple(links)
        if self._spatial is not None:
            self._spatial.commit_reaction(position, reaction, pending.plan.spatial_reaction)
        for index, values in enumerate(pending.plan.source_delta):
            for component, delta in enumerate(values):
                self._source_totals[index][component] += delta
        self._emit(
            "cycle_committed", position, cost=pending.plan.cost, transfers=len(pending.plan.departures)
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
        for departure in pending.plan.departures:
            self._emit(
                "sent",
                position,
                port=departure.port,
                disturbance=self.initial.disturbances[departure.record.type_index].name,
                values=self.record_values(departure.record),
                arrival_tick=departure_tick,
            )

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
        if len(records) != len(cell.records):
            raise ValueError("spatial emission cannot change disturbance capacity")
        for before, after in zip(cell.records, records, strict=True):
            if before is None or after is None:
                if before is not after:
                    raise ValueError("spatial emission cannot change disturbance occupancy")
            elif self._current_emission_state(before, after) != after:
                raise ValueError("spatial emission cannot change a disturbance's physical values")
        cell.records = records

    def _merge_arrivals(
        self, cell: DisturbanceCell, packets: tuple[Packet, ...]
    ) -> tuple[DisturbanceRecord | None, ...]:
        records = list(cell.records)
        locked = set() if cell.pending is None else {slot for slot, _ in cell.pending.plan.replacements}
        for packet in packets:
            incoming = packet.record
            definition = self.initial.disturbances[incoming.type_index]
            match = None
            if definition.transport.mode == "split":
                match = next(
                    (
                        slot
                        for slot, old in enumerate(records)
                        if slot not in locked
                        and old is not None
                        and old.type_index == incoming.type_index
                        and old.channel_code == incoming.channel_code
                    ),
                    None,
                )
            if match is not None:
                old = records[match]
                assert old is not None
                combined: list[tuple[int, ...]] = []
                for index, (a, b) in enumerate(zip(old.values, incoming.values, strict=True)):
                    value = pack(
                        tuple(checked_work(x + y) for x, y in zip(unpack(a), unpack(b), strict=True))
                    )
                    self.initial.fields[index].validate(value)
                    combined.append(value)
                records[match] = replace(old, values=tuple(combined))
            else:
                try:
                    slot = records.index(None)
                except ValueError as error:
                    raise ValueError(
                        "local receiving capacity exhausted; no disturbance was discarded"
                    ) from error
                records[slot] = incoming
        return tuple(records)

    def _escape(self, origin: Address3, slot: int, packet: Packet) -> None:
        """Complete one terminal link; unused allowances are not physical stock."""
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
            cell = self._at(position)
            records = self._merge_arrivals(cell, tuple(packet for _, _, packet in deliveries))
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
                    port=packet.port ^ 1,
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
                    {p: cell.records for p, cell in self._cells.items()},
                    self._commit_emission_records,
                )
            for position in sorted(self._cells):
                cell = self._cells[position]
                self._begin(position, cell)
                self._commit(position, cell)
            self.tick = bounded(self.tick + 1)
            if self._spatial is not None:
                self._spatial.deliver(self.tick)
            self._deliver()
            for position in sorted(self._cells):
                self._commit(position, self._cells[position])
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
