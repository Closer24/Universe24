"""Bounded unit-link matter ownership and delayed release acknowledgements."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import NamedTuple

from .lattice import PeriodicLattice
from .state import EMPTY_SLOT, Address, checked


class MatterPacket(NamedTuple):
    origin: Address
    direction: int
    slot: int
    due: int


class MatterTransport:
    """Six K-slot outbound links per cell; references never duplicate inventory.

    ``packets`` owns matter in transit. ``busy`` only reserves a source link
    slot. An accepted packet leaves link inventory immediately, while a release
    acknowledgement takes a further unit-link tick to reach its sender.
    """

    def __init__(self, lattice: PeriodicLattice, capacity: int) -> None:
        checked(capacity)
        if capacity <= 0:
            raise ValueError("matter capacity must be positive")
        self.lattice = lattice
        self.capacity = capacity
        self._busy: dict[Address, tuple[int, ...]] = {}
        self._packets: dict[int, MatterPacket] = {}
        self._acks: dict[tuple[Address, int], int] = {}

    @property
    def packets(self) -> Mapping[int, MatterPacket]:
        return MappingProxyType(self._packets)

    @property
    def busy(self) -> Mapping[Address, tuple[int, ...]]:
        return MappingProxyType(self._busy)

    def launch(self, pid: int, origin: Address, direction: int, slot: int, tick: int) -> bool:
        for value in (pid, direction, slot, tick):
            checked(value)
        if pid < 0 or tick < 0 or not 0 <= direction < 6 or not 0 <= slot < self.capacity:
            raise ValueError("invalid matter departure")
        if origin != self.lattice.wrap(origin):
            raise ValueError("matter origin must be canonical")
        if pid in self._packets:
            raise ValueError("particle already belongs to a link")
        index = direction * self.capacity + slot
        old = self._busy.get(origin, (EMPTY_SLOT,) * (6 * self.capacity))
        if old[index] != EMPTY_SLOT:
            return False
        due = checked(tick + 1)
        self._busy[origin] = old[:index] + (pid,) + old[index + 1 :]
        self._packets[pid] = MatterPacket(origin, direction, slot, due)
        return True

    def completed(self, tick: int) -> Mapping[Address, tuple[int, ...]]:
        self._check_tick(tick)
        # This host grouping routes each packet to one endpoint. Each endpoint
        # receives at most six links of K slots, regardless of world size.
        arrivals: dict[Address, list[int]] = {}
        for pid, packet in self._packets.items():
            if packet.due <= tick:
                target = self.lattice.neighbor(packet.origin, packet.direction)
                arrivals.setdefault(target, []).append(pid)
        return {
            target: tuple(
                sorted(
                    pids,
                    key=lambda pid: (
                        self._packets[pid].direction ^ 1,
                        self._packets[pid].slot,
                    ),
                )
            )
            for target, pids in arrivals.items()
        }

    def accept(self, pid: int, tick: int) -> None:
        self._check_tick(tick)
        packet = self._packets[pid]
        if tick < packet.due:
            raise ValueError("matter packet has not completed its link")
        due = checked(tick + 1)
        index = packet.direction * self.capacity + packet.slot
        self._acks[packet.origin, index] = due
        del self._packets[pid]

    def receive_acks(self, tick: int) -> None:
        self._check_tick(tick)
        for (origin, index), due in tuple(self._acks.items()):
            if due <= tick:
                old = self._busy[origin]
                new = old[:index] + (EMPTY_SLOT,) + old[index + 1 :]
                if all(pid == EMPTY_SLOT for pid in new):
                    del self._busy[origin]
                else:
                    self._busy[origin] = new
                del self._acks[origin, index]

    @staticmethod
    def _check_tick(tick: int) -> None:
        checked(tick)
        if tick < 0:
            raise ValueError("tick must be non-negative")

    def _reservation(self, key: tuple[Address, int]) -> int:
        slots = self._busy.get(key[0], ())
        if len(slots) != 6 * self.capacity or not 0 <= key[1] < len(slots):
            raise ValueError("invalid matter reservation")
        return slots[key[1]]

    def validate(self) -> None:
        """Check fixed link capacity and exact reservation ownership."""
        claimed: set[tuple[Address, int]] = set()
        for pid, packet in self._packets.items():
            for value in (pid, packet.direction, packet.slot, packet.due):
                checked(value)
            if pid < 0 or not 0 <= packet.direction < 6 or not 0 <= packet.slot < self.capacity:
                raise ValueError("invalid matter packet")
            if packet.due <= 0 or packet.origin != self.lattice.wrap(packet.origin):
                raise ValueError("invalid matter route or arrival tick")
            key = packet.origin, packet.direction * self.capacity + packet.slot
            if key in claimed or self._reservation(key) != pid:
                raise ValueError("matter packet has no unique link reservation")
            claimed.add(key)
        for key, due in self._acks.items():
            checked(due)
            if due <= 0 or key[0] != self.lattice.wrap(key[0]):
                raise ValueError("invalid acknowledgement route or arrival tick")
            if key in claimed or self._reservation(key) == EMPTY_SLOT:
                raise ValueError("release acknowledgement has no unique reservation")
            claimed.add(key)
        for origin, slots in self._busy.items():
            if len(slots) != 6 * self.capacity:
                raise ValueError("invalid outbound matter capacity")
            for index, pid in enumerate(slots):
                checked(pid)
                if (pid != EMPTY_SLOT) != ((origin, index) in claimed):
                    raise ValueError("orphaned outbound reservation")
