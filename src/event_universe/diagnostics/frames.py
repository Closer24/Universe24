"""Copied diagnostic frames with explicit projection axes and true lattice coordinates."""

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Literal

from event_universe.core.engine import Engine
from event_universe.core.state import checked

from .measurements import ExactVector, total_momentum

Plane = Literal["XY", "XZ", "YZ"]
AXES: dict[Plane, tuple[int, int, int]] = {"XY": (0, 1, 2), "XZ": (0, 2, 1), "YZ": (1, 2, 0)}


@dataclass(frozen=True, slots=True)
class Slice:
    plane: Plane = "XY"
    coordinate: int = 0

    def __post_init__(self) -> None:
        if self.plane not in AXES:
            raise ValueError("plane must be XY, XZ or YZ")
        checked(self.coordinate)


@dataclass(slots=True)
class Frame:
    tick: int
    field: dict[tuple[int, int], int]
    particles: list[tuple[int, int, int, int, int, int]]
    total_momentum: ExactVector


@dataclass(slots=True)
class VolumeFrame:
    tick: int
    field: dict[tuple[int, int, int], int]
    particles: list[tuple[int, int, int, int, int, int, int]]
    total_momentum: ExactVector
    c_units: int | None = None
    shape: tuple[int, int, int] | None = None
    particle_scales: dict[int, tuple[int, int]] = dataclass_field(default_factory=dict)


def capture_volume(world: Engine) -> VolumeFrame:
    """Copy every nonzero scalar cell and each particle in full XYZ coordinates."""
    return VolumeFrame(
        world.tick,
        {position: cell.phi for position, cell in world.cells.items() if cell.phi != 0},
        [(pid, *particle.position, *particle.momentum) for pid, particle in world.particles.items()],
        total_momentum(world),
        world.config.c_units,
        (world.config.nx, world.config.ny, world.config.nz),
        {pid: (p.mass, p.momentum_den) for pid, p in world.particles.items()},
    )


def capture_frame(world: Engine, view: Slice) -> Frame:
    horizontal, vertical, fixed = AXES[view.plane]
    shape = (world.config.nx, world.config.ny, world.config.nz)
    if not 0 <= view.coordinate < shape[fixed]:
        raise ValueError("slice coordinate outside the simulation domain")
    field = {
        (p[horizontal], p[vertical]): c.phi
        for p, c in world.cells.items()
        if p[fixed] == view.coordinate and c.phi != 0
    }
    particles = [
        (pid, p[horizontal], p[vertical], p[3 + horizontal], p[3 + vertical], p[3 + fixed])
        for pid, p in world.particles.items()
        if p[fixed] == view.coordinate
    ]
    return Frame(world.tick, field, particles, total_momentum(world))
