"""Copied diagnostic frames with explicit projection axes and true lattice coordinates."""

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Literal

from event_universe.core.scalar_engine import ScalarEngine
from event_universe.core.state import checked
from event_universe.core.streaming_engine import StreamingEngine

from .measurements import ExactVector, total_momentum

Plane = Literal["XY", "XZ", "YZ"]
FieldKind = Literal["scalar", "stream-magnitude"]
AXES: dict[Plane, tuple[int, int, int]] = {"XY": (0, 1, 2), "XZ": (0, 2, 1), "YZ": (1, 2, 0)}


@dataclass(frozen=True, slots=True)
class Slice:
    plane: Plane = "XY"
    coordinate: int = 0

    def __post_init__(self) -> None:
        if self.plane not in AXES:
            raise ValueError("plane must be XY, XZ or YZ")
        checked(self.coordinate)

    def validate_shape(self, shape: tuple[int, int, int]) -> None:
        """Reject a slice outside its domain without capturing an unused projection."""
        if not 0 <= self.coordinate < shape[AXES[self.plane][2]]:
            raise ValueError("slice coordinate outside the simulation domain")


@dataclass(slots=True)
class Frame:
    tick: int
    field: dict[tuple[int, int], int]
    particles: list[tuple[int, int, int, int, int, int]]
    total_momentum: ExactVector
    field_kind: FieldKind = "scalar"


@dataclass(slots=True)
class VolumeFrame:
    tick: int
    field: dict[tuple[int, int, int], int]
    particles: list[tuple[int, int, int, int, int, int, int]]
    total_momentum: ExactVector
    c_units: int | None = None
    shape: tuple[int, int, int] | None = None
    particle_scales: dict[int, tuple[int, int]] = dataclass_field(default_factory=dict)
    field_kind: FieldKind = "scalar"


def _field_snapshot(world: ScalarEngine) -> tuple[dict[tuple[int, int, int], int], FieldKind]:
    """Copy diagnostic intensity without writing or materializing physical records."""
    if isinstance(world, StreamingEngine):
        return (
            {
                position: magnitude
                for position, cell in world.streams.cells.items()
                if (magnitude := sum(cell.populations)) != 0
            },
            "stream-magnitude",
        )
    return {position: cell.phi for position, cell in world.cells.items() if cell.phi != 0}, "scalar"


def capture_volume(world: ScalarEngine, *, momentum: ExactVector | None = None) -> VolumeFrame:
    """Copy full XYZ state, optionally reusing momentum measured from this same state."""
    field, field_kind = _field_snapshot(world)
    return VolumeFrame(
        world.tick,
        field,
        [(pid, *particle.position, *particle.momentum) for pid, particle in world.particles.items()],
        total_momentum(world) if momentum is None else momentum,
        world.config.c_units,
        (world.config.nx, world.config.ny, world.config.nz),
        {pid: (p.mass, p.momentum_den) for pid, p in world.particles.items()},
        field_kind,
    )


def capture_frame(world: ScalarEngine, view: Slice, *, momentum: ExactVector | None = None) -> Frame:
    """Copy a slice, optionally reusing momentum measured from this same state."""
    horizontal, vertical, fixed = AXES[view.plane]
    shape = (world.config.nx, world.config.ny, world.config.nz)
    view.validate_shape(shape)
    values, field_kind = _field_snapshot(world)
    field = {
        (p[horizontal], p[vertical]): value for p, value in values.items() if p[fixed] == view.coordinate
    }
    particles = [
        (pid, p[horizontal], p[vertical], p[3 + horizontal], p[3 + vertical], p[3 + fixed])
        for pid, p in world.particles.items()
        if p[fixed] == view.coordinate
    ]
    return Frame(
        world.tick,
        field,
        particles,
        total_momentum(world) if momentum is None else momentum,
        field_kind,
    )
