"""Bounded Node-owned output proposals, distinct from packets on Links."""

from dataclasses import dataclass, replace

from .disturbance_state import Packet, bounded
from .spatial_state import SpatialPacket


@dataclass(frozen=True, slots=True)
class OutputClock:
    sample_tick: int = -1
    sample: int = 0
    delays: tuple[int, ...] = (0,) * 6
    starts: tuple[int, ...] = (-1,) * 6
    ready: tuple[int, ...] = (0,) * 6

    def reserve(self, tick: int, ports: tuple[int, ...]) -> OutputClock:
        starts, ready = list(self.starts), list(self.ready)
        delays = self.delays if self.sample_tick == tick else (0,) * 6
        for port in ports:
            if starts[port] != tick and ready[port] > tick:
                raise ValueError("output face capacity collision")
            if starts[port] != tick:
                starts[port], ready[port] = tick, bounded(tick + delays[port])
        return replace(self, starts=tuple(starts), ready=tuple(ready))


@dataclass(frozen=True, slots=True)
class OutputHold[PacketType: Packet | SpatialPacket]:
    prepared_tick: int
    release_tick: int
    packet: PacketType


def stage_outputs[PacketType: Packet | SpatialPacket](
    held: tuple[OutputHold[PacketType] | None, ...],
    links: tuple[PacketType | None, ...],
    proposed: tuple[PacketType | None, ...],
    tick: int,
    delays: tuple[int, ...],
    link_ticks: int,
    *,
    port_indexed: bool = False,
) -> tuple[tuple[OutputHold[PacketType] | None, ...], tuple[PacketType | None, ...]]:
    """Prepare a bounded ownership transfer without changing any owner.

    The caller supplies delays selected by its generic local operation. Capacity
    conflicts reject the complete proposal; they never create a waiting policy.
    Spatial banks are indexed by Port; carrier banks use compact record slots.
    """
    if len(delays) != 6 or any(bounded(delay) < 0 for delay in delays):
        raise ValueError("output delays require six nonnegative integer counts")
    if len(held) != len(links) or len(proposed) != len(links):
        raise ValueError("output bank capacity cannot change")
    staged, outgoing = list(held), list(links)
    busy = {entry.packet.port for entry in held if entry is not None}
    busy.update(packet.port for packet in links if packet is not None)
    requested = {packet.port for packet in proposed if packet is not None}
    if busy & requested:
        raise ValueError("output face capacity collision")
    for packet in proposed:
        if packet is None:
            continue
        ready = bounded(tick + delays[packet.port])
        packet = replace(packet, arrival_tick=bounded(ready + link_ticks))
        if ready == tick:
            slot = (
                packet.port
                if port_indexed
                else next((i for i, value in enumerate(outgoing) if value is None), None)
            )
            if slot is None or outgoing[slot] is not None:
                raise ValueError("output Link bank capacity collision")
            outgoing[slot] = packet
        else:
            slot = (
                packet.port
                if port_indexed
                else next((i for i, value in enumerate(staged) if value is None), None)
            )
            if slot is None or staged[slot] is not None:
                raise ValueError("output hold bank capacity collision")
            staged[slot] = OutputHold(tick, ready, packet)
    return tuple(staged), tuple(outgoing)


def release_outputs[PacketType: Packet | SpatialPacket](
    held: tuple[OutputHold[PacketType] | None, ...],
    links: tuple[PacketType | None, ...],
    tick: int,
    *,
    port_indexed: bool = False,
) -> tuple[tuple[OutputHold[PacketType] | None, ...], tuple[PacketType | None, ...]]:
    """Release ready local owners to Links without changing their frozen time."""
    remaining, outgoing = list(held), list(links)
    for index, entry in enumerate(held):
        if entry is None or entry.release_tick > tick:
            continue
        if entry.release_tick != tick:
            raise ValueError("output release tick was skipped")
        if any(packet is not None and packet.port == entry.packet.port for packet in outgoing):
            raise ValueError("output release collides with an occupied Link")
        slot = (
            entry.packet.port
            if port_indexed
            else next((i for i, packet in enumerate(outgoing) if packet is None), None)
        )
        if slot is None or outgoing[slot] is not None:
            raise ValueError("output Link bank capacity collision")
        outgoing[slot], remaining[index] = entry.packet, None
    return tuple(remaining), tuple(outgoing)
