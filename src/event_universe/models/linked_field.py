"""Assembly for the independently identified local-link geometry hypothesis."""

from event_universe.core.links import LinkConfig
from event_universe.dynamics.transit import depart_movement
from event_universe.fields.geometry import MeanStretch
from event_universe.models.current_field import CURRENT_MODEL, CurrentFieldModel

MODEL_ID = "scalar-field-v11-local-links"
LINKED_MODEL = CurrentFieldModel(
    field=CURRENT_MODEL.field,
    turning=CURRENT_MODEL.turning,
    activity=CURRENT_MODEL.activity,
    movement=depart_movement,
)


def geometry_policy(config: LinkConfig) -> MeanStretch:
    return MeanStretch(config.base_length, config.stretch_num, config.stretch_den)
