"""Opt-in shared INTERACTION action; no copied generic arithmetic or world access."""

from dataclasses import dataclass

from event_universe.core.state import Config
from event_universe.dynamics.transit import depart_movement
from event_universe.dynamics.turning import FieldTurning, full_response
from event_universe.fields.interaction import ScalarInteraction
from event_universe.fields.policies import sample_changed_or_source
from event_universe.models.current_field import CURRENT_MODEL, CurrentFieldModel

MODEL_ID = "scalar-field-v12-shared-interaction"


@dataclass(frozen=True, slots=True)
class SharedActionConfig:
    """All numerical choices exposed; none is a fitted physical constant.

    coupling controls BOTH source and response. impulse_units is the impulse
    scale; 2048 gives 64/(2*2048)=1/64 at the default g. c_units is inherited
    digital transit scaling, NOT isotropic Euclidean c. field_den=7 retains
    screened relaxation. K remains a fixed local occupancy capacity.
    """

    nx: int = 64
    ny: int = 48
    nz: int = 32
    c_units: int = 12
    coupling: int = 64
    impulse_units: int = 2048
    field_den: int = 7
    max_particles_per_cell: int = 4

    def __post_init__(self) -> None:
        self.engine_config()
        if min(self.nx, self.ny, self.nz) < 3:
            raise ValueError("opposite neighbors must be distinct")
        if self.field_den < 7:
            raise ValueError("this candidate retains screened relaxation: field_den >= 7")

    def engine_config(self) -> Config:
        interaction = ScalarInteraction(self.coupling)
        return Config(
            nx=self.nx,
            ny=self.ny,
            nz=self.nz,
            c_units=self.c_units,
            source_strength=interaction.coupling,
            field_den=self.field_den,
            force_num=1,
            force_den=interaction.response_denominator(self.impulse_units),
            max_particles_per_cell=self.max_particles_per_cell,
        )


def shared_action_model(settings: SharedActionConfig) -> CurrentFieldModel:
    """Bind both variations to the SAME immutable interaction term."""
    interaction = ScalarInteraction(settings.coupling)
    return CurrentFieldModel(
        field=CURRENT_MODEL.field,
        turning=FieldTurning(select_direction=full_response),
        activity=sample_changed_or_source,
        movement=depart_movement,
        source=interaction.source,
        field_vector=interaction.force_numerator,
    )
