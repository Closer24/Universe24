"""Universe24: the engine of the Beam Law, defined by a world file.

The engine (numpy) loads on first use: importing the package imports the
world parser and the generic physics only; `NatureBeamSimulation` is resolved when
it is first read."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.events import BEAM_LAW, NatureBeamWorld, parse_nature_beam_world

if TYPE_CHECKING:
    from event_universe.events.engine import NatureBeamSimulation

__version__ = "0.3.1"
__all__ = [
    "BEAM_LAW",
    "NatureBeamSimulation",
    "NatureBeamWorld",
    "parse_nature_beam_world",
    "__version__",
]


def __getattr__(name: str) -> object:
    if name == "NatureBeamSimulation":
        from event_universe.events import engine

        return engine.NatureBeamSimulation
    raise AttributeError(name)
