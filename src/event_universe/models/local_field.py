"""Compatibility imports. New consumers use scalar_field, fields and dynamics."""

from event_universe.dynamics.movement import choose_axis
from event_universe.dynamics.turning import dominant_axis_transverse as transverse_gradient
from event_universe.fields.scalar import gradient

from .scalar_field import MODEL_ID, update_field, update_particle

__all__ = [
    "MODEL_ID",
    "choose_axis",
    "gradient",
    "transverse_gradient",
    "update_field",
    "update_particle",
]
