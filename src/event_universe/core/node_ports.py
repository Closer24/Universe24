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

    def bank(self, position: Address3) -> PortBank[PacketType]:
        bank = self._banks.get(position)
        if bank is None:
            bank = self._banks[position] = PortBank(self._empty)
        return bank

    def __getitem__(self, position: Address3) -> tuple[PacketType | None, ...]:
        bank = self._banks[position]
        if not bank.visible:
            raise KeyError(position)
        return bank.packets

    def __setitem__(self, position: Address3, packets: tuple[PacketType | None, ...]) -> None:
        self.bank(position).publish(packets)

    def __delitem__(self, position: Address3) -> None:
        bank = self._banks[position]
        if not bank.visible:
            raise KeyError(position)
        bank.packets, bank.visible = self._empty, 0

    def __iter__(self) -> Iterator[Address3]:
        return (position for position, bank in self._banks.items() if bank.visible)

    def __len__(self) -> int:
        return sum(bank.visible for bank in self._banks.values())
