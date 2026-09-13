"""The historical v10-contact scalar model: local source meaning, nonnegative field and response choices.

Reusable arithmetic lives in fields/ and dynamics/. This adapter alone maps
their records to the simulator's fixed node and particle state.
"""

from dataclasses import dataclass

from event_universe.core.contracts import ParticleUpdate
from event_universe.core.state import (
    Config,
    Neighbors,
    NodeState,
    ParticleState,
    checked,
    validate_node,
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
class ScalarFieldModel:
    """Replaceable scalar field and turning policy, composed once per simulation."""

    field: ScalarFieldRule
    turning: FieldTurning
    activity: ScalarActivity = value_changed_or_source
    movement: MovementRule = advance_movement

    def update_field(
        self, node: NodeState, neighbors: Neighbors, sources: int, config: Config
    ) -> NodeState:
        sample = self.field.advance(
            ScalarSample(node.phi, node.remainder),
            neighbors,
            source=uniform_source(sources, config.source_strength),
            denominator=config.field_den,
        )
        validate_sample(sample, config.field_den)
        selected = nonnegative_sample(sample)
        return node._replace(phi=selected.value, remainder=selected.remainder)

    def field_is_active(self, previous: NodeState, current: NodeState, sources: int) -> bool:
        return self.activity(
            ScalarSample(previous.phi, previous.remainder),
            ScalarSample(current.phi, current.remainder),
            sources,
        )

    def cancel_scalar_halo(self, node: NodeState) -> NodeState:
        """Map the selected local halo policy back to the fixed node record."""
        sample = cancel_scalar_sample(ScalarSample(node.phi, node.remainder))
        return node._replace(phi=sample.value, remainder=sample.remainder)

    def update_particle(
        self, particle: ParticleState, node: NodeState, neighbors: Neighbors, config: Config, tick: int
    ) -> ParticleUpdate:
        raw_gradient = gradient(neighbors)
        response = self.turning.apply(
            particle.momentum,
            (node.px, node.py, node.pz),
            raw_gradient,
            (particle.force_rx, particle.force_ry, particle.force_rz),
            numerator=config.force_num,
            denominator=config.force_den,
            momentum_den=particle.momentum_den,
        )
        move = self.movement(
            response.momentum,
            particle.move_budget,
            particle.axis_phase,
            speed_cap=config.c_units,
            mass=particle.mass,
            momentum_den=particle.momentum_den,
            budget_den=particle.move_budget_den,
        )
        next_node = node._replace(
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
            move_budget_den=move.budget_den,
            axis_phase=move.phase,
            last_update_tick=checked(tick),
        )
        validate_node(next_node)
        validate_particle(next_particle)
        return ParticleUpdate(next_particle, next_node, move.direction, raw_gradient, response.impulse)


# Model choices are explicit here; generic primitives have no defaults for this model.
SCALAR_MODEL = ScalarFieldModel(
    field=ScalarField(neighbor_weights=(1, 1, 1, 1, 1, 1), self_weight=0),
    turning=FieldTurning(select_direction=dominant_axis_transverse),
    activity=value_changed_or_source,
)

# Preserve the former callable interface without duplicating physical formulas.
update_field = SCALAR_MODEL.update_field
update_particle = SCALAR_MODEL.update_particle
