"""Fixed-port causal transport. Geometry is supplied as a pure local callable.

Positive ports own the edge record. Both endpoints can propose a length on the
OLD edge. At delivery both endpoints know the proposal; simultaneous proposals
use an injected symmetric merge policy. Ownership never biases the physical law.
No receiver reads a newly computed remote field or geometry register.
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import NamedTuple, cast

from .lattice import PeriodicLattice
from .state import Address, Neighbors, checked

LengthRule = Callable[[int, int], int]


@dataclass(frozen=True, slots=True)
class LinkConfig:
    base_length: int = 100
    stretch_num: int = 1
    stretch_den: int = 1

    def __post_init__(self) -> None:
        for value in (self.base_length, self.stretch_num, self.stretch_den):
            checked(value)
        if self.base_length < 1 or self.stretch_num < 0 or self.stretch_den < 1:
            raise ValueError("invalid link scale or stretch ratio")


class Packet(NamedTuple):
    value: int = 0
    announced_length: int = 0  # proposal activated at delivery, never a remote write
    remaining: int = 0


Ports = tuple[Packet, Packet, Packet, Packet, Packet, Packet]


class LinkNodeState(NamedTuple):
    received: Neighbors
    lengths: Neighbors  # positive authoritative lengths, negative received copies
    outgoing: Ports


ZERO_VALUES: Neighbors = (0, 0, 0, 0, 0, 0)
EMPTY_PORTS: Ports = (Packet(), Packet(), Packet(), Packet(), Packet(), Packet())
LINK_REGISTERS = 30  # 6 received + 6 lengths + 6 * 3 packet integers


class LinkTransport:
    """Six bounded serial ports per node; no queues or source-tagged histories."""

    def __init__(
        self,
        lattice: PeriodicLattice,
        config: LinkConfig,
        length_rule: LengthRule,
        merge_rule: LengthRule = max,
    ) -> None:
        self.lattice = lattice
        self.config = config
        self.length_rule = length_rule
        self.merge_rule = merge_rule
        self._nodes: dict[Address, LinkNodeState] = {}
        self._zero = LinkNodeState(ZERO_VALUES, (config.base_length,) * 6, EMPTY_PORTS)

    @property
    def nodes(self) -> Mapping[Address, LinkNodeState]:
        return MappingProxyType(self._nodes)

    def at(self, position: Address) -> LinkNodeState:
        return self._nodes.get(position, self._zero)

    def owner(self, position: Address, direction: int) -> tuple[Address, int]:
        if type(direction) is not int or not 0 <= direction < 6:
            raise ValueError("invalid port")
        if direction % 2 == 0:
            return position, direction
        return self.lattice.neighbor(position, direction), direction ^ 1

    def advance(self) -> set[Address]:
        """Deliver only packets already in flight; commit all mailbox changes together."""
        updates: dict[Address, LinkNodeState] = {}
        arrivals: set[Address] = set()
        geometry: dict[tuple[Address, int], int] = {}
        for origin, old in self._nodes.items():
            for direction, packet in enumerate(old.outgoing):
                if packet.remaining == 0:
                    continue
                current = updates.get(origin, old)
                ports = list(current.outgoing)
                ports[direction] = packet._replace(remaining=packet.remaining - 1)
                updates[origin] = current._replace(outgoing=cast(Ports, tuple(ports)))
                if packet.remaining != 1:
                    continue
                target = self.lattice.neighbor(origin, direction)
                destination = updates.get(target, self.at(target))
                received = list(destination.received)
                received[direction ^ 1] = packet.value
                updates[target] = destination._replace(received=cast(Neighbors, tuple(received)))
                arrivals.add(target)
                if packet.announced_length:
                    edge = self.owner(origin, direction)
                    proposal = packet.announced_length
                    if edge in geometry:
                        proposal = checked(self.merge_rule(geometry[edge], proposal))
                    if proposal < self.config.base_length:
                        raise ValueError("merged length is below the base length")
                    geometry[edge] = proposal
        for (owner, direction), length in geometry.items():
            other = self.lattice.neighbor(owner, direction)
            # Both ends have identical local evidence: their own delivered proposal
            # and the opposite packet that just arrived. No extra broadcast occurs.
            for address, port in ((owner, direction), (other, direction ^ 1)):
                endpoint = updates.get(address, self.at(address))
                lengths = list(endpoint.lengths)
                lengths[port] = length
                updates[address] = endpoint._replace(lengths=cast(Neighbors, tuple(lengths)))
        self._nodes.update(updates)
        return arrivals

    def publish(self, position: Address, value: int) -> None:
        """Compute from this node and its delivered inbox, never raw remote state."""
        checked(value)
        if value < 0:
            raise ValueError("nonnegative field required")
        old = self.at(position)
        outgoing = list(old.outgoing)
        for direction in range(6):
            previous = outgoing[direction]
            if previous.remaining:
                continue
            announced = checked(self.length_rule(value, old.received[direction]))
            if announced < self.config.base_length:
                raise ValueError("link law must not shorten below base length")
            if previous.value == value and (not announced or announced == old.lengths[direction]):
                continue
            outgoing[direction] = Packet(value, announced, old.lengths[direction])
        new = old._replace(outgoing=cast(Ports, tuple(outgoing)))
        if new != self._zero:
            self._nodes[position] = new

    def validate(self) -> None:
        """Global read-only diagnostic, never used as a physical correction."""
        for position, node in self._nodes.items():
            if len(node.received) != 6 or len(node.lengths) != 6 or len(node.outgoing) != 6:
                raise ValueError("fixed six-port schema required")
            for value in (*node.received, *node.lengths):
                checked(value)
            for direction, packet in enumerate(node.outgoing):
                for value in packet:
                    checked(value)
                if min(packet) < 0:
                    raise ValueError("invalid packet")
                if node.lengths[direction] < self.config.base_length:
                    raise ValueError("invalid length")
                other = self.at(self.lattice.neighbor(position, direction))
                if node.lengths[direction] != other.lengths[direction ^ 1]:
                    raise ValueError("edge endpoints disagree about active geometry")
