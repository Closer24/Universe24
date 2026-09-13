"""Fixed-clock ownership for configured spatial fields, separate from carriers."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from typing import Protocol

from .coupling_selectors import matches_type, selected_type_set
from .disturbance_state import Address3, DisturbanceRecord, InitialState, Values, bounded, pack, unpack
from .integer import add_components, checked_work
from .node_state import SpatialNodeView
from .spatial_state import (
    FieldInteractionGuard,
    SpatialBundle,
    SpatialCouplingResult,
    SpatialNode,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
)
from .topology import (
    inverse_port,
    neighbor_address,
    site_count,
    validate_position,
    validate_topology_configuration,
)

SpatialPlanner = Callable[
    [tuple[SpatialState, ...], tuple[DisturbanceRecord | None, ...], int], SpatialPlan
]
SpatialDecayer = Callable[[SpatialBundle], tuple[SpatialBundle, Values, int]]
EventSink = Callable[[dict[str, object]], None]
RecordCommit = Callable[[Address3, tuple[DisturbanceRecord | None, ...]], None]


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
    ) -> None:
        validate_topology_configuration(initial)
        self.initial = initial
        self.port_count = len(initial.topology.offsets)
        self.planner = planner
        self.observer = observer
        self.coupler = coupler
        self.decayer = decayer
        self.nodes: dict[Address3, SpatialNode] = {}
        # Host scheduling index only: retain physical registers in self.nodes.
        self._active: set[Address3] = set()
        self._field_tick = -1
        self.links: dict[Address3, tuple[SpatialPacket | None, ...]] = {}
        self.empty_links: tuple[SpatialPacket | None, ...] = (None,) * self.port_count
        self.sources = [[0] * field.components for field in initial.fields]
        self.dissipation = [[0] * field.components for field in initial.fields]
        self.reactions = [[0] * field.components for field in initial.fields]
        self.transformations = [[0] * field.components for field in initial.fields]
        self.escaped = [[0] * field.components for field in initial.fields]
        for seed in initial.spatial_seeds:
            node = self._at(seed.position)
            states = list(node.states)
            states[seed.spatial_field] = replace(
                states[seed.spatial_field], populations=seed.populations
            )
            node.states = tuple(states)
            self.values(seed.position)
        self._initial_totals = self.totals()

    @property
    def cells(self) -> Mapping[Address3, SpatialNode]:
        """Legacy read alias for the canonical node state mapping."""
        return self.nodes

    def node_view(self, position: Address3) -> SpatialNodeView | None:
        """Read local immutable references without materializing a node."""
        node = self.nodes.get(position)
        if node is None:
            return None
        return SpatialNodeView(
            node.states,
            node.last_cost,
            node.received_count,
            node.reaction_phases,
            node.sample_values,
            node.sample_fluxes,
            node.last_begin_tick,
            node.received_decay_cost,
            node.sample_ports,
        )

    def _blank_states(self) -> tuple[SpatialState, ...]:
        result = []
        for definition in self.initial.spatial_fields:
            zero = pack((0,) * self.initial.fields[definition.field].components)
            result.append(SpatialState((zero,) * 8, (zero,) * 8, (zero,) * self.port_count))
        return tuple(result)

    def _at(self, position: Address3) -> SpatialNode:
        validate_position(position, self.initial.shape, self.initial.topology)
        if position not in self.nodes:
            self.nodes[position] = SpatialNode(self._blank_states())
            self._active.add(position)
        elif position not in self._active:
            # An idle known node completed the empty phase without a host visit.
            # New nodes stay active, so this cannot backdate their creation.
            self.nodes[position].last_begin_tick = self._field_tick
        return self.nodes[position]

    def _neighbor(self, position: Address3, port: int) -> Address3 | None:
        return neighbor_address(
            position, port, self.initial.shape, self.initial.boundary, self.initial.topology
        )

    def _event(self, event: str, tick: int, position: Address3, **details: object) -> None:
        if self.observer is not None:
            self.observer({"event": event, "tick": tick, "position": position, **details})

    def begin(
        self,
        tick: int,
        residents: Mapping[Address3, tuple[DisturbanceRecord | None, ...]],
        commit_records: RecordCommit,
    ) -> None:
        if tick % self.initial.link_ticks:
            return
        self._field_tick = tick
        emitter_types = selected_type_set(self.initial.emissions)
        coupled_types = selected_type_set(
            self.initial.spatial_couplings, self.initial.spatial_interactions
        )
        positions = set(self._active)
        for position, records in residents.items():
            if any(
                record is not None and record.type_index in emitter_types | coupled_types
                for record in records
            ):
                positions.add(position)
        for position in sorted(positions):
            node = self._at(position)
            if any(packet is not None for packet in self.links.get(position, ())):
                raise ValueError("outgoing spatial links are occupied")
            records = residents.get(position, ())
            if self.coupler is not None and any(
                record is not None and record.type_index in coupled_types for record in records
            ):
                # Freeze only locally delivered input, before fresh source injection.
                node.sample_values = self.coupler.sample(node.states)
                node.sample_fluxes = self.coupler.sample_fluxes(node.states)
                if self.initial.spatial_interactions:
                    node.sample_ports = self.coupler.sample_ports(node.states)
            # Samples describe only the preceding delivery interval, never a permanent trail.
            states = (
                node.states
                if self.initial.field_rules
                else tuple(
                    replace(state, delivered=(pack((0,) * len(state.populations[0])),) * self.port_count)
                    for state in node.states
                )
            )
            active_source = any(
                record is not None
                and matches_type(rule, record.type_index)
                and (
                    rule.budget is None
                    or not record.emission_remaining
                    or any(unpack(record.emission_remaining[index]))
                )
                for record in records
                for index, rule in enumerate(self.initial.emissions)
            )
            active_field = any(any(unpack(payload)) for state in states for payload in state.populations)
            if not active_source and not active_field and node.received_count == 0:
                node.states = tuple(
                    replace(state, delivered=(pack((0,) * len(state.populations[0])),) * self.port_count)
                    for state in states
                )
                node.last_cost = 0
                node.last_begin_tick = tick
                self._active.discard(position)
                continue
            plan = self.planner(states, records, node.received_count)
            if len(plan.outgoing) != self.port_count:
                raise ValueError("spatial proposal has incorrect port count")
            cost = bounded(checked_work(plan.cost + node.received_decay_cost))
            packets: list[SpatialPacket | None] = [None] * self.port_count
            for port, bundle in enumerate(plan.outgoing):
                if any(any(unpack(payload)) for field in bundle for payload in field):
                    packets[port] = SpatialPacket(
                        bounded(tick + self.initial.link_ticks), position, port, bundle
                    )
            # All physical calculations and validation precede the local commit.
            commit_records(position, plan.emission_records)
            node.states = plan.states
            node.last_cost = cost
            node.received_count = 0
            node.received_decay_cost = 0
            node.last_begin_tick = tick
            self.links[position] = tuple(packets)
            # One following phase clears the reported cost before becoming idle.
            self._active.add(position)
            for index, payload in enumerate(plan.source_delta):
                for component, value in enumerate(payload):
                    self.sources[index][component] += value
            for index, payload in enumerate(plan.rule_delta):
                for component, value in enumerate(payload):
                    self.transformations[index][component] += value
            self._event(
                "spatial_cycle",
                tick,
                position,
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
            for packet in packets:
                if packet is not None:
                    self._event(
                        "spatial_sent",
                        tick,
                        position,
                        port=packet.port,
                        arrival_tick=packet.arrival_tick,
                    )

    def couple(
        self, position: Address3, records: tuple[DisturbanceRecord | None, ...]
    ) -> SpatialCouplingResult:
        if self.coupler is None:
            raise ValueError("spatial coupling requires an explicitly composed law")
        node = self._at(position)
        return self.coupler(records, node.sample_values, node.sample_fluxes, node.sample_ports)

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
        node = self._at(position)
        if node.last_begin_tick != tick:
            states, phases = self.coupler.deposit(node.states, node.reaction_phases, reaction)
            return ReactionCommit(states, phases, None)
        # Only this instant's departure buffers are still locally appendable.
        # Packets from an earlier departure are immutable while in transit.
        old_links = self.links.get(position, (None,) * self.port_count)
        arrival = bounded(tick + self.initial.link_ticks)
        if any(packet is not None and packet.arrival_tick != arrival for packet in old_links):
            raise ValueError("reaction cannot alter a spatial packet already in transit")
        states, phases, outgoing = self.coupler.forward_reaction(
            node.states, node.reaction_phases, reaction
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
        node = self._at(position)
        node.states = proposal.states
        node.reaction_phases = proposal.phases
        self._active.add(position)
        if proposal.links is not None:
            self.links[position] = proposal.links
        for index, values in enumerate(reaction):
            for component, value in enumerate(values):
                self.reactions[index][component] += value

    def _escape(self, packet: SpatialPacket, tick: int) -> None:
        """No receiving node exists outside; terminal stock escapes without exterior decay."""
        amounts = [[0] * field.components for field in self.initial.fields]
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
            node = self._at(position)
            losses = [[0] * field.components for field in self.initial.fields]
            decay_cost = node.received_decay_cost
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
                old = node.states[index]
                populations = [list(unpack(v)) for v in old.populations]
                directions = [[0] * field.components for _ in range(self.port_count)]
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
            received_count = bounded(checked_work(node.received_count + len(arrivals)))
            node.states = tuple(states)
            node.received_count = received_count
            node.received_decay_cost = decay_cost
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
                    self.initial.fields[definition.field].name: unpack(
                        state.delivered[inverse_port(port, self.initial.topology)]
                    )
                    for definition, state in zip(self.initial.spatial_fields, states, strict=True)
                }
                if any(packet.port == inverse_port(port, self.initial.topology) for packet in arrivals)
                else {}
                for port in range(self.port_count)
            ]
            self._event(
                "spatial_received",
                tick,
                position,
                packets=len(arrivals),
                received_fields=received_fields,
            )
            if self.decayer is not None:
                self._event(
                    "spatial_decayed",
                    tick,
                    position,
                    dissipated={
                        field.name: tuple(losses[i])
                        for i, field in enumerate(self.initial.fields)
                        if any(losses[i])
                    },
                    cost=arrival_cost,
                )

    def cost(self, position: Address3, tick: int) -> int:
        node = self.nodes.get(position)
        return 0 if node is None or tick % self.initial.link_ticks else node.last_cost

    def totals(self) -> list[list[int]]:
        result = [[0] * field.components for field in self.initial.fields]
        volume = site_count(self.initial.shape, self.initial.topology)
        for index, definition in enumerate(self.initial.spatial_fields):
            for component, value in enumerate(unpack(definition.baseline)):
                result[definition.field][component] += volume * value
            inventories = [self.nodes[position].states[index].populations for position in self._active]
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
        states = self.nodes[position].states if position in self.nodes else self._blank_states()
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
                {"position": position, "fields": self.values(position), "cost": node.last_cost}
                for position, node in sorted(self.nodes.items())
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
