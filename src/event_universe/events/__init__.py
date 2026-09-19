"""The law of events, the one engine (events-v1): selected by a world's
`"law": "events"` key; see docs/ENGINE.md. The engine (numpy) loads on first
use: importing the package, the world parser or the runner imports only
generic physics."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.events.world import EVENTS_LAW, EventWorld, is_event_world, parse_event_world

if TYPE_CHECKING:
    from event_universe.events.engine import EventSimulation, Measured

__all__ = [
    "EVENTS_LAW",
    "EventSimulation",
    "EventWorld",
    "Measured",
    "is_event_world",
    "parse_event_world",
]
_LAZY = {"Measured": ".engine", "EventSimulation": ".engine"}


def __getattr__(name: str) -> object:
    if name in _LAZY:
        from event_universe.events import engine

        return getattr(engine, name)
    raise AttributeError(name)
