"""Generic response to a supplied field vector, with exact local momentum exchange."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import NamedTuple

from event_universe.core.state import Vector, checked, checked_work, scaled_divrem

DirectionSelector = Callable[[Vector, Vector], Vector]


def full_response(momentum: Vector, field_vector: Vector) -> Vector:
    """Use every component of the supplied vector."""
    return field_vector


def dominant_axis_transverse(momentum: Vector, field_vector: Vector) -> Vector:
    """Suppress the dominant motion axis; ties choose x, then y, then z.

    This is a selectable discrete policy, not an orthogonal vector projection.
    """
    ax, ay, az = (abs(component) for component in momentum)
    gx, gy, gz = field_vector
    if ax >= ay and ax >= az and ax != 0:
        return 0, gy, gz
    if ay >= az and ay != 0:
        return gx, 0, gz
    if az != 0:
        return gx, gy, 0
    return field_vector


class TurningResult(NamedTuple):
    momentum: Vector
    field_momentum: Vector
    remainders: Vector
    impulse: Vector


@dataclass(frozen=True, slots=True)
class FieldTurning:
    """Shared impulse/remainder/exchange algorithm; the model selects direction.

    The input may be a scalar gradient or another local field vector. This operation
    does not know how the field was calculated or stored.
    """

    select_direction: DirectionSelector

    def apply(
        self,
        momentum: Vector,
        field_momentum: Vector,
        field_vector: Vector,
        remainders: Vector,
        *,
        numerator: int,
        denominator: int,
    ) -> TurningResult:
        checked(numerator)
        checked(denominator)
        if denominator <= 0:
            raise ValueError("positive denominator required")
        for vector in (momentum, field_momentum, remainders):
            if len(vector) != 3:
                raise ValueError("exactly three components are required")
            for component in vector:
                checked(component)
        if any(abs(remainder) >= denominator for remainder in remainders):
            raise ValueError("invalid carried response remainder")
        if len(field_vector) != 3:
            raise ValueError("exactly three field components are required")
        for component in field_vector:
            checked_work(component)
        selected = self.select_direction(momentum, field_vector)
        if len(selected) != 3:
            raise ValueError("direction selector must return three components")
        for component in selected:
            checked_work(component)
        ix, rx = scaled_divrem(selected[0], numerator, denominator, remainders[0])
        iy, ry = scaled_divrem(selected[1], numerator, denominator, remainders[1])
        iz, rz = scaled_divrem(selected[2], numerator, denominator, remainders[2])
        # Both sides are bounded before a result can be committed.
        next_momentum = (checked(momentum[0] + ix), checked(momentum[1] + iy), checked(momentum[2] + iz))
        next_field = (
            checked(field_momentum[0] - ix),
            checked(field_momentum[1] - iy),
            checked(field_momentum[2] - iz),
        )
        return TurningResult(
            next_momentum,
            next_field,
            (checked(rx), checked(ry), checked(rz)),
            (checked_work(ix), checked_work(iy), checked_work(iz)),
        )
