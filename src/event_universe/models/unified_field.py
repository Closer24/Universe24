"""Explicit full-vector response candidate; arithmetic stays in dynamics/."""

from event_universe.dynamics.turning import FieldTurning, full_response

MODEL_ID = "scalar-field-unified-action-v1"
LINKED_MODEL_ID = "scalar-field-unified-action-links-v1"
UNIFIED_RESPONSE = FieldTurning(select_direction=full_response)
