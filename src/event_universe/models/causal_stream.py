"""Opt-in causal outward-stream field candidate."""

from dataclasses import dataclass

from event_universe.core.state import Config
from event_universe.dynamics.movement import advance_movement
from event_universe.dynamics.turning import FieldTurning, full_response
from event_universe.fields.streaming import CausalOctantStream, attractive_samples
from event_universe.models.current_field import CURRENT_MODEL, CurrentFieldModel

MODEL_ID = "causal-octant-stream-v1"


@dataclass(frozen=True, slots=True)
class CausalStreamConfig:
    """Explicit candidate choices; source_per_octant is not a calibrated constant."""

    nx: int = 240
    ny: int = 240
    nz: int = 240
    c_units: int = 1000
    source_per_octant: int = 64
    force_num: int = 1
    force_den: int = 64
    max_particles_per_cell: int = 4

    def engine_config(self) -> Config:
        return Config(
            nx=self.nx,
            ny=self.ny,
            nz=self.nz,
            c_units=self.c_units,
            source_strength=0,
            field_den=1,
            force_num=self.force_num,
            force_den=self.force_den,
            max_particles_per_cell=self.max_particles_per_cell,
        )


STREAM_FIELD = CausalOctantStream()
STREAM_MODEL = CurrentFieldModel(
    field=CURRENT_MODEL.field,
    turning=FieldTurning(select_direction=full_response),
    activity=CURRENT_MODEL.activity,
    movement=advance_movement,
)
STREAM_SAMPLES = attractive_samples
