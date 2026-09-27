"""Universe24: the one engine, defined by a world file, a universe file and a
start file (no law's name and no version, ALGEBRA.md #the-primitives).

Importing the package imports the world parser only; the engine module
`event_universe.events.detector_law` loads numpy on its own import. The lazy
export of the ray law's `NatureBeamSimulation` is CANCELLED
(docs/CANCELLED_WORLDS.md section 9)."""

from __future__ import annotations

from event_universe.events import NatureBeamWorld
from event_universe.world_files import parse_nature_beam_world

__version__ = "0.3.1"
__all__ = [
    "NatureBeamWorld",
    "parse_nature_beam_world",
    "__version__",
]


def __getattr__(name: str) -> object:
    if name in {"NatureBeamSimulation", "BEAM_LAW"}:
        raise AttributeError(
            f"{name}: the ray law's engine and its name are cancelled (docs/CANCELLED_WORLDS.md)"
        )
    raise AttributeError(name)
