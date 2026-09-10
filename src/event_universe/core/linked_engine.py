"""Engine transport extension; field, geometry and transit arithmetic are injected."""

from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import NamedTuple

from .contracts import FieldActivity, FieldRule, Observer, ParticleRule
from .engine import Engine
from .links import LengthRule, LinkConfig, LinkTransport
from .state import Address, CellState, Config, Neighbors, Vector, checked, validate_cell

TransitRule = Callable[[int, Vector, int], int]


class Transit(NamedTuple):
    direction: int
    departure: int
    length: int
    due: int


class LinkedEngine(Engine):
    """Cell-owned links, delivered neighbor values and frozen integer transits.

    The original five cell fields and twelve particle fields remain unchanged.
    Extra state: thirty link registers per materialized cell; four per transit.
    Fixed K occupancy also bounds in-flight residents per departure cell.
    """

    def __init__(
        self,
        config: Config,
        field_rule: FieldRule,
        particle_rule: ParticleRule,
        observer: Observer | None = None,
        *,
        link_config: LinkConfig,
        length_rule: LengthRule,
        transit_rule: TransitRule,
        merge_rule: LengthRule = max,
        field_activity: FieldActivity | None = None,
    ) -> None:
        super().__init__(config, field_rule, particle_rule, observer, field_activity=field_activity)
        self.links = LinkTransport(self._lattice, link_config, length_rule, merge_rule)
        self._transit_rule = transit_rule
        self._transits: dict[int, Transit] = {}

    @property
    def transits(self) -> Mapping[int, Transit]:
        return MappingProxyType(self._transits)

    def add_particle(
        self, pid: int, x: int, y: int, z: int, px: int = 0, py: int = 0, pz: int = 0
    ) -> "LinkedEngine":
        if self.tick:
            raise RuntimeError("linked candidate accepts initial particles before tick zero only")
        super().add_particle(pid, x, y, z, px, py, pz)
        return self

    def _begin_tick(self) -> None:
        for pid, transit in tuple(self._transits.items()):
            if transit.due != self.tick:
                continue
            position = self._particles[pid].position
            slot = self._occupancy[position].index(pid)
            super()._move(pid, position, slot, transit.direction)
            # A full destination blocks this arrival. Retry requires a new full transit.
            del self._transits[pid]

    def _field_step(self) -> None:
        arrivals = self.links.advance()
        if self.tick == 0:
            # Initial field records must be published before a source-free law replaces them.
            for position, cell in self._cells.items():
                self.links.publish(position, cell.phi)
        work = self._active | arrivals | set(self.links.cells)
        updates: list[tuple[Address, CellState, bool]] = []
        for position in work:
            old = self.cell_at(position)
            sources = sum(pid >= 0 for pid in self._occupancy.get(position, ()))
            new = self._field_rule(old, self.links.at(position).received, sources, self.config)
            validate_cell(new)
            keep = True if self._field_activity is None else self._field_activity(old, new, sources)
            if type(keep) is not bool:
                raise TypeError("field activity policy must return bool")
            updates.append((position, new, keep))
        self._active = set()
        for position, new, keep in updates:
            self._cells[position] = new
            if keep:
                self._active.add(position)
        for position, new, _ in updates:
            self.links.publish(position, new.phi)

    def _particle_neighbors(self, position: Address) -> Neighbors:
        return self.links.at(position).received

    def _particle_ready(self, pid: int) -> bool:
        return pid not in self._transits

    def _move(self, pid: int, origin: Address, slot: int, direction: int) -> None:
        length = self.links.at(origin).lengths[direction]
        duration = checked(
            self._transit_rule(length, self._particles[pid].momentum, self.config.c_units)
        )
        if duration < length:
            raise ValueError("transit exceeds c=1 in the elementary length/time units")
        due = checked(self.tick + duration)
        self._transits[pid] = Transit(direction, self.tick, length, due)
