"""The law of the ray, the one engine (rays-v1): selected by a world's
`"law": "rays"` key; see docs/RAY_LAW.md. The engine (numpy) loads on first
use: importing the package, the world parser or the preflight imports only
generic physics; the runner and `NatureBeamSimulation` load the engine."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.events.world import (
    RAYS_LAW,
    NatureBeamWorld,
    is_nature_beam_world,
    parse_nature_beam_world,
)

if TYPE_CHECKING:
    from event_universe.events.engine import Measured, NatureBeamSimulation

__all__ = [
    "RAYS_LAW",
    "Measured",
    "NatureBeamSimulation",
    "NatureBeamWorld",
    "is_nature_beam_world",
    "parse_nature_beam_world",
]
_LAZY = {"Measured": ".engine", "NatureBeamSimulation": ".engine"}


def __getattr__(name: str) -> object:
    if name in _LAZY:
        from event_universe.events import engine

        return getattr(engine, name)
    raise AttributeError(name)
