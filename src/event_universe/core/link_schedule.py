"""Host-only arrival indexing that retains link ownership and insertion order."""

from collections.abc import ItemsView, Iterator, KeysView, MutableMapping, ValuesView
from typing import Protocol

from .disturbance_state import Address3


class TimedPacket(Protocol):
    @property
    def arrival_tick(self) -> int: ...


class LinkSchedule[PacketType: TimedPacket](MutableMapping[Address3, tuple[PacketType | None, ...]]):
    """Index occupied links by tick without discarding their physical records.

    Mapping writes update the index, including partial clears and replacements.
    Arrival ties retain each origin's first insertion order, as a dictionary scan
    would, independently of when that origin most recently sent a packet.
    """

    def __init__(self) -> None:
        self._packets: dict[Address3, tuple[PacketType | None, ...]] = {}
        self._due: dict[int, set[Address3]] = {}
        self._ticks: dict[Address3, set[int]] = {}
        self._order: dict[Address3, int] = {}
        self._next_order = 0
        # Link width is fixed in each physical owner. Cache only one width, so
        # arbitrary public mapping writes cannot create an unbounded intern pool.
        self._empty_packets: tuple[PacketType | None, ...] | None = None

    def __getitem__(self, position: Address3) -> tuple[PacketType | None, ...]:
        return self._packets[position]

    def __setitem__(self, position: Address3, packets: tuple[PacketType | None, ...]) -> None:
        if packets == self._packets.get(position):
            return
        old_ticks = self._ticks.get(position)
        new_ticks = {packet.arrival_tick for packet in packets if packet is not None}
        if old_ticks != new_ticks:
            if old_ticks is not None:
                for tick in old_ticks - new_ticks:
                    origins = self._due[tick]
                    origins.remove(position)
                    if not origins:
                        del self._due[tick]
            for tick in new_ticks:
                if old_ticks is None or tick not in old_ticks:
                    self._due.setdefault(tick, set()).add(position)
            if new_ticks:
                self._ticks[position] = new_ticks
            else:
                self._ticks.pop(position, None)
        if position not in self._packets:
            self._order[position] = self._next_order
            self._next_order += 1
        if not new_ticks:
            if self._empty_packets is None:
                if packets:
                    self._empty_packets = packets
            elif len(packets) == len(self._empty_packets):
                packets = self._empty_packets
        self._packets[position] = packets

    def __delitem__(self, position: Address3) -> None:
        self[position]
        self[position] = ()
        del self._packets[position]
        del self._order[position]

    def __iter__(self) -> Iterator[Address3]:
        return iter(self._packets)

    def __len__(self) -> int:
        return len(self._packets)

    def __repr__(self) -> str:
        return repr(self._packets)

    def __reversed__(self) -> Iterator[Address3]:
        return reversed(self._packets)

    def copy(self) -> dict[Address3, tuple[PacketType | None, ...]]:
        return self._packets.copy()

    def items(self) -> ItemsView[Address3, tuple[PacketType | None, ...]]:
        return self._packets.items()

    def keys(self) -> KeysView[Address3]:
        return self._packets.keys()

    def values(self) -> ValuesView[tuple[PacketType | None, ...]]:
        return self._packets.values()

    def due(self, tick: int) -> list[Address3]:
        """Return a stable snapshot; failed delivery leaves ownership indexed."""
        return sorted(self._due.get(tick, ()), key=self._order.__getitem__)
