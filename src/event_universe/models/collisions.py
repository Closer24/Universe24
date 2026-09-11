"""Choose classical elastic backscattering and map its fixed inputs and outputs."""

from event_universe.core.state import ParticleState
from event_universe.dynamics.collision import CollisionBody, elastic_backscatter

MODEL_ID = "scalar-field-v13-mass-elastic-contact"
LINKED_MODEL_ID = "scalar-field-v13-mass-elastic-local-links"


def collide(first: ParticleState, second: ParticleState) -> tuple[ParticleState, ParticleState]:
    result = elastic_backscatter(
        CollisionBody(first.momentum, first.mass, first.momentum_den),
        CollisionBody(second.momentum, second.mass, second.momentum_den),
    )
    return (
        first._replace(
            px=result.first.momentum[0],
            py=result.first.momentum[1],
            pz=result.first.momentum[2],
            momentum_den=result.first.denominator,
            axis_phase=0,
        ),
        second._replace(
            px=result.second.momentum[0],
            py=result.second.momentum[1],
            pz=result.second.momentum[2],
            momentum_den=result.second.denominator,
            axis_phase=0,
        ),
    )
