"""Fixed physical records and bounded integer arithmetic. No history lives here."""

from dataclasses import dataclass, fields
from typing import NamedTuple

from .integer import MAX_WORK_INT as MAX_WORK_INT
from .integer import checked_work as checked_work
from .integer import signed_divrem as _signed_divrem

Address = tuple[int, int, int]
Vector = tuple[int, int, int]
Neighbors = tuple[int, int, int, int, int, int]

MAX_CORE_INT = (1 << 31) - 1
EMPTY_SLOT = -1
PLUS_X, MINUS_X, PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = range(6)
DIRECTIONS: tuple[Address, ...] = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)
# Index aliases retained for existing notebooks. New code uses named attributes.
PHI, FIELD_PX, FIELD_PY, FIELD_PZ, FIELD_REM = range(5)
X, Y, Z, PX, PY, PZ, MOVE_BUDGET, AXIS_PHASE, FORCE_RX, FORCE_RY, FORCE_RZ, LAST_UPDATE_TICK = range(12)


def checked(value: int) -> int:
    """Reject booleans, non-integers and values outside a physical register."""
    if type(value) is not int:
        raise TypeError("physical registers require int, not bool or float")
    if not -MAX_CORE_INT <= value <= MAX_CORE_INT:
        raise OverflowError("32-bit physical register range exceeded")
    return value


def signed_divrem(numerator: int, denominator: int) -> tuple[int, int]:
    """Divide toward zero, preserving numerator == quotient * denominator + remainder."""
    checked_work(numerator)
    checked(denominator)
    return _signed_divrem(numerator, denominator)


def scaled_divrem(value: int, numerator: int, denominator: int, remainder: int) -> tuple[int, int]:
    """Scale and carry in bounded stages; cancellation cannot conceal product overflow."""
    checked_work(value)
    checked(numerator)
    checked(denominator)
    checked(remainder)
    if denominator <= 0 or abs(remainder) >= denominator:
        raise ValueError("positive denominator and a valid carried remainder are required")
    product = checked_work(numerator * value)
    return signed_divrem(checked_work(product + remainder), denominator)


@dataclass(frozen=True, slots=True)
class Config:
    """Immutable integer model parameters, validated before a world is created."""

    nx: int = 240
    ny: int = 240
    nz: int = 240
    c_units: int = 1000
    source_strength: int = 64
    field_den: int = 7
    force_num: int = 1
    force_den: int = 64
    max_particles_per_cell: int = 4

    def __post_init__(self) -> None:
        for field in fields(self):
            checked(getattr(self, field.name))
        if (
            min(
                self.nx,
                self.ny,
                self.nz,
                self.c_units,
                self.field_den,
                self.force_den,
                self.max_particles_per_cell,
            )
            <= 0
        ):
            raise ValueError("dimensions, denominators, speed cap and capacity must be positive")
        if self.source_strength < 0 or self.force_num < 0:
            raise ValueError("source strength and coupling must be non-negative")


class CellState(NamedTuple):
    phi: int = 0
    px: int = 0
    py: int = 0
    pz: int = 0
    remainder: int = 0


class ParticleState(NamedTuple):
    x: int
    y: int
    z: int
    px: int = 0
    py: int = 0
    pz: int = 0
    move_budget: int = 0
    axis_phase: int = 0
    force_rx: int = 0
    force_ry: int = 0
    force_rz: int = 0
    last_update_tick: int = -1
    mass: int = 1
    momentum_den: int = 1
    move_budget_den: int = 1
    last_collision_tick: int = -1

    @property
    def position(self) -> Address:
        return self.x, self.y, self.z

    @property
    def momentum(self) -> Vector:
        return self.px, self.py, self.pz


CELL_REGISTERS = len(CellState._fields)
PARTICLE_REGISTERS = len(ParticleState._fields)
ZERO_CELL = CellState()


def validate_cell(cell: CellState) -> None:
    for value in cell:
        checked(value)
    if cell.phi < 0:
        raise ValueError("scalar field must be non-negative")


def validate_particle(particle: ParticleState) -> None:
    for value in particle:
        checked(value)
    if min(particle.mass, particle.momentum_den, particle.move_budget_den) < 1:
        raise ValueError("mass and rational denominators must be positive integers")
    if particle.last_collision_tick < -1:
        raise ValueError("invalid collision tick")


def bounded_gcd(first: int, second: int) -> int:
    """Euclid on at most 63 magnitude bits; 128 divisions is a fixed upper bound."""
    a, b = abs(checked_work(first)), abs(checked_work(second))
    for _ in range(128):
        if b == 0:
            return a
        a, b = b, a % b
    raise ArithmeticError("bounded gcd iteration limit exceeded")


def reduced_ratio(numerator: int, denominator: int) -> tuple[int, int]:
    checked_work(numerator)
    checked_work(denominator)
    if denominator <= 0:
        raise ValueError("positive rational denominator required")
    divisor = bounded_gcd(numerator, denominator)
    return checked(numerator // divisor), checked(denominator // divisor)


def reduced_vector(momentum: Vector, denominator: int) -> tuple[Vector, int]:
    """Three numerators sharing one positive bounded integer denominator."""
    checked_work(denominator)
    if len(momentum) != 3 or denominator <= 0:
        raise ValueError("three components and a positive denominator required")
    divisor = denominator
    for value in momentum:
        divisor = bounded_gcd(divisor, value)
    return (
        (
            checked(momentum[0] // divisor),
            checked(momentum[1] // divisor),
            checked(momentum[2] // divisor),
        ),
        checked(denominator // divisor),
    )
