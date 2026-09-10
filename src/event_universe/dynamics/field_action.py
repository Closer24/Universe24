"""One local action: exchange an impulse, then schedule the resulting motion.

Response and movement remain replaceable generic components. The action does
not own a field, interpret sources, or keep state between calls. In particular,
it never applies a second independent "speed force" after changing momentum.
"""

from dataclasses import dataclass
from typing import NamedTuple

from event_universe.core.state import Vector
from event_universe.dynamics.movement import MovementResult, MovementRule
from event_universe.dynamics.turning import FieldTurning, TurningResult


class FieldActionResult(NamedTuple):
    response: TurningResult
    motion: MovementResult


@dataclass(frozen=True, slots=True)
class UnifiedFieldAction:
    """Pure bounded local composition; the model chooses both component laws."""

    response: FieldTurning
    movement: MovementRule

    def apply(
        self,
        momentum: Vector,
        field_momentum: Vector,
        field_vector: Vector,
        remainders: Vector,
        budget: int,
        phase: int,
        *,
        numerator: int,
        denominator: int,
        speed_cap: int,
    ) -> FieldActionResult:
        response = self.response.apply(
            momentum,
            field_momentum,
            field_vector,
            remainders,
            numerator=numerator,
            denominator=denominator,
        )
        motion = self.movement(response.momentum, budget, phase, speed_cap=speed_cap)
        return FieldActionResult(response, motion)
