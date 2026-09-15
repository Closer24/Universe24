"""Local output banks with a host-only address index for transport."""

from collections.abc import Iterator, MutableMapping
from dataclasses import dataclass

from .disturbance_state import Address3, Packet
from .spatial_state import SpatialPacket


@dataclass(slots=True)
class PortBank[PacketType: Packet | SpatialPacket]:
    """One node's fixed output slots; contains no address lookup or world."""

    packets: tuple[PacketType | None, ...]
    visible: int = 0

    def publish(self, packets: tuple[PacketType | None, ...]) -> None:
        if type(packets) is not tuple or len(packets) != len(self.packets):
            raise ValueError("node output bank capacity cannot change")
        self.packets = packets
        self.visible = 1


class PortTable[PacketType: Packet | SpatialPacket](
    MutableMapping[Address3, tuple[PacketType | None, ...]]
):
    """Transport owns the index; a node receives only its own bank."""

    def __init__(self, empty: tuple[PacketType | None, ...]) -> None:
        self._empty = empty
        self._banks: dict[Address3, PortBank[PacketType]] = {}
        self._order: dict[Address3, int] = {}
        self._active: set[Address3] = set()
        self.active_visits = 0

    def bank(self, position: Address3) -> PortBank[PacketType]:
        bank = self._banks.get(position)
        if bank is None:
            self._order[position] = len(self._banks)
            bank = self._banks[position] = PortBank(self._empty)
        return bank

    def __getitem__(self, position: Address3) -> tuple[PacketType | None, ...]:
        bank = self._banks[position]
        if not bank.visible:
            raise KeyError(position)
        return bank.packets

    def __setitem__(self, position: Address3, packets: tuple[PacketType | None, ...]) -> None:
        self.bank(position).publish(packets)
        self.refresh(position)

    def __delitem__(self, position: Address3) -> None:
        bank = self._banks[position]
        if not bank.visible:
            raise KeyError(position)
        bank.packets, bank.visible = self._empty, 0
        self._active.discard(position)

    def __iter__(self) -> Iterator[Address3]:
        return (position for position, bank in self._banks.items() if bank.visible)

    def __len__(self) -> int:
        return sum(bank.visible for bank in self._banks.values())

    def refresh(self, position: Address3) -> None:
        """Index one owner after a local transition; never enter physical NodeState."""
        bank = self._banks.get(position)
        if bank is not None and bank.visible and any(p is not None for p in bank.packets):
            self._active.add(position)
        else:
            self._active.discard(position)

    def active_items(self) -> Iterator[tuple[Address3, tuple[PacketType | None, ...]]]:
        """Snapshot active addresses in original bank order, including reactivation.

        Delivery may empty a bank during iteration. Nodes retain their fixed banks
        and the public mapping retains empty visible entries for exact snapshots.
        """
        positions = sorted(self._active, key=self._order.__getitem__)
        self.active_visits += len(positions)
        return ((position, self._banks[position].packets) for position in positions)

    def execution_report(self) -> dict[str, int]:
        return {"active_banks": len(self._active), "bank_visits": self.active_visits}
