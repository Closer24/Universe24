"""Port-local readiness around the existing atomic Node transaction owner.

The six Ports own bounded slot and lock views. The existing DisturbanceNode
continues to own physical records, pending proposals, costs and output packets.
One ready cohort invokes the existing joint transaction evaluator at most once;
this adapter does not compile that evaluator into the 24 internal Registers.
"""

from .disturbance_node import DisturbanceNode
from .disturbance_state import Packet, bounded
from .node_services import NodeServices
from .register_contracts import (
    OutgoingIntent,
    PortState,
    ReadyBatch,
    RegisterEffects,
    WakeIntent,
)


class PortExecutionNode:
    """Six external readiness units and one atomic Node transaction owner.

    This reusable Port adapter precedes the 24-internal-Register decomposition.
    It is not an implementation of that internal computation graph.
    """

    def __init__(self, node: DisturbanceNode, services: NodeServices, *, seed_port: int = 0) -> None:
        if type(seed_port) is not int or not 0 <= seed_port < 6:
            raise ValueError("seed Register port must be from zero through five")
        initial = services.initial
        if initial.spatial_fields or initial.event_program is not None or services.resolver is not None:
            raise ValueError("Register execution currently supports carrier-only local rules")
        if any(kind.transport.mode == "split" for kind in initial.disturbances):
            raise ValueError("Register execution currently requires whole-record transport")
        self.node = node
        self._services = services
        self._owners: tuple[int | None, ...] = tuple(
            seed_port if record is not None else None for record in node.records
        )
        self.ports: tuple[PortState, ...] = ()
        self._last_ready_tick: int | None = None
        self._refresh()

    def _refresh(self) -> None:
        owners = tuple(
            owner if record is not None else None
            for owner, record in zip(self._owners, self.node.records, strict=True)
        )
        if any(
            record is not None and owner is None
            for record, owner in zip(self.node.records, owners, strict=True)
        ):
            raise ValueError("a resident record has no local Register owner")
        locked = (
            set()
            if self.node.pending is None
            else {slot for slot, _ in self.node.pending.plan.replacements}
        )
        self._owners = owners
        self.ports = tuple(
            PortState(
                port,
                tuple(slot for slot, owner in enumerate(owners) if owner == port),
                tuple(slot for slot, owner in enumerate(owners) if owner == port and slot in locked),
            )
            for port in range(6)
        )

    @staticmethod
    def _validate_batches(batches: tuple[ReadyBatch, ...], *, arrivals: bool) -> None:
        if type(batches) is not tuple or not 1 <= len(batches) <= (32 if arrivals else 12):
            raise ValueError("one bounded ready cohort is required")
        if any(type(batch) is not ReadyBatch for batch in batches):
            raise ValueError("Register cohorts require ReadyBatch values")
        if not arrivals and len({(batch.port, batch.kind) for batch in batches}) != len(batches):
            raise ValueError("duplicate Register readiness in one cohort")
        if any((batch.kind == "arrival") != arrivals for batch in batches):
            raise ValueError("arrival admission and computation readiness are separate phases")

    def receive(self, batches: tuple[ReadyBatch, ...], tick: int) -> tuple[Packet, ...]:
        """Admit the whole delivered cohort before host release or local computation.

        Packet order is the host's existing deterministic delivery order. Return that
        same tuple for the host's acknowledgement phase. If validation fails, source
        PortBanks and all destination physical records remain unchanged.
        """
        self._validate_batches(batches, arrivals=True)
        if self._last_ready_tick == tick:
            raise ValueError("all same-tick arrivals must precede local computation")
        packets = tuple(packet for batch in batches for packet in batch.packets)
        if len(packets) > len(self.node.records):
            raise ValueError("arrival cohort exceeds fixed Node record capacity")
        # Whole-record receive assigns the earliest free slot in this same order.
        locked = (
            set()
            if self.node.pending is None
            else {slot for slot, _ in self.node.pending.plan.replacements}
        )
        free = tuple(
            slot
            for slot, record in enumerate(self.node.records)
            if record is None and slot not in locked
        )
        if len(packets) > len(free):
            raise ValueError("local receiving capacity exhausted; no disturbance was discarded")
        owners = list(self._owners)
        for slot, packet in zip(free, packets, strict=False):
            owners[slot] = packet.port ^ 1
        self.node.receive(packets, tick, self._services)
        self._owners = tuple(owners)
        self._refresh()
        return packets

    def acknowledge_receipt(self, packets: tuple[Packet, ...], tick: int) -> None:
        self.node.acknowledge_receipt(packets, tick, self._services)

    def _active_ports(self) -> tuple[int, ...]:
        active = tuple(
            register.port
            for register in self.ports
            if self._services.record_policy.has_work(
                tuple(self.node.records[slot] for slot in register.slots)
            )
        )
        if active or not self._services.record_policy.has_work(self.node.records):
            return active
        # Two zero-valued records may activate a joint rule while neither local
        # one-record view is independently active. Their cohort still has work.
        return tuple(register.port for register in self.ports if register.slots)

    def _wakes(self, tick: int, *, initial: bool = False) -> tuple[WakeIntent, ...]:
        active = self._active_ports()
        pending = self.node.pending
        if pending is not None:
            ports = tuple(register.port for register in self.ports if register.locked_slots)
            anchor = min(ports or active or (0,))
            return (WakeIntent(anchor, "commit", pending.ready_tick),)
        earliest = tick if initial else bounded(tick + 1)
        due = max(earliest, self.node.available_tick)
        return tuple(WakeIntent(port, "compute", due) for port in active)

    def bootstrap(self, tick: int = 0) -> RegisterEffects:
        """Seed only initially active local Registers without advancing physics."""
        if type(tick) is not int or bounded(tick) < 0:
            raise ValueError("bootstrap time must be a bounded nonnegative integer")
        return RegisterEffects(wakes=self._wakes(tick, initial=True))

    def ready(self, batches: tuple[ReadyBatch, ...], tick: int) -> RegisterEffects:
        """Dispatch one due cohort and commit at most one atomic Node transaction."""
        self._validate_batches(batches, arrivals=False)
        if type(tick) is not int or bounded(tick) < 0:
            raise ValueError("Register readiness time must be a bounded nonnegative integer")
        if self._last_ready_tick is not None and tick <= self._last_ready_tick:
            raise ValueError("a Node receives only one grouped readiness call per tick")
        before_pending = self.node.pending
        before_available = self.node.available_tick
        # Only the local transaction owner sees the complete frozen participant set.
        self.node.advance(
            tick,
            self._services,
            window_closed=all(batch.kind == "commit" for batch in batches),
        )
        self._last_ready_tick = tick
        self._refresh()
        committed = self.node.pending is None and (
            before_pending is not None or self.node.available_tick != before_available
        )
        return RegisterEffects(
            outgoing=tuple(
                OutgoingIntent(slot, packet.port, packet.arrival_tick)
                for slot, packet in enumerate(self.node.output.packets)
                if packet is not None
            ),
            wakes=self._wakes(tick),
            committed=committed,
        )
