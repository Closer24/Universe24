"""The law of the ray, the one engine (rays-v1): selected by a world's
`"law": "rays"` key; see docs/RAY_LAW.md. The engine (numpy) loads on first
use: importing the package, the world parser or the preflight imports only
generic physics; the runner and `RaySimulation` load the engine."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.events.world import RAYS_LAW, RayWorld, is_ray_world, parse_ray_world

if TYPE_CHECKING:
    from event_universe.events.engine import Measured, RaySimulation

__all__ = [
    "RAYS_LAW",
    "Measured",
    "RaySimulation",
    "RayWorld",
    "is_ray_world",
    "parse_ray_world",
]
_LAZY = {"Measured": ".engine", "RaySimulation": ".engine"}


def __getattr__(name: str) -> object:
    if name in _LAZY:
        from event_universe.events import engine

        return getattr(engine, name)
    raise AttributeError(name)
