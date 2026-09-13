"""Local law and observation interfaces; none expose the world to a law or observer."""

from collections.abc import Callable
from typing import NamedTuple, Protocol

from .state import Config, Neighbors, NodeState, ParticleState, Vector


class ParticleUpdate(NamedTuple):
    particle: ParticleState
    node: NodeState
    direction: int
    gradient: Vector
    impulse: Vector


FieldRule = Callable[[NodeState, Neighbors, int, Config], NodeState]
FieldActivity = Callable[[NodeState, NodeState, int], bool]
ParticleRule = Callable[[ParticleState, NodeState, Neighbors, Config, int], ParticleUpdate]
CollisionRule = Callable[[ParticleState, ParticleState], tuple[ParticleState, ParticleState]]


class CollisionRecord(NamedTuple):
    tick: int
    first_pid: int
    second_pid: int
    before_first: ParticleState
    before_second: ParticleState
    after_first: ParticleState
    after_second: ParticleState


LocalCellRule = Callable[[NodeState], NodeState]


class MoveRecord(NamedTuple):
    tick: int
    pid: int
    x: int
    y: int
    z: int


class ForceRecord(NamedTuple):
    tick: int
    pid: int
    x: int
    y: int
    z: int
    gx: int
    gy: int
    gz: int
    ix: int
    iy: int
    iz: int
    old_px: int
    old_py: int
    old_pz: int
    px: int
    py: int
    pz: int


class Observer(Protocol):
    """Receives immutable records after commit. No return value affects physics."""

    def on_move(self, event: MoveRecord) -> None: ...
    def on_force(self, event: ForceRecord) -> None: ...
    def on_blocked(self, event: MoveRecord) -> None: ...
    def on_collision(self, event: CollisionRecord) -> None: ...


class NullObserver:
    """Default: no retained event history."""

    def on_move(self, event: MoveRecord) -> None:
        pass

    def on_force(self, event: ForceRecord) -> None:
        pass

    def on_blocked(self, event: MoveRecord) -> None:
        pass

    def on_collision(self, event: CollisionRecord) -> None:
        pass
