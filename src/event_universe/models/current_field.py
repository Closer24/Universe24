"""Our v10-contact model: local source meaning, nonnegative field and response choices.

Reusable arithmetic lives in fields/ and dynamics/. This adapter alone maps
their records to the simulator's fixed cell and particle state.
"""

from dataclasses import dataclass

from event_universe.core.contracts import ParticleUpdate
from event_universe.core.state import (
    CellState,
    Config,
    Neighbors,
    ParticleState,
    checked,
    validate_cell,
    validate_particle,
)
from event_universe.dynamics.movement import MovementRule, advance_movement
from event_universe.dynamics.turning import FieldTurning, dominant_axis_transverse
from event_universe.fields.halo import cancel_scalar_sample
from event_universe.fields.policies import (
    ScalarActivity,
    nonnegative_sample,
    uniform_source,
    value_changed_or_source,
)
from event_universe.fields.scalar import (
    ScalarField,
    ScalarFieldRule,
    ScalarSample,
    gradient,
    validate_sample,
)

MODEL_ID = "scalar-field-v10-contact"


@dataclass(frozen=True, slots=True)
class CurrentFieldModel:
    """Replaceable scalar field and turning policy, composed once per simulation."""

    field: ScalarFieldRule
    turning: FieldTurning
    activity: ScalarActivity = value_changed_or_source
    movement: MovementRule = advance_movement

    def update_field(
        self, cell: CellState, neighbors: Neighbors, sources: int, config: Config
    ) -> CellState:
        sample = self.field.advance(
            ScalarSample(cell.phi, cell.remainder),
            neighbors,
            source=uniform_source(sources, config.source_strength),
            denominator=config.field_den,
        )
        validate_sample(sample, config.field_den)
        selected = nonnegative_sample(sample)
        return cell._replace(phi=selected.value, remainder=selected.remainder)

    def field_is_active(self, previous: CellState, current: CellState, sources: int) -> bool:
        return self.activity(
            ScalarSample(previous.phi, previous.remainder),
            ScalarSample(current.phi, current.remainder),
            sources,
        )

    def cancel_scalar_halo(self, cell: CellState) -> CellState:
        """Map the selected local halo policy back to the fixed cell record."""
        sample = cancel_scalar_sample(ScalarSample(cell.phi, cell.remainder))
        return cell._replace(phi=sample.value, remainder=sample.remainder)

    def update_particle(
        self, particle: ParticleState, cell: CellState, neighbors: Neighbors, config: Config, tick: int
    ) -> ParticleUpdate:
        raw_gradient = gradient(neighbors)
        response = self.turning.apply(
            particle.momentum,
            (cell.px, cell.py, cell.pz),
            raw_gradient,
            (particle.force_rx, particle.force_ry, particle.force_rz),
            numerator=config.force_num,
            denominator=config.force_den,
        )
        move = self.movement(
            response.momentum, particle.move_budget, particle.axis_phase, speed_cap=config.c_units
        )
        next_cell = cell._replace(
            px=response.field_momentum[0], py=response.field_momentum[1], pz=response.field_momentum[2]
        )
        next_particle = particle._replace(
            px=response.momentum[0],
            py=response.momentum[1],
            pz=response.momentum[2],
            force_rx=response.remainders[0],
            force_ry=response.remainders[1],
            force_rz=response.remainders[2],
            move_budget=move.budget,
            axis_phase=move.phase,
            last_update_tick=checked(tick),
        )
        validate_cell(next_cell)
        validate_particle(next_particle)
        return ParticleUpdate(next_particle, next_cell, move.direction, raw_gradient, response.impulse)


# Model choices are explicit here; generic primitives have no defaults for this model.
CURRENT_MODEL = CurrentFieldModel(
    field=ScalarField(neighbor_weights=(1, 1, 1, 1, 1, 1), self_weight=0),
    turning=FieldTurning(select_direction=dominant_axis_transverse),
    activity=value_changed_or_source,
)

# Preserve the former callable interface without duplicating physical formulas.
update_field = CURRENT_MODEL.update_field
update_particle = CURRENT_MODEL.update_particle
