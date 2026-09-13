"""Fixed-clock ownership for configured spatial fields, separate from carriers."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from typing import Protocol

from .disturbance_state import Address3, DisturbanceRecord, InitialState, Values, bounded, pack, unpack
from .event_space import CausalEventSpace
from .integer import add_components, checked_work
from .spatial_state import (
    FieldInteractionGuard,
    SpatialBundle,
    SpatialCell,
    SpatialCouplingResult,
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
        self.cells: dict[Address3, SpatialCell] = {}
        # Host scheduling index only: retain physical registers in self.cells.
        self._active: set[Address3] = set()
        self._field_tick = -1
        self.links: dict[Address3, tuple[SpatialPacket | None, ...]] = {}
        self.sources = [[0] * field.components for field in initial.fields]
        self.dissipation = [[0] * field.components for field in initial.fields]
        self.reactions = [[0] * field.components for field in initial.fields]
        self.transformations = [[0] * field.components for field in initial.fields]
        self.escaped = [[0] * field.components for field in initial.fields]
        for seed in initial.spatial_seeds:
            cell = self._at(seed.position)
            states = list(cell.states)
            states[seed.spatial_field] = replace(
                states[seed.spatial_field], populations=seed.populations
            )
            cell.states = tuple(states)
            self.values(seed.position)
        self._initial_totals = self.totals()
        if self.event_space is not None:
            self.event_space.require_room(len(self.cells))
            for position, cell in sorted(self.cells.items()):
                cell.cause_id = self._event("spatial_source", 0, position)

    def _blank_states(self) -> tuple[SpatialState, ...]:
        result = []
        for definition in self.initial.spatial_fields:
            zero = pack((0,) * self.initial.fields[definition.field].components)
            result.append(SpatialState((zero,) * 8, (zero,) * 8, (zero,) * 6))
        return tuple(result)

    def _at(self, position: Address3) -> SpatialCell:
        if position not in self.cells:
            self.cells[position] = SpatialCell(self._blank_states())
            self._active.add(position)
        elif position not in self._active:
            # An idle known cell completed the empty phase without a host visit.
            # New cells stay active, so this cannot backdate their creation.
            self.cells[position].last_begin_tick = self._field_tick
        return self.cells[position]

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
    ) -> None:
        if tick % self.initial.link_ticks:
            return
        self._field_tick = tick
        emitter_types = {rule.type_index for rule in self.initial.emissions}
        coupled_types = {rule.type_index for rule in self.initial.spatial_couplings} | {
            rule.type_index for rule in self.initial.spatial_interactions
        }
        positions = set(self._active)
        for position, records in residents.items():
            if any(
                record is not None and record.type_index in emitter_types | coupled_types
                for record in records
            ):
                positions.add(position)
        for position in sorted(positions):
            cell = self._at(position)
            if any(packet is not None for packet in self.links.get(position, ())):
                raise ValueError("outgoing spatial links are occupied")
            records = residents.get(position, ())
            sample_values, sample_fluxes, sample_ports = (
                cell.sample_values,
                cell.sample_fluxes,
                cell.sample_ports,
            )
            sample_cause = cell.sample_cause_id
            if self.coupler is not None and any(
                record is not None and record.type_index in coupled_types for record in records
            ):
                # Freeze only locally delivered input, before fresh source injection.
                sample_values = self.coupler.sample(cell.states)
                sample_fluxes = self.coupler.sample_fluxes(cell.states)
                sample_cause = cell.cause_id
                if self.initial.spatial_interactions:
                    sample_ports = self.coupler.sample_ports(cell.states)
            # Samples describe only the preceding delivery interval, never a permanent trail.
            states = (
                cell.states
                if self.initial.field_rules
                else tuple(
                    replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6)
                    for state in cell.states
                )
            )
            active_source = any(
                record is not None
                and record.type_index == rule.type_index
                and (
                    rule.budget is None
                    or not record.emission_remaining
                    or any(unpack(record.emission_remaining[index]))
                )
                for record in records
                for index, rule in enumerate(self.initial.emissions)
            )
            active_field = any(any(unpack(payload)) for state in states for payload in state.populations)
            if not active_source and not active_field and cell.received_count == 0:
                cell.states = tuple(
                    replace(state, delivered=(pack((0,) * len(state.populations[0])),) * 6)
                    for state in states
                )
                cell.last_cost = 0
                cell.cost_cause_id = None
                cell.sample_values, cell.sample_fluxes, cell.sample_ports = (
                    sample_values,
                    sample_fluxes,
                    sample_ports,
                )
                cell.sample_cause_id = sample_cause
                cell.last_begin_tick = tick
                self._active.discard(position)
                continue
            plan = self.planner(states, records, cell.received_count)
            cost = bounded(checked_work(plan.cost + cell.received_decay_cost))
            packets: list[SpatialPacket | None] = [None] * 6
            for port, bundle in enumerate(plan.outgoing):
                if any(any(unpack(payload)) for field in bundle for payload in field):
                    packets[port] = SpatialPacket(
                        bounded(tick + self.initial.link_ticks), position, port, bundle
                    )
            # All physical calculations and validation precede the local commit.
            if self.event_space is not None:
                self.event_space.require_room(1 + sum(p is not None for p in packets))
            carrier_cause = None if record_cause is None else record_cause(position)
            commit_records(position, plan.emission_records)
            cell.states = plan.states
            cell.last_cost = cost
            cell.received_count = 0
            cell.received_decay_cost = 0
            cell.last_begin_tick = tick
            cell.sample_values, cell.sample_fluxes, cell.sample_ports = (
                sample_values,
                sample_fluxes,
                sample_ports,
            )
            cell.sample_cause_id = sample_cause
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
                causes=(cell.cause_id, carrier_cause),
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
            cell.cause_id = cell.cost_cause_id = cause
            if cause is not None and commit_cause is not None and plan.emission_records != records:
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
        cell = self.cells.get(position)
        if cell is None:
            return ()
        causes = (
            cell.sample_cause_id if sampled else None,
            cell.cost_cause_id if tick % self.initial.link_ticks == 0 else None,
        )
        return tuple(dict.fromkeys(c for c in causes if c is not None))

    def reaction_causes(self, position: Address3, *, outgoing: bool) -> tuple[int, ...]:
        """Bounded owners read by a joint commit, including departure amendments."""
        cell = self.cells.get(position)
        if cell is None:
            return ()
        causes = (cell.cause_id,) + (
            tuple(p.cause_id for p in self.links.get(position, ()) if p is not None) if outgoing else ()
        )
        return tuple(dict.fromkeys(c for c in causes if c is not None))

    def link_reaction(self, position: Address3, proposal: ReactionCommit | None, cause: int) -> None:
        """The joint event owns the new stock and any amended departure bundle."""
        if proposal is None:
            return
        self.cells[position].cause_id = cause
        if proposal.links is not None:
            self.links[position] = tuple(
                None if p is None else replace(p, cause_id=cause) for p in proposal.links
            )

    def couple(
        self, position: Address3, records: tuple[DisturbanceRecord | None, ...]
    ) -> SpatialCouplingResult:
        if self.coupler is None:
            raise ValueError("spatial coupling requires an explicitly composed law")
        cell = self._at(position)
        return self.coupler(records, cell.sample_values, cell.sample_fluxes, cell.sample_ports)

    def validate_guards(
        self, position: Address3, reaction: Values, guards: tuple[FieldInteractionGuard, ...]
    ) -> None:
        if guards:
            if self.coupler is None:
                raise ValueError("spatial interaction guards require a configured response law")
            self.coupler.validate_guards(self._at(position).states, reaction, guards)

    def prepare_reaction(self, position: Address3, tick: int, reaction: Values) -> ReactionCommit | None:
        if not reaction or not any(any(payload) for payload in reaction):
            return None
        if self.coupler is None:
            raise ValueError("a spatial reaction requires its configured coupling law")
        cell = self._at(position)
        if cell.last_begin_tick != tick:
            states, phases = self.coupler.deposit(cell.states, cell.reaction_phases, reaction)
            return ReactionCommit(states, phases, None)
        # Only this instant's departure buffers are still locally appendable.
        # Packets from an earlier departure are immutable while in transit.
        old_links = self.links.get(position, (None,) * 6)
        arrival = bounded(tick + self.initial.link_ticks)
        if any(packet is not None and packet.arrival_tick != arrival for packet in old_links):
            raise ValueError("reaction cannot alter a spatial packet already in transit")
        states, phases, outgoing = self.coupler.forward_reaction(
            cell.states, cell.reaction_phases, reaction
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
                SpatialPacket(arrival, position, port, values)
                if any(any(unpack(payload)) for field in values for payload in field)
                else None
            )
        return ReactionCommit(states, phases, tuple(links))

    def commit_reaction(
        self, position: Address3, proposal: ReactionCommit | None, reaction: Values = ()
    ) -> None:
        if proposal is None:
            return
        cell = self._at(position)
        cell.states = proposal.states
        cell.reaction_phases = proposal.phases
        self._active.add(position)
        if proposal.links is not None:
            self.links[position] = proposal.links
        for index, values in enumerate(reaction):
            for component, value in enumerate(values):
                self.reactions[index][component] += value

    def _escape(self, packet: SpatialPacket, tick: int) -> None:
        """No receiving cell exists outside; terminal stock escapes without exterior decay."""
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
            cell = self._at(position)
            losses = [[0] * field.components for field in self.initial.fields]
            decay_cost = cell.received_decay_cost
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
            for index, definition in enumerate(self.initial.spatial_fields):
                field = self.initial.fields[definition.field]
                old = cell.states[index]
                populations = [list(unpack(v)) for v in old.populations]
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
                packed = tuple(pack(tuple(v)) for v in populations)
                delivered = tuple(pack(tuple(v)) for v in directions)
                for payload in (*packed, *delivered):
                    field.validate(payload)
                local = list(unpack(definition.baseline))
                for population_values in populations:
                    for component, value in enumerate(population_values):
                        local[component] = checked_work(local[component] + value)
                field.validate(pack(tuple(local)))
                states.append(SpatialState(packed, old.allocation_phases, delivered))
            received_count = bounded(checked_work(cell.received_count + len(arrivals)))
            cell.states = tuple(states)
            cell.received_count = received_count
            cell.received_decay_cost = decay_cost
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
                    self.initial.fields[definition.field].name: unpack(state.delivered[port ^ 1])
                    for definition, state in zip(self.initial.spatial_fields, states, strict=True)
                }
                if any(packet.port == port ^ 1 for packet in arrivals)
                else {}
                for port in range(6)
            ]
            notifications: list[dict[str, object]] = []
            cell.cause_id = self._event(
                "spatial_received",
                tick,
                position,
                causes=(cell.cause_id, *(p.cause_id for p in arrivals)),
                notifications=notifications,
                packets=len(arrivals),
                received_fields=received_fields,
            )
            if self.decayer is not None:
                cell.cause_id = self._event(
                    "spatial_decayed",
                    tick,
                    position,
                    causes=(cell.cause_id,),
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
        cell = self.cells.get(position)
        return 0 if cell is None or tick % self.initial.link_ticks else cell.last_cost

    def totals(self) -> list[list[int]]:
        result = [[0] * field.components for field in self.initial.fields]
        volume = self.initial.shape[0] * self.initial.shape[1] * self.initial.shape[2]
        for index, definition in enumerate(self.initial.spatial_fields):
            for component, value in enumerate(unpack(definition.baseline)):
                result[definition.field][component] += volume * value
            inventories = [self.cells[position].states[index].populations for position in self._active]
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
        states = self.cells[position].states if position in self.cells else self._blank_states()
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
                {"position": position, "fields": self.values(position), "cost": cell.last_cost}
                for position, cell in sorted(self.cells.items())
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
