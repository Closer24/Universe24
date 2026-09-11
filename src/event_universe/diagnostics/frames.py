"""Copied diagnostic frames with explicit projection axes and true lattice coordinates."""

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Literal, NamedTuple

from event_universe.core.engine import Engine
from event_universe.core.generic_engine import GenericEngine
from event_universe.core.state import Address, Neighbors, checked
from event_universe.core.streaming_engine import StreamingEngine

from .measurements import ExactVector, total_momentum

Plane = Literal["XY", "XZ", "YZ"]
FieldKind = Literal["scalar", "stream-magnitude", "face-magnitude"]
AXES: dict[Plane, tuple[int, int, int]] = {"XY": (0, 1, 2), "XZ": (0, 2, 1), "YZ": (1, 2, 0)}


class LinkParticle(NamedTuple):
    pid: int
    origin: Address
    direction: int
    due: int
    momentum: tuple[int, int, int]
    mass: int
    momentum_den: int


def _link_particles(world: Engine) -> list[LinkParticle]:
    transport = getattr(world, "matter_transport", None)
    if transport is None:
        return []
    return [
        LinkParticle(
            pid,
            packet.origin,
            packet.direction,
            packet.due,
            world.particles[pid].momentum,
            world.particles[pid].mass,
            world.particles[pid].momentum_den,
        )
        for pid, packet in sorted(transport.packets.items())
    ]


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
    field_kind: FieldKind = "scalar"
    field_faces: dict[Address, Neighbors] = dataclass_field(default_factory=dict)
    faces_available: bool = False
    primary_field_name: str | None = None
    field_faces_by_name: dict[str, dict[Address, Neighbors]] = dataclass_field(default_factory=dict)
    field_inventory_by_name: dict[str, dict[Address, tuple[int, ...]]] = dataclass_field(
        default_factory=dict
    )
    link_particles: list[LinkParticle] = dataclass_field(default_factory=list)


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
    field_faces: dict[Address, Neighbors] = dataclass_field(default_factory=dict)
    faces_available: bool = False
    primary_field_name: str | None = None
    field_faces_by_name: dict[str, dict[Address, Neighbors]] = dataclass_field(default_factory=dict)
    field_inventory_by_name: dict[str, dict[Address, tuple[int, ...]]] = dataclass_field(
        default_factory=dict
    )
    link_particles: list[LinkParticle] = dataclass_field(default_factory=list)


def _field_snapshot(world: Engine) -> tuple[dict[tuple[int, int, int], int], FieldKind]:
    """Copy diagnostic intensity without writing or materializing physical records."""
    if isinstance(world, GenericEngine):
        return (
            {
                position: magnitude
                for position, values in world.field_faces.items()
                if (magnitude := sum(abs(value) for value in values)) != 0
            },
            "face-magnitude",
        )
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


def _face_snapshot(world: Engine) -> tuple[dict[Address, Neighbors], bool]:
    """Copy delivered records; missing sparse addresses have six zero values."""
    source = getattr(world, "field_faces", None)
    if source is None:
        return {}, False
    faces = dict(source)
    for particle in world.particles.values():
        faces.setdefault(particle.position, (0, 0, 0, 0, 0, 0))
    return faces, True


def capture_volume(world: Engine) -> VolumeFrame:
    """Copy nonzero field intensity and each particle in full XYZ coordinates."""
    field, field_kind = _field_snapshot(world)
    faces, faces_available = _face_snapshot(world)
    links = _link_particles(world)
    link_ids = {p.pid for p in links}
    return VolumeFrame(
        world.tick,
        field,
        [
            (pid, *particle.position, *particle.momentum)
            for pid, particle in world.particles.items()
            if pid not in link_ids
        ],
        total_momentum(world),
        world.config.c_units,
        (world.config.nx, world.config.ny, world.config.nz),
        {pid: (p.mass, p.momentum_den) for pid, p in world.particles.items()},
        field_kind,
        faces,
        faces_available,
        getattr(world, "display_field_name", None),
        {name: dict(records) for name, records in getattr(world, "field_faces_by_name", {}).items()},
        {name: dict(records) for name, records in getattr(world, "field_inventory_by_name", {}).items()},
        links,
    )


def capture_frame(world: Engine, view: Slice) -> Frame:
    horizontal, vertical, fixed = AXES[view.plane]
    shape = (world.config.nx, world.config.ny, world.config.nz)
    if not 0 <= view.coordinate < shape[fixed]:
        raise ValueError("slice coordinate outside the simulation domain")
    values, field_kind = _field_snapshot(world)
    field = {
        (p[horizontal], p[vertical]): value for p, value in values.items() if p[fixed] == view.coordinate
    }
    links = _link_particles(world)
    link_ids = {p.pid for p in links}
    particles = [
        (pid, p[horizontal], p[vertical], p[3 + horizontal], p[3 + vertical], p[3 + fixed])
        for pid, p in world.particles.items()
        if p[fixed] == view.coordinate and pid not in link_ids
    ]
    all_faces, faces_available = _face_snapshot(world)
    faces = {
        position: values for position, values in all_faces.items() if position[fixed] == view.coordinate
    }
    return Frame(
        world.tick,
        field,
        particles,
        total_momentum(world),
        field_kind,
        faces,
        faces_available,
        getattr(world, "display_field_name", None),
        {
            name: {p: values for p, values in records.items() if p[fixed] == view.coordinate}
            for name, records in getattr(world, "field_faces_by_name", {}).items()
        },
        {
            name: {p: values for p, values in records.items() if p[fixed] == view.coordinate}
            for name, records in getattr(world, "field_inventory_by_name", {}).items()
        },
        [p for p in links if p.origin[fixed] == view.coordinate],
    )
