"""One-edge scalar packet transport with a persisted six-face local inbox."""

from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import cast

from .lattice import PeriodicLattice
from .state import Address, Neighbors, checked

FacePublisher = Callable[[int], Neighbors]
ZERO_FACES: Neighbors = (0, 0, 0, 0, 0, 0)
FACE_REGISTERS = 6


class ScalarFaceTransport:
    """Publish old local values through six ports; no response-time neighbor reads.

    Publisher output uses outgoing travel directions. Incoming storage uses the
    opposite, source-facing direction. An immutable old publication is routed
    once; newly delivered values never become sources in the same advance.
    """

    def __init__(self, lattice: PeriodicLattice, publisher: FacePublisher) -> None:
        self._lattice = lattice
        self._publisher = publisher
        self._cells: dict[Address, Neighbors] = {}
        if any(self._outgoing(0)):
            raise ValueError("sparse face publisher must preserve a zero value")

    def _outgoing(self, value: int) -> Neighbors:
        outgoing = self._publisher(checked(value))
        if not isinstance(outgoing, tuple) or len(outgoing) != 6:
            raise ValueError("publisher must return a fixed six-integer tuple")
        for amount in outgoing:
            checked(amount)
        return outgoing

    @property
    def cells(self) -> Mapping[Address, Neighbors]:
        return MappingProxyType(self._cells)

    def at(self, position: Address) -> Neighbors:
        return self._cells.get(position, ZERO_FACES)

    def advance(self, published: Mapping[Address, int]) -> None:
        proposals: dict[Address, list[int]] = {}
        for origin, value in tuple(published.items()):
            if self._lattice.wrap(origin) != origin:
                raise ValueError("canonical publication address required")
            outgoing = self._outgoing(value)
            for direction, amount in enumerate(outgoing):
                checked(amount)
                target = self._lattice.neighbor(origin, direction)
                incoming = proposals.setdefault(target, [0] * 6)
                incoming[direction ^ 1] = amount
        # Each face has exactly one neighboring sender, including periodic seams.
        # Zero publications erase old deliveries; proposals commit only together.
        self._cells = {
            address: cast(Neighbors, tuple(values))
            for address, values in proposals.items()
            if any(values)
        }

    def validate(self) -> None:
        """Read-only global diagnostic; never a physical repair."""
        for address, values in self._cells.items():
            if self._lattice.wrap(address) != address or len(values) != 6:
                raise ValueError("invalid delivered-face record")
            for value in values:
                checked(value)
