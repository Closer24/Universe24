"""The law of the shadow, the field-only engine (field-only-v1): a mode beside
the old engine, selected by a world's `"law": "shadow"` key; see
docs/SPATIAL_FIELDS.md, "The law of the shadow (field-only-v1)"."""

from event_universe.shadow.engine import Holder, ShadowSimulation
from event_universe.shadow.world import SHADOW_LAW, ShadowWorld, is_shadow_world, parse_shadow_world

__all__ = [
    "SHADOW_LAW",
    "Holder",
    "ShadowSimulation",
    "ShadowWorld",
    "is_shadow_world",
    "parse_shadow_world",
]
