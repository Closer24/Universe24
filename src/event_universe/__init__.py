"""Universe24: the engine of the law of the ray, defined by a world file.

The engine (numpy) loads on first use: importing the package imports the
world parser and the generic physics only; `RaySimulation` is resolved when
it is first read."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.events import RAYS_LAW, RayWorld, parse_ray_world

if TYPE_CHECKING:
    from event_universe.events.engine import RaySimulation

__version__ = "0.3.1"
__all__ = ["RAYS_LAW", "RaySimulation", "RayWorld", "parse_ray_world", "__version__"]


def __getattr__(name: str) -> object:
    if name == "RaySimulation":
        from event_universe.events import engine

        return engine.RaySimulation
    raise AttributeError(name)
