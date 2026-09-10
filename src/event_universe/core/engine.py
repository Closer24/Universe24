"""Sparse storage and tick scheduling. Candidate physical laws are injected.

Local work is bounded by six neighbors and K slots. World iteration, dictionary
storage and active-frontier management have separate, non-constant total costs.
"""

from collections.abc import Mapping
from types import MappingProxyType

from .contracts import (
    FieldActivity,
    FieldRule,
    ForceRecord,
    LocalCellRule,
    MoveRecord,
    NullObserver,
    Observer,
    ParticleRule,
)
from .lattice import PeriodicLattice
from .state import (
    EMPTY_SLOT,
    ZERO_CELL,
    Address,
    CellState,
    Config,
    Neighbors,
    ParticleState,
    checked,
    validate_cell,
    validate_particle,
)


class Engine:
    """One synchronous field phase followed by the legacy sequential movement phase."""

    def __init__(
        self,
        config: Config,
        field_rule: FieldRule,
        particle_rule: ParticleRule,
        observer: Observer | None = None,
        *,
        field_activity: FieldActivity | None = None,
        post_motion_halo: LocalCellRule | None = None,
    ) -> None:
        self._config = config
        self._field_rule = field_rule
        self._field_activity = field_activity
        self._post_motion_halo = post_motion_halo
        self._lattice = PeriodicLattice((config.nx, config.ny, config.nz))
        self._particle_rule = particle_rule
        self._observer = observer if observer is not None else NullObserver()
        self._cells: dict[Address, CellState] = {}
        self._particles: dict[int, ParticleState] = {}
        self._occupancy: dict[Address, tuple[int, ...]] = {}
        self._active: set[Address] = set()
        self._tick = 0
        self._faulted = False

    @property
    def config(self) -> Config:
        return self._config

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def faulted(self) -> bool:
        return self._faulted

    @property
    def cells(self) -> Mapping[Address, CellState]:
        return MappingProxyType(self._cells)

    @property
    def particles(self) -> Mapping[int, ParticleState]:
        return MappingProxyType(self._particles)

    @property
    def occupancy(self) -> Mapping[Address, tuple[int, ...]]:
        return MappingProxyType(self._occupancy)

    @property
    def active(self) -> frozenset[Address]:
        """Diagnostic copy, with O(number of active cells) cost."""
        return frozenset(self._active)

    def addr(self, x: int, y: int, z: int) -> Address:
        return self._lattice.wrap((x, y, z))

    def cell_at(self, position: Address) -> CellState:
        return self._cells.get(self.addr(*position), ZERO_CELL)

    def phi(self, position: Address) -> int:
        return self.cell_at(position).phi

    def _activate(self, position: Address) -> None:
        self._active.add(position)
        self._active.update(self._lattice.neighbors(position))

    def _empty_slots(self) -> tuple[int, ...]:
        return (EMPTY_SLOT,) * self.config.max_particles_per_cell

    def _ensure_healthy(self) -> None:
        if self._faulted:
            raise RuntimeError("world stopped after an update failure; create a new world to resume")

    def seed_field(self, position: Address, phi: int) -> None:
        """Explicit initial-condition API; cannot rewrite an evolving field."""
        self._ensure_healthy()
        if self.tick != 0:
            raise RuntimeError("seed_field is only available before the first tick")
        for value in position:
            checked(value)
        cell = CellState(phi=checked(phi))
        validate_cell(cell)
        address = self.addr(*position)
        self._cells[address] = cell
        self._activate(address)

    def add_particle(
        self, pid: int, x: int, y: int, z: int, px: int = 0, py: int = 0, pz: int = 0
    ) -> "Engine":
        self._ensure_healthy()
        for value in (pid, x, y, z, px, py, pz):
            checked(value)
        if pid < 0:
            raise ValueError("particle ids must be non-negative; -1 denotes an empty slot")
        if pid in self._particles:
            raise ValueError("duplicate particle id")
        position = self.addr(x, y, z)
        slots = self._occupancy.get(position, self._empty_slots())
        if EMPTY_SLOT not in slots:
            raise ValueError("cell particle capacity exceeded")
        slot = slots.index(EMPTY_SLOT)
        particle = ParticleState(*position, px, py, pz)
        validate_particle(particle)
        self._particles[pid] = particle
        self._occupancy[position] = slots[:slot] + (pid,) + slots[slot + 1 :]
        self._activate(position)
        self._observer.on_move(MoveRecord(self.tick, pid, *position))
        return self

    def _field_step(self) -> None:
        work = set(self._active)
        for position in tuple(self._active):
            work.update(self._lattice.neighbors(position))
        old_phi = {position: self.cell_at(position).phi for position in work}

        def previous_value(position: Address) -> int:
            return old_phi.get(position, 0)

        updates: list[tuple[Address, CellState, bool]] = []
        for position in work:
            old = self.cell_at(position)
            sources = sum(pid >= 0 for pid in self._occupancy.get(position, ()))
            new = self._field_rule(
                old, self._lattice.sample(position, previous_value), sources, self.config
            )
            validate_cell(new)
            # Without a quiescence policy, conservatively retain every visited cell.
            keep_active = (
                True if self._field_activity is None else self._field_activity(old, new, sources)
            )
            if type(keep_active) is not bool:
                raise TypeError("field activity policy must return bool")
            updates.append((position, new, keep_active))
        # All field proposals have passed validation before any is committed.
        self._active = set()
        next_active = set()
        for position, new, keep_active in updates:
            self._cells[position] = new
            if keep_active:
                next_active.add(position)
        for position in next_active:
            self._activate(position)

    def _begin_tick(self) -> None:
        """Transport extension hook; the baseline has no in-flight transitions."""

    def _apply_post_motion_halos(self, previous_positions: tuple[tuple[int, Address], ...]) -> None:
        """Apply an optional fixed six-neighbor rule at old and current positions."""
        if self._post_motion_halo is None:
            return
        targets: set[Address] = set()
        for pid, previous in previous_positions:
            targets.update(self._lattice.neighbors(previous))
            targets.update(self._lattice.neighbors(self._particles[pid].position))
        proposals = []
        for address in targets:
            cell = self._post_motion_halo(self.cell_at(address))
            validate_cell(cell)
            proposals.append((address, cell))
        for address, cell in proposals:
            self._cells[address] = cell
            self._activate(address)

    def _particle_ready(self, pid: int) -> bool:
        return True

    def _particle_neighbors(self, position: Address) -> Neighbors:
        return self._lattice.sample(position, self.phi)

    def _particle_step_in_cell(self, position: Address) -> None:
        for slot in range(self.config.max_particles_per_cell):
            # Re-read this fixed slot: an earlier move may have freed or filled it.
            pid = self._occupancy[position][slot]
            if pid == EMPTY_SLOT:
                continue
            old = self._particles[pid]
            if old.last_update_tick == self.tick or not self._particle_ready(pid):
                continue
            result = self._particle_rule(
                old,
                self.cell_at(position),
                self._particle_neighbors(position),
                self.config,
                self.tick,
            )
            validate_cell(result.cell)
            validate_particle(result.particle)
            if result.direction not in (-1, 0, 1, 2, 3, 4, 5):
                raise ValueError("a particle proposal must request at most one cardinal hop")
            if result.particle.position != old.position or result.particle.last_update_tick != self.tick:
                raise ValueError("laws must leave position to the engine and mark the current tick")
            self._cells[position] = result.cell
            self._particles[pid] = result.particle
            self._observer.on_force(
                ForceRecord(
                    self.tick,
                    pid,
                    *position,
                    *result.gradient,
                    *result.impulse,
                    *old.momentum,
                    *result.particle.momentum,
                )
            )
            if result.direction >= 0:
                self._move(pid, position, slot, result.direction)

    def _move(self, pid: int, origin: Address, slot: int, direction: int) -> None:
        target = self._lattice.neighbor(origin, direction)
        target_slots = self._occupancy.setdefault(target, self._empty_slots())
        if EMPTY_SLOT not in target_slots:
            self._observer.on_blocked(MoveRecord(self.tick, pid, *target))
            return
        free = target_slots.index(EMPTY_SLOT)
        origin_slots = self._occupancy[origin]
        self._occupancy[origin] = origin_slots[:slot] + (EMPTY_SLOT,) + origin_slots[slot + 1 :]
        # A one-cell periodic dimension can make target == origin.
        target_slots = self._occupancy[target]
        self._occupancy[target] = target_slots[:free] + (pid,) + target_slots[free + 1 :]
        self._particles[pid] = self._particles[pid]._replace(x=target[0], y=target[1], z=target[2])
        self._observer.on_move(MoveRecord(self.tick, pid, *target))
        self._activate(origin)
        self._activate(target)

    def step(self) -> "Engine":
        """Advance once. Failed ticks are terminal; successful local commits are retained."""
        self._ensure_healthy()
        next_tick = checked(self.tick + 1)
        try:
            previous_positions = tuple(
                (pid, particle.position) for pid, particle in self._particles.items()
            )
            self._begin_tick()
            self._field_step()
            # Legacy order is part of this model's movement/conflict semantics.
            for position in tuple(self._occupancy):
                self._particle_step_in_cell(position)
            self._apply_post_motion_halos(previous_positions)
            self._tick = next_tick
        except Exception:
            self._faulted = True
            raise
        return self

    def run(self, ticks: int) -> "Engine":
        """Low-level advance; the application runner owns HTML and run metadata."""
        checked(ticks)
        if ticks < 0:
            raise ValueError("ticks must be non-negative")
        for _ in range(ticks):
            self.step()
        return self
