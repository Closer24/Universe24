"""The engine's package (one engine, no law's name and no version, ALGEBRA.md
9.90 (1)): the world parser and the engine module `detector_law`. The lazy
exports of the ray law's engine (`Measured`, `NatureBeamSimulation` of
`engine.py`) are CANCELLED (docs/CANCELLED_WORLDS.md section 9)."""

from __future__ import annotations

from event_universe.loader.world import NatureBeamWorld, parse_world_document

# the engine's package imports no host module: the whole read of a world (its files
# and the stamp's digest) is `event_universe.world_files.parse_nature_beam_world`
__all__ = [
    "NatureBeamWorld",
    "parse_world_document",
]
_CANCELLED = {"Measured", "NatureBeamSimulation", "BEAM_LAW", "is_nature_beam_world"}


def __getattr__(name: str) -> object:
    if name in _CANCELLED:
        raise AttributeError(
            f"{name}: the ray law's engine and its name are cancelled (docs/CANCELLED_WORLDS.md)"
        )
    raise AttributeError(name)
