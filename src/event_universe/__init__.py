"""Universe24: the engine of the law of events, defined by a world file."""

from event_universe.events import EVENTS_LAW, EventSimulation, EventWorld, parse_event_world

__version__ = "0.2.0"
__all__ = ["EVENTS_LAW", "EventSimulation", "EventWorld", "parse_event_world", "__version__"]
