"""Fixed-state routing for outward causal field populations."""

from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import NamedTuple, cast

from .lattice import PeriodicLattice
from .state import Address, Neighbors, checked, checked_work

Octants = tuple[int, int, int, int, int, int, int, int]
Outgoing = tuple[Octants, Octants, Octants, Octants, Octants, Octants]
StreamRule = Callable[[Octants, int, int, int], Outgoing]
ZERO_OCTANTS: Octants = (0, 0, 0, 0, 0, 0, 0, 0)
ZERO_FLUX: Neighbors = (0, 0, 0, 0, 0, 0)


class StreamCell(NamedTuple):
    populations: Octants = ZERO_OCTANTS
    flux: Neighbors = ZERO_FLUX


STREAM_CELL_REGISTERS = 14


class StreamTransport:
    """Route fixed octant populations exactly one cardinal link per tick."""

    def __init__(self, lattice: PeriodicLattice, rule: StreamRule, source_per_octant: int) -> None:
        checked(source_per_octant)
        if source_per_octant < 0:
            raise ValueError("source stream strength must be non-negative")
        self._lattice = lattice
        self._rule = rule
        self._source_per_octant = source_per_octant
        self._cells: dict[Address, StreamCell] = {}

    @property
    def cells(self) -> Mapping[Address, StreamCell]:
        return MappingProxyType(self._cells)

    def at(self, position: Address) -> StreamCell:
        return self._cells.get(position, StreamCell())

    def advance(self, sources: Mapping[Address, int], phase: int) -> None:
        checked(phase)
        if phase < 0:
            raise ValueError("non-negative stream phase required")
        work = set(self._cells) | set(sources)
        next_populations: dict[Address, list[int]] = {}
        next_flux: dict[Address, list[int]] = {}
        for origin in work:
            count = sources.get(origin, 0)
            checked(count)
            if count < 0:
                raise ValueError("source count cannot be negative")
            outgoing = self._rule(self.at(origin).populations, count, self._source_per_octant, phase)
            if len(outgoing) != 6:
                raise ValueError("stream rule must return six outgoing ports")
            for direction, packet in enumerate(outgoing):
                if len(packet) != 8:
                    raise ValueError("each stream packet requires eight octants")
                target = self._lattice.neighbor(origin, direction)
                populations = next_populations.setdefault(target, [0] * 8)
                amount = 0
                for octant, value in enumerate(packet):
                    checked(value)
                    if value < 0:
                        raise ValueError("stream populations must be non-negative")
                    populations[octant] = checked(checked_work(populations[octant] + value))
                    amount = checked(checked_work(amount + value))
                flux = next_flux.setdefault(target, [0] * 6)
                flux[direction] = checked(checked_work(flux[direction] + amount))
        cells: dict[Address, StreamCell] = {}
        for position in set(next_populations) | set(next_flux):
            final_populations = cast(Octants, tuple(next_populations.get(position, [0] * 8)))
            final_flux = cast(Neighbors, tuple(next_flux.get(position, [0] * 6)))
            if any(final_populations) or any(final_flux):
                cells[position] = StreamCell(final_populations, final_flux)
        self._cells = cells
