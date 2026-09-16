"""An external due-work scheduler for the bounded carrier Port adapter.

The physical Node and Link owners, generic local law, snapshots and events remain
the existing implementation. This host adapter changes only which due owners are
visited. The ordinary Node scheduler remains the default and comparison reference.
"""

from .deadline_queue import DeadlineQueue, QueueKey
from .disturbance_engine import DisturbanceEngine
from .disturbance_state import Address3, Packet, bounded
from .port_transport import PortTransport
from .register_contracts import ReadyBatch, RegisterEffects
from .register_node import PortExecutionNode


class PortExecution:
    """Dispatch compute, Link receipt and commit through separate clock phases."""

    def __init__(self, world: DisturbanceEngine) -> None:
        self.world = world
        self.compute = DeadlineQueue()
        self.commit = DeadlineQueue()
        self.transport = PortTransport()
        self.nodes: dict[Address3, PortExecutionNode] = {}
        self._wakes: dict[Address3, set[QueueKey]] = {}
        self.node_cohorts = 0
        self.port_dispatches = 0
        for position in world._nodes:
            owner = self._at(position)
            self._effects(position, owner.bootstrap(world.tick), world.tick)

    def _at(self, position: Address3) -> PortExecutionNode:
        if position not in self.nodes:
            self.nodes[position] = PortExecutionNode(self.world._at(position), self.world._services)
            self.transport.register_owner(position)
        return self.nodes[position]

    def _effects(self, position: Address3, effects: RegisterEffects, tick: int) -> None:
        wakes = {(position, wake.port, wake.kind, 0): wake.due_tick for wake in effects.wakes}
        if len(wakes) != len(effects.wakes) or len(wakes) > 12:
            raise ValueError("local effects contain duplicate or excessive Port wakes")
        if any(due < tick for due in wakes.values()):
            raise ValueError("local effects cannot schedule work into the past")
        for key in self._wakes.get(position, set()):
            (self.compute if key[2] == "compute" else self.commit).cancel(key)
        for key, due in wakes.items():
            (self.compute if key[2] == "compute" else self.commit).set(key, due)
        if wakes:
            self._wakes[position] = set(wakes)
        else:
            self._wakes.pop(position, None)
        self.transport.schedule(position, effects.outgoing, tick)
        self.world._refresh_output(position)

    def _dispatch(self, keys: tuple[QueueKey, ...], tick: int) -> None:
        groups: dict[Address3, list[ReadyBatch]] = {}
        for position, port, kind, _ in keys:
            if kind not in ("compute", "commit"):
                raise ValueError("physical receipt must precede the local dispatch phase")
            groups.setdefault(position, []).append(ReadyBatch(port, kind))
        for position, batches in sorted(groups.items()):
            owner = self._at(position)
            self.node_cohorts += 1
            self.port_dispatches += len(batches)
            self.world._carrier_phase_visits += 1
            try:
                effects = owner.ready(tuple(batches), tick)
                self._effects(position, effects, tick)
            finally:
                self.world._refresh_output(position)
            self.world._sleep_carriers((position,))

    def _deliver(self, tick: int) -> None:
        ready: dict[Address3, list[tuple[Address3, int, Packet]]] = {}
        for origin, port, _, slot in self.transport.take(tick):
            packet = self.world._links[origin][slot]
            if packet is None or packet.origin != origin or packet.port != port:
                raise ValueError("scheduled Link handle no longer identifies its actual owner")
            if packet.arrival_tick != tick:
                raise ValueError("scheduled Link handle has an inconsistent arrival time")
            target = self.world.neighbor(origin, port)
            if target is None:
                self.world._escape(origin, slot, packet)
            else:
                ready.setdefault(target, []).append((origin, slot, packet))
        for position, deliveries in sorted(ready.items()):
            owner = self._at(position)
            # Repeated Port batches preserve original source-bank/slot order.
            batches = tuple(
                ReadyBatch(packet.port ^ 1, "arrival", (packet,)) for _, _, packet in deliveries
            )
            packets = owner.receive(batches, tick)
            for origin, slot, _ in deliveries:
                bank = list(self.world._links[origin])
                bank[slot] = None
                self.world._links[origin] = tuple(bank)
            owner.acknowledge_receipt(packets, tick)
            self._effects(position, owner.bootstrap(tick), tick)

    def step(self) -> None:
        """Preserve one opening computation phase and one later receipt/commit barrier."""
        try:
            self._dispatch(self.compute.take(self.world.tick), self.world.tick)
            self.world.tick = bounded(self.world.tick + 1)
            self._deliver(self.world.tick)
            self._dispatch(self.commit.take(self.world.tick), self.world.tick)
        except Exception:
            self.world.faulted = True
            raise

    def report(self) -> dict[str, object]:
        return {
            "strategy": "port",
            "scope": "whole-record carriers; atomic Node evaluator retained",
            "external_ports_per_node": 6,
            "node_cohorts": self.node_cohorts,
            "port_dispatches": self.port_dispatches,
            "compute": self.compute.report(),
            "commit": self.commit.report(),
            "transport": self.transport.deadlines.report(),
        }
