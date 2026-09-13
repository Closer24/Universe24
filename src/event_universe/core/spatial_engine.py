"""Fixed-clock ownership for configured spatial fields, separate from carriers."""

from collections.abc import Callable, Mapping
from dataclasses import replace

from .coupling_selectors import selected_type_set
from .disturbance_node import DisturbanceNode
from .disturbance_state import Address3, InitialState, pack, unpack
from .integer import checked_work
from .node_boundary import (
    validate_spatial_bundle,
)
from .node_ports import PortTable
from .node_state import SpatialNodeView
from .spatial_node import (
    NodeActivity,
    SpatialAccounting,
    SpatialNode,
    SpatialServices,
)
from .spatial_node import (
    SpatialCoupler as SpatialCoupler,
)
from .spatial_node import (
    SpatialDecayer as SpatialDecayer,
)
from .spatial_node import (
    SpatialPlanner as SpatialPlanner,
)
from .spatial_state import (
    SpatialPacket,
    SpatialState,
)
from .topology import (
    neighbor_address,
    site_count,
    validate_position,
    validate_topology_configuration,
)

EventSink = Callable[[dict[str, object]], None]


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
        self.observer = observer
        self.nodes: dict[Address3, SpatialNode] = {}
        # Host scheduling index only: retain physical registers in self.nodes.
        self._active: set[Address3] = set()
        self._field_tick = -1
        self.empty_links: tuple[SpatialPacket | None, ...] = (None,) * self.port_count
        self.links: PortTable[SpatialPacket] = PortTable(self.empty_links)
        self.sources = [[0] * field.components for field in initial.fields]
        self.dissipation = [[0] * field.components for field in initial.fields]
        self.reactions = [[0] * field.components for field in initial.fields]
        self.transformations = [[0] * field.components for field in initial.fields]
        self.escaped = [[0] * field.components for field in initial.fields]
        self.services = SpatialServices(
            replace(initial, seeds=(), spatial_seeds=(), event_program=None),
            planner,
            observer,
            coupler,
            decayer,
            NodeActivity(self._active),
            SpatialAccounting(self.sources, self.dissipation, self.reactions, self.transformations),
        )
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
            self.nodes[position] = SpatialNode(
                self._blank_states(), position=position, output=self.links.bank(position)
            )
            self._active.add(position)
        elif position not in self._active:
            # An idle known node completed the empty phase without a host visit.
            # New nodes stay active, so this cannot backdate their creation.
            self.nodes[position].catch_up_idle(self._field_tick)
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
        residents: Mapping[Address3, DisturbanceNode],
    ) -> None:
        if tick % self.initial.link_ticks:
            return
        self._field_tick = tick
        emitter_types = selected_type_set(self.initial.emissions)
        coupled_types = selected_type_set(
            self.initial.spatial_couplings, self.initial.spatial_interactions
        )
        positions = set(self._active)
        for position, carrier in residents.items():
            if any(
                record is not None and record.type_index in emitter_types | coupled_types
                for record in carrier.records
            ):
                positions.add(position)
        for position in sorted(positions):
            node = self._at(position)
            node.advance(tick, residents.get(position), self.services)

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
        for origin, packets in self.links.items():
            for port, packet in enumerate(packets):
                if packet is not None and packet.arrival_tick == tick:
                    if packet.origin != origin or packet.port != port:
                        raise ValueError("spatial packet provenance differs from its link owner")
                    target = self._neighbor(packet.origin, packet.port)
                    if target is None:
                        validate_spatial_bundle(self.initial, packet.fields)
                        self._escape(packet, tick)
                    else:
                        ready.setdefault(target, []).append(packet)
        for position, arrivals in sorted(ready.items()):
            node = self._at(position)
            messages = node.receive(tuple(arrivals), tick, self.services)
            for packet in arrivals:
                links = list(self.links[packet.origin])
                links[packet.port] = None
                self.links[packet.origin] = tuple(links)
            for message in messages:
                if self.observer is not None:
                    self.observer(message)

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
