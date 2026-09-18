"""The law of the shadow, the field-only engine (field-only-v1): a mode beside
the old engine, selected by a world's `"law": "shadow"` key; see
docs/SPATIAL_FIELDS.md, "The law of the shadow (field-only-v1)". The engine
(numpy) loads on first use: importing the package, the schema or the runner
imports only generic physics."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.shadow.world import SHADOW_LAW, ShadowWorld, is_shadow_world, parse_shadow_world

if TYPE_CHECKING:
    from event_universe.shadow.engine import Holder, ShadowSimulation

__all__ = [
    "SHADOW_LAW",
    "Holder",
    "ShadowSimulation",
    "ShadowWorld",
    "is_shadow_world",
    "parse_shadow_world",
]
_LAZY = {"Holder": ".engine", "ShadowSimulation": ".engine"}


def __getattr__(name: str) -> object:
    if name in _LAZY:
        from event_universe.shadow import engine

        return getattr(engine, name)
    raise AttributeError(name)
