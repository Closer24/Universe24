"""One periodic six-neighbor geometry for field reads, activity and movement."""

from collections.abc import Callable
from dataclasses import dataclass

from .state import DIRECTIONS, Address, Neighbors, checked, checked_work

NeighborAddresses = tuple[Address, Address, Address, Address, Address, Address]


@dataclass(frozen=True, slots=True)
class PeriodicLattice:
    shape: Address

    def __post_init__(self) -> None:
        if not isinstance(self.shape, tuple) or len(self.shape) != 3:
            raise ValueError("exactly three immutable dimensions are required")
        for size in self.shape:
            checked(size)
            if size <= 0:
                raise ValueError("lattice dimensions must be positive")

    def wrap(self, position: Address) -> Address:
        x, y, z = position
        return (
            checked_work(x) % self.shape[0],
            checked_work(y) % self.shape[1],
            checked_work(z) % self.shape[2],
        )

    def neighbor(self, position: Address, direction: int) -> Address:
        checked(direction)
        if not 0 <= direction < len(DIRECTIONS):
            raise ValueError("a cardinal direction is required")
        dx, dy, dz = DIRECTIONS[direction]
        x, y, z = self.wrap(position)
        return self.wrap((x + dx, y + dy, z + dz))

    def neighbors(self, position: Address) -> NeighborAddresses:
        a, b, c, d, e, f = (self.neighbor(position, direction) for direction in range(6))
        return a, b, c, d, e, f

    def sample(self, position: Address, value_at: Callable[[Address], int]) -> Neighbors:
        a, b, c, d, e, f = (value_at(address) for address in self.neighbors(position))
        return a, b, c, d, e, f
